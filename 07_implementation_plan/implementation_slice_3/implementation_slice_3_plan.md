---
title: Implementation Slice 3 Plan — Runtime and Execution
version: 2.0
status: populated
owner: platform-ontology
language: en
last_updated: 2026-07-06
---

# Implementation Slice 3 Plan — Runtime and Execution

## Purpose

Define the scope, implementation order, and acceptance criteria for the Runtime and Execution slice: Runtime Validation, Safety Gate, the Execution Adapter interface, feedback/world-state reconciliation, and audit wiring. This is where the architecture becomes exercisable end to end through a first formal reference flow.

## Relationship to `implementation_plan.md`

This document groups `implementation_plan.md` Section 8, Phase 15 through Phase 19. It assumes Implementation Slice 1 (foundation) and Implementation Slice 2 (registries) are complete.

`implementation_plan.md` Phase 15–19:

- Phase 15: Runtime Validation Design and Implementation
- Phase 16: Safety Gate Implementation
- Phase 17: Execution Request and External Control Integration
- Phase 18: Feedback and World State Update
- Phase 19: Observability and Audit Implementation

## Precondition (Not Yet Satisfied): Direct Reconciliation of `08_runtime_validation/`

Before any Runtime Validation or Safety Gate code is written, the following four documents must be read directly and reconciled against each other and against `03_core_specifications`:

- `08_runtime_validation/safety_gate/safety_gate.md`
- `08_runtime_validation/validators/validators.md`
- `08_runtime_validation/toctou/toctou.md`
- `08_runtime_validation/idempotency/idempotency_control.md`

This is the first task of this slice, not yet performed. `08_runtime_validation/*` is the primary source of truth for Phase 16 (see `AGENTS.md` Source of Truth) — it outranks `02_layer_stack_mapping/09_approved_action_safety_gate_stack_mapping.md`, which is a technology/responsibility reference only.

## Scope

Deliverables (see `implementation_plan.md` Section 8, Phase 15–19 for sequencing detail; field-level content comes from `08_runtime_validation/*`, `03_core_specifications/09_execution_adapter_model/`, `03_core_specifications/04_state_model_registry/`, and `03_core_specifications/10_audit_observability_model/` directly):

- Runtime Validation: the validator set defined in `08_runtime_validation/validators/validators.md`, applied to the reference fixtures from Implementation Slice 2. Includes TOCTOU (`08_runtime_validation/toctou/toctou.md`) and idempotency (`08_runtime_validation/idempotency/idempotency_control.md`) checks.
- Safety Gate: deterministic `SafetyGatePass` / `SafetyGateBlock` issuance per `08_runtime_validation/safety_gate/safety_gate.md`, consuming `RuntimeValidationResult`. The hot path never performs OWL reasoning, full SHACL validation, SPARQL queries, or LLM/SLM calls, per `AGENTS.md` and `00_first_construction.md`.
- Execution Adapter: `ExecutionRequestDTO`, `ExecutionContextSnapshotDTO`, `ExternalControlRequestDTO`, and the `ExecutionAdapter` interface, per `03_core_specifications/09_execution_adapter_model/9_execution_adapter_model.md`. `MockAdapter` and `DryRunAdapter` are implemented as complete, tested interface-stub adapters — these are the specification's own named `AdapterType` values (Section 8.11–8.12), not an incomplete-code placeholder. Every other `AdapterType` (`RobotMiddlewareAdapter`, `FleetManagerAdapter`, `PLCAdapter`, `SCADAAdapter`, `AccessControlAdapter`, etc.) is implemented as a class that satisfies the `ExecutionAdapter` interface but raises `NotImplementedError` on any dispatch method, with a docstring citing the Safety Boundary Rule as the reason real dispatch is not connected — this is a permanent architectural boundary, not a temporary scope cut.
- Feedback and World State Update: `FeedbackEventDTO` handling and world state reconciliation, including the fail-safe path per `03_core_specifications/04_state_model_registry` Section 9.4.
- Observability and Audit: `AuditRecordDTO` emission wired to every stage, plus `trace_id` / `correlation_id` / `decision_trace_id` propagation per `03_core_specifications/10_audit_observability_model/`. Full Prometheus/Grafana/Jaeger deployment from `02_layer_stack_mapping/00` is not required for this slice's reference flow — audit-record correctness is required; observability infrastructure is a separate, later concern.

## Non-Goals

- No real robot, PLC, SCADA, or access-control dispatch. This is not a scope limitation specific to this slice — it is the Safety Boundary Rule in `AGENTS.md`, a constitutional constraint that applies regardless of how mature the implementation becomes, and it is not lifted by completing more of the architecture. Real dispatch requires explicit human approval per adapter, separately from this implementation plan.
- No production OPA/Rego deployment — the interface-stub policy decision point (`DummyPDP`, per the specification's own naming) from Implementation Slice 2 is used.
- No UI (`frontend/`) work — the reference flow below is a backend/CLI-driven flow, per `AGENTS.md` Architecture Implementation Order (UI comes after framework, contracts, validation, and API boundaries).
- No emergency fast-path implementation unless a human-authored Emergency Policy already exists (see `03_core_specifications/08_policy_governance_model` Section 16); this slice covers the Standard Path only.
- No `agent_vocabulary_registry` or `model_adapter_registry` dependency (consistent with Implementation Slice 2).

## Acceptance Criteria

- The reference fixtures from Implementation Slice 2 run end to end: `Event → State → Snapshot → Evidence → Decision → Policy → Approval → RuntimeValidation → SafetyGate → ExecutionRequest → (interface-stub) External System → Feedback → Audit → World State Update`.
- A `SafetyGateBlock` path is also demonstrated for at least one failure case per reference fixture (e.g., stale state, missing evidence, or missing idempotency key), per `08_runtime_validation/safety_gate/safety_gate.md` fail-closed rule.
- Every object in the chain carries `trace_id` / `correlation_id` and is linked in the resulting `AuditRecord`.
- No `PhysicalCommand` object is ever created or creatable through the `ExecutionAdapter` interface.
- Every `AdapterType` other than `MockAdapter` / `DryRunAdapter` raises `NotImplementedError` on dispatch, with no silent no-op behavior.

## First Formal Reference Flow

A CLI or test-driven flow (`apps/cli/` per `AGENTS.md`, or `tests/integration/safety_gate_flow/`) that runs the Implementation Slice 2 reference fixtures end to end against interface-stub external systems and records the full audit trail. This is the first point in the implementation plan where the architecture is exercisable end to end. It is a verification exercise for the architecture, not a product feature or a permanent scope boundary — the DTOs, registries, and validators built across all three slices are general-purpose and are not written specifically for these fixture names.
