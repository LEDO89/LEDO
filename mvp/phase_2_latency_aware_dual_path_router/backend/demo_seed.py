from .schemas import EventUrgency, SiteEvent, new_id


def critical_collision_event() -> SiteEvent:
    trace_id = new_id("trace")
    return SiteEvent(
        id=new_id("event"),
        trace_id=trace_id,
        event_type="robot.collision_imminent",
        urgency=EventUrgency.CRITICAL_REALTIME,
        robot_id="R1",
        worker_id="P1",
        zone_id="Z1",
        reason="Robot R1 moving toward Worker P1 in Zone Z1; immediate collision risk detected.",
        payload={"scenario": "critical_collision", "domain_rule_status": "MVP placeholder facts"},
    )


def async_replan_event() -> SiteEvent:
    trace_id = new_id("trace")
    return SiteEvent(
        id=new_id("event"),
        trace_id=trace_id,
        event_type="planning.zone_delay_detected",
        urgency=EventUrgency.ASYNC_PLANNING,
        robot_id="R1",
        worker_id="P1",
        zone_id="Z1",
        reason="Zone Z1 productivity delay requires work replanning candidate.",
        payload={"scenario": "async_replan", "domain_rule_status": "Human domain expert must govern real planning rules."},
    )

