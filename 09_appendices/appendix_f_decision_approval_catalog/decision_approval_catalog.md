---
title: Decision Approval Catalog
version: 1.1
status: populated
owner: platform-ontology
language: en
last_updated: 2026-07-06
---

# Decision Approval Catalog

## Purpose

Catalog reference items and examples. Do not treat this appendix as executable runtime code.

This is the Decision / Approval Matrix Catalog referenced by `03_core_specifications/07_decision_approval_matrix/07_decision_approval_matrix.md` (Appendix F). The enum values below are copied from that document's Sections 8–10; the document itself remains the source of truth if they ever diverge.

## Notes

This document is intentionally written in English so that Codex and other coding agents can use it as an implementation source.

## Decision Route Values

AUTO_ALLOW
AUTO_DENY
NOTIFICATION_ONLY
SUPERVISOR_APPROVAL_REQUIRED
SAFETY_MANAGER_APPROVAL_REQUIRED
WAR_ROOM_APPROVAL_REQUIRED
EXPERT_REVIEW_REQUIRED
POLICY_EXCEPTION_REVIEW
EMERGENCY_FAST_PATH
FAIL_SAFE_REQUIRED
MANUAL_OVERRIDE_REQUIRED
MAPPING_REVIEW_REQUIRED
EVIDENCE_REVIEW_REQUIRED
RECONCILIATION_REQUIRED
NETWORK_HEALTH_REVIEW_REQUIRED
TOCTOU_REVALIDATION_REQUIRED
AUDIT_ONLY

## Risk Level

INFO — general information, automatic handling, or log recording
NOTICE — operator notification required
WARNING — supervisor review may be required
HIGH_RISK — safety manager or supervisor approval required
CRITICAL_EMERGENCY — emergency fast-path or fail-safe required
EXCEPTIONAL — expert review, war room, or policy exception review required

## Approval Level

NO_APPROVAL — automatic handling allowed
OPERATOR_ACK — operator acknowledgment required
SUPERVISOR_APPROVAL
SAFETY_MANAGER_APPROVAL
WAR_ROOM_APPROVAL
EXPERT_REVIEW
POLICY_OWNER_APPROVAL
EMERGENCY_POLICY_BYPASS
POST_HOC_AUDIT_ONLY

Note: `06_registry_specs/action_registry` and `03_core_specifications/03_action_type_registry` use a shorter Approval Level subset (`NO_APPROVAL`, `SUPERVISOR_APPROVAL`, `SAFETY_MANAGER_APPROVAL`, `WAR_ROOM_APPROVAL`, `EXPERT_REVIEW`, `EMERGENCY_POLICY_BYPASS`). This Decision / Approval Matrix list is the more complete superset (it additionally defines `OPERATOR_ACK` and `POLICY_OWNER_APPROVAL` and `POST_HOC_AUDIT_ONLY`); treat this appendix's list as canonical when the two differ, since `07_decision_approval_matrix` is the document of record for approval-level semantics.

## Full Catalog Categories (Beyond Initial Scope)

The following category catalogs are expected to grow beyond the enum lists above, per `07_decision_approval_matrix` Section 2.2. They are listed here as placeholders only; adding concrete matrix entries requires registry/policy governance (see `06_registry_specs/decision_registry/` and `06_registry_specs/approval_registry/`), not ad hoc addition:

safety decision matrix
robot decision matrix
construction task decision matrix
industrial alarm decision matrix
evidence conflict decision matrix
approval role matrix
emergency decision matrix
policy exception matrix
mapping review matrix
audit escalation matrix
