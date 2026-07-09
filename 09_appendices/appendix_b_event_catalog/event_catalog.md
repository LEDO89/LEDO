---
title: Event Catalog
version: 1.2
status: populated
owner: platform-ontology
language: en
last_updated: 2026-07-06
---

# Event Catalog

## Purpose

Catalog reference items and examples. Do not treat this appendix as executable runtime code.

This is the non-authoritative Event Type Catalog referenced by `03_core_specifications/02_event_type_taxonomy/2_event_type_taxonomy.md` (its Section 13 previously mislabeled this as "Appendix A"; this folder is Appendix A only for the Stack Catalog — this event catalog is Appendix B, and the source document has been corrected accordingly). The list below is copied from that document's Section 12 for convenience. If this appendix diverges from the governing specification or registry, the governing specification or registry wins.

## Notes

This document is intentionally written in English so that Codex and other coding agents can use it as a non-authoritative index. All event names below are non-normative reference fixtures, not a claim about real field conditions or thresholds.

## Initial Reference Event Type Set

### Industrial Reference Events

industrial.sensor.reading_received
industrial.sensor.threshold_crossed
industrial.sensor.offline_detected
industrial.plc.alarm_raised
industrial.equipment.mode_changed

### Construction Reference Events

construction.worker.entered_zone
construction.worker.exited_zone
construction.permit.expired
construction.task.status_changed
construction.inspection.failed

### Safety Reference Events

safety.zone.risk_level_changed
safety.worker.entered_danger_zone
safety.gas.critical_threshold_exceeded
safety.emergency.fast_path_triggered

### Robot Reference Events

robot.telemetry.received
robot.pose.updated
robot.mission.assigned
robot.mission.blocked
robot.mission.completed
robot.battery.critical

### Lifecycle Reference Events

validation.input.passed
canonicalization.identity.resolved
ontology.binding.completed
evidence.created
world_state.updated
agent.action_candidate.created
decision.case.created
approval.request.created
action.approved.created
execution.request.created
external_control.request.sent
feedback.completed
audit.record.created
audit.emergency.post_audit_pending
audit.emergency.post_audit_completed

## Full Catalog Categories (Beyond Initial Scope)

The following category catalogs are expected to grow beyond the reference set above, per `02_event_type_taxonomy` Section 13. They are listed here as placeholders only; populating them with additional concrete event names requires the same registry governance process as the reference set (see `06_registry_specs/event_registry/event_registry.md`), not ad hoc addition:

industrial event catalog (beyond initial scope)
construction event catalog (beyond initial scope)
robot event catalog (beyond initial scope)
safety event catalog (beyond initial scope)
AI / agent event catalog
decision / approval event catalog
execution event catalog
feedback / recovery event catalog
audit / governance event catalog
observability event catalog
vendor extension event examples
