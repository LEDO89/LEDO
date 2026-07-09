"""Canonical lifecycle boundary validators.

Primary source: 03_core_specifications/00_canonical_object_lifecycle/
0_canonical_object_lifecycle.md.

These functions validate lifecycle boundaries only. They do not approve actions,
run Safety Gate decisions, dispatch execution, or define domain-specific rules.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Any

from ledo_ontology_core.framework.schemas.action import ActionCandidateDTO
from ledo_ontology_core.framework.schemas.audit import AuditRecordDTO
from ledo_ontology_core.framework.schemas.execution import (
    ApprovedActionDTO,
    ExecutionRequestDTO,
)
from ledo_ontology_core.framework.schemas.enums import PathType
from ledo_ontology_core.framework.schemas.lifecycle_state import (
    FAILURE_STAGES,
    LIFECYCLE_STAGE_ORDER,
    LifecycleStage,
)
from ledo_ontology_core.framework.schemas.runtime_validation import (
    RuntimeValidationResultDTO,
)
from ledo_ontology_core.framework.schemas.safety_gate import SafetyGatePassDTO


class LifecycleBoundaryError(ValueError):
    """Raised when a lifecycle boundary rule is violated."""


ALLOWED_AI_OUTPUT_TYPES: frozenset[str] = frozenset(
    {
        "Intent",
        "ActionCandidate",
        "Explanation",
        "EvidenceSummary",
        "MappingProposal",
        "RiskInterpretation",
        "DocumentSummary",
        "PolicyImpactSuggestion",
        "ValidationSuggestion",
    }
)

FORBIDDEN_AI_OUTPUT_TYPES: frozenset[str] = frozenset(
    {
        "ApprovedAction",
        "EmergencyApprovedAction",
        "ExecutionRequest",
        "ExternalControlRequest",
        "PLC_COMMAND",
        "ROBOT_MOTION_COMMAND",
        "SCADA_COMMAND",
        "MACHINE_SEQUENCE_INSTRUCTION",
        "EMERGENCY_BYPASS_DECISION",
        "SAFETY_BYPASS_DECISION",
        "PHYSICAL_CONTROL_DECISION",
    }
)

_PHYSICAL_COMMAND_KEYS = frozenset(
    {
        "plc_command",
        "scada_command",
        "robot_motion_command",
        "motor_command",
        "machine_sequence_instruction",
        "physical_command",
        "emergency_stop_command",
    }
)


def validate_lifecycle_transition(
    path: PathType | str,
    stages: Sequence[LifecycleStage | str],
    *,
    allow_terminal_failure: bool = True,
) -> bool:
    """Validate monotonic lifecycle stage order and required execution boundaries."""

    lifecycle_path = _coerce_path(path)
    normalized_stages = tuple(_coerce_stage(stage) for stage in stages)
    canonical_order = LIFECYCLE_STAGE_ORDER[lifecycle_path]
    stage_positions = {stage: index for index, stage in enumerate(canonical_order)}
    previous_position = -1

    for stage in normalized_stages:
        if stage in FAILURE_STAGES:
            if allow_terminal_failure:
                return True
            raise LifecycleBoundaryError(f"{stage.value} is a failure stage")
        if stage not in stage_positions:
            raise LifecycleBoundaryError(
                f"{stage.value} is not valid for {lifecycle_path.value}"
            )
        position = stage_positions[stage]
        if position <= previous_position:
            raise LifecycleBoundaryError(
                f"{stage.value} does not advance the {lifecycle_path.value} lifecycle"
            )
        previous_position = position

    _require_intermediate_stages(
        stages=normalized_stages,
        earlier=LifecycleStage.APPROVED_ACTION_CREATED,
        later=LifecycleStage.EXECUTION_REQUEST_CREATED,
        required=(
            LifecycleStage.RUNTIME_VALIDATION_RESULT_CREATED,
            LifecycleStage.SAFETY_GATE_PASSED,
        ),
    )
    _require_intermediate_stages(
        stages=normalized_stages,
        earlier=LifecycleStage.EMERGENCY_APPROVED_ACTION_CREATED,
        later=LifecycleStage.EMERGENCY_EXECUTION_REQUEST_CREATED,
        required=(
            LifecycleStage.EMERGENCY_RUNTIME_VALIDATION_RESULT_CREATED,
            LifecycleStage.EMERGENCY_SAFETY_GATE_PASSED,
        ),
    )
    return True


def validate_ai_boundary(output_type: str, *, produced_by_ai: bool) -> bool:
    """Ensure AI output remains candidate/proposal-level."""

    if not produced_by_ai:
        return True
    if output_type in FORBIDDEN_AI_OUTPUT_TYPES:
        raise LifecycleBoundaryError(
            f"AI output must not directly produce {output_type}"
        )
    if output_type not in ALLOWED_AI_OUTPUT_TYPES:
        raise LifecycleBoundaryError(
            f"{output_type} is not an allowed AI output role"
        )
    return True


def validate_evidence_boundary(
    evidence_refs: Sequence[str],
    *,
    ai_summary_refs: Sequence[str] = (),
) -> bool:
    """Ensure AI summaries do not satisfy evidence requirements by themselves."""

    if not evidence_refs:
        raise LifecycleBoundaryError("Evidence is required for trusted decisions")
    if set(evidence_refs).issubset(set(ai_summary_refs)):
        raise LifecycleBoundaryError(
            "AI EvidenceSummary may summarize evidence but cannot be the only evidence"
        )
    return True


def validate_action_candidate_boundary(candidate: ActionCandidateDTO) -> bool:
    """ActionCandidate is not approval and not execution."""

    forbidden_keys = {
        "approved_action_id",
        "approval_decision_id",
        "execution_request_id",
    }
    if forbidden_keys.intersection(candidate.constraints):
        raise LifecycleBoundaryError(
            "ActionCandidate must not carry approval or execution identity"
        )
    return True


def validate_approved_action_boundary(approved_action: ApprovedActionDTO) -> bool:
    """ApprovedAction is approved intent, not physical command payload."""

    if _contains_physical_command(approved_action.constraints):
        raise LifecycleBoundaryError(
            "ApprovedAction must not contain direct physical command payloads"
        )
    return True


def validate_execution_request_boundary(
    execution_request: ExecutionRequestDTO,
    *,
    runtime_validation_result: RuntimeValidationResultDTO | None,
    safety_gate_pass: SafetyGatePassDTO | None,
) -> bool:
    """ExecutionRequest requires RuntimeValidationResult and SafetyGatePass."""

    if _contains_physical_command(execution_request.execution_constraints):
        raise LifecycleBoundaryError(
            "ExecutionRequest must not contain direct physical command payloads"
        )
    if runtime_validation_result is None:
        raise LifecycleBoundaryError(
            "ExecutionRequest requires RuntimeValidationResult"
        )
    if safety_gate_pass is None:
        raise LifecycleBoundaryError("ExecutionRequest requires SafetyGatePass")
    if (
        execution_request.approved_action_ref
        != runtime_validation_result.approved_action_id
    ):
        raise LifecycleBoundaryError(
            "ExecutionRequest and RuntimeValidationResult must reference the same "
            "ApprovedAction"
        )
    if execution_request.approved_action_ref != safety_gate_pass.approved_action_id:
        raise LifecycleBoundaryError(
            "ExecutionRequest and SafetyGatePass must reference the same ApprovedAction"
        )
    if (
        execution_request.execution_lease.get("safety_gate_pass_id")
        != safety_gate_pass.safety_gate_pass_id
    ):
        raise LifecycleBoundaryError(
            "ExecutionRequest lease must bind the same SafetyGatePass"
        )
    if execution_request.idempotency_key != safety_gate_pass.idempotency_key:
        raise LifecycleBoundaryError(
            "ExecutionRequest and SafetyGatePass idempotency keys must match"
        )
    return True


def validate_audit_trace_path(
    audit_record: AuditRecordDTO,
    objects: Iterable[Any],
) -> bool:
    """Ensure all lifecycle objects preserve the same trace id as the audit record."""

    missing_trace: list[str] = []
    mismatched_trace: list[str] = []

    for obj in objects:
        trace_id = _extract_trace_id(obj)
        type_name = type(obj).__name__
        if trace_id is None:
            missing_trace.append(type_name)
        elif trace_id != audit_record.trace_id:
            mismatched_trace.append(type_name)

    if missing_trace:
        raise LifecycleBoundaryError(
            f"Lifecycle objects missing trace id: {', '.join(missing_trace)}"
        )
    if mismatched_trace:
        raise LifecycleBoundaryError(
            f"Lifecycle objects have mismatched trace id: {', '.join(mismatched_trace)}"
        )
    return True


def _coerce_path(path: PathType | str) -> PathType:
    return path if isinstance(path, PathType) else PathType(path)


def _coerce_stage(stage: LifecycleStage | str) -> LifecycleStage:
    return stage if isinstance(stage, LifecycleStage) else LifecycleStage(stage)


def _require_intermediate_stages(
    *,
    stages: tuple[LifecycleStage, ...],
    earlier: LifecycleStage,
    later: LifecycleStage,
    required: tuple[LifecycleStage, ...],
) -> None:
    if earlier not in stages or later not in stages:
        return

    earlier_index = stages.index(earlier)
    later_index = stages.index(later)
    if later_index < earlier_index:
        raise LifecycleBoundaryError(
            f"{later.value} cannot occur before {earlier.value}"
        )

    between = set(stages[earlier_index + 1 : later_index])
    missing = [stage.value for stage in required if stage not in between]
    if missing:
        raise LifecycleBoundaryError(
            f"{later.value} requires intermediate stages: {', '.join(missing)}"
        )


def _extract_trace_id(obj: Any) -> str | None:
    trace_context = getattr(obj, "trace_context", None)
    if trace_context is not None:
        return getattr(trace_context, "trace_id", None)
    return getattr(obj, "trace_id", None)


def _contains_physical_command(value: Any) -> bool:
    if isinstance(value, dict):
        for key, nested in value.items():
            if str(key).lower() in _PHYSICAL_COMMAND_KEYS:
                return True
            if _contains_physical_command(nested):
                return True
    if isinstance(value, (list, tuple, set)):
        return any(_contains_physical_command(item) for item in value)
    return False
