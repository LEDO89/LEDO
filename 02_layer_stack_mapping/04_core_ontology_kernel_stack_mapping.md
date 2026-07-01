# **Ontology Centric “Core Ontology Kernel” Stack Mapping**

## **Layer 4\. Core Ontology Kernel Layer**

─ Core Position  
└── Core Ontology Kernel is the semantic kernel of the ontology-centric system  
└── It defines the formal meaning of objects, relationships, attributes, events, actions, capabilities, constraints, policies, workflows, and inference contracts  
└── It is the semantic source of truth for the system  
└── It defines what things are, how they relate, what actions mean, what constraints exist, and what conditions must be satisfied  
└── It does not execute physical commands  
└── It does not replace runtime world state storage  
└── It does not replace the policy engine  
└── It does not replace the decision router  
└── It does not replace the safety gate  
└── It provides the semantic model that other layers validate against

---

## **Core Role**

└── Define the formal meaning of construction site entities, relationships, actions, capabilities, states, policies, constraints, workflows, and inference contracts  
└── Provide ontology-grounded structure for workers, robots, equipment, zones, tasks, sensors, incidents, documents, resources, risks, policies, and actions  
└── Define object types, link types, attribute types, event types, and action types  
└── Define class hierarchy, domain / range, cardinality, disjointness, inverse relations, and transitive relations  
└── Define capability models, interface contracts, execution preconditions, and availability constraints  
└── Define semantic rules for safety, authorization, operational constraints, approval rules, and emergency rules  
└── Bind static ontology meaning to dynamic world state through explicit world state binding contracts  
└── Support ontology governance, versioning, migration, compatibility checks, and validation  
└── Provide formal semantic constraints used by agents, decision router, safety gate, knowledge layer, and execution request layer

---

## **Core Technologies**

└── OWL 2  
└── RDF  
└── RDFS  
└── SHACL  
└── SPARQL  
└── SWRL with restricted usage  
└── BFO  
└── SOSA / SSN  
└── SAREF  
└── PROV-O  
└── QUDT  
└── GeoSPARQL  
└── RDFLib  
└── OWLReady2  
└── Protégé  
└── HermiT  
└── Pellet  
└── Ontology Versioning  
└── Ontology Migration  
└── Compatibility Check  
└── Ontology Module Registry  
└── IRI Governance  
└── Namespace Governance

---

## **Optional Technologies**

└── Apache Jena SHACL  
└── Apache Jena Fuseki  
└── GraphDB Validation  
└── Stardog Integrity Constraints  
└── SHACL Rules  
└── SPARQL CONSTRUCT Materialization  
└── R2RML / RML Mapping  
└── YARRRML  
└── OWL API  
└── ROBOT Ontology Tool  
└── Ontology Diff Tool  
└── Ontology Release Pipeline  
└── CI-based Ontology Validation  
└── Ontology Documentation Generator  
└── SKOS for controlled vocabularies  
└── DCAT for dataset metadata

---

## **Ontology Schema Stack**

└── Object Types  
└── Link Types  
└── Attribute Types  
└── Event Types  
└── Action Types  
└── Capability Types  
└── Interface Types  
└── Policy Types  
└── Constraint Types  
└── Workflow Types  
└── State Types  
└── Evidence Types  
└── Approval Types  
└── Execution Request Types

Schema Purpose:  
└── Define the system vocabulary  
└── Define what entities can exist  
└── Define which relationships are allowed  
└── Define what attributes are valid  
└── Define what events and actions mean  
└── Provide stable contracts for APIs, agents, UI, validation, and execution request generation

---

## **Object Type Stack**

└── Worker  
└── Supervisor  
└── Robot  
└── Humanoid  
└── Drone  
└── Equipment  
└── Sensor  
└── Camera  
└── Zone  
└── Task  
└── WorkPackage  
└── Incident  
└── Hazard  
└── Risk  
└── Resource  
└── Material  
└── Document  
└── Permit  
└── Inspection  
└── Capability  
└── Interface  
└── Goal  
└── Policy  
└── Constraint  
└── Action  
└── ExecutionRequest  
└── FeedbackEvent

Design Rule:  
└── Object Types must be domain-meaningful, stable, and mapped to upper ontology alignment when useful  
└── Object Types should not be created randomly by LLM output  
└── New canonical object types require ontology governance review

---

## **Link Type Stack**

└── locatedIn  
└── assignedTo  
└── requiresCapability  
└── hasCapability  
└── hasRisk  
└── supervises  
└── dependsOn  
└── owns  
└── operates  
└── managedBy  
└── reportsTo  
└── observes  
└── detects  
└── generatedBy  
└── hasEvidence  
└── hasPolicy  
└── hasConstraint  
└── requiresApproval  
└── producedActionCandidate  
└── resultedIn  
└── affectedBy  
└── partOf  
└── adjacentTo  
└── withinZone

Control Boundary Rule:  
└── Link types such as controls, managedBy, or operates must be carefully defined  
└── The ontology may represent that an external controller controls a robot or machine  
└── The ontology system itself must not be modeled as directly performing low-level physical control unless the actual control boundary exists

Recommended Naming:  
└── isManagedBy for fleet manager relationships  
└── isControlledBy for physical controller relationships  
└── requestedBy for high-level execution request relationships  
└── executedBy for external system execution relationships

---

## **Attribute Type Stack**

└── identifier  
└── label  
└── description  
└── status  
└── mode  
└── availability  
└── location  
└── timestamp  
└── sourceTimestamp  
└── ingestionTimestamp  
└── confidenceScore  
└── riskLevel  
└── priority  
└── approvalStatus  
└── executionStatus  
└── capabilityLevel  
└── certificationStatus  
└── batteryLevel  
└── signalQuality  
└── freshness  
└── version  
└── validFrom  
└── validUntil

Attribute Rule:  
└── Static attributes belong to ontology / knowledge layer  
└── Dynamic attributes belong to world state binding and real-time state layer  
└── Every operational attribute used for decision-making must have source, timestamp, and freshness when relevant

---

## **Event Type Stack**

└── SensorEvent  
└── WorkerLocationEvent  
└── RobotTelemetryEvent  
└── EquipmentStatusEvent  
└── ZoneRiskEvent  
└── HazardDetectedEvent  
└── IncidentReportedEvent  
└── ActionCandidateCreatedEvent  
└── DecisionCaseCreatedEvent  
└── ApprovalRequestedEvent  
└── ApprovalDecisionEvent  
└── ApprovedActionCreatedEvent  
└── ExecutionRequestCreatedEvent  
└── ExternalControlFeedbackEvent  
└── ManualOverrideEvent  
└── EmergencyEvent  
└── OntologyChangeEvent  
└── PolicyChangeEvent  
└── AuditEvent

Event Rule:  
└── Event types define meaning and structure  
└── Event instances and event streams belong to real-time world state, event store, and observability layers

---

## **Action Type Stack**

└── ACTION\_STOP\_WORK  
└── ACTION\_EVACUATE  
└── ACTION\_LOCK\_ZONE  
└── ACTION\_NOTIFY\_MANAGER  
└── ACTION\_DISPATCH\_ROBOT  
└── ACTION\_REPLAN\_ROUTE  
└── ACTION\_RESUME\_WORK  
└── ACTION\_REQUEST\_INSPECTION  
└── ACTION\_EMERGENCY\_STOP  
└── ACTION\_REQUEST\_MANUAL\_REVIEW  
└── ACTION\_MARK\_ZONE\_RESTRICTED  
└── ACTION\_UPDATE\_RISK\_STATE  
└── ACTION\_REQUEST\_EQUIPMENT\_CHECK  
└── ACTION\_TRIGGER\_ALARM  
└── ACTION\_SEND\_WARNING

Action Type Rule:  
└── Only ontology-defined Action Types can become ActionCandidate or ApprovedAction  
└── Action Types must define preconditions, constraints, required capability, required approval, target object type, and expected feedback  
└── LLMs or agents may propose action candidates only using registered Action Types  
└── Unknown action types must be rejected or sent to ontology governance review

---

## **Ontology Semantics Stack**

└── Class Hierarchy  
└── SubClassOf  
└── EquivalentClass  
└── DisjointClass  
└── Domain  
└── Range  
└── Cardinality  
└── Inverse Relations  
└── Transitive Relations  
└── Symmetric Relations where appropriate  
└── Functional Properties where appropriate  
└── Object Properties  
└── Data Properties  
└── Annotation Properties  
└── TBox  
└── ABox  
└── RBox

Semantic Purpose:  
└── Define what each class means  
└── Define allowed relationship structures  
└── Define valid property usage  
└── Define constraints that make the knowledge model consistent and machine-checkable

---

## **Upper Ontology & Domain Alignment Stack**

└── BFO for upper-level structure  
└── SOSA / SSN for sensors, observations, sampling, and sensor systems  
└── SAREF for smart devices and energy-related device modeling when useful  
└── PROV-O for provenance, lineage, source, agent, and activity tracking  
└── QUDT for units, quantities, measurement values, and unit consistency  
└── GeoSPARQL for geospatial relationships, geometry, and spatial queries  
└── SKOS optional for vocabulary, labels, aliases, and controlled terms

Alignment Rule:  
└── BFO and standards should guide structure, not suffocate practical construction modeling  
└── Use standards where they clarify meaning, interoperability, provenance, measurement, or spatial semantics  
└── Do not force every domain class into excessive theoretical depth during MVP

---

## **Capability & Interface Stack**

└── Capability Model  
└── Interface Contract  
└── Execution Preconditions  
└── Availability State  
└── Operational State  
└── Required Capability  
└── Provided Capability  
└── Capability Level  
└── Certification Requirement  
└── Tool Requirement  
└── Zone Permission Requirement  
└── ExternalControlInterface  
└── FleetManagerInterface  
└── MovableInterface  
└── InspectableInterface  
└── CommunicableInterface  
└── OperableInterface  
└── TransportableInterface  
└── MonitorableInterface

Capability Examples:  
└── Robot hasCapability InspectionCapability  
└── Drone hasCapability AerialInspectionCapability  
└── Worker hasCertification ConfinedSpacePermit  
└── Equipment hasCapability HeavyLiftCapability  
└── FleetManager provides FleetManagerInterface  
└── ExternalControlSystem provides ExternalControlInterface

Capability Rule:  
└── Capability matching must be ontology-grounded  
└── Capability existence does not mean execution is allowed  
└── Execution still requires policy validation, current state validation, approval validation, and safety gate validation

---

## **Policy / Constraint Stack**

└── Safety Policy  
└── Authorization Policy  
└── Operational Constraint  
└── Approval Rule  
└── Emergency Rule  
└── Zone Constraint  
└── Task Constraint  
└── Robot Operation Constraint  
└── Equipment Operation Constraint  
└── Worker Certification Constraint  
└── Permit Constraint  
└── Environmental Constraint  
└── Legal Compliance Constraint  
└── Human Safety Constraint  
└── Execution Precondition  
└── Postcondition  
└── Conflict Rule

Boundary:  
└── Ontology defines semantic policy concepts and constraint structures  
└── Governance / Policy / Security evaluates authorization and authority policy  
└── Safety Gate validates executable action eligibility  
└── OPA / Rego may implement operational policy evaluation  
└── SHACL may validate structural and semantic constraints

---

## **Process / Workflow Model Stack**

└── Construction Workflow  
└── Safety Workflow  
└── Inspection Workflow  
└── Emergency Workflow  
└── Robot Workflow  
└── Approval Workflow  
└── Execution Workflow  
└── Recovery Workflow  
└── Work Package Model  
└── Task Dependency Model  
└── Procedure Model  
└── Permit Workflow  
└── Incident Response Workflow  
└── Manual Override Workflow

Workflow Rule:  
└── Ontology defines workflow meaning, allowed states, dependencies, and relationships  
└── Runtime workflow execution belongs to backend workflow engine, state machine, or orchestration service  
└── Workflow visualization belongs to Experience Layer

---

## **Inference Function Specification Stack**

└── Risk Score Definition  
└── Capability Matching Contract  
└── Task Allocation Rule Contract  
└── Conflict Resolution Policy  
└── Priority Evaluation Model  
└── Resource Optimization Constraint  
└── Safety Compatibility Rule  
└── Zone Access Rule  
└── Emergency Escalation Rule  
└── Approval Requirement Rule  
└── Evidence Requirement Rule

Important Boundary:  
└── Inference Function Specification is not the same as runtime inference execution  
└── This layer defines the meaning, input requirements, output contracts, and constraints of inference functions  
└── Runtime execution may happen in rule engine, graph query service, stream processor, decision router, agent service, or safety gate

Example:  
└── Ontology defines what RiskScore means  
└── Runtime service computes a risk score using current world state, policy, graph context, and rule engine  
└── ApprovalDecision produces ApprovedAction; Safety Gate validates execution readiness by consuming ApprovedAction plus RuntimeValidationResult

---

## **World State Binding Stack**

└── Current Site State Binding  
└── Current Worker State Binding  
└── Current Robot State Binding  
└── Current Equipment State Binding  
└── Current Zone State Binding  
└── Current Risk State Binding  
└── Current Task State Binding  
└── Current Approval State Binding  
└── Current Execution State Binding  
└── State Freshness Requirement  
└── State Version Requirement  
└── Source Timestamp Requirement  
└── Ingestion Timestamp Requirement  
└── Confidence Requirement  
└── Stale State Rejection Rule

Boundary:  
└── Ontology defines what each state means  
└── Real-Time World State Layer stores and updates current runtime state  
└── Redis or world state cache may hold current values  
└── RDF / OWL should not receive every high-frequency telemetry tick  
└── RDF materialization should happen at meaningful event, threshold, aggregation, confirmation, or audit boundaries

---

## **Ontology Governance Stack**

└── Ontology Versioning  
└── Ontology Module Registry  
└── Namespace Governance  
└── IRI Governance  
└── Class Change Review  
└── Property Change Review  
└── Action Type Change Review  
└── Capability Model Change Review  
└── SHACL Shape Versioning  
└── Mapping Rule Versioning  
└── Ontology Migration  
└── Compatibility Check  
└── Change Impact Analysis  
└── Deprecation Policy  
└── Release Approval  
└── Rollback Plan  
└── Ontology Change Audit

Governance Rule:  
└── Ontology changes must be reviewed, versioned, tested, documented, and auditable  
└── Action Types, safety constraints, approval rules, and capability contracts require stronger review than ordinary labels or annotations

---

## **SHACL Validation Stack**

└── SHACL Shapes  
└── NodeShape  
└── PropertyShape  
└── Target Class  
└── Required Property Validation  
└── Datatype Validation  
└── Cardinality Validation  
└── Range Validation  
└── Pattern Validation  
└── Severity Level  
└── Validation Report  
└── Target-specific Validation  
└── ActionCandidate Shape  
└── ExecutionRequest Shape  
└── WorldState DTO Shape  
└── Knowledge Ingestion Shape

SHACL Usage:  
└── Validate RDF graph structure  
└── Validate ontology-grounded data shape  
└── Validate action candidates before safety gate processing  
└── Validate execution request structure before dispatch  
└── Validate knowledge ingestion before publication

Runtime Rule:  
└── Target-specific SHACL validation may be used in runtime paths  
└── Full graph validation should run offline, in CI, release validation, or batch jobs

---

## **SPARQL Stack**

└── SPARQL Query  
└── SPARQL Update  
└── SPARQL CONSTRUCT  
└── SPARQL ASK  
└── Named Graph Query  
└── Graph Pattern Matching  
└── Ontology Lookup  
└── Capability Lookup  
└── Policy Context Lookup  
└── Relationship Lookup  
└── Evidence Query  
└── Materialized Fact Query

SPARQL Usage:  
└── Query structured semantic knowledge  
└── Retrieve class, property, relation, capability, policy, and evidence context  
└── Support graph-based validation and retrieval  
└── Build materialized views for runtime services when needed

Boundary:  
└── SPARQL is powerful but should be bounded for runtime latency  
└── High-risk real-time queries must also check current world state freshness

---

## **OWL Reasoning Stack**

└── HermiT  
└── Pellet  
└── OWLReady2 Reasoner Integration  
└── Class Consistency Check  
└── Property Consistency Check  
└── Inferred Class Hierarchy  
└── Equivalent Class Detection  
└── Disjointness Violation Detection  
└── Unsatisfiable Class Detection  
└── Batch Materialization  
└── Ontology Release Validation

Runtime Boundary:  
└── HermiT and Pellet are used for offline ontology consistency checking, static knowledge validation, ontology release validation, and batch materialization  
└── They should not be placed in the real-time operational decision path  
└── Real-time decisions should use cached views, SHACL target validation, OPA / Rego, rule engines, stream processors, graph queries, and current world state checks

---

## **SWRL Stack**

└── SWRL Rules  
└── Rule-based Inference  
└── Semantic Rule Specification  
└── Offline Rule Validation  
└── Limited Batch Inference  
└── Rule Documentation

SWRL Rule:  
└── Use SWRL carefully and selectively  
└── Do not depend on SWRL as the main runtime operational decision engine  
└── For runtime policy and safety checks, prefer OPA / Rego, SHACL, rule engine, state machine, or explicit service logic  
└── SWRL may be useful for semantic rule prototypes, ontology-level inference, or batch reasoning scenarios

---

## **RDF / OWL Storage Stack**

└── RDF Triple Store  
└── Named Graphs  
└── Turtle  
└── RDF/XML  
└── JSON-LD  
└── Ontology Module Graph  
└── Instance Graph  
└── Policy Graph  
└── Provenance Graph  
└── Site-specific Graph  
└── Versioned Named Graph  
└── Materialized Inference Graph  
└── Release Graph

Storage Rule:  
└── Ontology modules should be separated from runtime high-frequency state  
└── Static semantic truth belongs in ontology / RDF store  
└── Current operational state belongs in real-time world state layer  
└── Materialized RDF must be freshness-aware if used operationally

---

## **Ontology Module Stack**

└── Core Module  
└── Site Module  
└── Worker Module  
└── Robot Module  
└── Equipment Module  
└── Sensor Module  
└── Zone Module  
└── Task Module  
└── Risk Module  
└── Safety Module  
└── Policy Module  
└── Action Module  
└── Capability Module  
└── Workflow Module  
└── Provenance Module  
└── Unit / Measurement Module  
└── Geospatial Module

Module Rule:  
└── Keep modules small enough to govern, validate, test, and version  
└── Avoid one giant ontology file for everything  
└── Separate core domain meaning from site-specific instance data

---

## **IRI / Namespace Governance Stack**

└── Base IRI  
└── Namespace Prefix  
└── Canonical IRI  
└── Stable Identifier  
└── Human-readable Label  
└── Multilingual Label  
└── Alias Mapping  
└── Deprecated IRI  
└── Replacement IRI  
└── Version IRI  
└── Entity IRI Pattern  
└── Action Type IRI Pattern  
└── Property IRI Pattern  
└── Document IRI Pattern  
└── Site-specific IRI Pattern

IRI Rule:  
└── IRIs must be stable, governed, and not randomly generated by LLM output  
└── Human labels can change, but canonical IRIs should remain stable  
└── Deprecated terms must map to replacement IRIs when possible

---

## **Data Contract Stack**

└── OntologyClassDTO  
└── OntologyPropertyDTO  
└── ObjectTypeDTO  
└── LinkTypeDTO  
└── AttributeTypeDTO  
└── EventTypeDTO  
└── ActionTypeDTO  
└── CapabilityDTO  
└── InterfaceContractDTO  
└── ConstraintDTO  
└── SHACLValidationResultDTO  
└── OntologyVersionDTO  
└── OntologyChangeDTO  
└── WorldStateBindingDTO  
└── InferenceContractDTO

Rule:  
└── API and frontend should consume ontology-derived DTOs  
└── Runtime services should not depend on raw ontology files directly in every request  
└── Stable DTO contracts should be generated or synchronized from ontology definitions when possible

---

## **Knowledge / Ontology Boundary**

└── Ontology defines meaning, classes, relations, constraints, action types, policy concepts, and validation structure  
└── Knowledge Layer stores instances, graph facts, documents, events, embeddings, evidence, and historical knowledge  
└── Semantic Memory retrieves context but does not redefine semantic truth  
└── Vector search supports recall but does not define ontology meaning  
└── Neo4j may support graph exploration or read models, but ontology semantics should remain grounded in RDF / OWL / SHACL where formal semantics are required

Boundary Rule:  
└── Ontology Core is the semantic source of truth  
└── Knowledge & Semantic Memory is the contextual memory and retrieval layer

---

## **Policy / Ontology Boundary**

└── Ontology defines policy concepts, action types, constraints, approval requirement structures, and semantic relationships  
└── Governance Layer evaluates authority, access control, approval rules, security boundaries, and compliance decisions  
└── OPA / Rego implements operational policy evaluation  
└── Safety Gate consumes ApprovedAction plus RuntimeValidationResult based on precomputed ontology, policy, current state, capability, evidence, and approval materialization

Boundary Rule:  
└── Ontology explains what a policy means  
└── Governance decides who is authorized and which policy applies  
└── ApprovalDecision produces ApprovedAction; Safety Gate issues SafetyGatePass or SafetyGateBlock and does not decide whether a candidate becomes ApprovedAction

---

## **Agent / Ontology Boundary**

└── Agents may read ontology definitions  
└── Agents may generate ActionCandidates using ontology-defined action types  
└── Agents may use ontology grounding to identify nodes, risks, tasks, and capabilities  
└── Agents may not invent canonical ontology classes without governance  
└── Agents may not treat LLM output as semantic truth  
└── Agents must return ontology-grounded structured outputs

Agent Rule:  
└── Agent output must be mapped to canonical IRIs, ontology-defined action types, evidence references, and validation status before operational use

---

## **Execution / Ontology Boundary**

└── Ontology defines Action Types, preconditions, constraints, capabilities, interfaces, and expected feedback  
└── Unified Cyber-Physical Core creates execution lifecycle objects  
└── Execution Request & External Control Integration converts ApprovedAction into high-level external requests  
└── External systems execute physical behavior  
└── Ontology does not perform robot motion planning, fleet scheduling, PLC logic, or device-level control

Execution Boundary Rule:  
└── Ontology defines operational meaning and constraints  
└── External control systems perform specialized execution

---

## **Runtime Boundary**

└── HermiT and Pellet are offline / batch / release validation tools  
└── Full OWL reasoning is not in the real-time path  
└── Real-time validation uses target-specific SHACL, OPA / Rego, rule engines, graph queries, cached views, stream processors, and world state freshness checks  
└── Runtime services should use precompiled ontology contracts, cached shapes, validated action type registry, and materialized views where needed  
└── High-frequency sensor events should not continuously update full RDF / OWL graphs  
└── Critical decisions must use current world state freshness and policy validation, not stale materialized semantic views alone

---

## **Not Responsible For**

└── Rendering UI dashboards  
└── Acting as API Gateway  
└── Authenticating users directly  
└── Managing final access control alone  
└── Replacing OPA / Rego policy evaluation  
└── Replacing Governance / Policy / Security Layer  
└── Storing all operational history  
└── Replacing real-time world state cache  
└── Running all inference in real time  
└── Generating LLM action candidates  
└── Routing decisions by risk tier  
└── Approving actions  
└── Creating ApprovedAction independently  
└── Executing physical commands  
└── Controlling robots, drones, equipment, PLC, SCADA, or fleet managers  
└── Performing motion planning  
└── Performing fleet scheduling  
└── Performing low-level robot behavior tree execution  
└── Replacing external control systems

---

## **Recommended MVP Stack Mapping**

└── Ontology Language: OWL 2 \+ RDF / RDFS  
└── Validation: SHACL  
└── Query: SPARQL  
└── Upper Alignment: BFO-light alignment  
└── Sensor Modeling: SOSA / SSN for sensor and observation concepts  
└── Provenance: PROV-O for evidence and lineage  
└── Units: QUDT for measurements  
└── Geospatial: GeoSPARQL later if spatial complexity requires it  
└── Development Tool: Protégé  
└── Python Libraries: RDFLib \+ OWLReady2  
└── Reasoner: HermiT or Pellet for offline consistency checks  
└── Local Validation: pySHACL  
└── Core Modules: Worker, Equipment, Robot, Sensor, Zone, Task, Risk, Safety, Action, Policy, Capability  
└── Action Registry: ontology-defined Action Types  
└── Interface Registry: Capability and Interface Contracts  
└── Versioning: Git \+ ontology\_version \+ namespace governance  
└── Migration: manual migration first, automated migration later  
└── Compatibility Check: SHACL validation \+ SPARQL regression queries \+ reasoner consistency check

MVP Rule:  
└── Start with a small but strict ontology core  
└── Define Object Types, Link Types, Attribute Types, Event Types, Action Types, Capability Types, and World State Binding first  
└── Use SHACL for practical validation  
└── Use HermiT / Pellet only for offline consistency checks  
└── Do not put full OWL reasoning in the real-time safety path  
└── Do not overbuild the ontology before the first operational scenario is implemented

---

## **Core Ontology Kernel Core Principles**

1. Ontology Is the Semantic Source of Truth  
   └── It defines what objects, relationships, states, actions, capabilities, policies, constraints, and workflows mean.  
2. Meaning Comes Before Automation  
   └── The system must know what an entity or action means before agents, dashboards, policies, or execution requests use it.  
3. Only Defined Action Types Can Enter the Execution Pipeline  
   └── Unknown or unregistered action types must be rejected or sent to ontology governance review.  
4. LLM Output Must Not Create Semantic Truth  
   └── LLMs and agents may propose candidates, but canonical ontology meaning requires governed definitions.  
5. HermiT and Pellet Are Offline Reasoners  
   └── Full OWL reasoning belongs to consistency checks, release validation, static knowledge validation, and batch materialization, not real-time decisions.  
6. Runtime Validation Must Be Bounded  
   └── Runtime checks should use target-specific SHACL, OPA / Rego, rule engines, graph queries, cached views, and current world state checks.  
7. SHACL Is the Practical Runtime Shape Guard  
   └── SHACL validates whether data and candidate structures satisfy required shapes before operational use.  
8. OPA / Rego Handles Operational Policy Evaluation  
   └── Ontology defines policy concepts and constraints; OPA / Rego evaluates practical permission and policy decisions.  
9. World State Must Be Separated from Ontology Meaning  
   └── Ontology defines what WorkerLocation means; Real-Time World State stores where the worker is now.  
10. High-frequency Telemetry Must Not Become Triple Flood  
    └── Sensor ticks, robot telemetry, and worker location updates should update world state cache first and materialize RDF only at meaningful boundaries.  
11. Capability Does Not Equal Permission  
    └── A robot may have a capability, but execution still requires current availability, policy permission, safety validation, and approval when required.  
12. Interface Contracts Define Integration Meaning  
    └── FleetManagerInterface and ExternalControlInterface define expected integration semantics, not low-level physical control implementation.  
13. Policy Concepts and Policy Execution Are Different  
    └── Ontology models policy meaning; Governance and Safety Gate evaluate and enforce operational policy.  
14. Workflow Meaning and Workflow Execution Are Different  
    └── Ontology defines workflow concepts and dependencies; runtime services execute workflow state transitions.  
15. IRIs Must Be Stable and Governed  
    └── Labels may change, but canonical IRIs must remain stable, versioned, and auditable.  
16. Ontology Changes Must Be Reviewed  
    └── Changes to classes, properties, action types, constraints, capabilities, and policies must go through governance and compatibility checks.  
17. Standards Should Clarify, Not Overcomplicate  
    └── BFO, SOSA / SSN, SAREF, PROV-O, QUDT, and GeoSPARQL should be used where they improve meaning, interoperability, provenance, units, or spatial reasoning.  
18. Semantic Memory Must Serve Ontology Core  
    └── Documents, vectors, events, and graph memory must be grounded to ontology definitions before high-risk operational use.  
19. Agents Must Return Ontology-grounded Candidates  
    └── Agent outputs must reference canonical IRIs, defined action types, evidence, confidence, and validation status.  
20. Safety Gate Depends on Ontology Contracts  
    └── Safety Gate validates action candidates using action type definitions, constraints, preconditions, policy decisions, capabilities, approvals, and current state.  
21. Ontology Must Support Human Understanding  
    └── Ontology should be inspectable through ontology explorer, graph explorer, labels, documentation, examples, and governance records.  
22. Modular Ontology Beats One Giant Ontology  
    └── Core, safety, robot, equipment, worker, zone, task, action, policy, provenance, and workflow modules should be separated and versioned.  
23. Formal Semantics Must Remain Practical  
    └── The ontology must be formal enough for validation and reasoning, but practical enough to support construction operations.  
24. Real-time Decisions Must Check Freshness  
    └── If semantic facts are materialized, their freshness must be checked against current world state before operational use.  
25. Ontology Defines the Language of the System  
    └── Every layer should speak through ontology-aligned types, actions, relationships, and state definitions.  
26. The Ontology Kernel Must Not Become a Bottleneck  
    └── Runtime services should use compiled contracts, cached shapes, materialized views, and bounded validation instead of querying or reasoning over the full ontology for every operation.  
27. Evidence Must Be Semantically Linked  
    └── Documents, sensor events, agent outputs, approvals, and execution feedback should be linked to ontology entities and provenance records.  
28. Unknown Entities Must Be Candidate Entities First  
    └── New or ambiguous entities should be quarantined as candidate entities until linked, reviewed, or approved.  
29. Semantic Consistency Must Be Tested  
    └── Ontology releases should run reasoner checks, SHACL validation, SPARQL regression tests, and compatibility checks.  
30. Ontology Controls Meaning, Not Motors  
    └── The ontology system defines operational meaning, constraints, approval context, and execution request semantics; external control systems handle motion, machinery, fleet execution, and device-level behavior.
