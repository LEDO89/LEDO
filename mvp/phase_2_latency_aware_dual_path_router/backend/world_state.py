from .config import settings
from .schemas import Equipment, Hazard, Robot, Worker, WorldStateSnapshot, Zone, new_id, utc_now


def critical_collision_snapshot(trace_id: str, *, collision_active: bool = True, stale: bool = False) -> WorldStateSnapshot:
    observed_at = utc_now()
    if stale:
        from datetime import timedelta

        observed_at = observed_at - timedelta(seconds=3)
    return WorldStateSnapshot(
        id=new_id("snapshot"),
        trace_id=trace_id,
        reason="Current state cache materialized for critical collision hot path.",
        robot=Robot(id="R1", trace_id=trace_id, zone_id="Z1", moving=True, moving_toward_worker=True),
        worker=Worker(id="P1", trace_id=trace_id, zone_id="Z1"),
        equipment=Equipment(id="EQ1", trace_id=trace_id, zone_id="Z1"),
        zone=Zone(id="Z1", trace_id=trace_id, label="Zone Z1"),
        hazard=Hazard(id="HZ1", trace_id=trace_id, hazard_type="immediate_collision_risk", active=collision_active, zone_id="Z1"),
        collision_risk_active=collision_active,
        robot_worker_distance_m=1.2,
        observed_at=observed_at,
        max_age_ms=settings.max_snapshot_age_ms,
        policy_version=settings.policy_bundle_version,
        ontology_version=settings.ontology_version,
        snapshot_version=settings.snapshot_version,
    )


def async_replan_snapshot(trace_id: str) -> WorldStateSnapshot:
    return WorldStateSnapshot(
        id=new_id("snapshot"),
        trace_id=trace_id,
        reason="Current state cache materialized for async planning route.",
        robot=Robot(id="R1", trace_id=trace_id, zone_id="Z1", moving=False, moving_toward_worker=False),
        worker=Worker(id="P1", trace_id=trace_id, zone_id="Z1"),
        equipment=Equipment(id="EQ1", trace_id=trace_id, zone_id="Z1"),
        zone=Zone(id="Z1", trace_id=trace_id, label="Zone Z1"),
        hazard=Hazard(id="HZ2", trace_id=trace_id, hazard_type="productivity_delay_placeholder", active=True, zone_id="Z1"),
        collision_risk_active=False,
        robot_worker_distance_m=9.0,
        max_age_ms=settings.max_snapshot_age_ms,
        policy_version=settings.policy_bundle_version,
        ontology_version=settings.ontology_version,
        snapshot_version=settings.snapshot_version,
    )

