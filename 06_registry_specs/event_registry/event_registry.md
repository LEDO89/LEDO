# **Event registry**

## **1\. Overview**

`event_registry` is a core registry in the LEDO Ontology-Centric Cyber-Physical System. It defines and governs all Event Types, Event Categories, Event Schemas, Event Sources, Event Payload Contracts, Event Routing Rules, Event Lifecycles, Event Retention Rules, and Event Audit Rules used across the system.

The purpose of this registry is to prevent uncontrolled creation of arbitrary events inside the system and to ensure that every event follows a registered Event Type, schema, source rule, routing rule, lifecycle rule, and audit rule.

`event_registry` is not a simple list of event names.

It is an **operational contract registry for event meaning, structure, flow, and traceability** that defines the following:

Which Event Types may exist?

What does each Event mean?

Which source may produce the Event?

Which schema must the Event payload follow?

Which topic or stream should the Event be routed to?

Can the Event update the World State?

Can the Event trigger Agent, Decision, Approval, Execution, or Audit flows?

How long should the Event be retained?

Can the Event be replayed?

Must the Event be processed idempotently?

In other words, `event_registry` is the core registry that manages all system events with controlled meaning and structure.

---

## **2\. Core Principle**

An Event is a record of a fact or state change.

An Event is not a command.

An Event is not approval.

An Event is not physical execution.

An Event is not an `ActionCandidate`.

An Event is not an `ExecutionRequest`.

The basic meaning of an Event is:

Something occurred.

Something changed state.

Something was observed.

Something was requested.

Something returned a result.

Something must be recorded for audit.

Events are like the bloodstream of the system.

However, an Event must not become an execution command.

The core principle is:

Event informs.

Action proposes.

Decision evaluates.

Approval authorizes.

Safety Gate validates.

ExecutionRequest prepares execution.

External System performs physical execution.

---

## **3\. Position in the LEDO Architecture**

`event_registry` does not belong to only one specific layer.  
It is a cross-cutting registry across the entire LEDO system.

Sensors / External Systems / Agents / UI / Workflow

        ↓

Event creation

        ↓

event\_registry validation

        ↓

Kafka / MQTT / Event Bus / Stream

        ↓

World State Update / Agent Trigger / Decision Trigger / Audit Log

        ↓

ActionCandidate / DecisionCase / Approval / Execution Feedback

`event_registry` is connected to all of the following layers:

Real-Time World State Layer

Distributed Domain Agent Layer

Decision Router / Escalation Layer

Approval Layer

Safety Gate Layer

Unified Cyber-Physical Core Layer

Execution Integration Layer

Observability / Audit / Trace Layer

---

## **4\. Purpose**

The purpose of `event_registry` is to ensure the following:

1. Prevent creation of unregistered Event Types  
2. Define meaning and schema for each Event Type  
3. Define Event source and producer authority  
4. Define Event payload validation rules  
5. Define Event topic / stream routing rules  
6. Define whether an Event may update World State  
7. Define whether an Event may trigger agents  
8. Define whether an Event may trigger decision, approval, or execution workflows  
9. Define Event idempotency requirements  
10. Define whether an Event is replayable  
11. Define Event ordering requirements  
12. Define Event retention and archival rules  
13. Define Event audit and trace rules  
14. Manage Event versioning and migration  
15. Manage semantic alignment between Events and ontology classes, properties, and relations

---

## **5\. Core Distinctions**

### **5.1 Event Type**

`Event Type` is the controlled type of event allowed in the system.

Examples:

WorkerLocationUpdated

HazardDetected

ZoneStatusChanged

RobotStatusUpdated

EquipmentStatusChanged

ActionCandidateCreated

DecisionCaseCreated

ApprovalRequested

ApprovalGranted

SafetyGatePassed

ExecutionRequestCreated

ExecutionResultReceived

FeedbackEventReceived

AuditRecordCreated

Event Type defines “what happened.”

---

### **5.2 Event Instance**

`Event Instance` is an actual runtime event occurrence.

Example:

event\_id: evt\_01HT...

event\_type: WorkerLocationUpdated

occurred\_at: 2026-06-26T09:00:00Z

source: worker\_tracking\_system

payload: {...}

Event Type is the design-level definition.

Event Instance is the actual occurrence record.

---

### **5.3 Event Category**

Event Category functionally classifies Event Types.

Examples:

SENSOR\_EVENT

WORLD\_STATE\_EVENT

AGENT\_EVENT

ACTION\_EVENT

DECISION\_EVENT

APPROVAL\_EVENT

SAFETY\_GATE\_EVENT

EXECUTION\_EVENT

FEEDBACK\_EVENT

AUDIT\_EVENT

SYSTEM\_EVENT

ERROR\_EVENT

Category is used to determine routing, retention, audit, priority, and replay rules.

---

### **5.4 Event Source**

Event Source is the entity that produced the event.

Examples:

sensor\_gateway

worker\_tracking\_system

robot\_fleet\_manager

scada\_system

plc\_gateway

domain\_agent

decision\_engine

approval\_service

safety\_gate

execution\_dispatcher

external\_adapter

operator\_ui

audit\_service

Event Source must be registered and validated.

---

### **5.5 Event Payload**

Event Payload is the data carried by the event.

Payload must follow a registered schema.

Example:

{

  "worker\_id": "worker\_123",

  "zone\_id": "zone\_03",

  "position": {

    "x": 12.4,

    "y": 7.8,

    "z": 0.0

  },

  "confidence": 0.94

}

Payload differs by Event Type, but core metadata must always be maintained.

---

## **6\. Scope**

`event_registry` controls the following fields:

event\_type\_id: string

canonical\_name: string

display\_name: string

description: string

semantic\_iri: string

event\_category: string

version: string

status: draft | active | deprecated | migration\_required | retired | blocked

allowed\_producer\_refs:

  \- string

allowed\_source\_types:

  \- string

payload\_schema\_ref: string

metadata\_schema\_ref: string

required\_fields:

  \- string

optional\_fields:

  \- string

topic\_refs:

  \- string

stream\_refs:

  \- string

routing\_rule\_ref: string

world\_state\_effect: none | update | append | invalidate | trigger\_recompute

agent\_trigger\_allowed: boolean

decision\_trigger\_allowed: boolean

approval\_trigger\_allowed: boolean

execution\_trigger\_allowed: boolean

audit\_required: boolean

idempotency\_required: boolean

idempotency\_key\_strategy: string

ordering\_requirement: none | per\_entity | per\_site | global

replay\_allowed: boolean

retention\_policy\_ref: string

producer\_authority\_level: string

consumer\_scope\_refs:

  \- string

sensitivity\_level: public | internal | confidential | restricted | safety\_critical

pii\_classification: none | indirect | direct | sensitive

decision\_boundary: string

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

replacement\_event\_type\_id: string | null

---

## **7\. Non-Scope**

`event_registry` does not define the following:

1. Complete Kafka broker configuration  
2. Complete MQTT broker configuration  
3. Raw sensor driver logic  
4. PLC / SCADA command logic  
5. Robot motion planning  
6. Complete policy pass/fail logic  
7. Approval authority itself  
8. Final Safety Gate decision logic  
9. Adapter instance selection  
10. Low-level database storage implementation  
11. All domain threshold values  
12. All event processing algorithms  
13. Complete stream processing topology

These responsibilities belong to the following modules or systems:

message\_broker

stream\_processor

sensor\_gateway

world\_state\_store

policy\_registry

approval\_registry

decision\_registry

safety\_gate

adapter\_registry

external\_system\_registry

domain\_module

Kafka / MQTT / Redis / TimescaleDB

---

## **8\. Event Category Model**

Recommended Event Categories are:

SENSOR\_EVENT

WORLD\_STATE\_EVENT

AGENT\_EVENT

ACTION\_EVENT

DECISION\_EVENT

APPROVAL\_EVENT

SAFETY\_GATE\_EVENT

EXECUTION\_EVENT

EXTERNAL\_SYSTEM\_EVENT

FEEDBACK\_EVENT

AUDIT\_EVENT

SYSTEM\_EVENT

ERROR\_EVENT

SECURITY\_EVENT

### **8.1 SENSOR\_EVENT**

An event generated by sensors, IoT devices, location trackers, cameras, or environmental measurement devices.

Examples:

WorkerLocationUpdated

TemperatureSensorUpdated

GasLevelDetected

VibrationThresholdExceeded

---

### **8.2 WORLD\_STATE\_EVENT**

An event representing a change in World State.

Examples:

ZoneStatusChanged

EquipmentAvailabilityChanged

RobotMissionStateChanged

WorkerEnteredZone

WorkerExitedZone

---

### **8.3 AGENT\_EVENT**

An event related to agent observation, analysis, recommendation, or candidate generation.

Examples:

AgentObservationCreated

RiskSignalCreated

ActionCandidateCreated

EvidenceBundleCreated

---

### **8.4 ACTION\_EVENT**

An event related to the ActionCandidate or Action Type lifecycle.

Examples:

ActionCandidateCreated

ActionCandidateValidated

ActionCandidateRejected

---

### **8.5 DECISION\_EVENT**

An event related to DecisionCase and judgment flow.

Examples:

DecisionCaseCreated

DecisionEvidenceEvaluated

DecisionPolicyEvaluated

DecisionOutcomeSelected

DecisionEscalated

---

### **8.6 APPROVAL\_EVENT**

An event related to the approval lifecycle.

Examples:

ApprovalRequested

ApprovalGranted

ApprovalRejected

ApprovalExpired

ApprovalRevoked

---

### **8.7 SAFETY\_GATE\_EVENT**

An event related to Safety Gate validation results.

Examples:

SafetyGateValidationStarted

SafetyGatePassed

SafetyGateFailed

SafetyGateBlocked

---

### **8.8 EXECUTION\_EVENT**

An event related to ExecutionRequest and ExecutionDispatcher flow.

Examples:

ExecutionRequestCreated

ExecutionDispatched

ExecutionAcceptedByAdapter

ExecutionRejectedByAdapter

ExecutionTimedOut

---

### **8.9 FEEDBACK\_EVENT**

An event related to feedback returned from external systems.

Examples:

ExternalExecutionStarted

ExternalExecutionCompleted

ExternalExecutionFailed

RobotMissionFeedbackReceived

SCADAStatusFeedbackReceived

---

### **8.10 AUDIT\_EVENT**

An event generated for audit and traceability.

Examples:

AuditRecordCreated

PolicyDecisionAudited

ApprovalDecisionAudited

ExecutionTraceRecorded

---

## **9\. Registry Entry Schema**

Each Event Registry entry should follow this structure:

event\_type\_id: string

canonical\_name: string

display\_name: string

description: string

semantic\_iri: string

event\_category: string

version: string

status: draft | active | deprecated | migration\_required | retired | blocked

allowed\_producer\_refs:

  \- string

allowed\_source\_types:

  \- string

payload\_schema\_ref: string

metadata\_schema\_ref: string

required\_fields:

  \- string

optional\_fields:

  \- string

topic\_refs:

  \- string

stream\_refs:

  \- string

routing\_rule\_ref: string

world\_state\_effect: none | update | append | invalidate | trigger\_recompute

agent\_trigger\_allowed: boolean

decision\_trigger\_allowed: boolean

approval\_trigger\_allowed: boolean

execution\_trigger\_allowed: boolean

audit\_required: boolean

idempotency\_required: boolean

idempotency\_key\_strategy: string

ordering\_requirement: none | per\_entity | per\_site | global

replay\_allowed: boolean

retention\_policy\_ref: string

producer\_authority\_level: string

consumer\_scope\_refs:

  \- string

sensitivity\_level: public | internal | confidential | restricted | safety\_critical

pii\_classification: none | indirect | direct | sensitive

decision\_boundary: string

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

replacement\_event\_type\_id: string | null

---

## **10\. Core Event Metadata Schema**

Every event instance must have at least the following metadata:

event\_id: string

event\_type\_id: string

event\_version: string

occurred\_at: datetime

observed\_at: datetime | null

received\_at: datetime

producer\_id: string

source\_system\_ref: string

site\_id: string | null

zone\_id: string | null

entity\_refs:

  \- string

correlation\_id: string | null

causation\_id: string | null

trace\_id: string | null

idempotency\_key: string

payload\_schema\_version: string

sensitivity\_level: string

### **10.1 event\_id**

A unique ID for each event instance.

---

### **10.2 occurred\_at**

The time when the actual event occurred.

---

### **10.3 observed\_at**

The time when a sensor or external system observed the event.

---

### **10.4 received\_at**

The time when the LEDO system received the event.

---

### **10.5 correlation\_id**

An ID that connects events belonging to the same workflow or lifecycle.

---

### **10.6 causation\_id**

The ID of the event that caused this event.

---

### **10.7 idempotency\_key**

A key used to prevent duplicate event processing.

---

## **11\. Registry Entry Example: WorkerLocationUpdated**

event\_type\_id: event:WorkerLocationUpdated

canonical\_name: worker\_location\_updated

display\_name: Worker Location Updated

description: Indicates that a worker's location information has been updated.

semantic\_iri: ledo:WorkerLocationUpdatedEvent

event\_category: SENSOR\_EVENT

version: 1.0.0

status: active

allowed\_producer\_refs:

  \- producer:worker\_tracking\_gateway

  \- producer:uwb\_location\_system

  \- producer:vision\_location\_system

allowed\_source\_types:

  \- sensor\_gateway

  \- location\_tracking\_system

payload\_schema\_ref: schema:worker\_location\_updated\_payload\_v1

metadata\_schema\_ref: schema:core\_event\_metadata\_v1

required\_fields:

  \- worker\_id

  \- position

  \- confidence

  \- coordinate\_frame

optional\_fields:

  \- velocity

  \- floor\_id

  \- device\_id

topic\_refs:

  \- topic:site.worker.location.updated

stream\_refs:

  \- stream:world\_state\_worker\_location

routing\_rule\_ref: routing:worker\_location\_update\_routing

world\_state\_effect: update

agent\_trigger\_allowed: true

decision\_trigger\_allowed: false

approval\_trigger\_allowed: false

execution\_trigger\_allowed: false

audit\_required: false

idempotency\_required: true

idempotency\_key\_strategy: worker\_id\_occurred\_at\_source

ordering\_requirement: per\_entity

replay\_allowed: true

retention\_policy\_ref: retention:worker\_location\_short\_term

producer\_authority\_level: registered\_sensor\_gateway

consumer\_scope\_refs:

  \- consumer:world\_state\_service

  \- consumer:safety\_risk\_agent

  \- consumer:worker\_proximity\_agent

sensitivity\_level: restricted

pii\_classification: direct

decision\_boundary: does\_not\_create\_decision\_case\_directly

execution\_boundary: does\_not\_create\_execution\_request

safety\_boundary: may\_trigger\_safety\_analysis\_but\_not\_safety\_gate\_pass

audit\_event\_refs:

  \- audit:event\_received

  \- audit:event\_validation\_failed

owner\_module: worker\_domain\_module

owner\_team: LEDO Worker Safety

source\_document: worker\_event\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_event\_type\_id: null

---

## **12\. Registry Entry Example: HazardDetected**

event\_type\_id: event:HazardDetected

canonical\_name: hazard\_detected

display\_name: Hazard Detected

description: Indicates that a hazard has been detected on site.

semantic\_iri: ledo:HazardDetectedEvent

event\_category: SENSOR\_EVENT

version: 1.0.0

status: active

allowed\_producer\_refs:

  \- producer:hazard\_detection\_model

  \- producer:gas\_sensor\_gateway

  \- producer:vision\_safety\_model

  \- producer:manual\_operator\_report

allowed\_source\_types:

  \- sensor\_gateway

  \- ai\_model

  \- operator\_ui

payload\_schema\_ref: schema:hazard\_detected\_payload\_v1

metadata\_schema\_ref: schema:core\_event\_metadata\_v1

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

topic\_refs:

  \- topic:site.safety.hazard.detected

stream\_refs:

  \- stream:safety\_events

  \- stream:world\_state\_hazard

routing\_rule\_ref: routing:hazard\_detected\_routing

world\_state\_effect: append

agent\_trigger\_allowed: true

decision\_trigger\_allowed: true

approval\_trigger\_allowed: false

execution\_trigger\_allowed: false

audit\_required: true

idempotency\_required: true

idempotency\_key\_strategy: hazard\_type\_location\_time\_window\_source

ordering\_requirement: per\_site

replay\_allowed: true

retention\_policy\_ref: retention:safety\_event\_long\_term

producer\_authority\_level: registered\_safety\_source

consumer\_scope\_refs:

  \- consumer:world\_state\_service

  \- consumer:safety\_risk\_agent

  \- consumer:decision\_engine

  \- consumer:audit\_service

sensitivity\_level: safety\_critical

pii\_classification: indirect

decision\_boundary: may\_trigger\_decision\_case\_creation

execution\_boundary: does\_not\_create\_execution\_request

safety\_boundary: hazard\_event\_must\_not\_directly\_trigger\_physical\_command

audit\_event\_refs:

  \- audit:event\_received

  \- audit:event\_validated

  \- audit:safety\_event\_recorded

owner\_module: safety\_domain\_module

owner\_team: LEDO Safety Governance

source\_document: safety\_event\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_event\_type\_id: null

---

## **13\. Registry Entry Example: ActionCandidateCreated**

event\_type\_id: event:ActionCandidateCreated

canonical\_name: action\_candidate\_created

display\_name: Action Candidate Created

description: Indicates that an agent or workflow has created an ActionCandidate.

semantic\_iri: ledo:ActionCandidateCreatedEvent

event\_category: ACTION\_EVENT

version: 1.0.0

status: active

allowed\_producer\_refs:

  \- producer:safety\_risk\_agent

  \- producer:robot\_dispatch\_agent

  \- producer:workflow\_engine

  \- producer:operator\_ui

allowed\_source\_types:

  \- domain\_agent

  \- workflow\_engine

  \- operator\_ui

payload\_schema\_ref: schema:action\_candidate\_created\_payload\_v1

metadata\_schema\_ref: schema:core\_event\_metadata\_v1

required\_fields:

  \- action\_candidate\_id

  \- action\_type\_id

  \- proposed\_by

  \- target\_ref

  \- evidence\_bundle\_ref

  \- confidence\_score

optional\_fields:

  \- recommendation\_reason

  \- risk\_class

  \- priority\_hint

  \- related\_event\_refs

topic\_refs:

  \- topic:action.candidate.created

stream\_refs:

  \- stream:action\_lifecycle

routing\_rule\_ref: routing:action\_candidate\_created\_routing

world\_state\_effect: none

agent\_trigger\_allowed: false

decision\_trigger\_allowed: true

approval\_trigger\_allowed: false

execution\_trigger\_allowed: false

audit\_required: true

idempotency\_required: true

idempotency\_key\_strategy: action\_candidate\_id

ordering\_requirement: per\_entity

replay\_allowed: true

retention\_policy\_ref: retention:action\_lifecycle\_long\_term

producer\_authority\_level: registered\_agent\_or\_operator

consumer\_scope\_refs:

  \- consumer:action\_validator

  \- consumer:decision\_engine

  \- consumer:audit\_service

sensitivity\_level: internal

pii\_classification: indirect

decision\_boundary: may\_trigger\_decision\_rule\_lookup

execution\_boundary: does\_not\_create\_execution\_request

safety\_boundary: action\_candidate\_is\_not\_approved\_action

audit\_event\_refs:

  \- audit:action\_candidate\_event\_recorded

  \- audit:event\_validation\_failed

owner\_module: action\_lifecycle\_module

owner\_team: LEDO Governance

source\_document: action\_event\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_event\_type\_id: null

---

## **14\. Registry Entry Example: ExecutionResultReceived**

event\_type\_id: event:ExecutionResultReceived

canonical\_name: execution\_result\_received

display\_name: Execution Result Received

description: Indicates that an execution result has been returned from an external adapter or external system.

semantic\_iri: ledo:ExecutionResultReceivedEvent

event\_category: FEEDBACK\_EVENT

version: 1.0.0

status: active

allowed\_producer\_refs:

  \- producer:execution\_dispatcher

  \- producer:robot\_fleet\_adapter

  \- producer:scada\_adapter

  \- producer:plc\_adapter

  \- producer:site\_platform\_adapter

allowed\_source\_types:

  \- execution\_dispatcher

  \- external\_adapter

  \- external\_system

payload\_schema\_ref: schema:execution\_result\_received\_payload\_v1

metadata\_schema\_ref: schema:core\_event\_metadata\_v1

required\_fields:

  \- execution\_request\_id

  \- adapter\_id

  \- external\_system\_ref

  \- result\_status

  \- result\_timestamp

optional\_fields:

  \- error\_code

  \- error\_message

  \- external\_reference\_id

  \- feedback\_payload\_ref

  \- retry\_recommended

topic\_refs:

  \- topic:execution.result.received

stream\_refs:

  \- stream:execution\_feedback

  \- stream:audit\_execution\_trace

routing\_rule\_ref: routing:execution\_result\_received\_routing

world\_state\_effect: update

agent\_trigger\_allowed: true

decision\_trigger\_allowed: false

approval\_trigger\_allowed: false

execution\_trigger\_allowed: false

audit\_required: true

idempotency\_required: true

idempotency\_key\_strategy: execution\_request\_id\_adapter\_result\_status

ordering\_requirement: per\_entity

replay\_allowed: true

retention\_policy\_ref: retention:execution\_trace\_long\_term

producer\_authority\_level: registered\_execution\_component

consumer\_scope\_refs:

  \- consumer:execution\_state\_manager

  \- consumer:world\_state\_service

  \- consumer:audit\_service

  \- consumer:supervisor\_ui

sensitivity\_level: restricted

pii\_classification: indirect

decision\_boundary: may\_trigger\_follow\_up\_decision\_but\_not\_direct\_approval

execution\_boundary: result\_event\_is\_not\_new\_execution\_request

safety\_boundary: failed\_execution\_may\_trigger\_safety\_review

audit\_event\_refs:

  \- audit:execution\_result\_recorded

  \- audit:execution\_trace\_updated

owner\_module: execution\_integration\_module

owner\_team: LEDO Execution Integration

source\_document: execution\_event\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_event\_type\_id: null

---

## **15\. Event Lifecycle Alignment**

Events may be connected to the following lifecycle:

Event Produced

    ↓

Event Registry Validation

    ↓

Schema Validation

    ↓

Producer Authorization Check

    ↓

Idempotency Check

    ↓

Routing

    ↓

Consumer Processing

    ↓

World State Update / Agent Trigger / Decision Trigger / Audit Record

    ↓

Feedback / Derived Event / Error Event

The important point is that an Event may trigger a lifecycle, but it must not bypass lifecycle boundaries.

A HazardDetected event may trigger a Safety Agent.

A HazardDetected event may lead to ActionCandidate generation.

However, a HazardDetected event must not directly create ApprovedAction or ExecutionRequest.

---

## **16\. Validation Rules**

An Event Type is valid only when the following conditions are satisfied:

1. `event_type_id` exists in the registry.  
2. Its status is `active`.  
3. Event category is declared.  
4. Allowed producers are declared.  
5. Allowed source types are declared.  
6. Payload schema reference is declared.  
7. Metadata schema reference is declared.  
8. Required fields are declared.  
9. Topic or stream references are declared.  
10. Routing rule is declared.  
11. World State effect is declared.  
12. Idempotency rule is declared.  
13. Ordering requirement is declared.  
14. Retention policy is declared.  
15. Sensitivity level is declared.  
16. Boundaries are declared.  
17. Owner module is declared.  
18. Version is valid.  
19. If deprecated, migration metadata exists.

If any of these conditions are missing, the Event Type must not be used in the operational lifecycle.

---

## **17\. Event Instance Validation**

An Event Instance may be accepted only when the following conditions are satisfied:

Does the Event Type exist in the registry?

Is the Event Type active?

Is the producer allowed?

Is the source type allowed?

Does the payload pass schema validation?

Does the metadata pass the core event schema?

Are all required fields present?

Does idempotency\_key exist?

Is it not a duplicate event?

Does it satisfy sensitivity policy?

Does a routing rule exist?

If these conditions are not satisfied, the event must be handled as reject, quarantine, or dead-letter queue.

---

## **18\. Event Routing Rule**

Event Registry defines where an event should be delivered.

Example routing targets:

world\_state\_service

safety\_risk\_agent

robot\_dispatch\_agent

decision\_engine

approval\_service

execution\_state\_manager

audit\_service

operator\_ui

supervisor\_ui

Routing may be topic-based or stream-based.

Kafka topic

MQTT topic

Redis stream

Internal async queue

Event sourcing log

The important principle is:

Event routing is not execution.

Event routing is not physical control command.

---

## **19\. World State Effect Rule**

The effect of an Event on World State must be explicitly declared.

Recommended values:

none

update

append

invalidate

trigger\_recompute

### **19.1 none**

The Event does not change World State.

Examples:

AuditRecordCreated

ApprovalRequested

---

### **19.2 update**

The Event updates an existing entity state.

Examples:

WorkerLocationUpdated

RobotStatusUpdated

EquipmentStatusChanged

---

### **19.3 append**

The Event appends a new incident or event record.

Examples:

HazardDetected

IncidentReported

ExecutionResultReceived

---

### **19.4 invalidate**

The Event invalidates an existing cache or state snapshot.

Examples:

OntologyVersionChanged

PolicyVersionChanged

AdapterStatusChanged

---

### **19.5 trigger\_recompute**

The Event triggers recomputation of risk, plan, route, or resource allocation.

Examples:

ZoneBlocked

HighRiskHazardDetected

RobotUnavailable

---

## **20\. Idempotency Rule**

Event processing must be safe against duplicate processing.

Idempotency is required because of:

Kafka replay

MQTT duplicate delivery

network retry

external system retry

consumer crash recovery

event sourcing replay

Recommended idempotency key strategies:

event\_id

entity\_id \+ occurred\_at \+ source

execution\_request\_id \+ adapter\_id \+ result\_status

action\_candidate\_id

decision\_case\_id

approval\_request\_id

Important principle:

Even if the same event is received twice,

World State, DecisionCase, ApprovalRequest, or ExecutionResult

must not be duplicated.

---

## **21\. Ordering Rule**

Some events require ordering.

Recommended ordering requirements:

none

per\_entity

per\_site

global

### **21.1 none**

Ordering is not important.

---

### **21.2 per\_entity**

Ordering must be preserved for the same entity.

Examples:

Location events per worker\_id

Status events per robot\_id

Status events per equipment\_id

---

### **21.3 per\_site**

Ordering is important at the site level.

Examples:

Emergency escalation event

Site-wide evacuation event

---

### **21.4 global**

Ordering is important across the entire system.

This should be avoided whenever possible.  
Global ordering can create bottlenecks and single points of failure.

---

## **22\. Replay Rule**

Whether an Event is replayable must be explicitly declared.

Replay is useful for:

World State reconstruction

Audit trace reproduction

Incident investigation

Model evaluation

Decision debugging

Disaster recovery

However, not all events should be replayed.

Events that require caution:

Events that may trigger external execution again

Events that may send duplicate notifications

Events that may create duplicate approval requests

Replay principle:

Replay must be used for state reconstruction.

Replay must not trigger physical execution again.

---

## **23\. Retention Rule**

Retention duration must differ by Event Type.

Examples:

WorkerLocationUpdated: short-term retention

HazardDetected: long-term safety retention

ApprovalGranted: long-term governance retention

ExecutionResultReceived: long-term audit retention

AuditRecordCreated: long-term or immutable retention

Retention must consider legal, safety, audit, cost, and privacy requirements.

---

## **24\. Sensitivity and PII Rule**

Events must have a sensitivity level and PII classification.

Recommended sensitivity levels:

public

internal

confidential

restricted

safety\_critical

Recommended PII classifications:

none

indirect

direct

sensitive

Examples:

WorkerLocationUpdated:

    sensitivity\_level: restricted

    pii\_classification: direct

HazardDetected:

    sensitivity\_level: safety\_critical

    pii\_classification: indirect

ExecutionResultReceived:

    sensitivity\_level: restricted

    pii\_classification: indirect

Events containing PII require masking, access control, retention limits, and audit access rules.

---

## **25\. Relationship to Agent Vocabulary Registry**

`agent_vocabulary_registry` defines which events an agent may consume as input.

`event_registry` defines what the event type means and what schema it has.

event\_registry:

    What payload and meaning does WorkerLocationUpdated have?

agent\_vocabulary\_registry:

    Is SAFETY\_RISK\_AGENT allowed to consume WorkerLocationUpdated?

Agents must not consume unauthorized Event Types.

---

## **26\. Relationship to Action Registry**

Some events may trigger ActionCandidate generation.

However, the event does not directly create an Action Type.

HazardDetected

    ↓

Safety Agent analysis

    ↓

ActionCandidateCreated

    ↓

action\_registry validation

Event Registry may indicate which events can lead to ActionCandidate generation.

The validity of the Action Type is determined by `action_registry`.

---

## **27\. Relationship to Decision Registry**

Some events may trigger DecisionCase creation.

Example:

ActionCandidateCreated

    ↓

Decision Rule Lookup

    ↓

DecisionCaseCreated

Event Registry may declare `decision_trigger_allowed`, but `decision_registry` determines which Decision Rule applies.

---

## **28\. Relationship to Approval Registry**

Approval-related events record the approval lifecycle.

Examples:

ApprovalRequested

ApprovalGranted

ApprovalRejected

ApprovalExpired

ApprovalRevoked

Event Registry defines approval event schema and routing.

Approval rules and approval authority are managed by `approval_registry`.

---

## **29\. Relationship to Adapter Registry**

Execution or feedback events are connected to adapters.

Examples:

ExecutionDispatched

ExecutionAcceptedByAdapter

ExecutionRejectedByAdapter

ExecutionResultReceived

Event Registry defines the structure and routing of adapter events.

Actual adapter instance selection is handled by `adapter_registry`.

---

## **30\. Relationship to Audit Registry**

Audit Events may be connected to a separate audit event registry.

event\_registry:

    Defines which events require audit

audit\_event\_registry:

    Defines which audit record schema and retention rule should be used

Not every event is an audit event.

However, safety-critical, approval, decision, and execution-related events should be audited.

---

## **31\. Relationship to Ontology**

Every important Event Type should have a semantic IRI.

Example:

event\_type\_id: event:HazardDetected

semantic\_iri: ledo:HazardDetectedEvent

In the ontology, it may be defined as follows:

ledo:HazardDetectedEvent

    rdf:type ledo:EventType ;

    rdfs:subClassOf ledo:SafetyEvent ;

    ledo:observes ledo:Hazard ;

    ledo:mayTrigger ledo:SafetyRiskAnalysis ;

    ledo:requiresEvidence ledo:HazardDetectionSnapshot .

Ontology provides the semantic foundation of Events.

Event Registry manages this foundation in the operational system through version, schema, routing, producer, retention, replay, and audit rules.

---

## **32\. Versioning and Migration**

Event Types must be versioned.

A version change is required when any of the following changes:

1. Payload schema changes  
2. Required fields change  
3. Metadata schema changes  
4. Allowed producers change  
5. Routing rule changes  
6. World State effect changes  
7. Trigger permission changes  
8. Idempotency strategy changes  
9. Ordering requirement changes  
10. Retention policy changes  
11. Sensitivity level changes  
12. Boundary changes

Status values:

draft

active

deprecated

migration\_required

retired

blocked

A deprecated Event Type must declare:

deprecated\_since: datetime

replacement\_event\_type\_id: string | null

migration\_notes: string

A blocked Event Type must not be accepted as a new event instance.

---

## **33\. Implementation Use**

`event_registry` is used to generate or validate:

1. `EventType` enum  
2. `EventCategory` enum  
3. CoreEvent metadata schema  
4. Event payload DTO constraints  
5. Event producer validation  
6. Event source validation  
7. Event schema validation  
8. Event routing rule lookup  
9. World State update rule lookup  
10. Agent trigger rule lookup  
11. Decision trigger rule lookup  
12. Audit requirement lookup  
13. Idempotency validation  
14. Ordering validation  
15. Replay rule validation  
16. Retention rule validation  
17. Sensitivity / PII rule validation  
18. Test case generation  
19. Migration rules

Implementation must not create or process unregistered Event Types.

---

## **34\. Recommended Code Structure**

registries/

    event\_registry/

        event\_registry.py

        event\_registry\_entry.py

        event\_category.py

        event\_status.py

        event\_effect.py

        event\_sensitivity.py

        event\_validation.py

        event\_errors.py

        event\_loader.py

        event\_migration.py

    schema\_registry/

    agent\_vocabulary\_registry/

    action\_registry/

    decision\_registry/

    approval\_registry/

    adapter\_registry/

    audit\_event\_registry/

---

## **35\. Minimal Pydantic Model**

from enum import Enum

from pydantic import BaseModel, Field

from typing import Optional

from datetime import datetime

class EventStatus(str, Enum):

    DRAFT \= "draft"

    ACTIVE \= "active"

    DEPRECATED \= "deprecated"

    MIGRATION\_REQUIRED \= "migration\_required"

    RETIRED \= "retired"

    BLOCKED \= "blocked"

class EventCategory(str, Enum):

    SENSOR\_EVENT \= "sensor\_event"

    WORLD\_STATE\_EVENT \= "world\_state\_event"

    AGENT\_EVENT \= "agent\_event"

    ACTION\_EVENT \= "action\_event"

    DECISION\_EVENT \= "decision\_event"

    APPROVAL\_EVENT \= "approval\_event"

    SAFETY\_GATE\_EVENT \= "safety\_gate\_event"

    EXECUTION\_EVENT \= "execution\_event"

    EXTERNAL\_SYSTEM\_EVENT \= "external\_system\_event"

    FEEDBACK\_EVENT \= "feedback\_event"

    AUDIT\_EVENT \= "audit\_event"

    SYSTEM\_EVENT \= "system\_event"

    ERROR\_EVENT \= "error\_event"

    SECURITY\_EVENT \= "security\_event"

class WorldStateEffect(str, Enum):

    NONE \= "none"

    UPDATE \= "update"

    APPEND \= "append"

    INVALIDATE \= "invalidate"

    TRIGGER\_RECOMPUTE \= "trigger\_recompute"

class OrderingRequirement(str, Enum):

    NONE \= "none"

    PER\_ENTITY \= "per\_entity"

    PER\_SITE \= "per\_site"

    GLOBAL \= "global"

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

class EventRegistryEntry(BaseModel):

    event\_type\_id: str

    canonical\_name: str

    display\_name: str

    description: str

    semantic\_iri: str

    event\_category: EventCategory

    version: str

    status: EventStatus \= EventStatus.DRAFT

    allowed\_producer\_refs: list\[str\] \= Field(default\_factory=list)

    allowed\_source\_types: list\[str\] \= Field(default\_factory=list)

    payload\_schema\_ref: str

    metadata\_schema\_ref: str

    required\_fields: list\[str\] \= Field(default\_factory=list)

    optional\_fields: list\[str\] \= Field(default\_factory=list)

    topic\_refs: list\[str\] \= Field(default\_factory=list)

    stream\_refs: list\[str\] \= Field(default\_factory=list)

    routing\_rule\_ref: str

    world\_state\_effect: WorldStateEffect \= WorldStateEffect.NONE

    agent\_trigger\_allowed: bool \= False

    decision\_trigger\_allowed: bool \= False

    approval\_trigger\_allowed: bool \= False

    execution\_trigger\_allowed: bool \= False

    audit\_required: bool \= False

    idempotency\_required: bool \= True

    idempotency\_key\_strategy: str

    ordering\_requirement: OrderingRequirement \= OrderingRequirement.NONE

    replay\_allowed: bool \= False

    retention\_policy\_ref: str

    producer\_authority\_level: str

    consumer\_scope\_refs: list\[str\] \= Field(default\_factory=list)

    sensitivity\_level: SensitivityLevel \= SensitivityLevel.INTERNAL

    pii\_classification: PIIClassification \= PIIClassification.NONE

    decision\_boundary: str

    execution\_boundary: str

    safety\_boundary: str

    audit\_event\_refs: list\[str\] \= Field(default\_factory=list)

    owner\_module: str

    owner\_team: str

    source\_document: str

    created\_at: datetime

    updated\_at: datetime

    deprecated\_since: Optional\[datetime\] \= None

    replacement\_event\_type\_id: Optional\[str\] \= None

---

## **36\. Core Validation Function**

def validate\_event\_instance(

    entry: EventRegistryEntry,

    event\_type\_id: str,

    producer\_ref: str,

    source\_type: str,

    payload: dict,

) \-\> None:

    if entry.status \!= EventStatus.ACTIVE:

        raise InvalidEventTypeError(

            f"Event Type is not active: {entry.event\_type\_id}"

        )

    if event\_type\_id \!= entry.event\_type\_id:

        raise EventTypeMismatchError(

            f"Event Type '{event\_type\_id}' does not match registry entry "

            f"'{entry.event\_type\_id}'"

        )

    if producer\_ref not in entry.allowed\_producer\_refs:

        raise EventProducerNotAllowedError(

            f"Producer '{producer\_ref}' is not allowed for Event Type "

            f"'{entry.event\_type\_id}'"

        )

    if source\_type not in entry.allowed\_source\_types:

        raise EventSourceTypeNotAllowedError(

            f"Source type '{source\_type}' is not allowed for Event Type "

            f"'{entry.event\_type\_id}'"

        )

    for field in entry.required\_fields:

        if field not in payload:

            raise EventPayloadValidationError(

                f"Required field '{field}' is missing from payload"

            )

    if not entry.payload\_schema\_ref:

        raise InvalidEventRegistryEntryError(

            "payload\_schema\_ref must be declared"

        )

    if not entry.metadata\_schema\_ref:

        raise InvalidEventRegistryEntryError(

            "metadata\_schema\_ref must be declared"

        )

    if not entry.routing\_rule\_ref:

        raise InvalidEventRegistryEntryError(

            "routing\_rule\_ref must be declared"

        )

    if entry.idempotency\_required and not entry.idempotency\_key\_strategy:

        raise InvalidEventRegistryEntryError(

            "idempotency\_key\_strategy must be declared when idempotency is required"

        )

    if not entry.retention\_policy\_ref:

        raise InvalidEventRegistryEntryError(

            "retention\_policy\_ref must be declared"

        )

---

## **37\. Test Scenarios**

Required tests:

1\. Reject unregistered Event Type.

2\. Reject inactive Event Type.

3\. Reject deprecated Event Type.

4\. Reject blocked Event Type.

5\. Reject event produced by unauthorized producer.

6\. Reject unauthorized source type.

7\. Reject payload schema mismatch.

8\. Reject missing required field.

9\. Reject missing metadata schema.

10\. Reject missing routing rule.

11\. Reject missing idempotency key.

12\. Verify duplicate event processing prevention.

13\. Verify ordering requirement.

14\. Verify that replay does not trigger physical execution again.

15\. Verify sensitivity / PII rules.

16\. Verify that audit\_required events create audit logs.

17\. Verify that world\_state\_effect update events correctly update World State.

18\. Verify that decision\_trigger\_allowed events do not bypass Decision Registry.

19\. Verify that events with execution\_trigger\_allowed \= false cannot create ExecutionRequest.

20\. Verify Event migration rules.

---

## **38\. Final Rule**

No registered Event Type,

no valid Event Instance.

No valid Event Instance,

no World State Update.

Event is not ActionCandidate.

Event is not DecisionCase.

Event is not ApprovalDecision.

Event is not ExecutionRequest.

Event is not PhysicalCommand.

Event is not External System control.

Event may trigger a lifecycle,

but it must not bypass lifecycle boundaries.

`event_registry` is the core deterministic registry that governs event flow across the entire LEDO system.

This module defines the meaning, schema, producer, routing, idempotency, replay, retention, sensitivity, and audit rules of every Event Type, and ensures that events do not cross the boundaries of Action, Decision, Approval, or Execution.

The core definition is:

Event Registry

\= not a list of event names,

but an operational contract registry that controls

the meaning, structure, source, routing, world state effect,

idempotency, replay, retention, sensitivity, and audit rules

of every event that occurs in the system.

# **event\_registry 설계 보고서**

## **1\. 개요**

`event_registry`는 LEDO Ontology-Centric Cyber-Physical System에서 사용되는 모든 Event Type, Event Category, Event Schema, Event Source, Event Payload Contract, Event Routing Rule, Event Lifecycle, Event Retention Rule, Event Audit Rule을 정의하고 통제하는 핵심 레지스트리이다.

이 모듈의 목적은 시스템 내부에서 임의의 event가 무분별하게 생성되는 것을 방지하고, 모든 event가 등록된 Event Type과 schema, source, routing, lifecycle, audit rule을 따르도록 보장하는 것이다.

`event_registry`는 단순한 이벤트 이름 목록이 아니다.

이 레지스트리는 다음을 정의하는 **이벤트 의미·구조·흐름·추적성 운영 계약 레지스트리**이다.

어떤 Event Type이 존재할 수 있는가?  
그 Event는 어떤 의미를 가지는가?  
어떤 source가 그 Event를 생성할 수 있는가?  
Event payload는 어떤 schema를 따라야 하는가?  
Event는 어떤 topic 또는 stream으로 전달되는가?  
Event가 World State를 변경할 수 있는가?  
Event가 Decision, Approval, Execution, Audit 흐름을 트리거할 수 있는가?  
Event는 얼마나 보관되어야 하는가?  
Event는 replay 가능한가?  
Event는 idempotent하게 처리되어야 하는가?

즉, `event_registry`는 LEDO 시스템 전체에서 발생하는 모든 사건을 통제된 의미와 구조로 관리하는 핵심 레지스트리이다.

---

## **2\. 핵심 원칙**

Event는 사실 또는 상태 변화의 기록이다.

Event는 명령이 아니다.

Event는 승인도 아니다.

Event는 물리 실행도 아니다.

Event는 ActionCandidate와 다르다.

Event는 ExecutionRequest와 다르다.

Event의 기본 의미는 다음과 같다.

무언가가 발생했다.  
무언가의 상태가 변경되었다.  
무언가가 관측되었다.  
무언가가 요청되었다.  
무언가의 결과가 반환되었다.  
무언가가 감사 기록으로 남아야 한다.

Event는 시스템의 혈류와 같다.  
하지만 event가 곧 실행 명령이 되어서는 안 된다.

핵심 원칙은 다음과 같다.

Event informs.  
Action proposes.  
Decision evaluates.  
Approval authorizes.  
Safety Gate validates.  
ExecutionRequest prepares execution.  
External System performs physical execution.

---

## **3\. LEDO 아키텍처 내 위치**

`event_registry`는 특정 단일 layer에만 속하지 않는다.  
LEDO 전체 시스템을 가로지르는 cross-cutting registry이다.

Sensors / External Systems / Agents / UI / Workflow  
        ↓  
Event 생성  
        ↓  
event\_registry validation  
        ↓  
Kafka / MQTT / Event Bus / Stream  
        ↓  
World State Update / Agent Trigger / Decision Trigger / Audit Log  
        ↓  
ActionCandidate / DecisionCase / Approval / Execution Feedback

`event_registry`는 다음 layer들과 모두 연결된다.

Real-Time World State Layer  
Distributed Domain Agent Layer  
Decision Router / Escalation Layer  
Approval Layer  
Safety Gate Layer  
Unified Cyber-Physical Core Layer  
Execution Integration Layer  
Observability / Audit / Trace Layer

---

## **4\. 목적**

`event_registry`의 목적은 다음과 같다.

1. 등록되지 않은 Event Type 생성 방지  
2. Event Type별 의미와 schema 정의  
3. Event source 및 producer 권한 정의  
4. Event payload validation rule 정의  
5. Event topic / stream routing rule 정의  
6. Event가 world state를 변경할 수 있는지 정의  
7. Event가 agent를 trigger할 수 있는지 정의  
8. Event가 decision, approval, execution workflow를 trigger할 수 있는지 정의  
9. Event idempotency requirement 정의  
10. Event replay 가능 여부 정의  
11. Event ordering requirement 정의  
12. Event retention 및 archival rule 정의  
13. Event audit 및 trace rule 정의  
14. Event versioning 및 migration 관리  
15. Event와 ontology class / property / relation의 의미론적 연결 관리

---

## **5\. 핵심 구분**

### **5.1 Event Type**

`Event Type`은 시스템에서 허용되는 사건 유형이다.

예시:

WorkerLocationUpdated  
HazardDetected  
ZoneStatusChanged  
RobotStatusUpdated  
EquipmentStatusChanged  
ActionCandidateCreated  
DecisionCaseCreated  
ApprovalRequested  
ApprovalGranted  
SafetyGatePassed  
ExecutionRequestCreated  
ExecutionResultReceived  
FeedbackEventReceived  
AuditRecordCreated

Event Type은 “무슨 일이 발생했는가”를 정의한다.

---

### **5.2 Event Instance**

`Event Instance`는 실제 런타임에서 발생한 개별 event이다.

예시:

event\_id: evt\_01HT...  
event\_type: WorkerLocationUpdated  
occurred\_at: 2026-06-26T09:00:00Z  
source: worker\_tracking\_system  
payload: {...}

Event Type은 설계 기준이고, Event Instance는 실제 발생 기록이다.

---

### **5.3 Event Category**

Event Category는 Event Type을 기능적으로 분류한다.

예시:

SENSOR\_EVENT  
WORLD\_STATE\_EVENT  
AGENT\_EVENT  
ACTION\_EVENT  
DECISION\_EVENT  
APPROVAL\_EVENT  
SAFETY\_GATE\_EVENT  
EXECUTION\_EVENT  
FEEDBACK\_EVENT  
AUDIT\_EVENT  
SYSTEM\_EVENT  
ERROR\_EVENT

Category는 routing, retention, audit, priority, replay rule을 결정하는 기준이 된다.

---

### **5.4 Event Source**

Event Source는 event를 생성한 주체이다.

예시:

sensor\_gateway  
worker\_tracking\_system  
robot\_fleet\_manager  
scada\_system  
plc\_gateway  
domain\_agent  
decision\_engine  
approval\_service  
safety\_gate  
execution\_dispatcher  
external\_adapter  
operator\_ui  
audit\_service

Event Source는 반드시 등록되고 검증되어야 한다.

---

### **5.5 Event Payload**

Event Payload는 event가 담고 있는 데이터이다.

Payload는 반드시 schema를 따라야 한다.

예시:

{  
  "worker\_id": "worker\_123",  
  "zone\_id": "zone\_03",  
  "position": {  
    "x": 12.4,  
    "y": 7.8,  
    "z": 0.0  
  },  
  "confidence": 0.94  
}

Payload는 event type마다 다르지만, 공통 metadata는 반드시 유지되어야 한다.

---

## **6\. Scope**

`event_registry`는 다음 항목을 통제한다.

event\_type\_id: string  
canonical\_name: string  
display\_name: string  
description: string  
semantic\_iri: string

event\_category: string  
version: string  
status: draft | active | deprecated | migration\_required | retired | blocked

allowed\_producer\_refs:  
  \- string

allowed\_source\_types:  
  \- string

payload\_schema\_ref: string  
metadata\_schema\_ref: string

required\_fields:  
  \- string

optional\_fields:  
  \- string

topic\_refs:  
  \- string

stream\_refs:  
  \- string

routing\_rule\_ref: string

world\_state\_effect: none | update | append | invalidate | trigger\_recompute  
agent\_trigger\_allowed: boolean  
decision\_trigger\_allowed: boolean  
approval\_trigger\_allowed: boolean  
execution\_trigger\_allowed: boolean  
audit\_required: boolean

idempotency\_required: boolean  
idempotency\_key\_strategy: string  
ordering\_requirement: none | per\_entity | per\_site | global  
replay\_allowed: boolean  
retention\_policy\_ref: string

producer\_authority\_level: string  
consumer\_scope\_refs:  
  \- string

sensitivity\_level: public | internal | confidential | restricted | safety\_critical  
pii\_classification: none | indirect | direct | sensitive

decision\_boundary: string  
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
replacement\_event\_type\_id: string | null

---

## **7\. Non-Scope**

`event_registry`는 다음을 정의하지 않는다.

1. 실제 Kafka broker 설정 전체  
2. MQTT broker 내부 구성 전체  
3. raw sensor driver logic  
4. PLC / SCADA command logic  
5. robot motion planning  
6. policy pass/fail logic 전체  
7. approval authority 자체  
8. Safety Gate 최종 판정 로직  
9. adapter instance selection  
10. low-level database storage implementation  
11. 모든 domain threshold 값  
12. 모든 event processing algorithm  
13. 전체 stream processing topology

이 책임들은 다음 모듈에 속한다.

message\_broker  
stream\_processor  
sensor\_gateway  
world\_state\_store  
policy\_registry  
approval\_registry  
decision\_registry  
safety\_gate  
adapter\_registry  
external\_system\_registry  
domain\_module  
Kafka / MQTT / Redis / TimescaleDB

---

## **8\. Event Category 모델**

권장 Event Category는 다음과 같다.

SENSOR\_EVENT  
WORLD\_STATE\_EVENT  
AGENT\_EVENT  
ACTION\_EVENT  
DECISION\_EVENT  
APPROVAL\_EVENT  
SAFETY\_GATE\_EVENT  
EXECUTION\_EVENT  
EXTERNAL\_SYSTEM\_EVENT  
FEEDBACK\_EVENT  
AUDIT\_EVENT  
SYSTEM\_EVENT  
ERROR\_EVENT  
SECURITY\_EVENT

### **8.1 SENSOR\_EVENT**

센서, IoT, 위치 추적, 카메라, 환경 측정 장치 등에서 발생한 event이다.

예시:

WorkerLocationUpdated  
TemperatureSensorUpdated  
GasLevelDetected  
VibrationThresholdExceeded

---

### **8.2 WORLD\_STATE\_EVENT**

World State의 상태 변경을 나타낸다.

예시:

ZoneStatusChanged  
EquipmentAvailabilityChanged  
RobotMissionStateChanged  
WorkerEnteredZone  
WorkerExitedZone

---

### **8.3 AGENT\_EVENT**

Agent의 관찰, 분석, 추천, 후보 생성과 관련된 event이다.

예시:

AgentObservationCreated  
RiskSignalCreated  
ActionCandidateCreated  
EvidenceBundleCreated

---

### **8.4 ACTION\_EVENT**

ActionCandidate 또는 Action Type lifecycle과 관련된 event이다.

예시:

ActionCandidateCreated  
ActionCandidateValidated  
ActionCandidateRejected

---

### **8.5 DECISION\_EVENT**

DecisionCase와 판단 흐름 관련 event이다.

예시:

DecisionCaseCreated  
DecisionEvidenceEvaluated  
DecisionPolicyEvaluated  
DecisionOutcomeSelected  
DecisionEscalated

---

### **8.6 APPROVAL\_EVENT**

Approval lifecycle 관련 event이다.

예시:

ApprovalRequested  
ApprovalGranted  
ApprovalRejected  
ApprovalExpired  
ApprovalRevoked

---

### **8.7 SAFETY\_GATE\_EVENT**

Safety Gate 검증 결과와 관련된 event이다.

예시:

SafetyGateValidationStarted  
SafetyGatePassed  
SafetyGateFailed  
SafetyGateBlocked

---

### **8.8 EXECUTION\_EVENT**

ExecutionRequest 및 ExecutionDispatcher 흐름과 관련된 event이다.

예시:

ExecutionRequestCreated  
ExecutionDispatched  
ExecutionAcceptedByAdapter  
ExecutionRejectedByAdapter  
ExecutionTimedOut

---

### **8.9 FEEDBACK\_EVENT**

외부 시스템으로부터 반환된 feedback 관련 event이다.

예시:

ExternalExecutionStarted  
ExternalExecutionCompleted  
ExternalExecutionFailed  
RobotMissionFeedbackReceived  
SCADAStatusFeedbackReceived

---

### **8.10 AUDIT\_EVENT**

감사와 추적성을 위해 생성되는 event이다.

예시:

AuditRecordCreated  
PolicyDecisionAudited  
ApprovalDecisionAudited  
ExecutionTraceRecorded

---

## **9\. Registry Entry Schema**

각 Event Registry entry는 다음 구조를 따른다.

event\_type\_id: string  
canonical\_name: string  
display\_name: string  
description: string  
semantic\_iri: string

event\_category: string

version: string  
status: draft | active | deprecated | migration\_required | retired | blocked

allowed\_producer\_refs:  
  \- string

allowed\_source\_types:  
  \- string

payload\_schema\_ref: string  
metadata\_schema\_ref: string

required\_fields:  
  \- string

optional\_fields:  
  \- string

topic\_refs:  
  \- string

stream\_refs:  
  \- string

routing\_rule\_ref: string

world\_state\_effect: none | update | append | invalidate | trigger\_recompute  
agent\_trigger\_allowed: boolean  
decision\_trigger\_allowed: boolean  
approval\_trigger\_allowed: boolean  
execution\_trigger\_allowed: boolean  
audit\_required: boolean

idempotency\_required: boolean  
idempotency\_key\_strategy: string  
ordering\_requirement: none | per\_entity | per\_site | global  
replay\_allowed: boolean  
retention\_policy\_ref: string

producer\_authority\_level: string  
consumer\_scope\_refs:  
  \- string

sensitivity\_level: public | internal | confidential | restricted | safety\_critical  
pii\_classification: none | indirect | direct | sensitive

decision\_boundary: string  
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
replacement\_event\_type\_id: string | null

---

## **10\. 공통 Event Metadata Schema**

모든 event instance는 최소한 다음 metadata를 가져야 한다.

event\_id: string  
event\_type\_id: string  
event\_version: string  
occurred\_at: datetime  
observed\_at: datetime | null  
received\_at: datetime  
producer\_id: string  
source\_system\_ref: string  
site\_id: string | null  
zone\_id: string | null  
entity\_refs:  
  \- string  
correlation\_id: string | null  
causation\_id: string | null  
trace\_id: string | null  
idempotency\_key: string  
payload\_schema\_version: string  
sensitivity\_level: string

### **10.1 event\_id**

각 event instance의 고유 ID이다.

---

### **10.2 occurred\_at**

실제 사건이 발생한 시간이다.

---

### **10.3 observed\_at**

센서나 외부 시스템이 사건을 관측한 시간이다.

---

### **10.4 received\_at**

LEDO system이 event를 수신한 시간이다.

---

### **10.5 correlation\_id**

같은 workflow 또는 lifecycle에 속한 event들을 연결하는 ID이다.

---

### **10.6 causation\_id**

이 event를 발생시킨 원인 event의 ID이다.

---

### **10.7 idempotency\_key**

중복 event 처리 방지를 위한 key이다.

---

## **11\. Registry Entry 예시: WorkerLocationUpdated**

event\_type\_id: event:WorkerLocationUpdated  
canonical\_name: worker\_location\_updated  
display\_name: Worker Location Updated  
description: 작업자의 위치 정보가 갱신되었음을 나타내는 event이다.  
semantic\_iri: ledo:WorkerLocationUpdatedEvent

event\_category: SENSOR\_EVENT

version: 1.0.0  
status: active

allowed\_producer\_refs:  
  \- producer:worker\_tracking\_gateway  
  \- producer:uwb\_location\_system  
  \- producer:vision\_location\_system

allowed\_source\_types:  
  \- sensor\_gateway  
  \- location\_tracking\_system

payload\_schema\_ref: schema:worker\_location\_updated\_payload\_v1  
metadata\_schema\_ref: schema:core\_event\_metadata\_v1

required\_fields:  
  \- worker\_id  
  \- position  
  \- confidence  
  \- coordinate\_frame

optional\_fields:  
  \- velocity  
  \- floor\_id  
  \- device\_id

topic\_refs:  
  \- topic:site.worker.location.updated

stream\_refs:  
  \- stream:world\_state\_worker\_location

routing\_rule\_ref: routing:worker\_location\_update\_routing

world\_state\_effect: update  
agent\_trigger\_allowed: true  
decision\_trigger\_allowed: false  
approval\_trigger\_allowed: false  
execution\_trigger\_allowed: false  
audit\_required: false

idempotency\_required: true  
idempotency\_key\_strategy: worker\_id\_occurred\_at\_source  
ordering\_requirement: per\_entity  
replay\_allowed: true  
retention\_policy\_ref: retention:worker\_location\_short\_term

producer\_authority\_level: registered\_sensor\_gateway  
consumer\_scope\_refs:  
  \- consumer:world\_state\_service  
  \- consumer:safety\_risk\_agent  
  \- consumer:worker\_proximity\_agent

sensitivity\_level: restricted  
pii\_classification: direct

decision\_boundary: does\_not\_create\_decision\_case\_directly  
execution\_boundary: does\_not\_create\_execution\_request  
safety\_boundary: may\_trigger\_safety\_analysis\_but\_not\_safety\_gate\_pass

audit\_event\_refs:  
  \- audit:event\_received  
  \- audit:event\_validation\_failed

owner\_module: worker\_domain\_module  
owner\_team: LEDO Worker Safety  
source\_document: worker\_event\_contract\_v1  
created\_at: 2026-06-26T00:00:00Z  
updated\_at: 2026-06-26T00:00:00Z  
deprecated\_since: null  
replacement\_event\_type\_id: null

---

## **12\. Registry Entry 예시: HazardDetected**

event\_type\_id: event:HazardDetected  
canonical\_name: hazard\_detected  
display\_name: Hazard Detected  
description: 현장에서 위험 요인이 감지되었음을 나타내는 event이다.  
semantic\_iri: ledo:HazardDetectedEvent

event\_category: SENSOR\_EVENT

version: 1.0.0  
status: active

allowed\_producer\_refs:  
  \- producer:hazard\_detection\_model  
  \- producer:gas\_sensor\_gateway  
  \- producer:vision\_safety\_model  
  \- producer:manual\_operator\_report

allowed\_source\_types:  
  \- sensor\_gateway  
  \- ai\_model  
  \- operator\_ui

payload\_schema\_ref: schema:hazard\_detected\_payload\_v1  
metadata\_schema\_ref: schema:core\_event\_metadata\_v1

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

topic\_refs:  
  \- topic:site.safety.hazard.detected

stream\_refs:  
  \- stream:safety\_events  
  \- stream:world\_state\_hazard

routing\_rule\_ref: routing:hazard\_detected\_routing

world\_state\_effect: append  
agent\_trigger\_allowed: true  
decision\_trigger\_allowed: true  
approval\_trigger\_allowed: false  
execution\_trigger\_allowed: false  
audit\_required: true

idempotency\_required: true  
idempotency\_key\_strategy: hazard\_type\_location\_time\_window\_source  
ordering\_requirement: per\_site  
replay\_allowed: true  
retention\_policy\_ref: retention:safety\_event\_long\_term

producer\_authority\_level: registered\_safety\_source  
consumer\_scope\_refs:  
  \- consumer:world\_state\_service  
  \- consumer:safety\_risk\_agent  
  \- consumer:decision\_engine  
  \- consumer:audit\_service

sensitivity\_level: safety\_critical  
pii\_classification: indirect

decision\_boundary: may\_trigger\_decision\_case\_creation  
execution\_boundary: does\_not\_create\_execution\_request  
safety\_boundary: hazard\_event\_must\_not\_directly\_trigger\_physical\_command

audit\_event\_refs:  
  \- audit:event\_received  
  \- audit:event\_validated  
  \- audit:safety\_event\_recorded

owner\_module: safety\_domain\_module  
owner\_team: LEDO Safety Governance  
source\_document: safety\_event\_contract\_v1  
created\_at: 2026-06-26T00:00:00Z  
updated\_at: 2026-06-26T00:00:00Z  
deprecated\_since: null  
replacement\_event\_type\_id: null

---

## **13\. Registry Entry 예시: ActionCandidateCreated**

event\_type\_id: event:ActionCandidateCreated  
canonical\_name: action\_candidate\_created  
display\_name: Action Candidate Created  
description: Agent 또는 workflow가 ActionCandidate를 생성했음을 나타내는 event이다.  
semantic\_iri: ledo:ActionCandidateCreatedEvent

event\_category: ACTION\_EVENT

version: 1.0.0  
status: active

allowed\_producer\_refs:  
  \- producer:safety\_risk\_agent  
  \- producer:robot\_dispatch\_agent  
  \- producer:workflow\_engine  
  \- producer:operator\_ui

allowed\_source\_types:  
  \- domain\_agent  
  \- workflow\_engine  
  \- operator\_ui

payload\_schema\_ref: schema:action\_candidate\_created\_payload\_v1  
metadata\_schema\_ref: schema:core\_event\_metadata\_v1

required\_fields:  
  \- action\_candidate\_id  
  \- action\_type\_id  
  \- proposed\_by  
  \- target\_ref  
  \- evidence\_bundle\_ref  
  \- confidence\_score

optional\_fields:  
  \- recommendation\_reason  
  \- risk\_class  
  \- priority\_hint  
  \- related\_event\_refs

topic\_refs:  
  \- topic:action.candidate.created

stream\_refs:  
  \- stream:action\_lifecycle

routing\_rule\_ref: routing:action\_candidate\_created\_routing

world\_state\_effect: none  
agent\_trigger\_allowed: false  
decision\_trigger\_allowed: true  
approval\_trigger\_allowed: false  
execution\_trigger\_allowed: false  
audit\_required: true

idempotency\_required: true  
idempotency\_key\_strategy: action\_candidate\_id  
ordering\_requirement: per\_entity  
replay\_allowed: true  
retention\_policy\_ref: retention:action\_lifecycle\_long\_term

producer\_authority\_level: registered\_agent\_or\_operator  
consumer\_scope\_refs:  
  \- consumer:action\_validator  
  \- consumer:decision\_engine  
  \- consumer:audit\_service

sensitivity\_level: internal  
pii\_classification: indirect

decision\_boundary: may\_trigger\_decision\_rule\_lookup  
execution\_boundary: does\_not\_create\_execution\_request  
safety\_boundary: action\_candidate\_is\_not\_approved\_action

audit\_event\_refs:  
  \- audit:action\_candidate\_event\_recorded  
  \- audit:event\_validation\_failed

owner\_module: action\_lifecycle\_module  
owner\_team: LEDO Governance  
source\_document: action\_event\_contract\_v1  
created\_at: 2026-06-26T00:00:00Z  
updated\_at: 2026-06-26T00:00:00Z  
deprecated\_since: null  
replacement\_event\_type\_id: null

---

## **14\. Registry Entry 예시: ExecutionResultReceived**

event\_type\_id: event:ExecutionResultReceived  
canonical\_name: execution\_result\_received  
display\_name: Execution Result Received  
description: External adapter 또는 external system으로부터 실행 결과가 반환되었음을 나타내는 event이다.  
semantic\_iri: ledo:ExecutionResultReceivedEvent

event\_category: FEEDBACK\_EVENT

version: 1.0.0  
status: active

allowed\_producer\_refs:  
  \- producer:execution\_dispatcher  
  \- producer:robot\_fleet\_adapter  
  \- producer:scada\_adapter  
  \- producer:plc\_adapter  
  \- producer:site\_platform\_adapter

allowed\_source\_types:  
  \- execution\_dispatcher  
  \- external\_adapter  
  \- external\_system

payload\_schema\_ref: schema:execution\_result\_received\_payload\_v1  
metadata\_schema\_ref: schema:core\_event\_metadata\_v1

required\_fields:  
  \- execution\_request\_id  
  \- adapter\_id  
  \- external\_system\_ref  
  \- result\_status  
  \- result\_timestamp

optional\_fields:  
  \- error\_code  
  \- error\_message  
  \- external\_reference\_id  
  \- feedback\_payload\_ref  
  \- retry\_recommended

topic\_refs:  
  \- topic:execution.result.received

stream\_refs:  
  \- stream:execution\_feedback  
  \- stream:audit\_execution\_trace

routing\_rule\_ref: routing:execution\_result\_received\_routing

world\_state\_effect: update  
agent\_trigger\_allowed: true  
decision\_trigger\_allowed: false  
approval\_trigger\_allowed: false  
execution\_trigger\_allowed: false  
audit\_required: true

idempotency\_required: true  
idempotency\_key\_strategy: execution\_request\_id\_adapter\_result\_status  
ordering\_requirement: per\_entity  
replay\_allowed: true  
retention\_policy\_ref: retention:execution\_trace\_long\_term

producer\_authority\_level: registered\_execution\_component  
consumer\_scope\_refs:  
  \- consumer:execution\_state\_manager  
  \- consumer:world\_state\_service  
  \- consumer:audit\_service  
  \- consumer:supervisor\_ui

sensitivity\_level: restricted  
pii\_classification: indirect

decision\_boundary: may\_trigger\_follow\_up\_decision\_but\_not\_direct\_approval  
execution\_boundary: result\_event\_is\_not\_new\_execution\_request  
safety\_boundary: failed\_execution\_may\_trigger\_safety\_review

audit\_event\_refs:  
  \- audit:execution\_result\_recorded  
  \- audit:execution\_trace\_updated

owner\_module: execution\_integration\_module  
owner\_team: LEDO Execution Integration  
source\_document: execution\_event\_contract\_v1  
created\_at: 2026-06-26T00:00:00Z  
updated\_at: 2026-06-26T00:00:00Z  
deprecated\_since: null  
replacement\_event\_type\_id: null

---

## **15\. Event Lifecycle Alignment**

Event는 다음 lifecycle과 연결될 수 있다.

Event Produced  
    ↓  
Event Registry Validation  
    ↓  
Schema Validation  
    ↓  
Producer Authorization Check  
    ↓  
Idempotency Check  
    ↓  
Routing  
    ↓  
Consumer Processing  
    ↓  
World State Update / Agent Trigger / Decision Trigger / Audit Record  
    ↓  
Feedback / Derived Event / Error Event

중요한 점은 event가 lifecycle을 trigger할 수는 있지만, lifecycle 단계를 우회할 수는 없다는 것이다.

HazardDetected event는 Safety Agent를 trigger할 수 있다.  
HazardDetected event는 ActionCandidate 생성을 유도할 수 있다.  
하지만 HazardDetected event가 직접 ApprovedAction이나 ExecutionRequest를 만들 수는 없다.

---

## **16\. Validation Rules**

Event Type은 다음 조건을 만족할 때만 유효하다.

1. `event_type_id`가 registry에 존재해야 한다.  
2. status가 `active`이어야 한다.  
3. event category가 선언되어야 한다.  
4. allowed producer가 선언되어야 한다.  
5. allowed source type이 선언되어야 한다.  
6. payload schema reference가 선언되어야 한다.  
7. metadata schema reference가 선언되어야 한다.  
8. required field가 선언되어야 한다.  
9. topic 또는 stream reference가 선언되어야 한다.  
10. routing rule이 선언되어야 한다.  
11. world state effect가 선언되어야 한다.  
12. idempotency rule이 선언되어야 한다.  
13. ordering requirement가 선언되어야 한다.  
14. retention policy가 선언되어야 한다.  
15. sensitivity level이 선언되어야 한다.  
16. boundary가 선언되어야 한다.  
17. owner module이 선언되어야 한다.  
18. version이 유효해야 한다.  
19. deprecated 상태라면 migration metadata가 있어야 한다.

하나라도 누락되면 해당 Event Type은 operational lifecycle에 사용되면 안 된다.

---

## **17\. Event Instance Validation**

Event Instance는 다음 조건을 만족할 때만 수락될 수 있다.

Event Type이 registry에 존재하는가?  
Event Type이 active 상태인가?  
Producer가 허용된 producer인가?  
Source type이 허용되어 있는가?  
Payload가 schema를 통과하는가?  
Metadata가 core event schema를 통과하는가?  
Required fields가 모두 존재하는가?  
idempotency\_key가 존재하는가?  
중복 event가 아닌가?  
sensitivity policy를 만족하는가?  
routing rule이 존재하는가?

이 조건을 만족하지 못하면 event는 reject, quarantine, dead-letter queue 중 하나로 처리되어야 한다.

---

## **18\. Event Routing Rule**

Event Registry는 event가 어디로 전달되어야 하는지 정의한다.

예시 routing target:

world\_state\_service  
safety\_risk\_agent  
robot\_dispatch\_agent  
decision\_engine  
approval\_service  
execution\_state\_manager  
audit\_service  
operator\_ui  
supervisor\_ui

Routing은 topic 또는 stream 기반으로 수행될 수 있다.

Kafka topic  
MQTT topic  
Redis stream  
Internal async queue  
Event sourcing log

중요한 원칙은 다음과 같다.

Event routing은 실행이 아니다.  
Event routing은 물리 제어 명령이 아니다.

---

## **19\. World State Effect Rule**

Event가 World State에 미치는 영향은 명확히 선언되어야 한다.

권장 값:

none  
update  
append  
invalidate  
trigger\_recompute

### **19.1 none**

World State를 변경하지 않는다.

예시:

AuditRecordCreated  
ApprovalRequested

---

### **19.2 update**

기존 entity state를 갱신한다.

예시:

WorkerLocationUpdated  
RobotStatusUpdated  
EquipmentStatusChanged

---

### **19.3 append**

새로운 사건 기록을 추가한다.

예시:

HazardDetected  
IncidentReported  
ExecutionResultReceived

---

### **19.4 invalidate**

기존 cache 또는 state snapshot을 무효화한다.

예시:

OntologyVersionChanged  
PolicyVersionChanged  
AdapterStatusChanged

---

### **19.5 trigger\_recompute**

위험도, 계획, 경로, resource allocation 등을 재계산하도록 trigger한다.

예시:

ZoneBlocked  
HighRiskHazardDetected  
RobotUnavailable

---

## **20\. Idempotency Rule**

Event processing은 반드시 중복 처리에 안전해야 한다.

Idempotency가 필요한 이유는 다음과 같다.

Kafka replay  
MQTT duplicate delivery  
network retry  
external system retry  
consumer crash recovery  
event sourcing replay

권장 idempotency key 전략:

event\_id  
entity\_id \+ occurred\_at \+ source  
execution\_request\_id \+ adapter\_id \+ result\_status  
action\_candidate\_id  
decision\_case\_id  
approval\_request\_id

중요한 원칙:

같은 event가 두 번 들어와도  
World State, DecisionCase, ApprovalRequest, ExecutionResult가  
중복 생성되면 안 된다.

---

## **21\. Ordering Rule**

일부 event는 순서가 중요하다.

권장 ordering requirement:

none  
per\_entity  
per\_site  
global

### **21.1 none**

순서가 중요하지 않다.

---

### **21.2 per\_entity**

같은 entity에 대해서는 순서가 유지되어야 한다.

예시:

worker\_id별 위치 event  
robot\_id별 상태 event  
equipment\_id별 상태 event

---

### **21.3 per\_site**

현장 단위 순서가 중요하다.

예시:

emergency escalation event  
site-wide evacuation event

---

### **21.4 global**

전체 시스템에서 순서가 중요하다.

가급적 피해야 한다.  
Global ordering은 병목과 장애 지점을 만들 수 있다.

---

## **22\. Replay Rule**

Event는 replay 가능 여부를 명확히 선언해야 한다.

Replay가 필요한 경우:

World State 재구성  
Audit trace 재현  
Incident investigation  
Model evaluation  
Decision debugging  
Disaster recovery

하지만 모든 event가 replay되어서는 안 된다.

주의할 event:

외부 실행을 다시 유발할 수 있는 event  
알림을 중복 발송할 수 있는 event  
승인 요청을 중복 생성할 수 있는 event

Replay 시 원칙:

Replay는 상태 재구성용이어야 한다.  
Replay가 물리 실행을 다시 유발하면 안 된다.

---

## **23\. Retention Rule**

Event Type별 보관 기간은 다르게 설정되어야 한다.

예시:

WorkerLocationUpdated: short-term retention  
HazardDetected: long-term safety retention  
ApprovalGranted: long-term governance retention  
ExecutionResultReceived: long-term audit retention  
AuditRecordCreated: long-term or immutable retention

Retention은 법규, 안전, 감사, 비용, 개인정보 보호 요구사항을 고려해야 한다.

---

## **24\. Sensitivity 및 PII Rule**

Event는 sensitivity level과 PII classification을 가져야 한다.

권장 sensitivity level:

public  
internal  
confidential  
restricted  
safety\_critical

권장 PII classification:

none  
indirect  
direct  
sensitive

예시:

WorkerLocationUpdated:  
    sensitivity\_level: restricted  
    pii\_classification: direct

HazardDetected:  
    sensitivity\_level: safety\_critical  
    pii\_classification: indirect

ExecutionResultReceived:  
    sensitivity\_level: restricted  
    pii\_classification: indirect

PII가 포함된 event는 masking, access control, retention limit, audit access rule이 필요하다.

---

## **25\. Relationship to Agent Vocabulary Registry**

`agent_vocabulary_registry`는 agent가 어떤 event를 입력으로 받을 수 있는지 정의한다.

`event_registry`는 해당 event type이 무엇이고 어떤 schema를 가지는지 정의한다.

event\_registry:  
    WorkerLocationUpdated는 어떤 payload와 의미를 가지는가?

agent\_vocabulary\_registry:  
    SAFETY\_RISK\_AGENT가 WorkerLocationUpdated를 입력으로 받을 수 있는가?

Agent는 허용되지 않은 event type을 consume하면 안 된다.

---

## **26\. Relationship to Action Registry**

일부 event는 ActionCandidate 생성을 trigger할 수 있다.

하지만 event가 Action Type을 직접 생성하는 것은 아니다.

HazardDetected  
    ↓  
Safety Agent 분석  
    ↓  
ActionCandidateCreated  
    ↓  
action\_registry validation

Event Registry는 어떤 event가 action candidate generation을 유도할 수 있는지 표시할 수 있다.

Action Type의 유효성은 `action_registry`가 판단한다.

---

## **27\. Relationship to Decision Registry**

일부 event는 DecisionCase 생성을 trigger할 수 있다.

예시:

ActionCandidateCreated  
    ↓  
Decision Rule Lookup  
    ↓  
DecisionCaseCreated

Event Registry는 `decision_trigger_allowed`를 선언할 수 있지만, 어떤 Decision Rule을 적용할지는 `decision_registry`가 결정한다.

---

## **28\. Relationship to Approval Registry**

Approval 관련 event는 approval lifecycle을 기록한다.

예시:

ApprovalRequested  
ApprovalGranted  
ApprovalRejected  
ApprovalExpired  
ApprovalRevoked

Event Registry는 approval event의 schema와 routing을 정의한다.

Approval rule과 approval authority는 `approval_registry`가 관리한다.

---

## **29\. Relationship to Adapter Registry**

Execution 또는 feedback 관련 event는 adapter와 연결된다.

예시:

ExecutionDispatched  
ExecutionAcceptedByAdapter  
ExecutionRejectedByAdapter  
ExecutionResultReceived

Event Registry는 adapter event의 구조와 routing을 정의한다.

실제 adapter instance 선택은 `adapter_registry`가 담당한다.

---

## **30\. Relationship to Audit Registry**

Audit Event는 별도 audit event registry와 연결될 수 있다.

event\_registry:  
    어떤 event가 audit\_required인지 정의

audit\_event\_registry:  
    어떤 audit record schema와 retention rule을 사용할지 정의

모든 event가 audit event는 아니다.  
하지만 safety-critical, approval, decision, execution 관련 event는 audit 대상이어야 한다.

---

## **31\. Relationship to Ontology**

모든 중요한 Event Type은 semantic IRI를 가져야 한다.

예시:

event\_type\_id: event:HazardDetected  
semantic\_iri: ledo:HazardDetectedEvent

Ontology에서는 다음과 같이 정의할 수 있다.

ledo:HazardDetectedEvent  
    rdf:type ledo:EventType ;  
    rdfs:subClassOf ledo:SafetyEvent ;  
    ledo:observes ledo:Hazard ;  
    ledo:mayTrigger ledo:SafetyRiskAnalysis ;  
    ledo:requiresEvidence ledo:HazardDetectionSnapshot .

Ontology는 Event의 의미론적 기반을 제공한다.

Event Registry는 이를 운영 시스템에서 version, schema, routing, producer, retention, replay, audit rule로 관리한다.

---

## **32\. Versioning 및 Migration**

Event Type은 반드시 versioning되어야 한다.

다음 항목 중 하나라도 변경되면 version 변경이 필요하다.

1. payload schema 변경  
2. required field 변경  
3. metadata schema 변경  
4. allowed producer 변경  
5. routing rule 변경  
6. world state effect 변경  
7. trigger permission 변경  
8. idempotency strategy 변경  
9. ordering requirement 변경  
10. retention policy 변경  
11. sensitivity level 변경  
12. boundary 변경

Status 값:

draft  
active  
deprecated  
migration\_required  
retired  
blocked

Deprecated Event Type은 다음을 선언해야 한다.

deprecated\_since: datetime  
replacement\_event\_type\_id: string | null  
migration\_notes: string

Blocked Event Type은 새로운 event instance로 수락되면 안 된다.

---

## **33\. Implementation Use**

`event_registry`는 다음을 생성하거나 검증하는 데 사용된다.

1. `EventType` enum  
2. `EventCategory` enum  
3. CoreEvent metadata schema  
4. Event payload DTO constraints  
5. Event producer validation  
6. Event source validation  
7. Event schema validation  
8. Event routing rule lookup  
9. World State update rule lookup  
10. Agent trigger rule lookup  
11. Decision trigger rule lookup  
12. Audit requirement lookup  
13. Idempotency validation  
14. Ordering validation  
15. Replay rule validation  
16. Retention rule validation  
17. Sensitivity / PII rule validation  
18. Test case generation  
19. Migration rules

Implementation은 등록되지 않은 Event Type을 생성하거나 처리하면 안 된다.

---

## **34\. 권장 Code Structure**

registries/  
    event\_registry/  
        event\_registry.py  
        event\_registry\_entry.py  
        event\_category.py  
        event\_status.py  
        event\_effect.py  
        event\_sensitivity.py  
        event\_validation.py  
        event\_errors.py  
        event\_loader.py  
        event\_migration.py

    schema\_registry/  
    agent\_vocabulary\_registry/  
    action\_registry/  
    decision\_registry/  
    approval\_registry/  
    adapter\_registry/  
    audit\_event\_registry/

---

## **35\. Minimal Pydantic Model**

from enum import Enum  
from pydantic import BaseModel, Field  
from typing import Optional  
from datetime import datetime

class EventStatus(str, Enum):  
    DRAFT \= "draft"  
    ACTIVE \= "active"  
    DEPRECATED \= "deprecated"  
    MIGRATION\_REQUIRED \= "migration\_required"  
    RETIRED \= "retired"  
    BLOCKED \= "blocked"

class EventCategory(str, Enum):  
    SENSOR\_EVENT \= "sensor\_event"  
    WORLD\_STATE\_EVENT \= "world\_state\_event"  
    AGENT\_EVENT \= "agent\_event"  
    ACTION\_EVENT \= "action\_event"  
    DECISION\_EVENT \= "decision\_event"  
    APPROVAL\_EVENT \= "approval\_event"  
    SAFETY\_GATE\_EVENT \= "safety\_gate\_event"  
    EXECUTION\_EVENT \= "execution\_event"  
    EXTERNAL\_SYSTEM\_EVENT \= "external\_system\_event"  
    FEEDBACK\_EVENT \= "feedback\_event"  
    AUDIT\_EVENT \= "audit\_event"  
    SYSTEM\_EVENT \= "system\_event"  
    ERROR\_EVENT \= "error\_event"  
    SECURITY\_EVENT \= "security\_event"

class WorldStateEffect(str, Enum):  
    NONE \= "none"  
    UPDATE \= "update"  
    APPEND \= "append"  
    INVALIDATE \= "invalidate"  
    TRIGGER\_RECOMPUTE \= "trigger\_recompute"

class OrderingRequirement(str, Enum):  
    NONE \= "none"  
    PER\_ENTITY \= "per\_entity"  
    PER\_SITE \= "per\_site"  
    GLOBAL \= "global"

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

class EventRegistryEntry(BaseModel):  
    event\_type\_id: str  
    canonical\_name: str  
    display\_name: str  
    description: str  
    semantic\_iri: str

    event\_category: EventCategory

    version: str  
    status: EventStatus \= EventStatus.DRAFT

    allowed\_producer\_refs: list\[str\] \= Field(default\_factory=list)  
    allowed\_source\_types: list\[str\] \= Field(default\_factory=list)

    payload\_schema\_ref: str  
    metadata\_schema\_ref: str

    required\_fields: list\[str\] \= Field(default\_factory=list)  
    optional\_fields: list\[str\] \= Field(default\_factory=list)

    topic\_refs: list\[str\] \= Field(default\_factory=list)  
    stream\_refs: list\[str\] \= Field(default\_factory=list)  
    routing\_rule\_ref: str

    world\_state\_effect: WorldStateEffect \= WorldStateEffect.NONE

    agent\_trigger\_allowed: bool \= False  
    decision\_trigger\_allowed: bool \= False  
    approval\_trigger\_allowed: bool \= False  
    execution\_trigger\_allowed: bool \= False  
    audit\_required: bool \= False

    idempotency\_required: bool \= True  
    idempotency\_key\_strategy: str  
    ordering\_requirement: OrderingRequirement \= OrderingRequirement.NONE  
    replay\_allowed: bool \= False  
    retention\_policy\_ref: str

    producer\_authority\_level: str  
    consumer\_scope\_refs: list\[str\] \= Field(default\_factory=list)

    sensitivity\_level: SensitivityLevel \= SensitivityLevel.INTERNAL  
    pii\_classification: PIIClassification \= PIIClassification.NONE

    decision\_boundary: str  
    execution\_boundary: str  
    safety\_boundary: str

    audit\_event\_refs: list\[str\] \= Field(default\_factory=list)

    owner\_module: str  
    owner\_team: str  
    source\_document: str

    created\_at: datetime  
    updated\_at: datetime  
    deprecated\_since: Optional\[datetime\] \= None  
    replacement\_event\_type\_id: Optional\[str\] \= None

---

## **36\. Core Validation Function**

def validate\_event\_instance(  
    entry: EventRegistryEntry,  
    event\_type\_id: str,  
    producer\_ref: str,  
    source\_type: str,  
    payload: dict,  
) \-\> None:  
    if entry.status \!= EventStatus.ACTIVE:  
        raise InvalidEventTypeError(  
            f"Event Type is not active: {entry.event\_type\_id}"  
        )

    if event\_type\_id \!= entry.event\_type\_id:  
        raise EventTypeMismatchError(  
            f"Event Type '{event\_type\_id}' does not match registry entry "  
            f"'{entry.event\_type\_id}'"  
        )

    if producer\_ref not in entry.allowed\_producer\_refs:  
        raise EventProducerNotAllowedError(  
            f"Producer '{producer\_ref}' is not allowed for Event Type "  
            f"'{entry.event\_type\_id}'"  
        )

    if source\_type not in entry.allowed\_source\_types:  
        raise EventSourceTypeNotAllowedError(  
            f"Source type '{source\_type}' is not allowed for Event Type "  
            f"'{entry.event\_type\_id}'"  
        )

    for field in entry.required\_fields:  
        if field not in payload:  
            raise EventPayloadValidationError(  
                f"Required field '{field}' is missing from payload"  
            )

    if not entry.payload\_schema\_ref:  
        raise InvalidEventRegistryEntryError(  
            "payload\_schema\_ref must be declared"  
        )

    if not entry.metadata\_schema\_ref:  
        raise InvalidEventRegistryEntryError(  
            "metadata\_schema\_ref must be declared"  
        )

    if not entry.routing\_rule\_ref:  
        raise InvalidEventRegistryEntryError(  
            "routing\_rule\_ref must be declared"  
        )

    if entry.idempotency\_required and not entry.idempotency\_key\_strategy:  
        raise InvalidEventRegistryEntryError(  
            "idempotency\_key\_strategy must be declared when idempotency is required"  
        )

    if not entry.retention\_policy\_ref:  
        raise InvalidEventRegistryEntryError(  
            "retention\_policy\_ref must be declared"  
        )

---

## **37\. Test Scenarios**

필수 테스트는 다음과 같다.

1\. 등록되지 않은 Event Type 거부  
2\. inactive Event Type 거부  
3\. deprecated Event Type 사용 거부  
4\. blocked Event Type 사용 거부  
5\. 허용되지 않은 producer가 생성한 event 거부  
6\. 허용되지 않은 source type 거부  
7\. payload schema 불일치 거부  
8\. required field 누락 거부  
9\. metadata schema 누락 거부  
10\. routing rule 누락 거부  
11\. idempotency key 누락 거부  
12\. duplicate event 중복 처리 방지 검증  
13\. ordering requirement 검증  
14\. replay 시 physical execution 재발생 방지 검증  
15\. sensitivity / PII rule 검증  
16\. audit\_required event가 audit log를 생성하는지 검증  
17\. world\_state\_effect update event가 World State를 정확히 갱신하는지 검증  
18\. decision\_trigger\_allowed event가 Decision Registry를 우회하지 않는지 검증  
19\. execution\_trigger\_allowed가 false인 event가 ExecutionRequest를 만들지 못하는지 검증  
20\. Event migration rule 검증

---

## **38\. Final Rule**

등록된 Event Type이 없으면,  
유효한 Event Instance도 없다.

유효한 Event Instance가 없으면,  
World State Update도 없다.

Event는 ActionCandidate가 아니다.

Event는 DecisionCase가 아니다.

Event는 ApprovalDecision이 아니다.

Event는 ExecutionRequest가 아니다.

Event는 PhysicalCommand가 아니다.

Event는 External System 제어가 아니다.

Event는 lifecycle을 trigger할 수 있지만,  
lifecycle boundary를 우회할 수 없다.

`event_registry`는 LEDO 시스템 전체의 사건 흐름을 통제하는 핵심 결정론적 레지스트리이다.

이 모듈은 모든 Event Type의 의미, schema, producer, routing, idempotency, replay, retention, sensitivity, audit rule을 정의하고, event가 Action, Decision, Approval, Execution의 경계를 침범하지 못하도록 보장한다.

핵심 정의는 다음과 같다.

Event Registry  
\= 이벤트 이름 목록이 아니라,  
시스템에서 발생하는 모든 사건의 의미, 구조, source,  
routing, world state effect, idempotency, replay,  
retention, sensitivity, audit rule을 통제하는  
이벤트 운영 계약 레지스트리

