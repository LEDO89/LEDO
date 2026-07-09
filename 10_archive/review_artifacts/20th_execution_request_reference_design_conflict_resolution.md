# 20th ExecutionRequest Reference-Design Conflict Resolution

> Historical Review Artifact
>
> This document records a code and documentation correctness fix result.
> It is not an architecture source-of-truth document.
> If this document conflicts with AGENTS.md or 00_master_architecture/, AGENTS.md and 00_master_architecture/ take precedence.

## 1. Final Status

PATCH APPLIED

## 2. Scope

While continuing the user's directive to check for remaining architecture-vs-code problems, a genuine unresolved conflict was found between two `03_core_specifications/` documents describing the same DTO differently — not a naming nit like the 19th patch, but two different structural designs:

- `01_common_schema_dto/1_common_schema_dto.md` Section 17.3 ("Fields:") lists `ExecutionRequestDTO` as carrying policy/context data directly: `execution_request_id`, `approved_action_ref`, `action_type`, `target_ref`, `external_system_type`, `external_system_id`, `execution_constraints`, `expected_feedback`, `timeout_policy`, `retry_policy`, `recovery_policy`, `idempotency_key`, `execution_lease`, `trace_context`, `created_at_utc`. This matched the existing code in `src/ledo_ontology_core/framework/schemas/execution.py` exactly.
- `09_execution_adapter_model/9_execution_adapter_model.md` Section 7.2 stated "ExecutionRequest should be designed around references rather than directly carrying all fields" and listed a structurally different field set: `approved_action_ref`, `safety_gate_result_ref`, `execution_context_snapshot_ref`, `action_type`, `target_entity_refs`, `execution_mode`, `required_adapter_type`, `required_capability`, `idempotency_key`, `trace_id`, `decision_trace_id`.

`AGENTS.md`'s domain-specific priority rule groups both documents under the same bucket ("Lifecycle and DTO contracts: `03_core_specifications/`") with no finer ordering between individual documents within that folder, so this could not be resolved by rule alone. It was presented to the user via `AskUserQuestion`; the user selected keeping `1_common_schema_dto.md` Section 17.3 as the standard, then separately confirmed via direct instruction ("agent.md에 따라 2번을 기준으로 다 수정해" — per agent.md, fix everything based on option 2) to propagate that resolution throughout.

## 3. Modified Files

- `03_core_specifications/01_common_schema_dto/1_common_schema_dto.md`
- `03_core_specifications/09_execution_adapter_model/9_execution_adapter_model.md`

## 4. Created Files

- `10_archive/review_artifacts/20th_execution_request_reference_design_conflict_resolution.md`

## 5. Resolution Detail

`9_execution_adapter_model.md` Section 7.2's field list was replaced with `1_common_schema_dto.md` Section 17.3's exact field list, plus a "Canonical Reference" note stating Section 17.3 is the field-level contract and that this document's field list has been rewritten to match it — mirroring the established `DispatchStatus` Canonical Reference note pattern used in this document (Section 20/1008) for a prior conflict of the same kind.

Section 7.3 (`ExecutionContextSnapshot`)'s rationale was previously written as directly conditional on the now-rejected reference-based design ("If ExecutionRequestDTO directly carries too many fields... should be separated into ExecutionContextSnapshot"). This was rewritten to state plainly that `ExecutionContextSnapshot` is not part of `ExecutionRequestDTO`'s current canonical shape, and remains a documented option for a possible future audit/context-separation extension (consistent with `07_implementation_plan/implementation_slice_3/implementation_slice_3_plan.md`, which already names `ExecutionContextSnapshotDTO` as a Slice 3 build target, not a Step 1 target) — not deleted, since it may still be legitimate future-extension content, just not the currently implemented design.

Section 33.1's `target_entity_ref` / `target_entity_refs` mentions (internally inconsistent with each other in singular/plural form, and inconsistent with the chosen canonical `target_ref` field name) were normalized to `target_ref`.

`1_common_schema_dto.md` Section 17.3 gained a matching "Canonical Reference" note documenting the resolution, so a future reader hitting either document finds a consistent, cross-linked explanation rather than a silent one-way fix.

## 6. Deliberately Not Changed

- `10_audit_observability_model/10_audit_observability_model.md`'s `decision_trace_id` mentions (Sections describing `decision_trace_id` as a general trace-linking concept spanning the whole audit trail) were checked and left unchanged — this is a distinct, legitimate cross-cutting observability concept, not a competing claim about `ExecutionRequestDTO`'s own field shape.
- `07_implementation_plan/implementation_slice_3/implementation_slice_3_plan.md`'s reference to `ExecutionContextSnapshotDTO` as a Slice 3 build target was checked and left unchanged — it is consistent with, not contradictory to, the Section 7.3 rewrite above.

## 7. Verification Summary

This was a documentation-only fix; no `src/` or `tests/` files were touched (the code already matched Section 17.3). `.venv/bin/python -m pytest tests/unit/ -q` — 76 passed, 0 failed (re-run to confirm no incidental impact).

## 8. Recommended Next Step

No further architecture-vs-code or intra-document design conflicts are currently known. Continue Step 1 code review per the existing Codex-writes / Claude-reviews workflow, or continue the broader remaining-gap sweep if the user wants further module-by-module cross-checks (e.g., `ApprovedActionDTO`, `AuditRecordDTO`, `FeedbackEventDTO` against their respective module docs, which have not yet received this level of scrutiny).

## 9. Modification Confirmation

All files listed in Section 3 were intentionally modified as part of this patch, following the user's explicit decision (via `AskUserQuestion` and a direct follow-up instruction) to resolve the `ExecutionRequestDTO` design conflict in favor of `1_common_schema_dto.md` Section 17.3. No other files were modified.
