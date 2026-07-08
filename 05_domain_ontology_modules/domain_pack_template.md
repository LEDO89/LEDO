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

Do not fill in the fields below with invented values. Every field must be authored or approved by a human domain expert per `AGENTS.md` Domain Authority Rule and the `05_domain_ontology_modules/domain_module_contract.md` boundaries. Until a real value is approved, leave the field as `DOMAIN_DECISION_REQUIRED: pending domain expert review`.

## Minimum Domain Pack Fields

Per `05_domain_ontology_modules/README.md` Section 11, every Domain Pack should include at least the following fields:

```yaml
domain_name: "DOMAIN_DECISION_REQUIRED: pending domain expert review — see 05_domain_ontology_modules/domain_pack_template.md Section 2"
domain_scope: "DOMAIN_DECISION_REQUIRED: pending domain expert review — see 05_domain_ontology_modules/domain_pack_template.md Section 2"

domain_classes: []          # DOMAIN_DECISION_REQUIRED: domain classes pending domain expert review — see 04_ontology_foundation/03_owl_modeling_principles.md
domain_properties: []       # DOMAIN_DECISION_REQUIRED: domain properties pending domain expert review — see 04_ontology_foundation/05_relationship_and_property_design.md
domain_events: []           # DOMAIN_DECISION_REQUIRED: domain events pending domain expert review — see 06_registry_specs/event_registry/event_registry.md
domain_states: []           # DOMAIN_DECISION_REQUIRED: domain states pending domain expert review — see 06_registry_specs/state_registry/state_registry.md
domain_actions: []          # DOMAIN_DECISION_REQUIRED: domain actions pending domain expert review — see 06_registry_specs/action_registry/action_registry.md
domain_evidence_types: []   # DOMAIN_DECISION_REQUIRED: domain evidence types pending domain expert review — see 06_registry_specs/evidence_registry/evidence_registry.md

domain_policy_references: []               # DOMAIN_DECISION_REQUIRED: domain policy references pending domain expert review — see 06_registry_specs/policy_registry/policy_registry.md
domain_approval_requirements: []           # DOMAIN_DECISION_REQUIRED: domain approval requirements pending domain expert review — see 06_registry_specs/approval_registry/approval_registry.md
domain_runtime_validation_requirements: [] # DOMAIN_DECISION_REQUIRED: runtime validation requirements pending domain expert review — see 08_runtime_validation/validators/validators.md

domain_registry_extensions: []   # list of registry entries this pack proposes, one per target registry
external_system_assumptions: []  # DOMAIN_DECISION_REQUIRED: external system assumptions pending domain expert review — see 06_registry_specs/external_system_registry/external_system_registry.md

governance_owner: "DOMAIN_DECISION_REQUIRED: governance owner pending domain expert review — see 05_domain_ontology_modules/domain_module_contract.md"
version: 0.1.0
```

## Usage Notes

- This template mirrors the Domain Pack minimum structure in `05_domain_ontology_modules/README.md` Section 11 exactly. Do not add fields here that duplicate technical/framework concerns (API, backend, runtime, audit, validation, adapters) — those belong in `src/ledo_ontology_core/framework/`, not inside a Domain Pack, per `PROJECT_TREE.md` Notes ("Technical layers ... must not be duplicated inside every domain pack").
- Each list field above becomes a set of registry entries once approved, not free-standing domain logic. A Domain Pack proposes registry content; it does not implement validators, adapters, or runtime services itself.
- Before a Domain Pack is used to generate `src/ledo_ontology_core/domain_packs/<domain_name>/` code, every `DOMAIN_DECISION_REQUIRED` marker must be resolved or explicitly deferred with a tracked reason, per `AGENTS.md` Domain No-Guessing Rule.
