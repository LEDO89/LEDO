import unittest

from lifecycle import (
    create_approval_decision,
    create_approved_action,
    create_execution_request,
    create_safety_action_candidate,
    validate_runtime_state,
)
from mini_ontology import (
    ApprovedAction,
    ExecutionRequest,
    Hazard,
    PhysicalCommand,
    SafetyGateBlock,
    SafetyGatePass,
    Zone,
)
from safety_gate import evaluate_safety_gate


class SafetyPersonMvpTests(unittest.TestCase):
    def make_approved_action(self) -> ApprovedAction:
        zone = Zone(id="Z1")
        hazard = Hazard(id="H1", affects_zone_id="Z1", active=True)
        candidate = create_safety_action_candidate(zone=zone, hazard=hazard)
        approval = create_approval_decision(
            action_candidate=candidate,
            approved=True,
            approver="human_safety_reviewer",
        )
        return create_approved_action(
            action_candidate=candidate,
            approval_decision=approval,
        )

    def test_approved_action_cannot_be_produced_without_approval(self) -> None:
        zone = Zone(id="Z1")
        hazard = Hazard(id="H1", affects_zone_id="Z1", active=True)
        candidate = create_safety_action_candidate(zone=zone, hazard=hazard)
        denial = create_approval_decision(
            action_candidate=candidate,
            approved=False,
            approver="human_safety_reviewer",
        )

        with self.assertRaises(ValueError):
            create_approved_action(
                action_candidate=candidate,
                approval_decision=denial,
            )

    def test_safety_gate_does_not_create_approved_action(self) -> None:
        approved_action = self.make_approved_action()
        hazard = Hazard(id="H1", affects_zone_id="Z1", active=True)
        validation = validate_runtime_state(
            approved_action=approved_action,
            current_hazard=hazard,
        )

        gate_result = evaluate_safety_gate(
            approved_action=approved_action,
            validation_result=validation,
        )

        self.assertIsInstance(gate_result, SafetyGatePass)
        self.assertNotIsInstance(gate_result, ApprovedAction)

    def test_execution_request_cannot_be_created_without_safety_gate_pass(self) -> None:
        approved_action = self.make_approved_action()
        block = SafetyGateBlock(
            id="SGB1",
            approved_action_id=approved_action.id,
            validation_result_id="RVR1",
            reason="Blocked for test.",
        )

        with self.assertRaises(ValueError):
            create_execution_request(block)  # type: ignore[arg-type]

    def test_invalid_runtime_validation_result_produces_safety_gate_block(self) -> None:
        approved_action = self.make_approved_action()
        moved_hazard = Hazard(id="H1", affects_zone_id="Z2", active=True)
        validation = validate_runtime_state(
            approved_action=approved_action,
            current_hazard=moved_hazard,
        )

        gate_result = evaluate_safety_gate(
            approved_action=approved_action,
            validation_result=validation,
        )

        self.assertFalse(validation.valid)
        self.assertIsInstance(gate_result, SafetyGateBlock)

    def test_execution_request_is_not_a_physical_command(self) -> None:
        approved_action = self.make_approved_action()
        hazard = Hazard(id="H1", affects_zone_id="Z1", active=True)
        validation = validate_runtime_state(
            approved_action=approved_action,
            current_hazard=hazard,
        )
        gate_result = evaluate_safety_gate(
            approved_action=approved_action,
            validation_result=validation,
        )

        self.assertIsInstance(gate_result, SafetyGatePass)
        execution_request = create_execution_request(gate_result)

        self.assertIsInstance(execution_request, ExecutionRequest)
        self.assertNotIsInstance(execution_request, PhysicalCommand)


if __name__ == "__main__":
    unittest.main()
