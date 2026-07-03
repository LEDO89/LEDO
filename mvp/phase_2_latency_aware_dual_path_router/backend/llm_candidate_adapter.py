from .schemas import ActionCandidate, ActionType, CandidateSource, DecisionPath, EventUrgency, SiteEvent, new_id


class LLMCandidateAdapter:
    def __init__(self) -> None:
        self.call_count = 0

    def create_candidate(self, event: SiteEvent) -> ActionCandidate:
        self.call_count += 1
        return ActionCandidate(
            id=new_id("candidate"),
            trace_id=event.trace_id,
            reason="Mock LLM candidate for async replanning; non-authoritative and requires approval.",
            action_type=ActionType.REPLAN_WORK,
            source=CandidateSource.LLM_CANDIDATE_ADAPTER,
            target_entity_id=event.robot_id or "R1",
            target_zone_id=event.zone_id or "Z1",
            urgency=EventUrgency.ASYNC_PLANNING,
            decision_path=DecisionPath.ASYNC_LLM_APPROVAL_PATH,
            llm_generated=True,
            candidate_authoritative=False,
            requires_human_pre_approval=True,
        )

