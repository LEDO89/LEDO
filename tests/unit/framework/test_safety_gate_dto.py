from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from ledo_ontology_core.framework.schemas import (
    SafetyGateBlockDTO,
    SafetyGateInputDTO,
    SafetyGatePassDTO,
    SafetySnapshotDTO,
)


def now() -> datetime:
    return datetime.now(timezone.utc)


def test_safety_snapshot_requires_checksum_and_versions() -> None:
    with pytest.raises(ValidationError):
        SafetySnapshotDTO(
            id="snap-1",
            snapshot_version="1.0",
            ontology_version="1.0",
            policy_version="1.0",
            registry_version="1.0",
            status="ACTIVE",
            created_at=now(),
            expires_at=now() + timedelta(seconds=30),
            trace_id="trace-1",
        )

    dto = SafetySnapshotDTO(
        id="snap-1",
        snapshot_version="1.0",
        ontology_version="1.0",
        policy_version="1.0",
        registry_version="1.0",
        status="ACTIVE",
        created_at=now(),
        expires_at=now() + timedelta(seconds=30),
        checksum="checksum-1",
        trace_id="trace-1",
    )
    assert dto.checksum == "checksum-1"


def test_safety_gate_input_references_snapshot_and_runtime_result() -> None:
    dto = SafetyGateInputDTO(
        id="sgi-1",
        approved_action_id="approved-1",
        runtime_validation_result_id="rvr-1",
        safety_snapshot_id="snap-1",
        action_type="fixture_action",
        trace_id="trace-1",
    )

    assert dto.safety_snapshot_id == "snap-1"


def test_safety_gate_pass_is_a_short_lived_lease() -> None:
    dto = SafetyGatePassDTO(
        id="sgp-1",
        approved_action_id="approved-1",
        runtime_validation_result_id="rvr-1",
        action_type="fixture_action",
        status="PASS",
        issued_at=now(),
        expires_at=now() + timedelta(seconds=30),
        idempotency_key="idem-1",
        trace_id="trace-1",
    )

    assert dto.expires_at > dto.issued_at


def test_safety_gate_block_carries_failure_reasons() -> None:
    dto = SafetyGateBlockDTO(
        id="sgb-1",
        approved_action_id="approved-1",
        runtime_validation_result_id="rvr-1",
        action_type="fixture_action",
        status="BLOCKED",
        checked_at=now(),
        failure_reasons=["stale_state"],
        trace_id="trace-1",
    )

    assert dto.failure_reasons == ["stale_state"]
