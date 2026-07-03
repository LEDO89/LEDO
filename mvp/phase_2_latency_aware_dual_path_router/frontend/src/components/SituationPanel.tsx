import type { WarRoomState } from "../lib/types";

export function SituationPanel({ state }: { state: WarRoomState | null }) {
  const event = state?.current_event;
  const snapshot = state?.world_state;
  return (
    <section className="panel">
      <h2>Situation</h2>
      <dl className="grid">
        <dt>Event</dt><dd>{event?.event_type ?? "none"}</dd>
        <dt>Urgency</dt><dd>{event?.urgency ?? "none"}</dd>
        <dt>Robot / Worker / Zone</dt><dd>{event ? `${event.robot_id} / ${event.worker_id} / ${event.zone_id}` : "none"}</dd>
        <dt>Collision Risk</dt><dd>{String(snapshot?.collision_risk_active ?? false)}</dd>
        <dt>Distance</dt><dd>{snapshot?.robot_worker_distance_m ?? "n/a"} m</dd>
        <dt>Snapshot Fresh</dt><dd>{snapshot ? String(snapshot.max_age_ms >= 0) : "n/a"}</dd>
      </dl>
    </section>
  );
}

