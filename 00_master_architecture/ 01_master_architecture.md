**Master Architecture**

## **1\. Purpose**

`01_ledo_master_architecture.md` defines the full system architecture of the LEDO project.

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

  00\_ledo\_first\_constitution.md

  01\_ledo\_master\_architecture.md

Each document has the following role.

| Document | Role |
| ----- | ----- |
| `README.md` | Explains the purpose and role of the Master Architecture folder |
| `00_ledo_first_constitution.md` | Defines the non-negotiable principles and forbidden boundaries |
| `01_ledo_master_architecture.md` | Defines the full system structure and responsibility separation |

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

## **1\. 목적**

`01_ledo_master_architecture.md`는 LEDO 프로젝트의 전체 시스템 아키텍처를 정의하는 문서다.

이 문서는 LEDO가 어떤 시스템인지, 어떤 책임 구조를 가지는지, 각 계층이 어떤 역할을 담당하는지, 그리고 의미·증거·상태·정책·승인·검증·실행이 어떻게 분리되는지를 설명한다.

이 문서는 세부 구현 문서가 아니다.  
이 문서는 도메인별 규칙 문서가 아니다.  
이 문서는 특정 도구나 벤더에 종속되는 문서가 아니다.

이 문서는 LEDO 전체 구조의 기준점이다.

---

## **2\. 시스템 미션**

LEDO는 온톨로지 중심의 Cyber-Physical AI 아키텍처다.

LEDO의 목표는 산업 현장의 객체, 관계, 상태, 사건, 증거, 판단, 승인, 검증, 실행 요청, 감사 흐름을 하나의 일관된 구조로 모델링하는 것이다.

LEDO는 다음 문제를 해결하기 위해 설계된다.

산업 현장의 의미를 명확히 정의한다.  
실시간 상태와 과거 증거를 분리한다.  
AI 판단을 후보로 제한한다.  
정책과 승인을 실행 전에 통과시킨다.  
Safety Gate를 통해 실행 준비 상태를 검증한다.  
물리 실행은 외부 제어 시스템에 위임한다.  
전체 판단 경로를 감사 가능하게 보존한다.

LEDO는 단순한 에이전트 시스템이 아니다.  
LEDO는 의미, 검증, 정책, 승인, 실행 경계를 분리하는 산업용 아키텍처다.

---

## **3\. 핵심 아키텍처 명제**

LEDO의 핵심 명제는 다음과 같다.

Ontology defines meaning.  
Evidence supports truth.  
World State represents current condition.  
AI generates candidates.  
Policy determines permission.  
Approval grants authority.  
Safety Gate validates execution readiness.  
External Systems perform physical execution.  
Audit preserves accountability.

이를 한국어로 정리하면 다음과 같다.

Ontology는 의미를 정의한다.  
Evidence는 판단 근거를 제공한다.  
World State는 현재 상태를 표현한다.  
AI는 후보를 생성한다.  
Policy는 운영 허용 여부를 판단한다.  
Approval은 고위험 권한을 부여한다.  
Safety Gate는 실행 준비 상태를 검증한다.  
External System은 물리 실행을 수행한다.  
Audit은 책임 추적성을 보존한다.

이 책임들은 서로 합쳐지면 안 된다.

---

## **4\. 전체 시스템 큰 그림**

LEDO는 다음 흐름을 중심으로 작동한다.

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

이 흐름에서 중요한 점은 다음과 같다.

AI는 ActionCandidate를 만들 수 있다.  
ActionCandidate는 실행 명령이 아니다.  
Approval은 물리 명령이 아니다.  
ExecutionRequest도 물리 명령이 아니다.  
Safety Gate는 마지막 실행 준비 검증 계층이다.  
External System이 실제 물리 실행을 담당한다.

LEDO는 판단과 실행 사이에 여러 개의 경계를 둔다.  
이 경계가 시스템의 안전성과 신뢰성을 만든다.

---

## **5\. Repository Architecture**

LEDO repository는 책임 단위로 나뉜다.

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

각 폴더의 책임은 다음과 같다.

| 영역 | 책임 |
| ----- | ----- |
| `00_master_architecture/` | 최상위 아키텍처, 절대 원칙, 전체 구조 |
| `01_layer_architecture/` | 시스템 레이어 정의 |
| `02_layer_stack_mapping/` | 레이어와 기술, 책임, 런타임 구조의 매핑 |
| `03_core_specifications/` | 운영 계약, 객체 생명주기, DTO, Evidence, Action, Decision, Approval, Execution, Audit |
| `04_ontology_foundation/` | 의미 계약, OWL/RDF/SHACL/SPARQL, BFO, reasoning, property, governance |
| `05_domain_ontology_modules/` | 도메인별 온톨로지 확장 |
| `06_registry_specs/` | 통제된 어휘, 식별자, action/event/state/property registry |
| `07_implementation_plan/` | 구현 순서, 엔지니어링 계획, 코드화 전략 |
| `08_runtime_validation/` | Safety Gate, runtime snapshot, deterministic validation |
| `09_appendices/` | 용어, 참고 자료, 표준, 부록 |
| `10_archive/` | 폐기되었거나 대체된 문서 |

---

## **6\. Master Architecture 문서 관계**

`00_master_architecture`는 세 개의 핵심 문서로 구성된다.

00\_master\_architecture/  
  README.md  
  00\_ledo\_first\_constitution.md  
  01\_ledo\_master\_architecture.md

각 문서의 역할은 다음과 같다.

| 문서 | 역할 |
| ----- | ----- |
| `README.md` | 이 폴더의 목적과 역할을 설명한다 |
| `00_ledo_first_constitution.md` | 절대 원칙과 금지 경계를 정의한다 |
| `01_ledo_master_architecture.md` | 전체 시스템 구조와 책임 분리를 정의한다 |

필요할 경우 Source of Truth Matrix나 Document Control Map은 나중에 별도 문서로 분리할 수 있다.  
그러나 초기 Master Architecture는 위 세 문서로 충분히 강하게 유지한다.

---

## **7\. Core Responsibility Split**

LEDO는 다음 책임 분리를 기준으로 설계된다.

Core Specifications \= 운영 계약  
Ontology Foundation \= 의미 계약  
Runtime Validation \= 실행 준비 검증 계약  
Registry Specs \= 통제된 어휘와 식별자 관리  
Implementation Plan \= 구현 순서  
Source Code \= 승인된 사양의 구현

각 책임의 의미는 다음과 같다.

| 영역 | 의미 |
| ----- | ----- |
| Core Specifications | 시스템이 어떤 객체와 생명주기를 가져야 하는지 정의한다 |
| Ontology Foundation | 객체, 관계, 속성, 사건, 상태, 행동의 의미를 정의한다 |
| Runtime Validation | 실행 직전 무엇을 검증해야 하는지 정의한다 |
| Registry Specs | 고정 어휘, action type, event type, state type, property를 통제한다 |
| Implementation Plan | 문서를 어떤 순서로 코드화할지 정의한다 |
| Source Code | 승인된 명세를 실제 코드로 구현한다 |

이 분리는 LEDO 전체에서 유지되어야 한다.

---

## **8\. Layer Architecture**

LEDO의 시스템 레이어는 다음과 같이 구성된다.

| Layer | 이름 | 역할 |
| ----- | ----- | ----- |
| 0 | Observability / Audit / Trace Layer | 전체 이벤트, 판단, 실행, 실패, 변경 이력을 추적한다 |
| 1 | Experience / Presentation Layer | 사용자, 운영자, 관리자, 감독자가 시스템을 보고 개입하는 UI 계층이다 |
| 2 | API Gateway Layer | 외부 요청, UI, 시스템, 에이전트, 외부 플랫폼의 진입점을 통제한다 |
| 3 | Governance / Policy / Security Layer | 권한, 정책, 승인, 보안, 컴플라이언스를 통제한다 |
| 4 | Core Ontology Kernel Layer | 객체, 관계, 속성, 사건, 행동, 제약, 추론 계약의 의미 중심이다 |
| 5 | Knowledge & Semantic Memory Layer | 정적 지식, 문서, 그래프, 과거 사건, Evidence를 저장한다 |
| 6 | Real-Time World State Layer | 센서, 시스템, 로봇, 장비 상태를 현재 상태로 구성한다 |
| 7 | Distributed Domain Agent Layer | 도메인별 AI/SLM/Rule Agent가 후보 해석과 ActionCandidate를 생성한다 |
| 8 | Decision Router / Escalation Layer | 위험도, 긴급도, 승인 필요성에 따라 판단 경로를 분기한다 |
| 9 | Approved Action / Safety Gate Layer | 승인된 조치를 실행 직전 검증한다 |
| 10 | Unified Cyber-Physical Core Layer | Action, Decision, Execution, Feedback, Audit 흐름을 공통 구조로 묶는다 |
| 11 | Execution Request & External Control Integration Layer | 외부 제어 시스템에 실행 요청을 전달한다 |
| 12 | Physical World | 실제 로봇, 장비, PLC, SCADA, 현장 시스템이 물리 실행을 수행한다 |

이 레이어 구조의 핵심은 LLM이나 Agent가 중심이 아니라 Ontology, Evidence, Policy, Approval, Safety Gate가 함께 중심을 형성한다는 점이다.

---

## **9\. Meaning Flow**

LEDO에서 의미는 Ontology를 통해 정의된다.

Class  
→ Object  
→ Relationship  
→ Property  
→ Axiom  
→ Constraint  
→ Inference  
→ Validation Contract  
→ Materialized Runtime View

의미 흐름의 핵심은 다음과 같다.

Class는 의미 범주다.  
Property는 의미 관계다.  
Axiom은 논리적 의미 조건이다.  
Constraint는 데이터와 실행 조건을 검증한다.  
Inference는 추가 의미를 계산한다.  
Runtime View는 실행 검증을 위해 사전 계산된 결과다.

Ontology는 runtime hot path에서 직접 무거운 추론을 수행하지 않는다.  
필요한 의미 결과는 사전에 materialized view나 snapshot으로 변환된다.

---

## **10\. Evidence Flow**

Evidence는 판단의 근거다.

LEDO에서 중요한 판단은 Evidence 없이 신뢰될 수 없다.

Observation  
→ Source  
→ Timestamp  
→ Trust Metadata  
→ Provenance  
→ Evidence  
→ EvidenceBundle  
→ Decision Support  
→ Audit

Evidence의 핵심 원칙은 다음과 같다.

AI output은 Evidence가 아니다.  
Evidence는 출처와 시간을 가져야 한다.  
Evidence는 검증 상태를 가져야 한다.  
Evidence는 판단과 연결되어야 한다.  
Evidence는 Audit으로 추적 가능해야 한다.

AI는 Evidence를 요약할 수 있지만, Evidence 자체가 될 수 없다.

---

## **11\. State Flow**

World State는 현재 상태를 표현한다.

Ontology는 의미를 정의하지만, 모든 실시간 상태를 영구적인 ontology fact로 직접 저장하지 않는다.

Sensor / External Signal  
→ Ingestion  
→ Normalization  
→ Validation  
→ State Update  
→ World State Cache  
→ Event Detection  
→ Agent Interpretation

World State는 다음을 포함할 수 있다.

현재 위치  
현재 위험 상태  
현재 장비 상태  
현재 구역 제한 상태  
현재 승인 상태  
현재 외부 시스템 가용성  
현재 Evidence freshness

World State는 runtime decision을 위해 중요하지만, Ontology의 의미 권위를 대체하지 않는다.

---

## **12\. Decision Flow**

Decision Flow는 ActionCandidate가 실행 요청으로 발전하기까지의 경로다.

Agent Interpretation  
→ ActionCandidate  
→ Semantic Validation  
→ Evidence Check  
→ Policy Check  
→ Decision Routing  
→ Approval  
→ Safety Gate  
→ ExecutionRequest

각 단계의 책임은 다르다.

| 단계 | 책임 |
| ----- | ----- |
| Agent Interpretation | 상황을 해석하고 후보를 만든다 |
| ActionCandidate | 실행 후보를 표현한다 |
| Semantic Validation | 후보가 의미적으로 가능한지 확인한다 |
| Evidence Check | 판단 근거가 충분한지 확인한다 |
| Policy Check | 운영상 허용 가능한지 확인한다 |
| Decision Routing | 위험도와 승인 경로를 결정한다 |
| Approval | 고위험 권한을 부여한다 |
| Safety Gate | 실행 직전 준비 상태를 검증한다 |
| ExecutionRequest | 외부 시스템에 실행 요청을 전달한다 |

Decision Flow의 핵심 원칙은 다음과 같다.

후보는 실행이 아니다.  
승인은 물리 명령이 아니다.  
실행 요청은 물리 명령이 아니다.

---

## **13\. Execution Boundary**

LEDO는 물리 실행을 직접 수행하지 않는다.

LEDO는 다음을 정의한다.

intent  
target  
constraints  
approval reference  
evidence reference  
policy reference  
safety validation result  
trace id  
idempotency key

LEDO가 생성하는 ExecutionRequest는 외부 시스템에 대한 요청이다.

실제 물리 실행은 다음과 같은 외부 시스템이 담당한다.

Robot Middleware  
Fleet Manager  
PLC  
SCADA  
Access Control System  
Equipment Controller  
Site Operation System  
Safety-rated Controller

이 경계는 절대 유지되어야 한다.

---

## **14\. Safety Gate Architecture**

Safety Gate는 실행 직전의 최종 검증 계층이다.

Safety Gate는 다음을 판단한다.

승인이 유효한가?  
Evidence가 충분하고 최신인가?  
현재 상태가 실행 가능한가?  
정책 위반이 없는가?  
충돌 상태가 없는가?  
외부 시스템이 사용 가능한가?  
Snapshot이 유효한가?

Safety Gate는 runtime hot path에서 무거운 연산을 수행하지 않는다.

금지되는 항목은 다음과 같다.

OWL Reasoner  
Full SHACL Validation  
SPARQL Query  
Graph DB Network Call  
LLM / SLM Call  
External API Call  
Disk I/O  
Unbounded Computation

Safety Gate는 사전 계산된 Snapshot을 읽는다.

Precomputed Validation  
→ Materialized Safety Snapshot  
→ Deterministic Lookup  
→ Allow / Deny / Hold / Escalate

Safety Gate는 불확실하면 fail-closed한다.

---

## **15\. Source of Truth Matrix**

LEDO는 하나의 계층이 모든 진실을 독점하지 않는다.

각 영역의 Source of Truth는 분리된다.

| 영역 | Source of Truth |
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

이 분리는 LEDO의 안전성과 설명 가능성을 만든다.

---

## **16\. AI / Agent Boundary**

AI와 Agent는 LEDO에서 중요하지만 최종 권한을 갖지 않는다.

AI와 Agent는 다음을 할 수 있다.

Intent 해석  
상황 요약  
위험 해석  
MappingProposal 생성  
EvidenceSummary 생성  
ActionCandidate 생성  
PolicyImpactSuggestion 생성  
설명 생성

AI와 Agent는 다음을 할 수 없다.

Evidence 생성  
Policy Decision 확정  
Approval 부여  
Safety Gate Decision 수행  
ExecutionRequest 직접 확정  
ExternalControlRequest 직접 확정  
Physical Command 생성

AI output은 후보이며, 검증 대상이다.

---

## **17\. Registry Architecture**

Registry는 LEDO에서 통제된 어휘와 식별자를 관리한다.

Registry가 필요한 대상은 다음과 같다.

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

Registry의 목적은 다음과 같다.

임의 생성 방지  
버전 관리  
고정 어휘 통제  
검증 가능성 확보  
코드와 문서의 일관성 유지

Registry는 의미를 직접 정의하지 않는다.  
의미는 Ontology와 사양 문서가 정의한다.  
Registry는 정의된 의미를 안정적으로 참조하고 통제한다.

---

## **18\. Domain Extension Boundary**

LEDO의 Framework와 Domain Module은 분리되어야 한다.

Framework는 구조를 정의한다.

DTO  
Registry  
Validator  
Interface  
Adapter Boundary  
Audit Structure  
Safety Gate Contract

Domain Module은 도메인 의미를 정의한다.

산업별 객체  
현장별 상태  
도메인별 위험 유형  
도메인별 작업 유형  
도메인별 승인 기준  
도메인별 정책 매핑

도메인 의미는 임의로 생성되지 않는다.  
도메인 의미는 전문가 검토와 거버넌스를 통해 관리되어야 한다.

---

## **19\. Architecture Invariants**

LEDO 전체에서 반드시 유지되어야 하는 불변 조건은 다음과 같다.

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

이 불변 조건을 깨는 설계는 LEDO 아키텍처가 아니다.

---

## **20\. Final Architecture Statement**

LEDO는 온톨로지 중심의 Cyber-Physical AI 아키텍처다.

LEDO는 의미와 실행을 직접 연결하지 않는다.  
의미는 Ontology가 정의하고, 판단은 Evidence와 State를 기반으로 하며, 허가는 Policy가 판단하고, 고위험 권한은 Approval이 부여하며, 실행 준비는 Safety Gate가 검증하고, 물리 실행은 External System이 수행한다.

LEDO의 최종 구조는 다음과 같다.

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

최종 원칙은 다음과 같다.

Meaning must be explicit.  
Evidence must be traceable.  
State must be current.  
Policy must be enforceable.  
Approval must be auditable.  
Validation must be deterministic.  
Execution must be bounded.  
Safety must fail closed.  
Audit must preserve accountability.

