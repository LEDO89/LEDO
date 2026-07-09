"""Shared enum types for common schema/DTO contracts.

Canonical source for each enum is `03_core_specifications/01_common_schema_dto/1_common_schema_dto.md`
unless noted otherwise. `DispatchStatus` is the one exception: its canonical,
implementation-authoritative definition lives in
`03_core_specifications/09_execution_adapter_model/9_execution_adapter_model.md` Section 20
("Dispatch Lifecycle"), which explicitly forbids a second enum being derived from the
shorter illustrative lists in `1_common_schema_dto.md` Section 18.3 or
`03_action_type_registry.md` Section 9.1.
"""

from __future__ import annotations

from enum import Enum


class ValidationStatus(str, Enum):
    """Section 5.2 / 10.1."""

    PASSED = "PASSED"
    FAILED = "FAILED"
    PARTIALLY_PASSED = "PARTIALLY_PASSED"
    QUARANTINED = "QUARANTINED"
    REJECTED = "REJECTED"


class PathType(str, Enum):
    """Section 12.3."""

    STANDARD = "STANDARD"
    EMERGENCY_FAST_PATH = "EMERGENCY_FAST_PATH"
    MONITORING_ONLY = "MONITORING_ONLY"


class BindingStatus(str, Enum):
    """Section 14.2."""

    BOUND = "BOUND"
    PARTIALLY_BOUND = "PARTIALLY_BOUND"
    BINDING_FAILED = "BINDING_FAILED"
    UNCLASSIFIED = "UNCLASSIFIED"


class PolicyDecisionResult(str, Enum):
    """Canonical source: 08_policy_governance_model.md Section 7 ("Policy Decision
    Result"). The shorter 5-member list previously derived from
    1_common_schema_dto.md Section 19.7 is superseded — that section's list is
    illustrative and does not match the Policy Governance Model's actual result set.
    """

    ALLOW = "ALLOW"
    DENY = "DENY"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"
    REQUIRE_EVIDENCE = "REQUIRE_EVIDENCE"
    REQUIRE_REVALIDATION = "REQUIRE_REVALIDATION"
    REQUIRE_FAIL_SAFE = "REQUIRE_FAIL_SAFE"
    REQUIRE_MANUAL_OVERRIDE = "REQUIRE_MANUAL_OVERRIDE"
    REQUIRE_POLICY_EXCEPTION_REVIEW = "REQUIRE_POLICY_EXCEPTION_REVIEW"


class RiskLevel(str, Enum):
    """Canonical source: 03_core_specifications/07_decision_approval_matrix/
    07_decision_approval_matrix.md Section 9.1 ("Risk Level"). Cross-confirmed by
    usage in 08_policy_governance_model.md (e.g. Sections 16.2, 22). Registry-level
    illustrative lists in 06_registry_specs/action_registry/action_registry.md and
    06_registry_specs/decision_registry/decision_registry.md use a different,
    lowercase, non-matching value set and must not be treated as canonical.
    """

    INFO = "INFO"
    NOTICE = "NOTICE"
    WARNING = "WARNING"
    HIGH_RISK = "HIGH_RISK"
    CRITICAL_EMERGENCY = "CRITICAL_EMERGENCY"
    EXCEPTIONAL = "EXCEPTIONAL"


class ApprovalAuthority(str, Enum):
    """Canonical source: 08_policy_governance_model.md Section 13 ("Approval
    Authority Model"). Independently cross-confirmed by
    09_appendices/appendix_f_decision_approval_catalog/decision_approval_catalog.md
    ("Approval Level" list, itself sourced from 07_decision_approval_matrix.md).
    06_registry_specs/approval_registry/approval_registry.md Section 8 defines a
    different, non-matching 10-member set and must not be treated as canonical.

    Applied to `PolicyDecisionDTO.required_approval_level` (schemas/decision.py),
    merged in from 08_policy_governance_model.md Section 23
    ("PolicyDecisionResponseDTO"). 1_common_schema_dto.md Section 16.4's
    ApprovalRequestDTO field list still has no approval-level field of its own to
    attach this to — do not add one there to force additional use of this enum;
    ApprovalRequestDTO's own approval_status is a different, already-covered field.
    """

    NO_APPROVAL = "NO_APPROVAL"
    OPERATOR_ACK = "OPERATOR_ACK"
    SUPERVISOR_APPROVAL = "SUPERVISOR_APPROVAL"
    SAFETY_MANAGER_APPROVAL = "SAFETY_MANAGER_APPROVAL"
    WAR_ROOM_APPROVAL = "WAR_ROOM_APPROVAL"
    EXPERT_REVIEW = "EXPERT_REVIEW"
    POLICY_OWNER_APPROVAL = "POLICY_OWNER_APPROVAL"
    EMERGENCY_POLICY_BYPASS = "EMERGENCY_POLICY_BYPASS"
    POST_HOC_AUDIT_ONLY = "POST_HOC_AUDIT_ONLY"


class DecisionTier(str, Enum):
    """Lifecycle doc (0_canonical_object_lifecycle.md) Section 4.8."""

    ROUTINE = "ROUTINE"
    NOTICE = "NOTICE"
    WARNING = "WARNING"
    HIGH_RISK = "HIGH_RISK"
    CRITICAL_EMERGENCY = "CRITICAL_EMERGENCY"
    EXCEPTIONAL = "EXCEPTIONAL"


class PostAuditStatus(str, Enum):
    """Section 17.2."""

    PENDING = "PENDING"
    REVIEWED = "REVIEWED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ESCALATED = "ESCALATED"


class ReviewStatus(str, Enum):
    """Section 18.4."""

    PENDING = "PENDING"
    REVIEWED = "REVIEWED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ESCALATED = "ESCALATED"
    REQUIRES_POLICY_UPDATE = "REQUIRES_POLICY_UPDATE"
    REQUIRES_ONTOLOGY_UPDATE = "REQUIRES_ONTOLOGY_UPDATE"


class AggregationType(str, Enum):
    """Section 13.3."""

    RAW_SAMPLES = "RAW_SAMPLES"
    AVERAGE = "AVERAGE"
    MIN_MAX = "MIN_MAX"
    COUNT = "COUNT"
    LAST_VALUE = "LAST_VALUE"
    THRESHOLD_CROSSING = "THRESHOLD_CROSSING"


class ValidatorStatus(str, Enum):
    """Canonical source: 08_runtime_validation/validators/validators.md Section 7
    ("Validator Output Contract"), the `status` field. Also applied to
    RuntimeValidationResultDTO.result, which aggregates ValidatorResult outputs and
    uses the same status vocabulary per that document's Section 3
    ("Validator results are aggregated by Runtime Validation").
    """

    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"
    HOLD = "HOLD"
    RETRY = "RETRY"
    REQUIRES_REVALIDATION = "REQUIRES_REVALIDATION"
    REQUIRES_REAPPROVAL = "REQUIRES_REAPPROVAL"
    MANUAL_REVIEW_REQUIRED = "MANUAL_REVIEW_REQUIRED"
    BLOCK = "BLOCK"


class SafetyGatePassTerminalStatus(str, Enum):
    """Canonical source: 08_runtime_validation/toctou/toctou.md Section 21
    ("Lease Consumption Rule"), cross-confirmed by
    08_runtime_validation/idempotency/idempotency_control.md Section 9
    ("SafetyGatePass Terminal Token Rule"). Applied to SafetyGatePassDTO.status,
    which corresponds to the canonical `terminal_status` field named in
    safety_gate.md Section 8 ("SafetyGatePass Contract").
    """

    ISSUED = "ISSUED"
    DISPATCHING = "DISPATCHING"
    CONSUMED_ACCEPTED = "CONSUMED_ACCEPTED"
    CONSUMED_REJECTED = "CONSUMED_REJECTED"
    CONSUMED_DROPPED = "CONSUMED_DROPPED"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"


class Severity(str, Enum):
    """Canonical source: 08_runtime_validation/validators/validators.md Section 7
    ("Validator Output Contract"), the `severity` field.
    """

    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class CriticalityTier(str, Enum):
    """Canonical source: 08_runtime_validation/safety_gate/safety_gate.md Section 14
    ("Criticality Tier Handling"), cross-confirmed by
    08_runtime_validation/toctou/toctou.md Section 16 ("Validation Criticality Tier").
    Neither document gives a separate short-form enum string — these values encode the
    section heading text directly (e.g. "Tier 1. Safety-Critical") rather than
    inventing new terminology.
    """

    TIER_1_SAFETY_CRITICAL = "TIER_1_SAFETY_CRITICAL"
    TIER_2_OPERATIONAL_CRITICAL = "TIER_2_OPERATIONAL_CRITICAL"
    TIER_3_INFORMATIONAL = "TIER_3_INFORMATIONAL"


class SafetyGateResultStatus(str, Enum):
    """Canonical source: 08_runtime_validation/safety_gate/safety_gate.md Section 23
    ("SafetyGateResult Contract"), the `status` field. This is a distinct, smaller
    (6-member) list from `ValidatorStatus` (9 members) — the source document gives it
    as its own "Possible status" list, not as a cross-reference to Section 7.
    """

    PASS = "PASS"
    BLOCK = "BLOCK"
    MANUAL_REVIEW_REQUIRED = "MANUAL_REVIEW_REQUIRED"
    HOLD = "HOLD"
    REQUIRES_REVALIDATION = "REQUIRES_REVALIDATION"
    REQUIRES_REAPPROVAL = "REQUIRES_REAPPROVAL"


class BlockReason(str, Enum):
    """Canonical source: 08_runtime_validation/safety_gate/safety_gate.md Section 10
    ("SafetyGateBlock Contract"), "Possible block reasons" list.
    """

    MISSING_REQUIRED_VALIDATION = "MISSING_REQUIRED_VALIDATION"
    INVALID_RUNTIME_VALIDATION_RESULT = "INVALID_RUNTIME_VALIDATION_RESULT"
    STALE_STATE = "STALE_STATE"
    STALE_SNAPSHOT = "STALE_SNAPSHOT"
    TOCTOU_CONFLICT = "TOCTOU_CONFLICT"
    CRITICAL_CONDITION_CHANGED = "CRITICAL_CONDITION_CHANGED"
    INVALID_APPROVAL = "INVALID_APPROVAL"
    EXPIRED_APPROVAL = "EXPIRED_APPROVAL"
    POLICY_FAILED = "POLICY_FAILED"
    EXTERNAL_SYSTEM_UNREACHABLE = "EXTERNAL_SYSTEM_UNREACHABLE"
    ADAPTER_UNHEALTHY = "ADAPTER_UNHEALTHY"
    FEEDBACK_CHANNEL_UNAVAILABLE = "FEEDBACK_CHANNEL_UNAVAILABLE"
    IDEMPOTENCY_FAILURE = "IDEMPOTENCY_FAILURE"
    TERMINAL_SAFETY_GATE_PASS_REPLAY = "TERMINAL_SAFETY_GATE_PASS_REPLAY"
    SHACL_VALIDATION_FAILED = "SHACL_VALIDATION_FAILED"
    CLOCK_SKEW_EXCEEDED = "CLOCK_SKEW_EXCEEDED"
    UNKNOWN_REQUIRED_CONDITION = "UNKNOWN_REQUIRED_CONDITION"


class TimeTrustLevel(str, Enum):
    """Canonical source: 05_evidence_model/5_evidence_model.md Section 7.5
    ("time_trust_level Values"), cross-confirmed by 10_audit_observability_model.md
    Section 17 ("Evidence Audit must reference the following fields from the
    Evidence Model: ... time_trust_level ...").
    """

    HIGH_TIME_TRUST = "HIGH_TIME_TRUST"
    MEDIUM_TIME_TRUST = "MEDIUM_TIME_TRUST"
    LOW_TIME_TRUST = "LOW_TIME_TRUST"
    UNTRUSTED_TIME = "UNTRUSTED_TIME"
    UNKNOWN_TIME_TRUST = "UNKNOWN_TIME_TRUST"


class ClockSyncStatus(str, Enum):
    """Canonical source: 05_evidence_model/5_evidence_model.md Section 7.3
    ("clock_sync_status Values"), cross-confirmed by 10_audit_observability_model.md
    Section 17 ("Evidence Audit must reference the following fields from the
    Evidence Model: ... clock_sync_status ...").
    """

    SYNCED = "SYNCED"
    PARTIALLY_SYNCED = "PARTIALLY_SYNCED"
    UNSYNCED = "UNSYNCED"
    DRIFT_DETECTED = "DRIFT_DETECTED"
    OFFLINE_ESTIMATED = "OFFLINE_ESTIMATED"
    UNKNOWN = "UNKNOWN"


class SourceTrustLevel(str, Enum):
    """Canonical source: 05_evidence_model/5_evidence_model.md Section 6.1
    ("Source Trust Level"). Applies to `SourceMetadataDTO.source_trust_level`.
    """

    TRUSTED_SYSTEM = "TRUSTED_SYSTEM"
    VERIFIED_DEVICE = "VERIFIED_DEVICE"
    VERIFIED_HUMAN = "VERIFIED_HUMAN"
    VERIFIED_DOCUMENT = "VERIFIED_DOCUMENT"
    THIRD_PARTY_VERIFIED = "THIRD_PARTY_VERIFIED"
    AI_DERIVED = "AI_DERIVED"
    ATTESTED_AI_DERIVED = "ATTESTED_AI_DERIVED"
    UNVERIFIED_SOURCE = "UNVERIFIED_SOURCE"
    UNKNOWN_SOURCE = "UNKNOWN_SOURCE"


class EvidenceCategory(str, Enum):
    """Canonical source: 05_evidence_model/5_evidence_model.md Section 5.1
    ("Evidence Category"). Distinct from `evidence_type`, which remains a
    registry-managed vocabulary (06_registry_specs/evidence_registry) per
    1_common_schema_dto.md Section 8.2, not a fixed enum.
    """

    SENSOR_RAW = "SENSOR_RAW"
    SENSOR_DERIVED = "SENSOR_DERIVED"
    ROBOT_TELEMETRY = "ROBOT_TELEMETRY"
    WORKER_LOCATION = "WORKER_LOCATION"
    EQUIPMENT_TELEMETRY = "EQUIPMENT_TELEMETRY"
    EXTERNAL_SYSTEM_FEEDBACK = "EXTERNAL_SYSTEM_FEEDBACK"
    HUMAN_REPORT = "HUMAN_REPORT"
    DOCUMENT_VERIFIED = "DOCUMENT_VERIFIED"
    DOCUMENT_EXTRACTED = "DOCUMENT_EXTRACTED"
    PERMIT_RECORD = "PERMIT_RECORD"
    INSPECTION_RECORD = "INSPECTION_RECORD"
    SYSTEM_LOG = "SYSTEM_LOG"
    POLICY_DECISION = "POLICY_DECISION"
    ONTOLOGY_BINDING = "ONTOLOGY_BINDING"
    ONTOLOGY_INFERENCE = "ONTOLOGY_INFERENCE"
    DERIVED_AI = "DERIVED_AI"
    AUDIT_RECORD = "AUDIT_RECORD"
    THIRD_PARTY_API = "THIRD_PARTY_API"


class TimeSourceType(str, Enum):
    """Canonical source: 05_evidence_model/5_evidence_model.md Section 7.2
    ("time_source_type Values").
    """

    PTP = "PTP"
    NTP = "NTP"
    DEVICE_INTERNAL = "DEVICE_INTERNAL"
    EDGE_GATEWAY = "EDGE_GATEWAY"
    RELATIVE = "RELATIVE"
    MANUAL = "MANUAL"
    UNKNOWN = "UNKNOWN"


class ClockDriftCalculationMethod(str, Enum):
    """Canonical source: 05_evidence_model/5_evidence_model.md Section 7.4
    ("clock_drift_calculation_method Values").
    """

    PTP_SYNC = "PTP_SYNC"
    NTP_SYNC = "NTP_SYNC"
    EDGE_GATEWAY_COMPARISON = "EDGE_GATEWAY_COMPARISON"
    NEIGHBOR_COMPARISON = "NEIGHBOR_COMPARISON"
    SERVER_RECEIVE_DELTA = "SERVER_RECEIVE_DELTA"
    LAST_KNOWN_GOOD = "LAST_KNOWN_GOOD"
    MANUAL_ESTIMATION = "MANUAL_ESTIMATION"
    UNKNOWN = "UNKNOWN"


class EvidenceValidityStatus(str, Enum):
    """Canonical source: 05_evidence_model/5_evidence_model.md Section 9.2
    ("Evidence Validity Status"). A separate, larger enum from `ValidationStatus`
    (which governs `EvidenceDTO.validation_status`, sourced from
    1_common_schema_dto.md Section 5.2) — this one governs `EvidenceDTO.validity_status`.
    """

    VALID = "VALID"
    STALE = "STALE"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"
    CONFLICTED = "CONFLICTED"
    UNVERIFIED = "UNVERIFIED"
    SUPERSEDED = "SUPERSEDED"
    INVALID = "INVALID"
    ANONYMIZED = "ANONYMIZED"
    PSEUDONYMIZED = "PSEUDONYMIZED"
    PII_REDACTED = "PII_REDACTED"
    CRYPTO_SHREDDED = "CRYPTO_SHREDDED"
    RETENTION_EXPIRED = "RETENTION_EXPIRED"
    ACCESS_RESTRICTED = "ACCESS_RESTRICTED"
    LEGAL_HOLD = "LEGAL_HOLD"


class AttestationType(str, Enum):
    """Canonical source: 05_evidence_model/5_evidence_model.md Section 10.2
    ("Attestation Type").
    """

    HUMAN_STEWARD = "HUMAN_STEWARD"
    RULE_ENGINE = "RULE_ENGINE"
    CROSS_SYSTEM = "CROSS_SYSTEM"
    MULTI_PARTY = "MULTI_PARTY"
    DETERMINISTIC_PARSER = "DETERMINISTIC_PARSER"
    DOCUMENT_HASH_MATCH = "DOCUMENT_HASH_MATCH"


class TrustUpgradeStatus(str, Enum):
    """Canonical source: 05_evidence_model/5_evidence_model.md Section 10.3
    ("Trust Upgrade Status").
    """

    NO_UPGRADE = "NO_UPGRADE"
    TRUST_UPGRADE_PENDING = "TRUST_UPGRADE_PENDING"
    TRUST_UPGRADED_BY_RULE = "TRUST_UPGRADED_BY_RULE"
    TRUST_UPGRADED_BY_HUMAN = "TRUST_UPGRADED_BY_HUMAN"
    TRUST_UPGRADED_BY_CROSS_CHECK = "TRUST_UPGRADED_BY_CROSS_CHECK"
    TRUST_UPGRADED_BY_MULTI_PARTY = "TRUST_UPGRADED_BY_MULTI_PARTY"
    TRUST_UPGRADE_REJECTED = "TRUST_UPGRADE_REJECTED"


class ConflictStatus(str, Enum):
    """Canonical source: 05_evidence_model/5_evidence_model.md Section 14.1
    ("Conflict Status").
    """

    NO_CONFLICT = "NO_CONFLICT"
    CONFLICT_DETECTED = "CONFLICT_DETECTED"
    CONFLICT_UNDER_REVIEW = "CONFLICT_UNDER_REVIEW"
    CONFLICT_RESOLVED = "CONFLICT_RESOLVED"
    CONFLICT_ESCALATED = "CONFLICT_ESCALATED"
    FAIL_SAFE_ON_CONFLICT = "FAIL_SAFE_ON_CONFLICT"


class ConflictResolutionStrategy(str, Enum):
    """Canonical source: 05_evidence_model/5_evidence_model.md Section 14.2
    ("Conflict Resolution Strategy").
    """

    MANUAL_REVIEW_ONLY = "MANUAL_REVIEW_ONLY"
    TRUST_WEIGHTED_SELECTION = "TRUST_WEIGHTED_SELECTION"
    DEVICE_HEALTH_WEIGHTED_SELECTION = "DEVICE_HEALTH_WEIGHTED_SELECTION"
    SPATIAL_VOTING = "SPATIAL_VOTING"
    TEMPORAL_FRESHNESS_PRIORITY = "TEMPORAL_FRESHNESS_PRIORITY"
    SAFETY_CONSERVATIVE_PRIORITY = "SAFETY_CONSERVATIVE_PRIORITY"
    MAJORITY_VOTE = "MAJORITY_VOTE"
    FAIL_SAFE_ON_CONFLICT = "FAIL_SAFE_ON_CONFLICT"


class PrivacyLifecycleStatus(str, Enum):
    """Canonical source: 05_evidence_model/5_evidence_model.md Section 15.2
    ("Privacy Lifecycle Status").
    """

    PII_NOT_PRESENT = "PII_NOT_PRESENT"
    PII_PRESENT = "PII_PRESENT"
    PII_MASKED = "PII_MASKED"
    PII_PSEUDONYMIZED = "PII_PSEUDONYMIZED"
    PII_ANONYMIZED = "PII_ANONYMIZED"
    PII_CRYPTO_SHREDDED = "PII_CRYPTO_SHREDDED"
    PII_RETENTION_EXPIRED = "PII_RETENTION_EXPIRED"
    LEGAL_HOLD = "LEGAL_HOLD"


class NetworkHealthStatus(str, Enum):
    """Canonical source: 08_runtime_validation/network_health/network_health.md
    Section 7 ("Health Status Model"). Applies to `NetworkHealthResultDTO.health_status`.
    """

    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNREACHABLE = "UNREACHABLE"
    TIMEOUT = "TIMEOUT"
    CIRCUIT_OPEN = "CIRCUIT_OPEN"
    UNKNOWN = "UNKNOWN"


class CircuitBreakerStatus(str, Enum):
    """Canonical source: 08_runtime_validation/network_health/network_health.md
    Section 13 ("Circuit Breaker Rule").
    """

    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class SHACLValidationStatus(str, Enum):
    """Canonical source: 08_runtime_validation/shacl_shapes/shacl_shapes.md
    Section 17.1 ("SHACLValidationResultShape"), "Allowed validation statuses".
    """

    VALID = "VALID"
    INVALID = "INVALID"
    WARNING = "WARNING"
    SKIPPED = "SKIPPED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class IdempotencyLedgerStatus(str, Enum):
    """Canonical source: 08_runtime_validation/idempotency/idempotency_control.md
    Section 8 ("Idempotency Ledger"), "Recommended statuses".
    """

    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    BLOCKED = "BLOCKED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"
    TERMINAL = "TERMINAL"
    UNKNOWN = "UNKNOWN"


class DispatchStatus(str, Enum):
    """Canonical dispatch/execution state enum.

    Source of truth: 03_core_specifications/09_execution_adapter_model/9_execution_adapter_model.md
    Section 20 ("Dispatch Lifecycle"). Do not add members here from any other document's
    illustrative state list without updating that source document first.
    """

    CREATED = "CREATED"
    READY_TO_DISPATCH = "READY_TO_DISPATCH"
    DISPATCHED = "DISPATCHED"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    ACCEPTANCE_PENDING = "ACCEPTANCE_PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    IN_PROGRESS = "IN_PROGRESS"
    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    TIMEOUT = "TIMEOUT"
    ACK_TIMEOUT = "ACK_TIMEOUT"
    ACCEPTANCE_TIMEOUT = "ACCEPTANCE_TIMEOUT"
    FEEDBACK_TIMEOUT = "FEEDBACK_TIMEOUT"
    CANCELLED = "CANCELLED"
    FEEDBACK_MISSING = "FEEDBACK_MISSING"
    RECOVERY_REQUIRED = "RECOVERY_REQUIRED"
    MANUAL_OVERRIDE_REQUIRED = "MANUAL_OVERRIDE_REQUIRED"
    CLOSED = "CLOSED"
