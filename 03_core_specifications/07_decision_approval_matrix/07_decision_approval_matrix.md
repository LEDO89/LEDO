# **Ontologic centric Decision / Approval Matrix**

# **1\. Purpose**

This document defines the core rules of the Decision / Approval Matrix used in an ontology-centric cyber-physical platform.

The Decision / Approval Matrix is the structure that determines the following when the platform receives a specific Event, State, Evidence, or ActionCandidate:

Can this situation be handled automatically?  
Is it enough to notify a human?  
Does this situation require supervisor approval?  
Does this situation require safety manager approval?  
Does this situation require war room approval?  
Does this situation require expert review?  
Should this situation be handled immediately through the emergency fast-path?  
Should this situation be rejected due to insufficient evidence?  
Should this situation be held due to stale state?  
Should this situation be routed to fail-safe because of conflict?  
Should this situation be dropped or routed to fail-safe because of network latency or heartbeat issues?  
Is there a TOCTOU risk caused by a state change between approval time and execution time?  
Does this judgment satisfy the time trust, source trust, device health, trust upgrade, and privacy lifecycle requirements defined in the Evidence Model?

If an Event Type expresses "what happened," a State Model expresses "what is currently in what state," an Evidence Model expresses "what proves that judgment," and an Action Type expresses "what response can be taken," then the Decision / Approval Matrix expresses "who must judge and approve at what level under these conditions."

The core principle is as follows:

Decision selects a route.  
Approval grants authority.  
Safety Gate validates execution eligibility.  
ExecutionRequest asks external systems to act.  
Feedback proves execution result.  
Audit preserves accountability.

Decision determines the route.  
Approval grants authority.  
Safety Gate validates execution eligibility.  
ExecutionRequest sends an execution request to an external system.  
Feedback proves the execution result.  
Audit preserves accountability and traceability.

---

# **2\. Document Separation Principle**

The Decision / Approval Matrix document is divided into two parts.

## **2.1 Core Decision / Approval Matrix Specification**

This is the present document.

It covers:

Decision Matrix definition  
Approval Matrix definition  
Difference between Decision and Approval  
Decision Input and Decision Output  
DecisionContext structure  
Risk Level and Severity classification  
Approval Level classification  
Decision Route classification  
Human-in-the-loop rules  
Emergency fast-path rules  
Connection to the Evidence Model  
Connection to state freshness  
TOCTOU prevention rules  
Network latency / heartbeat validation rules  
Connection to conflict handling  
Connection to Safety Gate  
SafetyGatePrecheck execution order  
Policy Engine / PDP / PEP integration  
PolicyEngineAdapter interface definition  
Approval timeout / escalation rules  
Idempotency rule  
AI governance trace rule  
Fallback route priority  
DecisionTrace linkage rule  
DecisionCaseDTO definition  
DecisionContextDTO definition  
ApprovalRequestDTO definition  
ApprovalDecisionDTO definition  
DecisionMatrixSpecDTO definition  
ApprovalMatrixSpecDTO definition  
MVP decision / approval matrix set  
Core scenario flows

## **2.2 Appendix F: Decision / Approval Matrix Catalog**

This is a separate appendix document.

It covers:

safety decision matrix  
robot decision matrix  
construction task decision matrix  
industrial alarm decision matrix  
evidence conflict decision matrix  
approval role matrix  
emergency decision matrix  
policy exception matrix  
mapping review matrix  
audit escalation matrix

By separating the documents this way, the Core document can remain short and stable, while the actual matrix catalog can continue to expand according to field operation policies.

---

# **3\. Definition of Decision / Approval Matrix**

## **3.1 Definition of Decision Matrix**

A Decision Matrix is a set of rules that defines which decision route should be selected in a specific situation.

The Decision Matrix must answer the following questions:

What risk level does this event have?  
Is this state normal, warning, high-risk, or emergency?  
Is this action candidate acceptable?  
Is the required evidence sufficient?  
Is evidence freshness valid?  
Is the time trust level sufficient?  
Is the clock sync status acceptable?  
Is the source trust level sufficient?  
Is the device health snapshot acceptable?  
What is the trust upgrade status?  
Does the privacy lifecycle status affect operational approval?  
Is the state not stale?  
Does conflict exist?  
Is network latency within the allowed range?  
Is the external system heartbeat healthy?  
Has the target state changed between approval time and execution time?  
Can this action be handled automatically?  
Does this action require human approval?  
Is this action subject to the emergency fast-path?  
Should this action be blocked?  
Is this judgment subject to audit?

---

## **3.2 Definition of Approval Matrix**

An Approval Matrix is a set of rules that defines what approval level is required for a specific action or decision.

The Approval Matrix must answer the following questions:

Who can approve it?  
What role is required?  
What clearance is required?  
What approval level is required?  
Is a single approval sufficient?  
Is multi-party approval required?  
Can approval be bypassed under a pre-approved emergency policy?  
If bypassed, is post-hoc audit required?  
What happens when approval times out?  
What recovery path is used if approval is rejected?  
Does the approval result have an idempotency\_key?  
Is the Safety Gate executed within the valid approval period?  
Does the state snapshot at approval time match the state snapshot at execution time?

---

# **4\. Core Distinctions**

## **4.1 Difference Between Decision and Approval**

Decision determines the judgment route.

Approval grants authority.

Example:

Decision:  
This situation requires SAFETY\_MANAGER\_APPROVAL.

Approval:  
Safety Manager Kim approved ACTION\_STOP\_WORK.

Decision is the route.  
Approval is the authority grant.

---

## **4.2 Difference Between Decision and Policy Decision**

The Decision Matrix determines the route at the platform level.

A Policy Decision is a judgment returned by a specific policy engine, such as allow / deny / require\_approval.

Example:

Decision Matrix:  
ZoneRiskState.CRITICAL → emergency route

Policy Decision:  
OPA allows ACTION\_EMERGENCY\_EVACUATE\_ZONE under EmergencyPolicy\_001

The Decision Matrix determines the overall workflow route.  
A Policy Decision is the result of a specific rule set.

---

## **4.3 Difference Between Approval and Safety Gate**

Approval is the act of authorizing an action by a human or policy.

Safety Gate is the final validation structure before an approved action can become an actual execution request.

Example:

Approval:  
Supervisor approved ACTION\_DISABLE\_ROBOT\_MISSION.

Safety Gate:  
Evidence valid?  
Time trust valid?  
Clock sync acceptable?  
Device health acceptable?  
Target valid?  
State fresh?  
Approval still valid?  
TOCTOU risk acceptable?  
Robot capability available?  
No unresolved conflict?  
External adapter available?  
Network latency within threshold?  
External system heartbeat healthy?  
Idempotency key valid?

Even if approval exists, an ExecutionRequest cannot be created unless the Safety Gate is passed.

---

## **4.4 Difference Between Approval and Execution**

Approval is execution authority.

Execution is sending an execution request to an external system.

Example:

ApprovedAction:  
ACTION\_DISABLE\_ROBOT\_MISSION approved.

ExecutionRequest:  
Send disable mission request to FleetManager.

ApprovedAction is not a direct physical control command.

---

## **4.5 Difference Between Emergency Bypass and No Approval**

Emergency bypass does not mean "no approval is required."

Emergency bypass means that an execution request may be allowed before human approval under a predefined emergency policy, while post-hoc audit is required afterward.

Example:

Gas level critical  
- Emergency policy matched  
- EmergencyApprovedAction created  
- EmergencyRuntimeValidationInput prepared  
- EmergencyRuntimeValidationResult produced  
- Emergency Safety Gate evaluated  
- EmergencySafetyGatePass issued or EmergencySafetyGateBlock issued  
- EmergencyExecutionRequest sent only if EmergencySafetyGatePass exists  
- Post-hoc audit required

Emergency bypass is not irresponsible automatic execution.  
Emergency bypass is a structure that combines pre-approved policy with post-hoc audit.

EmergencyApprovedAction grants emergency authority. EmergencySafetyGatePass grants short-lived execution readiness. EmergencySafetyGateBlock prevents EmergencyExecutionRequest creation.

EmergencyExecutionRequest MUST NOT be created unless an EmergencySafetyGatePass has been issued from a valid EmergencyRuntimeValidationResult.

The emergency path may be accelerated, but it must not bypass Runtime Validation or Safety Gate.

---

# **5\. Explicit Connection to the Evidence Model**

The Decision / Approval Matrix must be directly connected to the Evidence Model.

The following values defined in the Evidence Model must be directly referenced in Decision Input or DecisionContext:

clock\_drift\_estimate\_ms  
time\_trust\_level  
clock\_sync\_status  
time\_authority\_ref  
offline\_clock\_trust\_policy\_ref  
source\_trust\_level  
device\_health\_snapshot  
device\_health\_snapshot\_version  
calibration\_status  
historical\_reliability\_score  
trust\_upgrade\_status  
attestation\_type  
conflict\_status  
applied\_conflict\_weights  
privacy\_lifecycle\_status  
legal\_hold\_status  
payload\_hash  
prov\_entity\_ref  
activity\_refs

---

## **5.1 Extending evidence\_freshness\_summary**

`evidence_freshness_summary` must not express only whether evidence is stale.

It must include the following values:

freshness\_status  
captured\_at  
received\_at  
capture\_receive\_delta\_ms  
clock\_sync\_status  
clock\_drift\_estimate\_ms  
time\_trust\_level  
time\_validation\_status  
source\_trust\_level  
device\_health\_status

Example:

evidence\_freshness\_summary \= {  
  freshness\_status: VALID,  
  time\_trust\_level: HIGH\_TIME\_TRUST,  
  clock\_sync\_status: SYNCED,  
  clock\_drift\_estimate\_ms: 120,  
  device\_health\_status: OK  
}

---

## **5.2 Connecting AI\_DERIVED\_ONLY and trust\_upgrade\_status**

The Decision Matrix must connect AI-derived evidence with `trust_upgrade_status` from the Evidence Model.

AI\_DERIVED\_ONLY  
- trust\_upgrade\_status \= NO\_UPGRADE or TRUST\_UPGRADE\_PENDING  
- approval not allowed

ATTESTED\_AI\_DERIVED  
- trust\_upgrade\_status \= TRUST\_UPGRADED\_BY\_RULE / TRUST\_UPGRADED\_BY\_HUMAN / TRUST\_UPGRADED\_BY\_CROSS\_CHECK  
- limited use allowed

AI\_DERIVED\_ONLY can be used for explanation or candidate generation.  
AI\_DERIVED\_ONLY cannot be used as the basis for high-risk approval.  
ATTESTED\_AI\_DERIVED can be used for limited purposes, but must not become the sole basis for a physical emergency fast-path.

---

## **5.3 Connecting device\_health\_snapshot**

The Decision Matrix must consider device health when using sensor or robot evidence.

device\_health\_snapshot \= OK  
- normal evidence weighting

device\_health\_snapshot \= WARNING  
- lower confidence or conflict policy required

device\_health\_snapshot \= CRITICAL  
- evidence review or fail-safe evaluation

device\_health\_snapshot missing in high-risk path  
- evidence review required

---

## **5.4 Connecting privacy\_lifecycle\_status**

Privacy-related evidence may affect a decision depending on its privacy lifecycle.

PII\_PRESENT  
- access policy required

PII\_MASKED  
- limited use

PII\_CRYPTO\_SHREDDED  
- audit shell exists, operational approval not allowed

LEGAL\_HOLD  
- retention and audit restrictions apply

---

# **6\. Decision Input Model**

The Decision Matrix must evaluate multiple inputs together.

## **6.1 Core Decision Inputs**

Recommended inputs:

event\_type  
event\_category  
current\_state  
inferred\_state  
risk\_level  
severity  
action\_candidate  
target\_entity  
target\_state  
evidence\_bundle  
source\_trust\_level  
evidence\_freshness\_status  
state\_freshness\_status  
conflict\_status  
policy\_decision  
actor\_role  
actor\_clearance  
site\_context  
operational\_context  
time\_context  
spatial\_context  
network\_context  
external\_system\_context  
ai\_trace\_context  
decision\_context\_ref

---

## **6.2 Decision Input Principle**

A decision must not be made by looking at a single event alone.

The following combination must be evaluated together:

Event \+ State \+ Evidence \+ Policy \+ Context \+ ActionCandidate

In high-risk CPS, the following must also be evaluated together:

Time Trust \+ Device Health \+ Network Health \+ Approval Validity \+ TOCTOU State Delta

Example:

safety.gas.critical\_threshold\_exceeded  
\+ ZoneRiskState.CRITICAL  
\+ verified gas sensor evidence  
\+ HIGH\_TIME\_TRUST  
\+ device health OK  
\+ workers present in Zone\_A  
\+ EmergencyPolicy matched  
\+ ACTION\_EMERGENCY\_EVACUATE\_ZONE  
\+ FleetManager heartbeat healthy  
\+ network latency within threshold

This combination is required to route the case to the emergency route.

---

# **7\. DecisionContextDTO**

To prevent DecisionCaseDTO from becoming too heavy, detailed context is separated into DecisionContextDTO or snapshot references.

DecisionCaseDTO contains the core judgment result and reference IDs.  
DecisionContextDTO contains detailed state snapshots, evidence snapshots, network snapshots, and AI trace snapshots used for the decision.

---

## **7.1 DecisionContextDTO Fields**

Recommended fields:

decision\_context\_id  
decision\_case\_id

state\_snapshot\_ref  
evidence\_snapshot\_ref  
network\_snapshot\_ref  
ai\_snapshot\_ref  
policy\_context\_ref  
ontology\_mapping\_snapshot\_ref

state\_summary  
evidence\_summary  
network\_summary  
ai\_trace\_summary  
policy\_summary

created\_at  
trace\_id  
correlation\_id

---

## **7.2 Snapshot Reference Principle**

In high-risk decisions, snapshots must be fixed.

state\_snapshot\_ref  
- World State snapshot at decision time

evidence\_snapshot\_ref  
- Evidence Bundle snapshot at decision time

network\_snapshot\_ref  
- heartbeat / latency snapshot at decision time

ai\_snapshot\_ref  
- AI model, prompt, retrieval, ontology mapping snapshot

This keeps DecisionCaseDTO lightweight, while detailed information needed for audit can still be traced through snapshot refs.

---

# **8\. Decision Output Model**

The Decision Matrix must return a decision route as the judgment result.

## **8.1 Core Decision Outputs**

Recommended outputs:

decision\_route  
approval\_level\_required  
required\_approver\_roles  
required\_evidence\_types  
required\_policy\_refs  
safety\_gate\_required  
human\_approval\_required  
post\_hoc\_audit\_required  
allowed\_action\_types  
blocked\_action\_types  
escalation\_target  
timeout\_policy  
fallback\_route  
fallback\_priority  
decision\_reason  
network\_precondition  
toctou\_precheck\_required  
decision\_trace\_id

---

## **8.2 Decision Route Values**

Recommended values:

AUTO\_ALLOW  
AUTO\_DENY  
NOTIFICATION\_ONLY  
SUPERVISOR\_APPROVAL\_REQUIRED  
SAFETY\_MANAGER\_APPROVAL\_REQUIRED  
WAR\_ROOM\_APPROVAL\_REQUIRED  
EXPERT\_REVIEW\_REQUIRED  
POLICY\_EXCEPTION\_REVIEW  
EMERGENCY\_FAST\_PATH  
FAIL\_SAFE\_REQUIRED  
MANUAL\_OVERRIDE\_REQUIRED  
MAPPING\_REVIEW\_REQUIRED  
EVIDENCE\_REVIEW\_REQUIRED  
RECONCILIATION\_REQUIRED  
NETWORK\_HEALTH\_REVIEW\_REQUIRED  
TOCTOU\_REVALIDATION\_REQUIRED  
AUDIT\_ONLY

---

# **9\. Risk Level / Severity Model**

The Decision Matrix determines approval level based on risk level.

## **9.1 Risk Level**

Recommended values:

INFO  
NOTICE  
WARNING  
HIGH\_RISK  
CRITICAL\_EMERGENCY  
EXCEPTIONAL

---

## **9.2 Meaning of Risk Levels**

INFO  
- General information, automatic handling, or log recording

NOTICE  
- Operator notification required

WARNING  
- Supervisor review may be required

HIGH\_RISK  
- Safety manager or supervisor approval required

CRITICAL\_EMERGENCY  
- Emergency fast-path or fail-safe required

EXCEPTIONAL  
- Expert review, war room, or policy exception review required

---

# **10\. Approval Level Model**

The Approval Matrix must clearly define approval levels.

## **10.1 Approval Level**

Recommended values:

NO\_APPROVAL  
OPERATOR\_ACK  
SUPERVISOR\_APPROVAL  
SAFETY\_MANAGER\_APPROVAL  
WAR\_ROOM\_APPROVAL  
EXPERT\_REVIEW  
POLICY\_OWNER\_APPROVAL  
EMERGENCY\_POLICY\_BYPASS  
POST\_HOC\_AUDIT\_ONLY

---

## **10.2 Meaning of Approval Levels**

NO\_APPROVAL  
- Automatic handling allowed

OPERATOR\_ACK  
- Operator acknowledgment required

SUPERVISOR\_APPROVAL  
- Field supervisor approval required

SAFETY\_MANAGER\_APPROVAL  
- Safety manager approval required

WAR\_ROOM\_APPROVAL  
- Multi-party approval required in complex high-risk situations

EXPERT\_REVIEW  
- Review required from structural, legal, AI, robotics, or equipment experts

POLICY\_OWNER\_APPROVAL  
- Policy exception or policy change required

EMERGENCY\_POLICY\_BYPASS  
- Immediate handling allowed under a predefined emergency policy; post-hoc audit is mandatory

POST\_HOC\_AUDIT\_ONLY  
- Only post-hoc audit is required

---

# **11\. Mapping Between Decision Route and Approval Level**

## **11.1 Basic Mapping**

INFO  
- AUTO\_ALLOW or AUDIT\_ONLY  
- NO\_APPROVAL

NOTICE  
- NOTIFICATION\_ONLY  
- OPERATOR\_ACK

WARNING  
- SUPERVISOR\_APPROVAL\_REQUIRED  
- SUPERVISOR\_APPROVAL

HIGH\_RISK  
- SAFETY\_MANAGER\_APPROVAL\_REQUIRED  
- SAFETY\_MANAGER\_APPROVAL

CRITICAL\_EMERGENCY  
- EMERGENCY\_FAST\_PATH or FAIL\_SAFE\_REQUIRED  
- EMERGENCY\_POLICY\_BYPASS \+ POST\_HOC\_AUDIT\_ONLY

EXCEPTIONAL  
- WAR\_ROOM\_APPROVAL\_REQUIRED or EXPERT\_REVIEW\_REQUIRED  
- WAR\_ROOM\_APPROVAL / EXPERT\_REVIEW

---

## **11.2 Important Exceptions**

A decision must not be made based only on Risk Level.

If any of the following conditions exist, the route may be escalated:

evidence missing  
evidence conflict unresolved  
state stale  
source trust insufficient  
time trust insufficient  
clock sync invalid  
device health degraded  
target invalid  
policy exception detected  
human presence detected  
robot-human shared zone  
external system unavailable  
network latency exceeded  
heartbeat lost  
approval expired  
TOCTOU state delta detected  
ontology mapping uncertain

Example:

risk\_level \= WARNING  
but evidence\_conflict\_unresolved \= true  
- EVIDENCE\_REVIEW\_REQUIRED or SAFETY\_MANAGER\_APPROVAL\_REQUIRED

Example:

risk\_level \= HIGH\_RISK  
but network\_latency\_exceeded \= true  
- NETWORK\_HEALTH\_REVIEW\_REQUIRED or FAIL\_SAFE\_REQUIRED

---

# **12\. Evidence Requirement Connection**

The Decision / Approval Matrix must be directly connected to the Evidence Model.

## **12.1 Evidence Rule**

A high-risk decision must not be approved without an evidence bundle.

An emergency decision requires minimum evidence and mandatory post-hoc audit.

AI-derived evidence cannot be used as the sole basis for approval.

ATTESTED\_AI\_DERIVED evidence can be used only for limited purposes.

Stale evidence cannot be used for high-risk action approval.

Evidence with low time\_trust\_level cannot be used for high-risk decisions.

If clock\_sync\_status is DRIFT\_DETECTED or UNKNOWN, freshness must be revalidated.

If device\_health\_snapshot is WARNING or CRITICAL, conflict policy or evidence review is required.

---

## **12.2 Decision Impact by Evidence Status**

VALID  
- normal judgment possible

STALE  
- high-risk approval not allowed, revalidation required

CONFLICTED  
- conflict resolution required

UNVERIFIED  
- approval not allowed, evidence review required

AI\_DERIVED\_ONLY  
- explanation allowed, approval not allowed

ATTESTED\_AI\_DERIVED  
- limited use allowed

CRYPTO\_SHREDDED  
- audit shell exists, but not usable for operational approval

---

## **12.3 Decision Impact by Time Trust Status**

HIGH\_TIME\_TRUST  
- normal decision allowed

MEDIUM\_TIME\_TRUST  
- allowed for non-critical decision, high-risk requires policy

LOW\_TIME\_TRUST  
- revalidation required

UNTRUSTED\_TIME  
- approval blocked

UNKNOWN\_TIME\_TRUST  
- evidence review required

---

## **12.4 Decision Impact by Device Health Status**

OK  
- normal evidence use

WARNING  
- lower confidence, conflict policy required

CRITICAL  
- evidence review or fail-safe evaluation

UNKNOWN  
- high-risk approval blocked unless alternative verified evidence exists

---

# **13\. State Freshness Connection**

The Decision / Approval Matrix must be directly connected to the State Model.

## **13.1 State Rule**

A high-risk action must not be approved based on stale state.

pending\_state must not be treated as confirmed\_state.

If inferred\_state and runtime state are inconsistent within the temporal grace period, the system must not immediately treat it as a conflict.

If reconciliation failure is safety-critical, it must be routed to the fail-safe path.

---

## **13.2 Decision Impact by State Status**

CONFIRMED  
- normal judgment possible

PENDING  
- execution may be held even if approval is possible

STALE  
- revalidation required

UNKNOWN  
- manual review or fail-safe evaluation

CONFLICT  
- reconciliation required

FAIL\_SAFE\_TRIGGERED  
- emergency route

---

# **14\. TOCTOU Prevention Rule**

TOCTOU means Time-of-Check to Time-of-Use.

It is dangerous when the state at approval time and the state at actual ExecutionRequest creation time differ.

Example:

Approval time:  
Zone\_A has no worker.

Execution time:  
Worker\_17 entered Zone\_A.

In this case, the approved action must not be executed as-is.

---

## **14.1 TOCTOU Precheck**

SafetyGatePrecheck must compare the following:

state\_snapshot\_ref\_at\_decision  
state\_snapshot\_ref\_at\_approval  
state\_snapshot\_ref\_at\_execution  
evidence\_snapshot\_ref\_at\_decision  
evidence\_snapshot\_ref\_at\_execution  
target\_state\_at\_approval  
target\_state\_at\_execution

---

## **14.2 TOCTOU Decision Result**

NO\_DELTA  
- execution may proceed

LOW\_RISK\_DELTA  
- proceed with audit

HIGH\_RISK\_DELTA  
- TOCTOU\_REVALIDATION\_REQUIRED

SAFETY\_CRITICAL\_DELTA  
- FAIL\_SAFE\_REQUIRED or MANUAL\_OVERRIDE\_REQUIRED

---

## **14.3 TOCTOU Principle**

Approval does not freeze the world.  
Safety Gate must re-check the world before execution.

Approval does not freeze the world.  
Safety Gate must re-check the current world state immediately before execution.

---

# **15\. Network Latency / Heartbeat Rule**

In high-risk CPS, even an approved action must not be executed if the network condition is poor.

Robots, PLCs, SCADA, FleetManager, and field access control systems must validate heartbeat and latency.

---

## **15.1 Network Health Check Targets**

external\_adapter  
fleet\_manager  
robot\_middleware  
PLC / SCADA gateway  
access\_control\_system  
edge\_gateway  
message\_broker

---

## **15.2 Validation Items**

heartbeat\_status  
last\_heartbeat\_at  
network\_latency\_ms  
max\_allowed\_latency\_ms  
packet\_loss\_rate  
adapter\_availability  
external\_system\_availability  
command\_ack\_timeout

---

## **15.3 Decision Impact by Network Status**

HEALTHY  
- normal execution path

DEGRADED  
- approval may remain valid, execution requires caution or recheck

LATENCY\_EXCEEDED  
- NETWORK\_HEALTH\_REVIEW\_REQUIRED or FAIL\_SAFE\_REQUIRED

HEARTBEAT\_LOST  
- execution blocked

ADAPTER\_UNAVAILABLE  
- execution blocked or fallback route

COMMAND\_ACK\_TIMEOUT  
- recovery or fail-safe evaluation

---

## **15.4 Core Principle**

ApprovedAction is not enough.  
External path must be alive.

ApprovedAction alone is not enough.  
The external execution path must be alive.

---

# **16\. Conflict Handling Rule**

If evidence conflict or state conflict exists, the decision route must change.

## **16.1 Conflict Decision Rule**

NO\_CONFLICT  
- normal decision route

CONFLICT\_DETECTED  
- apply conflict policy

CONFLICT\_RESOLVED  
- judgment possible based on selected evidence

CONFLICT\_UNDER\_REVIEW  
- approval hold

CONFLICT\_ESCALATED  
- safety manager or expert review

FAIL\_SAFE\_ON\_CONFLICT  
- emergency fast-path or fail-safe required

---

## **16.2 Safety-Critical Conflict Rule**

Fail-safe evaluation is performed when the following condition is met:

risk\_level \>= HIGH\_RISK  
AND conflict\_status \!= CONFLICT\_RESOLVED

Or:

risk\_level \= CRITICAL\_EMERGENCY  
AND evidence\_conflict\_detected \= true

Result:

decision\_route \= FAIL\_SAFE\_REQUIRED  
approval\_level\_required \= EMERGENCY\_POLICY\_BYPASS  
post\_hoc\_audit\_required \= true

---

# **17\. Human-in-the-loop Rule**

The Decision / Approval Matrix must clearly define where human intervention is required.

## **17.1 Cases That Require Human Approval**

Human approval is required in the following cases:

high-risk action  
work stop  
zone lock  
robot mission disable  
permit override  
policy exception  
unresolved evidence conflict  
manual override request  
state reconciliation failure  
mapping uncertainty in high-risk path  
TOCTOU high-risk delta  
network degraded high-risk path  
device health degraded high-risk path  
time trust insufficient high-risk path

---

## **17.2 Cases That May Not Require Human Approval**

Automatic handling may be possible in the following cases:

low-risk notification  
dashboard update  
audit-only logging  
normal telemetry state update  
routine state transition  
pre-approved emergency fast-path

However, a pre-approved emergency fast-path requires post-hoc audit.

---

# **18\. Emergency Fast-Path Rule**

Emergency Fast-Path is used in critical emergency situations.

## **18.1 Conditions**

The following conditions must be satisfied:

risk\_level \= CRITICAL\_EMERGENCY  
emergency\_policy\_matched \= true  
minimum\_evidence\_bundle\_present \= true  
target\_entity\_valid \= true  
network\_minimum\_viable \= true  
external\_adapter\_available \= true  
safety\_gate\_required \= true  
post\_hoc\_audit\_required \= true

---

## **18.2 Definition of Minimum Evidence Bundle**

For `minimum_evidence_bundle_present = true` in the Emergency Fast-Path, the following conditions must be satisfied:

at least one VERIFIED\_DEVICE or TRUSTED\_SYSTEM operational evidence exists  
AND evidence freshness is valid or emergency-acceptable  
AND time\_trust\_level \>= MEDIUM\_TIME\_TRUST  
AND target entity is bound  
AND emergency policy is matched

ATTESTED\_AI\_DERIVED evidence may be used as supporting evidence.

Example:

Permit condition extracted from document  
- ATTESTED\_AI\_DERIVED  
- can support emergency context  
- cannot be the sole emergency trigger

That is, physical emergency fast-path execution must not be triggered by AI or document-extracted evidence alone.

---

## **18.3 Prohibitions**

Emergency fast-path must not be executed based only on LLM output.

Emergency fast-path must not be executed based only on AI\_DERIVED\_ONLY evidence.

Physical emergency fast-path must not be executed based only on ATTESTED\_AI\_DERIVED evidence.

Emergency fast-path must not be executed based only on unverified sources.

Emergency fast-path must not be executed if the target is unclear.

An emergency execution request must not be created if the external adapter is unavailable.

An execution request must not be sent to an external system whose heartbeat is lost.

An execution request must not be created if network latency exceeds the allowed limit. However, if a local fail-safe action is predefined, the system may switch to that route.

---

## **18.4 Emergency Fast-Path Flow**

Critical Event  
- Minimum Evidence Bundle  
- Emergency Policy Match  
- Network / Heartbeat Check  
- Decision Route: EMERGENCY\_FAST\_PATH  
- EmergencyApprovedAction  
- EmergencyRuntimeValidationInput  
- EmergencyRuntimeValidationResult  
- Emergency Safety Gate  
- EmergencySafetyGatePass or EmergencySafetyGateBlock  
- EmergencyExecutionRequest only if EmergencySafetyGatePass exists  
- External Control System  
- Feedback  
- Post-hoc Audit

EmergencyApprovedAction grants emergency authority. EmergencySafetyGatePass grants short-lived execution readiness. EmergencySafetyGateBlock prevents EmergencyExecutionRequest creation. EmergencyExecutionRequest MUST NOT be created unless an EmergencySafetyGatePass has been issued from a valid EmergencyRuntimeValidationResult.

---

# **19\. Policy Engine / PDP / PEP Integration**

The Decision / Approval Matrix is connected to the policy engine.

## **19.1 Components**

PAP \= Policy Administration Point  
PDP \= Policy Decision Point  
PEP \= Policy Enforcement Point  
PIP \= Policy Information Point

---

## **19.2 Roles Inside the Platform**

PAP  
- manages policy registry, approval matrix, safety policy, and emergency policy

PDP  
- OPA / Rego / policy evaluator returns allow / deny / require\_approval decisions

PEP  
- enforces policy at the API Gateway, Safety Gate, and External Adapter

PIP  
- World State, Ontology, Evidence Store, Role DB, Approval DB

---

## **19.3 Relationship Between Decision Matrix and PDP**

The Decision Matrix determines the workflow route.

The PDP returns a specific policy decision.

Example:

Decision Matrix:  
ZoneRiskState.CRITICAL → EMERGENCY\_FAST\_PATH

PDP:  
EmergencyPolicy\_001 allows ACTION\_EMERGENCY\_EVACUATE\_ZONE

Both are necessary.

---

# **20\. PolicyEngineAdapter Rule**

For DecisionRouter to function correctly, the PolicyEngineAdapter interface must be defined early.

Even if the PDP is not fully implemented yet, a dummy PDP response must be defined first so integration testing can be performed.

---

## **20.1 Responsibilities of PolicyEngineAdapter**

build policy context  
send request to PDP  
receive policy decision  
normalize allow / deny / require\_approval  
attach policy decision refs  
support dummy PDP for testing

---

## **20.2 Example PDP Call Context**

PolicyEngineAdapter sends the following context to the PDP:

policy\_context \= {  
  "actor": {  
    "role": "Supervisor",  
    "clearance": "SAFETY\_LEVEL\_2"  
  },  
  "action": {  
    "action\_type": "ACTION\_EVACUATE\_ZONE",  
    "target\_entity": "Zone\_A"  
  },  
  "risk": {  
    "risk\_level": "CRITICAL\_EMERGENCY",  
    "severity": "HIGH"  
  },  
  "state": {  
    "zone\_risk\_state": "CRITICAL",  
    "worker\_presence": true,  
    "state\_freshness\_status": "VALID"  
  },  
  "evidence": {  
    "source\_trust\_level": "VERIFIED\_DEVICE",  
    "time\_trust\_level": "HIGH\_TIME\_TRUST",  
    "clock\_sync\_status": "SYNCED",  
    "device\_health\_status": "OK",  
    "trust\_upgrade\_status": "NO\_UPGRADE"  
  },  
  "network": {  
    "heartbeat\_status": "HEALTHY",  
    "network\_latency\_ms": 45  
  },  
  "context": {  
    "site\_id": "Site\_001",  
    "zone\_id": "Zone\_A",  
    "trace\_id": "trace-123"  
  }  
}

---

## **20.3 Basic Structure of PolicyDecisionResponse**

policy\_decision\_id  
policy\_engine  
policy\_engine\_version  
input\_context\_hash  
decision\_result  
required\_approval\_level  
matched\_policy\_refs  
denied\_policy\_refs  
decision\_reason  
created\_at  
trace\_id  
correlation\_id

---

## **20.4 decision\_result Values**

ALLOW  
DENY  
REQUIRE\_APPROVAL  
REQUIRE\_EVIDENCE  
REQUIRE\_REVALIDATION  
REQUIRE\_FAIL\_SAFE

---

## **20.5 Implementation Principle**

DecisionRouter must not hard-code policy logic.  
DecisionRouter calls PolicyEngineAdapter.  
PolicyEngineAdapter may use OPA / Rego / local rules / dummy PDP.

DecisionRouter must not hard-code policy logic.  
DecisionRouter calls PolicyEngineAdapter.

---

# **21\. Approval Timeout and Escalation Rule**

Approval cannot wait indefinitely.

## **21.1 Approval Timeout**

ApprovalRequest must have a timeout\_policy.

Recommended timeout examples:

OPERATOR\_ACK → 30 seconds  
SUPERVISOR\_APPROVAL → 2 minutes  
SAFETY\_MANAGER\_APPROVAL → 5 minutes  
WAR\_ROOM\_APPROVAL → 15 minutes  
EXPERT\_REVIEW → policy-defined

---

## **21.2 Cascading Timeout Rule**

When approval is escalated, the timeout must not simply restart as if nothing happened.

The higher-level approver must receive the time already delayed in the previous step.

ApprovalRequestDTO must preserve the following information:

previous\_approval\_level  
previous\_timeout\_at  
previous\_approver\_id  
previous\_approver\_response\_time  
elapsed\_time\_before\_escalation  
total\_elapsed\_time  
escalation\_reason  
escalation\_history  
original\_requested\_at  
current\_expires\_at

---

## **21.3 Timeout Calculation Principle**

current\_expires\_at \=  
  escalation\_started\_at \+ timeout\_for\_new\_level

However, the following must also be preserved in audit:

original\_requested\_at  
total\_elapsed\_time  
elapsed\_time\_before\_escalation  
previous\_approver\_response\_time  
escalation\_history

That is, the timeout for the higher approval stage is recalculated dynamically, but the full delay history must not disappear.

---

## **21.4 Handling After Timeout**

NO\_RESPONSE  
- escalate

REJECTED  
- deny or recovery route

TIMEOUT\_HIGH\_RISK  
- escalate to safety manager

TIMEOUT\_CRITICAL  
- emergency policy evaluation or fail-safe evaluation

TIMEOUT\_EXCEPTIONAL  
- war room escalation

---

# **22\. Idempotency Rule**

Execution requests to physical systems must not be executed more than once.

Even if network retries, timeouts, client retries, or message broker redelivery occur, the same command must not be executed multiple times.

Therefore, ApprovalDecisionDTO and ExecutionRequestDTO must have an idempotency\_key.

---

## **22.1 idempotency\_key Generation Principle**

Recommended method:

idempotency\_key \= hash(  
  approval\_decision\_id,  
  decision\_case\_id,  
  approved\_action\_type,  
  target\_entity\_refs,  
  trace\_id,  
  lifecycle\_version  
)

---

## **22.2 Scope of Application**

ApprovalDecisionDTO  
ApprovedActionDTO  
ExecutionRequestDTO  
EmergencyExecutionRequestDTO  
ExternalControlRequestDTO

---

## **22.3 Core Principle**

Same approval decision must not create duplicate physical execution.  
Retry must be safe.

The same approval decision must not create duplicate physical execution.  
Retries must be safe.

---

# **23\. AI Governance Trace Rule**

If AI generates an ActionCandidate, RiskInterpretation, EvidenceSummary, or MappingProposal, DecisionCaseDTO or DecisionContextDTO must record the AI trace.

---

## **23.1 AI Trace Fields**

Recommended fields:

ai\_model\_name  
ai\_model\_version  
ai\_model\_version\_hash  
prompt\_hash  
retrieval\_snapshot\_id  
ontology\_mapping\_snapshot\_id  
evidence\_snapshot\_id  
temperature  
ai\_output\_ref  
trust\_upgrade\_status  
attestation\_type

---

## **23.2 AI Trace Principle**

AI output may influence candidate generation.  
AI trace must be auditable.  
AI output must not approve action.

AI output may influence candidate generation.  
AI trace must be auditable.  
AI output must not approve action.

---

# **24\. Safety Gate Requirement Reference**

The Decision / Approval Matrix does not perform final execution-time validation.

It identifies risk, priority, approval requirements, and references the Runtime Validation and Safety Gate requirements that must be satisfied later.

TOCTOU, network health, idempotency, freshness, approval validity, policy revalidation, and evidence validity result generation belongs to `08_runtime_validation/`.

The Safety Gate consumes RuntimeValidationResult and issues SafetyGatePass or SafetyGateBlock.

## **24.1 Required Validations**

Referenced for every ApprovedAction; performed by Runtime Validation before Safety Gate.

approval\_valid\_until\_check  
idempotency\_key\_check  
target\_validity\_check  
policy\_decision\_still\_valid\_check  
conflict\_status\_check

---

## **24.2 High-Risk Conditional Validations**

Referenced when risk\_level is HIGH\_RISK or higher; performed by Runtime Validation before Safety Gate.

evidence\_freshness\_check  
state\_freshness\_check  
TOCTOU\_state\_delta\_check  
time\_trust\_check  
device\_health\_check  
source\_trust\_check

---

## **24.3 External System Conditional Validations**

Referenced when external systems, robots, PLCs, SCADA, or access control systems are involved; performed by Runtime Validation or external integration health checks before Safety Gate.

network\_latency\_check  
heartbeat\_check  
external\_adapter\_availability\_check  
command\_ack\_timeout\_check

---

## **24.4 AI-Derived Conditional Validations**

Referenced when AI-derived or attested AI-derived evidence influenced the action candidate; evidence validity result generation belongs to Runtime Validation and Evidence validation.

ai\_trace\_check  
trust\_upgrade\_status\_check  
attestation\_ref\_check  
evidence\_grounding\_check

---

## **24.5 High-Frequency Event Handling Principle**

If every Runtime Validation requirement is applied directly to high-frequency sensor telemetry, it can create a bottleneck.

Therefore, high-frequency telemetry must first pass through the stream layer and evidence promotion rules.

High-frequency telemetry  
- stream aggregation  
- threshold / anomaly / state change detection  
- semantic event promotion  
- decision evaluation

The Decision / Approval Matrix operates on semantic events or promoted evidence.

---

## **24.6 Handling on Failure**

approval expired  
- deny execution, request re-approval

TOCTOU high-risk delta  
- TOCTOU\_REVALIDATION\_REQUIRED

network latency exceeded  
- NETWORK\_HEALTH\_REVIEW\_REQUIRED or FAIL\_SAFE\_REQUIRED

heartbeat lost  
- block execution

adapter unavailable  
- fallback route or fail-safe evaluation

idempotency collision  
- return previous result or block duplicate execution

time trust insufficient  
- EVIDENCE\_REVIEW\_REQUIRED

device health critical  
- EVIDENCE\_REVIEW\_REQUIRED or FAIL\_SAFE\_REQUIRED

---

# **25\. DecisionTrace Rule**

The entire flow from DecisionCase → ApprovalRequest → ApprovalDecision → ApprovedAction → RuntimeValidationInput → RuntimeValidationResult → Safety Gate → SafetyGatePass or SafetyGateBlock → ExecutionRequest → Feedback → AuditRecord must be connected with a single decision\_trace\_id.

---

## **25.1 Objects That Use decision\_trace\_id**

DecisionCaseDTO  
DecisionContextDTO  
ApprovalRequestDTO  
ApprovalDecisionDTO  
ApprovedActionDTO  
ExecutionRequestDTO  
ExternalControlRequestDTO  
FeedbackEventDTO  
AuditRecordDTO

---

## **25.2 Decision Trace Principle**

One decision path must be traceable end-to-end.

One decision path must be traceable end-to-end.

---

# **26\. Fallback Route Priority Rule**

When multiple fallback routes exist, priority is required.

## **26.1 Recommended Priority**

1\. FAIL\_SAFE\_REQUIRED  
2\. EMERGENCY\_FAST\_PATH  
3\. MANUAL\_OVERRIDE\_REQUIRED  
4\. SAFETY\_MANAGER\_APPROVAL\_REQUIRED  
5\. EVIDENCE\_REVIEW\_REQUIRED  
6\. RECONCILIATION\_REQUIRED  
7\. NETWORK\_HEALTH\_REVIEW\_REQUIRED  
8\. NOTIFICATION\_ONLY  
9\. AUDIT\_ONLY

---

## **26.2 Core Principle**

In safety-critical situations, safe stop or fail-safe takes priority.

Operational convenience must not take priority over safety.

---

# **27\. DecisionCaseDTO**

Decision results are managed through DecisionCaseDTO.

To avoid making DecisionCaseDTO excessively heavy, it should not directly contain every detailed context field. Instead, it should be built around snapshot references.

---

## **27.1 DecisionCaseDTO Fields**

Recommended fields:

decision\_case\_id  
decision\_trace\_id  
decision\_type  
decision\_route  
risk\_level  
severity

decision\_context\_ref

trigger\_event\_refs  
target\_entity\_refs  
action\_candidate\_refs  
evidence\_bundle\_refs  
policy\_decision\_refs

source\_trust\_summary  
evidence\_freshness\_summary  
state\_freshness\_summary  
conflict\_status  
reconciliation\_status

network\_health\_summary  
heartbeat\_status

approval\_level\_required  
required\_approver\_roles  
required\_clearance  
human\_approval\_required  
safety\_gate\_required  
toctou\_precheck\_required  
post\_hoc\_audit\_required

fallback\_route  
fallback\_priority

decision\_reason  
decision\_explanation  
decision\_trace

created\_at  
created\_by  
trace\_id  
correlation\_id

---

# **28\. ApprovalRequestDTO**

Approval requests are managed through ApprovalRequestDTO.

## **28.1 ApprovalRequestDTO Fields**

Recommended fields:

approval\_request\_id  
decision\_trace\_id  
decision\_case\_id  
requested\_action\_type  
target\_entity\_refs  
approval\_level  
required\_roles  
required\_clearance

approver\_candidates  
assigned\_approver  
approval\_status  
approval\_result  
approval\_reason

evidence\_bundle\_refs  
policy\_refs  
risk\_level  
severity

requested\_at  
expires\_at  
approved\_at  
rejected\_at  
escalated\_at

original\_requested\_at  
previous\_approval\_level  
previous\_timeout\_at  
previous\_approver\_id  
previous\_approver\_response\_time  
elapsed\_time\_before\_escalation  
total\_elapsed\_time  
escalation\_reason  
escalation\_history

timeout\_policy  
escalation\_policy  
fallback\_route

created\_by  
trace\_id  
correlation\_id

---

# **29\. ApprovalDecisionDTO**

Approval results are managed through ApprovalDecisionDTO.

## **29.1 ApprovalDecisionDTO Fields**

Recommended fields:

approval\_decision\_id  
decision\_trace\_id  
approval\_request\_id  
decision\_case\_id

idempotency\_key

approver\_id  
approver\_role  
approval\_result  
approval\_reason

approved\_action\_type  
denied\_action\_type  
conditions  
constraints

state\_snapshot\_ref\_at\_approval  
evidence\_snapshot\_ref\_at\_approval  
approval\_context\_hash

requires\_safety\_gate  
requires\_toctou\_precheck  
requires\_network\_health\_check  
requires\_post\_hoc\_audit  
valid\_until

created\_at  
signature  
trace\_id  
correlation\_id

---

# **30\. DecisionMatrixSpecDTO**

Decision Matrix is managed through DecisionMatrixSpecDTO.

DecisionMatrixSpecDTO belongs to the Platform Core Registry or the operational registry of the Policy Module.

From the perspective of the Ontology Module Boundary, DecisionMatrixSpecDTO belongs to the Registry, not to the Ontology itself.

---

## **30.1 DecisionMatrixSpecDTO Fields**

Recommended fields:

matrix\_id  
matrix\_name  
domain\_module  
registry\_owner\_module  
applicable\_event\_types  
applicable\_state\_models  
applicable\_action\_types  
applicable\_risk\_levels

input\_conditions  
required\_evidence\_types  
minimum\_source\_trust\_level  
minimum\_time\_trust\_level  
device\_health\_requirement  
state\_freshness\_requirement  
network\_health\_requirement  
toctou\_policy\_ref  
conflict\_policy\_ref  
policy\_refs

decision\_route  
approval\_level\_required  
required\_roles  
safety\_gate\_required  
network\_health\_check\_required  
toctou\_precheck\_required  
post\_hoc\_audit\_required

fallback\_route  
fallback\_priority  
escalation\_route  
timeout\_policy

owner  
version  
status  
valid\_from  
valid\_until  
deprecated\_at  
replacement\_matrix  
change\_reason

---

# **31\. ApprovalMatrixSpecDTO**

Approval Matrix is managed through ApprovalMatrixSpecDTO.

ApprovalMatrixSpecDTO belongs to the Policy Module or the Platform Governance Registry.

Ontology defines the meaning of Approval.  
ApprovalMatrixSpecDTO defines the actual operational approval rules.

---

## **31.1 ApprovalMatrixSpecDTO Fields**

Recommended fields:

approval\_matrix\_id  
matrix\_name  
domain\_module  
registry\_owner\_module  
action\_type  
risk\_level  
target\_entity\_type

approval\_level  
required\_roles  
required\_clearance  
minimum\_approver\_count  
multi\_party\_required

emergency\_bypass\_allowed  
post\_hoc\_audit\_required  
approval\_timeout\_policy  
cascading\_timeout\_policy  
escalation\_policy

allowed\_approval\_results  
denial\_fallback\_route

owner  
version  
status  
valid\_from  
valid\_until  
deprecated\_at  
replacement\_matrix  
change\_reason

---

# **32\. Registry Operating Policy**

The Decision / Approval Matrix is subject to governance.

## **32.1 Registry Status**

Recommended values:

DRAFT  
ACTIVE  
DEPRECATED  
RETIRED  
BLOCKED

---

## **32.2 Versioning**

Backward-compatible changes:

Add a new low-risk route  
Add optional metadata  
Enhance approval timeout  
Enhance description  
Enhance audit requirement  
Add network health requirement  
Add AI trace metadata  
Add snapshot\_ref  
Add decision\_trace\_id

Breaking changes:

Relax approval level  
Relax emergency bypass conditions  
Remove required evidence  
Remove required role  
Remove Safety Gate requirement  
Remove network health check  
Remove TOCTOU precheck  
Relax minimum time trust level  
Remove device health requirement  
Change high-risk action route  
Remove fallback route

As a rule, breaking changes must be separated into a new matrix version or a new matrix.

---

## **32.3 Approval Process**

Changes to the Decision / Approval Matrix require approval from the following:

Policy Owner  
Safety Owner  
Domain Owner  
Ontology Steward  
Platform Architect

Emergency-related matrices require additional approval from the following:

Audit Owner  
Legal / Compliance Owner  
External System Owner

---

# **33\. Core Scenarios**

## **33.1 Scenario 1: Gas Critical - Emergency Evacuation**

Situation:

The gas critical threshold was exceeded in Zone\_A.

Input:

event\_type \= safety.gas.critical\_threshold\_exceeded  
state \= ZoneRiskState.CRITICAL  
evidence\_bundle \= valid gas sensor \+ worker location \+ policy  
risk\_level \= CRITICAL\_EMERGENCY  
action\_candidate \= ACTION\_EMERGENCY\_EVACUATE\_ZONE  
time\_trust\_level \= HIGH\_TIME\_TRUST  
clock\_sync\_status \= SYNCED  
device\_health\_snapshot \= OK  
network\_latency\_ms \= within threshold  
heartbeat\_status \= healthy

Decision:

decision\_route \= EMERGENCY\_FAST\_PATH  
approval\_level\_required \= EMERGENCY\_POLICY\_BYPASS  
safety\_gate\_required \= true  
network\_health\_check\_required \= true  
post\_hoc\_audit\_required \= true

Result:

EmergencyApprovedAction  
- EmergencyRuntimeValidationInput  
- EmergencyRuntimeValidationResult  
- Emergency Safety Gate  
- EmergencySafetyGatePass or EmergencySafetyGateBlock  
- EmergencyExecutionRequest only if EmergencySafetyGatePass exists  
- External Control System  
- Feedback  
- Post-hoc Audit

---

## **33.2 Scenario 2: Robot Mission Blocked - Supervisor Approval**

Situation:

Mission\_991 of Robot\_07 is in a blocked state.

Input:

event\_type \= robot.mission.blocked  
state \= MissionStatus.BLOCKED  
risk\_level \= WARNING  
action\_candidate \= ACTION\_DISABLE\_ROBOT\_MISSION  
evidence \= robot telemetry \+ fleet manager state

Decision:

decision\_route \= SUPERVISOR\_APPROVAL\_REQUIRED  
approval\_level\_required \= SUPERVISOR\_APPROVAL  
safety\_gate\_required \= true

Result:

ApprovalRequest  
- Supervisor Approval  
- ApprovedAction  
- Safety Gate  
- ExecutionRequest to FleetManager

---

## **33.3 Scenario 3: Stale Worker Location - Approval Hold**

Situation:

WorkerLocationEvidence is stale.

Input:

action\_candidate \= ACTION\_LOCK\_ZONE  
worker\_location\_state \= STALE  
risk\_level \= HIGH\_RISK

Decision:

decision\_route \= EVIDENCE\_REVIEW\_REQUIRED  
approval\_level\_required \= SAFETY\_MANAGER\_APPROVAL  
execution\_allowed \= false

Result:

Request fresh worker location evidence  
- hold approval  
- re-evaluate

---

## **33.4 Scenario 4: Evidence Conflict - Fail-Safe**

Situation:

Two gas sensors conflict.

Input:

GasSensor\_A \= 87 ppm  
GasSensor\_B \= 0 ppm  
conflict\_status \= CONFLICT\_DETECTED  
risk\_level \= CRITICAL\_EMERGENCY

Decision:

decision\_route \= FAIL\_SAFE\_REQUIRED  
approval\_level\_required \= EMERGENCY\_POLICY\_BYPASS  
post\_hoc\_audit\_required \= true

Result:

Fail-safe evaluation  
- Emergency action candidate  
- EmergencyApprovedAction  
- EmergencyRuntimeValidationInput  
- EmergencyRuntimeValidationResult  
- Emergency Safety Gate  
- EmergencySafetyGatePass or EmergencySafetyGateBlock  
- EmergencyExecutionRequest only if EmergencySafetyGatePass exists

---

## **33.5 Scenario 5: LLM Proposed Action - Evidence Check**

Situation:

The LLM proposed ACTION\_STOP\_WORK.

Input:

action\_candidate\_source \= AI\_DERIVED  
trust\_upgrade\_status \= NO\_UPGRADE  
evidence\_bundle \= missing  
risk\_level \= HIGH\_RISK

Decision:

decision\_route \= EVIDENCE\_REVIEW\_REQUIRED  
approval\_level\_required \= SAFETY\_MANAGER\_APPROVAL  
execution\_allowed \= false

Result:

LLM proposal stored as ActionCandidate  
- request evidence grounding  
- no approval until evidence bundle exists

---

## **33.6 Scenario 6: Approval Valid But TOCTOU State Changed**

Situation:

The supervisor approved ACTION\_LOCK\_ZONE.  
However, after approval, Worker\_17 entered Zone\_A.

Input:

approval\_status \= APPROVED  
state\_snapshot\_ref\_at\_approval \= no worker in Zone\_A  
state\_snapshot\_ref\_at\_execution \= Worker\_17 in Zone\_A  
risk\_level \= HIGH\_RISK

SafetyGatePrecheck:

TOCTOU\_state\_delta\_check \= HIGH\_RISK\_DELTA

Decision:

decision\_route \= TOCTOU\_REVALIDATION\_REQUIRED  
execution\_allowed \= false

Result:

Hold ExecutionRequest  
- request fresh approval or emergency evaluation

---

## **33.7 Scenario 7: Network Latency Exceeded**

Situation:

Robot mission disable was approved, but the FleetManager heartbeat was lost.

Input:

approval\_status \= APPROVED  
heartbeat\_status \= HEARTBEAT\_LOST  
network\_latency\_ms \= exceeded  
action\_candidate \= ACTION\_DISABLE\_ROBOT\_MISSION

SafetyGatePrecheck:

network\_health\_check \= failed

Decision:

decision\_route \= NETWORK\_HEALTH\_REVIEW\_REQUIRED  
execution\_allowed \= false  
fallback\_route \= FAIL\_SAFE\_REQUIRED if safety-critical

Result:

Do not send ExecutionRequest  
- escalate or use local fail-safe policy

---

# **34\. MVP Decision / Approval Matrix Set**

For the MVP, reduce the scope and implement the following three first:

Safety Decision Matrix  
Evidence Conflict Matrix  
Emergency Fast-Path Matrix

The reasons for implementing these three first are as follows:

Safety is the highest-value domain.  
Evidence Conflict is the main source of wrong decisions.  
Emergency Fast-Path defines the physical safety boundary.

---

## **34.1 MVP Phase 1**

Gas critical threshold decision matrix  
Evidence conflict decision matrix  
Emergency fast-path matrix  
Post-hoc audit matrix

---

## **34.2 MVP Phase 2**

Robot mission blocked decision matrix  
Robot mission disable approval matrix  
Stale evidence decision matrix  
TOCTOU revalidation matrix  
Network health review matrix

---

## **34.3 MVP Phase 3**

Permit expired decision matrix  
Inspection failed decision matrix  
Task hold approval matrix  
Manual override matrix  
Policy exception approval matrix

---

# **35\. Recommended File Structure**

## **35.1 Decision / Approval Registry**

decision\_registry/  
  \_\_init\_\_.py  
  decision\_case.py  
  decision\_context.py  
  decision\_matrix\_spec.py  
  approval\_matrix\_spec.py  
  approval\_request.py  
  approval\_decision.py  
  decision\_trace.py  
  risk\_level.py  
  decision\_route.py  
  approval\_level.py  
  fallback\_route.py  
  escalation\_policy.py  
  timeout\_policy.py  
  idempotency\_policy.py  
  toctou\_policy.py  
  network\_health\_policy.py

---

## **35.2 Policy Integration**

decision\_registry/policy/  
  policy\_engine\_adapter.py  
  dummy\_pdp.py  
  opa\_pdp\_client.py  
  policy\_decision.py  
  policy\_context\_builder.py  
  approval\_policy\_adapter.py

---

## **35.3 Matrix Catalog**

decision\_registry/catalog/  
  safety\_decision\_matrices.py  
  evidence\_conflict\_matrices.py  
  emergency\_decision\_matrices.py  
  robot\_decision\_matrices.py  
  construction\_decision\_matrices.py  
  approval\_matrices.py

---

## **35.4 Validation**

decision\_registry/validation/  
  evidence\_requirement\_validator.py  
  time\_trust\_validator.py  
  device\_health\_validator.py  
  state\_freshness\_validator.py  
  conflict\_status\_validator.py  
  approval\_level\_validator.py  
  emergency\_fast\_path\_validator.py  
  safety\_gate\_precheck.py  
  toctou\_validator.py  
  network\_health\_validator.py  
  idempotency\_validator.py  
  fallback\_route\_validator.py

---

# **36\. Recommended Implementation Order**

The MVP implementation order should be as follows.

DecisionRoute enum  
ApprovalLevel enum  
RiskLevel enum  
ApprovalStatus enum  
PolicyDecisionResult enum  
DecisionTraceDTO  
DecisionContextDTO  
DecisionCaseDTO  
ApprovalRequestDTO  
ApprovalDecisionDTO  
DecisionMatrixSpecDTO  
ApprovalMatrixSpecDTO  
PolicyEngineAdapter interface  
DummyPDP  
PolicyDecisionAdapter  
EvidenceRequirementValidator  
TimeTrustValidator  
DeviceHealthValidator  
StateFreshnessValidator  
ConflictStatusValidator  
NetworkHealthValidator  
TOCTOUValidator  
IdempotencyValidator  
FallbackRouteValidator  
DecisionRouter  
ApprovalRouter  
EmergencyFastPathValidator  
SafetyGatePrecheck  
MVP Safety Decision Matrix  
MVP Evidence Conflict Matrix  
MVP Emergency Fast-Path Matrix  
Audit integration  
Post-hoc Audit integration

PolicyEngineAdapter and DummyPDP should be defined before DecisionRouter.

Reason:

DecisionRouter integration test requires predictable PDP response.

---

# **37\. Final Principle**

The Decision / Approval Matrix is the judgment and approval language of the platform.

Event tells what happened.  
State tells the current condition.  
Evidence tells the basis of judgment.  
ActionCandidate tells what is proposed.  
Decision tells the judgment route.  
Approval tells the authority grant.  
Safety Gate tells execution eligibility validation.  
ExecutionRequest tells the execution request to an external system.

LLM can propose ActionCandidate.  
LLM cannot independently confirm Decision.  
LLM cannot perform Approval.  
LLM cannot create ExecutionRequest.

High-risk actions must not be approved without an evidence bundle.  
High-risk actions must not be approved based on stale state.  
High-risk actions must not be approved based on low time trust evidence.  
Evidence with degraded device health must escalate the decision route.  
If conflict is unresolved, the route must be escalated.  
Emergency fast-path requires predefined policy and minimum verified operational evidence.  
ATTESTED\_AI\_DERIVED evidence may support emergency context, but cannot become the sole emergency trigger.  
Emergency bypass must always require post-hoc audit.  
Even if Approval exists, ExecutionRequest cannot be created unless Runtime Validation passes and the Safety Gate issues a valid SafetyGatePass.  
Even if Approval is valid, TOCTOU revalidation is required if the world state changes immediately before execution.  
Even if the external adapter is alive, execution must not proceed if heartbeat or network latency exceeds the threshold.  
Physical execution requests must prevent duplicate execution using idempotency\_key.  
AI-derived decision support must leave auditable model version, prompt, retrieval snapshot, and ontology mapping snapshot.  
DecisionCase must be separated into DecisionContext and snapshot\_ref so that it does not become excessively heavy.  
DecisionCase → ApprovalRequest → ApprovalDecision → ApprovedAction → RuntimeValidationInput → RuntimeValidationResult → Safety Gate → SafetyGatePass or SafetyGateBlock → ExecutionRequest → Feedback → AuditRecord must be connected through decision\_trace\_id.  
Fallback routes must follow safety-first priority.

The final principles are as follows:

Different events, one decision route.  
Different risks, one approval discipline.  
Different evidence, one grounding requirement.  
Different clocks, one time trust rule.  
Different devices, one health-aware decision.  
Different states, one freshness rule.  
Different approvals, one TOCTOU check.  
Different networks, one heartbeat discipline.  
Different retries, one idempotency rule.  
Different AI outputs, one audit trace.  
Different contexts, one decision context.  
Different fallbacks, one safety-first priority.  
Different actions, one approval matrix.  
Different emergencies, one fast-path policy.  
Different humans, one authority model.  
Different policies, one decision backbone.

## **Decision / Approval Matrix** 

