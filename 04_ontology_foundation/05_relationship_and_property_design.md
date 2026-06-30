**Relationship and Property Design**

## **1\. Purpose**

This document defines the principles for designing relationships and properties in the LEDO Industrial Ontology Foundation.

In LEDO, a relationship is not merely a graph edge. A relationship is a **semantic contract** that fixes the meaning between objects, agents, sensors, events, risks, evidence, policies, action candidates, approvals, execution requests, and external control systems.

The purpose of this document is to clarify the following.

How should Object Properties and Data Properties be separated?

How should relationships connect to SHACL, SPARQL, Policy, and the Safety Gate?

How should RDF relations be transformed into materialized maps for the runtime hot path?

How should missing values be represented without polluting the graph?

How should property chains, inverse properties, and transitive relations be restricted?

How should properties be managed through registry and governance?

The core principles are as follows.

A Class defines a semantic category.

A Property defines a semantic relationship.

A Relationship connects reasoning, validation, policy, audit, and execution boundaries.

The Safety Gate does not directly traverse RDF relations; it only looks up materialized relations.

---

## **2\. Document Location**

This document belongs to the following location.

04\_ontology\_foundation/

  05\_relationship\_and\_property\_design/

    relationship\_and\_property\_design.md

This document connects to the following documents.

01\_semantic\_web\_technology\_stack

03\_owl\_modeling\_principles

04\_reasoning\_and\_constraint\_model

03\_core\_specifications/

  01\_common\_schema\_dto

  05\_evidence\_model

  07\_decision\_approval\_matrix

  08\_policy\_governance\_model

  09\_execution\_adapter\_model

  10\_audit\_observability\_model

06\_runtime\_validation/

  safety\_gate/

    safety\_gate\_validation\_rules.md

While `OWL Modeling Principles` covers the general principles of classes, axioms, domain/range, inverse properties, transitive properties, and functional properties, this document focuses on how those properties connect to **runtime validation, materialized relation maps, and Safety Gate lookup**.

---

## **3\. Core Meaning of Relationships**

Relationships in LEDO must answer the following questions.

Who generated it?

What was observed?

What is the supporting evidence?

Which risk affects which space?

Which action mitigates which risk?

Which policy restricts which action?

Which approval approved which action?

Which ExecutionRequest was delivered to which external system?

Which feedback proves which execution result?

Examples are as follows.

GasRisk\_01 ot:affects Zone\_A .

EvidenceBundle\_01 ot:supportedBy SensorObservation\_01 .

ActionCandidate\_01 ot:hasTarget Zone\_A .

ActionCandidate\_01 ot:hasEvidence EvidenceBundle\_01 .

ApprovedAction\_01 ot:derivedFromCandidate ActionCandidate\_01 .

ExecutionRequest\_01 ot:sentToExternalSystem VentilationController\_03 .

AuditRecord\_01 ot:usedSnapshotVersion SafetyGateSnapshot\_0007 .

The core principle is as follows.

A relationship is not a graph edge; it is a semantic contract.

---

## **4\. Property Types**

LEDO separates properties as follows.

| Property Type | Meaning | Examples |
| ----- | ----- | ----- |
| Object Property | Relationship between individuals | `generatedBy`, `supportedBy`, `affects`, `hasTarget` |
| Data Property | Relationship between an individual and a literal value | `hasTimestamp`, `hasStatus`, `hasConfidence` |
| Annotation Property | Label, comment, definition, version | `rdfs:label`, `skos:prefLabel`, `rdfs:comment` |
| Mapping Property | Connection to external standards or external systems | `hasExternalIdentifier`, `externallyMappedTo` |
| Provenance Property | Source, evidence, and lineage connection | `wasDerivedFrom`, `hasProvenance` |
| Materialized Relation | Precomputed relation used in the Safety Gate snapshot | `relation_allowed_map`, `action_permission_map` |

The important boundary is as follows.

A Materialized Relation is not an OWL property itself.

A Materialized Relation is a runtime lookup structure flattened from OWL / SHACL / SPARQL / Policy results.

---

## **5\. Object Property Design Principles**

An Object Property defines a semantic relationship between individuals.

Representative properties include:

locatedIn

observes

generatedBy

supportedBy

requires

authorizes

mitigates

affects

hasTarget

hasEvidence

hasCapability

requiresCapability

derivedFrom

sentToExternalSystem

hasExecutionResult

hasFeedback

Simple usage examples are as follows.

SensorObservation\_01 ot:generatedBy GasSensor\_01 .

GasSensor\_01 ot:observes Zone\_A .

GasRisk\_01 ot:affects Zone\_A .

ActionCandidate\_01 ot:hasTarget Zone\_A .

ActionCandidate\_01 ot:mitigates GasRisk\_01 .

ExecutionRequest\_01 ot:sentToExternalSystem PLC\_01 .

Before creating an Object Property, check the following.

Is the direction of the relationship clear?

Can an existing property represent it?

Is it needed for SHACL, SPARQL, or Policy validation?

Is it needed for audit traceability?

Should it be materialized into the Safety Gate snapshot?

The core principle is as follows.

An Object Property expresses a semantic relationship.

An Object Property is not a link created merely for implementation convenience.

---

## **6\. Data Property Design Principles**

A Data Property connects an individual to a literal value.

Representative properties include:

hasTimestamp

hasStatus

hasConfidence

hasRiskLevel

hasBatteryLevel

hasTemperature

hasGasConcentration

hasSourceSystem

hasChecksum

hasSnapshotVersion

Simple usage examples are as follows.

SensorObservation\_01 ot:hasTimestamp "2026-06-25T09:00:00Z"^^xsd:dateTime .

SensorObservation\_01 ot:hasGasConcentration "45.2"^^xsd:decimal .

SensorObservation\_01 ot:hasConfidence "0.98"^^xsd:decimal .

SafetyGateSnapshot\_0007 ot:hasChecksum "sha256:..." .

Before creating a Data Property, check the following.

Is the datatype clear?

Is a unit required?

Is a QUDT reference required?

Does the value change over time?

Is the value stable enough to be stored in the RDF graph?

Should high-frequency telemetry be stored in a time-series store instead?

Should it enter the Safety Gate snapshot as a flag or compact value?

The core principle is as follows.

Stable semantic attributes may be stored in the RDF graph.

High-frequency runtime values should be stored in the time-series or world state store, while RDF keeps only the necessary references.

---

## **6.1 Null / Void / Missing Value Representation**

Data Properties must not use sentinel values such as empty strings, `"null"`, `"N/A"`, `"unknown"`, or `-9999`.

If the data does not actually exist, the corresponding data property triple must not be created.

Forbidden examples:

SensorObservation\_01 ot:hasGasConcentration "" .

SensorObservation\_01 ot:hasGasConcentration "N/A" .

SensorObservation\_01 ot:hasGasConcentration "-9999"^^xsd:decimal .

SensorObservation\_01 ot:hasGasConcentration "null" .

These values can remain in the graph as if they were real measurements and contaminate SPARQL queries, SLM training data, statistical analysis, and Safety Gate Snapshot generation.

Allowed handling:

If the value does not exist, do not create the ot:hasGasConcentration triple.

Detect the missing value through SHACL sh:minCount 1 failure.

Represent sensor fault, disconnection, or timeout as a separate ObservationState or SensorFaultEvent.

Example:

SensorObservation\_01 rdf:type ot:GasObservation .

SensorObservation\_01 ot:generatedBy ot:GasSensor\_01 .

SensorObservation\_01 ot:hasTimestamp "2026-06-25T09:00:00Z"^^xsd:dateTime .

SensorObservation\_01 ot:hasObservationState ot:MissingValueState .

SensorFaultEvent\_01 rdf:type ot:SensorFaultEvent .

SensorFaultEvent\_01 ot:affects ot:GasSensor\_01 .

SensorFaultEvent\_01 ot:hasFaultType ot:SignalDisconnected .

SHACL example:

GasObservationShape

  sh:property \[

    sh:path ot:hasGasConcentration ;

    sh:minCount 1 ;

    sh:datatype xsd:decimal ;

  \] .

The core principle is as follows.

A missing value is not a literal value.

A missing value is represented as a validation failure or a state/event.

---

## **7\. Annotation Property Design Principles**

Annotation Properties represent human-readable descriptions, labels, comments, versions, and documentation metadata.

Examples include:

rdfs:label

rdfs:comment

skos:prefLabel

skos:altLabel

skos:definition

owl:versionInfo

Annotation Properties are not directly used for reasoning or runtime validation.

Their purposes include:

Terminology explanation

Multilingual labels

Documentation

Standards mapping explanation

Developer understanding support

SLM training vocabulary support

The core principle is as follows.

Annotation is explanation.

Annotation must not be used as runtime decision logic.

---

## **8\. Property Naming Principles**

Property names must clearly express direction and meaning.

Good examples include:

generatedBy

supportedBy

hasEvidence

hasTarget

affects

mitigates

requiresPermit

approvedBy

derivedFrom

sentToExternalSystem

hasExecutionResult

hasFeedback

Avoid the following examples.

relatesTo

connectedTo

hasData

link

ref

nodeToNode

objectInfo

usesThing

The core principle is as follows.

A property name must reveal the meaning and direction of the relationship.

---

## **9\. Foundation Property Families**

In the LEDO Foundation, properties are managed by functional families.

| Family | Representative Properties | Purpose |
| ----- | ----- | ----- |
| Identity / Mapping | `hasIdentifier`, `hasExternalIdentifier`, `externallyMappedTo` | Connect external systems to canonical identity |
| Spatial | `locatedIn`, `containsZone`, `hasBoundary`, `hasGeofence` | Represent zones, locations, and boundaries |
| Observation / Evidence | `observes`, `generatedBy`, `hasEvidence`, `wasDerivedFrom` | Connect observations, evidence, and provenance |
| Risk / Safety | `affects`, `mitigates`, `hasRiskLevel`, `hasRestriction` | Represent risk, impact, and mitigation |
| Action / Decision | `hasActionType`, `hasTarget`, `requiresApproval`, `approvedBy` | Connect action candidates and approvals |
| Execution / Feedback | `sentToExternalSystem`, `hasExecutionResult`, `hasFeedback` | Connect execution requests and feedback |
| Capability / Task | `hasCapability`, `requiresCapability`, `assignedTo` | Connect agent capabilities and tasks |
| Audit / Trace | `usedSnapshotVersion`, `usedPolicyVersion`, `hasReasonCode` | Trace decision paths |

The core principle is as follows.

A property family is a management unit for design consistency.

A property family must also have runtime materialization and governance criteria.

---

## **10\. Domain / Range Design Summary**

The detailed principles for Domain and Range are covered in `03_owl_modeling_principles`.  
This document summarizes only the runtime connection perspective.

The domain and range of Foundation properties must not be too narrow.

A risky example is:

hasTarget rdfs:range Zone .

If the following triple is added:

ActionCandidate\_01 ot:hasTarget RobotAgent\_01 .

the reasoner may infer:

RobotAgent\_01 rdf:type Zone .

A safer Foundation design is:

hasTarget rdfs:domain ActionCandidate .

hasTarget rdfs:range Entity .

Specific target constraints by action type are handled by SHACL, Policy, and the Safety Gate Snapshot.

restrict\_access → target must be Zone

dispatch\_robot → target may be RobotAgent or Task

request\_inspection → target may be Zone, System, or PhysicalObject

notify\_manager → target may be HumanAgent or Role

The core principle is as follows.

Foundation domain/range should remain broad.

Specific validation belongs to SHACL, SPARQL, Policy, and the Safety Gate Snapshot.

---

## **11\. Summary of Inverse / Transitive / Functional Property Restrictions**

The detailed principles for this area are covered in `03_owl_modeling_principles`.  
This document summarizes only the relationship runtime risk perspective.

### **11.1 Inverse Property**

An Inverse Property is used only when the relationship is an exact reverse relation.

generatedBy inverseOf generates

locatedIn inverseOf containsEntity

Do not create inverse properties merely for query convenience.

---

### **11.2 Transitive Property**

A Transitive Property is used only when the relationship is truly transitive.

Possible candidates:

isPartOf

locatedWithin

subZoneOf

dependsOn

Relationships requiring caution:

controls

observes

affects

supports

authorizes

mitigates

These are not always transitive in the real world.

---

### **11.3 Functional / InverseFunctional Property**

FunctionalProperty and InverseFunctionalProperty must be used very restrictively.

For example, declaring `hasLocation` as a FunctionalProperty makes it difficult to represent current location, estimated location, last known location, and design location.

Declaring `hasSerialNumber` as an InverseFunctionalProperty may cause incorrect identity merging due to external system errors or vendor duplication.

The core principle is as follows.

Strong property characteristics must be minimized.

Identity must be resolved through evidence and governance.

Runtime validation belongs to the Safety Gate Snapshot.

---

## **11.4 Property Chain Axiom Restriction**

`owl:propertyChainAxiom` is a powerful OWL feature that combines multiple property paths into a single inferred relationship.

In the LEDO Foundation, property chain axioms are prohibited by default. If needed, they may be used only in Domain Modules under strict constraints.

The following combinations are prohibited without governance review.

Combination of owl:inverseOf and owl:propertyChainAxiom

Combination of owl:TransitiveProperty and owl:propertyChainAxiom

Cyclic chains within the same property family

Property chains directly used for Safety Gate runtime decisions

The reason is as follows.

When property chains and inverse relations are combined,

unexpected relation closure,

inference expansion,

cyclic relation growth,

and increased runtime materialization can occur.

Allowed conditions are as follows.

The property chain must be acyclic.

It must be defined in a Domain Module, not the Foundation Layer.

It must pass reasoner consistency tests.

Its inferred result must be materialized once in an offline / async worker.

The Safety Gate hot path must not execute property chain reasoning directly.

The result must be looked up only through relation\_allowed\_map or relation\_closure\_map.

The core principle is as follows.

A property chain is not a runtime reasoning tool.

A property chain is an offline semantic expansion tool.

---

## **12\. Relationship Validation and Runtime Materialization Matrix**

A property does not end at definition.  
Each relationship must have a validation layer and a runtime usage location.

| Relationship | Meaning | Validation Layer | Runtime Use |
| ----- | ----- | ----- | ----- |
| `generatedBy` | Observation generated by Sensor/Agent | SHACL, SPARQL | evidence provenance |
| `supportedBy` | Candidate supported by EvidenceBundle | SPARQL, Evidence Check | evidence sufficiency |
| `affects` | Risk affects Zone/System | SPARQL, Spatial Check | risk\_action\_matrix |
| `mitigates` | Action mitigates Risk | OWL, SPARQL, Policy | risk\_action\_matrix |
| `hasTarget` | Target of ActionCandidate | SHACL, Policy | action\_permission\_map |
| `requiresPermit` | Task/Action requires permit | OWL, Policy | permit\_validity\_map |
| `approvedBy` | Action approved by approver | Policy, Audit | approval\_state\_map |
| `sentToExternalSystem` | ExecutionRequest sent to external system | Execution Adapter, Audit | execution trace |
| `hasFeedback` | Execution result linked to feedback | Audit, Feedback Handler | reconciliation |
| `usedSnapshotVersion` | Decision used a specific snapshot | Audit | traceability |

The core principle is as follows.

Important relationships must have both a validation layer and a runtime usage location.

---

## **13\. Safety Gate Materialized Relation**

The Safety Gate does not directly traverse OWL properties.

The Safety Gate looks up precomputed compact relation maps.

Examples are as follows.

relation\_allowed\_map:

  GasRisk\_01 affects Zone\_A → true

  Evidence\_01 supports ActionCandidate\_01 → true

  RobotAgent\_01 directlyControls Valve\_01 → false

action\_permission\_map:

  RobotAgent\_01 \+ dispatch\_robot \+ InspectionTask\_77 → allowed

  RobotAgent\_01 \+ direct\_physical\_control \+ Valve\_01 → denied

risk\_action\_matrix:

  GasRisk \+ restrict\_access → allowed\_mitigation

  GasRisk \+ notify\_manager → allowed\_mitigation

  GasRisk \+ resume\_work → denied

zone\_restriction\_map:

  Zone\_A → restricted

  Zone\_B → speed\_limited

  Zone\_C → normal

The core principle is as follows.

Ontology properties create meaning.

Materialized relation maps enable runtime lookup.

The Safety Gate reads only materialized relations.

---

## **14\. Property Registry**

LEDO must manage properties through a registry.

A property registry entry includes:

property\_iri

property\_label

property\_type

property\_family

domain

range

inverse\_of

property\_chain\_participation

is\_transitive

is\_functional

is\_inverse\_functional

shacl\_shape\_reference

sparql\_validation\_reference

policy\_reference

materialized\_map\_reference

used\_in\_safety\_gate

governance\_status

owner\_module

version

Example:

property\_iri: ot:supportedBy

property\_label: supported by

property\_type: object\_property

property\_family: evidence

domain: ot:ActionCandidate

range: ot:EvidenceBundle

inverse\_of: ot:supportsCandidate

property\_chain\_participation: false

is\_transitive: false

is\_functional: false

is\_inverse\_functional: false

shacl\_shape\_reference: ActionCandidateShape

sparql\_validation\_reference: EvidenceSupportAskQuery

policy\_reference: EvidenceSufficiencyPolicy

materialized\_map\_reference: relation\_allowed\_map

used\_in\_safety\_gate: true

governance\_status: approved

owner\_module: evidence\_model

version: 1.0.0

The core principle is as follows.

Properties must be managed like code.

A property must have an owner, version, validation references, and governance status.

---

## **15\. Property Creation Procedure**

When creating a new property, follow only the essential procedure below.

1\. Define the meaning of the relationship

2\. Check whether an existing property can be reused

3\. Classify it as Object / Data / Annotation / Mapping property

4\. Decide whether it belongs to the Foundation or a Domain Module

5\. Define domain and range

6\. Decide whether it participates in inverse, transitive, functional, or property chain behavior

7\. Define missing value handling

8\. Decide whether SHACL / SPARQL / Policy validation is required

9\. Decide whether Safety Gate materialization is required

10\. Register it in the Property Registry and perform Governance Review

The core principle is as follows.

A property must not be created impulsively.

A property must be registered only after its meaning, validation, and runtime usage are confirmed.

---

## **16\. Anti-Patterns**

| Anti-pattern | Problem | Alternative |
| ----- | ----- | ----- |
| Representing every relationship as `relatedTo` | Meaning disappears | Use specific properties |
| Setting domain/range too narrowly | Incorrect inference occurs | Keep Foundation broad; use SHACL/Policy for specific validation |
| Overusing inverse properties for query convenience | Graph complexity increases | Use inverse only for exact reverse relations |
| Overusing property chains in the Foundation | Inference expansion and relation closure increase | Use only in Domain Modules under constraints |
| Merging external IDs with `sameAs` | Identity pollution | Use mapping properties and evidence |
| Representing missing values as `""`, `"N/A"`, or `-9999` | Graph and training data contamination | Drop triple \+ SHACL minCount failure |
| Fixing runtime state as a TBox property | State change cannot be represented | Use State/Event/World State |
| Directly traversing RDF relations in the Safety Gate | Hot path latency increases | Use materialized relation maps |
| Adding properties without a property registry | Governance becomes impossible | Manage through registry |
| Treating AI output as Evidence | Hallucination contaminates evidence | Separate AI output as candidate |

---

## **17\. Final Operating Principles**

A relationship is a semantic contract.

An Object Property represents a semantic relationship between individuals.

A Data Property represents a literal value.

A missing value must not be represented as a literal.

An Annotation Property is used for explanation and vocabulary support.

A Mapping Property connects external systems to canonical identity.

Foundation domain/range should remain broad.

Specific validation belongs to SHACL, SPARQL, Policy, and Safety Gate Snapshot.

An Inverse Property is used only for exact reverse relations.

Property Chain Axioms are prohibited by default in the Foundation and allowed only restrictively in Domain Modules.

Transitive / Functional / InverseFunctional Properties must be used very carefully.

The Safety Gate does not directly traverse RDF relations; it looks up materialized relation maps.

Properties are managed through registry and governance.

---

## **18\. Final Conclusion**

The core of LEDO Relationship and Property Design is not to create many properties.

The core is to clearly define the semantic relationships of the industrial world and fix how those relationships connect to reasoning, validation, policy, evidence, audit, and execution boundaries.

The final structure is as follows.

OWL Property

→ semantic relation definition

SHACL

→ data and shape validation

SPARQL / Graph Query

→ relation consistency validation

Policy

→ operational permission interpretation

Materialized Relation Map

→ runtime lookup structure

Safety Gate

→ deterministic lookup and final pre-execution decision

Audit

→ relationship-based traceability

The final principle is as follows.

Class defines what something is.

Property defines how things are related.

Constraint validates whether the relationship is acceptable.

Policy decides whether the relationship is operationally allowed.

Snapshot materializes runtime-ready relationships.

Safety Gate reads only the materialized result.

# 

# 

# 

# 

# 

# 

# 

# 

# 

# **Relationship and Property Design**

## **1\. 목적**

이 문서는 LEDO Industrial Ontology Foundation에서 relationship과 property를 설계하는 원칙을 정의한다.

LEDO에서 relationship은 단순한 graph edge가 아니다. Relationship은 객체, 에이전트, 센서, 이벤트, 위험, 증거, 정책, 행동 후보, 승인, 실행 요청, 외부 제어 시스템 사이의 의미적 연결을 고정하는 **semantic contract**다.

이 문서의 목적은 다음을 명확히 하는 것이다.

Object Property와 Data Property를 어떻게 구분할 것인가?  
Relationship을 SHACL, SPARQL, Policy, Safety Gate와 어떻게 연결할 것인가?  
Runtime hot path에서 RDF relation을 어떻게 materialized map으로 변환할 것인가?  
Missing value를 어떻게 graph 오염 없이 표현할 것인가?  
Property chain, inverse, transitive 관계를 어떻게 제한할 것인가?  
Property를 registry와 governance로 어떻게 관리할 것인가?

핵심 원칙은 다음과 같다.

Class는 의미 범주다.  
Property는 의미 관계다.  
Relationship은 reasoning, validation, policy, audit, execution boundary를 연결한다.  
Safety Gate는 RDF relation을 직접 탐색하지 않고 materialized relation만 조회한다.

---

## **2\. 문서 위치**

이 문서는 다음 위치에 속한다.

04\_ontology\_foundation/  
  05\_relationship\_and\_property\_design/  
    relationship\_and\_property\_design.md

이 문서는 다음 문서들과 연결된다.

01\_semantic\_web\_technology\_stack  
03\_owl\_modeling\_principles  
04\_reasoning\_and\_constraint\_model

03\_core\_specifications/  
  01\_common\_schema\_dto  
  05\_evidence\_model  
  07\_decision\_approval\_matrix  
  08\_policy\_governance\_model  
  09\_execution\_adapter\_model  
  10\_audit\_observability\_model

06\_runtime\_validation/  
  safety\_gate/  
    safety\_gate\_validation\_rules.md

`OWL Modeling Principles`가 class, axiom, domain/range, inverse, transitive, functional property의 일반 원칙을 다룬다면, 이 문서는 그 property들이 **runtime validation, materialized relation map, Safety Gate lookup**으로 어떻게 연결되는지를 중심으로 다룬다.

---

## **3\. Relationship의 핵심 의미**

Relationship은 LEDO에서 다음 질문에 답할 수 있어야 한다.

누가 생성했는가?  
무엇을 관측했는가?  
무엇을 근거로 삼았는가?  
어떤 위험이 어떤 공간에 영향을 주는가?  
어떤 action이 어떤 risk를 완화하는가?  
어떤 policy가 어떤 action을 제한하는가?  
어떤 approval이 어떤 action을 승인했는가?  
어떤 ExecutionRequest가 어떤 external system으로 전달되었는가?  
어떤 feedback이 어떤 execution 결과를 증명하는가?

예시는 다음과 같다.

GasRisk\_01 ot:affects Zone\_A .  
EvidenceBundle\_01 ot:supportedBy SensorObservation\_01 .  
ActionCandidate\_01 ot:hasTarget Zone\_A .  
ActionCandidate\_01 ot:hasEvidence EvidenceBundle\_01 .  
ApprovedAction\_01 ot:derivedFromCandidate ActionCandidate\_01 .  
ExecutionRequest\_01 ot:sentToExternalSystem VentilationController\_03 .  
AuditRecord\_01 ot:usedSnapshotVersion SafetyGateSnapshot\_0007 .

핵심 원칙은 다음과 같다.

Relationship은 graph edge가 아니라 semantic contract다.

---

## **4\. Property의 종류**

LEDO는 property를 다음과 같이 구분한다.

| Property Type | 의미 | 예시 |
| ----- | ----- | ----- |
| Object Property | individual과 individual 사이의 관계 | `generatedBy`, `supportedBy`, `affects`, `hasTarget` |
| Data Property | individual과 literal value 사이의 관계 | `hasTimestamp`, `hasStatus`, `hasConfidence` |
| Annotation Property | label, comment, definition, version | `rdfs:label`, `skos:prefLabel`, `rdfs:comment` |
| Mapping Property | 외부 표준/외부 시스템과의 연결 | `hasExternalIdentifier`, `externallyMappedTo` |
| Provenance Property | source, evidence, lineage 연결 | `wasDerivedFrom`, `hasProvenance` |
| Materialized Relation | Safety Gate snapshot에서 쓰는 사전 계산 관계 | `relation_allowed_map`, `action_permission_map` |

중요한 경계는 다음과 같다.

Materialized Relation은 OWL property 자체가 아니다.  
Materialized Relation은 OWL / SHACL / SPARQL / Policy 결과를 runtime lookup용으로 평탄화한 구조다.

---

## **5\. Object Property 설계 원칙**

Object Property는 individual과 individual 사이의 의미 관계를 정의한다.

대표 property는 다음과 같다.

locatedIn  
observes  
generatedBy  
supportedBy  
requires  
authorizes  
mitigates  
affects  
hasTarget  
hasEvidence  
hasCapability  
requiresCapability  
derivedFrom  
sentToExternalSystem  
hasExecutionResult  
hasFeedback

간단한 사용 예시는 다음과 같다.

SensorObservation\_01 ot:generatedBy GasSensor\_01 .  
GasSensor\_01 ot:observes Zone\_A .  
GasRisk\_01 ot:affects Zone\_A .  
ActionCandidate\_01 ot:hasTarget Zone\_A .  
ActionCandidate\_01 ot:mitigates GasRisk\_01 .  
ExecutionRequest\_01 ot:sentToExternalSystem PLC\_01 .

Object Property를 만들기 전에 다음을 확인한다.

관계 방향이 명확한가?  
기존 property로 표현 가능한가?  
SHACL, SPARQL, Policy 검증에 필요한가?  
Audit trace에 필요한가?  
Safety Gate snapshot으로 materialize되어야 하는가?

핵심 원칙은 다음과 같다.

Object Property는 의미 관계를 표현한다.  
Object Property는 단순한 구현 편의용 링크가 아니다.

---

## **6\. Data Property 설계 원칙**

Data Property는 individual과 literal value를 연결한다.

대표 property는 다음과 같다.

hasTimestamp  
hasStatus  
hasConfidence  
hasRiskLevel  
hasBatteryLevel  
hasTemperature  
hasGasConcentration  
hasSourceSystem  
hasChecksum  
hasSnapshotVersion

간단한 사용 예시는 다음과 같다.

SensorObservation\_01 ot:hasTimestamp "2026-06-25T09:00:00Z"^^xsd:dateTime .  
SensorObservation\_01 ot:hasGasConcentration "45.2"^^xsd:decimal .  
SensorObservation\_01 ot:hasConfidence "0.98"^^xsd:decimal .  
SafetyGateSnapshot\_0007 ot:hasChecksum "sha256:..." .

Data Property를 만들기 전에 다음을 확인한다.

datatype이 명확한가?  
unit이 필요한가?  
QUDT reference가 필요한가?  
값이 시간에 따라 변하는가?  
RDF graph에 둘 만큼 안정적인가?  
고빈도 telemetry라면 time-series store에 둘 값인가?  
Safety Gate snapshot에 flag 또는 compact value로 들어가야 하는가?

핵심 원칙은 다음과 같다.

Stable semantic attribute는 RDF graph에 둘 수 있다.  
High-frequency runtime value는 time-series 또는 world state store에 두고, RDF에는 필요한 reference만 둔다.

---

## **6.1 Null / Void / Missing Value 표현 원칙**

Data Property에는 빈 문자열, `"null"`, `"N/A"`, `"unknown"`, `-9999` 같은 sentinel value를 주입하지 않는다.

데이터가 실제로 존재하지 않는 경우에는 해당 data property triple을 생성하지 않는다.

금지 예시는 다음과 같다.

SensorObservation\_01 ot:hasGasConcentration "" .  
SensorObservation\_01 ot:hasGasConcentration "N/A" .  
SensorObservation\_01 ot:hasGasConcentration "-9999"^^xsd:decimal .  
SensorObservation\_01 ot:hasGasConcentration "null" .

이런 값은 실제 측정값처럼 graph에 남아 SPARQL query, SLM training data, 통계 분석, Safety Gate Snapshot 생성 과정을 오염시킬 수 있다.

허용되는 방식은 다음과 같다.

값이 없으면 ot:hasGasConcentration triple을 생성하지 않는다.  
SHACL sh:minCount 1 검증 실패로 missing value를 감지한다.  
Sensor fault, disconnection, timeout은 별도의 ObservationState 또는 SensorFaultEvent로 표현한다.

예시:

SensorObservation\_01 rdf:type ot:GasObservation .  
SensorObservation\_01 ot:generatedBy ot:GasSensor\_01 .  
SensorObservation\_01 ot:hasTimestamp "2026-06-25T09:00:00Z"^^xsd:dateTime .  
SensorObservation\_01 ot:hasObservationState ot:MissingValueState .

SensorFaultEvent\_01 rdf:type ot:SensorFaultEvent .  
SensorFaultEvent\_01 ot:affects ot:GasSensor\_01 .  
SensorFaultEvent\_01 ot:hasFaultType ot:SignalDisconnected .

SHACL 예시는 다음과 같다.

GasObservationShape  
  sh:property \[  
    sh:path ot:hasGasConcentration ;  
    sh:minCount 1 ;  
    sh:datatype xsd:decimal ;  
  \] .

핵심 원칙은 다음과 같다.

Missing value는 literal value가 아니다.  
Missing value는 validation failure 또는 state/event로 표현한다.

---

## **7\. Annotation Property 설계 원칙**

Annotation Property는 사람이 읽는 설명, label, comment, version, documentation metadata를 표현한다.

예시는 다음과 같다.

rdfs:label  
rdfs:comment  
skos:prefLabel  
skos:altLabel  
skos:definition  
owl:versionInfo

Annotation Property는 reasoning이나 runtime validation에 직접 사용하지 않는다.

사용 목적은 다음과 같다.

용어 설명  
다국어 label  
문서화  
표준 mapping 설명  
개발자 이해 보조  
SLM training vocabulary support

핵심 원칙은 다음과 같다.

Annotation은 설명이다.  
Annotation을 runtime decision logic으로 사용하지 않는다.

---

## **8\. Property Naming 원칙**

Property 이름은 관계 방향과 의미를 명확히 표현해야 한다.

좋은 예시는 다음과 같다.

generatedBy  
supportedBy  
hasEvidence  
hasTarget  
affects  
mitigates  
requiresPermit  
approvedBy  
derivedFrom  
sentToExternalSystem  
hasExecutionResult  
hasFeedback

피해야 할 예시는 다음과 같다.

relatesTo  
connectedTo  
hasData  
link  
ref  
nodeToNode  
objectInfo  
usesThing

핵심 원칙은 다음과 같다.

Property 이름은 관계의 의미와 방향을 드러내야 한다.

---

## **9\. Foundation Property Family**

LEDO Foundation에서 property는 기능별 family로 관리한다.

| Family | 대표 Property | 목적 |
| ----- | ----- | ----- |
| Identity / Mapping | `hasIdentifier`, `hasExternalIdentifier`, `externallyMappedTo` | 외부 시스템과 canonical identity 연결 |
| Spatial | `locatedIn`, `containsZone`, `hasBoundary`, `hasGeofence` | zone, 위치, boundary 표현 |
| Observation / Evidence | `observes`, `generatedBy`, `hasEvidence`, `wasDerivedFrom` | 관측, 증거, provenance 연결 |
| Risk / Safety | `affects`, `mitigates`, `hasRiskLevel`, `hasRestriction` | 위험, 영향, 완화 관계 |
| Action / Decision | `hasActionType`, `hasTarget`, `requiresApproval`, `approvedBy` | action candidate와 approval 연결 |
| Execution / Feedback | `sentToExternalSystem`, `hasExecutionResult`, `hasFeedback` | 실행 요청과 feedback 연결 |
| Capability / Task | `hasCapability`, `requiresCapability`, `assignedTo` | agent capability와 task 연결 |
| Audit / Trace | `usedSnapshotVersion`, `usedPolicyVersion`, `hasReasonCode` | 판단 경로 추적 |

핵심 원칙은 다음과 같다.

Property family는 설계 일관성을 유지하기 위한 관리 단위다.  
Property family는 runtime materialization과 governance 기준을 함께 가져야 한다.

---

## **10\. Domain / Range 설계 요약**

Domain과 Range의 세부 원칙은 `03_owl_modeling_principles`에서 다룬다.  
이 문서에서는 runtime 연결 관점만 정리한다.

Foundation property의 domain/range는 너무 좁게 잡지 않는다.

위험한 예시는 다음과 같다.

hasTarget rdfs:range Zone .

이 경우 다음 triple이 들어오면:

ActionCandidate\_01 ot:hasTarget RobotAgent\_01 .

reasoner가 다음을 추론할 수 있다.

RobotAgent\_01 rdf:type Zone .

더 안전한 Foundation 설계는 다음과 같다.

hasTarget rdfs:domain ActionCandidate .  
hasTarget rdfs:range Entity .

구체적인 action type별 target 제약은 SHACL, Policy, Safety Gate Snapshot에서 처리한다.

restrict\_access → target must be Zone  
dispatch\_robot → target may be RobotAgent or Task  
request\_inspection → target may be Zone, System, or PhysicalObject  
notify\_manager → target may be HumanAgent or Role

핵심 원칙은 다음과 같다.

Foundation domain/range는 넓게 둔다.  
구체적 검증은 SHACL, SPARQL, Policy, Safety Gate Snapshot이 담당한다.

---

## **11\. Inverse / Transitive / Functional Property 제한 요약**

이 영역의 세부 원칙은 `03_owl_modeling_principles`에서 다룬다.  
이 문서에서는 relationship runtime risk 관점만 정리한다.

### **11.1 Inverse Property**

Inverse Property는 정확한 반대 관계일 때만 사용한다.

generatedBy inverseOf generates  
locatedIn inverseOf containsEntity

단순 query 편의만으로 inverse property를 만들지 않는다.

---

### **11.2 Transitive Property**

Transitive Property는 실제로 전이되는 관계에만 사용한다.

가능 후보:

isPartOf  
locatedWithin  
subZoneOf  
dependsOn

주의 관계:

controls  
observes  
affects  
supports  
authorizes  
mitigates

이들은 현실 세계에서 항상 전이되지 않는다.

---

### **11.3 Functional / InverseFunctional Property**

FunctionalProperty와 InverseFunctionalProperty는 매우 제한적으로 사용한다.

예를 들어 `hasLocation`을 FunctionalProperty로 선언하면 current location, estimated location, last known location, design location을 표현하기 어렵다.

`hasSerialNumber`를 InverseFunctionalProperty로 선언하면 외부 시스템 오류나 vendor duplication 때문에 잘못된 identity merge가 발생할 수 있다.

핵심 원칙은 다음과 같다.

Strong property characteristic은 최소화한다.  
Identity는 evidence와 governance로 해결한다.  
Runtime validation은 Safety Gate Snapshot에서 처리한다.

---

## **11.4 Property Chain Axiom 제한**

`owl:propertyChainAxiom`은 여러 property path를 하나의 추론 관계로 결합하는 강력한 OWL 기능이다.

LEDO Foundation에서는 property chain axiom을 기본적으로 사용하지 않는다. 필요한 경우 Domain Module에서만 제한적으로 허용한다.

다음 조합은 governance review 없이는 금지한다.

owl:inverseOf와 owl:propertyChainAxiom의 결합  
owl:TransitiveProperty와 owl:propertyChainAxiom의 결합  
동일 property family 안에서 순환 chain을 만드는 구조  
Safety Gate runtime 판단에 직접 사용되는 property chain

이유는 다음과 같다.

property chain과 inverse relation이 결합되면  
예상하지 못한 relation closure,  
추론 폭발,  
순환적 관계 확장,  
runtime materialization 증가가 발생할 수 있다.

허용 조건은 다음과 같다.

Property chain은 acyclic해야 한다.  
Foundation Layer가 아니라 Domain Module에서 정의해야 한다.  
Reasoner consistency test를 통과해야 한다.  
추론 결과는 offline / async worker에서 1회 materialization해야 한다.  
Safety Gate hot path에서는 property chain reasoning을 직접 실행하지 않는다.  
결과는 relation\_allowed\_map 또는 relation\_closure\_map으로만 조회한다.

핵심 원칙은 다음과 같다.

Property chain은 runtime reasoning 도구가 아니다.  
Property chain은 offline semantic expansion 도구다.

---

## **12\. Relationship Validation and Runtime Materialization Matrix**

Property는 단순 정의로 끝나지 않는다.  
각 relationship은 검증 계층과 runtime 사용 위치를 가져야 한다.

| Relationship | 의미 | 검증 계층 | Runtime 사용 |
| ----- | ----- | ----- | ----- |
| `generatedBy` | Observation이 Sensor/Agent에 의해 생성됨 | SHACL, SPARQL | evidence provenance |
| `supportedBy` | Candidate가 EvidenceBundle에 의해 지원됨 | SPARQL, Evidence Check | evidence sufficiency |
| `affects` | Risk가 Zone/System에 영향을 줌 | SPARQL, Spatial Check | risk\_action\_matrix |
| `mitigates` | Action이 Risk를 완화함 | OWL, SPARQL, Policy | risk\_action\_matrix |
| `hasTarget` | ActionCandidate의 대상 | SHACL, Policy | action\_permission\_map |
| `requiresPermit` | Task/Action이 permit 필요 | OWL, Policy | permit\_validity\_map |
| `approvedBy` | Action이 승인자에게 승인됨 | Policy, Audit | approval\_state\_map |
| `sentToExternalSystem` | ExecutionRequest가 외부 시스템으로 전달됨 | Execution Adapter, Audit | execution trace |
| `hasFeedback` | Execution 결과가 feedback으로 연결됨 | Audit, Feedback Handler | reconciliation |
| `usedSnapshotVersion` | Decision이 특정 snapshot을 사용함 | Audit | traceability |

핵심 원칙은 다음과 같다.

중요한 relationship은 반드시 검증 계층과 runtime 사용 위치를 가져야 한다.

---

## **13\. Safety Gate Materialized Relation**

Safety Gate는 OWL property를 직접 탐색하지 않는다.

Safety Gate는 사전 계산된 compact relation map을 조회한다.

예시는 다음과 같다.

relation\_allowed\_map:  
  GasRisk\_01 affects Zone\_A → true  
  Evidence\_01 supports ActionCandidate\_01 → true  
  RobotAgent\_01 directlyControls Valve\_01 → false

action\_permission\_map:  
  RobotAgent\_01 \+ dispatch\_robot \+ InspectionTask\_77 → allowed  
  RobotAgent\_01 \+ direct\_physical\_control \+ Valve\_01 → denied

risk\_action\_matrix:  
  GasRisk \+ restrict\_access → allowed\_mitigation  
  GasRisk \+ notify\_manager → allowed\_mitigation  
  GasRisk \+ resume\_work → denied

zone\_restriction\_map:  
  Zone\_A → restricted  
  Zone\_B → speed\_limited  
  Zone\_C → normal

핵심 원칙은 다음과 같다.

Ontology property는 의미를 만든다.  
Materialized relation map은 runtime lookup을 가능하게 한다.  
Safety Gate는 materialized relation만 읽는다.

---

## **14\. Property Registry**

LEDO는 property를 registry로 관리해야 한다.

Property registry 항목은 다음을 포함한다.

property\_iri  
property\_label  
property\_type  
property\_family  
domain  
range  
inverse\_of  
property\_chain\_participation  
is\_transitive  
is\_functional  
is\_inverse\_functional  
shacl\_shape\_reference  
sparql\_validation\_reference  
policy\_reference  
materialized\_map\_reference  
used\_in\_safety\_gate  
governance\_status  
owner\_module  
version

예시:

property\_iri: ot:supportedBy  
property\_label: supported by  
property\_type: object\_property  
property\_family: evidence  
domain: ot:ActionCandidate  
range: ot:EvidenceBundle  
inverse\_of: ot:supportsCandidate  
property\_chain\_participation: false  
is\_transitive: false  
is\_functional: false  
is\_inverse\_functional: false  
shacl\_shape\_reference: ActionCandidateShape  
sparql\_validation\_reference: EvidenceSupportAskQuery  
policy\_reference: EvidenceSufficiencyPolicy  
materialized\_map\_reference: relation\_allowed\_map  
used\_in\_safety\_gate: true  
governance\_status: approved  
owner\_module: evidence\_model  
version: 1.0.0

핵심 원칙은 다음과 같다.

Property는 코드처럼 관리해야 한다.  
Property는 owner, version, validation, governance status를 가져야 한다.

---

## **15\. Property 생성 절차**

새 property를 만들 때는 다음 핵심 절차만 따른다.

1\. 관계 의미 정의  
2\. 기존 property 재사용 가능성 확인  
3\. Object / Data / Annotation / Mapping property 구분  
4\. Foundation property인지 Domain property인지 결정  
5\. Domain / Range 설정  
6\. Inverse / Transitive / Functional / Property Chain 참여 여부 판단  
7\. Missing value 처리 방식 확인  
8\. SHACL / SPARQL / Policy 검증 필요 여부 판단  
9\. Safety Gate materialization 필요 여부 판단  
10\. Property Registry 등록 및 Governance Review

핵심 원칙은 다음과 같다.

Property는 즉흥적으로 만들지 않는다.  
Property는 의미, 검증, runtime 사용 여부를 확인한 뒤 등록한다.

---

## **16\. Anti-Patterns**

| Anti-pattern | 문제 | 대안 |
| ----- | ----- | ----- |
| 모든 관계를 `relatedTo`로 표현 | 의미가 사라짐 | 구체적 property 사용 |
| Domain / Range를 너무 좁게 설정 | 잘못된 inference 발생 | Foundation은 넓게, 구체 검증은 SHACL/Policy로 처리 |
| query 편의로 inverse를 남발 | graph 복잡도 증가 | 정확한 inverse에만 사용 |
| property chain을 Foundation에서 남용 | 추론 폭발과 relation closure 증가 | Domain Module에서 제한적으로 사용 |
| `sameAs`로 외부 ID 통합 | identity pollution | mapping property와 evidence 사용 |
| missing value를 `""`, `"N/A"`, `-9999`로 표현 | graph와 training data 오염 | triple drop \+ SHACL minCount failure |
| runtime state를 TBox property로 고정 | 상태 변화 표현 실패 | State/Event/World State 사용 |
| Safety Gate에서 RDF relation 직접 탐색 | hot path latency 증가 | materialized relation map 사용 |
| property registry 없이 property 추가 | governance 불가능 | registry 관리 |
| AI output을 Evidence처럼 취급 | hallucination이 evidence로 오염 | AI output은 candidate로 분리 |

---

## **17\. 최종 운영 원칙**

Relationship은 semantic contract다.  
Object Property는 individual 간 의미 관계를 표현한다.  
Data Property는 literal value를 표현한다.  
Missing value는 literal로 표현하지 않는다.  
Annotation Property는 설명과 vocabulary 지원에 사용한다.  
Mapping Property는 외부 시스템과 canonical identity를 연결한다.  
Foundation domain/range는 넓게 설정한다.  
구체적 검증은 SHACL, SPARQL, Policy, Safety Gate Snapshot이 담당한다.  
Inverse Property는 정확한 반대 관계일 때만 사용한다.  
Property Chain Axiom은 Foundation에서 기본 금지하고 Domain Module에서 제한적으로만 허용한다.  
Transitive / Functional / InverseFunctional Property는 매우 신중하게 사용한다.  
Safety Gate는 RDF relation을 직접 탐색하지 않고 materialized relation map을 조회한다.  
Property는 registry와 governance로 관리한다.

---

## **18\. 최종 결론**

LEDO Relationship and Property Design의 핵심은 property를 많이 만드는 것이 아니다.

핵심은 산업 세계의 의미 관계를 명확히 정의하고, 그 관계가 reasoning, validation, policy, evidence, audit, execution boundary와 어떻게 연결되는지 고정하는 것이다.

최종 구조는 다음과 같다.

OWL Property  
→ semantic relation definition

SHACL  
→ data and shape validation

SPARQL / Graph Query  
→ relation consistency validation

Policy  
→ operational permission interpretation

Materialized Relation Map  
→ runtime lookup structure

Safety Gate  
→ deterministic lookup and final pre-execution decision

Audit  
→ relationship-based traceability

최종 원칙은 다음과 같다.

Class defines what something is.  
Property defines how things are related.  
Constraint validates whether the relationship is acceptable.  
Policy decides whether the relationship is operationally allowed.  
Snapshot materializes runtime-ready relationships.  
Safety Gate reads only the materialized result.

