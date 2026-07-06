---
title: Evidence Catalog
version: 1.1
status: populated
owner: platform-ontology
language: en
last_updated: 2026-07-06
---

# Evidence Catalog

## Purpose

Catalog reference items and examples. Do not treat this appendix as executable runtime code.

This is the Evidence Type Catalog referenced by `03_core_specifications/05_evidence_model/5_evidence_model.md` (Appendix D). The category and type lists below are copied from that document's Sections 5.1–5.2; the document itself remains the source of truth if they ever diverge.

## Notes

This document is intentionally written in English so that Codex and other coding agents can use it as an implementation source. `AI_SUMMARY_EVIDENCE` and any AI-derived evidence type are support-only per the Evidence Model and `08_policy_governance_model` — they must never be the sole basis for high-risk approval or emergency execution.

## Evidence Category

SENSOR_RAW
SENSOR_DERIVED
ROBOT_TELEMETRY
WORKER_LOCATION
EQUIPMENT_TELEMETRY
EXTERNAL_SYSTEM_FEEDBACK
HUMAN_REPORT
DOCUMENT_VERIFIED
DOCUMENT_EXTRACTED
PERMIT_RECORD
INSPECTION_RECORD
SYSTEM_LOG
POLICY_DECISION
ONTOLOGY_BINDING
ONTOLOGY_INFERENCE
DERIVED_AI
AUDIT_RECORD
THIRD_PARTY_API

## Core Evidence Types

SENSOR_OBSERVATION_EVIDENCE
ROBOT_TELEMETRY_EVIDENCE
WORKER_LOCATION_EVIDENCE
EQUIPMENT_TELEMETRY_EVIDENCE
EXTERNAL_FEEDBACK_EVIDENCE
HUMAN_CONFIRMATION_EVIDENCE
DOCUMENT_EVIDENCE
PERMIT_EVIDENCE
INSPECTION_EVIDENCE
SYSTEM_LOG_EVIDENCE
AUDIT_RECORD_EVIDENCE
POLICY_DECISION_EVIDENCE
ONTOLOGY_BINDING_EVIDENCE
INFERENCE_EVIDENCE
AI_SUMMARY_EVIDENCE
DOCUMENT_EXTRACTED_EVIDENCE
THIRD_PARTY_API_EVIDENCE

## Full Catalog Categories (Beyond Initial Scope)

The following category catalogs are expected to grow beyond the type list above, per `05_evidence_model` Section 24. They are listed here as placeholders only; adding concrete evidence catalog entries requires registry governance (see `06_registry_specs/evidence_registry/evidence_registry.md`), not ad hoc addition:

sensor evidence catalog (beyond initial scope)
robot telemetry evidence catalog (beyond initial scope)
worker location evidence catalog (beyond initial scope)
device health evidence catalog
external feedback evidence catalog (beyond initial scope)
human confirmation evidence catalog
document evidence catalog
permit evidence catalog
inspection evidence catalog
policy evidence catalog
AI-derived evidence catalog
privacy lifecycle evidence catalog
