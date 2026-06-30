# **Ontology Foundation Report**

# **1\. Purpose**

The LEDO Industrial Ontology Foundation is not an ontology for describing one specific domain. This Foundation is an upper semantic basis for accepting lower-level industrial domains such as construction, manufacturing, plants, logistics, energy, ports, shipbuilding, railways, autonomous driving, guided driving, robotics, humanoids, sensors, control rooms, worker management, equipment management, safety management, and emergency response.

The purpose of this report is to define the semantic structure on which industrial objects, relationships, attributes, states, events, tasks, risks, evidence, policies, approvals, execution, feedback, and audit should be modeled. This Foundation is not a warehouse that directly contains all domain knowledge. Instead, it defines the minimal upper structure, axiom system, relationship design principles, identifier strategy, standards alignment method, SKOS-based vocabulary system, and role separation between reasoning and validation so that all domain knowledge can be safely added later.

If the LEDO Core Specifications are the operational constitution for platform decision-making, approval, execution, and audit, then the LEDO Industrial Ontology Foundation is the ontological constitution for semantically describing the industrial world. The Core Specifications define how the system makes decisions and controls execution. The Ontology Foundation defines what the targets of those decisions and executions are, and what relationships, attributes, and semantic rules those targets have.

The final goal of this Foundation is not merely to build a knowledge graph. The goal is to build a reusable semantic foundation for a world-class industrial Physical AI operating environment. Therefore, this Foundation must consider international standards, identifier strategy, ontology axioms, data validation, time synchronization, safety, security, agent interoperability, and SKOS-based trainability from the beginning. Reworking standards, IRIs, axioms, relationships, and attribute structures later would shake the entire graph, codebase, and domain module system. Therefore, the Foundation must be defined with maximum care at the beginning.

---

# **2\. Position Within the Overall Structure**

In the current LEDO project structure, the Ontology Foundation sits between the Core Specifications and the Domain Ontology Modules.

01\_layer\_architecture/  
02\_layer\_stack\_mapping/  
03\_core\_specifications/  
04\_ontology\_foundation/  
05\_domain\_ontology\_modules/

Layer Architecture defines the overall system layers. Layer Stack Mapping defines which technology stacks are placed in each layer. Core Specifications define the shared constitution for object lifecycle, common DTOs, events, actions, states, evidence, policies, approvals, execution, and audit. The Ontology Foundation defines the semantic system that all of those Core structures reference. Domain Ontology Modules add specific industrial domain classes, relationships, attributes, SKOS terms, and mappings on top of that Foundation.

Therefore, the Ontology Foundation must sit above the domain modules. Domains can be added at any time, but the Foundation must provide the shared semantic structure used by every domain. Construction, robotics, autonomous driving, sensors, control systems, and worker management may all differ as domains, but their definitions, identifiers, relationships, attributes, axioms, constraints, reasoning, graph structure, context, and governance principles must follow the same Foundation.

---

# **3\. Core Philosophy of the Foundation**

The core philosophy of the LEDO Industrial Ontology Foundation is “small but strong upper structure.” If every domain is directly inserted into the Foundation, the Foundation becomes bloated and turns into a bottleneck. If the Foundation is too weak, each domain module will create objects and relationships in its own way, and the entire system will lose consistency. Therefore, the Foundation should not directly contain many domain-specific details. It should contain the upper semantic rules that every domain must follow.

The major pillars required by this Foundation are:

Definition  
Identity  
Relation  
Attribute  
Axiom  
Constraint  
Inference  
Graph  
Context  
Governance

Definition creates concepts. Identity fixes targets. Relation connects concepts. Attribute assigns values and states. Axiom fixes meaning. Constraint validates data quality. Inference derives hidden meaning. Graph creates the full connection structure. Context allows the same relationship to be interpreted differently depending on the situation. Governance controls the long-term evolution of the ontology.

Among these, the most important pillar is the axiom. If there are only class names, the result is a vocabulary list. If there are only relationships, the result is a graph. If there are only attributes, the result is a schema. Only when axioms exist does it become an ontology. Axioms are logical statements that assign semantic meaning to definitions, relationships, and attributes. Therefore, the center of the LEDO Foundation must be the OWL Axiom System.

---

# **4\. Single `ot:` Namespace Strategy**

The LEDO Industrial Ontology Foundation uses a single primary namespace. The default prefix is `ot:`.

ot:  
→ the default namespace prefix of the LEDO Industrial Ontology

The reason for using a single namespace is to keep the entire Foundation inside one semantic world. Splitting prefixes Single `ot:` Namespace Strategy

The LEDO Industrial Ontology Foundation uses a single primary namespace. The default prefix is `ot:`.

ot:  
→ the default namespace prefix of the LEDO Industrial Ontology

The reason for using a single namespace is carelessly by domain may look convenient at first, but over time it can create concept duplication, relationship duplication, mapping conflicts, SKOS label duplication, and external system identifier conflicts. Therefore, the official TBox of the Foundation is controlled around `ot:`.

However, TBox and ABox are designed differently. The TBox contains structures that humans must read and govern, such as classes, properties, axioms, schemas, and vocabulary systems. Therefore, TBox IRIs follow a controlled vertical structure that humans can understand.

ot:Agent  
ot:RobotAgent  
ot:Sensor  
ot:Observation  
ot:Risk  
ot:WorkZone  
ot:DangerZone  
ot:Permit  
ot:Evidence  
ot:Action  
ot:Policy  
ot:ExecutionRequest

The ABox, on the other hand, contains real-world field individuals. Real-world individuals may have different IDs across external systems, different names across sites, and labels that change over time. Therefore, the IRI of an ABox real-world individual should not depend on human-assigned names. It should use a 128-bit hash-based composite structure.

ot:abox/\<128bit\_hash\>

The ABox hash should be generated by combining the following elements:

namespace\_version  
source\_system\_id  
source\_object\_id  
canonical\_object\_type  
site\_or\_org\_scope  
optional\_external\_identifier

This strategy satisfies two goals at the same time. First, the TBox remains a controlled structure that humans can read and review. Second, the ABox can stably identify real-world individuals in large-scale industrial sites. This structure also connects directly to the Canonical Object Lifecycle. A real-world field object is first resolved into a canonical identity, and the result is fixed as a 128-bit hash-based ABox IRI.

The core principles are:

TBox uses controlled readable ot: IRIs.  
ABox uses 128-bit hash-based real-world object IRIs.  
ABox identity must not depend on mutable human labels.  
Every external identifier must be mapped, not blindly trusted.  
Canonical identity precedes ontology binding.

---

# **5\. Identity Resolution Flow**

Identity Resolution is the process of converting an object ID from an external system into a stable ABox individual inside the ontology. In industrial systems, the same real-world object may exist under different names and IDs in multiple systems. Without this flow, duplicate individuals will explode as the graph grows.

The recommended flow is:

External ID  
→ Source System Identifier  
→ Identifier Mapping Record  
→ Identity Resolution Evidence  
→ Canonical Identity  
→ 128-bit ABox Hash IRI  
→ Ontology Binding

Each stage means the following:

External ID  
→ the original ID assigned by an external system

Source System Identifier  
→ the system or data source from which the ID came

Identifier Mapping Record  
→ a record connecting the external ID to an internal candidate object

Identity Resolution Evidence  
→ evidence used to decide that objects refer to the same target

Canonical Identity  
→ the single object identity confirmed inside the platform

128-bit ABox Hash IRI  
→ the stable real-world individual IRI used in the ontology graph

Ontology Binding  
→ the assertion that connects the real-world individual to a TBox class

For example, one humanoid may enter the system with different IDs from Robot Middleware, a work management system, and a control dashboard. In this case, directly connecting external IDs with `owl:sameAs` is dangerous. A mapping record and evidence must be created first, the canonical identity must be confirmed, and only then should the ABox hash IRI be generated.

The core principles are:

External IDs are evidence, not truth.  
Canonical identity must be resolved before ontology binding.  
Strong sameAs assertions require governance.  
ABox hash IRI must remain stable even if human-readable labels change.

---

# **6\. Definition Layer**

The Definition Layer defines the concepts of the industrial world. The important point here is that not every domain-specific class should be inserted into the Foundation. The Foundation should contain only the minimal upper concepts required to wrap lower-level domains.

The basic definition categories of the Foundation should be approximately:

Entity  
Agent  
HumanAgent  
MachineAgent  
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
Risk  
Zone  
Policy  
Permit  
Action  
Feedback  
AuditRecord

These categories are not locked to one industry. Humanoids, industrial machines, autonomous vehicles, guided vehicles, sensors, control systems, workers, equipment, access control, and environmental risks can all extend from these upper categories.

The purpose of the Definition Layer is not to create many domain-specific details. Its purpose is to provide criteria for where lower-domain concepts should attach. For example, an object that can generate action candidates or participate in tasks may be placed under the Agent family. An object that physically exists and has location may be placed under the PhysicalObject family. A device that observes a state may be placed under the Sensor family. Equipment that performs work or is controlled may be specialized under Machine or Robot.

Definitions must include `skos:definition`, `rdfs:label`, `rdfs:comment`, and, when necessary, both Korean and English labels. This is important not only for human understanding, but also for future SLM training, search, mapping, and documentation automation.

---

# **7\. Identity Layer**

The Identity Layer fixes the same target as one object. One of the largest bottlenecks in industrial systems is object duplication. The same humanoid may have one ID in a Fleet Manager, another name in a control system, and another asset number in a field work management system. The same sensor may also enter through PLC, SCADA, IoT Gateway, and RDF graph under different names.

Therefore, the Foundation must treat identity not as a simple string, but as a structured concept.

The Identity Layer includes the following concepts:

CanonicalIdentity  
ExternalIdentifier  
SourceSystemIdentifier  
DeviceIdentifier  
AssetIdentifier  
AgentIdentifier  
LocationIdentifier  
HashBasedIRI  
IdentifierMappingRecord  
IdentityResolutionEvidence

`owl:sameAs` has very strong semantics and must not be overused. Equality can have a strong inference impact across the entire system. Therefore, when merging real-world objects in the ABox, the system should first use internal references such as `canonical_identity_ref`, `identifier_mapping_ref`, and `identity_resolution_evidence_ref`, and allow strong equality assertions only when they are verified and governed.

The core principles are:

Names are not identity.  
External IDs are not automatically canonical.  
Canonical identity must be evidence-backed.  
Strong identity assertions require governance.  
ABox hash IRI must be stable across system boundaries.

---

# **8\. Relation Layer**

The Relation Layer connects concepts and individuals. Relationships are central to ontology, but if too many relationships are created, the Foundation becomes a bottleneck. If too few relationships are created, everything becomes an ambiguous link. Therefore, the Foundation should provide a small but strong set of upper relationships, and lower domains should extend them when necessary.

Recommended upper relationship categories are:

isPartOf  
locatedIn  
participatesIn  
performs  
uses  
observes  
controls  
affects  
requires  
authorizes  
generates  
supports  
causes  
mitigates  
restricts  
reportsTo  
communicatesWith

These relationships can be applied to most industrial domains. For example, a RobotAgent can perform a Task, a Sensor can observe an ObservableCondition, an AccessControlSystem can restrict ZoneAccess, and a Permit can authorize a HighRiskTask. A ControlSystem can control an IndustrialMachine, an Observation can support Evidence, and an Event can cause a StateChange.

The key principle in relationship design is not to create domain-specific relationships endlessly. First, check whether the meaning can be expressed using an upper relationship from the Foundation. Only when that is insufficient should a lower-level relationship be created.

controls  
  └── remotelyControls  
  └── automaticallyControls  
  └── manuallyControls  
  └── supervisesControl  
  └── requestsControl

observes  
  └── observesPosition  
  └── observesGasLevel  
  └── observesTemperature

restricts  
  └── restrictsZoneAccess  
  └── restrictsTaskExecution

`ot:controls` must be designed especially carefully. `controls` may mean a direct physical command, a supervisory control request, or an approved control intention. Therefore, the Foundation should not interpret `controls` too strongly. Its meaning should be separated through lower-level relationships.

ot:controls  
→ broad control relationship

ot:requestsControl  
→ platform or agent requests a control action

ot:supervisesControl  
→ control system supervises another system

ot:automaticallyControls  
→ automated control relationship

ot:manuallyControls  
→ human-mediated control relationship

ot:remotelyControls  
→ remote control relationship

Every relationship must be reviewed for Domain, Range, Inverse, and Property Characteristics. Adding relationship names alone is not ontology design. The subject, object, inverse relationship, transitivity, and functionality of a relationship must all be reviewed.

---

# **9\. Attribute Layer**

The Attribute Layer represents the values and states of individuals. Attributes are important because they connect the ontology to the real world, but if too many attributes are inserted into the Foundation, the Foundation becomes a bottleneck. Therefore, attributes must be divided into common attributes, state attributes, and domain attributes.

Common attributes are shared by most objects.

identifier  
label  
source  
created\_at  
updated\_at  
version  
lifecycle\_status  
confidence  
provenance\_ref

State attributes change over time.

location  
operational\_status  
connectivity\_status  
health\_status  
risk\_level  
task\_status  
battery\_level  
mode

Domain attributes are defined in lower domain modules.

gas\_concentration  
tool\_grip\_force  
joint\_temperature  
vehicle\_speed  
machine\_load  
zone\_occupancy\_count

The Foundation does not directly contain every domain attribute. Instead, the Foundation defines the types of attributes and the criteria for designing them. It provides criteria for deciding whether an attribute should be a DataProperty, whether it should be separated into State, whether it should be represented as an Observation, and whether it should be connected to Evidence.

The important principles are:

Stable attributes belong to object description.  
Dynamic attributes belong to state or observation.  
Evidence-backed attributes must reference evidence.  
Raw sensor values should not all become semantic attributes.  
Domain-specific attributes belong to domain modules.

---

# **10\. OWL Axiom System**

The OWL Axiom System is the center of this Foundation. Axioms are the logical sentences of an ontology. Classes, relationships, and attributes are materials; axioms turn those materials into a meaningful system.

Axioms are divided into the following types:

Class Axioms  
Property Axioms  
Individual Axioms  
Equivalence Axioms  
Disjointness Axioms  
Domain and Range Axioms  
Inverse Property Axioms  
Property Characteristic Axioms  
Restriction Axioms  
Cardinality Axioms

Class Axioms define semantic relationships between classes.

HumanoidRobot SubClassOf RobotAgent.  
GasSensor SubClassOf Sensor.  
DangerZone DisjointWith SafeZone.

Property Axioms define the meaning of relationships themselves.

observes Domain Sensor.  
observes Range ObservableCondition.  
performs Domain Agent.  
performs Range Task.  
requiresPermit Domain HighRiskTask.  
requiresPermit Range Permit.

Individual Axioms assert facts about real-world individuals.

HumanoidRobot\_01 Type HumanoidRobot.  
GasSensor\_17 Type GasSensor.  
HumanoidRobot\_01 isLocatedIn Zone\_A.  
GasSensor\_17 observes GasConcentration\_Zone\_A.

Restriction Axioms define semantic conditions that a class must satisfy.

HighRiskTask SubClassOf requiresPermit some Permit.  
SensorObservation SubClassOf generatedBy some Sensor.  
RobotInspectionTask SubClassOf performedBy some RobotAgent.

Cardinality Axioms express minimum, maximum, or exact numbers of connections. However, Cardinality must be understood together with the Open World Assumption. Even if OWL declares that at least one Permit is required, missing Permit data does not immediately become an error. OWL assumes that an unknown Permit may still exist. Therefore, pre-execution validation must be handled by SHACL and Safety Gate.

The core principles for axiom design are:

Axioms must be intentional, not decorative.  
Every strong axiom must have a reason.  
Disjointness must be used carefully.  
Transitivity must be rare and controlled.  
Domain and range must not over-constrain early.  
Runtime safety must not depend only on OWL reasoning.

---

# **11\. Constraint Layer**

The Constraint Layer checks whether data satisfies rules. OWL and SHACL must be separated here.

OWL declares meaning and creates reasoning. SHACL validates whether data satisfies conditions. Policy Engine determines operational permission and prohibition. Safety Gate validates safety conditions immediately before execution.

OWL  
→ semantic meaning and reasoning

SHACL  
→ data validation and shape checking

Policy Engine  
→ operational permission and prohibition

Safety Gate  
→ pre-execution safety validation

For example, OWL can declare `HighRiskTask SubClassOf requiresPermit some Permit`. This creates the semantic condition that a high-risk task should be connected to a Permit. However, checking whether actual data is missing a Permit is the role of SHACL. Deciding whether that task may be executed is the role of Policy Governance and Safety Gate.

The actual runtime validation sequence should be separated as follows.

Input Data  
→ SHACL Validation  
→ Ontology Binding  
→ State / Evidence Update  
→ Policy Evaluation  
→ Decision / Approval  
→ Safety Gate Validation  
→ Execution Adapter Request  
→ Feedback / Audit

Each stage has a different responsibility. SHACL checks input data structure, required fields, and value ranges. Ontology Binding checks which individual and class the data connects to. State/Evidence Update updates current world state and decision evidence. Policy Evaluation decides permission and prohibition. Decision/Approval confirms the route and authority. Safety Gate rechecks conditions immediately before execution. Execution Adapter only sends a request to an external system.

Constraint Layer includes the following validation types:

required property validation  
datatype validation  
value range validation  
cardinality validation  
class membership validation  
target shape validation  
cross-reference validation  
evidence reference validation  
state freshness validation

SHACL is especially important for maintaining ABox data quality. Sensor data, work permits, risk states, robot states, zone access states, and control feedback should pass SHACL validation when entering the RDF graph.

---

# **12\. Inference Layer**

The Inference Layer derives meaning that was not explicitly entered. Reasoning derives new facts from axioms, relationships, and attributes.

Inference is divided into the following types:

class inference  
property inference  
identity inference  
relation inference  
state inference  
risk inference  
context inference  
evidence inference

For example, if a RobotAgent performs a GasInspectionTask, and GasInspectionTask is a subclass of HighRiskTask, then the system can infer that the task is high-risk. If GasRisk is active in a Zone, and an Agent is located in that Zone, the system can infer that the Agent may be exposed to risk.

However, inference in industrial Physical AI must be handled carefully. Offline OWL reasoners are powerful for ontology consistency checking, class classification, and relationship reasoning. But runtime safety paths must not depend entirely on OWL reasoners. At runtime, SHACL, Policy Engine, Safety Gate, rules, cached state, and graph queries must work together.

The core principles are:

Reasoning expands meaning.  
Validation checks data quality.  
Policy decides permission.  
Safety Gate validates execution eligibility.  
Runtime safety must remain deterministic.

---

# **13\. Graph Layer**

The Graph Layer is the structure where definitions, relationships, attributes, axioms, and inference results are connected. An RDF graph is the representation form of the ontology, but the graph itself is not the goal. The graph must be a semantic connection network.

The Graph Layer must be divided into three types.

Semantic Graph  
Runtime Graph  
Evidence Graph

The Semantic Graph contains the TBox, axioms, classes, relationships, and SKOS terms. The Runtime Graph contains current states and recent semantic events. The Evidence Graph connects decision evidence, sources, evidence bundles, and audit records.

Not every raw sensor stream should be inserted into the RDF graph. Doing so creates a graph bottleneck. Raw streams should be processed in a time-series store or stream processing layer, and only meaningful events, verified states, and evidence-backed decisions should be promoted into the graph.

Raw stream  
→ time-series or stream store

Meaningful event  
→ Event Graph

Verified state  
→ Runtime Graph

Evidence-backed decision  
→ Evidence and Audit Graph

This principle prevents the graph from becoming a dumping ground for operational data.

---

# **14\. Context Layer**

The Context Layer allows the same relationship or state to be interpreted differently depending on the situation. In industrial systems, simple relationships are not enough. The same `locatedIn` relationship can mean different things depending on whether the target is working, waiting, in an emergency situation, under control approval, or inside a risk state.

Therefore, the Foundation must explicitly model Context.

OperationalContext  
SafetyContext  
ExecutionContext  
ObservationContext  
PolicyContext  
TemporalContext  
SpatialContext  
HumanRobotCollaborationContext  
ControlContext

For example, the fact that a HumanoidRobot is located in Zone\_A may not be dangerous by itself. However, if Zone\_A has an active gas risk, the RobotAgent is performing an inspection task, and its communication status is degraded, then the same locatedIn relationship becomes much more meaningful.

HumanoidRobot\_01 locatedIn Zone\_A.  
Zone\_A hasActiveRisk GasRisk\_01.  
HumanoidRobot\_01 performs InspectionTask\_09.  
HumanoidRobot\_01 hasConnectivityStatus DEGRADED.

In this situation, a SafetyContext may be created that means “inspection task under risk exposure with degraded communication,” not merely a location relationship. This Context must connect to Policy Evaluation, Safety Gate, and Audit Observability.

The Context Layer allows situational meaning to be represented without exploding the number of relationships. Instead of creating endless relationships, the Foundation adjusts meaning through Context. This is an important strategy for avoiding Foundation bottlenecks.

---

# **15\. Causality and Multi-Cause Scenario**

Causality is the causal system that connects Event, State, Evidence, Risk, Action, and Audit. One incident does not always have only one cause. In industrial environments, multiple sensors, states, and system conditions often combine to produce one risk decision or emergency action.

The recommended structure is:

primary\_causality\_id  
causality\_ids  
causality\_role  
causality\_direction

Example:

GasSensor\_01 reports critical gas concentration.  
HumanoidRobot\_01 is located in Zone\_A.  
VentilationSystem\_02 is degraded.  
CommunicationLink\_07 is degraded.

In this situation, a single cause is not enough. The gas sensor threshold violation, the humanoid’s location, the degraded ventilation system, and degraded communication together create the meaning.

causality\_ids:  
  \- gas critical reading  
  \- robot located in affected zone  
  \- ventilation degraded  
  \- communication degraded

result:  
  \- Emergency Policy Evaluation  
  \- Safety Gate Revalidation  
  \- Access Restriction  
  \- Human Supervisor Notification  
  \- Post-Hoc Audit

This structure directly connects to the Audit Observability Model. An AuditRecord should be able to reference `causality_ids`, not just a single `causality_id`. This allows post-hoc analysis to reconstruct not “one cause created the result,” but “a combination of conditions created the result.”

---

# **16\. SKOS Lexical Foundation for SLM**

The SKOS Lexical Foundation is the basis for future SLM training, search, terminology alignment, multilingual labels, and domain description generation. OWL handles strict reasoning and axioms, but SLMs cannot learn sufficiently from axioms alone. SLMs need linguistic structures such as terms, definitions, synonyms, explanations, examples, scope notes, and hidden labels.

In one sentence:

OWL defines formal meaning; SKOS organizes language around that meaning.

Therefore, the Foundation must include sufficient SKOS entries.

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

Foundation SKOS has the following purposes:

human-readable ontology documentation  
SLM training support  
semantic search support  
term normalization  
multilingual label management  
domain vocabulary alignment  
mapping between field language and ontology terms

However, the Foundation does not automatically create actual domain training text. Domain experts must provide that text directly. The Foundation provides the structure that can contain it. In other words, SKOS is the vessel for SLM learning, and the actual content is filled by people with domain experience and field language.

SKOS Concept Schemes may be divided as follows:

AgentConceptScheme  
MachineConceptScheme  
RobotConceptScheme  
SensorConceptScheme  
TaskConceptScheme  
RiskConceptScheme  
ZoneConceptScheme  
PolicyConceptScheme  
EvidenceConceptScheme  
ControlSystemConceptScheme

SKOS and OWL are different. An OWL Class is a strict logical class, while a SKOS Concept is for terminology and conceptual organization. Therefore, not every SKOS Concept should be automatically converted into an OWL Class. Only important concepts should be connected to OWL Classes, while the rest should remain in the vocabulary system.

The core principles are:

OWL is for formal semantics.  
SKOS is for lexical and conceptual organization.  
SLM training text belongs to SKOS-oriented documentation, not core axioms.  
Domain expert text must remain distinguishable from formal ontology axioms.

---

# **17\. Standards Alignment Matrix**

An export-grade industrial Physical AI ontology cannot exist without alignment to international standards. Standards are not decorative references. They are the basis for interoperability, safety, security, certification readiness, and technology exportability.

Standards should be managed in the Foundation using the following structure:

StandardFamily  
StandardReference  
MappedOntologyArea  
MappedCoreSpec  
ComplianceRole  
ImplementationImpact  
ReviewRequired

LEDO uses the following three application levels.

MUST  
→ a requirement that must be reflected in Foundation design

SHOULD  
→ strongly recommended and should be prioritized in industrial application

MAY  
→ optional depending on domain, customer, region, or certification scope

The standards alignment matrix is defined as follows.

| Standard Family | LEDO Application Level | Role in the Foundation |
| ----- | ----- | ----- |
| W3C RDF / RDFS | MUST | RDF graph, triple model, basic class/property structure |
| W3C OWL 2 | MUST | formal ontology, class/property/individual axiom, reasoning |
| W3C SPARQL | MUST | graph query, semantic retrieval, audit/evidence query |
| W3C SHACL | MUST | ABox data validation, shape constraint |
| W3C SKOS | MUST | vocabulary system, SLM training structure, multilingual labels |
| W3C PROV-O | SHOULD | provenance, evidence lineage, source tracking |
| W3C OWL-Time | SHOULD | time concepts, temporal relations, event timing |
| OGC GeoSPARQL | SHOULD | space, zone, location, geometry query |
| ISO/IEC 21838 / BFO | MUST | upper ontology, category discipline |
| IFC / BIM / ISO 16739 | SHOULD | external industrial asset alignment, BIM mapping |
| IEC 61508 | SHOULD | functional safety, safety lifecycle, SIL alignment |
| IEC 61511 | SHOULD | process safety, safety instrumented system alignment |
| IEC 62541 / OPC UA | SHOULD | industrial communication, telemetry, external system model |
| IEC 62264 / ISA-95 | SHOULD | enterprise-control integration boundary |
| ISA/IEC 62443 | MUST | industrial cybersecurity, OT/ICS security boundary |
| IEEE 1588 | MUST | time synchronization, clock trust, timestamp reliability |
| ISO 10218 / ISO robotics safety family | SHOULD | robot safety reference |
| ISO 8373 | MAY | robotics vocabulary reference |
| NIST SP 800-53 | SHOULD | security and privacy control reference |
| NIST AI RMF | SHOULD | AI risk governance reference |
| RFC 2119 / RFC 8174 | MUST | MUST/SHOULD/MAY requirement language |
| FIPA ACL | MAY | agent communication reference |

This does not mean that all of these standards are directly implemented. The Foundation identifies which design area each standard influences. For example, IEEE 1588 affects time synchronization and fields such as `time_trust_level`, `clock_sync_status`, and `clock_drift_estimate_ms`. IEC 61508 and IEC 61511 affect Safety Gate, Risk, Fail-safe, Emergency Policy, and Safety Instrumented System models. OPC UA affects adapters, telemetry, feedback, and control boundaries with external industrial systems. NIST SP 800-53 and IEC 62443 affect security policy, access control, audit, zero-trust, and OT security design.

---

# **18\. Upper Ontology and BFO Mapping**

BFO is used as the upper ontological reference in the Foundation. Using BFO does not mean mechanically forcing every domain class into BFO terms. Its purpose is to provide an upper ontological discipline so that lower domains do not create concepts based on incompatible philosophies.

In the Foundation, BFO is used to support the following distinctions:

continuant vs occurrent  
material entity  
process  
role  
function  
disposition  
site  
temporal region  
quality

Example mappings are as follows.

| LEDO Concept | BFO-oriented category | Description |
| ----- | ----- | ----- |
| HumanoidRobot | material entity / object | A physically persistent robot individual |
| GasSensor | material entity / device-like object | A physical sensor with an observation function |
| InspectionTask | process / planned process | A task process performed over time |
| HighRiskTask | process with risk context | A task process with risk conditions attached |
| WorkerRole | role | A role performed by a human in a specific context |
| RobotOperatorRole | role | An operation role assigned to a robot or control system |
| GasRisk | disposition / risk context | A risk potential or risk-state context |
| DangerZone | site / spatial region | A spatial region connected to risk |
| SafetyPolicy | generically dependent continuant / information artifact | A policy information object |
| SensorObservation | process or information content entity depending on modeling choice | An observation act or observation result information |

The core principles for BFO Mapping are:

Use BFO to avoid category confusion.  
Do not overload domain classes with upper ontology meaning.  
Keep BFO mapping explicit and reviewable.  
Use BFO for alignment, not for domain bloat.

---

# **19\. External Industrial Model Alignment**

The Foundation does not replace external industrial models. IFC, BIM, OPC UA Information Model, PLC tag model, SCADA model, MES model, robotics vocabulary, and sensor models may all exist as external models. The LEDO Foundation does not directly copy them. Instead, it connects them through a Mapping Layer.

The basic structure for external model alignment is:

External Model  
→ Mapping Module  
→ Canonical Object  
→ Ontology Binding  
→ Evidence / State / Action / Audit

This structure is important because it prevents the Foundation itself from being shaken when external standards or field systems change. The Foundation does not absorb every detail of an external model. It provides the criteria for connecting external models to canonical objects and ontology classes.

The core principles are:

External standards are aligned, not blindly copied.  
Mapping modules absorb external schema changes.  
Canonical identity must sit between external IDs and ontology individuals.  
Domain modules must not directly depend on one vendor-specific schema.

---

# **20\. Governance Layer**

Ontology Governance determines the long-term survival of the Foundation. Ontology is not code that is written once and finished. As domains are added, standards change, field data grows, and new robots, equipment, and sensors enter the system, the ontology must evolve as well.

The Governance Layer includes:

versioning  
deprecation  
migration  
mapping review  
axiom review  
property review  
SKOS term review  
standard alignment review  
module boundary review  
reasoner consistency check  
SHACL validation test  
competency question test

Axiom changes must be governed strictly. Adding a class may be relatively safe. However, changing domain/range, disjointness, transitive properties, inverse properties, or cardinality restrictions can change the entire inference result. Therefore, strong axiom changes must be reviewed.

---

## **20.1 Axiom Change Impact Assessment**

Axiom Change Impact Assessment is central to ontology governance. A single axiom can change the inference result of the entire graph, so the impact must be evaluated both quantitatively and qualitatively before and after the change.

The evaluation criteria are:

affected\_class\_count  
affected\_property\_count  
affected\_individual\_count  
changed\_inference\_count  
new\_inconsistency\_count  
new\_unsatisfiable\_class\_count  
changed\_SHACL\_result\_count  
changed\_competency\_question\_result\_count  
affected\_domain\_modules  
runtime\_safety\_impact

Risk level by change type:

| Change Type | Impact | Review Level |
| ----- | ----- | ----- |
| Add rdfs:label | Low | lightweight review |
| Add skos:altLabel | Low | lightweight review |
| Add new subclass | Medium | ontology review |
| Add new relation | Medium | property review |
| Change domain/range | High | axiom review required |
| Add disjointness | High | reasoner test required |
| Add transitive property | Very high | strict review required |
| Change inverse property | High | inference regression test required |
| Change cardinality restriction | High | SHACL and reasoning test required |
| Change sameAs policy | Very high | identity governance review required |

Before and after an axiom change, at least the following tests must be performed:

reasoner consistency check  
unsatisfiable class check  
sample ABox inference comparison  
SHACL regression test  
competency question regression test  
module dependency check  
runtime safety impact review

Governance principles are:

Axioms require review.  
Strong property changes require regression tests.  
SKOS terms require curation.  
Mappings require versioning.  
Deprecated terms must not disappear silently.  
Breaking changes must be explicitly marked.  
Every ontology release must be testable.

---

# **21\. Quality, Testing, and Evaluation**

The Ontology Foundation must have quality testing criteria. It is not enough for an ontology to look good in documentation. It must be tested with reasoners, SHACL, SPARQL queries, and domain scenarios.

Quality criteria include:

consistency  
satisfiability  
classification correctness  
property hierarchy correctness  
domain/range sanity  
disjointness safety  
SHACL validation pass rate  
competency question coverage  
SPARQL query usability  
SKOS label completeness  
mapping stability  
module dependency cleanliness  
runtime usability

Competency Questions are especially important. The questions that the ontology must answer should be defined first, and then the ontology should be tested against them.

Example questions:

Which agents are currently located in a danger zone?  
Which tasks require a permit?  
Which observations support a high-risk decision?  
Which sensors generated evidence for a gas risk event?  
Which external systems received an execution request?  
Which robot agents are assigned to inspection tasks?  
Which zones are restricted by access control policy?

If the ontology cannot answer these questions, then even if many classes and relationships exist, it is insufficient as a practical industrial ontology.

---

# **22\. Anti-patterns**

The design errors that the Foundation must avoid are clear.

| Anti-pattern | Reason | Possible Problem | Impact Scale |
| ----- | ----- | ----- | ----- |
| Inserting too many domain-specific classes into the Foundation | The Foundation becomes dependent on a specific domain | Conflicts increase when new domains are added | High |
| Creating properties carelessly for every domain | Relationship systems become duplicated | Query, reasoning, and mapping complexity increase | High |
| Setting domain/range too narrowly | Early design blocks future domains | Ontology conflicts when external domains are extended | High |
| Overusing transitive properties | Inference scope explodes | Incorrect relationship inference and performance degradation | Very high |
| Replacing runtime validation with OWL | Open World Assumption and execution validation have different purposes | Missing data may lead to dangerous execution | Very high |
| Storing all raw sensor data in RDF graph | The graph becomes an operational data store | Graph write/read bottleneck | Very high |
| Confusing SKOS and OWL | Vocabulary system and formal meaning become mixed | SLM training text and formal axioms become mixed | Medium |
| Directly using AI/SLM output as Evidence | AI output is not verified fact | Invalid decision basis and audit failure | Very high |
| Overusing sameAs | Equality inference is too strong | Incorrect object merging and data contamination | Very high |
| Aligning standards after the fact | The structure must be redesigned later | Export, certification, and integration costs explode | Very high |

The core idea is simple. The Foundation is not a place that directly contains everything. It is the standard layer that allows everything to be added correctly.

---

# **23\. LEDO Industrial Ontology Application Strategy**

The LEDO Industrial Ontology Foundation is the standard for sequentially extending lower-level domains. Lower-level domains can be added at any time. The important rule is that every lower-level domain must follow the same Foundation.

A lower-level domain module is added through the following process:

Domain concept  
→ Foundation category mapping  
→ TBox class extension  
→ property alignment  
→ axiom review  
→ SHACL shape design  
→ SKOS concept registration  
→ mapping module connection  
→ competency question test

For example, when a new autonomous driving domain is added, the first step is to determine whether AutonomousVehicle should be placed under Agent, Machine, PhysicalObject, ControlledSystem, or a combination of them. Then, its movement state, location, route, control command, sensor observation, risk state, and execution request relationships are connected using Foundation relations and properties. Domain-specific lower relationships and attributes are created only when necessary. Finally, SKOS terms, SHACL validation, SPARQL queries, and Competency Questions are added.

The humanoid domain enters in the same way. HumanoidRobot may simultaneously have the characteristics of RobotAgent, PhysicalObject, SensorPlatform, and ExecutionTarget. However, this complexity should not be pushed directly into the Foundation. The Foundation provides upper concepts such as Agent, PhysicalObject, Sensor, Task, Risk, Evidence, Action, and ExecutionTarget, and the Humanoid domain module combines them to create the detailed model.

This strategy allows all domains to be wrapped while avoiding bottlenecks. The Foundation must be small but strong. Domain Modules must be large and freely extensible, but governed. Mapping Modules must absorb changes in external standards and field systems. SKOS must support human language and SLM training. OWL Axioms must fix meaning. SHACL must validate data quality. SPARQL must explore the graph. Governance must control all changes.

The final principles are:

Foundation must be small but strong.  
Domains must be extensible but governed.  
Axioms must be central.  
IRI strategy must be stable from the beginning.  
TBox must be readable and controlled.  
ABox must be hash-based and scalable.  
SKOS must support SLM training and semantic search.  
International standards must guide export-grade design.  
OWL, SHACL, SPARQL, Policy, and Safety Gate must have separate roles.  
The graph must contain meaning, not every raw signal.  
Axiom changes must be impact-assessed.

The LEDO Industrial Ontology Foundation is not merely an ontology explanation document. It is the semantic foundation that allows industrial Physical AI to be explainable, extensible, standards-aligned, and safely operable in the global market. If this Foundation is solid, the system will not collapse no matter how many lower-level domains are added.

# **Ontology Industrial Foundation Report**

# **1\. 목적**

LEDO Industrial Ontology Foundation은 특정 도메인 하나를 설명하기 위한 온톨로지가 아니다. 이 Foundation은 건설, 제조, 플랜트, 물류, 에너지, 항만, 조선, 철도, 자율주행, 지정주행, 로봇, 휴머노이드, 센서, 관제, 작업자 관리, 설비관리, 안전관리, 비상대응 등 하위 산업 도메인을 모두 수용하기 위한 상위 의미 기반이다.

이 보고서의 목적은 산업 세계의 객체, 관계, 속성, 상태, 사건, 작업, 위험, 증거, 정책, 승인, 실행, 피드백, 감사가 어떤 의미 구조 위에서 정의되어야 하는지 기준을 정하는 것이다. 이 Foundation은 모든 도메인 지식을 직접 담는 창고가 아니다. 오히려 모든 도메인 지식이 들어올 수 있는 최소 상위 구조, 공리 체계, 관계 설계 원칙, 식별자 체계, 표준 정렬 방식, SKOS 기반 용어 체계, 추론과 검증의 역할 분리를 정의한다.

LEDO Core Specifications가 플랫폼의 판단, 승인, 실행, 감사 헌법이라면, LEDO Industrial Ontology Foundation은 산업 세계를 의미적으로 설명하기 위한 존재론적 헌법이다. Core Specifications는 “시스템이 어떻게 판단하고 실행을 통제하는가”를 정의하고, Ontology Foundation은 “그 판단과 실행의 대상이 무엇이며, 그 대상들이 어떤 관계와 속성과 의미 규칙을 갖는가”를 정의한다.

이 Foundation의 최종 목표는 단순한 지식그래프 구축이 아니다. 목표는 세계적인 산업 피지컬 AI 운영 환경에서 재사용 가능한 의미 기반을 만드는 것이다. 따라서 이 Foundation은 처음부터 국제 표준, 식별자 전략, 온톨로지 공리, 데이터 검증, 시간 동기화, 안전성, 보안성, 에이전트 상호운용성, SKOS 기반 학습 가능성을 함께 고려해야 한다. 나중에 표준, IRI, 공리, 관계, 속성 체계를 다시 바꾸는 것은 전체 그래프와 코드와 도메인 모듈을 흔들 수 있으므로, Foundation 단계에서 최대한 신중하게 기준을 세워야 한다.

---

# **2\. 전체 구조 안에서의 위치**

LEDO 프로젝트의 현재 구조에서 Ontology Foundation은 Core Specifications와 Domain Ontology Modules 사이에 위치한다.

01\_layer\_architecture/  
02\_layer\_stack\_mapping/  
03\_core\_specifications/  
04\_ontology\_foundation/  
05\_domain\_ontology\_modules/

Layer Architecture는 전체 시스템의 층 구조를 정의한다. Layer Stack Mapping은 각 층에 어떤 기술스택이 배치되는지 정의한다. Core Specifications는 객체 생애주기, 공통 DTO, 이벤트, 행동, 상태, 증거, 정책, 승인, 실행, 감사의 공통 헌법을 정의한다. Ontology Foundation은 이 모든 Core 구조가 참조할 의미 체계를 정의한다. Domain Ontology Modules는 그 Foundation 위에 개별 산업 도메인의 클래스, 관계, 속성, SKOS 용어, 매핑을 추가한다.

따라서 Ontology Foundation은 도메인 모듈보다 상위에 있어야 한다. 도메인은 언제든 추가될 수 있지만, Foundation은 모든 도메인이 공유하는 의미 구조를 제공해야 한다. 건설 도메인, 로봇 도메인, 자율주행 도메인, 센서 도메인, 관제 도메인, 작업자 관리 도메인은 모두 다를 수 있지만, 이들이 사용하는 정의, 식별자, 관계, 속성, 공리, 제약, 추론, 그래프, 맥락, 거버넌스 원칙은 동일한 Foundation을 따라야 한다.

---

# **3\. Foundation의 핵심 철학**

LEDO Industrial Ontology Foundation의 핵심 철학은 “작지만 강한 상위 구조”다. 모든 도메인을 Foundation에 직접 넣으려 하면 Foundation은 비대해지고 병목이 된다. 반대로 Foundation이 너무 빈약하면 도메인 모듈마다 다른 방식으로 객체와 관계를 만들게 되어 전체 시스템의 일관성이 무너진다. 따라서 Foundation은 도메인 세부사항을 직접 많이 담지 않고, 모든 도메인이 따라야 할 상위 의미 규칙을 담아야 한다.

이 Foundation이 반드시 가져야 할 큰 축은 다음과 같다.

Definition  
Identity  
Relation  
Attribute  
Axiom  
Constraint  
Inference  
Graph  
Context  
Governance

정의는 개념을 만든다. 식별은 대상을 고정한다. 관계는 개념을 연결한다. 속성은 값과 상태를 부여한다. 공리는 의미를 고정한다. 제약은 데이터 품질을 검증한다. 추론은 숨은 의미를 도출한다. 그래프는 전체 연결 구조를 만든다. 맥락은 같은 관계가 상황에 따라 다르게 해석되도록 한다. 거버넌스는 온톨로지의 장기 진화를 통제한다.

이 중에서도 가장 중요한 것은 공리다. 클래스 이름만 있으면 용어 목록이다. 관계만 있으면 그래프다. 속성만 있으면 스키마다. 공리가 있어야 온톨로지가 된다. 공리는 정의, 관계, 속성에 논리적 의미를 부여하는 문장이다. 따라서 LEDO Foundation의 중심은 OWL Axiom System이어야 한다.

---

# **4\. `ot:` 단일 네임스페이스 전략**

LEDO Industrial Ontology Foundation은 단일 기본 네임스페이스를 사용한다. 기본 prefix는 `ot:`로 둔다.

ot:  
→ LEDO Industrial Ontology의 기본 namespace prefix

단일 namespace를 사용하는 이유는 Foundation 전체를 하나의 의미 세계로 유지하기 위해서다. 도메인마다 prefix를 무분별하게 나누면 초기에 보기 편할 수 있지만, 시간이 지나면 개념 중복, 관계 중복, 매핑 충돌, SKOS 라벨 중복, 외부 시스템 식별자 충돌이 발생할 수 있다. 따라서 Foundation의 공식 TBox는 `ot:`를 중심으로 통제한다.

다만 TBox와 ABox는 다르게 설계한다. TBox는 클래스, 속성, 공리, 스키마, 용어 체계처럼 사람이 읽고 관리해야 하는 구조다. 그러므로 TBox IRI는 사람이 이해할 수 있는 통제된 수직 구조를 따른다.

ot:Agent  
ot:RobotAgent  
ot:Sensor  
ot:Observation  
ot:Risk  
ot:WorkZone  
ot:DangerZone  
ot:Permit  
ot:Evidence  
ot:Action  
ot:Policy  
ot:ExecutionRequest

반면 ABox는 실제 현장 개체를 담는다. 실제 개체는 외부 시스템마다 ID가 다르고, 현장마다 이름이 다르고, 시간이 지나며 명칭이 바뀔 수 있다. 따라서 ABox의 실물 개체 IRI는 사람이 붙인 이름에 의존하지 않고, 128비트 해시 기반 결합 구조를 사용한다.

ot:abox/\<128bit\_hash\>

ABox hash는 다음 요소를 조합해 생성하는 것을 원칙으로 한다.

namespace\_version  
source\_system\_id  
source\_object\_id  
canonical\_object\_type  
site\_or\_org\_scope  
optional\_external\_identifier

이 전략은 두 가지 목표를 동시에 만족시킨다. 첫째, TBox는 사람이 읽고 검토할 수 있는 통제된 구조가 된다. 둘째, ABox는 대규모 산업 현장의 실물 객체를 안정적으로 식별할 수 있다. 이 구조는 Canonical Object Lifecycle과도 연결된다. 실제 현장 객체는 먼저 canonical identity로 정리되고, 그 결과가 128비트 hash 기반 ABox IRI로 고정된다.

핵심 원칙은 다음과 같다.

TBox uses controlled readable ot: IRIs.  
ABox uses 128-bit hash-based real-world object IRIs.  
ABox identity must not depend on mutable human labels.  
Every external identifier must be mapped, not blindly trusted.  
Canonical identity precedes ontology binding.

---

# **5\. Identity Resolution Flow**

Identity Resolution은 외부 시스템의 객체 ID를 온톨로지의 안정적인 ABox 개체로 바꾸는 과정이다. 산업 시스템에서는 같은 실물 객체가 여러 시스템에서 서로 다른 이름과 ID로 존재하기 때문에, 이 흐름이 없으면 그래프가 커질수록 중복 개체가 폭발한다.

권장 흐름은 다음과 같다.

External ID  
→ Source System Identifier  
→ Identifier Mapping Record  
→ Identity Resolution Evidence  
→ Canonical Identity  
→ 128-bit ABox Hash IRI  
→ Ontology Binding

각 단계의 의미는 다음과 같다.

External ID  
→ 외부 시스템이 부여한 원본 ID

Source System Identifier  
→ 해당 ID가 나온 시스템 또는 데이터 소스

Identifier Mapping Record  
→ 외부 ID와 내부 후보 객체의 연결 기록

Identity Resolution Evidence  
→ 같은 객체라고 판단한 근거

Canonical Identity  
→ 플랫폼 내부에서 확정된 단일 객체 정체성

128-bit ABox Hash IRI  
→ ontology graph에서 사용하는 안정적인 실물 개체 IRI

Ontology Binding  
→ 해당 실물 개체가 어떤 TBox class와 연결되는지에 대한 선언

예를 들어 하나의 휴머노이드가 Robot Middleware, 작업 관리 시스템, 관제 대시보드에서 서로 다른 ID로 들어올 수 있다. 이때 외부 ID를 그대로 `owl:sameAs`로 연결하면 위험하다. 먼저 mapping record와 evidence를 만들고, canonical identity를 확정한 뒤, ABox hash IRI를 생성해야 한다.

핵심 원칙은 다음과 같다.

External IDs are evidence, not truth.  
Canonical identity must be resolved before ontology binding.  
Strong sameAs assertions require governance.  
ABox hash IRI must remain stable even if human-readable labels change.

---

# **6\. Definition Layer**

Definition Layer는 산업 세계의 개념을 정의하는 층이다. 여기서 중요한 것은 모든 도메인 세부 클래스를 Foundation에 넣지 않는 것이다. Foundation은 하위 도메인을 감싸기 위한 최소 상위 개념만 가져야 한다.

Foundation의 기본 정의 카테고리는 다음 정도가 적절하다.

Entity  
Agent  
HumanAgent  
MachineAgent  
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
Risk  
Zone  
Policy  
Permit  
Action  
Feedback  
AuditRecord

이 카테고리들은 특정 산업에 갇히지 않는다. 휴머노이드, 산업기계, 자율주행체, 지정주행체, 센서, 관제 시스템, 작업자, 설비, 접근통제, 환경위험은 모두 이 상위 카테고리 아래에서 확장될 수 있다.

Definition Layer의 목적은 도메인 세부사항을 많이 만드는 것이 아니라, 하위 도메인이 어디에 붙어야 하는지 기준을 제공하는 것이다. 예를 들어 어떤 객체가 스스로 행동 후보를 만들거나 작업에 참여할 수 있으면 Agent 계열에 둘 수 있다. 물리적으로 존재하고 위치를 갖는다면 PhysicalObject 계열에 둘 수 있다. 상태를 관측하는 장치라면 Sensor 계열에 둘 수 있다. 작업을 수행하거나 통제 대상이 되는 장비라면 Machine 또는 Robot 계열로 세분화할 수 있다.

정의는 반드시 `skos:definition`, `rdfs:label`, `rdfs:comment`, 필요 시 한국어/영어 라벨을 함께 가져야 한다. 이것은 사람이 이해하기 위한 목적뿐 아니라, 향후 SLM 학습과 검색, 매핑, 문서 자동화에도 중요하다.

---

# **7\. Identity Layer**

Identity Layer는 같은 대상을 하나로 고정하는 층이다. 산업 시스템에서 가장 큰 병목 중 하나는 객체 중복이다. 같은 휴머노이드가 Fleet Manager에서는 다른 ID를 갖고, 관제 시스템에서는 다른 이름으로 보이며, 현장 작업 관리 시스템에서는 또 다른 자산번호로 기록될 수 있다. 같은 센서도 PLC, SCADA, IoT Gateway, RDF graph에서 서로 다른 이름으로 들어올 수 있다.

따라서 Foundation은 identity를 단순 문자열이 아니라 구조화된 개념으로 다뤄야 한다.

Identity Layer는 다음 개념을 포함한다.

CanonicalIdentity  
ExternalIdentifier  
SourceSystemIdentifier  
DeviceIdentifier  
AssetIdentifier  
AgentIdentifier  
LocationIdentifier  
HashBasedIRI  
IdentifierMappingRecord  
IdentityResolutionEvidence

`owl:sameAs`는 매우 강한 의미를 가지므로 남발하면 안 된다. 동일성은 시스템 전체에 강한 추론 영향을 줄 수 있다. 따라서 ABox에서 실물 객체를 합칠 때는 `sameAs`를 직접 사용하기보다, 내부적으로 `canonical_identity_ref`, `identifier_mapping_ref`, `identity_resolution_evidence_ref`를 먼저 두고, 검증된 경우에만 강한 동일성 선언을 허용한다.

핵심 원칙은 다음과 같다.

Names are not identity.  
External IDs are not automatically canonical.  
Canonical identity must be evidence-backed.  
Strong identity assertions require governance.  
ABox hash IRI must be stable across system boundaries.

---

# **8\. Relation Layer**

Relation Layer는 개념과 개체를 연결하는 층이다. 관계는 온톨로지의 핵심이지만, 관계를 너무 많이 만들면 Foundation이 병목이 된다. 반대로 관계가 너무 적으면 모든 것이 모호한 링크가 된다. 따라서 Foundation은 적지만 강한 상위 관계를 제공하고, 하위 도메인은 이 관계를 확장하는 방식으로 설계해야 한다.

추천 상위 관계 카테고리는 다음과 같다.

isPartOf  
locatedIn  
participatesIn  
performs  
uses  
observes  
controls  
affects  
requires  
authorizes  
generates  
supports  
causes  
mitigates  
restricts  
reportsTo  
communicatesWith

이 관계들은 대부분의 산업 도메인에 적용 가능하다. 예를 들어 RobotAgent는 Task를 수행할 수 있고, Sensor는 ObservableCondition을 관측할 수 있으며, AccessControlSystem은 ZoneAccess를 제한할 수 있고, Permit은 HighRiskTask를 허가할 수 있다. ControlSystem은 IndustrialMachine을 제어할 수 있고, Observation은 Evidence를 지지할 수 있으며, Event는 StateChange를 유발할 수 있다.

관계 설계의 핵심은 도메인별 관계를 무한정 새로 만들지 않는 것이다. 먼저 Foundation의 상위 관계로 표현할 수 있는지 검토하고, 충분하지 않을 때만 하위 관계를 만든다.

controls  
  └── remotelyControls  
  └── automaticallyControls  
  └── manuallyControls  
  └── supervisesControl  
  └── requestsControl

observes  
  └── observesPosition  
  └── observesGasLevel  
  └── observesTemperature

restricts  
  └── restrictsZoneAccess  
  └── restrictsTaskExecution

`ot:controls`는 특히 조심해서 설계해야 한다. `controls`는 직접 물리 명령을 의미할 수도 있고, 상위 관제 요청을 의미할 수도 있으며, 정책적으로 승인된 제어 의도를 의미할 수도 있다. 따라서 Foundation에서는 `controls`를 너무 강하게 해석하지 않고, 하위 관계를 통해 의미를 분리한다.

ot:controls  
→ broad control relationship

ot:requestsControl  
→ platform or agent requests a control action

ot:supervisesControl  
→ control system supervises another system

ot:automaticallyControls  
→ automated control relationship

ot:manuallyControls  
→ human-mediated control relationship

ot:remotelyControls  
→ remote control relationship

관계는 반드시 Domain, Range, Inverse, Property Characteristic을 검토해야 한다. 관계 이름만 추가하는 것은 온톨로지 설계가 아니다. 관계가 어떤 주어와 목적어를 갖고, 어떤 역관계가 있고, 전이성이나 함수성이 있는지 검토해야 한다.

---

# **9\. Attribute Layer**

Attribute Layer는 개체가 갖는 값과 상태를 표현한다. 속성은 온톨로지를 현실 세계와 연결하는 중요한 요소지만, 속성을 Foundation에 과도하게 넣으면 병목이 된다. 따라서 속성은 공통 속성, 상태 속성, 도메인 속성으로 나눠야 한다.

공통 속성은 대부분의 객체가 공유한다.

identifier  
label  
source  
created\_at  
updated\_at  
version  
lifecycle\_status  
confidence  
provenance\_ref

상태 속성은 시간에 따라 변한다.

location  
operational\_status  
connectivity\_status  
health\_status  
risk\_level  
task\_status  
battery\_level  
mode

도메인 속성은 하위 도메인 모듈에서 정의한다.

gas\_concentration  
tool\_grip\_force  
joint\_temperature  
vehicle\_speed  
machine\_load  
zone\_occupancy\_count

Foundation은 모든 도메인 속성을 직접 담지 않는다. Foundation은 속성의 종류와 설계 기준을 정한다. 어떤 속성이 DataProperty인지, 어떤 속성이 State로 분리되어야 하는지, 어떤 속성이 Observation으로 들어가야 하는지, 어떤 속성이 Evidence로 연결되어야 하는지를 결정하는 기준을 제공한다.

중요한 원칙은 다음과 같다.

Stable attributes belong to object description.  
Dynamic attributes belong to state or observation.  
Evidence-backed attributes must reference evidence.  
Raw sensor values should not all become semantic attributes.  
Domain-specific attributes belong to domain modules.

---

# **10\. OWL Axiom System**

OWL Axiom System은 이 Foundation의 중심이다. 공리는 온톨로지의 논리 문장이다. 클래스, 관계, 속성은 재료이고, 공리는 그 재료를 의미 있는 체계로 만든다.

공리는 다음 종류로 구분한다.

Class Axioms  
Property Axioms  
Individual Axioms  
Equivalence Axioms  
Disjointness Axioms  
Domain and Range Axioms  
Inverse Property Axioms  
Property Characteristic Axioms  
Restriction Axioms  
Cardinality Axioms

Class Axiom은 클래스 간 의미 관계를 정의한다.

HumanoidRobot SubClassOf RobotAgent.  
GasSensor SubClassOf Sensor.  
DangerZone DisjointWith SafeZone.

Property Axiom은 관계 자체의 의미를 정의한다.

observes Domain Sensor.  
observes Range ObservableCondition.  
performs Domain Agent.  
performs Range Task.  
requiresPermit Domain HighRiskTask.  
requiresPermit Range Permit.

Individual Axiom은 실제 개체에 대한 사실을 선언한다.

HumanoidRobot\_01 Type HumanoidRobot.  
GasSensor\_17 Type GasSensor.  
HumanoidRobot\_01 isLocatedIn Zone\_A.  
GasSensor\_17 observes GasConcentration\_Zone\_A.

Restriction Axiom은 어떤 클래스가 만족해야 하는 의미 조건을 정의한다.

HighRiskTask SubClassOf requiresPermit some Permit.  
SensorObservation SubClassOf generatedBy some Sensor.  
RobotInspectionTask SubClassOf performedBy some RobotAgent.

Cardinality Axiom은 최소, 최대, 정확한 연결 수를 표현한다. 다만 Cardinality는 Open World Assumption과 함께 이해해야 한다. OWL에서 최소 하나의 Permit이 필요하다고 선언해도, 데이터에 Permit이 없다는 이유만으로 즉시 오류가 되는 것은 아니다. OWL은 아직 알려지지 않은 Permit이 있을 수 있다고 본다. 따라서 실행 전 검증은 SHACL과 Safety Gate가 담당해야 한다.

공리 설계의 핵심 원칙은 다음과 같다.

Axioms must be intentional, not decorative.  
Every strong axiom must have a reason.  
Disjointness must be used carefully.  
Transitivity must be rare and controlled.  
Domain and range must not over-constrain early.  
Runtime safety must not depend only on OWL reasoning.

---

# **11\. Constraint Layer**

Constraint Layer는 데이터가 규칙을 만족하는지 검사하는 층이다. 여기서 OWL과 SHACL을 반드시 분리해야 한다.

OWL은 의미를 선언하고 추론을 만든다. SHACL은 데이터가 조건을 만족하는지 검증한다. Policy Engine은 운영상 허용과 금지를 판단한다. Safety Gate는 실행 직전 안전 조건을 검증한다.

OWL  
→ semantic meaning and reasoning

SHACL  
→ data validation and shape checking

Policy Engine  
→ operational permission and prohibition

Safety Gate  
→ pre-execution safety validation

예를 들어 OWL에서는 `HighRiskTask SubClassOf requiresPermit some Permit`이라고 선언할 수 있다. 이것은 고위험 작업이 Permit과 연결되어야 한다는 의미 조건을 만든다. 그러나 실제 데이터에 Permit이 빠져 있는지 검사하는 것은 SHACL의 역할이다. 그리고 그 작업을 실행해도 되는지 판단하는 것은 Policy Governance와 Safety Gate의 역할이다.

실제 런타임 검증 순서는 다음과 같이 분리하는 것이 좋다.

Input Data  
→ SHACL Validation  
→ Ontology Binding  
→ State / Evidence Update  
→ Policy Evaluation  
→ Decision / Approval  
→ Safety Gate Validation  
→ Execution Adapter Request  
→ Feedback / Audit

각 단계의 책임은 다르다. SHACL은 입력 데이터의 구조와 필수 필드와 값 범위를 본다. Ontology Binding은 해당 데이터가 어떤 개체와 클래스에 연결되는지 본다. State/Evidence Update는 현재 세계 상태와 판단 근거를 갱신한다. Policy Evaluation은 허용과 금지를 판단한다. Decision/Approval은 경로와 권한을 확정한다. Safety Gate는 실행 직전 조건을 다시 확인한다. Execution Adapter는 외부 시스템에 요청만 보낸다.

Constraint Layer는 다음 검증을 포함해야 한다.

required property validation  
datatype validation  
value range validation  
cardinality validation  
class membership validation  
target shape validation  
cross-reference validation  
evidence reference validation  
state freshness validation

SHACL은 특히 ABox 데이터 품질을 유지하는 데 중요하다. 센서 데이터, 작업 허가, 위험 상태, 로봇 상태, 구역 접근 상태, 관제 피드백이 RDF graph에 들어올 때 SHACL 검증을 통과해야 한다.

---

# **12\. Inference Layer**

Inference Layer는 명시적으로 입력되지 않은 의미를 도출하는 층이다. 추론은 공리와 관계와 속성에서 새로운 사실을 이끌어낸다.

추론은 다음 유형으로 나뉜다.

class inference  
property inference  
identity inference  
relation inference  
state inference  
risk inference  
context inference  
evidence inference

예를 들어 어떤 RobotAgent가 GasInspectionTask를 수행하고, GasInspectionTask가 HighRiskTask의 하위 클래스라면, 해당 작업이 고위험 작업이라는 것을 추론할 수 있다. 어떤 Zone에 GasRisk가 활성화되어 있고, 어떤 Agent가 그 Zone에 위치한다면, 해당 Agent가 위험에 노출되었을 가능성을 도출할 수 있다.

그러나 산업 피지컬 AI에서 추론은 조심해야 한다. Offline OWL reasoner는 온톨로지 일관성 검토, 클래스 분류, 관계 추론에 강하다. 하지만 런타임 안전 경로에서 모든 판단을 OWL reasoner에 의존하면 안 된다. 런타임에서는 SHACL, Policy Engine, Safety Gate, rules, cached state, graph query가 함께 작동해야 한다.

핵심 원칙은 다음과 같다.

Reasoning expands meaning.  
Validation checks data quality.  
Policy decides permission.  
Safety Gate validates execution eligibility.  
Runtime safety must remain deterministic.

---

# **13\. Graph Layer**

Graph Layer는 정의, 관계, 속성, 공리, 추론 결과가 연결되는 구조다. RDF graph는 온톨로지의 표현 형태이지만, 그래프 자체가 목적은 아니다. 그래프는 의미 연결망이어야 한다.

Graph Layer는 세 가지로 구분해야 한다.

Semantic Graph  
Runtime Graph  
Evidence Graph

Semantic Graph는 TBox와 공리, 클래스, 관계, SKOS 용어를 담는다. Runtime Graph는 현재 상태와 최근 의미 이벤트를 담는다. Evidence Graph는 판단 근거와 출처, 증거 번들, 감사 기록과 연결된다.

모든 raw sensor stream을 RDF graph에 넣으면 안 된다. 그것은 그래프 병목을 만든다. Raw stream은 time-series store나 stream processing layer에서 처리하고, 의미 있는 이벤트, 검증된 상태, evidence-backed decision만 그래프에 승격해야 한다.

Raw stream  
→ time-series or stream store

Meaningful event  
→ Event Graph

Verified state  
→ Runtime Graph

Evidence-backed decision  
→ Evidence and Audit Graph

이 원칙이 있어야 그래프가 운영 데이터 쓰레기통이 되지 않는다.

---

# **14\. Context Layer**

Context Layer는 같은 관계나 상태가 상황에 따라 다르게 해석될 수 있도록 하는 층이다. 산업 시스템에서는 단순 관계만으로 충분하지 않다. 같은 `locatedIn`도 작업 중인지, 대기 중인지, 비상 상황인지, 관제 승인 상태인지, 위험 상태인지에 따라 의미가 달라진다.

따라서 Foundation은 Context를 명시적으로 다뤄야 한다.

OperationalContext  
SafetyContext  
ExecutionContext  
ObservationContext  
PolicyContext  
TemporalContext  
SpatialContext  
HumanRobotCollaborationContext  
ControlContext

예를 들어 어떤 HumanoidRobot이 Zone\_A에 위치한다는 사실은 그 자체로는 위험하지 않을 수 있다. 그러나 Zone\_A에 active gas risk가 있고, 해당 RobotAgent가 inspection task를 수행 중이며, 통신 상태가 degraded라면 같은 locatedIn 관계는 훨씬 높은 의미를 가진다.

HumanoidRobot\_01 locatedIn Zone\_A.  
Zone\_A hasActiveRisk GasRisk\_01.  
HumanoidRobot\_01 performs InspectionTask\_09.  
HumanoidRobot\_01 hasConnectivityStatus DEGRADED.

이 상황에서는 단순 위치 관계가 아니라, “위험 노출 상태에서 통신이 불안정한 점검 작업”이라는 SafetyContext가 생성될 수 있다. 이 Context는 Policy Evaluation, Safety Gate, Audit Observability와 연결되어야 한다.

Context Layer는 관계의 의미를 폭발적으로 세분화하지 않고도 상황 의미를 표현할 수 있게 해준다. 즉, 관계를 무한히 늘리는 대신 Context를 통해 의미를 조정한다. 이것은 Foundation의 병목을 피하는 중요한 전략이다.

---

# **15\. Causality and Multi-Cause Scenario**

Causality는 Event, State, Evidence, Risk, Action, Audit를 연결하는 인과 체계다. 하나의 사건은 하나의 원인만 갖지 않는다. 산업 환경에서는 여러 센서, 여러 상태, 여러 시스템 조건이 동시에 결합해 하나의 위험 판단이나 비상 조치를 발생시킨다.

권장 구조는 다음과 같다.

primary\_causality\_id  
causality\_ids  
causality\_role  
causality\_direction

예시는 다음과 같다.

GasSensor\_01 reports critical gas concentration.  
HumanoidRobot\_01 is located in Zone\_A.  
VentilationSystem\_02 is degraded.  
CommunicationLink\_07 is degraded.

이 상황에서 단일 원인은 충분하지 않다. GasSensor의 임계값 초과, 휴머노이드의 위치, 환기 시스템의 저하, 통신 저하가 함께 의미를 만든다.

causality\_ids:  
  \- gas critical reading  
  \- robot located in affected zone  
  \- ventilation degraded  
  \- communication degraded

result:  
  \- Emergency Policy Evaluation  
  \- Safety Gate Revalidation  
  \- Access Restriction  
  \- Human Supervisor Notification  
  \- Post-Hoc Audit

이 구조는 Audit Observability Model과 직접 연결된다. AuditRecord는 단일 `causality_id`가 아니라 `causality_ids`를 참조할 수 있어야 한다. 그래야 사후 분석 시 “어떤 하나의 원인 때문에 발생했다”가 아니라 “어떤 복합 조건이 결합되어 발생했다”를 재구성할 수 있다.

---

# **16\. SKOS Lexical Foundation for SLM**

SKOS Lexical Foundation은 향후 SLM 훈련과 검색, 용어 정렬, 다국어 라벨, 도메인 설명 생성을 위한 기반이다. OWL은 엄격한 추론과 공리를 담당하지만, SLM은 공리만으로 충분히 학습하지 못한다. SLM은 용어, 정의문, 동의어, 설명, 예시, scope note, hidden label 같은 언어적 구조를 필요로 한다.

한 문장으로 정리하면 다음과 같다.

OWL defines formal meaning; SKOS organizes language around that meaning.

따라서 Foundation은 SKOS 항목을 충분히 가져야 한다.

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

Foundation SKOS는 다음 목적을 가진다.

human-readable ontology documentation  
SLM training support  
semantic search support  
term normalization  
multilingual label management  
domain vocabulary alignment  
mapping between field language and ontology terms

단, 실제 도메인 훈련 텍스트는 Foundation이 자동으로 만들지 않는다. 도메인 전문가가 직접 넣어야 한다. Foundation은 그 텍스트를 담을 구조를 제공한다. 즉 SKOS는 SLM 학습을 위한 그릇이고, 실제 내용은 도메인 경험과 현장 언어를 가진 사람이 채운다.

SKOS Concept Scheme은 다음처럼 나눌 수 있다.

AgentConceptScheme  
MachineConceptScheme  
RobotConceptScheme  
SensorConceptScheme  
TaskConceptScheme  
RiskConceptScheme  
ZoneConceptScheme  
PolicyConceptScheme  
EvidenceConceptScheme  
ControlSystemConceptScheme

SKOS와 OWL은 서로 다르다. OWL Class는 엄격한 논리 클래스이고, SKOS Concept은 용어와 개념 조직을 위한 것이다. 따라서 모든 SKOS Concept을 OWL Class로 무조건 변환하면 안 된다. 중요한 개념만 OWL Class와 연결하고, 나머지는 용어 체계로 유지한다.

핵심 원칙은 다음과 같다.

OWL is for formal semantics.  
SKOS is for lexical and conceptual organization.  
SLM training text belongs to SKOS-oriented documentation, not core axioms.  
Domain expert text must remain distinguishable from formal ontology axioms.

---

# **17\. Standards Alignment Matrix**

세계 수출형 산업 피지컬 AI 온톨로지는 국제 표준 정렬 없이 성립하기 어렵다. 표준은 단순 참고자료가 아니라, 상호운용성, 안전성, 보안성, 인증 가능성, 기술 수출 가능성의 기반이다.

Foundation에서 표준은 다음 방식으로 관리해야 한다.

StandardFamily  
StandardReference  
MappedOntologyArea  
MappedCoreSpec  
ComplianceRole  
ImplementationImpact  
ReviewRequired

LEDO 적용 등급은 다음 세 가지로 둔다.

MUST  
→ Foundation 설계에서 반드시 반영해야 하는 기준

SHOULD  
→ 강하게 권장되며, 산업 적용 시 우선 반영해야 하는 기준

MAY  
→ 도메인, 고객, 지역, 인증 범위에 따라 선택적으로 반영하는 기준

표준 정렬 매트릭스는 다음과 같이 잡는다.

| 표준군 | LEDO 적용 등급 | Foundation에서의 역할 |
| ----- | ----- | ----- |
| W3C RDF / RDFS | MUST | RDF graph, triple model, class/property 기본 구조 |
| W3C OWL 2 | MUST | formal ontology, class/property/individual axiom, reasoning |
| W3C SPARQL | MUST | graph query, semantic retrieval, audit/evidence query |
| W3C SHACL | MUST | ABox data validation, shape constraint |
| W3C SKOS | MUST | 용어 체계, SLM 학습 구조, multilingual label |
| W3C PROV-O | SHOULD | provenance, evidence lineage, source tracking |
| W3C OWL-Time | SHOULD | 시간 개념, temporal relation, event timing |
| OGC GeoSPARQL | SHOULD | 공간, 구역, 위치, geometry query |
| ISO/IEC 21838 / BFO | MUST | upper ontology, category discipline |
| IFC / BIM / ISO 16739 | SHOULD | external industrial asset alignment, BIM mapping |
| IEC 61508 | SHOULD | functional safety, safety lifecycle, SIL alignment |
| IEC 61511 | SHOULD | process safety, safety instrumented system alignment |
| IEC 62541 / OPC UA | SHOULD | industrial communication, telemetry, external system model |
| IEC 62264 / ISA-95 | SHOULD | enterprise-control integration boundary |
| ISA/IEC 62443 | MUST | industrial cybersecurity, OT/ICS security boundary |
| IEEE 1588 | MUST | time synchronization, clock trust, timestamp reliability |
| ISO 10218 / ISO robotics safety family | SHOULD | robot safety reference |
| ISO 8373 | MAY | robotics vocabulary reference |
| NIST SP 800-53 | SHOULD | security and privacy control reference |
| NIST AI RMF | SHOULD | AI risk governance reference |
| RFC 2119 / RFC 8174 | MUST | MUST/SHOULD/MAY requirement language |
| FIPA ACL | MAY | agent communication reference |

이 표준들을 모두 직접 구현한다는 뜻은 아니다. Foundation은 각 표준이 어느 설계 영역에 영향을 주는지 명시한다. 예를 들어 IEEE 1588은 시간 동기화와 `time_trust_level`, `clock_sync_status`, `clock_drift_estimate_ms`에 영향을 준다. IEC 61508과 IEC 61511은 Safety Gate, Risk, Fail-safe, Emergency Policy, Safety Instrumented System 모델에 영향을 준다. OPC UA는 외부 산업 시스템과의 adapter, telemetry, feedback, control boundary에 영향을 준다. NIST SP 800-53과 IEC 62443은 보안 정책, 접근통제, audit, zero-trust, OT 보안 설계에 영향을 준다.

---

# **18\. Upper Ontology and BFO Mapping**

BFO는 Foundation에서 상위 존재론 기준으로 사용한다. BFO를 사용한다는 것은 모든 도메인 클래스를 BFO 용어로 기계적으로 억지 매핑한다는 뜻이 아니다. 목적은 하위 도메인들이 서로 다른 철학으로 개념을 만들지 않도록 상위 존재론적 기준을 제공하는 것이다.

Foundation에서 BFO는 다음 구분에 사용된다.

continuant vs occurrent  
material entity  
process  
role  
function  
disposition  
site  
temporal region  
quality

예시 매핑은 다음과 같다.

| LEDO Concept | BFO-oriented category | 설명 |
| ----- | ----- | ----- |
| HumanoidRobot | material entity / object | 물리적으로 지속되는 로봇 개체 |
| GasSensor | material entity / device-like object | 관측 기능을 가진 물리 센서 |
| InspectionTask | process / planned process | 시간 안에서 수행되는 작업 과정 |
| HighRiskTask | process with risk context | 위험 조건이 부여된 작업 과정 |
| WorkerRole | role | 사람이 특정 맥락에서 수행하는 역할 |
| RobotOperatorRole | role | 로봇 또는 관제 시스템에 부여되는 조작 역할 |
| GasRisk | disposition / risk context | 위험 가능성 또는 위험 상태 맥락 |
| DangerZone | site / spatial region | 위험이 연결된 공간 영역 |
| SafetyPolicy | generically dependent continuant / information artifact | 정책 정보 객체 |
| SensorObservation | process or information content entity depending on modeling choice | 관측 행위 또는 관측 결과 정보 |

BFO Mapping의 핵심 원칙은 다음과 같다.

Use BFO to avoid category confusion.  
Do not overload domain classes with upper ontology meaning.  
Keep BFO mapping explicit and reviewable.  
Use BFO for alignment, not for domain bloat.

---

# **19\. External Industrial Model Alignment**

Foundation은 외부 산업 모델을 대체하지 않는다. IFC, BIM, OPC UA Information Model, PLC tag model, SCADA model, MES model, robotics vocabulary, sensor model 등은 모두 외부 모델로 존재할 수 있다. LEDO Foundation은 이들을 직접 복제하지 않고, Mapping Layer를 통해 연결한다.

외부 모델 정렬의 기본 구조는 다음과 같다.

External Model  
→ Mapping Module  
→ Canonical Object  
→ Ontology Binding  
→ Evidence / State / Action / Audit

이 구조가 중요한 이유는 외부 표준이 바뀌거나 현장 시스템이 바뀌어도 Foundation 자체가 흔들리지 않기 때문이다. Foundation은 외부 모델의 모든 세부사항을 흡수하지 않고, 외부 모델을 canonical object와 ontology class에 연결하는 기준을 제공한다.

핵심 원칙은 다음과 같다.

External standards are aligned, not blindly copied.  
Mapping modules absorb external schema changes.  
Canonical identity must sit between external IDs and ontology individuals.  
Domain modules must not directly depend on one vendor-specific schema.

---

# **20\. Governance Layer**

Ontology Governance는 Foundation의 장기 생존을 결정한다. 온톨로지는 한 번 만들고 끝나는 코드가 아니다. 도메인이 추가되고, 표준이 바뀌고, 현장 데이터가 늘어나고, 새로운 로봇과 설비와 센서가 들어오면 온톨로지도 진화해야 한다.

Governance Layer는 다음을 포함한다.

versioning  
deprecation  
migration  
mapping review  
axiom review  
property review  
SKOS term review  
standard alignment review  
module boundary review  
reasoner consistency check  
SHACL validation test  
competency question test

특히 공리 변경은 엄격하게 관리해야 한다. 클래스 하나를 추가하는 것은 비교적 안전할 수 있다. 그러나 domain/range, disjointness, transitive property, inverse property, cardinality restriction을 바꾸는 것은 전체 추론 결과를 바꿀 수 있다. 따라서 강한 공리 변경은 반드시 review 대상이어야 한다.

---

## **20.1 Axiom Change Impact Assessment**

공리 변경 영향도 평가는 온톨로지 거버넌스의 핵심이다. 공리 하나가 전체 그래프의 추론 결과를 바꿀 수 있기 때문에, 변경 전후 영향을 정량·정성으로 평가해야 한다.

평가 기준은 다음과 같다.

affected\_class\_count  
affected\_property\_count  
affected\_individual\_count  
changed\_inference\_count  
new\_inconsistency\_count  
new\_unsatisfiable\_class\_count  
changed\_SHACL\_result\_count  
changed\_competency\_question\_result\_count  
affected\_domain\_modules  
runtime\_safety\_impact

변경 유형별 위험도는 다음과 같이 본다.

| 변경 유형 | 영향도 | Review 수준 |
| ----- | ----- | ----- |
| rdfs:label 추가 | 낮음 | lightweight review |
| skos:altLabel 추가 | 낮음 | lightweight review |
| 새 하위 클래스 추가 | 중간 | ontology review |
| 새 relation 추가 | 중간 | property review |
| domain/range 변경 | 높음 | axiom review required |
| disjointness 추가 | 높음 | reasoner test required |
| transitive property 추가 | 매우 높음 | strict review required |
| inverse property 변경 | 높음 | inference regression test required |
| cardinality restriction 변경 | 높음 | SHACL and reasoning test required |
| sameAs 정책 변경 | 매우 높음 | identity governance review required |

공리 변경 전후에는 최소한 다음 테스트를 수행해야 한다.

reasoner consistency check  
unsatisfiable class check  
sample ABox inference comparison  
SHACL regression test  
competency question regression test  
module dependency check  
runtime safety impact review

Governance 원칙은 다음과 같다.

Axioms require review.  
Strong property changes require regression tests.  
SKOS terms require curation.  
Mappings require versioning.  
Deprecated terms must not disappear silently.  
Breaking changes must be explicitly marked.  
Every ontology release must be testable.

---

# **21\. Quality, Testing, and Evaluation**

Ontology Foundation은 품질 테스트 기준을 가져야 한다. 온톨로지는 문서상 좋아 보이는 것만으로 충분하지 않다. 실제로 reasoner와 SHACL과 SPARQL query와 domain scenario를 통해 검증되어야 한다.

품질 기준은 다음과 같다.

consistency  
satisfiability  
classification correctness  
property hierarchy correctness  
domain/range sanity  
disjointness safety  
SHACL validation pass rate  
competency question coverage  
SPARQL query usability  
SKOS label completeness  
mapping stability  
module dependency cleanliness  
runtime usability

Competency Question은 매우 중요하다. 온톨로지가 답해야 하는 질문을 먼저 정하고, 그 질문에 답할 수 있는지 테스트해야 한다.

예시 질문은 다음과 같다.

Which agents are currently located in a danger zone?  
Which tasks require a permit?  
Which observations support a high-risk decision?  
Which sensors generated evidence for a gas risk event?  
Which external systems received an execution request?  
Which robot agents are assigned to inspection tasks?  
Which zones are restricted by access control policy?

이런 질문에 답할 수 없다면, 클래스와 관계를 많이 만들었더라도 실무 온톨로지로는 부족하다.

---

# **22\. Anti-patterns**

Foundation에서 피해야 할 설계 오류는 명확하다.

| Anti-pattern | 이유 | 발생 가능한 문제 | 피해 규모 |
| ----- | ----- | ----- | ----- |
| Foundation에 도메인 세부 클래스를 과도하게 넣기 | Foundation이 특정 도메인에 종속됨 | 새 도메인 추가 시 충돌 증가 | 높음 |
| property를 도메인마다 무분별하게 생성 | 관계 체계가 중복됨 | query, reasoning, mapping 복잡도 증가 | 높음 |
| domain/range를 너무 좁게 설정 | 초기 설계가 미래 도메인을 막음 | 외부 도메인 확장 시 ontology conflict | 높음 |
| transitive property 남발 | 추론 범위가 폭발함 | 잘못된 관계 추론, 성능 저하 | 매우 높음 |
| OWL로 runtime validation 대체 | Open World Assumption과 실행 검증의 목적이 다름 | 누락 데이터가 위험으로 이어질 수 있음 | 매우 높음 |
| 모든 raw sensor data를 RDF graph에 저장 | 그래프가 운영 데이터 저장소로 변질됨 | graph write/read 병목 | 매우 높음 |
| SKOS와 OWL 혼동 | 용어 체계와 형식 의미가 섞임 | SLM 학습용 문장과 formal axiom 혼재 | 중간 |
| AI/SLM 출력을 Evidence로 직접 사용 | AI output은 검증된 사실이 아님 | 잘못된 판단 근거, 감사 불가능 | 매우 높음 |
| sameAs 남발 | 동일성 추론이 너무 강함 | 잘못된 객체 병합, 데이터 오염 | 매우 높음 |
| 표준을 사후에 맞추려 함 | 구조를 다시 뜯어고쳐야 함 | 수출·인증·연동 비용 폭증 | 매우 높음 |

핵심은 단순하다. Foundation은 모든 것을 직접 담는 곳이 아니라, 모든 것을 올바르게 받을 수 있도록 하는 기준층이다.

---

# **23\. LEDO Industrial Ontology Application Strategy**

LEDO Industrial Ontology Foundation은 하위 도메인을 순차적으로 확장하기 위한 기준이다. 하위 도메인은 언제든 추가될 수 있다. 중요한 것은 모든 하위 도메인이 동일한 Foundation을 따라야 한다는 점이다.

하위 도메인 모듈은 다음 방식으로 추가된다.

Domain concept  
→ Foundation category mapping  
→ TBox class extension  
→ property alignment  
→ axiom review  
→ SHACL shape design  
→ SKOS concept registration  
→ mapping module connection  
→ competency question test

예를 들어 새로운 자율주행 도메인이 들어오면, 먼저 AutonomousVehicle을 Agent, Machine, PhysicalObject, ControlledSystem 중 어디에 둘지 결정한다. 그런 다음 이동 상태, 위치, 경로, 관제 명령, 센서 관측, 위험 상태, 실행 요청과의 관계를 Foundation relation과 property로 연결한다. 필요한 경우에만 도메인별 하위 relation과 속성을 만든다. 마지막으로 SKOS 용어와 SHACL 검증, SPARQL 질의, competency question을 추가한다.

휴머노이드 도메인도 같은 방식으로 들어온다. HumanoidRobot은 RobotAgent, PhysicalObject, SensorPlatform, ExecutionTarget의 성격을 동시에 가질 수 있다. 그러나 이 복합성을 Foundation에 무작정 밀어 넣지 않는다. Foundation은 Agent, PhysicalObject, Sensor, Task, Risk, Evidence, Action, ExecutionTarget 같은 상위 개념을 제공하고, Humanoid 도메인 모듈이 이들을 조합해서 세부 모델을 만든다.

이 전략은 모든 도메인을 감싸면서도 병목을 피하는 방식이다. Foundation은 작고 강해야 한다. Domain Module은 크고 자유롭게 확장되어야 한다. Mapping Module은 외부 표준과 현장 시스템의 변화를 흡수해야 한다. SKOS는 인간 언어와 SLM 학습을 지원해야 한다. OWL Axiom은 의미를 고정해야 한다. SHACL은 데이터 품질을 검증해야 한다. SPARQL은 그래프를 탐색해야 한다. Governance는 이 모든 변화를 통제해야 한다.

최종 원칙은 다음과 같다.

Foundation must be small but strong.  
Domains must be extensible but governed.  
Axioms must be central.  
IRI strategy must be stable from the beginning.  
TBox must be readable and controlled.  
ABox must be hash-based and scalable.  
SKOS must support SLM training and semantic search.  
International standards must guide export-grade design.  
OWL, SHACL, SPARQL, Policy, and Safety Gate must have separate roles.  
The graph must contain meaning, not every raw signal.  
Axiom changes must be impact-assessed.

LEDO Industrial Ontology Foundation은 단순한 온톨로지 설명서가 아니다. 이것은 산업 피지컬 AI가 세계 시장에서 설명 가능하고, 확장 가능하고, 표준 정렬 가능하고, 안전하게 운영될 수 있도록 만드는 의미 기반이다. 이 Foundation이 단단해야 하위 도메인이 아무리 늘어나도 시스템은 무너지지 않는다.

