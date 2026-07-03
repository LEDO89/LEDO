from .schemas import ApprovalStatus, DecisionCase


def approval_required(case: DecisionCase) -> bool:
    return case.approval_status == ApprovalStatus.PENDING

