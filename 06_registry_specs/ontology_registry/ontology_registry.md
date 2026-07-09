# **Ontology registry**

## **1\. Overview**

`ontology_registry` is a core registry in the LEDO Ontology-Centric Cyber-Physical System. It defines and governs all Ontology Modules, Ontology Versions, Namespaces, IRI Policies, Import Rules, Alignment Rules, Class / Property / Relation / Axiom References, SHACL Shapes, Reasoning Profiles, Validation Rules, Migration Rules, and Release Statuses used across the system.

The purpose of this module is to prevent the semantic system used across LEDO from being changed arbitrarily, and to prevent unverified ontology versions from being used by Agents, Decisions, Approvals, Safety Gate, Execution, UI, and External System Integration.

`ontology_registry` is not a simple list of ontology files.

It is an **operational contract registry for semantic systems, versions, namespaces, reasoning, validation, and migration** that defines the following:

Which Ontology Modules officially exist?

Which Ontology Version is active?

Which namespace and IRI policy are used?

Which upper ontology is the module aligned with?

How is it related to BFO, SOSA/SSN, PROV-O, QUDT, and GeoSPARQL?

Which classes, properties, relations, and axiom sets are included?

Which SHACL shapes and validation rules are required?

Which reasoning profile is allowed?

Which registries depend on this ontology version?

What migration is required when the ontology changes?

Which ontology version may be used at runtime?

In other words, `ontology_registry` is the highest-level semantic registry that deterministically controls **“what this concept means”** inside the LEDO system.

---

## **2\. Core Principle**

Ontology is the standard of meaning.

Ontology is not merely a data store.

Ontology is different from the Knowledge Graph.

Ontology is different from World State.

Ontology is not an Agent.

Ontology is not the Decision Engine.

Ontology is not Approval Authority.

Ontology is not the Safety Gate itself.

However, Ontology is the semantic foundation for all of them.

The core principle is:

Ontology defines meaning.

Registry defines operational validity.

Knowledge Graph stores facts.

World State stores current facts.

Reasoner derives logical implications.

Policy decides permission.

Decision Registry defines judgment flow.

Safety Gate validates execution readiness.

In LEDO, ontology answers the following questions:

What is a Worker?

What is a Hazard?

What is a Zone?

What is a RobotCapability?

What does the STOP\_WORK Action mean?

What object does Evidence prove?

Which entity does a Sensor Observation observe?

Which relation is transitive?

Which property has an inverse relation?

Which classes are disjoint from one another?

`ontology_registry` controls which version and boundary of this semantic system may be used in the operational system.

---

## **3\. Position in the LEDO Architecture**

`ontology_registry` belongs to the Core Ontology Kernel Layer, but it is also a cross-cutting semantic registry across the entire LEDO lifecycle.

Core Ontology Kernel

        ↓

ontology\_registry

        ↓

Ontology Module / Version / Namespace / IRI / Axiom / Shape

        ↓

Knowledge Graph / World State / Agent / Decision / Approval / Safety Gate

Its position in the full system flow is as follows:

Ontology Registry

        ↓

Provides Class / Property / Relation / Axiom / Shape standards

        ↓

Event Registry / Evidence Registry / Action Registry / Decision Registry

        ↓

Agent Vocabulary Registry / Policy Registry / Approval Registry

        ↓

Safety Gate / Execution Request / External System Integration

All other registries should reference the semantic IRIs and versions managed by `ontology_registry`.

---

## **4\. Purpose**

The purpose of `ontology_registry` is to ensure the following:

1. Prevent the use of unregistered ontology modules  
2. Manage ontology version lifecycle  
3. Control namespace and IRI policies  
4. Manage upper ontology alignment  
5. Manage domain ontology modules  
6. Manage ontology import dependencies  
7. Manage Class / Property / Relation / Axiom references  
8. Manage SHACL shape and validation rule references  
9. Manage reasoning profiles  
10. Separate static reasoning from runtime validation boundaries  
11. Manage registry migration caused by ontology changes  
12. Manage ontology release, deprecation, and retirement  
13. Validate semantic IRIs used by Agents, Models, Policies, Actions, and Evidence  
14. Preserve the distinction between Ontology, Knowledge Graph, and World State  
15. Manage ontology change audit and trace

---

## **5\. Core Distinctions**

### **5.1 Ontology Module**

`Ontology Module` is a unit of ontology responsible for a specific semantic domain.

Examples:

core\_construction\_ontology

safety\_ontology

worker\_ontology

equipment\_ontology

robot\_capability\_ontology

sensor\_observation\_ontology

zone\_spatial\_ontology

action\_ontology

event\_ontology

evidence\_ontology

policy\_ontology

execution\_ontology

external\_system\_ontology

audit\_trace\_ontology

Rather than placing everything into one huge OWL file, ontology should be divided into domain-specific modules.

---

### **5.2 Ontology Version**

`Ontology Version` is a versioned release of a specific ontology module.

Examples:

ontology:core\_construction:v1.0.0

ontology:safety:v1.2.0

ontology:robot\_capability:v0.9.0

ontology:execution:v1.0.0

Ontology without versioning is dangerous in an operational system.

Reasons:

Class meaning may change.

Property domain/range may change.

SHACL shapes may change.

The semantic meaning of an Action Type may change.

An IRI referenced by a Decision Rule may be deprecated.

---

### **5.3 Namespace**

Namespace is the base space of IRIs.

Examples:

ledo:

bfo:

sosa:

ssn:

prov:

qudt:

geo:

schema:

rdf:

rdfs:

owl:

xsd:

LEDO must have clear internal namespaces.

Examples:

https://ledo.ai/ontology/core\#

https://ledo.ai/ontology/safety\#

https://ledo.ai/ontology/action\#

https://ledo.ai/ontology/evidence\#

https://ledo.ai/ontology/execution\#

---

### **5.4 IRI Policy**

IRI Policy defines how identifiers are created for classes, properties, individuals, actions, events, and evidence.

Examples:

Class IRI:

    ledo:Worker

    ledo:HazardZone

    ledo:RobotCapability

Object Property IRI:

    ledo:locatedIn

    ledo:hasCapability

    ledo:requiresEvidence

Data Property IRI:

    ledo:hasRiskScore

    ledo:hasConfidenceScore

Action IRI:

    ledo:StopWorkAction

    ledo:DispatchRobotAction

Event IRI:

    ledo:HazardDetectedEvent

Evidence IRI:

    ledo:WorkerLocationSnapshotEvidence

IRI is both the address and the semantic identifier of an ontology term.  
It must not be generated arbitrarily.

---

### **5.5 Ontology Alignment**

Ontology Alignment defines how the LEDO ontology connects to external standard ontologies.

Examples:

LEDO Worker

    aligned with BFO Material Entity or Object

LEDO SensorObservation

    aligned with SOSA Observation

LEDO ProvenanceRecord

    aligned with PROV-O Entity / Activity / Agent

LEDO QuantityValue

    aligned with QUDT QuantityValue

LEDO Location / Zone

    aligned with GeoSPARQL Feature / Geometry

The core alignment direction for LEDO is:

Use BFO as the upper ontology foundation.

Use SOSA/SSN for sensor observations.

Use PROV-O for evidence, audit, and trace lineage.

Use QUDT for units and measurements.

Use GeoSPARQL for space and geometry.

---

### **5.6 Ontology Profile**

Ontology Profile defines the expressiveness and reasoning scope of an ontology.

Examples:

OWL 2 EL

OWL 2 RL

OWL 2 QL

OWL 2 DL

RDFS profile

SHACL-only runtime profile

Hybrid OWL \+ SHACL profile

In LEDO, the following principle is important:

Heavy OWL reasoning is used for static ontology validation and offline inference.

Runtime hot paths use SHACL, rules, policy, and cached materialization.

In other words, reasoners such as HermiT or Pellet must not be directly placed inside the real-time physical execution loop.

---

### **5.7 SHACL Shape**

SHACL Shape is a validation rule that checks whether a data graph or instance graph satisfies ontology constraints.

Examples:

WorkerLocationEvidenceShape

ActionCandidateShape

ExecutionRequestShape

RobotCapabilityShape

HazardZoneShape

ApprovalRequestShape

OWL is strong for defining meaning and logical relations.  
SHACL is strong for validating whether operational data satisfies required conditions.

---

## **6\. Scope**

`ontology_registry` controls the following fields:

ontology\_module\_id: string

canonical\_name: string

display\_name: string

description: string

semantic\_iri: string

ontology\_category: string

ontology\_domain: string

version: string

status: draft | active | deprecated | migration\_required | retired | blocked

namespace\_refs:

  \- string

base\_iri: string

preferred\_prefix: string

upper\_ontology\_refs:

  \- string

import\_module\_refs:

  \- string

alignment\_refs:

  \- string

class\_refs:

  \- string

object\_property\_refs:

  \- string

data\_property\_refs:

  \- string

annotation\_property\_refs:

  \- string

individual\_refs:

  \- string

axiom\_set\_refs:

  \- string

shacl\_shape\_refs:

  \- string

reasoning\_profile: rdfs | owl\_el | owl\_rl | owl\_ql | owl\_dl | shacl\_only | hybrid

reasoner\_refs:

  \- string

runtime\_usable: boolean

hot\_path\_allowed: boolean

offline\_reasoning\_required: boolean

validation\_rule\_refs:

  \- string

competency\_question\_refs:

  \- string

dependent\_registry\_refs:

  \- string

dependent\_service\_refs:

  \- string

migration\_policy\_ref: string

compatibility\_policy\_ref: string

release\_artifact\_refs:

  \- string

source\_file\_refs:

  \- string

documentation\_refs:

  \- string

owner\_module: string

owner\_team: string

source\_document: string

created\_at: datetime

updated\_at: datetime

deprecated\_since: datetime | null

replacement\_ontology\_module\_id: string | null

---

## **7\. Non-Scope**

`ontology_registry` does not directly define the following:

1. All RDF triple instance data  
2. All runtime World State facts  
3. All sensor data  
4. All event instances  
5. All evidence instances  
6. Complete Knowledge Graph storage implementation  
7. Internal Triple Store implementation  
8. Detailed SPARQL endpoint operation  
9. Complete policy pass/fail logic  
10. Complete agent reasoning workflow  
11. Final Safety Gate decision  
12. Physical execution command  
13. External system protocol transformation  
14. Complete UI visualization logic

These responsibilities belong to the following modules:

knowledge\_graph\_store

triple\_store

world\_state\_store

event\_registry

evidence\_registry

policy\_registry

decision\_registry

safety\_gate

adapter\_registry

external\_system\_registry

experience\_layer

`ontology_registry` manages the semantic system and the operational validity of ontology modules.  
Actual fact storage is handled by the Knowledge Graph, Triple Store, and World State.

---

## **8\. Ontology Category Model**

Recommended Ontology Categories are:

CORE\_ONTOLOGY

UPPER\_ONTOLOGY\_ALIGNMENT

DOMAIN\_ONTOLOGY

PROCESS\_ONTOLOGY

ACTION\_ONTOLOGY

EVENT\_ONTOLOGY

EVIDENCE\_ONTOLOGY

POLICY\_ONTOLOGY

EXECUTION\_ONTOLOGY

SENSOR\_ONTOLOGY

ROBOT\_ONTOLOGY

SPATIAL\_ONTOLOGY

AUDIT\_ONTOLOGY

EXTERNAL\_SYSTEM\_ONTOLOGY

### **8.1 CORE\_ONTOLOGY**

Defines the highest-level domain concepts across LEDO.

Examples:

Entity

PhysicalObject

Agent

Process

Event

Action

Evidence

Capability

Constraint

Policy

---

### **8.2 UPPER\_ONTOLOGY\_ALIGNMENT**

Manages alignment with external upper or reference ontologies such as BFO, DUL, and PROV-O.

Examples:

BFO alignment

PROV-O alignment

SOSA/SSN alignment

QUDT alignment

GeoSPARQL alignment

---

### **8.3 DOMAIN\_ONTOLOGY**

Defines construction-site domain objects.

Examples:

Worker

Equipment

Crane

Excavator

Scaffold

ConcretePouringTask

ConfinedSpace

HazardZone

WorkZone

---

### **8.4 PROCESS\_ONTOLOGY**

Defines work, process, workflow, and lifecycle concepts.

Examples:

InspectionProcess

SafetyCheckProcess

RobotMissionProcess

ConcretePouringProcess

EmergencyEvacuationProcess

---

### **8.5 ACTION\_ONTOLOGY**

Defines the meaning of Action Types.

Examples:

StopWorkAction

DispatchRobotAction

LockZoneAction

RequestInspectionAction

NotifyManagerAction

---

### **8.6 EVENT\_ONTOLOGY**

Defines the meaning of Event Types.

Examples:

HazardDetectedEvent

WorkerLocationUpdatedEvent

ApprovalGrantedEvent

ExecutionResultReceivedEvent

---

### **8.7 EVIDENCE\_ONTOLOGY**

Defines the meaning of Evidence Types.

Examples:

WorkerLocationSnapshotEvidence

HazardDetectionSnapshotEvidence

RobotAvailabilitySnapshotEvidence

PolicyEvaluationEvidence

---

### **8.8 POLICY\_ONTOLOGY**

Defines the meaning of policies, authorities, constraints, and approval conditions.

Examples:

SafetyPolicy

StopWorkPolicy

ApprovalPolicy

AccessPolicy

EmergencyOverridePolicy

---

### **8.9 EXECUTION\_ONTOLOGY**

Defines the meaning of execution requests, external control requests, feedback, and execution results.

Examples:

ExecutionRequest

ExternalControlRequest

ExecutionResult

CommandLifecycle

FeedbackEvent

---

## **9\. Registry Entry Schema**

Each Ontology Registry entry follows this structure:

ontology\_module\_id: string

canonical\_name: string

display\_name: string

description: string

semantic\_iri: string

ontology\_category: string

ontology\_domain: string

version: string

status: draft | active | deprecated | migration\_required | retired | blocked

namespace\_refs:

  \- string

base\_iri: string

preferred\_prefix: string

upper\_ontology\_refs:

  \- string

import\_module\_refs:

  \- string

alignment\_refs:

  \- string

class\_refs:

  \- string

object\_property\_refs:

  \- string

data\_property\_refs:

  \- string

annotation\_property\_refs:

  \- string

individual\_refs:

  \- string

axiom\_set\_refs:

  \- string

shacl\_shape\_refs:

  \- string

reasoning\_profile: string

reasoner\_refs:

  \- string

runtime\_usable: boolean

hot\_path\_allowed: boolean

offline\_reasoning\_required: boolean

validation\_rule\_refs:

  \- string

competency\_question\_refs:

  \- string

dependent\_registry\_refs:

  \- string

dependent\_service\_refs:

  \- string

migration\_policy\_ref: string

compatibility\_policy\_ref: string

release\_artifact\_refs:

  \- string

source\_file\_refs:

  \- string

documentation\_refs:

  \- string

owner\_module: string

owner\_team: string

source\_document: string

created\_at: datetime

updated\_at: datetime

deprecated\_since: datetime | null

replacement\_ontology\_module\_id: string | null

---

## **10\. Registry Entry Example: Core Construction Ontology**

ontology\_module\_id: ontology:core\_construction:v1.0.0

canonical\_name: core\_construction\_ontology

display\_name: Core Construction Ontology

description: A core ontology module that defines the key concepts, upper-level classes, and basic relations of the LEDO construction domain.

semantic\_iri: ledo:CoreConstructionOntology

ontology\_category: CORE\_ONTOLOGY

ontology\_domain: construction

version: 1.0.0

status: draft

namespace\_refs:

  \- namespace:ledo\_core

  \- namespace:bfo

  \- namespace:rdf

  \- namespace:rdfs

  \- namespace:owl

  \- namespace:xsd

base\_iri: https://ledo.ai/ontology/core\#

preferred\_prefix: ledo

upper\_ontology\_refs:

  \- ontology:bfo:v2.0

import\_module\_refs:

  \- ontology:upper\_bfo\_alignment:v1.0.0

alignment\_refs:

  \- alignment:ledo\_core\_to\_bfo\_v1

class\_refs:

  \- class:Worker

  \- class:Equipment

  \- class:WorkZone

  \- class:Hazard

  \- class:Task

  \- class:Process

  \- class:Capability

  \- class:Constraint

object\_property\_refs:

  \- property:locatedIn

  \- property:hasPart

  \- property:participatesIn

  \- property:hasCapability

  \- property:requiresCapability

data\_property\_refs:

  \- property:hasIdentifier

  \- property:hasLabel

  \- property:hasRiskScore

annotation\_property\_refs:

  \- property:definition

  \- property:source

  \- property:versionNote

individual\_refs: \[\]

axiom\_set\_refs:

  \- axiom\_set:core\_disjointness\_v1

  \- axiom\_set:core\_domain\_range\_v1

  \- axiom\_set:core\_hierarchy\_v1

shacl\_shape\_refs:

  \- shape:WorkerShape

  \- shape:EquipmentShape

  \- shape:WorkZoneShape

reasoning\_profile: owl\_rl

reasoner\_refs:

  \- reasoner:owlready2

  \- reasoner:jena\_rule\_engine

runtime\_usable: true

hot\_path\_allowed: false

offline\_reasoning\_required: true

validation\_rule\_refs:

  \- validation:iri\_policy\_v1

  \- validation:domain\_range\_consistency\_v1

  \- validation:disjointness\_check\_v1

competency\_question\_refs:

  \- cq:which\_workers\_are\_located\_in\_a\_hazard\_zone

  \- cq:which\_equipment\_requires\_operator\_certification

  \- cq:which\_tasks\_require\_specific\_capability

dependent\_registry\_refs:

  \- registry:action\_registry

  \- registry:event\_registry

  \- registry:evidence\_registry

  \- registry:decision\_registry

  \- registry:identity\_registry

dependent\_service\_refs:

  \- service:ontology\_lookup\_service

  \- service:knowledge\_graph\_service

  \- service:world\_state\_service

migration\_policy\_ref: migration:core\_ontology\_migration\_policy\_v1

compatibility\_policy\_ref: compatibility:core\_ontology\_semver\_policy\_v1

release\_artifact\_refs:

  \- artifact:core\_construction\_ontology\_owl\_v1

  \- artifact:core\_construction\_shapes\_ttl\_v1

source\_file\_refs:

  \- file:ontology/core/core\_construction.owl

  \- file:ontology/core/core\_construction\_shapes.ttl

documentation\_refs:

  \- doc:core\_construction\_ontology\_spec\_v1

owner\_module: core\_ontology\_kernel

owner\_team: LEDO Ontology Governance

source\_document: ontology\_core\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_ontology\_module\_id: null

---

## **11\. Registry Entry Example: Safety Ontology**

ontology\_module\_id: ontology:safety:v1.0.0

canonical\_name: safety\_ontology

display\_name: Safety Ontology

description: An ontology module that defines the meaning of hazards, risks, safety actions, safety evidence, and safety policies on construction sites.

semantic\_iri: ledo:SafetyOntology

ontology\_category: DOMAIN\_ONTOLOGY

ontology\_domain: construction\_safety

version: 1.0.0

status: draft

namespace\_refs:

  \- namespace:ledo\_safety

  \- namespace:ledo\_core

  \- namespace:prov

  \- namespace:sosa

  \- namespace:qudt

base\_iri: https://ledo.ai/ontology/safety\#

preferred\_prefix: ledo\_safety

upper\_ontology\_refs:

  \- ontology:bfo:v2.0

  \- ontology:prov\_o:v1.0

  \- ontology:sosa\_ssn:v1.0

import\_module\_refs:

  \- ontology:core\_construction:v1.0.0

  \- ontology:evidence:v1.0.0

  \- ontology:event:v1.0.0

  \- ontology:policy:v1.0.0

alignment\_refs:

  \- alignment:safety\_to\_bfo\_v1

  \- alignment:safety\_evidence\_to\_prov\_o\_v1

  \- alignment:safety\_observation\_to\_sosa\_v1

class\_refs:

  \- class:Hazard

  \- class:SafetyRisk

  \- class:HazardZone

  \- class:SafetyIncident

  \- class:StopWorkCondition

  \- class:EmergencyCondition

  \- class:SafetyEvidence

object\_property\_refs:

  \- property:hasHazard

  \- property:exposesWorkerTo

  \- property:requiresStopWork

  \- property:requiresInspection

  \- property:supportedByEvidence

data\_property\_refs:

  \- property:hasRiskScore

  \- property:hasSeverityLevel

  \- property:hasConfidenceScore

annotation\_property\_refs:

  \- property:safetyDefinition

  \- property:regulatoryReference

individual\_refs:

  \- individual:risk\_level\_low

  \- individual:risk\_level\_warning

  \- individual:risk\_level\_high

  \- individual:risk\_level\_critical

  \- individual:risk\_level\_emergency

axiom\_set\_refs:

  \- axiom\_set:safety\_hazard\_hierarchy\_v1

  \- axiom\_set:safety\_risk\_disjointness\_v1

  \- axiom\_set:safety\_action\_requirements\_v1

shacl\_shape\_refs:

  \- shape:HazardShape

  \- shape:SafetyRiskShape

  \- shape:StopWorkConditionShape

  \- shape:SafetyEvidenceShape

reasoning\_profile: hybrid

reasoner\_refs:

  \- reasoner:owlready2

  \- reasoner:shacl\_engine

  \- reasoner:rule\_engine

runtime\_usable: true

hot\_path\_allowed: false

offline\_reasoning\_required: true

validation\_rule\_refs:

  \- validation:safety\_risk\_consistency\_v1

  \- validation:hazard\_zone\_shape\_v1

  \- validation:safety\_evidence\_requirement\_v1

competency\_question\_refs:

  \- cq:which\_hazards\_require\_stop\_work

  \- cq:which\_workers\_are\_exposed\_to\_high\_risk

  \- cq:which\_evidence\_supports\_safety\_decision

dependent\_registry\_refs:

  \- registry:action\_registry

  \- registry:evidence\_registry

  \- registry:decision\_registry

  \- registry:approval\_registry

  \- registry:safety\_gate\_registry

dependent\_service\_refs:

  \- service:safety\_risk\_agent

  \- service:decision\_engine

  \- service:safety\_gate\_service

migration\_policy\_ref: migration:safety\_ontology\_migration\_policy\_v1

compatibility\_policy\_ref: compatibility:safety\_ontology\_semver\_policy\_v1

release\_artifact\_refs:

  \- artifact:safety\_ontology\_owl\_v1

  \- artifact:safety\_shapes\_ttl\_v1

source\_file\_refs:

  \- file:ontology/safety/safety.owl

  \- file:ontology/safety/safety\_shapes.ttl

documentation\_refs:

  \- doc:safety\_ontology\_spec\_v1

owner\_module: safety\_domain\_module

owner\_team: LEDO Safety Ontology

source\_document: safety\_ontology\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_ontology\_module\_id: null

---

## **12\. Registry Entry Example: Robot Capability Ontology**

ontology\_module\_id: ontology:robot\_capability:v1.0.0

canonical\_name: robot\_capability\_ontology

display\_name: Robot Capability Ontology

description: An ontology module that defines the meaning of robot capabilities, missions, task suitability, and external fleet integration.

semantic\_iri: ledo:RobotCapabilityOntology

ontology\_category: ROBOT\_ONTOLOGY

ontology\_domain: robotics\_in\_construction

version: 1.0.0

status: draft

namespace\_refs:

  \- namespace:ledo\_robot

  \- namespace:ledo\_core

  \- namespace:prov

  \- namespace:sosa

base\_iri: https://ledo.ai/ontology/robot\#

preferred\_prefix: ledo\_robot

upper\_ontology\_refs:

  \- ontology:bfo:v2.0

import\_module\_refs:

  \- ontology:core\_construction:v1.0.0

  \- ontology:action:v1.0.0

  \- ontology:execution:v1.0.0

  \- ontology:external\_system:v1.0.0

alignment\_refs:

  \- alignment:robot\_capability\_to\_bfo\_v1

class\_refs:

  \- class:Robot

  \- class:RobotFleet

  \- class:RobotCapability

  \- class:RobotMission

  \- class:RobotTask

  \- class:NavigationCapability

  \- class:InspectionCapability

  \- class:PayloadCapability

object\_property\_refs:

  \- property:hasRobotCapability

  \- property:canPerformMission

  \- property:assignedToRobot

  \- property:managedByFleetManager

  \- property:requiresFleetManager

data\_property\_refs:

  \- property:hasBatteryLevel

  \- property:hasPayloadLimit

  \- property:hasNavigationStatus

  \- property:hasAvailabilityStatus

annotation\_property\_refs:

  \- property:robotVendorReference

  \- property:capabilityDefinition

individual\_refs:

  \- individual:robot\_status\_available

  \- individual:robot\_status\_busy

  \- individual:robot\_status\_faulted

  \- individual:robot\_status\_unavailable

axiom\_set\_refs:

  \- axiom\_set:robot\_capability\_hierarchy\_v1

  \- axiom\_set:robot\_mission\_precondition\_v1

  \- axiom\_set:robot\_external\_system\_boundary\_v1

shacl\_shape\_refs:

  \- shape:RobotCapabilityShape

  \- shape:RobotMissionShape

  \- shape:RobotAvailabilityShape

reasoning\_profile: owl\_rl

reasoner\_refs:

  \- reasoner:owlready2

  \- reasoner:shacl\_engine

runtime\_usable: true

hot\_path\_allowed: false

offline\_reasoning\_required: true

validation\_rule\_refs:

  \- validation:robot\_capability\_consistency\_v1

  \- validation:robot\_mission\_shape\_v1

  \- validation:robot\_external\_system\_boundary\_v1

competency\_question\_refs:

  \- cq:which\_robot\_can\_perform\_this\_mission

  \- cq:which\_robot\_capabilities\_are\_required\_for\_dispatch

  \- cq:which\_fleet\_manager\_controls\_this\_robot

dependent\_registry\_refs:

  \- registry:action\_registry

  \- registry:evidence\_registry

  \- registry:external\_system\_registry

  \- registry:adapter\_registry

dependent\_service\_refs:

  \- service:robot\_dispatch\_agent

  \- service:execution\_dispatcher

  \- service:world\_state\_service

migration\_policy\_ref: migration:robot\_capability\_ontology\_migration\_policy\_v1

compatibility\_policy\_ref: compatibility:robot\_capability\_semver\_policy\_v1

release\_artifact\_refs:

  \- artifact:robot\_capability\_ontology\_owl\_v1

  \- artifact:robot\_capability\_shapes\_ttl\_v1

source\_file\_refs:

  \- file:ontology/robot/robot\_capability.owl

  \- file:ontology/robot/robot\_capability\_shapes.ttl

documentation\_refs:

  \- doc:robot\_capability\_ontology\_spec\_v1

owner\_module: robot\_domain\_module

owner\_team: LEDO Robotics Ontology

source\_document: robot\_capability\_ontology\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_ontology\_module\_id: null

---

## **13\. Ontology Lifecycle Alignment**

Ontology is connected to the following lifecycle:

Ontology Draft Created

        ↓

Namespace / IRI Policy Validation

        ↓

Import Dependency Validation

        ↓

Axiom Consistency Check

        ↓

SHACL Shape Validation

        ↓

Competency Question Test

        ↓

Reasoner Compatibility Test

        ↓

Registry Dependency Impact Analysis

        ↓

Release Candidate

        ↓

Active Ontology Version

        ↓

Runtime Reference / Offline Reasoning / KG Validation

        ↓

Migration / Deprecation / Retirement

The important point is that an ontology being active does not mean heavy reasoning may be used in every runtime hot path.

An ontology version may be active.

However, hot\_path\_allowed may still be false.

OWL reasoners may be used for static validation.

Runtime execution paths should use SHACL / rules / policy / cache-based validation.

---

## **14\. Validation Rules**

An Ontology Registry Entry is valid only when the following conditions are satisfied:

1. `ontology_module_id` exists in the registry.  
2. Its status is `active`.  
3. Ontology category is declared.  
4. Ontology domain is declared.  
5. Base IRI is declared.  
6. Preferred prefix is declared.  
7. Namespace references are declared.  
8. Upper ontology reference or alignment policy is declared.  
9. Import module dependencies are validated.  
10. Class / property / axiom references are declared.  
11. SHACL shape references are declared.  
12. Reasoning profile is declared.  
13. Validation rule references are declared.  
14. Competency question references are declared.  
15. Migration policy is declared.  
16. Compatibility policy is declared.  
17. Release artifact references are declared.  
18. Source file references are declared.  
19. Owner module is declared.  
20. Version is valid.  
21. If deprecated, migration metadata exists.

If any of these conditions are missing, the Ontology Module must not be used in the operational lifecycle.

---

## **15\. Runtime Ontology Reference Validation**

Before an Agent, Registry, or Service references an ontology, the following validations are required:

Does the Ontology Module exist in the registry?

Is the Ontology Module active?

Does the referenced IRI exist in that ontology version?

Is the referenced class / property not deprecated?

Are all required import modules active?

Is the ontology version compatible?

Does it match the reasoning profile required by the registry?

Is the reference usable on the runtime hot path?

If a SHACL shape or validation rule is required, does it exist?

If these conditions are not satisfied, the semantic reference must be rejected.

---

## **16\. Namespace and IRI Rule**

Namespace and IRI are the lifeline of ontology.

Recommended namespace rules:

Each ontology module must have a clear base IRI.

Prefixes must not conflict.

Class IRIs and instance IRIs must not be confused.

Deprecated IRIs should not be immediately deleted; replacement mappings should be provided.

External standard ontology IRIs should preserve their original identifiers.

Recommended IRI pattern:

Class:

    ledo:Worker

    ledo:HazardZone

Object Property:

    ledo:locatedIn

    ledo:hasCapability

Data Property:

    ledo:hasRiskScore

Event Type:

    ledo:HazardDetectedEvent

Evidence Type:

    ledo:HazardDetectionSnapshotEvidence

Action Type:

    ledo:StopWorkAction

Core principle:

No stable IRI,

no stable meaning.

---

## **17\. Import Dependency Rule**

Ontology modules may import other ontology modules.

Example:

safety\_ontology

    imports core\_construction\_ontology

    imports event\_ontology

    imports evidence\_ontology

    imports policy\_ontology

Import dependency validation checks:

Does the imported ontology exist in the registry?

Is the imported ontology active?

Is the version compatibility valid?

Is there no circular import?

Does it avoid importing deprecated ontology modules?

Does the upper ontology alignment remain consistent?

Circular imports should be avoided as much as possible.

---

## **18\. Axiom Rule**

Ontology Registry should know which axiom sets are included in each ontology module.

Major axiom types:

SubClassOf

EquivalentClass

DisjointClass

ObjectPropertyDomain

ObjectPropertyRange

DataPropertyDomain

DataPropertyRange

InverseObjectProperties

TransitiveObjectProperty

FunctionalProperty

CardinalityRestriction

ClassAssertion

PropertyAssertion

However, not every axiom is suitable for runtime hot paths.

Disjointness check:

    suitable for static validation

Transitive relation:

    suitable for materialized graph or cached inference

Cardinality restriction:

    usable together with SHACL validation

Heavy class expression:

    suitable for offline reasoning

---

## **19\. SHACL Validation Rule**

SHACL is highly important for operational validation in LEDO.

Example SHACL Shapes:

ActionCandidateShape

EvidenceBundleShape

ExecutionRequestShape

WorkerLocationEvidenceShape

RobotCapabilityShape

ExternalSystemShape

SHACL is powerful in the following situations:

required field validation

datatype validation

cardinality validation

allowed value validation

class membership validation

property path validation

runtime object shape validation

Core principle:

OWL defines meaning.

SHACL validates operational data shape.

---

## **20\. Reasoning Profile Rule**

Each ontology module must have a reasoning profile.

Recommended profiles:

rdfs

owl\_el

owl\_rl

owl\_ql

owl\_dl

shacl\_only

hybrid

Recommended LEDO approach:

Core ontology:

    owl\_rl or owl\_el

Safety ontology:

    hybrid

Runtime validation ontology:

    shacl\_only or hybrid

Heavy conceptual ontology:

    owl\_dl, offline only

Core principle:

Heavy reasoning must not block real-time physical control paths.

---

## **21\. Competency Question Rule**

A Competency Question is a core question that the ontology must be able to answer.

Examples:

Which workers are located in a hazard zone?

Which hazards require STOP\_WORK?

Which evidence supports this DecisionCase?

Which robot has the capability to perform this mission?

Which External System controls this equipment?

Which Approval Rule applies to this Action Type?

Before ontology release, competency question tests must pass.

Core principle:

No competency question,

no proof that ontology serves its purpose.

---

## **22\. Ontology Change Impact Rule**

Ontology changes can affect many registries.

Examples:

StopWorkAction IRI changed

    → affects action\_registry

    → affects decision\_registry

    → affects approval\_registry

    → affects safety\_gate

    → affects audit trace

WorkerLocationSnapshotEvidence class changed

    → affects evidence\_registry

    → affects decision\_registry

    → affects safety\_gate

RobotCapability property changed

    → affects robot\_dispatch\_agent

    → affects external\_system\_registry

    → affects adapter\_registry

Therefore, ontology changes require impact analysis.

Review targets:

dependent\_registry\_refs

dependent\_service\_refs

SHACL shape

SPARQL query

Agent prompt / tool schema

RAG retrieval mapping

UI visualization mapping

Audit trace schema

---

## **23\. Relationship to Knowledge Graph Store**

`ontology_registry` manages the semantic schema.

Knowledge Graph Store stores instance facts.

ontology\_registry:

    Defines the meaning of Worker class and locatedIn property.

knowledge\_graph\_store:

    Stores the fact that worker\_123 locatedIn zone\_03.

Ontology and Knowledge Graph must not be confused.

Ontology \= meaning and constraints

Knowledge Graph \= facts and relationships

---

## **24\. Relationship to World State Layer**

World State stores current-state facts.

Ontology defines the meaning and constraints of those facts.

World State:

    worker\_123 is currently in zone\_03.

Ontology:

    Worker is a PhysicalObject,

    and locatedIn is a relation between PhysicalObject and SpatialRegion.

World State changes rapidly.  
Ontology should be relatively stable.

---

## **25\. Relationship to Event Registry**

`event_registry` defines the operational contract of Event Types.

`ontology_registry` provides the semantic IRI and meaning of Event Types.

event\_registry:

    What payload and routing rule does event:HazardDetected have?

ontology\_registry:

    What kind of Event is ledo:HazardDetectedEvent, and what does it observe?

Event Types should have semantic IRIs that exist in the ontology.

---

## **26\. Relationship to Evidence Registry**

`evidence_registry` defines the schema, freshness, and quality rules of Evidence Types.

`ontology_registry` provides the meaning of Evidence Types.

evidence\_registry:

    What freshness and confidence threshold does hazard\_detection\_snapshot require?

ontology\_registry:

    ledo:HazardDetectionSnapshotEvidence is SafetyEvidence that proves Hazard.

Evidence Types must be connected to ontology meaning.

---

## **27\. Relationship to Action Registry**

`action_registry` defines the operational contract of Action Types.

`ontology_registry` defines the semantic meaning of Action Types.

action\_registry:

    What target, risk, approval, and adapter boundary does STOP\_WORK have?

ontology\_registry:

    ledo:StopWorkAction is a SafetyAction that stops a WorkProcess.

Action Types must not reference meanings that do not exist in the ontology.

---

## **28\. Relationship to Decision Registry**

`decision_registry` defines judgment procedures.

`ontology_registry` defines the meaning of judgment targets and relations.

decision\_registry:

    Which evidence and policy does the STOP\_WORK Decision evaluate?

ontology\_registry:

    What is the relation between Hazard, WorkerExposure, SafetyRisk, and StopWorkCondition?

Decision Rules should clearly define their judgment targets through ontology IRIs.

---

## **29\. Relationship to Policy Registry**

Policy determines permitted conditions.

Ontology defines the meaning of the objects referenced by policies.

policy\_registry:

    Only safety\_supervisor may approve STOP\_WORK.

ontology\_registry:

    Defines the meaning of SafetySupervisor, StopWorkAction, and HazardZone.

Roles, actions, targets, and evidence used by policies must be grounded in ontology.

---

## **30\. Relationship to Agent Vocabulary Registry**

Agents should interpret and generate candidates only within ontology scope.

agent\_vocabulary\_registry:

    SAFETY\_RISK\_AGENT may handle Hazard, Worker, Zone, and StopWorkAction.

ontology\_registry:

    Defines the meaning and relations of these classes and actions.

If an Agent generates a class or relation that does not exist in the ontology, it must be rejected.

---

## **31\. Relationship to Model Adapter Registry**

Model output must pass ontology grounding.

model\_adapter\_registry:

    safety\_slm output must pass ontology\_guard.

ontology\_registry:

    Verifies whether the entity, relation, and action IRIs in the output exist in the active ontology version.

Core principle:

Model generated concept must be grounded in active ontology.

---

## **32\. Relationship to Safety Gate**

Safety Gate validates runtime execution readiness.

Ontology Registry provides the meanings and shapes used by Safety Gate.

Example:

Safety Gate validation:

    worker\_not\_in\_hazard\_zone

Ontology Registry:

    Provides the meaning of Worker, HazardZone, locatedIn, and exposedTo

SHACL Shape:

    Validates required runtime evidence shape

Core principle:

Safety Gate must use active ontology and validation shapes.

---

## **33\. Relationship to Audit Registry**

Ontology changes must always be audited.

Audit targets:

ontology\_module\_created

ontology\_version\_released

ontology\_deprecated

ontology\_migration\_required

ontology\_import\_changed

ontology\_iri\_deprecated

ontology\_alignment\_changed

ontology\_shape\_changed

ontology\_reasoning\_profile\_changed

Audit Record should include the following:

ontology\_module\_id: string

version: string

changed\_by\_identity\_id: string

change\_type: string

affected\_registry\_refs:

  \- string

affected\_service\_refs:

  \- string

migration\_required: boolean

trace\_id: string

timestamp: datetime

Core principle:

No ontology change without audit.

---

## **34\. Relationship to Ontology Authoring Tools**

`ontology_registry` may connect with tools such as Protégé, RDFLib, OWLReady2, GraphDB, and Jena.

Example roles:

Protégé:

    ontology authoring / manual modeling

RDFLib:

    RDF graph parsing / serialization / validation support

OWLReady2:

    Python object access / reasoning integration

GraphDB / Jena:

    triple store / SPARQL / inference support

SHACL Engine:

    shape validation

However, authoring tools and the registry are different.

Protégé is a tool for editing ontology.

ontology\_registry controls which ontology version is valid in the operational system.

---

## **35\. Versioning and Migration**

Ontology Modules must be versioned.

A version change is required when any of the following changes:

1. Base IRI changes  
2. Namespace changes  
3. Classes are added / removed / semantically changed  
4. Properties are added / removed / domain-range changed  
5. Axioms change  
6. SHACL shapes change  
7. Import dependencies change  
8. Upper ontology alignment changes  
9. Reasoning profile changes  
10. Competency questions change  
11. Registry dependencies change  
12. Runtime usability changes  
13. Hot path permission changes  
14. Deprecated IRIs are added  
15. Replacement mappings change

Status values:

draft

active

deprecated

migration\_required

retired

blocked

### **35.1 draft**

An ontology version under authoring.  
It must not be used in the operational system.

---

### **35.2 active**

An ontology version that may be referenced by the operational system.

---

### **35.3 deprecated**

An ontology version that is no longer recommended but is preserved for migration.

---

### **35.4 migration\_required**

Existing registry entries or KG instances must be migrated to a new ontology version.

---

### **35.5 retired**

A version removed from operational reference.

---

### **35.6 blocked**

A version prohibited from use due to consistency errors, safety errors, IRI conflicts, reasoning failures, or similar issues.

---

## **36\. Implementation Use**

`ontology_registry` is used to generate or validate:

1. OntologyModule enum  
2. OntologyStatus enum  
3. OntologyCategory enum  
4. Namespace registry  
5. IRI policy validation  
6. Ontology import validation  
7. Class reference validation  
8. Property reference validation  
9. Axiom set validation  
10. SHACL shape lookup  
11. Reasoning profile validation  
12. Competency question tests  
13. Registry dependency impact analysis  
14. Runtime semantic reference validation  
15. Ontology version compatibility validation  
16. Ontology migration planning  
17. Audit log expectations  
18. Test case generation  
19. Release artifact management  
20. Ontology lookup service configuration

Implementation must not use unregistered ontology IRIs or deprecated ontology references in the operational lifecycle.

---

## **37\. Recommended Code Structure**

registries/

    ontology\_registry/

        ontology\_registry.py

        ontology\_entry.py

        ontology\_category.py

        ontology\_status.py

        namespace\_registry.py

        iri\_policy.py

        ontology\_imports.py

        ontology\_alignment.py

        reasoning\_profile.py

        shacl\_shape\_ref.py

        axiom\_set\_ref.py

        competency\_question.py

        ontology\_validation.py

        ontology\_errors.py

        ontology\_loader.py

        ontology\_migration.py

    class\_registry/

    property\_registry/

    action\_registry/

    event\_registry/

    evidence\_registry/

    decision\_registry/

    policy\_registry/

    model\_adapter\_registry/

    audit\_event\_registry/

---

## **38\. Minimal Pydantic Model**

from enum import Enum

from pydantic import BaseModel, Field

from typing import Optional

from datetime import datetime

class OntologyStatus(str, Enum):

    DRAFT \= "draft"

    ACTIVE \= "active"

    DEPRECATED \= "deprecated"

    MIGRATION\_REQUIRED \= "migration\_required"

    RETIRED \= "retired"

    BLOCKED \= "blocked"

class OntologyCategory(str, Enum):

    CORE\_ONTOLOGY \= "core\_ontology"

    UPPER\_ONTOLOGY\_ALIGNMENT \= "upper\_ontology\_alignment"

    DOMAIN\_ONTOLOGY \= "domain\_ontology"

    PROCESS\_ONTOLOGY \= "process\_ontology"

    ACTION\_ONTOLOGY \= "action\_ontology"

    EVENT\_ONTOLOGY \= "event\_ontology"

    EVIDENCE\_ONTOLOGY \= "evidence\_ontology"

    POLICY\_ONTOLOGY \= "policy\_ontology"

    EXECUTION\_ONTOLOGY \= "execution\_ontology"

    SENSOR\_ONTOLOGY \= "sensor\_ontology"

    ROBOT\_ONTOLOGY \= "robot\_ontology"

    SPATIAL\_ONTOLOGY \= "spatial\_ontology"

    AUDIT\_ONTOLOGY \= "audit\_ontology"

    EXTERNAL\_SYSTEM\_ONTOLOGY \= "external\_system\_ontology"

class ReasoningProfile(str, Enum):

    RDFS \= "rdfs"

    OWL\_EL \= "owl\_el"

    OWL\_RL \= "owl\_rl"

    OWL\_QL \= "owl\_ql"

    OWL\_DL \= "owl\_dl"

    SHACL\_ONLY \= "shacl\_only"

    HYBRID \= "hybrid"

class OntologyRegistryEntry(BaseModel):

    ontology\_module\_id: str

    canonical\_name: str

    display\_name: str

    description: str

    semantic\_iri: str

    ontology\_category: OntologyCategory

    ontology\_domain: str

    version: str

    status: OntologyStatus \= OntologyStatus.DRAFT

    namespace\_refs: list\[str\] \= Field(default\_factory=list)

    base\_iri: str

    preferred\_prefix: str

    upper\_ontology\_refs: list\[str\] \= Field(default\_factory=list)

    import\_module\_refs: list\[str\] \= Field(default\_factory=list)

    alignment\_refs: list\[str\] \= Field(default\_factory=list)

    class\_refs: list\[str\] \= Field(default\_factory=list)

    object\_property\_refs: list\[str\] \= Field(default\_factory=list)

    data\_property\_refs: list\[str\] \= Field(default\_factory=list)

    annotation\_property\_refs: list\[str\] \= Field(default\_factory=list)

    individual\_refs: list\[str\] \= Field(default\_factory=list)

    axiom\_set\_refs: list\[str\] \= Field(default\_factory=list)

    shacl\_shape\_refs: list\[str\] \= Field(default\_factory=list)

    reasoning\_profile: ReasoningProfile

    reasoner\_refs: list\[str\] \= Field(default\_factory=list)

    runtime\_usable: bool \= True

    hot\_path\_allowed: bool \= False

    offline\_reasoning\_required: bool \= True

    validation\_rule\_refs: list\[str\] \= Field(default\_factory=list)

    competency\_question\_refs: list\[str\] \= Field(default\_factory=list)

    dependent\_registry\_refs: list\[str\] \= Field(default\_factory=list)

    dependent\_service\_refs: list\[str\] \= Field(default\_factory=list)

    migration\_policy\_ref: str

    compatibility\_policy\_ref: str

    release\_artifact\_refs: list\[str\] \= Field(default\_factory=list)

    source\_file\_refs: list\[str\] \= Field(default\_factory=list)

    documentation\_refs: list\[str\] \= Field(default\_factory=list)

    owner\_module: str

    owner\_team: str

    source\_document: str

    created\_at: datetime

    updated\_at: datetime

    deprecated\_since: Optional\[datetime\] \= None

    replacement\_ontology\_module\_id: Optional\[str\] \= None

---

## **39\. Core Validation Function**

def validate\_ontology\_reference(

    entry: OntologyRegistryEntry,

    semantic\_iri: str,

    required\_reasoning\_profile: ReasoningProfile | None \= None,

    require\_runtime\_usable: bool \= True,

    require\_hot\_path\_allowed: bool \= False,

) \-\> None:

    if entry.status \!= OntologyStatus.ACTIVE:

        raise InvalidOntologyModuleError(

            f"Ontology Module is not active: {entry.ontology\_module\_id}"

        )

    if require\_runtime\_usable and not entry.runtime\_usable:

        raise OntologyRuntimeNotAllowedError(

            f"Ontology Module is not runtime usable: {entry.ontology\_module\_id}"

        )

    if require\_hot\_path\_allowed and not entry.hot\_path\_allowed:

        raise OntologyHotPathNotAllowedError(

            f"Ontology Module is not allowed on hot path: {entry.ontology\_module\_id}"

        )

    known\_refs \= (

        entry.class\_refs

        \+ entry.object\_property\_refs

        \+ entry.data\_property\_refs

        \+ entry.annotation\_property\_refs

        \+ entry.individual\_refs

    )

    if semantic\_iri not in known\_refs:

        raise OntologyReferenceNotFoundError(

            f"Semantic IRI '{semantic\_iri}' is not registered in "

            f"Ontology Module '{entry.ontology\_module\_id}'"

        )

    if required\_reasoning\_profile is not None:

        if entry.reasoning\_profile \!= required\_reasoning\_profile:

            raise OntologyReasoningProfileMismatchError(

                f"Ontology reasoning profile '{entry.reasoning\_profile}' "

                f"does not match required profile '{required\_reasoning\_profile}'"

            )

    if not entry.base\_iri:

        raise InvalidOntologyModuleError(

            "base\_iri must be declared"

        )

    if not entry.preferred\_prefix:

        raise InvalidOntologyModuleError(

            "preferred\_prefix must be declared"

        )

    if not entry.validation\_rule\_refs:

        raise InvalidOntologyModuleError(

            "validation\_rule\_refs must be declared"

        )

    if not entry.compatibility\_policy\_ref:

        raise InvalidOntologyModuleError(

            "compatibility\_policy\_ref must be declared"

        )

---

## **40\. Test Scenarios**

Required tests:

1\. Reject unregistered Ontology Module.

2\. Reject inactive Ontology Module.

3\. Reject runtime use of deprecated Ontology Module.

4\. Reject blocked Ontology Module.

5\. Reject missing base IRI.

6\. Reject prefix conflicts.

7\. Reject missing namespace.

8\. Reject missing import dependency.

9\. Detect circular imports.

10\. Reject deprecated IRI reference.

11\. Reject missing class reference.

12\. Reject missing property reference.

13\. Reject missing SHACL shape.

14\. Reject missing reasoning profile.

15\. Reject heavy OWL reasoning on hot path.

16\. Reject release when competency question tests fail.

17\. Reject missing dependent registry impact analysis.

18\. Reject ontology version compatibility mismatch.

19\. Reject operational use while in migration\_required status.

20\. Verify ontology change audit trace creation.

21\. Verify replacement IRI mapping.

22\. Reject missing release artifact.

---

## **41\. Final Rule**

No registered Ontology Module,

no official semantic system.

No active Ontology Version,

no trustworthy registry reference.

No stable IRI,

no stable meaning.

Ontology is not Knowledge Graph.

Ontology is not World State.

Ontology is not Policy.

Ontology is not Approval.

Ontology is not Safety Gate.

Ontology is not PhysicalCommand.

Ontology defines meaning.

Registry defines operational validity.

`ontology_registry` is the core deterministic registry that governs the operational validity of every class, property, relation, axiom, shape, namespace, version, alignment, and reasoning profile used in the LEDO system.

This module ensures that every semantic IRI used by Agents, Models, Events, Evidence, Actions, Decisions, Approvals, Safety Gate, and Execution is grounded in an active ontology version.

The core definition is:

Ontology Registry

\= not a list of OWL files,

but an operational contract registry that controls

the version, namespace, IRI policy, import dependency,

alignment, class/property reference, axiom set,

SHACL shape, reasoning profile, validation rule,

migration rule, and audit trace

of every ontology module used in LEDO.

