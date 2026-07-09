# 28th Architecture MD Governance Alignment

> Historical Review Artifact
>
> This document records a documentation governance and architecture consistency fix result.
> It is not an architecture source-of-truth document.
> If this document conflicts with AGENTS.md or 00_master_architecture/, AGENTS.md and 00_master_architecture/ take precedence.

## 1. Final Status

PATCH APPLIED

## 2. Scope

The user requested a direct review of all active architecture markdown documents using `AGENTS.md` as the governing instruction set. The review read the master architecture documents first, then checked active documents under `01_layer_architecture/`, `02_layer_stack_mapping/`, `03_core_specifications/`, `04_ontology_foundation/`, `05_domain_ontology_modules/`, `06_registry_specs/`, `07_implementation_plan/`, `08_runtime_validation/`, and `09_appendices/`.

The patch corrected source-of-truth ordering, placeholder registry status, appendix authority language, runtime validation safety wording, and stale Runtime Validation references.

## 3. Modified Architecture / Specification Files

- `01_layer_architecture/implementation_guide.md`
- `02_layer_stack_mapping/implementation_guide.md`
- `02_layer_stack_mapping/07_distributed_domain_agent_stack_mapping.md`
- `02_layer_stack_mapping/08_decision_router_escalation_stack_mapping.md`
- `02_layer_stack_mapping/09_approved_action_safety_gate_stack_mapping.md`
- `03_core_specifications/00_canonical_object_lifecycle/0_canonical_object_lifecycle.md`
- `03_core_specifications/01_common_schema_dto/1_common_schema_dto.md`
- `03_core_specifications/04_state_model_registry/4_state_model_registry.md`
- `03_core_specifications/05_evidence_model/5_evidence_model.md`
- `03_core_specifications/README.md`
- `04_ontology_foundation/00_ontology_foundation_report.md`
- `04_ontology_foundation/04_reasoning_and_constraint_model.md`
- `04_ontology_foundation/06_ontology_governance_and_versioning.md`
- `05_domain_ontology_modules/*/*_ontology.md`
- `05_domain_ontology_modules/*/implementation_guide.md`
- `06_registry_specs/*/*.md`
- `08_runtime_validation/network_health/network_health.md`
- `09_appendices/README.md`
- `09_appendices/appendix_a_stack_catalog/stack_catalog.md`
- `09_appendices/appendix_b_event_catalog/event_catalog.md`
- `09_appendices/appendix_c_state_catalog/state_catalog.md`
- `09_appendices/appendix_d_evidence_catalog/evidence_catalog.md`
- `09_appendices/appendix_e_ontology_module_catalog/ontology_module_catalog.md`
- `09_appendices/appendix_f_decision_approval_catalog/decision_approval_catalog.md`

## 4. Created Files

- `10_archive/review_artifacts/28th_architecture_md_governance_alignment.md`

## 5. Finding 1: Placeholder Registry Entries Marked Active

Several registry documents explicitly labeled example entries as non-normative placeholders while their YAML-like example blocks still used `status: active`. This conflicted with `AGENTS.md`, which requires missing registry content to use `status: draft` and never `active`.

Fixed by changing all registry example `status: active` occurrences under `06_registry_specs/*/*.md` to `status: draft`, including deferred `agent_vocabulary_registry` and `model_adapter_registry` examples so their presence cannot be mistaken for implementation approval.

## 6. Finding 2: Implementation Guides Outranked Module Specs

`implementation_guide.md` files in `01_layer_architecture/`, `02_layer_stack_mapping/`, and `05_domain_ontology_modules/*/` listed themselves above the module specification markdown file in their local Source of Truth sections.

Fixed by placing the module specification markdown file above the implementation guide, matching `AGENTS.md`'s rule that implementation guides are orientation documents and must not outrank factual specification files.

## 7. Finding 3: Appendices Presented as Source-of-Truth or Implementation Sources

Several `09_appendices/` documents described themselves as implementation sources or said their copied lists remained the source of truth if they diverged. `AGENTS.md` defines appendices as non-authoritative convenience indexes.

Fixed by rewriting appendix language to say these documents are non-authoritative indexes. If an appendix diverges from a governing specification or registry, the governing document wins.

## 8. Finding 4: Core Specs Delegated Governed Values to Appendices

`03_core_specifications/04_state_model_registry/4_state_model_registry.md` and `03_core_specifications/05_evidence_model/5_evidence_model.md` said the full lists of state/evidence values were managed in Appendices C/D.

Fixed by clarifying that appendices summarize initial reference lists only, while governed runtime state/evidence values and registry entries are controlled by `06_registry_specs/state_registry/state_registry.md` and `06_registry_specs/evidence_registry/evidence_registry.md`.

## 9. Finding 5: Network Health Wording Implied Safety

`08_runtime_validation/network_health/network_health.md` stated `network reachable -> safe to execute`, immediately followed by the correct principle that reachability does not mean execution is safe.

Fixed by changing the first phrase to `network reachable -> eligible as one validation input`, preserving Network Health as only one Runtime Validation input and not a Safety Gate pass.

## 10. Finding 6: Stale Runtime Validation Paths

`04_ontology_foundation/04_reasoning_and_constraint_model.md` referenced `06_runtime_validation/` and `safety_gate_validation_rules.md`. `04_ontology_foundation/06_ontology_governance_and_versioning.md` also referenced `safety_gate_validation_rules.md`.

Fixed by pointing these references to `08_runtime_validation/safety_gate/safety_gate.md`.

## 11. Finding 7: Domain Ontology Placeholder Wording

The lightweight domain ontology placeholder documents said they could be used as implementation sources. To avoid implying permission to invent domain meaning, their note was changed to say they are scaffolding sources only and do not authorize invented domain meaning.

## 12. Additional Partial Review Corrections

After the user requested correction of the documents reviewed so far in the renewed direct-read pass, the following additional issues were corrected within the already-reviewed scope:

- `02_layer_stack_mapping/07_distributed_domain_agent_stack_mapping.md`: removed wording that made Safety Gate appear to determine whether candidate actions become ApprovedAction records.
- `02_layer_stack_mapping/08_decision_router_escalation_stack_mapping.md`: replaced legacy "approved cyber-physical command lifecycle" wording with the explicit ApprovedAction -> RuntimeValidationResult -> SafetyGatePass -> ExecutionRequest boundary.
- `02_layer_stack_mapping/09_approved_action_safety_gate_stack_mapping.md`: clarified that missing approval blocks ApprovedAction creation through governance, while hard interlocks block SafetyGatePass and ExecutionRequest readiness.
- `03_core_specifications/00_canonical_object_lifecycle/0_canonical_object_lifecycle.md`: separated ActionCandidate routing/approval from Runtime Validation and Safety Gate execution-readiness validation.
- `03_core_specifications/01_common_schema_dto/1_common_schema_dto.md`: changed `ApprovedActionDTO` ownership from Safety Gate to the approval or governance workflow after a valid ApprovalDecision.
- `03_core_specifications/04_state_model_registry/4_state_model_registry.md`: changed the preemptive authority example so it creates a governed state assertion or restriction request rather than silently forcing state truth.
- `03_core_specifications/05_evidence_model/5_evidence_model.md`: changed a concrete freshness example to a domain-defined freshness window and marked the block as non-normative.
- `03_core_specifications/README.md`: clarified that it is an index, not a field-level implementation source.
- `04_ontology_foundation/00_ontology_foundation_report.md`: reconciled the old single `ot:` namespace strategy with the module-specific namespace strategy governed by the Ontology Module Boundary specification, and softened execution wording to execution readiness and requests.

This section records only the partial pass over documents that had already been directly read again. It does not claim completion of the renewed 00-09 full reread.

## 13. Deliberately Not Changed

The separate schema-code hygiene change that standardized `DOMAIN_DECISION_REQUIRED` comments remains in the working tree but is not the main subject of this architecture markdown governance artifact.

## 14. Verification Summary

Static checks were run for the corrected conflict patterns:

- no remaining `status: active` under `06_registry_specs`
- no remaining appendix `source of truth` wording from the reviewed patterns
- no remaining stale `06_runtime_validation` / `safety_gate_validation_rules` references in active architecture docs
- implementation guides no longer list themselves above module specs

Additional static checks after the partial review corrections found no remaining matches for the corrected Safety Gate / ApprovedAction ownership patterns, stale `within 5 seconds` evidence example, duplicated namespace sentence, or Core Specs README implementation-source wording.

Previous test verification:

`pytest` — 104 passed, 0 failed.

## 15. Modification Confirmation

The files listed in Section 3 were intentionally modified as part of this patch, per the user's explicit instruction to fix all reviewed architecture markdown issues. This archive artifact was created afterward to preserve the review and patch history.
