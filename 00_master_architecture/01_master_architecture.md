**Master Architecture**

## **1\. Purpose**

`01_master_architecture.md` defines the full system architecture of the LEDO project.

This document explains what kind of system LEDO is, what responsibility structure it follows, what each layer owns, and how meaning, evidence, state, policy, approval, validation, and execution are separated.

This document is not a detailed implementation document.  
This document is not a domain-specific rule document.  
This document is not dependent on any specific tool or vendor.

This document is the architectural reference point for the entire LEDO system.

---

## **2\. System Mission**

LEDO is an ontology-centric Cyber-Physical AI architecture.

The mission of LEDO is to model industrial objects, relationships, states, events, evidence, decisions, approvals, validation, execution requests, feedback, and audit flows within one consistent structure.

LEDO is designed to solve the following problems.

Clearly define the meaning of industrial systems.

Separate real-time state from historical evidence.

Limit AI judgment to candidate generation.

Validate policy and approval before execution.

Validate execution readiness through the Safety Gate.

Delegate physical execution to external control systems.

Preserve the full decision path for auditability.

LEDO is not merely an agent system.  
LEDO is an industrial architecture that separates meaning, validation, policy, approval, and execution boundaries.

---

## **3\. Core Architectural Thesis**

The core thesis of LEDO is as follows.

Ontology defines meaning.

Evidence supports truth.

World State represents current condition.

AI generates candidates.

Policy determines permission.

Approval grants authority.

Safety Gate validates execution readiness.

External Systems perform physical execution.

Audit preserves accountability.

These responsibilities must not be merged.

---

## **4\. System Big Picture**

LEDO operates around the following flow.

External Data / Sensor / System Signal

→ Ingestion

→ Normalization

→ Validation

→ Ontology Binding

→ Evidence Binding

→ World State Update

→ Event Detection

→ Agent Interpretation

→ ActionCandidate

→ Semantic Validation

→ Policy Check

→ Decision Routing

→ Approval

→ Safety Gate

→ ExecutionRequest

→ External Control Integration

→ Feedback

→ Audit

The key architectural rules are:

AI may create an ActionCandidate.

ActionCandidate is not an execution command.

Approval is not a physical command.

ExecutionRequest is not a physical command.

Safety Gate is the final execution-readiness validation layer.

External Systems perform actual physical execution.

LEDO places multiple boundaries between judgment and execution.  
These boundaries create safety, explainability, and operational reliability.

---

## **5\. Repository Architecture**

The LEDO repository is divided by responsibility.

ledo\_ontology\_core/

  00\_master\_architecture/

  01\_layer\_architecture/

  02\_layer\_stack\_mapping/

  03\_core\_specifications/

  04\_ontology\_foundation/

  05\_domain\_ontology\_modules/

  06\_registry\_specs/

  07\_implementation\_plan/

  08\_runtime\_validation/

  09\_appendices/

  10\_archive/

Each folder has the following responsibility.

| Area | Responsibility |
| ----- | ----- |
| `00_master_architecture/` | Top-level architecture, first principles, and full-system structure |
| `01_layer_architecture/` | System layer definitions |
| `02_layer_stack_mapping/` | Mapping between layers, technologies, responsibilities, and runtime structure |
| `03_core_specifications/` | Operational contracts, lifecycle, DTOs, Evidence, Action, Decision, Approval, Execution, and Audit |
| `04_ontology_foundation/` | Semantic contracts, OWL/RDF/SHACL/SPARQL, BFO, reasoning, properties, and governance |
| `05_domain_ontology_modules/` | Domain-specific ontology extensions |
| `06_registry_specs/` | Controlled vocabularies, identifiers, action/event/state/property registries |
| `07_implementation_plan/` | Implementation sequence, engineering roadmap, and code strategy |
| `08_runtime_validation/` | Safety Gate, runtime snapshot, and deterministic validation |
| `09_appendices/` | Glossary, references, standards, and supporting materials |
| `10_archive/` | Deprecated or superseded documents |

---

## **6\. Master Architecture Document Relationship**

`00_master_architecture` is composed of three core documents.

00\_master\_architecture/

  README.md

  00\_first\_construction.md

  01\_master\_architecture.md

Each document has the following role.

| Document | Role |
| ----- | ----- |
| `README.md` | Explains the purpose and role of the Master Architecture folder |
| `00_first_construction.md` | Defines the non-negotiable principles and forbidden boundaries |
| `01_master_architecture.md` | Defines the full system structure and responsibility separation |

If needed, a Source of Truth Matrix or Document Control Map may be separated into an additional document later.  
At the initial Master Architecture level, these three documents are sufficient and should remain strong.

---

## **7\. Core Responsibility Split**

LEDO is designed around the following responsibility split.

Core Specifications \= Operational contracts

Ontology Foundation \= Semantic contracts

Runtime Validation \= Execution-readiness validation contracts

Registry Specs \= Controlled vocabularies and identifier management

Implementation Plan \= Implementation sequence

Source Code \= Implementation of approved specifications

Each responsibility means the following.

| Area | Meaning |
| ----- | ----- |
| Core Specifications | Defines what objects, lifecycles, and operational contracts the system must have |
| Ontology Foundation | Defines the meaning of objects, relationships, properties, events, states, and actions |
| Runtime Validation | Defines what must be validated immediately before execution |
| Registry Specs | Controls fixed vocabularies, action types, event types, state types, and properties |
| Implementation Plan | Defines the order in which documents are transformed into code |
| Source Code | Implements approved specifications |

This separation must be preserved across the entire LEDO system.

---

## **8\. Layer Architecture**

The LEDO system is organized into the following layers.

| Layer | Name | Role |
| ----- | ----- | ----- |
| 0 | Observability / Audit / Trace Layer | Tracks events, decisions, executions, failures, changes, and history |
| 1 | Experience / Presentation Layer | Provides user, operator, supervisor, and management interfaces |
| 2 | API Gateway Layer | Controls entry points for UI, external systems, agents, and platforms |
| 3 | Governance / Policy / Security Layer | Controls authorization, policy, approval, security, and compliance |
| 4 | Core Ontology Kernel Layer | Defines the semantic center of objects, relationships, properties, events, actions, constraints, and reasoning contracts |
| 5 | Knowledge & Semantic Memory Layer | Stores static knowledge, documents, graphs, historical events, and Evidence |
| 6 | Real-Time World State Layer | Builds current state from sensors, systems, robots, and equipment |
| 7 | Distributed Domain Agent Layer | Generates candidate interpretations and ActionCandidates through domain agents, SLMs, and rules |
| 8 | Decision Router / Escalation Layer | Routes decisions based on risk, urgency, approval requirements, and escalation policy |
| 9 | Approved Action / Safety Gate Layer | Validates approved actions immediately before execution |
| 10 | Unified Cyber-Physical Core Layer | Unifies Action, Decision, Execution, Feedback, and Audit flows |
| 11 | Execution Request & External Control Integration Layer | Sends execution requests to external control systems |
| 12 | Physical World | Contains real robots, equipment, PLCs, SCADA systems, and physical site systems |

The key point of this layer structure is that LLMs or agents are not the center of authority.  
Ontology, Evidence, Policy, Approval, and Safety Gate together form the operational control structure.

---

## **9\. Meaning Flow**

Meaning in LEDO is defined through Ontology.

Class

→ Object

→ Relationship

→ Property

→ Axiom

→ Constraint

→ Inference

→ Validation Contract

→ Materialized Runtime View

The key principles of the meaning flow are:

Class is a semantic category.

Property is a semantic relationship.

Axiom is a logical meaning condition.

Constraint validates data and execution conditions.

Inference computes additional meaning.

Runtime View stores precomputed results for execution validation.

Ontology does not perform heavy reasoning directly inside the runtime hot path.  
Required semantic results are precomputed into materialized views or snapshots.

---

## **10\. Evidence Flow**

Evidence is the basis of judgment.

Important decisions in LEDO cannot be trusted without Evidence.

Observation

→ Source

→ Timestamp

→ Trust Metadata

→ Provenance

→ Evidence

→ EvidenceBundle

→ Decision Support

→ Audit

The core principles of Evidence are:

AI output is not Evidence.

Evidence must have source and time.

Evidence must have validation status.

Evidence must be connected to decisions.

Evidence must be traceable through Audit.

AI may summarize Evidence, but it cannot become Evidence by itself.

---

## **11\. State Flow**

World State represents current condition.

Ontology defines meaning, but it does not directly store every real-time state as a permanent ontology fact.

Sensor / External Signal

→ Ingestion

→ Normalization

→ Validation

→ State Update

→ World State Cache

→ Event Detection

→ Agent Interpretation

World State may include:

current location

current risk state

current equipment state

current zone restriction state

current approval state

current external system availability

current Evidence freshness

World State is critical for runtime decisions, but it does not replace the semantic authority of Ontology.

---

## **12\. Decision Flow**

Decision Flow describes how an ActionCandidate develops into an execution request.

Agent Interpretation

→ ActionCandidate

→ Semantic Validation

→ Evidence Check

→ Policy Check

→ Decision Routing

→ Approval

→ Safety Gate

→ ExecutionRequest

Each stage has a different responsibility.

| Stage | Responsibility |
| ----- | ----- |
| Agent Interpretation | Interprets the situation and creates a candidate |
| ActionCandidate | Represents a candidate action |
| Semantic Validation | Checks whether the candidate is semantically possible |
| Evidence Check | Checks whether supporting Evidence is sufficient |
| Policy Check | Checks whether the action is operationally allowed |
| Decision Routing | Determines risk level and approval path |
| Approval | Grants high-risk authority |
| Safety Gate | Validates execution readiness immediately before execution |
| ExecutionRequest | Sends a request to an external system |

The core principles of Decision Flow are:

A candidate is not execution.

Approval is not a physical command.

An execution request is not a physical command.

---

## **13\. Execution Boundary**

LEDO does not directly perform physical execution.

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

An ExecutionRequest produced by LEDO is a request to an external system.

Actual physical execution belongs to external systems such as:

Robot Middleware

Fleet Manager

PLC

SCADA

Access Control System

Equipment Controller

Site Operation System

Safety-rated Controller

This boundary must never be broken.

---

## **14\. Safety Gate Architecture**

Safety Gate is the final validation layer before execution.

Safety Gate checks:

Is approval valid?

Is Evidence sufficient and fresh?

Is the current state executable?

Is there any policy violation?

Is there any conflict state?

Is the external system available?

Is the Snapshot valid?

Safety Gate does not perform heavy computation in the runtime hot path.

The following are forbidden in the runtime hot path.

OWL Reasoner

Full SHACL Validation

SPARQL Query

Graph DB Network Call

LLM / SLM Call

External API Call

Disk I/O

Unbounded Computation

Safety Gate reads a precomputed Snapshot.

Precomputed Validation

→ Materialized Safety Snapshot

→ Deterministic Lookup

→ Allow / Deny / Hold / Escalate

If uncertain, Safety Gate fails closed.

---

## **15\. Source of Truth Matrix**

LEDO does not allow one layer to monopolize every form of truth.

Each area has a separate Source of Truth.

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

This separation creates safety, explainability, and accountability.

---

## **16\. AI / Agent Boundary**

AI and Agents are important in LEDO, but they do not hold final authority.

AI and Agents may perform:

Intent interpretation

Situation summarization

Risk interpretation

MappingProposal generation

EvidenceSummary generation

ActionCandidate generation

PolicyImpactSuggestion generation

Explanation generation

AI and Agents must not perform:

Evidence creation

Final Policy Decision

Approval granting

Safety Gate Decision

Direct ExecutionRequest finalization

Direct ExternalControlRequest finalization

Physical Command generation

AI output is a candidate and must be validated.

---

## **17\. Registry Architecture**

Registry manages controlled vocabularies and identifiers in LEDO.

Registry may be required for:

Class

Property

Action Type

Event Type

State Type

Evidence Type

Policy Reference

Adapter Type

Snapshot Schema

Agent Vocabulary

The purpose of Registry is:

prevent arbitrary generation

manage versions

control fixed vocabularies

ensure validation

maintain consistency between documents and code

Registry does not define meaning directly.  
Meaning is defined by Ontology and specification documents.  
Registry stably references and controls defined meanings.

---

## **18\. Domain Extension Boundary**

LEDO separates Framework from Domain Modules.

Framework defines structure.

DTO

Registry

Validator

Interface

Adapter Boundary

Audit Structure

Safety Gate Contract

Domain Modules define domain meaning.

industry-specific objects

site-specific states

domain-specific risk types

domain-specific task types

domain-specific approval criteria

domain-specific policy mappings

Domain meaning must not be generated arbitrarily.  
Domain meaning must be governed through expert review and governance.

---

## **19\. Architecture Invariants**

The following invariants must be preserved across the entire LEDO architecture.

Ontology is the semantic authority.

AI output is candidate, not truth.

Evidence is required for trusted decisions.

Policy determines operational permission.

Human approval governs high-risk authority.

Safety Gate validates execution readiness.

ExecutionRequest is not a physical command.

External Systems perform physical execution.

Runtime hot path reads precomputed results only.

Audit preserves traceability.

Any design that breaks these invariants is not LEDO architecture.

---

## **20\. Final Architecture Statement**

LEDO is an ontology-centric Cyber-Physical AI architecture.

LEDO does not directly connect meaning to execution.  
Meaning is defined by Ontology, judgment is supported by Evidence and State, permission is determined by Policy, high-risk authority is granted by Approval, execution readiness is validated by Safety Gate, and physical execution is performed by External Systems.

The final structure of LEDO is:

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

The final principles are:

Meaning must be explicit.

Evidence must be traceable.

State must be current.

Policy must be enforceable.

Approval must be auditable.

Validation must be deterministic.

Execution must be bounded.

Safety must fail closed.

Audit must preserve accountability.

# **Master Architecture**

