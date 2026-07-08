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
        id="vr-1",
        validator_id="validator-1",
        approved_action_id="approved-1",
        result="PASS",
        checked_at=now(),
        trace_id="trace-1",
    )

    assert dto.result == "PASS"


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
        id="vr-1",
        validator_id="validator-1",
        approved_action_id="approved-1",
        result="PASS",
        checked_at=now(),
        trace_id="trace-1",
    )

    assert dto.result == "PASS"
    assert isinstance(dto, ValidatorResultDTO)
