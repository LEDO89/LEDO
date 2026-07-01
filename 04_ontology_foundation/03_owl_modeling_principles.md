# **Ontology foundation “OWL Modeling Principles”**

## **1\. Purpose**

This document defines the principles for OWL modeling in the LEDO Industrial Ontology Foundation.

In LEDO, OWL is not a simple list of terms. OWL is the semantic layer that formally defines semantic relationships among industrial objects, agents, sensors, events, risks, evidence, policies, action candidates, execution requests, and audit records.

The purpose of this document is to define:

OWL class design criteria  
Object property / Data property design criteria  
Axiom usage principles  
Domain / Range usage criteria  
Disjointness usage criteria  
EquivalentClass / sameAs restriction criteria  
Property characteristic usage criteria  
Restriction / Cardinality usage criteria  
OWL reasoning usage criteria  
Boundaries among OWL, SHACL, Policy, and Safety Gate  
Reasoning result materialization criteria

The core principle is as follows.

OWL defines meaning.  
SHACL validates data.  
Policy determines operational permission.  
Safety Gate performs deterministic pre-execution validation.  
Audit records the full decision path.

---

## **2\. Position Within the LEDO Structure**

This document belongs to the following location.

04\_ontology\_foundation/  
  03\_owl\_modeling\_principles/  
    owl\_modeling\_principles.md

This document is connected to the following documents.

00\_ontology\_foundation\_report  
→ Overall philosophy and core elements of the Foundation

01\_semantic\_web\_technology\_stack  
→ Responsibility separation among RDF, RDFS, OWL, SHACL, SPARQL, SKOS, PROV-O, OWL-Time, and GeoSPARQL

02\_upper\_ontology\_and\_standards  
→ BFO category discipline and international standards alignment

04\_reasoning\_and\_constraint\_model  
→ Boundary among Reasoning, Validation, Policy, and Safety Gate

05\_relationship\_and\_property\_design  
→ Object property and Data property design

06\_ontology\_governance\_and\_versioning  
→ Axiom changes, property changes, reasoner regression tests, and governance review

---

## **3\. Role of OWL**

In LEDO, OWL performs the following roles.

Class hierarchy definition  
Property hierarchy definition  
Formal semantic modeling  
Semantic restriction definition  
Class inference support  
Relationship inference support  
Consistency checking  
Unsatisfiable class detection  
Ontology QA  
Candidate semantic validation support  
Controlled semantic enrichment

OWL helps answer the following questions.

Which class does this object belong to?  
Which upper category does this class belong under?  
What domain and range does this relation have?  
Can this class and that class be true at the same time?  
Does this task semantically require a permit?  
Which sensor or agent generated this observation?  
Is this ActionCandidate semantically compatible with its target class?

However, OWL does not perform the following roles.

Final runtime execution permission decision  
Safety Gate hot path validation  
External system call  
Physical control execution  
Fact creation from AI output  
Raw telemetry storage  
High-frequency world state update

---

## **4\. Basic Layers of the OWL Model**

The LEDO OWL model consists of the following layers.

TBox  
→ Defines classes, properties, axioms, restrictions, and semantic structure

ABox  
→ Manages real object, event, observation, evidence, state, and action individuals

RBox  
→ Defines property hierarchy and property characteristics

LEDO follows these principles.

TBox must remain small but strong.  
ABox must be managed based on canonical identity.  
RBox must be designed carefully while avoiding property explosion.

---

## **5\. Class Modeling Principles**

An OWL class defines a semantic category.

A class is not a simple label. A class indicates which upper category a concept belongs to, what relations and restrictions it may have, and what reasoning it can participate in.

### **5.1 Foundation Class**

Foundation classes are upper-level concepts that can be commonly reused across industrial domains.

Examples are as follows.

Entity  
Agent  
HumanAgent  
RobotAgent  
PhysicalObject  
DigitalObject  
System  
Sensor  
Actuator  
Controller  
Task  
Process  
Event  
State  
Observation  
Evidence  
EvidenceBundle  
Risk  
Zone  
Policy  
Permit  
Action  
ActionCandidate  
ExecutionRequest  
Feedback  
AuditRecord  
Identifier

### **5.2 Domain Class**

Domain classes are classes specialized for a specific industry, site, customer, equipment family, or operational context.

Examples are as follows.

GasSensor  
ThermalSensor  
InspectionTask  
GasRisk  
RestrictedZone  
SpeedLimitedZone  
VentilationSystem  
AutonomousVehicle  
HumanoidRobot

Domain classes must extend Foundation classes and must not contaminate the Foundation.

### **5.3 Criteria for Creating a New Class**

Before creating a new class, check the following questions.

Can it be represented using an existing class?  
Should it belong to the Foundation or a Domain Module?  
From the BFO perspective, does it belong to material entity, process, information artifact, role, function, disposition, quality, site, or spatial region?  
Is this class necessary for reasoning?  
Can it be sufficiently represented with a SHACL shape?  
Can it be sufficiently represented as a SKOS concept?  
Is it merely a data field, status value, or UI label?  
Does it contribute to at least one competency question?

The core principle is as follows.

A class is a semantic category.  
Do not turn simple data fields, temporary tags, UI labels, or raw values into OWL classes.

---

## **6\. Class Naming Principles**

Class names must follow these criteria.

They must be clear.  
They must be stable.  
They must be understandable to domain experts.  
They must be semantically natural with their upper class.  
They must not be unnecessarily long.  
They must avoid excessive abbreviation.

Recommended examples are as follows.

Sensor  
GasSensor  
RobotAgent  
HumanoidRobot  
Observation  
GasObservation  
Risk  
GasRisk  
Zone  
DangerZone  
RestrictedZone  
Task  
InspectionTask  
ExecutionRequest

Examples to avoid are as follows.

Data1  
ObjectInfo  
ThingStatus  
TempClass  
SystemStuff  
GeneralNode  
AIResult

The core principle is as follows.

A class name must express a semantic category, not implementation convenience.

---

## **7\. SubClassOf Usage Principles**

`rdfs:subClassOf` defines a class hierarchy.

Examples are as follows.

ot:GasSensor rdfs:subClassOf ot:Sensor.  
ot:HumanoidRobot rdfs:subClassOf ot:RobotAgent.  
ot:InspectionTask rdfs:subClassOf ot:Task.  
ot:GasRisk rdfs:subClassOf ot:Risk.  
ot:DangerZone rdfs:subClassOf ot:Zone.

Before using `SubClassOf`, check the following.

Is A always B?  
Can every instance of A safely be treated as an instance of B?  
Does this hierarchy contribute to reasoning?  
Does this relation remain valid even when time and context change?

The principles are as follows.

A subclass must always satisfy the meaning of its superclass.  
Do not create a subclass relation merely because two concepts are similar.  
Class hierarchy affects reasoning results.  
An overly deep hierarchy makes maintenance difficult.

---

## **8\. EquivalentClass Usage Principles**

`owl:equivalentClass` declares that two classes have logically identical meanings.

This is a very strong axiom.

A equivalentClass B  
→ Every instance of A is an instance of B.  
→ Every instance of B is an instance of A.

LEDO uses `EquivalentClass` only in limited cases.

Allowed cases are as follows.

When an external standard class and a LEDO class have been strictly verified as identical  
When creating a logically defined class  
When defining a class through necessary and sufficient conditions  
When reasoning-based classification is required

Cases to avoid are as follows.

Using equivalentClass because labels are similar  
Using equivalentClass because translated terms are the same  
Using equivalentClass because an external standard term looks similar  
Using equivalentClass to merge classes for convenience

The core principle is as follows.

EquivalentClass is a very strong logical declaration.  
When uncertain, use a mapping relation or SKOS relation.

---

## **9\. DisjointClass Usage Principles**

`owl:disjointWith` means that two classes cannot be true for the same individual at the same time.

An example is as follows.

ot:PhysicalObject owl:disjointWith ot:InformationArtifact.

Disjointness is useful but dangerous.

It can be used in the following cases.

When categories are clearly different  
When being both would be a logical error  
When consistency checking is required  
When the separation remains valid even when time and context change

Be careful in the following cases.

When state changes over time  
When classification depends on context  
When the same object can perform multiple roles  
When sensor delay or data uncertainty exists  
When the class distinction is actually expressing runtime state

The core principle is as follows.

Stable category separation can be expressed with disjointness.  
Runtime conditions that change over time should be expressed with state, context, event, and time interval.

---

## **10\. Disjointness Examples**

### **10.1 Good Example**

PhysicalObject disjointWith InformationArtifact

Meaning:

One individual cannot be both a physical object and an information artifact.

A logical error example is as follows.

Robot\_01 rdf:type PhysicalObject.  
Robot\_01 rdf:type InformationArtifact.

This usage is relatively safe for the following reasons.

PhysicalObject and InformationArtifact belong to different upper categories.  
If these two concepts are confused, it is likely an identity modeling error.  
It helps reasoner consistency checking.

### **10.2 Bad Example**

SafeZone disjointWith DangerZone

At first, this may look reasonable, but it can be dangerous in industrial runtime systems.

A zone’s risk state can change over time.

09:00 Zone\_A is Safe  
09:05 GasRiskEvent occurs  
09:06 Zone\_A is Danger  
09:30 Ventilation completed  
09:40 Zone\_A returns to Safe

In this situation, if `SafeZone` and `DangerZone` are modeled as permanently disjoint classes, the time context is lost.

A better modeling approach is as follows.

Zone\_A rdf:type Zone.  
Zone\_A hasCurrentRiskState Danger.  
Zone\_A participatesIn GasRiskContext\_2026\_06\_24\_0905.

Or:

RiskContext\_001 affects Zone\_A.  
RiskContext\_001 hasRiskLevel High.  
RiskContext\_001 validDuring TimeInterval\_001.

The core principle is as follows.

Permanent category differences should be expressed with disjointness.  
Changing states should be expressed with state, context, event, and time interval.

---

## **11\. Object Property Modeling Principles**

Object properties define relationships between individuals.

Examples are as follows.

ot:locatedIn  
ot:observes  
ot:generatedBy  
ot:supportedBy  
ot:requires  
ot:authorizes  
ot:mitigates  
ot:affects  
ot:controls  
ot:requestsControl  
ot:hasTarget  
ot:hasEvidence

Object properties are the skeleton of the LEDO graph.

Before creating a new object property, check the following.

Is the direction of the relation clear?  
What are its domain and range?  
Can an existing property express it?  
Is an inverse property needed?  
Is a transitive property needed?  
Is it used for runtime validation?  
Is it used for audit trace?  
Is the relation stable enough to belong in the ontology?

The core principle is as follows.

Object properties are central to graph reasoning.  
Unnecessary property explosion must be avoided.

---

## **12\. Data Property Modeling Principles**

Data properties connect individuals to literal values.

Examples are as follows.

ot:hasTimestamp  
ot:hasConfidence  
ot:hasStatus  
ot:hasRiskLevel  
ot:hasBatteryLevel  
ot:hasTemperature  
ot:hasGasConcentration

Before creating a new data property, check the following.

Is the datatype clear?  
Is a unit required?  
Is QUDT or a unit reference required?  
Does the value change over time?  
Should it be stored in the RDF graph, world state store, or time-series store?  
Is it raw telemetry or a stable semantic attribute?

High-frequency raw telemetry must not all be stored as RDF data properties.

The core principle is as follows.

Stable attributes can be stored in the ontology graph.  
Dynamic high-frequency values should be stored in time-series or world state stores, with only necessary references in RDF.

---

## **13\. Domain / Range Usage Principles**

`rdfs:domain` and `rdfs:range` define the subject and object scope of a property.

Examples are as follows.

ot:observes rdfs:domain ot:Sensor.  
ot:observes rdfs:range ot:ObservableCondition.

ot:generatedBy rdfs:domain ot:Observation.  
ot:generatedBy rdfs:range ot:Sensor.

ot:hasTarget rdfs:domain ot:ActionCandidate.  
ot:hasTarget rdfs:range ot:Entity.

The important point is that domain/range can cause inference. They are not simple validation constraints.

For example:

ot:observes rdfs:domain ot:Sensor.  
X ot:observes Y.

A reasoner can infer:

X rdf:type Sensor.

Therefore, if domain/range is defined too narrowly, incorrect class inference may occur.

The principles are as follows.

The domain/range of Foundation properties must not be too narrow.  
Domain Modules may add more specific restrictions.  
Use SHACL when the purpose is data validation.  
Use Policy or Safety Gate Snapshot when the purpose is execution validation.

---

## **14\. Domain / Range Examples**

### **14.1 Bad Example: Range Too Narrow**

Assume the following property.

hasTarget rdfs:domain ActionCandidate.  
hasTarget rdfs:range Zone.

Then the following triple is added.

ActionCandidate\_01 hasTarget Robot\_01.

In this case, a reasoner may infer:

Robot\_01 rdf:type Zone.

This is incorrect inference.

The problem is that the range of `hasTarget` was defined too narrowly as `Zone`.

In LEDO, an action target may be not only a zone but also an agent, robot, system, task, external system, or physical object.

A better design is as follows.

hasTarget rdfs:domain ActionCandidate.  
hasTarget rdfs:range Entity.

Then action-type-specific target validation should be handled separately.

restrict\_access action  
→ target must be Zone

dispatch\_robot action  
→ target may be RobotAgent or Task

request\_inspection action  
→ target may be Zone, System, or PhysicalObject

notify\_manager action  
→ target may be HumanAgent or Role

The core principle is as follows.

OWL domain/range provides broad semantic inference.  
Specific execution validation belongs to SHACL, Policy, or Safety Gate Snapshot.

### **14.2 Good Example: Appropriately Broad Domain / Range**

generatedBy rdfs:domain Observation.  
generatedBy rdfs:range Agent.

In a Domain Module, this can be specialized further.

SensorObservation  
→ generatedBy some Sensor

ManualInspectionObservation  
→ generatedBy some HumanAgent

Actual data validation is then performed in SHACL.

SensorObservationShape  
→ generatedBy minCount 1  
→ generatedBy class Sensor

The core principle is as follows.

Foundation properties should remain broad.  
Domain Modules and SHACL should handle specialization.

---

## **15\. Inverse Property Usage Principles**

`owl:inverseOf` defines two properties as the same relation in opposite directions.

Examples are as follows.

ot:generatedBy owl:inverseOf ot:generates.  
ot:locatedIn owl:inverseOf ot:contains.  
ot:hasEvidence owl:inverseOf ot:supportsActionCandidate.

Inverse properties are useful for querying and reasoning, but overuse makes the graph complex.

Use them based on the following criteria.

Is bidirectional query frequently needed?  
Is it needed for audit trace?  
Is the reasoning benefit clear?  
Is the reverse relation logically exact?

Avoid them in the following cases.

When the reverse relation is not exactly the same relation  
When it is added only for query convenience  
When graph duplication becomes excessive

The core principle is as follows.

Use inverse properties only when the reverse relation is exact.  
Do not overuse inverse properties merely for query convenience.

---

## **16\. Transitive Property Usage Principles**

`owl:TransitiveProperty` means that a relation propagates along a chain.

Example:

A isPartOf B.  
B isPartOf C.  
→ A isPartOf C.

Candidate transitive properties in LEDO include:

isPartOf  
locatedWithin  
subZoneOf  
dependsOn

However, not every relation is transitive.

Use caution with the following relations.

controls  
observes  
affects  
supports  
authorizes  
mitigates

For example:

A controls B.  
B controls C.

This does not always mean:

A controls C.

The core principle is as follows.

Transitive properties can cause inference explosion.  
Use them only for relations that are truly mathematically or semantically transitive.

---

## **17\. Property Characteristic Usage Principles**

OWL property characteristics include the following.

FunctionalProperty  
InverseFunctionalProperty  
TransitiveProperty  
SymmetricProperty  
AsymmetricProperty  
ReflexiveProperty  
IrreflexiveProperty

LEDO uses property characteristics very carefully.

The following require particular caution.

FunctionalProperty  
→ Means that one subject can have only one object for that property.

InverseFunctionalProperty  
→ Means that one object can identify only one subject through that property.

TransitiveProperty  
→ Means that the relation propagates along a chain.

SymmetricProperty  
→ Means that if A has the relation with B, then B has the same relation with A.

Industrial systems have practical realities such as:

State changing over time  
Sensor errors  
Duplicate systems  
External identifier collisions  
Legacy migration issues  
Multiple data sources

Therefore, strong property characteristics can cause incorrect inference.

The core principle is as follows.

Property characteristics increase reasoning power, but also increase risk.  
Use them minimally in the Foundation.

---

## **18\. FunctionalProperty / InverseFunctionalProperty Examples**

### **18.1 FunctionalProperty Caution Example**

`FunctionalProperty` means that one subject can have only one object for the property.

The following declaration must be used carefully.

hasLocation rdf:type owl:FunctionalProperty.

In industrial systems, one object can have multiple location representations at the same time.

GPS location  
Indoor positioning location  
BIM coordinate  
Control room logical zone  
Last known location  
Estimated location

If `hasLocation` is declared as a FunctionalProperty, it may become difficult to handle different location representations simultaneously, and consistency issues or unintended inference may occur.

A safer design is as follows.

hasLocation  
hasCurrentLocation  
hasEstimatedLocation  
hasLastKnownLocation  
hasDesignLocation

The rule that there must be only one current location should be handled by world state logic, SHACL, Policy, or Safety Gate depending on the context.

### **18.2 InverseFunctionalProperty Caution Example**

`InverseFunctionalProperty` means that one object can identify only one subject through the property.

The following declaration must be used carefully.

hasSerialNumber rdf:type owl:InverseFunctionalProperty.

A serial number may look unique, but in real industrial systems, the following issues may occur.

Source system input error  
Vendor serial number duplication  
Temporary equipment ID  
Test device clone  
Legacy migration error  
Serial number reuse across vendors

An incorrect InverseFunctionalProperty can create the possibility that different physical objects are mistakenly merged into the same individual.

A safer design is as follows.

hasExternalIdentifier  
hasIdentifierScheme  
issuedBySourceSystem  
validDuring  
supportedBy IdentityResolutionEvidence

The core principle is as follows.

Do not use InverseFunctionalProperty just because an identifier appears unique.  
Identity must be resolved through evidence and governance.

---

## **19\. Restriction Usage Principles**

OWL restrictions define semantic conditions that a class has.

Major restrictions include:

someValuesFrom  
allValuesFrom  
hasValue  
minCardinality  
maxCardinality  
exactCardinality

Examples are as follows.

HighRiskTask  
→ requiresPermit some Permit

SensorObservation  
→ generatedBy some Sensor

ActionCandidate  
→ hasTarget some Entity

EvidenceBackedDecision  
→ supportedBy some EvidenceBundle

Restrictions are powerful, but they must not be confused with runtime data validation.

OWL restriction  
→ Semantic condition and reasoning

SHACL shape  
→ Actual data validation

The core principle is as follows.

Restriction defines meaning.  
SHACL validates whether required data exists.

---

## **20\. Boundary Between Restriction and SHACL**

Assume the following OWL restriction.

SensorObservation  
→ generatedBy some Sensor

The meaning is as follows.

A SensorObservation is semantically an observation generated by some Sensor.

However, if `generatedBy` is missing in actual ABox data, OWL alone cannot immediately determine that the data is invalid. This is because OWL follows Open World Assumption.

Actual validation is handled by SHACL.

SensorObservationShape  
→ generatedBy minCount 1  
→ generatedBy class Sensor

The distinction is as follows.

| Purpose | Technology |
| ----- | ----- |
| Define that SensorObservation is semantically generated by a Sensor | OWL restriction |
| Validate that generatedBy exists in actual data | SHACL minCount |
| Validate that the generatedBy target is a Sensor | SHACL class |
| Validate evidence freshness before execution | Safety Gate Snapshot |
| Determine whether an observation can be used as action evidence | Evidence \+ Policy \+ Safety Gate |

The core principle is as follows.

OWL restriction explains meaning.  
SHACL shape catches missing data and structural errors.  
Safety Gate validates usability at execution time.

---

## **21\. Cardinality Usage Principles**

Cardinality restricts the number of relationships.

Examples are as follows.

exactly 1 generatedBy Sensor  
min 1 supportedBy EvidenceBundle  
max 1 currentPrimaryState

Cardinality must be used very carefully.

The following situations are common in industrial systems.

One object may be connected to multiple sensors.  
One event may be supported by multiple evidence items.  
One ActionCandidate may have multiple risk reasons.  
One external object may have multiple identifiers.  
One object may have multiple location sources.

Foundation-level cardinality should be minimized.

Recommended principles are as follows.

Required minimum data should be validated with SHACL.  
OWL cardinality should be used only when it is logically unavoidable.  
Runtime state cardinality should be validated by Policy or Safety Gate.

---

## **22\. sameAs Usage Principles**

`owl:sameAs` declares that two individuals are exactly the same entity.

This is a very strong equality declaration.

A owl:sameAs B  
→ All facts about A also apply to B.  
→ All facts about B also apply to A.

LEDO restricts `owl:sameAs` by default.

Do not use `sameAs` immediately just because external IDs appear to match.

The recommended identity flow is as follows.

External Identifier  
→ Identifier Mapping Record  
→ Identity Resolution Evidence  
→ Canonical Identity  
→ ABox Hash IRI

Alternative relations are as follows.

ot:possiblySameAs  
ot:externallyMappedTo  
ot:hasExternalIdentifier  
ot:resolvedAsCanonicalIdentity  
ot:sourceSystemIdentifier

The core principle is as follows.

sameAs is a very strong equality declaration.  
If uncertain, do not use sameAs.

---

## **23\. sameAs Examples**

### **23.1 Bad Example**

IFC\_Object\_123 owl:sameAs LEDO\_Object\_456.

This declaration is dangerous for the following reasons.

The external object may be a design object, not a runtime object.  
The same external ID may be reused in another context.  
The IFC object may change while the LEDO canonical object must remain stable.  
Source-specific facts may propagate incorrectly.  
Audit may have difficulty tracing which source created which fact.

A better design is as follows.

LEDO\_Object\_456 hasExternalIdentifier IFC\_GlobalId\_123.  
LEDO\_Object\_456 externallyMappedTo IFC\_Object\_123.  
IdentityResolutionRecord\_01 resolvedAsCanonicalIdentity LEDO\_Object\_456.  
IdentityResolutionRecord\_01 supportedBy EvidenceBundle\_77.

### **23.2 Limited Cases Where sameAs May Be Considered**

`sameAs` may be considered only when all of the following conditions are satisfied.

Both individuals refer to exactly the same real-world entity.  
All facts from both sides can be shared without logical problems.  
The identity policy of the source system is trustworthy.  
Identity resolution evidence exists.  
Governance review has approved it.

Otherwise, use a mapping relation.

The core principle is as follows.

Identity is not solved by sameAs alone.  
Identity is resolved through canonical identity, mapping records, evidence, and governance.

---

## **24\. Open World Assumption**

OWL follows Open World Assumption.

That means:

Lack of information does not mean false.

For example:

There is no information that Observation\_1 was generatedBy Sensor\_1.

This does not mean:

Observation\_1 was not generated by a Sensor.

It only means:

Unknown.

This is very important in runtime validation.

OWL  
→ Unknown when information is missing

SHACL / Safety Gate  
→ Required missing information may become invalid, deny, hold, or escalate

The core principle is as follows.

OWL is open-world.  
Safety Gate requires closed-world-like validation.  
Therefore, runtime validation must not rely only on OWL.

---

## **25\. OWL Reasoning Usage Criteria**

OWL reasoners are used for the following.

Ontology consistency checking  
Unsatisfiable class detection  
Class hierarchy inference  
Property inference  
Controlled semantic enrichment  
Release validation  
Axiom change impact assessment  
Regression testing

OWL reasoners are not used directly for the following.

Safety Gate hot path  
Real-time execution validation  
External control request generation  
Raw telemetry processing  
High-frequency world state update  
Low-level physical control

Reasoning results are precomputed and converted into materialized views or Safety Gate Runtime Snapshot.

OWL Reasoning  
→ inferred\_class\_map  
→ class membership bitset  
→ selected relation closure  
→ materialized semantic view  
→ Safety Gate Runtime Snapshot

---

## **26\. Reasoning Result Materialization**

LEDO does not directly execute OWL reasoning in the runtime hot path.

Reasoning results are precomputed and converted into materialized views or Safety Gate Runtime Snapshot.

### **26.1 Reasoning Results That Can Be Precomputed**

The following results can be precomputed.

Class membership inference  
Subclass closure  
Property hierarchy expansion  
Selected inverse relation expansion  
Selected transitive closure  
Risk-action compatibility  
Task-permit requirement  
Zone containment relation  
Agent capability classification  
Object category classification

Example:

GasSensor subClassOf Sensor.  
Sensor subClassOf PhysicalObject.

GasSensor\_01 rdf:type GasSensor.

Reasoning result:  
GasSensor\_01 rdf:type Sensor.  
GasSensor\_01 rdf:type PhysicalObject.

Materialized form:

inferred\_class\_map\[GasSensor\_01\] \= {  
  GasSensor,  
  Sensor,  
  PhysicalObject  
}

Runtime-optimized form:

class\_membership\_bitset\[object\_id\] \= 0b010010001...

### **26.2 Reasoning Results That the Safety Gate May Query**

The Safety Gate may need to answer the following questions quickly.

Is this target a Zone?  
Is this action type allowed for this target class?  
Can this action mitigate this risk type?  
Does this task require a permit?  
Is this evidence fresh?  
Does this agent have the required role?  
Is this external system available?  
Is this zone currently restricted?

The snapshot tables required for this include:

target\_class\_bitset  
action\_target\_permission\_matrix  
risk\_action\_matrix  
task\_permit\_requirement\_map  
evidence\_freshness\_map  
agent\_role\_permission\_map  
external\_system\_health\_map  
zone\_restriction\_map

### **26.3 Reasoning Result Generation Flow**

OWL TBox  
→ controlled reasoner execution  
→ inferred hierarchy  
→ inferred class membership  
→ relation expansion  
→ semantic materialized view  
→ Safety Gate Runtime Snapshot  
→ lock-free read-only lookup

The detailed flow is as follows.

1\. Fix ontology version  
2\. TBox consistency check  
3\. Sample ABox validation  
4\. Execute OWL reasoner  
5\. Generate inferred class map  
6\. Generate selected relation closure  
7\. Combine SHACL validation result flags  
8\. Combine Policy pre-check results  
9\. Convert into Snapshot schema  
10\. Validate checksum / version / timestamp  
11\. Publish as active snapshot

The core principle is as follows.

Reasoning runs in the background.  
Safety Gate queries reasoning results.

---

## **27\. Boundary Between OWL and SHACL**

OWL and SHACL have different purposes.

| Category | OWL | SHACL |
| ----- | ----- | ----- |
| Purpose | Meaning definition and reasoning | Data validation |
| World assumption | Open World | Close to closed-world validation |
| Usage timing | Modeling, reasoning, QA | Data input, state change, candidate validation |
| Failure meaning | Inconsistency or unsatisfiability | Validation violation |
| Runtime usage | Precomputed / controlled | Validation pipeline |

The core principle is as follows.

OWL defines what something is.  
SHACL validates whether the data has the required shape.

---

## **28\. Boundary Between OWL and Policy**

OWL defines meaning.  
Policy determines operational permission and prohibition.

OWL may state the following.

HighRiskTask requiresPermit some Permit.

But Policy performs the following judgments.

Does this user have authority to approve this task now?  
Is this action allowed under current operational policy?  
Can this action be automatically executed in this state?  
Does this action require human approval?

The core principle is as follows.

OWL does not replace policy decisions.  
Policy can use ontology meaning, but operational permission judgment is performed by the Policy Engine.

---

## **29\. Boundary Between OWL and Safety Gate**

The Safety Gate is the final checkpoint immediately before execution.

The Safety Gate does not directly perform OWL reasoning.

The Safety Gate performs the following.

Precomputed inference lookup  
Candidate validity flag check  
Evidence freshness check  
Approval validity check  
Policy result check  
External system health check  
Conflict matrix check  
allow / deny / hold / escalate decision

The core principle is as follows.

OWL reasoning creates material for the Safety Gate.  
The Safety Gate immediately looks up that material.

---

## **30\. Competency Question-Based Modeling**

OWL modeling must be validated through competency questions.

A new class, property, or axiom must contribute to answering at least one meaningful question.

Examples are as follows.

CQ-01.  
Which ActionCandidate is supported by which EvidenceBundle?

CQ-02.  
Which RiskEvent affects which Zone?

CQ-03.  
What Restriction is currently applied to a specific Zone?

CQ-04.  
Which Task can a specific RobotAgent perform?

CQ-05.  
Which Task requires a Permit, and is that Permit still valid?

CQ-06.  
Which Sensor or Agent generated a specific Observation?

CQ-07.  
Which source system and timestamp does a specific EvidenceBundle have?

CQ-08.  
Is the target of a specific ActionCandidate within the allowed range for its action type?

CQ-09.  
Which ExecutionRequest did a specific ExternalControlRequest originate from?

CQ-10.  
Which snapshot version and policy version were used for a specific Safety Gate decision?

CQ-11.  
Which GeofencingBoundary or SpatialRegion contains a specific Zone?

CQ-12.  
If a specific action was denied, was the denial reason evidence shortage, policy violation, state conflict, or external system unavailability?

Each competency question must be connected to the following.

Required class  
Required object property  
Required data property  
Required SHACL shape  
Required SPARQL query  
Required materialized view  
Required audit field

Example:

CQ:  
Is the target of a specific ActionCandidate within the allowed range for its action type?

Required classes:  
ActionCandidate, Action, Entity, Zone, Agent, System

Required properties:  
hasTarget, hasActionType

Required validation:  
action\_target\_permission\_matrix

Required runtime structure:  
SafetyGateSnapshot.action\_permission\_map

Required audit:  
decision\_reason\_code, snapshot\_version

The core principle is as follows.

Ontology elements that do not answer meaningful questions should be removed or deferred.

---

## **31\. OWL Change Management Principles**

Changes to OWL classes, properties, and axioms are governance targets.

The following changes must be reviewed.

domain/range change  
disjointness addition  
equivalentClass addition  
sameAs addition  
transitive property addition  
cardinality restriction addition  
inverse property change  
class hierarchy relocation  
property hierarchy relocation  
property characteristic addition

When changes occur, perform the following checks.

Reasoner consistency check  
Unsatisfiable class check  
Sample ABox inference comparison  
SHACL regression test  
Competency question regression test  
Module dependency check  
Runtime safety impact review

The core principle is as follows.

OWL changes can change meaning and inference.  
Therefore, OWL changes must go through governance, review, and regression testing.

---

## **32\. OWL Modeling Anti-Patterns**

| Anti-pattern | Why It Is Dangerous | Practical Damage | Alternative |
| ----- | ----- | ----- | ----- |
| Turning every term into a class | Ontology becomes a word list instead of a meaning model | Class explosion makes reasoning and maintenance difficult | Separate SKOS vocabulary from OWL classes |
| Turning simple data fields into classes | Class hierarchy becomes polluted like a data schema | Unnecessary classes such as TemperatureValue and BatteryLevelValue increase | Use data properties, SHACL, and time-series stores |
| Setting domain/range too narrowly | Unwanted class inference occurs | A Robot may be inferred as a Zone | Keep the Foundation broad and specialize in Domain Modules |
| Overusing disjointness | Time and state changes cannot be represented | SafeZone/DangerZone transition may cause inconsistency | Use state, context, event, and time interval |
| Overusing EquivalentClass | Similar concepts are forced into the same meaning | External standard changes may collapse internal class meaning | Use mapping relations or SKOS relations |
| Overusing sameAs | Identity pollution and fact propagation errors occur | Different source objects may be merged and audit may fail | Use canonical identity and mapping records |
| Overusing TransitiveProperty | Inference explosion occurs | Relation closure becomes large and reasoner performance degrades | Use only for truly transitive relations |
| Overusing FunctionalProperty | Real-world multi-value states become difficult to represent | Multiple location sources may conflict | Separate current / estimated / last-known / design location |
| Overusing InverseFunctionalProperty | Incorrect identifiers may create object merge risk | Serial number errors may make different objects appear as one | Use identifier scheme \+ source \+ evidence |
| Replacing SHACL validation with OWL restriction | Missing data is not detected | Observations without generatedBy may pass | Use SHACL minCount / class validation |
| Running a reasoner inside the Safety Gate | Runtime jitter and timeout occur | Pre-execution validation bottleneck | Use Safety Snapshot |
| Directly inserting AI output as OWL facts | Hallucination enters the ontology | Nonexistent risk/event becomes factual | Reflect only after evidence-backed validation |
| Copying external standard classes directly into the Foundation | Foundation becomes dependent on external schema | IFC/OPC-UA changes destabilize the core ontology | Use Mapping Modules |
| Storing logical boundary only as a string | Spatial reasoning becomes impossible | Geofencing/access/speed restriction validation fails | Use GeoSPARQL \+ SpatialRegion modeling |
| Modeling runtime state as a permanent class | Time change and state transition are lost | Current state and past state conflict | Use State/Event/TimeInterval model |

---

## **33\. The Five Most Important Principles in This Document**

### **33.1 A Class Is Not a Tag**

A class is not a simple label.  
A class is a semantic category with upper category, relations, axioms, and reasoning implications.

Simple state values, data fields, temporary labels, and UI labels must not be made into classes.

### **33.2 OWL Defines Meaning and SHACL Validates Data**

OWL restriction  
→ semantic condition

SHACL shape  
→ actual data validation

OWL follows Open World Assumption.  
SHACL is required to detect missing data.

### **33.3 Strong Axioms Must Be Minimized**

The following axioms must be used very carefully.

equivalentClass  
disjointWith  
sameAs  
FunctionalProperty  
InverseFunctionalProperty  
TransitiveProperty  
cardinality restriction

Strong axioms increase reasoning power, but when misused, they can contaminate the entire ontology.

### **33.4 Runtime Safety Gate Is Not an OWL Reasoner**

OWL reasoning  
→ background / controlled reasoning layer

Safety Gate  
→ precomputed snapshot lookup

The Safety Gate hot path must not perform OWL reasoning, full SHACL validation, SPARQL, external API calls, or LLM calls.

### **33.5 Identity Is Resolved Through Canonical Identity and Evidence, Not sameAs**

External Identifier  
→ Mapping Record  
→ Identity Resolution Evidence  
→ Canonical Identity  
→ ABox Hash IRI

Do not use `owl:sameAs` immediately just because external IDs appear to match.  
Identity is a core area that requires evidence and governance.

---

## **34\. Final Core Principles**

Class is a semantic category.  
Property is a semantic relationship.  
Axiom is a rule that fixes meaning.  
Restriction is a semantic condition.  
SHACL is data validation.  
Policy is operational decision-making.  
Safety Gate is deterministic pre-execution validation.  
Reasoner must belong to a controlled reasoning layer, not the runtime hot path.  
AI output is candidate interpretation, not an ontology fact.  
External standards are mapped, not copied.  
Identity is managed through canonical identity and evidence.

---

## **35\. Final Conclusion**

LEDO OWL modeling is not about creating many classes.

LEDO OWL modeling is the work of fixing industrial meaning into a structure that can be:

Inferable  
Validatable  
Auditable  
Governable  
Standards-aligned  
Runtime-safe  
Connected to Physical AI execution boundaries

The final principle is as follows.

OWL creates meaning.  
SHACL validates data.  
Policy determines permission.  
Safety Gate validates executability.  
Audit records the full path.

And the final architectural boundary is as follows.

OWL is the semantic engine of LEDO.  
But OWL is not the Safety Gate.

OWL creates meaning,  
and the Safety Gate validates executability.

