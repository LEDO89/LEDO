from __future__ import annotations

from .approval import approve_action, create_decision_case, decide
from .audit_trace import AuditTrace, LAYER_NAMES
from .cyber_physical_core import CyberPhysicalCore
from .decision_router import DecisionRouter
from .demo_seed import async_replan_event, critical_collision_event
from .domain_agent import AsyncPlanningAgent
from .event_bus import EventBus
from .evidence_binder import bind_evidence
from .governance_policy import GovernancePolicy
from .graph_projection import project_graph
from .graph_store import GraphStore
from .llm_candidate_adapter import LLMCandidateAdapter
from .persistence import Persistence
from .rdf_seed import build_decision_chain_triples
from .redis_store import RedisWorldStateStore
from .rule_core import RuleEmergencyCore
from .runtime_validation import RuntimeValidator
from .safety_gate import SafetyGate
from .schemas import (
    ActionType,
    ApprovalStatus,
    ApprovedAction,
    DecisionPath,
    PhysicalCommandStatus,
    SafetyGatePass,
    SiteEvent,
    WarRoomState,
    new_id,
)
from .semantic_memory import SemanticMemory
from .world_state import async_replan_snapshot, critical_collision_snapshot


class MVPService:
    def __init__(self) -> None:
        self.audit = AuditTrace()
        self.policy = GovernancePolicy()
        self.router = DecisionRouter()
        self.rule_core = RuleEmergencyCore()
        self.llm_adapter = LLMCandidateAdapter()
        self.agent = AsyncPlanningAgent(self.llm_adapter)
        self.runtime_validator = RuntimeValidator()
        self.safety_gate = SafetyGate()
        self.cyber_physical_core = CyberPhysicalCore()
        self.graph_store = GraphStore()
        self.semantic_memory = SemanticMemory(self.graph_store)
        self.persistence = Persistence()
        self.world_store = RedisWorldStateStore()
        self.event_bus = EventBus()
        self.state = WarRoomState(layer_coverage=LAYER_NAMES.copy())

    def current_state(self) -> WarRoomState:
        self.state.audit_trace = self._active_audit_trace()
        return self.state

    def reset(self) -> WarRoomState:
        self.__init__()
        self.audit.record(
            trace_id="reset",
            layer=0,
            event_type="MVP_RESET",
            actor="api_gateway",
            target="war_room_state",
            result="RESET",
            reason="Local MVP state reset.",
        )
        self.state.audit_trace = self.audit.all()
        return self.state

    def _active_audit_trace(self) -> list:
        if self.state.trace_id in {"not_started", "reset"}:
            return self.audit.all()
        return self.audit.for_trace(self.state.trace_id)

    def _record_layer_coverage(self, trace_id: str, event_id=None) -> None:
        for layer, name in LAYER_NAMES.items():
            if not any(e.layer == layer and e.trace_id == trace_id for e in self.audit.events):
                self.audit.record(
                    trace_id=trace_id,
                    event_id=event_id,
                    layer=layer,
                    event_type=f"LAYER_{layer}_OBSERVED",
                    actor="mvp_service",
                    target=name,
                    result="OBSERVED",
                    reason=f"Layer {layer} contributed to the MVP trace.",
                )

    def _common_ingest(self, event: SiteEvent, async_path: bool = False) -> None:
        self.audit.reset()
        self.graph_store.reset()
        self.state = WarRoomState(trace_id=event.trace_id, current_event=event, layer_coverage=LAYER_NAMES.copy())
        self.event_bus.publish_site_event(event)
        self.audit.record(trace_id=event.trace_id, event_id=event.id, layer=0, event_type="AUDIT_TRACE_STARTED", actor="observability", target=event.trace_id, result="STARTED", reason="Structured trace opened with OpenTelemetry-compatible IDs.")
        self.audit.record(trace_id=event.trace_id, event_id=event.id, layer=2, event_type="API_EVENT_INGESTED", actor="api_gateway", target=event.id, result="ACCEPTED", reason="API Gateway accepted and validated SiteEvent.")
        self.policy.precheck_event(event)
        self.audit.record(trace_id=event.trace_id, event_id=event.id, layer=3, event_type="POLICY_PRECHECK_PASSED", actor="governance_policy", target=event.id, result="ALLOW", reason="Governance policy allowed event to proceed to ontology binding.")
        snapshot = async_replan_snapshot(event.trace_id) if async_path else critical_collision_snapshot(event.trace_id)
        self.state.world_state = snapshot
        self.world_store.set_json("current_world_state", snapshot.model_dump(mode="json"))
        self.audit.record(trace_id=event.trace_id, event_id=event.id, layer=4, event_type="ONTOLOGY_BINDING_PREPARED", actor="ontology_kernel", target=event.id, result="MAPPED", reason="Ontology Kernel mapped event/state/action semantics into RDF triples.")
        self.audit.record(trace_id=event.trace_id, event_id=event.id, layer=6, event_type="WORLD_STATE_SNAPSHOT_MATERIALIZED", actor="redis_world_state", target=snapshot.id, result="STORED", reason="Redis/current-state cache stores materialized runtime snapshot.")
        evidence = bind_evidence(event, snapshot)
        self.state.evidence.append(evidence)
        self.audit.record(trace_id=event.trace_id, event_id=event.id, layer=5, event_type="EVIDENCE_BOUND", actor="evidence_binder", target=evidence.id, result="VALIDATED", reason=evidence.reason)

    def _finalize_graph_and_state(self) -> WarRoomState:
        triples = build_decision_chain_triples(self.state)
        self.graph_store.upload_triples(triples)
        self.audit.record(trace_id=self.state.trace_id, event_id=self.state.current_event.id if self.state.current_event else None, layer=4, event_type="GRAPH_DB_TRIPLES_PERSISTED", actor="graph_store", target="FusekiGraphStore", result="PERSISTED", reason="Semantic decision-chain triples persisted to Graph DB boundary.")
        nodes, edges = project_graph(self.graph_store)
        self.state.graph_nodes = nodes
        self.state.graph_edges = edges
        self.audit.record(trace_id=self.state.trace_id, event_id=self.state.current_event.id if self.state.current_event else None, layer=1, event_type="WAR_ROOM_STATE_REFRESHED", actor="war_room_ui", target="ReactFlowProjection", result="READY", reason="War Room graph/audit/state payload refreshed from backend query results.")
        self.audit.record(trace_id=self.state.trace_id, event_id=self.state.current_event.id if self.state.current_event else None, layer=12, event_type="PHYSICAL_BOUNDARY_VERIFIED", actor="physical_world_boundary", target="PhysicalCommand", result=PhysicalCommandStatus.NEVER_CREATED.value, reason="PhysicalCommand was never created; external system boundary remains mock-only.")
        self.state.audit_trace = self._active_audit_trace()
        self.persistence.persist_audit(self.state.audit_trace)
        self.persistence.persist_decision_case(self.state.decision_case)
        self.persistence.persist_approval_decision(self.state.approval_decision)
        self.persistence.persist_approved_action(self.state.approved_action)
        self.persistence.persist_execution_request(self.state.execution_request)
        self.persistence.persist_adapter_result(self.state.adapter_result)
        self.persistence.persist_feedback_event(self.state.feedback_event)
        self.state.timestamp = self.state.timestamp
        return self.state

    def run_critical_collision(self, *, collision_active: bool = True, stale: bool = False, forbidden_policy: bool = False) -> WarRoomState:
        event = critical_collision_event()
        self._common_ingest(event, async_path=False)
        if self.state.world_state:
            self.state.world_state.collision_risk_active = collision_active
            if self.state.world_state.hazard:
                self.state.world_state.hazard.active = collision_active
        self.policy.set_forbidden(ActionType.E_STOP, forbidden_policy)
        self.state.router_result = self.router.route(event)
        self.audit.record(trace_id=event.trace_id, event_id=event.id, layer=8, event_type="REALTIME_RULE_PATH_SELECTED", actor="decision_router", target=self.state.router_result.id, result=DecisionPath.REALTIME_RULE_PATH.value, reason=self.state.router_result.reason)
        self.audit.record(trace_id=event.trace_id, event_id=event.id, layer=8, event_type="LLM_BYPASSED", actor="decision_router", target="LLMCandidateAdapter", result="BYPASSED", reason="Critical realtime path must not wait for LLM.")
        self.audit.record(trace_id=event.trace_id, event_id=event.id, layer=8, event_type="HUMAN_PRE_APPROVAL_BYPASSED", actor="decision_router", target="approval", result="BYPASSED", reason="Emergency path bypasses human pre-approval but still validates policy/runtime/Safety Gate.")
        self.audit.record(trace_id=event.trace_id, event_id=event.id, layer=7, event_type="RULE_EVALUATION_STARTED", actor="RuleEmergencyCore", target=event.id, result="STARTED", reason="Deterministic emergency core evaluated inspectable rules.")
        candidate, rule_trace = self.rule_core.evaluate(event, self.state.world_state)
        self.state.rule_decision_trace = rule_trace
        for ev in rule_trace.evaluations:
            self.audit.record(trace_id=event.trace_id, event_id=event.id, layer=7, event_type="RULE_MATCHED" if ev.matched else "RULE_NOT_MATCHED", actor="RuleEmergencyCore", target=ev.rule_id, result=str(ev.matched), reason=ev.reason, attributes=ev.model_dump(mode="json"))
        if candidate:
            self.state.action_candidate = candidate
            self.audit.record(trace_id=event.trace_id, event_id=event.id, layer=7, event_type="RULE_ACTION_CANDIDATE_CREATED", actor="RuleEmergencyCore", target=candidate.id, result=candidate.action_type.value, reason=candidate.reason)
            policy_result = self.policy.evaluate_action(candidate.action_type, event)
            self.audit.record(trace_id=event.trace_id, event_id=event.id, layer=3, event_type="EMERGENCY_POLICY_CHECK", actor="governance_policy", target=candidate.action_type.value, result="ALLOW" if policy_result.allowed else "BLOCK", reason=policy_result.reason)
            if policy_result.allowed:
                case = create_decision_case(event.id, candidate, approval_required=False)
                self.state.decision_case = case
                self.state.approved_action = approve_action(case, approval=None)
                self.state.approved_action.reason = "Emergency ApprovedAction created from deterministic policy-not-required path; still not a physical command."
                self.audit.record(trace_id=event.trace_id, event_id=event.id, decision_case_id=case.id, layer=10, event_type="APPROVED_ACTION_CREATED", actor="cyber_physical_core", target=self.state.approved_action.id, result="CREATED", reason=self.state.approved_action.reason)
                if stale and self.state.world_state:
                    self.state.world_state.max_age_ms = -1
                self._runtime_safety_execute(self.state.approved_action)
            else:
                self.state.router_result.selected_path = DecisionPath.BLOCKED_BY_POLICY
                self.audit.record(trace_id=event.trace_id, event_id=event.id, layer=9, event_type="BLOCKED_BY_POLICY", actor="governance_policy", target=candidate.id, result="BLOCK", reason=policy_result.reason)
        return self._finalize_graph_and_state()

    def run_async_replan(self) -> WarRoomState:
        event = async_replan_event()
        self._common_ingest(event, async_path=True)
        self.semantic_memory.lookup_context(event.trace_id)
        self.audit.record(trace_id=event.trace_id, event_id=event.id, layer=5, event_type="SEMANTIC_MEMORY_LOOKUP", actor="semantic_memory", target="GraphDB", result="READ", reason="Async planning may read semantic graph outside Safety Gate hot path.")
        self.state.router_result = self.router.route(event)
        self.audit.record(trace_id=event.trace_id, event_id=event.id, layer=8, event_type="ASYNC_LLM_APPROVAL_PATH_SELECTED", actor="decision_router", target=self.state.router_result.id, result=DecisionPath.ASYNC_LLM_APPROVAL_PATH.value, reason=self.state.router_result.reason)
        candidate = self.agent.propose(event)
        self.state.action_candidate = candidate
        self.audit.record(trace_id=event.trace_id, event_id=event.id, layer=7, event_type="LLM_CANDIDATE_CREATED", actor="LLMCandidateAdapter", target=candidate.id, result="NON_AUTHORITATIVE", reason=candidate.reason)
        case = create_decision_case(event.id, candidate, approval_required=True)
        self.state.decision_case = case
        self.audit.record(trace_id=event.trace_id, event_id=event.id, decision_case_id=case.id, layer=3, event_type="HUMAN_APPROVAL_REQUIRED", actor="governance_policy", target=case.id, result="PENDING", reason="LLM candidate cannot create ApprovedAction or ExecutionRequest without approval.")
        return self._finalize_graph_and_state()

    def approve_pending(self) -> WarRoomState:
        case = self.state.decision_case
        if case is None:
            return self.state
        approval = decide(case, ApprovalStatus.APPROVED, "manager.mock", "Mock manager approved async replanning candidate.")
        self.state.approval_decision = approval
        case.approval_status = ApprovalStatus.APPROVED
        self.audit.record(trace_id=case.trace_id, event_id=case.event_id, decision_case_id=case.id, layer=3, event_type="APPROVAL_DECISION_CREATED", actor=approval.approver_id, target=case.id, result=approval.status.value, reason=approval.reason)
        self.state.approved_action = approve_action(case, approval)
        self.audit.record(trace_id=case.trace_id, event_id=case.event_id, decision_case_id=case.id, layer=10, event_type="APPROVED_ACTION_CREATED", actor="approval_service", target=self.state.approved_action.id, result="CREATED", reason=self.state.approved_action.reason)
        self._runtime_safety_execute(self.state.approved_action)
        return self._finalize_graph_and_state()

    def reject_pending(self) -> WarRoomState:
        case = self.state.decision_case
        if case is None:
            return self.state
        approval = decide(case, ApprovalStatus.REJECTED, "manager.mock", "Mock manager rejected async replanning candidate.")
        self.state.approval_decision = approval
        case.approval_status = ApprovalStatus.REJECTED
        self.audit.record(trace_id=case.trace_id, event_id=case.event_id, decision_case_id=case.id, layer=3, event_type="APPROVAL_DECISION_CREATED", actor=approval.approver_id, target=case.id, result=approval.status.value, reason=approval.reason)
        self.audit.record(trace_id=case.trace_id, event_id=case.event_id, decision_case_id=case.id, layer=10, event_type="APPROVED_ACTION_NOT_CREATED", actor="approval_service", target=case.id, result="REJECTED", reason="Rejection prevents ApprovedAction and ExecutionRequest.")
        return self._finalize_graph_and_state()

    def _runtime_safety_execute(self, approved_action: ApprovedAction) -> None:
        self.state.runtime_validation_result = self.runtime_validator.validate(approved_action, self.state.world_state)
        self.audit.record(trace_id=approved_action.trace_id, decision_case_id=approved_action.decision_case_id, layer=9, event_type="RUNTIME_VALIDATION_COMPLETED", actor="runtime_validation", target=self.state.runtime_validation_result.id, result="PASS" if self.state.runtime_validation_result.valid else "BLOCK", reason=self.state.runtime_validation_result.reason)
        gate_result = self.safety_gate.evaluate(approved_action, self.state.runtime_validation_result)
        if isinstance(gate_result, SafetyGatePass):
            self.state.safety_gate_pass = gate_result
            self.audit.record(trace_id=approved_action.trace_id, decision_case_id=approved_action.decision_case_id, layer=9, event_type="SAFETY_GATE_PASS", actor="safety_gate", target=gate_result.id, result="PASS", reason=gate_result.reason)
            req, adapter_result, feedback = self.cyber_physical_core.execute(approved_action, gate_result)
            self.state.execution_request = req
            self.state.adapter_result = adapter_result
            self.state.feedback_event = feedback
            self.audit.record(trace_id=approved_action.trace_id, decision_case_id=approved_action.decision_case_id, layer=10, event_type="EXECUTION_REQUEST_CREATED", actor="cyber_physical_core", target=req.id, result="CREATED", reason=req.reason)
            self.audit.record(trace_id=approved_action.trace_id, decision_case_id=approved_action.decision_case_id, layer=11, event_type="ADAPTER_MOCK_ACCEPTED", actor="adapter_mock", target=adapter_result.id, result=adapter_result.status, reason=adapter_result.reason)
            self.audit.record(trace_id=approved_action.trace_id, decision_case_id=approved_action.decision_case_id, layer=11, event_type="FEEDBACK_RECEIVED", actor="feedback_handler", target=feedback.id, result=feedback.status, reason=feedback.reason)
        else:
            self.state.safety_gate_block = gate_result
            self.audit.record(trace_id=approved_action.trace_id, decision_case_id=approved_action.decision_case_id, layer=9, event_type="SAFETY_GATE_BLOCK", actor="safety_gate", target=gate_result.id, result="BLOCK", reason=gate_result.reason)


service = MVPService()
