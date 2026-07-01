# **Ontology foundation “Upper Ontology and Standards Alignment Guideline”**

## **1\. Purpose**

This document defines how the LEDO Industrial Ontology Foundation aligns with upper ontologies and international standards.

LEDO is not an ontology dependent on a single industry. LEDO aims to provide an industrial ontology foundation capable of supporting construction, manufacturing, energy, robotics, facilities, safety, logistics, operations, control rooms, and Physical AI.

Therefore, at the Foundation level, the following must be clearly defined.

Which concepts belong in the Foundation  
Which concepts belong in Domain Modules  
How to use upper ontologies such as BFO  
Whether to copy or map industrial standards  
How to define the boundary between external standards and the internal canonical model  
How standards alignment connects to the runtime execution structure

The core purposes are as follows.

Keep the LEDO Foundation small but strong.  
Prevent category confusion through upper ontology alignment.  
Create a structure compatible with international standards.  
Treat external standards as mapping targets, not direct dependencies.  
Prevent Domain Modules from contaminating the Foundation.

---

## **2\. Position Within the Overall LEDO Structure**

This document belongs to the following location.

04\_ontology\_foundation/  
  02\_upper\_ontology\_and\_standards/  
    upper\_ontology\_and\_standards.md

This document is connected to the following documents.

00\_ontology\_foundation\_report  
→ Overall philosophy and principles of the Foundation

01\_semantic\_web\_technology\_stack  
→ Responsibility separation among RDF, OWL, SHACL, SPARQL, SKOS, PROV-O, and related technologies

03\_owl\_modeling\_principles  
→ OWL class, property, and axiom modeling principles

04\_reasoning\_and\_constraint\_model  
→ Boundaries among reasoning, validation, policy, and Safety Gate

05\_relationship\_and\_property\_design  
→ Relationship and property design principles

06\_ontology\_governance\_and\_versioning  
→ Standards mapping changes, axiom changes, and version governance

---

## **3\. Core Principles**

The upper ontology and standards alignment principles of LEDO are as follows.

Upper ontology provides category discipline.  
International standards provide compatibility and export-grade design.  
External standards are mapped, not copied.  
The Foundation must remain small.  
Domain details must be separated into Domain Modules.  
Runtime execution safety is not guaranteed by standard names alone.  
Standards alignment must connect to Evidence, Policy, Safety Gate, and Audit.

The most important principles are as follows.

Standards are aligned, not blindly copied.  
BFO is used for category discipline, not domain bloat.

---

## **4\. Boundary Between Foundation and Domain Modules**

The LEDO Foundation contains only the upper structures commonly required across industrial domains.

The following concepts may belong in the Foundation.

Entity  
Agent  
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
Identifier

The following concepts must not be placed directly into the Foundation.

Detailed classifications of industry-specific equipment  
Detailed steps of a specific manufacturing process  
Detailed names of specific field operations  
Detailed clauses of a specific national regulation  
Vendor-specific API schemas  
Specific PLC tag structures  
The full set of detailed BIM object attributes  
Internal low-level control commands of a specific robot model

These should be placed in Domain Modules or Mapping Modules.

Foundation  
→ Common semantic structure

Domain Module  
→ Industry-specific detailed concepts

Mapping Module  
→ Connection to external standards, vendor systems, and data schemas

Runtime Module  
→ Actual processing, validation, execution requests, feedback, and audit

---

## **5\. Purpose of Using BFO**

BFO is used in LEDO as an upper ontology alignment reference.

The purpose of using BFO is not to make the Foundation unnecessarily difficult. The purpose is to prevent category confusion.

For example, the following must not be confused.

Physical object and process  
Role and person  
Function and equipment  
Risk state and risk cause  
Spatial zone and physical equipment  
Observation act and observation result  
Policy document and actual execution

BFO provides an upper-level reference that helps maintain these distinctions.

---

## **6\. Core BFO Distinctions**

The following BFO-oriented distinctions are especially important in the LEDO Foundation.

Continuant  
→ Something that persists through time

Occurrent  
→ Something that happens or unfolds through time

Material Entity  
→ A physically existing entity

Immaterial Entity  
→ A non-material entity that can still be ontologically treated, such as a boundary, space, location, or zone

Process  
→ A process that unfolds through time

Role  
→ A role performed in a specific context

Function  
→ A function that an entity is designed or expected to perform

Disposition  
→ A tendency or potential that may be realized under certain conditions

Quality  
→ A characteristic possessed by an entity

Site / Spatial Region  
→ A spatial location or region

Information Artifact  
→ An information object such as a policy, document, model, or record

In LEDO, these distinctions guide class design, property design, axiom design, and reasoning design.

In particular, spatial concepts such as `Zone`, `DangerZone`, `RestrictedZone`, `GeofencingBoundary`, and `SpeedLimitedZone` may have operational impact even when there is no physical wall. From a BFO-oriented perspective, such concepts are aligned with `Immaterial Entity`, `Site`, or `Spatial Region`.

This distinction is important for GeoSPARQL, spatial containment relations, danger zone judgment, access restriction, speed limitation, robot path constraints, and control room zone configuration.

The core principles are as follows.

Not every zone means a physical wall.  
Logical boundaries can also affect runtime safety and policy decisions.  
Logical spatial boundaries must be explicitly aligned with Immaterial Entity / Site / Spatial Region.

---

## **7\. BFO-Oriented Mapping of LEDO Concepts**

| LEDO Concept | BFO-Oriented Category | Description | Mapping Rationale |
| ----- | ----- | ----- | ----- |
| Agent | material entity or role-bearing entity | An entity that performs actions or participates in decision-making | It may be a physical entity or a subject performing a role in a specific context |
| HumanAgent | material entity | A human agent | A human is a physical entity that persists through time |
| RobotAgent | material entity | A physically existing robot agent | A robot exists in physical space and has state and location |
| HumanoidRobot | material entity / object | A humanoid robot individual | It is a physical robotic object and can act as a task-performing subject |
| Sensor | material entity / device-like object | A physical device with an observation function | It is a physical device that can generate observations |
| Actuator | material entity / device-like object | A device that performs physical action | It can act on the physical world in response to external control requests |
| Controller | material entity or system component | A system component that performs a control function | It may be a physical device or digital control component performing a control function |
| Task | planned process | A planned process of execution | It has a beginning and end and unfolds through time |
| InspectionTask | planned process | A task process with an inspection purpose | It is a planned process whose purpose is inspection |
| HighRiskTask | planned process with risk context | A task process connected to risk conditions | The task itself is a process, and high risk is a risk context attached to that process |
| Event | occurrent | An event that occurs through time | It is a change that occurs at a specific time or within a time interval |
| Observation | process or information content entity | An observation act or observation result information | The act of observing is a process, while the result can be managed as an information object |
| Evidence | information artifact | An information object used as a basis for judgment | It is not a physical object itself, but an informational artifact supporting judgment |
| Risk | disposition or risk context | A state or context representing the possibility of harm under certain conditions | It is not necessarily an event that has already occurred, but a potential condition that may lead to harm |
| Zone | immaterial entity / site / spatial region | A spatial region | It is not a physical object, but a spatial area with location and containment relations |
| DangerZone | site with risk context | A spatial region connected to a risk context | The zone is a spatial region, and danger is a risk context attached to it |
| RestrictedZone | site with policy restriction | A spatial region connected to an access restriction policy | It may be policy-restricted even without a physical wall |
| GeofencingBoundary | immaterial entity / spatial boundary | A logically defined spatial boundary | It is not a physical wall, but a non-material boundary used for location-based judgment and control constraints |
| SpeedLimitedZone | spatial region with operational constraint | A spatial region connected to a speed limitation condition | It imposes behavioral constraints on agents or machines within a specific region |
| Policy | information artifact | An operational rule or policy information object | It is not an action itself, but an information object that restricts or permits action |
| Permit | information artifact / authorization record | A permit or approval record | It records an authorization state and is used for execution permission judgment |
| ActionCandidate | information artifact / planned action proposal | A candidate action before execution | It is not actual execution, but a proposed action generated by an agent |
| ExecutionRequest | information artifact / request object | A request passed to an external execution layer | It is not physical control itself, but a request object delivered to an external system |
| AuditRecord | information artifact | An audit record | It records the basis and process of judgment and execution |

This mapping does not mean that LEDO classes are identical to BFO classes. It indicates the upper category discipline that LEDO classes must follow.

---

## **8\. Principles for Using BFO**

The principles for using BFO are as follows.

BFO is used for category discipline in the Foundation.  
BFO is not copied directly as a domain ontology.  
Domain classes must be explicitly aligned with BFO categories.  
Role, Function, Process, and Object must not be confused.  
Physical objects and information objects must not be confused.  
Runtime actions and policy documents must not be confused.  
Physical spaces and logical spatial boundaries must be distinguished, while recognizing that both can be targets of spatial reasoning.

For example, `Policy` is not an actual physical action.  
`ExecutionRequest` is not a physical command itself.  
`ActionCandidate` is not an execution command, but a pre-execution proposed action.  
`GeofencingBoundary` is not a physical wall, but it can affect runtime policy and spatial validation as a non-material spatial boundary.

This distinction is very important for the Safety Gate, GeoSPARQL, and Audit.

---

## **9\. Standards Alignment Levels**

LEDO classifies standards alignment levels into the following three categories.

MUST  
→ A requirement that must be reflected in the Foundation design

SHOULD  
→ A strongly recommended requirement for industrial applicability and extensibility

MAY  
→ A requirement that may be applied depending on domain, customer, country, or certification scope

These levels follow RFC-style requirement language.

---

## **10\. Standards Alignment Matrix**

| Standards Family | LEDO Application Level | Role in the Foundation |
| ----- | ----- | ----- |
| W3C RDF / RDFS | MUST | RDF graph, triple model, basic class/property structure |
| W3C OWL 2 | MUST | Formal ontology, class/property/individual axioms, reasoning |
| W3C SPARQL | MUST | Graph query, semantic retrieval, evidence/audit query |
| W3C SHACL | MUST | ABox data validation, shape constraints |
| W3C SKOS | MUST | Vocabulary system, SLM training structure, multilingual labels |
| W3C PROV-O | SHOULD | Provenance, evidence lineage, source tracking |
| W3C OWL-Time | SHOULD | Time concepts, temporal relations, event timing |
| OGC GeoSPARQL | SHOULD | Space, zone, location, geometry query |
| ISO/IEC 21838 / BFO | MUST | Upper ontology, category discipline |
| IFC / ISO 16739 | SHOULD | External industrial asset alignment, BIM mapping |
| IEC 61508 | SHOULD | Functional safety, safety lifecycle, SIL alignment |
| IEC 61511 | SHOULD | Process safety, safety instrumented system alignment |
| IEC 62541 / OPC UA | SHOULD | Industrial communication, telemetry, external system model |
| IEC 62264 / ISA-95 | SHOULD | Enterprise-control integration boundary |
| ISA/IEC 62443 | MUST | Industrial cybersecurity, OT/ICS security boundary |
| IEEE 1588 | MUST | Time synchronization, clock trust, timestamp reliability |
| ISO robotics safety family | SHOULD | Robot safety reference |
| ISO 8373 | MAY | Robotics vocabulary reference |
| NIST SP 800-53 | SHOULD | Security and privacy control reference |
| NIST AI RMF | SHOULD | AI risk governance reference |
| RFC 2119 / RFC 8174 | MUST | MUST/SHOULD/MAY requirement language |
| FIPA ACL | MAY | Agent communication reference |

---

## **11\. Boundary of Standards Application**

Standards are not copied directly into the LEDO Foundation.

LEDO applies standards in the following way.

Understand the core concepts of the standard.  
Align them with LEDO Foundation categories.  
Extend detailed concepts in Domain Modules when needed.  
Connect external schemas through Mapping Modules.  
Process data at runtime based on canonical objects.  
Keep standards alignment rationale traceable in Audit.

External standards are not the owners of the internal LEDO structure.  
The semantic authority inside LEDO is the Core Ontology Kernel.

---

## **12\. External Standards Alignment Flow**

External standards are connected to LEDO through the following flow.

External Standard Concept  
→ Mapping Module  
→ Canonical Object / Canonical Class  
→ Ontology Binding  
→ Evidence / State / Action / Audit

For example, equipment IDs, BIM object IDs, OPC-UA nodes, PLC tags, and robot state messages from external systems do not directly become ontology individuals.

They are first normalized into canonical identity and canonical objects, and then bound to the ontology.

External ID  
→ Identifier Mapping Record  
→ Canonical Identity  
→ ABox Hash IRI  
→ Ontology Binding

---

## **13\. IFC / BIM Alignment Criteria**

IFC / BIM standards can be connected to industrial assets, spaces, components, and design information.

In LEDO, IFC / BIM plays the following roles.

asset reference  
space reference  
geometry reference  
building/facility component reference  
external design model mapping  
digital twin alignment

However, IFC classes must not be copied directly into the LEDO Foundation.

The principles are as follows.

IFC is an external model.  
The LEDO Foundation is a canonical semantic layer.  
IFC objects are connected to LEDO objects through Mapping Modules.  
Changes to the IFC schema must not directly destabilize the Foundation.

---

## **14\. Example Flow for Mapping IFC Objects**

The basic flow for an IFC-based external object entering LEDO is as follows.

IFC Object  
→ IFC GlobalId / External Identifier  
→ Source System Identifier  
→ Identifier Mapping Record  
→ Canonical Identity  
→ ABox Hash IRI  
→ Canonical Object  
→ Ontology Binding  
→ RDF Reference  
→ Digital Twin Alignment  
→ Evidence / Audit Reference

Assume that a spatial object or facility object from an IFC model enters LEDO. LEDO does not copy that IFC object directly as an internal ontology class. It first records the external identifier and determines which canonical identity the object corresponds to inside LEDO.

The following questions must then be reviewed.

Which LEDO Foundation category does this IFC object belong to?  
Is it a PhysicalObject, Zone, System, or DigitalObject?  
Is this object the same as an existing canonical object?  
Should this object's geometry be used only as a spatial reference?  
Is this object a runtime object that affects World State?  
Is this object only a reference needed for Evidence or Digital Twin alignment?

This flow prevents changes in the IFC schema from directly destabilizing the LEDO Foundation.

The core principles are as follows.

IFC objects may serve as external references for LEDO objects.  
IFC objects must not become the semantic authority of LEDO.

---

## **15\. OPC-UA and Industrial Communication Standards Alignment Criteria**

Industrial communication standards such as OPC-UA are connected to facilities, sensors, control systems, and telemetry.

In LEDO, OPC-UA plays the following roles.

external telemetry source  
industrial communication model  
node identifier source  
equipment state source  
control system integration point

However, OPC-UA nodes or PLC tags must not be turned directly into ontology classes.

The principles are as follows.

An OPC-UA node is a source identifier.  
LEDO canonical identity is managed separately.  
Telemetry enters as raw data and becomes an Observation or State through semantic binding.  
Control requests are not executed by LEDO as low-level commands, but are passed as ExternalControlRequests.

---

## **16\. Example Flow for Mapping OPC-UA Nodes / Telemetry**

The basic flow for an OPC-UA node or telemetry entering LEDO is as follows.

OPC-UA Node  
→ Source System Identifier  
→ Raw Telemetry Record  
→ Normalize  
→ SHACL Validation  
→ Canonical Object Resolution  
→ Observation or State  
→ Ontology Binding  
→ Evidence Binding with PROV-O  
→ World State Update  
→ Event Detection  
→ Audit Reference

Assume that a sensor value enters from an OPC-UA node. This node does not immediately become a LEDO class. The node identifier is recorded as a source identifier, and actual meaning is assigned only after normalization and canonical object resolution.

The review questions are as follows.

Which source system did this node come from?  
Which canonical sensor or system component is this node connected to?  
Is the incoming value an Observation or a State?  
Is the timestamp trustworthy?  
Are the unit and value range normal?  
Can this Observation be used as Evidence?  
Is it fresh enough to update the World State?

This flow prevents changes in OPC-UA or PLC tag structures from contaminating the entire LEDO ontology structure.

The core principles are as follows.

OPC-UA is an external communication and telemetry layer.  
The LEDO Ontology is the canonical semantic layer that gives meaning to that telemetry.

---

## **17\. Functional Safety Standards Alignment Criteria**

Functional safety standards such as IEC 61508 and IEC 61511 are connected to the LEDO safety lifecycle.

In LEDO, these standards support the following.

risk classification  
safety lifecycle alignment  
safety requirement traceability  
evidence-based decision support  
approval and validation process  
safety-related audit

However, the LEDO Foundation does not replace functional safety certification itself.

The principles are as follows.

LEDO supports safety evidence and traceability.  
LEDO does not replace certification by an accredited functional safety authority.  
The Safety Gate performs runtime safety validation.  
Functional safety standards alignment strengthens design and auditability.

---

## **18\. OT / ICS Cybersecurity Standards Alignment Criteria**

Security standards such as ISA/IEC 62443 and NIST SP 800-53 are connected to LEDO governance, access control, audit, network boundaries, and system integrity.

In LEDO, these standards support the following.

role-based access control  
zone and conduit thinking  
asset security boundary  
audit trail  
system hardening reference  
least privilege  
identity and access management  
incident traceability

Security standards connect both to the semantic structure of the Foundation and to the runtime policy layer.

The principle is as follows.

Security is not an add-on.  
Security must be embedded into identity, policy, evidence, execution, and audit.

---

## **19\. IEEE 1588 and Time Synchronization Criteria**

Time synchronization standards such as IEEE 1588 are highly important in LEDO.

In Physical AI and industrial systems, event order is central to judgment. Time is not merely metadata. It is directly connected to Evidence trust, World State trust, Safety Gate trust, and Audit trust.

LEDO must verify the following.

When did the Observation occur?  
When was the Event detected?  
Is the Evidence still fresh?  
When was the ActionCandidate created?  
Did Approval occur after the candidate was created?  
When did Safety Gate validation occur?  
Did Feedback arrive within the expected time window?

If time synchronization is unstable, the following problems may occur.

Event order may be distorted.  
Evidence freshness cannot be trusted.  
It becomes difficult to determine whether the World State is current.  
Approval validity becomes difficult to verify.  
The Safety Gate may validate execution readiness based on outdated state.  
The audit timeline cannot be reconstructed.

Therefore, in LEDO, clock trust is part of evidence trust.

Clock trust is part of evidence trust.  
If clocks are not trustworthy, event order, evidence freshness, approval validity, and Safety Gate validation become unreliable.

The core principles are as follows.

Timestamp is safety-critical.  
Clock trust is evidence-critical.  
Time synchronization is not an infrastructure detail; it is part of semantic and safety validity.

---

## **20\. Robotics and Physical AI Standards Alignment Criteria**

Robotics and Physical AI standards are connected to RobotAgent, HumanoidRobot, autonomous systems, controllers, actuators, tasks, and safety boundaries.

In LEDO, robotics-related standards are used for the following.

robot vocabulary reference  
robot safety boundary  
human-robot collaboration context  
autonomous task execution context  
robot state interpretation  
external robot middleware mapping

However, LEDO does not replace robot controllers.

The principle is as follows.

LEDO interprets robot meaning and governs high-level action requests.  
Robot middleware and control systems execute physical control.

---

## **21\. NIST AI RMF and AI Governance Alignment Criteria**

AI risk governance standards are connected to LEDO agent interpretation, model output handling, human approval, audit, and risk governance.

In LEDO, AI output is not Evidence. AI output is not truth. AI output is candidate interpretation.

The core principles are as follows.

LLM / SLM output is candidate interpretation.  
Agent output is not truth.  
AI output must be supported by evidence before decision.  
High-risk action requires policy, approval, and Safety Gate validation.

AI output may initiate investigation or generate an ActionCandidate. However, AI output must not directly become Evidence, Decision, Approval, or ExecutionRequest.

In LEDO, AI output may initiate investigation or generate an ActionCandidate,  
but it must not directly become Evidence, Decision, Approval, or ExecutionRequest.

AI governance standards connect to the following.

model risk management  
human oversight  
explainability support  
traceability  
bias and failure review  
incident investigation

---

## **22\. RFC 2119 / 8174 Requirement Language**

LEDO documents use the following expressions to clearly define requirement levels.

MUST  
→ Required

MUST NOT  
→ Strictly prohibited

SHOULD  
→ Strongly recommended

SHOULD NOT  
→ Strongly discouraged

MAY  
→ Permitted depending on context

This requirement language is used consistently across design documents, implementation guides, validation rules, and governance rules.

---

## **23\. RFC 2119 Requirements and SHACL Severity Mapping**

LEDO does not use requirement language only at the document level. Requirement levels may be connected to SHACL validation severity.

The default mapping is as follows.

| Requirement Level | SHACL Severity | Runtime Handling Criteria |
| ----- | ----- | ----- |
| MUST | sh:Violation | Block pipeline or reject state update |
| MUST NOT | sh:Violation | Immediately block and generate a security/safety event candidate |
| SHOULD | sh:Warning | Allow flow, but record warning log, audit, and review target |
| SHOULD NOT | sh:Warning | Flow may be allowed, but governance review or policy review is required |
| MAY | sh:Info | Record as reference information; do not block |

Examples are as follows.

An Observation MUST have a timestamp.  
→ Missing timestamp becomes sh:Violation  
→ Evidence Binding or World State Update is blocked

An EvidenceBundle SHOULD have source lineage.  
→ Insufficient source lineage becomes sh:Warning  
→ Flow is allowed, but audit warning is recorded

A SKOS concept MAY have an altLabel.  
→ Missing altLabel becomes sh:Info or no validation  
→ Pipeline is not blocked

This mapping becomes the basis for governance automation.

MUST requirements connect to blocking validation.  
SHOULD requirements connect to warnings and review targets.  
MAY requirements are managed as reference information.

However, not every RFC 2119 sentence automatically becomes a SHACL shape. Only requirements that require actual runtime validation are implemented as SHACL shapes.

The core principles are as follows.

Requirement language must be operationalizable.  
MUST should map to blocking validation when it affects safety, identity, evidence, or execution.  
SHOULD should map to warning validation when it affects quality, governance, or completeness.  
MAY should not block runtime flow.

---

## **24\. Runtime Flow and Standards Alignment**

Standards alignment does not end as document-level mapping. It must have an actual role inside the runtime flow.

Raw Data  
→ May enter from an external standard source

Normalize  
→ Requires standard-specific field mapping

Canonical Object  
→ Converts external IDs into internal canonical identity

Ontology Binding  
→ Aligns with BFO / OWL / RDFS categories

Evidence Binding  
→ Connects PROV-O and source lineage

World State Update  
→ Requires time synchronization and state validity

Event Detection  
→ May reflect risk, safety, and security standard criteria

ActionCandidate  
→ AI output is treated only as a candidate

Candidate Validation  
→ Validated using OWL, SHACL, SPARQL, and policy criteria

Safety Gate  
→ Performs runtime safety validation

ExecutionRequest  
→ Adapter mapping to external control standards

Feedback  
→ Connects execution result to evidence and audit

Audit  
→ Preserves standards alignment rationale and full trace

---

## **25\. Domain Module Extension Criteria**

Domain Modules extend the Foundation, but must not contaminate it.

When creating a new class in a Domain Module, the following must be checked.

Which Foundation category does it belong under?  
Is it a continuant or occurrent under BFO?  
Is it a physical object or information object?  
Is it a role, function, or process?  
Can it be represented using an existing class?  
Is a new property needed, or is an existing property sufficient?  
Does it require mapping to an external standard?  
Does it require a SHACL shape?  
Does it require SKOS term registration?  
Does it have competency questions?

The Domain Module extension flow is as follows.

1\. Identify Domain Concept  
   → Define the domain concept to be modeled.

2\. Foundation Category Mapping  
   → Check which Foundation category it belongs under, such as Agent, Sensor, Task, Event, Risk, Zone, or Evidence.

3\. BFO-oriented Category Check  
   → Check whether it is a continuant, occurrent, material entity, process, role, or function.

4\. External Standard Mapping  
   → Check whether it needs to connect to external standards such as IFC, OPC-UA, ISO, IEC, IEEE, or NIST.

5\. TBox Class Extension  
   → Add a class to the TBox if a new class is necessary.

6\. Property Alignment  
   → Check whether existing properties are sufficient and design a new property only when unavoidable.

7\. Axiom Review  
   → Review whether subclass, domain/range, disjointness, and restrictions are safe.

8\. SHACL Shape Design  
   → Design shapes for ABox data validation if needed.

9\. SKOS Concept Registration  
   → Register terms, labels, definitions, synonyms, and field expressions.

10\. Competency Question Test  
   → Check which questions this concept must help answer.

11\. Governance Review  
   → Review version, deprecation, mapping, and axiom impact.

The summarized flow is as follows.

Domain Concept  
→ Foundation Category Mapping  
→ BFO Category Check  
→ External Standard Mapping  
→ TBox Class Extension  
→ Property Alignment  
→ Axiom Review  
→ SHACL Shape Design  
→ SKOS Concept Registration  
→ Competency Question Test  
→ Governance Review

---

## **26\. Anti-Patterns**

| Anti-pattern | Problem | Possible Damage | Alternative / Expected Benefit |
| ----- | ----- | ----- | ----- |
| Copying external standard classes directly into the Foundation | The Foundation becomes dependent on a specific standard | The whole structure becomes unstable when the standard changes | Use Mapping Modules. This absorbs the impact of external standard changes. |
| Exposing BFO too directly and excessively | Domain users may find it difficult to understand | Modeling complexity increases | Use BFO as internal category discipline. This preserves both structural rigor and practical usability. |
| Placing domain details into the Foundation | The Foundation becomes bloated | Expansion into other industrial domains becomes difficult | Separate them into Domain Modules. This keeps the Foundation small and strong. |
| Creating ontology classes directly from OPC-UA nodes | Source identifiers and semantic classes are confused | Ontology contamination | Use canonical identity and mapping records. This separates source schemas from ontology meaning. |
| Using IFC objects directly as internal objects | Internal structure becomes dependent on an external schema | BIM changes affect the internal structure | Use an IFC mapping layer. This preserves Digital Twin alignment while protecting the Core Ontology. |
| Treating AI output as Evidence | Unverified judgment is turned into fact | Wrong actions and audit failure | Use AI output only as a candidate. This preserves evidence-based judgment. |
| Replacing the Safety Gate with references to standards documents | Runtime validation is missing | Execution risk increases | Use deterministic validation rules. This validates execution-time safety based on actual current state. |
| Ignoring time synchronization | Evidence order and freshness become unclear | Incorrect state judgment | Apply clock trust and timestamp governance. This secures evidence and audit timeline reliability. |
| Changing standards mappings without governance | Semantic relations break | Reasoning, validation, and audit errors | Apply mapping review and versioning. This controls change impact. |
| Treating logical spatial boundaries only as string attributes | Spatial reasoning becomes impossible | Errors in geofencing, access restriction, and speed limitation judgment | Model GeofencingBoundary and RestrictedZone as Immaterial Entity / Spatial Region categories. |
| Not connecting MUST / SHOULD / MAY to validation severity | Requirements remain only in documents and do not operate at runtime | Validation automation fails and governance becomes inconsistent | Map RFC 2119 requirements to SHACL severity. |

---

## **27\. Core Principles**

The Foundation must be small but strong.  
BFO provides category discipline.  
Immaterial Entity / Site / Spatial Region are important for modeling logical spatial boundaries.  
External standards are mapped, not copied.  
Domain details are separated into Domain Modules.  
Mapping Modules absorb the impact of external schema changes.  
The Core Ontology Kernel is the semantic authority.  
Runtime safety is guaranteed by Safety Gate validation, not by standard names.  
AI output is a candidate, not Evidence.  
Timestamp and clock trust are safety-critical.  
RFC 2119 requirements should be operationalized through SHACL severity when needed.  
Standards alignment must connect to Evidence, Policy, Safety Gate, and Audit.

The final principles are as follows.

LEDO follows standards, but does not become dependent on them.  
LEDO uses upper ontology to establish semantic order,  
and uses international standards to secure industrial compatibility and auditability.

