from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Literal, Optional, Union
from uuid import uuid4

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


class EventUrgency(str, Enum):
    CRITICAL_REALTIME = "CRITICAL_REALTIME"
    HIGH_RISK = "HIGH_RISK"
    ASYNC_PLANNING = "ASYNC_PLANNING"
    ROUTINE = "ROUTINE"


class DecisionPath(str, Enum):
    REALTIME_RULE_PATH = "REALTIME_RULE_PATH"
    ASYNC_LLM_APPROVAL_PATH = "ASYNC_LLM_APPROVAL_PATH"
    BLOCKED_BY_POLICY = "BLOCKED_BY_POLICY"


class ActionType(str, Enum):
    E_STOP = "E_STOP"
    LOCK_ZONE = "LOCK_ZONE"
    REPLAN_WORK = "REPLAN_WORK"


class SafetyGateResult(str, Enum):
    PASS = "PASS"
    BLOCK = "BLOCK"


class PhysicalCommandStatus(str, Enum):
    NEVER_CREATED = "NEVER_CREATED"


class ApprovalStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    NOT_REQUIRED = "NOT_REQUIRED"


class CandidateSource(str, Enum):
    RULE_EMERGENCY_CORE = "RULE_EMERGENCY_CORE"
    LLM_CANDIDATE_ADAPTER = "LLM_CANDIDATE_ADAPTER"


class PolicyResult(BaseModel):
    id: str = Field(default_factory=lambda: new_id("policy"))
    trace_id: str
    timestamp: datetime = Field(default_factory=utc_now)
    allowed: bool
    approval_status: ApprovalStatus
    decision_path: Optional[DecisionPath] = None
    reason: str
    policy_id: str
    policy_bundle_version: str = "mvp-phase-2-rego-v1"


class TraceObject(BaseModel):
    id: str
    trace_id: str
    timestamp: datetime = Field(default_factory=utc_now)
    reason: str = ""


class SiteEvent(TraceObject):
    event_type: str
    urgency: EventUrgency
    robot_id: Optional[str] = None
    worker_id: Optional[str] = None
    zone_id: Optional[str] = None
    source: str = "mvp.simulator"
    payload: dict[str, Any] = Field(default_factory=dict)


class Worker(BaseModel):
    id: str
    trace_id: str
    timestamp: datetime = Field(default_factory=utc_now)
    reason: str = "MVP worker placeholder; domain meaning requires expert governance."
    zone_id: str


class Robot(BaseModel):
    id: str
    trace_id: str
    timestamp: datetime = Field(default_factory=utc_now)
    reason: str = "MVP robot placeholder; no robot behavior semantics are implemented."
    zone_id: str
    moving: bool
    moving_toward_worker: bool


class Equipment(BaseModel):
    id: str
    trace_id: str
    timestamp: datetime = Field(default_factory=utc_now)
    reason: str = "MVP equipment placeholder."
    zone_id: str
    status: str = "SIMULATED"


class Zone(BaseModel):
    id: str
    trace_id: str
    timestamp: datetime = Field(default_factory=utc_now)
    reason: str = "MVP zone placeholder."
    label: str


class Hazard(BaseModel):
    id: str
    trace_id: str
    timestamp: datetime = Field(default_factory=utc_now)
    reason: str = "MVP hazard placeholder derived from simulated event evidence."
    hazard_type: str
    active: bool
    zone_id: str


class WorldStateSnapshot(TraceObject):
    robot: Robot
    worker: Worker
    zone: Zone
    equipment: Optional[Equipment] = None
    hazard: Optional[Hazard] = None
    collision_risk_active: bool = False
    robot_worker_distance_m: Optional[float] = None
    snapshot_version: str = "snapshot-mvp-phase-2-v1"
    observed_at: datetime = Field(default_factory=utc_now)
    max_age_ms: int = 1000
    policy_version: str = "mvp-phase-2-rego-v1"
    ontology_version: str = "ot-mvp-phase-2-v1"

    def age_ms(self) -> float:
        return (utc_now() - self.observed_at).total_seconds() * 1000

    @property
    def fresh(self) -> bool:
        return self.age_ms() <= self.max_age_ms


class EvidenceRecord(TraceObject):
    source: str
    provenance: str
    trust_metadata: dict[str, Any]
    validation_status: str
    linked_event_id: str
    snapshot_id: str


class RuleEvaluation(BaseModel):
    id: str = Field(default_factory=lambda: new_id("rule_eval"))
    trace_id: str
    timestamp: datetime = Field(default_factory=utc_now)
    rule_id: str
    rule_name: str
    matched: bool
    input_facts: dict[str, Any]
    output_decision: dict[str, Any]
    reason: str


class RuleDecisionTrace(TraceObject):
    evaluations: list[RuleEvaluation] = Field(default_factory=list)
    matched_rule_id: Optional[str] = None
    matched_rule_name: Optional[str] = None
    rule_core_used: bool = True


class DecisionRouterResult(TraceObject):
    selected_path: DecisionPath
    llm_bypassed: bool
    human_pre_approval_required: bool
    rule_core_used: bool = False
    risk_level: str = "UNSET"


class ActionCandidate(TraceObject):
    action_type: ActionType
    source: CandidateSource
    target_entity_id: str
    target_zone_id: str
    urgency: EventUrgency
    decision_path: DecisionPath
    rule_id: Optional[str] = None
    rule_name: Optional[str] = None
    llm_generated: bool = False
    candidate_authoritative: bool = False
    requires_human_pre_approval: bool = True


class DecisionCase(TraceObject):
    event_id: str
    candidate: ActionCandidate
    approval_required: bool
    approval_status: ApprovalStatus
    selected_path: DecisionPath


class ApprovalDecision(TraceObject):
    decision_case_id: str
    approver_id: str
    status: ApprovalStatus


class ApprovedAction(TraceObject):
    decision_case_id: str
    action_candidate_id: str
    action_type: ActionType
    approval_decision_id: Optional[str]
    target_entity_id: str
    target_zone_id: str
    idempotency_key: str


class RuntimeValidationResult(TraceObject):
    action_type: ActionType
    valid: bool
    validator_results: dict[str, Union[bool, str, float]]


class SafetyGatePass(TraceObject):
    result: Literal[SafetyGateResult.PASS] = SafetyGateResult.PASS
    approved_action_id: str
    runtime_validation_result_id: str
    idempotency_key: str


class SafetyGateBlock(TraceObject):
    result: Literal[SafetyGateResult.BLOCK] = SafetyGateResult.BLOCK
    approved_action_id: Optional[str] = None
    runtime_validation_result_id: Optional[str] = None
    block_code: str


class ExecutionRequest(TraceObject):
    approved_action_id: str
    safety_gate_pass_id: str
    action_type: ActionType
    target_entity_id: str
    target_zone_id: str
    target_external_system: str
    idempotency_key: str
    physical_command_status: PhysicalCommandStatus = PhysicalCommandStatus.NEVER_CREATED


class AdapterResult(TraceObject):
    execution_request_id: str
    adapter_id: str
    accepted: bool
    status: str
    physical_command_status: PhysicalCommandStatus = PhysicalCommandStatus.NEVER_CREATED


class FeedbackEvent(TraceObject):
    execution_request_id: str
    adapter_result_id: str
    status: str
    physical_command_status: PhysicalCommandStatus = PhysicalCommandStatus.NEVER_CREATED


class AuditEvent(BaseModel):
    id: str = Field(default_factory=lambda: new_id("audit"))
    trace_id: str
    event_id: Optional[str] = None
    decision_case_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=utc_now)
    layer: int
    layer_name: str
    event_type: str
    actor: str
    target: str
    result: str
    reason: str
    attributes: dict[str, Any] = Field(default_factory=dict)


class OntologyGraphNode(BaseModel):
    id: str
    label: str
    type: str
    data: dict[str, Any] = Field(default_factory=dict)


class OntologyGraphEdge(BaseModel):
    id: str
    source: str
    target: str
    label: str
    type: str = "semantic"


class WarRoomState(BaseModel):
    id: str = "war_room_state"
    trace_id: str = "not_started"
    timestamp: datetime = Field(default_factory=utc_now)
    current_event: Optional[SiteEvent] = None
    world_state: Optional[WorldStateSnapshot] = None
    evidence: list[EvidenceRecord] = Field(default_factory=list)
    router_result: Optional[DecisionRouterResult] = None
    rule_decision_trace: Optional[RuleDecisionTrace] = None
    action_candidate: Optional[ActionCandidate] = None
    decision_case: Optional[DecisionCase] = None
    approval_decision: Optional[ApprovalDecision] = None
    approved_action: Optional[ApprovedAction] = None
    runtime_validation_result: Optional[RuntimeValidationResult] = None
    safety_gate_pass: Optional[SafetyGatePass] = None
    safety_gate_block: Optional[SafetyGateBlock] = None
    execution_request: Optional[ExecutionRequest] = None
    adapter_result: Optional[AdapterResult] = None
    feedback_event: Optional[FeedbackEvent] = None
    audit_trace: list[AuditEvent] = Field(default_factory=list)
    graph_nodes: list[OntologyGraphNode] = Field(default_factory=list)
    graph_edges: list[OntologyGraphEdge] = Field(default_factory=list)
    physical_command_status: PhysicalCommandStatus = PhysicalCommandStatus.NEVER_CREATED
    layer_coverage: dict[int, str] = Field(default_factory=dict)
