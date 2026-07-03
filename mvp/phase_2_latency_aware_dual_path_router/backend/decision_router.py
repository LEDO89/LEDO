from .schemas import DecisionPath, DecisionRouterResult, EventUrgency, SiteEvent, new_id


class DecisionRouter:
    def route(self, event: SiteEvent) -> DecisionRouterResult:
        if event.urgency == EventUrgency.CRITICAL_REALTIME:
            return DecisionRouterResult(
                id=new_id("router"),
                trace_id=event.trace_id,
                selected_path=DecisionPath.REALTIME_RULE_PATH,
                llm_bypassed=True,
                human_pre_approval_required=False,
                rule_core_used=True,
                risk_level="SAFETY_CRITICAL",
                reason="Critical realtime event routes to deterministic RuleEmergencyCore.",
            )
        if event.urgency == EventUrgency.ASYNC_PLANNING:
            return DecisionRouterResult(
                id=new_id("router"),
                trace_id=event.trace_id,
                selected_path=DecisionPath.ASYNC_LLM_APPROVAL_PATH,
                llm_bypassed=False,
                human_pre_approval_required=True,
                rule_core_used=False,
                risk_level="PLANNING",
                reason="Async planning event may use LLM candidate generation, then approval.",
            )
        return DecisionRouterResult(
            id=new_id("router"),
            trace_id=event.trace_id,
            selected_path=DecisionPath.BLOCKED_BY_POLICY,
            llm_bypassed=True,
            human_pre_approval_required=True,
            risk_level="UNKNOWN",
            reason="No MVP route defined; fail closed.",
        )

