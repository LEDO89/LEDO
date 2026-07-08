from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from ledo_ontology_core.framework.schemas import (
    EmergencyActionSpecDTO,
    EmergencyApprovedActionDTO,
    EmergencyExecutionRequestDTO,
    EmergencyRuntimeValidationInputDTO,
    EmergencyRuntimeValidationResultDTO,
    EmergencySafetyGateBlockDTO,
    EmergencySafetyGatePassDTO,
    EntityRefDTO,
    PostHocAuditDTO,
    RecoveryPolicyDTO,
    TimeoutPolicyDTO,
    TraceContextDTO,
)


def now() -> datetime:
    return datetime.now(timezone.utc)


def trace() -> TraceContextDTO:
    return TraceContextDTO(trace_id="trace-1")


def timeout_policy() -> TimeoutPolicyDTO:
    return TimeoutPolicyDTO(
        timeout_ms=5000,
        on_timeout_action="ESCALATE",
        max_wait_ms=10000,
        requires_recovery=True,
    )


def recovery_policy() -> RecoveryPolicyDTO:
    return RecoveryPolicyDTO(
        recovery_policy_id="recovery-1",
        recovery_type="safe_state",
        manual_override_required=True,
    )


def test_emergency_action_spec_constructs_with_typed_policies() -> None:
    spec = EmergencyActionSpecDTO(
        emergency_action_type="ACTION_EMERGENCY_STOP",
        emergency_condition_type="CRITICAL_GAS_THRESHOLD",
        local_rule_id="rule-1",
        policy_id="policy-1",
        timeout_policy=timeout_policy(),
        recovery_policy=recovery_policy(),
        audit_level="full",
        approval_model="pre_registered",
        post_hoc_audit_required=True,
        version="1.0",
        owner="safety_committee",
        valid_from=now(),
    )

    assert spec.timeout_policy.timeout_ms == 5000
    assert spec.recovery_policy.manual_override_required is True


def test_emergency_action_spec_rejects_missing_required_fields() -> None:
    with pytest.raises(ValidationError):
        EmergencyActionSpecDTO(
            emergency_action_type="ACTION_EMERGENCY_STOP",
            emergency_condition_type="CRITICAL_GAS_THRESHOLD",
        )


def test_emergency_approved_action_requires_post_audit_status() -> None:
    with pytest.raises(ValidationError):
        EmergencyApprovedActionDTO(
            emergency_approved_action_id="eaa-1",
            emergency_policy_id="policy-1",
            emergency_condition_id="cond-1",
            action_type="ACTION_EMERGENCY_STOP",
            target_ref=EntityRefDTO(entity_id="zone-1", entity_type="zone"),
            local_rule_result="triggered",
            idempotency_key="idem-1",
            timeout_policy=timeout_policy(),
            expected_feedback={"status": "ack"},
            post_hoc_audit_required=True,
            post_audit_status="not_a_real_status",
            trace_context=trace(),
            created_at_utc=now(),
        )


def test_emergency_approved_action_constructs_with_valid_status() -> None:
    dto = EmergencyApprovedActionDTO(
        emergency_approved_action_id="eaa-1",
        emergency_policy_id="policy-1",
        emergency_condition_id="cond-1",
        action_type="ACTION_EMERGENCY_STOP",
        target_ref=EntityRefDTO(entity_id="zone-1", entity_type="zone"),
        local_rule_result="triggered",
        idempotency_key="idem-1",
        timeout_policy=timeout_policy(),
        expected_feedback={"status": "ack"},
        post_hoc_audit_required=True,
        post_audit_status="PENDING",
        trace_context=trace(),
        created_at_utc=now(),
    )

    assert dto.is_emergency_bypass is True
    assert dto.post_audit_status == "PENDING"


def test_post_hoc_audit_rejects_invalid_review_status() -> None:
    with pytest.raises(ValidationError):
        PostHocAuditDTO(
            post_hoc_audit_id="pha-1",
            emergency_approved_action_ref="eaa-1",
            review_status="not_a_real_status",
            trace_context=trace(),
        )


def test_post_hoc_audit_constructs_with_valid_review_status() -> None:
    dto = PostHocAuditDTO(
        post_hoc_audit_id="pha-1",
        emergency_approved_action_ref="eaa-1",
        review_status="REVIEWED",
        reviewed_at_utc=now() + timedelta(minutes=5),
        trace_context=trace(),
    )

    assert dto.review_status == "REVIEWED"


def test_emergency_runtime_validation_input_requires_trace_id() -> None:
    with pytest.raises(ValidationError):
        EmergencyRuntimeValidationInputDTO(
            id="ervi-1",
            emergency_approved_action_id="eaa-1",
            action_type="ACTION_EMERGENCY_STOP",
            created_at_utc=now(),
        )

    dto = EmergencyRuntimeValidationInputDTO(
        id="ervi-1",
        emergency_approved_action_id="eaa-1",
        action_type="ACTION_EMERGENCY_STOP",
        trace_id="trace-1",
        created_at_utc=now(),
    )
    assert dto.emergency_approved_action_id == "eaa-1"


def test_emergency_runtime_validation_result_rejects_invalid_status() -> None:
    with pytest.raises(ValidationError):
        EmergencyRuntimeValidationResultDTO(
            id="ervr-1",
            emergency_approved_action_id="eaa-1",
            action_type="ACTION_EMERGENCY_STOP",
            result="NOT_A_REAL_STATUS",
            checked_at=now(),
            trace_id="trace-1",
        )

    dto = EmergencyRuntimeValidationResultDTO(
        id="ervr-1",
        emergency_approved_action_id="eaa-1",
        action_type="ACTION_EMERGENCY_STOP",
        result="PASS",
        checked_at=now(),
        trace_id="trace-1",
    )
    assert dto.result == "PASS"


def emergency_safety_gate_pass_kwargs(**overrides: object) -> dict:
    base = dict(
        emergency_safety_gate_pass_id="esgp-1",
        emergency_approved_action_id="eaa-1",
        action_type="ACTION_EMERGENCY_STOP",
        issued_at=now(),
        expires_at=now() + timedelta(seconds=5),
        lease_duration_ms=500,
        lease_started_monotonic_ms=1000,
        lease_expires_monotonic_ms=1500,
        target_external_system="mock_emergency_system",
        execution_request_scope="fixture_scope",
        idempotency_key="idem-1",
        safety_snapshot_ref="snap-1",
        emergency_runtime_validation_result_ref="ervr-1",
        trace_id="trace-1",
        terminal_status="ISSUED",
    )
    base.update(overrides)
    return base


def test_emergency_safety_gate_pass_rejects_invalid_terminal_status() -> None:
    with pytest.raises(ValidationError):
        EmergencySafetyGatePassDTO(
            **emergency_safety_gate_pass_kwargs(terminal_status="NOT_A_REAL_STATUS")
        )

    dto = EmergencySafetyGatePassDTO(**emergency_safety_gate_pass_kwargs())
    assert dto.terminal_status == "ISSUED"


def test_emergency_safety_gate_block_carries_failure_reasons() -> None:
    dto = EmergencySafetyGateBlockDTO(
        emergency_safety_gate_block_id="esgb-1",
        emergency_approved_action_id="eaa-1",
        action_type="ACTION_EMERGENCY_STOP",
        blocked_at=now(),
        block_reasons=["STALE_STATE"],
        safety_snapshot_ref="snap-1",
        severity="CRITICAL",
        tier="TIER_1_SAFETY_CRITICAL",
        manual_review_required=True,
        trace_id="trace-1",
    )
    assert dto.block_reasons == ["STALE_STATE"]


def test_emergency_execution_request_requires_emergency_safety_gate_pass_lease() -> None:
    with pytest.raises(ValidationError, match="EmergencySafetyGatePass"):
        EmergencyExecutionRequestDTO(
            execution_request_id="eer-1",
            emergency_approved_action_ref="eaa-1",
            action_type="ACTION_EMERGENCY_STOP",
            target_ref=EntityRefDTO(entity_id="zone-1", entity_type="zone"),
            external_system_type="mock",
            external_system_id="mock-1",
            execution_constraints={},
            expected_feedback={"status": "ack"},
            timeout_policy={"timeout_ms": 1000},
            retry_policy={"max_retries": 0},
            recovery_policy={"mode": "manual"},
            idempotency_key="idem-1",
            execution_lease={},
            trace_context=trace(),
            created_at_utc=now(),
        )

    dto = EmergencyExecutionRequestDTO(
        execution_request_id="eer-1",
        emergency_approved_action_ref="eaa-1",
        action_type="ACTION_EMERGENCY_STOP",
        target_ref=EntityRefDTO(entity_id="zone-1", entity_type="zone"),
        external_system_type="mock",
        external_system_id="mock-1",
        execution_constraints={},
        expected_feedback={"status": "ack"},
        timeout_policy={"timeout_ms": 1000},
        retry_policy={"max_retries": 0},
        recovery_policy={"mode": "manual"},
        idempotency_key="idem-1",
        execution_lease={"emergency_safety_gate_pass_id": "esgp-1"},
        trace_context=trace(),
        created_at_utc=now(),
    )
    assert dto.execution_lease["emergency_safety_gate_pass_id"] == "esgp-1"
