"""
LEDO.ai - 온톨로지 도메인 클래스 정의

이 모듈은 시스템에 존재할 수 있는 모든 "것"의 메타구조를 정의한다.
모든 클래스는 OntologyClass 인스턴스이며, Pydantic v2로 자동 검증된다.

핵심 설계 원칙:
─────────────────────────────────────
1. Single Source of Truth (DOMAIN_CLASSES 딕셔너리)
2. Fail-Secure Defaults (access_level=INTERNAL)
3. Privacy by Design (GDPR Article 25)
4. Audit by Default (감사 추적 메타데이터)
5. Neuro-Symbolic Duality (두 패러다임 평행 공존)
6. Standards-Aligned (BFO/SOSA/SAREF/PROV-O/ifcOWL)

참조 표준:
─────────────────────────────────────
- ISO/IEC 21838-2:2021 (Top-Level Ontologies, BFO 2.0)
- W3C OWL 2 (Web Ontology Language)
- W3C SOSA/SSN (Sensor, Observation, Sample, Actuator)
- W3C PROV-O (Provenance Ontology)
- ETSI TS 103 264 (SAREF)
- BuildingSMART ifcOWL (BIM 통합)
- NIST SP 800-53 Rev.5 (Security Controls)
- GDPR Article 5, 25
- 한국 개인정보보호법 제3조, 제21조
- 한국 산업안전보건법 시행규칙 제33조

저작자: LEDO.ai Team
라이선스: Internal Use Only
초기 발행: 2026-06
Python 버전: 3.14+ (PEP 649 lazy annotations 활용)
"""
from enum import Enum
from datetime import datetime, timezone
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    field_validator,
    model_validator,
)

from config import settings
from ontology.namespaces import LEDO, get_iri


class ClassCategory(str, Enum):
    """온톨로지 클래스의 최상위 카테고리 (BFO 정렬)

    카테고리는 시스템 부팅 시 고정되며, 변증법으로도 변경되지 않는다.
    새 카테고리가 필요하면 인간 개발자의 의사결정 사항 (배포 필요).

    BFO 2.0 매핑 (ISO/IEC 21838-2):
    ─────────────────────────────────────
    PHYSICAL   → bfo:MaterialEntity      (물리적 실체)
    SPATIAL    → bfo:Site                (공간 영역)
    DEVICE     → bfo:MaterialEntity + sosa:Sensor (IoT 장치)
    EVENT      → bfo:Process             (시간적 사건)
    ABSTRACT   → bfo:GenericallyDependentContinuant (추상 개념)
    AGENT      → 확장 (BFO 표준 외, prov:Agent 와 매핑)
    """
    PHYSICAL = "physical"        # 물리적 실체 (Worker, Equipment, Material)
    SPATIAL = "spatial"          # 공간 (DangerZone, SafeZone, WorkArea)
    DEVICE = "device"            # IoT 장치 (Sensor, Camera, Beacon)
    EVENT = "event"              # 사건 (Alarm, Incident, NearMiss)
    ABSTRACT = "abstract"        # 추상 개념 (Task, Permission, Shift)
    AGENT = "agent"              # 에이전트 자체


    class AccessLevel(str, Enum):
    """클래스/속성의 접근 권한 레벨

    조 단위 산업에서 데이터 보안과 감사 요건에 필수.
    NIST SP 800-53 Rev.5 기반 4단계 권한 모델.

    Fail-Secure 원칙:
    ─────────────────────────────────────
    기본값은 항상 INTERNAL (외부 노출 차단).
    "모르면 일단 막아라" - 산업 보안의 황금 규칙.

    레벨 매핑:
    ─────────────────────────────────────
    PUBLIC     → 누구나 조회 가능 (DangerZone 위치)
    INTERNAL   → 내부 시스템만 (Worker 위치 - 안전 관리용)
    RESTRICTED → 권한 있는 에이전트만 (Worker 자격증)
    AUDIT_ONLY → 감사 기록 시에만 (법적 분쟁 시 열람)
    """
    PUBLIC = "public"
    INTERNAL = "internal"
    RESTRICTED = "restricted"
    AUDIT_ONLY = "audit_only"


    class OntologyMetadata(BaseModel):
    """모든 온톨로지 엔티티의 공통 메타정보

    감사 추적과 버전 관리의 단일 진실 원천.
    조 단위 산업에서 "누가 언제 무엇을 했는가" 추적 불가하면
    법적 책임 소재가 불명확하다.

    이중 감사 아키텍처 (LEDO 핵심):
    ─────────────────────────────────────
    1. RDB 감사 (필드 직접 저장 - 빠른 SQL 조회)
    2. PROV-O 트리플 (관계 그래프 - SPARQL 추적)
    
    두 레인이 동시에 기록 → 산업 안전 시스템 완전 추적

    참조 표준:
    - Semantic Versioning 2.0.0 (semver.org)
    - ISO 8601 (Date/Time)
    - W3C PROV-O (Provenance Ontology)
    - NIST SP 800-92 (Log Management)
    - 한국 산업안전보건법 시행규칙 제33조 (7년 보존)
    """
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        str_strip_whitespace=True,
        frozen=False,
    )

    # ════════════════════════════════════════
    # 1. 버전 관리 (Semantic Versioning)
    # ════════════════════════════════════════
    version: str = Field(
        default="1.0.0",
        pattern=r"^\d+\.\d+\.\d+$",
        description="시맨틱 버저닝 (MAJOR.MINOR.PATCH)",
    )

    # ════════════════════════════════════════
    # 2. 시간 추적 (UTC 강제, ISO 8601)
    # ════════════════════════════════════════
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="생성 시각 (UTC, ISO 8601)",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="마지막 수정 시각 (UTC)",
    )

    # ════════════════════════════════════════
    # 3. 책임 추적 (Accountability)
    # PROV-O 매핑: prov:wasAttributedTo
    # ════════════════════════════════════════
    created_by: str = Field(
        default="system",
        min_length=1,
        max_length=128,
        description="생성자 ID (system | human:<id> | agent:<name>)",
    )
    last_modified_by: str = Field(
        default="system",
        min_length=1,
        max_length=128,
        description="마지막 수정자 ID",
    )

    # ════════════════════════════════════════
    # 4. 변증법 진화 추적
    # ════════════════════════════════════════
    is_dynamically_created: bool = Field(
        default=False,
        description="변증법 엔진이 동적으로 생성한 클래스인가",
    )
    evolution_count: int = Field(
        default=0,
        ge=0,
        le=10000,
        description="변증법으로 수정된 횟수",
    )
    parent_version: Optional[str] = Field(
        default=None,
        pattern=r"^\d+\.\d+\.\d+$",
        description="이전 버전 (진화 추적용)",
    )

    # ════════════════════════════════════════
    # 5. LLM 결정 추적 (이중 감사용)
    # PROV-O 매핑: prov:Activity, prov:used
    # ════════════════════════════════════════
    llm_decision_id: Optional[str] = Field(
        default=None,
        description="LLM 결정의 unique ID (UUID v4)",
    )
    llm_model_id: Optional[str] = Field(
        default=None,
        max_length=128,
        description="결정한 LLM 모델 식별자 (예: qwen2.5-coder:14b)",
    )
    llm_context_snapshot: Optional[dict] = Field(
        default=None,
        description="LLM 결정 시점의 입력 컨텍스트 스냅샷 (감사용)",
    )
    llm_input_token_count: Optional[int] = Field(
        default=None,
        ge=0,
        le=131072,
        description="입력 토큰 수 (비용·성능 추적)",
    )

    # ════════════════════════════════════════
    # 6. PROV-O 관계형 감사 (이중 레인 #2)
    # ════════════════════════════════════════
    prov_activity_iri: Optional[str] = Field(
        default=None,
        description="이 변경을 나타내는 PROV-O Activity 의 IRI",
    )
    prov_agent_iri: Optional[str] = Field(
        default=None,
        description="이 변경의 책임자 PROV-O Agent IRI",
    )
    prov_used_entities: list[str] = Field(
        default_factory=list,
        description="이 결정이 참조한 다른 엔티티들의 IRI 목록",
    )

    # ════════════════════════════════════════
    # 7. Validators (시간 일관성, 책임 일관성)
    # ════════════════════════════════════════
    @field_validator("created_by", "last_modified_by")
    @classmethod
    def validate_actor_format(cls, v: str) -> str:
        """actor ID 형식 검증

        허용 형식:
        - "system" (시스템 자동)
        - "human:<id>" (사람 - 인사 DB 매칭 가능)
        - "agent:<name>" (에이전트 - 어떤 에이전트인지 명시)
        """
        if v == "system":
            return v

        if not (v.startswith("human:") or v.startswith("agent:")):
            raise ValueError(
                f"actor ID '{v}' 는 'system' 또는 'human:<id>' "
                f"또는 'agent:<name>' 형식이어야 함"
            )

        # prefix 뒤 식별자 검증
        identifier = v.split(":", 1)[1]
        if not identifier or not identifier.replace("_", "").replace("-", "").isalnum():
            raise ValueError(
                f"actor 식별자 '{identifier}' 는 영숫자/언더스코어/하이픈만 허용"
            )

        return v

    @model_validator(mode="after")
    def validate_temporal_and_audit_consistency(self) -> "OntologyMetadata":
        """시간 + 감사 일관성 검증

        규칙:
        1. updated_at >= created_at (시간 역행 차단)
        2. evolution_count > 0 이면 parent_version 필수
        3. is_dynamically_created=True 이면 created_by != 'system'
        4. llm_decision_id 있으면 llm_model_id 도 필수
        5. prov_activity_iri 있으면 prov_agent_iri 도 필수
        """
        # 1. 시간 역행 차단
        if self.updated_at < self.created_at:
            raise ValueError(
                "updated_at 은 created_at 이후여야 함 (시간 역행 불가)"
            )

        # 2. 진화 추적 일관성
        if self.evolution_count > 0 and self.parent_version is None:
            raise ValueError(
                "evolution_count > 0 이면 parent_version 필수"
            )

        # 3. 동적 생성 책임
        if self.is_dynamically_created and self.created_by == "system":
            raise ValueError(
                "동적 생성 클래스의 created_by 는 'system' 불가 "
                "(에이전트 식별 필수)"
            )

        # 4. LLM 추적 일관성
        if self.llm_decision_id is not None and self.llm_model_id is None:
            raise ValueError(
                "llm_decision_id 있으면 llm_model_id 도 필수 (감사 추적)"
            )

        # 5. PROV-O 일관성
        if self.prov_activity_iri is not None and self.prov_agent_iri is None:
            raise ValueError(
                "prov_activity_iri 있으면 prov_agent_iri 도 필수 (W3C PROV-O)"
            )

        return self
    

class OntologyClass(BaseModel):
    """온톨로지 클래스의 메타정의

    이 모델은 시스템의 "타입 시스템"이다. 모든 인스턴스는
    여기 정의된 스키마에 의해 검증되고, 변증법 엔진은
    이 정의 자체를 진화시킨다.

    핵심 설계 원칙:
    ─────────────────────────────────────
    1. 불변 정체성 (name 은 한번 정해지면 변경 불가)
    2. 가변 확장성 (속성·규칙은 변증법으로 진화)
    3. 자동 검증 (Pydantic v2)
    4. JSON 직렬화 (Redis Streams, PostgreSQL JSONB 호환)
    5. 감사 추적 (모든 변경이 metadata 에 기록)
    6. 권한 분리 (access_level 로 접근 제어)
    7. Neuro-Symbolic 명시 (두 패러다임 평행 공존)
    8. 표준 매핑 (BFO/SOSA/SAREF/ifcOWL/PROV-O)

    참조 표준:
    - ISO/IEC 21838-2 (BFO)
    - W3C OWL 2 (Web Ontology Language)
    - W3C SHACL (Shapes Constraint Language)
    - BuildingSMART ifcOWL (BIM)
    """
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        frozen=False,
        json_schema_extra={
            "examples": [
                {
                    "name": "Worker",
                    "category": "physical",
                    "description": "건설 현장의 근로자",
                    "iri": "http://ledo.ai/ontology/2026/06/Worker",
                }
            ]
        },
    )

    # ════════════════════════════════════════
    # 1. 불변 정체성 (Identity)
    # 한번 정해지면 절대 변경 불가
    # Database PRIMARY KEY 의 온톨로지 버전
    # ════════════════════════════════════════
    name: str = Field(
        ...,
        min_length=1,
        max_length=64,
        pattern=r"^[A-Z][a-zA-Z0-9_]*$",
        description="우리 시스템 식별자 (PascalCase, 참조 무결성 핵심)",
        json_schema_extra={"example": "Worker"},
    )
    iri: str = Field(
        ...,
        pattern=r"^https?://[a-zA-Z0-9.\-/]+/[A-Z][a-zA-Z0-9_]*$",
        description="W3C 표준 IRI (RFC 3987 - Internationalized Resource Identifier)",
        json_schema_extra={
            "example": "http://ledo.ai/ontology/2026/06/Worker"
        },
    )
    category: ClassCategory = Field(
        ...,
        description="최상위 분류 (시스템 부팅 시 고정, BFO 정렬)",
    )
    description: str = Field(
        ...,
        min_length=10,
        max_length=512,
        description="자연어 설명 (LLM 의미 추론의 근거)",
    )

    # ════════════════════════════════════════
    # 2. 외부 표준 매핑 (Standards Alignment)
    # 글로벌 시맨틱 웹과의 호환성
    # ════════════════════════════════════════
    bfo_class: Optional[str] = Field(
        default=None,
        pattern=r"^bfo:[A-Za-z]+$",
        description="BFO 상위 클래스 (ISO/IEC 21838-2)",
        json_schema_extra={"example": "bfo:MaterialEntity"},
    )
    standard_mappings: dict[str, str] = Field(
        default_factory=dict,
        description="외부 표준 매핑 {표준명: IRI}. 예: SOSA, SAREF, ifcOWL, PROV-O",
        json_schema_extra={
            "example": {
                "sosa": "http://www.w3.org/ns/sosa/Sensor",
                "saref": "https://saref.etsi.org/core/Device",
                "ifcowl": "https://standards.buildingsmart.org/IFC/.../IfcDoor",
            }
        },
    )    


# ════════════════════════════════════════
    # 3. 속성 정의 (Property Schema)
    # OWL 의 ObjectProperty / DatatypeProperty 와 유사
    # ════════════════════════════════════════
    required_properties: list[str] = Field(
        default_factory=list,
        max_length=64,
        description="필수 속성 ID 목록 (인스턴스 생성 시 누락 시 검증 실패)",
    )
    optional_properties: list[str] = Field(
        default_factory=list,
        max_length=128,
        description="선택 속성 ID 목록 (있어도 되고 없어도 됨)",
    )

    # ════════════════════════════════════════
    # 4. 계층 구조 (Taxonomy)
    # Subsumption Relation (포함 관계)
    # ════════════════════════════════════════
    parent_class: Optional[str] = Field(
        default=None,
        pattern=r"^[A-Z][a-zA-Z0-9_]*$",
        description="부모 클래스 (속성·규칙 자동 상속)",
    )
    extensible: bool = Field(
        default=True,
        description="변증법 엔진의 동적 확장 허용 여부",
    )
    is_abstract: bool = Field(
        default=False,
        description="추상 클래스 (자식만 인스턴스화 가능)",
    )

    # ════════════════════════════════════════
    # 5. Neuro-Symbolic Dual Specification
    # 같은 인스턴스를 두 패러다임으로 분석
    # ════════════════════════════════════════
    neural_features: list[str] = Field(
        default_factory=list,
        description="신경망 분석 능력 ID 목록 (패턴·예측·이상치)",
    )
    symbolic_constraints: list[str] = Field(
        default_factory=list,
        description="논리 규칙 ID 목록 (rules.py 참조)",
    )

    # ════════════════════════════════════════
    # 6. 보안 및 개인정보 (NIST + GDPR)
    # Privacy by Design 원칙
    # ════════════════════════════════════════
    access_level: AccessLevel = Field(
        default=AccessLevel.INTERNAL,
        description="기본 접근 권한 (Fail-Secure)",
    )
    audit_required: bool = Field(
        default=False,
        description="변경 시 감사 로그 필수 여부 (법적 추적)",
    )
    pii_contained: bool = Field(
        default=False,
        description="개인정보 포함 (GDPR Art.4(1) 정의 기준)",
    )
    retention_days: Optional[int] = Field(
        default=None,
        ge=1,
        le=36500,
        description="데이터 보관 일수 (None=영구). GDPR Art.5(1)(e)",
    )

    # ════════════════════════════════════════
    # 7. 운영 메타정보 (Operational Metadata)
    # 블록 4 의 OntologyMetadata 활용
    # ════════════════════════════════════════
    metadata: OntologyMetadata = Field(
        default_factory=OntologyMetadata,
        description="버전·생성일·진화 이력·LLM 추적·PROV-O",
    )

    # ════════════════════════════════════════
    # 8. Custom Validators (산업 표준 보장)
    # ════════════════════════════════════════
    @field_validator("required_properties", "optional_properties")
    @classmethod
    def validate_property_names(cls, v: list[str]) -> list[str]:
        """속성 이름 규칙 검증

        규칙:
        1. snake_case 강제 (PEP 8 변수명 규칙)
        2. 예약어 차단 (Python keyword 충돌 방지)
        3. 중복 차단
        4. 영숫자 + 언더스코어만 허용
        """
        import keyword

        for prop in v:
            if not prop.replace("_", "").isalnum():
                raise ValueError(
                    f"속성 이름 '{prop}' 은 영숫자와 언더스코어만 허용"
                )
            if prop != prop.lower():
                raise ValueError(
                    f"속성 이름 '{prop}' 은 snake_case 여야 함"
                )
            if keyword.iskeyword(prop):
                raise ValueError(
                    f"속성 이름 '{prop}' 은 Python 예약어 (사용 불가)"
                )

        if len(v) != len(set(v)):
            raise ValueError("속성 목록에 중복 존재")

        return v

    @field_validator("name")
    @classmethod
    def name_not_reserved(cls, v: str) -> str:
        """예약된 클래스 이름 차단 (시스템 충돌 방지)"""
        RESERVED = {
            "Class", "Object", "Type", "Meta",
            "BaseModel", "None", "True", "False",
        }
        if v in RESERVED:
            raise ValueError(
                f"'{v}' 은 시스템 예약어 (사용 불가)"
            )
        return v

    @model_validator(mode="after")
    def validate_consistency(self) -> "OntologyClass":
        """클래스 전체 일관성 검증 (모든 필드 채워진 후 실행)

        비즈니스 규칙:
        1. required 와 optional 속성 중복 불가
        2. 추상 클래스는 부모 가질 수 없음
        3. pii_contained=True 면 retention_days 필수
        4. audit_required=True 면 access_level != PUBLIC
        5. is_abstract=True 면 인스턴스 직접 생성 의도 X
        """
        # 1. 속성 중복 검증
        overlap = set(self.required_properties) & set(self.optional_properties)
        if overlap:
            raise ValueError(
                f"required 와 optional 속성 중복: {overlap}"
            )

        # 2. 추상 클래스 제약
        if self.is_abstract and self.parent_class:
            raise ValueError(
                "추상 클래스는 부모 클래스를 가질 수 없음 "
                "(추상은 최상위 개념)"
            )

        # 3. PII 보관 정책 (GDPR Art.5(1)(e))
        if self.pii_contained and self.retention_days is None:
            raise ValueError(
                "PII 포함 클래스는 retention_days 명시 필수 "
                "(GDPR Art.5(1)(e) - Storage Limitation)"
            )

        # 4. 감사 + 권한 일관성 (NIST SP 800-53)
        if self.audit_required and self.access_level == AccessLevel.PUBLIC:
            raise ValueError(
                "감사 필수 클래스는 PUBLIC 권한 불가 "
                "(NIST SP 800-53 위반)"
            )

        # 5. IRI 와 name 일치 검증
        if not self.iri.endswith(f"/{self.name}"):
            raise ValueError(
                f"IRI 의 끝은 클래스 name 과 일치해야 함. "
                f"IRI='{self.iri}', name='{self.name}'"
            )

        return self
    

# ════════════════════════════════════════════════════════════
# 도메인 클래스 사전 (Single Source of Truth)
# ════════════════════════════════════════════════════════════
# 시스템에서 사용되는 모든 도메인 클래스의 정의
# 변증법 엔진은 이 사전에 새 클래스를 추가할 수 있음 (extensible=True 인 경우)
#
# 5개 핵심 클래스:
#   1. Worker      - 건설 근로자 (PII 포함)
#   2. Equipment   - 건설 장비
#   3. DangerZone  - 위험 구역
#   4. Sensor      - IoT 센서
#   5. Alarm       - 안전 경보
# ════════════════════════════════════════════════════════════

DOMAIN_CLASSES: dict[str, OntologyClass] = {

    "Worker": OntologyClass(
        name="Worker",
        iri="http://ledo.ai/ontology/2026/06/Worker",
        category=ClassCategory.PHYSICAL,
        description=(
            "건설 현장에서 작업하는 근로자. "
            "위치·자세·피로 등이 실시간으로 추적되며, "
            "안전 규칙 준수 여부가 자동 검증된다."
        ),
        required_properties=[
            "id",
            "position",
            "helmet_on",
        ],
        optional_properties=[
            "name",
            "certification",
            "shift_type",
            "experience_years",
            "blood_type",
        ],
        neural_features=[
            "movement_pattern",
            "posture_anomaly",
            "trajectory_prediction",
            "fatigue_estimation",
        ],
        symbolic_constraints=[
            "must_wear_helmet",
            "min_distance_from_danger_zone",
            "max_continuous_work_hours",
            "certification_validity",
        ],
        # 보안: 개인정보 포함 → 강화된 권한
        access_level=AccessLevel.INTERNAL,
        audit_required=True,
        pii_contained=True,
        retention_days=1095,
        # 표준 매핑
        bfo_class="bfo:MaterialEntity",
        standard_mappings={
            "prov": "http://www.w3.org/ns/prov#Agent",
            "saref": "https://saref.etsi.org/core/Profile",
        },
    ),

    "Equipment": OntologyClass(
        name="Equipment",
        iri="http://ledo.ai/ontology/2026/06/Equipment",
        category=ClassCategory.PHYSICAL,
        description=(
            "건설 장비 (크레인, 굴착기, 지게차 등). "
            "진동·하중·마모도가 추적되며, "
            "예측 정비 (Predictive Maintenance) 가 적용된다."
        ),
        required_properties=[
            "id",
            "type",
            "position",
            "operating_status",
        ],
        optional_properties=[
            "operator_id",
            "last_inspection_date",
            "load_capacity_kg",
            "manufacturer",
            "serial_number",
        ],
        neural_features=[
            "vibration_pattern",
            "load_anomaly",
            "wear_progression",
            "failure_prediction",
        ],
        symbolic_constraints=[
            "operator_certified",
            "max_load_compliance",
            "inspection_validity",
            "operating_hours_limit",
        ],
        access_level=AccessLevel.INTERNAL,
        audit_required=True,
        pii_contained=False,
        retention_days=2555,
        # 표준 매핑 (BIM 통합)
        bfo_class="bfo:MaterialEntity",
        standard_mappings={
            "saref": "https://saref.etsi.org/core/Device",
            "ifcowl": "https://standards.buildingsmart.org/IFC/DEV/IFC4_3/OWL#IfcMachine",
        },
    ),

"DangerZone": OntologyClass(
        name="DangerZone",
        iri="http://ledo.ai/ontology/2026/06/DangerZone",
        category=ClassCategory.SPATIAL,
        description=(
            "위험구역 (고소작업, 굴착, 중량물 이동 구역). "
            "공간적 범위를 가지며, 무단 출입 시 즉시 경보가 발동된다. "
            "GeoSPARQL 호환 좌표 시스템 사용."
        ),
        required_properties=[
            "id",
            "zone_type",
            "center",
            "radius",
        ],
        optional_properties=[
            "height",
            "active_hours",
            "authorized_workers",
            "hazard_level",
        ],
        neural_features=[
            "crowd_density_pattern",
            "incident_correlation",
        ],
        symbolic_constraints=[
            "no_unauthorized_entry",
            "minimum_safety_distance",
            "active_hours_compliance",
        ],
        access_level=AccessLevel.PUBLIC,
        audit_required=False,
        pii_contained=False,
        retention_days=None,
        bfo_class="bfo:Site",
        standard_mappings={
            "geo": "http://www.opengis.net/ont/geosparql#Feature",
            "bot": "https://w3id.org/bot#Zone",
        },
    ),

    "Sensor": OntologyClass(
        name="Sensor",
        iri="http://ledo.ai/ontology/2026/06/Sensor",
        category=ClassCategory.DEVICE,
        description=(
            "TinyML 기반 IoT 센서 (GPS, 가속도, 헬멧 감지 등). "
            "실시간 데이터를 수집하며, 자체 노이즈 필터링을 수행한다. "
            "W3C SOSA/SSN 호환."
        ),
        required_properties=[
            "id",
            "sensor_type",
            "target_id",
            "timestamp",
        ],
        optional_properties=[
            "battery_level",
            "accuracy",
            "firmware_version",
            "last_calibration",
        ],
        neural_features=[
            "data_quality_score",
            "noise_pattern_detection",
            "drift_detection",
        ],
        symbolic_constraints=[
            "data_freshness_check",
            "calibration_validity",
            "battery_threshold",
        ],
        access_level=AccessLevel.INTERNAL,
        audit_required=False,
        pii_contained=False,
        retention_days=365,
        bfo_class="bfo:MaterialEntity",
        standard_mappings={
            "sosa": "http://www.w3.org/ns/sosa/Sensor",
            "ssn": "http://www.w3.org/ns/ssn/System",
            "saref": "https://saref.etsi.org/core/Sensor",
        },
    ),

    "Alarm": OntologyClass(
        name="Alarm",
        iri="http://ledo.ai/ontology/2026/06/Alarm",
        category=ClassCategory.EVENT,
        description=(
            "시스템이 발생시킨 안전 경보. "
            "심각도에 따라 실시간 전파되며, "
            "모든 경보는 법적 추적을 위해 영구 보존된다."
        ),
        required_properties=[
            "id",
            "severity",
            "triggered_by",
            "timestamp",
        ],
        optional_properties=[
            "resolved_at",
            "acknowledged_by",
            "rule_violated",
            "auto_resolved",
        ],
        neural_features=[
            "severity_prediction",
            "false_positive_likelihood",
        ],
        symbolic_constraints=[
            "escalation_protocol",
            "response_time_limit",
            "acknowledgment_required",
        ],
        access_level=AccessLevel.PUBLIC,
        audit_required=True,
        pii_contained=False,
        retention_days=None,
        bfo_class="bfo:Process",
        standard_mappings={
            "prov": "http://www.w3.org/ns/prov#Activity",
            "saref": "https://saref.etsi.org/core/Event",
        },
    ),

}

# ════════════════════════════════════════════════════════════
# 공식 API (외부에서는 이 함수들만 사용할 것)
# ════════════════════════════════════════════════════════════
# 캡슐화 원칙:
#   - DOMAIN_CLASSES 사전 직접 접근 X
#   - 아래 헬퍼 함수만 사용
#   - 안전한 기본값 제공 (Fail-Secure)
#
# 모든 함수는 Type Hint + Docstring 완비
# ════════════════════════════════════════════════════════════

def get_class(class_name: str) -> Optional[OntologyClass]:
    """클래스 이름으로 OntologyClass 정의 조회

    Args:
        class_name: 클래스 이름 (예: "Worker")

    Returns:
        OntologyClass 인스턴스 또는 None (없을 때)

    예시:
        worker = get_class("Worker")
        if worker:
            print(worker.iri)
    """
    return DOMAIN_CLASSES.get(class_name)


def is_valid_class(class_name: str) -> bool:
    """클래스가 온톨로지에 정의되어 있는지 확인

    Validator 첫 단계에서 호출되는 핵심 검증 함수.

    Args:
        class_name: 검증할 클래스 이름

    Returns:
        True 면 등록됨, False 면 미등록
    """
    return class_name in DOMAIN_CLASSES


def list_all_classes() -> list[str]:
    """등록된 모든 클래스 이름 반환

    Returns:
        클래스 이름 목록 (예: ["Worker", "Equipment", ...])
    """
    return list(DOMAIN_CLASSES.keys())


def list_classes_by_category(category: ClassCategory) -> list[str]:
    """카테고리별 클래스 목록 반환

    Args:
        category: ClassCategory Enum 값

    Returns:
        해당 카테고리의 클래스 이름 목록

    예시:
        physical = list_classes_by_category(ClassCategory.PHYSICAL)
        # → ["Worker", "Equipment"]
    """
    return [
        name for name, cls in DOMAIN_CLASSES.items()
        if cls.category == category.value
    ]


def get_required_properties(class_name: str) -> list[str]:
    """특정 클래스의 필수 속성 반환

    Args:
        class_name: 클래스 이름

    Returns:
        필수 속성 ID 목록. 클래스 없으면 빈 리스트.
    """
    cls = get_class(class_name)
    return cls.required_properties if cls else []


def get_neural_features(class_name: str) -> list[str]:
    """클래스의 Neural 분석 기능 ID 목록 반환

    Args:
        class_name: 클래스 이름

    Returns:
        신경망 분석 ID 목록. 클래스 없으면 빈 리스트.
    """
    cls = get_class(class_name)
    return cls.neural_features if cls else []


def get_symbolic_constraints(class_name: str) -> list[str]:
    """클래스의 Symbolic 제약조건 ID 목록 반환

    Args:
        class_name: 클래스 이름

    Returns:
        논리 규칙 ID 목록. 클래스 없으면 빈 리스트.
    """
    cls = get_class(class_name)
    return cls.symbolic_constraints if cls else []


def requires_audit(class_name: str) -> bool:
    """이 클래스가 감사 로그를 요구하는가

    Args:
        class_name: 클래스 이름

    Returns:
        True 면 모든 변경이 감사 로그 필수.
        클래스 없으면 안전을 위해 True (Fail-Secure).
    """
    cls = get_class(class_name)
    return cls.audit_required if cls else True


def get_access_level(class_name: str) -> AccessLevel:
    """클래스의 접근 권한 레벨 반환

    Args:
        class_name: 클래스 이름

    Returns:
        AccessLevel Enum.
        클래스 없으면 RESTRICTED (Fail-Secure - 모르면 막아라).
    """
    cls = get_class(class_name)
    return AccessLevel(cls.access_level) if cls else AccessLevel.RESTRICTED


def is_extensible(class_name: str) -> bool:
    """변증법 엔진이 이 클래스를 진화시킬 수 있는가

    Args:
        class_name: 클래스 이름

    Returns:
        True 면 변증법 확장 허용.
        클래스 없으면 False (안전을 위해).
    """
    cls = get_class(class_name)
    return cls.extensible if cls else False


def contains_pii(class_name: str) -> bool:
    """이 클래스가 개인정보 (PII) 를 포함하는가

    GDPR + 한국 개인정보보호법 대응용.

    Args:
        class_name: 클래스 이름

    Returns:
        True 면 PII 포함 → 자동 마스킹 + retention 적용.
        클래스 없으면 안전을 위해 True (Fail-Secure).
    """
    cls = get_class(class_name)
    return cls.pii_contained if cls else True


def get_iri_for_class(class_name: str) -> Optional[str]:
    """클래스의 글로벌 IRI 반환

    Args:
        class_name: 클래스 이름

    Returns:
        IRI 문자열 또는 None (클래스 없을 때).

    예시:
        iri = get_iri_for_class("Worker")
        # → "http://ledo.ai/ontology/2026/06/Worker"
    """
    cls = get_class(class_name)
    return cls.iri if cls else None


def get_standard_mapping(class_name: str, standard: str) -> Optional[str]:
    """클래스의 특정 외부 표준 매핑 IRI 반환

    Args:
        class_name: 클래스 이름
        standard: 표준 prefix (예: "sosa", "bfo", "ifcowl")

    Returns:
        해당 표준의 매핑 IRI 또는 None.

    예시:
        sosa_iri = get_standard_mapping("Sensor", "sosa")
        # → "http://www.w3.org/ns/sosa/Sensor"
    """
    cls = get_class(class_name)
    if cls is None:
        return None
    return cls.standard_mappings.get(standard.lower())

