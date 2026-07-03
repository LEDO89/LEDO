export type GraphNode = { id: string; label: string; type: string; data: Record<string, unknown> };
export type GraphEdge = { id: string; source: string; target: string; label: string; type: string };

export type WarRoomState = {
  trace_id: string;
  current_event?: any;
  world_state?: any;
  router_result?: any;
  rule_decision_trace?: any;
  action_candidate?: any;
  decision_case?: any;
  approval_decision?: any;
  runtime_validation_result?: any;
  safety_gate_pass?: any;
  safety_gate_block?: any;
  execution_request?: any;
  adapter_result?: any;
  feedback_event?: any;
  audit_trace: any[];
  graph_nodes: GraphNode[];
  graph_edges: GraphEdge[];
  physical_command_status: string;
};

