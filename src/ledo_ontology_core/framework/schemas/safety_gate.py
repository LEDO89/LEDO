"""Safety Gate DTO contracts from 01_common_schema_dto Section 17.3A.

Architecture-level contracts only — no Safety Gate decision logic lives here.

`SafetyGatePassDTO` and `SafetyGateBlockDTO` match the canonical field lists in
08_runtime_validation/safety_gate/safety_gate.md Sections 8 and 10 exactly, including
field names (`safety_gate_pass_id`/`terminal_status`, `safety_gate_block_id`/
`blocked_at`/`block_reasons`, not the previous `id`/`status`/`checked_at`/
`failure_reasons`). `SafetyGateResultDTO` is the Section 23 aggregate contract,
previously undefined in code.

`SafetySnapshotDTO` field names/additions (`snapshot_id`, `valid_until`,
`source_state_versions`, `target_scope`, `site_ref`, `zone_ref`, `critical_state_refs`,
`schema_version`) are cross-confirmed by both safety_gate.md Section 11.1 (via
shacl_shapes.md) and validators.md Section 10.2's `snapshot_freshness_validator`
input list. `status` remains plain `str`: no closed value list for this field was
found anywhere.

`SafetyGateInputDTO` is expanded to safety_gate.md Section 6's full "Recommended
inputs" list. Per that section's own text ("For safety-critical actions, missing
required input must result in block"), only `approved_action_id`, `action_type`,
`runtime_validation_result_ref`, and `safety_snapshot_ref` are treated as always
required; the remaining validator-category result refs are optional, since not
every action type exercises every validator category.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from ledo_ontology_core.framework.schemas.base import StrictDTO
from ledo_ontology_core.framework.schemas.enums import (
    BlockReason,
    CriticalityTier,
    SafetyGatePassTerminalStatus,
    SafetyGateResultStatus,
    Severity,
)


class SafetySnapshotDTO(StrictDTO):
    snapshot_id: str
    snapshot_version: str
    ontology_version: str
    policy_version: str
    registry_version: str
    status: str
    created_at: datetime
    valid_until: datetime
    source_state_versions: dict[str, str] = Field(default_factory=dict)
    target_scope: str
    site_ref: str
    zone_ref: str
    critical_state_refs: list[str] = Field(default_factory=list)
    schema_version: str
    checksum: str
    trace_id: str
    audit_ref: str | None = None


class SafetyGateInputDTO(StrictDTO):
    safety_gate_input_id: str
    approved_action_id: str
    action_type: str
    runtime_validation_result_ref: str
    safety_snapshot_ref: str
    validator_result_summary_ref: str | None = None
    toctou_result_ref: str | None = None
    shacl_validation_result_ref: str | None = None
    network_health_result_ref: str | None = None
    idempotency_result_ref: str | None = None
    approval_validity_result_ref: str | None = None
    policy_revalidation_result_ref: str | None = None
    evidence_validity_result_ref: str | None = None
    capability_availability_result_ref: str | None = None
    input_refs: list[str] = Field(default_factory=list)
    trace_id: str
    correlation_id: str | None = None


class SafetyGatePassDTO(StrictDTO):
    safety_gate_pass_id: str
    approved_action_id: str
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
    runtime_validation_result_ref: str
    trace_id: str
    correlation_id: str | None = None
    terminal_status: SafetyGatePassTerminalStatus


class SafetyGateBlockDTO(StrictDTO):
    safety_gate_block_id: str
    approved_action_id: str
    action_type: str
    blocked_at: datetime
    block_reasons: list[BlockReason] = Field(default_factory=list)
    failed_validator_refs: list[str] = Field(default_factory=list)
    failed_runtime_validation_ref: str | None = None
    safety_snapshot_ref: str
    severity: Severity
    tier: CriticalityTier
    suggested_next_state: str | None = None
    manual_review_required: bool
    trace_id: str
    correlation_id: str | None = None
    audit_ref: str | None = None


class SafetyGateResultDTO(StrictDTO):
    result_id: str
    approved_action_id: str
    action_type: str
    status: SafetyGateResultStatus
    issued_pass_ref: str | None = None
    block_ref: str | None = None
    checked_at: datetime
    runtime_validation_result_ref: str
    safety_snapshot_ref: str
    validator_summary_ref: str | None = None
    decision_reasons: list[str] = Field(default_factory=list)
    failure_reasons: list[str] = Field(default_factory=list)
    warning_reasons: list[str] = Field(default_factory=list)
    suggested_next_state: str | None = None
    trace_id: str
    correlation_id: str | None = None
    audit_ref: str | None = None
