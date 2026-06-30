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

# **OWL 모델링 원칙**

## **1\. 목적**

이 문서는 LEDO Industrial Ontology Foundation에서 OWL 모델링을 수행할 때 따라야 할 원칙을 정의한다.

LEDO에서 OWL은 단순한 용어 목록이 아니다. OWL은 산업 객체, 에이전트, 센서, 사건, 위험, 증거, 정책, 행동 후보, 실행 요청, 감사 기록 사이의 의미 관계를 형식적으로 정의하는 semantic layer다.

이 문서의 목적은 다음과 같다.

OWL class 설계 기준 정의  
Object property / Data property 설계 기준 정의  
Axiom 사용 원칙 정의  
Domain / Range 사용 기준 정의  
Disjointness 사용 기준 정의  
EquivalentClass / sameAs 사용 제한 기준 정의  
Property characteristic 사용 기준 정의  
Restriction / Cardinality 사용 기준 정의  
OWL reasoning 활용 기준 정의  
OWL, SHACL, Policy, Safety Gate의 경계 정의  
Reasoning 결과 materialization 기준 정의

핵심 원칙은 다음과 같다.

OWL은 의미를 정의한다.  
SHACL은 데이터를 검증한다.  
Policy는 운영 허용 여부를 판단한다.  
Safety Gate는 실행 직전 결정론적 검증을 수행한다.  
Audit은 전체 판단 경로를 기록한다.

---

## **2\. LEDO 구조 안에서의 위치**

이 문서는 다음 위치에 속한다.

04\_ontology\_foundation/  
  03\_owl\_modeling\_principles/  
    owl\_modeling\_principles.md

이 문서는 다음 문서들과 연결된다.

00\_ontology\_foundation\_report  
→ Foundation 전체 철학과 핵심 요소

01\_semantic\_web\_technology\_stack  
→ RDF, RDFS, OWL, SHACL, SPARQL, SKOS, PROV-O, OWL-Time, GeoSPARQL의 책임 분리

02\_upper\_ontology\_and\_standards  
→ BFO category discipline과 국제 표준 정렬

04\_reasoning\_and\_constraint\_model  
→ Reasoning, Validation, Policy, Safety Gate의 경계

05\_relationship\_and\_property\_design  
→ Object property와 Data property 설계

06\_ontology\_governance\_and\_versioning  
→ Axiom 변경, property 변경, reasoner regression test, governance review

---

## **3\. OWL의 역할**

LEDO에서 OWL은 다음 역할을 수행한다.

Class hierarchy 정의  
Property hierarchy 정의  
Formal semantic modeling  
Semantic restriction 정의  
Class inference 지원  
Relationship inference 지원  
Consistency checking  
Unsatisfiable class 탐지  
Ontology QA  
Candidate semantic validation 지원  
Controlled semantic enrichment

OWL은 다음 질문에 답하는 데 도움을 준다.

이 객체는 어떤 class에 속하는가?  
이 class는 어떤 상위 category 아래에 있는가?  
이 relation은 어떤 domain과 range를 가지는가?  
이 class와 저 class는 동시에 성립 가능한가?  
이 task는 의미상 permit을 요구하는가?  
이 observation은 어떤 sensor 또는 agent에 의해 생성되었는가?  
이 ActionCandidate는 target class와 의미적으로 맞는가?

하지만 OWL은 다음 역할을 하지 않는다.

최종 runtime execution permission 판단  
Safety Gate hot path 검증  
외부 시스템 호출  
물리 제어 실행  
AI output의 사실화  
raw telemetry 저장  
high-frequency world state update

---

## **4\. OWL 모델의 기본 계층**

LEDO OWL 모델은 다음 계층으로 구성된다.

TBox  
→ class, property, axiom, restriction, semantic structure 정의

ABox  
→ 실제 object, event, observation, evidence, state, action individual 관리

RBox  
→ property hierarchy와 property characteristic 정의

LEDO는 다음 원칙을 따른다.

TBox는 작고 강하게 유지한다.  
ABox는 canonical identity 기반으로 관리한다.  
RBox는 property explosion을 피하며 신중하게 설계한다.

---

## **5\. Class 모델링 원칙**

OWL class는 의미 범주를 정의한다.

Class는 단순 label이 아니다. Class는 해당 개념이 어떤 상위 category에 속하고, 어떤 relation과 restriction을 가지며, 어떤 reasoning에 참여할 수 있는지를 나타낸다.

### **5.1 Foundation Class**

Foundation class는 산업 도메인 전반에서 공통으로 재사용될 수 있는 상위 개념이다.

예시는 다음과 같다.

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

Domain class는 특정 산업, 현장, 고객, 장비군, 운영 맥락에 특화된 class다.

예시는 다음과 같다.

GasSensor  
ThermalSensor  
InspectionTask  
GasRisk  
RestrictedZone  
SpeedLimitedZone  
VentilationSystem  
AutonomousVehicle  
HumanoidRobot

Domain class는 Foundation class 아래에 확장되어야 하며, Foundation을 오염시켜서는 안 된다.

### **5.3 새 Class 생성 기준**

새 class를 만들기 전에 다음 질문을 확인한다.

이미 존재하는 class로 표현 가능한가?  
Foundation에 들어가야 하는가, Domain Module에 들어가야 하는가?  
BFO 기준으로 material entity, process, information artifact, role, function, disposition, quality, site, spatial region 중 어디에 속하는가?  
Reasoning에 필요한 class인가?  
SHACL shape로 충분히 표현 가능한가?  
SKOS concept으로 충분한가?  
단순 data field, status value, UI label은 아닌가?  
하나 이상의 competency question에 기여하는가?

핵심 원칙은 다음과 같다.

Class는 의미 범주다.  
단순 데이터 필드, 임시 태그, UI label, raw value를 OWL class로 만들지 않는다.

---

## **6\. Class Naming 원칙**

Class 이름은 다음 기준을 따른다.

명확해야 한다.  
안정적이어야 한다.  
도메인 전문가가 이해할 수 있어야 한다.  
상위 class와 의미적으로 자연스러워야 한다.  
불필요하게 길지 않아야 한다.  
약어 남용을 피해야 한다.

권장 예시는 다음과 같다.

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

피해야 할 예시는 다음과 같다.

Data1  
ObjectInfo  
ThingStatus  
TempClass  
SystemStuff  
GeneralNode  
AIResult

핵심 원칙은 다음과 같다.

Class 이름은 구현 편의가 아니라 의미 범주를 표현해야 한다.

---

## **7\. SubClassOf 사용 원칙**

`rdfs:subClassOf`는 class hierarchy를 정의한다.

예시는 다음과 같다.

ot:GasSensor rdfs:subClassOf ot:Sensor.  
ot:HumanoidRobot rdfs:subClassOf ot:RobotAgent.  
ot:InspectionTask rdfs:subClassOf ot:Task.  
ot:GasRisk rdfs:subClassOf ot:Risk.  
ot:DangerZone rdfs:subClassOf ot:Zone.

`SubClassOf`를 사용하기 전에는 다음을 확인한다.

A는 항상 B인가?  
A의 모든 instance를 B의 instance로 안전하게 볼 수 있는가?  
이 hierarchy가 reasoning에 기여하는가?  
시간과 맥락이 바뀌어도 이 관계가 유지되는가?

원칙은 다음과 같다.

하위 class는 상위 class의 의미를 항상 만족해야 한다.  
비슷하다는 이유만으로 subclass를 만들지 않는다.  
Class hierarchy는 reasoning 결과에 영향을 준다.  
너무 깊은 hierarchy는 유지보수를 어렵게 한다.

---

## **8\. EquivalentClass 사용 원칙**

`owl:equivalentClass`는 두 class가 논리적으로 동일한 의미를 가진다고 선언한다.

이는 매우 강한 공리다.

A equivalentClass B  
→ A의 모든 instance는 B의 instance다.  
→ B의 모든 instance는 A의 instance다.

LEDO는 `EquivalentClass`를 제한적으로 사용한다.

사용 가능한 경우는 다음과 같다.

외부 표준 class와 LEDO class가 엄격히 동일하다고 검증된 경우  
논리적 정의 class를 만들 때  
necessary and sufficient condition으로 class를 정의할 때  
reasoning 기반 classification이 필요한 경우

피해야 할 경우는 다음과 같다.

label이 비슷해서 equivalentClass 사용  
번역어가 같아서 equivalentClass 사용  
외부 표준 term이 유사해서 equivalentClass 사용  
편의를 위해 class를 병합하기 위해 사용

핵심 원칙은 다음과 같다.

EquivalentClass는 매우 강한 논리 선언이다.  
확실하지 않으면 mapping relation 또는 SKOS relation을 사용한다.

---

## **9\. DisjointClass 사용 원칙**

`owl:disjointWith`는 두 class가 동일 individual에 대해 동시에 성립할 수 없음을 의미한다.

예시는 다음과 같다.

ot:PhysicalObject owl:disjointWith ot:InformationArtifact.

Disjointness는 유용하지만 위험하다.

사용할 수 있는 경우는 다음과 같다.

category가 명확히 다른 경우  
동시에 성립하면 논리 오류인 경우  
consistency checking이 필요한 경우  
시간과 맥락이 바뀌어도 분리가 유지되는 경우

주의해야 할 경우는 다음과 같다.

상태가 시간에 따라 변하는 경우  
classification이 맥락에 의존하는 경우  
같은 object가 여러 role을 수행할 수 있는 경우  
센서 지연 또는 데이터 불확실성이 있는 경우  
class 구분이 사실상 runtime state를 표현하는 경우

핵심 원칙은 다음과 같다.

안정적인 category 분리는 disjointness로 표현할 수 있다.  
시간에 따라 변하는 runtime condition은 state, context, event, time interval로 표현한다.

---

## **10\. Disjointness 예시**

### **10.1 좋은 예시**

PhysicalObject disjointWith InformationArtifact

의미:

하나의 individual이 동시에 물리 객체이면서 정보 객체일 수 없다는 선언이다.

논리 오류 예시는 다음과 같다.

Robot\_01 rdf:type PhysicalObject.  
Robot\_01 rdf:type InformationArtifact.

이 사용이 비교적 안전한 이유는 다음과 같다.

PhysicalObject와 InformationArtifact는 상위 category가 다르다.  
두 개념이 혼동되면 identity modeling 오류일 가능성이 높다.  
Reasoner consistency checking에 도움이 된다.

### **10.2 나쁜 예시**

SafeZone disjointWith DangerZone

처음에는 합리적으로 보이지만 산업 runtime에서는 위험할 수 있다.

Zone의 위험 상태는 시간에 따라 바뀔 수 있기 때문이다.

09:00 Zone\_A is Safe  
09:05 GasRiskEvent 발생  
09:06 Zone\_A is Danger  
09:30 Ventilation 완료  
09:40 Zone\_A returns to Safe

이 상황에서 `SafeZone`과 `DangerZone`을 영구적으로 disjoint한 class로 만들면 시간 맥락을 잃는다.

더 나은 모델링은 다음과 같다.

Zone\_A rdf:type Zone.  
Zone\_A hasCurrentRiskState Danger.  
Zone\_A participatesIn GasRiskContext\_2026\_06\_24\_0905.

또는:

RiskContext\_001 affects Zone\_A.  
RiskContext\_001 hasRiskLevel High.  
RiskContext\_001 validDuring TimeInterval\_001.

핵심 원칙은 다음과 같다.

영구적인 category 차이는 disjointness로 표현한다.  
변하는 상태는 state, context, event, time interval로 표현한다.

---

## **11\. Object Property 모델링 원칙**

Object property는 individual과 individual 사이의 관계를 정의한다.

예시는 다음과 같다.

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

Object property는 LEDO graph의 뼈대다.

새 object property를 만들기 전에 다음을 확인한다.

관계 방향이 명확한가?  
domain과 range는 무엇인가?  
기존 property로 표현 가능한가?  
inverse property가 필요한가?  
transitive property가 필요한가?  
runtime validation에 사용되는가?  
audit trace에 사용되는가?  
ontology에 둘 만큼 안정적인 관계인가?

핵심 원칙은 다음과 같다.

Object property는 graph reasoning의 핵심이다.  
불필요한 property explosion을 피해야 한다.

---

## **12\. Data Property 모델링 원칙**

Data property는 individual과 literal value를 연결한다.

예시는 다음과 같다.

ot:hasTimestamp  
ot:hasConfidence  
ot:hasStatus  
ot:hasRiskLevel  
ot:hasBatteryLevel  
ot:hasTemperature  
ot:hasGasConcentration

새 data property를 만들기 전에 다음을 확인한다.

datatype이 명확한가?  
unit이 필요한가?  
QUDT 또는 unit reference가 필요한가?  
시간에 따라 변하는 값인가?  
RDF graph, world state store, time-series store 중 어디에 있어야 하는가?  
raw telemetry인가, stable semantic attribute인가?

고빈도 raw telemetry를 모두 RDF data property로 저장해서는 안 된다.

핵심 원칙은 다음과 같다.

Stable attribute는 ontology graph에 둘 수 있다.  
Dynamic high-frequency value는 time-series 또는 world state store에 두고, RDF에는 필요한 reference만 둔다.

---

## **13\. Domain / Range 사용 원칙**

`rdfs:domain`과 `rdfs:range`는 property의 subject와 object 범위를 정의한다.

예시는 다음과 같다.

ot:observes rdfs:domain ot:Sensor.  
ot:observes rdfs:range ot:ObservableCondition.

ot:generatedBy rdfs:domain ot:Observation.  
ot:generatedBy rdfs:range ot:Sensor.

ot:hasTarget rdfs:domain ot:ActionCandidate.  
ot:hasTarget rdfs:range ot:Entity.

주의할 점은 domain/range가 단순 validation constraint가 아니라 inference를 발생시킬 수 있다는 점이다.

예를 들어:

ot:observes rdfs:domain ot:Sensor.  
X ot:observes Y.

Reasoner는 다음을 추론할 수 있다.

X rdf:type Sensor.

따라서 domain/range를 너무 좁게 잡으면 잘못된 class inference가 생길 수 있다.

원칙은 다음과 같다.

Foundation property의 domain/range는 지나치게 좁게 잡지 않는다.  
Domain Module에서 더 구체적인 restriction을 추가할 수 있다.  
데이터 검증 목적이면 SHACL을 사용한다.  
실행 검증 목적이면 Policy 또는 Safety Gate Snapshot을 사용한다.

---

## **14\. Domain / Range 예시**

### **14.1 나쁜 예시: Range를 너무 좁게 잡은 경우**

다음 property가 있다고 가정한다.

hasTarget rdfs:domain ActionCandidate.  
hasTarget rdfs:range Zone.

그리고 다음 triple이 들어온다.

ActionCandidate\_01 hasTarget Robot\_01.

이 경우 reasoner는 다음을 추론할 수 있다.

Robot\_01 rdf:type Zone.

이는 잘못된 inference다.

문제는 `hasTarget`의 range를 `Zone`으로 너무 좁게 정의했기 때문이다.

LEDO에서 action target은 zone뿐 아니라 agent, robot, system, task, external system, physical object가 될 수 있다.

더 나은 설계는 다음과 같다.

hasTarget rdfs:domain ActionCandidate.  
hasTarget rdfs:range Entity.

그리고 action type별 target 검증은 별도로 처리한다.

restrict\_access action  
→ target must be Zone

dispatch\_robot action  
→ target may be RobotAgent or Task

request\_inspection action  
→ target may be Zone, System, or PhysicalObject

notify\_manager action  
→ target may be HumanAgent or Role

핵심 원칙은 다음과 같다.

OWL domain/range는 넓은 의미 추론을 제공한다.  
구체적 실행 검증은 SHACL, Policy, Safety Gate Snapshot이 담당한다.

### **14.2 좋은 예시: 적절히 넓은 Domain / Range**

generatedBy rdfs:domain Observation.  
generatedBy rdfs:range Agent.

Domain Module에서는 더 구체화할 수 있다.

SensorObservation  
→ generatedBy some Sensor

ManualInspectionObservation  
→ generatedBy some HumanAgent

그리고 실제 데이터 검증은 SHACL에서 수행한다.

SensorObservationShape  
→ generatedBy minCount 1  
→ generatedBy class Sensor

핵심 원칙은 다음과 같다.

Foundation property는 넓게 둔다.  
Domain Module과 SHACL에서 구체화한다.

---

## **15\. Inverse Property 사용 원칙**

`owl:inverseOf`는 두 property가 서로 반대 방향의 동일한 관계임을 정의한다.

예시는 다음과 같다.

ot:generatedBy owl:inverseOf ot:generates.  
ot:locatedIn owl:inverseOf ot:contains.  
ot:hasEvidence owl:inverseOf ot:supportsActionCandidate.

Inverse property는 query와 reasoning에 유용하지만 남용하면 graph가 복잡해진다.

사용 기준은 다음과 같다.

양방향 query가 자주 필요한가?  
Audit trace에 필요한가?  
Reasoning 이점이 분명한가?  
반대 방향 관계가 논리적으로 정확한가?

피해야 할 경우는 다음과 같다.

반대 관계가 정확히 동일하지 않은 경우  
단순 query 편의를 위해 추가하는 경우  
graph duplication이 과도하게 증가하는 경우

핵심 원칙은 다음과 같다.

Inverse property는 정확한 반대 관계일 때만 사용한다.  
단순 query 편의만으로 남용하지 않는다.

---

## **16\. Transitive Property 사용 원칙**

`owl:TransitiveProperty`는 관계가 chain을 따라 전이됨을 의미한다.

예시는 다음과 같다.

A isPartOf B.  
B isPartOf C.  
→ A isPartOf C.

LEDO에서 transitive property 후보는 다음과 같다.

isPartOf  
locatedWithin  
subZoneOf  
dependsOn

하지만 모든 관계가 전이되는 것은 아니다.

주의해야 할 관계는 다음과 같다.

controls  
observes  
affects  
supports  
authorizes  
mitigates

예를 들어:

A controls B.  
B controls C.

이것이 항상 다음을 의미하지는 않는다.

A controls C.

핵심 원칙은 다음과 같다.

Transitive property는 inference explosion을 만들 수 있다.  
정말 수학적 또는 의미적으로 전이되는 관계에만 사용한다.

---

## **17\. Property Characteristic 사용 원칙**

OWL property characteristic에는 다음이 있다.

FunctionalProperty  
InverseFunctionalProperty  
TransitiveProperty  
SymmetricProperty  
AsymmetricProperty  
ReflexiveProperty  
IrreflexiveProperty

LEDO는 property characteristic을 매우 신중하게 사용한다.

특히 다음은 주의가 필요하다.

FunctionalProperty  
→ 하나의 subject가 해당 property로 하나의 object만 가질 수 있음을 의미한다.

InverseFunctionalProperty  
→ 하나의 object가 해당 property로 하나의 subject만 가질 수 있음을 의미한다.

TransitiveProperty  
→ 관계가 chain을 따라 전이됨을 의미한다.

SymmetricProperty  
→ A가 B와 관계를 가지면 B도 A와 같은 관계를 가진다는 의미다.

산업 시스템에는 다음과 같은 현실적 문제가 있다.

시간에 따라 변하는 상태  
센서 오류  
중복 시스템  
외부 identifier 충돌  
legacy migration 문제  
여러 data source

따라서 강한 property characteristic은 잘못된 inference를 유발할 수 있다.

핵심 원칙은 다음과 같다.

Property characteristic은 reasoning power를 높이지만 위험도 높인다.  
Foundation에서는 최소한으로 사용한다.

---

## **18\. FunctionalProperty / InverseFunctionalProperty 예시**

### **18.1 FunctionalProperty 주의 예시**

`FunctionalProperty`는 하나의 subject가 해당 property에 대해 하나의 object만 가질 수 있음을 의미한다.

다음 선언은 조심해야 한다.

hasLocation rdf:type owl:FunctionalProperty.

산업 시스템에서 하나의 object는 여러 location 표현을 동시에 가질 수 있다.

GPS location  
Indoor positioning location  
BIM coordinate  
Control room logical zone  
Last known location  
Estimated location

이 경우 `hasLocation`을 FunctionalProperty로 선언하면, 서로 다른 location 표현을 동시에 다루기 어려워지고 consistency 문제 또는 의도하지 않은 추론 가능성이 생긴다.

더 안전한 설계는 다음과 같다.

hasLocation  
hasCurrentLocation  
hasEstimatedLocation  
hasLastKnownLocation  
hasDesignLocation

현재 위치가 하나만 있어야 한다는 검증은 사용 맥락에 따라 world state logic, SHACL, Policy, Safety Gate에서 처리한다.

### **18.2 InverseFunctionalProperty 주의 예시**

`InverseFunctionalProperty`는 하나의 object가 해당 property를 통해 하나의 subject만 식별할 수 있음을 의미한다.

다음 선언은 조심해야 한다.

hasSerialNumber rdf:type owl:InverseFunctionalProperty.

Serial number는 unique해 보일 수 있지만 실제 산업 시스템에서는 다음 문제가 생길 수 있다.

source system 입력 오류  
vendor serial number 중복  
temporary equipment ID  
test device clone  
legacy migration error  
vendor 간 serial number 재사용

잘못된 InverseFunctionalProperty는 서로 다른 physical object가 같은 individual로 잘못 병합될 가능성을 만든다.

더 안전한 설계는 다음과 같다.

hasExternalIdentifier  
hasIdentifierScheme  
issuedBySourceSystem  
validDuring  
supportedBy IdentityResolutionEvidence

핵심 원칙은 다음과 같다.

Identifier가 unique해 보인다고 바로 InverseFunctionalProperty를 사용하지 않는다.  
Identity는 evidence와 governance로 해결한다.

---

## **19\. Restriction 사용 원칙**

OWL restriction은 class가 가져야 하는 의미 조건을 정의한다.

주요 restriction은 다음과 같다.

someValuesFrom  
allValuesFrom  
hasValue  
minCardinality  
maxCardinality  
exactCardinality

예시는 다음과 같다.

HighRiskTask  
→ requiresPermit some Permit

SensorObservation  
→ generatedBy some Sensor

ActionCandidate  
→ hasTarget some Entity

EvidenceBackedDecision  
→ supportedBy some EvidenceBundle

Restriction은 강력하지만 runtime data validation과 혼동하면 안 된다.

OWL restriction  
→ 의미 조건과 reasoning

SHACL shape  
→ 실제 데이터 검증

핵심 원칙은 다음과 같다.

Restriction은 의미를 정의한다.  
필수 데이터 존재 여부는 SHACL이 검증한다.

---

## **20\. Restriction과 SHACL의 경계**

예를 들어 다음 OWL restriction이 있다고 하자.

SensorObservation  
→ generatedBy some Sensor

의미는 다음과 같다.

SensorObservation은 의미상 어떤 Sensor에 의해 생성된 observation이다.

하지만 실제 ABox 데이터에 `generatedBy`가 없다고 해서 OWL만으로 즉시 “데이터가 잘못되었다”고 판단하기는 어렵다. OWL은 Open World Assumption을 따르기 때문이다.

실제 검증은 SHACL이 담당한다.

SensorObservationShape  
→ generatedBy minCount 1  
→ generatedBy class Sensor

정리하면 다음과 같다.

| 목적 | 사용 기술 |
| ----- | ----- |
| SensorObservation이 의미상 Sensor에 의해 생성되어야 함을 정의 | OWL restriction |
| 실제 데이터에 generatedBy가 존재하는지 검증 | SHACL minCount |
| generatedBy 대상이 Sensor인지 검증 | SHACL class |
| execution 직전 evidence freshness 검증 | Safety Gate Snapshot |
| observation이 action 근거로 사용 가능한지 판단 | Evidence \+ Policy \+ Safety Gate |

핵심 원칙은 다음과 같다.

OWL restriction은 의미를 설명한다.  
SHACL shape는 missing data와 structural error를 잡는다.  
Safety Gate는 실행 시점의 사용 가능성을 검증한다.

---

## **21\. Cardinality 사용 원칙**

Cardinality는 관계 개수를 제한한다.

예시는 다음과 같다.

exactly 1 generatedBy Sensor  
min 1 supportedBy EvidenceBundle  
max 1 currentPrimaryState

Cardinality는 매우 신중하게 사용한다.

산업 시스템에서는 다음 상황이 흔하다.

하나의 object에 여러 sensor가 연결될 수 있다.  
하나의 event에 여러 evidence가 연결될 수 있다.  
하나의 ActionCandidate에 여러 risk reason이 연결될 수 있다.  
하나의 external object가 여러 identifier를 가질 수 있다.  
하나의 object에 여러 location source가 존재할 수 있다.

Foundation level cardinality는 최소화한다.

권장 원칙은 다음과 같다.

필수 최소 데이터는 SHACL로 검증한다.  
정말 논리적으로 불가피한 경우에만 OWL cardinality를 사용한다.  
Runtime state cardinality는 Policy 또는 Safety Gate에서 검증한다.

---

## **22\. sameAs 사용 원칙**

`owl:sameAs`는 두 individual이 완전히 같은 entity임을 선언한다.

이는 매우 강한 equality 선언이다.

A owl:sameAs B  
→ A에 대한 모든 사실은 B에도 적용된다.  
→ B에 대한 모든 사실은 A에도 적용된다.

LEDO는 기본적으로 `owl:sameAs`를 제한한다.

외부 ID가 같아 보인다고 곧바로 `sameAs`를 사용하지 않는다.

권장 identity 흐름은 다음과 같다.

External Identifier  
→ Identifier Mapping Record  
→ Identity Resolution Evidence  
→ Canonical Identity  
→ ABox Hash IRI

대안 관계는 다음과 같다.

ot:possiblySameAs  
ot:externallyMappedTo  
ot:hasExternalIdentifier  
ot:resolvedAsCanonicalIdentity  
ot:sourceSystemIdentifier

핵심 원칙은 다음과 같다.

sameAs는 매우 강한 equality 선언이다.  
확실하지 않으면 sameAs를 사용하지 않는다.

---

## **23\. sameAs 예시**

### **23.1 나쁜 예시**

IFC\_Object\_123 owl:sameAs LEDO\_Object\_456.

이 선언이 위험한 이유는 다음과 같다.

외부 object는 design object이고 runtime object가 아닐 수 있다.  
동일 외부 ID가 다른 context에서 재사용될 수 있다.  
IFC object는 변경되었지만 LEDO canonical object는 안정적으로 유지되어야 할 수 있다.  
source-specific fact가 잘못 전파될 수 있다.  
Audit에서 어떤 source가 어떤 사실을 만들었는지 추적하기 어려워질 수 있다.

더 나은 설계는 다음과 같다.

LEDO\_Object\_456 hasExternalIdentifier IFC\_GlobalId\_123.  
LEDO\_Object\_456 externallyMappedTo IFC\_Object\_123.  
IdentityResolutionRecord\_01 resolvedAsCanonicalIdentity LEDO\_Object\_456.  
IdentityResolutionRecord\_01 supportedBy EvidenceBundle\_77.

### **23.2 sameAs를 고려할 수 있는 제한적 경우**

`sameAs`는 다음 조건을 모두 만족할 때만 고려한다.

두 individual이 완전히 같은 real-world entity를 가리킨다.  
양쪽의 모든 사실을 공유해도 논리 문제가 없다.  
source system의 identity 정책이 신뢰 가능하다.  
identity resolution evidence가 존재한다.  
governance review를 통과했다.

그 외에는 mapping relation을 사용한다.

핵심 원칙은 다음과 같다.

Identity는 sameAs 하나로 해결하지 않는다.  
Identity는 canonical identity, mapping record, evidence, governance로 해결한다.

---

## **24\. Open World Assumption**

OWL은 Open World Assumption을 따른다.

즉:

정보가 없다는 것은 거짓을 의미하지 않는다.

예를 들어:

Observation\_1 generatedBy Sensor\_1 정보가 없다.

이것은 다음을 의미하지 않는다.

Observation\_1은 Sensor에 의해 생성되지 않았다.

단지 다음을 의미한다.

Unknown.

이 점은 runtime validation에서 매우 중요하다.

OWL  
→ 정보가 없으면 unknown

SHACL / Safety Gate  
→ 필수 정보가 없으면 invalid, deny, hold, escalate 가능

핵심 원칙은 다음과 같다.

OWL은 open-world다.  
Safety Gate는 closed-world에 가까운 검증이 필요하다.  
따라서 runtime validation을 OWL만으로 수행하지 않는다.

---

## **25\. OWL Reasoning 사용 기준**

OWL reasoner는 다음에 사용한다.

Ontology consistency checking  
Unsatisfiable class detection  
Class hierarchy inference  
Property inference  
Controlled semantic enrichment  
Release validation  
Axiom change impact assessment  
Regression testing

OWL reasoner는 다음에 직접 사용하지 않는다.

Safety Gate hot path  
Real-time execution validation  
External control request generation  
Raw telemetry processing  
High-frequency world state update  
Low-level physical control

Reasoning 결과는 사전 계산하고 materialized view 또는 Safety Gate Runtime Snapshot으로 변환한다.

OWL Reasoning  
→ inferred\_class\_map  
→ class membership bitset  
→ selected relation closure  
→ materialized semantic view  
→ Safety Gate Runtime Snapshot

---

## **26\. Reasoning Result Materialization**

LEDO는 runtime hot path에서 OWL reasoning을 직접 실행하지 않는다.

Reasoning 결과는 사전 계산되어 materialized view 또는 Safety Gate Runtime Snapshot으로 변환된다.

### **26.1 사전 계산 가능한 Reasoning 결과**

다음 결과는 미리 계산할 수 있다.

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

예시:

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

Runtime 최적화 형태:

class\_membership\_bitset\[object\_id\] \= 0b010010001...

### **26.2 Safety Gate가 조회할 수 있는 Reasoning 결과**

Safety Gate는 다음 질문에 빠르게 답해야 할 수 있다.

이 target은 Zone인가?  
이 action type은 이 target class에 허용되는가?  
이 action은 이 risk type을 완화할 수 있는가?  
이 task는 permit을 요구하는가?  
이 evidence는 fresh한가?  
이 agent는 필요한 role을 가지는가?  
이 external system은 available한가?  
이 zone은 restricted 상태인가?

이를 위한 snapshot table은 다음과 같다.

target\_class\_bitset  
action\_target\_permission\_matrix  
risk\_action\_matrix  
task\_permit\_requirement\_map  
evidence\_freshness\_map  
agent\_role\_permission\_map  
external\_system\_health\_map  
zone\_restriction\_map

### **26.3 Reasoning 결과 생성 흐름**

OWL TBox  
→ controlled reasoner execution  
→ inferred hierarchy  
→ inferred class membership  
→ relation expansion  
→ semantic materialized view  
→ Safety Gate Runtime Snapshot  
→ lock-free read-only lookup

세부 흐름은 다음과 같다.

1\. Ontology version 확정  
2\. TBox consistency check  
3\. Sample ABox validation  
4\. OWL reasoner 실행  
5\. inferred class map 생성  
6\. selected relation closure 생성  
7\. SHACL validation result flag 결합  
8\. Policy pre-check result 결합  
9\. Snapshot schema로 변환  
10\. checksum / version / timestamp 검증  
11\. active snapshot으로 publish

핵심 원칙은 다음과 같다.

Reasoning은 background에서 수행한다.  
Safety Gate는 reasoning result를 조회한다.

---

## **27\. OWL과 SHACL의 경계**

OWL과 SHACL은 서로 다른 목적을 가진다.

| 구분 | OWL | SHACL |
| ----- | ----- | ----- |
| 목적 | 의미 정의와 추론 | 데이터 검증 |
| 세계관 | Open World | Closed-world validation에 가까움 |
| 사용 시점 | Modeling, reasoning, QA | Data input, state change, candidate validation |
| 실패 의미 | inconsistency 또는 unsatisfiability | validation violation |
| Runtime 사용 | precomputed / controlled | validation pipeline |

핵심 원칙은 다음과 같다.

OWL은 무엇인지를 정의한다.  
SHACL은 데이터가 필요한 형태를 갖췄는지 검증한다.

---

## **28\. OWL과 Policy의 경계**

OWL은 의미를 정의한다.  
Policy는 운영상 허용/금지를 판단한다.

OWL은 다음을 말할 수 있다.

HighRiskTask requiresPermit some Permit.

하지만 다음 판단은 Policy가 수행한다.

이 사용자가 지금 이 task를 승인할 권한이 있는가?  
이 action은 현재 운영 정책상 허용되는가?  
이 상태에서 자동 실행이 가능한가?  
이 action은 human approval을 요구하는가?

핵심 원칙은 다음과 같다.

OWL은 policy decision을 대체하지 않는다.  
Policy는 ontology meaning을 사용할 수 있지만, 운영 허용 판단은 Policy Engine이 수행한다.

---

## **29\. OWL과 Safety Gate의 경계**

Safety Gate는 실행 직전 최종 검문소다.

Safety Gate는 OWL reasoning을 직접 수행하지 않는다.

Safety Gate는 다음을 수행한다.

Precomputed inference lookup  
Candidate validity flag check  
Evidence freshness check  
Approval validity check  
Policy result check  
External system health check  
Conflict matrix check  
allow / deny / hold / escalate decision

핵심 원칙은 다음과 같다.

OWL reasoning은 Safety Gate를 위한 재료를 만든다.  
Safety Gate는 그 재료를 즉시 조회한다.

---

## **30\. Competency Question 기반 모델링**

OWL 모델링은 competency question으로 검증해야 한다.

새 class, property, axiom은 최소 하나 이상의 의미 있는 질문에 답하는 데 기여해야 한다.

예시는 다음과 같다.

CQ-01.  
어떤 ActionCandidate가 어떤 EvidenceBundle에 의해 지원되는가?

CQ-02.  
어떤 RiskEvent가 어떤 Zone에 영향을 주는가?

CQ-03.  
특정 Zone에 현재 적용 중인 Restriction은 무엇인가?

CQ-04.  
특정 RobotAgent는 어떤 Task를 수행할 capability를 가지는가?

CQ-05.  
어떤 Task가 Permit을 요구하며, 해당 Permit은 아직 유효한가?

CQ-06.  
특정 Observation은 어떤 Sensor 또는 Agent에 의해 생성되었는가?

CQ-07.  
특정 EvidenceBundle은 어떤 source system과 timestamp를 가지는가?

CQ-08.  
특정 ActionCandidate의 target은 action type의 허용 range 안에 있는가?

CQ-09.  
특정 ExternalControlRequest는 어떤 ExecutionRequest에서 파생되었는가?

CQ-10.  
특정 Safety Gate decision은 어떤 snapshot version과 policy version을 사용했는가?

CQ-11.  
특정 Zone은 어떤 GeofencingBoundary 또는 SpatialRegion 안에 포함되는가?

CQ-12.  
특정 action이 deny된 경우, deny reason은 evidence 부족, policy 위반, state conflict, external system unavailable 중 무엇인가?

각 competency question은 다음과 연결되어야 한다.

필요 class  
필요 object property  
필요 data property  
필요 SHACL shape  
필요 SPARQL query  
필요 materialized view  
필요 audit field

예시:

CQ:  
특정 ActionCandidate의 target은 action type의 허용 range 안에 있는가?

필요 class:  
ActionCandidate, Action, Entity, Zone, Agent, System

필요 property:  
hasTarget, hasActionType

필요 validation:  
action\_target\_permission\_matrix

필요 runtime structure:  
SafetyGateSnapshot.action\_permission\_map

필요 audit:  
decision\_reason\_code, snapshot\_version

핵심 원칙은 다음과 같다.

의미 있는 질문에 답하지 못하는 ontology element는 제거하거나 보류한다.

---

## **31\. OWL 변경 관리 원칙**

OWL class, property, axiom 변경은 governance 대상이다.

다음 변경은 반드시 review가 필요하다.

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

변경 시 다음 검사를 수행한다.

Reasoner consistency check  
Unsatisfiable class check  
Sample ABox inference comparison  
SHACL regression test  
Competency question regression test  
Module dependency check  
Runtime safety impact review

핵심 원칙은 다음과 같다.

OWL 변경은 의미와 inference를 바꿀 수 있다.  
따라서 OWL 변경은 governance, review, regression test를 거쳐야 한다.

---

## **32\. OWL Modeling Anti-Patterns**

| Anti-pattern | 왜 위험한가 | 실제 피해 | 대안 |
| ----- | ----- | ----- | ----- |
| 모든 용어를 class로 만드는 것 | Ontology가 의미 모델이 아니라 단어 목록이 됨 | Class explosion으로 reasoning과 유지보수 어려움 | SKOS vocabulary와 OWL class 분리 |
| 단순 데이터 필드를 class로 만드는 것 | Class hierarchy가 data schema처럼 오염됨 | TemperatureValue, BatteryLevelValue 같은 불필요 class 증가 | Data property, SHACL, time-series store 사용 |
| Domain/range를 너무 좁게 설정 | 원하지 않는 class inference 발생 | Robot이 Zone으로 추론될 수 있음 | Foundation에서는 넓게, Domain Module에서 구체화 |
| Disjointness 남용 | 시간과 상태 변화를 표현하지 못함 | SafeZone/DangerZone 전환 시 inconsistency 발생 | State, context, event, time interval 사용 |
| EquivalentClass 남용 | 유사 개념을 동일 의미로 강제 병합 | 외부 표준 변경 시 내부 class 의미 붕괴 | Mapping relation 또는 SKOS relation 사용 |
| sameAs 남용 | Identity 오염과 fact propagation 오류 발생 | 서로 다른 source object가 병합되어 audit 실패 | Canonical identity \+ mapping record 사용 |
| TransitiveProperty 남용 | Inference explosion 발생 | Relation closure가 커져 reasoner 성능 저하 | 실제로 전이되는 관계에만 제한 사용 |
| FunctionalProperty 남용 | 현실의 다중 값 상태를 표현하기 어려워짐 | 여러 location source 처리 충돌 | Current / estimated / last-known / design location 분리 |
| InverseFunctionalProperty 남용 | 잘못된 identifier가 object 병합 가능성을 만듦 | Serial number 오류로 서로 다른 object가 하나처럼 취급될 수 있음 | Identifier scheme \+ source \+ evidence 사용 |
| OWL restriction으로 SHACL 검증을 대체 | Missing data를 잡지 못함 | generatedBy 없는 observation이 통과 | SHACL minCount / class validation 사용 |
| Safety Gate에서 reasoner 실행 | Runtime jitter와 timeout 발생 | 실행 직전 검증 병목 | Safety Snapshot 사용 |
| AI output을 OWL fact로 직접 입력 | Hallucination이 ontology에 주입 | 존재하지 않는 risk/event가 사실화됨 | Evidence-backed validation 후 반영 |
| 외부 표준 class를 Foundation에 직접 복사 | Foundation이 외부 schema에 종속됨 | IFC/OPC-UA 변경 시 core ontology 흔들림 | Mapping Module 사용 |
| Logical boundary를 string으로만 저장 | Spatial reasoning 불가능 | Geofencing/access/speed 제한 검증 실패 | GeoSPARQL \+ SpatialRegion 모델링 |
| Runtime state를 영구 class로 표현 | 시간 변화와 state transition을 잃음 | 현재 상태와 과거 상태가 충돌 | State/Event/TimeInterval 모델 사용 |

---

## **33\. 이 문서에서 가장 중요한 5가지 원칙**

### **33.1 Class는 tag가 아니다**

Class는 단순 label이 아니다.  
Class는 upper category, relation, axiom, reasoning implication을 가지는 의미 범주다.

단순 상태값, 데이터 필드, 임시 label, UI label은 class로 만들지 않는다.

### **33.2 OWL은 의미를 정의하고 SHACL은 데이터를 검증한다**

OWL restriction  
→ semantic condition

SHACL shape  
→ actual data validation

OWL은 Open World Assumption을 따른다.  
Missing data를 잡으려면 SHACL이 필요하다.

### **33.3 강한 공리는 최소화한다**

다음 공리는 매우 신중하게 사용한다.

equivalentClass  
disjointWith  
sameAs  
FunctionalProperty  
InverseFunctionalProperty  
TransitiveProperty  
cardinality restriction

강한 공리는 reasoning power를 높이지만 잘못 사용하면 ontology 전체를 오염시킬 수 있다.

### **33.4 Runtime Safety Gate는 OWL Reasoner가 아니다**

OWL reasoning  
→ background / controlled reasoning layer

Safety Gate  
→ precomputed snapshot lookup

Safety Gate hot path에서는 OWL reasoning, full SHACL validation, SPARQL, external API call, LLM call을 수행하지 않는다.

### **33.5 Identity는 sameAs가 아니라 canonical identity와 evidence로 해결한다**

External Identifier  
→ Mapping Record  
→ Identity Resolution Evidence  
→ Canonical Identity  
→ ABox Hash IRI

외부 ID가 같아 보인다고 바로 `owl:sameAs`를 사용하지 않는다.  
Identity는 evidence와 governance가 필요한 핵심 영역이다.

---

## **34\. 최종 핵심 원칙**

Class는 의미 범주다.  
Property는 의미 관계다.  
Axiom은 의미를 고정하는 규칙이다.  
Restriction은 의미 조건이다.  
SHACL은 데이터 검증이다.  
Policy는 운영 판단이다.  
Safety Gate는 실행 직전 결정론적 검증이다.  
Reasoner는 runtime hot path가 아니라 controlled reasoning layer에 있어야 한다.  
AI output은 ontology fact가 아니라 candidate interpretation이다.  
External standard는 복사하지 않고 mapping한다.  
Identity는 canonical identity와 evidence로 관리한다.

---

## **35\. 최종 결론**

LEDO OWL 모델링은 class를 많이 만드는 작업이 아니다.

LEDO OWL 모델링은 산업 세계의 의미를 다음과 같은 구조로 고정하는 작업이다.

추론 가능해야 한다.  
검증 가능해야 한다.  
감사 가능해야 한다.  
거버넌스 가능해야 한다.  
표준 정렬 가능해야 한다.  
Runtime-safe해야 한다.  
Physical AI 실행 경계와 연결 가능해야 한다.

최종 원칙은 다음과 같다.

OWL은 의미를 만든다.  
SHACL은 데이터를 검증한다.  
Policy는 허용 여부를 판단한다.  
Safety Gate는 실행 가능성을 검증한다.  
Audit은 전체 경로를 기록한다.

그리고 최종 아키텍처 경계는 다음과 같다.

OWL은 LEDO의 semantic engine이다.  
하지만 OWL은 Safety Gate가 아니다.

OWL은 의미를 만들고,  
Safety Gate는 실행 가능성을 검증한다.

