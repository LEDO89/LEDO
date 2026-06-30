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
MVP event type set

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

# **12\. MVP Event Type Set**

The full event list is managed in the appendix.

In the MVP, only the following event types should be registered first.

## **12.1 Industrial MVP Events**

industrial.sensor.reading\_received  
industrial.sensor.threshold\_crossed  
industrial.sensor.offline\_detected  
industrial.plc.alarm\_raised  
industrial.equipment.mode\_changed

## **12.2 Construction MVP Events**

construction.worker.entered\_zone  
construction.worker.exited\_zone  
construction.permit.expired  
construction.task.status\_changed  
construction.inspection.failed

## **12.3 Safety MVP Events**

safety.zone.risk\_level\_changed  
safety.worker.entered\_danger\_zone  
safety.gas.critical\_threshold\_exceeded  
safety.emergency.fast\_path\_triggered

## **12.4 Robot MVP Events**

robot.telemetry.received  
robot.pose.updated  
robot.mission.assigned  
robot.mission.blocked  
robot.mission.completed  
robot.battery.critical

## **12.5 Lifecycle MVP Events**

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

# **13\. Separation Criteria for Appendix A: Event Type Catalog**

Detailed lists by Event Category are not included in the main body.

The following items are managed in Appendix A:

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

The MVP implementation order should be as follows.

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
MVP event type constants  
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

# **1\. 목적**

본 문서는 온톨로지 중심 사이버-물리 플랫폼에서 사용되는 Event Type Taxonomy의 핵심 규칙을 정의한다.

Event Type Taxonomy는 시스템 안에서 발생하는 사건을 표준 이름과 분류 체계로 정리하는 것이다.

이 문서는 모든 event type 목록을 길게 나열하는 문서가 아니다.

본 문서는 다음에 집중한다.

1. Event Type이 무엇인지 정의한다.  
2. Event Type 이름 규칙을 정의한다.  
3. Stream Data와 Discrete Event를 구분한다.  
4. Event Type과 Ontology Mapping의 관계를 정의한다.  
5. Event Type과 Action Type, DTO Type을 구분한다.  
6. Event Type Registry 운영 원칙을 정의한다.  
7. Vendor-specific event 확장 방식을 정의한다.  
8. Event Type이 lifecycle path, storage route, ontology bus entry, audit과 어떻게 연결되는지 정의한다.

전체 event type 목록은 별도 문서인 Appendix A: Event Type Catalog에서 관리한다.

---

# **2\. 문서 분리 원칙**

기존 문서는 Core Taxonomy와 Event Catalog가 하나의 문서 안에 섞여 있었다.

이 방식은 설계 초안 단계에서는 유용하지만, 실무 문서로는 너무 길고 반복이 많다.

따라서 Event Type Taxonomy는 다음 2개 문서로 분리한다.

## **2.1 Core Taxonomy Specification**

본 문서다.

다루는 내용:

event type 정의  
naming convention  
classification model  
stream vs discrete 구분  
ontology mapping rule  
vendor extension pattern  
registry governance  
lifecycle routing rule  
MVP event type set

## **2.2 Appendix A: Event Type Catalog**

별도 부록 문서다.

다루는 내용:

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

이렇게 분리하면 핵심 문서는 짧고 안정적으로 유지되고, event catalog는 계속 확장할 수 있다.

---

# **3\. Event Type의 정의**

Event Type은 플랫폼 안에서 발생한 사건의 표준 분류명이다.

Event Type은 다음 질문에 답해야 한다.

무엇이 발생했는가?  
어느 도메인에서 발생했는가?  
어떤 entity가 관련되었는가?  
이 사건은 stream data인가, discrete event인가?  
이 사건은 monitoring-only인가, standard path인가, emergency path인가?  
이 사건은 ontology property 변경을 유발하는가?  
이 사건은 ActionCandidate를 만들 수 있는가?  
이 사건은 audit 대상인가?

예:

industrial.sensor.reading\_received

의미:

산업 도메인에서 센서 측정값이 수신되었다.

robot.mission.blocked

의미:

로봇 미션이 차단 상태가 되었다.

construction.permit.expired

의미:

건설 작업 허가가 만료되었다.

safety.gas.critical\_threshold\_exceeded

의미:

가스 센서 값이 critical threshold를 초과했다.

---

# **4\. 핵심 구분**

## **4.1 Event Type과 DTO Type의 구분**

DTO Type은 데이터를 담는 구조다.

Event Type은 그 구조 안에 들어가는 사건의 이름이다.

예:

DTO Type:

CanonicalEventEnvelopeDTO

Event Type:

industrial.sensor.reading\_received  
robot.mission.blocked  
construction.permit.expired

즉:

DTO는 그릇이다.  
Event Type은 그 그릇 안에 들어가는 사건의 이름이다.

---

## **4.2 Event Type과 Action Type의 구분**

Event Type은 이미 발생한 사건이다.

Action Type은 앞으로 수행하려는 조치다.

예:

Event Type:

safety.worker.entered\_danger\_zone

의미:

작업자가 위험 구역에 들어갔다.

Action Type:

ACTION\_NOTIFY\_SUPERVISOR  
ACTION\_STOP\_WORK  
ACTION\_EVACUATE\_ZONE

의미:

감독자에게 알린다.  
작업을 중지한다.  
구역을 대피시킨다.

Event는 원인이다.  
Action은 대응이다.

---

## **4.3 Stream Data와 Discrete Event의 구분**

Stream Data는 고주기, 반복, 연속적인 데이터다.

예:

robot.pose.updated  
robot.telemetry.received  
industrial.sensor.reading\_received  
monitoring.timeseries.bundle\_received

Discrete Event는 의미 있는 상태 변화나 사건이다.

예:

robot.mission.blocked  
construction.permit.expired  
safety.worker.entered\_danger\_zone  
industrial.plc.critical\_alarm\_raised  
approval.decision.granted  
feedback.completed

핵심 원칙:

Stream Data는 기본적으로 Time-Series DB로 간다.  
Discrete Event는 기본적으로 Event Store와 Ontology Bus로 간다.  
Stream Data가 threshold, anomaly, state change를 만들면 Discrete Event로 승격된다.

예:

robot.pose.updated  
→ Time-Series DB

robot.proximity.warning  
→ Standard Path

robot.collision\_imminent  
→ Emergency Fast-Path

---

## **4.4 Monitoring Event와 Stream Data의 구분**

Monitoring은 처리 목적이다.

Stream Data는 데이터 형태다.

따라서 두 개념은 같지 않다.

예:

robot.pose.updated

이 이벤트는 stream data이면서 monitoring-only일 가능성이 높다.

monitoring.threshold.crossed

이 이벤트는 monitoring 영역에서 발생했지만, discrete event로 승격될 수 있다.

정리:

Stream Data  
→ 연속적으로 들어오는 데이터 형태

Monitoring Event  
→ 감시, dashboard, trend, heartbeat 목적의 event

Threshold / anomaly 발생  
→ Monitoring-only에서 Standard 또는 Emergency Path로 승격

---

# **5\. Event Type Naming Convention**

## **5.1 기본 형식**

기본 형식은 다음과 같다.

domain.entity.event\_action

예:

industrial.sensor.reading\_received  
industrial.plc.alarm\_raised  
robot.mission.blocked  
construction.permit.expired  
safety.zone.risk\_level\_changed  
feedback.execution.completed

---

## **5.2 세부 형식**

더 구체적인 경우 다음 형식을 사용할 수 있다.

domain.subdomain.entity.event\_action

예:

industrial.opcua.node\_value\_changed  
industrial.modbus.register\_value\_changed  
robot.fleet.mission\_assigned  
construction.safety.scaffold\_inspection\_failed  
ai.rag.evidence\_summary\_generated

---

## **5.3 Vendor Extension 형식**

외부 vendor, 특정 장비 제조사, 특정 로봇 플랫폼의 event는 다음 형식을 허용한다.

domain.subdomain.vendor.entity.event\_action

예:

robot.fleet.boston\_dynamics.spot.payload\_detached  
industrial.plc.siemens.s7.connection\_lost  
industrial.plc.mitsubishi.fx.critical\_alarm\_raised  
robot.arm.doosan.cobot.safety\_stop\_triggered

이 형식은 vendor-specific event를 core taxonomy 안에 무리하게 모두 등록하지 않기 위한 확장 패턴이다.

---

## **5.4 이름 규칙**

event type은 소문자 snake\_case를 사용한다.

좋은 예:

construction.worker.entered\_zone  
robot.mission.status\_changed  
industrial.sensor.reading\_received

나쁜 예:

IndustrialSensorReadingReceived  
RobotMissionBlocked  
Worker Entered Zone  
sensorEvent1

---

## **5.5 Event Action은 과거형 또는 상태 변화형을 사용한다**

Event는 이미 발생한 사건이다.

따라서 event\_action은 과거형 또는 상태 변화형을 사용한다.

좋은 예:

reading\_received  
status\_changed  
alarm\_raised  
permit\_expired  
mission\_completed  
feedback\_received

나쁜 예:

read\_sensor  
change\_status  
raise\_alarm  
expire\_permit  
move\_robot

명령형은 Event Type이 아니라 Action Type에서 사용한다.

---

# **6\. Classification Model**

기존 문서에서는 분류 축이 너무 많이 나열되어 있었다.

최종 구조에서는 분류 축을 4개 그룹으로 묶는다.

---

## **6.1 Semantic Classification**

이 event가 무엇을 의미하는지 정의한다.

필드:

event\_type  
event\_category  
domain\_module  
subject\_type  
source\_type  
severity  
evidence\_eligibility

예:

event\_type \= safety.gas.critical\_threshold\_exceeded  
domain\_module \= safety  
subject\_type \= Sensor  
severity \= CRITICAL\_EMERGENCY  
evidence\_eligibility \= EVIDENCE\_REQUIRED

---

## **6.2 Routing Classification**

이 event가 어디로 흘러가야 하는지 정의한다.

필드:

default\_lifecycle\_path  
actionability  
can\_generate\_candidate  
can\_trigger\_emergency  
requires\_audit

예:

default\_lifecycle\_path \= EMERGENCY\_FAST\_PATH  
actionability \= REQUIRES\_EMERGENCY\_ACTION  
can\_trigger\_emergency \= true  
requires\_audit \= true

---

## **6.3 Data Handling Classification**

이 event의 저장 경로와 처리 방식을 정의한다.

필드:

is\_stream\_data  
storage\_route  
supports\_batching  
supports\_windowing  
ontology\_bus\_entry\_policy

예:

event\_type \= robot.pose.updated  
is\_stream\_data \= true  
storage\_route \= TIME\_SERIES\_DB  
ontology\_bus\_entry\_policy \= ON\_ANOMALY

---

## **6.4 Ontology Mapping Classification**

이 event가 ontology에 어떤 영향을 주는지 정의한다.

필드:

requires\_ontology\_binding  
ontology\_mapping\_effect  
mapped\_ontology\_property  
requires\_subject\_binding  
requires\_object\_binding

예:

event\_type \= construction.worker.entered\_zone  
ontology\_mapping\_effect \= UPDATES\_OBJECT\_PROPERTY  
mapped\_ontology\_property \= hasLocation

---

# **7\. 핵심 분류 값**

## **7.1 Lifecycle Path**

Lifecycle Path는 event가 어떤 처리 경로를 타는지를 의미한다.

값:

STANDARD  
EMERGENCY\_FAST\_PATH  
MONITORING\_ONLY  
GOVERNANCE\_REVIEW  
AUDIT\_ONLY

역할:

처리 workflow를 결정한다.

---

## **7.2 Actionability**

Actionability는 event가 action 후보를 만들 수 있는지를 의미한다.

값:

NO\_ACTION  
MAY\_GENERATE\_CANDIDATE  
REQUIRES\_CANDIDATE  
REQUIRES\_EMERGENCY\_ACTION  
AUDIT\_ONLY

역할:

ActionCandidate 생성 가능성을 결정한다.

---

## **7.3 Storage Route**

Storage Route는 event가 기본적으로 저장되는 위치를 의미한다.

값:

TIME\_SERIES\_DB  
EVENT\_STORE  
KNOWLEDGE\_GRAPH  
AUDIT\_STORE  
OBSERVABILITY\_STORE

역할:

데이터 저장 경로를 결정한다.

예:

robot.pose.updated  
→ TIME\_SERIES\_DB

construction.permit.expired  
→ EVENT\_STORE \+ KNOWLEDGE\_GRAPH \+ AUDIT\_STORE

---

## **7.4 Ontology Bus Entry Policy**

Ontology Bus Entry Policy는 event가 ontology bus에 들어가는 조건을 의미한다.

값:

ALWAYS  
ON\_THRESHOLD  
ON\_ANOMALY  
ON\_STATE\_CHANGE  
ON\_ESCALATION  
NEVER

역할:

모든 event가 ontology bus를 타지 않도록 제어한다.

예:

industrial.sensor.reading\_received  
→ ON\_THRESHOLD

robot.mission.blocked  
→ ALWAYS

---

## **7.5 Ontology Mapping Effect**

Ontology Mapping Effect는 event가 ontology individual, ObjectProperty, DataProperty에 어떤 영향을 주는지 의미한다.

값:

NO\_ONTOLOGY\_EFFECT  
UPDATES\_DATA\_PROPERTY  
UPDATES\_OBJECT\_PROPERTY  
CREATES\_RELATION  
REMOVES\_RELATION  
CREATES\_INDIVIDUAL  
UPDATES\_INDIVIDUAL\_STATE  
TRIGGERS\_MAPPING\_REVIEW

예:

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

Event Type은 ontology class와 반드시 1:1일 필요는 없다.

하지만 WorldStateUpdateDTO 또는 OntologyBoundEventDTO로 갈 때는 어떤 ontology element가 변하는지 명확해야 한다.

따라서 Event Type Registry는 Event-to-Ontology Mapping Table을 가져야 한다.

## **8.1 Mapping Table 필드**

권장 필드:

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

## **8.2 ObjectProperty 변경 예**

Event Type:

construction.worker.entered\_zone

Ontology Effect:

Worker individual과 Zone individual 사이의 hasLocation 관계 생성 또는 갱신

Mapping:

subject\_type \= Worker  
object\_type \= Zone  
ontology\_property \= hasLocation  
ontology\_mapping\_effect \= UPDATES\_OBJECT\_PROPERTY

---

## **8.3 DataProperty 변경 예**

Event Type:

industrial.sensor.reading\_changed

Ontology Effect:

Sensor individual의 hasCurrentValue 값 업데이트

Mapping:

subject\_type \= Sensor  
ontology\_property \= hasCurrentValue  
ontology\_mapping\_effect \= UPDATES\_DATA\_PROPERTY

---

## **8.4 Individual State 변경 예**

Event Type:

robot.mission.blocked

Ontology Effect:

Mission individual의 hasMissionStatus 값을 Blocked로 변경

Mapping:

subject\_type \= Mission  
ontology\_property \= hasMissionStatus  
ontology\_mapping\_effect \= UPDATES\_INDIVIDUAL\_STATE

---

# **9\. Vendor Extension Pattern**

## **9.1 문제**

건설 현장과 로봇 플릿에는 다양한 외부 장비가 들어온다.

예:

Boston Dynamics Spot  
Doosan Robotics Cobot  
Siemens PLC  
Mitsubishi PLC  
Honeywell Sensor  
vendor-specific fleet manager

이 장비들이 내보내는 모든 error code와 event를 core registry에 직접 등록하는 것은 불가능하다.

---

## **9.2 해결 원칙**

Core registry는 vendor-specific event를 wildcard pattern으로 수용한다.

예:

robot.fleet.\*  
industrial.plc.\*  
industrial.sensor.\*  
robot.arm.\*

Vendor-specific payload 해석은 adapter layer가 담당한다.

즉:

Core Registry  
→ 공통 event contract, lifecycle rule, safety rule 관리

Vendor Adapter  
→ vendor error code, proprietary payload, vendor-specific event 해석

---

## **9.3 Vendor Event 예**

robot.fleet.boston\_dynamics.spot.payload\_detached  
robot.fleet.boston\_dynamics.spot.estop\_triggered  
industrial.plc.siemens.s7.connection\_lost  
industrial.plc.mitsubishi.fx.critical\_alarm\_raised  
robot.arm.doosan.cobot.safety\_stop\_triggered

---

# **10\. Event Type Registry 운영 정책**

기존 문서에서 가장 부족했던 부분은 registry 운영 방식이었다.

Event Type Taxonomy는 단순 목록이 아니라 registry로 운영되어야 한다.

---

## **10.1 EventTypeSpecDTO 필드**

권장 필드:

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

Event Type은 다음 status를 가질 수 있다.

DRAFT  
ACTIVE  
DEPRECATED  
RETIRED  
BLOCKED

의미:

DRAFT  
→ 검토 중

ACTIVE  
→ 사용 가능

DEPRECATED  
→ 더 이상 권장하지 않지만 하위 호환을 위해 유지

RETIRED  
→ 신규 event 수신 금지

BLOCKED  
→ 보안 또는 안전 문제로 차단

---

## **10.3 Registry Versioning**

Event Type은 version을 가져야 한다.

Backward-compatible change:

optional metadata 추가  
allowed source 추가  
monitoring metric 추가  
storage route 보강  
description 추가  
validator 강화

Breaking change:

event\_type 이름 변경  
severity 의미 변경  
lifecycle path 변경  
storage route 변경  
ontology mapping effect 변경  
audit requirement 제거  
emergency trigger 의미 변경

Breaking change는 새 event\_type으로 분리하는 것이 원칙이다.

---

## **10.4 Approval Process**

Event Type 변경은 owner와 domain steward의 승인을 받아야 한다.

권장 승인 주체:

Domain Owner  
Ontology Steward  
Safety Owner  
Policy Owner  
Platform Architect  
Vendor Adapter Owner

고위험 event는 Safety Owner와 Policy Owner 승인이 필수다.

---

## **10.5 Deprecation Policy**

Event Type을 바로 삭제하지 않는다.

권장 절차:

1. DEPRECATED 상태로 변경  
2. replacement\_event\_type 지정  
3. dual-read / dual-write 기간 운영  
4. downstream consumer migration  
5. audit compatibility 확인  
6. RETIRED 상태로 변경  
7. major version에서 제거 가능

---

## **10.6 Registry Compatibility Rule**

과거 event record는 항상 재해석 가능해야 한다.

따라서 EventTypeSpecDTO는 생성 당시 version과 status를 보존해야 한다.

AuditRecord는 event\_type뿐 아니라 event\_type\_version도 참조해야 한다.

---

# **11\. Post-hoc Audit Event Lifecycle**

Emergency Fast-Path를 사용한 event와 action은 반드시 사후 감사 lifecycle을 가져야 한다.

## **11.1 기본 흐름**

action.emergency\_approved.created  
→ action.emergency\_approved.post\_audit\_required  
→ audit.emergency.post\_audit\_pending  
→ audit.emergency.post\_audit\_completed

## **11.2 문제 발생 시 흐름**

audit.emergency.post\_audit\_pending  
→ audit.emergency.post\_audit\_escalated

또는:

audit.emergency.post\_audit\_completed  
→ governance.policy.updated

또는:

audit.emergency.post\_audit\_completed  
→ governance.emergency\_action.deprecated

## **11.3 원칙**

Emergency Fast-Path는 빠르기 때문에 사후 감사가 더 강해야 한다.

비상 action이 실제 현장에서 어떻게 종료되었는지 인간 관리자가 확인해야 한다.

사후 감사가 닫히지 않은 Emergency event는 lifecycle이 완전히 종료된 것으로 보지 않는다.

---

# **12\. MVP Event Type Set**

전체 event 목록은 부록으로 관리한다.

MVP에서는 다음 event type만 우선 등록한다.

## **12.1 Industrial MVP Events**

industrial.sensor.reading\_received  
industrial.sensor.threshold\_crossed  
industrial.sensor.offline\_detected  
industrial.plc.alarm\_raised  
industrial.equipment.mode\_changed

## **12.2 Construction MVP Events**

construction.worker.entered\_zone  
construction.worker.exited\_zone  
construction.permit.expired  
construction.task.status\_changed  
construction.inspection.failed

## **12.3 Safety MVP Events**

safety.zone.risk\_level\_changed  
safety.worker.entered\_danger\_zone  
safety.gas.critical\_threshold\_exceeded  
safety.emergency.fast\_path\_triggered

## **12.4 Robot MVP Events**

robot.telemetry.received  
robot.pose.updated  
robot.mission.assigned  
robot.mission.blocked  
robot.mission.completed  
robot.battery.critical

## **12.5 Lifecycle MVP Events**

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

# **13\. Appendix A: Event Type Catalog 분리 기준**

Event Category별 상세 목록은 본문에 모두 넣지 않는다.

다음 항목은 Appendix A에서 관리한다.

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

이렇게 해야 Core 문서가 길어지지 않는다.

---

# **14\. 권장 파일 구조**

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

# **15\. 우선 구현 순서**

MVP 구현 순서는 다음이 좋다.

1. EventCategory enum  
2. DomainModule enum  
3. LifecyclePath enum  
4. SeverityLevel enum  
5. Actionability enum  
6. EvidenceEligibility enum  
7. StreamClassification enum  
8. StorageRoute enum  
9. OntologyBusEntryPolicy enum  
10. OntologyMappingEffect enum  
11. EventTypeSpecDTO  
12. EventTypeRegistry  
13. Registry status enum  
14. Vendor wildcard pattern validator  
15. Event-to-Ontology Mapping Table  
16. MVP event type constants  
17. EventType validation function  
18. CanonicalEventEnvelopeDTO와 연결  
19. PathClassificationDTO와 연결

---

# **16\. 최종 원칙**

Event Type Taxonomy는 플랫폼의 사건 언어다.

DTO가 데이터의 그릇이라면, Event Type은 그 그릇 안에 들어가는 사건의 이름이다.

Ontology가 의미의 뼈대라면, Event Type은 시스템이 현실 변화를 감지하는 표준 감각 체계다.

하지만 모든 감각 신호가 곧바로 지식 그래프를 바꾸는 것은 아니다.

고주기 stream data는 시계열 경로를 탄다.  
의미 있는 변화만 ontology bus로 승격된다.  
Discrete event는 semantic pipeline으로 들어간다.  
Vendor-specific event는 adapter layer에서 해석한다.  
Core registry는 wildcard pattern으로 통제한다.  
Emergency event는 post-hoc audit lifecycle을 반드시 가진다.  
Event Type은 ontology property 변경의 trigger가 될 수 있다.

최종 원칙은 다음과 같다.

Different sources, one event language.  
Different signals, one taxonomy.  
Different frequencies, one routing policy.  
Different domains, one event registry.  
Different vendors, one extension pattern.  
Different risks, one lifecycle classification.  
Different events, one semantic backbone.

