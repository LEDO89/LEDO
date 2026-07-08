"""Approval DTO contracts from 01_common_schema_dto Section 16."""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from ledo_ontology_core.framework.schemas.base import StrictDTO
from ledo_ontology_core.framework.schemas.context import TraceContextDTO
from ledo_ontology_core.framework.schemas.refs import ActorRefDTO, EntityRefDTO


class ApprovalRequestDTO(StrictDTO):
    approval_request_id: str
    decision_case_ref: str
    action_type: str
    target_ref: EntityRefDTO
    required_role: str
    required_clearance: str | None = None
    approver_ref: ActorRefDTO | None = None
    approval_status: str
    approval_reason: str | None = None
    expires_at_utc: datetime
    created_at_utc: datetime
    approved_at_utc: datetime | None = None
    trace_context: TraceContextDTO


class ApprovalDecisionDTO(StrictDTO):
    approval_decision_id: str
    approval_request_ref: str
    decision: str
    decided_by: ActorRefDTO
    decision_reason: str
    decision_time_utc: datetime
    policy_refs: list[str] = Field(default_factory=list)
    trace_context: TraceContextDTO
