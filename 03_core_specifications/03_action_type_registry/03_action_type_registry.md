# **Ontology centric “Action Type Registry”**

# **1\. Purpose**

This document defines the core rules of the Action Type Registry used in an ontology-centric cyber-physical platform.

The Action Type Registry is a structure for registering and managing the standard types of actions that the system can perform.

If an Event Type expresses “what happened,” an Action Type expresses “what response can be taken in response to that event.”

This document focuses on the following:

Define what an Action Type is.  
Distinguish Action Types from Event Types.  
Distinguish Action Types from ActionCandidates, ApprovedActions, and ExecutionRequests.  
Define Action Type naming rules.  
Define the operating principles of the Action Type Registry.  
Define how Action Types connect to ontology targets, expected state mutation, policy, approval, the Safety Gate, and external control.  
Distinguish Emergency Action Types from regular Action Types.  
Define the asynchronous feedback loop and execution states.  
Define the responsibility boundary for idempotency.  
Define how vendor-specific actions and external adapter actions can be extended without contaminating the core registry.

The complete list of action types is managed in a separate document: `06_registry_specs/action_registry/action_registry.md` (there is no dedicated "Action Type Catalog" appendix under `09_appendices/`; `09_appendices/appendix_b_event_catalog/` is the Event Type Catalog, not the Action Type Catalog).

---

# **2\. Document Separation Principle**

The Action Type Registry document is divided into two parts.

## **2.1 Core Action Type Specification**

This is the present document.

It covers:

Action Type definition  
Action Type naming convention  
Action Type classification model  
Action Type Registry operating policy  
Relationship between Action Type and Event Type  
Relationship between Action Type and Ontology Target  
Relationship between Action Type and World State Mutation  
Relationship between Action Type and Policy / Approval  
Relationship between Action Type and Safety Gate  
Relationship between Action Type and ExecutionRequest  
Relationship between Action Type and Feedback / Reconciliation  
Emergency Action Type rules  
External Adapter Extension Pattern  
Initial reference action type set

## **2.2 Action Type Catalog (`06_registry_specs/action_registry/`)**

This is a separate registry document, not a `09_appendices/` file.

It covers:

safety action list  
construction action list  
robot action list  
industrial action list  
notification action list  
governance action list  
emergency action list  
external adapter action examples  
vendor-specific action examples

By separating the document this way, the core document can remain short and stable, while the action catalog can continue to expand according to field requirements and equipment expansion.

---

# **3\. Definition of Action Type**

An Action Type is a standard type of response that the platform can perform.

An Action Type must answer the following questions:

What action is this?  
Which event is this action responding to?  
Which target entity can this action be applied to?  
What state change is expected from this action?  
Does this action require human approval?  
Does this action need to pass the Safety Gate?  
Is this action delivered to an external system?  
Is this an emergency action?  
Does this action require idempotency?  
Is this action subject to audit?  
What feedback confirms whether this action succeeded?  
If feedback is delayed or fails, which recovery path should be followed?

Examples:

ACTION\_NOTIFY\_SUPERVISOR

Meaning:

Send a notification to the supervisor.

ACTION\_STOP\_WORK

Meaning:

Request a work stoppage.

ACTION\_EVACUATE\_ZONE

Meaning:

Request evacuation of a specific zone.

ACTION\_DISABLE\_ROBOT\_MISSION

Meaning:

Stop or disable a robot mission.

ACTION\_LOCK\_ZONE

Meaning:

Change a specific zone into an access-restricted state.

---

# **4\. Core Distinctions**

## **4.1 Distinction Between Action Type and Event Type**

An Event Type is something that has already happened.

An Action Type is a response that can be performed in response to that event.

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

## **4.2 Distinction Between Action Type and ActionCandidate**

An Action Type is a type of possible action.

An ActionCandidate is a candidate action proposed in a specific situation.

Example:

Action Type:

ACTION\_EVACUATE\_ZONE

ActionCandidate:

Because the gas concentration in Zone\_A exceeded the critical threshold, propose evacuation of Zone\_A.

In other words:

An Action Type is a standard action name registered in the registry.  
An ActionCandidate is a concrete proposal generated based on an event, evidence, and world state.

---

## **4.3 Distinction Between ActionCandidate and ApprovedAction**

An ActionCandidate is not yet an executable object.

An ApprovedAction is an authority object produced by ApprovalDecision after policy, evidence, and approval validation.

Core principles:

An ActionCandidate is a proposal.  
An ApprovedAction grants authority, not execution readiness.  
An ActionCandidate cannot be executed directly.  
ExecutionRequest MUST NOT be created unless a SafetyGatePass has been issued from a valid RuntimeValidationResult.

---

## **4.4 Distinction Between ApprovedAction and ExecutionRequest**

An ApprovedAction expresses “what is allowed to be done.”

An ExecutionRequest expresses “which high-level request should be sent to which external system.”

Example:

ApprovedAction:

ACTION\_DISABLE\_ROBOT\_MISSION is approved for Robot\_07 Mission\_991.

ExecutionRequest:

Send disable mission request to FleetManager\_A for Robot\_07 Mission\_991.

An ApprovedAction is the authority boundary.  
An ExecutionRequest is the execution request sent to an external system.

---

## **4.5 Distinction Between Action Type and External Command**

An Action Type is a platform-level standard action name.

An External Command is the actual command format understood by a specific external system, vendor API, robot middleware, SCADA, PLC, or fleet manager.

Example:

Action Type:

ACTION\_DISABLE\_ROBOT\_MISSION

External Command:

POST /fleet/robots/{robot\_id}/missions/{mission\_id}/disable

Or:

ROS2 service call

Or:

SCADA command request

The Core Action Registry does not directly manage external command details.  
External command details are managed by the adapter layer.

---

# **5\. Action Type Naming Convention**

## **5.1 Basic Format**

Action Types use uppercase snake\_case.

Basic format:

ACTION\_VERB\_OBJECT

Examples:

ACTION\_NOTIFY\_SUPERVISOR

ACTION\_STOP\_WORK

ACTION\_EVACUATE\_ZONE

ACTION\_LOCK\_ZONE

ACTION\_UNLOCK\_ZONE

ACTION\_DISABLE\_ROBOT\_MISSION

ACTION\_REQUEST\_INSPECTION

---

## **5.2 More Specific Format**

When needed, the following format may be used:

ACTION\_VERB\_DOMAIN\_OBJECT

Examples:

ACTION\_NOTIFY\_SAFETY\_MANAGER

ACTION\_REQUEST\_SITE\_INSPECTION

ACTION\_DISABLE\_ROBOT\_MISSION

ACTION\_TRIGGER\_LOCAL\_ALARM

ACTION\_ESCALATE\_WAR\_ROOM

---

## **5.3 Emergency Action Format**

Emergency Actions must be clearly distinguished.

Recommended format:

ACTION\_EMERGENCY\_VERB\_OBJECT

Examples:

ACTION\_EMERGENCY\_STOP

ACTION\_EMERGENCY\_EVACUATE\_ZONE

ACTION\_EMERGENCY\_TRIGGER\_ALARM

ACTION\_EMERGENCY\_LOCK\_ZONE

ACTION\_EMERGENCY\_DISABLE\_ROBOT\_MISSION

Emergency Actions must have stricter registry governance and post-hoc audit requirements than regular actions.

---

## **5.4 Naming Rules**

Good examples:

ACTION\_STOP\_WORK

ACTION\_EVACUATE\_ZONE

ACTION\_NOTIFY\_SUPERVISOR

ACTION\_DISABLE\_ROBOT\_MISSION

Bad examples:

stopWork

evacuateZone

RobotDisableAction

do\_something

emergency1

An Action Type must be clear to humans and stable enough for system-level registry lookup.

---

# **6\. Classification Model**

An Action Type is not just a name.

The Action Type Registry must maintain the following classification information for each action type.

---

## **6.1 Semantic Classification**

Defines what the action means.

Fields:

action\_type

action\_category

domain\_module

description

allowed\_target\_types

required\_target\_refs

Example:

action\_type \= ACTION\_EVACUATE\_ZONE

action\_category \= SAFETY

domain\_module \= safety

allowed\_target\_types \= Zone

---

## **6.2 Risk Classification**

Defines how risky the action is.

Fields:

risk\_level

is\_safety\_critical

is\_emergency\_action

requires\_post\_hoc\_audit

Examples:

ACTION\_NOTIFY\_SUPERVISOR

→ risk\_level \= NOTICE

→ is\_safety\_critical \= false

ACTION\_EVACUATE\_ZONE

→ risk\_level \= HIGH\_RISK

→ is\_safety\_critical \= true

ACTION\_EMERGENCY\_STOP

→ risk\_level \= CRITICAL\_EMERGENCY

→ is\_emergency\_action \= true

→ requires\_post\_hoc\_audit \= true

---

## **6.3 Approval / Policy Classification**

Defines what approval and policy validation the action must pass.

Fields:

approval\_level

requires\_human\_approval

required\_policy\_refs

required\_roles

required\_clearance

requires\_safety\_gate

## **6.3.1 Relationship Between approval\_level and requires\_human\_approval**

`approval_level` is the source of truth.

`requires_human_approval` is a derived flag used for implementation convenience and fast lookup.

Recommended rules:

approval\_level \= NO\_APPROVAL

→ requires\_human\_approval \= false

approval\_level \= SUPERVISOR\_APPROVAL

→ requires\_human\_approval \= true

approval\_level \= SAFETY\_MANAGER\_APPROVAL

→ requires\_human\_approval \= true

approval\_level \= WAR\_ROOM\_APPROVAL

→ requires\_human\_approval \= true

approval\_level \= EXPERT\_REVIEW

→ requires\_human\_approval \= true

approval\_level \= EMERGENCY\_POLICY\_BYPASS

→ requires\_human\_approval \= false before execution

→ requires\_post\_hoc\_audit \= true after execution

In general, `requires_human_approval` should not be manually configured.  
It should be computed from `approval_level`.

Exceptions should only be allowed when explicitly approved through registry governance.

---

## **6.4 Execution Classification**

Defines whether the action is delivered to an external system.

Fields:

execution\_required

execution\_mode

allowed\_external\_systems

required\_adapter\_type

expected\_feedback\_types

feedback\_requirement

execution\_state\_model

timeout\_policy

retry\_policy

recovery\_policy

idempotency\_required

idempotency\_key\_strategy

idempotency\_scope

Examples:

ACTION\_NOTIFY\_SUPERVISOR

→ execution\_mode \= NOTIFICATION\_ONLY

→ external system \= notification service

ACTION\_DISABLE\_ROBOT\_MISSION

→ execution\_mode \= EXTERNAL\_SYSTEM\_REQUEST

→ external system \= fleet manager

ACTION\_LOCK\_ZONE

→ execution\_mode \= EXTERNAL\_SYSTEM\_REQUEST

→ external system \= access control system

---

## **6.5 Ontology Target / Mutation Classification**

Defines which ontology target the action applies to and what state change is expected after successful execution.

Fields:

target\_entity\_type

target\_ontology\_class

target\_required\_state

target\_forbidden\_state

expected\_mutated\_state

mutation\_timing

required\_capability

`expected_mutated_state` is the target entity state that the platform expects after the action is successfully performed.

Important points:

`expected_mutated_state` is not proof of actual completion.  
Actual completion must be confirmed through feedback.  
However, the platform can use this value to manage pending state, expected state, confirmed state, and reconciled state.

Examples:

ACTION\_DISABLE\_ROBOT\_MISSION

→ target\_entity\_type \= Mission

→ target\_ontology\_class \= robot:Mission

→ expected\_mutated\_state \= MissionStatus.DISABLED

ACTION\_LOCK\_ZONE

→ target\_entity\_type \= Zone

→ target\_ontology\_class \= construction:Zone

→ expected\_mutated\_state \= AccessState.LOCKED

ACTION\_EVACUATE\_ZONE

→ target\_entity\_type \= Zone

→ target\_ontology\_class \= construction:Zone

→ expected\_mutated\_state \= EvacuationState.EVACUATION\_REQUESTED

---

# **7\. Core Classification Values**

## **7.1 Action Category**

Action Category means the broad purpose of the action.

Values:

SAFETY

ROBOT

CONSTRUCTION

INDUSTRIAL

NOTIFICATION

GOVERNANCE

INSPECTION

ACCESS\_CONTROL

RECOVERY

EMERGENCY

---

## **7.2 Risk Level**

Risk Level means the degree of risk that may arise when performing the action.

Values:

INFO

NOTICE

WARNING

HIGH\_RISK

CRITICAL\_EMERGENCY

EXCEPTIONAL

---

## **7.3 Approval Level**

Approval Level means the level of approval required before performing the action.

Values:

NO\_APPROVAL

SUPERVISOR\_APPROVAL

SAFETY\_MANAGER\_APPROVAL

WAR\_ROOM\_APPROVAL

EXPERT\_REVIEW

EMERGENCY\_POLICY\_BYPASS

---

## **7.4 Execution Mode**

Execution Mode means how the action proceeds into the execution path.

Values:

NO\_EXTERNAL\_EXECUTION

NOTIFICATION\_ONLY

HUMAN\_TASK\_REQUEST

EXTERNAL\_SYSTEM\_REQUEST

EMERGENCY\_EXECUTION\_REQUEST

Examples:

ACTION\_NOTIFY\_SUPERVISOR

→ NOTIFICATION\_ONLY

ACTION\_REQUEST\_INSPECTION

→ HUMAN\_TASK\_REQUEST

ACTION\_DISABLE\_ROBOT\_MISSION

→ EXTERNAL\_SYSTEM\_REQUEST

ACTION\_EMERGENCY\_STOP

→ EMERGENCY\_EXECUTION\_REQUEST

---

## **7.5 Feedback Requirement**

Feedback Requirement means how completion of the action must be confirmed.

Values:

NO\_FEEDBACK\_REQUIRED

ACK\_REQUIRED

ACCEPTANCE\_REQUIRED

PROGRESS\_REQUIRED

COMPLETION\_REQUIRED

STATE\_CHANGE\_REQUIRED

HUMAN\_CONFIRMATION\_REQUIRED

POST\_HOC\_AUDIT\_REQUIRED

Examples:

ACTION\_NOTIFY\_SUPERVISOR

→ ACK\_REQUIRED

ACTION\_DISABLE\_ROBOT\_MISSION

→ COMPLETION\_REQUIRED or STATE\_CHANGE\_REQUIRED

ACTION\_EVACUATE\_ZONE

→ HUMAN\_CONFIRMATION\_REQUIRED

ACTION\_EMERGENCY\_STOP

→ POST\_HOC\_AUDIT\_REQUIRED

---

# **8\. expected\_mutated\_state and World State Synchronization**

In a CPS environment, sending a request to an external system does not mean that the physical world changes immediately.

Therefore, the Action Type Registry must explicitly define the expected state change after successful execution of the action.

## **8.1 State Distinctions**

Recommended state distinctions are as follows:

current\_state

expected\_mutated\_state

pending\_state

confirmed\_state

reconciled\_state

Meaning:

`current_state`  
The state currently known by the platform.

`expected_mutated_state`  
The state expected if the action succeeds.

`pending_state`  
A temporary state while waiting for feedback after the ExecutionRequest has been dispatched.

`confirmed_state`  
The state confirmed through external feedback or human confirmation.

`reconciled_state`  
The final synchronized state after checking consistency across feedback, world state, and ontology state.

---

## **8.2 World State Update Timing**

After action execution, World State is managed through the following sequence:

ApprovedAction created

→ expected\_mutated\_state recorded

→ RuntimeValidationInput created

→ RuntimeValidationResult produced

→ Safety Gate issues SafetyGatePass or SafetyGateBlock

→ ExecutionRequest created

→ pending\_state applied

→ Feedback received

→ confirmed\_state updated

→ reconciliation performed

→ reconciled\_state committed

ExecutionRequest MUST NOT be created unless a SafetyGatePass has been issued from a valid RuntimeValidationResult.

Example:

ACTION\_DISABLE\_ROBOT\_MISSION

State flow:

current\_state \= MissionStatus.ACTIVE

expected\_mutated\_state \= MissionStatus.DISABLED

pending\_state \= MissionStatus.DISABLE\_REQUESTED

confirmed\_state \= MissionStatus.DISABLED after feedback

reconciled\_state \= MissionStatus.DISABLED after reconciliation

---

## **8.3 Managing pending\_state Before Feedback**

Until feedback arrives, the platform must maintain a pending state rather than a final state.

Example:

ACTION\_LOCK\_ZONE

State flow:

current\_state \= AccessState.OPEN

expected\_mutated\_state \= AccessState.LOCKED

pending\_state \= AccessState.LOCK\_REQUESTED

At this point, the platform must not assume that Zone\_A is already locked.

Instead, it should represent the state as:

Zone\_A access lock requested, awaiting confirmation.

---

## **8.4 Handling Reconciliation Failure**

If feedback does not match the expected\_mutated\_state, it must be handled as a reconciliation failure.

Example:

Expected state:

MissionStatus.DISABLED

Actual feedback:

MissionStatus.STILL\_ACTIVE

Handling:

reconciliation.status \= FAILED

execution\_state \= RECOVERY\_REQUIRED

world\_state \= STATE\_CONFLICT\_DETECTED

manual\_review\_required \= true

Required follow-up actions:

Create recovery action  
Notify supervisor  
Request manual override  
Update audit record  
Review policy if the issue repeats

---

# **9\. Asynchronous Execution State Model**

The physical world is asynchronous.

Robots, SCADA, PLC, access control systems, mobile notifications, and smart helmet alerts do not complete immediately after receiving a request.

Therefore, intermediate states after ExecutionRequest must be clearly managed.

## **9.1 Core Execution States**

Canonical Reference: the states below are the minimal subset relevant to Feedback Requirement mapping (Section 9.3). The single canonical, implementation-authoritative enum (`DispatchStatus`) is defined in `03_core_specifications/09_execution_adapter_model/9_execution_adapter_model.md`, Section 20 "Dispatch Lifecycle", which additionally defines `READY_TO_DISPATCH`, `ACCEPTANCE_PENDING`, `REJECTED`, `ACK_TIMEOUT`, `ACCEPTANCE_TIMEOUT`, and `FEEDBACK_TIMEOUT`. Implementations must use one `DispatchStatus` enum sourced from `09_execution_adapter_model`; this section must not be implemented as a second, separate enum.

Recommended core states are as follows:

CREATED

DISPATCHED

ACKNOWLEDGED

ACCEPTED

IN\_PROGRESS

PARTIAL\_SUCCESS

COMPLETED

FAILED

TIMEOUT

FEEDBACK\_MISSING

RECOVERY\_REQUIRED

MANUAL\_OVERRIDE\_REQUIRED

CLOSED

## **9.2 State Meanings**

`CREATED`  
The ExecutionRequest has been created.

`DISPATCHED`  
The request has been sent to the external system.

`ACKNOWLEDGED`  
The external system has confirmed receipt of the request.

`ACCEPTED`  
The external system has accepted the request for execution.

`IN_PROGRESS`  
The request is being executed.

`PARTIAL_SUCCESS`  
Some targets succeeded, but the entire action is not complete.

`COMPLETED`  
The requested action has been completed.

`FAILED`  
Execution failed.

`TIMEOUT`  
No response was received within the configured time.

`FEEDBACK_MISSING`  
Feedback is missing after dispatch.

`RECOVERY_REQUIRED`  
A recovery procedure is required.

`MANUAL_OVERRIDE_REQUIRED`  
Human intervention is required.

`CLOSED`  
The execution lifecycle has ended.

---

## **9.3 Connecting Feedback Requirement to Execution State**

`ACK_REQUIRED`  
At least `ACKNOWLEDGED` is required.

`ACCEPTANCE_REQUIRED`  
At least `ACCEPTED` is required.

`PROGRESS_REQUIRED`  
`IN_PROGRESS` or a later state is required.

`COMPLETION_REQUIRED`  
`COMPLETED` is required.

`STATE_CHANGE_REQUIRED`  
A confirmed state matching the expected\_mutated\_state is required in World State or KG.

`HUMAN_CONFIRMATION_REQUIRED`  
A human confirmation event is required.

`POST_HOC_AUDIT_REQUIRED`  
PostHocAudit completed state is required.

---

# **10\. Event-to-Action Mapping Rule**

An Event Type does not directly execute an Action Type.

An Event Type only provides the condition under which an ActionCandidate may be generated.

Therefore, Event-to-Action Mapping must have the following structure.

## **10.1 Mapping Table Fields**

Recommended fields:

event\_type

condition

required\_evidence\_types

required\_world\_state

candidate\_action\_types

default\_action\_type

risk\_level

requires\_approval

requires\_safety\_gate

valid\_from

valid\_until

version

---

## **10.2 Mapping Example 1: Entry into a Danger Zone**

Event Type:

safety.worker.entered\_danger\_zone

Candidate Action Types:

ACTION\_NOTIFY\_SUPERVISOR

ACTION\_STOP\_WORK

ACTION\_EVACUATE\_ZONE

Condition:

The worker is inside a danger zone, equipment is active, and there is no permit or insufficient clearance.

---

## **10.3 Mapping Example 2: Gas Critical Threshold Exceeded**

Event Type:

safety.gas.critical\_threshold\_exceeded

Candidate Action Types:

ACTION\_EMERGENCY\_EVACUATE\_ZONE

ACTION\_EMERGENCY\_TRIGGER\_ALARM

ACTION\_EMERGENCY\_LOCK\_ZONE

Condition:

Gas concentration exceeded the critical threshold, and workers or robots are present in the corresponding zone.

---

## **10.4 Mapping Example 3: Robot Mission Blocked**

Event Type:

robot.mission.blocked

Candidate Action Types:

ACTION\_NOTIFY\_OPERATOR

ACTION\_REPLAN\_ROBOT\_MISSION

ACTION\_DISABLE\_ROBOT\_MISSION

Condition:

The robot has been blocked longer than the configured duration, and the mission timeout is approaching.

---

# **11\. Idempotency Responsibility Boundary**

Idempotency is a core mechanism for preventing duplicate physical execution.

It is especially mandatory for physical actions, emergency actions, and external system requests.

---

## **11.1 Core Responsibility**

The Platform Core generates the idempotency\_key.

Recommended generation rule:

idempotency\_key \= hash(

  approved\_action\_id,

  action\_type,

  target\_ref,

  trace\_id,

  idempotency\_scope,

  lifecycle\_version

)

For the current implementation stage, the following may be used:

idempotency\_key \= ApprovedActionID

The Core must ensure the following:

Prevent duplicate ExecutionRequests from being created from the same ApprovedAction.  
Include idempotency\_key in ExecutionRequestDTO.  
Record idempotency\_key in AuditRecordDTO.  
Maintain the same idempotency\_key across Timeout, Retry, and Recovery.

---

## **11.2 Adapter Responsibility**

The Adapter receives the idempotency\_key from the Core and forwards it to the external system.

If the external system supports idempotency, the same key is used.

If the external system does not support idempotency, the adapter must operate an internal deduplication table.

The Adapter must ensure the following:

Detect duplicate requests with the same idempotency\_key.  
Maintain the same key during external API retries.  
Return duplicate dispatch status through feedback.  
If duplicate execution is possible, transition the state to RECOVERY\_REQUIRED or MANUAL\_OVERRIDE\_REQUIRED.

---

## **11.3 External System Responsibility**

If the external system supports idempotency:

It must return the same result for the same idempotency\_key.  
It must not re-execute a duplicate command physically.  
If the request has already been completed, it must return completed or already\_processed status.

If the external system does not support idempotency:

The Core and Adapter must limit retries conservatively.

---

## **11.4 idempotency\_scope**

`idempotency_scope` means the range within which duplicate execution must be prevented.

Example values:

PER\_APPROVED\_ACTION

PER\_TARGET

PER\_ZONE

PER\_MISSION

PER\_ROBOT

PER\_WORKER

PER\_EXTERNAL\_SYSTEM

PER\_EMERGENCY\_INCIDENT

PER\_NOTIFICATION\_RECIPIENT

Examples:

ACTION\_NOTIFY\_SUPERVISOR

→ PER\_NOTIFICATION\_RECIPIENT

ACTION\_STOP\_WORK

→ PER\_ZONE or PER\_TASK

ACTION\_EVACUATE\_ZONE

→ PER\_ZONE

ACTION\_LOCK\_ZONE

→ PER\_ZONE

ACTION\_DISABLE\_ROBOT\_MISSION

→ PER\_MISSION

ACTION\_RETURN\_ROBOT\_TO\_SAFE\_ZONE

→ PER\_ROBOT

ACTION\_EMERGENCY\_STOP

→ PER\_EMERGENCY\_INCIDENT

ACTION\_SEND\_SMART\_HELMET\_ALERT

→ PER\_WORKER

---

# **12\. Action Type Registry Operating Policy**

The Action Type Registry is not a simple list.  
It is a governance-controlled registry.

Because an incorrect action type can lead to an incorrect execution request, it must be managed more strictly than the Event Type Registry.

---

## **12.1 ActionTypeSpecDTO Canonical Fields**

Recommended fields:

action\_type

action\_category

domain\_module

description

allowed\_event\_types

allowed\_target\_types

required\_target\_refs

required\_target\_states

forbidden\_target\_states

risk\_level

is\_safety\_critical

is\_emergency\_action

approval\_level

requires\_human\_approval

requires\_safety\_gate

requires\_post\_hoc\_audit

required\_policy\_refs

required\_roles

required\_clearance

execution\_required

execution\_mode

allowed\_external\_systems

required\_adapter\_type

expected\_feedback\_types

feedback\_requirement

execution\_state\_model

timeout\_policy

retry\_policy

recovery\_policy

idempotency\_required

idempotency\_key\_strategy

idempotency\_scope

target\_entity\_type

target\_ontology\_class

target\_required\_state

target\_forbidden\_state

expected\_mutated\_state

mutation\_timing

required\_capability

owner

version

status

valid\_from

valid\_until

deprecated\_at

replacement\_action\_type

change\_reason

---

## **12.2 Registry Status**

An Action Type may have the following statuses:

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
→ New action generation is prohibited

BLOCKED  
→ Blocked due to security, safety, or legal issues

---

## **12.3 Registry Versioning**

An Action Type must have a version.

Backward-compatible changes:

Adding a description  
Adding allowed\_event\_types  
Adding expected\_feedback\_types  
Enhancing timeout\_policy  
Enhancing retry\_policy  
Adding metadata

Breaking changes:

Changing the action\_type name  
Changing the meaning of risk\_level  
Changing approval\_level  
Removing requires\_safety\_gate  
Removing requires\_post\_hoc\_audit  
Changing allowed\_target\_types  
Changing execution\_mode  
Changing the external system route  
Changing the meaning of expected\_mutated\_state  
Changing idempotency\_scope

As a rule, breaking changes should be separated into a new action\_type.

---

## **12.4 Approval Process**

Changes to an Action Type must be approved by the owner and the domain steward.

Recommended approval authorities:

Domain Owner  
Ontology Steward  
Safety Owner  
Policy Owner  
Platform Architect  
External Adapter Owner  
Legal / Compliance Owner

For high-risk actions and emergency actions, approval from the Safety Owner, Policy Owner, and Platform Architect is mandatory.

---

## **12.5 Deprecation Policy**

An Action Type should not be deleted immediately.

Recommended process:

Change status to DEPRECATED  
Specify replacement\_action\_type  
Operate a dual-read / dual-write period  
Migrate downstream consumers  
Verify audit compatibility  
Change status to RETIRED  
Remove in a major version if necessary

---

## **12.6 Registry Compatibility Rule**

Past action records must always remain interpretable.

Therefore, ApprovedActionDTO and AuditRecordDTO must reference not only action\_type, but also action\_type\_version.

---

# **13\. Emergency Action Registry**

Emergency Actions must have stronger governance than regular Action Types.

Emergency Actions may be executed quickly, but not every action can enter the emergency path.

Only pre-registered and pre-validated actions are allowed as Emergency Actions.

---

## **13.1 Emergency Action Conditions**

Emergency Actions must have the following conditions:

pre-approved emergency condition  
deterministic rule  
allowed target types  
minimal evidence requirement  
local policy check  
idempotency requirement  
timeout policy  
recovery policy  
expected feedback  
expected\_mutated\_state  
post-hoc audit requirement

---

## **13.2 Emergency Action Examples**

ACTION\_EMERGENCY\_STOP

ACTION\_EMERGENCY\_EVACUATE\_ZONE

ACTION\_EMERGENCY\_TRIGGER\_ALARM

ACTION\_EMERGENCY\_LOCK\_ZONE

ACTION\_EMERGENCY\_DISABLE\_ROBOT\_MISSION

---

## **13.3 Emergency Action Rule**

Emergency Actions cannot be created directly by an LLM.

An LLM or agent may describe an emergency situation or propose an ActionCandidate.

However, an EmergencyApprovedAction grants emergency authority only; EmergencyExecutionRequest requires EmergencyRuntimeValidationResult and EmergencySafetyGatePass.

---

# **14\. Vendor / External Adapter Action Pattern**

External systems each have different command structures.

Examples:

Robot Fleet Manager  
ROS2 Bridge  
SCADA  
PLC Gateway  
Access Control System  
Smart Helmet Alert System  
Mobile Notification Service  
Inspection Platform

A Core Action Type does not directly include external command details.

A Core Action Type only defines the standard meaning of the action.

The External Adapter translates the Action Type into a vendor-specific command.

Example:

Core Action Type:

ACTION\_DISABLE\_ROBOT\_MISSION

Adapter Translation:

FleetManager.disable\_mission(robot\_id, mission\_id)

Or:

ROS2 service call

Or:

Vendor REST API request

This structure prevents the core registry from being contaminated by vendor details.

---

# **15\. Post-hoc Audit Rule**

Emergency Actions or high-risk actions must have post-hoc audit.

Basic flow:

ApprovedAction created

→ RuntimeValidationInput created

→ RuntimeValidationResult produced

→ Safety Gate issues SafetyGatePass or SafetyGateBlock

→ ExecutionRequest created

→ Feedback received

→ PostHocAudit pending

→ PostHocAudit completed

ExecutionRequest MUST NOT be created unless a SafetyGatePass has been issued from a valid RuntimeValidationResult.

If a problem occurs:

PostHocAudit pending

→ PostHocAudit escalated

Or:

PostHocAudit completed

→ Policy updated

Or:

PostHocAudit completed

→ ActionType deprecated

Principles:

The faster an action is executed, the stronger its post-hoc audit must be.  
An emergency action whose post-hoc audit has not been closed is not considered to have fully completed its lifecycle.

---

# **16\. Initial Reference Action Type Set**

The complete action type list is managed in `06_registry_specs/action_registry/action_registry.md`.

**Non-normative note:** the action type names below are reference fixtures used to exercise the registry and lifecycle end to end. They are not an approved domain decision; see `06_registry_specs/action_registry/action_registry.md` Sections 11–12 for the corresponding non-normative marking on the registry side.

For the first formal implementation, only the following action types should be registered first.

## **16.1 Safety Reference Actions**

ACTION\_NOTIFY\_SUPERVISOR

ACTION\_STOP\_WORK

ACTION\_EVACUATE\_ZONE

ACTION\_LOCK\_ZONE

ACTION\_TRIGGER\_LOCAL\_ALARM

## **16.2 Emergency Reference Actions**

ACTION\_EMERGENCY\_STOP

ACTION\_EMERGENCY\_EVACUATE\_ZONE

ACTION\_EMERGENCY\_TRIGGER\_ALARM

ACTION\_EMERGENCY\_LOCK\_ZONE

ACTION\_EMERGENCY\_DISABLE\_ROBOT\_MISSION

## **16.3 Robot Reference Actions**

ACTION\_NOTIFY\_OPERATOR

ACTION\_DISABLE\_ROBOT\_MISSION

ACTION\_REPLAN\_ROBOT\_MISSION

ACTION\_RETURN\_ROBOT\_TO\_SAFE\_ZONE

## **16.4 Construction Reference Actions**

ACTION\_REQUEST\_INSPECTION

ACTION\_HOLD\_TASK

ACTION\_RESUME\_TASK

ACTION\_REQUEST\_PERMIT\_REVIEW

## **16.5 Governance Reference Actions**

ACTION\_REQUEST\_APPROVAL

ACTION\_ESCALATE\_TO\_SAFETY\_MANAGER

ACTION\_ESCALATE\_TO\_WAR\_ROOM

ACTION\_CREATE\_MAPPING\_REVIEW

## **16.6 Notification Reference Actions**

ACTION\_SEND\_MOBILE\_ALERT

ACTION\_SEND\_DASHBOARD\_ALERT

ACTION\_SEND\_SMART\_HELMET\_ALERT

---

# **17\. Separation Criteria for the Action Type Catalog (`06_registry_specs/action_registry/`)**

Detailed lists by Action Category are not included in the main body.

The following items are managed in `06_registry_specs/action_registry/action_registry.md`, not in `09_appendices/`:

safety action catalog  
emergency action catalog  
robot action catalog  
construction action catalog  
industrial action catalog  
notification action catalog  
governance action catalog  
inspection action catalog  
recovery action catalog  
vendor adapter action examples

This prevents the Core document from becoming too long.

---

# **18\. Recommended File Structure**

## **18.1 Core Action Registry**

action\_registry/

  \_\_init\_\_.py

  core.py

  action\_type\_spec.py

  registry.py

  classification.py

  approval\_policy.py

  execution\_policy.py

  mutation\_policy.py

  emergency\_action\_registry.py

  feedback\_requirement.py

  idempotency\_policy.py

  vendor\_adapter\_policy.py

## **18.2 Action Catalog**

action\_registry/catalog/

  safety\_actions.py

  emergency\_actions.py

  robot\_actions.py

  construction\_actions.py

  industrial\_actions.py

  notification\_actions.py

  governance\_actions.py

  recovery\_actions.py

## **18.3 Mapping Tables**

action\_registry/mappings/

  event\_to\_action\_mapping.py

  action\_to\_policy\_mapping.py

  action\_to\_adapter\_mapping.py

  action\_to\_feedback\_mapping.py

  action\_to\_ontology\_target\_mapping.py

  action\_to\_mutation\_mapping.py

---

# **19\. Recommended Implementation Order**

The implementation order should be as follows.

ActionCategory enum  
RiskLevel enum  
ApprovalLevel enum  
ExecutionMode enum  
FeedbackRequirement enum  
ExecutionState enum  
IdempotencyScope enum  
ActionTypeStatus enum  
ActionTypeSpecDTO  
ActionTypeRegistry  
EmergencyActionSpecDTO  
WorldStateMutationPlanDTO  
Event-to-Action Mapping Table  
Action-to-Policy Mapping Table  
Action-to-Adapter Mapping Table  
Action-to-Feedback Mapping Table  
Action-to-Mutation Mapping Table  
Initial reference action type constants  
ActionType validation function  
Connection to ActionCandidateDTO  
Connection to ApprovedActionDTO  
Connection to ExecutionRequestDTO  
Connection to FeedbackEventDTO

---

# **21\. Final Principle**

The Action Type Registry is the standard response language of the platform.

Event Type is the cause.  
Action Type is the response.  
ActionCandidate is a proposal.  
ApprovedAction is an approved action.  
ExecutionRequest is a request sent to an external system.  
Feedback is evidence confirming the execution result.  
PostHocAudit is the responsibility boundary for high-risk or emergency actions.

The system must not assume that an action has succeeded.  
An action may have an expected\_mutated\_state.  
However, the actual state change must be confirmed through feedback and reconciliation.

Idempotency begins in the Core and is enforced by the Adapter.  
If the external system supports idempotency, it is connected to external idempotency as well.  
If not, the adapter must conservatively prevent duplicate execution.

The final principles are as follows:

Different events, one action language.  
Different risks, one approval model.  
Different targets, one ontology-aware mutation model.  
Different systems, one execution boundary.  
Different feedback delays, one execution state model.  
Different vendors, one adapter pattern.  
Different retries, one idempotency discipline.  
Different emergencies, one post-hoc audit discipline.

# 

# 

# **Ontology centric “Action Type Registry”**

