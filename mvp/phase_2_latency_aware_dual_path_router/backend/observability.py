from .audit_trace import AuditTrace, LAYER_NAMES


def otel_fields(trace_id: str, event_id=None, decision_case_id=None) -> dict:
    return {
        "trace_id": trace_id,
        "event_id": event_id,
        "decision_case_id": decision_case_id,
        "service.name": "ledo-mvp-phase-2",
        "deployment.environment": "local-mvp",
    }
