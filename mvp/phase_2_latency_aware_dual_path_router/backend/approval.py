from typing import Optional

from .schemas import (
    ActionCandidate,
    ApprovalDecision,
    ApprovalStatus,
    ApprovedAction,
    DecisionCase,
    new_id,
)


def create_decision_case(event_id: str, candidate: ActionCandidate, approval_required: bool) -> DecisionCase:
    return DecisionCase(
        id=new_id("decision_case"),
        trace_id=candidate.trace_id,
        event_id=event_id,
        candidate=candidate,
        approval_required=approval_required,
        approval_status=ApprovalStatus.PENDING if approval_required else ApprovalStatus.NOT_REQUIRED,
        selected_path=candidate.decision_path,
        reason="Decision case created; approval required only for async LLM candidate path.",
    )


def decide(case: DecisionCase, status: ApprovalStatus, approver_id: str, reason: str) -> ApprovalDecision:
    return ApprovalDecision(
        id=new_id("approval"),
        trace_id=case.trace_id,
        decision_case_id=case.id,
        approver_id=approver_id,
        status=status,
        reason=reason,
    )


def approve_action(case: DecisionCase, approval: Optional[ApprovalDecision]) -> ApprovedAction:
    return ApprovedAction(
        id=new_id("approved_action"),
        trace_id=case.trace_id,
        decision_case_id=case.id,
        action_candidate_id=case.candidate.id,
        action_type=case.candidate.action_type,
        approval_decision_id=approval.id if approval else None,
        target_entity_id=case.candidate.target_entity_id,
        target_zone_id=case.candidate.target_zone_id,
        idempotency_key=f"idem:{case.trace_id}:{case.candidate.action_type.value}:{case.candidate.target_entity_id}",
        reason="ApprovedAction is approved intent only; it is not a physical command.",
    )
