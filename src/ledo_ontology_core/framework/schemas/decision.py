"""Decision DTO contracts from 01_common_schema_dto Section 16."""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from ledo_ontology_core.framework.schemas.base import StrictDTO
from ledo_ontology_core.framework.schemas.context import TraceContextDTO
from ledo_ontology_core.framework.schemas.enums import DecisionTier, PolicyDecisionResult


class DecisionCaseDTO(StrictDTO):
    decision_case_id: str
    candidate_ref: str
    decision_tier: DecisionTier
    risk_level: str
    urgency: str
    routing_result: str
    required_approval: bool
    policy_precheck_result: str | None = None
    evidence_summary: str | None = None
    state_freshness_result: str | None = None
    recommended_next_step: str | None = None
    trace_context: TraceContextDTO


class PolicyDecisionDTO(StrictDTO):
    policy_decision_id: str
    policy_refs: list[str] = Field(default_factory=list)
    input_context: dict
    decision_result: PolicyDecisionResult
    reason: str
    obligations: list[str] = Field(default_factory=list)
    denial_reasons: list[str] = Field(default_factory=list)
    evaluated_at_utc: datetime
