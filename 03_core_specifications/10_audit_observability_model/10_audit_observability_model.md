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
- Canonical Object  
- Ontology-Bound Object  
- Evidence-Linked Object  
- State-Tracked Object  
- ActionCandidate  
- DecisionCase  
- PolicyDecision  
- ApprovalDecision  
- ApprovedAction  
- Safety Gate  
- ExecutionRequest  
- ExternalControlRequest  
- FeedbackEvent  
- Reconciliation  
- AuditRecord

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
- PolicyDecision  
- ApprovalDecision  
- SafetyGatePass or SafetyGateBlock  
- ExecutionRequest  
- ExternalControlRequest  
- FeedbackEvent

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
- policy engine call  
- Safety Gate call  
- adapter dispatch

---

## **8.2 correlation\_id**

`correlation_id` groups multiple traces into one business or incident unit.

Example:

Worker entered danger zone incident  
- sensor event  
- dashboard alert  
- supervisor approval  
- zone lock request  
- feedback event

---

## **8.3 decision\_trace\_id**

`decision_trace_id` groups the full decision chain.

Example:

ActionCandidate  
- DecisionCase  
- PolicyDecision  
- ApprovalDecision  
- SafetyGatePass or SafetyGateBlock  
- ExecutionRequest

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
- Emergency Policy Bypass  
- Evacuation Warning  
- Stop Work Request  
- Access Restriction  
- Post-Hoc Audit

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

Canonical Reference: `01_common_schema_dto/1_common_schema_dto.md` Section 18.5 is the field-level contract for `AuditRecordDTO`. `AuditRecordDTO` keeps the stage-reference design (`candidate_ref`, `decision_case_ref`, `approved_action_ref`, `execution_request_ref`, `external_request_ref`, `feedback_event_ref`, etc.), for the same reason documented for `ExecutionRequest` in `09_execution_adapter_model.md` Section 7.2 — do not implement it against a reference-only redesign built around a separate `AuditContextSnapshotDTO`.

Fields:

audit\_record\_id  
trace\_id  
lifecycle\_path  
event\_refs  
evidence\_refs  
candidate\_ref  
decision\_case\_ref  
approval\_request\_ref  
approved\_action\_ref  
execution\_request\_ref  
external\_request\_ref  
feedback\_event\_ref  
policy\_refs  
actor\_refs  
final\_status  
created\_at\_utc  
is\_emergency\_bypass  
post\_audit\_status  
post\_hoc\_audit\_ref  
audit\_event\_type  
severity  
audit\_reason  
occurred\_at  
time\_trust\_level  
clock\_sync\_status  
source\_system\_ref  
correlation\_id  
decision\_trace\_id  
primary\_causality\_id  
causality\_ids  
integrity\_policy\_ref  
content\_hash  
previous\_record\_hash  
integrity\_status

The tamper-evident hash chain (`integrity_policy_ref`, `content_hash`, `previous_record_hash`, `integrity_status`) and multi-causality trace correlation (`correlation_id`, `decision_trace_id`, `primary_causality_id`, `causality_ids`, see Sections 8.3-8.5) were the real, non-redundant capability this section originally named that Section 18.5 lacked; they have been merged into Section 18.5 directly. `severity` uses the `Severity` enum. `time_trust_level` uses `TimeTrustLevel` (Section 7.5 of `05_evidence_model.md`). `clock_sync_status` uses `ClockSyncStatus` (Section 7.3 of `05_evidence_model.md`). `audit_event_type` and `integrity_status` remain plain `str`: Section 16.1's dispatch-stage mapping is only a partial value list for `audit_event_type`, and no closed list was found anywhere for `integrity_status`.

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

Not implemented as part of `AuditRecordDTO`'s current canonical shape (`01_common_schema_dto/1_common_schema_dto.md` Section 18.5), which keeps its stage-reference fields directly rather than delegating them to a separate snapshot object — see the Canonical Reference note in Section 9.1. The grouping pattern below remains a documented option for a possible future extension (`AuditContextSnapshotDTO` is a Rollout Stage 1 item per Section 29.1, not a current Step 1 target), not a current build target.

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
- audit\_context\_snapshot\_ref  
- decision\_trace\_ref  
- related object refs

Example:

SAFETY\_GATE\_BLOCKED AuditRecord  
- AuditContextSnapshot  
   - safety\_gate\_result\_refs  
   - evidence\_bundle\_refs  
   - state\_snapshot\_refs  
   - policy\_decision\_refs  
- DecisionTrace  
   - ActionCandidate  
   - PolicyDecision  
   - ApprovalDecision  
   - SafetyGatePass or SafetyGateBlock

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
SafetyGatePass or SafetyGateBlock  
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

DecisionTraceDTO must be included starting with Rollout Stage 1 (Section 29.1).

Reasons:

The decision flow can be reconstructed from the beginning.  
PolicyDecision, ApprovalDecision, and SafetyGatePass or SafetyGateBlock connections can be tested.  
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
- Merge as a new record without overwriting existing records.

SOURCE\_TRUST\_PRIORITY  
- Prioritize the record from the more trusted source\_system\_ref.

TIME\_TRUST\_PRIORITY  
- Prioritize the record with better time\_trust\_level and clock\_sync\_status.

MANUAL\_REVIEW\_REQUIRED  
- Route to human review when automatic merge is risky.

MARK\_AS\_CONFLICTED  
- Mark as conflicted and require follow-up reconciliation.

REJECT\_UNTRUSTED\_RECORD  
- Do not include the untrusted record in the audit chain.

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
- no integrity chain

BASIC\_HASH  
- store only the individual record content hash

CHAINED\_HASH  
- include previous\_record\_hash in the chain

SIGNED\_CHAIN  
- include a signature reference

EXTERNAL\_ANCHOR  
- record to an external immutable store or separate anchor

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
- short retention

metrics  
- medium retention

high-risk audit records  
- long retention

emergency bypass audit  
- long retention

PII-heavy raw payload  
- minimized or redacted retention

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
- apply normal retention policy

PSEUDONYMIZED\_PII  
- may be retained for the period required for audit purposes

DIRECT\_PII  
- requires access control and masking

SENSITIVE\_PII  
- minimal retention, strong access control, export restriction

PII\_HEAVY\_PAYLOAD  
- do not retain original payload long-term; prefer redacted references

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
- debugging and runtime diagnostics

Metrics Store  
- time-series performance and health indicators

Trace Store  
- distributed request tracing

Audit Store  
- accountability and compliance-grade records

Evidence Store  
- evidence objects and validation records

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
- ACCEPTANCE\_PENDING or ACCEPTANCE\_TIMEOUT should be investigated

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
- audit\_context\_snapshot\_ref  
- safety\_gate\_result\_refs  
- failure\_codes  
- evidence\_bundle\_refs  
- state\_snapshot\_refs  
- policy\_decision\_refs

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
- causality\_ids  
- related Evidence  
- related StateSnapshot  
- related Event

Expected interpretation:

causality\_ids:  
\- GasSensor critical reading  
\- WorkerLocation near danger zone  
\- VentilationSystem degraded

- Multi-causality emergency bypass

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
- ACTION\_CANDIDATE\_CREATED  
- POLICY\_DECISION\_EVALUATED  
- SAFETY\_GATE\_PASSED  
- EXECUTION\_REQUEST\_CREATED

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

# **29\. Implementation Rollout Scope**

Note: the "Rollout Stage 1/2/3" labels below are internal to this document only. They are not the same numbering as `07_implementation_plan/implementation_plan.md`'s Phase 0–19, nor the same as `07_implementation_plan/implementation_slice_1/2/3`. `AuditRecordDTO` and the interface-stub `InMemoryAuditWriter`/`FileAuditWriter` are built as part of Implementation Slice 3 (Runtime and Execution); Rollout Stage 2 and 3 below describe later hardening work beyond the current implementation stage.

## **29.1 Rollout Stage 1**

Rollout Stage 1 implements the following:

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

In Rollout Stage 1, an external observability stack is not required.

InMemoryAuditWriter and FileAuditWriter are sufficient.

DecisionTraceDTO must be included starting with Rollout Stage 1.

---

## **29.2 Rollout Stage 2**

Rollout Stage 2 adds the following:

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

## **29.3 Rollout Stage 3**

Rollout Stage 3 adds the following:

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

