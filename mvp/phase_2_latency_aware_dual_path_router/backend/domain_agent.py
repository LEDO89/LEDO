from .llm_candidate_adapter import LLMCandidateAdapter
from .schemas import ActionCandidate, SiteEvent


class AsyncPlanningAgent:
    def __init__(self, llm_adapter: LLMCandidateAdapter) -> None:
        self.llm_adapter = llm_adapter

    def propose(self, event: SiteEvent) -> ActionCandidate:
        return self.llm_adapter.create_candidate(event)

