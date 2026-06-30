**README.md — 05 Domain Ontology Modules**

## **1\. Purpose**

`05_domain_ontology_modules` is the area for extending domain-specific meaning on top of the LEDO Ontology Core.

This folder does not predefine the rules of a specific industry.  
This folder defines how domain ontology modules can safely extend the Core Ontology Foundation.

The core structure of LEDO must remain an industry-neutral platform core, while domain-specific meaning must be separated into independent Domain Modules or Domain Packs.

---

## **2\. Core Principles**

Framework defines structure.

Domain Module defines domain meaning.

Domain meaning must be governed.

LEDO is not fixed to a single industry.

Domain Modules enable industry-specific extension and must follow these principles.

Domain meaning must not be generated arbitrarily.

Domain rules must be reviewed by domain experts.

Domain modules must follow Foundation principles.

Domain modules must be connected to Registries.

Domain modules must not bypass Runtime Validation.

Domain modules must not define physical execution commands.

---

## **3\. Responsibilities of This Folder**

`05_domain_ontology_modules` is responsible for:

Defining the structure of Domain Modules

Defining the domain extension contract

Defining the Domain Pack template

Defining how domain-specific Classes and Properties are extended

Defining how domain-specific Events, States, and Actions are extended

Defining how domain-specific Evidence, Policy, and Runtime Validation requirements are connected

Defining the boundary between Foundation and Domain Modules

This folder defines the container for domains.  
It does not arbitrarily define actual domain rules.

---

## **4\. What This Folder Does Not Own**

This folder does not directly define:

Real industrial safety standards

Real equipment operation rules

Real work permit rules

Real risk thresholds

Real legal interpretations

Real emergency procedures

Real robot behavior rules

Real PLC / SCADA command semantics

Site-specific approval authority

These must be defined in separate Domain Packs through domain expert review and governance.

---

## **5\. Role of a Domain Module**

A Domain Module extends domain-specific meaning on top of the Ontology Foundation.

A Domain Module may define:

Domain-specific object types

Domain-specific state types

Domain-specific event types

Domain-specific action candidate types

Domain-specific Evidence types

Domain-specific Policy references

Domain-specific Runtime Validation requirements

Domain-specific external system integration requirements

However, a Domain Module must not violate the non-negotiable boundaries of LEDO.

AI output is not Evidence.

ActionCandidate is not an execution command.

ApprovedAction is not a physical command.

ExecutionRequest is not a physical command.

Safety Gate must not be bypassed.

Physical Execution belongs to External Systems.

---

## **6\. Relationship to Foundation**

`04_ontology_foundation` defines common semantic principles.

`05_domain_ontology_modules` extends domain-specific meaning on top of those principles.

Ontology Foundation

→ Common semantic contract

Domain Ontology Modules

→ Domain-specific semantic extension

A Domain Module must follow the Foundation principles for Classes, Properties, Axioms, Constraints, Reasoning, and Governance.

A Domain Module does not replace the Foundation.

---

## **7\. Relationship to Core Specifications**

`03_core_specifications` defines operational contracts.

A Domain Module may connect to the operational objects defined by Core Specifications.

Examples:

Domain Event

→ CoreEvent

Domain ActionCandidate

→ ActionCandidate

Domain Evidence Type

→ Evidence Model

Domain Approval Requirement

→ Decision / Approval Model

Domain Execution Requirement

→ ExecutionRequest Model

A Domain Module must not bypass the Core object lifecycle.

---

## **8\. Relationship to Registry**

Fixed vocabularies defined by Domain Modules must be connected to Registries.

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

Domain Approval Requirement

→ Approval Registry

Registries prevent uncontrolled domain value creation and provide version control and validation support.

---

## **9\. Relationship to Runtime Validation**

A Domain Module may declare Runtime Validation requirements.

However, it must not directly extend the runtime hot path or insert heavy reasoning into the Safety Gate.

Domain-specific Runtime Validation requirements must follow this flow.

Domain Rule Requirement

→ Validation Specification

→ Registry Reference

→ Materialization Rule

→ Safety Snapshot

→ Safety Gate Lookup

Safety Gate must only read precomputed results.

---

## **10\. Recommended Structure**

At the initial stage, this folder should remain lightweight.

05\_domain\_ontology\_modules/

  README.md

  domain\_module\_contract.md

  domain\_pack\_template.md

Real industry-specific Domain Packs should be added after the Foundation, Registry, and Runtime Validation structures become stable.

Possible future extension structure:

05\_domain\_ontology\_modules/

  construction\_domain\_pack/

  manufacturing\_domain\_pack/

  logistics\_domain\_pack/

  energy\_domain\_pack/

  robotics\_domain\_pack/

Each Domain Pack must be managed independently and must not contaminate the common Framework.

---

## **11\. Minimum Domain Pack Structure**

Each Domain Pack should include at least:

domain\_name

domain\_scope

domain\_classes

domain\_properties

domain\_events

domain\_states

domain\_actions

domain\_evidence\_types

domain\_policy\_references

domain\_approval\_requirements

domain\_runtime\_validation\_requirements

domain\_registry\_extensions

external\_system\_assumptions

governance\_owner

version

Actual domain-specific values should be added only after expert review and approval.

---

## **12\. Final Principles**

`05_domain_ontology_modules` does not predefine a specific industry.

This folder defines the extension structure that allows multiple industry domains to safely build on top of the LEDO Core.

Platform first.

Domain later.

Structure first.

Meaning governed.

No domain guessing.

No safety shortcut.

Final principle:

Domain Modules extend meaning.

They do not override the architecture.

# **README.md — 05 Domain Ontology Modules**

## **1\. 목적**

`05_domain_ontology_modules`는 LEDO Ontology Core 위에 도메인별 의미를 확장하기 위한 영역이다.

이 폴더는 특정 산업의 규칙을 미리 확정하는 곳이 아니다.  
이 폴더는 도메인 온톨로지 모듈이 Core Ontology Foundation 위에서 안전하게 확장되는 방식을 정의하는 곳이다.

LEDO의 기본 구조는 산업 공통 코어로 유지되어야 하며, 도메인별 의미는 독립적인 Domain Module 또는 Domain Pack으로 분리되어야 한다.

---

## **2\. 핵심 원칙**

Framework defines structure.  
Domain Module defines domain meaning.  
Domain meaning must be governed.

LEDO는 특정 산업에 고정된 시스템이 아니다.

도메인 모듈은 산업별 확장을 가능하게 하는 구조이며, 다음 원칙을 따른다.

도메인 의미는 임의로 생성하지 않는다.  
도메인 규칙은 전문가 검토를 거친다.  
도메인 모듈은 Foundation 원칙을 따른다.  
도메인 모듈은 Registry와 연결된다.  
도메인 모듈은 Runtime Validation을 직접 우회하지 않는다.  
도메인 모듈은 물리 실행 명령을 정의하지 않는다.

---

## **3\. 이 폴더가 담당하는 것**

`05_domain_ontology_modules`는 다음을 담당한다.

도메인 모듈의 구조 정의  
도메인 확장 계약 정의  
도메인 팩 템플릿 정의  
도메인별 Class / Property 확장 방식 정의  
도메인별 Event / State / Action 확장 방식 정의  
도메인별 Evidence / Policy / Runtime Validation 연결 방식 정의  
Foundation과 Domain Module의 경계 정의

이 폴더는 도메인을 담는 그릇을 정의한다.  
도메인 규칙 자체를 임의로 확정하지 않는다.

---

## **4\. 이 폴더가 담당하지 않는 것**

이 폴더는 다음을 직접 확정하지 않는다.

실제 산업 안전 기준  
실제 장비 운전 규칙  
실제 작업 허가 기준  
실제 위험 임계값  
실제 법규 해석  
실제 비상 절차  
실제 로봇 행동 규칙  
실제 PLC / SCADA 명령 의미  
현장별 승인 권한

위 내용은 도메인 전문가의 검토와 거버넌스를 통해 별도 Domain Pack에서 정의되어야 한다.

---

## **5\. Domain Module의 역할**

Domain Module은 Ontology Foundation 위에서 특정 산업의 의미를 확장한다.

Domain Module은 다음을 정의할 수 있다.

도메인별 객체 유형  
도메인별 상태 유형  
도메인별 사건 유형  
도메인별 행동 후보 유형  
도메인별 Evidence 유형  
도메인별 Policy 참조  
도메인별 Runtime Validation 요구사항  
도메인별 외부 시스템 연계 요구사항

그러나 Domain Module은 LEDO의 절대 경계를 위반할 수 없다.

AI output은 Evidence가 아니다.  
ActionCandidate는 실행 명령이 아니다.  
ApprovedAction은 물리 명령이 아니다.  
ExecutionRequest는 물리 명령이 아니다.  
Safety Gate는 우회할 수 없다.  
Physical Execution은 External System이 담당한다.

---

## **6\. Foundation과의 관계**

`04_ontology_foundation`은 공통 의미 원칙을 정의한다.

`05_domain_ontology_modules`는 그 원칙 위에서 도메인별 의미를 확장한다.

Ontology Foundation  
→ 공통 의미 계약

Domain Ontology Modules  
→ 도메인별 의미 확장

Domain Module은 Foundation의 Class, Property, Axiom, Constraint, Reasoning, Governance 원칙을 따라야 한다.

Domain Module은 Foundation을 대체하지 않는다.

---

## **7\. Core Specifications와의 관계**

`03_core_specifications`는 운영 계약을 정의한다.

Domain Module은 Core Specification의 운영 객체와 연결될 수 있다.

예시는 다음과 같다.

Domain Event  
→ CoreEvent

Domain ActionCandidate  
→ ActionCandidate

Domain Evidence Type  
→ Evidence Model

Domain Approval Requirement  
→ Decision / Approval Model

Domain Execution Requirement  
→ ExecutionRequest Model

Domain Module은 Core 객체 생명주기를 우회하지 않는다.

---

## **8\. Registry와의 관계**

도메인 모듈에서 정의되는 고정 어휘는 Registry와 연결되어야 한다.

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

Domain Approval Requirement  
→ Approval Registry

Registry는 도메인 값의 무분별한 생성을 막고, 버전 관리와 검증 가능성을 제공한다.

---

## **9\. Runtime Validation과의 관계**

Domain Module은 Runtime Validation 요구사항을 선언할 수 있다.

그러나 Runtime hot path를 직접 확장하거나 무거운 추론을 삽입해서는 안 된다.

Domain Module의 Runtime Validation 요구사항은 다음 흐름을 따라야 한다.

Domain Rule Requirement  
→ Validation Specification  
→ Registry Reference  
→ Materialization Rule  
→ Safety Snapshot  
→ Safety Gate Lookup

Safety Gate는 사전 계산된 결과만 조회해야 한다.

---

## **10\. 권장 구조**

초기 단계에서는 이 폴더를 가볍게 유지한다.

05\_domain\_ontology\_modules/  
  README.md  
  domain\_module\_contract.md  
  domain\_pack\_template.md

실제 산업별 도메인 팩은 Foundation, Registry, Runtime Validation 구조가 안정된 뒤 추가한다.

예상 가능한 확장 구조는 다음과 같다.

05\_domain\_ontology\_modules/  
  construction\_domain\_pack/  
  manufacturing\_domain\_pack/  
  logistics\_domain\_pack/  
  energy\_domain\_pack/  
  robotics\_domain\_pack/

각 Domain Pack은 독립적으로 관리되어야 하며, 공통 Framework를 오염시키면 안 된다.

---

## **11\. Domain Pack 최소 구성**

각 Domain Pack은 최소한 다음 정보를 가져야 한다.

domain\_name  
domain\_scope  
domain\_classes  
domain\_properties  
domain\_events  
domain\_states  
domain\_actions  
domain\_evidence\_types  
domain\_policy\_references  
domain\_approval\_requirements  
domain\_runtime\_validation\_requirements  
domain\_registry\_extensions  
external\_system\_assumptions  
governance\_owner  
version

도메인별 실제 값은 전문가 검토와 승인 이후 추가한다.

---

## **12\. 최종 원칙**

`05_domain_ontology_modules`는 특정 산업을 미리 고정하는 곳이 아니다.

이 폴더는 여러 산업 도메인이 LEDO Core 위에 안전하게 올라올 수 있도록 확장 구조를 정의하는 곳이다.

Platform first.  
Domain later.  
Structure first.  
Meaning governed.  
No domain guessing.  
No safety shortcut.

최종 원칙은 다음과 같다.

Domain Modules extend meaning.  
They do not override the architecture.

