from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from ledo_ontology_core.framework.schemas import (
    AuditRecordDTO,
    ConfidenceDTO,
    DecisionCaseDTO,
    DispatchStatus,
    OntologyBindingDTO,
    PathClassificationDTO,
    TraceContextDTO,
)
from ledo_ontology_core.framework.schemas.refs import EntityRefDTO


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
            risk_level="high",
            urgency="high",
            routing_result="fixture",
            required_approval=True,
            trace_context=TraceContextDTO(trace_id="trace-1"),
        )


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
