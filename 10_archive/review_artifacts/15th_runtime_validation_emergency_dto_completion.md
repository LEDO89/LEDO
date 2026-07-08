# 15th Runtime Validation / Emergency DTO Completion

> Historical Review Artifact
>
> This document records a code and documentation correctness fix result.
> It is not an architecture source-of-truth document.
> If this document conflicts with AGENTS.md or 00_master_architecture/, AGENTS.md and 00_master_architecture/ take precedence.

## 1. Final Status

PATCH APPLIED

## 2. Scope

Direct follow-up to `14th_policy_risk_approval_enum_canonicalization.md`. That patch left five open items from the full-repository read; this patch resolves four of them and formally closes the fifth as "not a bug."

## 3. Modified Files

- `06_registry_specs/action_registry/action_registry.md`
- `06_registry_specs/approval_registry/approval_registry.md`
- `src/ledo_ontology_core/framework/schemas/__init__.py`
- `src/ledo_ontology_core/framework/schemas/emergency.py`
- `src/ledo_ontology_core/framework/schemas/enums.py`
- `src/ledo_ontology_core/framework/schemas/runtime_validation.py`
- `src/ledo_ontology_core/framework/schemas/safety_gate.py`
- `tests/unit/framework/test_emergency_dto.py`
- `tests/unit/framework/test_runtime_validation_dto.py`
- `tests/unit/framework/test_safety_gate_dto.py`

## 4. Created Files

- `10_archive/review_artifacts/15th_runtime_validation_emergency_dto_completion.md`

## 5. Item 1 — DecisionTier vs RiskLevel: Resolved As Not A Bug

A direct re-read of `0_canonical_object_lifecycle.md` Section 4.8 found that `decision_tier` (`ROUTINE`/`NOTICE`/`WARNING`/`HIGH_RISK`/`CRITICAL_EMERGENCY`/`EXCEPTIONAL`) is a `DecisionCase`-specific classification field defined by that document, while `risk_level` (`INFO`/`NOTICE`/`WARNING`/`HIGH_RISK`/`CRITICAL_EMERGENCY`/`EXCEPTIONAL`) is defined by `07_decision_approval_matrix.md` Section 8 and applies to multiple other DTOs (`ActionCandidateDTO`, `ApprovedActionDTO`, `CapabilitySpecDTO`, `ActionTypeSpecDTO`). The two enums share 5 of 6 members but are sourced from different documents, under different names, applied to different fields — including both appearing as separate fields on the same `DecisionCaseDTO`. This is a near-duplicate value set, not a contradiction, and was left unchanged. No code was modified for this item.

## 6. Item 2 — RuntimeValidation / SafetyGate Status Fields: Enum-ified Where Confirmed

Two new enums were added to `enums.py`:

- `ValidatorStatus` (9 members: `PASS`, `FAIL`, `WARNING`, `HOLD`, `RETRY`, `REQUIRES_REVALIDATION`, `REQUIRES_REAPPROVAL`, `MANUAL_REVIEW_REQUIRED`, `BLOCK`), sourced from `08_runtime_validation/validators/validators.md` Section 7 ("Validator Output Contract"). Applied to `ValidatorResultDTO.result` (and its 7 subclasses via inheritance) and `RuntimeValidationResultDTO.result`.
- `SafetyGatePassTerminalStatus` (7 members: `ISSUED`, `DISPATCHING`, `CONSUMED_ACCEPTED`, `CONSUMED_REJECTED`, `CONSUMED_DROPPED`, `EXPIRED`, `REVOKED`), sourced from `08_runtime_validation/toctou/toctou.md` Section 21, cross-confirmed by `08_runtime_validation/idempotency/idempotency_control.md` Section 9. Applied to `SafetyGatePassDTO.status`, which corresponds to the canonical `terminal_status` field named in `safety_gate.md` Section 8 (field name was not renamed — only the value set was fixed, see Section 8 below).

`SafetyGateBlockDTO.status` and `SafetySnapshotDTO.status` were deliberately left as plain `str`. `safety_gate.md` Section 10's canonical `SafetyGateBlock` field list does not include a `status` field at all, and no closed value list for a `SafetySnapshot` status field was found anywhere in `08_runtime_validation/`. Inventing values for either would violate the no-domain-guessing rule.

## 7. Item 3 — Missing Emergency-Prefixed DTOs: Added

Five new DTOs were added to `schemas/emergency.py` (the file the lifecycle doc's own Section 12 "Recommended Code Mapping" designates for all emergency-path schema content):

- `EmergencyRuntimeValidationInputDTO`
- `EmergencyRuntimeValidationResultDTO` (uses `ValidatorStatus`)
- `EmergencySafetyGatePassDTO` (uses `SafetyGatePassTerminalStatus`)
- `EmergencySafetyGateBlockDTO`
- `EmergencyExecutionRequestDTO` (enforces via `model_validator` that `execution_lease` carries an `emergency_safety_gate_pass_id`, mirroring `ExecutionRequestDTO`'s existing `safety_gate_pass_id` requirement, per `07_decision_approval_matrix.md`'s explicit rule: "EmergencyExecutionRequest MUST NOT be created unless an EmergencySafetyGatePass has been issued from a valid EmergencyRuntimeValidationResult.")

These object names are required by the emergency lifecycle described in `0_canonical_object_lifecycle.md` Section 4.11, `07_decision_approval_matrix.md` (Sections 4, 18, 33), and `08_policy_governance_model.md` Section 16, but none of those documents give a dedicated field-level schema for the Emergency-prefixed variants — they only appear as flow-step object names. Each new DTO is therefore modeled as a structural mirror of its standard (non-emergency) counterpart, substituting `emergency_approved_action_id`/`_ref` for `approved_action_id`/`_ref`. This applies an existing, already-approved shape to a required object name; it does not invent new domain content.

## 8. Item 4 — ApprovalAuthority Wiring: Confirmed As Correctly Unwired

`1_common_schema_dto.md` Section 16.4's `ApprovalRequestDTO` field list (`approval_request_id`, `decision_case_ref`, `action_type`, `target_ref`, `required_role`, `required_clearance`, `approver_ref`, `approval_status`, `approval_reason`, `expires_at_utc`, `created_at_utc`, `approved_at_utc`, `trace_context`) has no approval-level or approval-authority field. The current code already matches this list exactly. Adding a field to force `ApprovalAuthority` into use would be new schema content beyond what `1_common_schema_dto.md` specifies, not a value-list correction — so no field was added. `enums.py`'s `ApprovalAuthority` docstring was updated to record this finding and note that the enum's more likely eventual home is `06_registry_specs/approval_registry`'s `required_approval_level`, once that registry is implemented.

## 9. Item 5 — Non-Canonical Registry Illustrative Lists: Cross-Referenced

Non-normative callout notes (matching the pattern already used in `1_common_schema_dto.md` Section 8.1 and the pre-existing `action_registry.md` Section 11 "Non-normative placeholder" notes) were added directly above the illustrative lists in:

- `06_registry_specs/approval_registry/approval_registry.md` Section 8 ("Approval Level Model") — points to the canonical `ApprovalAuthority` set in `08_policy_governance_model.md` Section 13.
- `06_registry_specs/action_registry/action_registry.md` Section 9 ("Risk and Criticality Model") — points to the canonical `RiskLevel` set in `07_decision_approval_matrix.md` Section 8, and separately notes `criticality` remains an open question not addressed by this patch.

`03_core_specifications/03_action_type_registry/03_action_type_registry.md` Sections 7.2–7.3 were checked and found to already match the canonical `RiskLevel` and a correct subset of `ApprovalAuthority` exactly — no change was needed there. This confirms `appendix_f_decision_approval_catalog.md`'s existing note that `03_action_type_registry.md` uses a legitimate subset, not a conflicting list.

## 10. Verification Summary

`.venv/bin/python -m pytest tests/unit/framework/ -v` — 75 passed, 0 failed (up from 70 after the 14th patch).

New tests added: `ValidatorStatus` invalid-value rejection and exact-membership (9 members); `SafetyGatePassTerminalStatus` invalid-value rejection and exact-membership (7 members); construction and validation tests for all 5 new Emergency-prefixed DTOs, including the `EmergencyExecutionRequestDTO` lease-requirement enforcement test.

## 11. Remaining Open Items

- `DecisionTier` vs `RiskLevel` near-duplicate value sets remain as two intentionally separate enums (see Section 5) — no further action planned unless a future review finds a document that explicitly equates them.
- `SafetyGateBlockDTO.status` and `SafetySnapshotDTO.status` remain unconfirmed `str` fields (see Section 6).
- `criticality` (on `ActionTypeSpecDTO`/registry docs) has no confirmed canonical source and remains open.
- `06_registry_specs/README.md` mojibake remains unresolved (carried over from the 12th cleanup, not addressed here).

## 12. Recommended Next Step

Continue Step 1 code review per the existing Codex-writes / Claude-reviews workflow. No further code changes are recommended from this patch's scope until the next explicit instruction.

## 13. Modification Confirmation

All files listed in Section 3 were intentionally modified as part of this patch, following direct confirmation against `0_canonical_object_lifecycle.md`, `07_decision_approval_matrix.md`, `08_policy_governance_model.md`, and `08_runtime_validation/`. No other files were modified.
