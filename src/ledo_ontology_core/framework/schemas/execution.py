"""Approved action and execution DTO contracts from Section 17."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field, model_validator

from ledo_ontology_core.framework.schemas.base import StrictDTO
from ledo_ontology_core.framework.schemas.context import TraceContextDTO
from ledo_ontology_core.framework.schemas.enums import RiskLevel
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
