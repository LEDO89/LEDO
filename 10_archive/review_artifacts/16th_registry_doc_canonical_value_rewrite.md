# 16th Registry Document Canonical Value Rewrite

> Historical Review Artifact
>
> This document records a documentation correctness fix result.
> It is not an architecture source-of-truth document.
> If this document conflicts with AGENTS.md or 00_master_architecture/, AGENTS.md and 00_master_architecture/ take precedence.

## 1. Final Status

PATCH APPLIED

## 2. Scope

Direct follow-up to the 14th and 15th patches. Those patches added "non-normative, canonical source is elsewhere" callout notes above the wrong illustrative lists in `approval_registry.md` and `action_registry.md`, but left the wrong lists themselves in place. On review, this was judged to be the wrong shape of fix: a document carrying incorrect content plus a disclaimer is still a document a reader can misread, and the annotation pattern does not scale — every new correction adds another footnote instead of making the document simply correct. This patch replaces the annotation approach with direct correction: wrong values are rewritten to the canonical values in place, and values with no canonical equivalent are deleted rather than kept with a warning label.

A broader repository search (see Section 4) also found two previously-missed occurrences of the wrong lists: `decision_registry.md` Section 18 ("Risk Classification Rule"), and stale inline values in `1_common_schema_dto.md` Section 19.7 that the 14th patch's `enums.py` fix did not propagate back into the document itself.

## 3. Modified Files

- `03_core_specifications/01_common_schema_dto/1_common_schema_dto.md`
- `06_registry_specs/action_registry/action_registry.md`
- `06_registry_specs/approval_registry/approval_registry.md`
- `06_registry_specs/decision_registry/decision_registry.md`

## 4. Created Files

- `10_archive/review_artifacts/16th_registry_doc_canonical_value_rewrite.md`

## 5. Non-Canonical Value Disposition

Per explicit user decision, of `approval_registry.md` Section 8's 10 illustrative approval levels, the 5 with no canonical `ApprovalAuthority` equivalent were deleted rather than kept as a registry-specific extension:

- `auto_approval` — deleted. No canonical equivalent; conceptually redundant with `PolicyDecisionResult.ALLOW` gating straight to `NO_APPROVAL`.
- `site_manager_approval` — deleted.
- `compliance_officer_approval` — deleted.
- `robot_operations_approval` — deleted.
- `multi_party_approval` — deleted.

The remaining values were renamed to their canonical form (`none` → `NO_APPROVAL`, `operator_acknowledgement` → `OPERATOR_ACK`, `supervisor_approval` → `SUPERVISOR_APPROVAL`, `safety_supervisor_approval` → `SAFETY_MANAGER_APPROVAL`, `emergency_override_approval` → `EMERGENCY_POLICY_BYPASS`), and the 3 canonical values the registry document was missing entirely (`WAR_ROOM_APPROVAL`, `EXPERT_REVIEW`, `POLICY_OWNER_APPROVAL`, `POST_HOC_AUDIT_ONLY`) were added with descriptions grounded in `08_policy_governance_model.md` Sections 16 and 19.

`action_registry.md` and `decision_registry.md`'s `risk_class` lists (`routine`/`notice`/`warning`/`high_risk`/`critical`/`emergency`) map 1:1 in count to the canonical `RiskLevel` set but not in name for the last two members; they were replaced with `INFO`/`NOTICE`/`WARNING`/`HIGH_RISK`/`CRITICAL_EMERGENCY`/`EXCEPTIONAL` — no deletions were needed here since the count already matched.

## 6. approval_registry.md Changes

- Section 8 ("Approval Level Model") and its 9 subsections (8.1–8.9) rewritten to the canonical 9-value set with corrected names and descriptions; the old 10-value list and its 9 subsections were replaced, not annotated.
- Section 5.1/5.2 examples updated to canonical value names.
- Section 12/13 example registry entries (`STOP_WORK`, `DISPATCH_ROBOT`) updated: `applicable_risk_classes` and `required_approval_level` now use canonical `RiskLevel`/`ApprovalAuthority` values.
- The `ApprovalLevel` Python enum in the "Minimal Pydantic Model" section (Section 31) rewritten to the canonical 9 members.
- One ontology example (`ledo:hasApprovalLevel ledo:SafetySupervisorApproval`) updated to `ledo:SafetyManagerApproval`.
- Cosmetic identifiers (e.g. `canonical_name: stop_work_safety_supervisor_approval`, `approval_rule_id: approval:stop_work_safety_supervisor_v1`) were left unchanged — these are registry entry labels/IDs, not the approval-level value itself, and renaming them would cascade into cross-registry reference strings in other documents (e.g. `identity_registry.md`) for no correctness benefit.

## 7. action_registry.md Changes

- Section 9 ("Risk and Criticality Model") rewritten: the illustrative `risk_class` list replaced with the canonical `RiskLevel` set; the earlier non-normative callout note removed since the list itself is now correct. `criticality` explicitly kept as its own open, unconfirmed field, separate from this fix.
- Section 11/12 example registry entries (`DISPATCH_ROBOT`, `STOP_WORK`) updated: `risk_class` and `required_approval_level` now use canonical values.
- A `RiskLevel` and `ApprovalLevel` Python enum were added to the "Minimal Pydantic Model" section (previously `risk_class`/`required_approval_level` were untyped `str` even in the illustrative model, unlike `ActionCategory`/`Reversibility` in the same model), and `ActionRegistryEntry.risk_class`/`required_approval_level` retyped accordingly.

## 8. decision_registry.md Changes

- Section 18 ("Risk Classification Rule")'s `Recommended risk classes` list replaced with the canonical `RiskLevel` set.
- Section 12/13 example registry entries' `applicable_risk_classes` updated to canonical values.
- Section 20's escalation condition example (`risk_class >= critical`) updated to `risk_class >= CRITICAL_EMERGENCY`.
- A `RiskLevel` Python enum was added to the "Minimal Pydantic Model" section (this document already had `DecisionStatus`/`DecisionCategory`/`DecisionOutcome` as typed enums but left `applicable_risk_classes` as `list[str]`), and the field retyped to `list[RiskLevel]`.

## 9. 1_common_schema_dto.md Changes

- Section 19.7 (`PolicyDecisionDTO`) still carried the old, wrong 5-member `PolicyDecisionResult` list inline (`ALLOW`, `DENY`, `REQUIRE_APPROVAL`, `ESCALATE`, `EMERGENCY_ALLOW`) even after the 14th patch corrected `enums.py` itself — the 14th patch's Section 8.1/8.2 edits were a summary elsewhere in the document, not a fix to this section. Corrected in place to the canonical 8 members.
- Sections 16.2 (`ActionCandidateDTO`), 16.3 (`DecisionCaseDTO`), 17.1 (`ApprovedActionDTO`), 19.1 (`ActionTypeSpecDTO`), and 19.5 (`CapabilitySpecDTO`) each received a one-line note stating that their `risk_level`/`default_risk_level` field uses `RiskLevel`, matching the existing per-section documentation pattern already used for `decision_tier` and `PolicyDecisionResult`.
- Section 17.3A gained equivalent notes for `ValidatorStatus`, `SafetyGatePassTerminalStatus`, the unresolved `SafetySnapshotDTO.status`/`SafetyGateBlockDTO.status` fields, and a pointer to the Emergency-prefixed DTO mirrors added to `schemas/emergency.py` in the 15th patch.

## 10. Verification Summary

`.venv/bin/python -m pytest tests/unit/framework/ -q` — 75 passed, 0 failed (docs-only changes; no Python code was touched in this patch).

A repository-wide search for every deleted/renamed value string (`auto_approval`, `site_manager_approval`, `compliance_officer_approval`, `robot_operations_approval`, `multi_party_approval`, and lowercase `risk_class`/`risk_level` values) across all active `.md` files, excluding `10_archive/review_artifacts/`, confirmed zero remaining occurrences.

## 11. Remaining Open Items

- Cosmetic registry entry IDs referencing the old `safety_supervisor` naming (e.g. `approval:stop_work_safety_supervisor_v1`) were intentionally left unchanged (see Section 6) — not a correctness issue, just a naming legacy.
- `criticality` (action/decision registries) and `urgency` (`DecisionCaseDTO`) remain open, unconfirmed fields — unrelated to this patch's scope.
- `06_registry_specs/README.md` mojibake remains unresolved (carried over from the 12th cleanup).

## 12. Recommended Next Step

Continue Step 1 code review per the existing Codex-writes / Claude-reviews workflow. No further code or documentation changes are recommended from this patch's scope until the next explicit instruction.

## 13. Modification Confirmation

All files listed in Section 3 were intentionally modified as part of this patch, following explicit user direction to replace non-canonical illustrative content in place rather than annotate around it, and explicit user confirmation to delete (not retain as an extension) the 5 approval-level values with no canonical equivalent. No other files were modified.
