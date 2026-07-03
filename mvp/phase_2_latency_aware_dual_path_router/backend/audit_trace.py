from .schemas import AuditEvent


LAYER_NAMES = {
    0: "Observability / Audit / Trace",
    1: "Experience / Presentation",
    2: "API Gateway",
    3: "Governance / Policy / Security",
    4: "Core Ontology Kernel",
    5: "Knowledge & Semantic Memory",
    6: "Real-Time World State",
    7: "Distributed Domain Agent",
    8: "Decision Router / Escalation",
    9: "Approved Action / Safety Gate",
    10: "Unified Cyber-Physical Core",
    11: "Execution Request & External Control Integration",
    12: "Physical World Boundary",
}


class AuditTrace:
    def __init__(self) -> None:
        self.events: list[AuditEvent] = []

    def record(
        self,
        *,
        trace_id: str,
        layer: int,
        event_type: str,
        actor: str,
        target: str,
        result: str,
        reason: str,
        event_id=None,
        decision_case_id=None,
        attributes=None,
    ) -> AuditEvent:
        event = AuditEvent(
            trace_id=trace_id,
            layer=layer,
            layer_name=LAYER_NAMES[layer],
            event_type=event_type,
            actor=actor,
            target=target,
            result=result,
            reason=reason,
            event_id=event_id,
            decision_case_id=decision_case_id,
            attributes=attributes or {},
        )
        self.events.append(event)
        return event

    def reset(self) -> None:
        self.events.clear()

    def all(self) -> list[AuditEvent]:
        return sorted(self.events, key=lambda event: event.timestamp)

    def for_trace(self, trace_id: str) -> list[AuditEvent]:
        return sorted(
            [event for event in self.events if event.trace_id == trace_id],
            key=lambda event: event.timestamp,
        )
