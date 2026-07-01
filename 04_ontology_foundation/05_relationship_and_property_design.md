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

