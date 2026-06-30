# **Ontology-Centric State Model Registry**

---

# **1\. Purpose**

This document defines the core rules of the State Model Registry used in an ontology-centric cyber-physical platform.

The State Model Registry is a structure for registering and managing standard state values, state transition rules, state ownership, state synchronization criteria, reconciliation checks, and fail-safe transition rules used within the platform.

If an Event Type expresses “what happened,” and an Action Type expresses “what response can be taken,” then a State Model expresses “what is currently in what state.”

This document is not a catalog that lists every state value in detail.

This document focuses on the following:

Define what a State Model is.  
Distinguish State from Event, Action, and Feedback.  
Distinguish Discrete Semantic State from Continuous Streaming State.  
Define current\_state, expected\_state, pending\_state, confirmed\_state, and reconciled\_state.  
Define valid state transitions.  
Define synchronization criteria between World State and Knowledge Graph state.  
Define external system feedback and reconciliation rules.  
Define state ownership and authority arbitration rules.  
Define pending\_state timeout, fallback, and recovery rules.  
Define the temporal grace period between runtime world state and ontology inferred state.  
Define deterministic fail-safe transition rules when reconciliation fails.  
Define the operating policy of the State Model Registry.

The full list of state values is managed in a separate document: Appendix C: State Model Catalog.

---

# **2\. Document Separation Principle**

In the previous version, the Core State Model and the State Catalog were mixed into one document.

This approach is useful during the design draft phase, but as a practical implementation document, it becomes too long and repetitive.

Therefore, the State Model Registry is divided into the following two documents.

## **2.1 Core State Model Specification**

This is the present document.

It covers:

State Model definition  
Distinction between State and Event / Action / Feedback  
State type classification  
State lifecycle management  
State transition rules  
World State synchronization  
Reconciliation rules  
Fail-safe rules  
Ownership and authority arbitration  
Registry governance  
MVP state model set  
Core scenario flows

## **2.2 Appendix C: State Model Catalog**

This is a separate appendix document.

It covers:

worker state list  
zone state list  
permit state list  
task state list  
equipment state list  
sensor state list  
robot state list  
mission state list  
approval state list  
execution state list  
feedback state list  
emergency state list  
audit state list  
reconciliation state list

By separating the documents this way, the core document can remain short and stable, while the state catalog can continue to expand according to field requirements and domain expansion.

---

# **3\. Philosophy and Core Distinctions of the State Model**

## **3.1 Definition of State Model**

A State Model is a standard model that defines the state values a specific entity can have and the rules for state transitions.

A State Model must answer the following questions:

Which entity does this state belong to?  
What state values are allowed?  
Is this state a discrete semantic state or a continuous streaming state?  
What are the initial state and terminal state?  
Which state transitions are allowed?  
Which event triggers a state transition?  
Which action requests an expected state mutation?  
Which feedback creates a confirmed state?  
What is the source of truth for this state?  
Which authority can preempt state ownership during an emergency?  
When does the state become stale?  
If pending\_state times out, where does it fall back to?  
If reconciliation failure occurs, which fail-safe state should it transition to?

---

## **3.2 Distinction Between State and Event**

An Event is something that happened.

A State is the current condition an entity has after that event.

Example:

Event Type: robot.mission.blocked  
State: MissionStatus.BLOCKED

An Event can trigger a state transition.  
However, the Event itself is not the State.

---

## **3.3 Distinction Between State and Action**

An Action is a measure that requests a state change.

A State is the result, or the expected result, after that action.

Example:

Action Type: ACTION\_DISABLE\_ROBOT\_MISSION  
Expected State: MissionStatus.DISABLED

An Action is a request.  
A State is the result or expected result.

---

## **3.4 Distinction Between State and Feedback**

Feedback is the execution result returned from an external system or a human.

State is the value the platform confirms or updates after interpreting that feedback.

Example:

Feedback: FleetManager reports mission disabled.  
Confirmed State: MissionStatus.DISABLED

Feedback is evidence.  
State is the current understanding reflected from that evidence.

---

## **3.5 Distinction Between World State and Ontology State**

World State is the current operational state used at runtime.

Ontology State is the semantic state reflected in the Knowledge Graph or semantic layer.

Example:

World State:  
Robot\_07 current battery \= 18%

Ontology State:  
Robot\_07 hasBatteryRiskLevel LOW\_BATTERY

World State changes quickly.  
Ontology State is semantically refined.

Not every World State change directly modifies the Knowledge Graph.

---

# **4\. State Type Classification**

State Models are broadly divided into two types.

DISCRETE\_SEMANTIC\_STATE  
CONTINUOUS\_STREAMING\_STATE

---

## **4.1 Discrete Semantic State**

A Discrete Semantic State is a meaningful state change.

Examples:

MissionStatus.BLOCKED  
PermitStatus.EXPIRED  
ZoneAccessState.LOCKED  
EmergencyState.ACTIVE  
ExecutionState.FAILED  
ApprovalStatus.APPROVED

Processing flow:

Event / Action / Feedback  
→ State Transition  
→ World State Update  
→ Ontology Mapping  
→ Reconciliation  
→ Audit if needed

A Discrete Semantic State can be directly connected to the ontology bus, policy engine, audit, and decision routing.

---

## **4.2 Continuous Streaming State**

A Continuous Streaming State is high-frequency, repeated, continuous state data.

Examples:

RobotPoseState  
GasSensorValueState  
WorkerLocationState  
EquipmentTelemetryState  
BatteryPercentageState  
TemperatureSensorValueState

Processing flow:

Stream Input  
→ Edge Window Buffer  
→ Time-Series DB  
→ Aggregation / Threshold / Anomaly Detection  
→ Semantic Event Promotion only when meaningful

A Continuous Streaming State does not directly call the Knowledge Graph or ontology reasoner every time.

It is promoted to a semantic event only when a threshold crossing, anomaly detection, state change, or escalation condition occurs.

Example:

GasSensorValueState normal range  
→ Time-Series DB only

GasSensorValueState exceeds critical threshold  
→ safety.gas.critical\_threshold\_exceeded  
→ Discrete Semantic State transition

---

# **5\. State Naming Convention**

## **5.1 State Model Name**

State Models use PascalCase.

Format:

EntityStateName

Examples:

MissionStatus  
ZoneAccessState  
PermitStatus  
TaskStatus  
ExecutionState  
ApprovalStatus  
EquipmentOperationalState  
SensorHealthState  
RobotConnectivityState  
ReconciliationStatus

---

## **5.2 State Value Name**

State Values use uppercase snake\_case.

Examples:

IN\_PROGRESS  
BLOCKED  
COMPLETED  
FAILED  
LOCKED  
EXPIRED  
REVOKED  
LOW\_BATTERY  
DISCONNECTED  
PENDING\_RECONCILIATION  
FAIL\_SAFE\_TRIGGERED

---

# **6\. State Modeling Rules**

The State Model Registry must maintain the following information for each state model.

## **6.1 Semantic Classification**

Defines what the state means.

Fields:

state\_model  
state\_category  
state\_kind  
domain\_module  
entity\_type  
ontology\_class  
description

Example:

state\_model \= MissionStatus  
state\_kind \= DISCRETE\_SEMANTIC\_STATE  
domain\_module \= robot  
entity\_type \= Mission  
ontology\_class \= robot:Mission

---

## **6.2 Lifecycle Classification**

Defines what the state means within the lifecycle.

Fields:

initial\_states  
intermediate\_states  
terminal\_states  
failure\_states  
recovery\_states  
unknown\_state  
stale\_state  
fail\_safe\_state

Example:

MissionStatus.initial\_states \= ASSIGNED  
MissionStatus.intermediate\_states \= ACCEPTED, IN\_PROGRESS, BLOCKED, DISABLE\_REQUESTED  
MissionStatus.terminal\_states \= COMPLETED, CANCELLED, DISABLED  
MissionStatus.failure\_states \= FAILED, TIMEOUT  
MissionStatus.recovery\_states \= RECOVERY\_REQUIRED  
MissionStatus.unknown\_state \= UNKNOWN  
MissionStatus.fail\_safe\_state \= DISABLED or EMERGENCY\_STOPPED

---

## **6.3 Transition Classification**

Defines which state transitions are allowed.

Fields:

from\_state  
to\_state  
allowed\_event\_types  
allowed\_action\_types  
required\_feedback\_types  
requires\_policy\_check  
requires\_safety\_gate  
requires\_audit  
timeout\_policy  
auto\_fallback\_state

Example:

from\_state \= IN\_PROGRESS  
to\_state \= BLOCKED  
allowed\_event\_types \= robot.mission.blocked

from\_state \= DISABLE\_REQUESTED  
to\_state \= DISABLED  
allowed\_action\_types \= ACTION\_DISABLE\_ROBOT\_MISSION  
required\_feedback\_types \= feedback.completed  
timeout\_policy \= 5 seconds  
auto\_fallback\_state \= UNKNOWN

---

## **6.4 Stream Processing Classification**

Defines how Continuous Streaming State is processed.

Fields:

stream\_processing\_policy  
window\_size  
sampling\_rate  
aggregation\_policy  
promotion\_event\_types  
ontology\_update\_policy

Example:

state\_model \= GasSensorValueState  
state\_kind \= CONTINUOUS\_STREAMING\_STATE  
window\_size \= 5 seconds  
sampling\_rate \= 1 second  
aggregation\_policy \= MAX / AVG / THRESHOLD  
ontology\_update\_policy \= ON\_THRESHOLD  
promotion\_event\_types \= safety.gas.critical\_threshold\_exceeded

---

# **7\. State Lifecycle Management**

The state lifecycle is managed around the following five concepts.

current\_state  
expected\_state  
pending\_state  
confirmed\_state  
reconciled\_state

---

## **7.1 current\_state**

`current_state` is the state currently known by the platform.

Example:

Mission\_991.current\_state \= MissionStatus.IN\_PROGRESS

---

## **7.2 expected\_state**

`expected_state` is the state expected based on a specific event, action, or policy judgment.

Example:

ACTION\_DISABLE\_ROBOT\_MISSION  
→ expected\_state \= MissionStatus.DISABLED

---

## **7.3 pending\_state**

`pending_state` is a temporary state while waiting for feedback after an action request.

Example:

Mission\_991.pending\_state \= MissionStatus.DISABLE\_REQUESTED

Principles:

pending\_state is not confirmed state.  
pending\_state must not be treated as actual completion.  
Every pending\_state must have a timeout\_policy.  
pending\_state without timeout is prohibited.

---

## **7.4 confirmed\_state**

`confirmed_state` is a state confirmed by feedback or human confirmation.

Example:

FleetManager feedback: mission disabled  
→ confirmed\_state \= MissionStatus.DISABLED

---

## **7.5 inferred\_state**

`inferred_state` is a state derived by an ontology reasoner, rule engine, or semantic inference.

Example:

Robot\_07 battery \= 18%  
→ inferred\_state \= BatteryRiskLevel.LOW\_BATTERY

inferred\_state is useful, but it may arrive later than runtime world state.

Therefore, if inferred\_state and current\_state temporarily differ, it must not be treated immediately as a conflict.

---

## **7.6 reconciled\_state**

`reconciled_state` is the final synchronized state after feedback, world state, ontology state, and inferred state have passed consistency checks.

Example:

confirmed\_state \= MissionStatus.DISABLED  
ontology\_state \= MissionStatus.DISABLED  
world\_state \= MissionStatus.DISABLED  
→ reconciled\_state \= MissionStatus.DISABLED

---

# **8\. State Transition Rule**

State transitions must not occur arbitrarily.

The State Model Registry must register only allowed state transitions.

## **8.1 StateTransitionSpecDTO Fields**

Recommended fields:

state\_model  
from\_state  
to\_state  
transition\_type  
trigger\_event\_types  
trigger\_action\_types  
required\_feedback\_types  
required\_evidence\_types  
required\_policy\_refs  
requires\_safety\_gate  
requires\_human\_approval  
requires\_audit  
timeout\_policy  
timeout\_duration  
auto\_fallback\_state  
timeout\_transition\_type  
timeout\_recovery\_action\_types  
temporal\_grace\_period  
reconciliation\_wait\_policy  
valid\_from  
valid\_until  
version

---

## **8.2 Transition Type**

Values:

EVENT\_DRIVEN  
ACTION\_REQUESTED  
FEEDBACK\_CONFIRMED  
POLICY\_DRIVEN  
SYSTEM\_TIMEOUT  
MANUAL\_OVERRIDE  
RECOVERY\_DRIVEN  
FAIL\_SAFE\_TRIGGERED

Meaning:

`EVENT_DRIVEN`  
A state transition caused by an event.

`ACTION_REQUESTED`  
An expected or pending state transition caused by an action request.

`FEEDBACK_CONFIRMED`  
A confirmed state transition caused by feedback confirmation.

`POLICY_DRIVEN`  
A state transition caused by policy judgment.

`SYSTEM_TIMEOUT`  
A state transition caused by response delay or timeout.

`MANUAL_OVERRIDE`  
A state transition caused by human manual intervention.

`RECOVERY_DRIVEN`  
A state transition caused by a recovery procedure.

`FAIL_SAFE_TRIGGERED`  
A fail-safe transition caused by safety-critical conflict or reconciliation failure.

---

# **9\. Timeout, Reconciliation, and Fail-Safe Rules**

In the previous document, timeout, reconciliation, and fail-safe were repeated across multiple sections.

In the final document, these are integrated into one lifecycle safety rule.

---

## **9.1 Pending State Timeout Rule**

pending\_state must have a timeout\_policy.

Core principles:

Every pending\_state must have timeout\_duration.  
pending\_state without timeout is prohibited.  
After timeout, it transitions to auto\_fallback\_state.  
High-risk states must connect to recovery or fail-safe after timeout.

Example:

from\_state \= DISABLE\_REQUESTED  
expected\_state \= DISABLED  
timeout\_duration \= 5 seconds  
auto\_fallback\_state \= UNKNOWN  
timeout\_transition\_type \= SYSTEM\_TIMEOUT  
timeout\_recovery\_action\_types \= \[  
  ACTION\_NOTIFY\_OPERATOR,  
  ACTION\_REQUEST\_MANUAL\_OVERRIDE,  
  ACTION\_RETURN\_ROBOT\_TO\_SAFE\_ZONE  
\]

---

## **9.2 Reconciliation Rule**

Reconciliation is the process of checking whether expected state, feedback state, world state, ontology state, and inferred state are consistent with one another.

Success example:

expected\_state \= MissionStatus.DISABLED  
feedback\_state \= MissionStatus.DISABLED  
world\_state \= MissionStatus.DISABLED  
ontology\_state \= MissionStatus.DISABLED

reconciliation\_status \= SUCCESS  
reconciled\_state \= MissionStatus.DISABLED

Failure example:

expected\_state \= MissionStatus.DISABLED  
feedback\_state \= MissionStatus.STILL\_ACTIVE  
world\_state \= MissionStatus.IN\_PROGRESS  
ontology\_state \= MissionStatus.DISABLE\_REQUESTED

reconciliation\_status \= FAILED  
state\_conflict\_detected \= true  
recovery\_required \= true  
manual\_review\_required \= true

Follow-up actions:

Create recovery action  
Notify supervisor  
Request manual override  
Update audit record  
Review policy if repeated  
Review ontology mapping if semantic mismatch is suspected  
Evaluate fail-safe if safety-critical

---

## **9.3 Temporal Grace Period Rule**

There may be a time lag between ontology inferred state and runtime world state.

If this time lag is treated immediately as a conflict, false positives can explode.

Therefore, a temporal grace period is applied.

Additional fields:

temporal\_grace\_period  
settling\_time  
inference\_lag\_tolerance  
reconciliation\_wait\_policy

Processing example:

runtime world state:  
Robot\_07 battery \= 18%

ontology inferred state:  
Robot\_07 hasBatteryRiskLevel NORMAL

This is not immediately treated as a conflict.

First:

reconciliation\_status \= IN\_TRANSIT  
reason \= ontology inference pending  
grace\_period \= 3 seconds

If the mismatch still remains after 3 seconds:

reconciliation\_status \= CONFLICT  
manual\_review\_required \= true

Principles:

An ontology mismatch immediately after a runtime state change is not an immediate conflict.  
Within the grace period, it is handled as IN\_TRANSIT or PENDING\_RECONCILIATION.  
If the mismatch remains after the grace period, it is promoted to CONFLICT.

---

## **9.4 Fail-Safe Interception Rule**

For safety-critical entities, simple notification is not enough when reconciliation failure occurs.

State inconsistency means that the world perceived by the platform may differ from the actual physical world.

Therefore, a safety-critical state model must have a deterministic fail-safe state.

Basic flow:

Reconciliation FAILED  
→ Safety Interceptor triggered  
→ Pre-approved Emergency Action selected  
→ EmergencyApprovedAction created  
→ EmergencyExecutionRequest sent  
→ External Safety / Control System executes  
→ Feedback received  
→ Post-hoc Audit

Important architectural boundary:

Ontology Platform  
→ fail-safe judgment and emergency request generation

External Control System  
→ actual physical control execution

In other words, the State Model Registry defines the fail-safe judgment and request boundary.  
Actual physical control is performed by PLC, robot middleware, fleet manager, SCADA, or access control system.

---

# **10\. Ownership and Authority Arbitration**

Every state must have an owner.

The state owner defines the authoritative source and update authority for that state.

However, in a CPS environment, safety authority may need to override the existing source of truth during emergencies.

---

## **10.1 Source of Truth Examples**

RobotPoseState  
→ primary\_source\_of\_truth \= RobotTelemetrySystem

MissionStatus  
→ primary\_source\_of\_truth \= FleetManager

ZoneAccessState  
→ primary\_source\_of\_truth \= AccessControlSystem

PermitStatus  
→ primary\_source\_of\_truth \= PermitManagementSystem

ExecutionState  
→ primary\_source\_of\_truth \= PlatformExecutionCore

ApprovalStatus  
→ primary\_source\_of\_truth \= ApprovalService

AuditStatus  
→ primary\_source\_of\_truth \= AuditService

---

## **10.2 Preemptive Authority Example**

ZoneAccessState.primary\_source\_of\_truth \= AccessControlSystem  
ZoneAccessState.preemptive\_authorities \= EmergencyPolicyEngine, SafetyManagementSystem

Emergency situation:

gas leak detected  
→ SafetyManagementSystem preempts ZoneAccessState  
→ ZoneAccessState \= EVACUATION\_REQUESTED or RESTRICTED

---

## **10.3 Authority Rule**

Under normal conditions, the primary\_source\_of\_truth updates confirmed\_state.

Systems that are not the primary\_source\_of\_truth cannot directly update confirmed\_state under normal conditions.

However, they may do the following:

Create pending\_state  
Record expected\_state  
Create conflict flag  
Create review request  
Create reconciliation request

In an emergency, a preemptive\_authority may force a transition to confirmed\_state or fail\_safe\_state.

In this case, audit is mandatory.

---

# **11\. State Freshness Rule**

State can become stale over time.

Freshness management is especially important for sensors, robot pose, worker location, and equipment telemetry.

Freshness TTL examples:

RobotPoseState → 2 seconds  
WorkerLocationState → 5 seconds  
GasSensorValueState → 1 second  
EquipmentOperationalState → 10 seconds  
PermitStatus → 1 hour  
TaskStatus → 5 minutes  
ExecutionState → lifecycle controlled  
ApprovalStatus → lifecycle controlled

If a state becomes stale, it is handled as one of the following:

STALE  
UNKNOWN  
REVALIDATION\_REQUIRED  
MANUAL\_CONFIRMATION\_REQUIRED

High-risk actions must not be approved based on stale state.

---

# **12\. StateModelSpecDTO**

The State Model Registry must be managed through StateModelSpecDTO.

## **12.1 StateModelSpecDTO Fields**

Recommended fields:

state\_model  
state\_category  
state\_kind  
domain\_module  
entity\_type  
ontology\_class

allowed\_state\_values  
initial\_states  
intermediate\_states  
terminal\_states  
failure\_states  
recovery\_states  
unknown\_state  
stale\_state

primary\_source\_of\_truth  
authoritative\_source  
fallback\_source  
update\_authority  
preemptive\_authorities  
authority\_priority\_level  
preemption\_conditions  
preemption\_audit\_required

freshness\_ttl  
confidence\_required  
evidence\_required  
requires\_audit

stream\_processing\_policy  
window\_size  
sampling\_rate  
aggregation\_policy  
promotion\_event\_types  
ontology\_update\_policy

temporal\_grace\_period  
settling\_time  
inference\_lag\_tolerance

deterministic\_fail\_safe\_state  
fail\_safe\_trigger\_conditions  
fail\_safe\_action\_types  
fail\_safe\_authority  
fail\_safe\_audit\_required

owner  
version  
status  
valid\_from  
valid\_until  
deprecated\_at  
replacement\_state\_model  
change\_reason

---

# **13\. StateTransitionSpecDTO**

State transitions are managed through StateTransitionSpecDTO.

## **13.1 StateTransitionSpecDTO Fields**

Recommended fields:

state\_model  
from\_state  
to\_state  
transition\_type  
trigger\_event\_types  
trigger\_action\_types  
required\_feedback\_types  
required\_evidence\_types  
required\_policy\_refs  
requires\_safety\_gate  
requires\_human\_approval  
requires\_audit

timeout\_policy  
timeout\_duration  
auto\_fallback\_state  
timeout\_transition\_type  
timeout\_recovery\_action\_types

temporal\_grace\_period  
reconciliation\_wait\_policy

owner  
version  
status  
valid\_from  
valid\_until  
deprecated\_at  
change\_reason

---

# **14\. Registry Operating Policy**

The State Model Registry is not a simple enum list.

The State Model Registry is a governance-controlled registry that connects ontology, runtime world state, external system feedback, audit, and the fail-safe execution boundary.

---

## **14.1 Registry Status**

A State Model may have the following statuses:

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
→ New state usage is prohibited

BLOCKED  
→ Blocked due to safety, security, or legal issues

---

## **14.2 Versioning**

Backward-compatible changes:

Add a new state value  
Add optional metadata  
Enhance freshness\_ttl  
Add a transition rule  
Add fallback\_source  
Add preemptive\_authority  
Enhance temporal\_grace\_period  
Add description

Breaking changes:

Rename a state value  
Change the meaning of a terminal state  
Change the meaning of a failure state  
Remove a transition rule  
Change source\_of\_truth  
Change authority priority  
Change ontology\_class  
Change the meaning of freshness\_ttl  
Change the meaning of fail\_safe\_state

As a rule, breaking changes must be separated into a new state\_model version or a new state\_model.

---

## **14.3 Approval Process**

State Model changes must be approved by the owner and the domain steward.

High-risk state models require approval from the following authorities:

Ontology Steward  
Safety Owner  
Policy Owner  
Platform Architect  
Domain Owner  
External System Owner

---

## **14.4 Deprecation Policy**

A State Model should not be deleted immediately.

Recommended process:

Change status to DEPRECATED  
Specify replacement\_state\_model  
Operate a dual-read / dual-write period  
Migrate downstream consumers  
Verify audit compatibility  
Change status to RETIRED  
Remove in a major version if necessary

---

## **14.5 Compatibility Rule**

Past state records must always remain interpretable.

Therefore, WorldStateUpdateDTO, FeedbackEventDTO, and AuditRecordDTO must reference not only state\_model, but also state\_model\_version.

---

# **15\. Core Scenarios**

## **15.1 Scenario 1: ACTION\_DISABLE\_ROBOT\_MISSION**

Situation:

Robot\_07’s Mission\_991 is blocked, and timeout is approaching.

Flow:

Event:  
robot.mission.blocked

Current State:  
MissionStatus.BLOCKED

ActionCandidate:  
ACTION\_DISABLE\_ROBOT\_MISSION

ApprovedAction:  
ACTION\_DISABLE\_ROBOT\_MISSION approved for Mission\_991

Expected State:  
MissionStatus.DISABLED

Pending State:  
MissionStatus.DISABLE\_REQUESTED

ExecutionRequest:  
Send disable mission request to FleetManager

Feedback:  
FleetManager reports mission disabled

Confirmed State:  
MissionStatus.DISABLED

Reconciliation:  
World State, Feedback, and Ontology State match

Final State:  
MissionStatus.DISABLED

Failure flow:

Pending State:  
DISABLE\_REQUESTED

Timeout:  
5 seconds elapsed without feedback

Fallback:  
UNKNOWN

Recovery:  
ACTION\_NOTIFY\_OPERATOR  
ACTION\_REQUEST\_MANUAL\_OVERRIDE  
ACTION\_RETURN\_ROBOT\_TO\_SAFE\_ZONE

---

## **15.2 Scenario 2: Reconciliation Failure → Fail-Safe**

Situation:

The platform expects that the robot mission has been disabled, but feedback returns still active.

Flow:

Expected State:  
MissionStatus.DISABLED

Feedback State:  
MissionStatus.STILL\_ACTIVE

World State:  
MissionStatus.IN\_PROGRESS

Reconciliation:  
FAILED

Safety-Critical Check:  
true

Safety Interceptor:  
triggered

Fail-Safe State:  
RobotOperationalState.EMERGENCY\_STOPPED

Emergency Action:  
ACTION\_EMERGENCY\_STOP

Execution Boundary:  
EmergencyExecutionRequest sent to external robot control system

Post-hoc Audit:  
required

Principles:

The platform does not directly control the robot motor.  
The platform makes the fail-safe judgment and generates an emergency request.  
Actual physical control is performed by the external control system.

---

## **15.3 Scenario 3: GasSensorValueState Stream Promotion**

Situation:

GasSensor\_17 sends values every second.

Normal flow:

GasSensorValueState received  
→ Edge Window Buffer  
→ Time-Series DB  
→ Aggregation  
→ No semantic event

Threshold-exceeded flow:

GasSensorValueState exceeds critical threshold  
→ safety.gas.critical\_threshold\_exceeded  
→ ZoneRiskState.CRITICAL  
→ ActionCandidate:  
   ACTION\_EMERGENCY\_EVACUATE\_ZONE  
   ACTION\_EMERGENCY\_TRIGGER\_ALARM  
→ EmergencyApprovedAction  
→ EmergencyExecutionRequest  
→ Feedback  
→ Post-hoc Audit

Principles:

Gas sensor values arriving every second must not update the Knowledge Graph every time.  
Only meaningful changes are promoted to semantic events.

---

# **16\. MVP State Model Set**

For the MVP, the following state models should be registered first.

## **16.1 Robot / Mission**

RobotConnectivityState  
RobotBatteryRiskState  
RobotPoseState  
MissionStatus  
RobotOperationalState

## **16.2 Construction**

PermitStatus  
TaskStatus  
ZoneAccessState  
WorkerLocationState

## **16.3 Safety**

ZoneRiskState  
GasSensorRiskState  
EmergencyState  
EvacuationState

## **16.4 Industrial**

EquipmentOperationalState  
SensorHealthState  
PLCConnectionState  
AlarmState  
GasSensorValueState

## **16.5 Platform Lifecycle**

ApprovalStatus  
ExecutionState  
FeedbackStatus  
AuditStatus  
ReconciliationStatus

---

# **17\. Separation Criteria for Appendix C: State Model Catalog**

Detailed state value lists are not included in the main body.

The following items are managed in Appendix C:

robot state catalog  
mission state catalog  
construction state catalog  
safety state catalog  
industrial state catalog  
platform lifecycle state catalog  
execution state catalog  
feedback state catalog  
audit state catalog  
reconciliation state catalog

This prevents the Core document from becoming too long.

---

# **18\. Recommended File Structure**

## **18.1 Core State Registry**

state\_registry/  
  \_\_init\_\_.py  
  core.py  
  state\_model\_spec.py  
  transition\_spec.py  
  registry.py  
  classification.py  
  ownership.py  
  authority\_arbitration.py  
  freshness\_policy.py  
  stream\_state\_policy.py  
  reconciliation\_policy.py  
  temporal\_grace\_policy.py  
  fail\_safe\_policy.py  
  mutation\_policy.py

## **18.2 State Catalog**

state\_registry/catalog/  
  robot\_states.py  
  mission\_states.py  
  construction\_states.py  
  safety\_states.py  
  industrial\_states.py  
  platform\_lifecycle\_states.py

## **18.3 Mapping Tables**

state\_registry/mappings/  
  event\_to\_state\_transition.py  
  action\_to\_expected\_state.py  
  feedback\_to\_confirmed\_state.py  
  state\_to\_ontology\_property.py  
  state\_reconciliation\_rules.py  
  stream\_promotion\_rules.py  
  fail\_safe\_transition\_rules.py

---

# **19\. Recommended Implementation Order**

The MVP implementation order should be as follows.

StateCategory enum  
StateKind enum  
StateModelStatus enum  
TransitionType enum  
ReconciliationStatus enum  
AuthorityPriority enum  
StateModelSpecDTO  
StateTransitionSpecDTO  
StateRegistry  
StateTransitionRegistry  
MVP state value constants  
Event-to-State Transition Mapping  
Action-to-Expected-State Mapping  
Feedback-to-Confirmed-State Mapping  
State-to-Ontology Mapping  
Stream Promotion Rule  
Freshness Policy  
Temporal Grace Policy  
Authority Arbitration Policy  
Reconciliation Policy  
Fail-Safe Policy  
Connection to WorldStateUpdateDTO  
Connection to OntologyBoundEventDTO  
Connection to FeedbackEventDTO  
Connection to AuditRecordDTO

---

# **20\. Final Principle**

The State Model Registry is the state language of the platform.

Event Type describes the event.  
Action Type describes the response.  
State Model describes what is currently in what state.

State is not a simple enum.  
State is a meaningful current value of an entity, and it has transition rules, ownership, freshness, reconciliation, and fail-safe rules.

In CPS, an action request and an actual state change are different.  
Therefore, expected\_state, pending\_state, confirmed\_state, and reconciled\_state must be distinguished.

High-frequency stream state must not perform ontology mutation every time.  
Stream state must follow the edge buffer and time-series path, and only meaningful changes should be promoted to semantic events.

Systems that are not the source of truth must not directly update confirmed\_state under normal conditions.  
However, in emergency situations, a preemptive\_authority may force a state transition.

pending\_state must always have timeout and fallback.  
High-risk actions must not be approved based on stale state.  
A temporal grace period is required between runtime state and ontology inferred state.  
If reconciliation fails and safety-critical conditions are met, the fail-safe path must activate immediately.

The final principles are as follows:

Different entities, one state language.  
Different systems, one authority model.  
Different streams, one promotion policy.  
Different events, one transition discipline.  
Different actions, one expected mutation model.  
Different feedback delays, one reconciliation model.  
Different inference lags, one temporal grace policy.  
Different failures, one fail-safe discipline.  
Different states, one semantic backbone.

# **Ontology centric State Model Registry**

# **1\. 목적**

본 문서는 온톨로지 중심 사이버-물리 플랫폼에서 사용되는 State Model Registry의 핵심 규칙을 정의한다.

State Model Registry는 플랫폼 안에서 사용되는 표준 상태값, 상태 전이 규칙, 상태 소유권, 상태 동기화 기준, 정합성 검사, fail-safe 전이 규칙을 등록하고 관리하는 구조다.

Event Type이 “무슨 일이 발생했는가”를 표현하고, Action Type이 “어떤 대응을 할 수 있는가”를 표현한다면, State Model은 “현재 무엇이 어떤 상태인가”를 표현한다.

이 문서는 모든 상태값을 길게 나열하는 catalog 문서가 아니다.

본 문서는 다음에 집중한다.

State Model이 무엇인지 정의한다.  
State와 Event, Action, Feedback의 차이를 구분한다.  
Discrete Semantic State와 Continuous Streaming State를 구분한다.  
current\_state, expected\_state, pending\_state, confirmed\_state, reconciled\_state를 정의한다.  
합법적인 state transition을 정의한다.  
World State와 Knowledge Graph 상태 동기화 기준을 정의한다.  
External system feedback과 reconciliation 규칙을 정의한다.  
State ownership과 authority arbitration 규칙을 정의한다.  
pending\_state timeout, fallback, recovery 규칙을 정의한다.  
runtime world state와 ontology inferred state 사이의 temporal grace period를 정의한다.  
Reconciliation 실패 시 deterministic fail-safe 전이 규칙을 정의한다.  
State Model Registry 운영 정책을 정의한다.

전체 state value 목록은 별도 문서인 Appendix C: State Model Catalog에서 관리한다.

---

# **2\. 문서 분리 원칙**

기존 문서는 Core State Model과 State Catalog가 하나의 문서 안에 섞여 있었다.

이 방식은 설계 초안 단계에서는 유용하지만, 실무 구현 문서로는 너무 길고 반복이 많다.

따라서 State Model Registry는 다음 두 문서로 분리한다.

## **2.1 Core State Model Specification**

본 문서다.

다루는 내용:

State Model 정의  
State와 Event / Action / Feedback의 차이  
State 종류 구분  
State lifecycle management  
State transition rule  
World State synchronization  
Reconciliation rule  
Fail-safe rule  
Ownership and authority arbitration  
Registry governance  
MVP state model set  
핵심 시나리오 흐름

## **2.2 Appendix C: State Model Catalog**

별도 부록 문서다.

다루는 내용:

worker state list  
zone state list  
permit state list  
task state list  
equipment state list  
sensor state list  
robot state list  
mission state list  
approval state list  
execution state list  
feedback state list  
emergency state list  
audit state list  
reconciliation state list

이렇게 분리하면 core 문서는 짧고 안정적으로 유지되고, state catalog는 현장 요구와 도메인 확장에 따라 계속 확장할 수 있다.

---

# **3\. State Model의 철학과 핵심 구분**

## **3.1 State Model의 정의**

State Model은 특정 entity가 가질 수 있는 상태값과 상태 전이 규칙을 정의하는 표준 모델이다.

State Model은 다음 질문에 답해야 한다.

어떤 entity의 상태인가?  
허용되는 상태값은 무엇인가?  
이 state는 discrete semantic state인가, continuous streaming state인가?  
초기 상태와 최종 상태는 무엇인가?  
어떤 상태 전이가 허용되는가?  
어떤 event가 state transition을 유발하는가?  
어떤 action이 expected state mutation을 요청하는가?  
어떤 feedback이 confirmed state를 만드는가?  
상태의 source of truth는 무엇인가?  
비상시 어떤 authority가 상태 소유권을 preempt할 수 있는가?  
상태가 stale해지는 기준은 무엇인가?  
pending\_state가 timeout되면 어디로 fallback하는가?  
reconciliation failure가 발생하면 어떤 fail-safe state로 전이하는가?

---

## **3.2 State와 Event의 구분**

Event는 발생한 사건이다.

State는 그 사건 이후 entity가 가지는 현재 상태다.

예:

Event Type: robot.mission.blocked  
State: MissionStatus.BLOCKED

Event는 상태 전이를 유발할 수 있다.  
하지만 Event 자체가 State는 아니다.

---

## **3.3 State와 Action의 구분**

Action은 상태 변화를 요청하는 조치다.

State는 그 조치 이후 확인되거나 기대되는 상태다.

예:

Action Type: ACTION\_DISABLE\_ROBOT\_MISSION  
Expected State: MissionStatus.DISABLED

Action은 요청이다.  
State는 결과 또는 기대 결과다.

---

## **3.4 State와 Feedback의 구분**

Feedback은 외부 시스템이나 사람으로부터 돌아온 실행 결과다.

State는 feedback을 해석한 뒤 platform이 확정하거나 갱신하는 값이다.

예:

Feedback: FleetManager reports mission disabled.  
Confirmed State: MissionStatus.DISABLED

Feedback은 증거다.  
State는 그 증거를 반영한 현재 인식이다.

---

## **3.5 World State와 Ontology State의 구분**

World State는 runtime에서 사용되는 현재 operational state다.

Ontology State는 Knowledge Graph 또는 semantic layer에 반영되는 의미 상태다.

예:

World State:  
Robot\_07 current battery \= 18%

Ontology State:  
Robot\_07 hasBatteryRiskLevel LOW\_BATTERY

World State는 빠르게 변한다.  
Ontology State는 의미적으로 정제된 상태다.

모든 World State 변경이 Knowledge Graph를 직접 바꾸는 것은 아니다.

---

# **4\. State 종류 구분**

State Model은 크게 두 종류로 나눈다.

DISCRETE\_SEMANTIC\_STATE  
CONTINUOUS\_STREAMING\_STATE

---

## **4.1 Discrete Semantic State**

Discrete Semantic State는 의미 있는 상태 변화다.

예:

MissionStatus.BLOCKED  
PermitStatus.EXPIRED  
ZoneAccessState.LOCKED  
EmergencyState.ACTIVE  
ExecutionState.FAILED  
ApprovalStatus.APPROVED

처리 방식:

Event / Action / Feedback  
→ State Transition  
→ World State Update  
→ Ontology Mapping  
→ Reconciliation  
→ Audit if needed

Discrete Semantic State는 ontology bus, policy engine, audit, decision routing과 직접 연결될 수 있다.

---

## **4.2 Continuous Streaming State**

Continuous Streaming State는 고주기, 반복, 연속적인 상태 데이터다.

예:

RobotPoseState  
GasSensorValueState  
WorkerLocationState  
EquipmentTelemetryState  
BatteryPercentageState  
TemperatureSensorValueState

처리 방식:

Stream Input  
→ Edge Window Buffer  
→ Time-Series DB  
→ Aggregation / Threshold / Anomaly Detection  
→ Semantic Event Promotion only when meaningful

Continuous Streaming State는 매번 Knowledge Graph나 ontology reasoner를 직접 호출하지 않는다.

임계값 초과, 이상 탐지, 상태 변화, escalation 조건이 발생할 때만 semantic event로 승격된다.

예:

GasSensorValueState normal range  
→ Time-Series DB only

GasSensorValueState exceeds critical threshold  
→ safety.gas.critical\_threshold\_exceeded  
→ Discrete Semantic State transition

---

# **5\. State Naming Convention**

## **5.1 State Model 이름**

State Model은 PascalCase를 사용한다.

형식:

EntityStateName

예:

MissionStatus  
ZoneAccessState  
PermitStatus  
TaskStatus  
ExecutionState  
ApprovalStatus  
EquipmentOperationalState  
SensorHealthState  
RobotConnectivityState  
ReconciliationStatus

---

## **5.2 State Value 이름**

State Value는 대문자 snake\_case를 사용한다.

예:

IN\_PROGRESS  
BLOCKED  
COMPLETED  
FAILED  
LOCKED  
EXPIRED  
REVOKED  
LOW\_BATTERY  
DISCONNECTED  
PENDING\_RECONCILIATION  
FAIL\_SAFE\_TRIGGERED

---

# **6\. State Modeling Rules**

State Model Registry는 각 state model에 대해 다음 정보를 가져야 한다.

## **6.1 Semantic Classification**

이 state가 무엇을 의미하는지 정의한다.

필드:

state\_model  
state\_category  
state\_kind  
domain\_module  
entity\_type  
ontology\_class  
description

예:

state\_model \= MissionStatus  
state\_kind \= DISCRETE\_SEMANTIC\_STATE  
domain\_module \= robot  
entity\_type \= Mission  
ontology\_class \= robot:Mission

---

## **6.2 Lifecycle Classification**

이 state가 lifecycle에서 어떤 의미를 가지는지 정의한다.

필드:

initial\_states  
intermediate\_states  
terminal\_states  
failure\_states  
recovery\_states  
unknown\_state  
stale\_state  
fail\_safe\_state

예:

MissionStatus.initial\_states \= ASSIGNED  
MissionStatus.intermediate\_states \= ACCEPTED, IN\_PROGRESS, BLOCKED, DISABLE\_REQUESTED  
MissionStatus.terminal\_states \= COMPLETED, CANCELLED, DISABLED  
MissionStatus.failure\_states \= FAILED, TIMEOUT  
MissionStatus.recovery\_states \= RECOVERY\_REQUIRED  
MissionStatus.unknown\_state \= UNKNOWN  
MissionStatus.fail\_safe\_state \= DISABLED or EMERGENCY\_STOPPED

---

## **6.3 Transition Classification**

어떤 상태 전이가 허용되는지 정의한다.

필드:

from\_state  
to\_state  
allowed\_event\_types  
allowed\_action\_types  
required\_feedback\_types  
requires\_policy\_check  
requires\_safety\_gate  
requires\_audit  
timeout\_policy  
auto\_fallback\_state

예:

from\_state \= IN\_PROGRESS  
to\_state \= BLOCKED  
allowed\_event\_types \= robot.mission.blocked

from\_state \= DISABLE\_REQUESTED  
to\_state \= DISABLED  
allowed\_action\_types \= ACTION\_DISABLE\_ROBOT\_MISSION  
required\_feedback\_types \= feedback.completed  
timeout\_policy \= 5 seconds  
auto\_fallback\_state \= UNKNOWN

---

## **6.4 Stream Processing Classification**

Continuous Streaming State의 처리 방식을 정의한다.

필드:

stream\_processing\_policy  
window\_size  
sampling\_rate  
aggregation\_policy  
promotion\_event\_types  
ontology\_update\_policy

예:

state\_model \= GasSensorValueState  
state\_kind \= CONTINUOUS\_STREAMING\_STATE  
window\_size \= 5 seconds  
sampling\_rate \= 1 second  
aggregation\_policy \= MAX / AVG / THRESHOLD  
ontology\_update\_policy \= ON\_THRESHOLD  
promotion\_event\_types \= safety.gas.critical\_threshold\_exceeded

---

# **7\. State Lifecycle Management**

상태 생명주기는 다음 5개 개념을 중심으로 관리한다.

current\_state  
expected\_state  
pending\_state  
confirmed\_state  
reconciled\_state

---

## **7.1 current\_state**

`current_state`는 platform이 현재 알고 있는 상태다.

예:

Mission\_991.current\_state \= MissionStatus.IN\_PROGRESS

---

## **7.2 expected\_state**

`expected_state`는 특정 event, action, policy 판단에 의해 기대되는 상태다.

예:

ACTION\_DISABLE\_ROBOT\_MISSION  
→ expected\_state \= MissionStatus.DISABLED

---

## **7.3 pending\_state**

`pending_state`는 action 요청 이후 feedback을 기다리는 임시 상태다.

예:

Mission\_991.pending\_state \= MissionStatus.DISABLE\_REQUESTED

원칙:

pending\_state는 confirmed state가 아니다.  
pending\_state를 실제 완료 상태로 간주하면 안 된다.  
모든 pending\_state는 timeout\_policy를 가져야 한다.  
timeout 없는 pending\_state는 금지한다.

---

## **7.4 confirmed\_state**

`confirmed_state`는 feedback 또는 human confirmation으로 확인된 상태다.

예:

FleetManager feedback: mission disabled  
→ confirmed\_state \= MissionStatus.DISABLED

---

## **7.5 inferred\_state**

`inferred_state`는 ontology reasoner, rule engine, semantic inference가 도출한 상태다.

예:

Robot\_07 battery \= 18%  
→ inferred\_state \= BatteryRiskLevel.LOW\_BATTERY

inferred\_state는 유용하지만 runtime world state보다 늦게 도착할 수 있다.

따라서 inferred\_state와 current\_state가 잠시 다르다고 해서 즉시 conflict로 처리하면 안 된다.

---

## **7.6 reconciled\_state**

`reconciled_state`는 feedback, world state, ontology state, inferred state가 정합성 검사를 통과한 최종 동기화 상태다.

예:

confirmed\_state \= MissionStatus.DISABLED  
ontology\_state \= MissionStatus.DISABLED  
world\_state \= MissionStatus.DISABLED  
→ reconciled\_state \= MissionStatus.DISABLED

---

# **8\. State Transition Rule**

State transition은 아무렇게나 일어나면 안 된다.

State Model Registry는 허용 가능한 상태 전이만 등록해야 한다.

## **8.1 StateTransitionSpecDTO 필드**

권장 필드:

state\_model  
from\_state  
to\_state  
transition\_type  
trigger\_event\_types  
trigger\_action\_types  
required\_feedback\_types  
required\_evidence\_types  
required\_policy\_refs  
requires\_safety\_gate  
requires\_human\_approval  
requires\_audit  
timeout\_policy  
timeout\_duration  
auto\_fallback\_state  
timeout\_transition\_type  
timeout\_recovery\_action\_types  
temporal\_grace\_period  
reconciliation\_wait\_policy  
valid\_from  
valid\_until  
version

---

## **8.2 Transition Type**

값:

EVENT\_DRIVEN  
ACTION\_REQUESTED  
FEEDBACK\_CONFIRMED  
POLICY\_DRIVEN  
SYSTEM\_TIMEOUT  
MANUAL\_OVERRIDE  
RECOVERY\_DRIVEN  
FAIL\_SAFE\_TRIGGERED

의미:

`EVENT_DRIVEN`  
event 발생으로 인한 상태 전이다.

`ACTION_REQUESTED`  
action 요청으로 인한 expected 또는 pending 상태 전이다.

`FEEDBACK_CONFIRMED`  
feedback 확인으로 인한 confirmed 상태 전이다.

`POLICY_DRIVEN`  
policy 판단에 의한 상태 전이다.

`SYSTEM_TIMEOUT`  
응답 지연 또는 timeout에 의한 상태 전이다.

`MANUAL_OVERRIDE`  
사람의 수동 개입에 의한 상태 전이다.

`RECOVERY_DRIVEN`  
복구 절차에 의한 상태 전이다.

`FAIL_SAFE_TRIGGERED`  
safety-critical conflict 또는 reconciliation failure로 인한 fail-safe 전이다.

---

# **9\. Timeout, Reconciliation, and Fail-Safe Rules**

기존 문서에서는 timeout, reconciliation, fail-safe가 여러 섹션에 반복되어 있었다.

최종 문서에서는 이 내용을 하나의 lifecycle safety rule로 통합한다.

---

## **9.1 Pending State Timeout Rule**

pending\_state는 반드시 timeout\_policy를 가져야 한다.

기본 원칙:

모든 pending\_state는 timeout\_duration을 가져야 한다.  
timeout 없는 pending\_state는 금지한다.  
timeout 이후 auto\_fallback\_state로 전이한다.  
고위험 상태는 timeout 이후 recovery 또는 fail-safe로 연결한다.

예:

from\_state \= DISABLE\_REQUESTED  
expected\_state \= DISABLED  
timeout\_duration \= 5 seconds  
auto\_fallback\_state \= UNKNOWN  
timeout\_transition\_type \= SYSTEM\_TIMEOUT  
timeout\_recovery\_action\_types \= \[  
  ACTION\_NOTIFY\_OPERATOR,  
  ACTION\_REQUEST\_MANUAL\_OVERRIDE,  
  ACTION\_RETURN\_ROBOT\_TO\_SAFE\_ZONE  
\]

---

## **9.2 Reconciliation Rule**

Reconciliation은 expected state, feedback state, world state, ontology state, inferred state가 서로 맞는지 확인하는 과정이다.

성공 예:

expected\_state \= MissionStatus.DISABLED  
feedback\_state \= MissionStatus.DISABLED  
world\_state \= MissionStatus.DISABLED  
ontology\_state \= MissionStatus.DISABLED

reconciliation\_status \= SUCCESS  
reconciled\_state \= MissionStatus.DISABLED

실패 예:

expected\_state \= MissionStatus.DISABLED  
feedback\_state \= MissionStatus.STILL\_ACTIVE  
world\_state \= MissionStatus.IN\_PROGRESS  
ontology\_state \= MissionStatus.DISABLE\_REQUESTED

reconciliation\_status \= FAILED  
state\_conflict\_detected \= true  
recovery\_required \= true  
manual\_review\_required \= true

후속 조치:

Recovery action 생성  
Supervisor notification  
Manual override request  
Audit record update  
Policy review if repeated  
Ontology mapping review if semantic mismatch is suspected  
Fail-safe evaluation if safety-critical

---

## **9.3 Temporal Grace Period Rule**

Ontology inferred state와 runtime world state 사이에는 시간차가 발생할 수 있다.

이 시간차를 즉시 conflict로 처리하면 false positive가 폭발한다.

따라서 temporal grace period를 적용한다.

추가 필드:

temporal\_grace\_period  
settling\_time  
inference\_lag\_tolerance  
reconciliation\_wait\_policy

처리 예:

runtime world state:  
Robot\_07 battery \= 18%

ontology inferred state:  
Robot\_07 hasBatteryRiskLevel NORMAL

즉시 conflict로 처리하지 않는다.

먼저:

reconciliation\_status \= IN\_TRANSIT  
reason \= ontology inference pending  
grace\_period \= 3 seconds

3초 후에도 불일치하면:

reconciliation\_status \= CONFLICT  
manual\_review\_required \= true

원칙:

runtime state 변경 직후의 ontology mismatch는 즉시 conflict가 아니다.  
grace period 안에서는 IN\_TRANSIT 또는 PENDING\_RECONCILIATION으로 처리한다.  
grace period 이후에도 불일치하면 CONFLICT로 승격한다.

---

## **9.4 Fail-Safe Interception Rule**

Safety-critical entity에서 reconciliation failure가 발생하면 단순 알림만으로는 부족하다.

상태 정합성이 깨졌다는 것은 platform이 인식하는 세계와 실제 물리 세계가 다를 수 있다는 뜻이다.

따라서 safety-critical state model은 deterministic fail-safe state를 가져야 한다.

기본 흐름:

Reconciliation FAILED  
→ Safety Interceptor triggered  
→ Pre-approved Emergency Action selected  
→ EmergencyApprovedAction created  
→ EmergencyExecutionRequest sent  
→ External Safety / Control System executes  
→ Feedback received  
→ Post-hoc Audit

중요한 아키텍처 경계:

Ontology Platform  
→ fail-safe 판단과 emergency request 생성

External Control System  
→ 실제 물리 제어 수행

즉, State Model Registry는 fail-safe 판단과 요청 경계를 정의한다.  
실제 물리 제어는 PLC, robot middleware, fleet manager, SCADA, access control system이 수행한다.

---

# **10\. Ownership and Authority Arbitration**

모든 state는 owner를 가져야 한다.

State owner는 해당 상태의 authoritative source와 update authority를 정의한다.

하지만 CPS에서는 비상 상황에서 기존 source of truth보다 safety authority가 우선해야 할 수 있다.

---

## **10.1 Source of Truth 예시**

RobotPoseState  
→ primary\_source\_of\_truth \= RobotTelemetrySystem

MissionStatus  
→ primary\_source\_of\_truth \= FleetManager

ZoneAccessState  
→ primary\_source\_of\_truth \= AccessControlSystem

PermitStatus  
→ primary\_source\_of\_truth \= PermitManagementSystem

ExecutionState  
→ primary\_source\_of\_truth \= PlatformExecutionCore

ApprovalStatus  
→ primary\_source\_of\_truth \= ApprovalService

AuditStatus  
→ primary\_source\_of\_truth \= AuditService

---

## **10.2 Preemptive Authority 예시**

ZoneAccessState.primary\_source\_of\_truth \= AccessControlSystem  
ZoneAccessState.preemptive\_authorities \= EmergencyPolicyEngine, SafetyManagementSystem

비상 상황:

gas leak detected  
→ SafetyManagementSystem preempts ZoneAccessState  
→ ZoneAccessState \= EVACUATION\_REQUESTED or RESTRICTED

---

## **10.3 Authority Rule**

평상시에는 primary\_source\_of\_truth가 confirmed\_state를 갱신한다.

primary\_source\_of\_truth가 아닌 시스템은 평상시에 confirmed\_state를 직접 갱신할 수 없다.

단, 다음은 가능하다.

pending\_state 생성  
expected\_state 기록  
conflict flag 생성  
review request 생성  
reconciliation request 생성

비상 상황에서는 preemptive\_authority가 confirmed\_state 또는 fail\_safe\_state를 강제 전이할 수 있다.

이 경우 반드시 audit이 필요하다.

---

# **11\. State Freshness Rule**

상태는 시간이 지나면 stale해질 수 있다.

특히 sensor, robot pose, worker location, equipment telemetry는 freshness 관리가 중요하다.

Freshness TTL 예시:

RobotPoseState → 2 seconds  
WorkerLocationState → 5 seconds  
GasSensorValueState → 1 second  
EquipmentOperationalState → 10 seconds  
PermitStatus → 1 hour  
TaskStatus → 5 minutes  
ExecutionState → lifecycle controlled  
ApprovalStatus → lifecycle controlled

상태가 stale하면 다음 중 하나로 처리한다.

STALE  
UNKNOWN  
REVALIDATION\_REQUIRED  
MANUAL\_CONFIRMATION\_REQUIRED

고위험 action은 stale state를 기반으로 승인되면 안 된다.

---

# **12\. StateModelSpecDTO**

State Model Registry는 StateModelSpecDTO로 관리되어야 한다.

## **12.1 StateModelSpecDTO 필드**

권장 필드:

state\_model  
state\_category  
state\_kind  
domain\_module  
entity\_type  
ontology\_class

allowed\_state\_values  
initial\_states  
intermediate\_states  
terminal\_states  
failure\_states  
recovery\_states  
unknown\_state  
stale\_state

primary\_source\_of\_truth  
authoritative\_source  
fallback\_source  
update\_authority  
preemptive\_authorities  
authority\_priority\_level  
preemption\_conditions  
preemption\_audit\_required

freshness\_ttl  
confidence\_required  
evidence\_required  
requires\_audit

stream\_processing\_policy  
window\_size  
sampling\_rate  
aggregation\_policy  
promotion\_event\_types  
ontology\_update\_policy

temporal\_grace\_period  
settling\_time  
inference\_lag\_tolerance

deterministic\_fail\_safe\_state  
fail\_safe\_trigger\_conditions  
fail\_safe\_action\_types  
fail\_safe\_authority  
fail\_safe\_audit\_required

owner  
version  
status  
valid\_from  
valid\_until  
deprecated\_at  
replacement\_state\_model  
change\_reason

---

# **13\. StateTransitionSpecDTO**

State transition은 StateTransitionSpecDTO로 관리한다.

## **13.1 StateTransitionSpecDTO 필드**

권장 필드:

state\_model  
from\_state  
to\_state  
transition\_type  
trigger\_event\_types  
trigger\_action\_types  
required\_feedback\_types  
required\_evidence\_types  
required\_policy\_refs  
requires\_safety\_gate  
requires\_human\_approval  
requires\_audit

timeout\_policy  
timeout\_duration  
auto\_fallback\_state  
timeout\_transition\_type  
timeout\_recovery\_action\_types

temporal\_grace\_period  
reconciliation\_wait\_policy

owner  
version  
status  
valid\_from  
valid\_until  
deprecated\_at  
change\_reason

---

# **14\. Registry 운영 정책**

State Model Registry는 단순 enum 목록이 아니다.

State Model Registry는 ontology, runtime world state, external system feedback, audit, fail-safe execution boundary를 연결하는 governance 대상이다.

---

## **14.1 Registry Status**

State Model은 다음 status를 가질 수 있다.

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
→ 신규 state 사용 금지

BLOCKED  
→ 안전, 보안, 법적 문제로 차단

---

## **14.2 Versioning**

Backward-compatible change:

새 state value 추가  
optional metadata 추가  
freshness\_ttl 보강  
transition rule 추가  
fallback\_source 추가  
preemptive\_authority 추가  
temporal\_grace\_period 보강  
description 추가

Breaking change:

state value 이름 변경  
terminal state 의미 변경  
failure state 의미 변경  
transition rule 제거  
source\_of\_truth 변경  
authority priority 변경  
ontology\_class 변경  
freshness\_ttl 의미 변경  
fail\_safe\_state 의미 변경

Breaking change는 새 state\_model version 또는 새 state\_model로 분리하는 것이 원칙이다.

---

## **14.3 Approval Process**

State Model 변경은 owner와 domain steward의 승인을 받아야 한다.

고위험 state model은 다음 승인이 필요하다.

Ontology Steward  
Safety Owner  
Policy Owner  
Platform Architect  
Domain Owner  
External System Owner

---

## **14.4 Deprecation Policy**

State Model을 바로 삭제하지 않는다.

권장 절차:

DEPRECATED 상태로 변경  
replacement\_state\_model 지정  
dual-read / dual-write 기간 운영  
downstream consumer migration  
audit compatibility 확인  
RETIRED 상태로 변경  
major version에서 제거 가능

---

## **14.5 Compatibility Rule**

과거 state record는 항상 재해석 가능해야 한다.

따라서 WorldStateUpdateDTO, FeedbackEventDTO, AuditRecordDTO는 state\_model뿐 아니라 state\_model\_version도 참조해야 한다.

---

# **15\. 핵심 시나리오**

## **15.1 시나리오 1: ACTION\_DISABLE\_ROBOT\_MISSION**

상황:

Robot\_07의 Mission\_991이 blocked 상태이고, timeout이 임박했다.

흐름:

Event:  
robot.mission.blocked

Current State:  
MissionStatus.BLOCKED

ActionCandidate:  
ACTION\_DISABLE\_ROBOT\_MISSION

ApprovedAction:  
ACTION\_DISABLE\_ROBOT\_MISSION approved for Mission\_991

Expected State:  
MissionStatus.DISABLED

Pending State:  
MissionStatus.DISABLE\_REQUESTED

ExecutionRequest:  
Send disable mission request to FleetManager

Feedback:  
FleetManager reports mission disabled

Confirmed State:  
MissionStatus.DISABLED

Reconciliation:  
World State, Feedback, Ontology State match

Final State:  
MissionStatus.DISABLED

실패 흐름:

Pending State:  
DISABLE\_REQUESTED

Timeout:  
5 seconds elapsed without feedback

Fallback:  
UNKNOWN

Recovery:  
ACTION\_NOTIFY\_OPERATOR  
ACTION\_REQUEST\_MANUAL\_OVERRIDE  
ACTION\_RETURN\_ROBOT\_TO\_SAFE\_ZONE

---

## **15.2 시나리오 2: Reconciliation Failure → Fail-Safe**

상황:

플랫폼은 로봇 미션이 disabled 되었다고 기대하지만, feedback은 still active를 반환한다.

흐름:

Expected State:  
MissionStatus.DISABLED

Feedback State:  
MissionStatus.STILL\_ACTIVE

World State:  
MissionStatus.IN\_PROGRESS

Reconciliation:  
FAILED

Safety-Critical Check:  
true

Safety Interceptor:  
triggered

Fail-Safe State:  
RobotOperationalState.EMERGENCY\_STOPPED

Emergency Action:  
ACTION\_EMERGENCY\_STOP

Execution Boundary:  
EmergencyExecutionRequest sent to external robot control system

Post-hoc Audit:  
required

원칙:

플랫폼은 로봇 모터를 직접 제어하지 않는다.  
플랫폼은 fail-safe 판단과 emergency request를 생성한다.  
실제 물리 제어는 external control system이 수행한다.

---

## **15.3 시나리오 3: GasSensorValueState Stream Promotion**

상황:

GasSensor\_17이 1초 단위로 값을 전송한다.

일반 흐름:

GasSensorValueState received  
→ Edge Window Buffer  
→ Time-Series DB  
→ Aggregation  
→ No semantic event

임계값 초과 흐름:

GasSensorValueState exceeds critical threshold  
→ safety.gas.critical\_threshold\_exceeded  
→ ZoneRiskState.CRITICAL  
→ ActionCandidate:  
   ACTION\_EMERGENCY\_EVACUATE\_ZONE  
   ACTION\_EMERGENCY\_TRIGGER\_ALARM  
→ EmergencyApprovedAction  
→ EmergencyExecutionRequest  
→ Feedback  
→ Post-hoc Audit

원칙:

가스 센서 값이 매초 들어온다고 해서 매번 Knowledge Graph를 갱신하지 않는다.  
의미 있는 변화가 발생했을 때만 semantic event로 승격한다.

---

# **16\. MVP State Model Set**

MVP에서는 다음 state model부터 등록한다.

## **16.1 Robot / Mission**

RobotConnectivityState  
RobotBatteryRiskState  
RobotPoseState  
MissionStatus  
RobotOperationalState

## **16.2 Construction**

PermitStatus  
TaskStatus  
ZoneAccessState  
WorkerLocationState

## **16.3 Safety**

ZoneRiskState  
GasSensorRiskState  
EmergencyState  
EvacuationState

## **16.4 Industrial**

EquipmentOperationalState  
SensorHealthState  
PLCConnectionState  
AlarmState  
GasSensorValueState

## **16.5 Platform Lifecycle**

ApprovalStatus  
ExecutionState  
FeedbackStatus  
AuditStatus  
ReconciliationStatus

---

# **17\. Appendix C: State Model Catalog 분리 기준**

상세 state value 목록은 본문에 모두 넣지 않는다.

다음 항목은 Appendix C에서 관리한다.

robot state catalog  
mission state catalog  
construction state catalog  
safety state catalog  
industrial state catalog  
platform lifecycle state catalog  
execution state catalog  
feedback state catalog  
audit state catalog  
reconciliation state catalog

이렇게 해야 Core 문서가 길어지지 않는다.

---

# **18\. 권장 파일 구조**

## **18.1 Core State Registry**

state\_registry/  
  \_\_init\_\_.py  
  core.py  
  state\_model\_spec.py  
  transition\_spec.py  
  registry.py  
  classification.py  
  ownership.py  
  authority\_arbitration.py  
  freshness\_policy.py  
  stream\_state\_policy.py  
  reconciliation\_policy.py  
  temporal\_grace\_policy.py  
  fail\_safe\_policy.py  
  mutation\_policy.py

## **18.2 State Catalog**

state\_registry/catalog/  
  robot\_states.py  
  mission\_states.py  
  construction\_states.py  
  safety\_states.py  
  industrial\_states.py  
  platform\_lifecycle\_states.py

## **18.3 Mapping Tables**

state\_registry/mappings/  
  event\_to\_state\_transition.py  
  action\_to\_expected\_state.py  
  feedback\_to\_confirmed\_state.py  
  state\_to\_ontology\_property.py  
  state\_reconciliation\_rules.py  
  stream\_promotion\_rules.py  
  fail\_safe\_transition\_rules.py

---

# **19\. 우선 구현 순서**

MVP 구현 순서는 다음이 좋다.

StateCategory enum  
StateKind enum  
StateModelStatus enum  
TransitionType enum  
ReconciliationStatus enum  
AuthorityPriority enum  
StateModelSpecDTO  
StateTransitionSpecDTO  
StateRegistry  
StateTransitionRegistry  
MVP state value constants  
Event-to-State Transition Mapping  
Action-to-Expected-State Mapping  
Feedback-to-Confirmed-State Mapping  
State-to-Ontology Mapping  
Stream Promotion Rule  
Freshness Policy  
Temporal Grace Policy  
Authority Arbitration Policy  
Reconciliation Policy  
Fail-Safe Policy  
WorldStateUpdateDTO와 연결  
OntologyBoundEventDTO와 연결  
FeedbackEventDTO와 연결  
AuditRecordDTO와 연결

---

# **20\. 최종 원칙**

State Model Registry는 플랫폼의 상태 언어다.

Event Type은 사건을 말한다.  
Action Type은 대응을 말한다.  
State Model은 현재 무엇이 어떤 상태인지 말한다.

State는 단순 enum이 아니다.  
State는 entity의 의미 있는 현재값이고, 전이 규칙, 소유권, freshness, reconciliation, fail-safe 규칙을 가진다.

CPS에서는 action 요청과 실제 상태 변경이 다르다.  
따라서 expected\_state, pending\_state, confirmed\_state, reconciled\_state를 구분해야 한다.

고주기 stream state는 매번 ontology mutation을 수행하면 안 된다.  
Stream state는 edge buffer와 time-series path를 타고, 의미 있는 변화만 semantic event로 승격되어야 한다.

source\_of\_truth가 아닌 시스템은 평상시에 confirmed\_state를 직접 갱신하면 안 된다.  
하지만 비상 상황에서는 preemptive\_authority가 상태를 강제 전이할 수 있다.

pending\_state는 반드시 timeout과 fallback을 가져야 한다.  
고위험 action은 stale state를 기반으로 승인되면 안 된다.  
runtime state와 ontology inferred state 사이에는 temporal grace period가 필요하다.  
Reconciliation이 실패하고 safety-critical 조건이 만족되면 fail-safe path가 즉시 작동해야 한다.

최종 원칙은 다음과 같다.

Different entities, one state language.  
Different systems, one authority model.  
Different streams, one promotion policy.  
Different events, one transition discipline.  
Different actions, one expected mutation model.  
Different feedback delays, one reconciliation model.  
Different inference lags, one temporal grace policy.  
Different failures, one fail-safe discipline.  
Different states, one semantic backbone.

