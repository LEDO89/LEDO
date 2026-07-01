# **Ontology-Centric Module Boundary**

# **1\. Purpose**

This document defines the core rules of the Ontology Module Boundary used in an ontology-centric cyber-physical platform.

The Ontology Module Boundary is the criterion for separating modules with different semantic responsibilities, instead of turning the entire ontology into one gigantic file or one gigantic set of classes.

If an Event Type expresses “what happened,” an Action Type expresses “what response can be taken,” a State Model expresses “what is currently in what state,” and an Evidence Model expresses “what proves that judgment,” then the Ontology Module Boundary expresses “which ontology module a given semantic concept should belong to.”

This document focuses on the following:

Define what an Ontology Module is.  
Distinguish the boundary between Core Ontology and Domain Ontology.  
Separate Core into core-upper and core-crosscutting.  
Define the responsibilities of the Construction, Industrial, Robot, Policy, AI, Evidence, Event, State, Action, and Mapping modules.  
Explicitly define the connection between the previous Evidence Model document and the Evidence Ontology Module.  
Distinguish common concepts from domain concepts.  
Define module dependency direction as a DAG structure.  
Prevent bypass contamination through the domain / range of Object Properties.  
Mediate complex cross-domain relationships through Mediation Concepts.  
Separate the roles of OWL Reasoning and SHACL Validation in runtime environments.  
Isolate the External Mapping Module as a Semantic Adapter.  
Define independent versioning, hot-swap, rollback, and conflict resolution policies for the Mapping Module.  
Define Namespace and IRI design criteria.  
Provide examples of versioned IRIs and owl:imports.  
Define module ownership, SemVer versioning, and deprecation rules.  
Define governance based on Impact Level.  
Define CI/CD-based module boundary validators.  
Prevent ontology drift, domain pollution, vendor pollution, AI pollution, and property pollution.  
Define the ontology module set to be implemented first in the MVP.

The full class/property catalog is managed in a separate document: Appendix E: Ontology Module Catalog.

---

# **2\. Document Separation Principle**

The Ontology Module Boundary document is divided into two parts.

## **2.1 Core Ontology Module Boundary Specification**

This is the present document.

It covers:

Ontology Module definition  
Layered Semantic Architecture  
Distinction between Core Upper and Core Crosscutting  
Distinction between Core Ontology and Domain Ontology  
Common / Core Module responsibilities  
Construction Module responsibilities  
Industrial Module responsibilities  
Robot Module responsibilities  
Policy Module responsibilities  
AI Module responsibilities  
Evidence Module responsibilities  
Event / State / Action Module responsibilities  
External Mapping / Semantic Adapter responsibilities  
Module dependency rules  
Object Property Boundary Rule  
Mediation Concept Pattern  
Reasoning Wall prevention rule  
Runtime SHACL Validation Rule  
Namespace / IRI rules  
owl:imports rules  
Import / Reference Rule  
Module Ownership  
SemVer Versioning / Deprecation Rule  
Impact Level Governance  
Runtime Validation / CI/CD Rule  
MVP Ontology Module Set  
Core scenario flows

## **2.2 Appendix E: Ontology Module Catalog**

This is a separate appendix document.

It covers:

core-upper class list  
core-crosscutting class list  
common property list  
construction class list  
industrial class list  
robot class list  
policy class list  
AI class list  
evidence class list  
state class list  
event class list  
action class list  
cross-module mapping list  
external ontology mapping list  
object property catalog  
SHACL shape catalog  
Mediation Concept catalog

By separating the documents this way, the Boundary document can remain short and stable, while the detailed class/property catalog can continue to expand according to domain expansion.

---

# **3\. Definition of Ontology Module**

An Ontology Module is an ontology unit responsible for a specific semantic area.

A single platform must not be operated as one gigantic ontology file.

Instead, semantic responsibilities should be divided as follows:

Core Upper Ontology  
Core Crosscutting Ontology  
Construction Ontology  
Industrial Ontology  
Robot Ontology  
Policy Ontology  
AI Ontology  
Evidence Ontology  
Event Ontology  
State Ontology  
Action Ontology  
External Mapping Ontology

An Ontology Module must answer the following questions:

What semantic area is this module responsible for?  
What classes can be included in this module?  
What properties can be included in this module?  
What domain / range can the ObjectProperties of this module have?  
Which other modules can this module import?  
Which other modules can this module reference?  
Which modules must this module not reference?  
Through which mediation concept should complex cross-domain relationships be connected?  
Who is the owner of this module?  
What is the versioning policy of this module?  
What is the impact level of changes to this module?  
How does this module connect to external standard ontologies?  
What impact do changes to this module have on the runtime system?  
Is this module subject to offline reasoner validation or runtime SHACL validation?

---

# **4\. Layered Semantic Architecture**

The Ontology Module Boundary must have the structure of a directed acyclic graph, or DAG.

The dependency direction is as follows:

Application / Service Layer  
        ↓  
Registry / Runtime Specification Layer  
        ↓  
Semantic Adapter / Mapping Layer  
        ↓  
Domain Ontology Modules  
        ↓  
Core Crosscutting Ontology  
        ↓  
Core Upper Ontology  
        ↓  
External Upper Ontology Alignment

Core principles:

Ontology module dependency must form a DAG.  
Circular dependency is prohibited.  
Core Upper must never import domain modules.  
Core Crosscutting may import Core Upper.  
Domain modules may import Core.  
Domain-to-domain direct dependency is restricted.  
Mapping modules isolate external schemas.  
Runtime validation must enforce dependency direction.

Core must not know Domain.  
Domain extends Core.  
Mapping connects external schemas with the internal semantic system.  
Registry manages operational rules.  
The Application Layer accesses through Registry and Adapter without directly contaminating the Ontology.

---

# **5\. Core Philosophy**

The core philosophy of the Ontology Module Boundary is as follows:

Place the most stable common concepts in core-upper.  
Place cross-domain shared concepts with higher extensibility in core-crosscutting.  
Place domain-specific concepts in Domain Modules.  
Place external standards and vendor schemas in the Mapping Module.  
Place runtime objects in DTO / World State / Registry.  
Place semantic definitions in Ontology.  
Do not place physical execution commands in Ontology.

The ontology is not a database that contains everything.

The ontology defines the following:

What is what  
What kind of thing something is  
What is related to what  
Which states and actions are semantically allowed  
Which evidence is required for a given judgment  
Which target a given action can be applied to  
Which module is responsible for which meaning  
Which mediation concept connects a given cross-domain relationship

The ontology does not directly perform the following:

Sensor data storage  
High-frequency telemetry storage  
Robot motor control  
PLC command execution  
LLM inference execution  
Real-time message dispatch  
External API calls  
Runtime policy evaluation  
Mapping transformation execution

---

# **6\. Two-Layer Structure of Core Ontology**

If the existing Core Module contains Event, State, Action, Evidence, Policy, and Provenance all together, the Core may become too large.

Therefore, Core is divided into two layers:

core-upper  
core-crosscutting

---

## **6.1 core-upper**

core-upper defines the most stable top-level concepts used commonly across all domains.

core-upper should rarely change.

Classes that can be included:

Entity  
Agent  
HumanAgent  
MachineAgent  
PhysicalObject  
DigitalObject  
Location  
SpatialRegion  
TimeInstant  
TimeInterval  
Source  
Capability  
Identifier

Properties that can be included:

hasIdentifier  
hasName  
hasType  
locatedIn  
hasTimestamp  
hasSource  
hasCapability  
partOf  
hasPart

Roles of core-upper:

Provide the most stable semantic foundation  
Provide top-level abstract classes for Domain Modules  
Provide a foundation for reducing cross-domain coupling  
Maintain IRI stability

## **6.2 core-crosscutting**

core-crosscutting defines concepts that are shared across multiple domains but are more likely to be extended than core-upper.

Classes that can be included:

Event  
State  
Action  
Evidence  
Observation  
Risk  
Policy  
Approval  
Feedback  
AuditRecord  
ProvenanceRecord  
Candidate  
Proposal  
Interpretation  
DerivedInformation  
OperationalContext  
RelationContext  
ActionTarget  
Decision

Properties that can be included:

hasState  
generatesEvent  
generatesEvidence  
supportsAction  
requiresEvidence  
requiresApproval  
hasRiskLevel  
hasProvenance  
wasDerivedFrom  
targetsEntity  
targetsLocation  
hasOperationalContext  
hasRelationContext

Roles of core-crosscutting:

Provide common abstractions for Event / State / Action / Evidence / Policy families  
Provide indirect connections between Domain Modules  
Provide a semantic bridge between Registry and Ontology  
Provide Mediation Concepts

## **6.3 Core Separation Principle**

core-upper contains only the most stable upper-level concepts.  
core-crosscutting contains operational semantic concepts shared across domains.  
Domain Modules may reference core-upper and core-crosscutting.  
core-upper does not import core-crosscutting.  
core-crosscutting may import core-upper.

---

# **7\. Distinction Between Core Ontology and Domain Ontology**

## **7.1 Core Ontology**

Core Ontology is the most basic semantic structure commonly used across all domains.

Core Ontology is the semantic constitution of the platform.

Core Ontology must not change frequently.  
Core Ontology must remain as small and stable as possible.

## **7.2 Domain Ontology**

Domain Ontology is a semantic structure specialized for a specific industry, site, equipment, or work area.

Examples:

Construction Ontology  
Industrial Ontology  
Robot Ontology  
Policy Ontology  
AI Ontology  
Evidence Ontology  
State Ontology  
Action Ontology  
Event Ontology

Domain Ontology extends Core Ontology.

Examples:

construction:Worker  
  subClassOf core\_upper:HumanAgent

robot:Robot  
  subClassOf core\_upper:MachineAgent

industrial:GasSensor  
  subClassOf industrial:Sensor

construction:WorkZone  
  subClassOf core\_upper:Location

evidence:SensorObservationEvidence  
  subClassOf core\_cross:Evidence

---

# **8\. Common / Core Module**

## **8.1 Responsibility**

The Common / Core Module defines top-level concepts and crosscutting concepts shared by all domains.

This module is the reference point for the semantic structure of the entire platform.

## **8.2 Classes That Can Be Included**

core-upper:

Entity  
Agent  
HumanAgent  
MachineAgent  
PhysicalObject  
DigitalObject  
Location  
SpatialRegion  
TimeInstant  
TimeInterval  
Source  
Capability  
Identifier

core-crosscutting:

Event  
State  
Action  
Evidence  
Observation  
Risk  
Policy  
Approval  
Feedback  
AuditRecord  
ProvenanceRecord  
DigitalSystem  
ActionTarget  
Candidate  
Proposal  
Interpretation  
DerivedInformation  
OperationalContext  
RelationContext  
Decision

## **8.3 Prohibitions**

Domain-specific classes must not be placed in the Core Module.

Prohibited examples:

TowerCrane  
HotWorkPermit  
HumanoidRobot  
PLCRegister  
GasSensor17  
ScaffoldInspection  
ConcretePourTask  
VendorRobotCommand

These concepts belong in Domain Modules such as Construction, Industrial, Robot, or Mapping.

---

# **9\. Construction Ontology Module**

## **9.1 Responsibility**

The Construction Module defines meanings related to construction sites, work, spaces, materials, personnel, permits, inspections, and safety zones.

## **9.2 Classes That Can Be Included**

ConstructionSite  
Building  
Floor  
WorkZone  
DangerZone  
RestrictedZone  
Worker  
Supervisor  
Subcontractor  
WorkPackage  
ConstructionTask  
Permit  
HotWorkPermit  
Scaffold  
Formwork  
Rebar  
ConcretePour  
Material  
Inspection  
SafetyInspection  
EvacuationArea

## **9.3 Connection to Core**

construction:Worker  
  subClassOf core\_upper:HumanAgent

construction:WorkZone  
  subClassOf core\_upper:Location

construction:ConstructionTask  
  subClassOf core\_cross:ActionTarget

construction:Permit  
  subClassOf core\_cross:Policy

construction:Inspection  
  subClassOf core\_cross:Observation

## **9.4 Prohibitions**

The Construction Module must not directly define a robot’s internal mission state or PLC register.

Prohibited examples:

RobotBatteryState  
PLCRegister  
SCADAAlarmCode  
LLMPromptTrace  
VendorRobotMissionStatus

These concepts belong in the Robot, Industrial, AI, or Mapping Module.

---

# **10\. Industrial Ontology Module**

## **10.1 Responsibility**

The Industrial Module defines meanings related to sensors, equipment, PLC, SCADA, alarms, telemetry, and equipment state.

## **10.2 Classes That Can Be Included**

Equipment  
Machine  
Sensor  
GasSensor  
TemperatureSensor  
PressureSensor  
PLC  
SCADA  
Alarm  
TelemetrySignal  
ControlMode  
EquipmentOperationalState  
PLCConnectionState  
SensorHealthState  
Register  
Tag  
IndustrialEvent

## **10.3 Connection to Core**

industrial:Sensor  
  subClassOf core\_upper:PhysicalObject

industrial:GasSensor  
  subClassOf industrial:Sensor

industrial:Alarm  
  subClassOf core\_cross:Event

industrial:TelemetrySignal  
  subClassOf core\_cross:Observation

industrial:Equipment  
  subClassOf core\_upper:PhysicalObject

## **10.4 Prohibitions**

The Industrial Module must not directly define work permits, construction work types, robot missions, or LLM summaries.

---

# **11\. Robot Ontology Module**

## **11.1 Responsibility**

The Robot Module defines meanings related to robots, humanoids, AMRs, AGVs, drones, missions, capabilities, fleet managers, and robot middleware.

## **11.2 Classes That Can Be Included**

Robot  
HumanoidRobot  
AMR  
AGV  
Drone  
RobotMission  
RobotTask  
RobotCapability  
RobotPose  
RobotBatteryState  
RobotOperationalState  
Fleet  
FleetManager  
RobotMiddleware  
NavigationState  
MissionStatus  
BehaviorTree

## **11.3 Connection to Core**

robot:Robot  
  subClassOf core\_upper:MachineAgent

robot:RobotMission  
  subClassOf core\_cross:ActionTarget

robot:RobotCapability  
  subClassOf core\_upper:Capability

robot:RobotPose  
  subClassOf core\_cross:Observation

robot:FleetManager  
  subClassOf core\_cross:DigitalSystem

## **11.4 Prohibitions**

The Robot Module must not directly define work permit policies, sensor raw telemetry storage structures, AI prompts, or evidence trust policies.

---

# **12\. Policy Ontology Module**

## **12.1 Responsibility**

The Policy Module defines meanings related to roles, permissions, approvals, access control, safety policies, legal constraints, and emergency policies.

## **12.2 Classes That Can Be Included**

Role  
Permission  
Approval  
ApprovalLevel  
Clearance  
PolicyRule  
SafetyRule  
AccessControlRule  
LegalConstraint  
EmergencyPolicy  
HumanApproval  
PolicyDecision  
PolicyException

## **12.3 Connection to Core**

policy:Approval  
  subClassOf core\_cross:Approval

policy:SafetyRule  
  subClassOf core\_cross:Policy

policy:PolicyDecision  
  subClassOf core\_cross:Decision

policy:EmergencyPolicy  
  subClassOf core\_cross:Policy

## **12.4 Prohibitions**

The Policy Module must not directly manage actual Rego code, OPA bundles, or OpenFGA tuples as ontology classes.

The ontology defines the meaning of policies.  
OPA / Rego / OpenFGA are responsible for runtime policy execution.

---

# **13\. AI Ontology Module**

## **13.1 Responsibility**

The AI Module defines meanings related to LLM output, RAG results, model explanations, prompt traces, mapping proposals, risk interpretations, and action candidates.

## **13.2 Classes That Can Be Included**

ModelOutput  
LLMOutput  
RAGResult  
EvidenceSummary  
RiskInterpretation  
MappingProposal  
ActionCandidate  
Explanation  
PromptTrace  
ModelInference  
ConfidenceScore  
AIExtractionCandidate

## **13.3 Connection to Core**

ai:ActionCandidate  
  subClassOf core\_cross:Candidate

ai:EvidenceSummary  
  subClassOf core\_cross:DerivedInformation

ai:MappingProposal  
  subClassOf core\_cross:Proposal

ai:RiskInterpretation  
  subClassOf core\_cross:Interpretation

## **13.4 Prohibitions**

The AI Module must not have meanings that directly create ApprovedAction, EmergencyApprovedAction, ExecutionRequest, or PhysicalCommand.

Core principle:

AI can propose.  
AI cannot approve.  
AI cannot execute.

---

# **14\. Evidence Ontology Module**

## **14.1 Responsibility**

The Evidence Module defines meanings related to evidence types, evidence sources, trust levels, provenance, evidence bundles, and evidence graph relationships.

This module must semantically accommodate the structure defined in the previous document, the Evidence Model.

The Evidence Model defines DTOs and operational rules.  
The Evidence Ontology Module defines the semantic structure of those concepts.

## **14.2 Explicit Connection to the Evidence Model**

The Evidence Module must be able to semantically represent the following concepts defined in the Evidence Model:

EvidenceRecord  
EvidenceBundle  
EvidenceSource  
SourceTrustLevel  
TimeTrustLevel  
ClockSyncStatus  
ClockDriftCalculationMethod  
SpatialValidity  
DeviceHealthContext  
AttestedExtraction  
TrustUpgradeStatus  
EvidenceConflict  
ConflictResolutionStrategy  
PrivacyLifecycleStatus  
CryptoShreddingStatus  
LegalHoldStatus  
EvidenceGraph  
Provenance

That is, the following fields from the Evidence Model must be connectable as classes or properties in the Evidence Ontology Module:

clock\_drift\_estimate\_ms  
time\_trust\_level  
clock\_sync\_status  
time\_authority\_ref  
offline\_clock\_trust\_policy\_ref  
trust\_upgrade\_status  
attestation\_type  
attestation\_evidence\_refs  
conflict\_status  
applied\_conflict\_weights  
privacy\_lifecycle\_status  
legal\_hold\_status  
payload\_hash  
prov\_entity\_ref  
activity\_refs

## **14.3 Classes That Can Be Included**

Evidence  
EvidenceRecord  
EvidenceBundle  
EvidenceSource  
SourceTrustLevel  
TimeTrust  
SpatialValidity  
DeviceHealthContext  
EvidenceConflict  
ConflictResolution  
EvidenceChain  
EvidenceGraph  
Attestation  
AttestedExtraction  
TrustUpgrade  
PrivacyLifecycle  
CryptoShredding  
LegalHold  
Provenance

## **14.4 Connection to Core**

evidence:EvidenceRecord  
  subClassOf core\_cross:Evidence

evidence:EvidenceBundle  
  subClassOf core\_cross:Evidence

evidence:Attestation  
  subClassOf core\_cross:ProvenanceRecord

evidence:EvidenceConflict  
  subClassOf core\_cross:Event

evidence:PrivacyLifecycle  
  subClassOf core\_cross:State

## **14.5 Attested Extraction Connection**

The Evidence Module does not treat values extracted by AI/RAG/OCR directly as primary evidence.

Instead, it has the following structure:

evidence:DocumentExtractedEvidence  
  subClassOf evidence:EvidenceRecord

evidence:DocumentExtractedEvidence  
  evidence:wasExtractedFrom evidence:DocumentEvidence

evidence:DocumentExtractedEvidence  
  evidence:hasAttestation evidence:Attestation

evidence:DocumentExtractedEvidence  
  evidence:hasTrustUpgradeStatus evidence:TrustUpgradeStatus

Core principle:

AI-extracted value is AI\_DERIVED by default.  
AI-extracted value can become ATTESTED\_AI\_DERIVED only through attestation.

## **14.6 Conflict Resolution Matrix Connection**

The Evidence Module must semantically represent Evidence Conflict.

Example:

evidence:GasSensorAReading  
  evidence:conflictsWith evidence:GasSensorBReading

evidence:ConflictResolution\_001  
  evidence:usesStrategy evidence:DEVICE\_HEALTH\_WEIGHTED\_SELECTION

evidence:ConflictResolution\_001  
  evidence:selectedEvidence evidence:GasSensorAReading

The actual calculation and weighting of conflict resolution are performed in the Registry / Policy Layer.  
The Ontology Module defines the semantic relationships.

## **14.7 Privacy Lifecycle Connection**

The Evidence Module must distinguish between the append-only audit shell and protection of the PII payload.

Example:

evidence:WorkerLocationEvidence\_001  
  evidence:hasPrivacyLifecycleStatus evidence:PII\_PRESENT

evidence:WorkerLocationEvidence\_001  
  evidence:hasPrivacyLifecycleStatus evidence:PII\_CRYPTO\_SHREDDED

evidence:WorkerLocationEvidence\_001  
  evidence:hasPayloadHash "abc123"

Core principle:

Audit shell remains.  
PII payload may be masked, anonymized, or crypto-shredded.  
Payload hash remains for audit proof.

## **14.8 Prohibitions**

The Evidence Module does not directly store sensor raw streams.

High-frequency raw telemetry is handled by the Time-Series DB or Stream Layer.  
The Evidence Module defines the meaning of the data only when it is promoted to judgment-supporting evidence.

---

# **15\. Event / State / Action Ontology Modules**

## **15.1 Event Module**

The Event Module defines the meaning of semantic events used by the platform.

Examples:

SafetyEvent  
RobotEvent  
ConstructionEvent  
IndustrialEvent  
GovernanceEvent  
AuditEvent  
EvidenceConflictEvent  
MappingValidationEvent

It is connected to the Event Type Registry.

## **15.2 State Module**

The State Module defines the meaning of semantic states that an entity can have.

Examples:

MissionStatus  
ZoneRiskState  
PermitStatus  
ExecutionState  
ReconciliationStatus  
EvidenceValidityStatus  
PrivacyLifecycleStatus  
MappingCompatibilityStatus

It is connected to the State Model Registry.

## **15.3 Action Module**

The Action Module defines the meaning of action types used by the platform.

Examples:

SafetyAction  
RobotAction  
NotificationAction  
EmergencyAction  
RecoveryAction  
GovernanceAction  
MappingReviewAction

It is connected to the Action Type Registry.

## **15.4 Boundary Between Semantic Definition and Operational Rules**

The Event / State / Action Modules define meaning.

The Event Type Registry, State Model Registry, and Action Type Registry manage operational registries.

Ontology Module  
→ meaning definition

Registry  
→ operational specification

Example:

state:MissionStatus  
→ semantic definition of the MissionStatus concept

StateModelRegistry.MissionStatus  
→ allowed values, transition rules, timeout policy, ownership, freshness rule

---

# **16\. External Mapping Module / Semantic Adapter**

## **16.1 Responsibility**

The External Mapping Module defines mappings between external standards, external systems, vendor-specific schemas, and internal ontology modules.

Targets of connection:

BFO  
SOSA  
SAREF  
PROV-O  
Brick  
BOT  
IFC  
OPC UA  
Vendor Robot API  
SCADA tag schema  
ERP / PMIS schema

## **16.2 Classes / Properties That Can Be Included**

ExternalClassMapping  
ExternalPropertyMapping  
VendorMapping  
SchemaMapping  
IRIAlignment  
EquivalentClassMapping  
EquivalentPropertyMapping  
NarrowerMapping  
BroaderMapping  
SemanticAdapter  
MappingVersion  
ExternalSchemaVersion  
MappingCompatibilityStatus  
MappingConflict  
MappingConflictResolution

## **16.3 Principle**

External standards must not be directly mixed into the core ontology.

External standards are connected through the mapping layer.

## **16.4 Semantic Adapter Rule**

The Mapping Module is treated not as a simple auxiliary file, but as a Semantic Adapter.

Internal Ontology  
→ stable semantic model

Mapping Module  
→ external schema alignment layer

Adapter Layer  
→ runtime transformation

Core principles:

External schema changes must not force internal ontology changes.  
Mapping modules must have independent versioning.  
Mapping modules must support hot-swap deployment.  
Mapping failure must be isolated from core ontology.

## **16.5 Mapping Module Independent Versioning**

The Mapping Module must have a separate versioning track from internal ontology modules.

Example:

mapping:IFC\_4\_3\_IfcWall\_to\_construction\_Wall  
  mapping:externalSchemaVersion "IFC 4.3"  
  mapping:internalOntologyVersion "construction-1.2"  
  mapping:compatibilityStatus "ACTIVE"

If a Vendor API changes, only the mapping is replaced instead of modifying the internal Robot Ontology.

Example:

mapping:VendorRobotAPI\_v2\_to\_robot\_RobotMission

The internal concept `robot:RobotMission` remains stable.

## **16.6 Mapping Conflict Resolution Rule**

Multiple external mappings may be attached to the same internal class.

Example:

IFC\_Wall → construction:Wall  
VendorWallObject → construction:Wall  
PMIS\_WallActivity → construction:Wall

In this case, a mapping conflict resolution policy is required.

Recommended strategies:

PREFER\_INTERNAL  
PREFER\_EXTERNAL  
PREFER\_NEWER\_VERSION  
PREFER\_HIGHER\_TRUST\_MAPPING  
MANUAL\_REVIEW  
BLOCK\_ON\_CONFLICT

Example:

mapping:MappingConflict\_001  
  mapping:internalClass construction:Wall  
  mapping:externalClass ifc:IfcWall  
  mapping:externalClass vendor:WallObject  
  mapping:conflictResolutionStrategy mapping:MANUAL\_REVIEW

Core principles:

Mapping conflict must not mutate internal ontology.  
Mapping conflict must be resolved in mapping layer.  
Internal class remains stable.

## **16.7 Mapping Hot-swap / Rollback Policy**

The Mapping Module must support hot-swap and rollback.

Required rules:

Mapping update must not mutate internal ontology class definitions.  
Mapping update must be versioned independently.  
Mapping update must pass mapping compatibility validation.  
Mapping update must support rollback to previous active mapping.  
Mapping failure must degrade gracefully.

---

# **17\. Module Dependency Rules**

Ontology Modules must not reference one another arbitrarily.

Dependencies must have directionality.

## **17.1 Basic Dependency Direction**

Application / Registry Layer  
        ↓  
Semantic Adapter / Mapping Layer  
        ↓  
Domain Modules  
        ↓  
Core Crosscutting  
        ↓  
Core Upper

A Domain Module may reference a Core Module.

A Core Module must not reference a Domain Module.

Example:

construction:Worker  
  subClassOf core\_upper:HumanAgent

Allowed.

But:

core\_upper:HumanAgent  
  subClassOf construction:Worker

Prohibited.

## **17.2 Module Dependency DAG Rule**

All module dependencies must have a DAG structure.

Prohibited:

Construction → Robot → Construction  
Robot → Industrial → Robot  
Policy → AI → Policy

Allowed:

CoreCrosscutting → CoreUpper  
Construction → CoreUpper  
Construction → CoreCrosscutting  
Robot → CoreUpper  
Robot → CoreCrosscutting  
Industrial → CoreUpper  
Industrial → CoreCrosscutting  
Mapping → Construction  
Mapping → Robot  
Mapping → Industrial

If a cycle is found, the module release must be blocked.

---

# **18\. Object Property Boundary Rule**

## **18.1 Problem**

Module contamination does not occur only through class inheritance.

In actual implementation, bypass contamination can occur through the `rdfs:domain` and `rdfs:range` of ObjectProperties.

Problem example:

robot:operatesIn  
  rdfs:domain robot:Robot  
  rdfs:range construction:WorkZone

At first glance, the class hierarchy looks clean.

However, at the property range level, the Robot Module directly references the Construction Module.

This tightly couples the Robot Module and the Construction Module.

## **18.2 Core Rule**

An ObjectProperty belonging to a Domain Module must not directly reference a class from another Domain Module as its `rdfs:domain` or `rdfs:range`.

If it needs to reference a concept from another domain, it must use a Core class or a Mediation Concept as its domain or range.

Prohibited:

robot:operatesIn  
  rdfs:domain robot:Robot  
  rdfs:range construction:WorkZone

Allowed:

robot:operatesIn  
  rdfs:domain robot:Robot  
  rdfs:range core\_upper:Location

And in the Construction Module:

construction:WorkZone  
  subClassOf core\_upper:Location

The connection is made this way.

---

# **19\. Mediation Concept Pattern**

## **19.1 Need**

Some cross-domain relationships cannot be sufficiently represented by a simple abstract class such as core:Location.

For example, the following relationships are complex:

A robot mission is connected to a specific work zone, time, permit state, risk state, and worker presence.  
Sensor evidence supports an action candidate together with a specific zone, equipment state, and policy judgment.  
A construction task and a robot mission are coordinated within the same operational context.

In such cases, a Mediation Concept is used instead of a direct reference.

## **19.2 Recommended Mediation Concepts**

The following classes are placed in core-crosscutting:

OperationalContext  
RelationContext  
CoordinationContext  
SafetyContext  
ExecutionContext  
EvidenceContext  
MappingContext

## **19.3 Example: Connecting Robot Mission and Construction Zone**

Direct coupling is prohibited:

robot:RobotMission  
  robot:targetsWorkZone construction:WorkZone

Using a Mediation Concept:

robot:RobotMission  
  core\_cross:hasOperationalContext core\_cross:OperationalContext

core\_cross:OperationalContext  
  core\_cross:hasLocation core\_upper:Location  
  core\_cross:hasRisk core\_cross:Risk  
  core\_cross:hasPolicy core\_cross:Policy

construction:WorkZone  
  subClassOf core\_upper:Location

Judgment:

The Robot Module does not directly reference the Construction Module.  
OperationalContext mediates the relationship.

---

# **20\. Reasoning Wall and SHACL Validation**

## **20.1 Reasoning Wall Problem**

As the ontology grows and the number of mapping modules increases, the computational cost of the OWL Reasoner can increase rapidly.

This becomes especially dangerous when the following are connected together:

BFO  
SOSA  
SAREF  
PROV-O  
IFC  
BOT  
OPC UA  
Vendor mapping  
Construction module  
Robot module  
Industrial module  
Evidence module  
Policy module

If HermiT / Pellet reasoning is executed every time at runtime over all of these, the system can freeze.

This is called the Reasoning Wall.

## **20.2 Offline / Build-time Reasoning Rule**

The OWL Reasoner is used for static consistency checks.

Use cases:

module consistency check  
class hierarchy validation  
equivalent class validation  
disjointness validation  
ontology release validation  
mapping sanity check

Tools:

Pellet  
HermiT  
OWL reasoner  
Protégé validation  
CI ontology validation pipeline

## **20.3 Runtime SHACL Validation Rule**

At runtime, full OWL reasoning is minimized and SHACL is used as the main guardrail.

Use cases:

incoming event validation  
state transition validation  
evidence requirement validation  
action target validation  
module boundary validation  
object property domain/range validation  
cross-module reference validation  
mapping compatibility validation

Tools:

SHACL  
SPARQL ASK  
policy validator  
cached ontology view  
registry compatibility check

## **20.4 Core Principle**

OWL reasoner is for static consistency.  
SHACL is the main runtime guardrail.  
Runtime safety path must not depend on full OWL reasoning.

From the MVP stage, the following items must be validated with SHACL:

ObjectProperty domain/range boundary  
Core → Domain forbidden import  
Domain-to-domain direct property reference  
Mapping module isolation  
Action target class validity  
Evidence target binding validity  
State transition target validity

---

# **21\. Namespace / IRI Rules**

Each ontology module must have an independent namespace.

## **21.1 Recommended Namespaces**

core\_upper:    https://example.org/ontology/core-upper\#  
core\_cross:    https://example.org/ontology/core-crosscutting\#  
construction:  https://example.org/ontology/construction\#  
industrial:    https://example.org/ontology/industrial\#  
robot:         https://example.org/ontology/robot\#  
policy:        https://example.org/ontology/policy\#  
ai:            https://example.org/ontology/ai\#  
evidence:      https://example.org/ontology/evidence\#  
event:         https://example.org/ontology/event\#  
state:         https://example.org/ontology/state\#  
action:        https://example.org/ontology/action\#  
mapping:       https://example.org/ontology/mapping\#

## **21.2 Versioned IRI Examples**

In production environments, versioned IRIs can be used.

Examples:

https://example.org/ontology/core-upper/2026-06\#  
https://example.org/ontology/core-crosscutting/2026-06\#  
https://example.org/ontology/construction/2026-06\#  
https://example.org/ontology/robot/2026-06\#  
https://example.org/ontology/mapping/ifc/4.3\#

Principles:

Class IRIs remain stable.  
Module version IRIs are used for release management.  
Existing class IRIs must not be arbitrarily changed.  
Breaking changes are separated into a new version IRI or a new module.

## **21.3 IRI Principles**

IRIs must be stable.

IRIs must not be arbitrarily changed.

Class IRIs and individual IRIs must be distinguished.

Example:

Class:

robot:Robot

Individual:

robot:Robot\_07

State class:

state:MissionStatus

State value individual:

state:MissionStatus\_DISABLED

---

# **22\. owl:imports Rules**

## **22.1 Allowed Example**

The Construction Module may import core-upper and core-crosscutting.

@prefix owl: \<http://www.w3.org/2002/07/owl\#\> .

\<https://example.org/ontology/construction/2026-06\>  
    a owl:Ontology ;  
    owl:imports  
        \<https://example.org/ontology/core-upper/2026-06\> ,  
        \<https://example.org/ontology/core-crosscutting/2026-06\> .

The Robot Module may also import core.

\<https://example.org/ontology/robot/2026-06\>  
    a owl:Ontology ;  
    owl:imports  
        \<https://example.org/ontology/core-upper/2026-06\> ,  
        \<https://example.org/ontology/core-crosscutting/2026-06\> .

## **22.2 Prohibited Example**

Core Upper must not import a Domain Module.

\<https://example.org/ontology/core-upper/2026-06\>  
    a owl:Ontology ;  
    owl:imports  
        \<https://example.org/ontology/construction/2026-06\> .

Prohibited.

The Robot Module is also generally prohibited from directly importing the Construction Module.

\<https://example.org/ontology/robot/2026-06\>  
    a owl:Ontology ;  
    owl:imports  
        \<https://example.org/ontology/construction/2026-06\> .

Prohibited.

In this case, Core abstraction or a Mediation Concept is used.

---

# **23\. Module Boundary Rule**

## **23.1 What Can Be Placed in Core**

A concept can be placed in Core if it satisfies the following conditions:

It is commonly used across all domains.  
It is not dependent on a specific industry or equipment.  
It is stable over the long term.  
It is an upper-level concept that other modules need to reference.

Examples:

Entity  
Agent  
Location  
Time  
Capability  
Event  
State  
Action  
Evidence  
Risk  
Policy  
Provenance  
OperationalContext

## **23.2 What Belongs in a Domain Module**

A concept should be placed in a Domain Module if it satisfies the following conditions:

It is specialized for a specific industry, site, equipment, or task.  
It extends a Core concept.  
It may not be used in other domains.

Examples:

HotWorkPermit  
TowerCrane  
GasSensor  
HumanoidRobot  
RobotMission  
ScaffoldInspection

## **23.3 What Belongs in the Mapping Module**

A concept should be placed in the Mapping Module if it satisfies the following conditions:

It connects external standards with the internal ontology.  
It connects vendor schemas with internal classes.  
It aligns identical or similar concepts.  
It acts as an adapter for external schema changes.

Examples:

IFC\_Wall ↔ construction:Wall  
SOSA\_Sensor ↔ industrial:Sensor  
PROV\_Entity ↔ evidence:EvidenceRecord  
VendorRobotMission ↔ robot:RobotMission

## **23.4 What Belongs in a Registry**

The following are managed not in ontology modules, but in registries:

EventTypeSpec  
ActionTypeSpec  
StateModelSpec  
EvidenceModelSpec  
PolicySpec  
AdapterSpec  
TimeoutPolicy  
RetryPolicy  
FreshnessPolicy  
SHACLShapeSpec  
SemanticAdapterSpec

Ontology defines meaning.  
Registry defines operational rules.

---

# **24\. Ontology Module Boundary Anti-Patterns**

The following must be avoided.

## **24.1 God Ontology**

Putting all classes and properties into a single ontology file.

Problems:

The scope of change impact becomes too large.  
Domain ownership becomes unclear.  
Reasoning cost increases.  
Versioning becomes difficult.

## **24.2 Domain Pollution**

Putting domain-specific concepts into the Core Module.

Examples:

core:TowerCrane  
core:HotWorkPermit  
core:RobotBatteryState

Problems:

Core becomes large and unstable.  
Other domain modules become contaminated.

## **24.3 Vendor Pollution**

Putting vendor-specific APIs or tags directly into ontology core.

Examples:

core:BostonDynamicsSpotCommand  
core:SiemensPLCRegister40001

Problem:

A vendor change can destabilize the core ontology.

Vendor-specific concepts belong in the External Mapping Module or Adapter Layer.

## **24.4 AI Pollution**

Putting AI output directly into the ontology as truth or approved action.

Example:

ai:LLMDecision  
  equivalentTo action:ApprovedAction

Prohibited.

AI can propose.  
AI cannot approve.  
AI cannot execute.

## **24.5 Property Pollution**

Directly referencing another domain module through the domain or range of an ObjectProperty.

Example:

robot:operatesIn  
  rdfs:range construction:WorkZone

Prohibited.

Solution:

robot:operatesIn  
  rdfs:range core\_upper:Location

Or:

robot:RobotMission  
  core\_cross:hasOperationalContext core\_cross:OperationalContext

---

# **25\. OntologyModuleSpecDTO**

An Ontology Module is managed through OntologyModuleSpecDTO.

## **25.1 OntologyModuleSpecDTO Fields**

Recommended fields:

module\_id  
module\_name  
module\_category  
namespace  
base\_iri  
versioned\_iri  
description

owner  
domain\_owner  
ontology\_steward

allowed\_class\_patterns  
allowed\_property\_patterns  
forbidden\_class\_patterns  
forbidden\_property\_patterns

allowed\_import\_modules  
forbidden\_import\_modules  
allowed\_reference\_modules  
dependency\_direction

external\_standard\_refs  
mapping\_module\_refs

impact\_level  
semver  
version  
status  
valid\_from  
valid\_until  
deprecated\_at  
replacement\_module  
change\_reason

requires\_review  
requires\_reasoner\_check  
requires\_shacl\_validation  
requires\_regression\_test

## **25.2 impact\_level Values**

LOW  
MEDIUM  
HIGH  
CRITICAL

Meaning:

LOW  
→ Changes at the level of annotations, descriptions, or optional metadata

MEDIUM  
→ Adding a new class, new optional property, or new mapping

HIGH  
→ Changing domain / range, strengthening a SHACL rule, or making a major mapping change

CRITICAL  
→ Changing Core, changing ObjectProperty boundaries, changing safety-critical classes, or changing the meaning of Action / State / Evidence

CRITICAL changes require approval from all of the following:

Domain Owner  
Ontology Steward  
Safety Owner  
Platform Architect

For Evidence Module or privacy-related changes, the following additional approvals are required:

Audit Owner  
Privacy / Compliance Owner

---

# **26\. CrossModuleReferenceSpecDTO**

References between modules are managed through CrossModuleReferenceSpecDTO.

## **26.1 CrossModuleReferenceSpecDTO Fields**

Recommended fields:

reference\_id  
source\_module  
target\_module  
source\_class  
target\_class  
reference\_type  
property\_ref  
allowed\_cardinality  
semantic\_reason  
is\_required  
is\_bidirectional  
requires\_mapping\_layer  
impact\_level  
affected\_downstream\_modules  
owner  
version  
status  
valid\_from  
valid\_until

## **26.2 reference\_type Values**

SUBCLASS\_OF  
OBJECT\_PROPERTY  
DATA\_PROPERTY  
EQUIVALENT\_CLASS  
EQUIVALENT\_PROPERTY  
MAPPING\_ONLY  
ANNOTATION\_ONLY  
MEDIATION\_CONTEXT

---

# **27\. ObjectPropertyBoundarySpecDTO**

A separate specification is used to prevent ObjectProperty bypass contamination.

## **27.1 ObjectPropertyBoundarySpecDTO Fields**

Recommended fields:

property\_id  
property\_module  
property\_name

domain\_class  
range\_class  
domain\_module  
range\_module

is\_cross\_domain\_property  
requires\_core\_abstraction  
requires\_mediation\_concept  
mediation\_concept\_ref

allowed\_domain\_modules  
allowed\_range\_modules

is\_runtime\_only\_relation  
requires\_mapping\_layer  
requires\_shacl\_validation

impact\_level  
affected\_downstream\_modules  
boundary\_violation\_status  
owner  
version  
status  
valid\_from  
valid\_until

## **27.2 boundary\_violation\_status Values**

NO\_VIOLATION  
DIRECT\_DOMAIN\_COUPLING\_DETECTED  
CORE\_ABSTRACTION\_REQUIRED  
MEDIATION\_CONCEPT\_REQUIRED  
MAPPING\_LAYER\_REQUIRED  
FORBIDDEN\_REFERENCE  
UNDER\_REVIEW

---

# **28\. SemanticAdapterSpecDTO**

The External Mapping Module is managed as a Semantic Adapter.

## **28.1 SemanticAdapterSpecDTO Fields**

Recommended fields:

adapter\_id  
adapter\_name  
mapping\_module  
external\_standard  
external\_schema\_version  
internal\_ontology\_module  
internal\_ontology\_version

mapping\_rules\_ref  
mapping\_conflict\_resolution\_strategy  
compatibility\_status  
hot\_swap\_supported  
rollback\_supported  
previous\_adapter\_ref  
next\_adapter\_ref

validation\_policy\_ref  
shacl\_shape\_refs  
test\_dataset\_refs

impact\_level  
affected\_downstream\_modules  
effective\_from  
superseded\_by  
owner  
version  
status

## **28.2 compatibility\_status Values**

DRAFT  
ACTIVE  
COMPATIBLE  
PARTIALLY\_COMPATIBLE  
INCOMPATIBLE  
DEPRECATED  
RETIRED  
BLOCKED

## **28.3 mapping\_conflict\_resolution\_strategy Values**

PREFER\_INTERNAL  
PREFER\_EXTERNAL  
PREFER\_NEWER\_VERSION  
PREFER\_HIGHER\_TRUST\_MAPPING  
MANUAL\_REVIEW  
BLOCK\_ON\_CONFLICT

---

# **29\. ModuleValidationResultDTO**

The runtime validation layer must create ModuleValidationResultDTO.

## **29.1 ModuleValidationResultDTO Fields**

Recommended fields:

validation\_id  
module\_id  
validation\_type  
validation\_target  
validation\_status

violated\_rule\_refs  
violation\_severity  
violation\_message

affected\_downstream\_modules  
requires\_reasoner\_check  
requires\_shacl\_validation  
requires\_manual\_review

created\_at  
validated\_by  
trace\_id  
correlation\_id

## **29.2 validation\_type Values**

IMPORT\_DIRECTION\_CHECK  
DAG\_CYCLE\_CHECK  
CORE\_PURITY\_CHECK  
DOMAIN\_POLLUTION\_CHECK  
OBJECT\_PROPERTY\_BOUNDARY\_CHECK  
VENDOR\_POLLUTION\_CHECK  
AI\_POLLUTION\_CHECK  
MAPPING\_ISOLATION\_CHECK  
MAPPING\_CONFLICT\_CHECK  
SHACL\_RUNTIME\_CHECK  
REASONER\_CONSISTENCY\_CHECK  
SEMVER\_COMPATIBILITY\_CHECK  
IMPACT\_LEVEL\_CHECK

---

# **30\. Runtime Module Boundary Validation Rule**

Document rules alone are not enough.

When actual TTL files, Python classes, registries, and mappings are created, the runtime validator must validate them.

Required validators:

ModuleDependencyValidator  
ObjectPropertyBoundaryValidator  
ImportCycleValidator  
CorePurityValidator  
DomainPollutionValidator  
VendorPollutionValidator  
AIPollutionValidator  
MappingIsolationValidator  
MappingConflictValidator  
SHACLRuntimeValidator  
ReasonerConsistencyValidator  
SemVerCompatibilityValidator  
ImpactLevelValidator

Example validation rules:

Core module must not import domain module.  
Core-upper must not import core-crosscutting.  
Domain module object property must not directly range another domain class.  
External vendor class must not appear in core module.  
AI module must not define ApprovedAction as equivalent class.  
Mapping module must not mutate internal class definitions.  
Runtime registry must not reference retired ontology module.  
Circular module dependency is prohibited.  
Runtime safety path must not depend on full OWL reasoning.  
CRITICAL impact change must require multi-owner approval.

---

# **31\. CI/CD Validation Rule**

Ontology Module Boundary validation must run automatically in the CI/CD pipeline.

## **31.1 Required CI/CD Steps**

TTL syntax validation  
owl:imports validation  
DAG cycle validation  
Core purity validation  
Domain pollution validation  
ObjectProperty boundary validation  
Mapping isolation validation  
Mapping conflict validation  
SHACL validation  
Reasoner consistency check  
SemVer compatibility check  
Impact level approval check  
Regression test

## **31.2 Recommended Tools**

ROBOT  
Apache Jena  
SHACL engine  
Owlready2  
Pellet / HermiT  
Custom Python validator  
pytest  
pre-commit hook  
GitHub Actions / GitLab CI

## **31.3 CI/CD Principles**

Ontology boundary violation blocks merge.  
CRITICAL impact change requires explicit approval.  
Runtime safety-related ontology changes require SHACL and regression test.  
Mapping adapter update must pass compatibility test.

---

# **32\. Module Ownership Rule**

Each ontology module must have an owner.

Recommended ownership structure:

Core Upper Module  
→ Platform Ontology Steward

Core Crosscutting Module  
→ Platform Ontology Steward \+ Architecture Owner

Construction Module  
→ Construction Domain Owner \+ Ontology Steward

Industrial Module  
→ Industrial Systems Owner \+ Ontology Steward

Robot Module  
→ Robotics Owner \+ Ontology Steward

Policy Module  
→ Policy Owner \+ Safety Owner

AI Module  
→ AI Platform Owner \+ Governance Owner

Evidence Module  
→ Audit Owner \+ Safety Owner \+ Ontology Steward

External Mapping Module  
→ Integration Owner \+ Ontology Steward

The Module owner is responsible for the following:

Approval of class additions  
Approval of property additions  
Approval of ObjectProperty domain / range  
Approval of module imports  
Approval of breaking changes  
Approval of impact level  
Approval of deprecation  
Approval of external mappings  
Confirmation that SHACL validation passes  
Confirmation that reasoner consistency checks pass  
Confirmation of runtime compatibility

---

# **33\. SemVer Versioning Rule**

Ontology Modules follow Semantic Versioning.

Format:

MAJOR.MINOR.PATCH

Examples:

core-upper 1.0.0  
core-crosscutting 1.2.0  
construction 0.8.3  
robot 0.7.1  
mapping-ifc 0.3.0

## **33.1 PATCH Change**

PATCH is a modification that does not change the semantic structure.

Examples:

Typo correction  
Label correction  
Comment enhancement  
Annotation enhancement  
Adding non-breaking metadata

## **33.2 MINOR Change**

MINOR is a backward-compatible change.

Examples:

Adding a new class  
Adding a new optional property  
Adding an annotation  
Adding an external mapping  
Adding a SHACL warning rule  
Enhancing a description  
Adding a new mapping adapter  
Adding a new validation rule

## **33.3 MAJOR Change**

MAJOR is a breaking change.

Examples:

Changing a class IRI  
Changing a property IRI  
Deleting a class  
Deleting a property  
Changing domain / range  
Strengthening cardinality  
Changing a superclass  
Changing module dependency direction  
Removing an existing mapping  
Relaxing an ObjectProperty boundary rule  
Changing Core to reference Domain

A MAJOR change requires a separate migration plan and downstream impact analysis.

---

# **34\. Deprecation Rule**

Ontology classes, properties, and modules are not deleted immediately.

Recommended process:

Change status to DEPRECATED  
Specify replacement\_class or replacement\_property  
Operate a dual-read period  
Maintain mapping  
Migrate downstream consumers  
Reasoner regression test  
SHACL validation test  
Verify audit compatibility  
Change status to RETIRED  
Remove in a major version if necessary

Recommended dual-read period:

LOW impact: minimum 14 days  
MEDIUM impact: minimum 30 days  
HIGH impact: minimum 60 days  
CRITICAL impact: minimum 90 days or Safety Owner approval required

---

# **35\. Governance and Validation Rule**

Ontology Module changes must go through a governance process.

High-risk module changes must pass the following validations:

ontology review  
domain owner approval  
reasoner consistency check  
SHACL validation  
registry compatibility check  
mapping compatibility check  
runtime impact analysis  
audit compatibility check  
object property boundary check  
DAG cycle check  
impact level review  
downstream module impact review

The following modules require stricter review:

Core Upper Module  
Core Crosscutting Module  
Policy Module  
Evidence Module  
Action Module  
State Module  
External Mapping Module

---

# **36\. Core Scenarios**

## **36.1 Scenario 1: Where Does Worker Belong?**

Problem:

Worker is a construction-site worker.  
But Worker is also an Agent.

Modeling:

construction:Worker  
  subClassOf core\_upper:HumanAgent

Judgment:

Worker itself belongs in the Construction Module.  
HumanAgent belongs in the Core Upper Module.

## **36.2 Scenario 2: Where Does GasSensor Belong?**

Problem:

GasSensor is an industrial sensor.  
But it also generates evidence.

Modeling:

industrial:GasSensor  
  subClassOf industrial:Sensor

industrial:GasSensor  
  core\_cross:generatesEvidence evidence:SensorObservationEvidence

Judgment:

The GasSensor class belongs in the Industrial Module.  
SensorObservationEvidence belongs in the Evidence Module.

## **36.3 Scenario 3: Connecting Robot Mission and Construction Zone**

Problem:

RobotMission is in the Robot Module, and Zone is in the Construction Module.  
If the two are strongly coupled directly, module coupling increases.

Modeling:

robot:RobotMission  
  core\_cross:hasOperationalContext core\_cross:OperationalContext

core\_cross:OperationalContext  
  core\_cross:hasLocation core\_upper:Location

construction:WorkZone  
  subClassOf core\_upper:Location

Judgment:

Robot Mission does not directly depend on Construction Zone as a class dependency.  
It connects through OperationalContext and Location.

## **36.4 Scenario 4: Preventing ObjectProperty Bypass Contamination**

Problem:

In the Robot Module, someone wants to set the range of `robot:operatesIn` to `construction:WorkZone`.

Prohibited modeling:

robot:operatesIn  
  rdfs:domain robot:Robot  
  rdfs:range construction:WorkZone

Allowed modeling:

robot:operatesIn  
  rdfs:domain robot:Robot  
  rdfs:range core\_upper:Location

construction:WorkZone  
  subClassOf core\_upper:Location

Or:

robot:RobotMission  
  core\_cross:hasOperationalContext core\_cross:OperationalContext

Judgment:

An ObjectProperty range must not directly reference another Domain class.  
Use Core abstraction or a Mediation Concept.

## **36.5 Scenario 5: ActionCandidate Generated by LLM**

Problem:

The LLM proposed ACTION\_EVACUATE\_ZONE.

Modeling:

ai:ActionCandidate  
  subClassOf core\_cross:Candidate

ai:ActionCandidate  
  core\_cross:suggestsAction action:SafetyAction

Prohibited:

ai:ActionCandidate  
  equivalentTo action:ApprovedAction

Judgment:

AI output can only go up to candidate.  
ApprovedAction must pass through the Action / Policy / Safety Gate boundary.

## **36.6 Scenario 6: Connecting IFC and Internal Construction Ontology**

Problem:

IFC’s IfcWall must be connected to the internal construction:Wall.

Modeling:

mapping:IFC\_IfcWall\_to\_ConstructionWall  
  mapping:externalClass ifc:IfcWall  
  mapping:internalClass construction:Wall  
  mapping:relationType mapping:EquivalentClassMapping

Judgment:

IFC mapping is not mixed directly into the Construction Module.  
It is managed in the External Mapping Module.

## **36.7 Scenario 7: Vendor Robot API Change**

Problem:

Vendor Robot API changed from v1 to v2.  
However, the internal robot ontology must remain unchanged.

Processing:

mapping:VendorRobotAPI\_v1\_to\_robot\_RobotMission  
  status \= DEPRECATED

mapping:VendorRobotAPI\_v2\_to\_robot\_RobotMission  
  status \= ACTIVE

Judgment:

The internal `robot:RobotMission` is not changed.  
Only the Mapping Adapter is replaced.

## **36.8 Scenario 8: Connecting Evidence Model and Evidence Module**

Problem:

The Evidence Model defined `clock_drift_estimate_ms`, `time_trust_level`, `trust_upgrade_status`, and `privacy_lifecycle_status`.  
Where should these be located in the Ontology Module Boundary?

Modeling:

evidence:EvidenceRecord  
  subClassOf core\_cross:Evidence

evidence:EvidenceRecord  
  evidence:hasTimeTrustLevel evidence:TimeTrustLevel

evidence:EvidenceRecord  
  evidence:hasTrustUpgradeStatus evidence:TrustUpgradeStatus

evidence:EvidenceRecord  
  evidence:hasPrivacyLifecycleStatus evidence:PrivacyLifecycleStatus

evidence:EvidenceRecord  
  evidence:hasClockDriftEstimate xsd:integer

Judgment:

Operational fields are managed in EvidenceRecordDTO.  
Their semantic classes and properties are defined in the Evidence Ontology Module.  
Core has only the upper-level concept Evidence.

---

# **37\. MVP Ontology Module Set**

For the MVP, the following modules should be implemented first.

core-upper  
core-crosscutting  
construction  
industrial  
robot  
policy  
evidence  
event  
state  
action  
ai  
mapping

---

# **38\. Recommended File Structure**

## **38.1 Ontology Source Structure**

ontology/  
  core\_upper/  
    core\_upper.ttl  
    core\_upper\_classes.py  
    core\_upper\_properties.py

  core\_crosscutting/  
    core\_crosscutting.ttl  
    core\_crosscutting\_classes.py  
    core\_crosscutting\_properties.py

  construction/  
    construction.ttl  
    construction\_classes.py  
    construction\_properties.py

  industrial/  
    industrial.ttl  
    industrial\_classes.py  
    industrial\_properties.py

  robot/  
    robot.ttl  
    robot\_classes.py  
    robot\_properties.py

  policy/  
    policy.ttl  
    policy\_classes.py  
    policy\_properties.py

  evidence/  
    evidence.ttl  
    evidence\_classes.py  
    evidence\_properties.py

  event/  
    event.ttl  
    event\_classes.py  
    event\_properties.py

  state/  
    state.ttl  
    state\_classes.py  
    state\_properties.py

  action/  
    action.ttl  
    action\_classes.py  
    action\_properties.py

  ai/  
    ai.ttl  
    ai\_classes.py  
    ai\_properties.py

  mapping/  
    external\_mappings.ttl  
    ifc\_mapping.py  
    sosa\_mapping.py  
    prov\_o\_mapping.py  
    vendor\_mapping.py

## **38.2 Registry Structure**

ontology\_registry/  
  ontology\_module\_spec.py  
  cross\_module\_reference\_spec.py  
  object\_property\_boundary\_spec.py  
  semantic\_adapter\_spec.py  
  module\_validation\_result.py  
  module\_dependency\_policy.py  
  namespace\_registry.py  
  iri\_registry.py  
  semver\_policy.py  
  deprecation\_policy.py  
  impact\_level\_policy.py  
  validation\_policy.py

## **38.3 Validation Structure**

ontology\_validation/  
  module\_dependency\_validator.py  
  import\_cycle\_validator.py  
  core\_purity\_validator.py  
  domain\_pollution\_validator.py  
  object\_property\_boundary\_validator.py  
  vendor\_pollution\_validator.py  
  ai\_pollution\_validator.py  
  mapping\_isolation\_validator.py  
  mapping\_conflict\_validator.py  
  shacl\_runtime\_validator.py  
  reasoner\_consistency\_validator.py  
  semver\_compatibility\_validator.py  
  impact\_level\_validator.py

---

# **39\. Recommended Implementation Order**

The MVP implementation order should be as follows.

OntologyModule enum  
OntologyModuleCategory enum  
NamespaceRegistry  
IRIRegistry  
ImpactLevel enum  
SemVerPolicy  
OntologyModuleSpecDTO  
ObjectPropertyBoundarySpecDTO  
ObjectPropertyBoundaryValidator  
CrossModuleReferenceSpecDTO  
SemanticAdapterSpecDTO  
ModuleValidationResultDTO  
ModuleDependencyPolicy  
Core Upper Module skeleton  
Core Crosscutting Module skeleton  
Construction Module skeleton  
Industrial Module skeleton  
Robot Module skeleton  
Policy Module skeleton  
Evidence Module skeleton  
Event Module skeleton  
State Module skeleton  
Action Module skeleton  
AI Module skeleton  
External Mapping Module skeleton  
ObjectProperty Boundary Rule  
Mediation Concept Rule  
SHACL validation rule  
Reasoner consistency check  
Module import test  
DAG cycle test  
Cross-module reference test  
Mapping adapter compatibility test  
Registry compatibility test  
CI/CD validation pipeline

ObjectPropertyBoundarySpecDTO and ObjectPropertyBoundaryValidator must be implemented early in the MVP.

Reason:

Property boundary contamination occurs more frequently than class boundary contamination.  
If it is not blocked early, later refactoring cost becomes large.

---

# **40\. Final Principle**

The Ontology Module Boundary is the semantic boundary line of the platform.

Core must be small and stable.  
Core is divided into core-upper and core-crosscutting.  
Domain Modules must extend Core.  
Core must not reference Domain.  
Vendor-specific concepts must not enter Core.  
AI output must not become truth or ApprovedAction.  
Registry manages operational rules, while Ontology defines semantic structure.  
The Evidence Module must semantically accommodate time trust, attested extraction, conflict resolution, and privacy lifecycle from the Evidence Model.  
The External Mapping Module connects external standards with the internal semantic system.  
The Mapping Module is managed as a hot-swappable Semantic Adapter.  
Mapping conflicts are resolved in the Mapping Layer and must not change the internal ontology.  
Not only class boundaries but also ObjectProperty domain / range boundaries must be validated.  
Complex cross-domain relationships are mediated through Mediation Concepts.  
OWL Reasoner is for static consistency checks, and the runtime guardrail must be SHACL.  
Module Boundary must be enforced not by document rules alone, but by validators and the CI/CD pipeline.  
Ontology changes must be managed through SemVer and impact\_level.

The final principles are as follows:

Different domains, one semantic core.  
Different core layers, one stable foundation.  
Different modules, one dependency discipline.  
Different properties, one boundary rule.  
Different contexts, one mediation pattern.  
Different vendors, one semantic adapter layer.  
Different mappings, one conflict policy.  
Different registries, one ontology backbone.  
Different AI outputs, one approval boundary.  
Different standards, one alignment layer.  
Different reasoners, one validation discipline.  
Different changes, one SemVer governance.  
Different meanings, one controlled ontology system.

# Ontology Centric "Module Boundary”

