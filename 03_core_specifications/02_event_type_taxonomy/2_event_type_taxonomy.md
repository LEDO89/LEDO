# **Ontology-Centric “Event Type Taxonomy” v1 26.06**

---

# **1\. Purpose**

This document defines the core rules of the Event Type Taxonomy used in an ontology-centric cyber-physical platform.

Event Type Taxonomy is the practice of organizing all events occurring within the system using standardized names and a standardized classification structure.

This document is not intended to list every event type in detail.

This document focuses on the following:

Define what an Event Type is.  
Define Event Type naming rules.  
Distinguish Stream Data from Discrete Events.  
Define the relationship between Event Types and Ontology Mapping.  
Distinguish Event Types from Action Types and DTO Types.  
Define the operating principles of the Event Type Registry.  
Define how vendor-specific events can be extended.  
Define how Event Types connect to lifecycle path, storage route, ontology bus entry, and audit.

The full event type list is managed in a separate document: Appendix A: Event Type Catalog.

---

# **2\. Document Separation Principle**

In the previous version, Core Taxonomy and Event Catalog were mixed into one document.

This approach is useful during the design draft phase, but as a practical implementation document, it becomes too long and repetitive.

Therefore, Event Type Taxonomy is divided into the following two documents.

## **2.1 Core Taxonomy Specification**

This is the present document.

It covers:

event type definition  
naming convention  
classification model  
stream vs discrete distinction  
ontology mapping rule  
vendor extension pattern  
registry governance  
lifecycle routing rule  
Initial reference event type set

## **2.2 Appendix A: Event Type Catalog**

This is a separate appendix document.

It covers:

industrial event list  
construction event list  
robot event list  
safety event list  
AI / agent event list  
decision / approval event list  
execution event list  
feedback / recovery event list  
audit / governance event list  
observability event list  
vendor extension examples

By separating the documents this way, the core document can remain short and stable, while the event catalog can continue to expand.

---

# **3\. Definition of Event Type**

An Event Type is the standardized classification name of an event that occurs within the platform.

An Event Type must answer the following questions:

What happened?  
In which domain did it happen?  
Which entity is involved?  
Is this event stream data or a discrete event?  
Is this event monitoring-only, standard path, or emergency path?  
Does this event trigger an ontology property change?  
Can this event create an ActionCandidate?  
Is this event subject to audit?

Examples:

industrial.sensor.reading\_received

Meaning:

A sensor reading was received in the industrial domain.

robot.mission.blocked

Meaning:

A robot mission became blocked.

construction.permit.expired

Meaning:

A construction work permit expired.

safety.gas.critical\_threshold\_exceeded

Meaning:

A gas sensor value exceeded the critical threshold.

---

# **4\. Core Distinctions**

## **4.1 Distinction Between Event Type and DTO Type**

A DTO Type is a structure that holds data.

An Event Type is the name of the event contained within that structure.

Example:

DTO Type:

CanonicalEventEnvelopeDTO

Event Types:

industrial.sensor.reading\_received  
robot.mission.blocked  
construction.permit.expired

In other words:

A DTO is the container.  
An Event Type is the name of the event inside that container.

---

## **4.2 Distinction Between Event Type and Action Type**

An Event Type is something that has already happened.

An Action Type is something to be performed in response.

Example:

Event Type:

safety.worker.entered\_danger\_zone

Meaning:

A worker entered a danger zone.

Action Types:

ACTION\_NOTIFY\_SUPERVISOR  
ACTION\_STOP\_WORK  
ACTION\_EVACUATE\_ZONE

Meaning:

Notify the supervisor.  
Stop the work.  
Evacuate the zone.

An Event is the cause.  
An Action is the response.

---

## **4.3 Distinction Between Stream Data and Discrete Event**

Stream Data refers to high-frequency, repeated, continuous data.

Examples:

robot.pose.updated  
robot.telemetry.received  
industrial.sensor.reading\_received  
monitoring.timeseries.bundle\_received

A Discrete Event refers to a meaningful state change or incident.

Examples:

robot.mission.blocked  
construction.permit.expired  
safety.worker.entered\_danger\_zone  
industrial.plc.critical\_alarm\_raised  
approval.decision.granted  
feedback.completed

Core principles:

Stream Data goes to the Time-Series DB by default.  
Discrete Events go to the Event Store and Ontology Bus by default.  
When Stream Data creates a threshold crossing, anomaly, or state change, it is promoted to a Discrete Event.

Examples:

robot.pose.updated  
→ Time-Series DB

robot.proximity.warning  
→ Standard Path

robot.collision\_imminent  
→ Emergency Fast-Path

---

## **4.4 Distinction Between Monitoring Event and Stream Data**

Monitoring is a processing purpose.

Stream Data is a data form.

Therefore, the two concepts are not the same.

Example:

robot.pose.updated

This event is likely both stream data and monitoring-only.

monitoring.threshold.crossed

This event occurs in the monitoring domain, but it can be promoted to a discrete event.

Summary:

Stream Data  
→ A form of continuously incoming data

Monitoring Event  
→ An event used for monitoring, dashboarding, trend tracking, or heartbeat purposes

Threshold / anomaly occurrence  
→ Promotes an event from Monitoring-Only to the Standard or Emergency Path

---

# **5\. Event Type Naming Convention**

## **5.1 Basic Format**

The basic format is as follows:

domain.entity.event\_action

Examples:

industrial.sensor.reading\_received  
industrial.plc.alarm\_raised  
robot.mission.blocked  
construction.permit.expired  
safety.zone.risk\_level\_changed  
feedback.execution.completed

---

## **5.2 Detailed Format**

For more specific cases, the following format may be used:

domain.subdomain.entity.event\_action

Examples:

industrial.opcua.node\_value\_changed  
industrial.modbus.register\_value\_changed  
robot.fleet.mission\_assigned  
construction.safety.scaffold\_inspection\_failed  
ai.rag.evidence\_summary\_generated

---

## **5.3 Vendor Extension Format**

For events from external vendors, specific equipment manufacturers, or specific robot platforms, the following format is allowed:

domain.subdomain.vendor.entity.event\_action

Examples:

robot.fleet.boston\_dynamics.spot.payload\_detached  
industrial.plc.siemens.s7.connection\_lost  
industrial.plc.mitsubishi.fx.critical\_alarm\_raised  
robot.arm.doosan.cobot.safety\_stop\_triggered

This format is an extension pattern that prevents the core taxonomy from being forced to register every vendor-specific event.

---

## **5.4 Naming Rules**

Event types use lowercase snake\_case.

Good examples:

construction.worker.entered\_zone  
robot.mission.status\_changed  
industrial.sensor.reading\_received

Bad examples:

IndustrialSensorReadingReceived  
RobotMissionBlocked  
Worker Entered Zone  
sensorEvent1

---

## **5.5 Event Action Uses Past Tense or State-Change Form**

An Event is something that has already happened.

Therefore, event\_action should use past tense or a state-change form.

Good examples:

reading\_received  
status\_changed  
alarm\_raised  
permit\_expired  
mission\_completed  
feedback\_received

Bad examples:

read\_sensor  
change\_status  
raise\_alarm  
expire\_permit  
move\_robot

Imperative forms should be used for Action Types, not Event Types.

---

# **6\. Classification Model**

In the previous document, there were too many separate classification axes.

In the final structure, the classification axes are grouped into four categories.

---

## **6.1 Semantic Classification**

Defines what the event means.

Fields:

event\_type  
event\_category  
domain\_module  
subject\_type  
source\_type  
severity  
evidence\_eligibility

Example:

event\_type \= safety.gas.critical\_threshold\_exceeded  
domain\_module \= safety  
subject\_type \= Sensor  
severity \= CRITICAL\_EMERGENCY  
evidence\_eligibility \= EVIDENCE\_REQUIRED

---

## **6.2 Routing Classification**

Defines where the event should flow.

Fields:

default\_lifecycle\_path  
actionability  
can\_generate\_candidate  
can\_trigger\_emergency  
requires\_audit

Example:

default\_lifecycle\_path \= EMERGENCY\_FAST\_PATH  
actionability \= REQUIRES\_EMERGENCY\_ACTION  
can\_trigger\_emergency \= true  
requires\_audit \= true

---

## **6.3 Data Handling Classification**

Defines the event’s storage route and processing method.

Fields:

is\_stream\_data  
storage\_route  
supports\_batching  
supports\_windowing  
ontology\_bus\_entry\_policy

Example:

event\_type \= robot.pose.updated  
is\_stream\_data \= true  
storage\_route \= TIME\_SERIES\_DB  
ontology\_bus\_entry\_policy \= ON\_ANOMALY

---

## **6.4 Ontology Mapping Classification**

Defines how the event affects the ontology.

Fields:

requires\_ontology\_binding  
ontology\_mapping\_effect  
mapped\_ontology\_property  
requires\_subject\_binding  
requires\_object\_binding

Example:

event\_type \= construction.worker.entered\_zone  
ontology\_mapping\_effect \= UPDATES\_OBJECT\_PROPERTY  
mapped\_ontology\_property \= hasLocation

---

# **7\. Core Classification Values**

## **7.1 Lifecycle Path**

Lifecycle Path means which processing path the event follows.

Values:

STANDARD  
EMERGENCY\_FAST\_PATH  
MONITORING\_ONLY  
GOVERNANCE\_REVIEW  
AUDIT\_ONLY

Role:

Determines the processing workflow.

---

## **7.2 Actionability**

Actionability means whether the event can create an action candidate.

Values:

NO\_ACTION  
MAY\_GENERATE\_CANDIDATE  
REQUIRES\_CANDIDATE  
REQUIRES\_EMERGENCY\_ACTION  
AUDIT\_ONLY

Role:

Determines the possibility of ActionCandidate generation.

---

## **7.3 Storage Route**

Storage Route means where the event is stored by default.

Values:

TIME\_SERIES\_DB  
EVENT\_STORE  
KNOWLEDGE\_GRAPH  
AUDIT\_STORE  
OBSERVABILITY\_STORE

Role:

Determines the data storage route.

Example:

robot.pose.updated  
→ TIME\_SERIES\_DB

construction.permit.expired  
→ EVENT\_STORE \+ KNOWLEDGE\_GRAPH \+ AUDIT\_STORE

---

## **7.4 Ontology Bus Entry Policy**

Ontology Bus Entry Policy defines the condition under which an event enters the ontology bus.

Values:

ALWAYS  
ON\_THRESHOLD  
ON\_ANOMALY  
ON\_STATE\_CHANGE  
ON\_ESCALATION  
NEVER

Role:

Prevents every event from entering the ontology bus.

Example:

industrial.sensor.reading\_received  
→ ON\_THRESHOLD

robot.mission.blocked  
→ ALWAYS

---

## **7.5 Ontology Mapping Effect**

Ontology Mapping Effect defines how the event affects ontology individuals, ObjectProperties, or DataProperties.

Values:

NO\_ONTOLOGY\_EFFECT  
UPDATES\_DATA\_PROPERTY  
UPDATES\_OBJECT\_PROPERTY  
CREATES\_RELATION  
REMOVES\_RELATION  
CREATES\_INDIVIDUAL  
UPDATES\_INDIVIDUAL\_STATE  
TRIGGERS\_MAPPING\_REVIEW

Examples:

construction.worker.entered\_zone  
→ UPDATES\_OBJECT\_PROPERTY  
→ hasLocation

industrial.sensor.reading\_changed  
→ UPDATES\_DATA\_PROPERTY  
→ hasCurrentValue

robot.mission.blocked  
→ UPDATES\_INDIVIDUAL\_STATE  
→ hasMissionStatus

---

# **8\. Event-to-Ontology Mapping Rule**

An Event Type does not necessarily need to map one-to-one to an ontology class.

However, when it flows into WorldStateUpdateDTO or OntologyBoundEventDTO, it must be clear which ontology element is changing.

Therefore, the Event Type Registry must include an Event-to-Ontology Mapping Table.

## **8.1 Mapping Table Fields**

Recommended fields:

event\_type  
subject\_type  
object\_type  
ontology\_property  
ontology\_mapping\_effect  
state\_type  
value\_source\_path  
requires\_subject\_binding  
requires\_object\_binding  
requires\_evidence  
requires\_world\_state\_update  
version  
valid\_from  
valid\_until

---

## **8.2 ObjectProperty Change Example**

Event Type:

construction.worker.entered\_zone

Ontology Effect:

Creates or updates the `hasLocation` relationship between a Worker individual and a Zone individual.

Mapping:

subject\_type \= Worker  
object\_type \= Zone  
ontology\_property \= hasLocation  
ontology\_mapping\_effect \= UPDATES\_OBJECT\_PROPERTY

---

## **8.3 DataProperty Change Example**

Event Type:

industrial.sensor.reading\_changed

Ontology Effect:

Updates the `hasCurrentValue` value of a Sensor individual.

Mapping:

subject\_type \= Sensor  
ontology\_property \= hasCurrentValue  
ontology\_mapping\_effect \= UPDATES\_DATA\_PROPERTY

---

## **8.4 Individual State Change Example**

Event Type:

robot.mission.blocked

Ontology Effect:

Changes the `hasMissionStatus` value of a Mission individual to Blocked.

Mapping:

subject\_type \= Mission  
ontology\_property \= hasMissionStatus  
ontology\_mapping\_effect \= UPDATES\_INDIVIDUAL\_STATE

---

# **9\. Vendor Extension Pattern**

## **9.1 Problem**

Construction sites and robot fleets use many types of external equipment.

Examples:

Boston Dynamics Spot  
Doosan Robotics Cobot  
Siemens PLC  
Mitsubishi PLC  
Honeywell Sensor  
vendor-specific fleet manager

It is nearly impossible to directly register every error code and event emitted by these devices into the core registry.

---

## **9.2 Solution Principle**

The Core Registry accepts vendor-specific events through wildcard patterns.

Examples:

robot.fleet.\*  
industrial.plc.\*  
industrial.sensor.\*  
robot.arm.\*

Vendor-specific payload interpretation is handled by the adapter layer.

In other words:

Core Registry  
→ Manages the common event contract, lifecycle rules, and safety rules

Vendor Adapter  
→ Interprets vendor error codes, proprietary payloads, and vendor-specific events

---

## **9.3 Vendor Event Examples**

robot.fleet.boston\_dynamics.spot.payload\_detached  
robot.fleet.boston\_dynamics.spot.estop\_triggered  
industrial.plc.siemens.s7.connection\_lost  
industrial.plc.mitsubishi.fx.critical\_alarm\_raised  
robot.arm.doosan.cobot.safety\_stop\_triggered

---

# **10\. Event Type Registry Operating Policy**

The weakest part of the previous document was the registry operating model.

Event Type Taxonomy must be operated as a registry, not merely as a list.

---

## **10.1 EventTypeSpecDTO Fields**

Recommended fields:

event\_type  
event\_category  
domain\_module  
allowed\_sources  
allowed\_subject\_types

default\_lifecycle\_path  
severity  
actionability  
evidence\_eligibility

is\_stream\_data  
storage\_route  
supports\_batching  
supports\_windowing  
ontology\_bus\_entry\_policy

requires\_validation  
requires\_ontology\_binding  
requires\_audit

ontology\_mapping\_effect  
mapped\_ontology\_property

vendor\_extension\_allowed  
vendor\_pattern

owner  
version  
status  
valid\_from  
valid\_until  
deprecated\_at  
replacement\_event\_type  
change\_reason

---

## **10.2 Registry Status**

An Event Type may have the following statuses:

DRAFT  
ACTIVE  
DEPRECATED  
RETIRED  
BLOCKED

Meaning:

DRAFT  
→ Under review

ACTIVE  
→ Available for use

DEPRECATED  
→ No longer recommended, but maintained for backward compatibility

RETIRED  
→ No new events may be received

BLOCKED  
→ Blocked due to a security or safety issue

---

## **10.3 Registry Versioning**

An Event Type must have a version.

Backward-compatible changes:

Adding optional metadata  
Adding an allowed source  
Adding a monitoring metric  
Enhancing the storage route  
Adding a description  
Strengthening a validator

Breaking changes:

Changing the event\_type name  
Changing the meaning of severity  
Changing the lifecycle path  
Changing the storage route  
Changing the ontology mapping effect  
Removing an audit requirement  
Changing the meaning of an emergency trigger

As a rule, breaking changes should be separated into a new event\_type.

---

## **10.4 Approval Process**

Changes to an Event Type must be approved by the owner and the domain steward.

Recommended approval authorities:

Domain Owner  
Ontology Steward  
Safety Owner  
Policy Owner  
Platform Architect  
Vendor Adapter Owner

For high-risk events, approval from the Safety Owner and Policy Owner is mandatory.

---

## **10.5 Deprecation Policy**

An Event Type should not be deleted immediately.

Recommended process:

Change status to DEPRECATED  
Specify replacement\_event\_type  
Operate a dual-read / dual-write period  
Migrate downstream consumers  
Verify audit compatibility  
Change status to RETIRED  
Remove in a major version if necessary

---

## **10.6 Registry Compatibility Rule**

Past event records must always remain interpretable.

Therefore, EventTypeSpecDTO must preserve the version and status at the time of creation.

AuditRecord must reference not only event\_type, but also event\_type\_version.

---

# **11\. Post-hoc Audit Event Lifecycle**

Events and actions that use the Emergency Fast-Path must always have a post-hoc audit lifecycle.

## **11.1 Basic Flow**

action.emergency\_approved.created  
→ action.emergency\_approved.post\_audit\_required  
→ audit.emergency.post\_audit\_pending  
→ audit.emergency.post\_audit\_completed

## **11.2 Flow When a Problem Occurs**

audit.emergency.post\_audit\_pending  
→ audit.emergency.post\_audit\_escalated

Or:

audit.emergency.post\_audit\_completed  
→ governance.policy.updated

Or:

audit.emergency.post\_audit\_completed  
→ governance.emergency\_action.deprecated

## **11.3 Principle**

Because the Emergency Fast-Path is fast, its post-hoc audit must be stronger.

A human manager must confirm how the emergency action actually ended in the field.

An Emergency event whose post-hoc audit has not been closed is not considered to have fully completed its lifecycle.

---

# **12\. Initial Reference Event Type Set**

The full event list is managed in the appendix.

In the initial implementation, only the following event types should be registered first.

## **12.1 Industrial Reference Events**

industrial.sensor.reading\_received  
industrial.sensor.threshold\_crossed  
industrial.sensor.offline\_detected  
industrial.plc.alarm\_raised  
industrial.equipment.mode\_changed

## **12.2 Construction Reference Events**

construction.worker.entered\_zone  
construction.worker.exited\_zone  
construction.permit.expired  
construction.task.status\_changed  
construction.inspection.failed

## **12.3 Safety Reference Events**

safety.zone.risk\_level\_changed  
safety.worker.entered\_danger\_zone  
safety.gas.critical\_threshold\_exceeded  
safety.emergency.fast\_path\_triggered

## **12.4 Robot Reference Events**

robot.telemetry.received  
robot.pose.updated  
robot.mission.assigned  
robot.mission.blocked  
robot.mission.completed  
robot.battery.critical

## **12.5 Lifecycle Reference Events**

validation.input.passed  
canonicalization.identity.resolved  
ontology.binding.completed  
evidence.created  
world\_state.updated  
agent.action\_candidate.created  
decision.case.created  
approval.request.created  
action.approved.created  
execution.request.created  
external\_control.request.sent  
feedback.completed  
audit.record.created  
audit.emergency.post\_audit\_pending  
audit.emergency.post\_audit\_completed

---

# **13\. Separation Criteria for Appendix B: Event Type Catalog**

Detailed lists by Event Category are not included in the main body.

The following items are managed in `09_appendices/appendix_b_event_catalog/event_catalog.md` (Appendix B; Appendix A is the Stack Catalog):

industrial event catalog  
construction event catalog  
robot event catalog  
safety event catalog  
AI / agent event catalog  
decision / approval event catalog  
execution event catalog  
feedback / recovery event catalog  
audit / governance event catalog  
observability event catalog  
vendor extension event examples

This prevents the Core document from becoming too long.

---

# **14\. Recommended File Structure**

## **14.1 Core Taxonomy**

event\_taxonomy/  
  \_\_init\_\_.py  
  core.py  
  event\_type\_spec.py  
  registry.py  
  classification.py  
  stream\_policy.py  
  storage\_route.py  
  ontology\_mapping\_effect.py  
  vendor\_patterns.py

## **14.2 Event Catalog**

event\_taxonomy/catalog/  
  industrial\_events.py  
  construction\_events.py  
  robot\_events.py  
  safety\_events.py  
  ai\_events.py  
  governance\_events.py  
  execution\_events.py  
  feedback\_events.py  
  observability\_events.py

## **14.3 Mapping Tables**

event\_taxonomy/mappings/  
  event\_to\_ontology\_mapping.py  
  event\_to\_lifecycle\_path.py  
  event\_to\_storage\_route.py  
  vendor\_event\_patterns.py

---

# **15\. Recommended Implementation Order**

The implementation order should be as follows.

EventCategory enum  
DomainModule enum  
LifecyclePath enum  
SeverityLevel enum  
Actionability enum  
EvidenceEligibility enum  
StreamClassification enum  
StorageRoute enum  
OntologyBusEntryPolicy enum  
OntologyMappingEffect enum  
EventTypeSpecDTO  
EventTypeRegistry  
Registry status enum  
Vendor wildcard pattern validator  
Event-to-Ontology Mapping Table  
Initial reference event type constants  
EventType validation function  
Connection to CanonicalEventEnvelopeDTO  
Connection to PathClassificationDTO

---

# **16\. Final Principle**

Event Type Taxonomy is the event language of the platform.

If a DTO is the container for data, an Event Type is the name of the event inside that container.

If ontology is the semantic skeleton, Event Type is the standardized sensory system through which the system detects changes in reality.

However, not every sensory signal immediately changes the knowledge graph.

High-frequency stream data follows the time-series path.  
Only meaningful changes are promoted to the ontology bus.  
Discrete events enter the semantic pipeline.  
Vendor-specific events are interpreted by the adapter layer.  
The Core Registry controls them through wildcard patterns.  
Emergency events must always have a post-hoc audit lifecycle.  
An Event Type can act as a trigger for ontology property changes.

The final principles are as follows:

Different sources, one event language.  
Different signals, one taxonomy.  
Different frequencies, one routing policy.  
Different domains, one event registry.  
Different vendors, one extension pattern.  
Different risks, one lifecycle classification.  
Different events, one semantic backbone.

# **Ontology-Centric “Event Type Taxonomy” v1 26.06**

