"""Runtime Validation and Safety Gate DTO contracts from 01_common_schema_dto Section 17.3A.

These DTOs define architecture-level contracts only. They do not define domain
thresholds, legal rules, robot behavior rules, PLC semantics, or SCADA write semantics.

`ValidatorResultDTO` (and its subclasses) match the canonical `ValidatorResult` field
list in 08_runtime_validation/validators/validators.md Section 7 ("Validator Output
Contract") exactly, including field names (`result_id`, `status`, not `id`, `result`).
`RuntimeValidationResultDTO` has no separate canonical field-level contract of its own
in 08_runtime_validation/ — it keeps its prior shape, only its `result` value type
(`ValidatorStatus`) is canonical-sourced.

The specialized subclasses below were previously near-empty (one optional reference
field each). Each has now been expanded to match its own dedicated contract section:
`TOCTOUResultDTO` (toctou.md Section 24, "TOCTOU Validation Result"),
`SHACLValidationResultDTO` (shacl_shapes.md Sections 17.1 and 20),
`NetworkHealthResultDTO` (network_health.md Section 16, "NetworkHealthResult Contract"),
`IdempotencyResultDTO` (idempotency_control.md Sections 8 and 19). Fields already
covered by the `ValidatorResultDTO` base (`result_id`, `checked_at`, `status`,
`trace_id`, `correlation_id`, `audit_ref`, `warning_reasons`, `failure_reasons`,
`safety_gate_eligible`) were not duplicated even where a source section re-lists them.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from ledo_ontology_core.framework.schemas.base import StrictDTO
from ledo_ontology_core.framework.schemas.enums import (
    BlockReason,
    CircuitBreakerStatus,
    CriticalityTier,
    IdempotencyLedgerStatus,
    NetworkHealthStatus,
    SHACLValidationStatus,
    Severity,
    ValidatorStatus,
)


class RuntimeValidationInputDTO(StrictDTO):
    id: str
    approved_action_id: str
    action_type: str
    input_refs: list[str] = Field(default_factory=list)
    trace_id: str
    correlation_id: str | None = None
    created_at_utc: datetime


class RuntimeValidationResultDTO(StrictDTO):
    id: str
    approved_action_id: str
    action_type: str
    result: ValidatorStatus
    checked_at: datetime
    input_refs: list[str] = Field(default_factory=list)
    validator_result_refs: list[str] = Field(default_factory=list)
    failure_reasons: list[str] = Field(default_factory=list)
    trace_id: str
    correlation_id: str | None = None
    audit_ref: str | None = None


class ValidatorResultDTO(StrictDTO):
    result_id: str
    validator_id: str
    validator_version: str
    approved_action_id: str
    action_type: str
    status: ValidatorStatus
    severity: Severity
    tier: CriticalityTier
    checked_at: datetime
    input_refs: list[str] = Field(default_factory=list)
    failure_reasons: list[str] = Field(default_factory=list)
    warning_reasons: list[str] = Field(default_factory=list)
    suggested_next_state: str | None = None
    safety_gate_eligible: bool
    trace_id: str
    correlation_id: str | None = None
    audit_ref: str | None = None


class TOCTOUResultDTO(ValidatorResultDTO):
    snapshot_comparison_ref: str | None = None
    approval_snapshot_ref: str | None = None
    execution_snapshot_ref: str | None = None
    changed_fields: list[str] = Field(default_factory=list)
    stale_fields: list[str] = Field(default_factory=list)
    conflict_fields: list[str] = Field(default_factory=list)
    block_reasons: list[BlockReason] = Field(default_factory=list)
    required_reapproval: bool = False


class SHACLValidationResultDTO(ValidatorResultDTO):
    shacl_shape_ref: str | None = None
    shape_id: str | None = None
    shape_version: str | None = None
    target_node: str | None = None
    target_type: str | None = None
    validation_status: SHACLValidationStatus | None = None
    violations: list[str] = Field(default_factory=list)


class NetworkHealthResultDTO(ValidatorResultDTO):
    adapter_ref: str | None = None
    external_system_id: str | None = None
    adapter_id: str | None = None
    health_status: NetworkHealthStatus | None = None
    # DOMAIN_DECISION_REQUIRED: heartbeat_status and feedback_channel_status have no closed value list; kept as str, not enums — see 08_runtime_validation/network_health/network_health.md Section 16
    heartbeat_status: str | None = None
    latency_ms: float | None = None
    error_rate: float | None = None
    circuit_breaker_status: CircuitBreakerStatus | None = None
    feedback_channel_status: str | None = None


class IdempotencyResultDTO(ValidatorResultDTO):
    idempotency_key: str | None = None
    safety_gate_pass_id: str | None = None
    execution_request_id: str | None = None
    external_control_request_id: str | None = None
    target_external_system: str | None = None
    first_seen_at: datetime | None = None
    last_seen_at: datetime | None = None
    ledger_status: IdempotencyLedgerStatus | None = None
    previous_result_ref: str | None = None
    terminal_token_ref: str | None = None
    # DOMAIN_DECISION_REQUIRED: terminal_token_status has no closed value list; kept as str, not an enum — see 08_runtime_validation/idempotency/idempotency_control.md Section 19
    terminal_token_status: str | None = None


class ApprovalValidityResultDTO(ValidatorResultDTO):
    approval_request_ref: str | None = None


class PolicyRevalidationResultDTO(ValidatorResultDTO):
    policy_ref: str | None = None


class EvidenceValidityResultDTO(ValidatorResultDTO):
    evidence_ref: str | None = None
