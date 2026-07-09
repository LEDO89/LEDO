# 

## **From Raw Input to Approved Action and Feedback**

---

## **0\. Document Control**

Document Name: Ontology-Centric Canonical Object Lifecycle  
Version: v1.0  
Status: Architecture Specification Draft  
Scope: Ontology-centered cyber-physical platform, industrial data, construction workflow, robot fleet, LLM/RAG output, human approval, and external control integration  
Primary Goal: Define how heterogeneous inputs become semantic events, evidence, world state, action candidates, approved actions, execution requests, feedback, and audit records.

### **Versioning Policy**

This lifecycle specification must be versioned.

Recommended versioning:

v1.0  
Initial canonical lifecycle definition

v1.1  
Backward-compatible additions such as new event types, optional fields, monitoring metrics, or non-breaking validation rules

v2.0  
Breaking changes such as lifecycle state changes, object schema restructuring, required field changes, or new execution boundary semantics

### **Compatibility Rule**

A newer lifecycle version must not silently break old event records, audit trails, policy decisions, or execution history.

Every lifecycle object should include:

schema\_version  
lifecycle\_version  
ontology\_version  
policy\_bundle\_version  
created\_at\_utc  
trace\_id

---

# **1\. Executive Summary**

This document defines the canonical object lifecycle for an ontology-centric cyber-physical platform.

The purpose of this lifecycle is to transform heterogeneous inputs from industrial equipment, sensors, robots, construction workflows, human workers, mobile devices, LLM/RAG systems, documents, and external control systems into one unified semantic flow.

The default lifecycle is:

RawInput  
→ CanonicalEventEnvelope  
→ Canonicalization  
→ OntologyBoundEvent  
→ Evidence  
→ WorldStateUpdate  
→ ActionCandidate  
→ DecisionCase  
→ PolicyEvaluation  
→ ApprovalRequest  
→ ApprovalDecision  
→ ApprovedAction  
→ RuntimeValidationInput  
→ RuntimeValidationResult  
→ Safety Gate  
→ SafetyGatePass or SafetyGateBlock  
→ ExecutionRequest  
→ ExternalControlRequest  
→ External System  
→ FeedbackEvent  
→ AuditRecord  
→ World State Update

However, in production environments, not every event should follow the same heavyweight lifecycle.

Therefore, this architecture explicitly defines three paths:

1. Standard Semantic Lifecycle  
   The standard path for semantic interpretation, evidence validation, policy decisioning, approval, execution, feedback, and audit.  
2. Emergency Fast-Path / Brake-Glass Lifecycle  
   A deterministic, pre-approved safety path for critical emergency situations, allowing immediate safety actions after minimal validation.  
3. Lightweight / Monitoring-Only Lifecycle  
   A lightweight path for high-frequency, low-risk sensor data, status monitoring, and simple telemetry updates.

The core philosophy is:

Raw input is not truth.  
LLM output is not truth.  
Human request is not an executable command.  
Sensor alarm is not a direct command.  
ActionCandidate is not an execution command.  
Only ApprovedAction may enter the execution lifecycle.  
ExecutionRequest is not physical control; it is a high-level approved request.  
Dispatch is not completion.  
Feedback and audit close the lifecycle.

---

# **2\. Core Non-Negotiable Rules**

To reduce repetition, all core rules are centralized in this section.

## **Rule 1\. Raw Input Is Not Truth**

RawInput is not operational fact.

RawInput becomes operational fact only after normalization, canonicalization, ontology binding, evidence validation, freshness checking, confidence assignment, and trace attachment.

## **Rule 2\. Binding Gives Meaning**

Ontology Binding gives meaning to data.

Example:

CR-001  
→ construction:Crane\_01

MODE  
→ industrial:hasOperationMode

LIFTING  
→ industrial:LiftingMode

## **Rule 3\. Grounding Gives Evidence**

Grounding attaches real-world evidence to decisions and candidate actions.

Evidence must include source, timestamp, confidence, freshness, and traceability.

## **Rule 4\. LLM Output Is Not Truth**

LLM/RAG output is not truth.

LLM/RAG output may be one of the following:

Intent  
Candidate  
Explanation  
EvidenceSummary  
MappingProposal  
RiskInterpretation

LLM/RAG output must not directly become ApprovedAction, ExecutionRequest, or ExternalControlRequest.

## **Rule 5\. ActionCandidate Is Not Command**

ActionCandidate is not an execution command.

ActionCandidate must pass through the Decision Router, policy evaluation, and approval workflow before it can become an ApprovedAction.

Only an ApprovedAction may enter Runtime Validation and Safety Gate evaluation for execution readiness.

## **Rule 6\. ApprovedAction Is the Execution Boundary**

ApprovedAction is the first object allowed to enter the execution lifecycle.

No object before ApprovedAction may be executed.

## **Rule 7\. ExecutionRequest Is Not Low-Level Control**

ExecutionRequest is a high-level approved request sent to an external control system.

Robot motor control, PLC ladder logic, SCADA internal control, and equipment sequence control remain the responsibility of specialized external control systems.

## **Rule 8\. Dispatch Is Not Completion**

An ExternalControlRequest being dispatched does not mean the execution is complete.

Completion requires FeedbackEvent and WorldState Reconciliation.

## **Rule 9\. Physical Rollback Is Impossible**

The physical world cannot be rolled back.

Post-failure handling is not rollback. It is one of the following:

safe-state transition  
compensating action  
recovery workflow  
manual override  
post-failure audit  
state reconciliation

## **Rule 10\. No Audit, No Trust**

High-risk decisions, emergency actions, external control requests, and physical execution lifecycles must be auditable.

If it cannot be audited, it should not be trusted.

---

# **3\. Lifecycle Paths**

## **3.1 Standard Semantic Lifecycle**

The Standard Path is the normal path for semantic interpretation, decisioning, approval, and execution.

RawInput  

→ CanonicalEventEnvelope
→ Canonicalization
→ OntologyBoundEvent
→ Evidence
→ WorldStateUpdate
→ ActionCandidate
→ DecisionCase
→ PolicyEvaluation
→ ApprovalRequest
→ ApprovalDecision
→ ApprovedAction
→ RuntimeValidationInput
→ RuntimeValidationResult
→ Safety Gate
→ SafetyGatePass or SafetyGateBlock
→ ExecutionRequest
→ ExternalControlRequest
→ FeedbackEvent
→ AuditRecord
→ World State Update

Example use cases:

Expired work permit  
Abnormal equipment state  
Delayed robot mission  
Restricted zone access  
Failed inspection result  
LLM-based action proposal  
Work-stop candidate generation  
Robot rerouting candidate generation

## **3.2 Emergency Fast-Path / Brake-Glass Lifecycle**

The Emergency Fast-Path is an ultra-low-latency safety path for Critical Emergency situations.

RawInput  

→ CanonicalEventEnvelope
→ Emergency Classification Check
→ Minimal Target Binding
→ Deterministic Safety Rule
→ Local Emergency Policy Check
→ EmergencyApprovedAction
→ RuntimeValidationInput
→ RuntimeValidationResult
→ Emergency Safety Gate Decision
→ EmergencySafetyGatePass or EmergencySafetyGateBlock
→ EmergencyExecutionRequest
→ ExternalControlRequest
→ FeedbackEvent
→ Post-hoc Ontology Binding
→ AuditRecord
→ World State Update

Example use cases:

Critical gas threshold exceeded  
Imminent robot collision  
Worker fall detected  
Fire detected  
Emergency stop button pressed  
Worker detected inside crane hazard radius  
PLC critical safety alarm

Important principle:

Emergency Fast-Path is not a Safety Gate bypass.  
Emergency Fast-Path is a pre-approved deterministic safety lane that still requires minimum deterministic Runtime Validation, an emergency Safety Gate pass/block decision, and post-hoc audit.

It is not a path where AI can invent and execute emergency actions on the fly.

## **3.3 Lightweight / Monitoring-Only Lifecycle**

Sending every high-frequency sensor update or low-risk telemetry signal through the full Standard Path is inefficient.

Therefore, a monitoring-only path is required.

RawInput  
→ CanonicalEventEnvelope  
→ Lightweight Canonicalization  
→ Basic Ontology Binding or Known Source Mapping  
→ WorldStateUpdate  
→ Metric / Trend / Dashboard Update  
→ Optional Audit Sampling

Example use cases:

Normal-range temperature sensor updates  
Minor vibration value changes  
Robot battery state updates  
Equipment heartbeat  
Low-risk telemetry  
Repeated sensor values with no state change  
Live metrics for dashboards

The Monitoring-Only Path may be used when:

The event is below risk threshold  
No action candidate is required  
No policy decision is required  
Only state update or trend update is required  
Evidence-grade preservation is unnecessary or audit sampling is sufficient  
The source is known and trusted  
The schema is stable

However, a Monitoring-Only event must be escalated to the Standard Path or Emergency Path when any of the following occurs:

Threshold exceeded  
State anomaly detected  
Sensor freshness failure  
Source trust degradation  
Critical asset heartbeat loss  
High-risk zone involvement  
Worker proximity risk  
Equipment fault signal

---

# **4\. Canonical Object Lifecycle**

## **4.1 RawInput**

RawInput is the first representation of incoming information.

Examples:

industrial sensor byte stream  
PLC tag value  
SCADA event  
Modbus register  
OPC-UA node update  
MQTT message  
robot telemetry  
fleet manager feedback  
construction task update  
permit status update  
inspection result  
worker mobile input  
supervisor approval  
LLM structured output  
RAG result  
document parser output  
vision detection  
manual operator request

RawInput cannot directly become an execution object.

## **4.2 CanonicalEventEnvelope**

CanonicalEventEnvelope is the common wrapper for all incoming events.

Recommended fields:

event\_id  
event\_type  
source\_type  
source\_id  
subject\_type  
subject\_id  
timestamp\_utc  
ingested\_at\_utc  
location\_ref  
payload  
confidence  
freshness\_ms  
trace\_id  
correlation\_id  
schema\_version  
lifecycle\_version  
source\_protocol  
raw\_ref  
tenant\_id  
site\_id  
emergency\_hint  
criticality\_hint

CanonicalEventEnvelope is the first branching point for the Standard Path, Emergency Fast-Path, and Monitoring-Only Path.

## **4.3 Canonicalization**

Canonicalization converts multiple local names, aliases, tags, IDs, and labels into one official platform identity.

Example:

CR-001  
Crane01  
TowerCrane-A  
?�비10045  
crane\_main\_01

→ construction:Crane\_01

Possible failure states:

UNCLASSIFIED\_ENTITY\_DETECTED  
BINDING\_PENDING  
QUARANTINED\_EVENT  
MAPPING\_REVIEW\_REQUIRED

Canonicalization failure does not mean full system shutdown.

However, an unclassified object must not directly participate in a high-risk execution path.

## **4.4 OntologyBoundEvent**

OntologyBoundEvent is a canonical event linked to ontology classes, properties, individuals, and relations.

Binding targets:

ontology class  
ontology property  
ontology individual  
canonical IRI  
runtime key  
domain module  
relation type  
action type  
state type  
evidence type

Example:

CR-001 MODE \= LIFTING

CR-001  
→ construction:Crane\_01

MODE  
→ industrial:hasOperationMode

LIFTING  
→ industrial:LiftingMode

Crane\_01  
→ industrial:HeavyEquipment

## **4.5 Evidence**

Evidence is information that can support a decision, state change, action candidate, approval, execution request, or audit record.

Evidence types:

SensorEvidence  
TelemetryEvidence  
PLCEventEvidence  
SCADAEventEvidence  
RobotFeedbackEvidence  
InspectionEvidence  
PhotoEvidence  
DocumentEvidence  
PermitEvidence  
HumanApprovalEvidence  
MobileAuthenticationEvidence  
LocationEvidence  
LLMEvidenceSummary

LLMEvidenceSummary is not direct evidence.

LLM may summarize evidence, but actual evidence must come from sensors, documents, logs, human approval, robot feedback, or verified records.

## **4.6 WorldStateUpdate**

WorldStateUpdate changes the current operational state based on ontology-bound events and evidence.

Examples:

Zone\_A.risk\_state \= high  
Worker\_17.location \= Zone\_A  
Robot\_07.mission\_status \= blocked  
Crane\_01.mode \= lifting  
Permit\_33.status \= expired  
Sensor\_17.status \= offline  
Equipment\_04.availability \= unavailable

World State fields:

state\_value  
source\_ref  
evidence\_ref  
timestamp\_utc  
freshness\_ms  
confidence  
valid\_until  
last\_updated\_by  
trace\_id  
version

World State is the runtime view of current state.

Ontology defines meaning.  
Evidence supports state changes.  
World State stores current operational state.

## **4.7 ActionCandidate**

ActionCandidate is a proposed action generated by an agent, rule engine, ML model, LLM, operator request, or workflow logic.

Sources:

Safety Agent  
Robot Agent  
Equipment Agent  
Inspection Agent  
Compliance Agent  
Rule Engine  
LLM / RAG  
Human Operator  
Supervisor Request  
Workflow Engine  
External Alarm

Action types:

ACTION\_NOTIFY  
ACTION\_STOP\_WORK  
ACTION\_EVACUATE\_ZONE  
ACTION\_LOCK\_ZONE  
ACTION\_REQUEST\_INSPECTION  
ACTION\_DISPATCH\_ROBOT  
ACTION\_REPLAN\_ROUTE  
ACTION\_RESUME\_WORK  
ACTION\_ESCALATE\_TO\_SUPERVISOR  
ACTION\_EMERGENCY\_STOP

## **4.8 DecisionCase**

DecisionCase classifies an ActionCandidate by risk, urgency, routing path, approval requirement, and escalation policy.

Decision tiers:

Routine  
Notice  
Warning  
High Risk  
Critical Emergency  
Exceptional

DecisionCase should include:

standard\_path  
emergency\_fast\_path  
monitoring\_only\_path  
approval\_required  
approval\_bypass\_allowed\_by\_policy  
manual\_review\_required  
binding\_incomplete  
evidence\_insufficient  
state\_stale  
adapter\_unavailable

## **4.9 ApprovalRequest**

ApprovalRequest is created when a DecisionCase requires human approval or authority validation.

Approval types:

NoApprovalRequired  
SupervisorApproval  
SafetyManagerApproval  
WarRoomApproval  
EmergencyPolicyBypass  
ExpertReviewRequired  
ManualOverrideRequired

Human approval alone is not enough.

Even approved requests must pass through the Safety Gate.

## **4.10 ApprovedAction**

ApprovedAction is an action created after the required policy and approval path grants authority for execution preparation.

ApprovedAction is not a SafetyGatePass.

ApprovedAction is not eligible to create an ExecutionRequest until Runtime Validation has produced a valid RuntimeValidationResult and the Safety Gate has issued a valid SafetyGatePass.

Required authority and preparation checks:

ontology valid  
action type valid  
target exists  
target type allowed  
evidence sufficient  
state fresh  
policy allowed  
approval valid  
capability available  
risk acceptable  
external adapter available  
expected feedback defined  
trace context attached  
idempotency key generated  
timeout policy defined  
recovery policy defined

## **4.11 EmergencyApprovedAction**

EmergencyApprovedAction may be created in the Emergency Fast-Path.

EmergencyApprovedAction is not a SafetyGatePass and must not create an EmergencyExecutionRequest unless deterministic emergency Runtime Validation and an emergency Safety Gate decision produce a valid pass.

Allowed emergency action examples:

ACTION\_EMERGENCY\_STOP  
ACTION\_EVACUATE\_ZONE  
ACTION\_NOTIFY\_EMERGENCY  
ACTION\_LOCK\_ZONE  
ACTION\_DISABLE\_ROBOT\_MISSION  
ACTION\_TRIGGER\_LOCAL\_ALARM

EmergencyApprovedAction must include:

emergency\_policy\_id  
emergency\_condition\_id  
minimal\_evidence\_refs  
local\_rule\_result  
idempotency\_key  
timeout\_policy  
expected\_feedback  
post\_hoc\_audit\_required

## **4.12 ExecutionRequest**

ExecutionRequest is created by the Unified Cyber-Physical Core from an ApprovedAction or EmergencyApprovedAction.

ExecutionRequest creation requires a valid SafetyGatePass or emergency SafetyGatePass bound to the same action, target, trace context, and idempotency key.

ExecutionRequest represents high-level approved intent.

Recommended fields:

execution\_request\_id  
approved\_action\_id  
action\_type  
target  
external\_system\_type  
external\_system\_id  
execution\_constraints  
expected\_feedback  
timeout\_policy  
retry\_policy  
recovery\_policy  
idempotency\_key  
execution\_lease  
trace\_id  
created\_at\_utc

ExecutionRequest must not contain direct robot motor commands, PLC ladder logic, or machine sequence instructions.

## **4.13 ExternalControlRequest**

ExternalControlRequest is an adapter-specific request.

Targets:

Fleet Manager  
Robot Middleware  
ROS2 Bridge  
PLC  
SCADA  
Equipment Controller  
Smart Helmet Alert System  
Mobile Notification System  
Site Operation Platform  
Inspection Platform  
Access Control System  
Alarm System

ExternalControlRequest must preserve approved intent, constraints, idempotency, trace ID, expected feedback, and timeout policy.

## **4.14 FeedbackEvent**

FeedbackEvent is the structured response returned from an external control system, physical system, human operator, robot, sensor, PLC, SCADA, or mobile device.

Feedback types:

Acknowledged  
Accepted  
Rejected  
Started  
InProgress  
Completed  
Failed  
Timeout  
Cancelled  
Blocked  
UnsafeStateDetected  
RecoveryRequired  
RecoveryStarted  
RecoveryCompleted  
ManualOverrideRequired  
WorkerAcknowledged  
ZoneCleared  
RobotBlocked  
EquipmentFault  
ExternalSystemOffline  
FeedbackMissing  
FeedbackDelayed  
FeedbackConflict

## **4.15 AuditRecord**

AuditRecord is the final traceable record of the lifecycle.

Audit must answer:

What was the original input?  
What event was created?  
Which lifecycle path was used?  
Was the Emergency Fast-Path used?  
Was it a Monitoring-Only Path?  
What ontology meaning was assigned?  
Did binding fail?  
Was an UnclassifiedEntity created?  
What evidence was used?  
What world state changed?  
Who or what generated the candidate?  
How was the decision routed?  
Was human approval required?  
Who approved it?  
What policy was applied?  
Did the Safety Gate pass or reject it?  
What ApprovedAction, RuntimeValidationResult, and SafetyGatePass or SafetyGateBlock were created?  
What ExecutionRequest was created?  
Which external system received the request?  
Did a timeout occur?  
Was recovery required?  
What feedback came back?  
Was the final state updated?

---

# **5\. Emergency Action Registry Governance**

Emergency Fast-Path only allows pre-registered emergency actions.

Therefore, an Emergency Action Registry is required.

## **5.1 Registry Contents**

Emergency Action Registry should include:

emergency\_action\_type  
emergency\_condition\_type  
allowed\_target\_types  
required\_minimal\_evidence  
local\_rule\_id  
policy\_id  
allowed\_external\_systems  
required\_feedback  
timeout\_policy  
recovery\_policy  
audit\_level  
approval\_model  
version  
owner  
valid\_from  
valid\_until

## **5.2 Approval Authority**

The creation, modification, and deprecation of emergency actions must be approved by:

Safety Committee  
Ontology Steward  
Policy Owner  
Site Operations Owner  
Control System Owner  
Security Owner

Any action connected to high-risk physical execution must not be registered by a single developer alone.

## **5.3 Change Process**

Emergency Action Registry change process:

1. Create change proposal  
2. Perform hazard analysis  
3. Review ontology impact  
4. Review policy impact  
5. Review external control impact  
6. Run simulation test  
7. Perform site-specific validation  
8. Obtain Safety Committee approval  
9. Obtain Ontology Steward approval  
10. Update policy bundle  
11. Deploy to edge  
12. Run canary validation  
13. Roll out fully  
14. Create audit record

## **5.4 Deprecation Process**

Emergency action deprecation process:

1. Record deprecation reason  
2. Define replacement action  
3. Review backward compatibility  
4. Update edge nodes  
5. Disable old action  
6. Preserve audit and rollback plan

## **5.5 Rule**

Emergency actions are fast, therefore they must be governed more strictly.

The speed of the Emergency Fast-Path is earned through prior governance.

---

# **6\. LLM/RAG Governance and Context Poisoning Defense**

LLM/RAG is a proposer, not an executor.

## **6.1 Allowed Roles**

LLM/RAG may produce:

Intent  
ActionCandidate  
Explanation  
EvidenceSummary  
MappingProposal  
RiskInterpretation  
DocumentSummary  
PolicyImpactSuggestion

## **6.2 Forbidden Roles**

LLM/RAG must not directly produce:

ApprovedAction  
EmergencyApprovedAction  
ExecutionRequest  
ExternalControlRequest  
PLC command  
Robot motion command  
SCADA command  
Machine sequence instruction  
Emergency bypass decision

## **6.3 Hallucination Defense**

All LLM/RAG outputs must be checked by:

ontology guard  
schema validator  
evidence validator  
policy validator  
source verifier  
human approval if required  
Safety Gate

## **6.4 Context Poisoning Defense**

RAG and context systems can be attacked or polluted.

Defense mechanisms:

source trust scoring  
document provenance tracking  
versioned document registry  
approved document whitelist  
stale document detection  
conflicting evidence detection  
prompt injection filtering  
retrieval boundary control  
policy-controlled tool access  
human review for high-risk proposals

## **6.5 Rule**

LLM/RAG output can support decision-making, but it cannot replace deterministic policy, evidence grounding, approval, or Safety Gate validation.

---

# **7\. Ontology Drift and Self-Healing Governance**

Field equipment, tags, sensors, robots, firmware, and work zones change continuously.

This creates ontology drift.

## **7.1 Drift Sources**

new sensor model  
new equipment type  
firmware update  
tag name change  
UNS topic change  
zone renaming  
new robot capability  
new contractor workflow  
new permit type  
document schema change

## **7.2 Failure States**

UNCLASSIFIED\_ENTITY\_DETECTED  
UNMAPPED\_SIGNAL\_DETECTED  
BINDING\_PENDING  
MAPPING\_REVIEW\_REQUIRED  
ONTOLOGY\_VERSION\_MISMATCH  
POLICY\_CONTEXT\_STALE

## **7.3 Self-Healing Loop**

1. Binding failure detected  
2. Event is preserved, not discarded  
3. Temporary UnclassifiedEntity is created  
4. High-risk execution path is blocked  
5. Monitoring-only visibility is allowed if safe  
6. LLM/RAG mapping assistant generates proposal  
7. Ontology Steward reviews proposal  
8. Human approval is required  
9. Mapping table is updated with version  
10. Ontology registry is updated  
11. Policy bundle is regenerated if needed  
12. Edge context is refreshed  
13. Previous events may be reprocessed if necessary

## **7.4 Rule**

Self-healing means assisted mapping, not autonomous ontology mutation.

LLM/RAG may propose.  
Ontology Steward approves.  
Governance updates.  
Runtime consumes.

---

# **8\. State Reconciliation, Saga, and Event Sourcing**

There is an asynchronous interval between ExternalControlRequest and FeedbackEvent.

This interval can range from milliseconds to minutes.

## **8.1 Required Mechanisms**

Event Sourcing  
Transactional Outbox  
Idempotency Key  
Execution Lease  
Timeout Watcher  
Retry Policy  
Dead Letter Queue  
Recovery Trigger  
Manual Override Trigger  
Feedback Reconciliation  
Audit Closure

## **8.2 Command State Machine**

Canonical Reference: this is a conceptual overview of the command/dispatch state progression. The single canonical, implementation-authoritative enum (`DispatchStatus`) is defined in `03_core_specifications/09_execution_adapter_model/9_execution_adapter_model.md`, Section 20 "Dispatch Lifecycle". `03_action_type_registry.md` Section 9.1 also derives from that same canonical enum. Code must implement `DispatchStatus` once, from `09_execution_adapter_model`, and this section's states must be read as a subset/paraphrase of it, not a second enum.

CREATED  
DISPATCH\_PENDING  
DISPATCHED  
ACKNOWLEDGED  
ACCEPTED  
STARTED  
IN\_PROGRESS  
COMPLETED  
FAILED  
TIMEOUT  
CANCELLED  
BLOCKED  
FEEDBACK\_MISSING  
RECOVERY\_REQUIRED  
RECOVERY\_STARTED  
RECOVERY\_COMPLETED  
MANUAL\_OVERRIDE\_REQUIRED  
CLOSED

## **8.3 Recovery Principle**

Missing feedback must not be treated as success.

Example:

If there is no feedback after sending a robot movement request:

WorldState \= mission\_status\_unknown  
ExecutionState \= FEEDBACK\_MISSING  
RecoveryRequired \= true  
Supervisor notification  
Fleet manager status query  
Robot heartbeat check  
Timeout policy execution  
Manual override if unresolved

## **8.4 Rule**

Every lifecycle after ExternalControlRequest must have a Timeout Policy and Recovery State Trigger.

---

# **9\. Observability and Operational Metrics**

Each stage must be operationally observable.

## **9.1 Stage Latency Metrics**

raw\_ingest\_latency\_ms  
canonical\_envelope\_latency\_ms  
canonicalization\_latency\_ms  
ontology\_binding\_latency\_ms  
evidence\_validation\_latency\_ms  
world\_state\_update\_latency\_ms  
candidate\_generation\_latency\_ms  
decision\_routing\_latency\_ms  
approval\_wait\_time\_ms  
safety\_gate\_latency\_ms  
execution\_request\_build\_latency\_ms  
external\_dispatch\_latency\_ms  
feedback\_latency\_ms  
audit\_closure\_latency\_ms

## **9.2 Path Metrics**

standard\_path\_count  
emergency\_fast\_path\_count  
monitoring\_only\_path\_count  
path\_escalation\_count  
path\_downgrade\_count

## **9.3 Rejection Metrics**

rejected\_invalid\_schema\_count  
rejected\_unknown\_source\_count  
rejected\_binding\_failed\_count  
rejected\_low\_confidence\_count  
rejected\_stale\_state\_count  
rejected\_insufficient\_evidence\_count  
rejected\_policy\_denied\_count  
rejected\_approval\_missing\_count  
rejected\_capability\_unavailable\_count  
rejected\_adapter\_unavailable\_count

## **9.4 Emergency Metrics**

emergency\_detected\_count  
emergency\_approved\_action\_count  
emergency\_policy\_denied\_count  
emergency\_feedback\_missing\_count  
emergency\_audit\_delay\_ms  
emergency\_false\_positive\_count  
emergency\_false\_negative\_review\_count

## **9.5 Drift Metrics**

unclassified\_entity\_count  
mapping\_review\_required\_count  
mapping\_proposal\_count  
mapping\_approval\_time\_ms  
ontology\_drift\_rate  
policy\_context\_stale\_count

## **9.6 Execution Metrics**

execution\_timeout\_count  
feedback\_missing\_count  
feedback\_conflict\_count  
recovery\_required\_count  
manual\_override\_required\_count  
idempotency\_duplicate\_detected\_count  
dead\_letter\_queue\_count

## **9.7 Rule**

If a lifecycle stage cannot be observed, it cannot be operated safely.

Observability is not an add-on.  
It is part of the safety architecture.

---

# **10\. Lifecycle State Machines**

## **10.1 Standard Path State Machine**

RAW\_RECEIVED  
→ ENVELOPED  
→ PATH\_CLASSIFIED  
→ CANONICALIZED  
→ ONTOLOGY\_BOUND  
→ EVIDENCE\_ATTACHED  
→ WORLD\_STATE\_UPDATED  
→ CANDIDATE\_GENERATED  
→ DECISION\_ROUTED  
→ APPROVAL\_PENDING  
→ APPROVAL\_GRANTED  
→ APPROVED\_ACTION\_CREATED  
→ RUNTIME\_VALIDATION\_INPUT\_CREATED  
→ RUNTIME\_VALIDATION\_RESULT\_CREATED  
→ SAFETY\_GATE\_PASSED  
→ EXECUTION\_REQUEST\_CREATED  
→ EXTERNAL\_REQUEST\_DISPATCHED  
→ FEEDBACK\_RECEIVED  
→ WORLD\_STATE\_RECONCILED  
→ AUDIT\_CLOSED

`APPROVED_ACTION_CREATED` must precede `RUNTIME_VALIDATION_INPUT_CREATED`: per Section 4.10, "ApprovedAction is not eligible to create an ExecutionRequest until Runtime Validation has produced a valid RuntimeValidationResult and the Safety Gate has issued a valid SafetyGatePass."

## **10.2 Emergency Fast-Path State Machine**

RAW\_RECEIVED  
→ ENVELOPED  
→ EMERGENCY\_DETECTED  
→ MINIMAL\_TARGET\_BOUND  
→ LOCAL\_EMERGENCY\_POLICY\_PASSED  
→ EMERGENCY\_APPROVED\_ACTION\_CREATED  
→ EMERGENCY\_RUNTIME\_VALIDATION\_INPUT\_CREATED  
→ EMERGENCY\_RUNTIME\_VALIDATION\_RESULT\_CREATED  
→ EMERGENCY\_SAFETY\_GATE\_PASSED  
→ EMERGENCY\_EXECUTION\_REQUEST\_CREATED  
→ EXTERNAL\_REQUEST\_DISPATCHED  
→ FEEDBACK\_RECEIVED  
→ POST\_HOC\_ONTOLOGY\_BINDING  
→ WORLD\_STATE\_RECONCILED  
→ AUDIT\_CLOSED

Per Section 4.11, "EmergencyApprovedAction is not a SafetyGatePass and must not create an EmergencyExecutionRequest unless deterministic emergency Runtime Validation and an emergency Safety Gate decision produce a valid pass."

## **10.3 Monitoring-Only Path State Machine**

RAW\_RECEIVED  
→ ENVELOPED  
→ LIGHTWEIGHT\_CANONICALIZED  
→ BASIC\_BOUND\_OR\_KNOWN\_SOURCE\_MAPPED  
→ WORLD\_STATE\_UPDATED  
→ METRIC\_UPDATED  
→ OPTIONAL\_AUDIT\_SAMPLED

## **10.4 Failure States**

REJECTED\_INVALID\_SCHEMA  
REJECTED\_UNKNOWN\_SOURCE  
REJECTED\_BINDING\_FAILED  
REJECTED\_LOW\_CONFIDENCE  
REJECTED\_STALE\_STATE  
REJECTED\_INSUFFICIENT\_EVIDENCE  
REJECTED\_POLICY\_DENIED  
REJECTED\_APPROVAL\_MISSING  
REJECTED\_CAPABILITY\_UNAVAILABLE  
REJECTED\_TARGET\_INVALID  
REJECTED\_ADAPTER\_UNAVAILABLE  
EXECUTION\_TIMEOUT  
EXECUTION\_FAILED  
FEEDBACK\_MISSING  
FEEDBACK\_CONFLICT  
RECOVERY\_REQUIRED  
MANUAL\_OVERRIDE\_REQUIRED  
AUDIT\_INCOMPLETE  
UNCLASSIFIED\_ENTITY\_DETECTED  
MAPPING\_REVIEW\_REQUIRED  
POLICY\_CONTEXT\_STALE

---

# **11\. Example Flows**

## **11.1 Standard Path Example**

Scenario:

A gas sensor detects abnormal but non-critical gas concentration in Zone\_A while a worker is present.

Flow:

RawInput  
→ CanonicalEventEnvelope  
→ Standard Path classification  
→ Ontology Binding  
→ Evidence  
→ WorldStateUpdate  
→ SafetyAgent creates ACTION\_EVACUATE\_ZONE candidate  
→ Decision Router classifies High Risk  
→ SupervisorApproval requested  
→ ApprovedAction created  
→ RuntimeValidationInput created  
→ RuntimeValidationResult produced  
→ Safety Gate consumes RuntimeValidationResult  
→ SafetyGatePass or SafetyGateBlock issued  
→ ExecutionRequest created only after SafetyGatePass  
→ Smart Helmet Alert \+ Site Operation Platform notified  
→ Feedback received  
→ AuditRecord closed  
→ World State updated

## **11.2 Emergency Fast-Path Example**

Scenario:

A gas sensor detects critical gas concentration in Zone\_A while Worker\_03 is inside Zone\_A.

Flow:

RawInput  
→ CanonicalEventEnvelope with emergency\_hint  
→ Emergency Classification Check  
→ Minimal Target Binding  
→ Deterministic Safety Rule  
→ Local Emergency Policy Check  
→ EmergencyApprovedAction  
→ Emergency RuntimeValidationInput
→ EmergencyRuntimeValidationResult
→ Emergency Safety Gate consumes EmergencyRuntimeValidationResult
→ EmergencySafetyGatePass or EmergencySafetyGateBlock
→ EmergencyExecutionRequest only after EmergencySafetyGatePass
→ Emergency alert dispatch  
→ Feedback received  
→ Post-hoc Ontology Binding  
→ AuditRecord closed  
→ World State updated

## **11.3 Monitoring-Only Path Example**

Scenario:

A temperature sensor sends a normal reading every 100ms.

Flow:

RawInput  
→ CanonicalEventEnvelope  
→ Lightweight Canonicalization  
→ Known Source Mapping  
→ WorldStateUpdate  
→ Dashboard metric update  
→ No ActionCandidate  
→ Optional audit sampling

If the temperature crosses a threshold:

Monitoring-Only Path  
→ Standard Path or Emergency Fast-Path escalation

---

# **12\. Recommended Code Mapping**

schemas/  
base.py  
event.py  
evidence.py  
world\_state.py  
action.py  
decision.py  
approval.py  
execution.py  
feedback.py  
audit.py  
emergency.py  
lifecycle.py

ingestion/  
industrial\_adapter.py  
robot\_adapter.py  
construction\_adapter.py  
llm\_adapter.py  
mobile\_adapter.py

normalization/  
canonicalizer.py  
event\_normalizer.py  
source\_normalizer.py  
path\_classifier.py  
emergency\_classifier.py  
lightweight\_classifier.py

ontology\_core/  
semantic\_binder.py  
class\_registry.py  
property\_registry.py  
action\_registry.py  
emergency\_action\_registry.py  
validators.py  
unclassified\_entity.py  
mapping\_proposal.py

knowledge\_memory/  
evidence\_store.py  
provenance.py

world\_state/  
state\_store.py  
freshness.py  
confidence.py  
state\_sync.py  
reconciliation.py

agents/  
safety\_agent.py  
robot\_agent.py  
inspection\_agent.py  
evidence\_binder.py

decision\_router/  
router.py  
risk\_classifier.py  
escalation\_policy.py

safety\_gate/  
gate.py  
emergency\_gate.py  
evidence\_validator.py  
policy\_validator.py  
state\_validator.py  
capability\_validator.py  
approval\_validator.py

execution\_core/  
lifecycle\_manager.py  
execution\_request\_builder.py  
idempotency.py  
recovery.py  
feedback\_handler.py  
timeout\_watcher.py  
event\_sourcing.py  
outbox.py

external\_adapters/  
base\_adapter.py  
mock\_adapter.py  
mqtt\_adapter.py  
rest\_adapter.py  
fleet\_manager\_adapter.py  
ros2\_bridge.py  
scada\_connector.py

audit/  
audit\_logger.py  
trace\_store.py  
decision\_trace.py  
execution\_trace.py  
emergency\_audit.py

governance/  
policy\_engine.py  
opa\_client.py  
approval\_matrix.py  
mapping\_review.py  
emergency\_registry\_review.py  
lifecycle\_version\_policy.py

observability/  
metrics.py  
tracing.py  
lifecycle\_metrics.py  
emergency\_metrics.py  
drift\_metrics.py

---

# **13\. Final Architecture Principle**

This lifecycle can be summarized as follows:

Input becomes event.  
Event becomes meaning.  
Meaning becomes evidence.  
Evidence updates state.  
State may generate candidate.  
Candidate becomes decision case.  
Decision case may become approved action only after policy, evidence, and approval requirements are satisfied.  
Approved action becomes execution request only after Runtime Validation and SafetyGatePass.  
Execution request becomes external control request.  
External control returns feedback.  
Feedback updates world state.  
Audit closes the loop.

After production hardening, the following principles are added:

Critical emergency must have a deterministic fast path.  
High-frequency low-risk telemetry must have a lightweight monitoring path.  
Execution must have timeout and recovery semantics.  
Unknown entities must enter governance, not break the system.  
LLM/RAG must propose, not execute.  
Feedback loss must trigger reconciliation, not silent success.  
Ontology drift must create mapping review, not uncontrolled execution.  
Every stage must be observable.  
The lifecycle specification itself must be versioned.

Final one-line summary:

Different sources.  
Different adapters.  
Different domain modules.

One semantic core.  
One canonical lifecycle.  
One emergency fast-path.  
One monitoring path.  
One decision pipeline.  
One recovery model.  
One audit trail.
