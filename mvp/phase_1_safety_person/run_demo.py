from lifecycle import (
    create_approval_decision,
    create_approved_action,
    create_execution_request,
    create_safety_action_candidate,
    validate_runtime_state,
)
from mini_ontology import Hazard, Person, SafetyGateBlock, SafetyGatePass, Zone
from safety_gate import evaluate_safety_gate


def print_step(label: str, value: object) -> None:
    print(f"{label}: {value}")


def run_pass_case() -> None:
    print("\nScenario A: pass case")

    person = Person(id="P1", located_in_zone_id="Z1")
    zone = Zone(id="Z1")
    hazard = Hazard(id="H1", affects_zone_id="Z1", active=True)
    print_step("Person located_in Zone", person)
    print_step("Hazard affects Zone", hazard)

    candidate = create_safety_action_candidate(zone=zone, hazard=hazard)
    print_step("ActionCandidate targets Zone", candidate)

    approval = create_approval_decision(
        action_candidate=candidate,
        approved=True,
        approver="human_safety_reviewer",
    )
    print_step("ApprovalDecision approves ActionCandidate", approval)

    approved_action = create_approved_action(
        action_candidate=candidate,
        approval_decision=approval,
    )
    print_step("ApprovedAction authorizes ActionCandidate", approved_action)

    validation = validate_runtime_state(
        approved_action=approved_action,
        current_hazard=hazard,
    )
    print_step("RuntimeValidationResult validates ApprovedAction", validation)

    gate_result = evaluate_safety_gate(
        approved_action=approved_action,
        validation_result=validation,
    )
    print_step("Safety Gate decision", gate_result)

    if isinstance(gate_result, SafetyGatePass):
        execution_request = create_execution_request(gate_result)
        print_step("SafetyGatePass permits ExecutionRequest", execution_request)


def run_block_case() -> None:
    print("\nScenario B: block case")

    person = Person(id="P1", located_in_zone_id="Z1")
    zone = Zone(id="Z1")
    original_hazard = Hazard(id="H1", affects_zone_id="Z1", active=True)
    current_hazard = Hazard(id="H1", affects_zone_id="Z2", active=True)
    print_step("Person located_in Zone", person)
    print_step("Original Hazard affects Zone", original_hazard)

    candidate = create_safety_action_candidate(zone=zone, hazard=original_hazard)
    print_step("ActionCandidate targets Zone", candidate)

    approval = create_approval_decision(
        action_candidate=candidate,
        approved=True,
        approver="human_safety_reviewer",
    )
    print_step("ApprovalDecision approves ActionCandidate", approval)

    approved_action = create_approved_action(
        action_candidate=candidate,
        approval_decision=approval,
    )
    print_step("ApprovedAction authorizes ActionCandidate", approved_action)

    validation = validate_runtime_state(
        approved_action=approved_action,
        current_hazard=current_hazard,
    )
    print_step("RuntimeValidationResult validates ApprovedAction", validation)

    gate_result = evaluate_safety_gate(
        approved_action=approved_action,
        validation_result=validation,
    )
    print_step("Safety Gate decision", gate_result)

    if isinstance(gate_result, SafetyGateBlock):
        print("SafetyGateBlock prevents ExecutionRequest.")


if __name__ == "__main__":
    run_pass_case()
    run_block_case()

