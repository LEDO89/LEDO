---
title: Implementation Slice 2 Plan — Registries
version: 2.0
status: populated
owner: platform-ontology
language: en
last_updated: 2026-07-06
---

# Implementation Slice 2 Plan — Registries

## Purpose

Define the scope, implementation order, and acceptance criteria for the Registry slice: the full set of registries (excluding two explicitly out-of-scope registries, see below) needed before Runtime Validation and Safety Gate can be exercised.

This slice implements real registry contracts per `06_registry_specs/`. It is not a prototype set — each registry loader, validator, and entry schema is production code.

## Relationship to `implementation_plan.md`

This document groups `implementation_plan.md` Section 8, Phase 5 through Phase 14, minus two phases explicitly excluded from this implementation stage (see "Out of Scope" below). It assumes Implementation Slice 1 (Common Contract Foundation, Semantic Foundation, Registry Base, Action/Identity/Ontology Registry, Identity and Access Foundation) is complete.

`implementation_plan.md` Phase 5–14 lists:

- Phase 5: Event Registry Implementation
- Phase 6: State Registry Implementation
- Phase 7: Snapshot Schema Registry Implementation
- Phase 8: Evidence Registry Implementation
- Phase 9: Agent Vocabulary Registry Implementation — **out of scope for this implementation stage, see below**
- Phase 10: Model Adapter Registry Implementation — **out of scope for this implementation stage, see below**
- Phase 11: Decision Registry Implementation
- Phase 12: Policy Registry Implementation
- Phase 13: Approval Registry Implementation
- Phase 14: External System Registry Implementation

In addition to Phase 5–14, this slice includes `adapter_registry`, grouped here rather than in Implementation Slice 3, per `06_registry_specs/README.md` Section 6: `adapter_registry` and `external_system_registry` are categorized together as "Integration Registry" and the README states both should be prioritized together at the early stage, alongside Operational, Runtime, and Semantic/Identity Registries. `implementation_plan.md`'s Phase 5–14 list does not name `adapter_registry` as a separate phase; its registry contract is built here, while the executable `ExecutionAdapter` interface and its interface-stub implementations are built in Implementation Slice 3, where they are exercised at runtime.

## Out of Scope: Agent Vocabulary Registry and Model Adapter Registry

Per your explicit instruction, `agent_vocabulary_registry` and `model_adapter_registry` are excluded entirely from this implementation stage:

- No DTO, enum, loader, or test file is created for either registry.
- No skeleton or placeholder module is created for either registry.
- Where another registry's schema references an agent or model concept (see the Decision Registry note below), the reference is left as an untyped placeholder field with an explicit `TODO` comment, not a stub class or a resolved cross-reference.
- `06_registry_specs/README.md` Section 11's status note is updated separately (see the corresponding fix to that file) to reflect that both registries are fully deferred, not skeleton-first.

## Scope

Registries in this slice: `event_registry`, `state_registry`, `snapshot_schema_registry`, `evidence_registry`, `adapter_registry`, `external_system_registry`, `decision_registry`, `policy_registry`, `approval_registry`. Each follows the Registry Base pattern from Implementation Slice 1 and the entry-schema conventions in its corresponding `06_registry_specs/*/*.md` document.

Deliverables (see `implementation_plan.md` Section 8, Phase 5–14 for sequencing detail; field-level content comes from `06_registry_specs/*` directly):

- Event Registry: entries per `06_registry_specs/event_registry/event_registry.md`, using the reference fixtures listed in `09_appendices/appendix_b_event_catalog/event_catalog.md` (see "Reference Fixtures" below for their non-normative status).
- State Registry: entries per `06_registry_specs/state_registry/state_registry.md`, using the reference fixtures in `09_appendices/appendix_c_state_catalog/state_catalog.md`, including `temporal_grace_period` handling per `03_core_specifications/04_state_model_registry` Section 9.3 (not to be confused with the Policy Governance Model's unrelated `GracePeriodPolicyDTO`).
- Snapshot Schema Registry: schema and versioning for point-in-time snapshot objects referenced by the reference fixtures below.
- Evidence Registry: entries per `06_registry_specs/evidence_registry/evidence_registry.md`, using the reference fixtures in `09_appendices/appendix_d_evidence_catalog/evidence_catalog.md`, sufficient to construct an `EvidenceBundle`.
- Adapter Registry: entries per `06_registry_specs/adapter_registry/adapter_registry.md` — registry contract only in this slice (adapter type, protocol, mode, capability declaration); the executable `ExecutionAdapter` interface is built in Implementation Slice 3.
- External System Registry: entries per `06_registry_specs/external_system_registry/external_system_registry.md`.
- Decision Registry: entries per `06_registry_specs/decision_registry/decision_registry.md`. Where an entry's `applicable_agent_type_refs` field would normally resolve against the (out-of-scope) Agent Vocabulary Registry, leave it as an empty list or an explicit `TODO`-commented placeholder; do not invent a resolution path.
- Policy Registry: entries per `06_registry_specs/policy_registry/policy_registry.md`; `PolicyEngineAdapter` interface with an interface-stub policy decision point implementing that interface (the source document `08_policy_governance_model.md` names this class `DummyPDP` — implemented under that name because the specification defines it, not as a throwaway placeholder).
- Approval Registry: entries per `06_registry_specs/approval_registry/approval_registry.md`.

## Reference Fixtures (Non-Normative)

Names such as `STOP_WORK`, `DISPATCH_ROBOT`, `HazardDetected`, `WorkerLocationUpdated`, `ZoneStatusChanged`, and `RobotStatusUpdated` recur across multiple source documents (`03_core_specifications/03_action_type_registry.md` Section 16, `06_registry_specs/action_registry/action_registry.md` Sections 11–12, `06_registry_specs/policy_registry/policy_registry.md` Sections 10–13, `07_implementation_plan/implementation_plan.md` Section 9). None of these documents declares them normative domain content; the registry documents explicitly mark their examples as non-normative placeholders. This slice uses them only as **reference fixtures** — consistent, recurring test data used to exercise the registries end to end — not as approved domain decisions. Every fixture using these names must carry an explicit non-normative marker in code and in tests.

## Non-Goals

- No Runtime Validation or Safety Gate implementation (Implementation Slice 3 scope).
- No Execution Request or External Control Integration (Implementation Slice 3 scope).
- No `agent_vocabulary_registry` or `model_adapter_registry` (see "Out of Scope" above).
- No real OPA/Rego policy content, no real approval authority assignment, no real evidence freshness thresholds — placeholder registry entries per `AGENTS.md` Domain Authority Rule and Domain No-Guessing Rule.
- No production adapter dispatch logic — this slice builds the `adapter_registry` contract only; executable adapter behavior is Implementation Slice 3, and real physical dispatch remains gated by the Safety Boundary Rule regardless of slice.

## Acceptance Criteria

- Each of the nine registries in scope loads, validates, and round-trips its reference-fixture entries with success/failure/edge-case tests.
- Registry entries for the reference fixtures exist end to end at the data level (an `EvidenceBundle` can be assembled and a `PolicyDecisionResponseDTO` can be produced), even though nothing downstream (Runtime Validation, Safety Gate) consumes them yet.
- No registry duplicates schema already owned by `03_core_specifications` (see `06_registry_specs/README.md` Section 12 registry-vs-core-spec boundary).
- No file, module, or test exists for `agent_vocabulary_registry` or `model_adapter_registry`.

## Reference Flow Status

Still no end-to-end reference flow. This slice's output is verified through registry-level unit and integration tests only (`tests/integration/registry_loading/`).
