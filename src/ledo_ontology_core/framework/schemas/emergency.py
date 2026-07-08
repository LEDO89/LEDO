"""Emergency Fast-Path DTO contracts.

Source: 01_common_schema_dto.md Section 17.2 (EmergencyApprovedActionDTO), Section 19.2
(EmergencyActionSpecDTO), Section 18.4 (PostHocAuditDTO). File name matches the lifecycle
doc's own Section 12 "Recommended Code Mapping" (`schemas/emergency.py`).

`EmergencyRuntimeValidationInputDTO`, `EmergencyRuntimeValidationResultDTO`,
`EmergencySafetyGatePassDTO`, `EmergencySafetyGateBlockDTO`, and
`EmergencyExecutionRequestDTO` are required by the emergency lifecycle named in
0_canonical_object_lifecycle.md Section 4.11, 03_core_specifications/07_decision_approval_matrix.md
(e.g. Sections 4, 18, 33), and 08_policy_governance_model.md Section 16, but none of those
documents give a dedicated field-level schema for the Emergency-prefixed variants — they
only appear as flow-step object names. Each is therefore modeled as a structural mirror
of its standard (non-emergency) counterpart in `runtime_validation.py`, `safety_gate.py`,
and `execution.py`, substituting `emergency_approved_action_id`/`_ref` for
`approved_action_id`/`_ref`. This is not new domain content — it applies the same shape
the standard objects already use, per the architecture's explicit requirement that the
emergency path run through the same validation stages as the standard path.

These are structural contracts only. Populating real Emergency Action Registry content
(an actual `emergency_action_type` entry, a real `local_rule_id`, etc.) requires the
governance process described in 0_canonical_object_lifecycle.md Section 5 (Safety
Committee, Ontology Steward, Policy Owner approval) and is out of scope for schema code.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field, model_validator

from ledo_ontology_core.framework.schemas.base import StrictDTO
from ledo_ontology_core.framework.schemas.context import TraceContextDTO
from ledo_ontology_core.framework.schemas.enums import (
    BlockReason,
    CriticalityTier,
    PostAuditStatus,
    ReviewStatus,
    SafetyGatePassTerminalStatus,
    Severity,
    ValidatorStatus,
)
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


class EmergencyRuntimeValidationInputDTO(StrictDTO):
    id: str
    emergency_approved_action_id: str
    action_type: str
    input_refs: list[str] = Field(default_factory=list)
    trace_id: str
    correlation_id: str | None = None
    created_at_utc: datetime


class EmergencyRuntimeValidationResultDTO(StrictDTO):
    id: str
    emergency_approved_action_id: str
    action_type: str
    result: ValidatorStatus
    checked_at: datetime
    input_refs: list[str] = Field(default_factory=list)
    validator_result_refs: list[str] = Field(default_factory=list)
    failure_reasons: list[str] = Field(default_factory=list)
    trace_id: str
    correlation_id: str | None = None
    audit_ref: str | None = None


class EmergencySafetyGatePassDTO(StrictDTO):
    emergency_safety_gate_pass_id: str
    emergency_approved_action_id: str
    action_type: str
    issued_at: datetime
    expires_at: datetime
    lease_duration_ms: int = Field(ge=0)
    lease_started_monotonic_ms: int = Field(ge=0)
    lease_expires_monotonic_ms: int = Field(ge=0)
    target_external_system: str
    execution_request_scope: str
    idempotency_key: str
    safety_snapshot_ref: str
    emergency_runtime_validation_result_ref: str
    trace_id: str
    correlation_id: str | None = None
    terminal_status: SafetyGatePassTerminalStatus


class EmergencySafetyGateBlockDTO(StrictDTO):
    emergency_safety_gate_block_id: str
    emergency_approved_action_id: str
    action_type: str
    blocked_at: datetime
    block_reasons: list[BlockReason] = Field(default_factory=list)
    failed_validator_refs: list[str] = Field(default_factory=list)
    failed_emergency_runtime_validation_ref: str | None = None
    safety_snapshot_ref: str
    severity: Severity
    tier: CriticalityTier
    suggested_next_state: str | None = None
    manual_review_required: bool
    trace_id: str
    correlation_id: str | None = None
    audit_ref: str | None = None


class EmergencyExecutionRequestDTO(StrictDTO):
    execution_request_id: str
    emergency_approved_action_ref: str
    action_type: str
    target_ref: EntityRefDTO
    external_system_type: str
    external_system_id: str
    execution_constraints: dict[str, Any] = Field(default_factory=dict)
    expected_feedback: dict[str, Any]
    timeout_policy: dict[str, Any]
    retry_policy: dict[str, Any]
    recovery_policy: dict[str, Any]
    idempotency_key: str
    execution_lease: dict[str, Any]
    trace_context: TraceContextDTO
    created_at_utc: datetime

    @model_validator(mode="after")
    def require_emergency_safety_gate_lease(self) -> "EmergencyExecutionRequestDTO":
        # 07_decision_approval_matrix.md: "EmergencyExecutionRequest MUST NOT be
        # created unless an EmergencySafetyGatePass has been issued from a valid
        # EmergencyRuntimeValidationResult."
        if not self.execution_lease.get("emergency_safety_gate_pass_id"):
            raise ValueError(
                "EmergencyExecutionRequestDTO requires an EmergencySafetyGatePass lease reference"
            )
        return self


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
