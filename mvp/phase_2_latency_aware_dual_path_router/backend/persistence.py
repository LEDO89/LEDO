from __future__ import annotations

from .schemas import (
    AdapterResult,
    ApprovalDecision,
    ApprovedAction,
    AuditEvent,
    DecisionCase,
    ExecutionRequest,
    FeedbackEvent,
)


class Persistence:
    """PostgreSQL boundary with local append-only fallback."""

    def __init__(self) -> None:
        self.audit_events: list[AuditEvent] = []
        self.decision_cases: list[DecisionCase] = []
        self.approval_decisions: list[ApprovalDecision] = []
        self.approved_actions: list[ApprovedAction] = []
        self.execution_requests: list[ExecutionRequest] = []
        self.adapter_results: list[AdapterResult] = []
        self.feedback_events: list[FeedbackEvent] = []

    def reset(self) -> None:
        self.__init__()

    def persist_audit(self, events: list[AuditEvent]) -> None:
        known = {e.id for e in self.audit_events}
        self.audit_events.extend([e for e in events if e.id not in known])

    def persist_decision_case(self, obj) -> None:
        if obj and obj.id not in {x.id for x in self.decision_cases}:
            self.decision_cases.append(obj)

    def persist_approval_decision(self, obj) -> None:
        if obj and obj.id not in {x.id for x in self.approval_decisions}:
            self.approval_decisions.append(obj)

    def persist_approved_action(self, obj) -> None:
        if obj and obj.id not in {x.id for x in self.approved_actions}:
            self.approved_actions.append(obj)

    def persist_execution_request(self, obj) -> None:
        if obj and obj.id not in {x.id for x in self.execution_requests}:
            self.execution_requests.append(obj)

    def persist_adapter_result(self, obj) -> None:
        if obj and obj.id not in {x.id for x in self.adapter_results}:
            self.adapter_results.append(obj)

    def persist_feedback_event(self, obj) -> None:
        if obj and obj.id not in {x.id for x in self.feedback_events}:
            self.feedback_events.append(obj)
