---
title: Implementation Slice 1 Plan — Foundation
version: 2.0
status: populated
owner: platform-ontology
language: en
last_updated: 2026-07-06
---

# Implementation Slice 1 Plan — Foundation

## Purpose

Define the scope, implementation order, and acceptance criteria for the Foundation slice: the shared contracts every later registry, validator, and service depends on.

This is a formal implementation slice of the architecture defined in `03_core_specifications/`, `06_registry_specs/`, and `04_ontology_foundation/`. It is not a prototype, a demo, or a throwaway scaffold — every DTO, enum, and loader produced here is production code and remains in the codebase permanently.

## Relationship to `implementation_plan.md`

`implementation_plan.md` Section 8 defines a single linear sequence, Phase 0 through Phase 19. This document groups the first five phases of that sequence. `implementation_plan.md` is a sequencing reference only (see `AGENTS.md` Source of Truth); the field-level content for everything below comes from `03_core_specifications/`, `06_registry_specs/`, and `04_ontology_foundation/` directly, not from `implementation_plan.md` itself.

Implementation Slice 1 = `implementation_plan.md` Phase 0–4:

- Phase 0: Architecture Freeze and Index Verification
- Phase 1: Common Contract Foundation
- Phase 2: Semantic Foundation Implementation
- Phase 3: Registry Base System
- Phase 4: Identity and Access Foundation

## Scope

This slice does not implement the event, state, snapshot, evidence, decision, policy, approval, adapter, or external system registries — those belong to Implementation Slice 2. It does not implement Runtime Validation, Safety Gate, or the Execution Adapter interface — those belong to Implementation Slice 3.

Deliverables (see `implementation_plan.md` Section 8, Phase 0–4 for sequencing detail; field-level content comes from the documents cited below, not from `implementation_plan.md`):

- Verification that Layer Architecture, Layer Stack Mapping, Core Specifications, Ontology Foundation, and Registry Specs folder structures are internally consistent (Phase 0).
- Common contract DTOs and enums from `03_core_specifications/01_common_schema_dto/` (base entity, trace context, version context, source metadata) (Phase 1).
- Minimal ontology foundation scaffolding per `04_ontology_foundation/00_ontology_foundation_report.md` and `01_semantic_web_technology_stack.md` (namespace, IRI generation scheme, base classes only — no domain classes) (Phase 2).
- A generic Registry Base pattern per `06_registry_specs/README.md` Sections 12, 12A, 12B: loader interface, common `RegistryStatus` enum, `*_boundary` prefix validator (`must_not_/does_not_/may_/requires_/cannot_`), and cross-registry reference resolver (`prefix:id` format, checked against target existence and `retired`/`blocked` status) (Phase 3).
- `action_registry` DTO and loader, per `06_registry_specs/action_registry/action_registry.md` Section 10 ("Registry Entry Schema"). Placed in this slice, not the Registry slice, because action types are referenced by every downstream registry (decision, policy, approval) and by the Common Object Lifecycle itself.
- `identity_registry` and `ontology_registry` DTO and loader, per `06_registry_specs/identity_registry/Identity_registry.md` and `06_registry_specs/ontology_registry/ontology_registry.md`.
- Role / Clearance / Permission DTO skeleton from `03_core_specifications/08_policy_governance_model/08_policy_governance_model.md` Sections 10–12, with placeholder registry entries only — no real role, clearance, or permission assignment (Phase 4).

## Non-Goals

- No event, state, snapshot, evidence, decision, policy, approval, adapter, or external system registry content (Implementation Slice 2 scope).
- No Runtime Validation, Safety Gate, or Execution Adapter code (Implementation Slice 3 scope).
- No real domain values, thresholds, or role/clearance assignments — placeholder registry entries and explicit `DOMAIN_DECISION_REQUIRED` markers only, per `AGENTS.md` Domain Authority Rule.
- No UI, no external system integration, no production infrastructure (database, message broker, or policy engine deployment).

## Acceptance Criteria

- All Phase 0 verification checklist items in `implementation_plan.md` Section 8 (Phase 0) pass.
- Common DTOs are type-safe (Pydantic v2) and covered by success/failure/edge-case tests per `AGENTS.md` Test Rule.
- The Registry Base pattern has at least one passing round-trip test (load → validate → status transition) using a placeholder registry entry, independent of any concrete registry from Implementation Slice 2.
- `action_registry`, `identity_registry`, and `ontology_registry` loaders pass success/failure/edge-case tests using placeholder registry entries explicitly marked non-normative.
- No physical command, real external system call, or invented domain rule appears anywhere in the diff.

## Reference Flow Status

There is no end-to-end reference flow at the end of this slice. The first formal reference flow (see Implementation Slice 3) only becomes runnable once Runtime Validation, Safety Gate, and the Execution Adapter interface are complete.
