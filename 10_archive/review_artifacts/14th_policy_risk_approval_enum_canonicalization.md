# 14th Policy / Risk / Approval Enum Canonicalization

> Historical Review Artifact
>
> This document records a code and documentation correctness fix result.
> It is not an architecture source-of-truth document.
> If this document conflicts with AGENTS.md or 00_master_architecture/, AGENTS.md and 00_master_architecture/ take precedence.

## 1. Final Status

PATCH APPLIED

## 2. Scope

This patch followed a full direct re-read of all 131 markdown files in the repository (00_master_architecture through 10_archive) to find cross-document field-value inconsistencies before further Step 1 code generation continued. The read surfaced three closed-value-set fields whose canonical source had been misidentified or left unresolved in `src/ledo_ontology_core/framework/schemas/`:

- `PolicyDecisionResult` — the existing 5-member enum was built from the illustrative list in `03_core_specifications/01_common_schema_dto/1_common_schema_dto.md` Section 19.7 instead of the actual canonical 8-member list in `03_core_specifications/08_policy_governance_model/08_policy_governance_model.md` Section 7.
- `risk_level` — previously left as plain `str` with a `DOMAIN_DECISION_REQUIRED` marker on the assumption that no closed value list existed anywhere in the specs. A direct read of `03_core_specifications/07_decision_approval_matrix/07_decision_approval_matrix.md` Section 8 found a 6-member canonical list, independently cross-confirmed by matching usage in `08_policy_governance_model.md` Sections 16.2 and 22.
- Approval level / authority — no enum existed in code at all. `08_policy_governance_model.md` Section 13 ("Approval Authority Model") defines a 9-member canonical list, independently cross-confirmed by `09_appendices/appendix_f_decision_approval_catalog/decision_approval_catalog.md`'s "Approval Level" list (itself sourced from `07_decision_approval_matrix.md`). Two lower-tier documents — `06_registry_specs/approval_registry/approval_registry.md` Section 8 and `06_registry_specs/action_registry/action_registry.md` / `03_core_specifications/03_action_type_registry/03_action_type_registry.md` — define different, non-matching illustrative sets and are not canonical for this field.

This patch does not address every finding from the full-repository read (e.g. `06_registry_specs/README.md` residual mojibake, the `DecisionTier` / `RiskLevel` naming proximity). Those remain open and are not in scope here.

## 3. Modified Files

- `03_core_specifications/01_common_schema_dto/1_common_schema_dto.md`
- `src/ledo_ontology_core/framework/schemas/enums.py`
- `src/ledo_ontology_core/framework/schemas/__init__.py`
- `src/ledo_ontology_core/framework/schemas/action.py`
- `src/ledo_ontology_core/framework/schemas/decision.py`
- `src/ledo_ontology_core/framework/schemas/execution.py`
- `src/ledo_ontology_core/framework/schemas/governance.py`
- `src/ledo_ontology_core/framework/schemas/registry.py`
- `tests/unit/framework/test_enums.py`
- `tests/unit/framework/test_initial_dto_contracts.py`
- `tests/unit/framework/test_registry_governance_observability_dto.py`

## 4. Created Files

- `10_archive/review_artifacts/14th_policy_risk_approval_enum_canonicalization.md`

## 5. Resolution Detail

`PolicyDecisionResult` was rebuilt to the canonical 8 members: `ALLOW`, `DENY`, `REQUIRE_APPROVAL`, `REQUIRE_EVIDENCE`, `REQUIRE_REVALIDATION`, `REQUIRE_FAIL_SAFE`, `REQUIRE_MANUAL_OVERRIDE`, `REQUIRE_POLICY_EXCEPTION_REVIEW`. The previous `ESCALATE` and `EMERGENCY_ALLOW` members do not exist in the canonical source and were removed.

A new `RiskLevel` enum was added with the canonical 6 members: `INFO`, `NOTICE`, `WARNING`, `HIGH_RISK`, `CRITICAL_EMERGENCY`, `EXCEPTIONAL`. It replaces plain `str` on every `risk_level` / `default_risk_level` field that previously carried a `DOMAIN_DECISION_REQUIRED` marker: `ActionCandidateDTO.risk_level`, `DecisionCaseDTO.risk_level`, `ApprovedActionDTO.risk_level`, `CapabilitySpecDTO.risk_level`, `ActionTypeSpecDTO.default_risk_level`.

A new `ApprovalAuthority` enum was added with the canonical 9 members: `NO_APPROVAL`, `OPERATOR_ACK`, `SUPERVISOR_APPROVAL`, `SAFETY_MANAGER_APPROVAL`, `WAR_ROOM_APPROVAL`, `EXPERT_REVIEW`, `POLICY_OWNER_APPROVAL`, `EMERGENCY_POLICY_BYPASS`, `POST_HOC_AUDIT_ONLY`. It is not yet wired to a DTO field, because no current DTO (`ApprovalRequestDTO`, `ApprovalDecisionDTO`) has an approval-level field to attach it to; it is available in `enums.py` for when that field is added.

`1_common_schema_dto.md` Section 8.1 was updated to list the two new enums and to explicitly document, for `PolicyDecisionResult`, `RiskLevel`, and `ApprovalAuthority`, which document each is actually sourced from (following the existing `DispatchStatus` pattern) instead of this document's own shorter illustrative lists. Section 8.2's "Genuinely undecided fields" paragraph was corrected to remove `risk_level`, since it is no longer undecided, with a note explaining the correction.

## 6. Fields Intentionally Left Unchanged

- `urgency`, `confidence_level`, `source_type` — still no closed value list found anywhere in the specs; remain `str` with `DOMAIN_DECISION_REQUIRED` markers, per `1_common_schema_dto.md` Section 8.2.
- `action_type`, `event_type`, `entity_type`, `state_type`, `evidence_type` — registry-managed vocabulary by design, not a code-level enum question.
- `DecisionTier` (`ROUTINE`/`NOTICE`/`WARNING`/`HIGH_RISK`/`CRITICAL_EMERGENCY`/`EXCEPTIONAL`, sourced from the canonical object lifecycle document) was left as-is. It is close to but not identical to the new `RiskLevel` (`INFO` vs `ROUTINE` as the first member) and applies to a different field (`decision_tier`, not `risk_level`). Whether these two enums should eventually be unified is an open question, not resolved by this patch.

## 7. Verification Summary

`.venv/bin/python -m pytest tests/unit/framework/ -v` — 66 passed, 0 failed.

New tests added: exact-membership assertions for `RiskLevel` (6), `PolicyDecisionResult` (8), and `ApprovalAuthority` (9); invalid-value rejection tests for `DecisionCaseDTO.risk_level`, `ApprovedActionDTO.risk_level`, and `PolicyRefDTO.decision_result`.

## 8. Remaining Open Items From the Full-Repository Read

- `06_registry_specs/README.md` retains unresolved Korean-text mojibake (deferred since the 12th cleanup).
- `06_registry_specs/approval_registry/approval_registry.md` Section 8 and `06_registry_specs/action_registry/action_registry.md` / `03_core_specifications/03_action_type_registry/03_action_type_registry.md` still contain illustrative risk-level and approval-level value lists that do not match the now-confirmed canonical sets. These are illustrative Pydantic-model sections in registry documents, not field-level contract text, so they do not block code correctness, but a future documentation pass should align or cross-reference them the same way `1_common_schema_dto.md` Section 8.1 now does.
- `DecisionTier` vs `RiskLevel` naming/value proximity noted above remains open.

## 9. Recommended Next Step

Continue Step 1 code review per the existing Codex-writes / Claude-reviews workflow. No further code changes are recommended from this patch's scope until the next explicit instruction.

## 10. Modification Confirmation

All files listed in Section 3 were intentionally modified as part of this patch, following direct confirmation of canonical values against `07_decision_approval_matrix.md` and `08_policy_governance_model.md`. No other files were modified, and no registry or domain-module markdown files were changed in this patch.
