"""Safety Gate DTO contracts from 01_common_schema_dto Section 17.3A.

Architecture-level contracts only — no Safety Gate decision logic lives here. `status`
fields are kept as plain `str`: the spec does not give an explicit closed value list for
them here (unlike `validation_status`, `path_type`, etc.).
"""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from ledo_ontology_core.framework.schemas.base import StrictDTO


class SafetySnapshotDTO(StrictDTO):
    id: str
    snapshot_version: str
    ontology_version: str
    policy_version: str
    registry_version: str
    status: str
    created_at: datetime
    expires_at: datetime
    checksum: str
    trace_id: str
    audit_ref: str | None = None


class SafetyGateInputDTO(StrictDTO):
    id: str
    approved_action_id: str
    runtime_validation_result_id: str
    safety_snapshot_id: str
    action_type: str
    input_refs: list[str] = Field(default_factory=list)
    trace_id: str
    correlation_id: str | None = None


class SafetyGatePassDTO(StrictDTO):
    id: str
    approved_action_id: str
    runtime_validation_result_id: str
    action_type: str
    status: str
    issued_at: datetime
    expires_at: datetime
    idempotency_key: str
    trace_id: str
    correlation_id: str | None = None
    audit_ref: str | None = None


class SafetyGateBlockDTO(StrictDTO):
    id: str
    approved_action_id: str
    runtime_validation_result_id: str
    action_type: str
    status: str
    checked_at: datetime
    failure_reasons: list[str] = Field(default_factory=list)
    trace_id: str
    correlation_id: str | None = None
    audit_ref: str | None = None
