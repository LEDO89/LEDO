"""Lifecycle constants for the MVP."""

CRITICAL_FLOW = [
    "SiteEvent",
    "WorldStateSnapshot",
    "EvidenceRecord",
    "DecisionRouterResult",
    "RuleEmergencyCore",
    "ActionCandidate",
    "ApprovedAction",
    "RuntimeValidationResult",
    "SafetyGatePass",
    "ExecutionRequest",
    "AdapterResult",
    "FeedbackEvent",
]

ASYNC_FLOW = [
    "SiteEvent",
    "SemanticMemoryLookup",
    "WorldStateSnapshot",
    "EvidenceRecord",
    "DecisionRouterResult",
    "LLMCandidateAdapter",
    "DecisionCase",
    "ApprovalDecision",
    "ApprovedAction",
    "RuntimeValidationResult",
    "SafetyGatePass",
    "ExecutionRequest",
    "AdapterResult",
    "FeedbackEvent",
]

