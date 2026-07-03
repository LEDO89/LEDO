from __future__ import annotations

from .graph_store import Triple
from .ontology_kernel import iri, rel
from .schemas import WarRoomState


def node(node_id: str, label: str, type_name: str, trace_id: str) -> list[Triple]:
    subject = iri(f"node_{node_id}")
    return [
        Triple(subject, rel("graphId"), node_id),
        Triple(subject, rel("graphLabel"), label),
        Triple(subject, rel("graphType"), type_name),
        Triple(subject, rel("traceId"), trace_id),
    ]


def edge(edge_id: str, source: str, target: str, label: str, trace_id: str) -> list[Triple]:
    subject = iri(f"edge_{edge_id}")
    return [
        Triple(subject, rel("edgeId"), edge_id),
        Triple(subject, rel("edgeSource"), source),
        Triple(subject, rel("edgeTarget"), target),
        Triple(subject, rel("edgeLabel"), label),
        Triple(subject, rel("traceId"), trace_id),
    ]


def build_decision_chain_triples(state: WarRoomState) -> list[Triple]:
    trace_id = state.trace_id
    triples: list[Triple] = []
    triples += node("RuleEmergencyCore", "RuleEmergencyCore", "RuleEmergencyCore", trace_id)
    triples += node("LLMCandidateAdapter", "LLMCandidateAdapter", "LLMCandidateAdapter", trace_id)
    triples += node("EmergencyPolicy", "EmergencyPolicy", "EmergencyPolicy", trace_id)
    triples += node("PhysicalWorldBoundary", "PhysicalCommand NEVER_CREATED", "PhysicalWorldBoundary", trace_id)
    if state.current_event:
        triples += node(state.current_event.id, state.current_event.event_type, "SiteEvent", trace_id)
        triples += node(f"urgency_{state.current_event.urgency.value}", state.current_event.urgency.value, "EventUrgency", trace_id)
        triples += edge(f"{state.current_event.id}_has_urgency", state.current_event.id, f"urgency_{state.current_event.urgency.value}", "has_urgency", trace_id)
    if state.world_state:
        triples += node(state.world_state.id, "WorldStateSnapshot", "WorldStateSnapshot", trace_id)
        triples += node(state.world_state.robot.id, "Robot R1", "Robot", trace_id)
        triples += node(state.world_state.worker.id, "Worker P1", "Worker", trace_id)
        triples += node(state.world_state.zone.id, "Zone Z1", "Zone", trace_id)
        triples += edge(f"{state.world_state.robot.id}_located_in", state.world_state.robot.id, state.world_state.zone.id, "located_in", trace_id)
        triples += edge(f"{state.world_state.worker.id}_located_in", state.world_state.worker.id, state.world_state.zone.id, "located_in", trace_id)
        if state.world_state.robot.moving_toward_worker:
            triples += edge("R1_moving_toward_P1", state.world_state.robot.id, state.world_state.worker.id, "moving_toward", trace_id)
    for evidence in state.evidence:
        triples += node(evidence.id, "EvidenceRecord", "EvidenceRecord", trace_id)
        if state.current_event:
            triples += edge(f"{evidence.id}_supports_{state.current_event.id}", evidence.id, state.current_event.id, "supported_by_evidence", trace_id)
    if state.router_result:
        triples += node(state.router_result.id, state.router_result.selected_path.value, "DecisionRouterResult", trace_id)
        triples += node(f"path_{state.router_result.selected_path.value}", state.router_result.selected_path.value, "DecisionPath", trace_id)
        if state.current_event:
            triples += edge(f"{state.current_event.id}_routed_to_{state.router_result.id}", state.current_event.id, state.router_result.id, "routed_to", trace_id)
        if state.router_result.llm_bypassed:
            triples += edge(f"{state.router_result.id}_bypasses_llm", state.router_result.id, "LLMCandidateAdapter", "bypasses_llm", trace_id)
        if not state.router_result.human_pre_approval_required:
            triples += edge(f"{state.router_result.id}_bypasses_human", state.router_result.id, "EmergencyPolicy", "bypasses_human_preapproval", trace_id)
    if state.rule_decision_trace:
        for ev in state.rule_decision_trace.evaluations:
            triples += node(ev.rule_id, ev.rule_name, "EmergencyRule", trace_id)
            triples += node(ev.id, ev.rule_id, "RuleEvaluation", trace_id)
            triples += edge(f"{ev.id}_evaluated_by_rule", ev.id, ev.rule_id, "evaluated_by_rule", trace_id)
            if ev.matched:
                triples += node(f"matched_{ev.rule_id}", ev.rule_name, "MatchedRule", trace_id)
                triples += edge(f"{ev.id}_matched_rule", ev.id, f"matched_{ev.rule_id}", "matched_rule", trace_id)
    if state.action_candidate:
        triples += node(state.action_candidate.id, state.action_candidate.action_type.value, "ActionCandidate", trace_id)
        if state.action_candidate.rule_id:
            triples += edge(f"{state.action_candidate.id}_produced_by_rule", state.action_candidate.rule_id, state.action_candidate.id, "produced_by_rule", trace_id)
            triples += edge(f"{state.action_candidate.id}_allowed_policy", "EmergencyPolicy", state.action_candidate.id, "allowed_by_emergency_policy", trace_id)
        else:
            triples += edge(f"{state.action_candidate.id}_generated_by_llm", "LLMCandidateAdapter", state.action_candidate.id, "generated_by", trace_id)
        if state.evidence:
            triples += edge(f"{state.action_candidate.id}_supported_by_evidence", state.action_candidate.id, state.evidence[-1].id, "supported_by_evidence", trace_id)
    if state.decision_case:
        triples += node(state.decision_case.id, "DecisionCase", "DecisionCase", trace_id)
        triples += edge(f"{state.decision_case.id}_requires_approval", state.decision_case.id, "EmergencyPolicy", "requires_approval", trace_id)
    if state.approval_decision:
        triples += node(state.approval_decision.id, state.approval_decision.status.value, "ApprovalDecision", trace_id)
        if state.decision_case:
            label = "approved_by" if state.approval_decision.status.value == "APPROVED" else "rejected_by"
            triples += edge(f"{state.decision_case.id}_{label}", state.decision_case.id, state.approval_decision.id, label, trace_id)
    if state.approved_action:
        triples += node(state.approved_action.id, state.approved_action.action_type.value, "ApprovedAction", trace_id)
    if state.runtime_validation_result:
        triples += node(state.runtime_validation_result.id, "RuntimeValidationResult", "RuntimeValidationResult", trace_id)
        if state.approved_action:
            triples += edge(f"{state.runtime_validation_result.id}_validates", state.runtime_validation_result.id, state.approved_action.id, "validates", trace_id)
    if state.safety_gate_pass:
        triples += node(state.safety_gate_pass.id, "SafetyGatePass", "SafetyGatePass", trace_id)
        if state.runtime_validation_result:
            triples += edge(f"{state.safety_gate_pass.id}_passed_by_safety_gate", state.runtime_validation_result.id, state.safety_gate_pass.id, "passed_by_safety_gate", trace_id)
    if state.safety_gate_block:
        triples += node(state.safety_gate_block.id, "SafetyGateBlock", "SafetyGateBlock", trace_id)
        if state.runtime_validation_result:
            triples += edge(f"{state.safety_gate_block.id}_blocked_by_safety_gate", state.runtime_validation_result.id, state.safety_gate_block.id, "blocked_by_safety_gate", trace_id)
    if state.execution_request:
        triples += node(state.execution_request.id, "ExecutionRequest", "ExecutionRequest", trace_id)
        if state.safety_gate_pass:
            triples += edge(f"{state.safety_gate_pass.id}_permits_execution_request", state.safety_gate_pass.id, state.execution_request.id, "permits_execution_request", trace_id)
        triples += edge(f"{state.execution_request.id}_no_physical_command", state.execution_request.id, "PhysicalWorldBoundary", "does_not_create_physical_command", trace_id)
    if state.adapter_result:
        triples += node(state.adapter_result.id, "AdapterResult", "AdapterResult", trace_id)
        if state.execution_request:
            triples += edge(f"{state.execution_request.id}_sent_to_adapter", state.execution_request.id, state.adapter_result.id, "sent_to_adapter", trace_id)
    if state.feedback_event:
        triples += node(state.feedback_event.id, "FeedbackEvent", "FeedbackEvent", trace_id)
        if state.adapter_result:
            triples += edge(f"{state.adapter_result.id}_produced_feedback", state.adapter_result.id, state.feedback_event.id, "produced_feedback", trace_id)
    return triples

