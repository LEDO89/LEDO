"""Decision DTO contracts from 01_common_schema_dto Section 16.

`PolicyDecisionDTO`'s original 8-field shape matched Section 19.7 exactly.
08_policy_governance_model.md Section 23 describes a differently-named but same-purpose
object, `PolicyDecisionResponseDTO`, with a 27-field list. Per the established
precedent (Section 17.3's ExecutionRequestDTO resolution), Section 19.7's field set
stays the baseline; the real, non-redundant fields Section 23 named that Section 19.7
lacked (policy engine identity, categorized policy-match refs, required approval/role/
evidence/clearance, safety-gate/audit/revalidation/fail-safe routing flags, trace
correlation) were merged in as additive fields. Section 23's `decision_reason` and
`created_at` were treated as the same concepts as the existing `reason` and
`evaluated_at_utc` fields, not duplicated.

`required_approval_level` is the first DTO field application of the `ApprovalAuthority`
enum (previously prepared in enums.py but unwired to any field).
"""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from ledo_ontology_core.framework.schemas.base import StrictDTO
from ledo_ontology_core.framework.schemas.context import TraceContextDTO
from ledo_ontology_core.framework.schemas.enums import (
    ApprovalAuthority,
    DecisionTier,
    PolicyDecisionResult,
    RiskLevel,
)


class DecisionCaseDTO(StrictDTO):
    decision_case_id: str
    candidate_ref: str
    decision_tier: DecisionTier
    risk_level: RiskLevel
    # DOMAIN_DECISION_REQUIRED: urgency has no closed value list in
    # 01_common_schema_dto.md Section 16.3 — kept as str, not an enum.
    urgency: str
    routing_result: str
    required_approval: bool
    policy_precheck_result: str | None = None
    evidence_summary: str | None = None
    state_freshness_result: str | None = None
    recommended_next_step: str | None = None
    trace_context: TraceContextDTO


class PolicyDecisionDTO(StrictDTO):
    policy_decision_id: str
    policy_refs: list[str] = Field(default_factory=list)
    input_context: dict
    decision_result: PolicyDecisionResult
    reason: str
    obligations: list[str] = Field(default_factory=list)
    denial_reasons: list[str] = Field(default_factory=list)
    evaluated_at_utc: datetime
    policy_engine: str | None = None
    policy_engine_version: str | None = None
    policy_bundle_version: str | None = None
    input_context_hash: str | None = None
    policy_context_ref: str | None = None
    resolution_context_ref: str | None = None
    audit_context_ref: str | None = None
    required_approval_level: ApprovalAuthority | None = None
    matched_policy_refs: list[str] = Field(default_factory=list)
    denied_policy_refs: list[str] = Field(default_factory=list)
    resolved_policy_refs: list[str] = Field(default_factory=list)
    suppressed_policy_refs: list[str] = Field(default_factory=list)
    policy_resolution_ref: str | None = None
    required_evidence_types: list[str] = Field(default_factory=list)
    required_roles: list[str] = Field(default_factory=list)
    required_clearance: str | None = None
    requires_safety_gate: bool = False
    requires_post_hoc_audit: bool = False
    requires_revalidation: bool = False
    requires_fail_safe: bool = False
    trace_id: str | None = None
    correlation_id: str | None = None
    decision_trace_id: str | None = None
