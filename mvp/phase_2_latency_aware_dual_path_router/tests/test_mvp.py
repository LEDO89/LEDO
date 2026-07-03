import inspect
from pathlib import Path

from backend.api_gateway import MVPService
from backend.app import LOCAL_MVP_FRONTEND_ORIGINS, app
from backend.graph_projection import project_graph
from backend.rdf_seed import build_decision_chain_triples
from backend.rule_core import RuleEmergencyCore
from backend.runtime_validation import RuntimeValidator
from backend.safety_gate import SafetyGate
from backend.schemas import (
    ActionType,
    ApprovalStatus,
    CandidateSource,
    DecisionPath,
    PhysicalCommandStatus,
    SafetyGatePass,
)


def event_types(state):
    return [event.event_type for event in state.audit_trace]


def assert_timestamps_sorted(state):
    timestamps = [event.timestamp for event in state.audit_trace]
    assert timestamps == sorted(timestamps)


def test_critical_collision_event_routes_to_realtime_rule_path():
    state = MVPService().run_critical_collision()
    assert state.router_result.selected_path == DecisionPath.REALTIME_RULE_PATH


def test_critical_path_does_not_call_llm_candidate_adapter():
    service = MVPService()
    service.run_critical_collision()
    assert service.llm_adapter.call_count == 0


def test_critical_path_bypasses_human_pre_approval():
    state = MVPService().run_critical_collision()
    assert state.router_result.human_pre_approval_required is False


def test_critical_path_creates_estop_action_candidate_via_rule_core():
    state = MVPService().run_critical_collision()
    assert state.action_candidate.action_type == ActionType.E_STOP
    assert state.action_candidate.source == CandidateSource.RULE_EMERGENCY_CORE


def test_r_estop_001_creates_estop_candidate_for_active_immediate_collision_risk():
    state = MVPService().run_critical_collision()
    assert state.rule_decision_trace.matched_rule_id == "R-ESTOP-001"
    assert state.action_candidate.action_type == ActionType.E_STOP


def test_r_estop_001_sets_llm_bypassed_true():
    state = MVPService().run_critical_collision()
    assert state.router_result.llm_bypassed is True


def test_r_estop_001_sets_human_pre_approval_required_false():
    state = MVPService().run_critical_collision()
    assert state.action_candidate.requires_human_pre_approval is False


def test_every_rule_decision_has_rule_id_and_reason():
    state = MVPService().run_critical_collision()
    assert all(e.rule_id and e.reason for e in state.rule_decision_trace.evaluations)


def test_critical_path_creates_execution_request_after_safety_gate_pass():
    state = MVPService().run_critical_collision()
    assert state.safety_gate_pass is not None
    assert state.execution_request is not None


def test_async_replan_event_routes_to_async_llm_approval_path():
    state = MVPService().run_async_replan()
    assert state.router_result.selected_path == DecisionPath.ASYNC_LLM_APPROVAL_PATH


def test_async_path_calls_llm_candidate_adapter():
    service = MVPService()
    service.run_async_replan()
    assert service.llm_adapter.call_count == 1


def test_async_path_cannot_create_approved_action_before_human_approval():
    state = MVPService().run_async_replan()
    assert state.decision_case.approval_status == ApprovalStatus.PENDING
    assert state.approved_action is None
    assert state.execution_request is None


def test_async_rejection_prevents_approved_action():
    service = MVPService()
    service.run_async_replan()
    state = service.reject_pending()
    assert state.approval_decision.status == ApprovalStatus.REJECTED
    assert state.approved_action is None


def test_async_rejection_prevents_execution_request():
    service = MVPService()
    service.run_async_replan()
    state = service.reject_pending()
    assert state.execution_request is None


def test_async_approval_allows_runtime_validation():
    service = MVPService()
    service.run_async_replan()
    state = service.approve_pending()
    assert state.runtime_validation_result is not None


def test_async_approval_allows_safety_gate_pass_when_current_truth_valid():
    service = MVPService()
    service.run_async_replan()
    state = service.approve_pending()
    assert state.safety_gate_pass is not None


def test_stale_world_state_blocks_safety_gate():
    state = MVPService().run_critical_collision(stale=True)
    assert state.safety_gate_block is not None
    assert state.execution_request is None
    assert "stale" in state.safety_gate_block.reason


def test_inactive_collision_risk_prevents_execution_request():
    state = MVPService().run_critical_collision(collision_active=False)
    assert state.execution_request is None


def test_emergency_policy_allows_estop_without_human_pre_approval():
    state = MVPService().run_critical_collision()
    assert state.decision_case.approval_status == ApprovalStatus.NOT_REQUIRED


def test_forbidden_policy_blocks_execution_request():
    state = MVPService().run_critical_collision(forbidden_policy=True)
    assert state.router_result.selected_path == DecisionPath.BLOCKED_BY_POLICY
    assert state.execution_request is None


def test_safety_gate_block_prevents_execution_request():
    state = MVPService().run_critical_collision(stale=True)
    assert state.safety_gate_block is not None
    assert state.execution_request is None


def test_adapter_mock_never_creates_physical_command():
    state = MVPService().run_critical_collision()
    assert state.adapter_result.physical_command_status == PhysicalCommandStatus.NEVER_CREATED


def test_rdf_triples_are_persisted_to_graph_db_boundary():
    service = MVPService()
    service.run_critical_collision()
    assert len(service.graph_store.triples) > 0


def test_sparql_query_returns_decision_chain():
    service = MVPService()
    service.run_critical_collision()
    assert service.graph_store.run_sparql("SELECT ?id WHERE { ?s ?p ?o }")


def test_sparql_query_returns_rule_evaluation_chain():
    service = MVPService()
    service.run_critical_collision()
    rows = service.graph_store.query_rule_evaluations()
    assert any(row["type"] == "RuleEvaluation" for row in rows)


def test_graph_projection_is_generated_from_graph_db_results():
    service = MVPService()
    service.run_critical_collision()
    nodes, edges = project_graph(service.graph_store)
    assert nodes and edges
    assert all(node.data["source"] == "GraphDBQueryResult" for node in nodes)


def test_war_room_ui_state_includes_graph_nodes_and_edges_from_graph_db():
    state = MVPService().run_critical_collision()
    assert state.graph_nodes and state.graph_edges
    assert state.graph_nodes[0].data["source"] == "GraphDBQueryResult"


def test_war_room_state_includes_rule_decision_trace():
    state = MVPService().run_critical_collision()
    assert state.rule_decision_trace is not None


def test_audit_trace_records_all_major_layer_transitions():
    state = MVPService().run_critical_collision()
    layers = {event.layer for event in state.audit_trace}
    assert set(range(13)).issubset(layers)


def test_audit_trace_records_rule_evaluation_events():
    state = MVPService().run_critical_collision()
    types = {event.event_type for event in state.audit_trace}
    assert {"RULE_EVALUATION_STARTED", "RULE_MATCHED", "RULE_ACTION_CANDIDATE_CREATED"}.issubset(types)


def test_audit_trace_is_sorted_by_timestamp_ascending():
    state = MVPService().run_critical_collision()
    assert_timestamps_sorted(state)


def test_reset_clears_previous_scenario_audit_trace():
    service = MVPService()
    service.run_critical_collision()
    state = service.reset()
    types = event_types(state)
    assert types == ["MVP_RESET"]
    assert "API_EVENT_INGESTED" not in types
    assert "WAR_ROOM_STATE_REFRESHED" not in types


def test_api_state_does_not_create_misleading_scenario_audit_events():
    if app is None:
        raise AssertionError("FastAPI app is required for API state regression test.")
    reset_endpoint = next(route.endpoint for route in app.routes if getattr(route, "path", None) == "/api/reset")
    state_endpoint = next(route.endpoint for route in app.routes if getattr(route, "path", None) == "/api/state")

    reset_endpoint()
    state = state_endpoint()
    types = event_types(state)
    assert "WAR_ROOM_STATE_REFRESHED" not in types
    assert "PHYSICAL_BOUNDARY_VERIFIED" not in types
    assert "API_EVENT_INGESTED" not in types


def test_critical_collision_audit_starts_with_trace_or_ingest_event():
    state = MVPService().run_critical_collision()
    types = event_types(state)
    assert types[0] in {"AUDIT_TRACE_STARTED", "API_EVENT_INGESTED"}
    assert types[0] != "WAR_ROOM_STATE_REFRESHED"


def test_async_replan_audit_starts_with_trace_or_ingest_event():
    state = MVPService().run_async_replan()
    types = event_types(state)
    assert types[0] in {"AUDIT_TRACE_STARTED", "API_EVENT_INGESTED"}
    assert types[0] != "WAR_ROOM_STATE_REFRESHED"


def test_war_room_state_refreshed_appears_after_graph_update():
    state = MVPService().run_critical_collision()
    types = event_types(state)
    assert types.index("GRAPH_DB_TRIPLES_PERSISTED") < types.index("WAR_ROOM_STATE_REFRESHED")


def test_physical_boundary_verified_is_last_active_trace_event():
    state = MVPService().run_critical_collision()
    assert event_types(state)[-1] == "PHYSICAL_BOUNDARY_VERIFIED"


def test_async_and_critical_audit_traces_are_not_mixed():
    service = MVPService()
    critical_state = service.run_critical_collision()
    async_state = service.run_async_replan()
    assert async_state.trace_id != critical_state.trace_id
    assert all(event.trace_id == async_state.trace_id for event in async_state.audit_trace)
    assert "REALTIME_RULE_PATH_SELECTED" not in event_types(async_state)


def test_frontend_audit_trace_panel_displays_timestamp_and_sorts_events():
    source = Path("frontend/src/components/AuditTracePanel.tsx").read_text()
    assert "<th>Timestamp</th>" in source
    assert ".sort(" in source
    assert "new Date(left.timestamp).getTime()" in source


def test_backend_app_has_local_mvp_cors_middleware_configured():
    if app is None:
        raise AssertionError("FastAPI app is required for CORS regression test.")
    cors = next(middleware for middleware in app.user_middleware if middleware.cls.__name__ == "CORSMiddleware")
    assert cors.kwargs["allow_origins"] == LOCAL_MVP_FRONTEND_ORIGINS
    assert "http://localhost:3000" in cors.kwargs["allow_origins"]
    assert "http://127.0.0.1:3000" in cors.kwargs["allow_origins"]
    assert "http://localhost:3001" in cors.kwargs["allow_origins"]
    assert "http://127.0.0.1:3001" in cors.kwargs["allow_origins"]
    assert cors.kwargs["allow_methods"] == ["*"]
    assert cors.kwargs["allow_headers"] == ["*"]


def test_frontend_api_uses_public_api_base_with_127_fallback():
    source = Path("frontend/src/lib/api.ts").read_text()
    assert 'process.env.NEXT_PUBLIC_API_BASE ?? "http://127.0.0.1:8765"' in source
    assert "API request failed for" in source


def test_war_room_dashboard_sets_state_from_action_responses():
    source = Path("frontend/src/components/WarRoomDashboard.tsx").read_text()
    assert "const nextState = await fn()" in source
    assert "setState(nextState)" in source
    assert "onClick={() => run(api.critical)}" in source
    assert "onClick={() => run(api.asyncReplan)}" in source
    assert "onClick={() => run(api.reset)}" in source
    assert "onApprove={() => run(api.approve)}" in source
    assert "onReject={() => run(api.reject)}" in source


def test_war_room_dashboard_displays_trace_id_last_updated_and_error_status():
    source = Path("frontend/src/components/WarRoomDashboard.tsx").read_text()
    assert "requestStatus" in source
    assert "setRequestStatus(\"loading\")" in source
    assert "setRequestStatus(\"success\")" in source
    assert "setRequestStatus(\"error\")" in source
    assert "Trace ID" in source
    assert "Last Updated" in source
    assert "role=\"alert\"" in source
    assert "console.error" in source


def test_safety_gate_hot_path_does_not_call_llm():
    source = inspect.getsource(SafetyGate) + inspect.getsource(RuntimeValidator)
    assert "LLMCandidateAdapter" not in source
    assert "llm" not in source.lower()


def test_rule_emergency_core_never_calls_llm_candidate_adapter():
    source = inspect.getsource(RuleEmergencyCore)
    assert "LLMCandidateAdapter" not in source
    assert "create_candidate" not in source


def test_execution_request_is_not_physical_command():
    state = MVPService().run_critical_collision()
    assert state.execution_request.physical_command_status == PhysicalCommandStatus.NEVER_CREATED


def test_physical_command_status_remains_never_created():
    state = MVPService().run_critical_collision()
    assert state.physical_command_status == PhysicalCommandStatus.NEVER_CREATED


def test_llm_candidate_output_is_never_authoritative():
    state = MVPService().run_async_replan()
    assert state.action_candidate.llm_generated is True
    assert state.action_candidate.candidate_authoritative is False
