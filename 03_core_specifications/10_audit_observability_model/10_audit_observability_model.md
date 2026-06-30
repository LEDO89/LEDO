# **Audit Observability Model**

## **Audit, Observability, and Traceability Model for an Ontology-Centric Platform v1.2**

---

# **1\. Purpose**

The Audit Observability Model is a Core Specification that defines how an ontology-centric platform records and traces all important decisions, approvals, policy evaluations, Safety Gate validations, external execution requests, feedback, failures, recovery actions, state reconciliation, ontology changes, and AI/SLM output usage.

This document answers the following questions:

Who did what?  
When did it happen?  
Which object was the target?  
Which policies and evidence were used as the basis?  
Which decision route was followed?  
Who approved it?  
What did the Safety Gate validate?  
How was the external system request dispatched?  
What feedback did the external system return?  
How are failures, timeouts, retries, and recovery actions recorded?  
Where was AI or SLM output used?  
Can the full flow be reconstructed after an issue occurs?  
What identifier standard should audit records and reference IDs follow?  
How should causality be represented when one incident has multiple causes or multiple effects?  
Which audit records require a strong integrity chain?  
How are audit records generated in Edge environments synchronized with the central system?  
How can operators and auditors query the execution flow?

The core purposes of the Audit Observability Model are:

Preserve accountability.  
Make system state observable.  
Make the full flow of decisions and execution traceable.  
Connect policies, evidence, approvals, execution, and feedback into one trace.  
Make failures and incidents analyzable.  
Support post-hoc audit and reproducibility.  
Allow operators, auditors, domain experts, and system engineers to see the same facts.  
Maintain a consistent identifier and reference system for audit records.  
Make the integrity of high-risk audit records verifiable.  
Prevent audit record loss in Edge environments.

The core principles are:

Audit preserves accountability.  
Observability exposes system behavior.  
Trace connects causality.  
Metrics show system health.  
Logs explain local events.  
Evidence supports decisions.  
Feedback confirms execution outcomes.  
Integrity protects critical audit records.  
Privacy protects sensitive information.

In plain terms:

Audit preserves responsibility.  
Observability makes system behavior visible.  
Trace connects causal flow.  
Metrics show system health.  
Logs explain local events.  
Evidence provides the basis for decisions.  
Feedback confirms execution outcomes.  
Integrity protects critical audit records.  
Privacy protects sensitive information.

---

# **2\. Position Within Core Specifications**

The Audit Observability Model is document 10 within the Core Specifications.

03\_core\_specifications/  
  00\_canonical\_object\_lifecycle/  
  01\_common\_schema\_dto/  
  02\_event\_type\_taxonomy/  
  03\_action\_type\_registry/  
  04\_state\_model\_registry/  
  05\_evidence\_model/  
  06\_ontology\_module\_boundary/  
  07\_decision\_approval\_matrix/  
  08\_policy\_governance\_model/  
  09\_execution\_adapter\_model/  
  10\_audit\_observability\_model/

This is the final document in the Core Specifications.

All previous Core Specifications define decision, policy, state, evidence, approval, and execution boundaries.

The Audit Observability Model connects all of those flows and enables the following:

post-hoc tracing  
audit  
failure analysis  
accountability investigation  
policy review  
safety incident analysis  
verification of AI output usage history  
reconstruction of external system execution history  
integrity verification for high-risk records

---

# **3\. Overall Position**

The Audit Observability Model does not operate only at the end of the flow.

Audit and Observability are cross-cutting concerns that connect across all stages.

Raw Object  
→ Canonical Object  
→ Ontology-Bound Object  
→ Evidence-Linked Object  
→ State-Tracked Object  
→ ActionCandidate  
→ DecisionCase  
→ PolicyDecision  
→ ApprovalDecision  
→ ApprovedAction  
→ Safety Gate  
→ ExecutionRequest  
→ ExternalControlRequest  
→ FeedbackEvent  
→ Reconciliation  
→ AuditRecord

All major stages must be connected by `trace_id`, `correlation_id`, `decision_trace_id`, and `causality_ids`.

---

# **4\. Scope of This Document**

The Audit Observability Model covers the following:

AuditRecord  
AuditContextSnapshot  
AuditEvent  
AuditTrail  
Trace  
DecisionTrace  
PolicyDecisionTrace  
ApprovalTrace  
SafetyGateTrace  
ExecutionTrace  
FeedbackTrace  
ReconciliationTrace  
LogEvent  
MetricEvent  
HealthEvent  
AlertEvent  
IncidentRecord  
ObservabilitySignal  
Telemetry  
Span  
Correlation  
Causality Chain  
Multi-Causality  
Audit Retention  
Privacy Masking  
PII Handling  
Edge Audit Buffer  
Offline Audit Sync  
Tamper-Evident Record  
Integrity Policy  
Post-Hoc Audit  
Audit Query Model

---

# **5\. Out of Scope**

The Audit Observability Model does not directly perform the following:

policy decision-making  
approval decision-making  
Safety Gate validation  
external system execution  
physical command creation  
robot control  
PLC control  
SCADA write  
domain safety rule creation

The Audit Observability Model is not a model that makes decisions or performs execution.

This model performs the following:

records  
connects  
preserves  
observes  
makes analysis possible  
enables post-hoc reconstruction  
protects records that require integrity verification

---

# **6\. Difference Between Audit, Observability, Logging, Metrics, and Trace**

## **6.1 Audit**

Audit is a record for accountability and evidentiary purposes.

Audit answers the following questions:

Who did it?  
What did they do?  
Why did they do it?  
What evidence was used?  
Which policy was followed?  
What result occurred?  
Can responsibility be assigned later?

Audit prioritizes retention, integrity, and reproducibility.

---

## **6.2 Observability**

Observability is the ability to understand system behavior.

Observability answers the following questions:

Is the system currently healthy?  
Where is latency occurring?  
Which adapter is failing?  
Which policies frequently cause blocks?  
Which sensor or edge node is degraded?

Observability prioritizes operational understanding.

---

## **6.3 Logging**

A Log is a local event record generated by a specific component.

Examples:

adapter request sent  
policy engine returned DENY  
Safety Gate blocked request  
feedback timeout occurred

Logs are used by developers and operators to analyze issues.

---

## **6.4 Metrics**

A Metric is a numerical state indicator.

Examples:

policy\_decision\_latency\_ms  
safety\_gate\_block\_count  
adapter\_timeout\_count  
execution\_success\_rate  
feedback\_missing\_count  
edge\_offline\_duration\_seconds

Metrics show system health and performance.

---

## **6.5 Trace**

A Trace connects the flow of one request or decision as it passes through multiple components in a distributed system.

Example:

ActionCandidate  
→ PolicyDecision  
→ ApprovalDecision  
→ SafetyGateResult  
→ ExecutionRequest  
→ ExternalControlRequest  
→ FeedbackEvent

Trace preserves causality.

---

# **7\. Core Principles**

The core principles of the Audit Observability Model are:

Every high-risk decision must be traceable.  
Every approval must be auditable.  
Every Safety Gate result must be recorded.  
Every ExecutionRequest must be linked to its ApprovedAction.  
Every ExternalControlRequest must be linked to feedback or timeout.  
Every emergency bypass must produce post-hoc audit.  
Every AI or SLM output used in decision flow must be traceable.  
Every policy version used in a decision must be preserved.  
Every evidence bundle used in a decision must be referenced.  
Every critical audit record must have an integrity strategy.  
Every audit reference must resolve to a stable identifier.  
AuditRecordDTO must remain lightweight and reference context snapshots.

In plain terms:

Every high-risk decision must be traceable.  
Every approval must be auditable.  
Every Safety Gate result must be recorded.  
Every ExecutionRequest must be linked to its ApprovedAction.  
Every ExternalControlRequest must be linked to either feedback or timeout.  
Every Emergency Bypass must create post-hoc audit.  
Every AI or SLM output used in the decision flow must be traceable.  
Every policy version used in a decision must be preserved.  
Every evidence bundle used in a decision must be referenced.  
Every critical audit record must have an integrity strategy.  
Every audit reference must resolve to a stable identifier.  
AuditRecordDTO must remain lightweight and reference context snapshots.

---

# **8\. Common Trace Identifiers**

All core objects must include common trace identifiers.

trace\_id  
correlation\_id  
decision\_trace\_id  
causality\_ids  
parent\_trace\_id  
root\_event\_id

---

## **8.1 trace\_id**

`trace_id` traces one technical request flow.

Example:

API request  
→ policy engine call  
→ Safety Gate call  
→ adapter dispatch

---

## **8.2 correlation\_id**

`correlation_id` groups multiple traces into one business or incident unit.

Example:

Worker entered danger zone incident  
→ sensor event  
→ dashboard alert  
→ supervisor approval  
→ zone lock request  
→ feedback event

---

## **8.3 decision\_trace\_id**

`decision_trace_id` groups the full decision chain.

Example:

ActionCandidate  
→ DecisionCase  
→ PolicyDecision  
→ ApprovalDecision  
→ SafetyGateResult  
→ ExecutionRequest

---

## **8.4 causality\_ids**

`causality_ids` connect causes and effects.

The model must not assume that only a single causal relationship exists.

One incident may arise from multiple causes, and one cause may produce multiple effects.

Therefore, `causality_id` should not be a single string. The recommended structure is `causality_ids: list[str]`.

Recommended field structure:

primary\_causality\_id  
causality\_ids  
causality\_role  
causality\_direction

Recommended `causality_role` values:

ROOT\_CAUSE  
CONTRIBUTING\_CAUSE  
DERIVED\_CAUSE  
RESULTING\_ACTION  
OBSERVED\_EFFECT

Recommended `causality_direction` values:

CAUSE\_TO\_EFFECT  
EFFECT\_TO\_CAUSE  
BIDIRECTIONAL\_RECONSTRUCTION

---

## **8.5 Multi-Causality Scenario: Gas Critical \+ Worker Location \+ Ventilation Degraded**

Situation:

GasSensor\_01 reports CRITICAL gas level.  
WorkerLocationState indicates workers may be present in Zone\_A.  
VentilationSystemState is DEGRADED.  
Emergency gas policy is ACTIVE.

Causality structure:

causality\_id\_1: GasSensor\_01 critical reading  
causality\_id\_2: WorkerLocationState near Zone\_A  
causality\_id\_3: VentilationSystemState degraded

primary\_causality\_id: causality\_id\_1  
causality\_ids:  
  \- causality\_id\_1  
  \- causality\_id\_2  
  \- causality\_id\_3

Resulting flow:

GasSensor critical event  
\+ Worker presence risk  
\+ Ventilation degraded  
→ Emergency Policy Bypass  
→ Evacuation Warning  
→ Stop Work Request  
→ Access Restriction  
→ Post-Hoc Audit

In this case, one Emergency Bypass has multiple causal sources.

Each resulting action may share the same `correlation_id`, and each action may reference the same `causality_ids` or a derived sub-causality chain.

Recommended recording pattern:

EmergencyBypassRecord  
  primary\_causality\_id \= GasSensor critical event  
  causality\_ids \= \[gas critical, worker presence risk, ventilation degraded\]

EvacuationWarning AuditRecord  
  causality\_role \= RESULTING\_ACTION  
  causality\_direction \= CAUSE\_TO\_EFFECT

AccessRestriction AuditRecord  
  causality\_role \= RESULTING\_ACTION  
  causality\_direction \= CAUSE\_TO\_EFFECT

PostHocAudit AuditRecord  
  causality\_role \= OBSERVED\_EFFECT  
  causality\_direction \= BIDIRECTIONAL\_RECONSTRUCTION

---

## **8.6 parent\_trace\_id**

`parent_trace_id` represents parent-child relationships in distributed tracing.

---

## **8.7 root\_event\_id**

`root_event_id` points to the first Event that triggered the entire flow.

---

## **8.8 Common ID Standard**

Audit records and reference IDs must follow a consistent standard.

The recommended standard is one of the following:

UUIDv4  
16-byte / 128-bit BLAKE2b hash-based virtual IRI

Examples of BLAKE2b-based virtual IRIs:

urn:ledo:audit:\<128bit\_hash\_hex\>  
urn:ledo:evidence:\<128bit\_hash\_hex\>  
urn:ledo:trace:\<128bit\_hash\_hex\>

If a reference field has the `_ref` suffix, the value must not imply a nested object. It must be a stable and resolvable identifier.

Examples:

evidence\_bundle\_ref  
policy\_decision\_ref  
safety\_gate\_result\_ref  
execution\_request\_ref  
external\_control\_request\_ref  
feedback\_event\_ref

Core principles:

A \*\_ref field must reference a stable object identity.  
A \*\_ref field must not imply embedded object nesting.  
Audit IDs must be globally unique within the platform boundary.  
Critical audit references should be resolvable across storage boundaries.

---

# **9\. AuditRecord**

AuditRecord is the basic unit of audit.

AuditRecord must record the following:

actor  
action  
target  
time  
reason  
result  
trace  
causality  
context snapshot reference  
integrity

AuditRecord is not a simple log.

AuditRecord is a structured record for accountability and reproducibility.

AuditRecordDTO must not directly carry all policy, evidence, state, and execution context.

AuditRecordDTO should remain lightweight, and detailed context should be connected through `AuditContextSnapshot` or `DecisionTrace`.

---

## **9.1 AuditRecordDTO**

Recommended fields:

audit\_record\_id  
audit\_event\_type  
actor\_ref  
actor\_role  
action\_type  
target\_entity\_refs  
result\_status  
risk\_level  
severity  
audit\_reason  
audit\_context\_snapshot\_ref  
decision\_trace\_ref  
created\_at  
occurred\_at  
time\_trust\_level  
clock\_sync\_status  
source\_system\_ref  
trace\_id  
correlation\_id  
decision\_trace\_id  
primary\_causality\_id  
causality\_ids  
integrity\_policy\_ref  
content\_hash  
previous\_record\_hash  
integrity\_status

`audit_record_id` and every field with the `_ref` suffix must follow a stable ID standard.

Recommended standard:

UUIDv4  
or  
16-byte / 128-bit BLAKE2b hash-based virtual IRI

AuditRecordDTO does not directly include all payloads.

Detailed payloads are connected by references.

---

## **9.2 AuditContextSnapshotDTO**

`AuditContextSnapshotDTO` groups the detailed decision context at the audit point.

The reasons for separating this object are:

Keep AuditRecordDTO lightweight.  
Reduce duplicate fields.  
Reuse audit context.  
Simplify the connection between DecisionTrace and AuditRecord.  
Separate Evidence, Policy, State, Safety Gate, and Execution context.

Recommended fields:

audit\_context\_snapshot\_id  
event\_refs  
state\_snapshot\_refs  
evidence\_bundle\_refs  
policy\_decision\_refs  
policy\_version\_refs  
policy\_resolution\_refs  
approval\_decision\_refs  
safety\_gate\_result\_refs  
execution\_request\_refs  
external\_control\_request\_refs  
feedback\_event\_refs  
reconciliation\_refs  
ai\_output\_refs  
slm\_output\_refs  
actor\_clearance\_refs  
target\_ontology\_classes  
time\_trust\_level  
clock\_sync\_status  
device\_health\_snapshot\_refs  
adapter\_status\_refs  
network\_health\_snapshot\_refs  
created\_at  
trace\_id  
correlation\_id  
decision\_trace\_id  
causality\_ids

---

## **9.3 Relationship Between AuditRecord and DecisionTrace**

`AuditRecord` is the record of an individual audit event.

`DecisionTrace` is the chain used to reconstruct the full decision flow.

Recommended structure:

AuditRecord  
→ audit\_context\_snapshot\_ref  
→ decision\_trace\_ref  
→ related object refs

Example:

SAFETY\_GATE\_BLOCKED AuditRecord  
→ AuditContextSnapshot  
   → safety\_gate\_result\_refs  
   → evidence\_bundle\_refs  
   → state\_snapshot\_refs  
   → policy\_decision\_refs  
→ DecisionTrace  
   → ActionCandidate  
   → PolicyDecision  
   → ApprovalDecision  
   → SafetyGateResult

---

# **10\. Audit Event Type**

Audit Event Type defines the types of events subject to audit.

Recommended values:

OBJECT\_CANONICALIZED  
ONTOLOGY\_BINDING\_CREATED  
ONTOLOGY\_BINDING\_CHANGED  
EVIDENCE\_CREATED  
EVIDENCE\_VALIDATED  
STATE\_UPDATED  
STATE\_RECONCILED  
ACTION\_CANDIDATE\_CREATED  
AI\_OUTPUT\_USED  
SLM\_OUTPUT\_USED  
DECISION\_CASE\_CREATED  
POLICY\_DECISION\_EVALUATED  
POLICY\_CONFLICT\_RESOLVED  
POLICY\_EXCEPTION\_USED  
GRACE\_PERIOD\_USED  
APPROVAL\_REQUESTED  
APPROVAL\_GRANTED  
APPROVAL\_DENIED  
APPROVAL\_EXPIRED  
SAFETY\_GATE\_PASSED  
SAFETY\_GATE\_BLOCKED  
SAFETY\_GATE\_REVALIDATION\_REQUIRED  
EXECUTION\_REQUEST\_CREATED  
EXTERNAL\_CONTROL\_REQUEST\_DISPATCHED  
EXTERNAL\_CONTROL\_REQUEST\_ACKNOWLEDGED  
EXTERNAL\_CONTROL\_REQUEST\_ACCEPTED  
EXTERNAL\_CONTROL\_REQUEST\_REJECTED  
EXTERNAL\_CONTROL\_REQUEST\_TIMEOUT  
FEEDBACK\_RECEIVED  
FEEDBACK\_MISSING  
RETRY\_ATTEMPTED  
IDEMPOTENCY\_CONFLICT\_DETECTED  
EMERGENCY\_POLICY\_BYPASS\_ACTIVATED  
POST\_HOC\_AUDIT\_CREATED  
MANUAL\_OVERRIDE\_REQUIRED  
MANUAL\_OVERRIDE\_PERFORMED  
RECOVERY\_REQUIRED  
FAIL\_SAFE\_TRIGGERED  
INCIDENT\_CREATED

---

# **11\. Observability Signal**

An Observability Signal is a signal for observing system operational state.

Recommended types:

LogEvent  
MetricEvent  
TraceSpan  
HealthEvent  
AlertEvent  
IncidentRecord  
TelemetrySnapshot

---

## **11.1 LogEvent**

LogEvent is a component-level local event.

Recommended fields:

log\_event\_id  
component\_name  
log\_level  
message  
event\_type  
target\_ref  
error\_code  
error\_detail\_ref  
created\_at  
trace\_id  
correlation\_id  
decision\_trace\_id

Recommended log levels:

DEBUG  
INFO  
WARNING  
ERROR  
CRITICAL

---

## **11.2 MetricEvent**

MetricEvent is a numerical observation indicator.

Recommended fields:

metric\_event\_id  
metric\_name  
metric\_value  
metric\_unit  
component\_name  
target\_ref  
window\_start  
window\_end  
created\_at  
trace\_id  
correlation\_id

Recommended metric examples:

policy\_decision\_latency\_ms  
safety\_gate\_latency\_ms  
adapter\_dispatch\_latency\_ms  
adapter\_ack\_timeout\_count  
adapter\_acceptance\_timeout\_count  
feedback\_missing\_count  
execution\_success\_rate  
state\_reconciliation\_count  
evidence\_stale\_block\_count  
emergency\_bypass\_count

---

## **11.3 TraceSpan**

TraceSpan is one segment of a distributed request flow.

Recommended fields:

span\_id  
trace\_id  
parent\_span\_id  
span\_name  
component\_name  
operation\_name  
start\_time  
end\_time  
duration\_ms  
status  
error\_code  
target\_ref  
metadata\_ref

---

## **11.4 HealthEvent**

HealthEvent represents the health state of a system component.

Recommended fields:

health\_event\_id  
component\_name  
component\_type  
health\_status  
availability\_status  
latency\_ms  
error\_rate  
last\_heartbeat\_at  
degraded\_reason  
created\_at  
trace\_id

Recommended health status values:

HEALTHY  
DEGRADED  
UNHEALTHY  
OFFLINE  
UNKNOWN

---

## **11.5 AlertEvent**

AlertEvent is an event that must be surfaced to operators.

Recommended fields:

alert\_event\_id  
alert\_type  
severity  
message  
target\_refs  
trigger\_event\_refs  
recommended\_action\_refs  
created\_at  
acknowledged\_by  
acknowledged\_at  
trace\_id  
correlation\_id

Recommended severity values:

INFO  
NOTICE  
WARNING  
HIGH  
CRITICAL  
EMERGENCY

---

## **11.6 IncidentRecord**

IncidentRecord groups multiple events, alerts, state changes, actions, and feedback into one incident.

Recommended fields:

incident\_id  
incident\_type  
severity  
root\_event\_ref  
related\_event\_refs  
related\_alert\_refs  
related\_audit\_record\_refs  
target\_entity\_refs  
state\_snapshot\_refs  
evidence\_bundle\_refs  
action\_refs  
execution\_request\_refs  
feedback\_event\_refs  
status  
created\_at  
closed\_at  
owner\_ref  
trace\_id  
correlation\_id  
causality\_ids

---

# **12\. Decision Trace**

DecisionTrace is a trace model for reconstructing the decision route.

DecisionTrace connects the following:

ActionCandidate  
DecisionCase  
PolicyDecision  
PolicyResolutionRecord  
ApprovalDecision  
SafetyGateResult  
ExecutionRequest

Recommended fields:

decision\_trace\_id  
root\_event\_ref  
action\_candidate\_refs  
decision\_case\_ref  
policy\_decision\_refs  
policy\_resolution\_refs  
approval\_decision\_refs  
safety\_gate\_result\_refs  
execution\_request\_refs  
final\_decision\_result  
created\_at  
trace\_id  
correlation\_id  
causality\_ids

DecisionTraceDTO must be included from MVP Phase 1\.

Reasons:

The decision flow can be reconstructed from the beginning.  
PolicyDecision, ApprovalDecision, and SafetyGateResult connections can be tested.  
Audit Query Service becomes easier to implement later.

---

# **13\. Policy Audit**

All policy-related changes and decisions must be audited.

Audit targets:

policy created  
policy reviewed  
policy approved  
policy activated  
policy deprecated  
policy retired  
policy blocked  
policy decision evaluated  
policy conflict resolved  
policy exception requested  
policy exception approved  
policy exception used

Policy Audit connects to `PolicyAuditEventDTO` in the Policy Governance Model.

---

# **14\. Approval Audit**

Approval is one of the most important audit targets in a high-risk system.

Audit targets:

approval requested  
approval granted  
approval denied  
approval expired  
approval revoked  
approval escalated  
approval bypassed by emergency policy

Approval Audit must include the following information:

approver\_ref  
approver\_role  
approver\_clearance\_refs  
approval\_level  
approval\_reason  
approved\_action\_ref  
policy\_decision\_refs  
evidence\_bundle\_refs  
valid\_until  
trace\_id  
decision\_trace\_id

---

# **15\. Safety Gate Audit**

Safety Gate results must be audited.

Audit targets:

SAFETY\_GATE\_PASSED  
SAFETY\_GATE\_BLOCKED  
SAFETY\_GATE\_REVALIDATION\_REQUIRED  
SAFETY\_GATE\_FAIL\_SAFE\_REQUIRED  
SAFETY\_GATE\_MANUAL\_OVERRIDE\_REQUIRED

Safety Gate Audit must include the following:

approved\_action\_ref  
safety\_gate\_result\_ref  
failure\_codes  
evidence\_refs  
state\_snapshot\_refs  
policy\_refs  
time\_trust\_level  
device\_health\_snapshot\_refs  
adapter\_status\_refs  
trace\_id  
decision\_trace\_id

---

# **16\. Execution Audit**

Execution Audit directly connects to the Execution Adapter Model.

Audit targets:

EXECUTION\_REQUEST\_CREATED  
EXTERNAL\_CONTROL\_REQUEST\_DISPATCHED  
EXTERNAL\_CONTROL\_REQUEST\_ACKNOWLEDGED  
EXTERNAL\_CONTROL\_REQUEST\_ACCEPTED  
EXTERNAL\_CONTROL\_REQUEST\_REJECTED  
EXTERNAL\_CONTROL\_REQUEST\_TIMEOUT  
FEEDBACK\_RECEIVED  
FEEDBACK\_MISSING  
RETRY\_ATTEMPTED  
IDEMPOTENCY\_CONFLICT\_DETECTED  
RECOVERY\_REQUIRED

Execution Audit must connect the following:

approved\_action\_ref  
execution\_request\_ref  
external\_control\_request\_ref  
adapter\_ref  
adapter\_mode  
external\_system\_ref  
idempotency\_key  
dispatch\_status  
feedback\_event\_ref  
failure\_code  
recovery\_result  
trace\_id  
decision\_trace\_id

---

## **16.1 Mapping Between DispatchStatus and AuditEventType**

`DispatchStatus` from the Execution Adapter Model must be connected to AuditEventType.

| DispatchStatus | AuditEventType | Description |
| ----- | ----- | ----- |
| CREATED | EXECUTION\_REQUEST\_CREATED | Internal execution request created |
| DISPATCHED | EXTERNAL\_CONTROL\_REQUEST\_DISPATCHED | External system request dispatched |
| ACKNOWLEDGED | EXTERNAL\_CONTROL\_REQUEST\_ACKNOWLEDGED | Receipt acknowledged by external system or communication layer |
| ACCEPTED | EXTERNAL\_CONTROL\_REQUEST\_ACCEPTED | Accepted by external system application layer |
| REJECTED | EXTERNAL\_CONTROL\_REQUEST\_REJECTED | Rejected by external system |
| ACK\_TIMEOUT | EXTERNAL\_CONTROL\_REQUEST\_TIMEOUT | ACK timeout |
| ACCEPTANCE\_TIMEOUT | EXTERNAL\_CONTROL\_REQUEST\_TIMEOUT | ACCEPT timeout |
| FEEDBACK\_TIMEOUT | EXTERNAL\_CONTROL\_REQUEST\_TIMEOUT | Feedback timeout |
| FEEDBACK\_MISSING | FEEDBACK\_MISSING | Result feedback missing |
| COMPLETED | FEEDBACK\_RECEIVED | Completion feedback received |
| PARTIAL\_SUCCESS | FEEDBACK\_RECEIVED | Partial success feedback received |
| FAILED | FEEDBACK\_RECEIVED | Failure feedback received |
| RECOVERY\_REQUIRED | RECOVERY\_REQUIRED | Recovery required |
| MANUAL\_OVERRIDE\_REQUIRED | MANUAL\_OVERRIDE\_REQUIRED | Manual intervention required |

This mapping clarifies the connection between the Execution Adapter Model and the Audit Observability Model.

---

# **17\. Evidence Audit**

Evidence is the basis for decisions, so its usage history must be audited.

Audit targets:

evidence created  
evidence validated  
evidence expired  
evidence revoked  
evidence conflicted  
evidence used in decision  
evidence used in Safety Gate  
evidence used in emergency bypass

Evidence Audit must reference the following fields from the Evidence Model:

source\_trust\_level  
time\_trust\_level  
clock\_sync\_status  
clock\_drift\_estimate\_ms  
device\_health\_snapshot\_ref  
freshness\_status  
trust\_upgrade\_status  
attestation\_status  
conflict\_status

---

# **18\. AI / SLM Audit**

If AI or SLM output is used in the decision flow, it must be audited.

Audit targets:

AI output generated  
SLM output generated  
AI output used in ActionCandidate  
SLM output used in RiskInterpretation  
AI output used in EvidenceSummary  
SLM output used in MappingProposal  
AI output rejected by policy  
AI output blocked from execution

AI / SLM Audit must include the following information:

model\_id  
model\_version  
prompt\_ref  
input\_context\_hash  
output\_ref  
output\_type  
output\_confidence  
ai\_governance\_policy\_ref  
used\_as\_evidence  
used\_as\_candidate  
approved\_for\_execution  
trace\_id  
decision\_trace\_id

Important principle:

AI or SLM output may be audited as input.  
AI or SLM output must not be audited as final authority.

In other words, AI/SLM output may be recorded as an input to the decision flow, but it must not be recorded as the final approval authority.

---

# **19\. Emergency and Post-Hoc Audit**

When Emergency Policy Bypass occurs, post-hoc audit is required.

Audit targets:

emergency policy activated  
emergency bypass used  
normal approval bypassed  
minimum evidence checked  
Safety Gate evaluated  
external request dispatched  
feedback received  
post-hoc audit created  
post-hoc audit reviewed

Post-Hoc Audit must answer the following questions:

Was this truly an emergency situation?  
Did a pre-approved emergency policy exist?  
Was minimum verified evidence available?  
Was the target a canonical object?  
Did the action pass the Safety Gate?  
Was the external request appropriate?  
Was feedback received?  
Was the policy abused?  
Does the policy need to be revised?

---

# **20\. Grace Period Audit**

When Grace Period is used, it must be audited.

Audit targets:

communication loss detected  
grace period evaluated  
grace period allowed  
grace period denied  
local safe action allowed  
fail-safe required  
manual override required  
reconnect reconciliation performed

Grace Period Audit must include the following:

grace\_policy\_ref  
connectivity\_status  
disconnected\_since  
last\_successful\_sync\_at  
last\_verified\_state\_snapshot\_ref  
last\_verified\_evidence\_bundle\_ref  
allowed\_action\_modes  
denied\_action\_types  
trace\_id  
correlation\_id  
decision\_trace\_id

---

# **21\. Reconciliation Audit**

World State Reconciliation is an audit target.

Audit targets:

state conflict detected  
state reconciliation started  
state reconciliation succeeded  
state reconciliation failed  
external feedback used for reconciliation  
manual reconciliation required

Reconciliation Audit must connect the following:

previous\_state\_snapshot\_ref  
new\_state\_snapshot\_ref  
feedback\_event\_refs  
evidence\_bundle\_refs  
conflict\_type  
resolution\_strategy  
reconciliation\_result  
trace\_id  
correlation\_id

---

# **22\. Edge / Offline Audit**

In field Edge environments, communication with the central system may be lost.

Even in this case, audit records must not disappear.

An Edge Audit Buffer is required.

The Edge Audit Buffer must guarantee the following:

local audit events are buffered  
local audit event order is preserved  
local sequence number is assigned  
local time and platform time are both preserved when possible  
audit records are synced after reconnect  
conflicts are reconciled after reconnect

Recommended fields:

edge\_audit\_event\_id  
edge\_node\_ref  
local\_sequence\_number  
local\_created\_at  
platform\_time\_ref  
sync\_status  
synced\_at  
conflict\_status  
trace\_id  
correlation\_id  
decision\_trace\_id

---

## **22.1 Edge Audit Sync Conflict Strategy**

After reconnect, conflicts may occur between the Edge Audit Buffer and the central Audit Store.

Conflict examples:

Different dispatch\_status values exist for the same idempotency\_key.  
Edge records FEEDBACK\_MISSING while the central system records FEEDBACK\_RECEIVED.  
The ordering of edge local time and platform time differs.  
Different results are recorded for the same external\_control\_request\_ref.

Recommended conflict strategies:

APPEND\_ONLY\_MERGE  
SOURCE\_TRUST\_PRIORITY  
TIME\_TRUST\_PRIORITY  
MANUAL\_REVIEW\_REQUIRED  
MARK\_AS\_CONFLICTED  
REJECT\_UNTRUSTED\_RECORD

Meanings:

APPEND\_ONLY\_MERGE  
→ Merge as a new record without overwriting existing records.

SOURCE\_TRUST\_PRIORITY  
→ Prioritize the record from the more trusted source\_system\_ref.

TIME\_TRUST\_PRIORITY  
→ Prioritize the record with better time\_trust\_level and clock\_sync\_status.

MANUAL\_REVIEW\_REQUIRED  
→ Route to human review when automatic merge is risky.

MARK\_AS\_CONFLICTED  
→ Mark as conflicted and require follow-up reconciliation.

REJECT\_UNTRUSTED\_RECORD  
→ Do not include the untrusted record in the audit chain.

Important rules:

Audit records must not be overwritten.  
Conflict resolution must also create a new AuditRecord.  
High-risk or emergency-related conflicts should default to manual review.

---

# **23\. Tamper-Evident Audit**

AuditRecord must not be mutable.

Audit records must follow the append-only principle.

Recommended principles:

Audit records should be append-only.  
Correction should create a new audit record, not overwrite the old one.  
Critical audit records should include content hash.  
Audit chains should preserve previous\_record\_hash when needed.  
Policy changes and emergency bypass records require stronger integrity guarantees.

However, applying a strong hash chain to every local log, metric, and debug event may create I/O bottlenecks on Edge devices.

Therefore, tamper-evident chains should be applied differentially.

---

## **23.1 Integrity Level**

Recommended integrity levels:

NONE  
BASIC\_HASH  
CHAINED\_HASH  
SIGNED\_CHAIN  
EXTERNAL\_ANCHOR

Meanings:

NONE  
→ no integrity chain

BASIC\_HASH  
→ store only the individual record content hash

CHAINED\_HASH  
→ include previous\_record\_hash in the chain

SIGNED\_CHAIN  
→ include a signature reference

EXTERNAL\_ANCHOR  
→ record to an external immutable store or separate anchor

---

## **23.2 IntegrityLevel Decision Table**

| Condition | Recommended IntegrityLevel | Description |
| ----- | ----- | ----- |
| DEBUG log | NONE or BASIC\_HASH | Development and diagnostic logs |
| INFO metric | NONE or BASIC\_HASH | General performance metrics |
| severity \= NOTICE | BASIC\_HASH | Ensures later verification capability |
| severity \>= WARNING | CHAINED\_HASH | Operationally meaningful warning or above |
| risk\_level \>= HIGH\_RISK | CHAINED\_HASH | High-risk decision or execution record |
| SAFETY\_GATE\_BLOCKED | CHAINED\_HASH | Safety block record |
| SAFETY\_GATE\_PASSED for high-risk action | CHAINED\_HASH | High-risk pre-execution pass record |
| EXECUTION\_REQUEST\_CREATED for high-risk action | CHAINED\_HASH | High-risk execution request creation |
| EXTERNAL\_CONTROL\_REQUEST\_DISPATCHED for high-risk action | CHAINED\_HASH | High-risk external request dispatch |
| POLICY\_EXCEPTION\_USED | SIGNED\_CHAIN | Policy exception usage |
| POLICY\_CONFLICT\_RESOLVED | CHAINED\_HASH | Policy conflict resolution |
| IDEMPOTENCY\_CONFLICT\_DETECTED | CHAINED\_HASH | Duplicate execution risk |
| MANUAL\_OVERRIDE\_PERFORMED | SIGNED\_CHAIN | Human manual intervention |
| FAIL\_SAFE\_TRIGGERED | SIGNED\_CHAIN | Safety recovery action |
| EMERGENCY\_POLICY\_BYPASS\_ACTIVATED | SIGNED\_CHAIN or EXTERNAL\_ANCHOR | Emergency policy bypass |
| POST\_HOC\_AUDIT\_CREATED | SIGNED\_CHAIN or EXTERNAL\_ANCHOR | Post-hoc audit creation |

Recommended fields:

integrity\_policy\_id  
applicable\_audit\_event\_types  
minimum\_severity  
minimum\_risk\_level  
integrity\_level  
requires\_previous\_record\_hash  
requires\_signature  
requires\_external\_anchor  
owner  
version  
status

Core principles:

All audit records should be append-only.  
Not all observability signals require chained hashing.  
Critical audit records require stronger integrity guarantees.  
Edge runtime efficiency must be considered.

---

# **24\. Privacy and PII Handling**

Audit and Observability may contain sensitive information.

Therefore, privacy and sensitive data handling are required.

Principles:

Audit must preserve accountability.  
Privacy policy must restrict unnecessary exposure.  
PII should be masked or tokenized when possible.  
Access to sensitive audit records must be policy-controlled.  
Audit export must be strongly controlled.

Recommended fields:

pii\_present  
pii\_category  
masking\_status  
redaction\_ref  
access\_policy\_refs  
retention\_policy\_ref  
export\_control\_required

---

# **25\. Retention Policy**

Audit and Observability data may have different retention periods.

Examples:

debug logs  
→ short retention

metrics  
→ medium retention

high-risk audit records  
→ long retention

emergency bypass audit  
→ long retention

PII-heavy raw payload  
→ minimized or redacted retention

Retention Policy must define the following:

record\_type  
risk\_level  
pii\_present  
pii\_category  
retention\_period  
archive\_policy  
deletion\_policy  
redaction\_policy  
legal\_hold\_required  
owner  
version

---

## **25.1 PII Retention Boundary**

Audit/Observability data that contains PII must have a separate retention standard.

Recommended classification:

NO\_PII  
PSEUDONYMIZED\_PII  
DIRECT\_PII  
SENSITIVE\_PII  
PII\_HEAVY\_PAYLOAD

Recommended principles:

NO\_PII  
→ apply normal retention policy

PSEUDONYMIZED\_PII  
→ may be retained for the period required for audit purposes

DIRECT\_PII  
→ requires access control and masking

SENSITIVE\_PII  
→ minimal retention, strong access control, export restriction

PII\_HEAVY\_PAYLOAD  
→ do not retain original payload long-term; prefer redacted references

Original PII payloads should not be retained long-term unless they are strictly required for audit accountability.

Recommended approach:

Retain original payloads for a short period.  
Retain redacted payloads or tokenized references for long-term audit.  
Export must pass the Data Privacy Policy in the Policy Governance Model.

---

# **26\. Audit Storage Boundary**

Audit storage may be separated from operational log storage.

Recommended separation:

Operational Logs  
→ debugging and runtime diagnostics

Metrics Store  
→ time-series performance and health indicators

Trace Store  
→ distributed request tracing

Audit Store  
→ accountability and compliance-grade records

Evidence Store  
→ evidence objects and validation records

Audit Store prioritizes accountability and retention.

Observability Store prioritizes operations and performance analysis.

---

# **27\. Audit Query Model**

Auditors must be able to query the following questions:

What evidence created this ActionCandidate?  
Who approved this Action?  
Which policy version was used in this policy decision?  
Why did the Safety Gate block this action?  
Which external system received this ExecutionRequest?  
Did the external system respond up to ACK, ACCEPT, or COMPLETE?  
Which requests are missing feedback?  
Where was Emergency Bypass used?  
Did any SLM output enter the execution flow?  
Which integrity policy did this audit record follow?  
Was this incident caused by a single cause or multiple causes?

Audit Query should be possible by the following keys:

trace\_id  
correlation\_id  
decision\_trace\_id  
causality\_ids  
target\_entity\_ref  
actor\_ref  
policy\_ref  
audit\_event\_type  
severity  
risk\_level  
integrity\_policy\_ref

---

## **27.1 Audit Query Example 1: Did the ExecutionRequest reach ACK or ACCEPT?**

Question:

Did ExecutionRequest ER-001 reach ACK only, or did it reach ACCEPT?

Conceptual query:

Find AuditRecords  
where execution\_request\_ref \= "ER-001"  
and audit\_event\_type in \[  
  EXTERNAL\_CONTROL\_REQUEST\_DISPATCHED,  
  EXTERNAL\_CONTROL\_REQUEST\_ACKNOWLEDGED,  
  EXTERNAL\_CONTROL\_REQUEST\_ACCEPTED,  
  EXTERNAL\_CONTROL\_REQUEST\_REJECTED,  
  EXTERNAL\_CONTROL\_REQUEST\_TIMEOUT,  
  FEEDBACK\_RECEIVED  
\]  
order by occurred\_at

Expected interpretation:

DISPATCHED exists  
ACKNOWLEDGED exists  
ACCEPTED does not exist  
FEEDBACK\_RECEIVED does not exist  
→ ACCEPTANCE\_PENDING or ACCEPTANCE\_TIMEOUT should be investigated

---

## **27.2 Audit Query Example 2: Why did the Safety Gate block the action?**

Question:

Why did the Safety Gate block ACTION\_LOCK\_ZONE?

Conceptual query:

Find AuditRecord  
where audit\_event\_type \= SAFETY\_GATE\_BLOCKED  
and action\_type \= ACTION\_LOCK\_ZONE  
and target\_entity\_refs contains Zone\_A

Connected records:

AuditRecord  
→ audit\_context\_snapshot\_ref  
→ safety\_gate\_result\_refs  
→ failure\_codes  
→ evidence\_bundle\_refs  
→ state\_snapshot\_refs  
→ policy\_decision\_refs

Expected interpretation:

failure\_code \= EVIDENCE\_STALE  
or  
failure\_code \= STATE\_CONFLICT\_UNRESOLVED  
or  
failure\_code \= POLICY\_DENIED

---

## **27.3 Audit Query Example 3: What caused the Emergency Bypass?**

Question:

Was Emergency Bypass EB-001 caused by a single cause or multiple causes?

Conceptual query:

Find AuditRecord  
where audit\_event\_type \= EMERGENCY\_POLICY\_BYPASS\_ACTIVATED  
and emergency\_bypass\_ref \= "EB-001"

Connected records:

AuditRecord  
→ causality\_ids  
→ related Evidence  
→ related StateSnapshot  
→ related Event

Expected interpretation:

causality\_ids:  
\- GasSensor critical reading  
\- WorkerLocation near danger zone  
\- VentilationSystem degraded

→ Multi-causality emergency bypass

---

# **28\. Connections to Other Core Specifications**

## **28.1 Canonical Object Lifecycle**

Audit targets must be based on canonical objects.

target\_entity\_ref must be canonicalized.  
target ontology binding must be known.  
target lifecycle status must be recorded.

---

## **28.2 Common Schema DTO**

All Audit, Log, Metric, and Trace DTOs must include common identifiers.

trace\_id  
correlation\_id  
schema\_version  
created\_at  
status  
version

---

## **28.3 Event Type Taxonomy**

AuditEventType may be connected to Event Type Taxonomy.

Example:

safety.worker.entered\_danger\_zone  
→ ACTION\_CANDIDATE\_CREATED  
→ POLICY\_DECISION\_EVALUATED  
→ SAFETY\_GATE\_PASSED  
→ EXECUTION\_REQUEST\_CREATED

---

## **28.4 Action Type Registry**

Audit must record `action_type`.

Examples:

ACTION\_STOP\_WORK  
ACTION\_LOCK\_ZONE  
ACTION\_RETURN\_ROBOT\_TO\_SAFE\_ZONE

---

## **28.5 State Model Registry**

Audit must record `state_snapshot_ref`.

---

## **28.6 Evidence Model**

Audit must record `evidence_bundle_refs`.

---

## **28.7 Decision / Approval Matrix**

Audit must record the decision route and approval level.

---

## **28.8 Policy Governance Model**

Audit must record `policy_decision_refs`, `policy_version_refs`, and `policy_resolution_refs`.

---

## **28.9 Execution Adapter Model**

Audit must record `execution_request_refs`, `external_control_request_refs`, and `feedback_event_refs`.

---

# **29\. MVP Scope**

## **29.1 MVP Phase 1**

MVP Phase 1 implements the following:

AuditRecordDTO  
AuditContextSnapshotDTO  
LogEventDTO  
MetricEventDTO  
TraceSpanDTO  
HealthEventDTO  
AlertEventDTO  
IncidentRecordDTO  
DecisionTraceDTO  
IntegrityPolicyDTO  
AuditEventType enum  
Severity enum  
HealthStatus enum  
AuditWriter interface  
InMemoryAuditWriter  
FileAuditWriter  
BasicTraceContext  
basic content\_hash support  
pytest unit tests

In Phase 1, an external observability stack is not required.

InMemoryAuditWriter and FileAuditWriter are sufficient.

DecisionTraceDTO must be included from Phase 1\.

---

## **29.2 MVP Phase 2**

MVP Phase 2 adds the following:

StructuredLogWriter  
MetricCollector  
TraceCollector  
AuditStoreRepository  
EdgeAuditBuffer  
AuditQueryService  
PolicyAudit integration  
SafetyGateAudit integration  
ExecutionAudit integration  
FeedbackAudit integration  
IntegrityPolicyEvaluator  
EdgeAuditConflictResolver

---

## **29.3 MVP Phase 3**

MVP Phase 3 adds the following:

OpenTelemetry-compatible trace exporter  
Metrics dashboard  
Audit dashboard  
Incident timeline view  
Emergency bypass audit view  
SLM / LLM audit view  
Tamper-evident audit chain  
PII masking and redaction workflow  
Integrity policy dashboard  
Audit query UI

---

# **30\. Recommended File Structure**

src/ledo\_ontology\_core/framework/audit/  
  \_\_init\_\_.py

  enums.py

  audit\_record.py  
  audit\_context\_snapshot.py  
  log\_event.py  
  metric\_event.py  
  trace\_span.py  
  health\_event.py  
  alert\_event.py  
  incident\_record.py  
  decision\_trace.py  
  edge\_audit\_event.py  
  retention\_policy.py  
  integrity\_policy.py

  audit\_writer.py  
  in\_memory\_audit\_writer.py  
  file\_audit\_writer.py  
  audit\_query\_service.py  
  audit\_integrity.py  
  integrity\_policy\_evaluator.py  
  edge\_audit\_conflict\_resolver.py  
  pii\_masker.py  
  trace\_context.py  
  id\_factory.py

tests/unit/framework/audit/  
  test\_audit\_record.py  
  test\_audit\_context\_snapshot.py  
  test\_log\_event.py  
  test\_metric\_event.py  
  test\_trace\_span.py  
  test\_decision\_trace.py  
  test\_in\_memory\_audit\_writer.py  
  test\_file\_audit\_writer.py  
  test\_audit\_integrity.py  
  test\_integrity\_policy.py  
  test\_edge\_audit\_conflict\_resolver.py  
  test\_pii\_masker.py  
  test\_id\_factory.py

---

# **31\. Implementation Order**

Recommended implementation order:

AuditEventType enum  
Severity enum  
HealthStatus enum  
AuditResult enum  
IntegrityStatus enum  
IntegrityLevel enum  
EdgeAuditConflictStrategy enum

AuditRecordDTO  
AuditContextSnapshotDTO  
LogEventDTO  
MetricEventDTO  
TraceSpanDTO  
HealthEventDTO  
AlertEventDTO  
IncidentRecordDTO  
DecisionTraceDTO  
EdgeAuditEventDTO  
RetentionPolicyDTO  
IntegrityPolicyDTO

AuditWriter interface  
InMemoryAuditWriter  
FileAuditWriter  
TraceContext  
IDFactory  
AuditIntegrity  
IntegrityPolicyEvaluator  
EdgeAuditConflictResolver  
PIIMasker  
AuditQueryService  
Unit tests

---

# **32\. Final Principles**

The Audit Observability Model is the memory system of the platform.

However, this model is not merely a logbook.

This model enables the following:

accountability tracing  
post-hoc audit  
failure analysis  
policy review  
safety incident analysis  
verification of AI/SLM usage history  
reconstruction of external execution outcomes  
integrity verification of critical audit records  
multi-causality reconstruction  
audit record preservation in Edge environments

The core principles are:

Audit preserves accountability.  
Observability exposes behavior.  
Trace connects causality.  
Multi-causality must be supported.  
Metrics expose system health.  
Logs explain local events.  
Evidence supports decisions.  
Feedback confirms outcomes.  
Emergency bypass requires post-hoc audit.  
AI and SLM outputs must be traceable.  
Audit record IDs and references must be stable.  
AuditRecordDTO should remain lightweight.  
AuditContextSnapshot should preserve detailed decision context.  
Critical audit records should be tamper-evident.  
Not every observability signal requires hash chaining.  
Edge audit conflicts must be resolved without overwriting records.  
Audit records should be append-only.  
Privacy must be protected.

In plain terms:

Audit preserves responsibility.  
Observability makes behavior visible.  
Trace connects causality.  
Multi-causality must be supported.  
Metrics show system health.  
Logs explain local events.  
Evidence supports decisions.  
Feedback confirms outcomes.  
Emergency Bypass requires post-hoc audit.  
AI and SLM outputs must be traceable.  
Audit record IDs and reference IDs must be stable.  
AuditRecordDTO must remain lightweight.  
AuditContextSnapshot must preserve detailed decision context.  
Critical audit records must be tamper-evident.  
Not every observability signal requires hash chaining.  
Edge audit conflicts must be resolved without overwriting records.  
Audit records must follow the append-only principle.  
Privacy must be protected.

# **Audit Observability Model**

# **1\. 목적**

Audit Observability Model은 온톨로지 중심 플랫폼에서 발생하는 모든 중요한 판단, 승인, 정책 평가, Safety Gate 검증, 외부 실행 요청, 피드백, 실패, 복구, 상태 조정, 온톨로지 변경, AI/SLM 출력 사용을 어떻게 기록하고 추적할 것인지 정의하는 Core Specification이다.

이 문서는 다음 질문에 답한다.\`

누가 무엇을 했는가?  
언제 했는가?  
어떤 객체를 대상으로 했는가?  
어떤 정책과 증거를 근거로 했는가?  
어떤 판단 경로를 거쳤는가?  
누가 승인했는가?  
Safety Gate는 무엇을 검증했는가?  
외부 시스템 요청은 어떻게 전송되었는가?  
외부 시스템은 어떤 피드백을 반환했는가?  
실패, timeout, retry, recovery는 어떻게 기록되는가?  
AI 또는 SLM 출력이 어디에 사용되었는가?  
문제가 발생했을 때 전체 흐름을 재구성할 수 있는가?  
감사 기록과 참조 ID는 어떤 규격을 따르는가?  
하나의 사건에 여러 원인 또는 여러 결과가 있을 때 인과관계는 어떻게 표현하는가?  
어떤 감사 기록에 강한 무결성 체인을 적용해야 하는가?  
Edge 환경에서 생성된 감사 기록은 중앙 시스템과 어떻게 동기화되는가?  
운영자와 감사자는 어떤 방식으로 실행 흐름을 질의할 수 있는가?

Audit Observability Model의 핵심 목적은 다음과 같다.

책임 소재를 남긴다.  
시스템 상태를 관측 가능하게 만든다.  
판단과 실행의 전체 흐름을 추적 가능하게 만든다.  
정책, 증거, 승인, 실행, 피드백을 하나의 trace로 연결한다.  
장애와 실패를 분석 가능하게 만든다.  
사후 감사와 재현성을 지원한다.  
운영자, 감사자, 도메인 전문가, 시스템 엔지니어가 같은 사실을 볼 수 있게 한다.  
감사 기록의 식별자와 참조 체계를 일관되게 유지한다.  
고위험 감사 기록의 무결성을 검증 가능하게 만든다.  
Edge 환경에서 발생한 감사 기록의 손실을 방지한다.

핵심 원칙은 다음과 같다.

Audit preserves accountability.  
Observability exposes system behavior.  
Trace connects causality.  
Metrics show system health.  
Logs explain local events.  
Evidence supports decisions.  
Feedback confirms execution outcomes.  
Integrity protects critical audit records.  
Privacy protects sensitive information.

한글로 정리하면 다음과 같다.

Audit는 책임을 보존한다.  
Observability는 시스템 동작을 보이게 한다.  
Trace는 인과 흐름을 연결한다.  
Metric은 시스템 건강 상태를 보여준다.  
Log는 국소 이벤트를 설명한다.  
Evidence는 판단 근거를 제공한다.  
Feedback은 실행 결과를 확인한다.  
Integrity는 핵심 감사 기록을 보호한다.  
Privacy는 민감 정보를 보호한다.

---

# **2\. Core Specification 안에서의 위치**

Audit Observability Model은 Core Specifications의 10번 문서다.

03\_core\_specifications/  
  00\_canonical\_object\_lifecycle/  
  01\_common\_schema\_dto/  
  02\_event\_type\_taxonomy/  
  03\_action\_type\_registry/  
  04\_state\_model\_registry/  
  05\_evidence\_model/  
  06\_ontology\_module\_boundary/  
  07\_decision\_approval\_matrix/  
  08\_policy\_governance\_model/  
  09\_execution\_adapter\_model/  
  10\_audit\_observability\_model/

이 문서는 Core Specification의 마지막 문서다.

앞선 모든 Core Spec은 판단, 정책, 상태, 증거, 승인, 실행 경계를 정의했다.

Audit Observability Model은 그 모든 흐름을 연결해서 다음을 가능하게 한다.

사후 추적  
감사  
장애 분석  
책임 규명  
정책 검토  
안전 사고 분석  
AI 출력 사용 이력 확인  
외부 시스템 실행 이력 재구성  
고위험 기록의 무결성 검증

---

# **3\. 전체 위치**

Audit Observability Model은 전체 흐름의 끝에서만 작동하는 것이 아니다.

Audit와 Observability는 모든 단계에 걸쳐 횡단적으로 연결된다.

Raw Object  
→ Canonical Object  
→ Ontology-Bound Object  
→ Evidence-Linked Object  
→ State-Tracked Object  
→ ActionCandidate  
→ DecisionCase  
→ PolicyDecision  
→ ApprovalDecision  
→ ApprovedAction  
→ Safety Gate  
→ ExecutionRequest  
→ ExternalControlRequest  
→ FeedbackEvent  
→ Reconciliation  
→ AuditRecord

모든 주요 단계는 `trace_id`, `correlation_id`, `decision_trace_id`, `causality_ids`로 연결되어야 한다.

---

# **4\. 이 문서가 다루는 것**

Audit Observability Model은 다음을 다룬다.

AuditRecord  
AuditContextSnapshot  
AuditEvent  
AuditTrail  
Trace  
DecisionTrace  
PolicyDecisionTrace  
ApprovalTrace  
SafetyGateTrace  
ExecutionTrace  
FeedbackTrace  
ReconciliationTrace  
LogEvent  
MetricEvent  
HealthEvent  
AlertEvent  
IncidentRecord  
ObservabilitySignal  
Telemetry  
Span  
Correlation  
Causality Chain  
Multi-Causality  
Audit Retention  
Privacy Masking  
PII Handling  
Edge Audit Buffer  
Offline Audit Sync  
Tamper-Evident Record  
Integrity Policy  
Post-Hoc Audit  
Audit Query Model

---

# **5\. 이 문서가 다루지 않는 것**

Audit Observability Model은 다음을 직접 수행하지 않는다.

정책 판단  
승인 결정  
Safety Gate 검증  
외부 시스템 실행  
물리 명령 생성  
로봇 제어  
PLC 제어  
SCADA write  
도메인 안전 기준 생성

Audit Observability Model은 판단하거나 실행하는 모델이 아니다.

이 모델은 다음을 수행한다.

기록한다.  
연결한다.  
보존한다.  
관측한다.  
분석 가능하게 만든다.  
사후 재구성을 가능하게 만든다.  
무결성 검증이 필요한 기록을 보호한다.

---

# **6\. Audit, Observability, Logging, Metrics, Trace의 차이**

## **6.1 Audit**

Audit는 책임과 증거성을 위한 기록이다.

Audit는 다음 질문에 답한다.

누가 했는가?  
무엇을 했는가?  
왜 했는가?  
어떤 근거로 했는가?  
어떤 정책을 따랐는가?  
어떤 결과가 발생했는가?  
나중에 책임을 물을 수 있는가?

Audit는 보존성, 무결성, 재현성이 중요하다.

---

## **6.2 Observability**

Observability는 시스템 동작을 이해하기 위한 관측 가능성이다.

Observability는 다음 질문에 답한다.

시스템이 지금 건강한가?  
어디서 지연이 발생하는가?  
어떤 adapter가 실패하고 있는가?  
어떤 정책이 자주 block을 발생시키는가?  
어떤 sensor나 edge node가 degraded 상태인가?

Observability는 운영 상태 이해가 중요하다.

---

## **6.3 Logging**

Log는 특정 컴포넌트에서 발생한 국소 이벤트 기록이다.

예시:

adapter request sent  
policy engine returned DENY  
Safety Gate blocked request  
feedback timeout occurred

Log는 개발자와 운영자가 문제를 분석하는 데 사용한다.

---

## **6.4 Metrics**

Metric은 수치화된 상태 지표다.

예시:

policy\_decision\_latency\_ms  
safety\_gate\_block\_count  
adapter\_timeout\_count  
execution\_success\_rate  
feedback\_missing\_count  
edge\_offline\_duration\_seconds

Metric은 시스템 건강 상태와 성능을 보여준다.

---

## **6.5 Trace**

Trace는 분산 시스템에서 하나의 요청이나 판단이 여러 컴포넌트를 지나가는 흐름을 연결한다.

예시:

ActionCandidate  
→ PolicyDecision  
→ ApprovalDecision  
→ SafetyGateResult  
→ ExecutionRequest  
→ ExternalControlRequest  
→ FeedbackEvent

Trace는 인과관계를 보존한다.

---

# **7\. 핵심 원칙**

Audit Observability Model의 핵심 원칙은 다음과 같다.

Every high-risk decision must be traceable.  
Every approval must be auditable.  
Every Safety Gate result must be recorded.  
Every ExecutionRequest must be linked to its ApprovedAction.  
Every ExternalControlRequest must be linked to feedback or timeout.  
Every emergency bypass must produce post-hoc audit.  
Every AI or SLM output used in decision flow must be traceable.  
Every policy version used in a decision must be preserved.  
Every evidence bundle used in a decision must be referenced.  
Every critical audit record must have an integrity strategy.  
Every audit reference must resolve to a stable identifier.  
AuditRecordDTO must remain lightweight and reference context snapshots.

한글로 정리하면 다음과 같다.

모든 고위험 판단은 추적 가능해야 한다.  
모든 승인은 감사 가능해야 한다.  
모든 Safety Gate 결과는 기록되어야 한다.  
모든 ExecutionRequest는 ApprovedAction과 연결되어야 한다.  
모든 ExternalControlRequest는 feedback 또는 timeout과 연결되어야 한다.  
모든 Emergency Bypass는 사후 감사를 만들어야 한다.  
판단 흐름에 사용된 모든 AI 또는 SLM 출력은 추적 가능해야 한다.  
판단에 사용된 모든 정책 버전은 보존되어야 한다.  
판단에 사용된 모든 evidence bundle은 참조되어야 한다.  
모든 핵심 감사 기록은 무결성 전략을 가져야 한다.  
모든 감사 참조는 안정적인 식별자로 해석 가능해야 한다.  
AuditRecordDTO는 경량화하고 context snapshot을 참조해야 한다.

---

# **8\. 공통 추적 식별자**

모든 핵심 객체는 공통 추적 식별자를 가져야 한다.

trace\_id  
correlation\_id  
decision\_trace\_id  
causality\_ids  
parent\_trace\_id  
root\_event\_id

---

## **8.1 trace\_id**

`trace_id`는 하나의 기술적 요청 흐름을 추적한다.

예시:

API request  
→ policy engine call  
→ Safety Gate call  
→ adapter dispatch

---

## **8.2 correlation\_id**

`correlation_id`는 여러 trace를 하나의 업무 또는 사건 단위로 묶는다.

예시:

Worker entered danger zone incident  
→ sensor event  
→ dashboard alert  
→ supervisor approval  
→ zone lock request  
→ feedback event

---

## **8.3 decision\_trace\_id**

`decision_trace_id`는 판단 계열 전체를 묶는다.

예시:

ActionCandidate  
→ DecisionCase  
→ PolicyDecision  
→ ApprovalDecision  
→ SafetyGateResult  
→ ExecutionRequest

---

## **8.4 causality\_ids**

`causality_ids`는 원인과 결과를 연결한다.

단일 인과관계만 존재한다고 가정하면 안 된다.

하나의 사건은 여러 원인에서 발생할 수 있고, 하나의 원인은 여러 결과를 만들 수 있다.

따라서 `causality_id`는 단일 문자열이 아니라 `causality_ids: list[str]` 구조를 권장한다.

권장 필드 구조:

primary\_causality\_id  
causality\_ids  
causality\_role  
causality\_direction

추천 `causality_role` 값:

ROOT\_CAUSE  
CONTRIBUTING\_CAUSE  
DERIVED\_CAUSE  
RESULTING\_ACTION  
OBSERVED\_EFFECT

추천 `causality_direction` 값:

CAUSE\_TO\_EFFECT  
EFFECT\_TO\_CAUSE  
BIDIRECTIONAL\_RECONSTRUCTION

---

## **8.5 Multi-Causality Scenario: Gas Critical \+ Worker Location \+ Ventilation Degraded**

상황:

GasSensor\_01 reports CRITICAL gas level.  
WorkerLocationState indicates workers may be present in Zone\_A.  
VentilationSystemState is DEGRADED.  
Emergency gas policy is ACTIVE.

인과 구조:

causality\_id\_1: GasSensor\_01 critical reading  
causality\_id\_2: WorkerLocationState near Zone\_A  
causality\_id\_3: VentilationSystemState degraded

primary\_causality\_id: causality\_id\_1  
causality\_ids:  
  \- causality\_id\_1  
  \- causality\_id\_2  
  \- causality\_id\_3

결과 흐름:

GasSensor critical event  
\+ Worker presence risk  
\+ Ventilation degraded  
→ Emergency Policy Bypass  
→ Evacuation Warning  
→ Stop Work Request  
→ Access Restriction  
→ Post-Hoc Audit

이 경우 하나의 Emergency Bypass는 여러 원인 causality를 가진다.

각 결과 action은 동일한 `correlation_id`를 공유할 수 있고, 각 action은 동일한 `causality_ids` 또는 하위 causality chain을 참조할 수 있다.

권장 기록 방식:

EmergencyBypassRecord  
  primary\_causality\_id \= GasSensor critical event  
  causality\_ids \= \[gas critical, worker presence risk, ventilation degraded\]

EvacuationWarning AuditRecord  
  causality\_role \= RESULTING\_ACTION  
  causality\_direction \= CAUSE\_TO\_EFFECT

AccessRestriction AuditRecord  
  causality\_role \= RESULTING\_ACTION  
  causality\_direction \= CAUSE\_TO\_EFFECT

PostHocAudit AuditRecord  
  causality\_role \= OBSERVED\_EFFECT  
  causality\_direction \= BIDIRECTIONAL\_RECONSTRUCTION

---

## **8.6 parent\_trace\_id**

`parent_trace_id`는 분산 trace에서 부모-자식 관계를 표현한다.

---

## **8.7 root\_event\_id**

`root_event_id`는 전체 흐름을 발생시킨 최초 Event를 가리킨다.

---

## **8.8 공통 ID 규격**

감사 기록과 참조 ID는 일관된 규격을 가져야 한다.

권장 규격은 다음 중 하나다.

UUIDv4  
16-byte / 128-bit BLAKE2b hash-based virtual IRI

BLAKE2b 기반 virtual IRI 예시:

urn:ledo:audit:\<128bit\_hash\_hex\>  
urn:ledo:evidence:\<128bit\_hash\_hex\>  
urn:ledo:trace:\<128bit\_hash\_hex\>

참조 필드의 접미사가 `_ref`인 경우, 해당 값은 단순 중첩 객체가 아니라 안정적으로 해석 가능한 식별자여야 한다.

예시:

evidence\_bundle\_ref  
policy\_decision\_ref  
safety\_gate\_result\_ref  
execution\_request\_ref  
external\_control\_request\_ref  
feedback\_event\_ref

핵심 원칙:

A \*\_ref field must reference a stable object identity.  
A \*\_ref field must not imply embedded object nesting.  
Audit IDs must be globally unique within the platform boundary.  
Critical audit references should be resolvable across storage boundaries.

---

# **9\. AuditRecord**

AuditRecord는 감사의 기본 단위다.

AuditRecord는 다음을 기록해야 한다.

actor  
action  
target  
time  
reason  
result  
trace  
causality  
context snapshot reference  
integrity

AuditRecord는 단순 로그가 아니다.

AuditRecord는 책임성과 재현성을 위한 구조화된 기록이다.

AuditRecordDTO는 모든 정책, 증거, 상태, 실행 context를 직접 들고 있지 않는다.

AuditRecordDTO는 경량 객체로 유지하고, 상세 맥락은 `AuditContextSnapshot` 또는 `DecisionTrace`로 연결한다.

---

## **9.1 AuditRecordDTO**

추천 필드:

audit\_record\_id  
audit\_event\_type  
actor\_ref  
actor\_role  
action\_type  
target\_entity\_refs  
result\_status  
risk\_level  
severity  
audit\_reason  
audit\_context\_snapshot\_ref  
decision\_trace\_ref  
created\_at  
occurred\_at  
time\_trust\_level  
clock\_sync\_status  
source\_system\_ref  
trace\_id  
correlation\_id  
decision\_trace\_id  
primary\_causality\_id  
causality\_ids  
integrity\_policy\_ref  
content\_hash  
previous\_record\_hash  
integrity\_status

`audit_record_id`와 모든 `_ref` 접미사 필드는 안정적인 ID 규격을 따라야 한다.

권장 규격:

UUIDv4  
or  
16-byte / 128-bit BLAKE2b hash-based virtual IRI

AuditRecordDTO는 모든 payload를 직접 담지 않는다.

상세 payload는 참조로 연결한다.

---

## **9.2 AuditContextSnapshotDTO**

`AuditContextSnapshotDTO`는 감사 시점의 상세 판단 맥락을 묶는 객체다.

이 객체를 분리하는 이유는 다음과 같다.

AuditRecordDTO 경량화  
중복 필드 감소  
감사 context 재사용  
DecisionTrace와 AuditRecord의 연결 단순화  
Evidence, Policy, State, Safety Gate, Execution context 분리

추천 필드:

audit\_context\_snapshot\_id  
event\_refs  
state\_snapshot\_refs  
evidence\_bundle\_refs  
policy\_decision\_refs  
policy\_version\_refs  
policy\_resolution\_refs  
approval\_decision\_refs  
safety\_gate\_result\_refs  
execution\_request\_refs  
external\_control\_request\_refs  
feedback\_event\_refs  
reconciliation\_refs  
ai\_output\_refs  
slm\_output\_refs  
actor\_clearance\_refs  
target\_ontology\_classes  
time\_trust\_level  
clock\_sync\_status  
device\_health\_snapshot\_refs  
adapter\_status\_refs  
network\_health\_snapshot\_refs  
created\_at  
trace\_id  
correlation\_id  
decision\_trace\_id  
causality\_ids

---

## **9.3 AuditRecord와 DecisionTrace의 관계**

`AuditRecord`는 개별 감사 사건의 기록이다.

`DecisionTrace`는 판단 흐름 전체를 재구성하기 위한 체인이다.

권장 구조:

AuditRecord  
→ audit\_context\_snapshot\_ref  
→ decision\_trace\_ref  
→ related object refs

예시:

SAFETY\_GATE\_BLOCKED AuditRecord  
→ AuditContextSnapshot  
   → safety\_gate\_result\_refs  
   → evidence\_bundle\_refs  
   → state\_snapshot\_refs  
   → policy\_decision\_refs  
→ DecisionTrace  
   → ActionCandidate  
   → PolicyDecision  
   → ApprovalDecision  
   → SafetyGateResult

---

# **10\. Audit Event Type**

Audit Event Type은 감사 대상 이벤트의 유형을 정의한다.

추천 값:

OBJECT\_CANONICALIZED  
ONTOLOGY\_BINDING\_CREATED  
ONTOLOGY\_BINDING\_CHANGED  
EVIDENCE\_CREATED  
EVIDENCE\_VALIDATED  
STATE\_UPDATED  
STATE\_RECONCILED  
ACTION\_CANDIDATE\_CREATED  
AI\_OUTPUT\_USED  
SLM\_OUTPUT\_USED  
DECISION\_CASE\_CREATED  
POLICY\_DECISION\_EVALUATED  
POLICY\_CONFLICT\_RESOLVED  
POLICY\_EXCEPTION\_USED  
GRACE\_PERIOD\_USED  
APPROVAL\_REQUESTED  
APPROVAL\_GRANTED  
APPROVAL\_DENIED  
APPROVAL\_EXPIRED  
SAFETY\_GATE\_PASSED  
SAFETY\_GATE\_BLOCKED  
SAFETY\_GATE\_REVALIDATION\_REQUIRED  
EXECUTION\_REQUEST\_CREATED  
EXTERNAL\_CONTROL\_REQUEST\_DISPATCHED  
EXTERNAL\_CONTROL\_REQUEST\_ACKNOWLEDGED  
EXTERNAL\_CONTROL\_REQUEST\_ACCEPTED  
EXTERNAL\_CONTROL\_REQUEST\_REJECTED  
EXTERNAL\_CONTROL\_REQUEST\_TIMEOUT  
FEEDBACK\_RECEIVED  
FEEDBACK\_MISSING  
RETRY\_ATTEMPTED  
IDEMPOTENCY\_CONFLICT\_DETECTED  
EMERGENCY\_POLICY\_BYPASS\_ACTIVATED  
POST\_HOC\_AUDIT\_CREATED  
MANUAL\_OVERRIDE\_REQUIRED  
MANUAL\_OVERRIDE\_PERFORMED  
RECOVERY\_REQUIRED  
FAIL\_SAFE\_TRIGGERED  
INCIDENT\_CREATED

---

# **11\. Observability Signal**

Observability Signal은 시스템 운영 상태를 관측하기 위한 신호다.

추천 유형:

LogEvent  
MetricEvent  
TraceSpan  
HealthEvent  
AlertEvent  
IncidentRecord  
TelemetrySnapshot

---

## **11.1 LogEvent**

LogEvent는 컴포넌트 수준의 국소 이벤트다.

추천 필드:

log\_event\_id  
component\_name  
log\_level  
message  
event\_type  
target\_ref  
error\_code  
error\_detail\_ref  
created\_at  
trace\_id  
correlation\_id  
decision\_trace\_id

추천 log level:

DEBUG  
INFO  
WARNING  
ERROR  
CRITICAL

---

## **11.2 MetricEvent**

MetricEvent는 수치형 관측 지표다.

추천 필드:

metric\_event\_id  
metric\_name  
metric\_value  
metric\_unit  
component\_name  
target\_ref  
window\_start  
window\_end  
created\_at  
trace\_id  
correlation\_id

추천 metric 예시:

policy\_decision\_latency\_ms  
safety\_gate\_latency\_ms  
adapter\_dispatch\_latency\_ms  
adapter\_ack\_timeout\_count  
adapter\_acceptance\_timeout\_count  
feedback\_missing\_count  
execution\_success\_rate  
state\_reconciliation\_count  
evidence\_stale\_block\_count  
emergency\_bypass\_count

---

## **11.3 TraceSpan**

TraceSpan은 분산 요청 흐름의 한 구간이다.

추천 필드:

span\_id  
trace\_id  
parent\_span\_id  
span\_name  
component\_name  
operation\_name  
start\_time  
end\_time  
duration\_ms  
status  
error\_code  
target\_ref  
metadata\_ref

---

## **11.4 HealthEvent**

HealthEvent는 시스템 컴포넌트의 건강 상태를 표현한다.

추천 필드:

health\_event\_id  
component\_name  
component\_type  
health\_status  
availability\_status  
latency\_ms  
error\_rate  
last\_heartbeat\_at  
degraded\_reason  
created\_at  
trace\_id

추천 health status:

HEALTHY  
DEGRADED  
UNHEALTHY  
OFFLINE  
UNKNOWN

---

## **11.5 AlertEvent**

AlertEvent는 운영자에게 알려야 하는 이벤트다.

추천 필드:

alert\_event\_id  
alert\_type  
severity  
message  
target\_refs  
trigger\_event\_refs  
recommended\_action\_refs  
created\_at  
acknowledged\_by  
acknowledged\_at  
trace\_id  
correlation\_id

추천 severity:

INFO  
NOTICE  
WARNING  
HIGH  
CRITICAL  
EMERGENCY

---

## **11.6 IncidentRecord**

IncidentRecord는 여러 이벤트, 알림, 상태 변화, 조치, 피드백을 하나의 사건으로 묶는다.

추천 필드:

incident\_id  
incident\_type  
severity  
root\_event\_ref  
related\_event\_refs  
related\_alert\_refs  
related\_audit\_record\_refs  
target\_entity\_refs  
state\_snapshot\_refs  
evidence\_bundle\_refs  
action\_refs  
execution\_request\_refs  
feedback\_event\_refs  
status  
created\_at  
closed\_at  
owner\_ref  
trace\_id  
correlation\_id  
causality\_ids

---

# **12\. Decision Trace**

DecisionTrace는 판단 경로를 재구성하기 위한 추적 모델이다.

DecisionTrace는 다음을 연결한다.

ActionCandidate  
DecisionCase  
PolicyDecision  
PolicyResolutionRecord  
ApprovalDecision  
SafetyGateResult  
ExecutionRequest

추천 필드:

decision\_trace\_id  
root\_event\_ref  
action\_candidate\_refs  
decision\_case\_ref  
policy\_decision\_refs  
policy\_resolution\_refs  
approval\_decision\_refs  
safety\_gate\_result\_refs  
execution\_request\_refs  
final\_decision\_result  
created\_at  
trace\_id  
correlation\_id  
causality\_ids

DecisionTraceDTO는 MVP Phase 1부터 포함해야 한다.

이유는 다음과 같다.

초기부터 판단 흐름을 재구성할 수 있다.  
PolicyDecision, ApprovalDecision, SafetyGateResult 연결을 테스트할 수 있다.  
나중에 Audit Query Service 구현이 쉬워진다.

---

# **13\. Policy Audit**

정책 관련 모든 변화와 판단은 감사되어야 한다.

감사 대상:

policy created  
policy reviewed  
policy approved  
policy activated  
policy deprecated  
policy retired  
policy blocked  
policy decision evaluated  
policy conflict resolved  
policy exception requested  
policy exception approved  
policy exception used

Policy Audit는 Policy Governance Model의 PolicyAuditEventDTO와 연결된다.

---

# **14\. Approval Audit**

승인은 고위험 시스템에서 가장 중요한 감사 대상 중 하나다.

감사 대상:

approval requested  
approval granted  
approval denied  
approval expired  
approval revoked  
approval escalated  
approval bypassed by emergency policy

Approval Audit는 다음 정보를 반드시 포함해야 한다.

approver\_ref  
approver\_role  
approver\_clearance\_refs  
approval\_level  
approval\_reason  
approved\_action\_ref  
policy\_decision\_refs  
evidence\_bundle\_refs  
valid\_until  
trace\_id  
decision\_trace\_id

---

# **15\. Safety Gate Audit**

Safety Gate 결과는 반드시 감사되어야 한다.

감사 대상:

SAFETY\_GATE\_PASSED  
SAFETY\_GATE\_BLOCKED  
SAFETY\_GATE\_REVALIDATION\_REQUIRED  
SAFETY\_GATE\_FAIL\_SAFE\_REQUIRED  
SAFETY\_GATE\_MANUAL\_OVERRIDE\_REQUIRED

Safety Gate Audit는 다음을 포함해야 한다.

approved\_action\_ref  
safety\_gate\_result\_ref  
failure\_codes  
evidence\_refs  
state\_snapshot\_refs  
policy\_refs  
time\_trust\_level  
device\_health\_snapshot\_refs  
adapter\_status\_refs  
trace\_id  
decision\_trace\_id

---

# **16\. Execution Audit**

Execution Audit는 Execution Adapter Model과 직접 연결된다.

감사 대상:

EXECUTION\_REQUEST\_CREATED  
EXTERNAL\_CONTROL\_REQUEST\_DISPATCHED  
EXTERNAL\_CONTROL\_REQUEST\_ACKNOWLEDGED  
EXTERNAL\_CONTROL\_REQUEST\_ACCEPTED  
EXTERNAL\_CONTROL\_REQUEST\_REJECTED  
EXTERNAL\_CONTROL\_REQUEST\_TIMEOUT  
FEEDBACK\_RECEIVED  
FEEDBACK\_MISSING  
RETRY\_ATTEMPTED  
IDEMPOTENCY\_CONFLICT\_DETECTED  
RECOVERY\_REQUIRED

Execution Audit는 다음을 연결해야 한다.

approved\_action\_ref  
execution\_request\_ref  
external\_control\_request\_ref  
adapter\_ref  
adapter\_mode  
external\_system\_ref  
idempotency\_key  
dispatch\_status  
feedback\_event\_ref  
failure\_code  
recovery\_result  
trace\_id  
decision\_trace\_id

---

## **16.1 DispatchStatus와 AuditEventType 매핑**

Execution Adapter Model의 `DispatchStatus`는 AuditEventType과 연결되어야 한다.

| DispatchStatus | AuditEventType | 설명 |
| ----- | ----- | ----- |
| CREATED | EXECUTION\_REQUEST\_CREATED | 내부 실행 요청 생성 |
| DISPATCHED | EXTERNAL\_CONTROL\_REQUEST\_DISPATCHED | 외부 시스템 요청 전송 |
| ACKNOWLEDGED | EXTERNAL\_CONTROL\_REQUEST\_ACKNOWLEDGED | 외부 시스템 또는 통신 계층 수신 확인 |
| ACCEPTED | EXTERNAL\_CONTROL\_REQUEST\_ACCEPTED | 외부 시스템 애플리케이션 계층 수락 |
| REJECTED | EXTERNAL\_CONTROL\_REQUEST\_REJECTED | 외부 시스템 거부 |
| ACK\_TIMEOUT | EXTERNAL\_CONTROL\_REQUEST\_TIMEOUT | ACK 시간 초과 |
| ACCEPTANCE\_TIMEOUT | EXTERNAL\_CONTROL\_REQUEST\_TIMEOUT | ACCEPT 시간 초과 |
| FEEDBACK\_TIMEOUT | EXTERNAL\_CONTROL\_REQUEST\_TIMEOUT | Feedback 시간 초과 |
| FEEDBACK\_MISSING | FEEDBACK\_MISSING | 결과 피드백 누락 |
| COMPLETED | FEEDBACK\_RECEIVED | 완료 피드백 수신 |
| PARTIAL\_SUCCESS | FEEDBACK\_RECEIVED | 부분 성공 피드백 수신 |
| FAILED | FEEDBACK\_RECEIVED | 실패 피드백 수신 |
| RECOVERY\_REQUIRED | RECOVERY\_REQUIRED | 복구 필요 |
| MANUAL\_OVERRIDE\_REQUIRED | MANUAL\_OVERRIDE\_REQUIRED | 수동 개입 필요 |

이 매핑은 Execution Adapter Model과 Audit Observability Model의 연결을 명확히 한다.

---

# **17\. Evidence Audit**

Evidence는 판단의 근거이므로 사용 이력이 감사되어야 한다.

감사 대상:

evidence created  
evidence validated  
evidence expired  
evidence revoked  
evidence conflicted  
evidence used in decision  
evidence used in Safety Gate  
evidence used in emergency bypass

Evidence Audit는 Evidence Model의 다음 필드를 참조해야 한다.

source\_trust\_level  
time\_trust\_level  
clock\_sync\_status  
clock\_drift\_estimate\_ms  
device\_health\_snapshot\_ref  
freshness\_status  
trust\_upgrade\_status  
attestation\_status  
conflict\_status

---

# **18\. AI / SLM Audit**

AI 또는 SLM 출력이 판단 흐름에 사용되면 반드시 감사되어야 한다.

감사 대상:

AI output generated  
SLM output generated  
AI output used in ActionCandidate  
SLM output used in RiskInterpretation  
AI output used in EvidenceSummary  
SLM output used in MappingProposal  
AI output rejected by policy  
AI output blocked from execution

AI / SLM Audit는 다음 정보를 포함해야 한다.

model\_id  
model\_version  
prompt\_ref  
input\_context\_hash  
output\_ref  
output\_type  
output\_confidence  
ai\_governance\_policy\_ref  
used\_as\_evidence  
used\_as\_candidate  
approved\_for\_execution  
trace\_id  
decision\_trace\_id

중요한 원칙:

AI or SLM output may be audited as input.  
AI or SLM output must not be audited as final authority.

즉, AI/SLM 출력은 판단 흐름의 입력으로 기록될 수 있지만, 최종 승인권자로 기록되어서는 안 된다.

---

# **19\. Emergency and Post-Hoc Audit**

Emergency Policy Bypass가 발생하면 사후 감사가 필수다.

감사 대상:

emergency policy activated  
emergency bypass used  
normal approval bypassed  
minimum evidence checked  
Safety Gate evaluated  
external request dispatched  
feedback received  
post-hoc audit created  
post-hoc audit reviewed

Post-Hoc Audit는 다음 질문에 답해야 한다.

정말 비상 상황이었는가?  
사전 승인된 emergency policy가 존재했는가?  
최소 검증 증거가 있었는가?  
target은 canonical object였는가?  
Safety Gate는 통과했는가?  
외부 요청은 적절했는가?  
feedback은 수신되었는가?  
정책 남용은 없었는가?  
정책 수정이 필요한가?

---

# **20\. Grace Period Audit**

Grace Period가 사용되면 반드시 감사되어야 한다.

감사 대상:

communication loss detected  
grace period evaluated  
grace period allowed  
grace period denied  
local safe action allowed  
fail-safe required  
manual override required  
reconnect reconciliation performed

Grace Period Audit는 다음을 포함해야 한다.

grace\_policy\_ref  
connectivity\_status  
disconnected\_since  
last\_successful\_sync\_at  
last\_verified\_state\_snapshot\_ref  
last\_verified\_evidence\_bundle\_ref  
allowed\_action\_modes  
denied\_action\_types  
trace\_id  
correlation\_id  
decision\_trace\_id

---

# **21\. Reconciliation Audit**

World State Reconciliation은 감사 대상이다.

감사 대상:

state conflict detected  
state reconciliation started  
state reconciliation succeeded  
state reconciliation failed  
external feedback used for reconciliation  
manual reconciliation required

Reconciliation Audit는 다음을 연결해야 한다.

previous\_state\_snapshot\_ref  
new\_state\_snapshot\_ref  
feedback\_event\_refs  
evidence\_bundle\_refs  
conflict\_type  
resolution\_strategy  
reconciliation\_result  
trace\_id  
correlation\_id

---

# **22\. Edge / Offline Audit**

현장 Edge 환경에서는 중앙 시스템과 통신이 끊길 수 있다.

이때도 감사 기록은 사라지면 안 된다.

Edge Audit Buffer가 필요하다.

Edge Audit Buffer는 다음을 보장해야 한다.

local audit events are buffered  
local audit event order is preserved  
local sequence number is assigned  
local time and platform time are both preserved when possible  
audit records are synced after reconnect  
conflicts are reconciled after reconnect

추천 필드:

edge\_audit\_event\_id  
edge\_node\_ref  
local\_sequence\_number  
local\_created\_at  
platform\_time\_ref  
sync\_status  
synced\_at  
conflict\_status  
trace\_id  
correlation\_id  
decision\_trace\_id

---

## **22.1 Edge Audit Sync Conflict Strategy**

Reconnect 이후 Edge Audit Buffer와 중앙 Audit Store 사이에 충돌이 발생할 수 있다.

충돌 예시:

동일한 idempotency\_key에 대해 서로 다른 dispatch\_status가 존재한다.  
Edge에서는 FEEDBACK\_MISSING인데 중앙에서는 FEEDBACK\_RECEIVED이다.  
Edge의 local time과 platform time 순서가 다르다.  
같은 external\_control\_request\_ref에 대해 서로 다른 결과가 기록되었다.

권장 conflict strategy:

APPEND\_ONLY\_MERGE  
SOURCE\_TRUST\_PRIORITY  
TIME\_TRUST\_PRIORITY  
MANUAL\_REVIEW\_REQUIRED  
MARK\_AS\_CONFLICTED  
REJECT\_UNTRUSTED\_RECORD

각 의미:

APPEND\_ONLY\_MERGE  
→ 기존 record를 덮어쓰지 않고 새 record로 병합한다.

SOURCE\_TRUST\_PRIORITY  
→ 더 신뢰도 높은 source\_system\_ref의 record를 우선한다.

TIME\_TRUST\_PRIORITY  
→ time\_trust\_level과 clock\_sync\_status가 더 좋은 record를 우선한다.

MANUAL\_REVIEW\_REQUIRED  
→ 자동 병합이 위험할 경우 사람 검토로 보낸다.

MARK\_AS\_CONFLICTED  
→ 충돌 상태로 표시하고 후속 reconciliation을 요구한다.

REJECT\_UNTRUSTED\_RECORD  
→ 신뢰할 수 없는 record를 감사 체인에 포함하지 않는다.

주의할 점:

Audit record는 overwrite하지 않는다.  
충돌 해결도 새로운 AuditRecord로 남긴다.  
High-risk 또는 emergency 관련 충돌은 manual review를 기본값으로 둔다.

---

# **23\. Tamper-Evident Audit**

AuditRecord는 변경 가능하면 안 된다.

감사 기록은 append-only 원칙을 따라야 한다.

추천 원칙:

Audit records should be append-only.  
Correction should create a new audit record, not overwrite the old one.  
Critical audit records should include content hash.  
Audit chains should preserve previous\_record\_hash when needed.  
Policy changes and emergency bypass records require stronger integrity guarantees.

하지만 모든 로컬 로그, 모든 metric, 모든 debug event에 강한 hash chain을 적용하면 Edge 장비에서 I/O 병목이 발생할 수 있다.

따라서 Tamper-Evident 체인은 차등 적용되어야 한다.

---

## **23.1 Integrity Level**

권장 무결성 레벨:

NONE  
BASIC\_HASH  
CHAINED\_HASH  
SIGNED\_CHAIN  
EXTERNAL\_ANCHOR

각 의미:

NONE  
→ 무결성 체인 없음

BASIC\_HASH  
→ 개별 record content hash만 저장

CHAINED\_HASH  
→ previous\_record\_hash를 포함한 체인

SIGNED\_CHAIN  
→ 서명 참조 포함

EXTERNAL\_ANCHOR  
→ 외부 immutable store 또는 별도 anchor에 기록

---

## **23.2 IntegrityLevel 적용 결정 테이블**

| 조건 | 권장 IntegrityLevel | 설명 |
| ----- | ----- | ----- |
| DEBUG log | NONE 또는 BASIC\_HASH | 개발·진단용 로그 |
| INFO metric | NONE 또는 BASIC\_HASH | 일반 성능 지표 |
| severity \= NOTICE | BASIC\_HASH | 추후 확인 가능성 확보 |
| severity \>= WARNING | CHAINED\_HASH | 운영상 의미 있는 경고 이상 |
| risk\_level \>= HIGH\_RISK | CHAINED\_HASH | 고위험 판단·실행 기록 |
| SAFETY\_GATE\_BLOCKED | CHAINED\_HASH | 안전 차단 기록 |
| SAFETY\_GATE\_PASSED for high-risk action | CHAINED\_HASH | 고위험 실행 전 통과 기록 |
| EXECUTION\_REQUEST\_CREATED for high-risk action | CHAINED\_HASH | 고위험 실행 요청 생성 |
| EXTERNAL\_CONTROL\_REQUEST\_DISPATCHED for high-risk action | CHAINED\_HASH | 고위험 외부 요청 전송 |
| POLICY\_EXCEPTION\_USED | SIGNED\_CHAIN | 정책 예외 사용 |
| POLICY\_CONFLICT\_RESOLVED | CHAINED\_HASH | 정책 충돌 해결 |
| IDEMPOTENCY\_CONFLICT\_DETECTED | CHAINED\_HASH | 중복 실행 위험 |
| MANUAL\_OVERRIDE\_PERFORMED | SIGNED\_CHAIN | 사람의 수동 개입 |
| FAIL\_SAFE\_TRIGGERED | SIGNED\_CHAIN | 안전 복구 조치 |
| EMERGENCY\_POLICY\_BYPASS\_ACTIVATED | SIGNED\_CHAIN 또는 EXTERNAL\_ANCHOR | 비상 정책 우회 |
| POST\_HOC\_AUDIT\_CREATED | SIGNED\_CHAIN 또는 EXTERNAL\_ANCHOR | 사후 감사 생성 |

추천 필드:

integrity\_policy\_id  
applicable\_audit\_event\_types  
minimum\_severity  
minimum\_risk\_level  
integrity\_level  
requires\_previous\_record\_hash  
requires\_signature  
requires\_external\_anchor  
owner  
version  
status

핵심 원칙:

All audit records should be append-only.  
Not all observability signals require chained hashing.  
Critical audit records require stronger integrity guarantees.  
Edge runtime efficiency must be considered.

---

# **24\. Privacy and PII Handling**

Audit와 Observability는 민감 정보를 포함할 수 있다.

따라서 개인정보와 민감 정보 처리가 필요하다.

원칙:

Audit must preserve accountability.  
Privacy policy must restrict unnecessary exposure.  
PII should be masked or tokenized when possible.  
Access to sensitive audit records must be policy-controlled.  
Audit export must be strongly controlled.

추천 필드:

pii\_present  
pii\_category  
masking\_status  
redaction\_ref  
access\_policy\_refs  
retention\_policy\_ref  
export\_control\_required

---

# **25\. Retention Policy**

Audit와 Observability 데이터는 보존 기간이 다를 수 있다.

예시:

debug logs  
→ short retention

metrics  
→ medium retention

high-risk audit records  
→ long retention

emergency bypass audit  
→ long retention

PII-heavy raw payload  
→ minimized or redacted retention

Retention Policy는 다음을 정의해야 한다.

record\_type  
risk\_level  
pii\_present  
pii\_category  
retention\_period  
archive\_policy  
deletion\_policy  
redaction\_policy  
legal\_hold\_required  
owner  
version

---

## **25.1 PII Retention Boundary**

PII가 포함된 Audit/Observability 데이터는 별도 보존 기준을 가져야 한다.

권장 분류:

NO\_PII  
PSEUDONYMIZED\_PII  
DIRECT\_PII  
SENSITIVE\_PII  
PII\_HEAVY\_PAYLOAD

권장 원칙:

NO\_PII  
→ 일반 retention policy 적용

PSEUDONYMIZED\_PII  
→ 감사 목적에 필요한 기간 동안 보존 가능

DIRECT\_PII  
→ 접근 통제와 masking 필요

SENSITIVE\_PII  
→ 최소 보존, 강한 접근 통제, export 제한

PII\_HEAVY\_PAYLOAD  
→ 원본 payload 장기 보존 금지, redacted reference 우선

PII 원본 payload는 감사 책임성에 꼭 필요한 경우를 제외하고 장기 보존하지 않는 것이 원칙이다.

권장 방식:

원본 payload는 짧게 보존한다.  
redacted payload 또는 tokenized reference를 장기 보존한다.  
export는 Policy Governance Model의 Data Privacy Policy를 통과해야 한다.

---

# **26\. Audit Storage Boundary**

Audit 저장소는 운영 로그 저장소와 분리될 수 있다.

권장 분리:

Operational Logs  
→ debugging and runtime diagnostics

Metrics Store  
→ time-series performance and health indicators

Trace Store  
→ distributed request tracing

Audit Store  
→ accountability and compliance-grade records

Evidence Store  
→ evidence objects and validation records

Audit Store는 책임성과 보존성을 우선한다.

Observability Store는 운영성과 성능 분석을 우선한다.

---

# **27\. Audit Query Model**

감사자는 다음 질문을 질의할 수 있어야 한다.

이 ActionCandidate는 어떤 증거로 생성되었는가?  
이 Action은 누가 승인했는가?  
이 정책 판단은 어떤 정책 버전을 사용했는가?  
Safety Gate가 왜 차단했는가?  
이 ExecutionRequest는 어떤 외부 시스템에 전달되었는가?  
외부 시스템은 ACK, ACCEPT, COMPLETE 중 어디까지 응답했는가?  
Feedback이 누락된 요청은 무엇인가?  
Emergency Bypass가 사용된 모든 사례는 무엇인가?  
SLM 출력이 실행 흐름에 들어간 적이 있는가?  
이 감사 기록은 어떤 integrity policy를 따랐는가?  
이 incident는 단일 원인인가, 다중 원인인가?

Audit Query는 다음 기준으로 가능해야 한다.

trace\_id  
correlation\_id  
decision\_trace\_id  
causality\_ids  
target\_entity\_ref  
actor\_ref  
policy\_ref  
audit\_event\_type  
severity  
risk\_level  
integrity\_policy\_ref

---

## **27.1 Audit Query Example 1: ExecutionRequest가 ACK까지 갔는가, ACCEPT까지 갔는가?**

질문:

ExecutionRequest ER-001은 외부 시스템에서 ACK까지만 갔는가, ACCEPT까지 갔는가?

개념 질의:

Find AuditRecords  
where execution\_request\_ref \= "ER-001"  
and audit\_event\_type in \[  
  EXTERNAL\_CONTROL\_REQUEST\_DISPATCHED,  
  EXTERNAL\_CONTROL\_REQUEST\_ACKNOWLEDGED,  
  EXTERNAL\_CONTROL\_REQUEST\_ACCEPTED,  
  EXTERNAL\_CONTROL\_REQUEST\_REJECTED,  
  EXTERNAL\_CONTROL\_REQUEST\_TIMEOUT,  
  FEEDBACK\_RECEIVED  
\]  
order by occurred\_at

기대 결과:

DISPATCHED 있음  
ACKNOWLEDGED 있음  
ACCEPTED 없음  
FEEDBACK\_RECEIVED 없음  
→ ACCEPTANCE\_PENDING 또는 ACCEPTANCE\_TIMEOUT 가능성 확인

---

## **27.2 Audit Query Example 2: Safety Gate가 왜 차단했는가?**

질문:

Safety Gate가 ACTION\_LOCK\_ZONE을 왜 차단했는가?

개념 질의:

Find AuditRecord  
where audit\_event\_type \= SAFETY\_GATE\_BLOCKED  
and action\_type \= ACTION\_LOCK\_ZONE  
and target\_entity\_refs contains Zone\_A

연결 확인:

AuditRecord  
→ audit\_context\_snapshot\_ref  
→ safety\_gate\_result\_refs  
→ failure\_codes  
→ evidence\_bundle\_refs  
→ state\_snapshot\_refs  
→ policy\_decision\_refs

기대 결과:

failure\_code \= EVIDENCE\_STALE  
or  
failure\_code \= STATE\_CONFLICT\_UNRESOLVED  
or  
failure\_code \= POLICY\_DENIED

---

## **27.3 Audit Query Example 3: Emergency Bypass가 어떤 원인으로 발생했는가?**

질문:

Emergency Bypass EB-001은 단일 원인인가, 다중 원인인가?

개념 질의:

Find AuditRecord  
where audit\_event\_type \= EMERGENCY\_POLICY\_BYPASS\_ACTIVATED  
and emergency\_bypass\_ref \= "EB-001"

연결 확인:

AuditRecord  
→ causality\_ids  
→ related Evidence  
→ related StateSnapshot  
→ related Event

기대 결과:

causality\_ids:  
\- GasSensor critical reading  
\- WorkerLocation near danger zone  
\- VentilationSystem degraded

→ Multi-causality emergency bypass

---

# **28\. 다른 Core Specification과의 연결**

## **28.1 Canonical Object Lifecycle**

Audit 대상 target은 canonical object 기준이어야 한다.

target\_entity\_ref must be canonicalized.  
target ontology binding must be known.  
target lifecycle status must be recorded.

---

## **28.2 Common Schema DTO**

모든 Audit, Log, Metric, Trace DTO는 공통 식별자를 가져야 한다.

trace\_id  
correlation\_id  
schema\_version  
created\_at  
status  
version

---

## **28.3 Event Type Taxonomy**

AuditEventType은 Event Type Taxonomy와 연결될 수 있다.

예시:

safety.worker.entered\_danger\_zone  
→ ACTION\_CANDIDATE\_CREATED  
→ POLICY\_DECISION\_EVALUATED  
→ SAFETY\_GATE\_PASSED  
→ EXECUTION\_REQUEST\_CREATED

---

## **28.4 Action Type Registry**

Audit는 action\_type을 기록해야 한다.

예시:

ACTION\_STOP\_WORK  
ACTION\_LOCK\_ZONE  
ACTION\_RETURN\_ROBOT\_TO\_SAFE\_ZONE

---

## **28.5 State Model Registry**

Audit는 state\_snapshot\_ref를 기록해야 한다.

---

## **28.6 Evidence Model**

Audit는 evidence\_bundle\_refs를 기록해야 한다.

---

## **28.7 Decision / Approval Matrix**

Audit는 decision route와 approval level을 기록해야 한다.

---

## **28.8 Policy Governance Model**

Audit는 policy\_decision\_refs, policy\_version\_refs, policy\_resolution\_refs를 기록해야 한다.

---

## **28.9 Execution Adapter Model**

Audit는 execution\_request\_refs, external\_control\_request\_refs, feedback\_event\_refs를 기록해야 한다.

---

# **29\. MVP 범위**

## **29.1 MVP Phase 1**

MVP Phase 1에서는 다음을 구현한다.

AuditRecordDTO  
AuditContextSnapshotDTO  
LogEventDTO  
MetricEventDTO  
TraceSpanDTO  
HealthEventDTO  
AlertEventDTO  
IncidentRecordDTO  
DecisionTraceDTO  
IntegrityPolicyDTO  
AuditEventType enum  
Severity enum  
HealthStatus enum  
AuditWriter interface  
InMemoryAuditWriter  
FileAuditWriter  
BasicTraceContext  
basic content\_hash support  
pytest unit tests

Phase 1에서는 외부 observability stack이 없어도 된다.

InMemoryAuditWriter와 FileAuditWriter만으로도 충분하다.

DecisionTraceDTO는 Phase 1부터 포함해야 한다.

---

## **29.2 MVP Phase 2**

MVP Phase 2에서는 다음을 추가한다.

StructuredLogWriter  
MetricCollector  
TraceCollector  
AuditStoreRepository  
EdgeAuditBuffer  
AuditQueryService  
PolicyAudit integration  
SafetyGateAudit integration  
ExecutionAudit integration  
FeedbackAudit integration  
IntegrityPolicyEvaluator  
EdgeAuditConflictResolver

---

## **29.3 MVP Phase 3**

MVP Phase 3에서는 다음을 추가한다.

OpenTelemetry-compatible trace exporter  
Metrics dashboard  
Audit dashboard  
Incident timeline view  
Emergency bypass audit view  
SLM / LLM audit view  
Tamper-evident audit chain  
PII masking and redaction workflow  
Integrity policy dashboard  
Audit query UI

---

# **30\. 추천 파일 구조**

src/ledo\_ontology\_core/framework/audit/  
  \_\_init\_\_.py

  enums.py

  audit\_record.py  
  audit\_context\_snapshot.py  
  log\_event.py  
  metric\_event.py  
  trace\_span.py  
  health\_event.py  
  alert\_event.py  
  incident\_record.py  
  decision\_trace.py  
  edge\_audit\_event.py  
  retention\_policy.py  
  integrity\_policy.py

  audit\_writer.py  
  in\_memory\_audit\_writer.py  
  file\_audit\_writer.py  
  audit\_query\_service.py  
  audit\_integrity.py  
  integrity\_policy\_evaluator.py  
  edge\_audit\_conflict\_resolver.py  
  pii\_masker.py  
  trace\_context.py  
  id\_factory.py

tests/unit/framework/audit/  
  test\_audit\_record.py  
  test\_audit\_context\_snapshot.py  
  test\_log\_event.py  
  test\_metric\_event.py  
  test\_trace\_span.py  
  test\_decision\_trace.py  
  test\_in\_memory\_audit\_writer.py  
  test\_file\_audit\_writer.py  
  test\_audit\_integrity.py  
  test\_integrity\_policy.py  
  test\_edge\_audit\_conflict\_resolver.py  
  test\_pii\_masker.py  
  test\_id\_factory.py

---

# **31\. 구현 순서**

권장 구현 순서:

AuditEventType enum  
Severity enum  
HealthStatus enum  
AuditResult enum  
IntegrityStatus enum  
IntegrityLevel enum  
EdgeAuditConflictStrategy enum

AuditRecordDTO  
AuditContextSnapshotDTO  
LogEventDTO  
MetricEventDTO  
TraceSpanDTO  
HealthEventDTO  
AlertEventDTO  
IncidentRecordDTO  
DecisionTraceDTO  
EdgeAuditEventDTO  
RetentionPolicyDTO  
IntegrityPolicyDTO

AuditWriter interface  
InMemoryAuditWriter  
FileAuditWriter  
TraceContext  
IDFactory  
AuditIntegrity  
IntegrityPolicyEvaluator  
EdgeAuditConflictResolver  
PIIMasker  
AuditQueryService  
Unit tests

---

# **32\. 최종 원칙**

Audit Observability Model은 플랫폼의 기억 장치다.

하지만 이 모델은 단순 기록장이 아니다.

이 모델은 다음을 가능하게 한다.

책임 추적  
사후 감사  
장애 분석  
정책 검토  
안전 사고 분석  
AI/SLM 사용 이력 검증  
외부 실행 결과 재구성  
핵심 감사 기록의 무결성 검증  
다중 인과관계 재구성  
Edge 환경의 감사 기록 보존

핵심 원칙은 다음과 같다.

Audit preserves accountability.  
Observability exposes behavior.  
Trace connects causality.  
Multi-causality must be supported.  
Metrics expose system health.  
Logs explain local events.  
Evidence supports decisions.  
Feedback confirms outcomes.  
Emergency bypass requires post-hoc audit.  
AI and SLM outputs must be traceable.  
Audit record IDs and references must be stable.  
AuditRecordDTO should remain lightweight.  
AuditContextSnapshot should preserve detailed decision context.  
Critical audit records should be tamper-evident.  
Not every observability signal requires hash chaining.  
Edge audit conflicts must be resolved without overwriting records.  
Audit records should be append-only.  
Privacy must be protected.

한글로 정리하면 다음과 같다.

Audit는 책임을 보존한다.  
Observability는 동작을 보이게 한다.  
Trace는 인과관계를 연결한다.  
다중 인과관계를 수용해야 한다.  
Metric은 시스템 건강 상태를 보여준다.  
Log는 국소 이벤트를 설명한다.  
Evidence는 판단을 지지한다.  
Feedback은 결과를 확인한다.  
Emergency Bypass는 사후 감사를 요구한다.  
AI와 SLM 출력은 추적 가능해야 한다.  
Audit record ID와 참조 ID는 안정적이어야 한다.  
AuditRecordDTO는 경량화되어야 한다.  
AuditContextSnapshot은 상세 판단 맥락을 보존해야 한다.  
핵심 감사 기록은 tamper-evident해야 한다.  
모든 observability signal에 hash chain을 강제할 필요는 없다.  
Edge audit conflict는 record overwrite 없이 해결되어야 한다.  
Audit record는 append-only 원칙을 따라야 한다.  
Privacy는 보호되어야 한다.

