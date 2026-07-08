from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from ledo_ontology_core.framework.schemas import (
    SafetyGateBlockDTO,
    SafetyGateInputDTO,
    SafetyGatePassDTO,
    SafetyGatePassTerminalStatus,
    SafetyGateResultDTO,
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


def safety_gate_pass_kwargs(**overrides: object) -> dict:
    base = dict(
        safety_gate_pass_id="sgp-1",
        approved_action_id="approved-1",
        action_type="fixture_action",
        issued_at=now(),
        expires_at=now() + timedelta(seconds=30),
        lease_duration_ms=500,
        lease_started_monotonic_ms=1000,
        lease_expires_monotonic_ms=1500,
        target_external_system="mock_fleet_manager",
        execution_request_scope="fixture_scope",
        idempotency_key="idem-1",
        safety_snapshot_ref="snap-1",
        runtime_validation_result_ref="rvr-1",
        trace_id="trace-1",
        terminal_status="ISSUED",
    )
    base.update(overrides)
    return base


def test_safety_gate_pass_is_a_short_lived_lease() -> None:
    dto = SafetyGatePassDTO(**safety_gate_pass_kwargs())

    assert dto.expires_at > dto.issued_at
    assert dto.lease_duration_ms == 500


def test_safety_gate_block_carries_failure_reasons() -> None:
    dto = SafetyGateBlockDTO(
        safety_gate_block_id="sgb-1",
        approved_action_id="approved-1",
        action_type="fixture_action",
        blocked_at=now(),
        block_reasons=["STALE_STATE"],
        safety_snapshot_ref="snap-1",
        severity="CRITICAL",
        tier="TIER_1_SAFETY_CRITICAL",
        manual_review_required=False,
        trace_id="trace-1",
    )

    assert dto.block_reasons == ["STALE_STATE"]


def test_safety_gate_pass_rejects_invalid_terminal_status() -> None:
    with pytest.raises(ValidationError):
        SafetyGatePassDTO(**safety_gate_pass_kwargs(terminal_status="NOT_A_REAL_STATUS"))


def test_safety_gate_result_rejects_invalid_status() -> None:
    dto = SafetyGateResultDTO(
        result_id="sgr-1",
        approved_action_id="approved-1",
        action_type="fixture_action",
        status="PASS",
        issued_pass_ref="sgp-1",
        checked_at=now(),
        runtime_validation_result_ref="rvr-1",
        safety_snapshot_ref="snap-1",
        trace_id="trace-1",
    )

    assert dto.status == "PASS"

    with pytest.raises(ValidationError):
        SafetyGateResultDTO(
            result_id="sgr-1",
            approved_action_id="approved-1",
            action_type="fixture_action",
            status="NOT_A_REAL_STATUS",
            checked_at=now(),
            runtime_validation_result_ref="rvr-1",
            safety_snapshot_ref="snap-1",
            trace_id="trace-1",
        )


def test_safety_gate_pass_terminal_status_has_exactly_the_seven_canonical_members() -> None:
    # Canonical source: 08_runtime_validation/toctou/toctou.md Section 21, cross-confirmed
    # by 08_runtime_validation/idempotency/idempotency_control.md Section 9.
    assert {member.value for member in SafetyGatePassTerminalStatus} == {
        "ISSUED",
        "DISPATCHING",
        "CONSUMED_ACCEPTED",
        "CONSUMED_REJECTED",
        "CONSUMED_DROPPED",
        "EXPIRED",
        "REVOKED",
    }
