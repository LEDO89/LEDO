from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from ledo_ontology_core.framework.schemas import (
    EmergencyActionSpecDTO,
    EmergencyApprovedActionDTO,
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
