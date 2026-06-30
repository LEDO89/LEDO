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

# **상위 온톨로지 및 표준 정렬 기준서**

## **1\. 목적**

이 문서는 LEDO 산업 온톨로지 Foundation이 상위 온톨로지와 국제 표준을 어떻게 정렬할 것인지 정의한다.

LEDO는 특정 산업 하나에만 종속된 온톨로지가 아니다. LEDO는 건설, 제조, 에너지, 로봇, 설비, 안전, 물류, 운영, 관제, Physical AI를 모두 수용할 수 있는 산업 온톨로지 기반을 목표로 한다.

따라서 Foundation 단계에서는 다음을 명확히 해야 한다.

어떤 개념을 Foundation에 둘 것인가  
어떤 개념을 Domain Module에 둘 것인가  
BFO 같은 상위 온톨로지를 어떻게 사용할 것인가  
산업 표준을 복사할 것인가, 매핑할 것인가  
외부 표준과 내부 canonical model 사이의 경계를 어떻게 둘 것인가  
표준 정렬이 runtime 실행 구조와 어떻게 연결되는가

핵심 목적은 다음과 같다.

LEDO Foundation을 작고 강하게 유지한다.  
상위 온톨로지로 category confusion을 방지한다.  
국제 표준과 호환 가능한 구조를 만든다.  
외부 표준은 직접 종속이 아니라 mapping 대상으로 다룬다.  
Domain Module이 Foundation을 오염시키지 않도록 한다.

---

## **2\. LEDO 전체 구조 안에서의 위치**

이 문서는 다음 위치에 속한다.

04\_ontology\_foundation/  
  02\_upper\_ontology\_and\_standards/  
    upper\_ontology\_and\_standards.md

이 문서는 다음 문서들과 연결된다.

00\_ontology\_foundation\_report  
→ Foundation 전체 철학과 원칙

01\_semantic\_web\_technology\_stack  
→ RDF, OWL, SHACL, SPARQL, SKOS, PROV-O 등 기술 책임 분리

03\_owl\_modeling\_principles  
→ OWL class/property/axiom 설계 원칙

04\_reasoning\_and\_constraint\_model  
→ reasoning, validation, policy, safety gate 경계

05\_relationship\_and\_property\_design  
→ 관계와 속성 설계 기준

06\_ontology\_governance\_and\_versioning  
→ 표준 매핑 변경, axiom 변경, version 관리

---

## **3\. 핵심 원칙**

LEDO의 상위 온톨로지 및 표준 정렬 원칙은 다음과 같다.

상위 온톨로지는 category discipline을 제공한다.  
국제 표준은 compatibility와 export-grade 설계를 제공한다.  
외부 표준은 복사하지 않고 mapping한다.  
Foundation은 작게 유지한다.  
Domain detail은 Domain Module로 분리한다.  
Runtime 실행 안전성은 표준 이름만으로 보장되지 않는다.  
표준 정렬은 Evidence, Policy, Safety Gate, Audit과 연결되어야 한다.

가장 중요한 원칙은 다음이다.

Standards are aligned, not blindly copied.  
BFO is used for category discipline, not domain bloat.

---

## **4\. Foundation과 Domain Module의 경계**

LEDO Foundation은 모든 산업 도메인에서 공통적으로 필요한 상위 구조만 포함한다.

Foundation에 들어갈 수 있는 것은 다음과 같다.

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

Foundation에 직접 넣지 말아야 할 것은 다음과 같다.

특정 산업 장비 상세 분류  
특정 제조 공정 세부 단계  
특정 현장 작업 세부 명칭  
특정 국가 법령의 세부 조항  
특정 벤더 API schema  
특정 PLC tag 구조  
특정 BIM 객체 세부 속성 전체  
특정 로봇 모델의 내부 제어 명령

이런 내용은 Domain Module 또는 Mapping Module에 둔다.

Foundation  
→ 공통 의미 구조

Domain Module  
→ 산업별 상세 개념

Mapping Module  
→ 외부 표준, 벤더 시스템, 데이터 schema와의 연결

Runtime Module  
→ 실제 처리, 검증, 실행 요청, feedback, audit

---

## **5\. BFO 사용 목적**

BFO는 LEDO에서 상위 온톨로지 정렬 기준으로 사용된다.

BFO를 사용하는 목적은 Foundation을 어렵게 만들기 위해서가 아니다. 목적은 category confusion을 방지하는 것이다.

예를 들어 다음을 혼동하면 안 된다.

물리 객체와 과정  
역할과 사람  
기능과 장비  
위험 상태와 위험 원인  
공간 구역과 물리 장비  
관측 행위와 관측 결과  
정책 문서와 실제 실행

BFO는 이런 구분을 잡아주는 상위 기준이다.

---

## **6\. BFO 핵심 구분**

LEDO Foundation에서 특히 중요한 BFO 계열 구분은 다음과 같다.

Continuant  
→ 시간 속에서 지속되는 것

Occurrent  
→ 시간 속에서 발생하거나 전개되는 것

Material Entity  
→ 물리적으로 존재하는 대상

Immaterial Entity  
→ 물리적 물질로 이루어져 있지는 않지만 경계, 공간, 위치, 구역처럼 존재론적으로 다룰 수 있는 비물질적 실체

Process  
→ 시간 속에서 진행되는 과정

Role  
→ 특정 맥락에서 수행되는 역할

Function  
→ 어떤 대상이 수행하도록 설계되거나 기대되는 기능

Disposition  
→ 특정 조건에서 발현될 수 있는 성향 또는 가능성

Quality  
→ 대상이 가지는 특성

Site / Spatial Region  
→ 공간적 위치 또는 구역

Information Artifact  
→ 정책, 문서, 모델, 기록 같은 정보 객체

LEDO에서 이 구분은 class 설계, property 설계, axiom 설계, reasoning 설계의 기준이 된다.

특히 `Zone`, `DangerZone`, `RestrictedZone`, `GeofencingBoundary`, `SpeedLimitedZone` 같은 공간 개념은 물리적 벽이 없어도 운영상 실제 영향을 가지는 공간 경계일 수 있다. 이런 개념은 BFO 지향 관점에서 `Immaterial Entity`, `Site`, `Spatial Region` 계열로 정렬한다.

이 구분은 GeoSPARQL, 공간 포함 관계, 위험 구역 판정, 접근 제한, 속도 제한, 로봇 경로 제약, 관제 구역 설정에서 중요하다.

핵심 원칙은 다음과 같다.

모든 구역이 물리적 벽을 의미하지는 않는다.  
논리적 경계도 runtime safety와 policy 판단에 영향을 줄 수 있다.  
논리적 공간 경계는 Immaterial Entity / Site / Spatial Region 계열로 명시적으로 정렬한다.

---

## **7\. LEDO 개념의 BFO 지향 매핑**

| LEDO 개념 | BFO 지향 category | 설명 | 매핑 이유 |
| ----- | ----- | ----- | ----- |
| Agent | material entity 또는 role-bearing entity | 행동을 수행하거나 의사결정에 참여하는 주체 | 실제 물리 개체일 수도 있고, 특정 맥락에서 역할을 수행하는 주체일 수도 있기 때문 |
| HumanAgent | material entity | 사람 agent | 시간 속에서 지속되는 물리적 인간 개체이기 때문 |
| RobotAgent | material entity | 물리적으로 존재하는 로봇 agent | 실제 공간에 존재하며 상태와 위치를 가지는 물리 개체이기 때문 |
| HumanoidRobot | material entity / object | 인간형 로봇 개체 | 로봇 형태의 물리 객체이며 task 수행 주체가 될 수 있기 때문 |
| Sensor | material entity / device-like object | 관측 기능을 가진 물리 장치 | 물리 장치이며 observation을 생성하는 기능을 가지기 때문 |
| Actuator | material entity / device-like object | 물리 작용을 수행하는 장치 | 외부 제어 요청에 따라 물리 세계에 작용할 수 있는 장치이기 때문 |
| Controller | material entity 또는 system component | 제어 기능을 수행하는 시스템 구성 요소 | 물리 장치 또는 디지털 제어 구성요소로서 control function을 수행하기 때문 |
| Task | planned process | 계획된 수행 과정 | 시간 속에서 시작과 종료를 가지며 수행되는 과정이기 때문 |
| InspectionTask | planned process | 점검 목적의 task process | 점검이라는 목적을 가진 계획된 수행 과정이기 때문 |
| HighRiskTask | planned process with risk context | 위험 조건이 연결된 task process | task 자체는 process이고, high risk는 그 process에 붙은 위험 맥락이기 때문 |
| Event | occurrent | 시간 속에서 발생한 사건 | 특정 시점 또는 시간 구간 안에서 발생하는 변화이기 때문 |
| Observation | process 또는 information content entity | 관측 행위 또는 관측 결과 정보 | 관측 행위는 process이고, 관측 결과는 정보 객체로 관리될 수 있기 때문 |
| Evidence | information artifact | 판단 근거로 사용되는 정보 객체 | 직접 물리 객체가 아니라 판단을 지원하는 정보적 산물이기 때문 |
| Risk | disposition 또는 risk context | 특정 조건에서 피해 가능성을 나타내는 상태/맥락 | 현재 즉시 발생한 사건이 아니라 조건에 따라 피해로 이어질 가능성을 나타내기 때문 |
| Zone | immaterial entity / site / spatial region | 공간 영역 | 물리 객체가 아니라 위치와 포함 관계를 갖는 공간적 영역이기 때문 |
| DangerZone | site with risk context | 위험 맥락이 연결된 공간 영역 | zone은 spatial region이고, danger는 해당 영역에 붙은 위험 맥락이기 때문 |
| RestrictedZone | site with policy restriction | 접근 제한 정책이 연결된 공간 영역 | 물리 벽이 없어도 정책적으로 제한되는 공간일 수 있기 때문 |
| GeofencingBoundary | immaterial entity / spatial boundary | 논리적으로 설정된 공간 경계 | 물리적 벽은 아니지만 위치 기반 판단과 제어 제약에 사용되는 비물질적 경계이기 때문 |
| SpeedLimitedZone | spatial region with operational constraint | 속도 제한 조건이 연결된 공간 영역 | 특정 공간 안에서 agent 또는 machine의 행동 제약을 부여하기 때문 |
| Policy | information artifact | 운영 규칙 또는 정책 정보 객체 | 실제 행위가 아니라 행위를 제한하거나 허용하는 정보 객체이기 때문 |
| Permit | information artifact / authorization record | 허가 또는 승인 기록 | 허가 상태를 기록하는 정보 객체이며 실행 권한 판단에 사용되기 때문 |
| ActionCandidate | information artifact / planned action proposal | 실행 전 후보 조치 | 실제 실행이 아니라 agent가 제안한 조치 후보 정보이기 때문 |
| ExecutionRequest | information artifact / request object | 외부 실행 계층으로 전달되는 요청 | 물리 제어 자체가 아니라 외부 시스템에 전달되는 요청 정보이기 때문 |
| AuditRecord | information artifact | 감사 기록 | 실행과 판단의 근거와 과정을 기록한 정보 객체이기 때문 |

이 매핑은 LEDO class가 BFO와 완전히 동일하다는 뜻이 아니다. LEDO class가 어떤 상위 category discipline을 따라야 하는지 나타내는 기준이다.

---

## **8\. BFO 사용 원칙**

BFO 사용 원칙은 다음과 같다.

BFO는 Foundation의 category discipline을 위해 사용한다.  
BFO를 그대로 domain ontology로 복사하지 않는다.  
Domain class는 BFO category와 명시적으로 정렬한다.  
Role, Function, Process, Object를 혼동하지 않는다.  
물리 객체와 정보 객체를 혼동하지 않는다.  
Runtime action과 policy document를 혼동하지 않는다.  
물리적 공간과 논리적 공간 경계를 구분하되, 둘 다 spatial reasoning의 대상이 될 수 있음을 인정한다.

예를 들어 `Policy`는 실제 물리 행위가 아니다.  
`ExecutionRequest`도 물리 명령 자체가 아니다.  
`ActionCandidate`는 실행 명령이 아니라 실행 전 후보 조치다.  
`GeofencingBoundary`는 물리 벽이 아니지만 runtime policy와 spatial validation에 영향을 줄 수 있는 비물질적 공간 경계다.

이 구분은 Safety Gate, GeoSPARQL, Audit에서 매우 중요하다.

---

## **9\. 표준 정렬 등급**

LEDO는 표준 정렬 수준을 다음 세 가지로 구분한다.

MUST  
→ Foundation 설계에 반드시 반영해야 하는 기준

SHOULD  
→ 산업 적용성과 확장성을 위해 강하게 권장되는 기준

MAY  
→ 도메인, 고객, 국가, 인증 범위에 따라 선택 적용 가능한 기준

이 등급은 RFC 스타일의 요구사항 언어를 따른다.

---

## **10\. 표준 정렬 매트릭스**

| 표준 계열 | LEDO 적용 등급 | Foundation에서의 역할 |
| ----- | ----- | ----- |
| W3C RDF / RDFS | MUST | RDF graph, triple model, 기본 class/property 구조 |
| W3C OWL 2 | MUST | 형식 온톨로지, class/property/individual axiom, reasoning |
| W3C SPARQL | MUST | graph query, semantic retrieval, evidence/audit query |
| W3C SHACL | MUST | ABox data validation, shape constraint |
| W3C SKOS | MUST | vocabulary system, SLM training structure, multilingual labels |
| W3C PROV-O | SHOULD | provenance, evidence lineage, source tracking |
| W3C OWL-Time | SHOULD | time concepts, temporal relations, event timing |
| OGC GeoSPARQL | SHOULD | space, zone, location, geometry query |
| ISO/IEC 21838 / BFO | MUST | upper ontology, category discipline |
| IFC / ISO 16739 | SHOULD | external industrial asset alignment, BIM mapping |
| IEC 61508 | SHOULD | functional safety, safety lifecycle, SIL alignment |
| IEC 61511 | SHOULD | process safety, safety instrumented system alignment |
| IEC 62541 / OPC UA | SHOULD | industrial communication, telemetry, external system model |
| IEC 62264 / ISA-95 | SHOULD | enterprise-control integration boundary |
| ISA/IEC 62443 | MUST | industrial cybersecurity, OT/ICS security boundary |
| IEEE 1588 | MUST | time synchronization, clock trust, timestamp reliability |
| ISO robotics safety family | SHOULD | robot safety reference |
| ISO 8373 | MAY | robotics vocabulary reference |
| NIST SP 800-53 | SHOULD | security and privacy control reference |
| NIST AI RMF | SHOULD | AI risk governance reference |
| RFC 2119 / RFC 8174 | MUST | MUST/SHOULD/MAY requirement language |
| FIPA ACL | MAY | agent communication reference |

---

## **11\. 표준 적용 경계**

표준은 LEDO Foundation에 직접 복사되지 않는다.

LEDO는 다음 방식으로 표준을 적용한다.

표준의 핵심 개념을 이해한다.  
LEDO Foundation category와 정렬한다.  
Domain Module에서 필요한 상세 개념을 확장한다.  
Mapping Module에서 외부 schema와 연결한다.  
Runtime에서는 canonical object를 기준으로 처리한다.  
Audit에서는 표준 정렬 근거를 추적 가능하게 남긴다.

즉 외부 표준은 LEDO 내부 구조의 주인이 아니다.  
LEDO 내부의 semantic authority는 Core Ontology Kernel이다.

---

## **12\. 외부 표준 정렬 흐름**

외부 표준은 다음 흐름으로 LEDO와 연결된다.

External Standard Concept  
→ Mapping Module  
→ Canonical Object / Canonical Class  
→ Ontology Binding  
→ Evidence / State / Action / Audit

예를 들어 외부 시스템의 장비 ID, BIM 객체 ID, OPC-UA node, PLC tag, robot state message는 바로 ontology individual이 되지 않는다.

먼저 canonical identity와 canonical object로 정규화된 뒤 ontology에 바인딩된다.

External ID  
→ Identifier Mapping Record  
→ Canonical Identity  
→ ABox Hash IRI  
→ Ontology Binding

---

## **13\. IFC / BIM 정렬 기준**

IFC / BIM 계열 표준은 산업 자산, 공간, 구성요소, 설계 정보와 연결될 수 있다.

LEDO에서 IFC / BIM은 다음 역할을 가진다.

asset reference  
space reference  
geometry reference  
building/facility component reference  
external design model mapping  
digital twin alignment

하지만 IFC class를 LEDO Foundation에 그대로 복사해서는 안 된다.

원칙은 다음과 같다.

IFC는 external model이다.  
LEDO Foundation은 canonical semantic layer다.  
IFC 객체는 Mapping Module을 통해 LEDO 객체와 연결한다.  
IFC schema 변경이 Foundation을 직접 흔들어서는 안 된다.

---

## **14\. IFC 객체 실제 매핑 흐름 예시**

IFC 기반 외부 객체가 LEDO로 들어올 때의 기본 흐름은 다음과 같다.

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

예를 들어 IFC 모델 안의 어떤 공간 객체 또는 설비 객체가 들어왔다고 가정한다. LEDO는 그 IFC 객체를 내부 온톨로지 class로 그대로 복사하지 않는다. 먼저 외부 식별자를 기록하고, 해당 객체가 LEDO 내부에서 어떤 canonical identity에 해당하는지 확인한다.

그 후 다음 질문을 검토한다.

이 IFC 객체는 LEDO의 어떤 Foundation category에 속하는가?  
PhysicalObject인가, Zone인가, System인가, DigitalObject인가?  
이 객체는 기존 canonical object와 같은 대상인가?  
이 객체의 geometry는 spatial reference로만 사용할 것인가?  
이 객체가 World State에 영향을 주는 runtime object인가?  
이 객체가 Evidence 또는 Digital Twin alignment에만 필요한 reference인가?

이 흐름을 통해 IFC schema의 변화가 LEDO Foundation을 직접 흔들지 않게 한다.

핵심 원칙은 다음과 같다.

IFC 객체는 LEDO 객체의 외부 참조일 수 있다.  
IFC 객체가 곧 LEDO semantic authority가 되어서는 안 된다.

---

## **15\. OPC-UA 및 산업 통신 표준 정렬 기준**

OPC-UA 같은 산업 통신 표준은 설비, 센서, 제어 시스템, telemetry와 연결된다.

LEDO에서 OPC-UA는 다음 역할을 가진다.

external telemetry source  
industrial communication model  
node identifier source  
equipment state source  
control system integration point

그러나 OPC-UA node나 PLC tag를 ontology class로 직접 만들면 안 된다.

원칙은 다음과 같다.

OPC-UA node는 source identifier다.  
LEDO canonical identity는 별도로 관리한다.  
Telemetry는 raw data로 들어오고, semantic binding을 거쳐 Observation 또는 State가 된다.  
제어 요청은 LEDO가 직접 low-level command를 실행하는 것이 아니라 ExternalControlRequest로 전달한다.

---

## **16\. OPC-UA Node / Telemetry 실제 매핑 흐름 예시**

OPC-UA node 또는 telemetry가 LEDO로 들어올 때의 기본 흐름은 다음과 같다.

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

예를 들어 OPC-UA node에서 특정 센서값이 들어왔다고 가정한다. 이 node는 곧바로 LEDO class가 되지 않는다. node identifier는 source identifier로 기록되고, 실제 의미는 정규화와 canonical object resolution 이후에 부여된다.

검토 질문은 다음과 같다.

이 node는 어떤 source system에서 왔는가?  
이 node는 어떤 canonical sensor 또는 system component에 연결되는가?  
들어온 값은 Observation인가, State인가?  
timestamp는 신뢰 가능한가?  
값의 단위와 범위는 정상인가?  
이 Observation은 Evidence로 사용할 수 있는가?  
World State를 갱신할 만큼 fresh한가?

이 흐름을 통해 OPC-UA나 PLC tag 구조가 바뀌어도 LEDO ontology 구조 전체가 오염되지 않는다.

핵심 원칙은 다음과 같다.

OPC-UA는 외부 통신 및 telemetry 계층이다.  
LEDO Ontology는 그 telemetry에 의미를 부여하는 canonical semantic layer다.

---

## **17\. Functional Safety 표준 정렬 기준**

IEC 61508, IEC 61511 같은 functional safety 계열 표준은 LEDO의 안전 생명주기와 연결된다.

LEDO에서 이 표준들은 다음을 지원한다.

risk classification  
safety lifecycle alignment  
safety requirement traceability  
evidence-based decision support  
approval and validation process  
safety-related audit

하지만 LEDO Foundation이 functional safety certification 자체를 대체하지 않는다.

원칙은 다음과 같다.

LEDO는 safety evidence와 traceability를 지원한다.  
LEDO는 인증기관의 기능안전 인증을 대체하지 않는다.  
Safety Gate는 runtime safety validation을 수행한다.  
Functional safety standard alignment는 설계와 감사 가능성을 강화한다.

---

## **18\. OT / ICS Cybersecurity 표준 정렬 기준**

ISA/IEC 62443, NIST SP 800-53 같은 보안 표준은 LEDO의 governance, access control, audit, network boundary, system integrity와 연결된다.

LEDO에서 이 표준들은 다음을 지원한다.

role-based access control  
zone and conduit thinking  
asset security boundary  
audit trail  
system hardening reference  
least privilege  
identity and access management  
incident traceability

보안 표준은 Foundation의 의미 구조와 runtime policy layer에 모두 연결된다.

원칙은 다음과 같다.

Security is not an add-on.  
Security must be embedded into identity, policy, evidence, execution, and audit.

---

## **19\. IEEE 1588 및 시간 동기화 기준**

IEEE 1588 같은 시간 동기화 표준은 LEDO에서 매우 중요하다.

Physical AI와 산업 시스템에서는 시간 순서가 판단의 핵심이다. 시간은 단순 metadata가 아니라 Evidence 신뢰성, World State 신뢰성, Safety Gate 신뢰성, Audit 신뢰성과 직접 연결된다.

LEDO는 다음을 확인해야 한다.

Observation은 언제 발생했는가  
Event는 언제 탐지되었는가  
Evidence는 아직 fresh한가  
ActionCandidate는 어느 시점에 생성되었는가  
Approval은 후보 생성 이후에 발생했는가  
Safety Gate 검증 시점은 언제인가  
Feedback은 기대 시간 내에 도착했는가

시간 동기화가 불안정하면 다음 문제가 발생한다.

Event 순서가 왜곡된다.  
Evidence freshness를 신뢰할 수 없다.  
World State가 현재 상태인지 판단할 수 없다.  
Approval 유효성을 확인하기 어렵다.  
Safety Gate가 오래된 상태를 기준으로 실행 가능성을 판단할 수 있다.  
Audit timeline이 재구성되지 않는다.

따라서 LEDO에서 clock trust는 evidence trust의 일부다.

Clock trust is part of evidence trust.  
If clocks are not trustworthy, event order, evidence freshness, approval validity, and Safety Gate validation become unreliable.

핵심 원칙은 다음과 같다.

Timestamp is safety-critical.  
Clock trust is evidence-critical.  
Time synchronization is not an infrastructure detail; it is part of semantic and safety validity.

---

## **20\. 로봇 및 Physical AI 표준 정렬 기준**

로봇 및 Physical AI 계열 표준은 RobotAgent, HumanoidRobot, autonomous system, controller, actuator, task, safety boundary와 연결된다.

LEDO에서 로봇 관련 표준은 다음에 사용된다.

robot vocabulary reference  
robot safety boundary  
human-robot collaboration context  
autonomous task execution context  
robot state interpretation  
external robot middleware mapping

그러나 LEDO는 로봇 제어기를 직접 대체하지 않는다.

원칙은 다음과 같다.

LEDO interprets robot meaning and governs high-level action requests.  
Robot middleware and control systems execute physical control.

---

## **21\. NIST AI RMF 및 AI Governance 정렬 기준**

AI risk governance 계열 표준은 LEDO의 agent interpretation, model output handling, human approval, audit, risk governance와 연결된다.

LEDO에서 AI output은 Evidence가 아니다. AI output은 truth가 아니다. AI output은 candidate interpretation이다.

핵심 원칙은 다음과 같다.

LLM / SLM output is candidate interpretation.  
Agent output is not truth.  
AI output must be supported by evidence before decision.  
High-risk action requires policy, approval, and Safety Gate validation.

AI output은 조사를 시작하거나 ActionCandidate를 생성할 수는 있다. 하지만 AI output이 직접 Evidence, Decision, Approval, ExecutionRequest가 되어서는 안 된다.

In LEDO, AI output may initiate investigation or generate an ActionCandidate,  
but it must not directly become Evidence, Decision, Approval, or ExecutionRequest.

AI governance 표준은 다음에 연결된다.

model risk management  
human oversight  
explainability support  
traceability  
bias and failure review  
incident investigation

---

## **22\. RFC 2119 / 8174 요구사항 언어**

LEDO 문서에서는 요구사항 수준을 명확히 하기 위해 다음 표현을 사용한다.

MUST  
→ 반드시 해야 한다.

MUST NOT  
→ 절대 해서는 안 된다.

SHOULD  
→ 강하게 권장된다.

SHOULD NOT  
→ 강하게 피해야 한다.

MAY  
→ 상황에 따라 허용된다.

이 요구사항 언어는 설계 문서, implementation guide, validation rule, governance rule에서 일관되게 사용한다.

---

## **23\. RFC 2119 요구사항과 SHACL Severity Mapping**

LEDO는 요구사항 언어를 문서 수준에서만 사용하지 않는다. 요구사항 수준은 SHACL 검증 severity와 연결될 수 있다.

기본 매핑은 다음과 같다.

| 요구사항 수준 | SHACL Severity | Runtime 처리 기준 |
| ----- | ----- | ----- |
| MUST | sh:Violation | pipeline 차단 또는 상태 갱신 거부 |
| MUST NOT | sh:Violation | 즉시 차단, 보안/안전 이벤트 후보 생성 |
| SHOULD | sh:Warning | 흐름은 허용하되 warning log, audit, review 대상 |
| SHOULD NOT | sh:Warning | 흐름은 허용 가능하나 governance review 또는 policy review 대상 |
| MAY | sh:Info | 참고 정보로 기록, 차단하지 않음 |

예시는 다음과 같다.

Observation은 timestamp를 MUST 가져야 한다.  
→ timestamp 누락 시 sh:Violation  
→ Evidence Binding 또는 World State Update 차단

EvidenceBundle은 source lineage를 SHOULD 가져야 한다.  
→ source lineage 부족 시 sh:Warning  
→ 흐름은 허용하되 audit warning 기록

SKOS concept은 altLabel을 MAY 가질 수 있다.  
→ altLabel 누락 시 sh:Info 또는 검증 없음  
→ pipeline 차단하지 않음

이 매핑은 governance 자동화의 기반이 된다.

MUST 요구사항은 실행 차단 조건으로 연결된다.  
SHOULD 요구사항은 경고와 검토 대상으로 연결된다.  
MAY 요구사항은 참고 정보로 관리된다.

단, 모든 RFC 2119 문장이 자동으로 SHACL shape가 되는 것은 아니다. 실제 runtime validation이 필요한 요구사항만 SHACL shape로 구현한다.

핵심 원칙은 다음과 같다.

Requirement language must be operationalizable.  
MUST should map to blocking validation when it affects safety, identity, evidence, or execution.  
SHOULD should map to warning validation when it affects quality, governance, or completeness.  
MAY should not block runtime flow.

---

## **24\. Runtime Flow와 표준 정렬**

표준 정렬은 문서상 매핑으로 끝나지 않는다. Runtime flow 안에서 실제 역할을 가져야 한다.

Raw Data  
→ external standard source에서 들어올 수 있음

Normalize  
→ 표준별 field mapping 필요

Canonical Object  
→ 외부 ID를 내부 canonical identity로 변환

Ontology Binding  
→ BFO / OWL / RDFS category에 정렬

Evidence Binding  
→ PROV-O와 source lineage 연결

World State Update  
→ 시간 동기화와 state validity 필요

Event Detection  
→ risk/safety/security 표준 기준 반영 가능

ActionCandidate  
→ AI output은 후보로만 취급

Candidate Validation  
→ OWL, SHACL, SPARQL, policy 기준 검증

Safety Gate  
→ runtime safety validation

ExecutionRequest  
→ 외부 제어 표준과 adapter mapping

Feedback  
→ 실행 결과와 evidence/audit 연결

Audit  
→ 표준 정렬 근거와 전체 trace 보존

---

## **25\. Domain Module 확장 기준**

Domain Module은 Foundation을 확장하지만 오염시켜서는 안 된다.

Domain Module에서 새 class를 만들 때는 다음을 확인해야 한다.

Foundation의 어떤 category 아래에 들어가는가  
BFO상 continuant인가 occurrent인가  
물리 객체인가 정보 객체인가  
role인가 function인가 process인가  
이미 존재하는 class로 표현 가능한가  
새 property가 필요한가, 기존 property로 충분한가  
외부 표준과 mapping이 필요한가  
SHACL shape가 필요한가  
SKOS term 등록이 필요한가  
Competency question이 있는가

Domain Module 확장 흐름은 다음과 같다.

1\. Domain Concept 식별  
   → 새로 모델링하려는 도메인 개념을 정의한다.

2\. Foundation Category Mapping  
   → 해당 개념이 Agent, Sensor, Task, Event, Risk, Zone, Evidence 등 어떤 Foundation category 아래에 들어가는지 확인한다.

3\. BFO-oriented Category Check  
   → continuant인지 occurrent인지, material entity인지 process인지, role인지 function인지 확인한다.

4\. External Standard Mapping  
   → IFC, OPC-UA, ISO, IEC, IEEE, NIST 등 외부 표준과 연결이 필요한지 확인한다.

5\. TBox Class Extension  
   → 새 class가 필요한 경우 TBox에 class를 추가한다.

6\. Property Alignment  
   → 기존 property로 표현 가능한지 확인하고, 불가피할 때만 새 property를 설계한다.

7\. Axiom Review  
   → subclass, domain/range, disjointness, restriction 등이 안전한지 검토한다.

8\. SHACL Shape Design  
   → ABox data validation을 위한 shape가 필요한지 설계한다.

9\. SKOS Concept Registration  
   → 용어, 라벨, 정의, 동의어, 현장 표현을 등록한다.

10\. Competency Question Test  
   → 이 개념을 통해 어떤 질문에 답할 수 있어야 하는지 확인한다.

11\. Governance Review  
   → version, deprecation, mapping, axiom impact를 검토한다.

요약 흐름은 다음과 같다.

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

| Anti-pattern | 문제 | 발생 가능한 피해 | 대안 / 기대 효과 |
| ----- | ----- | ----- | ----- |
| 외부 표준 class를 Foundation에 그대로 복사 | Foundation이 특정 표준에 종속됨 | 표준 변경 시 전체 구조 흔들림 | Mapping Module을 사용한다. 이렇게 하면 외부 표준 변경 충격을 흡수할 수 있다. |
| BFO를 과도하게 직접 노출 | 도메인 사용자가 이해하기 어려움 | 모델링 복잡도 증가 | BFO는 내부 category discipline으로 사용한다. 이렇게 하면 구조적 엄밀성과 실무 사용성을 동시에 유지할 수 있다. |
| Domain detail을 Foundation에 넣음 | Foundation이 비대해짐 | 다른 산업 도메인 확장 방해 | Domain Module로 분리한다. 이렇게 하면 Foundation은 작고 강하게 유지된다. |
| OPC-UA node를 ontology class로 직접 생성 | source identifier와 semantic class 혼동 | ontology 오염 | Canonical identity와 mapping record를 사용한다. 이렇게 하면 source schema와 ontology 의미를 분리할 수 있다. |
| IFC 객체를 그대로 내부 객체로 사용 | 외부 schema에 종속 | BIM 변경 시 내부 구조 영향 | IFC mapping layer를 사용한다. 이렇게 하면 Digital Twin alignment는 유지하면서 Core Ontology는 보호된다. |
| AI output을 Evidence로 취급 | 검증되지 않은 판단을 사실화 | 잘못된 조치와 감사 실패 | AI output은 candidate로만 사용한다. 이렇게 하면 증거 기반 판단 구조를 유지할 수 있다. |
| Safety Gate를 표준 문서 참조로 대체 | runtime 검증 부재 | 실행 위험 증가 | 결정론적 validation rule을 사용한다. 이렇게 하면 실행 직전 안전성을 실제 상태 기준으로 검증할 수 있다. |
| 시간 동기화를 무시 | evidence 순서와 freshness 불명확 | 잘못된 상태 판단 | clock trust와 timestamp governance를 적용한다. 이렇게 하면 evidence와 audit timeline의 신뢰성을 확보할 수 있다. |
| 표준 매핑 변경을 governance 없이 수행 | 의미 관계가 깨짐 | reasoning, validation, audit 오류 | mapping review와 versioning을 적용한다. 이렇게 하면 변경 영향도를 통제할 수 있다. |
| 논리적 공간 경계를 단순 문자열 속성으로만 처리 | spatial reasoning이 불가능해짐 | geofencing, 접근 제한, 속도 제한 판단 오류 | GeofencingBoundary, RestrictedZone 등을 Immaterial Entity / Spatial Region 계열로 모델링한다. |
| MUST / SHOULD / MAY를 검증 severity와 연결하지 않음 | 요구사항이 문서에만 남고 runtime에서 작동하지 않음 | validation 자동화 실패, governance 불일치 | RFC 2119 요구사항을 SHACL severity와 매핑한다. |

---

## **27\. 핵심 원칙**

Foundation은 작고 강해야 한다.  
BFO는 category discipline을 제공한다.  
Immaterial Entity / Site / Spatial Region은 논리적 공간 경계 모델링에 중요하다.  
외부 표준은 복사하지 않고 mapping한다.  
Domain detail은 Domain Module로 분리한다.  
Mapping Module은 외부 schema 변화의 충격을 흡수한다.  
Core Ontology Kernel은 semantic authority다.  
Runtime safety는 표준 이름이 아니라 Safety Gate 검증으로 보장된다.  
AI output은 Evidence가 아니라 candidate다.  
Timestamp와 clock trust는 safety-critical이다.  
RFC 2119 요구사항은 필요 시 SHACL severity로 운영화되어야 한다.  
표준 정렬은 Evidence, Policy, Safety Gate, Audit과 연결되어야 한다.

최종 원칙은 다음과 같다.

LEDO는 표준을 따르되 표준에 종속되지 않는다.  
LEDO는 상위 온톨로지로 의미의 질서를 잡고,  
국제 표준으로 산업 호환성과 감사 가능성을 확보한다.

