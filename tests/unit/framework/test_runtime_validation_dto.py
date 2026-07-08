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
