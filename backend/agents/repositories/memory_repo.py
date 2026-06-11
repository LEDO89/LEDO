"""
LEDO.ai - 인메모리 Repository 구현

용도: 개발 + 테스트 + 단위 테스트
프로덕션: PostgresRepository / RDFRepository 사용 (격상 #4)

특징:
─────────────────────────────────────
- 프로세스 안에서만 작동 (재시작 시 데이터 손실)
- asyncio.Lock 으로 동시성 보호
- 빠른 (메모리 접근)
- 분산 X (단일 프로세스만)

⚠️ 운영 환경에서 사용 X:
   - 재시작 시 데이터 손실
   - 여러 프로세스에서 상태 공유 X
   - 사용 시 경고 로그

참조:
- DDD 의 In-Memory Repository 패턴
- 단위 테스트의 표준 패턴 (Mock Repository)
"""
import asyncio
from datetime import datetime, timezone
from typing import Optional, Any
import logging

from agents.repositories.interface import AgentStateRepository


logger = logging.getLogger(__name__)


class InMemoryAgentStateRepository(AgentStateRepository):
    """인메모리 에이전트 상태 저장소

    개발 + 테스트 전용.
    프로덕션 환경에선 PostgresRepository 등 사용.

    내부 구조:
    ─────────────────────────────────────
    _agents:           {agent_id: metadata_dict}
    _stats:            {agent_id: {total_invocations, total_errors, ...}}
    _lifecycle_events: list of events (전체 공유)
    _lock:             asyncio.Lock (동시성 보호)
    """

    def __init__(self) -> None:
        """인메모리 저장소 초기화"""
        # 에이전트 메타데이터 저장소
        self._agents: dict[str, dict[str, Any]] = {}

        # 통계 카운터 저장소
        self._stats: dict[str, dict[str, Any]] = {}

        # 라이프사이클 이력 (시간 순)
        self._lifecycle_events: list[dict[str, Any]] = []

        # 동시성 보호 (atomic 보장)
        self._lock: asyncio.Lock = asyncio.Lock()

        logger.warning(
            "InMemoryAgentStateRepository 사용 중 - "
            "개발/테스트 전용 (프로덕션 X)"
        )

    # ════════════════════════════════════════
    # 1. 에이전트 등록 + 조회
    # ════════════════════════════════════════

    async def register_agent(self, metadata: dict[str, Any]) -> None:
        """에이전트 등록 (upsert)

        같은 agent_id 면 update.
        새 agent_id 면 insert.
        """
        agent_id = metadata.get("agent_id")
        if not agent_id:
            raise ValueError("metadata 에 agent_id 필수")

        async with self._lock:
            self._agents[agent_id] = metadata.copy()

            # 통계 초기화 (없을 때만)
            if agent_id not in self._stats:
                self._stats[agent_id] = {
                    "total_invocations": 0,
                    "total_errors": 0,
                    "last_invocation_at": None,
                    "registered_at": datetime.now(timezone.utc),
                }

        logger.debug(
            f"에이전트 등록: id={agent_id[:8]}..., "
            f"name={metadata.get('agent_name')}"
        )

    async def get_agent(self, agent_id: str) -> Optional[dict[str, Any]]:
        """agent_id 로 메타데이터 조회"""
        async with self._lock:
            data = self._agents.get(agent_id)
            return data.copy() if data else None

    async def deregister_agent(self, agent_id: str) -> bool:
        """에이전트 등록 해제

        ⚠️ 통계와 라이프사이클은 보존 (감사용)
        """
        async with self._lock:
            if agent_id in self._agents:
                del self._agents[agent_id]
                logger.debug(f"에이전트 해제: id={agent_id[:8]}...")
                return True
            return False

    # ════════════════════════════════════════
    # 2. 통계 카운터 (Atomic)
    # ════════════════════════════════════════

    async def increment_invocation(
        self,
        agent_id: str,
        timestamp: Optional[datetime] = None,
    ) -> int:
        """invocation 카운터 +1 (atomic)

        ⭐ asyncio.Lock 으로 atomic 보장:
           여러 동시 호출 → 정확히 1씩 증가
        """
        ts = timestamp or datetime.now(timezone.utc)

        async with self._lock:
            if agent_id not in self._stats:
                # 등록 안 된 에이전트도 통계는 생성 (Fail-Safe)
                self._stats[agent_id] = {
                    "total_invocations": 0,
                    "total_errors": 0,
                    "last_invocation_at": None,
                    "registered_at": ts,
                }

            self._stats[agent_id]["total_invocations"] += 1
            self._stats[agent_id]["last_invocation_at"] = ts

            return self._stats[agent_id]["total_invocations"]

    async def increment_error(self, agent_id: str) -> int:
        """error 카운터 +1 (atomic)"""
        async with self._lock:
            if agent_id not in self._stats:
                self._stats[agent_id] = {
                    "total_invocations": 0,
                    "total_errors": 0,
                    "last_invocation_at": None,
                    "registered_at": datetime.now(timezone.utc),
                }

            self._stats[agent_id]["total_errors"] += 1
            return self._stats[agent_id]["total_errors"]

    async def get_stats(self, agent_id: str) -> dict[str, Any]:
        """에이전트 통계 조회

        ⚠️ Fail-Safe:
           agent_id 없으면 모든 카운터 0 으로 반환
           (예외 발생 X)
        """
        async with self._lock:
            stats = self._stats.get(agent_id)
            if stats is None:
                return {
                    "total_invocations": 0,
                    "total_errors": 0,
                    "last_invocation_at": None,
                    "error_rate": 0.0,
                }

            total = stats["total_invocations"]
            errors = stats["total_errors"]
            error_rate = errors / total if total > 0 else 0.0

            return {
                "total_invocations": total,
                "total_errors": errors,
                "last_invocation_at": stats["last_invocation_at"],
                "error_rate": round(error_rate, 4),
            }

    # ════════════════════════════════════════
    # 3. 라이프사이클 이력
    # ════════════════════════════════════════

    async def record_lifecycle_event(
        self,
        agent_id: str,
        event_type: str,
        outcome: str,
        timestamp: Optional[datetime] = None,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        """라이프사이클 사건 기록"""
        ts = timestamp or datetime.now(timezone.utc)

        event = {
            "agent_id": agent_id,
            "event_type": event_type,
            "outcome": outcome,
            "timestamp": ts,
            "details": details or {},
        }

        async with self._lock:
            self._lifecycle_events.append(event)

    async def get_lifecycle_history(
        self,
        agent_id: str,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """라이프사이클 이력 조회 (최신 순)"""
        async with self._lock:
            # agent_id 필터링
            filtered = [
                e for e in self._lifecycle_events
                if e["agent_id"] == agent_id
            ]
            # 최신 순 정렬 (timestamp 내림차순)
            sorted_events = sorted(
                filtered,
                key=lambda e: e["timestamp"],
                reverse=True,
            )
            # 제한
            return [e.copy() for e in sorted_events[:limit]]

    # ════════════════════════════════════════
    # 4. 관측 가능성
    # ════════════════════════════════════════

    async def list_active_agents(
        self,
        agent_name: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        """활성 에이전트 목록"""
        async with self._lock:
            if agent_name is None:
                return [m.copy() for m in self._agents.values()]
            return [
                m.copy() for m in self._agents.values()
                if m.get("agent_name") == agent_name
            ]

    async def count_agents(
        self,
        agent_name: Optional[str] = None,
    ) -> int:
        """에이전트 수 카운트"""
        async with self._lock:
            if agent_name is None:
                return len(self._agents)
            return sum(
                1 for m in self._agents.values()
                if m.get("agent_name") == agent_name
            )

    # ════════════════════════════════════════
    # 5. Repository 자체 관리
    # ════════════════════════════════════════

    async def health_check(self) -> dict[str, Any]:
        """헬스 체크"""
        start = datetime.now(timezone.utc)

        async with self._lock:
            agent_count = len(self._agents)
            stats_count = len(self._stats)
            event_count = len(self._lifecycle_events)

        elapsed_ms = int(
            (datetime.now(timezone.utc) - start).total_seconds() * 1000
        )

        return {
            "status": "healthy",
            "backend": "in_memory",
            "latency_ms": elapsed_ms,
            "registered_agents": agent_count,
            "tracked_stats": stats_count,
            "lifecycle_events": event_count,
            "warning": "in-memory backend - data lost on restart",
        }

    # ════════════════════════════════════════
    # 6. 테스트 헬퍼 (운영 환경 X)
    # ════════════════════════════════════════

    async def _clear_all(self) -> None:
        """모든 데이터 삭제 (테스트 전용)

        ⚠️ 운영 환경 절대 호출 X
        """
        async with self._lock:
            self._agents.clear()
            self._stats.clear()
            self._lifecycle_events.clear()
        logger.warning("InMemoryRepository: 모든 데이터 삭제됨 (테스트)")