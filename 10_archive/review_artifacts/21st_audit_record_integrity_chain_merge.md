# 21st AuditRecordDTO Integrity Chain and Trust-Field Merge

> Historical Review Artifact
>
> This document records a code and documentation correctness fix result.
> It is not an architecture source-of-truth document.
> If this document conflicts with AGENTS.md or 00_master_architecture/, AGENTS.md and 00_master_architecture/ take precedence.

## 1. Final Status

PATCH APPLIED

## 2. Scope

Continuing the module-by-module DTO shape scan (following the 20th patch's `ExecutionRequestDTO` finding), `AuditRecordDTO` was found to have the same two-document design fork: `01_common_schema_dto/1_common_schema_dto.md` Section 18.5 (stage-reference design, matches existing code) versus `10_audit_observability_model/10_audit_observability_model.md` Section 9.1 (a reference-only redesign delegating stage context to a separate `AuditContextSnapshotDTO`). Unlike the `ExecutionRequestDTO` case, Section 9.1 also named genuinely new, non-redundant capability the existing shape lacked entirely: a tamper-evident hash chain and multi-causality trace correlation. Per explicit user instruction ("우선순위를 2번 common scheme dto로 진행하고 common scheme dto에 구조에 문제가 있으면 수정을 해. 그리고 audit_obsevaility_model도 수정하고. 이어서 코드도 수정하는 단계로." — keep `1_common_schema_dto.md` as priority baseline; if its structure has a real gap, fix it; fix `audit_observability_model.md` too; then fix the code), the missing capability was merged into Section 18.5 as additive, optional fields, `10_audit_observability_model.md` was rewritten to match, and the code/tests were updated.

## 3. Modified Files

- `03_core_specifications/01_common_schema_dto/1_common_schema_dto.md`
- `03_core_specifications/10_audit_observability_model/10_audit_observability_model.md`
- `src/ledo_ontology_core/framework/schemas/__init__.py`
- `src/ledo_ontology_core/framework/schemas/audit.py`
- `src/ledo_ontology_core/framework/schemas/enums.py`
- `tests/unit/framework/test_enums.py`
- `tests/unit/framework/test_registry_governance_observability_dto.py`

## 4. Created Files

- `10_archive/review_artifacts/21st_audit_record_integrity_chain_merge.md`

## 5. New Enums

- `TimeTrustLevel` (HIGH_TIME_TRUST, MEDIUM_TIME_TRUST, LOW_TIME_TRUST, UNTRUSTED_TIME, UNKNOWN_TIME_TRUST) — `05_evidence_model/5_evidence_model.md` Section 7.5, cross-confirmed by `10_audit_observability_model.md` Section 17 ("Evidence Audit must reference the following fields from the Evidence Model: ... time_trust_level ...").
- `ClockSyncStatus` (SYNCED, PARTIALLY_SYNCED, UNSYNCED, DRIFT_DETECTED, OFFLINE_ESTIMATED, UNKNOWN) — `05_evidence_model.md` Section 7.3, cross-confirmed the same way.

## 6. AuditRecordDTO Fields Added

`audit_event_type` (`str`, no closed value list found — Section 16.1 gives only a partial dispatch-stage mapping, so kept plain per the project's ambiguity-handling standard), `severity` (`Severity`, reused from the 17th patch), `audit_reason`, `occurred_at`, `time_trust_level` (`TimeTrustLevel`), `clock_sync_status` (`ClockSyncStatus`), `source_system_ref`, `correlation_id`, `decision_trace_id`, `primary_causality_id`, `causality_ids`, `integrity_policy_ref`, `content_hash`, `previous_record_hash`, `integrity_status` (`str`, no closed value list found anywhere). All added as optional/defaulted fields — this was an additive merge, not a breaking rename.

## 7. Fields From Section 9.1 Deliberately Not Added

`actor_ref`/`actor_role` (redundant with the existing plural `actor_refs`, which already supports multiple actors), `result_status` (redundant with the existing `final_status`), `action_type`/`target_entity_refs` (already reachable via the existing stage refs — `candidate_ref`, `approved_action_ref`, etc.), `audit_context_snapshot_ref` and `decision_trace_ref` (both assume the rejected reference-delegation design; `decision_trace_id` — a plain correlation string, not a reference to the not-yet-built `DecisionTraceDTO` object — was kept since it is a distinct, simple, valuable concept per Section 8.3).

## 8. Documentation Resolution

`10_audit_observability_model.md` Section 9.1's field list was directly replaced with `1_common_schema_dto.md` Section 18.5's field list (not left in place with a superseding footnote), matching the direct-rewrite precedent established in the 16th and 20th patches. Section 9.2 (`AuditContextSnapshotDTO`)'s rationale, which was written as conditional on the now-rejected delegation design, was corrected the same way Section 7.3 (`ExecutionContextSnapshot`) was corrected in the 20th patch: noted as a documented option for a possible future extension (`AuditContextSnapshotDTO` is a Rollout Stage 1 item per Section 29.1, not a current Step 1 target), not the current implemented design. `1_common_schema_dto.md` Section 18.5 gained a matching Canonical Reference note.

## 9. New Finding, Not Yet Investigated

While checking whether `time_trust_level`/`clock_sync_status` already existed elsewhere in code (they did not), `EvidenceDTO` (`schemas/evidence.py`) was noticed to not obviously carry the full field set `05_evidence_model.md` describes for evidence trust/freshness tracking (`source_trust_level`, `time_trust_level`, `clock_sync_status`, `clock_drift_estimate_ms`, `device_health_snapshot_ref`, `freshness_status`, etc. — some of these may already be nested inside `SourceMetadataDTO`/`FreshnessDTO`, which were not opened during this pass). This was not investigated further and is flagged as the next candidate for the module-by-module DTO shape scan, not fixed in this patch.

## 10. Verification Summary

`.venv/bin/python -m pytest tests/unit/ -q` — 81 passed, 0 failed (76 before this patch, plus 3 new `AuditRecordDTO` construction/rejection tests and 2 new enum member-count tests).

## 11. Recommended Next Step

Continue the module-by-module DTO shape scan. `EvidenceDTO` (Section 9 above) is the next flagged candidate. `FeedbackEventDTO` and `WorldStateUpdateDTO` have not yet been checked against their respective module docs either.

## 12. Modification Confirmation

All files listed in Section 3 were intentionally modified as part of this patch, following the user's explicit instruction to keep `1_common_schema_dto.md` as the priority baseline, fix its structure where genuinely deficient, fix `10_audit_observability_model.md` to match, and then update the code. No other files were modified.
