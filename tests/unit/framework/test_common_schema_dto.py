from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from ledo_ontology_core.framework.schemas import (
    BaseDTO,
    CanonicalEventEnvelopeDTO,
    ConfidenceDTO,
    EntityRefDTO,
    FreshnessDTO,
    LocationRefDTO,
    RawInputDTO,
    SourceMetadataDTO,
    TraceContextDTO,
    ValidationResultDTO,
    VersionContextDTO,
)


def now() -> datetime:
    return datetime.now(timezone.utc)


def source(source_type: str = "sensor") -> SourceMetadataDTO:
    return SourceMetadataDTO(
        source_type=source_type,
        source_id="src-1",
        source_name="fixture source",
        source_protocol="fixture",
        source_system="test",
        source_trust_level="TRUSTED_SYSTEM",
        ingested_at_utc=now(),
        raw_ref="raw-1",
    )


def trace() -> TraceContextDTO:
    return TraceContextDTO(
        trace_id="trace-1",
        correlation_id="corr-1",
        causation_id="cause-1",
        span_id="span-1",
        parent_span_id=None,
        request_id="req-1",
    )


def confidence() -> ConfidenceDTO:
    return ConfidenceDTO(
        confidence_score=0.8,
        confidence_level="medium",
        confidence_reason="test fixture",
        source_quality="fixture",
        validation_status="PASSED",
    )


def freshness() -> FreshnessDTO:
    timestamp_utc=now()
    return FreshnessDTO(
        timestamp_utc=timestamp_utc,
        ingested_at_utc=timestamp_utc,
        freshness_ms=10,
        valid_until=None,
        is_stale=False,
    )


def test_base_dto_accepts_required_contract_fields() -> None:
    dto = BaseDTO(
        id="base-1",
        schema_version="1.0",
        lifecycle_version="1.0",
    )

    assert dto.id == "base-1"
    assert dto.metadata == {}


def test_base_dto_rejects_missing_required_fields() -> None:
    with pytest.raises(ValidationError):
        BaseDTO(id="base-1", schema_version="1.0")


def test_trace_context_preserves_trace_mapping_fields() -> None:
    dto = trace()

    assert dto.trace_id == "trace-1"
    assert dto.correlation_id == "corr-1"
    assert dto.causation_id == "cause-1"


def test_confidence_score_is_bounded() -> None:
    with pytest.raises(ValidationError):
        ConfidenceDTO(
            confidence_score=1.5,
            confidence_level="invalid",
            validation_status="FAILED",
        )


def test_validation_result_rejects_unknown_extra_fields() -> None:
    with pytest.raises(ValidationError):
        ValidationResultDTO(
            validation_id="val-1",
            input_ref="raw-1",
            validation_status="PASSED",
            validation_errors=[],
            sanitized=True,
            sanitization_notes=[],
            rate_limited=False,
            replay_detected=False,
            source_authenticated=True,
            source_authorized=True,
            validated_at_utc=now(),
            unexpected="not allowed",
        )


def test_raw_input_and_canonical_event_construct_with_trace_and_version() -> None:
    entity = EntityRefDTO(
        entity_id="entity-1",
        entity_type="test_entity",
        canonical_id="canonical-1",
    )
    location = LocationRefDTO(location_id="loc-1", location_type="test_location")
    raw = RawInputDTO(
        raw_input_id="raw-1",
        source_metadata=source(),
        raw_payload={"value": 1},
        received_at_utc=now(),
        raw_format="json",
        encoding="utf-8",
        checksum="checksum",
        trace_context=trace(),
    )
    event = CanonicalEventEnvelopeDTO(
        event_id="event-1",
        event_type="FixtureEvent",
        source_metadata=raw.source_metadata,
        subject_ref=entity,
        location_ref=location,
        timestamp_utc=now(),
        payload={"value": 1},
        confidence=confidence(),
        freshness=freshness(),
        trace_context=trace(),
        version_context=VersionContextDTO(schema_version="1.0", lifecycle_version="1.0"),
        emergency_hint=False,
        criticality_hint=None,
        lifecycle_path_hint="STANDARD",
    )

    assert event.trace_context.trace_id == "trace-1"
    assert event.version_context.schema_version == "1.0"
