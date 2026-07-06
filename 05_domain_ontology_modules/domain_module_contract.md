---
title: Domain Module Extension Contract
version: 1.0
status: draft
owner: platform-ontology
language: en
last_updated: 2026-07-06
---

# Domain Module Extension Contract

## Purpose

`05_domain_ontology_modules/README.md` Section 10 ("Recommended Structure") names this file as one of the two documents every domain module folder should be checked against, but it did not previously exist. This document is that contract: the minimum set of conditions a Domain Module (`action`, `ai`, `construction`, `core_crosscutting`, `core_upper`, `event`, `evidence`, `industrial`, `mapping`, `policy`, `robot`, `state`, or any future module) must satisfy before it is considered a valid extension of the LEDO Ontology Core.

This document does not define any domain meaning itself. It defines the shape a domain module must have, and the boundaries it must not cross, per `05_domain_ontology_modules/README.md` Sections 2, 4, 5, 6, 7, 8, and 9.

## What a Domain Module May Define

A Domain Module may define:

- Domain-specific object types
- Domain-specific state types
- Domain-specific event types
- Domain-specific action candidate types
- Domain-specific Evidence types
- Domain-specific Policy references
- Domain-specific Runtime Validation requirements
- Domain-specific external system integration requirements

## What a Domain Module Must Not Define

Per `05_domain_ontology_modules/README.md` Section 4, a Domain Module must not directly define:

- Real industrial safety standards
- Real equipment operation rules
- Real work permit rules
- Real risk thresholds
- Real legal interpretations
- Real emergency procedures
- Real robot behavior rules
- Real PLC / SCADA command semantics
- Site-specific approval authority

These require a separate, governed Domain Pack with explicit domain-expert review — they are never authored directly inside `05_domain_ontology_modules/` or invented by Codex.

## Non-Negotiable Boundaries

A Domain Module must never violate:

- AI output is not Evidence.
- ActionCandidate is not an execution command.
- ApprovedAction is not a physical command.
- ExecutionRequest is not a physical command.
- Safety Gate must not be bypassed.
- Physical Execution belongs to External Systems.

## Required Relationships

Every Domain Module must satisfy all four of the following relationships before it is considered complete:

1. **Foundation relationship** (`04_ontology_foundation/`) — the module's classes, properties, axioms, and constraints must follow Foundation modeling principles (`03_owl_modeling_principles.md`), relationship/property design (`05_relationship_and_property_design.md`), and governance/versioning rules (`06_ontology_governance_and_versioning.md`). A Domain Module does not replace the Foundation.
2. **Core Specifications relationship** (`03_core_specifications/`) — domain events, action candidates, evidence types, and approval requirements must connect to the canonical objects already defined there (`CoreEvent`, `ActionCandidate`, the Evidence Model, the Decision/Approval Matrix, `ExecutionRequest`). A Domain Module does not bypass the Core object lifecycle.
3. **Registry relationship** (`06_registry_specs/`) — every domain-specific action type, event type, state type, evidence type, policy reference, and approval requirement must be registered in the matching registry (`action_registry`, `event_registry`, `state_registry`, `evidence_registry`, `policy_registry`, `approval_registry`). A Domain Module does not invent unregistered values.
4. **Runtime Validation relationship** (`08_runtime_validation/`) — any domain-specific validation requirement must flow through `Domain Rule Requirement → Validation Specification → Registry Reference → Materialization Rule → Safety Snapshot → Safety Gate Lookup`. A Domain Module must not insert direct reasoning, database calls, or heavy computation into the Safety Gate hot path.

## Minimum Contract Checklist

A Domain Module folder satisfies this contract when it has:

- [ ] A `<module_name>_ontology.md` file that states scope and (once governed) classes/properties, following `04_ontology_foundation` naming and modeling rules.
- [ ] An `implementation_guide.md` file with the same structure as the existing per-module implementation guides already present across the repository (for example `05_domain_ontology_modules/action/implementation_guide.md` or `02_layer_stack_mapping/implementation_guide.md`): Goal, Module Focus, Source of Truth, Default Implementation Order, Explicit Non-Goals, Acceptance Criteria. (There is no separate `templates/` folder in this repository; use an existing `implementation_guide.md` instance as the reference shape.)
- [ ] No concrete domain thresholds, safety rules, or legal interpretations authored directly in the module (see "What a Domain Module Must Not Define" above) — only placeholders, TODOs, or references to a governed Domain Pack.
- [ ] Explicit mapping from any domain-specific vocabulary to the registries listed in "Registry relationship" above, once that vocabulary is proposed.
- [ ] No direct references to physical control protocols, PLC ladder logic, or robot motion primitives — those remain owned by external systems per the Execution Boundary Rule.

## Relationship to `domain_pack_template.md`

This contract defines the rules a module must follow. `domain_pack_template.md` (in this same folder) is the fill-in template used once a module is ready to receive real, governed domain content — i.e., once a human domain expert is ready to move a module from placeholder scaffolding to an actual Domain Pack.
