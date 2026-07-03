from .config import settings
from .schemas import (
    ActionCandidate,
    ActionType,
    CandidateSource,
    DecisionPath,
    EventUrgency,
    RuleDecisionTrace,
    RuleEvaluation,
    SiteEvent,
    WorldStateSnapshot,
    new_id,
)


class RuleEmergencyCore:
    def evaluate(self, event: SiteEvent, world_state: WorldStateSnapshot):
        evaluations: list[RuleEvaluation] = []
        facts = {
            "event_urgency": event.urgency.value,
            "event_type": event.event_type,
            "collision_risk_active": world_state.collision_risk_active,
            "robot_moving_toward_worker": world_state.robot.moving_toward_worker,
            "robot_worker_distance_m": world_state.robot_worker_distance_m,
            "emergency_stop_distance_m": settings.emergency_stop_distance_m,
            "snapshot_fresh": world_state.fresh,
        }
        matched = (
            event.urgency == EventUrgency.CRITICAL_REALTIME
            and "collision" in event.event_type
            and world_state.collision_risk_active
            and world_state.robot.moving_toward_worker
            and world_state.robot_worker_distance_m is not None
            and world_state.robot_worker_distance_m <= settings.emergency_stop_distance_m
            and world_state.fresh
        )
        reason = (
            "Immediate collision risk requires deterministic E_STOP."
            if matched
            else "Immediate collision E-Stop rule did not match all required facts."
        )
        evaluations.append(
            RuleEvaluation(
                trace_id=event.trace_id,
                rule_id="R-ESTOP-001",
                rule_name="Immediate collision E-Stop",
                matched=matched,
                input_facts=facts,
                output_decision={"action_type": ActionType.E_STOP.value} if matched else {"action_type": None},
                reason=reason,
            )
        )
        candidate = None
        if matched:
            candidate = ActionCandidate(
                id=new_id("candidate"),
                trace_id=event.trace_id,
                reason=reason,
                action_type=ActionType.E_STOP,
                source=CandidateSource.RULE_EMERGENCY_CORE,
                rule_id="R-ESTOP-001",
                rule_name="Immediate collision E-Stop",
                target_entity_id=event.robot_id or world_state.robot.id,
                target_zone_id=event.zone_id or world_state.zone.id,
                urgency=event.urgency,
                decision_path=DecisionPath.REALTIME_RULE_PATH,
                llm_generated=False,
                candidate_authoritative=False,
                requires_human_pre_approval=False,
            )
        trace = RuleDecisionTrace(
            id=new_id("rule_trace"),
            trace_id=event.trace_id,
            reason=reason,
            evaluations=evaluations,
            matched_rule_id="R-ESTOP-001" if matched else None,
            matched_rule_name="Immediate collision E-Stop" if matched else None,
            rule_core_used=True,
        )
        return candidate, trace
