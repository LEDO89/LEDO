"""Safety Gate DTO contracts from 01_common_schema_dto Section 17.3A.

Architecture-level contracts only — no Safety Gate decision logic lives here.

`SafetyGatePassDTO.status` uses `SafetyGatePassTerminalStatus`, sourced from
08_runtime_validation/toctou/toctou.md Section 21 and cross-confirmed by
08_runtime_validation/idempotency/idempotency_control.md Section 9; it corresponds to
the canonical `terminal_status` field named in safety_gate.md Section 8.

`SafetySnapshotDTO.status` and `SafetyGateBlockDTO.status` remain plain `str`: no
closed value list for either specific field was found in 08_runtime_validation/ or
01_common_schema_dto.md. `SafetyGateBlockDTO`'s canonical field list
(safety_gate.md Section 10) does not include a `status` field at all — the field
present here has no confirmed canonical source and should not be treated as resolved.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from ledo_ontology_core.framework.schemas.base import StrictDTO
from ledo_ontology_core.framework.schemas.enums import SafetyGatePassTerminalStatus


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
    status: SafetyGatePassTerminalStatus
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
