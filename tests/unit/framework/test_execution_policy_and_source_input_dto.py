from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from ledo_ontology_core.framework.schemas import (
    IdempotencyContextDTO,
    RecoveryPolicyDTO,
    RetryPolicyDTO,
    StateSnapshotDTO,
    TimeoutPolicyDTO,
)
from ledo_ontology_core.framework.schemas.high_frequency import TimeSeriesSampleDTO
from ledo_ontology_core.framework.schemas.source_inputs import (
    ConstructionProcessInputDTO,
    DocumentParseInputDTO,
    IndustrialTimeSeriesInputDTO,
    MobileContextInputDTO,
    RobotTelemetryBundleInputDTO,
)


def now() -> datetime:
    return datetime.now(timezone.utc)


def test_retry_and_idempotency_policy_dto_construct() -> None:
    retry = RetryPolicyDTO(max_retries=3, retry_interval_ms=500, backoff_strategy="exponential")
    idem = IdempotencyContextDTO(
        idempotency_key="idem-1",
        deduplication_window_ms=1000,
        duplicate_detected=False,
        dedupe_strategy="first_write_wins",
    )
    assert retry.max_retries == 3
    assert idem.duplicate_detected is False


def test_timeout_and_recovery_policy_reject_missing_required_fields() -> None:
    with pytest.raises(ValidationError):
        TimeoutPolicyDTO(timeout_ms=1000)

    with pytest.raises(ValidationError):
        RecoveryPolicyDTO(recovery_policy_id="r-1")


def test_state_snapshot_carries_world_states() -> None:
    dto = StateSnapshotDTO(
        snapshot_id="snap-1",
        site_id="site-1",
        snapshot_time_utc=now(),
        ontology_version="1.0",
        created_at_utc=now(),
    )
    assert dto.states == []


def test_industrial_time_series_input_carries_samples() -> None:
    dto = IndustrialTimeSeriesInputDTO(
        device_id="device-1",
        tag="tag-1",
        protocol="modbus",
        samples=[
            TimeSeriesSampleDTO(
                timestamp_utc=now(), value=1.0, quality="good", sequence_number=1, sample_status="ok"
            )
        ],
        window_start_utc=now(),
        window_end_utc=now() + timedelta(seconds=10),
    )
    assert len(dto.samples) == 1


def test_robot_telemetry_bundle_input_constructs() -> None:
    dto = RobotTelemetryBundleInputDTO(
        robot_id="robot-1",
        telemetry_type="pose",
        window_start_utc=now(),
        window_end_utc=now() + timedelta(seconds=10),
    )
    assert dto.robot_id == "robot-1"


def test_construction_process_input_requires_status_and_updated_by() -> None:
    with pytest.raises(ValidationError):
        ConstructionProcessInputDTO(task_id="task-1", timestamp_utc=now())

    dto = ConstructionProcessInputDTO(
        task_id="task-1", status="in_progress", updated_by="fixture", timestamp_utc=now()
    )
    assert dto.status == "in_progress"


def test_mobile_context_input_constructs() -> None:
    dto = MobileContextInputDTO(user_id="user-1", device_id="device-1", timestamp_utc=now())
    assert dto.user_id == "user-1"


def test_document_parse_input_constructs() -> None:
    dto = DocumentParseInputDTO(
        document_id="doc-1", document_type="permit", parsed_at_utc=now()
    )
    assert dto.document_id == "doc-1"
