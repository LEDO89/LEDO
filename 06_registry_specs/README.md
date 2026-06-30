# **README.md — 06 Registry Specs**

## **1\. 목적**

`06_registry_specs`는 LEDO Ontology Core 전체에서 사용되는 통제된 어휘, 식별자, 버전, 상태, 참조 규칙을 정의하는 영역이다.

Registry는 시스템이 임의의 이름, 임의의 상태, 임의의 Action, 임의의 Event, 임의의 Adapter, 임의의 Snapshot 구조를 생성하지 못하도록 통제한다.

Registry는 의미를 직접 정의하지 않는다.  
의미는 Ontology와 Specification이 정의한다.  
Registry는 정의된 의미를 안정적으로 참조하고, 버전 관리하고, 검증 가능한 형태로 고정한다.

핵심 원칙은 다음과 같다.

Ontology defines meaning.  
Core Specifications define operational contracts.  
Registry controls names, identifiers, versions, and allowed vocabularies.  
Runtime Validation uses Registry for deterministic validation.  
Implementation uses Registry to generate enums, schemas, validators, and tests.

---

## **2\. Registry의 역할**

Registry는 LEDO 전체에서 다음 역할을 수행한다.

고정 어휘 통제  
식별자 통제  
버전 관리  
상태 관리  
참조 무결성 유지  
임의 생성 방지  
검증 가능성 확보  
코드와 문서의 일관성 유지  
도메인 확장 값의 등록 절차 제공

Registry는 단순한 목록이 아니다.

Registry는 문서, Ontology, Runtime Validation, Implementation 사이를 연결하는 통제 장치다.

---

## **3\. Registry가 아닌 것**

Registry는 다음을 수행하지 않는다.

도메인 의미를 직접 정의하지 않는다.  
실제 산업 규칙을 임의로 만들지 않는다.  
안전 기준이나 위험 임계값을 추정하지 않는다.  
물리 실행 명령을 정의하지 않는다.  
Ontology Foundation을 대체하지 않는다.  
Policy Engine을 대체하지 않는다.  
Safety Gate를 대체하지 않는다.

Registry는 의미의 주인이 아니다.  
Registry는 의미를 참조하는 식별자와 어휘의 통제자다.

---

## **4\. Registry의 전체 위치**

LEDO 구조에서 Registry는 모든 주요 계층과 연결된다.

Ontology Foundation  
→ 의미 정의

Core Specifications  
→ 운영 객체 계약 정의

Registry Specs  
→ 이름, 식별자, 어휘, 버전 통제

Runtime Validation  
→ Registry 기반 검증

Implementation  
→ Registry 기반 Enum, DTO, Validator, Test 생성

Domain Modules  
→ Domain-specific registry extension 제공

---

## **5\. 권장 폴더 구조**

`06_registry_specs`는 다음 구조를 기준으로 한다.

06\_registry\_specs/  
  README.md

  action\_registry/  
  approval\_registry/  
  decision\_registry/  
  event\_registry/  
  evidence\_registry/  
  policy\_registry/  
  state\_registry/

  adapter\_registry/  
  external\_system\_registry/  
  snapshot\_schema\_registry/  
  identity\_registry/  
  ontology\_registry/

향후 Agent와 SLM 구조가 안정된 뒤 다음 Registry를 추가할 수 있다.

 agent\_vocabulary\_registry/  
  model\_adapter\_registry/

---

## **6\. Registry 분류**

Registry는 크게 다섯 가지 범주로 나뉜다.

| 범주 | Registry | 역할 |
| ----- | ----- | ----- |
| Operational Registry | `action_registry`, `event_registry`, `state_registry`, `decision_registry`, `approval_registry`, `evidence_registry`, `policy_registry` | 운영 객체와 판단 흐름에서 사용되는 고정 어휘 통제 |
| Integration Registry | `adapter_registry`, `external_system_registry` | 외부 시스템 연결 방식과 실제 외부 대상 통제 |
| Runtime Registry | `snapshot_schema_registry` | Safety Gate Snapshot 구조와 버전 통제 |
| Semantic / Identity Registry | `ontology_registry`, `identity_registry` | Ontology 자원 식별자와 Canonical Identity 통제 |
| AI / Agent Registry | `agent_vocabulary_registry`, `model_adapter_registry` | 향후 Agent / SLM vocabulary 및 adapter compatibility 통제 |

초기 단계에서는 Operational, Integration, Runtime, Semantic / Identity Registry를 우선한다.

---

## **7\. Core Operational Registries**

Core Operational Registry는 LEDO의 판단 흐름에서 사용되는 고정 어휘를 관리한다.

### **7.1 Action Registry**

`action_registry`는 시스템이 인식할 수 있는 Action Type을 통제한다.

역할:

Action Type ID 관리  
Action Type 이름 관리  
ActionCandidate와 ApprovedAction에서 사용할 수 있는 Action 목록 관리  
Action Type별 target constraint 연결  
Action Type별 approval requirement 연결  
Action Type별 policy reference 연결  
Action Type별 runtime validation requirement 연결

Action Registry는 실제 물리 명령을 정의하지 않는다.

---

### **7.2 Event Registry**

`event_registry`는 시스템이 인식할 수 있는 Event Type을 통제한다.

역할:

Event Type ID 관리  
Event Type 이름 관리  
Event severity 연결  
Evidence requirement 연결  
World State update rule 참조  
Decision routing rule 참조  
Audit trace 연결

Event Registry는 실제 도메인 사건의 의미를 임의로 만들지 않는다.  
도메인별 Event Type은 Domain Module에서 정의되고 Registry에 등록된다.

---

### **7.3 State Registry**

`state_registry`는 시스템에서 사용하는 State Type과 State Value를 통제한다.

역할:

State Type ID 관리  
State Value 관리  
State transition reference 관리  
World State와 연결  
Safety Gate validation flag와 연결  
Runtime freshness requirement와 연결

State Registry는 현재 상태의 Source of Truth가 아니다.  
현재 상태의 Source of Truth는 Real-Time World State다.

---

### **7.4 Decision Registry**

`decision_registry`는 DecisionCase, routing decision, escalation type을 통제한다.

역할:

Decision Type ID 관리  
Decision outcome 관리  
Decision tier 관리  
Escalation category 관리  
Risk routing category 관리  
Approval path reference 연결  
Audit requirement 연결

Decision Registry는 최종 실행 권한을 부여하지 않는다.

---

### **7.5 Approval Registry**

`approval_registry`는 승인 유형과 승인 상태를 통제한다.

역할:

Approval Type 관리  
Approval State 관리  
Approval requirement reference 관리  
Approver role reference 관리  
Validity condition reference 관리  
Expiration rule reference 관리  
Audit requirement 연결

Approval Registry는 실제 승인 권한자를 임의로 결정하지 않는다.  
도메인별 승인 권한은 Domain Module과 Governance / Policy 구조에서 정의된다.

---

### **7.6 Evidence Registry**

`evidence_registry`는 Evidence Type과 Evidence requirement를 통제한다.

역할:

Evidence Type ID 관리  
Evidence source type 관리  
Evidence trust requirement 연결  
Timestamp requirement 연결  
Provenance requirement 연결  
Validation status 관리  
EvidenceBundle 구성 기준 연결

Evidence Registry는 Evidence 자체가 아니다.  
Evidence는 source, timestamp, trust metadata, provenance, validation status를 가진 실제 판단 근거다.

---

### **7.7 Policy Registry**

`policy_registry`는 Policy Reference와 Policy Category를 통제한다.

역할:

Policy ID 관리  
Policy category 관리  
Policy version reference 관리  
Policy engine reference 관리  
Action Type과 Policy 연결  
Approval requirement와 Policy 연결  
Runtime validation requirement와 Policy 연결

Policy Registry는 Policy Engine을 대체하지 않는다.  
Policy Registry는 어떤 정책을 참조해야 하는지 통제한다.

---

## **8\. Integration Registries**

Integration Registry는 외부 시스템 연결 구조를 통제한다.

### **8.1 Adapter Registry**

`adapter_registry`는 외부 시스템과 연결하는 Adapter의 종류, 모드, 프로토콜, 안전 경계를 관리한다.

역할:

Adapter ID 관리  
Adapter Type 관리  
Protocol 관리  
Mock / Dry-run / Production mode 구분  
Supported Action Type 관리  
Supported External System Type 관리  
Health Check Contract 관리  
Feedback Contract 관리  
Safety Boundary 관리  
Version 관리

Adapter Registry는 실제 외부 시스템의 물리 실행 권한을 소유하지 않는다.

Adapter는 요청을 전달하는 경계다.

---

### **8.2 External System Registry**

`external_system_registry`는 실제 연결 대상이 되는 외부 시스템을 관리한다.

역할:

External System ID 관리  
External System Type 관리  
Authority Boundary 정의  
Allowed Request Type 관리  
Operational Mode 관리  
Health Status Reference 관리  
Safety Responsibility Owner 관리  
Feedback Contract 관리  
Adapter Reference 연결

External System은 실제 물리 실행 권한을 가진다.

LEDO는 ExecutionRequest를 만들 수 있지만, 실제 물리 실행은 External System이 수행한다.

---

## **9\. Runtime Registry**

### **9.1 Snapshot Schema Registry**

`snapshot_schema_registry`는 Safety Gate가 읽는 Materialized Safety Snapshot의 구조와 버전을 통제한다.

역할:

Snapshot Schema ID 관리  
Snapshot Schema Version 관리  
Compatible Ontology Version 관리  
Compatible Policy Version 관리  
Compatible SHACL Shape Version 관리  
Required Materialized Map 정의  
Required Field 정의  
Checksum Rule 정의  
Expiration Rule 정의  
Fail-closed Condition 정의  
Hot-swap Compatibility 정의

Safety Gate는 runtime hot path에서 Snapshot Schema Registry를 기준으로 검증된 Snapshot만 읽어야 한다.

Snapshot Schema가 맞지 않으면 Safety Gate는 fail-closed해야 한다.

---

## **10\. Semantic / Identity Registries**

### **10.1 Identity Registry**

`identity_registry`는 외부 식별자와 내부 Canonical Identity의 연결을 통제한다.

역할:

Canonical ID 관리  
External ID 관리  
Source System 관리  
Identifier Scheme 관리  
Mapping Rule 관리  
Resolution Evidence 관리  
Confidence 관리  
Validity Period 관리  
Governance Status 관리

Identity Registry는 다음을 연결한다.

IFC GlobalId  
OPC-UA NodeId  
Robot ID  
Sensor ID  
Worker ID  
Equipment ID  
Zone ID  
Canonical Object ID

Identity Registry는 `sameAs`를 임의로 선언하지 않는다.  
동일성 판단은 Evidence와 Governance를 통해 관리되어야 한다.

---

### **10.2 Ontology Registry**

`ontology_registry`는 Ontology 자원의 식별자, 버전, 상태를 통제한다.

역할:

Class IRI 관리  
Property IRI 관리  
Ontology Module 관리  
Ontology Version 관리  
Deprecation Status 관리  
Replacement IRI 관리  
SHACL Reference 연결  
Policy Reference 연결  
Runtime Materialization Reference 연결  
Governance Status 관리

Ontology Registry는 의미를 직접 정의하지 않는다.

Ontology Foundation \= 의미 정의  
Ontology Registry \= 의미 자원 식별자와 버전 통제

---

## **11\. Future AI / Agent Registries**

Agent와 SLM 구조가 안정된 뒤 다음 Registry를 추가할 수 있다.

### **11.1 Agent Vocabulary Registry**

`agent_vocabulary_registry`는 Agent / SLM이 사용하는 고정 어휘, action phrases, ontology labels, SKOS terms, prompt-safe vocabulary를 관리한다.

역할:

Agent vocabulary version 관리  
Ontology label reference 관리  
SKOS term reference 관리  
Allowed output vocabulary 관리  
Forbidden output role 관리  
Agent-specific terminology 관리

---

### **11.2 Model Adapter Registry**

`model_adapter_registry`는 LoRA, SFT, DAPT, agent-specific adapter compatibility를 관리한다.

역할:

Model adapter ID 관리  
Base model reference 관리  
LoRA adapter version 관리  
Compatible ontology version 관리  
Compatible vocabulary version 관리  
Evaluation status 관리  
Promotion status 관리  
Rollback target 관리

이 Registry는 SLM / Agent 운영 구조가 본격화된 뒤 추가한다.

---

## **12\. Registry Entry 공통 필드**

모든 Registry는 가능한 경우 다음 공통 필드를 가진다.

registry\_id  
name  
description  
category  
version  
status  
owner\_module  
source\_document  
validation\_reference  
policy\_reference  
ontology\_reference  
runtime\_reference  
governance\_status  
created\_at  
updated\_at  
deprecated\_since  
replacement\_id

Registry별로 필요한 추가 필드는 각 하위 Registry 문서에서 정의한다.

---

## **13\. Registry Status**

Registry 항목은 다음 상태를 가질 수 있다.

draft  
active  
deprecated  
migration\_required  
retired  
blocked

상태 의미는 다음과 같다.

| Status | 의미 |
| ----- | ----- |
| `draft` | 아직 확정되지 않은 항목 |
| `active` | 현재 사용 가능한 항목 |
| `deprecated` | 더 이상 권장되지 않지만 아직 제거되지 않은 항목 |
| `migration_required` | 대체 항목으로 이전이 필요한 항목 |
| `retired` | 사용 종료된 항목 |
| `blocked` | 안전, 정책, 호환성 문제로 사용 금지된 항목 |

---

## **14\. Registry와 Domain Module의 관계**

Domain Module은 새로운 domain-specific 값을 정의할 수 있다.

그러나 그 값은 Registry에 등록되어야 한다.

Domain Action Type  
→ Action Registry

Domain Event Type  
→ Event Registry

Domain State Type  
→ State Registry

Domain Evidence Type  
→ Evidence Registry

Domain Policy Reference  
→ Policy Registry

Domain Adapter Requirement  
→ Adapter Registry

Domain External System  
→ External System Registry

Domain Snapshot Requirement  
→ Snapshot Schema Registry

Domain Module은 Registry를 우회할 수 없다.

---

## **15\. Registry와 Implementation의 관계**

Implementation은 Registry를 기준으로 생성되어야 한다.

Registry는 다음 구현 산출물의 기준이 된다.

Enum  
DTO field constraint  
Validator  
State transition table  
Failure mode table  
Safety Gate input contract  
Snapshot schema  
Adapter interface  
Mock behavior  
Test case  
Migration rule

Registry가 없는 값은 구현에서 임의로 생성하지 않는다.

---

## **16\. 최종 원칙**

`06_registry_specs`는 LEDO 전체의 통제된 이름 체계다.

Registry는 의미를 정의하지 않지만, 의미를 참조하는 이름, 식별자, 버전, 상태를 통제한다.

Ontology defines meaning.  
Registry controls references.  
Validation enforces contracts.  
Implementation follows Registry.  
Domain extensions must register.

최종 원칙은 다음과 같다.

No uncontrolled names.  
No uncontrolled identifiers.  
No uncontrolled action types.  
No uncontrolled external adapters.  
No uncontrolled snapshots.  
No uncontrolled domain extensions.

