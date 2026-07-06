# LEDO Ontology Core

## What This Repository Is

LEDO Ontology Core is an ontology-centered industrial AI architecture repository for structuring industrial domains, evidence, policy, approval, runtime validation, safety gates, execution requests, external control boundaries, feedback, and audit.

This repository defines framework structure for governing domain meaning safely. It is not a source of domain-specific industrial, safety, robotics, legal, or operational rules.

## Current Status

- Architecture v1 candidate / ready status.
- P0/P1 architecture boundary closed.
- Remaining known items are minor P2/P3 documentation hygiene items only.
- Implementation skeleton planning is the next major phase.

## Source-of-Truth Policy

- `AGENTS.md` is the repository-level operational entry document.
- `00_master_architecture/` contains the master architecture source-of-truth.
- `README.md` is only a navigation and orientation document, not architecture source of truth.
- `PROJECT_TREE.md` is only a repository structure map.
- `10_archive/` contains deprecated, superseded, and historical review materials.

If this README conflicts with `AGENTS.md` or `00_master_architecture/`, `AGENTS.md` and `00_master_architecture/` take precedence.

## Core Principles

- Model-independent
- Vendor-independent
- Domain-transferable
- Ontology-governed
- Safety-gated
- Evidence-backed
- Locally deployable

## Core Safety Invariants

- No approval, no ApprovedAction.
- Safety Gate does not create ApprovedAction.
- No RuntimeValidationResult, no SafetyGatePass.
- No SafetyGatePass, no ExecutionRequest.
- No EmergencySafetyGatePass, no EmergencyExecutionRequest.
- ExecutionRequest is not PhysicalCommand.
- External systems perform physical execution.
- No audit, no trust.

## Repository Map

- `00_master_architecture/` - master architecture source-of-truth and top-level boundaries.
- `01_layer_architecture/` - system layer definitions.
- `02_layer_stack_mapping/` - mapping between layers, technologies, and runtime responsibilities.
- `03_core_specifications/` - operational contracts, DTOs, lifecycle, evidence, approval, execution, and audit.
- `04_ontology_foundation/` - semantic contracts, OWL, SHACL, reasoning, property design, and governance.
- `05_domain_ontology_modules/` - domain-specific ontology extension area governed by human domain authority.
- `06_registry_specs/` - class, property, action, state, event, policy, adapter, and snapshot registries.
- `07_implementation_plan/` - implementation order, milestones, and module roadmap.
- `08_runtime_validation/` - Safety Gate, runtime snapshot, deterministic validation, and hot path constraints.
- `09_appendices/` - references, glossary, examples, and supporting notes.
- `10_archive/` - deprecated, superseded, and historical review materials.
- `src/` - Python implementation root.
- `src/ledo_ontology_core/domain_packs/` - implementation domain pack area that mirrors `05_domain_ontology_modules/` top-level module names for semantic traceability.
- `src/ledo_ontology_core/framework/` - shared backend implementation kernel.
- `apps/` - API, CLI, and worker application entrypoints.
- `frontend/` - root-level first-class operator UI product surface.
- `contracts/` - implementation contracts shared across backend, frontend, workers, adapters, LLM/tool interfaces, external systems, and tests.
- `contracts/` follows: Pydantic Models -> JSON Schema -> Examples -> OpenAPI -> AsyncAPI -> Protobuf.
- OpenAPI is not OpenAI and does not imply paid API usage.
- `infra/` - deployment and operations scaffolding.
- `tests/` - future unit, integration, fixture, and regression test suite area.

## Recommended Reading Order

1. `AGENTS.md`
2. `00_master_architecture/README.md`
3. `00_master_architecture/00_first_construction.md`
4. `00_master_architecture/01_master_architecture.md`
5. `PROJECT_TREE.md`
6. `01_layer_architecture/layer.md`
7. `03_core_specifications/00_canonical_object_lifecycle/0_canonical_object_lifecycle.md`
8. `03_core_specifications/01_common_schema_dto/1_common_schema_dto.md`
9. `08_runtime_validation/safety_gate/safety_gate.md`
10. `06_registry_specs/action_registry/action_registry.md`

## Optional Historical Context

- `10_archive/review_artifacts/README.md` - historical review evidence only; not part of the core reading order.

## Architecture Lifecycle

```text
ActionCandidate
-> DecisionCase
-> PolicyEvaluation
-> ApprovalRequest
-> ApprovalDecision
-> ApprovedAction
-> RuntimeValidationInput
-> RuntimeValidationResult
-> Safety Gate
-> SafetyGatePass or SafetyGateBlock
-> ExecutionRequest
-> ExternalControlRequest
-> External System
-> FeedbackEvent
-> AuditRecord
-> World State Update
```

## Implementation Direction

Implementation proceeds from schemas/DTOs, enums, registries, validators, runtime services, adapter interfaces, interface-stub adapter implementations (non-production test doubles for external systems not yet approved for production dispatch), tests, contracts, API/CLI/worker entrypoints, and then frontend integration.

Frontend and graph visualization are first-class product surfaces. They must consume backend contracts and must not become ontology source-of-truth.

Implementation work must preserve ontology authority, evidence provenance, policy evaluation, human approval boundaries, deterministic Safety Gate behavior, execution separation, and audit traceability.
