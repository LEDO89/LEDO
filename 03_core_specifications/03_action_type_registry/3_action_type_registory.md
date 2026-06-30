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

The complete list of action types is managed in a separate document: Appendix B: Action Type Catalog.

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
MVP action type set

## **2.2 Appendix B: Action Type Catalog**

This is a separate appendix document.

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

An ApprovedAction is an execution-approved object that has passed Safety Gate, policy, evidence, and approval validation.

Core principles:

An ActionCandidate is a proposal.  
An ApprovedAction is an approved action.  
An ActionCandidate cannot be executed directly.  
Only an ApprovedAction can be promoted to an ExecutionRequest.

---

## **4.4 Distinction Between ApprovedAction and ExecutionRequest**

An ApprovedAction expresses “what is allowed to be done.”

An ExecutionRequest expresses “which high-level request should be sent to which external system.”

Example:

ApprovedAction:

ACTION\_DISABLE\_ROBOT\_MISSION is approved for Robot\_07 Mission\_991.

ExecutionRequest:

Send disable mission request to FleetManager\_A for Robot\_07 Mission\_991.

An ApprovedAction is the policy and safety boundary.  
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

→ ExecutionRequest created

→ pending\_state applied

→ Feedback received

→ confirmed\_state updated

→ reconciliation performed

→ reconciled\_state committed

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

For the MVP, the following may be used:

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

However, an EmergencyApprovedAction must pass the registry, deterministic rule, local policy, and safety validation.

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

→ ExecutionRequest created

→ Feedback received

→ PostHocAudit pending

→ PostHocAudit completed

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

# **16\. MVP Action Type Set**

The complete action type list is managed in Appendix B.

For the MVP, only the following action types should be registered first.

## **16.1 Safety MVP Actions**

ACTION\_NOTIFY\_SUPERVISOR

ACTION\_STOP\_WORK

ACTION\_EVACUATE\_ZONE

ACTION\_LOCK\_ZONE

ACTION\_TRIGGER\_LOCAL\_ALARM

## **16.2 Emergency MVP Actions**

ACTION\_EMERGENCY\_STOP

ACTION\_EMERGENCY\_EVACUATE\_ZONE

ACTION\_EMERGENCY\_TRIGGER\_ALARM

ACTION\_EMERGENCY\_LOCK\_ZONE

ACTION\_EMERGENCY\_DISABLE\_ROBOT\_MISSION

## **16.3 Robot MVP Actions**

ACTION\_NOTIFY\_OPERATOR

ACTION\_DISABLE\_ROBOT\_MISSION

ACTION\_REPLAN\_ROBOT\_MISSION

ACTION\_RETURN\_ROBOT\_TO\_SAFE\_ZONE

## **16.4 Construction MVP Actions**

ACTION\_REQUEST\_INSPECTION

ACTION\_HOLD\_TASK

ACTION\_RESUME\_TASK

ACTION\_REQUEST\_PERMIT\_REVIEW

## **16.5 Governance MVP Actions**

ACTION\_REQUEST\_APPROVAL

ACTION\_ESCALATE\_TO\_SAFETY\_MANAGER

ACTION\_ESCALATE\_TO\_WAR\_ROOM

ACTION\_CREATE\_MAPPING\_REVIEW

## **16.6 Notification MVP Actions**

ACTION\_SEND\_MOBILE\_ALERT

ACTION\_SEND\_DASHBOARD\_ALERT

ACTION\_SEND\_SMART\_HELMET\_ALERT

---

# **17\. Separation Criteria for Appendix B: Action Type Catalog**

Detailed lists by Action Category are not included in the main body.

The following items are managed in Appendix B:

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

The MVP implementation order should be as follows.

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
MVP action type constants  
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

# **1\. 목적**

본 문서는 온톨로지 중심 사이버-물리 플랫폼에서 사용되는 Action Type Registry의 핵심 규칙을 정의한다.

Action Type Registry는 시스템이 수행할 수 있는 표준 조치 유형을 등록하고 관리하는 구조다.

Event Type이 “무슨 일이 발생했는가”를 표현한다면, Action Type은 “그 사건에 대해 어떤 대응을 할 수 있는가”를 표현한다.

이 문서는 다음에 집중한다.

Action Type이 무엇인지 정의한다.  
Action Type과 Event Type을 구분한다.  
Action Type과 ActionCandidate, ApprovedAction, ExecutionRequest를 구분한다.  
Action Type 이름 규칙을 정의한다.  
Action Type Registry 운영 원칙을 정의한다.  
Action Type이 ontology target, expected state mutation, policy, approval, Safety Gate, external control과 어떻게 연결되는지 정의한다.  
Emergency Action Type과 일반 Action Type을 구분한다.  
비동기 feedback loop와 execution state를 정의한다.  
Idempotency 책임 경계를 정의한다.  
Vendor-specific action과 external adapter action을 core registry 오염 없이 확장하는 방법을 정의한다.

전체 action type 목록은 별도 문서인 Appendix B: Action Type Catalog에서 관리한다.

---

# **2\. 문서 분리 원칙**

Action Type Registry 문서는 두 부분으로 나눈다.

## **2.1 Core Action Type Specification**

본 문서다.

다루는 내용:

Action Type 정의  
Action Type naming convention  
Action Type classification model  
Action Type Registry 운영 정책  
Action Type과 Event Type의 관계  
Action Type과 Ontology Target의 관계  
Action Type과 World State Mutation의 관계  
Action Type과 Policy / Approval의 관계  
Action Type과 Safety Gate의 관계  
Action Type과 ExecutionRequest의 관계  
Action Type과 Feedback / Reconciliation의 관계  
Emergency Action Type 규칙  
External Adapter Extension Pattern  
MVP action type set

## **2.2 Appendix B: Action Type Catalog**

별도 부록 문서다.

다루는 내용:

safety action list  
construction action list  
robot action list  
industrial action list  
notification action list  
governance action list  
emergency action list  
external adapter action examples  
vendor-specific action examples

이렇게 분리하면 core 문서는 짧고 안정적으로 유지되고, action catalog는 현장과 장비 확장에 따라 계속 확장할 수 있다.

---

# **3\. Action Type의 정의**

Action Type은 플랫폼이 수행할 수 있는 표준 조치 유형이다.

Action Type은 다음 질문에 답해야 한다.

무슨 조치인가?  
어떤 event에 대한 대응인가?  
어떤 target entity에 적용 가능한가?  
이 action은 어떤 상태 변화를 기대하는가?  
이 action은 사람이 승인해야 하는가?  
이 action은 Safety Gate를 통과해야 하는가?  
이 action은 external system으로 전달되는가?  
이 action은 emergency action인가?  
이 action은 idempotency가 필요한가?  
이 action은 audit 대상인가?  
이 action이 성공했는지 어떤 feedback으로 확인할 것인가?  
feedback이 늦거나 실패하면 어떤 recovery path를 타는가?

예:

ACTION\_NOTIFY\_SUPERVISOR

의미:

감독자에게 알림을 보낸다.

ACTION\_STOP\_WORK

의미:

작업 중지 조치를 요청한다.

ACTION\_EVACUATE\_ZONE

의미:

특정 구역의 대피를 요청한다.

ACTION\_DISABLE\_ROBOT\_MISSION

의미:

로봇 미션을 중지하거나 비활성화한다.

ACTION\_LOCK\_ZONE

의미:

특정 구역을 접근 제한 상태로 전환한다.

---

# **4\. 핵심 구분**

## **4.1 Action Type과 Event Type의 구분**

Event Type은 이미 발생한 사건이다.

Action Type은 그 사건에 대해 수행할 수 있는 대응 조치다.

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

## **4.2 Action Type과 ActionCandidate의 구분**

Action Type은 가능한 조치의 종류다.

ActionCandidate는 특정 상황에서 제안된 후보 조치다.

예:

Action Type:

ACTION\_EVACUATE\_ZONE

ActionCandidate:

Zone\_A에서 가스 농도가 critical threshold를 초과했으므로 Zone\_A 대피를 제안한다.

즉:

Action Type은 registry에 등록된 표준 조치명이다.  
ActionCandidate는 event, evidence, world state를 기반으로 생성된 구체적 제안이다.

---

## **4.3 ActionCandidate와 ApprovedAction의 구분**

ActionCandidate는 아직 실행 가능한 객체가 아니다.

ApprovedAction은 Safety Gate, policy, evidence, approval validation을 통과한 실행 승인 객체다.

핵심 원칙:

ActionCandidate는 제안이다.  
ApprovedAction은 승인된 조치다.  
ActionCandidate는 직접 실행될 수 없다.  
ApprovedAction만 ExecutionRequest로 승격될 수 있다.

---

## **4.4 ApprovedAction과 ExecutionRequest의 구분**

ApprovedAction은 “무엇을 해도 되는가”를 표현한다.

ExecutionRequest는 “어느 외부 시스템에 어떤 high-level 요청을 보낼 것인가”를 표현한다.

예:

ApprovedAction:

ACTION\_DISABLE\_ROBOT\_MISSION is approved for Robot\_07 Mission\_991.

ExecutionRequest:

Send disable mission request to FleetManager\_A for Robot\_07 Mission\_991.

ApprovedAction은 정책과 안전 경계다.  
ExecutionRequest는 외부 시스템으로 나가는 실행 요청이다.

---

## **4.5 Action Type과 External Command의 구분**

Action Type은 platform-level 표준 조치명이다.

External Command는 특정 외부 시스템, vendor API, robot middleware, SCADA, PLC, fleet manager가 이해하는 실제 명령 형식이다.

예:

Action Type:

ACTION\_DISABLE\_ROBOT\_MISSION

External Command:

POST /fleet/robots/{robot\_id}/missions/{mission\_id}/disable

또는:

ROS2 service call

또는:

SCADA command request

Core Action Registry는 external command detail을 직접 관리하지 않는다.  
External command detail은 adapter layer가 관리한다.

---

# **5\. Action Type Naming Convention**

## **5.1 기본 형식**

Action Type은 대문자 snake\_case를 사용한다.

기본 형식:

ACTION\_VERB\_OBJECT

예:

ACTION\_NOTIFY\_SUPERVISOR  
ACTION\_STOP\_WORK  
ACTION\_EVACUATE\_ZONE  
ACTION\_LOCK\_ZONE  
ACTION\_UNLOCK\_ZONE  
ACTION\_DISABLE\_ROBOT\_MISSION  
ACTION\_REQUEST\_INSPECTION

---

## **5.2 더 구체적인 형식**

필요하면 다음 형식을 사용할 수 있다.

ACTION\_VERB\_DOMAIN\_OBJECT

예:

ACTION\_NOTIFY\_SAFETY\_MANAGER  
ACTION\_REQUEST\_SITE\_INSPECTION  
ACTION\_DISABLE\_ROBOT\_MISSION  
ACTION\_TRIGGER\_LOCAL\_ALARM  
ACTION\_ESCALATE\_WAR\_ROOM

---

## **5.3 Emergency Action 형식**

Emergency Action은 명확히 구분한다.

권장 형식:

ACTION\_EMERGENCY\_VERB\_OBJECT

예:

ACTION\_EMERGENCY\_STOP  
ACTION\_EMERGENCY\_EVACUATE\_ZONE  
ACTION\_EMERGENCY\_TRIGGER\_ALARM  
ACTION\_EMERGENCY\_LOCK\_ZONE  
ACTION\_EMERGENCY\_DISABLE\_ROBOT\_MISSION

Emergency Action은 일반 action보다 더 엄격한 registry governance와 post-hoc audit을 가져야 한다.

---

## **5.4 이름 규칙**

좋은 예:

ACTION\_STOP\_WORK  
ACTION\_EVACUATE\_ZONE  
ACTION\_NOTIFY\_SUPERVISOR  
ACTION\_DISABLE\_ROBOT\_MISSION

나쁜 예:

stopWork  
evacuateZone  
RobotDisableAction  
do\_something  
emergency1

Action Type은 사람이 읽어도 의미가 명확해야 하고, 시스템이 registry에서 안정적으로 조회할 수 있어야 한다.

---

# **6\. Classification Model**

Action Type은 단순한 이름만으로 끝나지 않는다.

Action Type Registry는 각 action type에 대해 다음 분류 정보를 가져야 한다.

---

## **6.1 Semantic Classification**

이 action이 무엇을 의미하는지 정의한다.

필드:

action\_type  
action\_category  
domain\_module  
description  
allowed\_target\_types  
required\_target\_refs

예:

action\_type \= ACTION\_EVACUATE\_ZONE  
action\_category \= SAFETY  
domain\_module \= safety  
allowed\_target\_types \= Zone

---

## **6.2 Risk Classification**

이 action이 얼마나 위험한 조치인지 정의한다.

필드:

risk\_level  
is\_safety\_critical  
is\_emergency\_action  
requires\_post\_hoc\_audit

예:

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

이 action이 어떤 승인과 policy 검증을 받아야 하는지 정의한다.

필드:

approval\_level  
requires\_human\_approval  
required\_policy\_refs  
required\_roles  
required\_clearance  
requires\_safety\_gate

## **6.3.1 approval\_level과 requires\_human\_approval의 관계**

`approval_level`은 source of truth다.

`requires_human_approval`은 구현 편의와 빠른 조회를 위한 derived flag로 둔다.

권장 규칙:

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

즉, 일반적으로 `requires_human_approval`은 직접 수동 설정하지 않고 `approval_level`에서 계산하는 것이 안전하다.

예외는 registry governance 과정에서 명시적으로 승인된 경우에만 허용한다.

---

## **6.4 Execution Classification**

이 action이 external system으로 전달되는지 정의한다.

필드:

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

예:

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

이 action이 어떤 ontology target에 적용되고, 성공 후 어떤 상태 변화를 기대하는지 정의한다.

필드:

target\_entity\_type  
target\_ontology\_class  
target\_required\_state  
target\_forbidden\_state  
expected\_mutated\_state  
mutation\_timing  
required\_capability

`expected_mutated_state`는 Action이 성공적으로 수행된 후 platform이 기대하는 target entity의 상태 변화다.

중요한 점은 다음이다.

`expected_mutated_state`는 실제 완료 사실이 아니다.  
실제 완료 여부는 feedback으로 확인해야 한다.  
다만 platform은 이 값을 기준으로 pending state, expected state, confirmed state, reconciled state를 관리할 수 있다.

예:

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

# **7\. 핵심 분류 값**

## **7.1 Action Category**

Action Category는 action의 큰 목적을 의미한다.

값:

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

Risk Level은 action 수행 시 발생할 수 있는 위험도를 의미한다.

값:

INFO  
NOTICE  
WARNING  
HIGH\_RISK  
CRITICAL\_EMERGENCY  
EXCEPTIONAL

---

## **7.3 Approval Level**

Approval Level은 action 수행 전에 필요한 승인 수준을 의미한다.

값:

NO\_APPROVAL  
SUPERVISOR\_APPROVAL  
SAFETY\_MANAGER\_APPROVAL  
WAR\_ROOM\_APPROVAL  
EXPERT\_REVIEW  
EMERGENCY\_POLICY\_BYPASS

---

## **7.4 Execution Mode**

Execution Mode는 action이 어떻게 실행 경로로 내려가는지 의미한다.

값:

NO\_EXTERNAL\_EXECUTION  
NOTIFICATION\_ONLY  
HUMAN\_TASK\_REQUEST  
EXTERNAL\_SYSTEM\_REQUEST  
EMERGENCY\_EXECUTION\_REQUEST

예:

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

Feedback Requirement는 action 완료 여부를 어떤 방식으로 확인해야 하는지를 의미한다.

값:

NO\_FEEDBACK\_REQUIRED  
ACK\_REQUIRED  
ACCEPTANCE\_REQUIRED  
PROGRESS\_REQUIRED  
COMPLETION\_REQUIRED  
STATE\_CHANGE\_REQUIRED  
HUMAN\_CONFIRMATION\_REQUIRED  
POST\_HOC\_AUDIT\_REQUIRED

예:

ACTION\_NOTIFY\_SUPERVISOR  
→ ACK\_REQUIRED

ACTION\_DISABLE\_ROBOT\_MISSION  
→ COMPLETION\_REQUIRED or STATE\_CHANGE\_REQUIRED

ACTION\_EVACUATE\_ZONE  
→ HUMAN\_CONFIRMATION\_REQUIRED

ACTION\_EMERGENCY\_STOP  
→ POST\_HOC\_AUDIT\_REQUIRED

---

# **8\. expected\_mutated\_state와 World State 동기화**

CPS 환경에서는 외부 시스템에 요청을 보냈다고 해서 물리 세계가 즉시 바뀌지 않는다.

따라서 Action Type Registry는 action 성공 후 기대되는 상태 변화를 명시해야 한다.

## **8.1 상태 구분**

권장 상태 구분은 다음과 같다.

current\_state  
expected\_mutated\_state  
pending\_state  
confirmed\_state  
reconciled\_state

의미:

`current_state`  
현재 platform이 알고 있는 상태다.

`expected_mutated_state`  
action 성공 시 기대되는 상태다.

`pending_state`  
ExecutionRequest가 dispatch된 후, feedback을 기다리는 임시 상태다.

`confirmed_state`  
external feedback 또는 human confirmation으로 확인된 상태다.

`reconciled_state`  
feedback, world state, ontology state가 정합성 검사를 거친 최종 동기화 상태다.

---

## **8.2 World State 업데이트 시점**

Action 실행 후 World State는 다음 단계로 관리한다.

ApprovedAction created  
→ expected\_mutated\_state recorded  
→ ExecutionRequest created  
→ pending\_state applied  
→ Feedback received  
→ confirmed\_state updated  
→ reconciliation performed  
→ reconciled\_state committed

예:

ACTION\_DISABLE\_ROBOT\_MISSION

상태 흐름:

current\_state \= MissionStatus.ACTIVE  
expected\_mutated\_state \= MissionStatus.DISABLED  
pending\_state \= MissionStatus.DISABLE\_REQUESTED  
confirmed\_state \= MissionStatus.DISABLED after feedback  
reconciled\_state \= MissionStatus.DISABLED after reconciliation

---

## **8.3 Feedback 이전의 pending\_state 관리**

Feedback이 오기 전까지 platform은 최종 상태가 아니라 pending state를 유지해야 한다.

예:

ACTION\_LOCK\_ZONE

상태 흐름:

current\_state \= AccessState.OPEN  
expected\_mutated\_state \= AccessState.LOCKED  
pending\_state \= AccessState.LOCK\_REQUESTED

이때 platform은 Zone\_A가 이미 LOCKED 되었다고 단정하면 안 된다.

대신 다음처럼 표현해야 한다.

Zone\_A access lock requested, awaiting confirmation.

---

## **8.4 Reconciliation 실패 처리**

Feedback과 expected\_mutated\_state가 일치하지 않으면 reconciliation failure로 처리한다.

예:

기대한 상태:

MissionStatus.DISABLED

실제 feedback:

MissionStatus.STILL\_ACTIVE

처리:

reconciliation.status \= FAILED  
execution\_state \= RECOVERY\_REQUIRED  
world\_state \= STATE\_CONFLICT\_DETECTED  
manual\_review\_required \= true

필요한 후속 조치:

Recovery action 생성  
Supervisor notification  
Manual override request  
Audit record update  
Policy review if repeated

---

# **9\. 비동기 Execution State Model**

물리 세계는 비동기적이다.

로봇, SCADA, PLC, access control, mobile notification, smart helmet alert는 요청을 받은 즉시 완료되지 않는다.

따라서 ExecutionRequest 이후의 중간 상태를 명확히 관리해야 한다.

## **9.1 핵심 Execution States**

권장 핵심 상태는 다음과 같다.

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

## **9.2 상태 의미**

`CREATED`  
ExecutionRequest가 생성된 상태다.

`DISPATCHED`  
외부 system으로 요청이 전송되었다.

`ACKNOWLEDGED`  
외부 system이 요청 수신을 확인했다.

`ACCEPTED`  
외부 system이 요청을 수행 대상으로 수락했다.

`IN_PROGRESS`  
수행 중이다.

`PARTIAL_SUCCESS`  
일부 target에는 성공했지만 전체 완료는 아니다.

`COMPLETED`  
요청된 action이 완료되었다.

`FAILED`  
수행 실패다.

`TIMEOUT`  
정해진 시간 안에 응답이 오지 않았다.

`FEEDBACK_MISSING`  
dispatch 이후 feedback이 누락되었다.

`RECOVERY_REQUIRED`  
복구 절차가 필요하다.

`MANUAL_OVERRIDE_REQUIRED`  
사람 개입이 필요하다.

`CLOSED`  
execution lifecycle이 종료되었다.

---

## **9.3 Feedback Requirement와 Execution State 연결**

`ACK_REQUIRED`  
최소 `ACKNOWLEDGED` 상태가 필요하다.

`ACCEPTANCE_REQUIRED`  
최소 `ACCEPTED` 상태가 필요하다.

`PROGRESS_REQUIRED`  
`IN_PROGRESS` 또는 그 이후 상태가 필요하다.

`COMPLETION_REQUIRED`  
`COMPLETED` 상태가 필요하다.

`STATE_CHANGE_REQUIRED`  
World State 또는 KG에서 expected\_mutated\_state와 일치하는 confirmed state가 필요하다.

`HUMAN_CONFIRMATION_REQUIRED`  
사람의 확인 event가 필요하다.

`POST_HOC_AUDIT_REQUIRED`  
PostHocAudit completed 상태가 필요하다.

---

# **10\. Event-to-Action Mapping Rule**

Event Type은 Action Type을 직접 실행하지 않는다.

Event Type은 ActionCandidate를 생성할 수 있는 조건을 제공할 뿐이다.

따라서 Event-to-Action Mapping은 다음 구조를 가져야 한다.

## **10.1 Mapping Table 필드**

권장 필드:

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

## **10.2 Mapping 예시 1: 위험 구역 진입**

Event Type:

safety.worker.entered\_danger\_zone

Candidate Action Types:

ACTION\_NOTIFY\_SUPERVISOR  
ACTION\_STOP\_WORK  
ACTION\_EVACUATE\_ZONE

조건:

작업자가 위험 구역에 있고, 장비가 active 상태이며, 허가가 없거나 clearance가 부족한 경우.

---

## **10.3 Mapping 예시 2: 가스 임계값 초과**

Event Type:

safety.gas.critical\_threshold\_exceeded

Candidate Action Types:

ACTION\_EMERGENCY\_EVACUATE\_ZONE  
ACTION\_EMERGENCY\_TRIGGER\_ALARM  
ACTION\_EMERGENCY\_LOCK\_ZONE

조건:

가스 농도가 critical threshold를 초과했고, 해당 zone에 작업자 또는 로봇이 존재하는 경우.

---

## **10.4 Mapping 예시 3: 로봇 미션 차단**

Event Type:

robot.mission.blocked

Candidate Action Types:

ACTION\_NOTIFY\_OPERATOR  
ACTION\_REPLAN\_ROBOT\_MISSION  
ACTION\_DISABLE\_ROBOT\_MISSION

조건:

로봇이 지정 시간 이상 blocked 상태이고, mission timeout이 임박한 경우.

---

# **11\. Idempotency 책임 경계**

Idempotency는 물리적 중복 실행을 막기 위한 핵심 장치다.

특히 physical action, emergency action, external system request는 idempotency가 필수다.

---

## **11.1 Core 책임**

Platform Core는 idempotency\_key를 생성한다.

권장 생성 기준:

idempotency\_key \= hash(  
  approved\_action\_id,  
  action\_type,  
  target\_ref,  
  trace\_id,  
  idempotency\_scope,  
  lifecycle\_version  
)

MVP에서는 다음을 사용할 수 있다.

idempotency\_key \= ApprovedActionID

Core는 다음을 보장해야 한다.

같은 ApprovedAction에서 중복 ExecutionRequest가 생성되지 않도록 한다.  
ExecutionRequestDTO에 idempotency\_key를 포함한다.  
AuditRecordDTO에 idempotency\_key를 기록한다.  
Timeout, Retry, Recovery에서도 동일 idempotency\_key를 유지한다.

---

## **11.2 Adapter 책임**

Adapter는 core에서 받은 idempotency\_key를 외부 system에 전달한다.

외부 system이 idempotency를 지원하면 해당 key를 그대로 사용한다.

외부 system이 idempotency를 지원하지 않으면 adapter 내부에서 deduplication table을 운영해야 한다.

Adapter는 다음을 보장해야 한다.

같은 idempotency\_key의 중복 요청을 감지한다.  
외부 API retry 시 같은 key를 유지한다.  
중복 dispatch 여부를 feedback으로 반환한다.  
중복 실행 가능성이 있으면 RECOVERY\_REQUIRED 또는 MANUAL\_OVERRIDE\_REQUIRED로 전환한다.

---

## **11.3 External System 책임**

External system이 idempotency를 지원하는 경우:

동일 idempotency\_key에 대해 동일 결과를 반환해야 한다.  
중복 command를 실제로 재실행하지 않아야 한다.  
이미 완료된 요청이면 completed 또는 already\_processed 상태를 반환해야 한다.

External system이 idempotency를 지원하지 않는 경우:

Core와 Adapter가 retry를 보수적으로 제한해야 한다.

---

## **11.4 idempotency\_scope**

`idempotency_scope`는 중복 방지 범위를 의미한다.

값 예:

PER\_APPROVED\_ACTION  
PER\_TARGET  
PER\_ZONE  
PER\_MISSION  
PER\_ROBOT  
PER\_WORKER  
PER\_EXTERNAL\_SYSTEM  
PER\_EMERGENCY\_INCIDENT  
PER\_NOTIFICATION\_RECIPIENT

예:

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

# **12\. Action Type Registry 운영 정책**

Action Type Registry는 단순 목록이 아니라 governance 대상이다.

잘못된 action type은 잘못된 실행 요청으로 이어질 수 있으므로 Event Type Registry보다 더 엄격하게 관리해야 한다.

---

## **12.1 ActionTypeSpecDTO Canonical Fields**

권장 필드:

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

Action Type은 다음 status를 가질 수 있다.

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
→ 신규 action 생성 금지

BLOCKED  
→ 보안, 안전, 법적 문제로 차단

---

## **12.3 Registry Versioning**

Action Type은 version을 가져야 한다.

Backward-compatible change:

description 추가  
allowed\_event\_types 추가  
expected\_feedback\_types 추가  
timeout\_policy 보강  
retry\_policy 보강  
metadata 추가

Breaking change:

action\_type 이름 변경  
risk\_level 의미 변경  
approval\_level 변경  
requires\_safety\_gate 제거  
requires\_post\_hoc\_audit 제거  
allowed\_target\_types 변경  
execution\_mode 변경  
external system route 변경  
expected\_mutated\_state 의미 변경  
idempotency\_scope 변경

Breaking change는 새 action\_type으로 분리하는 것이 원칙이다.

---

## **12.4 Approval Process**

Action Type 변경은 반드시 owner와 domain steward의 승인을 받아야 한다.

권장 승인 주체:

Domain Owner  
Ontology Steward  
Safety Owner  
Policy Owner  
Platform Architect  
External Adapter Owner  
Legal / Compliance Owner

고위험 action과 emergency action은 Safety Owner, Policy Owner, Platform Architect 승인이 필수다.

---

## **12.5 Deprecation Policy**

Action Type을 바로 삭제하지 않는다.

권장 절차:

DEPRECATED 상태로 변경  
replacement\_action\_type 지정  
dual-read / dual-write 기간 운영  
downstream consumer migration  
audit compatibility 확인  
RETIRED 상태로 변경  
major version에서 제거 가능

---

## **12.6 Registry Compatibility Rule**

과거 action record는 항상 재해석 가능해야 한다.

따라서 ApprovedActionDTO와 AuditRecordDTO는 action\_type뿐 아니라 action\_type\_version도 참조해야 한다.

---

# **13\. Emergency Action Registry**

Emergency Action은 일반 Action Type보다 더 강한 governance를 가져야 한다.

Emergency Action은 빠르게 실행될 수 있지만, 아무 action이나 emergency path에 들어갈 수 없다.

Emergency Action은 사전에 등록되고 검증된 action만 허용한다.

---

## **13.1 Emergency Action 조건**

Emergency Action은 다음 조건을 가져야 한다.

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

## **13.2 Emergency Action 예**

ACTION\_EMERGENCY\_STOP  
ACTION\_EMERGENCY\_EVACUATE\_ZONE  
ACTION\_EMERGENCY\_TRIGGER\_ALARM  
ACTION\_EMERGENCY\_LOCK\_ZONE  
ACTION\_EMERGENCY\_DISABLE\_ROBOT\_MISSION

---

## **13.3 Emergency Action Rule**

Emergency Action은 LLM이 직접 만들 수 없다.

LLM 또는 agent는 emergency situation을 설명하거나 ActionCandidate를 제안할 수 있다.

하지만 EmergencyApprovedAction은 반드시 registry, deterministic rule, local policy, safety validation을 통과해야 한다.

---

# **14\. Vendor / External Adapter Action Pattern**

외부 시스템은 각자 다른 명령 구조를 가진다.

예:

Robot Fleet Manager  
ROS2 Bridge  
SCADA  
PLC Gateway  
Access Control System  
Smart Helmet Alert System  
Mobile Notification Service  
Inspection Platform

Core Action Type은 외부 command detail을 직접 포함하지 않는다.

Core Action Type은 표준 action 의미만 정의한다.

External Adapter가 Action Type을 vendor-specific command로 변환한다.

예:

Core Action Type:

ACTION\_DISABLE\_ROBOT\_MISSION

Adapter Translation:

FleetManager.disable\_mission(robot\_id, mission\_id)

또는:

ROS2 service call

또는:

Vendor REST API request

이 구조는 core registry가 vendor detail로 오염되는 것을 막는다.

---

# **15\. Post-hoc Audit Rule**

Emergency Action 또는 high-risk action은 post-hoc audit을 가져야 한다.

기본 흐름:

ApprovedAction created  
→ ExecutionRequest created  
→ Feedback received  
→ PostHocAudit pending  
→ PostHocAudit completed

문제가 있는 경우:

PostHocAudit pending  
→ PostHocAudit escalated

또는:

PostHocAudit completed  
→ Policy updated

또는:

PostHocAudit completed  
→ ActionType deprecated

원칙:

빠르게 실행된 action일수록 사후 감사는 더 강해야 한다.  
사후 감사가 닫히지 않은 emergency action은 lifecycle이 완전히 종료된 것으로 보지 않는다.

---

# **16\. MVP Action Type Set**

전체 action type 목록은 Appendix B에서 관리한다.

MVP에서는 다음 action type만 우선 등록한다.

## **16.1 Safety MVP Actions**

ACTION\_NOTIFY\_SUPERVISOR  
ACTION\_STOP\_WORK  
ACTION\_EVACUATE\_ZONE  
ACTION\_LOCK\_ZONE  
ACTION\_TRIGGER\_LOCAL\_ALARM

## **16.2 Emergency MVP Actions**

ACTION\_EMERGENCY\_STOP  
ACTION\_EMERGENCY\_EVACUATE\_ZONE  
ACTION\_EMERGENCY\_TRIGGER\_ALARM  
ACTION\_EMERGENCY\_LOCK\_ZONE  
ACTION\_EMERGENCY\_DISABLE\_ROBOT\_MISSION

## **16.3 Robot MVP Actions**

ACTION\_NOTIFY\_OPERATOR  
ACTION\_DISABLE\_ROBOT\_MISSION  
ACTION\_REPLAN\_ROBOT\_MISSION  
ACTION\_RETURN\_ROBOT\_TO\_SAFE\_ZONE

## **16.4 Construction MVP Actions**

ACTION\_REQUEST\_INSPECTION  
ACTION\_HOLD\_TASK  
ACTION\_RESUME\_TASK  
ACTION\_REQUEST\_PERMIT\_REVIEW

## **16.5 Governance MVP Actions**

ACTION\_REQUEST\_APPROVAL  
ACTION\_ESCALATE\_TO\_SAFETY\_MANAGER  
ACTION\_ESCALATE\_TO\_WAR\_ROOM  
ACTION\_CREATE\_MAPPING\_REVIEW

## **16.6 Notification MVP Actions**

ACTION\_SEND\_MOBILE\_ALERT  
ACTION\_SEND\_DASHBOARD\_ALERT  
ACTION\_SEND\_SMART\_HELMET\_ALERT

---

# **17\. Appendix B: Action Type Catalog 분리 기준**

Action Category별 상세 목록은 본문에 모두 넣지 않는다.

다음 항목은 Appendix B에서 관리한다.

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

이렇게 해야 Core 문서가 길어지지 않는다.

---

# **18\. 권장 파일 구조**

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

# **19\. 우선 구현 순서**

MVP 구현 순서는 다음이 좋다.

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
MVP action type constants  
ActionType validation function  
ActionCandidateDTO와 연결  
ApprovedActionDTO와 연결  
ExecutionRequestDTO와 연결  
FeedbackEventDTO와 연결

---

# **21\. 최종 원칙**

Action Type Registry는 플랫폼의 표준 대응 언어다.

Event Type은 원인이다.  
Action Type은 대응이다.  
ActionCandidate는 제안이다.  
ApprovedAction은 승인된 조치다.  
ExecutionRequest는 외부 시스템으로 나가는 요청이다.  
Feedback은 실행 결과를 확인하는 증거다.  
PostHocAudit은 고위험 또는 비상 조치의 사후 책임 경계다.

Action이 성공했다고 가정하면 안 된다.  
Action은 expected\_mutated\_state를 가질 수 있다.  
하지만 실제 상태 변경은 feedback과 reconciliation으로 확인해야 한다.

Idempotency는 Core에서 시작하고 Adapter에서 보장된다.  
외부 system이 지원하면 external idempotency까지 연결한다.  
지원하지 않으면 adapter가 보수적으로 중복 실행을 막아야 한다.

최종 원칙은 다음과 같다.

Different events, one action language.  
Different risks, one approval model.  
Different targets, one ontology-aware mutation model.  
Different systems, one execution boundary.  
Different feedback delays, one execution state model.  
Different vendors, one adapter pattern.  
Different retries, one idempotency discipline.  
Different emergencies, one post-hoc audit discipline.

