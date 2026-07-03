import type { WarRoomState } from "../lib/types";

export function ApprovalPanel({
  state,
  loading,
  onApprove,
  onReject
}: {
  state: WarRoomState | null;
  loading: boolean;
  onApprove: () => Promise<void>;
  onReject: () => Promise<void>;
}) {
  const pending = state?.decision_case?.approval_status === "PENDING";
  return (
    <section className="panel">
      <h2>Human Approval</h2>
      <dl className="grid">
        <dt>Manager</dt><dd>manager.mock</dd>
        <dt>Decision Case</dt><dd>{state?.decision_case?.id ?? "none"}</dd>
        <dt>Status</dt><dd>{state?.decision_case?.approval_status ?? "none"}</dd>
        <dt>Candidate Authoritative</dt><dd>{String(state?.action_candidate?.candidate_authoritative ?? false)}</dd>
      </dl>
      <div className="actions">
        <button onClick={onApprove} disabled={!pending || loading}>Approve</button>
        <button onClick={onReject} disabled={!pending || loading}>Reject</button>
      </div>
    </section>
  );
}
