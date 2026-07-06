**Evidence registry**

## **1\. Overview**

`evidence_registry` is a core registry in the LEDO Ontology-Centric Cyber-Physical System. It defines and governs all Evidence Types, Evidence Schemas, Evidence Sources, Evidence Quality Rules, Evidence Freshness Rules, Evidence Binding Rules, Evidence Trust Levels, and Evidence Retention Rules used across the system.

The purpose of this module is to prevent evidence used by Agents, Decisions, Approvals, and the Safety Gate from being created arbitrarily or used in judgment without validation.

`evidence_registry` is not a simple list of evidence names.

It is an **operational contract registry for evidence meaning, structure, source, trust, and validity** that defines the following:

Which Evidence Types may exist?

What does each Evidence prove?

Which source may generate the Evidence?

Which schema must the Evidence payload follow?

For which Action Type, Decision Rule, or Approval Rule may the Evidence be used?

How fresh must the Evidence be?

How are evidence trust and quality evaluated?

From which World State snapshot or Event was the Evidence derived?

Is the Evidence auditable and reproducible?

In other words, `evidence_registry` is the core deterministic registry that controls "what judgment was based on" in the LEDO system.

---

## **2\. Core Principle**

Evidence is the basis of judgment.

Evidence is not an Action.

Evidence is not Approval.

Evidence is not the Safety Gate.

Evidence is not an ExecutionRequest.

Evidence is not a Physical Command.

The basic meaning of Evidence is:

What is this judgment based on?

Which observation or fact supports this ActionCandidate?

Which evidence did this DecisionCase evaluate?

Which evidence was reviewed for this ApprovalDecision?

Which runtime evidence did the Safety Gate verify?

The core principle is:

No valid Evidence,

no reliable Decision.

No required Evidence,

no ApprovalRequest.

No fresh runtime Evidence,

no Safety Gate pass.

Evidence supports judgment.

Evidence does not execute.

---

## **3\. Position in the LEDO Architecture**

`evidence_registry` is a cross-cutting registry used across Events, Agents, Decisions, Approvals, and the Safety Gate.

Event / Sensor / World State / External System

        →
Evidence Generation or Evidence Binding

        →
evidence\_registry validation

        →
EvidenceBundle

        →
ActionCandidate

        →
DecisionCase

        →
ApprovalRequest

        →
ApprovalDecision

        →
ApprovedAction

        →
RuntimeValidationInput

        →
RuntimeValidationResult

        →
Safety Gate

        →
SafetyGatePass or SafetyGateBlock

        →
AuditRecord

`evidence_registry` is strongly connected to the following registries:

event\_registry

agent\_vocabulary\_registry

action\_registry

decision\_registry

approval\_registry

runtime\_validation\_registry

snapshot\_schema\_registry

audit\_event\_registry

ontology\_registry

---

## **4\. Purpose**

The purpose of `evidence_registry` is to ensure the following:

1. Prevent the use of unregistered Evidence Types  
2. Define the meaning and schema of each Evidence Type  
3. Define evidence source and producer authority  
4. Define evidence freshness requirements  
5. Define evidence quality and confidence criteria  
6. Define evidence trust levels  
7. Define which Action / Decision / Approval / Safety Gate may use each Evidence Type  
8. Define evidence binding rules  
9. Define EvidenceBundle composition rules  
10. Manage evidence lineage and provenance  
11. Define evidence retention and audit rules  
12. Manage evidence versioning and migration  
13. Prevent Agents or LLMs from arbitrarily creating unvalidated Evidence  
14. Prevent Decisions and Approvals from becoming judgments without grounds

---

## **5\. Core Distinctions**

### **5.1 Evidence Type**

`Evidence Type` is a controlled type of evidence allowed in the system.

Examples:

worker\_location\_snapshot

hazard\_detection\_snapshot

robot\_availability\_snapshot

zone\_accessibility\_snapshot

equipment\_status\_snapshot

risk\_assessment\_snapshot

sensor\_freshness\_snapshot

mission\_context\_snapshot

policy\_evaluation\_evidence

approval\_context\_evidence

execution\_feedback\_evidence

Evidence Type defines "what kind of basis this is."

---

### **5.2 Evidence Instance**

`Evidence Instance` is an individual piece of evidence generated at runtime.

Example:

evidence\_id: evidence\_01HT...

evidence\_type\_id: evidence:worker\_location\_snapshot

source\_event\_id: event:WorkerLocationUpdated:evt\_123

entity\_refs:

  \- worker:worker\_123

  \- zone:zone\_03

generated\_at: 2026-06-26T09:00:00Z

valid\_until: 2026-06-26T09:00:10Z

confidence\_score: 0.94

payload:

  worker\_id: worker\_123

  zone\_id: zone\_03

  position:

    x: 12.4

    y: 7.8

    z: 0.0

Evidence Type is the design-level definition, while Evidence Instance is the actual evidence object used for judgment.

---

### **5.3 Evidence Bundle**

`EvidenceBundle` is a collection of multiple Evidence Instances used for one ActionCandidate, DecisionCase, ApprovalRequest, or SafetyGatePass or SafetyGateBlock.

Example:

evidence\_bundle\_id: bundle\_123

related\_action\_candidate\_id: action\_candidate\_456

evidence\_refs:

  \- evidence:hazard\_detection\_snapshot\_001

  \- evidence:worker\_location\_snapshot\_002

  \- evidence:risk\_assessment\_snapshot\_003

EvidenceBundle is the evidence package for judgment.

---

### **5.4 Evidence Source**

Evidence Source is the origin that generates or provides evidence.

Examples:

sensor\_gateway

world\_state\_service

domain\_agent

risk\_engine

policy\_engine

external\_adapter

operator\_ui

inspection\_system

robot\_fleet\_manager

scada\_system

Evidence Source must be registered and validated.

---

### **5.5 Evidence Quality**

Evidence Quality is the standard used to evaluate whether evidence can be trusted.

Example criteria:

confidence\_score

freshness

source\_trust\_level

schema\_validity

sensor\_accuracy

model\_eval\_score

lineage\_completeness

conflict\_status

manual\_verification\_status

The existence of evidence does not automatically mean it can be used for judgment.

Evidence must pass quality requirements.

---

## **6\. Scope**

`evidence_registry` controls the following fields:

evidence\_type\_id: string

canonical\_name: string

display\_name: string

description: string

semantic\_iri: string

evidence\_category: string

version: string

status: draft | active | deprecated | migration\_required | retired | blocked

allowed\_producer\_refs:

  \- string

allowed\_source\_event\_type\_refs:

  \- string

allowed\_source\_system\_refs:

  \- string

payload\_schema\_ref: string

metadata\_schema\_ref: string

required\_fields:

  \- string

optional\_fields:

  \- string

applicable\_action\_type\_refs:

  \- string

applicable\_decision\_rule\_refs:

  \- string

applicable\_approval\_rule\_refs:

  \- string

applicable\_safety\_gate\_refs:

  \- string

freshness\_requirement:

  max\_age\_seconds: integer

  freshness\_policy\_ref: string

quality\_requirement:

  minimum\_confidence\_score: float

  minimum\_source\_trust\_level: string

  conflict\_policy\_ref: string

lineage\_required: boolean

provenance\_required: boolean

manual\_verification\_allowed: boolean

retention\_policy\_ref: string

audit\_required: boolean

sensitivity\_level: public | internal | confidential | restricted | safety\_critical

pii\_classification: none | indirect | direct | sensitive

decision\_boundary: string

approval\_boundary: string

execution\_boundary: string

safety\_boundary: string

audit\_event\_refs:

  \- string

owner\_module: string

owner\_team: string

source\_document: string

created\_at: datetime

updated\_at: datetime

deprecated\_since: datetime | null

replacement\_evidence\_type\_id: string | null

---

## **7\. Non-Scope**

`evidence_registry` does not define the following:

1. Raw sensor driver logic  
2. Complete AI model inference algorithms  
3. Complete policy pass/fail logic  
4. Approval authority itself  
5. Final Safety Gate decision logic  
6. Physical execution commands  
7. PLC / SCADA / Robot commands  
8. Adapter instance selection  
9. All domain-specific threshold values  
10. Actual database storage implementation  
11. Complete event stream processing topology  
12. Internal structure of all computer vision models

These responsibilities belong to the following modules:

sensor\_gateway

model\_registry

policy\_registry

approval\_registry

runtime\_validation\_registry

safety\_gate

adapter\_registry

external\_system\_registry

domain\_module

world\_state\_service

stream\_processor

---

## **8\. Evidence Category Model**

Recommended Evidence Categories are:

SENSOR\_EVIDENCE

WORLD\_STATE\_EVIDENCE

AGENT\_EVIDENCE

POLICY\_EVIDENCE

RISK\_EVIDENCE

APPROVAL\_EVIDENCE

RUNTIME\_VALIDATION\_EVIDENCE

EXECUTION\_FEEDBACK\_EVIDENCE

AUDIT\_EVIDENCE

MANUAL\_EVIDENCE

EXTERNAL\_SYSTEM\_EVIDENCE

### **8.1 SENSOR\_EVIDENCE**

Evidence derived from sensors or IoT systems.

Examples:

worker\_location\_snapshot

gas\_level\_snapshot

temperature\_snapshot

vibration\_snapshot

camera\_detection\_snapshot

---

### **8.2 WORLD\_STATE\_EVIDENCE**

Current-state evidence extracted from World State.

Examples:

zone\_status\_snapshot

robot\_status\_snapshot

equipment\_status\_snapshot

worker\_zone\_membership\_snapshot

---

### **8.3 AGENT\_EVIDENCE**

Evidence generated by Agent analysis.

Examples:

risk\_assessment\_snapshot

recommendation\_reasoning\_summary

agent\_confidence\_report

However, agent-generated evidence must always include source lineage and model/tool lineage.

---

### **8.4 POLICY\_EVIDENCE**

Evidence based on Policy Engine evaluation results.

Examples:

policy\_pass\_evidence

policy\_warning\_evidence

policy\_hard\_fail\_evidence

---

### **8.5 RISK\_EVIDENCE**

Risk-related evidence produced by a Risk Engine or Domain Module.

Examples:

risk\_score\_snapshot

hazard\_severity\_assessment

worker\_exposure\_assessment

---

### **8.6 APPROVAL\_EVIDENCE**

Evidence used for ApprovalRequest or ApprovalDecision.

Examples:

approval\_context\_summary

approver\_identity\_evidence

approval\_scope\_evidence

---

### **8.7 RUNTIME\_VALIDATION\_EVIDENCE**

Real-time validation evidence used by the Safety Gate or Runtime Validation.

Examples:

sensor\_freshness\_snapshot

external\_system\_reachable\_snapshot

adapter\_health\_snapshot

world\_state\_consistency\_snapshot

---

### **8.8 EXECUTION\_FEEDBACK\_EVIDENCE**

Evidence derived from external system execution results.

Examples:

execution\_result\_evidence

robot\_mission\_feedback\_evidence

scada\_status\_feedback\_evidence

---

## **9\. Registry Entry Schema**

Each Evidence Registry entry follows this structure:

evidence\_type\_id: string

canonical\_name: string

display\_name: string

description: string

semantic\_iri: string

evidence\_category: string

version: string

status: draft | active | deprecated | migration\_required | retired | blocked

allowed\_producer\_refs:

  \- string

allowed\_source\_event\_type\_refs:

  \- string

allowed\_source\_system\_refs:

  \- string

payload\_schema\_ref: string

metadata\_schema\_ref: string

required\_fields:

  \- string

optional\_fields:

  \- string

applicable\_action\_type\_refs:

  \- string

applicable\_decision\_rule\_refs:

  \- string

applicable\_approval\_rule\_refs:

  \- string

applicable\_safety\_gate\_refs:

  \- string

freshness\_requirement:

  max\_age\_seconds: integer

  freshness\_policy\_ref: string

quality\_requirement:

  minimum\_confidence\_score: float

  minimum\_source\_trust\_level: string

  conflict\_policy\_ref: string

lineage\_required: boolean

provenance\_required: boolean

manual\_verification\_allowed: boolean

retention\_policy\_ref: string

audit\_required: boolean

sensitivity\_level: string

pii\_classification: string

decision\_boundary: string

approval\_boundary: string

execution\_boundary: string

safety\_boundary: string

audit\_event\_refs:

  \- string

owner\_module: string

owner\_team: string

source\_document: string

created\_at: datetime

updated\_at: datetime

deprecated\_since: datetime | null

replacement\_evidence\_type\_id: string | null

---

## **10\. Core Evidence Metadata Schema**

Every Evidence Instance must have at least the following metadata:

evidence\_id: string

evidence\_type\_id: string

evidence\_version: string

generated\_at: datetime

observed\_at: datetime | null

valid\_until: datetime | null

producer\_id: string

source\_system\_ref: string

source\_event\_refs:

  \- string

source\_snapshot\_refs:

  \- string

entity\_refs:

  \- string

site\_id: string | null

zone\_id: string | null

correlation\_id: string | null

causation\_id: string | null

trace\_id: string | null

confidence\_score: float

source\_trust\_level: string

quality\_status: valid | degraded | stale | conflicting | invalid

payload\_schema\_version: string

sensitivity\_level: string

pii\_classification: string

### **10.1 evidence\_id**

A unique ID for each Evidence Instance.

---

### **10.2 generated\_at**

The time when the Evidence was generated.

---

### **10.3 observed\_at**

The time when the event or state on which the Evidence is based was actually observed.

---

### **10.4 valid\_until**

The expiration time until which the Evidence can be used for judgment.

---

### **10.5 source\_event\_refs**

References that trace which Events the Evidence was derived from.

---

### **10.6 source\_snapshot\_refs**

References that trace which World State Snapshot or Runtime Snapshot the Evidence was derived from.

---

### **10.7 confidence\_score**

The trust score of the Evidence.

---

### **10.8 quality\_status**

The current quality status of the Evidence.

valid

degraded

stale

conflicting

invalid

---

## **11\. Registry Entry Example: worker\_location\_snapshot**

> **Non-normative placeholder.** This entry and the two that follow (Sections 12–13) are illustrative scaffolding only. Every concrete value — confidence thresholds, freshness windows (`max_age_seconds`), trust levels, and similar numeric or policy fields — is an example, not an approved domain decision. Per `AGENTS.md` Domain Authority Rule and Domain No-Guessing Rule, real freshness/confidence thresholds must be provided by a domain expert and approved through registry governance before this entry is treated as `active` in a real deployment.

evidence\_type\_id: evidence:worker\_location\_snapshot

canonical\_name: worker\_location\_snapshot

display\_name: Worker Location Snapshot

description: Evidence representing the location of a worker at a specific point in time.

semantic\_iri: ledo:WorkerLocationSnapshotEvidence

evidence\_category: SENSOR\_EVIDENCE

version: 1.0.0

status: active

allowed\_producer\_refs:

  \- producer:worker\_tracking\_gateway

  \- producer:world\_state\_service

  \- producer:worker\_proximity\_agent

allowed\_source\_event\_type\_refs:

  \- event:WorkerLocationUpdated

  \- event:WorkerEnteredZone

  \- event:WorkerExitedZone

allowed\_source\_system\_refs:

  \- system:uwb\_location\_system

  \- system:vision\_location\_system

  \- system:world\_state\_store

payload\_schema\_ref: schema:worker\_location\_snapshot\_payload\_v1

metadata\_schema\_ref: schema:evidence\_metadata\_v1

required\_fields:

  \- worker\_id

  \- position

  \- zone\_id

  \- coordinate\_frame

  \- confidence

optional\_fields:

  \- velocity

  \- floor\_id

  \- device\_id

applicable\_action\_type\_refs:

  \- action:STOP\_WORK

  \- action:LOCK\_ZONE

  \- action:DISPATCH\_ROBOT

  \- action:NOTIFY\_MANAGER

applicable\_decision\_rule\_refs:

  \- decision:stop\_work\_safety\_risk\_v1

  \- decision:dispatch\_robot\_v1

applicable\_approval\_rule\_refs:

  \- approval:stop\_work\_safety\_supervisor\_v1

  \- approval:dispatch\_robot\_supervisor\_v1

applicable\_safety\_gate\_refs:

  \- safety\_gate:worker\_proximity\_validation

  \- safety\_gate:hazard\_zone\_validation

freshness\_requirement:

  max\_age\_seconds: 10

  freshness\_policy\_ref: freshness:worker\_location\_real\_time

quality\_requirement:

  minimum\_confidence\_score: 0.85

  minimum\_source\_trust\_level: registered\_sensor\_gateway

  conflict\_policy\_ref: conflict:worker\_location\_conflict\_policy

lineage\_required: true

provenance\_required: true

manual\_verification\_allowed: false

retention\_policy\_ref: retention:worker\_location\_evidence\_short\_term

audit\_required: true

sensitivity\_level: restricted

pii\_classification: direct

decision\_boundary: may\_support\_decision\_case\_but\_not\_create\_decision

approval\_boundary: may\_support\_approval\_but\_not\_grant\_approval

execution\_boundary: does\_not\_create\_execution\_request

safety\_boundary: may\_block\_execution\_if\_stale\_or\_conflicting

audit\_event\_refs:

  \- audit:evidence\_created

  \- audit:evidence\_bound\_to\_decision

  \- audit:evidence\_validation\_failed

owner\_module: worker\_domain\_module

owner\_team: LEDO Worker Safety

source\_document: worker\_evidence\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_evidence\_type\_id: null

---

## **12\. Registry Entry Example: hazard\_detection\_snapshot**

> **Non-normative placeholder.** See the governance note in Section 11.

evidence\_type\_id: evidence:hazard\_detection\_snapshot

canonical\_name: hazard\_detection\_snapshot

display\_name: Hazard Detection Snapshot

description: Evidence representing a hazard detected at a specific point in time.

semantic\_iri: ledo:HazardDetectionSnapshotEvidence

evidence\_category: SENSOR\_EVIDENCE

version: 1.0.0

status: active

allowed\_producer\_refs:

  \- producer:hazard\_detection\_model

  \- producer:gas\_sensor\_gateway

  \- producer:vision\_safety\_model

  \- producer:safety\_risk\_agent

  \- producer:manual\_operator\_report

allowed\_source\_event\_type\_refs:

  \- event:HazardDetected

  \- event:GasLevelDetected

  \- event:VibrationThresholdExceeded

  \- event:ManualHazardReported

allowed\_source\_system\_refs:

  \- system:vision\_safety\_model

  \- system:gas\_sensor\_system

  \- system:operator\_ui

  \- system:world\_state\_store

payload\_schema\_ref: schema:hazard\_detection\_snapshot\_payload\_v1

metadata\_schema\_ref: schema:evidence\_metadata\_v1

required\_fields:

  \- hazard\_type

  \- hazard\_location

  \- severity

  \- confidence

  \- detection\_method

optional\_fields:

  \- affected\_zone\_id

  \- related\_worker\_ids

  \- related\_equipment\_ids

  \- image\_ref

  \- sensor\_snapshot\_ref

applicable\_action\_type\_refs:

  \- action:STOP\_WORK

  \- action:LOCK\_ZONE

  \- action:NOTIFY\_MANAGER

  \- action:REQUEST\_INSPECTION

applicable\_decision\_rule\_refs:

  \- decision:stop\_work\_safety\_risk\_v1

  \- decision:request\_inspection\_v1

applicable\_approval\_rule\_refs:

  \- approval:stop\_work\_safety\_supervisor\_v1

applicable\_safety\_gate\_refs:

  \- safety\_gate:hazard\_still\_present\_validation

  \- safety\_gate:zone\_lock\_validation

freshness\_requirement:

  max\_age\_seconds: 30

  freshness\_policy\_ref: freshness:hazard\_detection\_recent

quality\_requirement:

  minimum\_confidence\_score: 0.80

  minimum\_source\_trust\_level: registered\_safety\_source

  conflict\_policy\_ref: conflict:hazard\_detection\_conflict\_policy

lineage\_required: true

provenance\_required: true

manual\_verification\_allowed: true

retention\_policy\_ref: retention:safety\_evidence\_long\_term

audit\_required: true

sensitivity\_level: safety\_critical

pii\_classification: indirect

decision\_boundary: may\_trigger\_or\_support\_safety\_decision

approval\_boundary: may\_support\_safety\_approval\_but\_not\_grant\_approval

execution\_boundary: does\_not\_create\_execution\_request

safety\_boundary: stale\_or\_low\_confidence\_hazard\_evidence\_requires\_revalidation

audit\_event\_refs:

  \- audit:evidence\_created

  \- audit:safety\_evidence\_recorded

  \- audit:evidence\_bound\_to\_approval

  \- audit:evidence\_validation\_failed

owner\_module: safety\_domain\_module

owner\_team: LEDO Safety Governance

source\_document: safety\_evidence\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_evidence\_type\_id: null

---

## **13\. Registry Entry Example: robot\_availability\_snapshot**

> **Non-normative placeholder.** See the governance note in Section 11.

evidence\_type\_id: evidence:robot\_availability\_snapshot

canonical\_name: robot\_availability\_snapshot

display\_name: Robot Availability Snapshot

description: Evidence representing the availability status of a robot or robot fleet at a specific point in time.

semantic\_iri: ledo:RobotAvailabilitySnapshotEvidence

evidence\_category: WORLD\_STATE\_EVIDENCE

version: 1.0.0

status: active

allowed\_producer\_refs:

  \- producer:robot\_fleet\_manager

  \- producer:robot\_status\_gateway

  \- producer:world\_state\_service

  \- producer:robot\_dispatch\_agent

allowed\_source\_event\_type\_refs:

  \- event:RobotStatusUpdated

  \- event:RobotMissionStateChanged

  \- event:RobotUnavailable

  \- event:ExternalSystemStatusUpdated

allowed\_source\_system\_refs:

  \- system:robot\_fleet\_manager

  \- system:robot\_middleware

  \- system:world\_state\_store

payload\_schema\_ref: schema:robot\_availability\_snapshot\_payload\_v1

metadata\_schema\_ref: schema:evidence\_metadata\_v1

required\_fields:

  \- robot\_id

  \- availability\_status

  \- current\_mission\_status

  \- battery\_level

  \- capability\_refs

optional\_fields:

  \- current\_location

  \- estimated\_available\_at

  \- fault\_code

  \- fleet\_manager\_status

applicable\_action\_type\_refs:

  \- action:DISPATCH\_ROBOT

  \- action:REPLAN\_ROUTE

  \- action:PAUSE\_MISSION

  \- action:RETURN\_TO\_BASE

applicable\_decision\_rule\_refs:

  \- decision:dispatch\_robot\_v1

applicable\_approval\_rule\_refs:

  \- approval:dispatch\_robot\_supervisor\_v1

applicable\_safety\_gate\_refs:

  \- safety\_gate:robot\_available\_validation

  \- safety\_gate:fleet\_manager\_reachable\_validation

freshness\_requirement:

  max\_age\_seconds: 15

  freshness\_policy\_ref: freshness:robot\_status\_real\_time

quality\_requirement:

  minimum\_confidence\_score: 0.90

  minimum\_source\_trust\_level: registered\_robot\_system

  conflict\_policy\_ref: conflict:robot\_availability\_conflict\_policy

lineage\_required: true

provenance\_required: true

manual\_verification\_allowed: false

retention\_policy\_ref: retention:robot\_evidence\_medium\_term

audit\_required: true

sensitivity\_level: restricted

pii\_classification: none

decision\_boundary: may\_support\_robot\_dispatch\_decision

approval\_boundary: may\_support\_robot\_dispatch\_approval

execution\_boundary: does\_not\_dispatch\_robot

safety\_boundary: stale\_robot\_availability\_blocks\_dispatch\_execution

audit\_event\_refs:

  \- audit:evidence\_created

  \- audit:robot\_evidence\_recorded

  \- audit:evidence\_validation\_failed

owner\_module: robot\_domain\_module

owner\_team: LEDO Robotics Integration

source\_document: robot\_evidence\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_evidence\_type\_id: null

---

## **14\. Evidence Lifecycle Alignment**

Evidence is connected to the following lifecycle:

Event / World State / External System / Agent Output

        →
Evidence Generation or Evidence Binding

        →
Evidence Registry Validation

        →
Schema Validation

        →
Quality / Freshness / Source Trust Validation

        →
Evidence Instance

        →
EvidenceBundle

        →
ActionCandidate / DecisionCase / ApprovalRequest / SafetyGatePass or SafetyGateBlock

        →
AuditRecord

The important point is that Evidence may support judgment, but it must not bypass lifecycle boundaries.

Evidence may support a DecisionCase.

Evidence may support an ApprovalRequest.

Evidence may be used for Safety Gate validation.

However, Evidence must not directly create an ApprovedAction or ExecutionRequest.

---

## **15\. Validation Rules**

An Evidence Type is valid only when the following conditions are satisfied:

1. `evidence_type_id` exists in the registry.  
2. Its status is `active`.  
3. Evidence category is declared.  
4. Allowed producers are declared.  
5. Allowed source event types or source systems are declared.  
6. Payload schema reference is declared.  
7. Metadata schema reference is declared.  
8. Required fields are declared.  
9. Applicable Action / Decision / Approval / Safety Gate references are declared.  
10. Freshness requirement is declared.  
11. Quality requirement is declared.  
12. Retention policy is declared.  
13. Sensitivity level is declared.  
14. Decision / approval / execution / safety boundaries are declared.  
15. Owner module is declared.  
16. Version is valid.  
17. If deprecated, migration metadata exists.

If any of these conditions are missing, the Evidence Type must not be used in the operational lifecycle.

---

## **16\. Evidence Instance Validation**

An Evidence Instance may be accepted only when the following conditions are satisfied:

Does the Evidence Type exist in the registry?

Is the Evidence Type active?

Is the producer allowed?

Is the source event type allowed?

Is the source system allowed?

Does the payload pass schema validation?

Does the metadata pass the evidence metadata schema?

Are all required fields present?

Does it satisfy the freshness requirement?

Is the confidence score above the minimum threshold?

Is the source trust level sufficient?

If lineage is required, does lineage exist?

Does it satisfy PII and sensitivity rules?

If these conditions are not satisfied, the evidence must be handled with one of the following statuses:

rejected

quarantined

stale

degraded

conflicting

requires\_manual\_verification

---

## **17\. Evidence Freshness Rule**

In a Cyber-Physical System, evidence freshness is critical.

Even the same evidence can no longer be used for judgment after enough time has passed.

Examples:

worker\_location\_snapshot: within 10 seconds

robot\_availability\_snapshot: within 15 seconds

hazard\_detection\_snapshot: within 30 seconds

approval\_context\_evidence: within 5 minutes

execution\_feedback\_evidence: long-lived

Expired evidence freshness should be handled as follows:

DecisionCase: hold\_for\_more\_evidence

ApprovalRequest: request new evidence

SafetyGate: fail or requires\_runtime\_revalidation

ExecutionRequest: cannot be created

Core principle:

Stale Evidence must not support Safety Gate pass.

---

## **18\. Evidence Quality Rule**

Evidence must have quality requirements.

Recommended quality criteria:

confidence\_score

source\_trust\_level

schema\_validity

freshness\_status

lineage\_completeness

provenance\_status

conflict\_status

manual\_verification\_status

sensor\_accuracy

model\_eval\_score

Evidence quality statuses:

valid

degraded

stale

conflicting

invalid

requires\_manual\_verification

Examples:

If confidence\_score \< 0.80, hazard evidence must not be used as a basis for automatic approval.

If worker\_location evidence is conflicting, the Safety Gate must revalidate it.

If sensor freshness is stale, robot dispatch must not proceed.

---

## **19\. Evidence Conflict Rule**

Multiple pieces of evidence may conflict with one another.

Example:

WorkerLocationUpdated event says the worker is in zone\_03.

Vision detection says the worker is in zone\_04.

UWB tracking has confidence 0.62.

In this case, an evidence conflict policy is required.

Recommended conflict handling outcomes:

prefer\_high\_trust\_source

prefer\_latest

require\_manual\_review

hold\_for\_more\_evidence

trigger\_recompute

block\_safety\_gate

In a safety-critical domain, conflicting evidence must not be ignored.

Core principle:

Conflicting safety evidence must trigger review or revalidation.

---

## **20\. Evidence Binding Rule**

Evidence must be explicitly bound to lifecycle objects.

Binding targets:

ActionCandidate

DecisionCase

ApprovalRequest

ApprovalDecision

SafetyGatePass or SafetyGateBlock

ExecutionResult

AuditRecord

Evidence Binding must record the following:

binding\_id: string

evidence\_id: string

bound\_to\_object\_type: string

bound\_to\_object\_id: string

binding\_purpose: string

bound\_at: datetime

bound\_by: string

binding\_trace\_id: string

If evidence was used in judgment, it must be traceable.

Which evidence was used in which DecisionCase?

Which evidence influenced which ApprovalDecision?

Which runtime evidence did the Safety Gate review before passing?

---

## **21\. EvidenceBundle Rule**

EvidenceBundle is a judgment evidence package composed of multiple Evidence Instances.

EvidenceBundle must include the following:

evidence\_bundle\_id: string

bundle\_purpose: string

related\_lifecycle\_object\_ref: string

evidence\_refs:

  \- string

created\_at: datetime

created\_by: string

completeness\_status: complete | partial | insufficient

quality\_status: valid | degraded | stale | conflicting | invalid

EvidenceBundle is very important for Decisions and Approvals.

Example:

A STOP\_WORK DecisionCase requires the following EvidenceBundle:

\- hazard\_detection\_snapshot

\- worker\_location\_snapshot

\- risk\_assessment\_snapshot

\- sensor\_freshness\_snapshot

---

## **22\. Lineage and Provenance Rule**

Evidence must have lineage and provenance.

### **22.1 Lineage**

Lineage indicates the data flow through which the evidence was generated.

Example:

Sensor Event

    - World State Update

    - Risk Agent Analysis

    - Evidence Instance

    - EvidenceBundle

    - DecisionCase

---

### **22.2 Provenance**

Provenance indicates the source and generation responsibility of the evidence.

Examples:

Who generated it?

Which system generated it?

Which model version was used?

Which sensor did it come from?

Which timestamp is it based on?

From an ontology perspective, this can be connected with PROV-O.

---

## **23\. Relationship to Event Registry**

`event_registry` defines which event occurred.

`evidence_registry` defines which evidence can be created from that event.

event\_registry:

    What payload and meaning does the HazardDetected event have?

evidence\_registry:

    Can hazard\_detection\_snapshot evidence be created from the HazardDetected event?

An Event can be the source of Evidence, but an Event itself is not always Evidence.

---

## **24\. Relationship to Agent Vocabulary Registry**

`agent_vocabulary_registry` restricts which evidence an Agent can generate or use.

agent\_vocabulary\_registry:

    Is SAFETY\_RISK\_AGENT allowed to use hazard\_detection\_snapshot?

evidence\_registry:

    What schema and quality requirements does hazard\_detection\_snapshot have?

Agents must not create arbitrary Evidence Types.

---

## **25\. Relationship to Action Registry**

`action_registry` declares which evidence is required for a specific Action Type.

`evidence_registry` defines the schema, freshness, quality, and source rules for that Evidence Type.

action\_registry:

    STOP\_WORK requires hazard\_detection\_snapshot.

evidence\_registry:

    Under what conditions is hazard\_detection\_snapshot valid?

---

## **26\. Relationship to Decision Registry**

`decision_registry` declares which evidence a DecisionCase must evaluate.

`evidence_registry` validates whether that evidence is valid.

decision\_registry:

    STOP\_WORK Decision requires worker\_location\_snapshot.

evidence\_registry:

    Is the worker\_location\_snapshot fresh and trustworthy?

---

## **27\. Relationship to Approval Registry**

`approval_registry` declares which evidence is required before an ApprovalDecision.

`evidence_registry` validates whether that evidence has sufficient quality to be used for approval.

approval\_registry:

    STOP\_WORK approval requires hazard\_detection\_snapshot and risk\_assessment\_snapshot.

evidence\_registry:

    Are these evidence items not stale, conflicting, or invalid?

---

## **28\. Relationship to Safety Gate**

The Safety Gate uses runtime evidence.

The following evidence is especially important:

sensor\_freshness\_snapshot

worker\_location\_snapshot

zone\_status\_snapshot

robot\_availability\_snapshot

adapter\_health\_snapshot

external\_system\_reachable\_snapshot

world\_state\_consistency\_snapshot

Core principle:

Evidence used during approval must not be assumed valid at Safety Gate time.

The Safety Gate must re-check fresh runtime evidence immediately before execution.

---

## **29\. Relationship to Runtime Validation Registry**

`runtime_validation_registry` defines which runtime validations should be performed.

`evidence_registry` defines the Evidence Types and quality requirements needed for those validations.

runtime\_validation\_registry:

    Performs worker\_not\_in\_hazard\_zone validation.

evidence\_registry:

    This validation requires fresh worker\_location\_snapshot and hazard\_zone\_snapshot.

---

## **30\. Relationship to Audit Registry**

Evidence usage must be auditable.

Audit targets:

evidence\_created

evidence\_validated

evidence\_rejected

evidence\_bound\_to\_action\_candidate

evidence\_bound\_to\_decision

evidence\_bound\_to\_approval

evidence\_bound\_to\_safety\_gate

evidence\_conflict\_detected

evidence\_stale\_detected

Judgment without evidence cannot be explained after the fact.

Therefore, EvidenceBundles used in Decisions, Approvals, and Safety Gate validation must always remain in the audit trace.

---

## **31\. Relationship to Ontology**

Every important Evidence Type should have a semantic IRI.

Example:

evidence\_type\_id: evidence:hazard\_detection\_snapshot

semantic\_iri: ledo:HazardDetectionSnapshotEvidence

In the ontology, it may be defined as follows:

ledo:HazardDetectionSnapshotEvidence

    rdf:type ledo:EvidenceType ;

    rdfs:subClassOf ledo:SafetyEvidence ;

    ledo:evidenceFor ledo:Hazard ;

    ledo:maySupportAction ledo:StopWorkAction ;

    ledo:requiresSource ledo:HazardDetectedEvent ;

    ledo:hasFreshnessRequirement ledo:HazardDetectionRecent .

Ontology provides the semantic foundation of Evidence.

Evidence Registry manages this foundation in the operational system through version, schema, freshness, quality, source, retention, and audit rules.

---

## **32\. Versioning and Migration**

Evidence Types must be versioned.

A version change is required when any of the following changes:

1. Payload schema changes  
2. Required fields change  
3. Metadata schema changes  
4. Allowed producers change  
5. Allowed source events change  
6. Applicable Action / Decision / Approval / Safety Gate references change  
7. Freshness requirements change  
8. Quality requirements change  
9. Trust levels change  
10. Retention policy changes  
11. Sensitivity level changes  
12. Boundaries change

Status values:

draft

active

deprecated

migration\_required

retired

blocked

A deprecated Evidence Type must declare:

deprecated\_since: datetime

replacement\_evidence\_type\_id: string | null

migration\_notes: string

A blocked Evidence Type must not be accepted as a new Evidence Instance.

---

## **33\. Implementation Use**

`evidence_registry` is used to generate or validate:

1. `EvidenceType` enum  
2. `EvidenceCategory` enum  
3. Evidence metadata schema  
4. Evidence payload DTO constraints  
5. Evidence producer validation  
6. Evidence source validation  
7. Evidence schema validation  
8. Evidence freshness validation  
9. Evidence quality validation  
10. Evidence conflict validation  
11. EvidenceBundle validation  
12. Evidence binding validation  
13. Decision evidence requirement lookup  
14. Approval evidence requirement lookup  
15. Safety Gate evidence lookup  
16. Audit log expectations  
17. Test case generation  
18. Migration rules

Implementation must not create or use unregistered Evidence Types for judgment.

---

## **34\. Recommended Code Structure**

registries/

    evidence\_registry/

        evidence\_registry.py

        evidence\_registry\_entry.py

        evidence\_category.py

        evidence\_status.py

        evidence\_quality.py

        evidence\_binding.py

        evidence\_bundle.py

        evidence\_validation.py

        evidence\_errors.py

        evidence\_loader.py

        evidence\_migration.py

    event\_registry/

    schema\_registry/

    agent\_vocabulary\_registry/

    action\_registry/

    decision\_registry/

    approval\_registry/

    runtime\_validation\_registry/

    audit\_event\_registry/

---

## **35\. Minimal Pydantic Model**

from enum import Enum

from pydantic import BaseModel, Field

from typing import Optional

from datetime import datetime

class EvidenceStatus(str, Enum):

    DRAFT \= "draft"

    ACTIVE \= "active"

    DEPRECATED \= "deprecated"

    MIGRATION\_REQUIRED \= "migration\_required"

    RETIRED \= "retired"

    BLOCKED \= "blocked"

class EvidenceCategory(str, Enum):

    SENSOR\_EVIDENCE \= "sensor\_evidence"

    WORLD\_STATE\_EVIDENCE \= "world\_state\_evidence"

    AGENT\_EVIDENCE \= "agent\_evidence"

    POLICY\_EVIDENCE \= "policy\_evidence"

    RISK\_EVIDENCE \= "risk\_evidence"

    APPROVAL\_EVIDENCE \= "approval\_evidence"

    RUNTIME\_VALIDATION\_EVIDENCE \= "runtime\_validation\_evidence"

    EXECUTION\_FEEDBACK\_EVIDENCE \= "execution\_feedback\_evidence"

    AUDIT\_EVIDENCE \= "audit\_evidence"

    MANUAL\_EVIDENCE \= "manual\_evidence"

    EXTERNAL\_SYSTEM\_EVIDENCE \= "external\_system\_evidence"

class EvidenceQualityStatus(str, Enum):

    VALID \= "valid"

    DEGRADED \= "degraded"

    STALE \= "stale"

    CONFLICTING \= "conflicting"

    INVALID \= "invalid"

    REQUIRES\_MANUAL\_VERIFICATION \= "requires\_manual\_verification"

class SensitivityLevel(str, Enum):

    PUBLIC \= "public"

    INTERNAL \= "internal"

    CONFIDENTIAL \= "confidential"

    RESTRICTED \= "restricted"

    SAFETY\_CRITICAL \= "safety\_critical"

class PIIClassification(str, Enum):

    NONE \= "none"

    INDIRECT \= "indirect"

    DIRECT \= "direct"

    SENSITIVE \= "sensitive"

class FreshnessRequirement(BaseModel):

    max\_age\_seconds: int

    freshness\_policy\_ref: str

class QualityRequirement(BaseModel):

    minimum\_confidence\_score: float

    minimum\_source\_trust\_level: str

    conflict\_policy\_ref: str

class EvidenceRegistryEntry(BaseModel):

    evidence\_type\_id: str

    canonical\_name: str

    display\_name: str

    description: str

    semantic\_iri: str

    evidence\_category: EvidenceCategory

    version: str

    status: EvidenceStatus \= EvidenceStatus.DRAFT

    allowed\_producer\_refs: list\[str\] \= Field(default\_factory=list)

    allowed\_source\_event\_type\_refs: list\[str\] \= Field(default\_factory=list)

    allowed\_source\_system\_refs: list\[str\] \= Field(default\_factory=list)

    payload\_schema\_ref: str

    metadata\_schema\_ref: str

    required\_fields: list\[str\] \= Field(default\_factory=list)

    optional\_fields: list\[str\] \= Field(default\_factory=list)

    applicable\_action\_type\_refs: list\[str\] \= Field(default\_factory=list)

    applicable\_decision\_rule\_refs: list\[str\] \= Field(default\_factory=list)

    applicable\_approval\_rule\_refs: list\[str\] \= Field(default\_factory=list)

    applicable\_safety\_gate\_refs: list\[str\] \= Field(default\_factory=list)

    freshness\_requirement: FreshnessRequirement

    quality\_requirement: QualityRequirement

    lineage\_required: bool \= True

    provenance\_required: bool \= True

    manual\_verification\_allowed: bool \= False

    retention\_policy\_ref: str

    audit\_required: bool \= True

    sensitivity\_level: SensitivityLevel \= SensitivityLevel.INTERNAL

    pii\_classification: PIIClassification \= PIIClassification.NONE

    decision\_boundary: str

    approval\_boundary: str

    execution\_boundary: str

    safety\_boundary: str

    audit\_event\_refs: list\[str\] \= Field(default\_factory=list)

    owner\_module: str

    owner\_team: str

    source\_document: str

    created\_at: datetime

    updated\_at: datetime

    deprecated\_since: Optional\[datetime\] \= None

    replacement\_evidence\_type\_id: Optional\[str\] \= None

---

## **36\. Core Validation Function**

from datetime import datetime, timezone

def validate\_evidence\_instance(

    entry: EvidenceRegistryEntry,

    evidence\_type\_id: str,

    producer\_ref: str,

    source\_event\_type\_ref: str | None,

    source\_system\_ref: str | None,

    payload: dict,

    generated\_at: datetime,

    confidence\_score: float,

) \-\> None:

    if entry.status \!= EvidenceStatus.ACTIVE:

        raise InvalidEvidenceTypeError(

            f"Evidence Type is not active: {entry.evidence\_type\_id}"

        )

    if evidence\_type\_id \!= entry.evidence\_type\_id:

        raise EvidenceTypeMismatchError(

            f"Evidence Type '{evidence\_type\_id}' does not match registry entry "

            f"'{entry.evidence\_type\_id}'"

        )

    if producer\_ref not in entry.allowed\_producer\_refs:

        raise EvidenceProducerNotAllowedError(

            f"Producer '{producer\_ref}' is not allowed for Evidence Type "

            f"'{entry.evidence\_type\_id}'"

        )

    if source\_event\_type\_ref is not None:

        if source\_event\_type\_ref not in entry.allowed\_source\_event\_type\_refs:

            raise EvidenceSourceEventNotAllowedError(

                f"Source Event Type '{source\_event\_type\_ref}' is not allowed"

            )

    if source\_system\_ref is not None:

        if source\_system\_ref not in entry.allowed\_source\_system\_refs:

            raise EvidenceSourceSystemNotAllowedError(

                f"Source System '{source\_system\_ref}' is not allowed"

            )

    for field in entry.required\_fields:

        if field not in payload:

            raise EvidencePayloadValidationError(

                f"Required field '{field}' is missing from evidence payload"

            )

    now \= datetime.now(timezone.utc)

    age\_seconds \= (now \- generated\_at).total\_seconds()

    if age\_seconds \> entry.freshness\_requirement.max\_age\_seconds:

        raise EvidenceStaleError(

            f"Evidence is stale. Age={age\_seconds}s, "

            f"max={entry.freshness\_requirement.max\_age\_seconds}s"

        )

    if confidence\_score \< entry.quality\_requirement.minimum\_confidence\_score:

        raise EvidenceQualityError(

            f"Evidence confidence score is too low: {confidence\_score}"

        )

    if not entry.payload\_schema\_ref:

        raise InvalidEvidenceRegistryEntryError(

            "payload\_schema\_ref must be declared"

        )

    if not entry.metadata\_schema\_ref:

        raise InvalidEvidenceRegistryEntryError(

            "metadata\_schema\_ref must be declared"

        )

---

## **37\. Test Scenarios**

Required tests:

1\. Reject unregistered Evidence Type.

2\. Reject inactive Evidence Type.

3\. Reject deprecated Evidence Type.

4\. Reject blocked Evidence Type.

5\. Reject evidence generated by an unauthorized producer.

6\. Reject unauthorized source event type.

7\. Reject unauthorized source system.

8\. Reject payload schema mismatch.

9\. Reject missing required field.

10\. Reject expired or stale evidence.

11\. Reject evidence below the confidence score threshold.

12\. Reject evidence below the source trust level threshold.

13\. Reject evidence with missing lineage.

14\. Verify conflicting evidence handling.

15\. Verify EvidenceBundle completeness.

16\. Verify hold\_for\_more\_evidence when required evidence is missing from DecisionCase.

17\. Verify that approval cannot proceed when required evidence is missing from ApprovalRequest.

18\. Verify that stale evidence cannot be used by the Safety Gate.

19\. Verify evidence binding audit trace creation.

20\. Verify evidence migration rules.

---

## **38\. Final Rule**

No registered Evidence Type,

no valid Evidence Instance.

No valid Evidence Instance,

no valid EvidenceBundle.

No required EvidenceBundle,

no DecisionCase progression.

No required Evidence,

no valid ApprovalRequest approval.

No fresh runtime Evidence,

no Safety Gate pass.

Evidence is not ActionCandidate.

Evidence is not DecisionCase.

Evidence is not ApprovalDecision.

Evidence is not ExecutionRequest.

Evidence is not PhysicalCommand.

`evidence_registry` is the core deterministic registry that governs the basis of every judgment in the LEDO system.

This module defines the meaning, schema, source, freshness, quality, trust, lineage, provenance, binding, retention, and audit rules of Evidence Types, and ensures that unsupported ActionCandidates, DecisionCases, ApprovalDecisions, and Safety Gate pass/block outputs cannot be created.

The core definition is:

Evidence Registry

\= not a list of evidence names,

but an operational contract registry that controls

the meaning, structure, source, trust, freshness,

quality, lineage, binding, and audit rules

of all evidence used for judgment.

