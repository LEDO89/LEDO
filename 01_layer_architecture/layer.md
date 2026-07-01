**Ontology-Centric Layer**

**1\. Purpose**

This document defines the final layer architecture of the LEDO Ontology Core.

LEDO is an ontology-centric Cyber-Physical AI architecture designed to separate meaning, evidence, state, policy, approval, validation, execution requests, feedback, and audit across clear responsibility boundaries.

---

## **2\. Core Architecture Thesis**

Ontology defines meaning.

Evidence supports judgment.

World State represents current condition.

Agents generate candidates.

Policy determines operational permission.

Approval grants high-risk authority.

Safety Gate validates execution readiness.

External Systems perform physical execution.

Audit preserves accountability.

No layer may collapse these responsibilities into a single shortcut.

---

## **3\. Final Layer Structure**

| Layer | Name | Core Responsibility |
| ----- | ----- | ----- |
| 0 | Observability / Audit / Trace Layer | Tracks events, evidence, decisions, approvals, execution requests, feedback, failures, ontology changes, and operational history |
| 1 | Experience / Presentation Layer | Provides user-facing views for operators, supervisors, managers, safety teams, and executives |
| 2 | API Gateway Layer | Controls access, routing, request validation, real-time communication, and external entry points |
| 3 | Governance / Policy / Security Layer | Defines authorization, policy, approval, security, compliance, and decision authority |
| 4 | Core Ontology Kernel Layer | Defines the formal meaning of objects, relationships, properties, events, actions, constraints, workflows, and inference contracts |
| 5 | Knowledge & Semantic Memory Layer | Stores static knowledge, documents, graphs, historical records, evidence, and materialized semantic knowledge |
| 6 | Real-Time World State Layer | Converts live signals into current operational state |
| 7 | Distributed Domain Agent Layer | Interprets domain conditions and generates alerts, ActionCandidates, EscalationCases, and DecisionCases |
| 8 | Decision Router / Escalation Layer | Routes cases by risk, urgency, approval requirement, operational impact, and escalation policy |
| 9 | Approved Action / Safety Gate Layer | Validates whether an approved action is ready to become an ExecutionRequest |
| 10 | Unified Cyber-Physical Core Layer | Structures the shared operational lifecycle of Action, Decision, Approval, ExecutionRequest, Feedback, Recovery, and Audit |
| 11 | Execution Request & External Control Integration Layer | Sends high-level execution requests to external control systems |
| 12 | Physical World Layer | Represents real workers, robots, equipment, sensors, PLCs, SCADA systems, sites, zones, and external control systems |

---

## **4\. End-to-End Architecture Flow**

Physical World

→ Real-Time World State

→ Knowledge / Evidence Binding

→ Distributed Domain Agents

→ ActionCandidate

→ Semantic Validation

→ Evidence Check

→ Policy Check

→ Decision Router

→ Approval

→ Safety Gate

→ ExecutionRequest

→ External Control Integration

→ External System

→ Physical World

→ Feedback

→ Audit

→ World State Update

---

## **5\. Responsibility Boundaries**

Candidate ≠ Decision

Decision ≠ Approval

Approval ≠ Physical Command

ApprovedAction ≠ Physical Command

ExecutionRequest ≠ Physical Command

ExternalControlRequest ≠ Physical Command

External System \= Physical Execution Authority

---

## **6\. Source of Truth Boundaries**

| Area | Source of Truth |
| ----- | ----- |
| Semantic Meaning | Ontology |
| Class / Property / Axiom | Ontology Foundation |
| Current Runtime State | Real-Time World State |
| Historical Evidence | Evidence Store / Audit |
| Operational Permission | Policy |
| High-Risk Authority | Approval |
| Execution Readiness | Safety Gate Snapshot |
| Physical Execution | External System |
| Identity Resolution | Canonical Identity / Registry |
| User View | Presentation Layer |
| AI Interpretation | Agent Output as Candidate |

---

## **7\. Repository Mapping**

| Architecture Responsibility | Repository Location |
| ----- | ----- |
| Master Architecture | `00_master_architecture/` |
| Layer Definitions | `01_layer_architecture/` |
| Layer-to-Technology Mapping | `02_layer_stack_mapping/` |
| Operational Contracts | `03_core_specifications/` |
| Semantic Contracts | `04_ontology_foundation/` |
| Domain Ontology Extensions | `05_domain_ontology_modules/` |
| Controlled Registries | `06_registry_specs/` |
| Implementation Roadmap | `07_implementation_plan/` |
| Runtime Validation / Safety Gate | `08_runtime_validation/` |
| Supporting References | `09_appendices/` |
| Deprecated Materials | `10_archive/` |

---

## **8\. Unified Cyber-Physical Core Placement**

Layer 10 does not require a separate root-level folder.

The Unified Cyber-Physical Core Layer is specified across `03_core_specifications/`.

It is composed of:

Canonical Object Lifecycle

Common Schema / DTO

Event Type Taxonomy

Action Type Registry

State Model Registry

Evidence Model

Decision / Approval Matrix

Execution Adapter Model

Audit / Observability Model

Layer 10 defines the common operational lifecycle connecting:

Event

Evidence

State Update

ActionCandidate

DecisionCase

Approval

ApprovedAction

SafetyGateResult

ExecutionRequest

ExternalControlRequest

FeedbackEvent

AuditRecord

---

## **9\. Safety Gate Rule**

Safety Gate validates execution readiness for approved actions.

It does not grant approval.

Approval grants authority.

Safety Gate validates execution readiness.

Safety Gate must be deterministic and fail-closed.

The runtime hot path must not perform:

OWL Reasoning

Full SHACL Validation

SPARQL Query

Graph DB Network Call

LLM / SLM Call

External API Call

Disk I/O

Unbounded Computation

The runtime hot path must only read precomputed validation results from a materialized Safety Snapshot.

---

## **10\. Execution Boundary Rule**

LEDO does not perform physical execution directly.

LEDO defines:

intent

target

constraints

approval reference

evidence reference

policy reference

safety validation result

trace id

idempotency key

expected feedback

Actual physical execution belongs to external systems such as:

Robot Middleware

Fleet Manager

PLC

SCADA

Access Control System

Equipment Controller

Site Operation System

Safety-rated Controller

---

## **11\. Agent Boundary Rule**

Agents may generate:

Intent Interpretation

Situation Summary

Risk Interpretation

MappingProposal

EvidenceSummary

ActionCandidate

EscalationCase

DecisionCase

PolicyImpactSuggestion

Explanation

Agents must not generate:

Evidence

Policy Decision

Approval

Safety Gate Decision

Final ExecutionRequest

Final ExternalControlRequest

Physical Command

Agent output is a candidate and must be validated.

---

## **12\. Architecture Invariants**

Ontology is the semantic authority.

AI output is candidate, not truth.

Evidence is required for trusted decisions.

Policy determines operational permission.

Approval grants high-risk authority.

Safety Gate validates execution readiness.

ExecutionRequest is not a physical command.

External Systems perform physical execution.

Runtime hot path reads precomputed results only.

Audit preserves traceability.

Any design that violates these invariants is not LEDO architecture.

---

## **13\. Final Architecture Statement**

LEDO is organized into layered responsibility boundaries.

Ontology defines meaning, Evidence supports judgment, World State represents current condition, Agents generate candidates, Policy determines permission, Approval grants high-risk authority, Safety Gate validates execution readiness, the Unified Cyber-Physical Core structures the operational lifecycle, External Control Integration sends bounded requests, and External Systems perform physical execution.

Final structure:

Meaning

→ Evidence

→ State

→ Candidate

→ Decision

→ Approval

→ Validation

→ Execution Request

→ External Execution

→ Feedback

→ Audit

Final principles:

Meaning must be explicit.

Evidence must be traceable.

State must be current.

Policy must be enforceable.

Approval must be auditable.

Validation must be deterministic.

Execution must be bounded.

Safety must fail closed.

Audit must preserve accountability.

