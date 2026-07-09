# 22nd Parallel Structure Scan — Tier 2 Quick Fixes

> Historical Review Artifact
>
> This document records a code and documentation correctness fix result.
> It is not an architecture source-of-truth document.
> If this document conflicts with AGENTS.md or 00_master_architecture/, AGENTS.md and 00_master_architecture/ take precedence.

## 1. Final Status

PATCH APPLIED

## 2. Scope

Per explicit user instruction ("dto만 보지말고 전체 구조를 보자. 병렬로 다른 작은 모델에게 검토시켜서 전체적으로 구조가 문제없는지 확인해" — don't just look at DTOs, look at the whole structure; use parallel smaller-model review agents to check the whole structure), 8 Haiku sub-agents were dispatched in parallel, each covering a distinct area of the repository (master architecture/layer docs, lifecycle+common schema DTO, event/action/state/evidence taxonomy, ontology/decision/policy docs, execution+audit re-verification, registry specs, runtime validation re-verification, appendices). Findings were consolidated, triaged into tiers by risk/effort, and the user chose to fix Tier 2 (small, self-contained, low-risk) findings first. This patch covers that Tier 2 pass.

## 3. Modified Files

- `03_core_specifications/01_common_schema_dto/1_common_schema_dto.md`
- `03_core_specifications/02_event_type_taxonomy/2_event_type_taxonomy.md`
- `06_registry_specs/action_registry/action_registry.md`
- `06_registry_specs/approval_registry/approval_registry.md`
- `06_registry_specs/decision_registry/decision_registry.md`
- `src/ledo_ontology_core/framework/schemas/enums.py`
- `src/ledo_ontology_core/framework/schemas/validation.py`
- `tests/unit/framework/test_enums.py`

## 4. Created Files

- `10_archive/review_artifacts/22nd_parallel_structure_scan_tier2_fixes.md`

## 5. Findings Investigated and Fixed

**`ValidationResultDTO.validation_status` was plain `str`.** `1_common_schema_dto.md` Section 5.2 explicitly states this field shares the `ValidationStatus` enum with `ConfidenceDTO.validation_status`, `EvidenceDTO.validation_status`, and `GenericPayloadDTO.validation_status` — the other three already used the enum; only `ValidationResultDTO` had been left as `str`. Fixed in `src/ledo_ontology_core/framework/schemas/validation.py`.

**`RiskLevel` enum docstring, and 9 other citations across the repo, cited the wrong section number.** `07_decision_approval_matrix.md` actually defines Risk Level in Section 9.1 ("Risk Level"), not Section 8 (Section 8 is "Core Decision Outputs" / "Decision Route Values"). Fixed the citation in `enums.py` and propagated the correction to every other place in the repo that cited "Section 8" for `RiskLevel`: `1_common_schema_dto.md` (6 occurrences), `action_registry.md`, `decision_registry.md`, `approval_registry.md`, and `tests/unit/framework/test_enums.py`'s comment.

**`2_event_type_taxonomy.md` Section 1 misnamed its own companion appendix.** Line 24 said "Appendix A: Event Type Catalog," but the actual companion document is `09_appendices/appendix_b_event_catalog/`, and the same source document's own Section 13 correctly says "Appendix B." Fixed the self-reference.

## 6. Finding Investigated and Determined to Be a False Positive

One sub-agent reported a self-contradiction in `08_policy_governance_model.md` between Section 7 (8-value `PolicyDecisionResult` list) and a claimed "Section 20.4 decision_result Values" (6-value list). Direct verification found no Section 20.4 exists in this document at all — Section 20 is "PolicyEngineAdapter" with no lettered subsections, and the only other `decision_result` mention is as one field name (not a value list) inside Section 23's `PolicyDecisionResponseDTO` field list. No fix was made; this was a sub-agent misread, not a real bug.

## 7. New Finding Surfaced During Investigation (Deferred to Tier 1)

While investigating the false positive above, `08_policy_governance_model.md` Section 23 ("PolicyDecisionResponseDTO") was found to describe a 25-field DTO under a different name than `1_common_schema_dto.md` Section 19.7's `PolicyDecisionDTO` (8 fields, matches current code exactly). This is the same two-document-fork pattern as `ExecutionRequestDTO`/`AuditRecordDTO`/`FeedbackEventDTO`/`ExternalControlRequestDTO`/`EvidenceDTO`. Not fixed in this patch — added to the Tier 1 backlog for sequential processing.

## 8. Verification Summary

`.venv/bin/python -m pytest tests/unit/ -q` — 81 passed, 0 failed (no test behavior changed; `ValidationResultDTO`'s existing test fixtures already used valid enum string values).

## 9. Recommended Next Step

Proceed to Tier 1 findings from the parallel structure scan, in order of confirmed severity: `EvidenceDTO` (largest — ~50+ fields missing relative to `05_evidence_model.md`'s `EvidenceRecordDTO`), `FeedbackEventDTO`, `ExternalControlRequestDTO`, `PolicyDecisionDTO`/`PolicyDecisionResponseDTO` (Section 7 above), and the four underdeveloped Runtime Validation specialized result DTOs (`NetworkHealthResultDTO`, `TOCTOUResultDTO`, `SHACLValidationResultDTO`, `IdempotencyResultDTO`).

## 10. Modification Confirmation

All files listed in Section 3 were intentionally modified as part of this patch, following the user's explicit instruction to fix Tier 2 (small, low-risk) findings from the parallel structure scan first. No other files were modified.
