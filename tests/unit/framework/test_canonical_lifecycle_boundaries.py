from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from ledo_ontology_core.framework.schemas.action import ActionCandidateDTO
from ledo_ontology_core.framework.schemas.audit import AuditRecordDTO
from ledo_ontology_core.framework.schemas.context import TraceContextDTO
from ledo_ontology_core.framework.schemas.execution import (
    ApprovedActionDTO,
    ExecutionRequestDTO,
)
from ledo_ontology_core.framework.schemas.enums import PathType
from ledo_ontology_core.framework.schemas.lifecycle_state import LifecycleStage
from ledo_ontology_core.framework.schemas.refs import EntityRefDTO
from ledo_ontology_core.framework.schemas.runtime_validation import (
    RuntimeValidationResultDTO,
)
from ledo_ontology_core.framework.schemas.safety_gate import SafetyGatePassDTO
from ledo_ontology_core.framework.validation.lifecycle import (
    LifecycleBoundaryError,
    validate_action_candidate_boundary,
    validate_ai_boundary,
    validate_approved_action_boundary,
    validate_audit_trace_path,
    validate_evidence_boundary,
    validate_execution_request_boundary,
    validate_lifecycle_transition,
)


def now() -> datetime:
    return datetime.now(timezone.utc)


def trace() -> TraceContextDTO:
    return TraceContextDTO(trace_id="trace-1", correlation_id="corr-1")


def entity() -> EntityRefDTO:
    return EntityRefDTO(entity_id="target-1", entity_type="fixture")


def candidate(**overrides: object) -> ActionCandidateDTO:
    values = dict(
        candidate_id="candidate-1",
        action_type="fixture_action",
        target_ref=entity(),
        proposed_by="agent-1",
        reason="fixture proposal",
        risk_level="HIGH_RISK",
        evidence_refs=["evidence-1"],
        confidence={
            "confidence_score": 0.9,
            "confidence_level": "high",
            "validation_status": "PASSED",
        },
        constraints={},
        required_capabilities=[],
        requires_approval=True,
        created_at_utc=now(),
        trace_context=trace(),
    )
    values.update(overrides)
    return ActionCandidateDTO(**values)


def approved_action(**overrides: object) -> ApprovedActionDTO:
    values = dict(
        approved_action_id="approved-1",
        candidate_ref="candidate-1",
        decision_case_ref="decision-1",
        action_type="fixture_action",
        target_ref=entity(),
        constraints={},
        approval_context={"approval_decision_ref": "approval-decision-1"},
        policy_result={"decision": "ALLOW"},
        evidence_refs=["evidence-1"],
        risk_level="HIGH_RISK",
        valid_until=now() + timedelta(minutes=5),
        idempotency_key="idem-1",
        trace_context=trace(),
        created_at_utc=now(),
    )
    values.update(overrides)
    return ApprovedActionDTO(**values)


def runtime_validation_result(**overrides: object) -> RuntimeValidationResultDTO:
    values = dict(
        id="runtime-result-1",
        approved_action_id="approved-1",
        action_type="fixture_action",
        result="PASS",
        checked_at=now(),
        validator_result_refs=["validator-result-1"],
        trace_id="trace-1",
    )
    values.update(overrides)
    return RuntimeValidationResultDTO(**values)


def safety_gate_pass(**overrides: object) -> SafetyGatePassDTO:
    values = dict(
        safety_gate_pass_id="sgp-1",
        approved_action_id="approved-1",
        action_type="fixture_action",
        issued_at=now(),
        expires_at=now() + timedelta(seconds=30),
        lease_duration_ms=30_000,
        lease_started_monotonic_ms=100,
        lease_expires_monotonic_ms=30_100,
        target_external_system="mock-system",
        execution_request_scope="fixture_scope",
        idempotency_key="idem-1",
        safety_snapshot_ref="snapshot-1",
        runtime_validation_result_ref="runtime-result-1",
        trace_id="trace-1",
        terminal_status="ISSUED",
    )
    values.update(overrides)
    return SafetyGatePassDTO(**values)


def execution_request(**overrides: object) -> ExecutionRequestDTO:
    values = dict(
        execution_request_id="exec-1",
        approved_action_ref="approved-1",
        action_type="fixture_action",
        target_ref=entity(),
        external_system_type="mock",
        external_system_id="mock-system",
        execution_constraints={"mode": "dry_run_fixture"},
        expected_feedback={"required": True},
        timeout_policy={"timeout_ms": 1000},
        retry_policy={"max_retries": 0},
        recovery_policy={"manual_review_required": True},
        idempotency_key="idem-1",
        execution_lease={"safety_gate_pass_id": "sgp-1"},
        trace_context=trace(),
        created_at_utc=now(),
    )
    values.update(overrides)
    return ExecutionRequestDTO(**values)


def audit_record(**overrides: object) -> AuditRecordDTO:
    values = dict(
        audit_record_id="audit-1",
        trace_id="trace-1",
        lifecycle_path="STANDARD",
        candidate_ref="candidate-1",
        approved_action_ref="approved-1",
        execution_request_ref="exec-1",
        evidence_refs=["evidence-1"],
        final_status="closed",
        created_at_utc=now(),
    )
    values.update(overrides)
    return AuditRecordDTO(**values)


def test_standard_path_dto_chain_can_carry_trace_ids() -> None:
    assert validate_audit_trace_path(
        audit_record(),
        [
            candidate(),
            approved_action(),
            runtime_validation_result(),
            safety_gate_pass(),
            execution_request(),
        ],
    )


def test_action_candidate_cannot_be_treated_as_approval() -> None:
    assert validate_action_candidate_boundary(candidate())

    with pytest.raises(LifecycleBoundaryError, match="approval"):
        validate_action_candidate_boundary(
            candidate(constraints={"approval_decision_id": "approval-decision-1"})
        )


def test_approved_action_cannot_be_treated_as_physical_command() -> None:
    assert validate_approved_action_boundary(approved_action())

    with pytest.raises(LifecycleBoundaryError, match="physical command"):
        validate_approved_action_boundary(
            approved_action(constraints={"plc_command": {"write": "forbidden"}})
        )


def test_execution_request_cannot_be_treated_as_physical_command() -> None:
    with pytest.raises(LifecycleBoundaryError, match="physical command"):
        validate_execution_request_boundary(
            execution_request(
                execution_constraints={"robot_motion_command": {"joint": "forbidden"}}
            ),
            runtime_validation_result=runtime_validation_result(),
            safety_gate_pass=safety_gate_pass(),
        )


def test_ai_origin_field_cannot_satisfy_evidence_requirement_by_itself() -> None:
    assert validate_ai_boundary("EvidenceSummary", produced_by_ai=True)

    with pytest.raises(LifecycleBoundaryError, match="AI EvidenceSummary"):
        validate_evidence_boundary(
            ["ai-summary-1"],
            ai_summary_refs=["ai-summary-1"],
        )

    with pytest.raises(LifecycleBoundaryError, match="ApprovedAction"):
        validate_ai_boundary("ApprovedAction", produced_by_ai=True)


def test_no_execution_request_without_runtime_validation_and_safety_gate_pass() -> None:
    request = execution_request()

    with pytest.raises(LifecycleBoundaryError, match="RuntimeValidationResult"):
        validate_execution_request_boundary(
            request,
            runtime_validation_result=None,
            safety_gate_pass=safety_gate_pass(),
        )

    with pytest.raises(LifecycleBoundaryError, match="SafetyGatePass"):
        validate_execution_request_boundary(
            request,
            runtime_validation_result=runtime_validation_result(),
            safety_gate_pass=None,
        )

    assert validate_execution_request_boundary(
        request,
        runtime_validation_result=runtime_validation_result(),
        safety_gate_pass=safety_gate_pass(),
    )


def test_execution_request_dto_still_requires_safety_gate_lease_reference() -> None:
    with pytest.raises(ValidationError, match="SafetyGatePass"):
        execution_request(execution_lease={})


def test_compressed_approved_action_to_execution_request_path_fails() -> None:
    with pytest.raises(LifecycleBoundaryError, match="intermediate stages"):
        validate_lifecycle_transition(
            PathType.STANDARD,
            [
                LifecycleStage.APPROVED_ACTION_CREATED,
                LifecycleStage.EXECUTION_REQUEST_CREATED,
            ],
        )

    assert validate_lifecycle_transition(
        PathType.STANDARD,
        [
            LifecycleStage.APPROVED_ACTION_CREATED,
            LifecycleStage.RUNTIME_VALIDATION_RESULT_CREATED,
            LifecycleStage.SAFETY_GATE_PASSED,
            LifecycleStage.EXECUTION_REQUEST_CREATED,
        ],
    )
