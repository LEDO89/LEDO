import type { WarRoomState } from "../lib/types";

export function ExternalSystemStatusPanel({ state }: { state: WarRoomState | null }) {
  return (
    <section className="panel">
      <h2>External Boundary</h2>
      <dl className="grid">
        <dt>ExecutionRequest</dt><dd>{state?.execution_request?.id ?? "none"}</dd>
        <dt>Adapter Result</dt><dd>{state?.adapter_result?.status ?? "none"}</dd>
        <dt>Feedback</dt><dd>{state?.feedback_event?.status ?? "none"}</dd>
        <dt>PhysicalCommandStatus</dt><dd>{state?.physical_command_status ?? "NEVER_CREATED"}</dd>
      </dl>
    </section>
  );
}

