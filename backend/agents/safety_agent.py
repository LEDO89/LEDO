"""
LEDO.ai - SafetyAgent (첫 진짜 에이전트)

건설 현장 작업자의 안전 상태를 평가하는 LLM 기반 에이전트.
BaseAgent 의 4개 격상 + LLMClient 모두 활용.

핵심 기능:
─────────────────────────────────────
1. 작업자 안전 데이터 입력 (헬멧/위치/작업)
2. LLM 안전 평가 (qwen2.5-coder:14b)
3. 구조화된 응답 (SafetyAssessment Pydantic)
4. 위험도 등급 (SAFE/CAUTION/WARNING/DANGER/CRITICAL)
5. Pub/Sub 자동 발행 (safety.assessment.*)
6. 변증법적 학습 기회 (DialecticAgent 연동)

확장성:
─────────────────────────────────────
- LoRA 어댑터: construction_safety_v3 (특화)
- 같은 코드, 다른 LoRA → 다양한 도메인:
  * crane_safety_v3 (크레인 작업)
  * welding_safety_v2 (용접)
  * humanoid_safety_v1 (휴머노이드)

산업 표준:
─────────────────────────────────────
- 한국 산업안전보건법 시행규칙 제33조
- OSHA Construction Safety Standards
- ISO 45001 (산업 안전 보건 관리 시스템)
- ConTech 안전 분류 체계

설계 원칙:
─────────────────────────────────────
1. Structured Output (Pydantic 검증)
2. Defensive Parsing (LLM 응답 안전 파싱)
3. Fail-Safe (LLM 실패 시 보수적 판정)
4. Auditable (모든 결정 추적)
5. Reactive (Pub/Sub 자동 발행)

Python 버전: 3.14+
"""
import json
import logging
import re
from datetime import datetime, timezone
from enum import Enum
from typing import Optional, Any

from pydantic import BaseModel, Field, ConfigDict, ValidationError

from config import settings
from ontology.classes import AccessLevel
from ontology.audit import AuditOutcome
from agents.base import BaseAgent, AgentResult
from agents.llm_client import (
    LLMClient,
    LLMResponse,
    LLMError,
    get_llm_client,
)
from agents.repositories.interface import AgentStateRepository
from agents.brokers.interface import MessageBroker, Message


logger = logging.getLogger(__name__)


# ════════════════════════════════════════════════════════════
# 1. 안전 등급 체계
# ════════════════════════════════════════════════════════════


class SafetyLevel(str, Enum):
    """안전 등급 (5단계)

    분류 기준:
    ─────────────
    SAFE     - 정상 작업 (모든 조건 충족)
    CAUTION  - 주의 필요 (경미한 위험 가능성)
    WARNING  - 경고 (즉각 개선 필요)
    DANGER   - 위험 (즉시 작업 중단 권장)
    CRITICAL - 매우 위급 (즉시 작업 중단 + 인명 위험)

    참조:
    - 한국 산업안전보건법 위험성 평가 5단계
    - OSHA Hazard Severity Levels
    - ISO 45001 Risk Assessment
    """
    SAFE = "safe"
    CAUTION = "caution"
    WARNING = "warning"
    DANGER = "danger"
    CRITICAL = "critical"


class SafetyConcern(str, Enum):
    """주요 안전 우려 사항"""
    HELMET_MISSING = "helmet_missing"
    HARNESS_MISSING = "harness_missing"
    DANGER_ZONE_ENTRY = "danger_zone_entry"
    FATIGUE = "fatigue"
    EQUIPMENT_MALFUNCTION = "equipment_malfunction"
    WEATHER_HAZARD = "weather_hazard"
    INSUFFICIENT_TRAINING = "insufficient_training"
    POLICY_VIOLATION = "policy_violation"
    OTHER = "other"


# ════════════════════════════════════════════════════════════
# 2. 안전 평가 결과 (Structured Output)
# ════════════════════════════════════════════════════════════


class SafetyAssessment(BaseModel):
    """안전 평가의 표준 결과 (LLM Structured Output)

    LLM 이 JSON 으로 반환하면 이 Pydantic 모델로 검증.
    """
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=False,
        frozen=True,
    )

    # 평가 결과
    safety_level: SafetyLevel = Field(
        ...,
        description="안전 등급 (safe/caution/warning/danger/critical)",
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="평가 신뢰도 (0.0-1.0)",
    )

    # 사유 (한국어)
    reasoning: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="평가 사유 (한국어, 상세)",
    )

    # 주요 우려 사항
    primary_concerns: list[SafetyConcern] = Field(
        default_factory=list,
        max_length=10,
        description="주요 안전 우려 사항 목록",
    )

    # 권장 조치
    recommended_actions: list[str] = Field(
        default_factory=list,
        max_length=10,
        description="권장 즉각 조치 목록",
    )

    # 즉각성
    requires_immediate_action: bool = Field(
        default=False,
        description="즉각 조치 필요 여부",
    )


# ════════════════════════════════════════════════════════════
# 3. 안전 평가 입력 (Type Safety)
# ════════════════════════════════════════════════════════════


class SafetyInput(BaseModel):
    """안전 평가 입력 데이터의 표준 형식"""
    model_config = ConfigDict(extra="forbid", frozen=True)

    # 작업자 정보
    worker_id: str = Field(
        ...,
        max_length=64,
        description="작업자 ID (예: 'W042')",
    )
    worker_role: Optional[str] = Field(
        default=None,
        max_length=128,
        description="작업자 역할 (예: 'crane_operator')",
    )

    # 안전 장비
    helmet_on: bool = Field(
        ...,
        description="안전모 착용 여부",
    )
    harness_on: Optional[bool] = Field(
        default=None,
        description="안전벨트 착용 여부 (해당 시)",
    )
    safety_vest_on: Optional[bool] = Field(
        default=None,
        description="안전 조끼 착용 여부",
    )

    # 위치 + 환경
    current_zone: str = Field(
        ...,
        max_length=128,
        description="현재 작업 구역 (예: 'DangerZone_001')",
    )
    zone_risk_level: Optional[str] = Field(
        default=None,
        max_length=32,
        description="구역 위험 등급 (low/medium/high)",
    )

    # 작업 상황
    current_task: Optional[str] = Field(
        default=None,
        max_length=256,
        description="현재 수행 작업",
    )
    work_duration_hours: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=24.0,
        description="현재 작업 시간 (피로도 계산용)",
    )

    # 환경 조건
    weather_condition: Optional[str] = Field(
        default=None,
        max_length=64,
        description="기상 상태 (예: 'rainy', 'windy')",
    )

    # 추가 컨텍스트
    additional_context: Optional[dict[str, Any]] = Field(
        default=None,
        description="추가 정보 (자유 형식)",
    )


# ════════════════════════════════════════════════════════════
# 4. SafetyAgent 본체
# ════════════════════════════════════════════════════════════


class SafetyAgent(BaseAgent):
    """건설 현장 작업자 안전 평가 에이전트

    BaseAgent 의 4개 격상 활용:
    ─────────────────────────────────────
    1. asyncio: 수천 동시 평가
    2. Repository: 통계 외부 저장
    3. Broker: Pub/Sub 자동 통신
    4. 자동 발행/구독: 라이프사이클 + 결과

    + LLMClient: 진짜 안전 평가

    자동 발행 토픽:
    ─────────────────────────────────────
    agent.safety.initialized
    agent.safety.shutdown
    agent.safety.result.success
    agent.safety.result.failure
    safety.assessment.<level>    ← 평가 결과별

    구독 가능 (커스터마이즈):
    ─────────────────────────────────────
    sensor.helmet.*    ← 헬멧 감지
    worker.position.*  ← 위치 변경
    equipment.*        ← 장비 이상

    사용 예시:
    ─────────────────────────────────────
        async with SafetyAgent(
            lora_adapter_id="construction_safety_v3",
            repository=pg_repo,
            broker=redis_broker,
        ) as agent:
            result = await agent.run({
                "worker_id": "W042",
                "helmet_on": False,
                "current_zone": "DangerZone_001",
                "current_task": "철근 조립",
            })
            
            # 결과:
            # - safety_level: warning/danger
            # - reasoning: "안전모 미착용 + 위험구역..."
            # - 자동 발행: agent.safety.result.success
            # - 자동 발행: safety.assessment.warning
    """

    # 시스템 프롬프트 (한국어, 도메인 특화)
    DEFAULT_SYSTEM_PROMPT = """당신은 한국 건설 현장의 안전 전문가입니다.
산업안전보건법과 OSHA 표준에 기반하여 작업자의 안전 상태를 평가합니다.

평가 시 고려 사항:
1. 개인 보호 장비 (안전모, 안전벨트, 안전 조끼)
2. 작업 구역의 위험 등급
3. 현재 작업의 위험성
4. 작업자의 피로도
5. 환경 조건 (기상, 시야)

응답은 반드시 다음 JSON 형식만 출력하세요:
{
  "safety_level": "safe|caution|warning|danger|critical",
  "confidence": 0.0-1.0 의 숫자,
  "reasoning": "평가 사유 (한국어, 100-500자)",
  "primary_concerns": ["우려 사항 ID 목록"],
  "recommended_actions": ["권장 조치 목록 (한국어)"],
  "requires_immediate_action": true 또는 false
}

primary_concerns 의 가능한 값:
- helmet_missing
- harness_missing
- danger_zone_entry
- fatigue
- equipment_malfunction
- weather_hazard
- insufficient_training
- policy_violation
- other

판정 기준:
- safe: 모든 조건 충족
- caution: 경미한 주의 사항
- warning: 즉각 개선 필요
- danger: 즉시 작업 중단 권장
- critical: 즉시 작업 중단 + 인명 위험

JSON 외 다른 텍스트는 출력하지 마세요."""

    def __init__(
        self,
        agent_name: str = "safety",
        lora_adapter_id: Optional[str] = "construction_safety_v3",
        repository: Optional[AgentStateRepository] = None,
        broker: Optional[MessageBroker] = None,
        llm_client: Optional[LLMClient] = None,
        system_prompt: Optional[str] = None,
    ) -> None:
        """SafetyAgent 초기화

        Args:
            agent_name: 에이전트 이름 (기본: 'safety')
            lora_adapter_id: LoRA 어댑터 (도메인 특화)
                기본: 'construction_safety_v3'
                * Ollama 에 실제 LoRA 없으면 base 모델 사용
            repository: 상태 저장소
            broker: 메시지 브로커
            llm_client: LLM 클라이언트 (기본: 글로벌 싱글톤)
            system_prompt: 커스텀 시스템 프롬프트
        """
        super().__init__(
            agent_name=agent_name,
            agent_class="SafetyAgent",
            version="1.0.0",
            access_level=AccessLevel.INTERNAL,
            can_modify_ontology=False,  # 안전 평가는 온톨로지 변경 X
            lora_adapter_id=lora_adapter_id,
            repository=repository,
            broker=broker,
        )

        # LLM 클라이언트 (글로벌 공유 가능)
        self._llm_client: LLMClient = llm_client or get_llm_client()

        # 시스템 프롬프트
        self._system_prompt: str = (
            system_prompt or self.DEFAULT_SYSTEM_PROMPT
        )

        # 통계 (Repository 외 추가)
        self._safety_level_counts: dict[str, int] = {
            level.value: 0 for level in SafetyLevel
        }

    # ════════════════════════════════════════
    # 라이프사이클 훅 (선택적)
    # ════════════════════════════════════════

    async def _on_initialize(self) -> None:
        """초기화 시 추가 작업

        ⭐ LLM 헬스 체크 (Ollama 작동 확인)
        """
        try:
            health = await self._llm_client.health_check()
            if health.get("status") != "healthy":
                self._logger.warning(
                    f"LLM 서버 비정상: {health}"
                )
            else:
                self._logger.info(
                    f"LLM 서버 정상: "
                    f"version={health.get('ollama_version')}, "
                    f"model={health.get('model_id')}"
                )
        except Exception as e:
            self._logger.warning(
                f"LLM 헬스 체크 실패 (계속 진행): {e}"
            )

    # ════════════════════════════════════════
    # 핵심: process 구현
    # ════════════════════════════════════════

    async def process(self, input_data: dict[str, Any]) -> AgentResult:
        """안전 평가 실행 (LLM 호출)

        흐름:
            1. 입력 검증 (SafetyInput Pydantic)
            2. 프롬프트 구성
            3. LLM 호출
            4. 응답 JSON 파싱
            5. SafetyAssessment 검증
            6. Pub/Sub 발행 (safety.assessment.<level>)
            7. AgentResult 반환

        Args:
            input_data: 안전 평가 입력 데이터

        Returns:
            AgentResult (output 에 SafetyAssessment 포함)
        """
        try:
            # 1. 입력 검증 (Pydantic)
            safety_input = SafetyInput(**input_data)

            # 2. 프롬프트 구성
            user_prompt = self._build_user_prompt(safety_input)

            # 3. LLM 호출
            llm_response = await self._llm_client.generate(
                prompt=user_prompt,
                system_prompt=self._system_prompt,
                lora_adapter_id=self.metadata.lora_adapter_id,
                temperature=0.3,  # 안전 평가는 일관성 중요
                max_tokens=1000,
            )

            # 4. JSON 파싱 (방어적)
            assessment_data = self._parse_llm_response(llm_response.content)

            # 5. SafetyAssessment 검증
            assessment = SafetyAssessment(**assessment_data)

            # 6. 통계 업데이트
            self._safety_level_counts[assessment.safety_level] += 1

            # 7. Pub/Sub 자동 발행 (안전 등급별)
            await self.publish(
                topic=f"safety.assessment.{assessment.safety_level}",
                payload={
                    "worker_id": safety_input.worker_id,
                    "safety_level": assessment.safety_level,
                    "confidence": assessment.confidence,
                    "requires_immediate_action": assessment.requires_immediate_action,
                    "concerns_count": len(assessment.primary_concerns),
                },
            )

            # 8. 위급 상황 별도 발행 (Critical/Danger)
            if assessment.requires_immediate_action:
                await self.publish(
                    topic="safety.alert.critical",
                    payload={
                        "worker_id": safety_input.worker_id,
                        "current_zone": safety_input.current_zone,
                        "safety_level": assessment.safety_level,
                        "reasoning": assessment.reasoning,
                        "recommended_actions": assessment.recommended_actions,
                    },
                )

            self._logger.info(
                f"안전 평가 완료: worker={safety_input.worker_id}, "
                f"level={assessment.safety_level}, "
                f"confidence={assessment.confidence:.2f}"
            )

            # 9. AgentResult 반환
            return AgentResult(
                agent_id=self.metadata.agent_id,
                outcome=AuditOutcome.SUCCESS,
                output={
                    "worker_id": safety_input.worker_id,
                    "assessment": assessment.model_dump(),
                    "llm_metadata": {
                        "model_id": llm_response.model_id,
                        "input_tokens": llm_response.input_tokens,
                        "output_tokens": llm_response.output_tokens,
                        "response_time_ms": llm_response.response_time_ms,
                    },
                },
                llm_tokens_used=llm_response.total_tokens,
            )

        except ValidationError as e:
            # 입력/응답 검증 실패
            self._logger.error(f"검증 실패: {e}")
            return self._make_error_result(
                input_data,
                f"검증 실패: {str(e)[:300]}",
            )

        except LLMError as e:
            # LLM 호출 실패
            self._logger.error(f"LLM 호출 실패: {e}")
            return self._make_error_result(
                input_data,
                f"LLM 실패: {type(e).__name__}: {str(e)[:200]}",
            )

        except Exception as e:
            # 예상 외 에러
            self._logger.error(
                f"예상 외 에러: {type(e).__name__}: {e}"
            )
            return self._make_error_result(
                input_data,
                f"내부 에러: {type(e).__name__}: {str(e)[:200]}",
            )

    # ════════════════════════════════════════
    # 헬퍼: 프롬프트 구성
    # ════════════════════════════════════════

    def _build_user_prompt(self, input: SafetyInput) -> str:
        """사용자 프롬프트 구성 (한국어)

        구조화된 입력 → 자연어 설명
        """
        lines = [
            f"## 작업자 안전 평가 요청",
            f"",
            f"### 작업자 정보",
            f"- ID: {input.worker_id}",
        ]

        if input.worker_role:
            lines.append(f"- 역할: {input.worker_role}")

        lines.extend([
            f"",
            f"### 안전 장비",
            f"- 안전모: {'착용' if input.helmet_on else '미착용 ⚠️'}",
        ])

        if input.harness_on is not None:
            lines.append(
                f"- 안전벨트: {'착용' if input.harness_on else '미착용 ⚠️'}"
            )

        if input.safety_vest_on is not None:
            lines.append(
                f"- 안전조끼: {'착용' if input.safety_vest_on else '미착용'}"
            )

        lines.extend([
            f"",
            f"### 위치 + 환경",
            f"- 현재 구역: {input.current_zone}",
        ])

        if input.zone_risk_level:
            lines.append(f"- 구역 위험도: {input.zone_risk_level}")

        if input.current_task:
            lines.append(f"- 현재 작업: {input.current_task}")

        if input.work_duration_hours is not None:
            lines.append(
                f"- 작업 시간: {input.work_duration_hours:.1f}시간"
            )

        if input.weather_condition:
            lines.append(f"- 기상 상태: {input.weather_condition}")

        if input.additional_context:
            lines.append(f"")
            lines.append(f"### 추가 정보")
            for k, v in input.additional_context.items():
                lines.append(f"- {k}: {v}")

        lines.extend([
            f"",
            f"위 정보를 바탕으로 작업자의 안전 상태를 평가하고 JSON 으로 응답하세요.",
        ])

        return "\n".join(lines)

    # ════════════════════════════════════════
    # 헬퍼: LLM 응답 파싱 (방어적)
    # ════════════════════════════════════════

    def _parse_llm_response(self, content: str) -> dict[str, Any]:
        """LLM 응답에서 JSON 추출 (방어적 파싱)

        LLM 이 종종 JSON 외 텍스트도 반환:
            "다음과 같이 평가합니다:
`````json
             {...}
`````
             추가 설명..."

        → 정규식으로 JSON 부분만 추출

        Args:
            content: LLM 응답 전체

        Returns:
            파싱된 dict

        Raises:
            ValueError: JSON 추출/파싱 실패
        """
        if not content or not content.strip():
            raise ValueError("LLM 응답이 비어있음")

        # 1. 직접 JSON 시도
        content_stripped = content.strip()
        if content_stripped.startswith("{") and content_stripped.endswith("}"):
            try:
                return json.loads(content_stripped)
            except json.JSONDecodeError:
                pass

        # 2. ```json ... ``` 블록 추출
        json_block_pattern = r"```(?:json)?\s*(\{.*?\})\s*```"
        match = re.search(json_block_pattern, content, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass

        # 3. 첫 { 부터 마지막 } 까지 추출
        first_brace = content.find("{")
        last_brace = content.rfind("}")
        if first_brace != -1 and last_brace != -1 and first_brace < last_brace:
            json_text = content[first_brace : last_brace + 1]
            try:
                return json.loads(json_text)
            except json.JSONDecodeError as e:
                raise ValueError(
                    f"JSON 파싱 실패: {e}, 추출된 텍스트: {json_text[:200]}"
                )

        raise ValueError(
            f"JSON 형식을 찾을 수 없음. 응답: {content[:300]}"
        )

    # ════════════════════════════════════════
    # 헬퍼: 에러 결과 생성
    # ════════════════════════════════════════

    def _make_error_result(
        self,
        input_data: dict[str, Any],
        error_message: str,
    ) -> AgentResult:
        """에러 발생 시 보수적 결과 반환 (Fail-Safe)

        ⚠️ 핵심 원칙:
           안전 시스템이 실패하면 → 보수적 판정 (WARNING 이상)
           = "확실하지 않으면 안전 측"
        """
        worker_id = input_data.get("worker_id", "unknown")

        return AgentResult(
            agent_id=self.metadata.agent_id,
            outcome=AuditOutcome.FAILURE,
            output={
                "worker_id": worker_id,
                "fallback_assessment": {
                    "safety_level": SafetyLevel.WARNING.value,
                    "confidence": 0.0,
                    "reasoning": f"평가 시스템 오류 - 보수적 판정 적용 ({error_message})",
                    "requires_immediate_action": True,
                },
            },
            error_message=error_message,
        )

    # ════════════════════════════════════════
    # 외부 API (관측 가능성)
    # ════════════════════════════════════════

    def get_safety_level_distribution(self) -> dict[str, int]:
        """평가된 안전 등급의 분포 통계

        Returns:
            {safety_level: count} dict

        ⭐ 운영 활용:
           "오늘 critical 평가 몇 건?"
           "주중 warning 비율 추이?"
        """
        return self._safety_level_counts.copy()