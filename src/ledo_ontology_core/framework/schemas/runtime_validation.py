"""Runtime Validation and Safety Gate DTO contracts from 01_common_schema_dto Section 17.3A.

These DTOs define architecture-level contracts only. They do not define domain
thresholds, legal rules, robot behavior rules, PLC semantics, or SCADA write semantics.

`result` fields are kept as plain `str` rather than an enum: the spec does not give an
explicit closed value list for them (unlike `validation_status`, `path_type`, etc.), and
per the plan's ambiguity standard, enum values are not invented without a source list.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from ledo_ontology_core.framework.schemas.base import StrictDTO


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
    result: str
    checked_at: datetime
    input_refs: list[str] = Field(default_factory=list)
    validator_result_refs: list[str] = Field(default_factory=list)
    failure_reasons: list[str] = Field(default_factory=list)
    trace_id: str
    correlation_id: str | None = None
    audit_ref: str | None = None


class ValidatorResultDTO(StrictDTO):
    id: str
    validator_id: str
    approved_action_id: str
    result: str
    checked_at: datetime
    failure_reasons: list[str] = Field(default_factory=list)
    trace_id: str
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
