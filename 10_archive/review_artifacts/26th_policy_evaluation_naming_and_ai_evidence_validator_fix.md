# 26th PolicyEvaluationDTO Naming Fix and AI-Evidence Validator Correction

> Historical Review Artifact
>
> This document records a code and documentation correctness fix result.
> It is not an architecture source-of-truth document.
> If this document conflicts with AGENTS.md or 00_master_architecture/, AGENTS.md and 00_master_architecture/ take precedence.

## 1. Final Status

PATCH APPLIED

## 2. Scope

This patch closes the two remaining open items noted at the end of the 25th patch: the `PolicyEvaluationDTO` naming question, and the `reject_ai_as_evidence` validator tension flagged (but deliberately not resolved) in the 23rd patch.

## 3. Modified Files

- `03_core_specifications/01_common_schema_dto/1_common_schema_dto.md`
- `src/ledo_ontology_core/framework/schemas/evidence.py`
- `tests/unit/framework/test_initial_dto_contracts.py`

## 4. Created Files

- `10_archive/review_artifacts/26th_policy_evaluation_naming_and_ai_evidence_validator_fix.md`

## 5. PolicyEvaluationDTO — Investigated and Resolved as a Naming Typo

`PolicyEvaluationDTO` appeared only once in the entire repository, inside `1_common_schema_dto.md`'s own final DTO-flow summary diagram (near line 2301), where every other entry in the list carries the literal `DTO`-suffixed class name (`RawInputDTO`, `ActionCandidateDTO`, etc.). No `PolicyEvaluationDTO` class, field list, or "Fields:" section exists anywhere — `PolicyDecisionDTO` (Section 19.7) is the actual, fully-specified, code-implemented class occupying this exact lifecycle position (between `DecisionCaseDTO` and `ApprovalRequestDTO`). `0_canonical_object_lifecycle.md`'s own flow lists use the bare concept name `PolicyEvaluation` (no `DTO` suffix, consistent with that document's own convention of using concept names, not class names, throughout its flow diagrams) — that usage was left unchanged, since it is not inconsistent with its own document's style. Only `1_common_schema_dto.md`'s DTO-suffixed flow diagram was corrected: `PolicyEvaluationDTO` → `PolicyDecisionDTO`.

## 6. `reject_ai_as_evidence` — Resolved

The 23rd patch flagged, but did not resolve, a tension between `05_evidence_model.md` Section 6.1 (which explicitly permits `AI_DERIVED`/`ATTESTED_AI_DERIVED` as legitimate `source_trust_level` values for an Evidence record) and `EvidenceDTO.reject_ai_as_evidence`, which rejected any evidence whose `source_metadata.source_type` was `"ai"`/`"llm"`/`"slm"` outright — a blanket rejection based on a fuzzy, still-undecided (`DOMAIN_DECISION_REQUIRED`) string field, stricter than the source document's actual rule.

Re-reading Section 4.5 ("Prohibited LLM roles: Create Primary Evidence") alongside Section 10 (the attestation/trust-upgrade process) and Section 10.6's worked example (which ends with `source_trust_level = ATTESTED_AI_DERIVED` as a legitimate, terminal state for an Evidence record derived from AI extraction) makes the intended rule clear: raw, unattested AI output must not become Evidence, but AI-derived data that has gone through the Section 10 attestation pipeline legitimately can.

The validator was renamed `reject_unattested_ai_as_evidence` and rewritten to check `source_metadata.source_trust_level == SourceTrustLevel.AI_DERIVED` specifically (rejecting only the raw, unattested case), rather than pattern-matching the fuzzy `source_type` string. `ATTESTED_AI_DERIVED` and every other `SourceTrustLevel` value now construct successfully.

## 7. Test Changes

`tests/unit/framework/test_initial_dto_contracts.py`: the `source()` fixture helper gained an optional `source_trust_level` parameter (previously hardcoded to `"TRUSTED_SYSTEM"`, which could never have triggered the old string-based rejection realistically). `test_evidence_rejects_ai_output_as_evidence` was renamed `test_evidence_rejects_unattested_ai_derived_source_trust_level` and now sets `source_trust_level="AI_DERIVED"` explicitly. A new test, `test_evidence_accepts_attested_ai_derived_source_trust_level`, confirms `ATTESTED_AI_DERIVED` evidence now constructs successfully, mirroring Section 10.6's worked example.

## 8. Verification Summary

`.venv/bin/python -m pytest tests/unit/ -q` — 104 passed, 0 failed (103 before this patch; 1 net-new test).

## 9. Recommended Next Step

Both items previously flagged as open are now closed. Continue scanning currently-unreviewed areas of the repository (`04_ontology_foundation/`, `05_domain_ontology_modules/`) if the user wants the structure sweep to continue, or return to normal Step 1 code review per the established Codex-writes / Claude-reviews workflow.

## 10. Modification Confirmation

All files listed in Section 3 were intentionally modified as part of this patch, per the user's explicit instruction to continue fixing. No other files were modified.
