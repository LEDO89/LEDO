# 29th Step 2 (Canonical Lifecycle Boundary) Review and Fixes

> Historical Review Artifact
>
> This document records a code and documentation correctness fix result.
> It is not an architecture source-of-truth document.
> If this document conflicts with AGENTS.md or 00_master_architecture/, AGENTS.md and 00_master_architecture/ take precedence.

## 1. Final Status

PATCH APPLIED

## 2. Scope

Codex wrote Step 2 ("Canonical Lifecycle Flow and Boundary Rules" per `07_implementation_plan/pre_code_generation_build_plan.md`) — `src/ledo_ontology_core/framework/schemas/lifecycle_state.py`, `src/ledo_ontology_core/framework/validation/lifecycle.py`, `src/ledo_ontology_core/framework/validation/__init__.py`, and `tests/unit/framework/test_canonical_lifecycle_boundaries.py`. Per the established Codex-writes/Claude-reviews workflow, this patch records the review findings and the fixes applied per explicit user direction.

## 3. Modified Files

- `03_core_specifications/00_canonical_object_lifecycle/0_canonical_object_lifecycle.md`
- `src/ledo_ontology_core/framework/schemas/audit.py` (restored — see Section 7)
- `src/ledo_ontology_core/framework/schemas/context.py` (restored — see Section 7)
- `src/ledo_ontology_core/framework/schemas/lifecycle_state.py`
- `src/ledo_ontology_core/framework/validation/lifecycle.py`
- `tests/unit/framework/test_canonical_lifecycle_boundaries.py`

## 4. Created Files

- `10_archive/review_artifacts/29th_step2_lifecycle_boundary_review_and_fixes.md`

## 5. Review Findings and Fixes

**Finding 1 (confirmed bug, fixed).** `ALLOWED_AI_OUTPUT_TYPES` in `lifecycle.py` was missing `ValidationSuggestion`, one of the 9 explicitly-named "Allowed LLM roles" in `AGENTS.md`'s "LLM Boundary Rule" section (the highest-priority source document). This meant `validate_ai_boundary("ValidationSuggestion", produced_by_ai=True)` would have incorrectly raised `LifecycleBoundaryError` for a role the architecture explicitly permits. Fixed by adding `"ValidationSuggestion"` to the set.

**Finding 2 (confirmed duplication, fixed).** `lifecycle_state.py` defined a new `LifecyclePath` enum (`STANDARD`, `EMERGENCY_FAST_PATH`, `MONITORING_ONLY`) that duplicated the existing `PathType` enum (`schemas/enums.py`, sourced from `1_common_schema_dto.md` Section 12.3, built in Step 1) member-for-member. Fixed by removing `LifecyclePath` entirely and using `PathType` throughout `lifecycle_state.py`, `lifecycle.py`, and the test file (`LIFECYCLE_STAGE_ORDER` is now keyed by `PathType`; `validate_lifecycle_transition`'s `path` parameter and `_coerce_path` now type against `PathType`).

**Finding 3 (confirmed, fixed via doc edit not code comment).** `0_canonical_object_lifecycle.md` Section 10.1 ("Standard Path State Machine") and Section 10.2 ("Emergency Fast-Path State Machine") named a single collapsed stage, `SAFETY_VALIDATED`, positioned *before* `APPROVED_ACTION_CREATED` — architecturally backwards, since Runtime Validation operates on an already-created `ApprovedAction` per the same document's own Section 4.10. Codex's `LifecycleStage` enum instead used a 3-stage granular breakdown (`RUNTIME_VALIDATION_INPUT_CREATED` → `RUNTIME_VALIDATION_RESULT_CREATED` → `SAFETY_GATE_PASSED`, positioned *after* `APPROVED_ACTION_CREATED`), matching the document's own Section 1 Executive Summary flow and Section 4.10/4.11's plain-text rules, but silently deviating from the literal text of the cited Section 10.1/10.2 without disclosure. Per explicit user instruction ("우리의 원칙은 주석을 명시하는 것이 아니라 아키텍처 MD를 수정하는 것" — our principle is to fix the architecture MD directly, not add code comments), Section 10.1 and Section 10.2 were rewritten to match the code's (correct) ordering, with each gaining one line quoting the exact existing Section 4.10/4.11 text that justifies the ordering. `SAFETY_VALIDATED` no longer appears anywhere in the document (confirmed via repository-wide search — it was not referenced by any other document or code).

**Finding 4 (confirmed gap, fixed).** `FORBIDDEN_AI_OUTPUT_TYPES` did not cover 2 of `AGENTS.md`'s 10 "Forbidden LLM roles" phrases ("safety bypass decision", "physical control decision"). Low severity — `validate_ai_boundary`'s default-deny structure (anything not in `ALLOWED_AI_OUTPUT_TYPES` is rejected regardless) meant this was a rejection-message-quality gap, not a security gap. Fixed by adding `"SAFETY_BYPASS_DECISION"` and `"PHYSICAL_CONTROL_DECISION"` to the set.

## 6. Findings Confirmed Not to Be Bugs

`PLC_COMMAND`, `SCADA_COMMAND`, `MACHINE_SEQUENCE_INSTRUCTION` (forbidden-output constants) and the `_PHYSICAL_COMMAND_KEYS` dict-scanning heuristic were verified against `AGENTS.md`'s LLM Boundary Rule and `0_canonical_object_lifecycle.md` Section 4.13 ("ExecutionRequest must not contain direct robot motor commands, PLC ladder logic, or machine sequence instructions") — legitimately sourced, just drawn from multiple sections without a single consolidated citation. `MONITORING_ONLY_STAGES` and `FAILURE_STAGES` (the 20 `REJECTED_*`/`EXECUTION_*`/etc. members) were verified to match Section 10.3/10.4 exactly. All 7 required test scenarios from the build plan's Step 2 entry were confirmed present and passing. The "Do not create" boundary (no execution dispatch, approval service, Safety Gate service, physical command class, or conflicting new DTO fields) was honored.

## 7. Unrelated Regression Found and Restored

While running tests after the above fixes, `src/ledo_ontology_core/framework/schemas/audit.py` and `src/ledo_ontology_core/framework/schemas/context.py` were found reverted in the uncommitted working tree relative to the last commit (`8d8dac7`, already pushed to `origin/main`): `AuditRecordDTO` had lost ~15 fields added in the 21st patch (the tamper-evident hash chain and multi-causality trace correlation fields), and `SourceMetadataDTO.source_trust_level` had reverted from the `SourceTrustLevel` enum back to plain `str`. This was unrelated to Step 2's own scope (the build plan explicitly forbids Step 2 from touching DTO field definitions) and was confirmed, via `git show HEAD:...` vs. the on-disk file, to be an accidental side effect of applying Codex's own changes to the working tree — not something done by this review. Restored both files via `git checkout HEAD -- <path>`.

## 8. Verification Summary

`.venv/bin/python -m pytest tests/unit/ -q` — 112 passed, 0 failed throughout (before fixes, after fixes, and after the audit.py/context.py restoration).

## 9. Recommended Next Step

Advise the Codex-side workflow to always diff its working-tree changes against the current `origin/main` HEAD before applying a patch generated from an older base, to avoid silently reverting already-merged work. Continue with Step 3 (Ontology Module Boundary Scaffolding) per the build plan's dependency order, or address the smaller message-quality items in Section 5's Finding 4 if further precision is wanted later.

## 10. Modification Confirmation

All files listed in Section 3 were intentionally modified as part of this patch: 4 findings from the Step 2 code review were fixed per explicit user instruction, and the accidental `audit.py`/`context.py` regression was restored from the last commit. No other files were modified.
