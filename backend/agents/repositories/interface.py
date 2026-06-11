"""
LEDO.ai - Agent State Repository 인터페이스

분산 시스템의 핵심: 에이전트 상태를 외부에 저장.
인스턴스 재시작/복제/마이그레이션 자유로움 보장.

설계 원칙 (Repository Pattern):
─────────────────────────────────────
1. Interface Segregation (인터페이스 분리)
2. Dependency Inversion (의존성 역전)
3. Stateless Agent (에이전트는 메모리 상태 X)
4. Pluggable Backends (구현 교체 가능)
5. Async-First (모든 메서드 비동기)

지원 백엔드 (구현 클래스):
─────────────────────────────────────
- InMemoryRepository  - 테스트/개발용 (이번 메시지)
- PostgresRepository  - 운영 RDB (격상 #4)
- RDFRepository       - PROV-O 트리플 (격상 #4)
- RedisRepository     - 임시 상태/캐시 (격상 #4)

참조 표준:
─────────────────────────────────────
- Domain-Driven Design (Eric Evans, 2003)
- Repository Pattern (Martin Fowler, PoEAA)
- Hexagonal Architecture (Ports & Adapters)
- Clean Architecture (Uncle Bob)
- 12-Factor App #6 (Stateless Processes)

Python 버전: 3.14+
"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Any


# ════════════════════════════════════════════════════════════
# 1. AgentStateRepository - 추상 인터페이스
# ════════════════════════════════════════════════════════════


class AgentStateRepository(ABC):
    """에이전트 상태 저장소의 추상 인터페이스

    ⭐ 모든 구현 클래스는 이 인터페이스를 따라야 함:
       - InMemoryRepository (테스트)
       - PostgresRepository (운영 RDB)
       - RDFRepository (PROV-O 그래프)
       - RedisRepository (캐시)

    ⭐ 에이전트는 이 인터페이스만 알면 됨:
       구체적 구현은 의존성 주입으로 결정

    Repository 의 책임:
    ─────────────────────────────────────
    1. 에이전트 메타데이터 영구 저장
    2. 통계 카운터 관리 (atomic increment)
    3. 라이프사이클 이력 추적
    4. 상태 조회 (헬스 체크용)

    예시 사용 (에이전트 안에서):
        async def _on_initialize(self):
            await self._repo.register_agent(self.metadata)

        async def _after_process(self, input_data, result):
            await self._repo.increment_invocation(
                self.metadata.agent_id
            )
    """

    # ════════════════════════════════════════
    # 1. 에이전트 등록 + 조회
    # ════════════════════════════════════════

    @abstractmethod
    async def register_agent(self, metadata: dict[str, Any]) -> None:
        """에이전트 인스턴스 등록 (initialize 시점)

        Args:
            metadata: AgentMetadata 의 dict 변환

        ⚠️ 같은 agent_id 재등록 시 update (upsert)
        """
        raise NotImplementedError

    @abstractmethod
    async def get_agent(self, agent_id: str) -> Optional[dict[str, Any]]:
        """agent_id 로 에이전트 메타데이터 조회

        Args:
            agent_id: UUID v4

        Returns:
            메타데이터 dict 또는 None (없을 때)
        """
        raise NotImplementedError

    @abstractmethod
    async def deregister_agent(self, agent_id: str) -> bool:
        """에이전트 등록 해제 (shutdown 시점)

        Args:
            agent_id: UUID v4

        Returns:
            True = 삭제됨, False = 없었음
        """
        raise NotImplementedError

    # ════════════════════════════════════════
    # 2. 통계 카운터 (Atomic Operations)
    # ════════════════════════════════════════

    @abstractmethod
    async def increment_invocation(
        self,
        agent_id: str,
        timestamp: Optional[datetime] = None,
    ) -> int:
        """invocation 카운터 +1 (atomic)

        ⚠️ Atomic 보장:
           여러 동시 호출 → 정확히 1씩 증가
           ✅ PostgreSQL: UPDATE ... SET counter = counter + 1
           ✅ Redis: INCR
           ✅ InMemory: asyncio.Lock 사용

        Args:
            agent_id: 에이전트 ID
            timestamp: invocation 시각 (last_invocation_at 업데이트)

        Returns:
            증가 후의 카운터 값
        """
        raise NotImplementedError

    @abstractmethod
    async def increment_error(self, agent_id: str) -> int:
        """error 카운터 +1 (atomic)

        Args:
            agent_id: 에이전트 ID

        Returns:
            증가 후의 카운터 값
        """
        raise NotImplementedError

    @abstractmethod
    async def get_stats(self, agent_id: str) -> dict[str, Any]:
        """에이전트 통계 조회

        Args:
            agent_id: 에이전트 ID

        Returns:
            {
                "total_invocations": int,
                "total_errors": int,
                "last_invocation_at": datetime | None,
                "error_rate": float,
            }

        ⚠️ agent_id 없으면 모든 카운터 0 으로 반환 (Fail-Safe)
        """
        raise NotImplementedError

    # ════════════════════════════════════════
    # 3. 라이프사이클 이력
    # ════════════════════════════════════════

    @abstractmethod
    async def record_lifecycle_event(
        self,
        agent_id: str,
        event_type: str,
        outcome: str,
        timestamp: Optional[datetime] = None,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        """라이프사이클 사건 기록

        Args:
            agent_id: 에이전트 ID
            event_type: 사건 종류 (initialize/shutdown/error)
            outcome: 결과 (success/failure)
            timestamp: 발생 시각 (기본: now)
            details: 추가 정보 (에러 메시지 등)
        """
        raise NotImplementedError

    @abstractmethod
    async def get_lifecycle_history(
        self,
        agent_id: str,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """라이프사이클 이력 조회

        Args:
            agent_id: 에이전트 ID
            limit: 최대 반환 개수

        Returns:
            사건 목록 (최신 순)
        """
        raise NotImplementedError

    # ════════════════════════════════════════
    # 4. 관측 가능성 (Observability)
    # ════════════════════════════════════════

    @abstractmethod
    async def list_active_agents(
        self,
        agent_name: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        """활성 에이전트 목록 조회

        Args:
            agent_name: 특정 이름 필터 (예: "safety")
                       None = 모두

        Returns:
            에이전트 메타데이터 목록

        ⭐ 산업 활용:
           "현재 작동 중인 SafetyAgent 인스턴스 모두?"
           → list_active_agents("safety")
        """
        raise NotImplementedError

    @abstractmethod
    async def count_agents(
        self,
        agent_name: Optional[str] = None,
    ) -> int:
        """에이전트 수 카운트

        Args:
            agent_name: 특정 이름 필터

        Returns:
            카운트
        """
        raise NotImplementedError

    # ════════════════════════════════════════
    # 5. Repository 자체 관리
    # ════════════════════════════════════════

    @abstractmethod
    async def health_check(self) -> dict[str, Any]:
        """Repository 자체 헬스 체크

        Returns:
            {
                "status": "healthy" | "degraded" | "unhealthy",
                "backend": str (예: "postgres", "memory"),
                "latency_ms": int,
                ...
            }

        ⭐ 운영 시 필수:
           DB 다운 → 알람
           느림 → 경고
        """
        raise NotImplementedError