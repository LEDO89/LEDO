from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from ledo_ontology_core.framework.schemas import (
    EntityRefDTO,
    EscalationTriggerDTO,
    FreshnessDTO,
    MonitoringOnlyEventDTO,
    MonitoringPayloadDTO,
    SourceMetadataDTO,
    TimeSeriesBundleInputDTO,
    TimeSeriesSampleDTO,
    TraceContextDTO,
    VersionContextDTO,
    WindowedInputDTO,
)


def now() -> datetime:
    return datetime.now(timezone.utc)


def trace() -> TraceContextDTO:
    return TraceContextDTO(trace_id="trace-1")


def source() -> SourceMetadataDTO:
    return SourceMetadataDTO(
        source_type="sensor",
        source_id="src-1",
        source_trust_level="test_fixture",
        ingested_at_utc=now(),
    )


def entity() -> EntityRefDTO:
    return EntityRefDTO(entity_id="entity-1", entity_type="fixture")


def freshness() -> FreshnessDTO:
    t = now()
    return FreshnessDTO(timestamp_utc=t, ingested_at_utc=t, freshness_ms=1, is_stale=False)


def sample() -> TimeSeriesSampleDTO:
    return TimeSeriesSampleDTO(
        timestamp_utc=now(),
        value=1.0,
        quality="good",
        sequence_number=1,
        sample_status="ok",
    )


def test_time_series_bundle_carries_samples_without_full_trace_per_sample() -> None:
    bundle = TimeSeriesBundleInputDTO(
        bundle_id="bundle-1",
        source_metadata=source(),
        subject_ref=entity(),
        signal_name="temperature",
        samples=[sample(), sample()],
        window_start_utc=now(),
        window_end_utc=now() + timedelta(seconds=10),
        sample_count=2,
        trace_context=trace(),
        version_context=VersionContextDTO(schema_version="1.0", lifecycle_version="1.0"),
    )

    assert len(bundle.samples) == 2
    assert bundle.trace_context.trace_id == "trace-1"


def test_windowed_input_rejects_invalid_aggregation_type() -> None:
    with pytest.raises(ValidationError):
        WindowedInputDTO(
            window_id="window-1",
            source_metadata=source(),
            window_start_utc=now(),
            window_end_utc=now() + timedelta(seconds=10),
            aggregation_type="NOT_A_REAL_AGGREGATION",
            trace_context=trace(),
        )


def test_windowed_input_accepts_valid_aggregation_type() -> None:
    dto = WindowedInputDTO(
        window_id="window-1",
        source_metadata=source(),
        window_start_utc=now(),
        window_end_utc=now() + timedelta(seconds=10),
        aggregation_type="THRESHOLD_CROSSING",
        trace_context=trace(),
    )

    assert dto.aggregation_type == "THRESHOLD_CROSSING"


def test_monitoring_only_event_defaults_to_monitoring_only_path() -> None:
    dto = MonitoringOnlyEventDTO(
        monitoring_event_id="mon-1",
        source_metadata=source(),
        subject_ref=entity(),
        monitoring_payload=MonitoringPayloadDTO(
            metric_name="temperature",
            metric_value=21.5,
            timestamp_utc=now(),
            quality="good",
            is_threshold_crossed=False,
            summary_status="normal",
        ),
        freshness=freshness(),
        trace_context=trace(),
    )

    assert dto.path_type == "MONITORING_ONLY"


def test_escalation_trigger_requires_from_and_to_path() -> None:
    with pytest.raises(ValidationError):
        EscalationTriggerDTO(
            trigger_id="trig-1",
            source_event_ref="event-1",
            trigger_reason="threshold_exceeded",
            from_path="MONITORING_ONLY",
            detected_at_utc=now(),
            trace_context=trace(),
        )

    dto = EscalationTriggerDTO(
        trigger_id="trig-1",
        source_event_ref="event-1",
        trigger_reason="threshold_exceeded",
        from_path="MONITORING_ONLY",
        to_path="STANDARD",
        detected_at_utc=now(),
        trace_context=trace(),
    )

    assert dto.to_path == "STANDARD"
