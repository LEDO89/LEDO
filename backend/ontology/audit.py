"""
LEDO.ai - 이중 감사 시스템 (Dual Audit Architecture)

이 모듈은 LEDO 시스템의 모든 결정과 변경을 두 가지 패러다임으로 기록한다:

레인 1: RDB (PostgreSQL audit_log 테이블)
  - 빠른 SQL 조회
  - 시간 범위 검색, actor 필터링, 토큰 비용 추적
  - 산업 표준 로그 관리

레인 2: PROV-O 트리플 (RDF Quad Store)
  - 관계 그래프 SPARQL 추적
  - "이 결정이 어떤 데이터에서 어떤 에이전트가 어떤 컨텍스트로"
  - W3C 표준 시맨틱 호환

설계 원칙:
─────────────────────────────────────
1. Write-Once (감사 기록은 절대 수정 X)
2. Append-Only (추가만, 삭제 X)
3. Fail-Safe (한 레인 실패해도 다른 레인 계속)
4. PII Aware (개인정보 자동 마스킹)
5. LLM Context (모든 LLM 결정의 입력 스냅샷 보존)

참조 표준:
─────────────────────────────────────
- W3C PROV-O (Provenance Ontology, 2013)
- NIST SP 800-92 (Guide to Computer Security Log Management)
- ISO/IEC 27037 (Digital Evidence Identification)
- GDPR Article 5(1)(f) (Integrity and Confidentiality)
- 한국 산업안전보건법 시행규칙 제33조 (7년 보존)
- 한국 개인정보보호법 제29조 (안전조치 의무)

저작자: LEDO.ai Team
초기 발행: 2026-06
Python 버전: 3.14+
"""
from enum import Enum
from datetime import datetime, timezone
from typing import Optional, Any
from uuid import uuid4

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    field_validator,
    model_validator,
)

from config import settings
from ontology.namespaces import LEDO, PROV
from ontology.classes import AccessLevel, OntologyMetadata

# ════════════════════════════════════════════════════════════
# 1. 감사 사건 분류 체계 (Audit Event Taxonomy)
# ════════════════════════════════════════════════════════════
# 모든 시스템 활동을 표준 카테고리로 분류
# 5년 후 SQL 조회 시: WHERE event_type = 'llm_decision' ← 이런 식으로


class AuditEventType(str, Enum):
    """감사 사건의 표준 분류 (NIST SP 800-92 기반)

    8개 카테고리로 모든 LEDO 시스템 활동 포괄:
    ─────────────────────────────────────
    LLM_DECISION       - LLM 의 의사결정 (가장 자주 발생)
    ONTOLOGY_CHANGE    - 온톨로지 구조 변경 (변증법)
    DATA_ACCESS        - 데이터 조회/접근
    DATA_MODIFICATION  - 데이터 생성/수정/삭제
    ALARM_TRIGGERED    - 안전 경보 발동
    AUTHORIZATION      - 권한 부여/거부
    SYSTEM_LIFECYCLE   - 시스템 시작/종료/재시작
    EXTERNAL_API       - 외부 시스템 호출

    참조 표준:
    - NIST SP 800-92 (Log Management)
    - ISO/IEC 27037 (Digital Evidence)
    - OWASP Logging Cheat Sheet
    """
    LLM_DECISION = "llm_decision"
    ONTOLOGY_CHANGE = "ontology_change"
    DATA_ACCESS = "data_access"
    DATA_MODIFICATION = "data_modification"
    ALARM_TRIGGERED = "alarm_triggered"
    AUTHORIZATION = "authorization"
    SYSTEM_LIFECYCLE = "system_lifecycle"
    EXTERNAL_API = "external_api"


class AuditOutcome(str, Enum):
    """감사 사건의 결과 분류

    SUCCESS    - 정상 완료
    FAILURE    - 실패 (예외, 오류)
    DENIED     - 권한 거부
    PARTIAL    - 부분 성공 (일부 실패)
    PENDING    - 진행 중 (비동기 작업)

    ⭐ NIST 권장 5단계:
       단순 success/failure 만으론 부족
       산업 안전 시스템엔 5단계 필요
    """
    SUCCESS = "success"
    FAILURE = "failure"
    DENIED = "denied"
    PARTIAL = "partial"
    PENDING = "pending"


class AuditSeverity(str, Enum):
    """감사 사건의 심각도 (RFC 5424 Syslog 기반)

    EMERGENCY - 시스템 불가능 (즉시 인간 개입)
    ALERT     - 즉각 조치 필요
    CRITICAL  - 위급 상황
    ERROR     - 오류 (운영 영향)
    WARNING   - 경고 (잠재 위험)
    NOTICE    - 주목할 정상 사건
    INFO      - 정보성 (대부분)
    DEBUG     - 디버그 (개발용)

    참조: RFC 5424 (The Syslog Protocol)
    """
    EMERGENCY = "emergency"
    ALERT = "alert"
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    NOTICE = "notice"
    INFO = "info"
    DEBUG = "debug"


# ════════════════════════════════════════════════════════════
# 2. AuditEvent: 감사 사건의 핵심 모델
# ════════════════════════════════════════════════════════════
# 모든 시스템 활동이 이 모델로 변환되어 두 레인에 기록됨
# Write-Once + Append-Only (변경 절대 불가)


class AuditEvent(BaseModel):
    """단일 감사 사건의 완전한 구조화된 표현

    이 모델 인스턴스 하나가:
      1. PostgreSQL audit_log 테이블의 1 row
      2. RDF Quad Store 의 PROV-O 트리플 집합
    두 곳에 동시 기록된다.

    핵심 설계 원칙:
    ─────────────────────────────────────
    1. Immutable (frozen=True - 한번 생성 후 변경 X)
    2. Self-Identifying (UUID v4 자동 생성)
    3. UTC 시간 (분산 시스템 일관성)
    4. PII Aware (개인정보 자동 마스킹 플래그)
    5. Standards-Aligned (PROV-O + NIST + RFC 5424)
    6. LLM Context (입력 스냅샷 영구 보존)
    7. Causal Chain (parent_event_id 로 인과 관계 추적)

    참조 표준:
    - W3C PROV-O (provenance model)
    - NIST SP 800-92 (Log Management)
    - ISO/IEC 27037 (Digital Evidence)
    - RFC 5424 (Syslog Protocol)
    """
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=False,
        use_enum_values=True,
        str_strip_whitespace=True,
        frozen=True,
        json_schema_extra={
            "examples": [
                {
                    "event_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                    "event_type": "llm_decision",
                    "outcome": "success",
                    "severity": "info",
                    "actor": "agent:safety",
                    "subject_iri": "http://ledo.ai/ontology/2026/06/Worker_042",
                }
            ]
        },
    )

    # ════════════════════════════════════════
    # 1. 사건 식별 (Event Identity)
    # 한번 생성되면 영구 불변
    # ════════════════════════════════════════
    event_id: str = Field(
        default_factory=lambda: str(uuid4()),
        pattern=r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$",
        description="UUID v4 - 전 세계 unique 사건 식별자",
    )
    timestamp_utc: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="사건 발생 시각 (UTC, ISO 8601, 마이크로초 정밀도)",
    )

    # ════════════════════════════════════════
    # 2. 사건 분류 (Classification)
    # 블록 2 의 3개 Enum 활용
    # ════════════════════════════════════════
    event_type: AuditEventType = Field(
        ...,
        description="사건 종류 (LLM 결정, 데이터 접근, 알람 등)",
    )
    outcome: AuditOutcome = Field(
        ...,
        description="사건 결과 (성공, 실패, 권한거부, 부분, 진행중)",
    )
    severity: AuditSeverity = Field(
        default=AuditSeverity.INFO,
        description="심각도 (RFC 5424 8단계, 기본 INFO)",
    )

    # ════════════════════════════════════════
    # 3. 행위자 (Actor - 누가)
    # 블록 4 의 OntologyMetadata 와 동일 형식
    # ════════════════════════════════════════
    actor: str = Field(
        ...,
        min_length=1,
        max_length=128,
        description="사건 발생시킨 주체 (system | human:<id> | agent:<name>)",
    )
    actor_session_id: Optional[str] = Field(
        default=None,
        max_length=128,
        description="actor 의 세션 ID (분산 추적용)",
    )

    # ════════════════════════════════════════
    # 4. 대상 (Subject - 무엇에)
    # ════════════════════════════════════════
    subject_iri: Optional[str] = Field(
        default=None,
        max_length=512,
        description="사건 대상 엔티티의 IRI (Worker_042 등)",
    )
    subject_class: Optional[str] = Field(
        default=None,
        pattern=r"^[A-Z][a-zA-Z0-9_]*$",
        description="대상의 OntologyClass 이름 (Worker, Equipment 등)",
    )

    # ════════════════════════════════════════
    # 5. 활동 (Action - 무엇을)
    # ════════════════════════════════════════
    action: str = Field(
        ...,
        min_length=1,
        max_length=256,
        description="구체적 활동 (예: 'detect_helmet_off', 'modify_position')",
    )
    action_parameters: dict[str, Any] = Field(
        default_factory=dict,
        description="활동의 입력 매개변수 (JSON 직렬화 가능)",
    )

    # ════════════════════════════════════════
    # 6. LLM 컨텍스트 (LLM Decision Audit)
    # ⭐ 본인의 핵심 요청 사항 #2
    # ════════════════════════════════════════
    llm_model_id: Optional[str] = Field(
        default=None,
        max_length=128,
        description="결정한 LLM 모델 (예: qwen2.5-coder:14b)",
    )
    llm_input_snapshot: Optional[dict[str, Any]] = Field(
        default=None,
        description="LLM 입력의 완전 스냅샷 (prompt + system + tools)",
    )
    llm_input_token_count: Optional[int] = Field(
        default=None,
        ge=0,
        le=131072,
        description="입력 토큰 수 (비용 + 성능 추적)",
    )
    llm_output_token_count: Optional[int] = Field(
        default=None,
        ge=0,
        le=131072,
        description="출력 토큰 수",
    )
    llm_response_time_ms: Optional[int] = Field(
        default=None,
        ge=0,
        le=600000,
        description="LLM 응답 시간 (밀리초, 최대 10분)",
    )
    llm_temperature: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=2.0,
        description="LLM temperature 파라미터 (재현성)",
    )

    # ════════════════════════════════════════
    # 7. PROV-O 관계형 감사 (블록 4 에서 활용)
    # ⭐ 본인의 핵심 요청 사항 #3
    # ════════════════════════════════════════
    prov_used_entities: list[str] = Field(
        default_factory=list,
        max_length=64,
        description="이 사건이 참조한 다른 엔티티들의 IRI 목록",
    )
    prov_generated_entities: list[str] = Field(
        default_factory=list,
        max_length=64,
        description="이 사건이 생성/수정한 엔티티들의 IRI 목록",
    )
    prov_derived_from: Optional[str] = Field(
        default=None,
        max_length=512,
        description="이 사건의 출처 (다른 사건이나 데이터)",
    )

    # ════════════════════════════════════════
    # 8. 인과 관계 (Causality Chain)
    # 사건들의 사슬 추적
    # ════════════════════════════════════════
    parent_event_id: Optional[str] = Field(
        default=None,
        pattern=r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$",
        description="이 사건을 발생시킨 부모 사건의 UUID",
    )
    correlation_id: Optional[str] = Field(
        default=None,
        max_length=128,
        description="관련 사건들의 그룹 ID (분산 추적용)",
    )

    # ════════════════════════════════════════
    # 9. 보안 + 개인정보 (Privacy Aware)
    # ════════════════════════════════════════
    access_level: AccessLevel = Field(
        default=AccessLevel.AUDIT_ONLY,
        description="이 감사 기록의 접근 권한 (기본 AUDIT_ONLY)",
    )
    contains_pii: bool = Field(
        default=False,
        description="이 사건에 개인정보 포함 여부 (자동 마스킹용)",
    )
    pii_masked_fields: list[str] = Field(
        default_factory=list,
        description="마스킹된 필드 이름 목록 (감사용)",
    )

    # ════════════════════════════════════════
    # 10. 운영 메타정보 (Operational)
    # ════════════════════════════════════════
    environment: str = Field(
        default_factory=lambda: settings.LEDO_ENV,
        max_length=32,
        description="발생 환경 (development | staging | production)",
    )
    host_node: Optional[str] = Field(
        default=None,
        max_length=128,
        description="발생 노드 (분산 시스템에서 어느 서버)",
    )
    error_message: Optional[str] = Field(
        default=None,
        max_length=2048,
        description="실패 시 에러 메시지 (FAILURE outcome 일 때)",
    )

    # ════════════════════════════════════════
    # 11. Validators (산업 표준 일관성)
    # ════════════════════════════════════════
    @field_validator("actor")
    @classmethod
    def validate_actor_format(cls, v: str) -> str:
        """actor ID 형식 검증 (OntologyMetadata 와 동일 규칙)"""
        if v == "system":
            return v

        if not (v.startswith("human:") or v.startswith("agent:")):
            raise ValueError(
                f"actor '{v}' 는 'system' 또는 'human:<id>' "
                f"또는 'agent:<name>' 형식이어야 함"
            )

        identifier = v.split(":", 1)[1]
        if not identifier or not identifier.replace("_", "").replace("-", "").isalnum():
            raise ValueError(
                f"actor 식별자 '{identifier}' 는 영숫자/언더스코어/하이픈만 허용"
            )

        return v

    @field_validator("subject_iri")
    @classmethod
    def validate_subject_iri(cls, v: Optional[str]) -> Optional[str]:
        """subject_iri 형식 검증 (있을 때만)"""
        if v is None:
            return v
        if not (v.startswith("http://") or v.startswith("https://")):
            raise ValueError(
                f"subject_iri '{v}' 는 http:// 또는 https:// 로 시작해야 함"
            )
        return v

    @model_validator(mode="after")
    def validate_event_consistency(self) -> "AuditEvent":
        """사건 전체 일관성 검증 (필드 간 비즈니스 규칙)

        규칙:
        1. FAILURE 결과는 error_message 필수
        2. LLM_DECISION 사건은 llm_model_id 필수
        3. PII 포함이면 access_level >= RESTRICTED
        4. ALARM_TRIGGERED 는 severity >= WARNING
        5. 시간이 미래일 수 없음 (5초 허용 - 시계 오차)
        6. parent_event_id == event_id 불가 (자기 참조 차단)
        """
        # 1. 실패 사건은 에러 메시지 필수
        if self.outcome == AuditOutcome.FAILURE.value and not self.error_message:
            raise ValueError(
                "FAILURE outcome 인 사건은 error_message 필수"
            )

        # 2. LLM 결정 사건은 모델 정보 필수
        if (
            self.event_type == AuditEventType.LLM_DECISION.value
            and self.llm_model_id is None
        ):
            raise ValueError(
                "LLM_DECISION 사건은 llm_model_id 필수 (감사 추적)"
            )

        # 3. PII 보호 - 권한 강화
        if self.contains_pii and self.access_level == AccessLevel.PUBLIC.value:
            raise ValueError(
                "PII 포함 사건은 PUBLIC 권한 불가 "
                "(GDPR + 한국 개인정보보호법)"
            )

        # 4. 알람은 적절한 심각도
        if self.event_type == AuditEventType.ALARM_TRIGGERED.value:
            allowed_severities = {
                AuditSeverity.WARNING.value,
                AuditSeverity.ERROR.value,
                AuditSeverity.CRITICAL.value,
                AuditSeverity.ALERT.value,
                AuditSeverity.EMERGENCY.value,
                AuditSeverity.NOTICE.value,
            }
            if self.severity not in allowed_severities:
                raise ValueError(
                    f"ALARM_TRIGGERED 사건의 severity 는 NOTICE 이상이어야 함. "
                    f"현재: {self.severity}"
                )

        # 5. 시간 검증 (미래 시간 차단, 5초 시계 오차 허용)
        now = datetime.now(timezone.utc)
        if self.timestamp_utc > now and (self.timestamp_utc - now).total_seconds() > 5:
            raise ValueError(
                "timestamp_utc 가 미래 (5초 시계 오차 한도 초과)"
            )

        # 6. 자기 참조 차단
        if self.parent_event_id == self.event_id:
            raise ValueError(
                "parent_event_id 가 event_id 와 같음 (자기 참조 불가)"
            )

        return self
    

# ════════════════════════════════════════════════════════════
# 3. ProvOAudit: PROV-O 트리플 생성 엔진
# ════════════════════════════════════════════════════════════
# AuditEvent 를 W3C PROV-O 표준 RDF 트리플로 변환
# RDF Quad Store 에 저장되어 SPARQL 쿼리 가능
#
# PROV-O 핵심 3 클래스:
#   prov:Entity   = 데이터/개체 (Worker, Equipment, ...)
#   prov:Activity = 활동 (감사 사건)
#   prov:Agent    = 행위자 (system, human, agent)
#
# 표준 매핑:
#   AuditEvent.event_id    → prov:Activity 의 IRI
#   AuditEvent.actor       → prov:Agent 의 IRI
#   AuditEvent.subject_iri → prov:Entity 의 IRI
#   AuditEvent.timestamp   → prov:startedAtTime / endedAtTime


from rdflib import Graph, Literal, URIRef, BNode
from rdflib.namespace import RDF, RDFS, XSD


class ProvOAudit:
    """W3C PROV-O 표준 트리플 생성기

    이 클래스는 AuditEvent 인스턴스를 받아
    PROV-O 호환 RDF 트리플 집합을 생성한다.

    생성된 트리플:
    ─────────────────────────────────────
    1. Activity 트리플 (사건 자체)
       <event_iri> a prov:Activity ;
                   prov:startedAtTime "2026-06-10T14:30:00Z" ;
                   ledo:eventType "llm_decision" .

    2. Agent 트리플 (행위자)
       <agent_iri> a prov:Agent ;
                   rdfs:label "agent:safety" .

    3. wasAssociatedWith 관계
       <event_iri> prov:wasAssociatedWith <agent_iri> .

    4. used 관계 (참조 엔티티)
       <event_iri> prov:used <entity_iri_1>, <entity_iri_2> .

    5. generated 관계 (생성 엔티티)
       <event_iri> prov:generated <entity_iri_3> .

    6. wasInformedBy 관계 (인과 사슬)
       <event_iri> prov:wasInformedBy <parent_event_iri> .

    참조 표준:
    - W3C PROV-O 1.0 (Recommendation, 2013)
    - W3C PROV-DM (Data Model, 2013)
    - RDF 1.1 Concepts (W3C 2014)
    """

    def __init__(self) -> None:
        """ProvOAudit 초기화 - 빈 그래프 생성

        graph: rdflib.Graph 인스턴스 (인메모리 RDF 저장소)
        모든 네임스페이스 자동 등록 (namespaces.py 의 ALL_NAMESPACES)
        """
        self.graph: Graph = Graph()
        self._bind_namespaces()

    def _bind_namespaces(self) -> None:
        """모든 표준 네임스페이스를 그래프에 등록

        등록된 prefix 들이 Turtle 출력 시 짧은 표기로 표시됨:
            ledo:Worker_042 (전체 IRI 대신)
            prov:Activity   (전체 IRI 대신)

        ⭐ namespaces.py 의 bind_to_graph 와 동일 원리
        """
        from ontology.namespaces import bind_to_graph
        bind_to_graph(self.graph)

    def event_to_triples(self, event: AuditEvent) -> Graph:
        """AuditEvent 를 PROV-O 트리플 집합으로 변환

        Args:
            event: 변환할 AuditEvent 인스턴스

        Returns:
            트리플이 추가된 rdflib.Graph

        ⭐ 이 함수가 audit.py 의 진짜 심장
           Pydantic 모델 → W3C PROV-O 표준 RDF
        """
        # 사건의 고유 IRI 생성
        event_iri = self._make_event_iri(event.event_id)
        agent_iri = self._make_agent_iri(event.actor)

        # 1. Activity 트리플 (사건 자체)
        self._add_activity_triples(event, event_iri)

        # 2. Agent 트리플 (행위자)
        self._add_agent_triples(event, agent_iri)

        # 3. 관계: 활동 -[수행]- 행위자
        self.graph.add((event_iri, PROV.wasAssociatedWith, agent_iri))

        # 4. 관계: 활동 -[참조]- 엔티티들
        self._add_used_relations(event, event_iri)

        # 5. 관계: 활동 -[생성]- 엔티티들
        self._add_generated_relations(event, event_iri)

        # 6. 관계: 활동 -[원인]- 부모 활동
        self._add_causality_relations(event, event_iri)

        # 7. 관계: 활동 -[대상]- 주체 엔티티
        if event.subject_iri:
            subject_iri_ref = URIRef(event.subject_iri)
            self.graph.add((event_iri, PROV.used, subject_iri_ref))

        return self.graph

    def _make_event_iri(self, event_id: str) -> URIRef:
        """사건 UUID 로부터 IRI 생성

        예시:
            event_id = "f47ac10b-58cc-4372-a567-0e02b2c3d479"
            결과:    <http://ledo.ai/ontology/2026/06/Activity_f47ac10b-58cc-4372-a567-0e02b2c3d479>
        """
        return URIRef(f"{LEDO}Activity_{event_id}")

    def _make_agent_iri(self, actor: str) -> URIRef:
        """actor 문자열로부터 Agent IRI 생성

        형식 변환:
            "system"        → ledo:Agent_system
            "agent:safety"  → ledo:Agent_safety
            "human:lee_001" → ledo:Agent_lee_001

        actor 의 prefix (system/human/agent) 가 LEDO 내부 IRI 로 변환
        """
        if actor == "system":
            identifier = "system"
        elif ":" in actor:
            identifier = actor.split(":", 1)[1]
        else:
            identifier = actor

        return URIRef(f"{LEDO}Agent_{identifier}")

    def _add_activity_triples(
        self,
        event: AuditEvent,
        event_iri: URIRef,
    ) -> None:
        """사건 자체에 대한 트리플 추가

        생성되는 트리플:
            <event_iri> a prov:Activity .
            <event_iri> prov:startedAtTime "2026-06-10T14:30:00Z"^^xsd:dateTime .
            <event_iri> ledo:eventType "llm_decision" .
            <event_iri> ledo:outcome "success" .
            <event_iri> ledo:severity "info" .
            <event_iri> rdfs:label "evaluate_helmet_status" .
        """
        # 1. 타입 명시 (prov:Activity)
        self.graph.add((event_iri, RDF.type, PROV.Activity))

        # 2. 시간 (xsd:dateTime 타입 강제)
        timestamp_literal = Literal(
            event.timestamp_utc.isoformat(),
            datatype=XSD.dateTime,
        )
        self.graph.add((event_iri, PROV.startedAtTime, timestamp_literal))

        # 3. LEDO 확장 속성: 사건 분류
        self.graph.add((
            event_iri,
            LEDO.eventType,
            Literal(event.event_type),
        ))
        self.graph.add((
            event_iri,
            LEDO.outcome,
            Literal(event.outcome),
        ))
        self.graph.add((
            event_iri,
            LEDO.severity,
            Literal(event.severity),
        ))

        # 4. 사람이 읽기 쉬운 라벨 (action 활용)
        self.graph.add((
            event_iri,
            RDFS.label,
            Literal(event.action, lang="ko"),
        ))

        # 5. LLM 결정 사건이면 모델 정보 추가
        if event.llm_model_id:
            self.graph.add((
                event_iri,
                LEDO.llmModelId,
                Literal(event.llm_model_id),
            ))
            if event.llm_input_token_count is not None:
                self.graph.add((
                    event_iri,
                    LEDO.llmInputTokens,
                    Literal(
                        event.llm_input_token_count,
                        datatype=XSD.integer,
                    ),
                ))

    def _add_agent_triples(
        self,
        event: AuditEvent,
        agent_iri: URIRef,
    ) -> None:
        """행위자 (Agent) 에 대한 트리플 추가

        생성되는 트리플:
            <agent_iri> a prov:Agent .
            <agent_iri> rdfs:label "agent:safety" .
            <agent_iri> ledo:actorType "agent" .  (또는 "human", "system")
        """
        # 1. 타입 명시
        self.graph.add((agent_iri, RDF.type, PROV.Agent))

        # 2. 라벨 (원래 actor 문자열)
        self.graph.add((
            agent_iri,
            RDFS.label,
            Literal(event.actor),
        ))

        # 3. actor 타입 추출 (system / human / agent)
        if event.actor == "system":
            actor_type = "system"
        elif ":" in event.actor:
            actor_type = event.actor.split(":", 1)[0]
        else:
            actor_type = "unknown"

        self.graph.add((
            agent_iri,
            LEDO.actorType,
            Literal(actor_type),
        ))

    def _add_used_relations(
        self,
        event: AuditEvent,
        event_iri: URIRef,
    ) -> None:
        """이 사건이 참조한 엔티티들에 대한 PROV-O 관계 추가

        생성되는 트리플:
            <event_iri> prov:used <entity_iri_1> .
            <event_iri> prov:used <entity_iri_2> .

        PROV-O 의미:
            "이 활동이 이 엔티티들을 활용/참조했다"
        """
        for entity_iri_str in event.prov_used_entities:
            entity_ref = URIRef(entity_iri_str)
            self.graph.add((event_iri, PROV.used, entity_ref))

    def _add_generated_relations(
        self,
        event: AuditEvent,
        event_iri: URIRef,
    ) -> None:
        """이 사건이 생성한 엔티티들에 대한 PROV-O 관계 추가

        생성되는 트리플:
            <event_iri> prov:generated <entity_iri_1> .
            <event_iri> prov:generated <entity_iri_2> .

        PROV-O 의미:
            "이 활동의 결과로 이 엔티티들이 생성/수정되었다"
        """
        for entity_iri_str in event.prov_generated_entities:
            entity_ref = URIRef(entity_iri_str)
            self.graph.add((event_iri, PROV.generated, entity_ref))

    def _add_causality_relations(
        self,
        event: AuditEvent,
        event_iri: URIRef,
    ) -> None:
        """인과 사슬 (parent_event_id) 에 대한 PROV-O 관계

        생성되는 트리플:
            <event_iri> prov:wasInformedBy <parent_event_iri> .

        PROV-O 의미:
            "이 활동이 부모 활동의 영향을 받았다"
            = 인과 관계 (causality)
        """
        if event.parent_event_id:
            parent_iri = self._make_event_iri(event.parent_event_id)
            self.graph.add((event_iri, PROV.wasInformedBy, parent_iri))

    def serialize(self, format: str = "turtle") -> str:
        """그래프를 문자열로 직렬화

        Args:
            format: 출력 형식
                - "turtle" (기본, 사람이 읽기 쉬움)
                - "xml" (RDF/XML)
                - "n3" (Notation3)
                - "json-ld" (JSON-LD)
                - "nt" (N-Triples)

        Returns:
            직렬화된 RDF 문자열

        예시 (turtle 출력):
            @prefix ledo: <http://ledo.ai/ontology/2026/06/> .
            @prefix prov: <http://www.w3.org/ns/prov#> .
            
            ledo:Activity_f47ac10b... a prov:Activity ;
                prov:startedAtTime "2026-06-10T14:30:00"^^xsd:dateTime ;
                rdfs:label "evaluate_helmet_status"@ko .
        """
        return self.graph.serialize(format=format)

    def get_triple_count(self) -> int:
        """현재 그래프의 총 트리플 개수 반환

        용도:
            - 단위 테스트 (예상 트리플 수 검증)
            - 메모리 사용량 모니터링
            - 디버깅
        """
        return len(self.graph)

    def clear(self) -> None:
        """그래프 비우기 (다음 사건 처리 전)

        ⚠️ 영구 저장 후 호출 (RDF Quad Store 에 commit 완료 후)
        """
        self.graph = Graph()
        self._bind_namespaces()

# ════════════════════════════════════════════════════════════
# 4. DualAuditWriter: 이중 감사 디스패처 (진짜 심장)
# ════════════════════════════════════════════════════════════
# AuditEvent 를 받아 두 레인에 동시 기록
#
# 레인 1 (RDB):
#   - PostgreSQL audit_log 테이블
#   - JSONB 컬럼으로 자유 형식 저장
#   - 빠른 SQL 조회 (인덱스 활용)
#
# 레인 2 (PROV-O):
#   - RDF Quad Store
#   - SPARQL 관계형 추적
#   - W3C 표준 호환
#
# 핵심 원칙: Fail-Safe (한 레인 실패해도 다른 레인 계속)


from typing import Callable
import json
import logging


# 모듈 레벨 로거 (구조화된 로깅)
logger = logging.getLogger(__name__)


class AuditWriteError(Exception):
    """감사 기록 실패 예외

    이 예외가 발생하면 두 레인 모두 실패한 것 (매우 심각).
    한 레인만 실패해도 다른 레인은 계속 작동.
    """
    pass


class DualAuditWriter:
    """이중 감사 시스템의 메인 디스패처

    AuditEvent 인스턴스를 받아:
      1. PostgreSQL audit_log 테이블에 row 추가 (레인 1)
      2. RDF Quad Store 에 PROV-O 트리플 추가 (레인 2)

    설계 원칙:
    ─────────────────────────────────────
    1. Fail-Safe (한 레인 실패해도 다른 레인 계속)
    2. Idempotent (같은 event_id 중복 호출 안전)
    3. Async-Ready (비동기 확장 준비)
    4. Observable (모든 작업이 로그 기록)
    5. Testable (의존성 주입 가능)
    6. PII Aware (자동 마스킹 적용)

    의존성 주입:
    ─────────────────────────────────────
    - sql_writer: RDB 기록 함수 (테스트 시 mock 가능)
    - rdf_writer: RDF 기록 함수 (테스트 시 mock 가능)
    - 기본: 인메모리 + 콘솔 출력 (Phase 4 에서 실제 DB 연결)

    참조 표준:
    - NIST SP 800-92 (Log Management)
    - W3C PROV-O
    - Hexagonal Architecture (Ports & Adapters)
    """

    def __init__(
        self,
        sql_writer: Optional[Callable[[AuditEvent], None]] = None,
        rdf_writer: Optional[Callable[[Graph], None]] = None,
    ) -> None:
        """DualAuditWriter 초기화

        Args:
            sql_writer: RDB 기록 콜백 (선택)
                기본: 인메모리 리스트 저장 (테스트용)
                운영: PostgreSQL INSERT 함수 주입
            rdf_writer: RDF 기록 콜백 (선택)
                기본: 인메모리 그래프 누적 (테스트용)
                운영: GraphDB/Apache Jena 함수 주입

        ⭐ Dependency Injection 패턴:
           운영 환경 vs 테스트 환경에서 다른 backend 사용 가능
           = Hexagonal Architecture 의 핵심
        """
        # 의존성 주입 (기본은 인메모리)
        self._sql_writer = sql_writer or self._default_sql_writer
        self._rdf_writer = rdf_writer or self._default_rdf_writer

        # 인메모리 저장소 (기본 구현, Phase 4 에서 교체)
        self._sql_storage: list[dict] = []
        self._rdf_storage: Graph = Graph()
        self._rdf_storage_bind_namespaces()

        # PROV-O 트리플 생성기 (블록 4 활용)
        self._prov_audit = ProvOAudit()

        # 통계 카운터 (관측 가능성)
        self._stats = {
            "total_events": 0,
            "sql_success": 0,
            "sql_failures": 0,
            "rdf_success": 0,
            "rdf_failures": 0,
            "both_failures": 0,
        }

    def _rdf_storage_bind_namespaces(self) -> None:
        """인메모리 RDF 저장소에 네임스페이스 등록"""
        from ontology.namespaces import bind_to_graph
        bind_to_graph(self._rdf_storage)

    def write(self, event: AuditEvent) -> dict[str, bool]:
        """AuditEvent 를 두 레인에 동시 기록 (핵심 함수)

        Args:
            event: 기록할 AuditEvent 인스턴스

        Returns:
            기록 결과 dict:
                {
                    "sql_success": bool,
                    "rdf_success": bool,
                    "both_failed": bool,
                }

        Raises:
            AuditWriteError: 두 레인 모두 실패 시

        ⭐ Fail-Safe 패턴:
           한 레인 실패 = 로그만 남기고 다른 레인 계속
           두 레인 실패 = AuditWriteError (시스템 알람)
        """
        self._stats["total_events"] += 1

        # PII 마스킹 적용 (필요시)
        event = self._apply_pii_masking(event)

        # 레인 1: RDB 기록
        sql_success = self._write_to_sql(event)

        # 레인 2: PROV-O 트리플 기록
        rdf_success = self._write_to_rdf(event)

        # 결과 종합
        both_failed = (not sql_success) and (not rdf_success)
        if both_failed:
            self._stats["both_failures"] += 1
            error_msg = (
                f"이중 감사 실패! event_id={event.event_id} "
                f"두 레인 모두 기록 실패 (시스템 위기)"
            )
            logger.error(error_msg)
            raise AuditWriteError(error_msg)

        return {
            "sql_success": sql_success,
            "rdf_success": rdf_success,
            "both_failed": both_failed,
        }

    def _write_to_sql(self, event: AuditEvent) -> bool:
        """레인 1: RDB 기록 (PostgreSQL 호환)

        Returns:
            True = 성공, False = 실패

        ⭐ Fail-Safe:
           예외 발생해도 raise 안 함
           로그 + False 반환
           → 시스템 계속 작동
        """
        try:
            self._sql_writer(event)
            self._stats["sql_success"] += 1
            logger.debug(
                f"SQL 기록 성공: event_id={event.event_id} "
                f"type={event.event_type}"
            )
            return True
        except Exception as e:
            self._stats["sql_failures"] += 1
            logger.error(
                f"SQL 기록 실패: event_id={event.event_id} "
                f"error={type(e).__name__}: {e}"
            )
            return False

    def _write_to_rdf(self, event: AuditEvent) -> bool:
        """레인 2: PROV-O 트리플 기록 (RDF Quad Store)

        Returns:
            True = 성공, False = 실패
        """
        try:
            # ProvOAudit 으로 트리플 생성
            self._prov_audit.clear()
            triples_graph = self._prov_audit.event_to_triples(event)

            # 콜백 호출 (실제 저장)
            self._rdf_writer(triples_graph)

            self._stats["rdf_success"] += 1
            logger.debug(
                f"RDF 기록 성공: event_id={event.event_id} "
                f"triples={len(triples_graph)}"
            )
            return True
        except Exception as e:
            self._stats["rdf_failures"] += 1
            logger.error(
                f"RDF 기록 실패: event_id={event.event_id} "
                f"error={type(e).__name__}: {e}"
            )
            return False

    def _apply_pii_masking(self, event: AuditEvent) -> AuditEvent:
        """PII 자동 마스킹 (GDPR 호환)

        contains_pii=True 인 경우:
          - llm_input_snapshot 안의 민감 필드 마스킹
          - action_parameters 안의 민감 필드 마스킹

        ⚠️ AuditEvent 는 frozen=True 라 직접 수정 불가
           → 새 인스턴스 생성 (model_copy)

        Returns:
            마스킹된 AuditEvent (또는 원본)
        """
        if not event.contains_pii:
            return event

        # 마스킹할 키 목록 (산업 표준)
        SENSITIVE_KEYS = {
            "name", "phone", "email", "address",
            "ssn", "rrn", "passport", "birth_date",
            "blood_type", "medical", "salary",
        }

        # llm_input_snapshot 마스킹
        masked_snapshot = self._mask_dict(
            event.llm_input_snapshot,
            SENSITIVE_KEYS,
        )

        # action_parameters 마스킹
        masked_params = self._mask_dict(
            event.action_parameters,
            SENSITIVE_KEYS,
        )

        # 마스킹된 필드 추적
        masked_fields: list[str] = []
        if event.llm_input_snapshot != masked_snapshot:
            masked_fields.append("llm_input_snapshot")
        if event.action_parameters != masked_params:
            masked_fields.append("action_parameters")

        # frozen 모델 복사 + 업데이트
        return event.model_copy(
            update={
                "llm_input_snapshot": masked_snapshot,
                "action_parameters": masked_params,
                "pii_masked_fields": masked_fields,
            }
        )

    def _mask_dict(
        self,
        data: Optional[dict[str, Any]],
        sensitive_keys: set[str],
    ) -> Optional[dict[str, Any]]:
        """dict 의 민감 필드 마스킹 (재귀)

        Args:
            data: 마스킹할 dict (None 가능)
            sensitive_keys: 민감 필드 이름 집합

        Returns:
            마스킹된 dict (None 이면 None 그대로)

        예시:
            입력: {"name": "Lee", "age": 30, "ssn": "9001-..."}
            출력: {"name": "***MASKED***", "age": 30, "ssn": "***MASKED***"}
        """
        if data is None:
            return None

        masked: dict[str, Any] = {}
        for key, value in data.items():
            if key.lower() in sensitive_keys:
                masked[key] = "***MASKED***"
            elif isinstance(value, dict):
                # 재귀: 중첩 dict 도 마스킹
                masked[key] = self._mask_dict(value, sensitive_keys)
            else:
                masked[key] = value
        return masked

    def _default_sql_writer(self, event: AuditEvent) -> None:
        """기본 SQL writer - 인메모리 저장 (Phase 4 에서 PostgreSQL 로 교체)

        실제 운영에선:
            INSERT INTO audit_log (event_id, timestamp_utc, ...)
            VALUES (...);

        지금은:
            self._sql_storage 리스트에 dict 로 추가
        """
        # AuditEvent → dict 변환 (JSONB 저장 형식)
        row = event.model_dump(mode="json")
        self._sql_storage.append(row)

    def _default_rdf_writer(self, graph: Graph) -> None:
        """기본 RDF writer - 인메모리 누적 (Phase 4 에서 GraphDB 로 교체)

        실제 운영에선:
            SPARQL UPDATE INSERT DATA { ... }

        지금은:
            self._rdf_storage 그래프에 트리플 병합
        """
        for triple in graph:
            self._rdf_storage.add(triple)

    # ════════════════════════════════════════
    # 관측 가능성 (Observability)
    # ════════════════════════════════════════

    def get_stats(self) -> dict[str, int]:
        """감사 시스템 통계 반환

        용도:
            - 운영 대시보드
            - 알람 (실패율 임계값 초과 시)
            - 디버깅

        Returns:
            {
                "total_events": int,
                "sql_success": int,
                "sql_failures": int,
                "rdf_success": int,
                "rdf_failures": int,
                "both_failures": int,
            }
        """
        return self._stats.copy()

    def get_sql_storage(self) -> list[dict]:
        """인메모리 SQL 저장소 조회 (테스트용)

        실제 운영에선 PostgreSQL 직접 조회
        """
        return self._sql_storage.copy()

    def get_rdf_storage(self) -> Graph:
        """인메모리 RDF 저장소 조회 (테스트용)

        실제 운영에선 GraphDB SPARQL 엔드포인트
        """
        return self._rdf_storage

    def query_by_actor(self, actor: str) -> list[dict]:
        """특정 actor 가 발생시킨 사건 조회 (간단한 검색)

        Args:
            actor: 검색할 actor (예: "agent:safety")

        Returns:
            매칭되는 사건의 dict 목록

        ⭐ 실제 운영에선:
           SELECT * FROM audit_log WHERE actor = 'agent:safety'
        """
        return [
            row for row in self._sql_storage
            if row.get("actor") == actor
        ]

    def query_by_event_type(
        self,
        event_type: AuditEventType,
    ) -> list[dict]:
        """특정 사건 종류 조회

        Args:
            event_type: AuditEventType Enum

        Returns:
            매칭되는 사건 목록
        """
        return [
            row for row in self._sql_storage
            if row.get("event_type") == event_type.value
        ]

    def export_provo_turtle(self) -> str:
        """RDF 저장소 전체를 Turtle 형식으로 내보내기

        용도:
            - 백업
            - 외부 시스템 (Protégé, GraphDB) import
            - 인간 검토

        Returns:
            Turtle 형식 RDF 문자열
        """
        return self._rdf_storage.serialize(format="turtle")

    def clear_all(self) -> None:
        """모든 저장소 비우기 (테스트 후 정리)

        ⚠️ 운영 환경에선 절대 호출 X
            감사 기록 영구 보존 의무 위반
        """
        self._sql_storage = []
        self._rdf_storage = Graph()
        self._rdf_storage_bind_namespaces()
        self._stats = {
            "total_events": 0,
            "sql_success": 0,
            "sql_failures": 0,
            "rdf_success": 0,
            "rdf_failures": 0,
            "both_failures": 0,
        }


# ════════════════════════════════════════════════════════════
# 5. 모듈 레벨 헬퍼 함수 (공식 API)
# ════════════════════════════════════════════════════════════
# 외부 모듈에서는 이 함수들을 통해 audit 시스템 사용
# DualAuditWriter 직접 사용 X (캡슐화)


# 글로벌 싱글톤 인스턴스 (시스템 전체에서 공유)
_global_audit_writer: Optional[DualAuditWriter] = None


def get_audit_writer() -> DualAuditWriter:
    """글로벌 DualAuditWriter 인스턴스 반환 (싱글톤)

    Returns:
        시스템 전체에서 공유되는 audit writer

    ⭐ Singleton Pattern:
       시스템 전체에서 하나의 감사 시스템
       메모리 효율 + 일관성
    """
    global _global_audit_writer
    if _global_audit_writer is None:
        _global_audit_writer = DualAuditWriter()
    return _global_audit_writer


def audit(event: AuditEvent) -> dict[str, bool]:
    """편의 함수: 단일 사건 기록

    Args:
        event: 기록할 AuditEvent

    Returns:
        기록 결과 dict

    예시:
        from ontology.audit import audit, AuditEvent, AuditEventType, AuditOutcome

        result = audit(AuditEvent(
            event_type=AuditEventType.LLM_DECISION,
            outcome=AuditOutcome.SUCCESS,
            actor="agent:safety",
            action="evaluate_helmet",
            llm_model_id="qwen2.5-coder:14b",
        ))
        # result = {"sql_success": True, "rdf_success": True, "both_failed": False}
    """
    writer = get_audit_writer()
    return writer.write(event)


def audit_llm_decision(
    actor: str,
    action: str,
    llm_model_id: str,
    llm_input_snapshot: dict[str, Any],
    outcome: AuditOutcome = AuditOutcome.SUCCESS,
    subject_iri: Optional[str] = None,
    llm_input_token_count: Optional[int] = None,
    llm_response_time_ms: Optional[int] = None,
    parent_event_id: Optional[str] = None,
    correlation_id: Optional[str] = None,
) -> dict[str, bool]:
    """편의 함수: LLM 결정 사건 빠르게 기록

    Args:
        actor: 결정한 에이전트 (예: "agent:safety")
        action: 활동명 (예: "evaluate_helmet")
        llm_model_id: 사용한 LLM 모델
        llm_input_snapshot: 입력 스냅샷
        outcome: 결과 (기본 SUCCESS)
        subject_iri: 대상 엔티티 IRI
        llm_input_token_count: 입력 토큰 수
        llm_response_time_ms: 응답 시간
        parent_event_id: 부모 사건 ID
        correlation_id: 워크플로우 ID

    Returns:
        기록 결과

    ⭐ 본인의 핵심 요청 사항 #2 의 사용 편의 함수
       LLM 결정마다 한 줄로 완전 추적
    """
    event = AuditEvent(
        event_type=AuditEventType.LLM_DECISION,
        outcome=outcome,
        actor=actor,
        action=action,
        subject_iri=subject_iri,
        llm_model_id=llm_model_id,
        llm_input_snapshot=llm_input_snapshot,
        llm_input_token_count=llm_input_token_count,
        llm_response_time_ms=llm_response_time_ms,
        parent_event_id=parent_event_id,
        correlation_id=correlation_id,
    )
    return audit(event)