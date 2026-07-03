from backend.api_gateway import MVPService
from backend.schemas import PhysicalCommandStatus


def print_header(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def print_rule_trace(state) -> None:
    print("Rule decision trace:")
    if not state.rule_decision_trace:
        print("  none")
        return
    for item in state.rule_decision_trace.evaluations:
        print(f"  {item.rule_id} | matched={item.matched} | {item.reason}")


def print_audit_summary(state) -> None:
    print("Audit trace summary:")
    for event in sorted(state.audit_trace, key=lambda item: item.timestamp):
        print(f"  L{event.layer} {event.event_type}: {event.result} - {event.reason}")


def print_graph_summary(state) -> None:
    print(f"Ontology graph projection: {len(state.graph_nodes)} nodes, {len(state.graph_edges)} edges")
    rule_nodes = [node for node in state.graph_nodes if node.type in {"RuleEvaluation", "MatchedRule", "EmergencyRule"}]
    print(f"Rule graph nodes: {len(rule_nodes)}")


def run() -> None:
    service = MVPService()

    print_header("1. Critical Collision Scenario")
    critical = service.run_critical_collision()
    print(f"Selected path: {critical.router_result.selected_path}")
    print(f"LLM bypassed: {critical.router_result.llm_bypassed}")
    print(f"Human pre-approval required: {critical.router_result.human_pre_approval_required}")
    print(f"ActionCandidate: {critical.action_candidate.action_type if critical.action_candidate else None}")
    print(f"Safety Gate: {'PASS' if critical.safety_gate_pass else 'BLOCK'}")
    print(f"ExecutionRequest created: {critical.execution_request is not None}")
    print(f"Adapter status: {critical.adapter_result.status if critical.adapter_result else None}")
    print(f"PhysicalCommandStatus: {critical.physical_command_status}")
    print_rule_trace(critical)
    print_graph_summary(critical)
    print_audit_summary(critical)

    print_header("2. Async Replan Scenario")
    service = MVPService()
    pending = service.run_async_replan()
    print(f"Selected path: {pending.router_result.selected_path}")
    print(f"LLM candidate used: {pending.action_candidate.llm_generated if pending.action_candidate else None}")
    print(f"Candidate authoritative: {pending.action_candidate.candidate_authoritative if pending.action_candidate else None}")
    print(f"Pending DecisionCase: {pending.decision_case.id if pending.decision_case else None}")
    print(f"ExecutionRequest before approval: {pending.execution_request}")
    approved = service.approve_pending()
    print(f"Approval status: {approved.approval_decision.status if approved.approval_decision else None}")
    print(f"Runtime validation valid: {approved.runtime_validation_result.valid if approved.runtime_validation_result else None}")
    print(f"Safety Gate: {'PASS' if approved.safety_gate_pass else 'BLOCK'}")
    print(f"ExecutionRequest created: {approved.execution_request is not None}")
    print(f"Adapter status: {approved.adapter_result.status if approved.adapter_result else None}")
    print(f"PhysicalCommandStatus: {approved.physical_command_status}")
    print_graph_summary(approved)
    print_audit_summary(approved)

    assert critical.physical_command_status == PhysicalCommandStatus.NEVER_CREATED
    assert approved.physical_command_status == PhysicalCommandStatus.NEVER_CREATED


if __name__ == "__main__":
    run()
