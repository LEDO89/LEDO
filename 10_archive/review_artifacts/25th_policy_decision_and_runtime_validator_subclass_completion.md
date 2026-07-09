# 25th PolicyDecisionDTO and Runtime Validator Subclass Completion

> Historical Review Artifact
>
> This document records a code and documentation correctness fix result.
> It is not an architecture source-of-truth document.
> If this document conflicts with AGENTS.md or 00_master_architecture/, AGENTS.md and 00_master_architecture/ take precedence.

## 1. Final Status

PATCH APPLIED

## 2. Scope

This patch completes the entire Tier 1 backlog identified by the 22nd patch's 8-way parallel structure scan: `PolicyDecisionDTO`/`PolicyDecisionResponseDTO` (a two-document-fork found while investigating a false positive during the 22nd patch), and the four Runtime Validation specialized result DTOs (`NetworkHealthResultDTO`, `TOCTOUResultDTO`, `SHACLValidationResultDTO`, `IdempotencyResultDTO`) that a sub-agent found were "severely underdeveloped" relative to their own dedicated contract sections.

## 3. Modified Files

- `03_core_specifications/01_common_schema_dto/1_common_schema_dto.md`
- `03_core_specifications/08_policy_governance_model/08_policy_governance_model.md`
- `08_runtime_validation/idempotency/idempotency_control.md`
- `08_runtime_validation/network_health/network_health.md`
- `08_runtime_validation/shacl_shapes/shacl_shapes.md`
- `08_runtime_validation/toctou/toctou.md`
- `src/ledo_ontology_core/framework/schemas/__init__.py`
- `src/ledo_ontology_core/framework/schemas/decision.py`
- `src/ledo_ontology_core/framework/schemas/enums.py`
- `src/ledo_ontology_core/framework/schemas/runtime_validation.py`
- `tests/unit/framework/test_registry_governance_observability_dto.py`
- `tests/unit/framework/test_runtime_validation_dto.py`

## 4. Created Files

- `10_archive/review_artifacts/25th_policy_decision_and_runtime_validator_subclass_completion.md`

## 5. PolicyDecisionDTO (Section 19.7 vs Section 23)

Section 19.7 (8 fields, matched code exactly) vs. Section 23's `PolicyDecisionResponseDTO` (27 fields, different name). Merged in as additive fields: `policy_engine`, `policy_engine_version`, `policy_bundle_version`, `input_context_hash`, `policy_context_ref`, `resolution_context_ref`, `audit_context_ref`, `required_approval_level` (typed `ApprovalAuthority` — its first DTO field application; the enum's docstring, previously noting it was unwired, was updated), `matched_policy_refs`, `denied_policy_refs`, `resolved_policy_refs`, `suppressed_policy_refs`, `policy_resolution_ref`, `required_evidence_types`, `required_roles`, `required_clearance`, `requires_safety_gate`, `requires_post_hoc_audit`, `requires_revalidation`, `requires_fail_safe`, `trace_id`, `correlation_id`, `decision_trace_id`. Section 23's `decision_reason`/`created_at` were treated as the same concepts as the existing `reason`/`evaluated_at_utc` fields.

## 6. Runtime Validator Subclasses (New Enums)

Four new enums, each with a closed value list confirmed directly against source:

- `NetworkHealthStatus` (6 members) — `network_health.md` Section 7.
- `CircuitBreakerStatus` (3 members) — `network_health.md` Section 13.
- `SHACLValidationStatus` (5 members) — `shacl_shapes.md` Section 17.1.
- `IdempotencyLedgerStatus` (8 members) — `idempotency_control.md` Section 8.

## 7. Runtime Validator Subclasses (Field Additions)

- `TOCTOUResultDTO` (`toctou.md` Section 24): added `approval_snapshot_ref`, `execution_snapshot_ref`, `changed_fields`, `stale_fields`, `conflict_fields`, `block_reasons` (`list[BlockReason]`, reusing the 17th patch's enum), `required_reapproval`.
- `SHACLValidationResultDTO` (`shacl_shapes.md` Sections 17.1 and 20): added `shape_id`, `shape_version`, `target_node`, `target_type`, `validation_status` (`SHACLValidationStatus`), `violations`.
- `NetworkHealthResultDTO` (`network_health.md` Section 16): added `external_system_id`, `adapter_id`, `health_status` (`NetworkHealthStatus`), `heartbeat_status` (`str`, no closed list found), `latency_ms`, `error_rate`, `circuit_breaker_status` (`CircuitBreakerStatus`), `feedback_channel_status` (`str`, no closed list found).
- `IdempotencyResultDTO` (`idempotency_control.md` Sections 8 and 19): added `safety_gate_pass_id`, `execution_request_id`, `external_control_request_id`, `target_external_system`, `first_seen_at`, `last_seen_at`, `ledger_status` (`IdempotencyLedgerStatus`), `previous_result_ref`, `terminal_token_ref`, `terminal_token_status` (`str`, no closed list found).

`ApprovalValidityResultDTO`, `PolicyRevalidationResultDTO`, and `EvidenceValidityResultDTO` were checked and found to have no dedicated contract section of their own in `08_runtime_validation/` beyond the `ValidatorResultDTO` base pattern — left unchanged.

## 8. Documentation Resolution

`08_policy_governance_model.md` Section 23 and `1_common_schema_dto.md` Section 19.7 gained matching Canonical Reference notes (Section 23's field list was not altered, since it did not conflict with the merged Section 19.7 shape once the naming/concept overlaps were identified). The four `08_runtime_validation/` source documents each gained a one-line Canonical Reference note confirming their contract sections are now implemented in code, since their "Recommended fields" framing was not in conflict with the implementation — just previously unimplemented.

## 9. Verification Summary

`.venv/bin/python -m pytest tests/unit/ -q` — 103 passed, 0 failed (94 before this patch; 9 new tests covering `PolicyDecisionDTO`'s new fields and each runtime validator subclass's new fields and enum rejections).

## 10. Recommended Next Step

The Tier 1 backlog from the 22nd patch's parallel structure scan is now fully closed. Remaining lower-priority items not yet investigated: `EvidenceDTO`'s new `reject_ai_as_evidence` tension (flagged in the 23rd patch, not resolved), and `PolicyEvaluationDTO` (referenced in flow diagrams per the 22nd patch's findings but never formally defined — still unconfirmed whether this is a naming alias or a genuine gap).

## 11. Modification Confirmation

All files listed in Section 3 were intentionally modified as part of this patch, completing the Tier 1 backlog per the user's explicit instruction to proceed through it sequentially. No other files were modified.
