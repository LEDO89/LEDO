from .schemas import ActionType, ApprovedAction, ExecutionRequest, SafetyGatePass, new_id


def create_execution_request(approved_action: ApprovedAction, safety_pass: SafetyGatePass) -> ExecutionRequest:
    target = "mock_robot_fleet_manager" if approved_action.action_type in {ActionType.E_STOP, ActionType.REPLAN_WORK} else "mock_site_system"
    return ExecutionRequest(
        id=new_id("execution_request"),
        trace_id=approved_action.trace_id,
        approved_action_id=approved_action.id,
        safety_gate_pass_id=safety_pass.id,
        action_type=approved_action.action_type,
        target_entity_id=approved_action.target_entity_id,
        target_zone_id=approved_action.target_zone_id,
        target_external_system=target,
        idempotency_key=safety_pass.idempotency_key,
        reason="ExecutionRequest is bounded intent for an external system; not a PhysicalCommand.",
    )

