from dataclasses import dataclass
from enum import Enum


class ActionType(str, Enum):
    LOCK_ZONE = "LOCK_ZONE"


@dataclass(frozen=True)
class Person:
    id: str
    located_in_zone_id: str


@dataclass(frozen=True)
class Zone:
    id: str


@dataclass(frozen=True)
class Hazard:
    id: str
    affects_zone_id: str
    active: bool


@dataclass(frozen=True)
class ActionCandidate:
    id: str
    action_type: ActionType
    target_zone_id: str
    reason: str


@dataclass(frozen=True)
class ApprovalDecision:
    id: str
    action_candidate_id: str
    approved: bool
    approver: str


@dataclass(frozen=True)
class ApprovedAction:
    id: str
    action_candidate: ActionCandidate
    approval_decision: ApprovalDecision


@dataclass(frozen=True)
class RuntimeValidationResult:
    id: str
    approved_action_id: str
    valid: bool
    message: str


@dataclass(frozen=True)
class SafetyGatePass:
    id: str
    approved_action_id: str
    validation_result_id: str
    message: str


@dataclass(frozen=True)
class SafetyGateBlock:
    id: str
    approved_action_id: str
    validation_result_id: str
    reason: str


@dataclass(frozen=True)
class ExecutionRequest:
    id: str
    approved_action_id: str
    safety_gate_pass_id: str
    external_system: str
    note: str


@dataclass(frozen=True)
class PhysicalCommand:
    id: str
    command: str

