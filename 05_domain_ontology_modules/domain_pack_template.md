---
title: Domain Pack Template
version: 1.0
status: draft
owner: platform-ontology
language: en
last_updated: 2026-07-06
---

# Domain Pack Template

## Purpose

`05_domain_ontology_modules/README.md` Section 10 ("Recommended Structure") names this file as the template used when a real, governed Domain Pack is created (for example `construction_domain_pack/`, `robotics_domain_pack/`). This file did not previously exist. It is a fill-in-the-blanks template, not a Domain Pack itself — copy this structure into a new Domain Pack directory once the fields below have real, governed values.

Do not fill in the fields below with invented values. Every field must be authored or approved by a human domain expert per `AGENTS.md` Domain Authority Rule and the `05_domain_ontology_modules/domain_module_contract.md` boundaries. Until a real value is approved, leave the field as `TODO: pending domain expert review`.

## Minimum Domain Pack Fields

Per `05_domain_ontology_modules/README.md` Section 11, every Domain Pack should include at least the following fields:

```yaml
domain_name: TODO: pending domain expert review
domain_scope: TODO: pending domain expert review

domain_classes: []          # TODO: pending domain expert review — must follow 04_ontology_foundation modeling rules
domain_properties: []       # TODO: pending domain expert review — must follow 04_ontology_foundation property design rules
domain_events: []           # TODO: pending domain expert review — must be registered in 06_registry_specs/event_registry
domain_states: []           # TODO: pending domain expert review — must be registered in 06_registry_specs/state_registry
domain_actions: []          # TODO: pending domain expert review — must be registered in 06_registry_specs/action_registry
domain_evidence_types: []   # TODO: pending domain expert review — must be registered in 06_registry_specs/evidence_registry

domain_policy_references: []               # TODO: pending domain expert review — must be registered in 06_registry_specs/policy_registry
domain_approval_requirements: []           # TODO: pending domain expert review — must be registered in 06_registry_specs/approval_registry
domain_runtime_validation_requirements: [] # TODO: pending domain expert review — must flow through 08_runtime_validation

domain_registry_extensions: []   # list of registry entries this pack proposes, one per target registry
external_system_assumptions: []  # TODO: pending domain expert review — external systems this pack assumes exist (fleet manager, PLC, SCADA, etc.)

governance_owner: TODO: pending domain expert review   # named individual or role responsible for this pack's domain accuracy
version: 0.1.0
```

## Usage Notes

- This template mirrors the Domain Pack minimum structure in `05_domain_ontology_modules/README.md` Section 11 exactly. Do not add fields here that duplicate technical/framework concerns (API, backend, runtime, audit, validation, adapters) — those belong in `src/ledo_ontology_core/framework/`, not inside a Domain Pack, per `PROJECT_TREE.md` Notes ("Technical layers ... must not be duplicated inside every domain pack").
- Each list field above becomes a set of registry entries once approved, not free-standing domain logic. A Domain Pack proposes registry content; it does not implement validators, adapters, or runtime services itself.
- Before a Domain Pack is used to generate `src/ledo_ontology_core/domain_packs/<domain_name>/` code, every `TODO: pending domain expert review` marker must be resolved or explicitly deferred with a tracked reason, per `AGENTS.md` Domain No-Guessing Rule.
