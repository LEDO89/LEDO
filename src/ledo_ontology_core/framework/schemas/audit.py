"""Audit DTO contracts from 01_common_schema_dto Section 18.5.

Section 18.5's stage-reference fields (`candidate_ref`, `decision_case_ref`, etc.) are
the canonical base shape, chosen over 10_audit_observability_model.md Section 9.1's
competing reference-only redesign for the same reason documented for
`ExecutionRequestDTO` (see execution.py). However, Section 9.1 also names real,
non-redundant capability that Section 18.5's original field list lacked entirely: a
tamper-evident hash chain (`content_hash`, `previous_record_hash`, `integrity_status`,
`integrity_policy_ref`) and multi-causality trace correlation (`correlation_id`,
`decision_trace_id`, `primary_causality_id`, `causality_ids`, Section 8.3-8.5). Those
fields, plus `severity`, `audit_reason`, `occurred_at`, `time_trust_level`,
`clock_sync_status`, and `source_system_ref`, were merged in as additive, optional
fields per explicit user instruction to fix the structural gap. Fields from Section
9.1 that duplicate existing capability (`actor_ref`/`actor_role` vs. existing
`actor_refs`; `result_status` vs. existing `final_status`; `audit_context_snapshot_ref`,
which assumes the rejected reference-delegation design) were not added.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from ledo_ontology_core.framework.schemas.base import StrictDTO
from ledo_ontology_core.framework.schemas.enums import (
    ClockSyncStatus,
    PostAuditStatus,
    Severity,
    TimeTrustLevel,
)


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
    # audit_event_type has no complete closed value list: 10_audit_observability_model.md
    # Section 16.1 gives only a partial mapping for dispatch-stage events.
    # DOMAIN_DECISION_REQUIRED before this becomes an enum.
    audit_event_type: str | None = None
    severity: Severity | None = None
    audit_reason: str | None = None
    occurred_at: datetime | None = None
    time_trust_level: TimeTrustLevel | None = None
    clock_sync_status: ClockSyncStatus | None = None
    source_system_ref: str | None = None
    correlation_id: str | None = None
    decision_trace_id: str | None = None
    primary_causality_id: str | None = None
    causality_ids: list[str] = Field(default_factory=list)
    integrity_policy_ref: str | None = None
    content_hash: str | None = None
    previous_record_hash: str | None = None
    # integrity_status has no closed value list found anywhere.
    # DOMAIN_DECISION_REQUIRED before this becomes an enum.
    integrity_status: str | None = None
