from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from ledo_ontology_core.framework.schemas import (
    ActionCandidateDTO,
    ApprovalRequestDTO,
    ApprovedActionDTO,
    AuditRecordDTO,
    CanonicalEventEnvelopeDTO,
    CanonicalIdentityDTO,
    ConfidenceDTO,
    DecisionCaseDTO,
    EntityRefDTO,
    EvidenceDTO,
    EvidenceRefDTO,
    ExecutionRequestDTO,
    ExternalControlRequestDTO,
    FeedbackEventDTO,
    FreshnessDTO,
    OntologyBindingDTO,
    OntologyBoundEventDTO,
    OntologyRefDTO,
    PathClassificationDTO,
    SanitizedInputDTO,
    SourceMetadataDTO,
    TraceContextDTO,
    ValidationResultDTO,
    VersionContextDTO,
    WorldStateDTO,
    WorldStateUpdateDTO,
)
from ledo_ontology_core.framework.schemas.source_inputs import LLMOutputInputDTO


def now() -> datetime:
    return datetime.now(timezone.utc)


def trace() -> TraceContextDTO:
    return TraceContextDTO(trace_id="trace-1", correlation_id="corr-1")


def source(source_type: str = "sensor", source_trust_level: str = "TRUSTED_SYSTEM") -> SourceMetadataDTO:
    return SourceMetadataDTO(
        source_type=source_type,
        source_id="src-1",
        source_trust_level=source_trust_level,
        ingested_at_utc=now(),
    )


def confidence() -> ConfidenceDTO:
    return ConfidenceDTO(
        confidence_score=0.9,
        confidence_level="high",
        validation_status="PASSED",
    )


def freshness() -> FreshnessDTO:
    t = now()
    return FreshnessDTO(
        timestamp_utc=t,
        ingested_at_utc=t,
        freshness_ms=1,
        valid_until=t + timedelta(seconds=30),
        is_stale=False,
    )


def entity() -> EntityRefDTO:
    return EntityRefDTO(entity_id="entity-1", entity_type="fixture")


def event() -> CanonicalEventEnvelopeDTO:
    return CanonicalEventEnvelopeDTO(
        event_id="event-1",
        event_type="FixtureEvent",
        source_metadata=source(),
        subject_ref=entity(),
        location_ref=None,
        timestamp_utc=now(),
        payload={"ok": True},
        confidence=confidence(),
        freshness=freshness(),
        trace_context=trace(),
        version_context=VersionContextDTO(schema_version="1.0", lifecycle_version="1.0"),
        emergency_hint=False,
        criticality_hint=None,
        lifecycle_path_hint="STANDARD",
    )


def evidence_ref() -> EvidenceRefDTO:
    return EvidenceRefDTO(
        evidence_id="ev-1",
        evidence_type="fixture_evidence",
        source_id="src-1",
        timestamp_utc=now(),
        confidence_score=0.9,
    )


def test_initial_required_dtos_from_section_23_are_importable() -> None:
    required = [
        ValidationResultDTO,
        SanitizedInputDTO,
        EntityRefDTO,
        OntologyRefDTO,
        EvidenceRefDTO,
        CanonicalEventEnvelopeDTO,
        PathClassificationDTO,
        CanonicalIdentityDTO,
        OntologyBindingDTO,
        OntologyBoundEventDTO,
        EvidenceDTO,
        WorldStateDTO,
        WorldStateUpdateDTO,
        ActionCandidateDTO,
        DecisionCaseDTO,
        ApprovalRequestDTO,
        ApprovedActionDTO,
        ExecutionRequestDTO,
        ExternalControlRequestDTO,
        FeedbackEventDTO,
        AuditRecordDTO,
    ]

    assert all(dto.__name__.endswith("DTO") for dto in required)


def test_evidence_rejects_unattested_ai_derived_source_trust_level() -> None:
    with pytest.raises(ValidationError, match="AI_DERIVED"):
        EvidenceDTO(
            evidence_id="evidence-1",
            evidence_type="ai_summary",
            source_metadata=source("llm", source_trust_level="AI_DERIVED"),
            subject_ref=entity(),
            location_ref=None,
            payload={"summary": "candidate only"},
            timestamp_utc=now(),
            confidence=confidence(),
            freshness=freshness(),
            trace_context=trace(),
            provenance={"source": "model output"},
            validation_status="PASSED",
        )


def test_evidence_accepts_attested_ai_derived_source_trust_level() -> None:
    dto = EvidenceDTO(
        evidence_id="evidence-1",
        evidence_type="permit_expiry_extraction",
        source_metadata=source("llm", source_trust_level="ATTESTED_AI_DERIVED"),
        subject_ref=entity(),
        location_ref=None,
        payload={"permit_expiry": "15:00"},
        timestamp_utc=now(),
        confidence=confidence(),
        freshness=freshness(),
        trace_context=trace(),
        provenance={"source": "ocr extraction, human attested"},
        validation_status="PASSED",
    )

    assert dto.source_metadata.source_trust_level == "ATTESTED_AI_DERIVED"


def test_llm_output_is_limited_to_candidate_roles() -> None:
    dto = LLMOutputInputDTO(
        model_id="model-1",
        prompt_id="prompt-1",
        output_type="EvidenceSummary",
        structured_output={"summary": "not evidence"},
        retrieved_doc_refs=["doc-1"],
        confidence=confidence(),
        created_at_utc=now(),
    )

    assert dto.output_type == "EvidenceSummary"

    with pytest.raises(ValidationError):
        LLMOutputInputDTO(
            model_id="model-1",
            prompt_id="prompt-1",
            output_type="Evidence",
            structured_output={},
            retrieved_doc_refs=[],
            confidence=confidence(),
            created_at_utc=now(),
        )


def test_execution_request_requires_safety_gate_lease_reference() -> None:
    approved = ApprovedActionDTO(
        approved_action_id="approved-1",
        candidate_ref="candidate-1",
        decision_case_ref="decision-1",
        action_type="fixture_action",
        target_ref=entity(),
        constraints={},
        approval_context={"approval_decision_ref": "approval-1"},
        policy_result={"decision": "allow_for_test"},
        evidence_refs=["ev-1"],
        risk_level="HIGH_RISK",
        valid_until=now() + timedelta(minutes=5),
        idempotency_key="idem-1",
        trace_context=trace(),
        created_at_utc=now(),
    )

    with pytest.raises(ValidationError, match="SafetyGatePass"):
        ExecutionRequestDTO(
            execution_request_id="exec-1",
            approved_action_ref=approved.approved_action_id,
            action_type=approved.action_type,
            target_ref=approved.target_ref,
            external_system_type="mock",
            external_system_id="mock-1",
            execution_constraints={},
            expected_feedback={"status": "ack"},
            timeout_policy={"timeout_ms": 1000},
            retry_policy={"max_retries": 0},
            recovery_policy={"mode": "manual"},
            idempotency_key=approved.idempotency_key,
            execution_lease={},
            trace_context=trace(),
            created_at_utc=now(),
        )

    request = ExecutionRequestDTO(
        execution_request_id="exec-1",
        approved_action_ref=approved.approved_action_id,
        action_type=approved.action_type,
        target_ref=approved.target_ref,
        external_system_type="mock",
        external_system_id="mock-1",
        execution_constraints={},
        expected_feedback={"status": "ack"},
        timeout_policy={"timeout_ms": 1000},
        retry_policy={"max_retries": 0},
        recovery_policy={"mode": "manual"},
        idempotency_key=approved.idempotency_key,
        execution_lease={"safety_gate_pass_id": "sg-pass-1"},
        trace_context=trace(),
        created_at_utc=now(),
    )

    assert request.execution_lease["safety_gate_pass_id"] == "sg-pass-1"


def test_trace_survives_initial_lifecycle_dto_chain() -> None:
    bound = OntologyBoundEventDTO(
        event_id="event-1",
        canonical_event=event(),
        ontology_bindings=[
            OntologyBindingDTO(
                binding_id="binding-1",
                entity_ref=entity(),
                domain_module="fixture",
                binding_status="BOUND",
            )
        ],
        subject_ref=entity(),
        state_type="fixture_state",
        event_semantics={},
        evidence_candidate=None,
        trace_context=trace(),
    )
    evidence = EvidenceDTO(
        evidence_id="evidence-1",
        evidence_type="fixture",
        source_metadata=source(),
        subject_ref=entity(),
        location_ref=None,
        payload={"observed": True},
        timestamp_utc=now(),
        confidence=confidence(),
        freshness=freshness(),
        trace_context=trace(),
        provenance={"raw_ref": "raw-1"},
        validation_status="PASSED",
    )
    state = WorldStateDTO(
        state_id="state-1",
        entity_ref=entity(),
        state_type="fixture_state",
        state_value="ready",
        source_ref="src-1",
        evidence_ref=evidence.evidence_id,
        timestamp_utc=now(),
        freshness=freshness(),
        confidence=confidence(),
        valid_until=None,
        trace_context=trace(),
        version="1",
    )
    update = WorldStateUpdateDTO(
        update_id="update-1",
        entity_ref=entity(),
        previous_state=None,
        new_state=state,
        change_reason="fixture",
        evidence_refs=[evidence.evidence_id],
        updated_by="test",
        updated_at_utc=now(),
        trace_context=trace(),
        idempotency_key="idem-state-1",
        state_version="1",
        expected_previous_version=None,
        deduplication_window_ms=1000,
    )

    assert bound.trace_context.trace_id == "trace-1"
    assert update.trace_context.trace_id == "trace-1"
