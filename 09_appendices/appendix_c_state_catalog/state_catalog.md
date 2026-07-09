---
title: State Catalog
version: 1.1
status: populated
owner: platform-ontology
language: en
last_updated: 2026-07-06
---

# State Catalog

## Purpose

Catalog reference items and examples. Do not treat this appendix as executable runtime code.

This is the non-authoritative State Model Catalog referenced by `03_core_specifications/04_state_model_registry/4_state_model_registry.md` (Appendix C). The list below is copied from that document's Section 16 for convenience. If this appendix diverges from the governing specification or registry, the governing specification or registry wins.

## Notes

This document is intentionally written in English so that Codex and other coding agents can use it as a non-authoritative index. State model names below are scaffolding identifiers; concrete allowed state values, transitions, and thresholds must come from the governed registry process, not be invented here.

## Initial Reference State Model Set

### Robot / Mission

RobotConnectivityState
RobotBatteryRiskState
RobotPoseState
MissionStatus
RobotOperationalState

### Construction

PermitStatus
TaskStatus
ZoneAccessState
WorkerLocationState

### Safety

ZoneRiskState
GasSensorRiskState
EmergencyState
EvacuationState

### Industrial

EquipmentOperationalState
SensorHealthState
PLCConnectionState
AlarmState
GasSensorValueState

### Platform Lifecycle

ApprovalStatus
ExecutionState
FeedbackStatus
AuditStatus
ReconciliationStatus

## Full Catalog Categories (Beyond Initial Scope)

The following category catalogs are expected to grow beyond the reference set above, per `04_state_model_registry` Section 17. They are listed here as placeholders only; adding concrete state values beyond the reference set requires registry governance (see `06_registry_specs/state_registry/state_registry.md`), not ad hoc addition:

robot state catalog (beyond initial scope)
mission state catalog (beyond initial scope)
construction state catalog (beyond initial scope)
safety state catalog (beyond initial scope)
industrial state catalog (beyond initial scope)
platform lifecycle state catalog (beyond initial scope)
execution state catalog — canonical enum lives in `03_core_specifications/09_execution_adapter_model/9_execution_adapter_model.md` Section 20 (`DispatchStatus`); do not redefine it here
feedback state catalog
audit state catalog
reconciliation state catalog
