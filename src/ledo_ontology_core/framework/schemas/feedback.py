"""Feedback DTO contracts from 01_common_schema_dto Section 18."""

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
