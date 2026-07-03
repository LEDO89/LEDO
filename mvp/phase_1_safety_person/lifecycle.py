from mini_ontology import (
    ActionCandidate,
    ActionType,
    ApprovalDecision,
    ApprovedAction,
    ExecutionRequest,
    Hazard,
    RuntimeValidationResult,
    SafetyGatePass,
    Zone,
)


def create_safety_action_candidate(zone: Zone, hazard: Hazard) -> ActionCandidate:
    return ActionCandidate(
        id="AC1",
        action_type=ActionType.LOCK_ZONE,
        target_zone_id=zone.id,
        reason=f"Hazard {hazard.id} affects zone {zone.id}",
    )


def create_approval_decision(
    action_candidate: ActionCandidate,
    approved: bool,
    approver: str,
) -> ApprovalDecision:
    return ApprovalDecision(
        id="AD1",
        action_candidate_id=action_candidate.id,
        approved=approved,
        approver=approver,
    )


def create_approved_action(
    action_candidate: ActionCandidate,
    approval_decision: ApprovalDecision,
) -> ApprovedAction:
    if approval_decision.action_candidate_id != action_candidate.id:
        raise ValueError("ApprovalDecision does not approve this ActionCandidate.")
    if not approval_decision.approved:
        raise ValueError("ApprovedAction requires an approved ApprovalDecision.")

    return ApprovedAction(
        id="AA1",
        action_candidate=action_candidate,
        approval_decision=approval_decision,
    )


def validate_runtime_state(
    approved_action: ApprovedAction,
    current_hazard: Hazard,
) -> RuntimeValidationResult:
    target_zone_id = approved_action.action_candidate.target_zone_id

    if not current_hazard.active:
        return RuntimeValidationResult(
            id="RVR1",
            approved_action_id=approved_action.id,
            valid=False,
            message="Runtime validation failed: hazard is no longer active.",
        )

    if current_hazard.affects_zone_id != target_zone_id:
        return RuntimeValidationResult(
            id="RVR1",
            approved_action_id=approved_action.id,
            valid=False,
            message="Runtime validation failed: hazard no longer affects target zone.",
        )

    return RuntimeValidationResult(
        id="RVR1",
        approved_action_id=approved_action.id,
        valid=True,
        message="Runtime validation passed: hazard still affects target zone.",
    )


def create_execution_request(
    safety_gate_pass: SafetyGatePass,
    external_system: str = "mock_external_site_system",
) -> ExecutionRequest:
    if not isinstance(safety_gate_pass, SafetyGatePass):
        raise ValueError("ExecutionRequest requires SafetyGatePass.")

    return ExecutionRequest(
        id="ER1",
        approved_action_id=safety_gate_pass.approved_action_id,
        safety_gate_pass_id=safety_gate_pass.id,
        external_system=external_system,
        note="Request only. External physical execution is out of scope.",
    )
