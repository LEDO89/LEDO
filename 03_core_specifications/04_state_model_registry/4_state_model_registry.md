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

