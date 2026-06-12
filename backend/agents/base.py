"""
LEDO.ai - BaseAgent 추상 클래스 (분산 시스템 완성판)

수백 개 에이전트 + LoRA + 휴머노이드 시스템의 진짜 토대.
4개 격상 모두 통합된 산업 표준 분산 시스템 아키텍처.

격상 단계:
─────────────────────────────────────
✅ 격상 #1: asyncio 비동기 (수천 동시 작동)
✅ 격상 #2: Repository Pattern (외부 상태 - Stateless)
✅ 격상 #3: Pub/Sub Message Broker (느슨한 결합 통신)
✅ 격상 #4: 통합 + 자동 발행/구독 ⭐ 완성

이 파일의 책임:
─────────────────────────────────────
- async/await 라이프사이클
- asyncio.Lock + Event (동시성)
- 비동기 컨텍스트 매니저 (async with)
- Repository 의존성 주입 (Stateless)
- Broker 의존성 주입 (Pub/Sub)
- 자동 라이프사이클 이벤트 발행
- 자동 결과 이벤트 발행
- 토픽 구독 헬퍼
- LoRA / Fine-tuning 메타데이터

분산 시스템 표준:
─────────────────────────────────────
- 12-Factor App #6 (Stateless Processes)
- 12-Factor App #11 (Logs as Event Streams)
- Hexagonal Architecture (Ports & Adapters)
- Domain-Driven Design (Eric Evans)
- Reactive Manifesto (Responsive, Resilient, Elastic, Message-driven)

Python 버전: 3.14+
"""
import asyncio
from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime, timezone
from typing import Optional, Any
from uuid import uuid4
import logging

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)

from config import settings
from ontology.classes import AccessLevel
from ontology.audit import (
    audit,
    AuditEvent,
    AuditEventType,
    AuditOutcome,
    AuditSeverity,
)

# ⭐ 격상 #2: Repository Pattern
from agents.repositories.interface import AgentStateRepository
from agents.repositories.memory_repo import InMemoryAgentStateRepository

# ⭐ 격상 #3 + #4: Message Broker (Pub/Sub)
from agents.brokers.interface import (
    MessageBroker,
    Message,
    MessageHandler,
    Subscription,
)
from agents.brokers.memory_broker import InMemoryBroker


logger = logging.getLogger(__name__)


# ════════════════════════════════════════════════════════════
# 1. AgentState - 8단계 라이프사이클 상태
# ════════════════════════════════════════════════════════════


class AgentState(str, Enum):
    """에이전트의 라이프사이클 상태 (분산 시스템 표준)

    Kubernetes Pod Phase 와 호환.
    """
    UNINITIALIZED = "uninitialized"
    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    IDLE = "idle"
    ERROR = "error"
    SHUTTING_DOWN = "shutting_down"
    TERMINATED = "terminated"


# ════════════════════════════════════════════════════════════
# 2. AgentMetadata - 식별자 + 운영 메타정보
# ════════════════════════════════════════════════════════════


class AgentMetadata(BaseModel):
    """에이전트 인스턴스의 메타정보 (Repository 영구 저장 가능)"""
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        str_strip_whitespace=True,
        frozen=False,
    )

    # 식별
    agent_id: str = Field(
        default_factory=lambda: str(uuid4()),
        pattern=r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$",
        description="UUID v4 (분산 unique)",
    )
    agent_name: str = Field(
        ...,
        min_length=1,
        max_length=64,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="snake_case 이름",
    )
    agent_class: str = Field(
        ...,
        min_length=1,
        max_length=64,
        pattern=r"^[A-Z][a-zA-Z0-9]*$",
        description="PascalCase 클래스명",
    )
    version: str = Field(
        default="1.0.0",
        pattern=r"^\d+\.\d+\.\d+$",
        description="SemVer 버전",
    )

    # 운영 정보
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="인스턴스 생성 시각 (UTC)",
    )
    environment: str = Field(
        default_factory=lambda: settings.LEDO_ENV,
        max_length=32,
    )
    host_node: Optional[str] = Field(
        default=None,
        max_length=128,
    )

    # 권한
    access_level: AccessLevel = Field(default=AccessLevel.INTERNAL)
    can_modify_ontology: bool = Field(default=False)

    # LoRA / Fine-tuning
    base_model_id: str = Field(
        default_factory=lambda: settings.OLLAMA_MODEL,
        max_length=128,
    )
    lora_adapter_id: Optional[str] = Field(default=None, max_length=128)
    fine_tuned_model_id: Optional[str] = Field(default=None, max_length=128)

    @property
    def actor_id(self) -> str:
        """audit.py 의 actor 형식 (예: 'agent:safety')"""
        return f"agent:{self.agent_name}"

    @property
    def is_specialized(self) -> bool:
        return (
            self.lora_adapter_id is not None
            or self.fine_tuned_model_id is not None
        )


# ════════════════════════════════════════════════════════════
# 3. AgentResult - 작업 결과 표준 형식
# ════════════════════════════════════════════════════════════


class AgentResult(BaseModel):
    """에이전트 작업의 표준 결과 (Immutable)"""
    model_config = ConfigDict(extra="forbid", frozen=True)

    result_id: str = Field(default_factory=lambda: str(uuid4()))
    agent_id: str = Field(...)
    timestamp_utc: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    outcome: AuditOutcome = Field(...)
    output: dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = Field(default=None, max_length=2048)
    duration_ms: int = Field(default=0, ge=0)
    llm_tokens_used: int = Field(default=0, ge=0)
    audit_event_id: Optional[str] = Field(default=None)
    correlation_id: Optional[str] = Field(default=None, max_length=128)


# ════════════════════════════════════════════════════════════
# 4. BaseAgent - 완성판 (4개 격상 통합)
# ════════════════════════════════════════════════════════════


class BaseAgent(ABC):
    """모든 LEDO 에이전트의 비동기 + Stateless + Pub/Sub 추상 부모

    4개 격상 통합:
    ─────────────────────────────────────
    1. asyncio 비동기 라이프사이클
    2. Repository (외부 상태)
    3. Broker (Pub/Sub 통신)
    4. 자동 발행/구독 통합

    자동 발행 토픽 (Lifecycle Events):
    ─────────────────────────────────────
    agent.<name>.initialized    - 초기화 완료
    agent.<name>.shutdown       - 종료
    agent.<name>.error          - 에러 발생
    agent.<name>.result.success - 작업 성공
    agent.<name>.result.failure - 작업 실패

    사용 예시 (분산 환경):
    ─────────────────────────────────────
        # 공유 인프라
        pg_repo = PostgresAgentRepository(...)
        redis_broker = RedisStreamsBroker(...)
        await redis_broker.start()

        # SafetyAgent (헬멧 감지 받음)
        class SafetyAgent(BaseAgent):
            async def _on_initialize(self):
                await self.subscribe(
                    "sensor.helmet.*",
                    self._handle_helmet,
                )

            async def _handle_helmet(self, msg):
                # 헬멧 사건 처리
                ...

            async def process(self, input_data):
                ...

        async with SafetyAgent(
            agent_name="safety",
            agent_class="SafetyAgent",
            lora_adapter_id="construction_v3",
            repository=pg_repo,
            broker=redis_broker,
        ) as agent:
            # 자동으로 "agent.safety.initialized" 발행됨
            # 자동으로 "sensor.helmet.*" 구독됨
            result = await agent.run({...})
    """

    def __init__(
        self,
        agent_name: str,
        agent_class: str,
        version: str = "1.0.0",
        access_level: AccessLevel = AccessLevel.INTERNAL,
        can_modify_ontology: bool = False,
        lora_adapter_id: Optional[str] = None,
        fine_tuned_model_id: Optional[str] = None,
        repository: Optional[AgentStateRepository] = None,
        broker: Optional[MessageBroker] = None,
    ) -> None:
        """BaseAgent 초기화

        Args:
            agent_name: snake_case
            agent_class: PascalCase
            version: SemVer
            access_level: 권한
            can_modify_ontology: 온톨로지 변경 권한
            lora_adapter_id: LoRA 어댑터
            fine_tuned_model_id: Fine-tuned 모델
            repository: 상태 저장소 (기본: InMemory)
            broker: 메시지 브로커 (기본: InMemory)
                ⭐ 격상 #4: Pub/Sub 통합
                프로덕션: RedisStreamsBroker 주입
        """
        # 메타데이터
        self.metadata: AgentMetadata = AgentMetadata(
            agent_name=agent_name,
            agent_class=agent_class,
            version=version,
            access_level=access_level,
            can_modify_ontology=can_modify_ontology,
            lora_adapter_id=lora_adapter_id,
            fine_tuned_model_id=fine_tuned_model_id,
        )

        # 상태
        self._state: AgentState = AgentState.UNINITIALIZED

        # 동시성
        self._state_lock: asyncio.Lock = asyncio.Lock()
        self._ready_event: asyncio.Event = asyncio.Event()
        self._shutdown_event: asyncio.Event = asyncio.Event()

        # ⭐ 격상 #2: Repository
        self._repo: AgentStateRepository = (
            repository or InMemoryAgentStateRepository()
        )

        # ⭐ 격상 #3 + #4: Broker
        self._broker: MessageBroker = broker or InMemoryBroker()
        self._broker_owned: bool = broker is None  # 자체 생성 = 자동 관리
        self._subscriptions: list[Subscription] = []

        # 로거
        self._logger = logging.getLogger(
            f"ledo.agents.{agent_name}"
        )

        self._logger.info(
            f"인스턴스 생성: {self.metadata.agent_class} "
            f"(id={self.metadata.agent_id[:8]}..., "
            f"lora={lora_adapter_id}, "
            f"repo={type(self._repo).__name__}, "
            f"broker={type(self._broker).__name__})"
        )

    # ════════════════════════════════════════
    # 라이프사이클 (Async Template Method)
    # ════════════════════════════════════════

    async def initialize(self) -> None:
        """에이전트 초기화 (4개 격상 통합)

        흐름:
            1. 상태 → INITIALIZING
            2. 브로커 시작 (자체 소유 시)
            3. _on_initialize() 자식 비동기 구현
            4. Repository 등록 + 이벤트 기록
            5. 상태 → READY
            6. ⭐ Broker 에 "agent.<name>.initialized" 발행
            7. ready_event 설정
            8. audit 기록
        """
        async with self._state_lock:
            if self._state != AgentState.UNINITIALIZED:
                raise RuntimeError(
                    f"이미 초기화됨: 현재={self._state.value}"
                )
            self._state = AgentState.INITIALIZING

        self._logger.info(f"초기화 시작: {self.metadata.agent_class}")

        try:
            # 1. ⭐ 격상 #4: 자체 브로커면 자동 시작
            if self._broker_owned:
                await self._broker.start()

            # 2. 자식의 비동기 초기화 (DB 연결, 모델 로드 등)
            await self._on_initialize()

            # 3. ⭐ 격상 #2: Repository 등록
            await self._repo.register_agent(
                self.metadata.model_dump(mode="json")
            )
            await self._repo.record_lifecycle_event(
                agent_id=self.metadata.agent_id,
                event_type="initialize",
                outcome="success",
            )

            # 4. 상태 → READY
            async with self._state_lock:
                self._state = AgentState.READY

            # 5. ⭐ 격상 #4: 라이프사이클 이벤트 발행
            await self._publish_lifecycle_event(
                "initialized",
                payload={
                    "agent_id": self.metadata.agent_id,
                    "agent_name": self.metadata.agent_name,
                    "lora_adapter": self.metadata.lora_adapter_id,
                },
            )

            # 6. 신호
            self._ready_event.set()

            self._logger.info(f"초기화 완료: 상태=READY")

            # 7. audit
            await self._audit_lifecycle_async(
                "initialize",
                AuditOutcome.SUCCESS,
            )

        except Exception as e:
            async with self._state_lock:
                self._state = AgentState.ERROR

            self._logger.error(
                f"초기화 실패: {type(e).__name__}: {e}"
            )

            # 실패 이벤트도 발행 + 기록 (Fail-Safe)
            try:
                await self._publish_lifecycle_event(
                    "error",
                    payload={"error": str(e), "phase": "initialize"},
                )
            except Exception:
                pass  # 발행 실패해도 계속

            try:
                await self._repo.record_lifecycle_event(
                    agent_id=self.metadata.agent_id,
                    event_type="initialize",
                    outcome="failure",
                    details={"error": str(e)},
                )
            except Exception as repo_err:
                self._logger.error(f"Repository 실패: {repo_err}")

            await self._audit_lifecycle_async(
                "initialize",
                AuditOutcome.FAILURE,
                error_message=str(e),
            )
            raise

    async def run(self, input_data: dict[str, Any]) -> AgentResult:
        """에이전트 작업 실행 (4개 격상 통합)

        흐름:
            1. 상태 검증 (READY/IDLE)
            2. 상태 → RUNNING
            3. Repository 에 invocation +1 (atomic)
            4. _before_process() 자식 훅
            5. process() 자식 실제 작업
            6. _after_process() 자식 훅
            7. ⭐ Broker 에 결과 발행 (success/failure)
            8. 상태 → IDLE
        """
        # 1. 상태 검증
        async with self._state_lock:
            if self._state not in (AgentState.READY, AgentState.IDLE):
                raise RuntimeError(
                    f"실행 불가: 현재={self._state.value}"
                )
            self._state = AgentState.RUNNING

        start_time = datetime.now(timezone.utc)

        # 2. Repository invocation 기록
        try:
            await self._repo.increment_invocation(
                agent_id=self.metadata.agent_id,
                timestamp=start_time,
            )
        except Exception as repo_err:
            self._logger.warning(
                f"Repository 기록 실패: {repo_err} (계속 진행)"
            )

        self._logger.debug(f"작업 시작")

        try:
            # 3. 자식 훅 + 실제 작업
            await self._before_process(input_data)
            result = await self.process(input_data)
            await self._after_process(input_data, result)

            # 4. duration 계산
            end_time = datetime.now(timezone.utc)
            duration_ms = int(
                (end_time - start_time).total_seconds() * 1000
            )
            result = result.model_copy(update={"duration_ms": duration_ms})

            # 5. 상태 → IDLE
            async with self._state_lock:
                self._state = AgentState.IDLE

            # 6. ⭐ 격상 #4: 결과 이벤트 발행
            outcome_str = "success" if result.outcome == AuditOutcome.SUCCESS else "failure"
            await self._publish_result_event(
                outcome=outcome_str,
                result=result,
            )

            self._logger.debug(
                f"작업 완료: outcome={result.outcome}, "
                f"duration={duration_ms}ms"
            )

            return result

        except Exception as e:
            # 에러 처리
            async with self._state_lock:
                self._state = AgentState.ERROR

            # Repository error 카운터
            try:
                await self._repo.increment_error(self.metadata.agent_id)
            except Exception as repo_err:
                self._logger.error(f"Repository error 실패: {repo_err}")

            end_time = datetime.now(timezone.utc)
            duration_ms = int(
                (end_time - start_time).total_seconds() * 1000
            )

            self._logger.error(
                f"작업 실패: {type(e).__name__}: {e}"
            )

            error_result = AgentResult(
                agent_id=self.metadata.agent_id,
                outcome=AuditOutcome.FAILURE,
                error_message=f"{type(e).__name__}: {str(e)}",
                duration_ms=duration_ms,
            )

            # ⭐ 격상 #4: 실패 이벤트 발행
            try:
                await self._publish_result_event(
                    outcome="failure",
                    result=error_result,
                )
            except Exception:
                pass  # 발행 실패해도 계속

            # audit
            try:
                audit(AuditEvent(
                    event_type=AuditEventType.LLM_DECISION,
                    outcome=AuditOutcome.FAILURE,
                    severity=AuditSeverity.ERROR,
                    actor=self.metadata.actor_id,
                    action="agent_run",
                    error_message=str(e),
                    llm_model_id=self.metadata.base_model_id,
                ))
            except Exception as audit_err:
                self._logger.error(f"audit 실패: {audit_err}")

            return error_result

    async def shutdown(self) -> None:
        """에이전트 종료 (4개 격상 통합)

        흐름:
            1. 상태 → SHUTTING_DOWN
            2. 모든 구독 해제 (Broker)
            3. _on_shutdown() 자식 정리
            4. Repository 이벤트 + deregister
            5. ⭐ Broker 에 "shutdown" 발행
            6. 상태 → TERMINATED
            7. 자체 브로커면 종료
        """
        async with self._state_lock:
            if self._state == AgentState.TERMINATED:
                self._logger.warning("이미 종료됨")
                return
            self._state = AgentState.SHUTTING_DOWN

        self._logger.info(f"종료 시작: {self.metadata.agent_class}")

        try:
            # 1. ⭐ 격상 #4: 모든 구독 해제
            for sub in self._subscriptions:
                try:
                    await self._broker.unsubscribe(sub.subscription_id)
                except Exception as e:
                    self._logger.error(f"구독 해제 실패: {e}")
            self._subscriptions.clear()

            # 2. 자식의 정리
            await self._on_shutdown()

            # 3. ⭐ 격상 #4: shutdown 이벤트 발행 (종료 전)
            try:
                await self._publish_lifecycle_event(
                    "shutdown",
                    payload={"agent_id": self.metadata.agent_id},
                )
            except Exception as e:
                self._logger.error(f"shutdown 발행 실패: {e}")

            # 4. Repository
            await self._repo.record_lifecycle_event(
                agent_id=self.metadata.agent_id,
                event_type="shutdown",
                outcome="success",
            )
            await self._repo.deregister_agent(self.metadata.agent_id)

            # 5. 상태 → TERMINATED
            async with self._state_lock:
                self._state = AgentState.TERMINATED

            # 6. 신호
            self._shutdown_event.set()
            self._ready_event.clear()

            # 7. ⭐ 격상 #4: 자체 브로커면 종료
            if self._broker_owned:
                # 잠시 대기 (shutdown 이벤트 전달 완료 위해)
                await asyncio.sleep(0.1)
                await self._broker.stop()

            self._logger.info(f"종료 완료")

            await self._audit_lifecycle_async(
                "shutdown",
                AuditOutcome.SUCCESS,
            )

        except Exception as e:
            async with self._state_lock:
                self._state = AgentState.ERROR

            self._logger.error(f"종료 실패: {e}")

            await self._audit_lifecycle_async(
                "shutdown",
                AuditOutcome.FAILURE,
                error_message=str(e),
            )
            raise

    # ════════════════════════════════════════
    # 비동기 컨텍스트 매니저
    # ════════════════════════════════════════

    async def __aenter__(self) -> "BaseAgent":
        await self.initialize()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any],
    ) -> None:
        await self.shutdown()

    # ════════════════════════════════════════
    # 추상 메서드 (자식 필수 구현)
    # ════════════════════════════════════════

    @abstractmethod
    async def process(self, input_data: dict[str, Any]) -> AgentResult:
        """에이전트의 실제 작업 로직 (Async)

        자식이 반드시 async def 로 구현.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} 가 async process() 구현 필요"
        )

    # ════════════════════════════════════════
    # 훅 메서드 (자식 선택적)
    # ════════════════════════════════════════

    async def _on_initialize(self) -> None:
        """초기화 시 추가 작업 (예: subscribe 토픽 등록)"""
        pass

    async def _on_shutdown(self) -> None:
        """종료 시 정리 작업"""
        pass

    async def _before_process(self, input_data: dict[str, Any]) -> None:
        """process 전 처리"""
        pass

    async def _after_process(
        self,
        input_data: dict[str, Any],
        result: AgentResult,
    ) -> None:
        """process 후 처리"""
        pass

    # ════════════════════════════════════════
    # ⭐ 격상 #4: Pub/Sub 헬퍼 API
    # ════════════════════════════════════════

    async def publish(
        self,
        topic: str,
        payload: dict[str, Any],
        correlation_id: Optional[str] = None,
    ) -> None:
        """메시지 발행 (자식 에이전트가 사용)

        Args:
            topic: 토픽 이름 (예: "alarm.triggered.helmet")
            payload: 메시지 데이터
            correlation_id: 워크플로우 그룹 ID

        사용 예시:
            class SafetyAgent(BaseAgent):
                async def process(self, input_data):
                    if not input_data["helmet_on"]:
                        await self.publish(
                            "alarm.triggered.helmet",
                            {"worker_id": input_data["worker_id"]},
                        )
                    ...
        """
        message = Message(
            topic=topic,
            publisher_id=self.metadata.actor_id,
            payload=payload,
            correlation_id=correlation_id,
        )
        await self._broker.publish(message)

    async def subscribe(
        self,
        topic_pattern: str,
        handler: MessageHandler,
    ) -> Subscription:
        """토픽 구독 (자식 에이전트가 사용)

        Args:
            topic_pattern: 토픽 패턴 (예: "sensor.helmet.*")
            handler: 비동기 핸들러 함수

        Returns:
            Subscription 인스턴스

        사용 예시:
            class SafetyAgent(BaseAgent):
                async def _on_initialize(self):
                    await self.subscribe(
                        "sensor.helmet.*",
                        self._handle_helmet_event,
                    )
                
                async def _handle_helmet_event(self, msg):
                    # 헬멧 사건 처리
                    ...
        """
        subscription = await self._broker.subscribe(
            topic_pattern=topic_pattern,
            handler=handler,
            subscriber_id=self.metadata.actor_id,
        )
        self._subscriptions.append(subscription)
        self._logger.info(
            f"구독 등록: pattern={topic_pattern}, "
            f"sub_id={subscription.subscription_id[:8]}..."
        )
        return subscription

    # ════════════════════════════════════════
    # ⭐ 격상 #4: 자동 이벤트 발행
    # ════════════════════════════════════════

    async def _publish_lifecycle_event(
        self,
        event: str,
        payload: dict[str, Any],
    ) -> None:
        """라이프사이클 이벤트 자동 발행 (Fail-Safe)

        토픽 형식: "agent.<name>.<event>"
        예시:
            agent.safety.initialized
            agent.safety.shutdown
            agent.safety.error

        ⚠️ Fail-Safe:
           발행 실패해도 에이전트 라이프사이클은 계속
        """
        try:
            topic = f"agent.{self.metadata.agent_name}.{event}"
            full_payload = {
                **payload,
                "agent_class": self.metadata.agent_class,
                "version": self.metadata.version,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            await self.publish(topic=topic, payload=full_payload)
        except Exception as e:
            self._logger.warning(
                f"라이프사이클 이벤트 발행 실패: event={event}, error={e}"
            )

    async def _publish_result_event(
        self,
        outcome: str,
        result: AgentResult,
    ) -> None:
        """작업 결과 이벤트 자동 발행 (Fail-Safe)

        토픽 형식: "agent.<name>.result.<outcome>"
        예시:
            agent.safety.result.success
            agent.safety.result.failure
        """
        try:
            topic = f"agent.{self.metadata.agent_name}.result.{outcome}"
            payload = {
                "agent_id": self.metadata.agent_id,
                "result_id": result.result_id,
                "outcome": result.outcome,
                "duration_ms": result.duration_ms,
                "output_keys": list(result.output.keys()),
                "has_error": result.error_message is not None,
            }
            await self.publish(
                topic=topic,
                payload=payload,
                correlation_id=result.correlation_id,
            )
        except Exception as e:
            self._logger.warning(
                f"결과 이벤트 발행 실패: outcome={outcome}, error={e}"
            )

    # ════════════════════════════════════════
    # 내부 헬퍼
    # ════════════════════════════════════════

    async def _audit_lifecycle_async(
        self,
        action: str,
        outcome: AuditOutcome,
        error_message: Optional[str] = None,
    ) -> None:
        """라이프사이클 사건 audit (Fail-Safe)"""
        try:
            audit(AuditEvent(
                event_type=AuditEventType.SYSTEM_LIFECYCLE,
                outcome=outcome,
                severity=(
                    AuditSeverity.INFO
                    if outcome == AuditOutcome.SUCCESS
                    else AuditSeverity.ERROR
                ),
                actor=self.metadata.actor_id,
                action=f"agent_{action}",
                error_message=error_message,
            ))
        except Exception as e:
            self._logger.error(f"audit 실패: {e}")

    # ════════════════════════════════════════
    # 비동기 대기
    # ════════════════════════════════════════

    async def wait_until_ready(
        self,
        timeout: Optional[float] = None,
    ) -> bool:
        """READY 까지 대기"""
        try:
            await asyncio.wait_for(
                self._ready_event.wait(),
                timeout=timeout,
            )
            return True
        except asyncio.TimeoutError:
            return False

    async def wait_until_terminated(
        self,
        timeout: Optional[float] = None,
    ) -> bool:
        """TERMINATED 까지 대기"""
        try:
            await asyncio.wait_for(
                self._shutdown_event.wait(),
                timeout=timeout,
            )
            return True
        except asyncio.TimeoutError:
            return False

    # ════════════════════════════════════════
    # 외부 API (관측 가능성)
    # ════════════════════════════════════════

    @property
    def state(self) -> AgentState:
        return self._state

    @property
    def is_ready(self) -> bool:
        return self._state in (AgentState.READY, AgentState.IDLE)

    @property
    def is_terminated(self) -> bool:
        return self._state == AgentState.TERMINATED

    async def get_health(self) -> dict[str, Any]:
        """헬스 체크 (4개 격상 통합)"""
        now = datetime.now(timezone.utc)
        uptime_seconds = int(
            (now - self.metadata.created_at).total_seconds()
        )

        # Repository 통계
        stats = await self._repo.get_stats(self.metadata.agent_id)

        # Broker 통계
        broker_stats = await self._broker.get_stats()

        return {
            "agent_id": self.metadata.agent_id,
            "agent_name": self.metadata.agent_name,
            "agent_class": self.metadata.agent_class,
            "state": self._state.value,
            "is_ready": self.is_ready,
            "uptime_seconds": uptime_seconds,
            "version": self.metadata.version,
            "base_model": self.metadata.base_model_id,
            "lora_adapter": self.metadata.lora_adapter_id,
            "is_specialized": self.metadata.is_specialized,
            # Repository 통계
            "total_invocations": stats["total_invocations"],
            "total_errors": stats["total_errors"],
            "error_rate": stats["error_rate"],
            "last_invocation_at": (
                stats["last_invocation_at"].isoformat()
                if stats["last_invocation_at"]
                else None
            ),
            "repository_backend": type(self._repo).__name__,
            # Broker 통계
            "broker_backend": type(self._broker).__name__,
            "active_subscriptions": len(self._subscriptions),
            "broker_published": broker_stats.get("total_published", 0),
            "broker_delivered": broker_stats.get("total_delivered", 0),
        }