import type { WarRoomState } from "../lib/types";

export function DecisionRouterPanel({ state }: { state: WarRoomState | null }) {
  const router = state?.router_result;
  const rule = state?.rule_decision_trace;
  return (
    <section className="panel">
      <h2>Decision Router</h2>
      <dl className="grid">
        <dt>Selected Path</dt><dd>{router?.selected_path ?? "none"}</dd>
        <dt>LLM Bypass</dt><dd>{String(router?.llm_bypassed ?? false)}</dd>
        <dt>Human Approval Required</dt><dd>{String(router?.human_pre_approval_required ?? false)}</dd>
        <dt>Risk Level</dt><dd>{router?.risk_level ?? "none"}</dd>
        <dt>Rule Core Used</dt><dd>{String(router?.rule_core_used ?? false)}</dd>
        <dt>Matched Rule</dt><dd>{rule?.matched_rule_id ?? "none"}</dd>
        <dt>Rule Name</dt><dd>{rule?.matched_rule_name ?? "none"}</dd>
        <dt>Reason</dt><dd>{router?.reason ?? "none"}</dd>
      </dl>
    </section>
  );
}

