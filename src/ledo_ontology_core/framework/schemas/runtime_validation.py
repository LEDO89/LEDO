"""Runtime Validation and Safety Gate DTO contracts from 01_common_schema_dto Section 17.3A.

These DTOs define architecture-level contracts only. They do not define domain
thresholds, legal rules, robot behavior rules, PLC semantics, or SCADA write semantics.

`ValidatorResultDTO` (and its subclasses) match the canonical `ValidatorResult` field
list in 08_runtime_validation/validators/validators.md Section 7 ("Validator Output
Contract") exactly, including field names (`result_id`, `status`, not `id`, `result`).
`RuntimeValidationResultDTO` has no separate canonical field-level contract of its own
in 08_runtime_validation/ — it keeps its prior shape, only its `result` value type
(`ValidatorStatus`) is canonical-sourced.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from ledo_ontology_core.framework.schemas.base import StrictDTO
from ledo_ontology_core.framework.schemas.enums import CriticalityTier, Severity, ValidatorStatus


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


class SHACLValidationResultDTO(ValidatorResultDTO):
    shacl_shape_ref: str | None = None


class NetworkHealthResultDTO(ValidatorResultDTO):
    adapter_ref: str | None = None


class IdempotencyResultDTO(ValidatorResultDTO):
    idempotency_key: str | None = None


class ApprovalValidityResultDTO(ValidatorResultDTO):
    approval_request_ref: str | None = None


class PolicyRevalidationResultDTO(ValidatorResultDTO):
    policy_ref: str | None = None


class EvidenceValidityResultDTO(ValidatorResultDTO):
    evidence_ref: str | None = None
