from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from ledo_ontology_core.framework.schemas import (
    ApprovalAuthority,
    AuditRecordDTO,
    ConfidenceDTO,
    DecisionCaseDTO,
    DispatchStatus,
    OntologyBindingDTO,
    PathClassificationDTO,
    PolicyDecisionResult,
    RiskLevel,
    TraceContextDTO,
)
from ledo_ontology_core.framework.schemas.execution import ApprovedActionDTO
from ledo_ontology_core.framework.schemas.refs import EntityRefDTO, PolicyRefDTO


def now() -> datetime:
    return datetime.now(timezone.utc)


def test_dispatch_status_has_exactly_the_20_canonical_members() -> None:
    assert len(DispatchStatus) == 20
    # Illustrative states from 1_common_schema_dto.md Section 18.3 that are NOT part of
    # the canonical 09_execution_adapter_model.md Section 20 enum must not leak in.
    non_canonical = {"STARTED", "BLOCKED", "RECOVERY_STARTED", "RECOVERY_COMPLETED"}
    assert non_canonical.isdisjoint({member.value for member in DispatchStatus})


def test_confidence_dto_rejects_invalid_validation_status() -> None:
    with pytest.raises(ValidationError):
        ConfidenceDTO(
            confidence_score=0.5,
            confidence_level="medium",
            validation_status="NOT_A_REAL_STATUS",
        )


def test_path_classification_rejects_invalid_path_type() -> None:
    with pytest.raises(ValidationError):
        PathClassificationDTO(
            path_type="NOT_A_REAL_PATH",
            classification_reason="fixture",
            emergency_detected=False,
            monitoring_only_allowed=False,
            standard_path_required=True,
            classified_at_utc=now(),
        )


def test_ontology_binding_rejects_invalid_binding_status() -> None:
    with pytest.raises(ValidationError):
        OntologyBindingDTO(
            binding_id="binding-1",
            entity_ref=EntityRefDTO(entity_id="entity-1", entity_type="fixture"),
            domain_module="fixture",
            binding_status="NOT_A_REAL_STATUS",
        )


def test_decision_case_rejects_invalid_decision_tier() -> None:
    with pytest.raises(ValidationError):
        DecisionCaseDTO(
            decision_case_id="dc-1",
            candidate_ref="candidate-1",
            decision_tier="NOT_A_REAL_TIER",
            risk_level="HIGH_RISK",
            urgency="high",
            routing_result="fixture",
            required_approval=True,
            trace_context=TraceContextDTO(trace_id="trace-1"),
        )


def test_decision_case_rejects_invalid_risk_level() -> None:
    with pytest.raises(ValidationError):
        DecisionCaseDTO(
            decision_case_id="dc-1",
            candidate_ref="candidate-1",
            decision_tier="ROUTINE",
            risk_level="not_a_real_level",
            urgency="high",
            routing_result="fixture",
            required_approval=True,
            trace_context=TraceContextDTO(trace_id="trace-1"),
        )


def test_risk_level_has_exactly_the_six_canonical_members() -> None:
    # Canonical source: 07_decision_approval_matrix.md Section 8, cross-confirmed by
    # 08_policy_governance_model.md. Registry docs (action_registry.md,
    # decision_registry.md) use a different lowercase set that must not leak in.
    assert {member.value for member in RiskLevel} == {
        "INFO",
        "NOTICE",
        "WARNING",
        "HIGH_RISK",
        "CRITICAL_EMERGENCY",
        "EXCEPTIONAL",
    }


def test_approved_action_rejects_invalid_risk_level() -> None:
    with pytest.raises(ValidationError):
        ApprovedActionDTO(
            approved_action_id="approved-1",
            candidate_ref="candidate-1",
            decision_case_ref="decision-1",
            action_type="fixture_action",
            target_ref=EntityRefDTO(entity_id="entity-1", entity_type="fixture"),
            constraints={},
            approval_context={"approval_decision_ref": "approval-1"},
            policy_result={"decision": "allow_for_test"},
            evidence_refs=["ev-1"],
            risk_level="not_a_real_level",
            valid_until=now(),
            idempotency_key="idem-1",
            trace_context=TraceContextDTO(trace_id="trace-1"),
            created_at_utc=now(),
        )


def test_policy_decision_result_has_exactly_the_eight_canonical_members() -> None:
    # Canonical source: 08_policy_governance_model.md Section 7. Supersedes the
    # 5-member illustrative list in 1_common_schema_dto.md Section 19.7.
    assert {member.value for member in PolicyDecisionResult} == {
        "ALLOW",
        "DENY",
        "REQUIRE_APPROVAL",
        "REQUIRE_EVIDENCE",
        "REQUIRE_REVALIDATION",
        "REQUIRE_FAIL_SAFE",
        "REQUIRE_MANUAL_OVERRIDE",
        "REQUIRE_POLICY_EXCEPTION_REVIEW",
    }


def test_policy_ref_rejects_invalid_decision_result() -> None:
    with pytest.raises(ValidationError):
        PolicyRefDTO(
            policy_id="policy-1",
            policy_type="fixture",
            policy_version="1.0.0",
            decision_result="ESCALATE",
        )


def test_approval_authority_has_exactly_the_nine_canonical_members() -> None:
    # Canonical source: 08_policy_governance_model.md Section 13, independently
    # cross-confirmed by appendix_f_decision_approval_catalog.md's "Approval Level"
    # list (itself sourced from 07_decision_approval_matrix.md). approval_registry.md
    # Section 8 defines a different, non-matching set and is not canonical.
    assert {member.value for member in ApprovalAuthority} == {
        "NO_APPROVAL",
        "OPERATOR_ACK",
        "SUPERVISOR_APPROVAL",
        "SAFETY_MANAGER_APPROVAL",
        "WAR_ROOM_APPROVAL",
        "EXPERT_REVIEW",
        "POLICY_OWNER_APPROVAL",
        "EMERGENCY_POLICY_BYPASS",
        "POST_HOC_AUDIT_ONLY",
    }


def test_audit_record_rejects_invalid_post_audit_status() -> None:
    with pytest.raises(ValidationError):
        AuditRecordDTO(
            audit_record_id="audit-1",
            trace_id="trace-1",
            lifecycle_path="STANDARD",
            final_status="closed",
            created_at_utc=now(),
            post_audit_status="NOT_A_REAL_STATUS",
        )
