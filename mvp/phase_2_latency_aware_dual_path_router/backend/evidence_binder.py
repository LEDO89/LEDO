from .schemas import EvidenceRecord, SiteEvent, WorldStateSnapshot, new_id


def bind_evidence(event: SiteEvent, snapshot: WorldStateSnapshot) -> EvidenceRecord:
    return EvidenceRecord(
        id=new_id("evidence"),
        trace_id=event.trace_id,
        reason="Evidence binds simulated source signal to a materialized world state snapshot; AI output is not evidence.",
        source=event.source,
        provenance=f"event:{event.id}->snapshot:{snapshot.id}",
        trust_metadata={"source_type": "simulated_fixture", "ai_generated": False, "validation": "MVP_SCHEMA_VALIDATED"},
        validation_status="VALIDATED",
        linked_event_id=event.id,
        snapshot_id=snapshot.id,
    )

