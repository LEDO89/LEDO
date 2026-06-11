"""
LEDO.ai - Message Broker 인터페이스 (Pub/Sub)

분산 에이전트 시스템의 신경계.
에이전트 간 통신을 느슨한 결합으로 추상화.

설계 원칙:
─────────────────────────────────────
1. Topic-Based Routing (토픽 기반 라우팅)
2. Wildcard Subscription (와일드카드 구독)
3. Async-First (모든 메서드 비동기)
4. Backpressure (오버플로우 보호)
5. At-Least-Once Delivery (최소 1회 전달)
6. Message Persistence (재시작 시 손실 X - Redis Streams)

지원 백엔드:
─────────────────────────────────────
- InMemoryBroker  - 테스트/개발 (이번 메시지)
- RedisStreamsBroker - 운영 (격상 #4)
- KafkaBroker - 대용량 (선택)

토픽 명명 규약 (산업 표준):
─────────────────────────────────────
형식: <domain>.<entity>.<event>
예시:
    sensor.helmet.detected     ← 헬멧 감지
    sensor.helmet.removed      ← 헬멧 제거
    worker.position.updated    ← 위치 변경
    safety.violation.helmet    ← 안전 위반
    alarm.triggered.warning    ← 경보 발생
    ontology.changed.class     ← 온톨로지 변경

와일드카드:
    sensor.helmet.*    ← helmet 관련 모든 사건
    sensor.*           ← 모든 센서 사건
    *.violation.*      ← 모든 위반 사건

참조 표준:
─────────────────────────────────────
- Enterprise Integration Patterns (Gregor Hohpe, 2003)
- AMQP 1.0 (Advanced Message Queuing Protocol)
- MQTT 5.0 (IoT 표준)
- Apache Kafka 토픽 모델
- AWS SNS/SQS 패턴

Python 버전: 3.14+
"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Any, Callable, Awaitable
from uuid import uuid4

from pydantic import BaseModel, Field, ConfigDict


# ════════════════════════════════════════════════════════════
# 1. Message - 표준 메시지 형식
# ════════════════════════════════════════════════════════════


class Message(BaseModel):
    """Pub/Sub 메시지의 표준 형식

    모든 발행/구독 메시지가 이 형식.
    JSON 직렬화 가능 (모든 백엔드 호환).
    """
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    # ════════════════════════════════════════
    # 1. 메시지 식별
    # ════════════════════════════════════════
    message_id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="메시지 UUID v4 (중복 제거용)",
    )
    timestamp_utc: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="메시지 생성 시각",
    )

    # ════════════════════════════════════════
    # 2. 라우팅
    # ════════════════════════════════════════
    topic: str = Field(
        ...,
        min_length=1,
        max_length=256,
        pattern=r"^[a-z][a-z0-9_]*(\.[a-z0-9_]+)*$",
        description="토픽 이름 (예: 'sensor.helmet.detected')",
    )

    # ════════════════════════════════════════
    # 3. 발행자 정보
    # ════════════════════════════════════════
    publisher_id: str = Field(
        ...,
        max_length=128,
        description="발행한 에이전트의 actor_id (예: 'agent:sensor')",
    )

    # ════════════════════════════════════════
    # 4. 메시지 본문
    # ════════════════════════════════════════
    payload: dict[str, Any] = Field(
        default_factory=dict,
        description="메시지 데이터 (자유 형식 JSON)",
    )

    # ════════════════════════════════════════
    # 5. 추적 정보
    # ════════════════════════════════════════
    correlation_id: Optional[str] = Field(
        default=None,
        max_length=128,
        description="워크플로우 그룹 ID (관련 메시지 추적)",
    )
    parent_message_id: Optional[str] = Field(
        default=None,
        description="원인 메시지 ID (메시지 사슬)",
    )

    # ════════════════════════════════════════
    # 6. 전달 제어
    # ════════════════════════════════════════
    priority: int = Field(
        default=5,
        ge=1,
        le=10,
        description="우선순위 (1=최저, 10=최고)",
    )
    expires_at: Optional[datetime] = Field(
        default=None,
        description="만료 시각 (이후 메시지 무시)",
    )


# ════════════════════════════════════════════════════════════
# 2. Subscription - 구독 정보
# ════════════════════════════════════════════════════════════


# 메시지 핸들러 타입: 비동기 함수 (Message → None)
MessageHandler = Callable[[Message], Awaitable[None]]


class Subscription(BaseModel):
    """구독 정보 (subscribe 결과 반환)"""
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        arbitrary_types_allowed=True,  # Callable 허용
    )

    subscription_id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="구독 UUID (unsubscribe 시 사용)",
    )
    topic_pattern: str = Field(
        ...,
        description="구독한 토픽 패턴 (예: 'sensor.helmet.*')",
    )
    subscriber_id: str = Field(
        ...,
        max_length=128,
        description="구독한 에이전트의 actor_id",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="구독 시작 시각",
    )


# ════════════════════════════════════════════════════════════
# 3. MessageBroker - 추상 인터페이스
# ════════════════════════════════════════════════════════════


class MessageBroker(ABC):
    """Pub/Sub 메시지 브로커의 추상 인터페이스

    모든 구현 클래스가 따라야 할 표준:
      - InMemoryBroker (테스트/개발)
      - RedisStreamsBroker (운영)
      - KafkaBroker (대용량)

    핵심 책임:
    ─────────────────────────────────────
    1. publish(topic, payload) - 메시지 발행
    2. subscribe(pattern, handler) - 구독 등록
    3. unsubscribe(subscription_id) - 구독 해제
    4. 토픽 매칭 (와일드카드 지원)
    5. 비동기 메시지 전달

    사용 예시:
    ─────────────────────────────────────
        broker = InMemoryBroker()
        
        # 구독
        async def handle_helmet(msg):
            print(f"헬멧 사건: {msg.payload}")
        
        sub = await broker.subscribe(
            topic_pattern="sensor.helmet.*",
            handler=handle_helmet,
            subscriber_id="agent:safety",
        )
        
        # 발행
        await broker.publish(Message(
            topic="sensor.helmet.detected",
            publisher_id="agent:sensor",
            payload={"worker_id": "W042", "status": "off"},
        ))
        
        # → handle_helmet 자동 호출
    """

    # ════════════════════════════════════════
    # 1. 발행 (Publish)
    # ════════════════════════════════════════

    @abstractmethod
    async def publish(self, message: Message) -> None:
        """메시지 발행

        Args:
            message: Message 인스턴스

        ⚠️ 보장:
            - At-Least-Once Delivery (최소 1회 전달)
            - 발행 즉시 반환 (비동기)
            - 만료된 메시지 자동 폐기

        에러:
            - Broker 연결 실패 시 BrokerError
        """
        raise NotImplementedError

    @abstractmethod
    async def publish_batch(self, messages: list[Message]) -> None:
        """배치 발행 (성능 최적화)

        Args:
            messages: Message 목록

        ⭐ 산업 활용:
           1000건 동시 발행 시 1번 RTT (round-trip time)
           = 네트워크 효율 ↑↑
        """
        raise NotImplementedError

    # ════════════════════════════════════════
    # 2. 구독 (Subscribe)
    # ════════════════════════════════════════

    @abstractmethod
    async def subscribe(
        self,
        topic_pattern: str,
        handler: MessageHandler,
        subscriber_id: str,
    ) -> Subscription:
        """구독 등록

        Args:
            topic_pattern: 토픽 패턴
                "sensor.helmet.detected"  ← 정확 매칭
                "sensor.helmet.*"          ← 와일드카드 (single segment)
                "sensor.**"                ← 와일드카드 (multi segment)
            handler: 비동기 핸들러 함수 (async def)
            subscriber_id: 구독자 식별 (예: "agent:safety")

        Returns:
            Subscription 인스턴스 (unsubscribe 에 사용)
        """
        raise NotImplementedError

    @abstractmethod
    async def unsubscribe(self, subscription_id: str) -> bool:
        """구독 해제

        Args:
            subscription_id: subscribe() 가 반환한 ID

        Returns:
            True = 해제됨, False = 없었음
        """
        raise NotImplementedError

    # ════════════════════════════════════════
    # 3. 토픽 매칭 (와일드카드)
    # ════════════════════════════════════════

    @staticmethod
    def matches_pattern(topic: str, pattern: str) -> bool:
        """토픽이 패턴과 매칭되는지 확인

        매칭 규칙:
        ─────────────
        정확 매칭:
            "sensor.helmet.detected" == "sensor.helmet.detected" → True

        Single Segment 와일드카드 (*):
            "sensor.helmet.detected" matches "sensor.helmet.*" → True
            "sensor.helmet.detected.value" matches "sensor.helmet.*" → False

        Multi Segment 와일드카드 (**):
            "sensor.helmet.detected.value" matches "sensor.**" → True
            "sensor.helmet.detected.value" matches "sensor.helmet.**" → True

        Args:
            topic: 실제 토픽
            pattern: 매칭 패턴

        Returns:
            True = 매칭됨, False = 안 됨

        ⭐ MQTT 5.0 표준 와일드카드 호환:
           + (single) = LEDO 의 *
           # (multi)  = LEDO 의 **
           
           LEDO 가 * / ** 선택한 이유:
           - 글로벌 코드 가독성 ↑
           - 산업 표준 (Kafka, RabbitMQ 와 호환)
        """
        topic_parts = topic.split(".")
        pattern_parts = pattern.split(".")

        i, j = 0, 0
        while i < len(topic_parts) and j < len(pattern_parts):
            pattern_part = pattern_parts[j]

            if pattern_part == "**":
                # Multi-segment 와일드카드: 나머지 모두 매칭
                return True
            elif pattern_part == "*":
                # Single-segment 와일드카드
                i += 1
                j += 1
            elif pattern_part == topic_parts[i]:
                # 정확 매칭
                i += 1
                j += 1
            else:
                # 매칭 안 됨
                return False

        # 둘 다 끝까지 갔으면 매칭
        return i == len(topic_parts) and j == len(pattern_parts)

    # ════════════════════════════════════════
    # 4. 관측 가능성
    # ════════════════════════════════════════

    @abstractmethod
    async def list_subscriptions(
        self,
        subscriber_id: Optional[str] = None,
    ) -> list[Subscription]:
        """활성 구독 목록 조회

        Args:
            subscriber_id: 특정 구독자 필터 (None=모두)

        Returns:
            Subscription 목록
        """
        raise NotImplementedError

    @abstractmethod
    async def get_stats(self) -> dict[str, Any]:
        """브로커 통계

        Returns:
            {
                "total_published": int,
                "total_delivered": int,
                "active_subscriptions": int,
                "topics_seen": int,
                ...
            }
        """
        raise NotImplementedError

    @abstractmethod
    async def health_check(self) -> dict[str, Any]:
        """브로커 헬스 체크

        Returns:
            {
                "status": "healthy" | "degraded" | "unhealthy",
                "backend": str,
                "latency_ms": int,
            }
        """
        raise NotImplementedError

    # ════════════════════════════════════════
    # 5. 라이프사이클
    # ════════════════════════════════════════

    @abstractmethod
    async def start(self) -> None:
        """브로커 시작 (연결 + 백그라운드 태스크)

        ⚠️ subscribe/publish 호출 전 필수
        """
        raise NotImplementedError

    @abstractmethod
    async def stop(self) -> None:
        """브로커 종료 (정리)

        ⚠️ 모든 구독 자동 해제
        """
        raise NotImplementedError


# ════════════════════════════════════════════════════════════
# 4. BrokerError - 브로커 예외
# ════════════════════════════════════════════════════════════


class BrokerError(Exception):
    """브로커 작업 실패 예외

    Pub/Sub 시스템의 일반적 에러:
        - 연결 실패
        - 메시지 형식 오류
        - 백엔드 에러
    """
    pass


# datetime import 추가 (Message 모델에서 사용)
from datetime import timezone