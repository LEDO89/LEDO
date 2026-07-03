from typing import Optional, Union

from mini_ontology import (
    ApprovedAction,
    RuntimeValidationResult,
    SafetyGateBlock,
    SafetyGatePass,
)


def evaluate_safety_gate(
    approved_action: ApprovedAction,
    validation_result: Optional[RuntimeValidationResult],
) -> Union[SafetyGatePass, SafetyGateBlock]:
    if validation_result is None:
        raise ValueError("RuntimeValidationResult is required before Safety Gate.")

    if validation_result.approved_action_id != approved_action.id:
        return SafetyGateBlock(
            id="SGB1",
            approved_action_id=approved_action.id,
            validation_result_id=validation_result.id,
            reason="RuntimeValidationResult does not validate this ApprovedAction.",
        )

    if not validation_result.valid:
        return SafetyGateBlock(
            id="SGB1",
            approved_action_id=approved_action.id,
            validation_result_id=validation_result.id,
            reason=validation_result.message,
        )

    return SafetyGatePass(
        id="SGP1",
        approved_action_id=approved_action.id,
        validation_result_id=validation_result.id,
        message="Safety Gate passed. ExecutionRequest may be created.",
    )
