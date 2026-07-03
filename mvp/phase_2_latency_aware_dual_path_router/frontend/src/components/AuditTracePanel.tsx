import type { WarRoomState } from "../lib/types";

export function AuditTracePanel({ state }: { state: WarRoomState | null }) {
  const events = [...(state?.audit_trace ?? [])].sort(
    (left, right) => new Date(left.timestamp).getTime() - new Date(right.timestamp).getTime()
  );

  return (
    <section className="panel audit">
      <h2>Audit Trace</h2>
      <table>
        <thead><tr><th>Timestamp</th><th>Layer</th><th>Event</th><th>Actor</th><th>Result</th><th>Reason</th></tr></thead>
        <tbody>
          {events.slice(-24).map((event) => (
            <tr key={event.id}>
              <td>{event.timestamp ? new Date(event.timestamp).toISOString() : "unknown"}</td>
              <td>{event.layer}</td>
              <td>{event.event_type}</td>
              <td>{event.actor}</td>
              <td>{event.result}</td>
              <td>{event.reason}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
