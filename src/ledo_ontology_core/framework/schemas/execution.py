"""Approved action and execution DTO contracts from Section 17.

`ExternalControlRequestDTO`'s original 12-field shape matched
01_common_schema_dto/1_common_schema_dto.md Section 17.4 exactly.
09_execution_adapter_model/9_execution_adapter_model.md Section 16 describes the same
object with a 28-field list under the same name. Per the established precedent
(Section 17.3's ExecutionRequestDTO resolution), Section 17.4's field-holding design
stays the baseline; the real, non-redundant fields Section 16 named that Section 17.4
lacked (adapter type/mode, dispatch tracking, ACK/ACCEPT/feedback deadlines, adapter-local
timing, clock sync) were merged in as additive fields. `sent_at`/`platform_sent_at` and
`trace_id`/`correlation_id` from Section 16 were treated as the same concepts as the
existing `sent_at_utc` and `trace_context` fields, not duplicated.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field, model_validator

from ledo_ontology_core.framework.schemas.base import StrictDTO
from ledo_ontology_core.framework.schemas.context import TraceContextDTO
from ledo_ontology_core.framework.schemas.enums import ClockSyncStatus, DispatchStatus, RiskLevel
from ledo_ontology_core.framework.schemas.refs import EntityRefDTO


class ApprovedActionDTO(StrictDTO):
    approved_action_id: str
    candidate_ref: str
    decision_case_ref: str
    # action_type is a registry-managed vocabulary (06_registry_specs/action_registry),
    # not a fixed enum. Same applies to action_type on ExecutionRequestDTO below.
    action_type: str
    target_ref: EntityRefDTO
    constraints: dict[str, Any] = Field(default_factory=dict)
    approval_context: dict[str, Any]
    policy_result: dict[str, Any]
    evidence_refs: list[str] = Field(default_factory=list)
    risk_level: RiskLevel
    valid_until: datetime
    idempotency_key: str
    trace_context: TraceContextDTO
    created_at_utc: datetime


class ExecutionRequestDTO(StrictDTO):
    execution_request_id: str
    approved_action_ref: str
    action_type: str
    target_ref: EntityRefDTO
    external_system_type: str
    external_system_id: str
    execution_constraints: dict[str, Any] = Field(default_factory=dict)
    expected_feedback: dict[str, Any]
    timeout_policy: dict[str, Any]
    retry_policy: dict[str, Any]
    recovery_policy: dict[str, Any]
    idempotency_key: str
    execution_lease: dict[str, Any]
    trace_context: TraceContextDTO
    created_at_utc: datetime

    @model_validator(mode="after")
    def require_safety_gate_lease(self) -> "ExecutionRequestDTO":
        if not self.execution_lease.get("safety_gate_pass_id"):
            raise ValueError("ExecutionRequestDTO requires a SafetyGatePass lease reference")
        return self


class ExternalControlRequestDTO(StrictDTO):
    external_request_id: str
    execution_request_ref: str
    adapter_id: str
    external_system_type: str
    protocol: str
    endpoint: str
    payload: dict[str, Any]
    idempotency_key: str
    timeout_policy: dict[str, Any]
    expected_feedback: dict[str, Any]
    trace_context: TraceContextDTO
    sent_at_utc: datetime
    execution_context_snapshot_ref: str | None = None
    adapter_type: str | None = None
    adapter_mode: str | None = None
    external_request_type: str | None = None
    external_payload_ref: str | None = None
    external_payload_hash: str | None = None
    idempotency_expires_at: datetime | None = None
    dispatch_context_ref: str | None = None
    dispatch_attempt: int | None = Field(default=None, ge=0)
    dispatch_status: DispatchStatus | None = None
    ack_deadline: datetime | None = None
    acceptance_deadline: datetime | None = None
    feedback_deadline: datetime | None = None
    adapter_local_received_at: datetime | None = None
    adapter_local_accepted_at: datetime | None = None
    clock_sync_status: ClockSyncStatus | None = None
    clock_drift_estimate_ms: float | None = None
    decision_trace_id: str | None = None


class TimeoutPolicyDTO(StrictDTO):
    timeout_ms: int = Field(ge=0)
    on_timeout_action: str
    max_wait_ms: int = Field(ge=0)
    requires_recovery: bool
    notify_actor_refs: list[str] = Field(default_factory=list)


class RetryPolicyDTO(StrictDTO):
    max_retries: int = Field(ge=0)
    retry_interval_ms: int = Field(ge=0)
    backoff_strategy: str
    retryable_errors: list[str] = Field(default_factory=list)
    non_retryable_errors: list[str] = Field(default_factory=list)


class RecoveryPolicyDTO(StrictDTO):
    recovery_policy_id: str
    recovery_type: str
    safe_state_target: str | None = None
    compensating_action_type: str | None = None
    manual_override_required: bool
    notify_actor_refs: list[str] = Field(default_factory=list)


class IdempotencyContextDTO(StrictDTO):
    idempotency_key: str
    deduplication_window_ms: int = Field(ge=0)
    original_request_id: str | None = None
    duplicate_detected: bool
    dedupe_strategy: str
