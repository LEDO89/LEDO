# 24th FeedbackEventDTO and ExternalControlRequestDTO Merge

> Historical Review Artifact
>
> This document records a code and documentation correctness fix result.
> It is not an architecture source-of-truth document.
> If this document conflicts with AGENTS.md or 00_master_architecture/, AGENTS.md and 00_master_architecture/ take precedence.

## 1. Final Status

PATCH APPLIED

## 2. Scope

Continuing the Tier 1 backlog from the 22nd patch's parallel structure scan, `FeedbackEventDTO` and `ExternalControlRequestDTO` were each found to have the same two-document-fork pattern as `ExecutionRequestDTO` (20th patch) and `AuditRecordDTO` (21st patch): `1_common_schema_dto.md` describes a smaller field set matching the existing code exactly, while `9_execution_adapter_model.md` describes the same object, under the same name, with a larger field set. Per the established precedent and the user's standing instruction, `1_common_schema_dto.md`'s field-holding design was kept as the baseline, and the real, non-redundant fields from `9_execution_adapter_model.md` were merged in as additive fields; `9_execution_adapter_model.md` was then rewritten to match, with a Canonical Reference note.

## 3. Modified Files

- `03_core_specifications/01_common_schema_dto/1_common_schema_dto.md`
- `03_core_specifications/09_execution_adapter_model/9_execution_adapter_model.md`
- `src/ledo_ontology_core/framework/schemas/execution.py`
- `src/ledo_ontology_core/framework/schemas/feedback.py`
- `tests/unit/framework/test_registry_governance_observability_dto.py`

## 4. Created Files

- `10_archive/review_artifacts/24th_feedback_and_external_control_request_merge.md`

## 5. FeedbackEventDTO (Section 18.1 vs Section 17)

Section 18.1 (15 fields, matched code exactly) vs. Section 17 (21 fields, same name). Merged in as additive fields: `feedback_status`, `result_status` (both plain `str` — no closed value list found for either), `result_message`, `external_reference_id`, `actual_started_at`, `actual_completed_at`, `observed_state_refs`, `feedback_payload_ref`, `error_detail_ref`, `requires_reconciliation`, `requires_audit`, `decision_trace_id`. Section 17's `external_control_request_ref` and `external_system_id` were treated as the same concepts as the existing `external_request_ref` and `source_system` fields, not duplicated.

## 6. ExternalControlRequestDTO (Section 17.4 vs Section 16)

Section 17.4 (12 fields, matched code exactly) vs. Section 16 (28 fields, same name). Merged in as additive fields: `execution_context_snapshot_ref`, `adapter_type`, `adapter_mode`, `external_request_type`, `external_payload_ref`, `external_payload_hash`, `idempotency_expires_at`, `dispatch_context_ref`, `dispatch_attempt`, `dispatch_status` (typed `DispatchStatus`, the existing 20-member canonical enum), `ack_deadline`, `acceptance_deadline`, `feedback_deadline`, `adapter_local_received_at`, `adapter_local_accepted_at`, `clock_sync_status` (typed `ClockSyncStatus`), `clock_drift_estimate_ms`, `decision_trace_id`. Section 16's `sent_at`/`platform_sent_at` and `trace_id`/`correlation_id` were treated as the same concepts as the existing `sent_at_utc` and `trace_context` fields, not duplicated.

## 7. Documentation Resolution

Both `9_execution_adapter_model.md` Section 17 and Section 16 field lists were directly replaced with their canonical counterparts (not left in place with a superseding footnote), matching the direct-rewrite precedent established in the 16th/20th/21st patches. Both `1_common_schema_dto.md` sections gained matching Canonical Reference notes.

## 8. Verification Summary

`.venv/bin/python -m pytest tests/unit/ -q` — 94 passed, 0 failed (91 before this patch; 4 new tests added covering `FeedbackEventDTO` and `ExternalControlRequestDTO` construction with the new fields, plus a `dispatch_status` rejection test).

## 9. Recommended Next Step

Continue the Tier 1 backlog: `PolicyDecisionDTO`/`PolicyDecisionResponseDTO` (found during the 22nd patch's investigation — `08_policy_governance_model.md` Section 23 describes a 25-field `PolicyDecisionResponseDTO` vs. `1_common_schema_dto.md` Section 19.7's 8-field `PolicyDecisionDTO`), and the four underdeveloped Runtime Validation specialized result DTOs (`NetworkHealthResultDTO`, `TOCTOUResultDTO`, `SHACLValidationResultDTO`, `IdempotencyResultDTO`).

## 10. Modification Confirmation

All files listed in Section 3 were intentionally modified as part of this patch, following the user's explicit instruction to continue the Tier 1 backlog sequentially. No other files were modified.
