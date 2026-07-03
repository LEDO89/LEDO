from typing import Optional, Union

from .schemas import ApprovedAction, RuntimeValidationResult, SafetyGateBlock, SafetyGatePass, new_id


class SafetyGate:
    def evaluate(
        self, approved_action: Optional[ApprovedAction], runtime_validation: Optional[RuntimeValidationResult]
    ) -> Union[SafetyGatePass, SafetyGateBlock]:
        if approved_action is None or runtime_validation is None:
            return SafetyGateBlock(
                id=new_id("safety_block"),
                trace_id="missing",
                block_code="MISSING_INPUT",
                reason="Missing ApprovedAction or RuntimeValidationResult.",
            )
        if not runtime_validation.valid:
            return SafetyGateBlock(
                id=new_id("safety_block"),
                trace_id=approved_action.trace_id,
                approved_action_id=approved_action.id,
                runtime_validation_result_id=runtime_validation.id,
                block_code="RUNTIME_VALIDATION_FAILED",
                reason=runtime_validation.reason,
            )
        return SafetyGatePass(
            id=new_id("safety_pass"),
            trace_id=approved_action.trace_id,
            approved_action_id=approved_action.id,
            runtime_validation_result_id=runtime_validation.id,
            idempotency_key=approved_action.idempotency_key,
            reason="Safety Gate pass permits ExecutionRequest creation only.",
        )
