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
    07_decision_approval_matrix.md Section 8 ("Risk Level"). Cross-confirmed by
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
