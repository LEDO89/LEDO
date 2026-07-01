# **Ontology foundation “Semantic Web Technology Stack”**

## **1\. Purpose**

This document defines how Semantic Web technologies are used within the LEDO Industrial Ontology Foundation.

The purpose is not to use technologies such as RDF, OWL, SHACL, and SPARQL simply for their own sake. The purpose is to clearly separate the responsibility of each technology so that ontology modeling, reasoning, validation, querying, vocabulary management, evidence traceability, time modeling, spatial modeling, and storage architecture do not become mixed.

In LEDO, Semantic Web technologies have the following roles.

RDF  
→ Graph data model

RDFS  
→ Basic class and property hierarchy

OWL  
→ Formal ontology and semantic reasoning

SPARQL  
→ Graph query and semantic search

SHACL  
→ Data validation and shape constraints

SKOS  
→ Terms, labels, vocabulary system, and SLM training support

PROV-O  
→ Provenance, evidence lineage, and data lineage

OWL-Time  
→ Time concepts and temporal relations

GeoSPARQL  
→ Spatial objects, zones, geometry, and spatial queries

Triple Store  
→ RDF graph storage and SPARQL execution

Reasoner  
→ Controlled semantic inference

Graph Database  
→ Operational relationship exploration and runtime graph traversal

The core principle is as follows.

Each technology must have one primary responsibility.  
No single technology should replace every other responsibility.

---

## **2\. Position Within the Overall LEDO Structure**

This document belongs to the following location.

04\_ontology\_foundation/  
  01\_semantic\_web\_technology\_stack/

This document supports the following areas of the overall LEDO architecture.

Core Ontology Kernel  
Knowledge & Semantic Memory  
Real-Time World State  
Agent Interpretation  
Candidate Semantic Validation  
Relation Graph Validation  
Evidence and Audit Graph

Semantic Web technologies do not directly control physical systems.  
Semantic Web technologies do not replace the Safety Gate.  
Semantic Web technologies do not replace the external execution layer.

The role of Semantic Web technologies is to provide meaning, structure, validation, query capability, and traceability.

---

## **3\. Core Separation Principle**

LEDO separates the following responsibilities.

Meaning definition  
→ OWL / RDFS

Graph representation  
→ RDF

Data validation  
→ SHACL

Graph query  
→ SPARQL

Vocabulary management  
→ SKOS

Evidence lineage  
→ PROV-O

Time modeling  
→ OWL-Time

Spatial modeling  
→ GeoSPARQL

Execution safety validation  
→ Safety Gate

Operational permission and prohibition decision  
→ Policy Engine

Physical execution  
→ External Control Systems

This separation is essential to prevent architectural confusion.

OWL defines what something means.  
SHACL validates whether data has the correct structure.  
SPARQL retrieves meaningful facts from the graph.  
SKOS organizes terms and labels.  
PROV-O explains where evidence came from.  
Safety Gate performs the final validation of whether an action can be executed at the current moment.

---

## **4\. Runtime Flow and Technology Intervention Points**

Semantic Web technologies intervene in the LEDO runtime flow at the following points.

Raw Data  
→ Normalize  
→ SHACL Validation  
→ Canonical Object  
→ Ontology Binding  
→ RDF Graph Update  
→ Evidence Binding with PROV-O  
→ World State Update  
→ Event Detection  
→ SPARQL / Graph Query Support  
→ Agent Interpretation  
→ ActionCandidate  
→ Candidate Semantic Validation  
→ Relation Graph Validation  
→ Policy Pre-check  
→ Decision Router  
→ Approval  
→ Safety Gate  
→ ExecutionRequest  
→ ExternalControlRequest  
→ Feedback  
→ Reconciliation  
→ Audit

The main technology intervention points for each stage are as follows.

| Runtime Stage | Main Technology | Role |
| ----- | ----- | ----- |
| Raw Data | None / external systems | Raw input without assigned meaning |
| Normalize | DTO / schema / parser | Normalize field names, units, time, and ID formats |
| SHACL Validation | SHACL | Validate the structure of normalized data |
| Canonical Object | Identity Resolver | Map external IDs to canonical identity |
| Ontology Binding | RDF / RDFS / OWL | Bind objects to classes, properties, and relations |
| RDF Graph Update | RDF / Triple Store | Reflect facts or references in the semantic graph |
| Evidence Binding | PROV-O / RDF | Connect decision basis and source lineage |
| World State Update | Runtime State Store / RDF reference | Update current state |
| Event Detection | Rules / SPARQL / Graph Query | Detect meaningful events from state changes |
| Agent Interpretation | Agent / Ontology Context | Interpret events and generate action candidates |
| ActionCandidate | DTO / RDF reference | Generate candidate actions that are not execution commands yet |
| Candidate Semantic Validation | OWL / SHACL / SPARQL | Validate whether the candidate is semantically valid |
| Relation Graph Validation | SPARQL / Graph DB / cached view | Check whether the action is possible in the relation graph |
| Policy Pre-check | Policy Engine / OPA-style rules | Perform preliminary permission/prohibition evaluation |
| Decision Router | Rules / Risk Matrix | Route to automation, approval, or escalation |
| Approval | Human / System Approval | Process authorized approval |
| Safety Gate | Deterministic Rules / cached state | Validate freshness, conflicts, and safety conditions before execution |
| ExecutionRequest | DTO / Adapter Schema | Generate a request that can be consumed by an external system |
| ExternalControlRequest | API / MQTT / OPC-UA / ROS2, etc. | Send a high-level request to an external control system |
| Feedback | Event / Evidence | Receive execution result |
| Reconciliation | State comparison / Audit | Compare request and actual result |
| Audit | PROV-O / Audit Log / RDF reference | Record the full trace |

The important design rules are as follows.

Semantic validation is performed before the Decision Router.  
Execution readiness validation is performed inside the Safety Gate.  
The Safety Gate is not a heavy reasoner, but a deterministic final checkpoint.

---

## **5\. RDF**

### **5.1 Role**

RDF is the basic graph data model for LEDO ontology data.

RDF represents knowledge in a triple structure.

subject → predicate → object

Examples are as follows.

ot:GasSensor\_17 ot:observes ot:GasConcentration\_Zone\_A.  
ot:GasSensor\_17 ot:locatedIn ot:Zone\_A.  
ot:GasObservation\_901 ot:generatedBy ot:GasSensor\_17.

RDF is used to represent the following.

Objects  
Classes  
Properties  
Relations  
Observations  
Events  
Evidence references  
Audit references  
External mapping references

### **5.2 LEDO Usage Criteria**

In LEDO, RDF is used to represent the semantic graph.

All raw sensor values must not be stored in RDF. High-frequency raw data may reside in stream storage, time-series storage, object storage, or relational storage. RDF stores meaning, relations, references, and selected evidence-backed facts.

### **5.3 Principle**

RDF stores meaning and relationships.  
RDF must not become a raw telemetry database.

---

## **6\. RDFS**

### **6.1 Role**

RDFS provides lightweight schema semantics.

RDFS is used to define the following.

rdfs:Class  
rdfs:subClassOf  
rdfs:subPropertyOf  
rdfs:domain  
rdfs:range  
rdfs:label  
rdfs:comment

### **6.2 LEDO Usage Criteria**

RDFS is used for the following.

Basic class hierarchy  
Basic property hierarchy  
Human-readable labels  
Simple domain/range declarations  
Documentation comments

Examples are as follows.

ot:GasSensor rdfs:subClassOf ot:Sensor.  
ot:RobotAgent rdfs:subClassOf ot:Agent.  
ot:observes rdfs:domain ot:Sensor.  
ot:observes rdfs:range ot:ObservableCondition.

### **6.3 Principle**

RDFS provides the basic skeleton.  
OWL provides stronger formal meaning.

---

## **7\. OWL**

### **7.1 Role**

OWL is used for formal ontology modeling and semantic reasoning.

OWL defines the following.

Class axioms  
Property axioms  
Equivalence  
Disjointness  
Inverse properties  
Restrictions  
Cardinality  
Property characteristics  
Class inference  
Relation inference

### **7.2 LEDO Usage Criteria**

OWL is used in LEDO to define formal meaning.

Examples are as follows.

ot:HumanoidRobot rdfs:subClassOf ot:RobotAgent.  
ot:GasSensor rdfs:subClassOf ot:Sensor.  
ot:DangerZone owl:disjointWith ot:SafeZone.  
ot:requiresPermit rdfs:domain ot:HighRiskTask.  
ot:requiresPermit rdfs:range ot:Permit.

OWL helps answer questions such as the following.

Is this object a kind of Agent?  
Is this task a kind of HighRiskTask?  
Does this zone classification conflict with another zone classification?  
Can this class membership be inferred from existing axioms?

### **7.3 Runtime Boundary**

OWL reasoning must be controlled.

Heavy OWL reasoning must not be placed directly on the real-time Safety Gate path.

In LEDO, OWL is mainly used for the following.

Ontology consistency checking  
Offline or controlled reasoning  
Class classification  
Semantic enrichment  
Candidate validation support  
Precomputed inference view generation

### **7.4 Principle**

OWL expands meaning.  
OWL does not replace runtime safety validation.

---

## **8\. SPARQL**

### **8.1 Role**

SPARQL is the query language for RDF graphs.

SPARQL is used to retrieve semantic facts, relations, evidence, and audit connections.

### **8.2 LEDO Usage Criteria**

SPARQL is used for the following.

Semantic search  
Competency question execution  
Evidence retrieval  
Relation exploration  
Audit investigation  
Ontology QA  
Candidate validation support

Example competency questions are as follows.

Which agents are currently located in a danger zone?  
Which observations support a high-risk decision?  
Which sensors generated evidence for a gas risk event?  
Which actions were proposed based on a specific risk?  
Which external systems received an execution request?

### **8.3 Runtime Boundary**

SPARQL can be used in runtime flows, but high-latency graph queries must not block the Safety Gate execution path.

Frequently used query results should be managed through cache or materialized views.

### **8.4 Principle**

SPARQL retrieves semantic facts.  
SPARQL must not become the entire runtime decision mechanism.

---

## **9\. SHACL**

### **9.1 Role**

SHACL is used for RDF data validation.

SHACL checks whether data conforms to the expected shape.

SHACL validates the following.

Required properties  
Data types  
Value ranges  
Cardinality  
Class membership  
Node shapes  
Property shapes  
Cross-reference conditions  
Evidence reference conditions

### **9.2 LEDO Usage Criteria**

SHACL is used at points where data enters or semantic state changes.

Major validation points are as follows.

After normalization  
Before ontology binding  
Before evidence binding  
Before World State update  
Before ActionCandidate promotion  
Before ExecutionRequest creation

Example validation questions are as follows.

Does this Observation have a source?  
Does this Observation have a timestamp?  
Does this EvidenceBundle reference original data?  
Does this ActionCandidate have an action type?  
Does this ActionCandidate have a target?  
Does this target belong to an allowed class?

### **9.3 Principle**

SHACL validates data.  
OWL defines meaning.  
They must not be confused.

---

## **10\. SKOS**

### **10.1 Role**

SKOS is used for vocabulary and terminology management.

SKOS provides the following.

skos:Concept  
skos:ConceptScheme  
skos:prefLabel  
skos:altLabel  
skos:hiddenLabel  
skos:definition  
skos:broader  
skos:narrower  
skos:related  
skos:scopeNote  
skos:example

### **10.2 LEDO Usage Criteria**

SKOS supports the following.

Human-readable terminology system  
Multilingual labels  
Domain terminology normalization  
Semantic search  
SLM training text structuring  
Mapping between field language and ontology terms  
Documentation

Examples are as follows.

ot:GasRiskConcept skos:prefLabel "Gas risk"@en.  
ot:GasRiskConcept skos:altLabel "Gas hazard"@en.  
ot:GasRiskConcept skos:definition "A risk condition involving hazardous gas concentration."@en.

### **10.3 Relationship Between SKOS and OWL**

SKOS does not replace OWL.

SKOS organizes language around concepts.  
OWL defines formal meaning.

For example, if there is an OWL class called `GasRisk`, SKOS organizes the human language around that class.

OWL  
→ ot:GasRisk is a subclass of Risk.

SKOS  
→ Organizes terms such as gas risk, gas hazard, and hazardous gas condition.

SKOS is useful for SLM training, search, documentation, and field terminology mapping.  
However, class hierarchy, disjointness, restrictions, and reasoning must be handled by OWL.

### **10.4 Principle**

OWL defines formal meaning.  
SKOS organizes the terminology around that meaning.  
SKOS must not be used as a formal ontology.

---

## **11\. PROV-O**

### **11.1 Role**

PROV-O is used for provenance and traceability.

PROV-O describes the following.

Entity  
Activity  
Agent  
Generation  
Derivation  
Attribution  
Usage  
Source lineage

### **11.2 LEDO Usage Criteria**

PROV-O is used to track the following.

Which sensor generated an observation  
Which system provided a data record  
Which agent generated an action candidate  
Which evidence supported a decision  
Which approval led to an execution request  
Which external feedback updated the World State

Examples are as follows.

ot:GasObservation\_901 prov:wasGeneratedBy ot:GasSensor\_17.  
ot:ActionCandidate\_55 prov:wasDerivedFrom ot:EvidenceBundle\_77.  
ot:ExecutionRequest\_21 prov:wasAttributedTo ot:SafetyGate\_01.

### **11.3 Evidence Bundle Generation Flow Example**

An Evidence Bundle is not a single data point. It is a bundle of evidence that can be used for judgment.

An example is as follows.

GasSensor\_17  
→ generated GasObservation\_901

GasObservation\_901  
→ derivedFrom RawTelemetryRecord\_5501

RawTelemetryRecord\_5501  
→ wasAttributedTo SourceSystem\_OPCUA\_01

GasObservation\_901  
→ includedIn EvidenceBundle\_77

EvidenceBundle\_77  
→ supports GasRiskEvent\_12

GasRiskEvent\_12  
→ derived ActionCandidate\_55

From the PROV-O perspective, this flow can be expressed as follows.

ot:GasObservation\_901 prov:wasGeneratedBy ot:GasSensor\_17.  
ot:GasObservation\_901 prov:wasDerivedFrom ot:RawTelemetryRecord\_5501.  
ot:RawTelemetryRecord\_5501 prov:wasAttributedTo ot:SourceSystem\_OPCUA\_01.  
ot:EvidenceBundle\_77 ot:includesEvidence ot:GasObservation\_901.  
ot:GasRiskEvent\_12 ot:supportedBy ot:EvidenceBundle\_77.  
ot:ActionCandidate\_55 prov:wasDerivedFrom ot:GasRiskEvent\_12.

This structure should make it possible to answer the following questions later.

Which evidence led to this action candidate?  
Which raw data produced that evidence?  
Which system produced the raw data?  
Is that system trustworthy?  
Is the evidence still temporally valid?

### **11.4 Principle**

Important decisions must not exist without provenance.  
Evidence must always be traceable.

---

## **12\. OWL-Time**

### **12.1 Role**

OWL-Time is used to represent time concepts and temporal relations.

OWL-Time supports the following.

instant  
interval  
duration  
before  
after  
during  
hasBeginning  
hasEnd

### **12.2 LEDO Usage Criteria**

OWL-Time supports the following.

Event timing  
Observation timing  
Evidence freshness  
State validity  
Approval validity  
Execution request timing  
Feedback timing  
Audit timeline

Important runtime questions are as follows.

Is this evidence still fresh?  
Did this event occur before the action candidate?  
Was approval granted after the candidate was created?  
Did feedback arrive within the expected time window?

### **12.3 Principle**

Time is not merely metadata.  
Time affects validity, safety, and auditability.

---

## **13\. GeoSPARQL**

### **13.1 Role**

GeoSPARQL is used for spatial representation and spatial queries.

GeoSPARQL supports the following.

Geometry  
Spatial object  
Spatial relation  
within  
intersects  
contains  
near  
distance

### **13.2 LEDO Usage Criteria**

GeoSPARQL supports the following.

Zone modeling  
Danger zone relations  
Agent location  
Equipment location  
Robot location  
Restricted area checks  
Spatial risk queries  
Digital twin spatial alignment

Example questions are as follows.

Which agents are inside Zone\_A?  
Which sensors observe areas that intersect a danger zone?  
Which robot agents are near a restricted region?  
Which work areas overlap with an active risk region?

### **13.3 Runtime Boundary**

Spatial computation can be expensive.

Frequently used spatial relations may be managed as cache or materialized views for runtime validation.

### **13.4 Principle**

GeoSPARQL provides spatial meaning.  
Real-time spatial safety validation may require cache or optimized runtime views.

---

## **14\. Triple Store and Graph Database**

### **14.1 Role of Triple Store**

A Triple Store stores RDF data and executes SPARQL queries.

A Triple Store is used for the following.

Ontology graph storage  
Semantic fact storage  
Class/property relation storage  
Selected evidence reference storage  
Semantic mapping storage  
Audit graph reference storage  
Competency question execution

A Triple Store is the primary store for semantic graph data.

### **14.2 Role of Graph Database**

A Graph Database such as Neo4j may be used for operational graph exploration, graph analytics, and runtime relationship exploration.

A Graph Database may support the following.

Runtime dependency graph  
Agent-task-resource graph  
Control relationship graph  
Impact analysis  
Shortest path analysis  
Operational relationship exploration

### **14.3 Decision Criteria**

A Triple Store should be used as primary when the data belongs to the following categories.

Data directly connected to OWL/RDFS meaning  
Data requiring SPARQL queries  
Semantic facts connected to ontology classes/properties  
Evidence, provenance, and audit references  
Data requiring standards-based RDF export

A Graph Database should be used when the following are required.

Fast graph traversal  
Frequent operational relationship exploration  
Path search or impact analysis  
Runtime dependency graph  
Fast handling of complex operational graph queries

The principle in LEDO is as follows.

Triple Store is the semantic authority.  
Graph Database is operational graph acceleration.

Even if a Graph Database is faster, it must not become the semantic authority.  
Operational graphs stored in a Graph Database must remain synchronized with the meaning defined by the Triple Store or Ontology Kernel.

---

## **15\. Reasoner**

### **15.1 Role**

A Reasoner infers additional facts from OWL axioms.

A Reasoner can perform the following.

Class classification  
Subclass inference  
Property inference  
Consistency checking  
Unsatisfiable class detection  
Equivalence inference  
Restriction-based inference

### **15.2 LEDO Usage Criteria**

A Reasoner is used for the following.

Ontology QA  
Model consistency checking  
Offline inference  
Controlled semantic enrichment  
Release validation  
Axiom change impact assessment

### **15.3 Runtime Boundary**

A Reasoner must not be placed directly inside the Safety Gate hot path.

Runtime should use the following.

Precomputed inference views  
Cached semantic classification  
SHACL validation  
Policy rules  
Graph queries  
Deterministic safety checks

### **15.4 Principle**

A Reasoner is powerful but must be controlled.  
Runtime safety must remain deterministic.

---

## **16\. Runtime Cache / Materialized View Strategy**

If every semantic query and spatial query is executed directly against the Triple Store or GeoSPARQL at runtime, bottlenecks may occur.

Therefore, LEDO may manage frequently used relations, classifications, risk states, and spatial containment relations through cache or materialized views.

The following may be precomputed or cached.

Which zone an agent is currently inside  
Whether a zone currently has an active risk  
Which target class is allowed for a specific action type  
Which action types can mitigate a specific risk  
Whether a specific task requires a permit  
The inferred class hierarchy of a specific object  
Whether specific evidence is still fresh  
Whether a specific external system is currently available  
Whether a specific zone is restricted  
Which zone a specific sensor observes

The Safety Gate should avoid directly executing heavy graph queries when possible. It should use the following instead.

Cached world state  
Precomputed inference view  
Materialized relation view  
Policy decision cache  
Freshness-checked evidence reference  
Deterministic rule evaluation

However, cache must always have a freshness and invalidation strategy.

Old cache is unsafe.  
Cache is fast, but it is not the source of truth.  
Cache results must be traceable to the original semantic graph.

---

## **17\. Major Technology Combination Examples**

### **17.1 When a Gas Risk Event Occurs**

When a gas risk event occurs, the following technology combination is used.

Raw gas telemetry  
→ Normalize  
→ SHACL Validation  
→ GasObservation RDF creation  
→ Source lineage connection with PROV-O  
→ Observation time/freshness recording with OWL-Time  
→ GasRisk-related class binding through Ontology Binding  
→ Related zone, sensor, and agent retrieval with SPARQL  
→ Affected target confirmation through Graph Validation  
→ EvidenceBundle generation  
→ Event Detection

The main technology combination is as follows.

SHACL  
→ Validates the structure of the observation

RDF / OWL  
→ Connects the meaning of GasObservation, GasRisk, Zone, and Sensor

PROV-O  
→ Connects data source and evidence lineage

OWL-Time  
→ Validates evidence freshness

SPARQL  
→ Retrieves related sensors, zones, and agents

Graph DB or cached view  
→ Quickly explores runtime impact scope

---

### **17.2 When Validating an ActionCandidate**

Assume an agent generated the following candidate.

ActionCandidate:  
  action\_type: restrict\_access  
  target: Zone\_A  
  reason: GasRiskEvent\_12

This candidate must not go directly to the Decision Router. Semantic validation and relation graph validation must be performed first.

Validation questions are as follows.

Is restrict\_access a registered action type?  
Is Zone\_A actually a Zone?  
Is GasRiskEvent\_12 supported by an EvidenceBundle?  
Is the EvidenceBundle fresh?  
Does GasRiskEvent\_12 affect Zone\_A?  
Can restrict\_access mitigate GasRisk?  
Is this action allowed when the target class is Zone?

The main technology combination is as follows.

OWL  
→ Confirms the meaning of action, risk, and zone classes

SHACL  
→ Validates the structure of the ActionCandidate

SPARQL  
→ Retrieves risk, target, and evidence relations

PROV-O  
→ Confirms which evidence produced the candidate action

OWL-Time  
→ Checks the temporal validity of evidence and world state

Policy Engine  
→ Checks preliminary permission/prohibition conditions

---

### **17.3 During an Audit Investigation**

Later, it may be necessary to investigate why a specific execution request was created.

The questions are as follows.

Why was ExecutionRequest\_21 created?  
Which ActionCandidate did it come from?  
Which Event did that candidate come from?  
Which EvidenceBundle supported that Event?  
Which Observation produced that EvidenceBundle?  
Which Sensor and SourceSystem produced that Observation?  
Who approved it?  
What did the Safety Gate validate?  
What was the external system feedback?

The main technology combination is as follows.

PROV-O  
→ Tracks the full lineage

RDF  
→ Represents related entity relationships

SPARQL  
→ Executes audit queries

OWL-Time  
→ Reconstructs the timeline

Audit Log  
→ Confirms approval, validation, execution, and feedback records

---

## **18\. Runtime Responsibility Matrix**

| Responsibility | Primary Technology | Runtime Use |
| ----- | ----- | ----- |
| Graph representation | RDF | Used |
| Basic class hierarchy | RDFS | Used |
| Formal ontology meaning | OWL | Controlled use |
| Semantic query | SPARQL | Used, with cache when needed |
| Data validation | SHACL | Used |
| Vocabulary and labels | SKOS | Used |
| Provenance / evidence lineage | PROV-O | Used |
| Time modeling | OWL-Time | Used |
| Spatial modeling | GeoSPARQL | Controlled / optimized use |
| Offline inference | OWL Reasoner | Offline or controlled |
| Runtime relation exploration | Graph Database | Used |
| Execution safety validation | Safety Gate | Used |
| Operational permission/prohibition decision | Policy Engine | Used |
| Physical execution | External Control System | Used |

---

## **19\. Anti-Patterns**

| Anti-pattern | Problem | Possible Damage | Alternative |
| ----- | ----- | ----- | ----- |
| Using OWL as runtime safety validation | OWL reasoning is not execution readiness validation | Delay in execution-time validation, missed dangerous conditions | Safety Gate should use deterministic rules and cached state |
| Storing all raw telemetry in RDF | Triple Store becomes overloaded | Graph write bottleneck, query delay | Store raw data in time-series/object storage and store references in RDF |
| Using SHACL as ontology semantics | SHACL validates shapes and does not define formal meaning | Semantic reasoning becomes impossible or confused | Separate meaning into OWL and validation into SHACL |
| Using SKOS as a formal ontology | SKOS manages vocabulary, while OWL defines formal meaning | Class hierarchy and vocabulary become confused | Use SKOS for labels, definitions, search, and SLM support |
| Placing a heavy reasoner inside the Safety Gate | Execution path becomes slow and unstable | Emergency actions may be delayed or time out | Use offline reasoning and precomputed inference views |
| Treating Graph DB as semantic authority | Operational graph may diverge from ontology meaning | Relation interpretation mismatch and audit errors | Keep Triple Store / Ontology Kernel as semantic authority |
| Ignoring provenance | Decisions become unauditable | Failure to trace causes after an incident and collapse of accountability | Use PROV-O and EvidenceBundle |
| Ignoring temporal validity | Old evidence may support dangerous decisions | Actions may be taken based on outdated state | Use OWL-Time, freshness checks, and state timestamps |
| Ignoring spatial modeling | Location-based risk reasoning becomes unstable | Actions may target unaffected entities or miss actual risk targets | Use GeoSPARQL or runtime spatial views |
| Hardcoding all graph checks inside agents | Validation becomes non-governed and inconsistent | Different agents make different judgments and results become non-reproducible | Separate into Candidate Semantic Validation layer |

---

## **20\. Core Principles**

RDF is the graph model.  
RDFS is the basic schema layer.  
OWL is the formal meaning layer.  
SPARQL is the query layer.  
SHACL is the validation layer.  
SKOS is the vocabulary layer.  
PROV-O is the provenance layer.  
OWL-Time is the temporal layer.  
GeoSPARQL is the spatial layer.  
Triple Store is the semantic graph store.  
Graph Database is operational graph acceleration.  
Reasoner is controlled semantic inference.  
Safety Gate is deterministic execution validation.

The final principle is as follows.

Semantic Web technologies define, validate, query, and trace meaning.  
Semantic Web technologies do not directly execute the physical world.

