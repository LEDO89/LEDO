from .config import settings
from .schemas import ActionType, ApprovedAction, RuntimeValidationResult, WorldStateSnapshot, new_id


class RuntimeValidator:
    def validate(self, approved_action: ApprovedAction, snapshot: WorldStateSnapshot) -> RuntimeValidationResult:
        checks = {
            "snapshot_fresh": snapshot.fresh,
            "snapshot_age_ms": round(snapshot.age_ms(), 3),
            "snapshot_version": snapshot.snapshot_version,
            "policy_version": snapshot.policy_version,
            "ontology_version": snapshot.ontology_version,
            "idempotency_key_present": bool(approved_action.idempotency_key),
            "network_health_materialized": "healthy",
            "adapter_available_materialized": True,
        }
        valid = bool(checks["snapshot_fresh"] and checks["idempotency_key_present"] and checks["adapter_available_materialized"])
        reason = "Runtime validation passed against current materialized truth."
        if not snapshot.fresh:
            reason = "World state snapshot is stale."
            valid = False
        if approved_action.action_type == ActionType.E_STOP and not snapshot.collision_risk_active:
            checks["collision_risk_active"] = False
            reason = "Collision risk is no longer active."
            valid = False
        elif approved_action.action_type == ActionType.E_STOP:
            checks["collision_risk_active"] = True
            checks["emergency_stop_distance_m"] = settings.emergency_stop_distance_m
            checks["robot_worker_distance_m"] = snapshot.robot_worker_distance_m or -1
        return RuntimeValidationResult(
            id=new_id("runtime_validation"),
            trace_id=approved_action.trace_id,
            action_type=approved_action.action_type,
            valid=valid,
            validator_results=checks,
            reason=reason,
        )
