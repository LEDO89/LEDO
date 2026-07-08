from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from ledo_ontology_core.framework.schemas import (
    ActionTypeSpecDTO,
    AdapterSpecDTO,
    CapabilitySpecDTO,
    EventTypeSpecDTO,
    ExecutionStateDTO,
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
        default_risk_level="low",
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
        risk_level="low",
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
    assert capability.risk_level == "low"
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
