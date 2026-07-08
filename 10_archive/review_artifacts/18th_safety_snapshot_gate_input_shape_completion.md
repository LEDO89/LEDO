# 18th SafetySnapshot / SafetyGateInput Shape Completion

> Historical Review Artifact
>
> This document records a code and documentation correctness fix result.
> It is not an architecture source-of-truth document.
> If this document conflicts with AGENTS.md or 00_master_architecture/, AGENTS.md and 00_master_architecture/ take precedence.

## 1. Final Status

PATCH APPLIED

## 2. Scope

The 17th patch explicitly flagged two remaining gaps: `SafetyGateInputDTO` not reconciled against `safety_gate.md` Section 6's fuller input list, and `SafetySnapshotDTO.status` left as an unconfirmed `str`. Per the user's explicit standing instruction ("나의 기준은 md 우선이야. 아키텍처 md가 맞지 않는다면 md를 우선순위 정해준 것에 따라서 전체 수정하고 이어서 세부내용들을 수정할것이야" — the architecture md is the standard; where docs conflict, resolve by AGENTS.md's priority order, fix the docs fully, then fix the details), this patch investigated both gaps directly against source documents and closed the `SafetyGateInputDTO` gap and the `SafetySnapshotDTO` field-shape gap (a larger issue than the `status` value-type question alone).

## 3. Modified Files

- `03_core_specifications/01_common_schema_dto/1_common_schema_dto.md`
- `src/ledo_ontology_core/framework/schemas/safety_gate.py`
- `tests/unit/framework/test_safety_gate_dto.py`

## 4. Created Files

- `10_archive/review_artifacts/18th_safety_snapshot_gate_input_shape_completion.md`

## 5. Investigation and Priority Resolution

`AGENTS.md` (lines 72-76) gives domain-specific priority among module-level spec folders: "Lifecycle and DTO contracts: `03_core_specifications/`... Validation and Safety Gate contracts: `08_runtime_validation/`." This means `1_common_schema_dto.md` is authoritative for DTO field lists, not `08_runtime_validation/`. However, `08_runtime_validation/shacl_shapes/shacl_shapes.md` Section 11.1 (`SafetySnapshotShape`) and `08_runtime_validation/validators/validators.md` Section 10.2 (`snapshot_freshness_validator`) both independently list fields (`snapshot_id`, `valid_until`, `source_state_versions`, `target_scope`, `site_ref`, `zone_ref`, `critical_state_refs`, `schema_version`) that `1_common_schema_dto.md`'s prior `SafetySnapshotDTO` field list did not contain at all. This is not a priority conflict to resolve by picking a winner — it is a completeness gap in the higher-priority document: the validation logic described in `08_runtime_validation/` cannot function unless the DTO it operates on actually carries the fields being validated. Both source documents independently and consistently use the same field names, giving strong cross-confirmation (the same standard applied to `CriticalityTier` in the 17th patch). `1_common_schema_dto.md` was therefore expanded, not overridden.

`validators.md` Section 10.2 also lists `action_scope` alongside `source_state_versions`; this was confirmed to refer to a different object's field (the action being checked, compared against the snapshot's own `target_scope` — see `shacl_shapes.md` line 331, "target_scope must match action_scope"), not a competing name for the snapshot's own scope field. No renaming conflict exists there.

## 6. SafetySnapshotDTO Shape Correction

Renamed `id` → `snapshot_id` and `expires_at` → `valid_until` (both cross-confirmed twice, in `shacl_shapes.md` and `validators.md`). Added: `source_state_versions` (`dict[str, str]`, inferred type — state identifier to version string, no explicit type given in source), `target_scope`, `site_ref`, `zone_ref`, `critical_state_refs` (`list[str]`), `schema_version`. `ontology_version`, `policy_version`, `registry_version`, `checksum`, `status`, `trace_id`, `audit_ref` were kept unchanged — these are already `1_common_schema_dto.md`'s own previously-declared canonical fields for this DTO and do not conflict with the `08_runtime_validation/` field lists (which only enumerate what those specific validators read, not the DTO's complete field set).

`status` remains plain `str`. No closed value list was found for this field in any document — the only nearby text (`safety_gate.md` lines 321/347: "SafetySnapshot is valid and fresh" / "stale SafetySnapshot") describes a validation condition in prose, not an enumerated set of status values. Per the project's own ambiguity-handling standard (`07_implementation_plan/pre_code_generation_build_plan.md` Section 4), enum membership is not invented without a source, so this is correctly left as `str`, not treated as a defect.

## 7. SafetyGateInputDTO Shape Correction

Expanded to `safety_gate.md` Section 6's full "Recommended inputs" list. Renamed own identifier `id` → `safety_gate_input_id` for consistency with the identifier-naming convention established across the DTO family in the 17th patch. Renamed `runtime_validation_result_id` → `runtime_validation_result_ref` and `safety_snapshot_id` → `safety_snapshot_ref` to match the `_ref` suffix convention used by every other cross-DTO reference field in this schema layer. Added one reference field per remaining named input type in Section 6: `validator_result_summary_ref`, `toctou_result_ref`, `shacl_validation_result_ref`, `network_health_result_ref`, `idempotency_result_ref`, `approval_validity_result_ref`, `policy_revalidation_result_ref`, `evidence_validity_result_ref`, `capability_availability_result_ref`.

Only `approved_action_id`, `action_type`, `runtime_validation_result_ref`, and `safety_snapshot_ref` are required fields. The remaining validator-category result refs are optional (`str | None = None`), because Section 6's own text ("For safety-critical actions, missing required input must result in block") implies non-safety-critical paths may legitimately lack some of these inputs — not every action type exercises every validator category. `input_refs: list[str]` is kept as a generic overflow field, matching the section's own "Recommended" (not strictly exhaustive) framing.

## 8. Investigated and Confirmed Not-a-Gap

Two other items on the previously-flagged remaining-gaps list were investigated and found to already be correctly resolved, not defects:

- **`urgency` / `criticality_hint`**: `urgency` is already explicitly marked `# DOMAIN_DECISION_REQUIRED` in `decision.py` and documented as "genuinely undecided" in `1_common_schema_dto.md` Section 8.2, per the project's own ambiguity-handling standard. `criticality_hint` (`event.py`) is a loosely-typed optional hint field, never claimed anywhere to require a closed enum. Neither is a bug.
- **`06_registry_specs/README.md` mojibake**: searched for replacement characters and common mojibake byte patterns; none found. Appears to have already been resolved by the 12th patch (`12th_encoding_mojibake_cleanup.md`). No action needed.

## 9. Remaining Known Item (Not Fixed, Low Priority)

Cosmetic registry entry IDs (e.g. `stop_work_safety_supervisor_v1`) remain unrenamed. This was previously assessed as a naming-style issue, not a correctness defect, and is intentionally left as-is unless the user requests it addressed.

## 10. Verification Summary

`.venv/bin/python -m pytest tests/unit/ -q` — 76 passed, 0 failed.

## 11. Recommended Next Step

No further architecture-vs-code gaps are currently known. Continue Step 1 code review per the existing Codex-writes / Claude-reviews workflow, or address Section 9's cosmetic item if the user wants it closed.

## 12. Modification Confirmation

All files listed in Section 3 were intentionally modified as part of this patch, following the user's explicit MD-first, priority-ordered-resolution instruction. No other files were modified.
