# 17th Safety Gate / Validator DTO Shape Correction

> Historical Review Artifact
>
> This document records a code and documentation correctness fix result.
> It is not an architecture source-of-truth document.
> If this document conflicts with AGENTS.md or 00_master_architecture/, AGENTS.md and 00_master_architecture/ take precedence.

## 1. Final Status

PATCH APPLIED

## 2. Scope

The 15th patch enum-ified `ValidatorResultDTO.result` and `SafetyGatePassDTO.status` but only corrected their value types, not their field shape. A direct re-read of `08_runtime_validation/safety_gate/safety_gate.md` Sections 8, 10, and 23, and `08_runtime_validation/validators/validators.md` Section 7, found that `ValidatorResultDTO`, `SafetyGatePassDTO`, and `SafetyGateBlockDTO` were missing multiple canonical fields entirely (not just wrong enum values), and that `SafetyGateResultDTO` — a distinct aggregate contract named in Section 23 — did not exist in code at all. Per explicit user instruction ("아키텍처 md가 기준이야. 코드를 수정해" — the architecture md is the standard, fix the code), this patch brings the DTO shapes into exact field-for-field alignment with the canonical contracts, including field names, not only value types.

## 3. Modified Files

- `03_core_specifications/01_common_schema_dto/1_common_schema_dto.md`
- `src/ledo_ontology_core/framework/schemas/__init__.py`
- `src/ledo_ontology_core/framework/schemas/emergency.py`
- `src/ledo_ontology_core/framework/schemas/enums.py`
- `src/ledo_ontology_core/framework/schemas/runtime_validation.py`
- `src/ledo_ontology_core/framework/schemas/safety_gate.py`
- `tests/unit/framework/test_emergency_dto.py`
- `tests/unit/framework/test_runtime_validation_dto.py`
- `tests/unit/framework/test_safety_gate_dto.py`

## 4. Created Files

- `10_archive/review_artifacts/17th_safety_gate_validator_dto_shape_correction.md`

## 5. New Enums

Four enums were added to `enums.py`:

- `Severity` (INFO, WARNING, ERROR, CRITICAL) — `validators.md` Section 7.
- `CriticalityTier` (TIER_1_SAFETY_CRITICAL, TIER_2_OPERATIONAL_CRITICAL, TIER_3_INFORMATIONAL) — `safety_gate.md` Section 14 ("Criticality Tier Handling"), cross-confirmed by `toctou.md` Section 16. Neither source document gives a short-form value string; these values encode the section heading text directly (e.g. "Tier 1. Safety-Critical") rather than inventing new terminology.
- `SafetyGateResultStatus` (PASS, BLOCK, MANUAL_REVIEW_REQUIRED, HOLD, REQUIRES_REVALIDATION, REQUIRES_REAPPROVAL) — `safety_gate.md` Section 23. This is a distinct, smaller (6-member) list from `ValidatorStatus` (9 members); the source document gives it as its own "Possible status" list, not a cross-reference to Section 7.
- `BlockReason` (17 members: `MISSING_REQUIRED_VALIDATION`, `INVALID_RUNTIME_VALIDATION_RESULT`, `STALE_STATE`, `STALE_SNAPSHOT`, `TOCTOU_CONFLICT`, `CRITICAL_CONDITION_CHANGED`, `INVALID_APPROVAL`, `EXPIRED_APPROVAL`, `POLICY_FAILED`, `EXTERNAL_SYSTEM_UNREACHABLE`, `ADAPTER_UNHEALTHY`, `FEEDBACK_CHANNEL_UNAVAILABLE`, `IDEMPOTENCY_FAILURE`, `TERMINAL_SAFETY_GATE_PASS_REPLAY`, `SHACL_VALIDATION_FAILED`, `CLOCK_SKEW_EXCEEDED`, `UNKNOWN_REQUIRED_CONDITION`) — `safety_gate.md` Section 10's "Possible block reasons" list.

## 6. ValidatorResultDTO Shape Correction

Renamed `id` → `result_id`, `result` → `status` (matching `validators.md` Section 7's field names exactly), and added the previously-missing fields: `validator_version`, `action_type`, `severity` (`Severity`), `tier` (`CriticalityTier`), `input_refs`, `warning_reasons`, `suggested_next_state`, `safety_gate_eligible`, `correlation_id`. All 7 specialized subclasses (`TOCTOUResultDTO`, `SHACLValidationResultDTO`, `NetworkHealthResultDTO`, `IdempotencyResultDTO`, `ApprovalValidityResultDTO`, `PolicyRevalidationResultDTO`, `EvidenceValidityResultDTO`) inherit the corrected shape automatically. `RuntimeValidationResultDTO` and `RuntimeValidationInputDTO` were left unchanged — no separate canonical field-level contract exists for them in `08_runtime_validation/`, only their `result` value type was canonical-sourced in the 15th patch.

## 7. SafetyGatePassDTO Shape Correction

Renamed `id` → `safety_gate_pass_id`, `status` → `terminal_status`, `runtime_validation_result_id` → `runtime_validation_result_ref` (matching `safety_gate.md` Section 8 exactly), and added: `lease_duration_ms`, `lease_started_monotonic_ms`, `lease_expires_monotonic_ms`, `target_external_system`, `execution_request_scope`, `safety_snapshot_ref`. `audit_ref` was removed — it does not appear in the canonical field list. This closes a real gap: the DTO previously could not represent the lease duration at all, which is the entire point of a SafetyGatePass being "a short-lived execution-readiness lease" (`safety_gate.md` Section 9).

## 8. SafetyGateBlockDTO Shape Correction

Renamed `id` → `safety_gate_block_id`, `checked_at` → `blocked_at`, `failure_reasons` → `block_reasons` (typed `list[BlockReason]`), removed the unconfirmed `status` field (the canonical `SafetyGateBlock` field list never included one — see the 15th patch's note), and added: `failed_validator_refs`, `failed_runtime_validation_ref`, `safety_snapshot_ref`, `severity` (`Severity`), `tier` (`CriticalityTier`), `suggested_next_state`, `manual_review_required`. This closes another real gap: the DTO previously could not represent criticality tier at all, despite `safety_gate.md` Section 14 explicitly requiring Tier 1/2/3 handling to differ (Tier 1 always blocks; Tier 2/3 may hold, retry, or warn).

## 9. SafetyGateResultDTO (New)

Added per `safety_gate.md` Section 23 ("SafetyGateResult Contract"), previously undefined in code: `result_id`, `approved_action_id`, `action_type`, `status` (`SafetyGateResultStatus`), `issued_pass_ref`, `block_ref`, `checked_at`, `runtime_validation_result_ref`, `safety_snapshot_ref`, `validator_summary_ref`, `decision_reasons`, `failure_reasons`, `warning_reasons`, `suggested_next_state`, `trace_id`, `correlation_id`, `audit_ref`.

## 10. Emergency Mirror Updates

`EmergencySafetyGatePassDTO` and `EmergencySafetyGateBlockDTO` in `schemas/emergency.py` were updated to mirror the corrected standard shapes exactly (substituting `emergency_approved_action_id` / `emergency_runtime_validation_result_ref` for the standard `approved_action_id` / `runtime_validation_result_ref`), consistent with the 15th patch's rationale that the Emergency-prefixed DTOs have no separate field-level spec of their own and are modeled as structural mirrors of their standard counterparts.

## 11. Remaining Known Gap (Not Fixed By This Patch)

`SafetyGateInputDTO` was not reconciled against `safety_gate.md` Section 6's fuller input list (`ValidatorResultSummary`, `TOCTOUResult`, `SHACLValidationResult`, `NetworkHealthResult`, `IdempotencyResult`, `ApprovalValidityResult`, `PolicyRevalidationResult`, `EvidenceValidityResult`, `CapabilityAvailabilityResult`). This is a known, explicitly-flagged remaining gap, not treated as resolved by this patch.

## 12. Verification Summary

`.venv/bin/python -m pytest tests/unit/framework/ -q` — 76 passed, 0 failed (up from 75 after the 16th patch; one net-new test added for `SafetyGateResultDTO`, several existing tests rewritten for the new field shapes).

## 13. Recommended Next Step

Continue Step 1 code review per the existing Codex-writes / Claude-reviews workflow, or address the `SafetyGateInputDTO` gap noted in Section 11 if the user wants it closed next. No further code or documentation changes are recommended from this patch's scope until the next explicit instruction.

## 14. Modification Confirmation

All files listed in Section 3 were intentionally modified as part of this patch, following explicit user instruction to treat `08_runtime_validation/safety_gate/safety_gate.md` and `08_runtime_validation/validators/validators.md` as the standard and correct the code to match, including field names and previously-missing fields. No other files were modified.
