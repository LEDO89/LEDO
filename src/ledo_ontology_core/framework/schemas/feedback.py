"""Feedback DTO contracts from 01_common_schema_dto Section 18.

`FeedbackEventDTO`'s original 15-field shape matched Section 18.1 exactly.
`09_execution_adapter_model/9_execution_adapter_model.md` Section 17 describes the
same object with a 21-field list under the same name. Per the established precedent
(Section 17.3's `ExecutionRequestDTO` resolution), Section 18.1's field-holding design
stays the baseline; the real, non-redundant fields Section 17 named that Section 18.1
lacked (result detail, actual execution timing, reconciliation/audit routing flags,
decision trace correlation) were merged in as additive fields. `external_control_request_ref`
and `external_system_id` from Section 17 were treated as the same concepts as the
existing `external_request_ref` and `source_system` fields (not duplicated).
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field

from ledo_ontology_core.framework.schemas.base import StrictDTO
from ledo_ontology_core.framework.schemas.context import ConfidenceDTO, TraceContextDTO
from ledo_ontology_core.framework.schemas.enums import DispatchStatus


class FeedbackEventDTO(StrictDTO):
    feedback_event_id: str
    execution_request_ref: str
    external_request_ref: str | None = None
    source_system: str
    feedback_type: str
    status: str
    payload: dict[str, Any]
    timestamp_utc: datetime
    confidence: ConfidenceDTO
    trace_context: TraceContextDTO
    correlation_id: str | None = None
    error_code: str | None = None
    recovery_required: bool
    is_emergency_bypass: bool = False
    post_audit_required: bool = False
    # DOMAIN_DECISION_REQUIRED: feedback_status and result_status have no closed value list; kept as str, not enums — see 03_core_specifications/09_execution_adapter_model/9_execution_adapter_model.md Section 17
    feedback_status: str | None = None
    result_status: str | None = None
    result_message: str | None = None
    external_reference_id: str | None = None
    actual_started_at: datetime | None = None
    actual_completed_at: datetime | None = None
    observed_state_refs: list[str] = Field(default_factory=list)
    feedback_payload_ref: str | None = None
    error_detail_ref: str | None = None
    requires_reconciliation: bool = False
    requires_audit: bool = False
    decision_trace_id: str | None = None


class WorldStateReconciliationDTO(StrictDTO):
    reconciliation_id: str
    feedback_event_ref: str
    affected_state_refs: list[str] = Field(default_factory=list)
    previous_states: list[str] = Field(default_factory=list)
    reconciled_states: list[str] = Field(default_factory=list)
    conflict_detected: bool
    reconciliation_result: str
    created_at_utc: datetime
    trace_context: TraceContextDTO


class ExecutionStateDTO(StrictDTO):
    execution_state_id: str
    execution_request_ref: str
    state: DispatchStatus
    last_feedback_ref: str | None = None
    updated_at_utc: datetime
    timeout_at_utc: datetime | None = None
    recovery_required: bool
    trace_context: TraceContextDTO
