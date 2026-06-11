"""
LEDO.ai - 인메모리 Message Broker 구현

용도: 개발 + 테스트
프로덕션: RedisStreamsBroker / KafkaBroker 사용

특징:
─────────────────────────────────────
- 프로세스 내부만 작동 (재시작 시 손실)
- asyncio.Queue 기반 (비동기 큐)
- 백그라운드 디스패처 태스크
- 동시성 안전 (asyncio.Lock)

⚠️ 운영 환경에서 사용 X:
   - 분산 시스템 아님 (1 프로세스만)
   - 메시지 영구 저장 X
   - 사용 시 경고 로그
"""
import asyncio
from datetime import datetime, timezone
from typing import Optional, Any
import logging

from agents.brokers.interface import (
    MessageBroker,
    Message,
    Subscription,
    MessageHandler,
    BrokerError,
)


logger = logging.getLogger(__name__)


class InMemoryBroker(MessageBroker):
    """인메모리 Pub/Sub 브로커

    개발 + 테스트 전용.
    프로덕션 환경에선 RedisStreamsBroker 사용.

    내부 구조:
    ─────────────────────────────────────
    _subscriptions:  {sub_id: Subscription}
    _handlers:       {sub_id: MessageHandler}
    _message_queue:  asyncio.Queue (발행된 메시지)
    _dispatcher_task: 백그라운드 디스패처
    _lock:           동시성 보호
    _stats:          통계 카운터
    """

    def __init__(self, queue_size: int = 10000) -> None:
        """인메모리 브로커 초기화

        Args:
            queue_size: 메시지 큐 최대 크기 (backpressure)
                10000 = 10K 메시지 대기 가능
                초과 시 publish 가 대기 (자연스러운 throttling)
        """
        # 구독 저장소
        self._subscriptions: dict[str, Subscription] = {}
        self._handlers: dict[str, MessageHandler] = {}

        # 메시지 큐 (asyncio.Queue - 비동기 안전)
        self._message_queue: asyncio.Queue[Message] = asyncio.Queue(
            maxsize=queue_size
        )

        # 백그라운드 디스패처 태스크
        self._dispatcher_task: Optional[asyncio.Task] = None
        self._running: bool = False

        # 동시성 보호
        self._lock: asyncio.Lock = asyncio.Lock()

        # 통계
        self._stats: dict[str, int] = {
            "total_published": 0,
            "total_delivered": 0,
            "total_failed_delivery": 0,
            "total_expired": 0,
        }
        self._topics_seen: set[str] = set()

        logger.warning(
            "InMemoryBroker 사용 중 - 개발/테스트 전용 (프로덕션 X)"
        )

    # ════════════════════════════════════════
    # 라이프사이클
    # ════════════════════════════════════════

    async def start(self) -> None:
        """브로커 시작 (백그라운드 디스패처 활성화)"""
        if self._running:
            logger.warning("이미 실행 중")
            return

        self._running = True

        # 백그라운드 디스패처 태스크 생성
        self._dispatcher_task = asyncio.create_task(
            self._dispatch_loop()
        )

        logger.info("InMemoryBroker 시작됨")

    async def stop(self) -> None:
        """브로커 종료 (디스패처 정지 + 구독 해제)"""
        if not self._running:
            return

        self._running = False

        # 디스패처 태스크 취소
        if self._dispatcher_task is not None:
            self._dispatcher_task.cancel()
            try:
                await self._dispatcher_task
            except asyncio.CancelledError:
                pass
            self._dispatcher_task = None

        # 모든 구독 해제
        async with self._lock:
            self._subscriptions.clear()
            self._handlers.clear()

        logger.info("InMemoryBroker 종료됨")

    # ════════════════════════════════════════
    # 발행 (Publish)
    # ════════════════════════════════════════

    async def publish(self, message: Message) -> None:
        """메시지 발행 (큐에 추가)

        ⚠️ 큐 가득 시 대기 (backpressure):
           메시지 손실 방지
           시스템 안전성 확보
        """
        if not self._running:
            raise BrokerError(
                "Broker 가 시작되지 않음. start() 호출 필요"
            )

        # 만료 검증
        if message.expires_at is not None:
            now = datetime.now(timezone.utc)
            if now > message.expires_at:
                async with self._lock:
                    self._stats["total_expired"] += 1
                logger.debug(
                    f"만료된 메시지 폐기: topic={message.topic}"
                )
                return

        # 큐에 추가 (가득하면 대기)
        await self._message_queue.put(message)

        async with self._lock:
            self._stats["total_published"] += 1
            self._topics_seen.add(message.topic)

        logger.debug(
            f"발행: topic={message.topic}, "
            f"publisher={message.publisher_id}"
        )

    async def publish_batch(self, messages: list[Message]) -> None:
        """배치 발행"""
        for msg in messages:
            await self.publish(msg)

    # ════════════════════════════════════════
    # 구독 (Subscribe)
    # ════════════════════════════════════════

    async def subscribe(
        self,
        topic_pattern: str,
        handler: MessageHandler,
        subscriber_id: str,
    ) -> Subscription:
        """구독 등록"""
        # 패턴 검증 (대충: 빈 문자열 차단)
        if not topic_pattern or not topic_pattern.strip():
            raise ValueError("topic_pattern 비어있음")

        subscription = Subscription(
            topic_pattern=topic_pattern,
            subscriber_id=subscriber_id,
        )

        async with self._lock:
            self._subscriptions[subscription.subscription_id] = subscription
            self._handlers[subscription.subscription_id] = handler

        logger.info(
            f"구독 등록: pattern={topic_pattern}, "
            f"subscriber={subscriber_id}, "
            f"sub_id={subscription.subscription_id[:8]}..."
        )

        return subscription

    async def unsubscribe(self, subscription_id: str) -> bool:
        """구독 해제"""
        async with self._lock:
            if subscription_id in self._subscriptions:
                del self._subscriptions[subscription_id]
                del self._handlers[subscription_id]
                logger.info(f"구독 해제: {subscription_id[:8]}...")
                return True
            return False

    # ════════════════════════════════════════
    # 백그라운드 디스패처
    # ════════════════════════════════════════

    async def _dispatch_loop(self) -> None:
        """메시지 큐에서 가져와 매칭 구독자에게 전달

        ⭐ 핵심 로직:
           1. 큐에서 메시지 꺼냄
           2. 모든 구독자 검색
           3. 토픽 매칭되는 구독자에게만 전달
           4. 핸들러 비동기 호출 (Fail-Safe)
        """
        logger.debug("디스패처 루프 시작")

        while self._running:
            try:
                # 큐에서 메시지 가져오기 (블로킹)
                message = await asyncio.wait_for(
                    self._message_queue.get(),
                    timeout=1.0,
                )

                # 매칭 구독자 찾기
                await self._dispatch_message(message)

            except asyncio.TimeoutError:
                # 타임아웃은 정상 (큐 비어있음)
                continue
            except asyncio.CancelledError:
                # 종료 신호
                logger.debug("디스패처 취소됨")
                break
            except Exception as e:
                # 기타 예외 (디스패처 자체는 계속)
                logger.error(f"디스패처 에러: {e}")

        logger.debug("디스패처 루프 종료")

    async def _dispatch_message(self, message: Message) -> None:
        """단일 메시지 디스패치

        매칭되는 모든 구독자에게 동시 전달.
        한 핸들러 실패 = 다른 핸들러 계속 (Fail-Safe).
        """
        # 매칭 구독자 찾기
        async with self._lock:
            matching = [
                (sub_id, sub, self._handlers[sub_id])
                for sub_id, sub in self._subscriptions.items()
                if MessageBroker.matches_pattern(
                    message.topic, sub.topic_pattern
                )
            ]

        if not matching:
            logger.debug(
                f"매칭 구독자 없음: topic={message.topic}"
            )
            return

        # 모든 매칭 핸들러 동시 호출 (asyncio.gather)
        tasks = [
            self._safe_handler_call(handler, message, sub_id)
            for sub_id, _, handler in matching
        ]
        await asyncio.gather(*tasks, return_exceptions=True)

    async def _safe_handler_call(
        self,
        handler: MessageHandler,
        message: Message,
        sub_id: str,
    ) -> None:
        """핸들러 안전 호출 (예외 → 로그만)

        한 구독자의 핸들러 실패 = 다른 구독자 영향 X
        Fail-Safe 원칙
        """
        try:
            await handler(message)
            async with self._lock:
                self._stats["total_delivered"] += 1
        except Exception as e:
            async with self._lock:
                self._stats["total_failed_delivery"] += 1
            logger.error(
                f"핸들러 실패: sub_id={sub_id[:8]}..., "
                f"topic={message.topic}, "
                f"error={type(e).__name__}: {e}"
            )

    # ════════════════════════════════════════
    # 관측 가능성
    # ════════════════════════════════════════

    async def list_subscriptions(
        self,
        subscriber_id: Optional[str] = None,
    ) -> list[Subscription]:
        """활성 구독 목록"""
        async with self._lock:
            if subscriber_id is None:
                return list(self._subscriptions.values())
            return [
                sub for sub in self._subscriptions.values()
                if sub.subscriber_id == subscriber_id
            ]

    async def get_stats(self) -> dict[str, Any]:
        """브로커 통계"""
        async with self._lock:
            return {
                **self._stats,
                "active_subscriptions": len(self._subscriptions),
                "topics_seen": len(self._topics_seen),
                "queue_size": self._message_queue.qsize(),
                "queue_max_size": self._message_queue.maxsize,
            }

    async def health_check(self) -> dict[str, Any]:
        """헬스 체크"""
        start = datetime.now(timezone.utc)

        async with self._lock:
            sub_count = len(self._subscriptions)
            queue_size = self._message_queue.qsize()
            queue_max = self._message_queue.maxsize

        latency_ms = int(
            (datetime.now(timezone.utc) - start).total_seconds() * 1000
        )

        # queue 가 80% 이상 차있으면 degraded
        queue_usage = queue_size / queue_max if queue_max > 0 else 0
        status = "healthy"
        if queue_usage > 0.8:
            status = "degraded"
        if not self._running:
            status = "unhealthy"

        return {
            "status": status,
            "backend": "in_memory",
            "latency_ms": latency_ms,
            "running": self._running,
            "active_subscriptions": sub_count,
            "queue_size": queue_size,
            "queue_usage_percent": round(queue_usage * 100, 1),
            "warning": "in-memory backend - data lost on restart",
        }
    
    