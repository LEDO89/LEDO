from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from ledo_ontology_core.framework.schemas import (
    ActionTypeSpecDTO,
    AdapterSpecDTO,
    AuditRecordDTO,
    CapabilitySpecDTO,
    ConfidenceDTO,
    EventTypeSpecDTO,
    ExecutionStateDTO,
    ExternalControlRequestDTO,
    FeedbackEventDTO,
    LifecycleMetricDTO,
    MappingReviewDTO,
    PolicyDecisionDTO,
    StateTypeSpecDTO,
    TraceContextDTO,
    WorldStateReconciliationDTO,
)


def now() -> datetime:
    return datetime.now(timezone.utc)


def trace() -> TraceContextDTO:
    return TraceContextDTO(trace_id="trace-1")


def test_action_type_spec_constructs() -> None:
    dto = ActionTypeSpecDTO(
        action_type="ACTION_NOTIFY",
        description="fixture",
        default_risk_level="INFO",
        requires_approval=False,
    )
    assert dto.action_type == "ACTION_NOTIFY"


def test_event_type_spec_constructs() -> None:
    dto = EventTypeSpecDTO(
        event_type="FixtureEvent",
        domain_module="fixture",
        default_lifecycle_path="STANDARD",
        can_generate_evidence=True,
        can_generate_candidate=True,
        monitoring_only_allowed=False,
        emergency_trigger_allowed=False,
        supports_batching=False,
        supports_windowing=False,
    )
    assert dto.default_lifecycle_path == "STANDARD"


def test_state_type_spec_constructs() -> None:
    dto = StateTypeSpecDTO(
        state_type="fixture_state",
        entity_type="fixture",
        value_type="string",
        freshness_requirement_ms=1000,
        is_safety_critical=False,
        requires_idempotent_update=True,
    )
    assert dto.freshness_requirement_ms == 1000


def test_capability_and_adapter_spec_construct() -> None:
    capability = CapabilitySpecDTO(
        capability_id="cap-1",
        capability_type="fixture",
        owner_entity_type="robot",
        constraints={},
        risk_level="INFO",
    )
    adapter = AdapterSpecDTO(
        adapter_id="adapter-1",
        adapter_type="mock",
        external_system_type="fleet_manager",
        protocol="mock",
        timeout_policy={"timeout_ms": 1000},
        retry_policy={"max_retries": 0},
        health_status="healthy",
    )
    assert capability.risk_level == "INFO"
    assert adapter.health_status == "healthy"


def test_mapping_review_rejects_invalid_review_status() -> None:
    with pytest.raises(ValidationError):
        MappingReviewDTO(
            mapping_review_id="mr-1",
            mapping_proposal_ref="proposal-1",
            reviewer_ref="reviewer-1",
            review_status="not_a_real_status",
            created_at_utc=now(),
        )


def test_lifecycle_metric_requires_valid_path_type() -> None:
    with pytest.raises(ValidationError):
        LifecycleMetricDTO(
            metric_id="metric-1",
            metric_name="latency_ms",
            metric_value=12.0,
            stage_name="safety_gate",
            path_type="not_a_real_path",
            timestamp_utc=now(),
            trace_id="trace-1",
        )

    dto = LifecycleMetricDTO(
        metric_id="metric-1",
        metric_name="latency_ms",
        metric_value=12.0,
        stage_name="safety_gate",
        path_type="STANDARD",
        timestamp_utc=now(),
        trace_id="trace-1",
    )
    assert dto.path_type == "STANDARD"


def test_policy_decision_dto_uses_datetime_not_str_for_evaluated_at() -> None:
    dto = PolicyDecisionDTO(
        policy_decision_id="pd-1",
        input_context={},
        decision_result="ALLOW",
        reason="fixture",
        evaluated_at_utc=now(),
    )
    assert isinstance(dto.evaluated_at_utc, datetime)

    with pytest.raises(ValidationError):
        PolicyDecisionDTO(
            policy_decision_id="pd-1",
            input_context={},
            decision_result="NOT_A_REAL_RESULT",
            reason="fixture",
            evaluated_at_utc=now(),
        )


def test_policy_decision_dto_carries_required_approval_level_and_routing_flags() -> None:
    dto = PolicyDecisionDTO(
        policy_decision_id="pd-1",
        input_context={},
        decision_result="REQUIRE_APPROVAL",
        reason="fixture",
        evaluated_at_utc=now(),
        policy_engine="opa",
        policy_engine_version="0.60.0",
        required_approval_level="SAFETY_MANAGER_APPROVAL",
        matched_policy_refs=["policy:stop_work_policy"],
        requires_safety_gate=True,
        requires_fail_safe=False,
        decision_trace_id="decision-trace-1",
    )

    assert dto.required_approval_level == "SAFETY_MANAGER_APPROVAL"
    assert dto.requires_safety_gate is True


def test_policy_decision_dto_rejects_invalid_required_approval_level() -> None:
    with pytest.raises(ValidationError):
        PolicyDecisionDTO(
            policy_decision_id="pd-1",
            input_context={},
            decision_result="ALLOW",
            reason="fixture",
            evaluated_at_utc=now(),
            required_approval_level="NOT_A_REAL_LEVEL",
        )


def test_world_state_reconciliation_constructs() -> None:
    dto = WorldStateReconciliationDTO(
        reconciliation_id="recon-1",
        feedback_event_ref="feedback-1",
        conflict_detected=False,
        reconciliation_result="reconciled",
        created_at_utc=now(),
        trace_context=trace(),
    )
    assert dto.conflict_detected is False


def test_execution_state_rejects_value_outside_canonical_dispatch_status() -> None:
    with pytest.raises(ValidationError):
        ExecutionStateDTO(
            execution_state_id="es-1",
            execution_request_ref="exec-1",
            state="BLOCKED",
            updated_at_utc=now(),
            recovery_required=False,
            trace_context=trace(),
        )


def test_execution_state_accepts_canonical_dispatch_status() -> None:
    dto = ExecutionStateDTO(
        execution_state_id="es-1",
        execution_request_ref="exec-1",
        state="DISPATCHED",
        updated_at_utc=now(),
        recovery_required=False,
        trace_context=trace(),
    )
    assert dto.state == "DISPATCHED"


def test_audit_record_carries_integrity_chain_and_trust_fields() -> None:
    dto = AuditRecordDTO(
        audit_record_id="audit-1",
        trace_id="trace-1",
        lifecycle_path="STANDARD",
        final_status="COMPLETED",
        created_at_utc=now(),
        audit_event_type="EXECUTION_REQUEST_CREATED",
        severity="WARNING",
        audit_reason="High-risk action executed",
        occurred_at=now(),
        time_trust_level="HIGH_TIME_TRUST",
        clock_sync_status="SYNCED",
        source_system_ref="edge-gateway-1",
        correlation_id="corr-1",
        decision_trace_id="decision-trace-1",
        primary_causality_id="cause-1",
        causality_ids=["cause-1", "cause-2"],
        integrity_policy_ref="policy:chained_hash",
        content_hash="sha256:abc",
        previous_record_hash="sha256:prev",
        integrity_status="VERIFIED",
    )

    assert dto.content_hash == "sha256:abc"
    assert dto.causality_ids == ["cause-1", "cause-2"]


def test_audit_record_rejects_invalid_time_trust_level() -> None:
    with pytest.raises(ValidationError):
        AuditRecordDTO(
            audit_record_id="audit-1",
            trace_id="trace-1",
            lifecycle_path="STANDARD",
            final_status="COMPLETED",
            created_at_utc=now(),
            time_trust_level="NOT_A_REAL_TRUST_LEVEL",
        )


def test_audit_record_rejects_invalid_clock_sync_status() -> None:
    with pytest.raises(ValidationError):
        AuditRecordDTO(
            audit_record_id="audit-1",
            trace_id="trace-1",
            lifecycle_path="STANDARD",
            final_status="COMPLETED",
            created_at_utc=now(),
            clock_sync_status="NOT_A_REAL_SYNC_STATUS",
        )


def test_feedback_event_carries_result_detail_and_timing_fields() -> None:
    t = now()
    dto = FeedbackEventDTO(
        feedback_event_id="fe-1",
        execution_request_ref="exec-1",
        external_request_ref="ext-1",
        source_system="mock_fleet_manager",
        feedback_type="mission_status",
        status="COMPLETED",
        payload={"result": "ok"},
        timestamp_utc=t,
        confidence=ConfidenceDTO(
            confidence_score=0.9, confidence_level="high", validation_status="PASSED"
        ),
        trace_context=trace(),
        recovery_required=False,
        feedback_status="RECEIVED",
        result_status="SUCCESS",
        result_message="Mission completed successfully",
        actual_started_at=t,
        actual_completed_at=t + timedelta(seconds=5),
        observed_state_refs=["state-1"],
        requires_reconciliation=True,
        requires_audit=True,
        decision_trace_id="decision-trace-1",
    )

    assert dto.result_status == "SUCCESS"
    assert dto.requires_reconciliation is True
    assert dto.observed_state_refs == ["state-1"]


def test_external_control_request_carries_dispatch_and_timing_fields() -> None:
    t = now()
    dto = ExternalControlRequestDTO(
        external_request_id="ecr-1",
        execution_request_ref="exec-1",
        adapter_id="mock_fleet_manager_adapter",
        external_system_type="mock_fleet_manager",
        protocol="https",
        endpoint="https://fleet.example/api/dispatch",
        payload={"mission_id": "m-1"},
        idempotency_key="idem-1",
        timeout_policy={"timeout_ms": 5000},
        expected_feedback={"status": "ack"},
        trace_context=trace(),
        sent_at_utc=t,
        adapter_type="FleetManagerAdapter",
        adapter_mode="PRODUCTION",
        dispatch_attempt=1,
        dispatch_status="DISPATCHED",
        ack_deadline=t + timedelta(seconds=2),
        acceptance_deadline=t + timedelta(seconds=10),
        feedback_deadline=t + timedelta(seconds=30),
        adapter_local_received_at=t,
        clock_sync_status="SYNCED",
        clock_drift_estimate_ms=12.5,
        decision_trace_id="decision-trace-1",
    )

    assert dto.dispatch_status == "DISPATCHED"
    assert dto.clock_sync_status == "SYNCED"


def test_external_control_request_rejects_invalid_dispatch_status() -> None:
    with pytest.raises(ValidationError):
        ExternalControlRequestDTO(
            external_request_id="ecr-1",
            execution_request_ref="exec-1",
            adapter_id="mock_fleet_manager_adapter",
            external_system_type="mock_fleet_manager",
            protocol="https",
            endpoint="https://fleet.example/api/dispatch",
            payload={"mission_id": "m-1"},
            idempotency_key="idem-1",
            timeout_policy={"timeout_ms": 5000},
            expected_feedback={"status": "ack"},
            trace_context=trace(),
            sent_at_utc=now(),
            dispatch_status="NOT_A_REAL_STATUS",
        )
