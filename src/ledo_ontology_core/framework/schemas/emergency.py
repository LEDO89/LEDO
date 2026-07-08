"""Emergency Fast-Path DTO contracts.

Source: 01_common_schema_dto.md Section 17.2 (EmergencyApprovedActionDTO), Section 19.2
(EmergencyActionSpecDTO), Section 18.4 (PostHocAuditDTO). File name matches the lifecycle
doc's own Section 12 "Recommended Code Mapping" (`schemas/emergency.py`).

These are structural contracts only. Populating real Emergency Action Registry content
(an actual `emergency_action_type` entry, a real `local_rule_id`, etc.) requires the
governance process described in 0_canonical_object_lifecycle.md Section 5 (Safety
Committee, Ontology Steward, Policy Owner approval) and is out of scope for schema code.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from ledo_ontology_core.framework.schemas.base import StrictDTO
from ledo_ontology_core.framework.schemas.context import TraceContextDTO
from ledo_ontology_core.framework.schemas.enums import PostAuditStatus, ReviewStatus
from ledo_ontology_core.framework.schemas.execution import RecoveryPolicyDTO, TimeoutPolicyDTO
from ledo_ontology_core.framework.schemas.refs import EntityRefDTO


class EmergencyActionSpecDTO(StrictDTO):
    emergency_action_type: str
    emergency_condition_type: str
    allowed_target_types: list[str] = Field(default_factory=list)
    required_minimal_evidence: list[str] = Field(default_factory=list)
    local_rule_id: str
    policy_id: str
    allowed_external_systems: list[str] = Field(default_factory=list)
    required_feedback: list[str] = Field(default_factory=list)
    timeout_policy: TimeoutPolicyDTO
    recovery_policy: RecoveryPolicyDTO
    audit_level: str
    approval_model: str
    post_hoc_audit_required: bool
    version: str
    owner: str
    valid_from: datetime
    valid_until: datetime | None = None


class EmergencyApprovedActionDTO(StrictDTO):
    emergency_approved_action_id: str
    emergency_policy_id: str
    emergency_condition_id: str
    action_type: str
    target_ref: EntityRefDTO
    minimal_evidence_refs: list[str] = Field(default_factory=list)
    local_rule_result: str
    idempotency_key: str
    timeout_policy: TimeoutPolicyDTO
    expected_feedback: dict
    post_hoc_audit_required: bool
    is_emergency_bypass: bool = True
    post_audit_status: PostAuditStatus
    trace_context: TraceContextDTO
    created_at_utc: datetime


class PostHocAuditDTO(StrictDTO):
    post_hoc_audit_id: str
    emergency_approved_action_ref: str
    execution_request_ref: str | None = None
    feedback_event_refs: list[str] = Field(default_factory=list)
    review_status: ReviewStatus
    reviewer_ref: str | None = None
    review_comment: str | None = None
    reviewed_at_utc: datetime | None = None
    required_followup_actions: list[str] = Field(default_factory=list)
    trace_context: TraceContextDTO
