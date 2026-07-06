---
title: Ontology Module Catalog
version: 1.1
status: populated
owner: platform-ontology
language: en
last_updated: 2026-07-06
---

# Ontology Module Catalog

## Purpose

Catalog reference items and examples. Do not treat this appendix as executable runtime code.

This is the Ontology Module Catalog referenced by `03_core_specifications/06_ontology_module_boundary/6_ontology_module_boundary.md` (Appendix E). The module list below reflects that document's Sections 6, 8–13 and the `05_domain_ontology_modules/` folder set; the source documents remain authoritative if they ever diverge.

## Notes

This document is intentionally written in English so that Codex and other coding agents can use it as an implementation source. No module listed here has concrete classes or properties defined yet — see `05_domain_ontology_modules/README.md`: domain meaning must be governed by human domain experts, not invented by Codex.

## Core Ontology Layers

core-upper — stable upper concepts (Entity, Agent, Object, Location, Time, Source, Capability)
core-crosscutting — cross-cutting operational concepts (Event, State, Action, Evidence, Risk, Policy, Approval, Feedback, Audit, Provenance)

Both correspond to the Definition Layer described in `04_ontology_foundation/00_ontology_foundation_report.md`; together they form the semantic core referred to elsewhere as the Core Ontology Kernel. This mapping is stated explicitly here because it is not spelled out verbatim in either source document.

## Domain Ontology Modules (`05_domain_ontology_modules/`)

action
ai
construction
core_crosscutting
core_upper
event
evidence
industrial
mapping
policy
robot
state

Each module folder currently contains only a placeholder `*_ontology.md` and `implementation_guide.md` — no concrete classes, properties, or domain values exist yet in any of them.

## Full Catalog Categories (Beyond Initial Scope)

The following category catalogs are expected to grow as domain modules mature, per `06_ontology_module_boundary` Section 2.2. They are listed here as placeholders only; adding concrete classes/properties requires ontology governance (see `04_ontology_foundation/06_ontology_governance_and_versioning.md`), not ad hoc addition:

core-upper class list
core-crosscutting class list
common property list
construction class list
industrial class list
robot class list
policy class list
AI class list
evidence class list
state class list
event class list
action class list
cross-module mapping list
external ontology mapping list
object property catalog
SHACL shape catalog
Mediation Concept catalog
