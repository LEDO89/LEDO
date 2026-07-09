from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from ledo_ontology_core.framework.schemas import (
    ApprovalValidityResultDTO,
    EvidenceValidityResultDTO,
    IdempotencyResultDTO,
    NetworkHealthResultDTO,
    PolicyRevalidationResultDTO,
    RuntimeValidationInputDTO,
    RuntimeValidationResultDTO,
    SHACLValidationResultDTO,
    TOCTOUResultDTO,
    ValidatorResultDTO,
    ValidatorStatus,
)


def now() -> datetime:
    return datetime.now(timezone.utc)


def test_runtime_validation_input_requires_trace_id() -> None:
    with pytest.raises(ValidationError):
        RuntimeValidationInputDTO(
            id="rvi-1",
            approved_action_id="approved-1",
            action_type="fixture_action",
            created_at_utc=now(),
        )

    dto = RuntimeValidationInputDTO(
        id="rvi-1",
        approved_action_id="approved-1",
        action_type="fixture_action",
        trace_id="trace-1",
        created_at_utc=now(),
    )
    assert dto.trace_id == "trace-1"


def test_runtime_validation_result_carries_validator_refs() -> None:
    dto = RuntimeValidationResultDTO(
        id="rvr-1",
        approved_action_id="approved-1",
        action_type="fixture_action",
        result="PASS",
        checked_at=now(),
        validator_result_refs=["validator-1", "validator-2"],
        trace_id="trace-1",
    )

    assert dto.validator_result_refs == ["validator-1", "validator-2"]


def test_validator_result_base_fields() -> None:
    dto = ValidatorResultDTO(
        result_id="vr-1",
        validator_id="validator-1",
        validator_version="1.0.0",
        approved_action_id="approved-1",
        action_type="fixture_action",
        status="PASS",
        severity="INFO",
        tier="TIER_1_SAFETY_CRITICAL",
        checked_at=now(),
        safety_gate_eligible=True,
        trace_id="trace-1",
    )

    assert dto.status == "PASS"


@pytest.mark.parametrize(
    "dto_cls",
    [
        TOCTOUResultDTO,
        SHACLValidationResultDTO,
        NetworkHealthResultDTO,
        IdempotencyResultDTO,
        ApprovalValidityResultDTO,
        PolicyRevalidationResultDTO,
        EvidenceValidityResultDTO,
    ],
)
def test_specialized_validator_results_follow_validator_result_pattern(dto_cls) -> None:
    dto = dto_cls(
        result_id="vr-1",
        validator_id="validator-1",
        validator_version="1.0.0",
        approved_action_id="approved-1",
        action_type="fixture_action",
        status="PASS",
        severity="INFO",
        tier="TIER_1_SAFETY_CRITICAL",
        checked_at=now(),
        safety_gate_eligible=True,
        trace_id="trace-1",
    )

    assert dto.status == "PASS"
    assert isinstance(dto, ValidatorResultDTO)


def test_validator_result_rejects_invalid_status() -> None:
    with pytest.raises(ValidationError):
        ValidatorResultDTO(
            result_id="vr-1",
            validator_id="validator-1",
            validator_version="1.0.0",
            approved_action_id="approved-1",
            action_type="fixture_action",
            status="NOT_A_REAL_STATUS",
            severity="INFO",
            tier="TIER_1_SAFETY_CRITICAL",
            checked_at=now(),
            safety_gate_eligible=True,
            trace_id="trace-1",
        )


def test_validator_status_has_exactly_the_nine_canonical_members() -> None:
    # Canonical source: 08_runtime_validation/validators/validators.md Section 7.
    assert {member.value for member in ValidatorStatus} == {
        "PASS",
        "FAIL",
        "WARNING",
        "HOLD",
        "RETRY",
        "REQUIRES_REVALIDATION",
        "REQUIRES_REAPPROVAL",
        "MANUAL_REVIEW_REQUIRED",
        "BLOCK",
    }


def base_result_kwargs(**overrides: object) -> dict:
    base = dict(
        result_id="vr-1",
        validator_id="validator-1",
        validator_version="1.0.0",
        approved_action_id="approved-1",
        action_type="fixture_action",
        status="PASS",
        severity="INFO",
        tier="TIER_1_SAFETY_CRITICAL",
        checked_at=now(),
        safety_gate_eligible=True,
        trace_id="trace-1",
    )
    base.update(overrides)
    return base


def test_toctou_result_carries_snapshot_comparison_fields() -> None:
    dto = TOCTOUResultDTO(
        **base_result_kwargs(
            approval_snapshot_ref="snap-approval-1",
            execution_snapshot_ref="snap-execution-1",
            changed_fields=["risk_level"],
            stale_fields=[],
            conflict_fields=[],
            block_reasons=["TOCTOU_CONFLICT"],
            required_reapproval=True,
        )
    )

    assert dto.required_reapproval is True
    assert dto.block_reasons == ["TOCTOU_CONFLICT"]


def test_shacl_result_carries_shape_and_violation_fields() -> None:
    dto = SHACLValidationResultDTO(
        **base_result_kwargs(
            shape_id="ApprovedActionShape",
            shape_version="1.0.0",
            target_node="approved-1",
            validation_status="INVALID",
            violations=["missing required property: idempotency_key"],
        )
    )

    assert dto.validation_status == "INVALID"


def test_shacl_result_rejects_invalid_validation_status() -> None:
    with pytest.raises(ValidationError):
        SHACLValidationResultDTO(**base_result_kwargs(validation_status="NOT_A_REAL_STATUS"))


def test_network_health_result_carries_circuit_breaker_and_latency_fields() -> None:
    dto = NetworkHealthResultDTO(
        **base_result_kwargs(
            external_system_id="fleet-manager-1",
            adapter_id="fleet-manager-adapter",
            health_status="DEGRADED",
            latency_ms=1200.5,
            error_rate=0.02,
            circuit_breaker_status="HALF_OPEN",
        )
    )

    assert dto.health_status == "DEGRADED"
    assert dto.circuit_breaker_status == "HALF_OPEN"


def test_network_health_result_rejects_invalid_health_status() -> None:
    with pytest.raises(ValidationError):
        NetworkHealthResultDTO(**base_result_kwargs(health_status="NOT_A_REAL_STATUS"))


def test_idempotency_result_carries_ledger_fields() -> None:
    t = now()
    dto = IdempotencyResultDTO(
        **base_result_kwargs(
            idempotency_key="idem-1",
            safety_gate_pass_id="sgp-1",
            execution_request_id="exec-1",
            first_seen_at=t,
            last_seen_at=t,
            ledger_status="COMPLETED",
            terminal_token_ref="token-1",
        )
    )

    assert dto.ledger_status == "COMPLETED"


def test_idempotency_result_rejects_invalid_ledger_status() -> None:
    with pytest.raises(ValidationError):
        IdempotencyResultDTO(**base_result_kwargs(ledger_status="NOT_A_REAL_STATUS"))
