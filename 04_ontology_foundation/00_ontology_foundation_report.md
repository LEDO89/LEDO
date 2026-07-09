# **Ontology Foundation Report**

# **1\. Purpose**

The LEDO Industrial Ontology Foundation is not an ontology for describing one specific domain. This Foundation is an upper semantic basis for accepting lower-level industrial domains such as construction, manufacturing, plants, logistics, energy, ports, shipbuilding, railways, autonomous driving, guided driving, robotics, humanoids, sensors, control rooms, worker management, equipment management, safety management, and emergency response.

The purpose of this report is to define the semantic structure on which industrial objects, relationships, attributes, states, events, tasks, risks, evidence, policies, approvals, execution, feedback, and audit should be modeled. This Foundation is not a warehouse that directly contains all domain knowledge. Instead, it defines the minimal upper structure, axiom system, relationship design principles, identifier strategy, standards alignment method, SKOS-based vocabulary system, and role separation between reasoning and validation so that all domain knowledge can be safely added later.

If the LEDO Core Specifications are the operational constitution for platform decision-making, approval, execution requests, and audit, then the LEDO Industrial Ontology Foundation is the ontological constitution for semantically describing the industrial world. The Core Specifications define how the system governs decisions, approvals, execution readiness, requests, and audit. The Ontology Foundation defines what the targets of those decisions and requests are, and what relationships, attributes, and semantic rules those targets have.

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

# **4\. Foundation Namespace Strategy**

The LEDO Industrial Ontology Foundation uses controlled namespace governance.

The `ot:` prefix is the historical root or family prefix for the Foundation examples in this report.

The authoritative module namespace strategy is defined by `03_core_specifications/06_ontology_module_boundary/6_ontology_module_boundary.md`. Foundation, cross-domain, domain, mapping, and external-standard modules may use distinct governed prefixes when that document requires them.

The reason for controlled namespace governance is to keep the Foundation in one governed semantic system while avoiding careless domain-by-domain prefix sprawl. Uncontrolled prefixes can create concept duplication, relationship duplication, mapping conflicts, SKOS label duplication, and external system identifier conflicts. Therefore, all official TBox namespaces and prefixes must be reviewed and governed, whether they use the historical `ot:` examples or module-specific prefixes.

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
Module-specific namespace rules override the example `ot:` prefix wherever the Ontology Module Boundary specification defines a more specific contract.

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
