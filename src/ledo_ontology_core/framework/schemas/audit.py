"""Audit DTO contracts from 01_common_schema_dto Section 18.5."""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from ledo_ontology_core.framework.schemas.base import StrictDTO
from ledo_ontology_core.framework.schemas.enums import PostAuditStatus


class AuditRecordDTO(StrictDTO):
    audit_record_id: str
    trace_id: str
    lifecycle_path: str
    event_refs: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    candidate_ref: str | None = None
    decision_case_ref: str | None = None
    approval_request_ref: str | None = None
    approved_action_ref: str | None = None
    execution_request_ref: str | None = None
    external_request_ref: str | None = None
    feedback_event_ref: str | None = None
    policy_refs: list[str] = Field(default_factory=list)
    actor_refs: list[str] = Field(default_factory=list)
    final_status: str
    created_at_utc: datetime
    is_emergency_bypass: bool = False
    post_audit_status: PostAuditStatus | None = None
    post_hoc_audit_ref: str | None = None
