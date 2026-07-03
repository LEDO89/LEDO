from .config import settings
from .schemas import ActionType, ApprovalStatus, DecisionPath, EventUrgency, PolicyResult, SiteEvent


class GovernancePolicy:
    """Deterministic evaluator mirroring policy_rules.rego for local MVP runs."""

    def __init__(self) -> None:
        self.forbidden_actions: set[ActionType] = set()

    def set_forbidden(self, action_type: ActionType, forbidden: bool = True) -> None:
        if forbidden:
            self.forbidden_actions.add(action_type)
        else:
            self.forbidden_actions.discard(action_type)

    def precheck_event(self, event: SiteEvent) -> PolicyResult:
        return PolicyResult(
            trace_id=event.trace_id,
            allowed=True,
            approval_status=ApprovalStatus.NOT_REQUIRED if event.urgency == EventUrgency.CRITICAL_REALTIME else ApprovalStatus.PENDING,
            reason="Policy precheck accepted event for ontology binding and routing.",
            policy_id="R-POLICY-PRECHECK-001",
            policy_bundle_version=settings.policy_bundle_version,
        )

    def evaluate_action(self, action_type: ActionType, event: SiteEvent) -> PolicyResult:
        if action_type in self.forbidden_actions:
            return PolicyResult(
                trace_id=event.trace_id,
                allowed=False,
                approval_status=ApprovalStatus.PENDING,
                decision_path=DecisionPath.BLOCKED_BY_POLICY,
                reason="Forbidden action blocks execution.",
                policy_id="R-POLICY-FORBIDDEN-001",
            )
        if action_type == ActionType.E_STOP and event.urgency == EventUrgency.CRITICAL_REALTIME:
            return PolicyResult(
                trace_id=event.trace_id,
                allowed=True,
                approval_status=ApprovalStatus.NOT_REQUIRED,
                reason="Emergency E_STOP is allowed without human pre-approval.",
                policy_id="R-POLICY-EMERGENCY-ALLOW-001",
            )
        if action_type == ActionType.REPLAN_WORK:
            return PolicyResult(
                trace_id=event.trace_id,
                allowed=True,
                approval_status=ApprovalStatus.PENDING,
                reason="Async planning candidate requires human approval before ApprovedAction.",
                policy_id="R-POLICY-ASYNC-APPROVAL-001",
            )
        return PolicyResult(
            trace_id=event.trace_id,
            allowed=False,
            approval_status=ApprovalStatus.PENDING,
            decision_path=DecisionPath.BLOCKED_BY_POLICY,
            reason="No MVP policy permits this action.",
            policy_id="R-POLICY-DEFAULT-DENY-001",
        )

