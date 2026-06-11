"""
LEDO.ai - BaseAgent 추상 클래스 (분산 시스템 표준)

수백 개 에이전트 + LoRA + 휴머노이드 시스템의 진짜 토대.
처음부터 산업 표준 분산 시스템 아키텍처 적용.

격상 단계:
─────────────────────────────────────
✅ 격상 #1: asyncio 비동기 (수천 개 동시 작동)
✅ 격상 #2: Repository Pattern (외부 상태 저장) ⭐ 현재
⏭️ 격상 #3: Pub/Sub Message Broker (다음)
⏭️ 격상 #4: 통합 + 검증 (마지막)

이 파일의 책임:
─────────────────────────────────────
- async/await 라이프사이클
- asyncio.Lock (동시성 보호)
- asyncio.Event (라이프사이클 신호)
- 비동기 컨텍스트 매니저 (async with)
- Repository 의존성 주입 (Stateless)
- 외부 상태 저장 (PostgreSQL/PROV-O/Redis 호환)
- LoRA / Fine-tuning 메타데이터

참조 표준:
─────────────────────────────────────
- PEP 492 (async/await)
- PEP 3156 (asyncio)
- Domain-Driven Design (Eric Evans, 2003)
- Repository Pattern (Martin Fowler, PoEAA)
- 12-Factor App #6 (Stateless Processes)
- Hexagonal Architecture (Alistair Cockburn, 2005)
- LangGraph BaseAgent 패턴

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


logger = logging.getLogger(__name__)


# ════════════════════════════════════════════════════════════
# 1. AgentState - 8단계 라이프사이클 상태
# ════════════════════════════════════════════════════════════


class AgentState(str, Enum):
    """에이전트의 라이프사이클 상태 (분산 시스템 표준)

    상태 전이도:
    ─────────────
    UNINITIALIZED → INITIALIZING → READY ↔ RUNNING → IDLE
                          ↓          ↓        ↓        ↓
                       ERROR ← ─── ─ ┴ ── ── ┴ ── ── ┘
                          ↓
                    SHUTTING_DOWN → TERMINATED

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
    """에이전트 인스턴스의 메타정보

    Repository 에 영구 저장 가능.
    분산 시스템에서 각 인스턴스 식별/추적의 핵심.

    ⭐ 격상 #2 변화:
       - total_invocations, total_errors 필드 삭제!
       - 통계는 Repository 가 관리 (Stateless)
       - 메타데이터는 식별/설정만 보유
    """
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        str_strip_whitespace=True,
        frozen=False,
    )

    # ════════════════════════════════════════
    # 1. 식별 (Identity)
    # ════════════════════════════════════════
    agent_id: str = Field(
        default_factory=lambda: str(uuid4()),
        pattern=r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$",
        description="에이전트 인스턴스의 UUID v4 (분산 시스템 unique)",
    )
    agent_name: str = Field(
        ...,
        min_length=1,
        max_length=64,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="에이전트 이름 (snake_case, 예: 'safety')",
    )
    agent_class: str = Field(
        ...,
        min_length=1,
        max_length=64,
        pattern=r"^[A-Z][a-zA-Z0-9]*$",
        description="에이전트 클래스명 (PascalCase, 예: 'SafetyAgent')",
    )
    version: str = Field(
        default="1.0.0",
        pattern=r"^\d+\.\d+\.\d+$",
        description="에이전트 버전 (SemVer)",
    )

    # ════════════════════════════════════════
    # 2. 운영 정보 (Runtime)
    # ════════════════════════════════════════
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="인스턴스 생성 시각 (UTC)",
    )
    environment: str = Field(
        default_factory=lambda: settings.LEDO_ENV,
        max_length=32,
        description="실행 환경",
    )
    host_node: Optional[str] = Field(
        default=None,
        max_length=128,
        description="실행 노드 식별자 (분산 환경)",
    )

    # ════════════════════════════════════════
    # 3. 권한 + 보안
    # ════════════════════════════════════════
    access_level: AccessLevel = Field(
        default=AccessLevel.INTERNAL,
        description="이 에이전트의 권한 레벨",
    )
    can_modify_ontology: bool = Field(
        default=False,
        description="온톨로지 변경 권한 (DialecticAgent 만 True)",
    )

    # ════════════════════════════════════════
    # 4. LoRA / Fine-tuning (확장성)
    # ════════════════════════════════════════
    base_model_id: str = Field(
        default_factory=lambda: settings.OLLAMA_MODEL,
        max_length=128,
        description="기본 LLM 모델 (예: qwen2.5-coder:14b)",
    )
    lora_adapter_id: Optional[str] = Field(
        default=None,
        max_length=128,
        description="LoRA 어댑터 ID (도메인 특화, 예: 'crane_safety_v3')",
    )
    fine_tuned_model_id: Optional[str] = Field(
        default=None,
        max_length=128,
        description="Fine-tuned 모델 ID",
    )

    @property
    def actor_id(self) -> str:
        """audit.py 의 actor 형식 변환 (예: 'agent:safety')"""
        return f"agent:{self.agent_name}"

    @property
    def is_specialized(self) -> bool:
        """도메인 특화 모델 사용 여부 (LoRA 또는 Fine-tuned)"""
        return (
            self.lora_adapter_id is not None
            or self.fine_tuned_model_id is not None
        )


# ════════════════════════════════════════════════════════════
# 3. AgentResult - 작업 결과 표준 형식
# ════════════════════════════════════════════════════════════


class AgentResult(BaseModel):
    """에이전트 작업의 표준 결과 (Immutable)"""
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    # 식별
    result_id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="결과 UUID v4",
    )
    agent_id: str = Field(
        ...,
        description="결과 생성한 에이전트의 ID",
    )
    timestamp_utc: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="결과 생성 시각 (UTC)",
    )

    # 결과 데이터
    outcome: AuditOutcome = Field(
        ...,
        description="작업 결과",
    )
    output: dict[str, Any] = Field(
        default_factory=dict,
        description="에이전트의 실제 출력",
    )
    error_message: Optional[str] = Field(
        default=None,
        max_length=2048,
        description="실패 시 에러 메시지",
    )

    # 성능 메트릭
    duration_ms: int = Field(
        default=0,
        ge=0,
        description="작업 소요 시간 (밀리초)",
    )
    llm_tokens_used: int = Field(
        default=0,
        ge=0,
        description="사용한 LLM 토큰 수",
    )

    # 추적 정보
    audit_event_id: Optional[str] = Field(
        default=None,
        description="audit 시스템의 event_id",
    )
    correlation_id: Optional[str] = Field(
        default=None,
        max_length=128,
        description="워크플로우 그룹 ID",
    )


# ════════════════════════════════════════════════════════════
# 4. BaseAgent - 비동기 + Stateless 추상 부모
# ════════════════════════════════════════════════════════════


class BaseAgent(ABC):
    """모든 LEDO 에이전트의 비동기 + Stateless 추상 부모

    asyncio + Repository Pattern 기반 분산 시스템 토대.
    수백 개 에이전트가 외부 상태 저장소를 공유.

    ⭐ 격상 #2 핵심:
       - 모든 통계는 Repository 에 저장
       - 인스턴스는 Stateless (메모리 상태 X)
       - 인스턴스 재시작/복제 자유
       - 같은 에이전트 N개 복제본 = 같은 상태 공유

    사용 예시:
    ─────────────────────────────────────
        # 기본 (인메모리 Repository)
        async with SafetyAgent() as agent:
            result = await agent.run({"worker_id": "W042"})

        # 운영 (공유 PostgreSQL Repository)
        pg_repo = PostgresAgentRepository(conn_string=...)
        async with SafetyAgent(repository=pg_repo) as agent:
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
    ) -> None:
        """BaseAgent 초기화 (인스턴스 생성)

        ⚠️ 실제 초기화 (DB 연결, 모델 로드) 는 async initialize() 에서.

        Args:
            agent_name: snake_case 이름
            agent_class: PascalCase 클래스명
            version: SemVer 버전
            access_level: 권한 레벨
            can_modify_ontology: 온톨로지 변경 권한
            lora_adapter_id: LoRA 어댑터 ID (도메인 특화)
            fine_tuned_model_id: Fine-tuned 모델 ID
            repository: 상태 저장소 (기본: InMemory)
                ⭐ 격상 #2: 외부 상태 분리
                프로덕션에선 PostgresRepository 주입
        """
        # 메타데이터 (Pydantic 검증)
        self.metadata: AgentMetadata = AgentMetadata(
            agent_name=agent_name,
            agent_class=agent_class,
            version=version,
            access_level=access_level,
            can_modify_ontology=can_modify_ontology,
            lora_adapter_id=lora_adapter_id,
            fine_tuned_model_id=fine_tuned_model_id,
        )

        # 상태 (메모리 - 빠른 전이용, 영구 상태는 Repository 에)
        self._state: AgentState = AgentState.UNINITIALIZED

        # 동시성 보호
        self._state_lock: asyncio.Lock = asyncio.Lock()

        # 라이프사이클 신호
        self._ready_event: asyncio.Event = asyncio.Event()
        self._shutdown_event: asyncio.Event = asyncio.Event()

        # ⭐ 격상 #2: Repository 의존성 주입 (Stateless)
        self._repo: AgentStateRepository = (
            repository or InMemoryAgentStateRepository()
        )

        # 에이전트별 로거 (계층적)
        self._logger = logging.getLogger(
            f"ledo.agents.{agent_name}"
        )

        self._logger.info(
            f"인스턴스 생성: {self.metadata.agent_class} "
            f"(id={self.metadata.agent_id[:8]}..., "
            f"lora={lora_adapter_id}, "
            f"repo={type(self._repo).__name__})"
        )

    # ════════════════════════════════════════
    # 라이프사이클 (Async Template Method)
    # ════════════════════════════════════════

    async def initialize(self) -> None:
        """에이전트 초기화 (Async Template Method)

        흐름:
            1. Lock 획득
            2. 상태 검증 (UNINITIALIZED)
            3. 상태 → INITIALIZING
            4. _on_initialize() 자식이 비동기 구현
            5. ⭐ Repository 에 에이전트 등록
            6. ⭐ Repository 에 lifecycle 이벤트 기록
            7. 상태 → READY
            8. ready_event 설정
            9. audit 기록
        """
        async with self._state_lock:
            if self._state != AgentState.UNINITIALIZED:
                raise RuntimeError(
                    f"이미 초기화됨: 현재 상태={self._state.value}"
                )
            self._state = AgentState.INITIALIZING

        self._logger.info(f"초기화 시작: {self.metadata.agent_class}")

        try:
            # 1. 자식의 비동기 초기화
            await self._on_initialize()

            # 2. ⭐ 격상 #2: Repository 에 등록 + 이벤트 기록
            await self._repo.register_agent(
                self.metadata.model_dump(mode="json")
            )
            await self._repo.record_lifecycle_event(
                agent_id=self.metadata.agent_id,
                event_type="initialize",
                outcome="success",
            )

            # 3. 상태 → READY
            async with self._state_lock:
                self._state = AgentState.READY

            # 4. ready 신호
            self._ready_event.set()

            self._logger.info(f"초기화 완료: 상태=READY")

            # 5. audit 기록
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

            # 실패 이벤트도 Repository 에 기록 (Fail-Safe)
            try:
                await self._repo.record_lifecycle_event(
                    agent_id=self.metadata.agent_id,
                    event_type="initialize",
                    outcome="failure",
                    details={"error": str(e)},
                )
            except Exception as repo_err:
                self._logger.error(f"Repository 기록 실패: {repo_err}")

            await self._audit_lifecycle_async(
                "initialize",
                AuditOutcome.FAILURE,
                error_message=str(e),
            )
            raise

    async def run(self, input_data: dict[str, Any]) -> AgentResult:
        """에이전트 작업 실행 (Async Template Method)

        흐름:
            1. 상태 검증 (READY/IDLE)
            2. 상태 → RUNNING
            3. ⭐ Repository 에 invocation 카운터 +1 (atomic)
            4. _before_process() 자식 훅
            5. process() 자식의 실제 작업
            6. _after_process() 자식 훅
            7. duration 측정
            8. 상태 → IDLE
            9. audit 기록

        에러 시:
            - ⭐ Repository 에 error 카운터 +1 (atomic)
            - 상태 → ERROR
        """
        # 1. 상태 검증
        async with self._state_lock:
            if self._state not in (AgentState.READY, AgentState.IDLE):
                raise RuntimeError(
                    f"실행 불가 상태: 현재={self._state.value}, "
                    f"필요: READY 또는 IDLE"
                )
            self._state = AgentState.RUNNING

        # 시간 측정 시작 (Lock 밖에서)
        start_time = datetime.now(timezone.utc)

        # ⭐ 격상 #2: Repository 에 invocation 기록 (atomic)
        try:
            await self._repo.increment_invocation(
                agent_id=self.metadata.agent_id,
                timestamp=start_time,
            )
        except Exception as repo_err:
            self._logger.warning(
                f"Repository invocation 기록 실패: {repo_err} "
                "(작업은 계속 진행)"
            )

        self._logger.debug(f"작업 시작")

        try:
            # 2. 자식 훅 (작업 전)
            await self._before_process(input_data)

            # 3. 실제 작업 (자식의 비동기 구현)
            result = await self.process(input_data)

            # 4. 자식 훅 (작업 후)
            await self._after_process(input_data, result)

            # 5. 소요 시간 계산
            end_time = datetime.now(timezone.utc)
            duration_ms = int(
                (end_time - start_time).total_seconds() * 1000
            )

            # 6. 결과에 duration 주입 (frozen 이라 model_copy)
            result = result.model_copy(update={"duration_ms": duration_ms})

            # 7. 상태 변경
            async with self._state_lock:
                self._state = AgentState.IDLE

            self._logger.debug(
                f"작업 완료: outcome={result.outcome}, "
                f"duration={duration_ms}ms"
            )

            return result

        except Exception as e:
            # 에러 처리
            async with self._state_lock:
                self._state = AgentState.ERROR

            # ⭐ 격상 #2: Repository 에 error 기록 (atomic)
            try:
                await self._repo.increment_error(self.metadata.agent_id)
            except Exception as repo_err:
                self._logger.error(f"Repository error 기록 실패: {repo_err}")

            end_time = datetime.now(timezone.utc)
            duration_ms = int(
                (end_time - start_time).total_seconds() * 1000
            )

            self._logger.error(
                f"작업 실패: {type(e).__name__}: {e}"
            )

            # 에러 결과 생성
            error_result = AgentResult(
                agent_id=self.metadata.agent_id,
                outcome=AuditOutcome.FAILURE,
                error_message=f"{type(e).__name__}: {str(e)}",
                duration_ms=duration_ms,
            )

            # audit 기록 (Fail-Safe)
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
        """에이전트 종료 (Async Template Method)

        흐름:
            1. 상태 → SHUTTING_DOWN
            2. _on_shutdown() 자식의 정리
            3. ⭐ Repository 에 shutdown 이벤트 기록
            4. ⭐ Repository 에서 deregister
            5. 상태 → TERMINATED
            6. shutdown_event 설정
        """
        async with self._state_lock:
            if self._state == AgentState.TERMINATED:
                self._logger.warning("이미 종료됨")
                return
            self._state = AgentState.SHUTTING_DOWN

        self._logger.info(f"종료 시작: {self.metadata.agent_class}")

        try:
            # 1. 자식의 정리 작업
            await self._on_shutdown()

            # 2. ⭐ 격상 #2: Repository 이벤트 + deregister
            await self._repo.record_lifecycle_event(
                agent_id=self.metadata.agent_id,
                event_type="shutdown",
                outcome="success",
            )
            await self._repo.deregister_agent(self.metadata.agent_id)

            # 3. 상태 변경
            async with self._state_lock:
                self._state = AgentState.TERMINATED

            # 4. 신호
            self._shutdown_event.set()
            self._ready_event.clear()

            self._logger.info(f"종료 완료")

            # 5. audit
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
    # 비동기 컨텍스트 매니저 (async with)
    # ════════════════════════════════════════

    async def __aenter__(self) -> "BaseAgent":
        """async with 시작 시 자동 호출"""
        await self.initialize()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any],
    ) -> None:
        """async with 종료 시 자동 호출 (예외 발생해도)"""
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
    # 훅 메서드 (자식 선택적 오버라이드)
    # ════════════════════════════════════════

    async def _on_initialize(self) -> None:
        """초기화 시 추가 작업 (비동기)"""
        pass

    async def _on_shutdown(self) -> None:
        """종료 시 정리 작업 (비동기)"""
        pass

    async def _before_process(
        self,
        input_data: dict[str, Any],
    ) -> None:
        """process 전 처리 (비동기)"""
        pass

    async def _after_process(
        self,
        input_data: dict[str, Any],
        result: AgentResult,
    ) -> None:
        """process 후 처리 (비동기)"""
        pass

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
    # 비동기 대기 메서드
    # ════════════════════════════════════════

    async def wait_until_ready(
        self,
        timeout: Optional[float] = None,
    ) -> bool:
        """에이전트가 READY 까지 대기"""
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
        """에이전트가 TERMINATED 까지 대기"""
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
        """현재 상태 (읽기 전용)"""
        return self._state

    @property
    def is_ready(self) -> bool:
        """작업 수행 가능?"""
        return self._state in (AgentState.READY, AgentState.IDLE)

    @property
    def is_terminated(self) -> bool:
        """종료됨?"""
        return self._state == AgentState.TERMINATED

    async def get_health(self) -> dict[str, Any]:
        """헬스 체크 (Repository 통합)

        ⭐ 격상 #2: 통계는 Repository 에서 조회
           에이전트는 메모리에 통계 X (Stateless)
        """
        now = datetime.now(timezone.utc)
        uptime_seconds = int(
            (now - self.metadata.created_at).total_seconds()
        )

        # ⭐ Repository 에서 통계 조회
        stats = await self._repo.get_stats(self.metadata.agent_id)

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
            # ⭐ Repository 통계
            "total_invocations": stats["total_invocations"],
            "total_errors": stats["total_errors"],
            "error_rate": stats["error_rate"],
            "last_invocation_at": (
                stats["last_invocation_at"].isoformat()
                if stats["last_invocation_at"]
                else None
            ),
            "repository_backend": type(self._repo).__name__,
        }
    
    