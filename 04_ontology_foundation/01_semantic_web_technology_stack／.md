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

# **LEDO 시맨틱 웹 기술 스택**

## **1\. 목적**

이 문서는 LEDO 산업 온톨로지 Foundation 안에서 시맨틱 웹 기술들을 어떤 역할로 사용할 것인지 정의한다.

목적은 RDF, OWL, SHACL, SPARQL 같은 기술을 많이 쓰는 것이 아니다. 목적은 각 기술의 책임을 명확히 분리해서 온톨로지 모델링, 추론, 검증, 질의, 어휘 관리, 증거 추적, 시간 모델링, 공간 모델링, 저장 구조가 서로 뒤섞이지 않도록 하는 것이다.

LEDO에서 시맨틱 웹 기술은 다음 역할을 가진다.

RDF  
→ 그래프 데이터 모델

RDFS  
→ 기본 클래스/속성 계층

OWL  
→ 형식 온톨로지와 의미 추론

SPARQL  
→ 그래프 질의와 의미 검색

SHACL  
→ 데이터 검증과 shape 제약

SKOS  
→ 용어, 라벨, 어휘 체계, SLM 학습 지원

PROV-O  
→ 출처, 증거 계보, 데이터 lineage

OWL-Time  
→ 시간 개념과 시간 관계

GeoSPARQL  
→ 공간 객체, 구역, geometry, 공간 질의

Triple Store  
→ RDF 그래프 저장과 SPARQL 실행

Reasoner  
→ 통제된 의미 추론

Graph Database  
→ 운영 관계 탐색과 runtime graph traversal

핵심 원칙은 다음과 같다.

각 기술은 하나의 주된 책임을 가져야 한다.  
하나의 기술이 모든 역할을 대신해서는 안 된다.

---

## **2\. LEDO 전체 구조 안에서의 위치**

이 문서는 다음 위치에 속한다.

04\_ontology\_foundation/  
  01\_semantic\_web\_technology\_stack/

이 문서는 LEDO 전체 아키텍처 중 다음 영역을 지원한다.

Core Ontology Kernel  
Knowledge & Semantic Memory  
Real-Time World State  
Agent Interpretation  
Candidate Semantic Validation  
Relation Graph Validation  
Evidence and Audit Graph

시맨틱 웹 기술은 물리 시스템을 직접 제어하지 않는다.  
시맨틱 웹 기술은 Safety Gate를 대체하지 않는다.  
시맨틱 웹 기술은 외부 실행 계층을 대체하지 않는다.

시맨틱 웹 기술의 역할은 의미 부여, 구조화, 검증, 질의, 추적성 제공이다.

---

## **3\. 핵심 분리 원칙**

LEDO는 다음 책임을 분리한다.

의미 정의  
→ OWL / RDFS

그래프 표현  
→ RDF

데이터 검증  
→ SHACL

그래프 질의  
→ SPARQL

어휘 관리  
→ SKOS

증거 계보  
→ PROV-O

시간 모델링  
→ OWL-Time

공간 모델링  
→ GeoSPARQL

실행 안전 검증  
→ Safety Gate

운영 허용/금지 판단  
→ Policy Engine

물리 실행  
→ External Control Systems

이 분리는 아키텍처 혼동을 막기 위해 필수다.

OWL은 어떤 것이 무엇을 의미하는지 정의한다.  
SHACL은 데이터가 올바른 구조인지 검증한다.  
SPARQL은 그래프에서 의미 있는 사실을 조회한다.  
SKOS는 용어와 라벨을 정리한다.  
PROV-O는 증거가 어디에서 왔는지 설명한다.  
Safety Gate는 지금 이 조치를 실행해도 되는지 최종 검증한다.

---

## **4\. Runtime Flow와 기술 개입 위치**

LEDO runtime flow에서 시맨틱 웹 기술은 다음 위치에 개입한다.

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

단계별 주요 기술 개입은 다음과 같다.

| Runtime 단계 | 주요 기술 | 역할 |
| ----- | ----- | ----- |
| Raw Data | 없음 / 외부 시스템 | 아직 의미가 부여되지 않은 원시 입력 |
| Normalize | DTO / schema / parser | 필드명, 단위, 시간, ID 형식 정규화 |
| SHACL Validation | SHACL | 정규화된 데이터 구조 검증 |
| Canonical Object | Identity Resolver | 외부 ID를 canonical identity로 매핑 |
| Ontology Binding | RDF / RDFS / OWL | 객체를 class, property, relation에 연결 |
| RDF Graph Update | RDF / Triple Store | 의미 그래프에 사실 또는 참조 반영 |
| Evidence Binding | PROV-O / RDF | 판단 근거와 출처 연결 |
| World State Update | Runtime State Store / RDF reference | 현재 상태 갱신 |
| Event Detection | Rules / SPARQL / Graph Query | 상태 변화에서 의미 있는 사건 탐지 |
| Agent Interpretation | Agent / Ontology Context | 사건 해석과 조치 후보 생성 |
| ActionCandidate | DTO / RDF reference | 아직 실행 명령이 아닌 후보 조치 생성 |
| Candidate Semantic Validation | OWL / SHACL / SPARQL | 후보가 의미적으로 타당한지 검증 |
| Relation Graph Validation | SPARQL / Graph DB / cached view | 관계 그래프상 조치가 가능한지 확인 |
| Policy Pre-check | Policy Engine / OPA-style rules | 정책상 허용 가능성 사전 확인 |
| Decision Router | Rules / Risk Matrix | 자동 처리, 승인, escalation 분기 |
| Approval | Human / System Approval | 권한 있는 승인 처리 |
| Safety Gate | Deterministic Rules / cached state | 실행 직전 현재성, 충돌, 안전 조건 검증 |
| ExecutionRequest | DTO / Adapter Schema | 외부 시스템이 받을 요청 생성 |
| ExternalControlRequest | API / MQTT / OPC-UA / ROS2 등 | 외부 제어 시스템에 고수준 요청 전달 |
| Feedback | Event / Evidence | 실행 결과 수신 |
| Reconciliation | State comparison / Audit | 요청과 실제 결과 비교 |
| Audit | PROV-O / Audit Log / RDF reference | 전 과정 추적 기록 |

중요한 설계 규칙은 다음과 같다.

Semantic validation은 Decision Router 이전에 수행한다.  
Execution readiness validation은 Safety Gate에서 수행한다.  
Safety Gate는 무거운 추론기가 아니라 결정론적 최종 검문소다.

---

## **5\. RDF**

## **5.1 역할**

RDF는 LEDO 온톨로지 데이터의 기본 그래프 데이터 모델이다.

RDF는 지식을 triple 구조로 표현한다.

주어 → 술어 → 목적어  
subject → predicate → object

예시는 다음과 같다.

ot:GasSensor\_17 ot:observes ot:GasConcentration\_Zone\_A.  
ot:GasSensor\_17 ot:locatedIn ot:Zone\_A.  
ot:GasObservation\_901 ot:generatedBy ot:GasSensor\_17.

RDF는 다음을 표현하는 데 사용된다.

객체  
클래스  
속성  
관계  
관측  
이벤트  
증거 참조  
감사 참조  
외부 매핑 참조

## **5.2 LEDO 사용 기준**

LEDO에서 RDF는 의미 그래프를 표현하는 데 사용한다.

모든 raw sensor value를 RDF에 저장해서는 안 된다. 고빈도 원시 데이터는 stream storage, time-series storage, object storage, relational storage에 둘 수 있다. RDF에는 의미, 관계, 참조, 증거 기반으로 선별된 사실을 저장한다.

## **5.3 원칙**

RDF는 의미와 관계를 저장한다.  
RDF는 raw telemetry database가 되어서는 안 된다.

---

## **6\. RDFS**

## **6.1 역할**

RDFS는 가벼운 schema semantics를 제공한다.

RDFS는 다음을 정의하는 데 사용된다.

rdfs:Class  
rdfs:subClassOf  
rdfs:subPropertyOf  
rdfs:domain  
rdfs:range  
rdfs:label  
rdfs:comment

## **6.2 LEDO 사용 기준**

RDFS는 다음에 사용한다.

기본 클래스 계층  
기본 속성 계층  
사람이 읽을 수 있는 라벨  
단순 domain/range 선언  
문서화 주석

예시는 다음과 같다.

ot:GasSensor rdfs:subClassOf ot:Sensor.  
ot:RobotAgent rdfs:subClassOf ot:Agent.  
ot:observes rdfs:domain ot:Sensor.  
ot:observes rdfs:range ot:ObservableCondition.

## **6.3 원칙**

RDFS는 기본 골격을 제공한다.  
OWL은 더 강한 형식 의미를 제공한다.

---

## **7\. OWL**

## **7.1 역할**

OWL은 형식 온톨로지 모델링과 의미 추론에 사용된다.

OWL은 다음을 정의한다.

클래스 공리  
속성 공리  
동등성  
분리성  
역속성  
제약  
카디널리티  
속성 특성  
클래스 추론  
관계 추론

## **7.2 LEDO 사용 기준**

OWL은 LEDO에서 형식적 의미를 정의하는 데 사용한다.

예시는 다음과 같다.

ot:HumanoidRobot rdfs:subClassOf ot:RobotAgent.  
ot:GasSensor rdfs:subClassOf ot:Sensor.  
ot:DangerZone owl:disjointWith ot:SafeZone.  
ot:requiresPermit rdfs:domain ot:HighRiskTask.  
ot:requiresPermit rdfs:range ot:Permit.

OWL은 다음 질문에 답하는 데 도움을 준다.

이 객체는 Agent의 한 종류인가?  
이 작업은 HighRiskTask의 한 종류인가?  
이 구역 분류는 다른 구역 분류와 충돌하는가?  
기존 공리로부터 이 클래스 소속을 추론할 수 있는가?

## **7.3 Runtime 경계**

OWL 추론은 통제되어야 한다.

무거운 OWL reasoning을 실시간 Safety Gate 경로에 직접 넣어서는 안 된다.

LEDO에서 OWL은 주로 다음에 사용한다.

온톨로지 일관성 검사  
offline 또는 controlled reasoning  
클래스 분류  
의미 확장  
후보 검증 보조  
precomputed inference view 생성

## **7.4 원칙**

OWL은 의미를 확장한다.  
OWL은 runtime safety validation을 대체하지 않는다.

---

## **8\. SPARQL**

## **8.1 역할**

SPARQL은 RDF 그래프를 질의하는 언어다.

SPARQL은 의미 사실, 관계, 증거, 감사 연결을 조회하는 데 사용된다.

## **8.2 LEDO 사용 기준**

SPARQL은 다음에 사용한다.

의미 검색  
competency question 실행  
증거 조회  
관계 탐색  
감사 조사  
온톨로지 QA  
후보 검증 보조

예시 competency question은 다음과 같다.

현재 위험 구역에 위치한 agent는 누구인가?  
고위험 판단을 뒷받침하는 observation은 무엇인가?  
가스 위험 이벤트의 증거를 생성한 sensor는 무엇인가?  
특정 risk를 근거로 제안된 action은 무엇인가?  
어떤 외부 시스템이 execution request를 받았는가?

## **8.3 Runtime 경계**

SPARQL은 runtime 흐름에서 사용할 수 있지만, 고지연 그래프 질의가 Safety Gate 실행 경로를 막아서는 안 된다.

자주 사용하는 질의 결과는 cache 또는 materialized view로 관리해야 한다.

## **8.4 원칙**

SPARQL은 의미 사실을 조회한다.  
SPARQL은 runtime decision mechanism 전체가 되어서는 안 된다.

---

## **9\. SHACL**

## **9.1 역할**

SHACL은 RDF 데이터 검증에 사용된다.

SHACL은 데이터가 기대하는 shape에 맞는지 확인한다.

SHACL은 다음을 검증한다.

필수 속성  
데이터 타입  
값 범위  
카디널리티  
클래스 소속  
node shape  
property shape  
cross-reference 조건  
evidence reference 조건

## **9.2 LEDO 사용 기준**

SHACL은 데이터가 들어오거나 semantic state가 바뀌는 지점에서 사용한다.

주요 검증 지점은 다음과 같다.

정규화 이후  
온톨로지 바인딩 이전  
증거 바인딩 이전  
World State 갱신 이전  
ActionCandidate 승격 이전  
ExecutionRequest 생성 이전

검증 질문 예시는 다음과 같다.

이 Observation은 source를 가지고 있는가?  
이 Observation은 timestamp를 가지고 있는가?  
이 EvidenceBundle은 원본 데이터를 참조하는가?  
이 ActionCandidate는 action type을 가지고 있는가?  
이 ActionCandidate는 target을 가지고 있는가?  
이 target은 허용된 class에 속하는가?

## **9.3 원칙**

SHACL은 데이터를 검증한다.  
OWL은 의미를 정의한다.  
둘을 혼동해서는 안 된다.

---

## **10\. SKOS**

## **10.1 역할**

SKOS는 어휘와 용어 관리를 위해 사용된다.

SKOS는 다음을 제공한다.

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

## **10.2 LEDO 사용 기준**

SKOS는 다음을 지원한다.

사람이 읽을 수 있는 용어 체계  
다국어 라벨  
도메인 용어 정규화  
의미 검색  
SLM 학습 텍스트 구조화  
현장 언어와 온톨로지 용어 매핑  
문서화

예시는 다음과 같다.

ot:GasRiskConcept skos:prefLabel "Gas risk"@en.  
ot:GasRiskConcept skos:altLabel "Gas hazard"@en.  
ot:GasRiskConcept skos:definition "A risk condition involving hazardous gas concentration."@en.

## **10.3 SKOS와 OWL의 관계**

SKOS는 OWL을 대체하지 않는다.

SKOS는 개념 주변의 언어를 정리한다.  
OWL은 형식 의미를 정의한다.

예를 들어 `GasRisk`라는 OWL class가 있다면, SKOS는 그 class 주변의 인간 언어를 정리한다.

OWL  
→ ot:GasRisk는 Risk의 하위 class다.

SKOS  
→ Gas risk, gas hazard, hazardous gas condition 같은 용어를 정리한다.

SLM 학습, 검색, 문서화, 현장 용어 매핑에는 SKOS가 유용하다.  
하지만 class hierarchy, disjointness, restriction, reasoning은 OWL이 담당해야 한다.

## **10.4 원칙**

OWL은 형식 의미를 정의한다.  
SKOS는 그 의미 주변의 용어를 정리한다.  
SKOS를 formal ontology로 사용해서는 안 된다.

---

## **11\. PROV-O**

## **11.1 역할**

PROV-O는 provenance와 traceability를 위해 사용된다.

PROV-O는 다음을 설명한다.

entity  
activity  
agent  
generation  
derivation  
attribution  
usage  
source lineage

## **11.2 LEDO 사용 기준**

PROV-O는 다음을 추적하는 데 사용한다.

어떤 sensor가 observation을 생성했는가  
어떤 system이 data record를 제공했는가  
어떤 agent가 action candidate를 생성했는가  
어떤 evidence가 decision을 지원했는가  
어떤 approval이 execution request로 이어졌는가  
어떤 external feedback이 world state를 갱신했는가

예시는 다음과 같다.

ot:GasObservation\_901 prov:wasGeneratedBy ot:GasSensor\_17.  
ot:ActionCandidate\_55 prov:wasDerivedFrom ot:EvidenceBundle\_77.  
ot:ExecutionRequest\_21 prov:wasAttributedTo ot:SafetyGate\_01.

## **11.3 Evidence Bundle 생성 흐름 예시**

Evidence Bundle은 단일 데이터가 아니라, 판단에 사용 가능한 증거 묶음이다.

예시는 다음과 같다.

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

이 흐름을 PROV-O 관점으로 표현하면 다음과 같다.

ot:GasObservation\_901 prov:wasGeneratedBy ot:GasSensor\_17.  
ot:GasObservation\_901 prov:wasDerivedFrom ot:RawTelemetryRecord\_5501.  
ot:RawTelemetryRecord\_5501 prov:wasAttributedTo ot:SourceSystem\_OPCUA\_01.  
ot:EvidenceBundle\_77 ot:includesEvidence ot:GasObservation\_901.  
ot:GasRiskEvent\_12 ot:supportedBy ot:EvidenceBundle\_77.  
ot:ActionCandidate\_55 prov:wasDerivedFrom ot:GasRiskEvent\_12.

이 구조를 통해 나중에 다음 질문에 답할 수 있어야 한다.

이 조치 후보는 어떤 증거에서 나왔는가?  
그 증거는 어떤 원시 데이터에서 나왔는가?  
그 원시 데이터는 어떤 시스템에서 왔는가?  
그 시스템은 신뢰 가능한가?  
그 증거는 아직 시간적으로 유효한가?

## **11.4 원칙**

중요한 판단은 provenance 없이 존재해서는 안 된다.  
Evidence는 반드시 추적 가능해야 한다.

---

## **12\. OWL-Time**

## **12.1 역할**

OWL-Time은 시간 개념과 시간 관계를 표현하는 데 사용된다.

OWL-Time은 다음을 지원한다.

instant  
interval  
duration  
before  
after  
during  
hasBeginning  
hasEnd

## **12.2 LEDO 사용 기준**

OWL-Time은 다음을 지원한다.

event timing  
observation timing  
evidence freshness  
state validity  
approval validity  
execution request timing  
feedback timing  
audit timeline

중요한 runtime 질문은 다음과 같다.

이 evidence는 아직 fresh한가?  
이 event는 action candidate보다 먼저 발생했는가?  
approval은 candidate 생성 이후에 이루어졌는가?  
feedback은 기대 시간 안에 도착했는가?

## **12.3 원칙**

시간은 단순 metadata가 아니다.  
시간은 유효성, 안전성, 감사 가능성에 영향을 준다.

---

## **13\. GeoSPARQL**

## **13.1 역할**

GeoSPARQL은 공간 표현과 공간 질의를 위해 사용된다.

GeoSPARQL은 다음을 지원한다.

geometry  
spatial object  
spatial relation  
within  
intersects  
contains  
near  
distance

## **13.2 LEDO 사용 기준**

GeoSPARQL은 다음을 지원한다.

zone modeling  
danger zone 관계  
agent location  
equipment location  
robot location  
restricted area check  
spatial risk query  
digital twin spatial alignment

예시 질문은 다음과 같다.

어떤 agent가 Zone\_A 안에 있는가?  
어떤 sensor가 danger zone과 교차하는 영역을 관측하는가?  
어떤 robot agent가 restricted region 근처에 있는가?  
어떤 작업 영역이 active risk region과 겹치는가?

## **13.3 Runtime 경계**

공간 계산은 비용이 클 수 있다.

자주 사용하는 공간 관계는 runtime validation을 위해 cache 또는 materialized view로 관리할 수 있다.

## **13.4 원칙**

GeoSPARQL은 공간 의미를 제공한다.  
실시간 공간 안전 검증은 cache 또는 최적화된 runtime view가 필요할 수 있다.

---

## **14\. Triple Store와 Graph Database**

## **14.1 Triple Store 역할**

Triple Store는 RDF 데이터를 저장하고 SPARQL 질의를 실행하는 저장소다.

Triple Store는 다음에 사용한다.

ontology graph 저장  
semantic fact 저장  
class/property 관계 저장  
선별된 evidence reference 저장  
semantic mapping 저장  
audit graph reference 저장  
competency question 실행

Triple Store는 semantic graph data의 primary store다.

## **14.2 Graph Database 역할**

Neo4j 같은 Graph Database는 운영 그래프 탐색, graph analytics, runtime relationship exploration에 사용할 수 있다.

Graph Database는 다음을 지원할 수 있다.

runtime dependency graph  
agent-task-resource graph  
control relationship graph  
impact analysis  
shortest path analysis  
operational relationship exploration

## **14.3 판단 기준**

Triple Store를 primary로 사용하는 경우는 다음과 같다.

OWL/RDFS 의미와 직접 연결되는 데이터  
SPARQL 질의가 필요한 데이터  
ontology class/property와 연결된 semantic fact  
evidence, provenance, audit reference  
표준 기반 RDF export가 필요한 데이터

Graph Database를 사용하는 경우는 다음과 같다.

빠른 graph traversal이 필요한 경우  
운영 관계 탐색이 많은 경우  
경로 탐색이나 영향도 분석이 필요한 경우  
runtime dependency graph가 필요한 경우  
복잡한 operational graph query를 빠르게 처리해야 하는 경우

LEDO에서 원칙은 다음과 같다.

Triple Store는 semantic authority다.  
Graph Database는 operational graph acceleration이다.

Graph Database가 더 빠르더라도 semantic authority가 되어서는 안 된다.  
Graph Database에 들어간 운영 그래프는 Triple Store 또는 Ontology Kernel의 의미 기준과 동기화되어야 한다.

---

## **15\. Reasoner**

## **15.1 역할**

Reasoner는 OWL 공리로부터 추가 사실을 추론한다.

Reasoner는 다음을 수행할 수 있다.

class classification  
subclass inference  
property inference  
consistency checking  
unsatisfiable class detection  
equivalence inference  
restriction-based inference

## **15.2 LEDO 사용 기준**

Reasoner는 다음에 사용한다.

ontology QA  
model consistency check  
offline inference  
controlled semantic enrichment  
release validation  
axiom change impact assessment

## **15.3 Runtime 경계**

Reasoner를 Safety Gate hot path 안에 직접 넣어서는 안 된다.

Runtime에서는 다음을 사용한다.

precomputed inference view  
cached semantic classification  
SHACL validation  
policy rule  
graph query  
deterministic safety check

## **15.4 원칙**

Reasoner는 강력하지만 통제되어야 한다.  
Runtime safety는 결정론적으로 유지되어야 한다.

---

## **16\. Runtime Cache / Materialized View 전략**

Runtime에서 모든 의미 질의와 공간 질의를 매번 Triple Store나 GeoSPARQL로 직접 수행하면 병목이 발생할 수 있다.

따라서 LEDO는 자주 사용하는 관계, 분류, 위험 상태, 공간 포함 관계를 cache 또는 materialized view로 관리할 수 있다.

미리 계산하거나 캐시할 수 있는 대상은 다음과 같다.

agent가 현재 어떤 zone 안에 있는가  
zone이 현재 active risk를 가지고 있는가  
특정 action type이 어떤 target class에 허용되는가  
특정 risk를 mitigate할 수 있는 action type은 무엇인가  
특정 task가 permit을 요구하는가  
특정 object의 inferred class hierarchy는 무엇인가  
특정 evidence가 아직 fresh한가  
특정 external system이 현재 available한가  
특정 zone이 restricted 상태인가  
특정 sensor가 어떤 zone을 관측하는가

Safety Gate는 가능하면 무거운 graph query를 직접 수행하지 않고, 다음을 사용해야 한다.

cached world state  
precomputed inference view  
materialized relation view  
policy decision cache  
freshness-checked evidence reference  
deterministic rule evaluation

단, cache는 항상 freshness와 invalidation 전략을 가져야 한다.

오래된 cache는 안전하지 않다.  
cache는 빠르지만 truth source가 아니다.  
cache 결과는 원본 semantic graph와 추적 가능해야 한다.

---

## **17\. 주요 기술 조합 예시**

## **17.1 Gas Risk Event 발생 시**

가스 위험 이벤트가 발생하면 다음 기술 조합이 사용된다.

Raw gas telemetry  
→ Normalize  
→ SHACL Validation  
→ GasObservation RDF 생성  
→ PROV-O로 source lineage 연결  
→ OWL-Time으로 observation time/freshness 기록  
→ Ontology Binding으로 GasRisk 관련 class 연결  
→ SPARQL로 관련 zone, sensor, agent 조회  
→ Graph Validation으로 영향을 받는 대상 확인  
→ EvidenceBundle 생성  
→ Event Detection

주요 기술 조합은 다음과 같다.

SHACL  
→ observation 구조 검증

RDF / OWL  
→ GasObservation, GasRisk, Zone, Sensor 의미 연결

PROV-O  
→ 데이터 출처와 증거 계보 연결

OWL-Time  
→ evidence freshness 검증

SPARQL  
→ 관련 sensor, zone, agent 조회

Graph DB 또는 cached view  
→ runtime 영향 범위 빠른 탐색

---

## **17.2 ActionCandidate 검증 시**

Agent가 다음 후보를 만들었다고 가정한다.

ActionCandidate:  
  action\_type: restrict\_access  
  target: Zone\_A  
  reason: GasRiskEvent\_12

이 후보는 바로 Decision Router로 가면 안 된다. 먼저 semantic validation과 relation graph validation을 수행해야 한다.

검증 질문은 다음과 같다.

restrict\_access는 등록된 action type인가?  
Zone\_A는 실제 Zone인가?  
GasRiskEvent\_12는 EvidenceBundle로 뒷받침되는가?  
해당 EvidenceBundle은 fresh한가?  
GasRiskEvent\_12가 Zone\_A에 영향을 주는가?  
restrict\_access는 GasRisk를 mitigate할 수 있는 action인가?  
이 action은 target class가 Zone일 때 허용되는가?

주요 기술 조합은 다음과 같다.

OWL  
→ action, risk, zone class 의미 확인

SHACL  
→ ActionCandidate 구조 검증

SPARQL  
→ risk, target, evidence 관계 조회

PROV-O  
→ 후보 조치가 어떤 evidence에서 나왔는지 확인

OWL-Time  
→ evidence와 world state의 시간 유효성 확인

Policy Engine  
→ 사전 허용/금지 조건 확인

---

## **17.3 Audit 조사 시**

나중에 특정 실행 요청이 왜 발생했는지 조사해야 할 수 있다.

질문은 다음과 같다.

왜 ExecutionRequest\_21이 생성되었는가?  
어떤 ActionCandidate에서 왔는가?  
그 후보는 어떤 Event에서 왔는가?  
그 Event는 어떤 EvidenceBundle로 뒷받침되었는가?  
그 EvidenceBundle은 어떤 Observation에서 왔는가?  
그 Observation은 어떤 Sensor와 SourceSystem에서 왔는가?  
누가 승인했는가?  
Safety Gate는 무엇을 검증했는가?  
외부 시스템 피드백은 무엇이었는가?

주요 기술 조합은 다음과 같다.

PROV-O  
→ 전체 lineage 추적

RDF  
→ 관련 entity 관계 표현

SPARQL  
→ 감사 질의 실행

OWL-Time  
→ timeline 재구성

Audit Log  
→ 승인, 검증, 실행, 피드백 기록 확인

---

## **18\. Runtime 책임 매트릭스**

| 책임 | 주 기술 | Runtime 사용 |
| ----- | ----- | ----- |
| 그래프 표현 | RDF | 사용 |
| 기본 클래스 계층 | RDFS | 사용 |
| 형식 온톨로지 의미 | OWL | 통제 사용 |
| 의미 질의 | SPARQL | 사용, 필요 시 cache |
| 데이터 검증 | SHACL | 사용 |
| 어휘와 라벨 | SKOS | 사용 |
| provenance / evidence lineage | PROV-O | 사용 |
| 시간 모델링 | OWL-Time | 사용 |
| 공간 모델링 | GeoSPARQL | 통제/최적화 사용 |
| Offline inference | OWL Reasoner | offline 또는 controlled |
| Runtime 관계 탐색 | Graph Database | 사용 |
| 실행 안전 검증 | Safety Gate | 사용 |
| 운영 허용/금지 판단 | Policy Engine | 사용 |
| 물리 실행 | External Control System | 사용 |

---

## **19\. Anti-Patterns**

| Anti-pattern | 문제 | 발생 가능한 피해 | 대안 |
| ----- | ----- | ----- | ----- |
| OWL을 runtime safety validation으로 사용하는 것 | OWL reasoning은 실행 가능성 검증이 아니다 | 실행 직전 검증 지연, 위험한 판단 누락 | Safety Gate는 deterministic rule과 cached state 사용 |
| 모든 raw telemetry를 RDF에 저장하는 것 | Triple Store가 과부하된다 | graph write bottleneck, query 지연 | raw data는 time-series/object store에 저장하고 RDF에는 reference 저장 |
| SHACL을 ontology semantics로 사용하는 것 | SHACL은 shape 검증이고 형식 의미 정의가 아니다 | 의미 추론이 불가능하거나 혼동됨 | 의미는 OWL, 검증은 SHACL로 분리 |
| SKOS를 formal ontology로 사용하는 것 | SKOS는 어휘 관리이고 OWL이 형식 의미를 정의한다 | class hierarchy와 vocabulary가 혼동됨 | SKOS는 label/definition/search/SLM용으로 사용 |
| 무거운 reasoner를 Safety Gate에 넣는 것 | 실행 경로가 느려지고 불안정해진다 | 긴급 조치 지연, timeout | offline reasoning과 precomputed inference view 사용 |
| Graph DB를 semantic authority로 취급하는 것 | 운영 그래프가 온톨로지 의미와 어긋날 수 있다 | 관계 해석 불일치, audit 오류 | Triple Store/Ontology Kernel을 semantic authority로 유지 |
| provenance를 무시하는 것 | 판단이 감사 불가능해진다 | 사고 후 원인 추적 실패, 책임성 붕괴 | PROV-O와 EvidenceBundle 사용 |
| 시간 유효성을 무시하는 것 | 오래된 evidence가 위험한 결정을 지원할 수 있다 | 이미 변한 상태에 근거한 조치 발생 | OWL-Time, freshness check, state timestamp 사용 |
| 공간 모델링을 무시하는 것 | 위치 기반 risk reasoning이 불안정해진다 | 영향을 받지 않는 대상에 조치하거나 실제 위험 대상 누락 | GeoSPARQL 또는 runtime spatial view 사용 |
| 모든 graph check를 agent 안에 hardcoding하는 것 | 검증이 비거버넌스화되고 일관성이 깨진다 | agent마다 다른 판단, 재현 불가 | Candidate Semantic Validation 계층으로 분리 |

---

## **20\. 핵심 원칙**

RDF는 graph model이다.  
RDFS는 basic schema layer다.  
OWL은 formal meaning layer다.  
SPARQL은 query layer다.  
SHACL은 validation layer다.  
SKOS는 vocabulary layer다.  
PROV-O는 provenance layer다.  
OWL-Time은 temporal layer다.  
GeoSPARQL은 spatial layer다.  
Triple Store는 semantic graph store다.  
Graph Database는 operational graph acceleration이다.  
Reasoner는 controlled semantic inference다.  
Safety Gate는 deterministic execution validation이다.

최종 원칙은 다음과 같다.

시맨틱 웹 기술은 의미를 정의하고, 검증하고, 질의하고, 추적한다.  
시맨틱 웹 기술은 물리 세계를 직접 실행하지 않는다.

