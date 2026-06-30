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

If an Event Type expresses “what happened,” a State Model expresses “what is currently in what state,” an Evidence Model expresses “what proves that judgment,” and an Action Type expresses “what response can be taken,” then the Decision / Approval Matrix expresses “who must judge and approve at what level under these conditions.”

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

Emergency bypass does not mean “no approval is required.”

Emergency bypass means that an execution request may be allowed before human approval under a predefined emergency policy, while post-hoc audit is required afterward.

Example:

Gas level critical  
→ Emergency policy matched  
→ EmergencyApprovedAction created  
→ EmergencyExecutionRequest sent  
→ Post-hoc audit required

Emergency bypass is not irresponsible automatic execution.  
Emergency bypass is a structure that combines pre-approved policy with post-hoc audit.

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
→ trust\_upgrade\_status \= NO\_UPGRADE or TRUST\_UPGRADE\_PENDING  
→ approval not allowed

ATTESTED\_AI\_DERIVED  
→ trust\_upgrade\_status \= TRUST\_UPGRADED\_BY\_RULE / TRUST\_UPGRADED\_BY\_HUMAN / TRUST\_UPGRADED\_BY\_CROSS\_CHECK  
→ limited use allowed

AI\_DERIVED\_ONLY can be used for explanation or candidate generation.  
AI\_DERIVED\_ONLY cannot be used as the basis for high-risk approval.  
ATTESTED\_AI\_DERIVED can be used for limited purposes, but must not become the sole basis for a physical emergency fast-path.

---

## **5.3 Connecting device\_health\_snapshot**

The Decision Matrix must consider device health when using sensor or robot evidence.

device\_health\_snapshot \= OK  
→ normal evidence weighting

device\_health\_snapshot \= WARNING  
→ lower confidence or conflict policy required

device\_health\_snapshot \= CRITICAL  
→ evidence review or fail-safe evaluation

device\_health\_snapshot missing in high-risk path  
→ evidence review required

---

## **5.4 Connecting privacy\_lifecycle\_status**

Privacy-related evidence may affect a decision depending on its privacy lifecycle.

PII\_PRESENT  
→ access policy required

PII\_MASKED  
→ limited use

PII\_CRYPTO\_SHREDDED  
→ audit shell exists, operational approval not allowed

LEGAL\_HOLD  
→ retention and audit restrictions apply

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
→ World State snapshot at decision time

evidence\_snapshot\_ref  
→ Evidence Bundle snapshot at decision time

network\_snapshot\_ref  
→ heartbeat / latency snapshot at decision time

ai\_snapshot\_ref  
→ AI model, prompt, retrieval, ontology mapping snapshot

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
→ General information, automatic handling, or log recording

NOTICE  
→ Operator notification required

WARNING  
→ Supervisor review may be required

HIGH\_RISK  
→ Safety manager or supervisor approval required

CRITICAL\_EMERGENCY  
→ Emergency fast-path or fail-safe required

EXCEPTIONAL  
→ Expert review, war room, or policy exception review required

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
→ Automatic handling allowed

OPERATOR\_ACK  
→ Operator acknowledgment required

SUPERVISOR\_APPROVAL  
→ Field supervisor approval required

SAFETY\_MANAGER\_APPROVAL  
→ Safety manager approval required

WAR\_ROOM\_APPROVAL  
→ Multi-party approval required in complex high-risk situations

EXPERT\_REVIEW  
→ Review required from structural, legal, AI, robotics, or equipment experts

POLICY\_OWNER\_APPROVAL  
→ Policy exception or policy change required

EMERGENCY\_POLICY\_BYPASS  
→ Immediate handling allowed under a predefined emergency policy; post-hoc audit is mandatory

POST\_HOC\_AUDIT\_ONLY  
→ Only post-hoc audit is required

---

# **11\. Mapping Between Decision Route and Approval Level**

## **11.1 Basic Mapping**

INFO  
→ AUTO\_ALLOW or AUDIT\_ONLY  
→ NO\_APPROVAL

NOTICE  
→ NOTIFICATION\_ONLY  
→ OPERATOR\_ACK

WARNING  
→ SUPERVISOR\_APPROVAL\_REQUIRED  
→ SUPERVISOR\_APPROVAL

HIGH\_RISK  
→ SAFETY\_MANAGER\_APPROVAL\_REQUIRED  
→ SAFETY\_MANAGER\_APPROVAL

CRITICAL\_EMERGENCY  
→ EMERGENCY\_FAST\_PATH or FAIL\_SAFE\_REQUIRED  
→ EMERGENCY\_POLICY\_BYPASS \+ POST\_HOC\_AUDIT\_ONLY

EXCEPTIONAL  
→ WAR\_ROOM\_APPROVAL\_REQUIRED or EXPERT\_REVIEW\_REQUIRED  
→ WAR\_ROOM\_APPROVAL / EXPERT\_REVIEW

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
→ EVIDENCE\_REVIEW\_REQUIRED or SAFETY\_MANAGER\_APPROVAL\_REQUIRED

Example:

risk\_level \= HIGH\_RISK  
but network\_latency\_exceeded \= true  
→ NETWORK\_HEALTH\_REVIEW\_REQUIRED or FAIL\_SAFE\_REQUIRED

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
→ normal judgment possible

STALE  
→ high-risk approval not allowed, revalidation required

CONFLICTED  
→ conflict resolution required

UNVERIFIED  
→ approval not allowed, evidence review required

AI\_DERIVED\_ONLY  
→ explanation allowed, approval not allowed

ATTESTED\_AI\_DERIVED  
→ limited use allowed

CRYPTO\_SHREDDED  
→ audit shell exists, but not usable for operational approval

---

## **12.3 Decision Impact by Time Trust Status**

HIGH\_TIME\_TRUST  
→ normal decision allowed

MEDIUM\_TIME\_TRUST  
→ allowed for non-critical decision, high-risk requires policy

LOW\_TIME\_TRUST  
→ revalidation required

UNTRUSTED\_TIME  
→ approval blocked

UNKNOWN\_TIME\_TRUST  
→ evidence review required

---

## **12.4 Decision Impact by Device Health Status**

OK  
→ normal evidence use

WARNING  
→ lower confidence, conflict policy required

CRITICAL  
→ evidence review or fail-safe evaluation

UNKNOWN  
→ high-risk approval blocked unless alternative verified evidence exists

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
→ normal judgment possible

PENDING  
→ execution may be held even if approval is possible

STALE  
→ revalidation required

UNKNOWN  
→ manual review or fail-safe evaluation

CONFLICT  
→ reconciliation required

FAIL\_SAFE\_TRIGGERED  
→ emergency route

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
→ execution may proceed

LOW\_RISK\_DELTA  
→ proceed with audit

HIGH\_RISK\_DELTA  
→ TOCTOU\_REVALIDATION\_REQUIRED

SAFETY\_CRITICAL\_DELTA  
→ FAIL\_SAFE\_REQUIRED or MANUAL\_OVERRIDE\_REQUIRED

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
→ normal execution path

DEGRADED  
→ approval may remain valid, execution requires caution or recheck

LATENCY\_EXCEEDED  
→ NETWORK\_HEALTH\_REVIEW\_REQUIRED or FAIL\_SAFE\_REQUIRED

HEARTBEAT\_LOST  
→ execution blocked

ADAPTER\_UNAVAILABLE  
→ execution blocked or fallback route

COMMAND\_ACK\_TIMEOUT  
→ recovery or fail-safe evaluation

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
→ normal decision route

CONFLICT\_DETECTED  
→ apply conflict policy

CONFLICT\_RESOLVED  
→ judgment possible based on selected evidence

CONFLICT\_UNDER\_REVIEW  
→ approval hold

CONFLICT\_ESCALATED  
→ safety manager or expert review

FAIL\_SAFE\_ON\_CONFLICT  
→ emergency fast-path or fail-safe required

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
→ ATTESTED\_AI\_DERIVED  
→ can support emergency context  
→ cannot be the sole emergency trigger

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
→ Minimum Evidence Bundle  
→ Emergency Policy Match  
→ Network / Heartbeat Check  
→ Decision Route: EMERGENCY\_FAST\_PATH  
→ EmergencyApprovedAction  
→ Safety Gate  
→ EmergencyExecutionRequest  
→ External Control System  
→ Feedback  
→ Post-hoc Audit

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
→ manages policy registry, approval matrix, safety policy, and emergency policy

PDP  
→ OPA / Rego / policy evaluator returns allow / deny / require\_approval decisions

PEP  
→ enforces policy at the API Gateway, Safety Gate, and External Adapter

PIP  
→ World State, Ontology, Evidence Store, Role DB, Approval DB

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
→ escalate

REJECTED  
→ deny or recovery route

TIMEOUT\_HIGH\_RISK  
→ escalate to safety manager

TIMEOUT\_CRITICAL  
→ emergency policy evaluation or fail-safe evaluation

TIMEOUT\_EXCEPTIONAL  
→ war room escalation

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

# **24\. SafetyGatePrecheck**

SafetyGatePrecheck is the final defense line after Approval and before ExecutionRequest creation.

## **24.1 Required Validations**

Performed for every ApprovedAction.

approval\_valid\_until\_check  
idempotency\_key\_check  
target\_validity\_check  
policy\_decision\_still\_valid\_check  
conflict\_status\_check

---

## **24.2 High-Risk Conditional Validations**

Performed when risk\_level is HIGH\_RISK or higher.

evidence\_freshness\_check  
state\_freshness\_check  
TOCTOU\_state\_delta\_check  
time\_trust\_check  
device\_health\_check  
source\_trust\_check

---

## **24.3 External System Conditional Validations**

Performed when external systems, robots, PLCs, SCADA, or access control systems are involved.

network\_latency\_check  
heartbeat\_check  
external\_adapter\_availability\_check  
command\_ack\_timeout\_check

---

## **24.4 AI-Derived Conditional Validations**

Performed when AI-derived or attested AI-derived evidence influenced the action candidate.

ai\_trace\_check  
trust\_upgrade\_status\_check  
attestation\_ref\_check  
evidence\_grounding\_check

---

## **24.5 High-Frequency Event Handling Principle**

If every SafetyGatePrecheck is performed for high-frequency sensor telemetry, it can create a bottleneck.

Therefore, high-frequency telemetry must first pass through the stream layer and evidence promotion rules.

High-frequency telemetry  
→ stream aggregation  
→ threshold / anomaly / state change detection  
→ semantic event promotion  
→ decision evaluation

The Decision / Approval Matrix operates on semantic events or promoted evidence.

---

## **24.6 Handling on Failure**

approval expired  
→ deny execution, request re-approval

TOCTOU high-risk delta  
→ TOCTOU\_REVALIDATION\_REQUIRED

network latency exceeded  
→ NETWORK\_HEALTH\_REVIEW\_REQUIRED or FAIL\_SAFE\_REQUIRED

heartbeat lost  
→ block execution

adapter unavailable  
→ fallback route or fail-safe evaluation

idempotency collision  
→ return previous result or block duplicate execution

time trust insufficient  
→ EVIDENCE\_REVIEW\_REQUIRED

device health critical  
→ EVIDENCE\_REVIEW\_REQUIRED or FAIL\_SAFE\_REQUIRED

---

# **25\. DecisionTrace Rule**

The entire flow from DecisionCase → ApprovalRequest → ApprovalDecision → ApprovedAction → ExecutionRequest → Feedback → AuditRecord must be connected with a single decision\_trace\_id.

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

## **33.1 Scenario 1: Gas Critical → Emergency Evacuation**

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
→ Safety Gate  
→ EmergencyExecutionRequest  
→ External Control System  
→ Feedback  
→ Post-hoc Audit

---

## **33.2 Scenario 2: Robot Mission Blocked → Supervisor Approval**

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
→ Supervisor Approval  
→ ApprovedAction  
→ Safety Gate  
→ ExecutionRequest to FleetManager

---

## **33.3 Scenario 3: Stale Worker Location → Approval Hold**

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
→ hold approval  
→ re-evaluate

---

## **33.4 Scenario 4: Evidence Conflict → Fail-Safe**

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
→ Emergency action candidate  
→ Safety Gate  
→ EmergencyExecutionRequest

---

## **33.5 Scenario 5: LLM Proposed Action → Evidence Check**

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
→ request evidence grounding  
→ no approval until evidence bundle exists

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
→ request fresh approval or emergency evaluation

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
→ escalate or use local fail-safe policy

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
Even if Approval exists, ExecutionRequest cannot be created unless the Safety Gate is passed.  
Even if Approval is valid, TOCTOU revalidation is required if the world state changes immediately before execution.  
Even if the external adapter is alive, execution must not proceed if heartbeat or network latency exceeds the threshold.  
Physical execution requests must prevent duplicate execution using idempotency\_key.  
AI-derived decision support must leave auditable model version, prompt, retrieval snapshot, and ontology mapping snapshot.  
DecisionCase must be separated into DecisionContext and snapshot\_ref so that it does not become excessively heavy.  
DecisionCase → ApprovalRequest → ApprovalDecision → ExecutionRequest → Feedback → AuditRecord must be connected through decision\_trace\_id.  
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

# **1\. 목적**

본 문서는 온톨로지 중심 사이버-물리 플랫폼에서 사용되는 Decision / Approval Matrix의 핵심 규칙을 정의한다.

Decision / Approval Matrix는 플랫폼이 특정 Event, State, Evidence, ActionCandidate를 받았을 때 다음을 결정하는 구조다.

이 상황은 자동 처리 가능한가?  
이 상황은 사람에게 알림만 보내면 되는가?  
이 상황은 supervisor approval이 필요한가?  
이 상황은 safety manager approval이 필요한가?  
이 상황은 war room approval이 필요한가?  
이 상황은 expert review가 필요한가?  
이 상황은 emergency fast-path로 즉시 처리해야 하는가?  
이 상황은 evidence 부족으로 거부해야 하는가?  
이 상황은 stale state 때문에 보류해야 하는가?  
이 상황은 conflict 때문에 fail-safe로 연결해야 하는가?  
이 상황은 network latency 또는 heartbeat 문제 때문에 drop / fail-safe 처리해야 하는가?  
승인 시점과 실행 시점 사이의 상태 변화, 즉 TOCTOU 위험이 존재하는가?  
이 판단은 Evidence Model에서 정의한 time trust, source trust, device health, trust upgrade, privacy lifecycle을 만족하는가?

Event Type이 “무슨 일이 발생했는가”를 표현하고, State Model이 “현재 무엇이 어떤 상태인가”를 표현하며, Evidence Model이 “그 판단을 무엇으로 증명할 수 있는가”를 표현하고, Action Type이 “어떤 대응을 할 수 있는가”를 표현한다면, Decision / Approval Matrix는 “이 조건에서 누가 어떤 수준으로 판단하고 승인해야 하는가”를 표현한다.

핵심 원칙은 다음이다.

Decision selects a route.  
Approval grants authority.  
Safety Gate validates execution eligibility.  
ExecutionRequest asks external systems to act.  
Feedback proves execution result.  
Audit preserves accountability.

Decision은 route를 결정한다.  
Approval은 권한을 부여한다.  
Safety Gate는 실행 가능성을 검증한다.  
ExecutionRequest는 외부 시스템에 실행 요청을 보낸다.  
Feedback은 실행 결과를 증명한다.  
Audit은 책임 추적성을 보존한다.

---

# **2\. 문서 분리 원칙**

Decision / Approval Matrix 문서는 두 부분으로 나눈다.

## **2.1 Core Decision / Approval Matrix Specification**

본 문서다.

다루는 내용:

Decision Matrix 정의  
Approval Matrix 정의  
Decision과 Approval의 차이  
Decision Input과 Decision Output  
DecisionContext 구조  
Risk Level과 Severity 분류  
Approval Level 분류  
Decision Route 분류  
Human-in-the-loop 규칙  
Emergency fast-path 규칙  
Evidence Model 연계  
State freshness 연계  
TOCTOU 방지 규칙  
Network latency / heartbeat 검증 규칙  
Conflict handling 연결  
Safety Gate 연결  
SafetyGatePrecheck 실행 순서  
Policy Engine / PDP / PEP 연결  
PolicyEngineAdapter interface 정의  
Approval timeout / escalation 규칙  
Idempotency rule  
AI governance trace rule  
Fallback route 우선순위  
DecisionTrace 연결 규칙  
DecisionCaseDTO 정의  
DecisionContextDTO 정의  
ApprovalRequestDTO 정의  
ApprovalDecisionDTO 정의  
DecisionMatrixSpecDTO 정의  
ApprovalMatrixSpecDTO 정의  
MVP decision / approval matrix set  
핵심 시나리오 흐름

## **2.2 Appendix F: Decision / Approval Matrix Catalog**

별도 부록 문서다.

다루는 내용:

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

이렇게 분리하면 Core 문서는 짧고 안정적으로 유지되고, 실제 matrix catalog는 현장 운영 정책에 따라 계속 확장할 수 있다.

---

# **3\. Decision / Approval Matrix의 정의**

## **3.1 Decision Matrix 정의**

Decision Matrix는 특정 상황에서 어떤 decision route를 선택할지 정의하는 규칙 집합이다.

Decision Matrix는 다음 질문에 답해야 한다.

이 event는 어떤 위험 수준인가?  
이 state는 정상인가, 경고인가, 위험인가, 비상인가?  
이 action candidate는 허용 가능한가?  
필요한 evidence가 충분한가?  
evidence freshness는 유효한가?  
time trust level은 충분한가?  
clock sync status는 정상인가?  
source trust level은 충분한가?  
device health snapshot은 정상인가?  
trust upgrade status는 어떤 상태인가?  
privacy lifecycle status가 operational approval에 영향을 주는가?  
state는 stale하지 않은가?  
conflict가 존재하는가?  
network latency가 허용 범위 안에 있는가?  
external system heartbeat가 정상인가?  
승인 시점과 실행 시점 사이에 target state가 바뀌었는가?  
이 action은 자동 처리 가능한가?  
이 action은 human approval이 필요한가?  
이 action은 emergency fast-path 대상인가?  
이 action은 차단되어야 하는가?  
이 판단은 audit 대상인가?

---

## **3.2 Approval Matrix 정의**

Approval Matrix는 특정 action이나 decision이 어떤 승인 수준을 요구하는지 정의하는 규칙 집합이다.

Approval Matrix는 다음 질문에 답해야 한다.

누가 승인할 수 있는가?  
어떤 role이 필요한가?  
어떤 clearance가 필요한가?  
어떤 approval level이 필요한가?  
단일 승인으로 충분한가?  
다중 승인이 필요한가?  
emergency 상황에서 사전 승인된 정책으로 우회 가능한가?  
우회 시 post-hoc audit이 필요한가?  
승인 timeout 시 어떻게 처리하는가?  
승인이 거부되면 어떤 recovery path로 가는가?  
승인 결과에 idempotency\_key가 있는가?  
승인 유효기간 안에 Safety Gate가 실행되는가?  
승인 시점의 state snapshot과 실행 시점의 state snapshot이 일치하는가?

---

# **4\. 핵심 구분**

## **4.1 Decision과 Approval의 구분**

Decision은 판단 경로를 정한다.

Approval은 권한을 부여한다.

예:

Decision:  
This situation requires SAFETY\_MANAGER\_APPROVAL.

Approval:  
Safety Manager Kim approved ACTION\_STOP\_WORK.

Decision은 route다.  
Approval은 authority grant다.

---

## **4.2 Decision과 Policy Decision의 구분**

Decision Matrix는 플랫폼 수준에서 route를 정한다.

Policy Decision은 특정 policy engine이 allow / deny / require\_approval 같은 정책 판단을 반환하는 것이다.

예:

Decision Matrix:  
ZoneRiskState.CRITICAL → emergency route

Policy Decision:  
OPA allows ACTION\_EMERGENCY\_EVACUATE\_ZONE under EmergencyPolicy\_001

Decision Matrix는 전체 workflow route를 정한다.  
Policy Decision은 특정 rule set의 판단 결과다.

---

## **4.3 Approval과 Safety Gate의 구분**

Approval은 사람이 또는 정책이 action을 승인하는 것이다.

Safety Gate는 승인된 action이 실제 실행 요청으로 넘어가기 전에 최종 검증하는 구조다.

예:

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

Approval이 있어도 Safety Gate를 통과하지 못하면 ExecutionRequest를 만들 수 없다.

---

## **4.4 Approval과 Execution의 구분**

Approval은 실행 권한이다.

Execution은 외부 시스템에 실행 요청을 보내는 것이다.

예:

ApprovedAction:  
ACTION\_DISABLE\_ROBOT\_MISSION approved.

ExecutionRequest:  
Send disable mission request to FleetManager.

ApprovedAction은 직접 물리 제어 명령이 아니다.

---

## **4.5 Emergency Bypass와 무승인의 구분**

Emergency bypass는 “승인이 필요 없다”는 뜻이 아니다.

Emergency bypass는 사전에 정의된 emergency policy에 따라 인간 승인 전 실행 요청을 허용하고, 이후 post-hoc audit을 요구하는 구조다.

예:

Gas level critical  
→ Emergency policy matched  
→ EmergencyApprovedAction created  
→ EmergencyExecutionRequest sent  
→ Post-hoc audit required

Emergency bypass는 무책임한 자동 실행이 아니다.  
Emergency bypass는 사전 정책 승인과 사후 감사가 결합된 구조다.

---

# **5\. Evidence Model과의 명시적 연계**

Decision / Approval Matrix는 Evidence Model과 직접 연결되어야 한다.

Evidence Model에서 정의한 다음 값들은 Decision Input 또는 DecisionContext에서 직접 참조되어야 한다.

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

## **5.1 evidence\_freshness\_summary 확장**

`evidence_freshness_summary`는 단순히 stale 여부만 표현하면 안 된다.

다음 값을 포함해야 한다.

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

예:

evidence\_freshness\_summary \= {  
  freshness\_status: VALID,  
  time\_trust\_level: HIGH\_TIME\_TRUST,  
  clock\_sync\_status: SYNCED,  
  clock\_drift\_estimate\_ms: 120,  
  device\_health\_status: OK  
}

---

## **5.2 AI\_DERIVED\_ONLY와 trust\_upgrade\_status 연결**

Decision Matrix는 AI-derived evidence를 Evidence Model의 `trust_upgrade_status`와 연결해야 한다.

AI\_DERIVED\_ONLY  
→ trust\_upgrade\_status \= NO\_UPGRADE or TRUST\_UPGRADE\_PENDING  
→ approval not allowed

ATTESTED\_AI\_DERIVED  
→ trust\_upgrade\_status \= TRUST\_UPGRADED\_BY\_RULE / TRUST\_UPGRADED\_BY\_HUMAN / TRUST\_UPGRADED\_BY\_CROSS\_CHECK  
→ limited use allowed

AI\_DERIVED\_ONLY는 explanation 또는 candidate generation에는 사용할 수 있다.  
AI\_DERIVED\_ONLY는 high-risk approval 근거가 될 수 없다.  
ATTESTED\_AI\_DERIVED는 제한된 목적에 사용할 수 있지만, 물리 emergency fast-path의 단독 근거가 되어서는 안 된다.

---

## **5.3 device\_health\_snapshot 연결**

Decision Matrix는 sensor 또는 robot evidence를 사용할 때 device health를 고려해야 한다.

device\_health\_snapshot \= OK  
→ normal evidence weighting

device\_health\_snapshot \= WARNING  
→ lower confidence or conflict policy required

device\_health\_snapshot \= CRITICAL  
→ evidence review or fail-safe evaluation

device\_health\_snapshot missing in high-risk path  
→ evidence review required

---

## **5.4 privacy\_lifecycle\_status 연결**

개인정보 관련 evidence는 privacy lifecycle이 decision에 영향을 줄 수 있다.

PII\_PRESENT  
→ access policy required

PII\_MASKED  
→ limited use

PII\_CRYPTO\_SHREDDED  
→ audit shell exists, operational approval not allowed

LEGAL\_HOLD  
→ retention and audit restrictions apply

---

# **6\. Decision Input Model**

Decision Matrix는 여러 입력을 함께 평가해야 한다.

## **6.1 Core Decision Inputs**

권장 입력:

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

## **6.2 Decision Input 원칙**

Decision은 단일 event만 보고 판단하면 안 된다.

다음 조합을 함께 봐야 한다.

Event \+ State \+ Evidence \+ Policy \+ Context \+ ActionCandidate

고위험 CPS에서는 다음도 함께 봐야 한다.

Time Trust \+ Device Health \+ Network Health \+ Approval Validity \+ TOCTOU State Delta

예:

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

이 조합이 있어야 emergency route로 갈 수 있다.

---

# **7\. DecisionContextDTO**

DecisionCaseDTO가 과도하게 커지는 것을 방지하기 위해, 상세 context는 DecisionContextDTO 또는 snapshot reference로 분리한다.

DecisionCaseDTO는 핵심 판단 결과와 참조 ID를 가진다.  
DecisionContextDTO는 판단에 사용된 상세 상태 snapshot, evidence snapshot, network snapshot, AI trace snapshot을 가진다.

---

## **7.1 DecisionContextDTO 필드**

권장 필드:

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

## **7.2 Snapshot Reference 원칙**

고위험 판단에서는 snapshot을 반드시 고정해야 한다.

state\_snapshot\_ref  
→ decision 시점의 World State snapshot

evidence\_snapshot\_ref  
→ decision 시점의 Evidence Bundle snapshot

network\_snapshot\_ref  
→ decision 시점의 heartbeat / latency snapshot

ai\_snapshot\_ref  
→ AI model, prompt, retrieval, ontology mapping snapshot

이렇게 하면 DecisionCaseDTO가 가벼워지고, 감사 시 필요한 상세 정보는 snapshot ref로 추적할 수 있다.

---

# **8\. Decision Output Model**

Decision Matrix는 판단 결과로 decision route를 반환해야 한다.

## **8.1 Core Decision Outputs**

권장 출력:

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

## **8.2 Decision Route 값**

권장 값:

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

Decision Matrix는 risk level을 기준으로 approval level을 결정한다.

## **9.1 Risk Level**

권장 값:

INFO  
NOTICE  
WARNING  
HIGH\_RISK  
CRITICAL\_EMERGENCY  
EXCEPTIONAL

---

## **9.2 Risk Level 의미**

INFO  
→ 일반 정보, 자동 처리 또는 로그 기록

NOTICE  
→ 운영자에게 알림 필요

WARNING  
→ supervisor 검토 필요 가능성 있음

HIGH\_RISK  
→ safety manager 또는 supervisor approval 필요

CRITICAL\_EMERGENCY  
→ emergency fast-path 또는 fail-safe 필요

EXCEPTIONAL  
→ expert review, war room, policy exception review 필요

---

# **10\. Approval Level Model**

Approval Matrix는 승인 수준을 명확히 정의해야 한다.

## **10.1 Approval Level**

권장 값:

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

## **10.2 Approval Level 의미**

NO\_APPROVAL  
→ 자동 처리 가능

OPERATOR\_ACK  
→ 운영자 확인 필요

SUPERVISOR\_APPROVAL  
→ 현장 supervisor 승인 필요

SAFETY\_MANAGER\_APPROVAL  
→ 안전 관리자 승인 필요

WAR\_ROOM\_APPROVAL  
→ 복합 고위험 상황에서 다자 승인 필요

EXPERT\_REVIEW  
→ 구조, 법무, AI, 로봇, 설비 전문가 검토 필요

POLICY\_OWNER\_APPROVAL  
→ 정책 예외 또는 정책 변경 필요

EMERGENCY\_POLICY\_BYPASS  
→ 사전 정의된 emergency policy로 즉시 처리 가능, 사후 감사 필수

POST\_HOC\_AUDIT\_ONLY  
→ 사후 감사만 요구

---

# **11\. Decision Route와 Approval Level 매핑**

## **11.1 기본 매핑**

INFO  
→ AUTO\_ALLOW or AUDIT\_ONLY  
→ NO\_APPROVAL

NOTICE  
→ NOTIFICATION\_ONLY  
→ OPERATOR\_ACK

WARNING  
→ SUPERVISOR\_APPROVAL\_REQUIRED  
→ SUPERVISOR\_APPROVAL

HIGH\_RISK  
→ SAFETY\_MANAGER\_APPROVAL\_REQUIRED  
→ SAFETY\_MANAGER\_APPROVAL

CRITICAL\_EMERGENCY  
→ EMERGENCY\_FAST\_PATH or FAIL\_SAFE\_REQUIRED  
→ EMERGENCY\_POLICY\_BYPASS \+ POST\_HOC\_AUDIT\_ONLY

EXCEPTIONAL  
→ WAR\_ROOM\_APPROVAL\_REQUIRED or EXPERT\_REVIEW\_REQUIRED  
→ WAR\_ROOM\_APPROVAL / EXPERT\_REVIEW

---

## **11.2 중요한 예외**

Risk Level만으로 결정하면 안 된다.

다음 조건이 있으면 route가 상향될 수 있다.

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

예:

risk\_level \= WARNING  
but evidence\_conflict\_unresolved \= true  
→ EVIDENCE\_REVIEW\_REQUIRED or SAFETY\_MANAGER\_APPROVAL\_REQUIRED

예:

risk\_level \= HIGH\_RISK  
but network\_latency\_exceeded \= true  
→ NETWORK\_HEALTH\_REVIEW\_REQUIRED or FAIL\_SAFE\_REQUIRED

---

# **12\. Evidence Requirement 연결**

Decision / Approval Matrix는 Evidence Model과 직접 연결되어야 한다.

## **12.1 Evidence Rule**

High-risk decision은 evidence bundle 없이 승인되면 안 된다.

Emergency decision은 최소 evidence를 요구하되, 사후 감사가 필수다.

AI-derived evidence는 단독으로 approval 근거가 될 수 없다.

ATTESTED\_AI\_DERIVED evidence는 제한된 목적에 한해 사용할 수 있다.

stale evidence는 high-risk action approval에 사용할 수 없다.

time\_trust\_level이 낮은 evidence는 high-risk decision에서 사용할 수 없다.

clock\_sync\_status가 DRIFT\_DETECTED 또는 UNKNOWN이면 freshness를 재검증해야 한다.

device\_health\_snapshot이 WARNING 또는 CRITICAL이면 conflict policy 또는 evidence review가 필요하다.

---

## **12.2 Evidence 상태별 Decision 영향**

VALID  
→ 정상 판단 가능

STALE  
→ high-risk approval 불가, revalidation 필요

CONFLICTED  
→ conflict resolution 필요

UNVERIFIED  
→ approval 불가, evidence review 필요

AI\_DERIVED\_ONLY  
→ explanation 가능, approval 불가

ATTESTED\_AI\_DERIVED  
→ 제한적 사용 가능

CRYPTO\_SHREDDED  
→ audit shell은 존재하지만 operational approval에는 사용 불가

---

## **12.3 Time Trust 상태별 Decision 영향**

HIGH\_TIME\_TRUST  
→ normal decision allowed

MEDIUM\_TIME\_TRUST  
→ allowed for non-critical decision, high-risk requires policy

LOW\_TIME\_TRUST  
→ revalidation required

UNTRUSTED\_TIME  
→ approval blocked

UNKNOWN\_TIME\_TRUST  
→ evidence review required

---

## **12.4 Device Health 상태별 Decision 영향**

OK  
→ normal evidence use

WARNING  
→ lower confidence, conflict policy required

CRITICAL  
→ evidence review or fail-safe evaluation

UNKNOWN  
→ high-risk approval blocked unless alternative verified evidence exists

---

# **13\. State Freshness 연결**

Decision / Approval Matrix는 State Model과 직접 연결되어야 한다.

## **13.1 State Rule**

stale state를 기반으로 high-risk action을 승인하면 안 된다.

pending\_state는 confirmed\_state로 간주하면 안 된다.

inferred\_state와 runtime state가 temporal grace period 안에서 불일치하는 경우 즉시 conflict로 처리하지 않는다.

reconciliation failure가 safety-critical이면 fail-safe path로 연결한다.

---

## **13.2 State 상태별 Decision 영향**

CONFIRMED  
→ 정상 판단 가능

PENDING  
→ approval 가능하더라도 execution 보류 가능

STALE  
→ revalidation required

UNKNOWN  
→ manual review or fail-safe evaluation

CONFLICT  
→ reconciliation required

FAIL\_SAFE\_TRIGGERED  
→ emergency route

---

# **14\. TOCTOU 방지 규칙**

TOCTOU는 Time-of-Check to Time-of-Use를 의미한다.

Approval이 내려진 시점의 상태와 실제 ExecutionRequest를 생성하는 시점의 상태가 다르면 위험하다.

예:

Approval time:  
Zone\_A has no worker.

Execution time:  
Worker\_17 entered Zone\_A.

이 경우 승인된 action이라도 그대로 실행하면 안 된다.

---

## **14.1 TOCTOU Precheck**

SafetyGatePrecheck는 다음을 비교해야 한다.

state\_snapshot\_ref\_at\_decision  
state\_snapshot\_ref\_at\_approval  
state\_snapshot\_ref\_at\_execution  
evidence\_snapshot\_ref\_at\_decision  
evidence\_snapshot\_ref\_at\_execution  
target\_state\_at\_approval  
target\_state\_at\_execution

---

## **14.2 TOCTOU Decision 결과**

NO\_DELTA  
→ execution may proceed

LOW\_RISK\_DELTA  
→ proceed with audit

HIGH\_RISK\_DELTA  
→ TOCTOU\_REVALIDATION\_REQUIRED

SAFETY\_CRITICAL\_DELTA  
→ FAIL\_SAFE\_REQUIRED or MANUAL\_OVERRIDE\_REQUIRED

---

## **14.3 TOCTOU 원칙**

Approval does not freeze the world.  
Safety Gate must re-check the world before execution.

Approval은 세상을 고정시키지 않는다.  
Safety Gate는 실행 직전에 현재 world state를 다시 확인해야 한다.

---

# **15\. Network Latency / Heartbeat Rule**

고위험 CPS에서는 승인된 action이라도 네트워크 상태가 나쁘면 실행하면 안 된다.

특히 로봇, PLC, SCADA, FleetManager, 현장 access control system은 heartbeat와 latency를 검증해야 한다.

---

## **15.1 Network Health Check 대상**

external\_adapter  
fleet\_manager  
robot\_middleware  
PLC / SCADA gateway  
access\_control\_system  
edge\_gateway  
message\_broker

---

## **15.2 검증 항목**

heartbeat\_status  
last\_heartbeat\_at  
network\_latency\_ms  
max\_allowed\_latency\_ms  
packet\_loss\_rate  
adapter\_availability  
external\_system\_availability  
command\_ack\_timeout

---

## **15.3 Network 상태별 Decision 영향**

HEALTHY  
→ normal execution path

DEGRADED  
→ approval may remain valid, execution requires caution or recheck

LATENCY\_EXCEEDED  
→ NETWORK\_HEALTH\_REVIEW\_REQUIRED or FAIL\_SAFE\_REQUIRED

HEARTBEAT\_LOST  
→ execution blocked

ADAPTER\_UNAVAILABLE  
→ execution blocked or fallback route

COMMAND\_ACK\_TIMEOUT  
→ recovery or fail-safe evaluation

---

## **15.4 핵심 원칙**

ApprovedAction is not enough.  
External path must be alive.

ApprovedAction이 있어도 외부 실행 경로가 살아 있어야 한다.

---

# **16\. Conflict Handling Rule**

Evidence conflict 또는 state conflict가 존재하면 decision route가 변경되어야 한다.

## **16.1 Conflict Decision Rule**

NO\_CONFLICT  
→ normal decision route

CONFLICT\_DETECTED  
→ conflict policy 적용

CONFLICT\_RESOLVED  
→ selected evidence 기준 판단 가능

CONFLICT\_UNDER\_REVIEW  
→ approval hold

CONFLICT\_ESCALATED  
→ safety manager or expert review

FAIL\_SAFE\_ON\_CONFLICT  
→ emergency fast-path or fail-safe required

---

## **16.2 Safety-critical Conflict Rule**

다음 조건이면 fail-safe evaluation을 수행한다.

risk\_level \>= HIGH\_RISK  
AND conflict\_status \!= CONFLICT\_RESOLVED

또는:

risk\_level \= CRITICAL\_EMERGENCY  
AND evidence\_conflict\_detected \= true

결과:

decision\_route \= FAIL\_SAFE\_REQUIRED  
approval\_level\_required \= EMERGENCY\_POLICY\_BYPASS  
post\_hoc\_audit\_required \= true

---

# **17\. Human-in-the-loop Rule**

Decision / Approval Matrix는 사람의 개입 지점을 명확히 정의해야 한다.

## **17.1 Human Approval이 필요한 경우**

다음 경우 human approval이 필요하다.

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

## **17.2 Human Approval이 필요하지 않을 수 있는 경우**

다음 경우 자동 처리 가능하다.

low-risk notification  
dashboard update  
audit-only logging  
normal telemetry state update  
routine state transition  
pre-approved emergency fast-path

단, pre-approved emergency fast-path는 post-hoc audit을 요구한다.

---

# **18\. Emergency Fast-Path Rule**

Emergency Fast-Path는 critical emergency 상황에서 사용한다.

## **18.1 조건**

다음 조건을 만족해야 한다.

risk\_level \= CRITICAL\_EMERGENCY  
emergency\_policy\_matched \= true  
minimum\_evidence\_bundle\_present \= true  
target\_entity\_valid \= true  
network\_minimum\_viable \= true  
external\_adapter\_available \= true  
safety\_gate\_required \= true  
post\_hoc\_audit\_required \= true

---

## **18.2 Minimum Evidence Bundle 정의**

Emergency Fast-Path에서 `minimum_evidence_bundle_present = true`가 되려면 다음 조건을 만족해야 한다.

at least one VERIFIED\_DEVICE or TRUSTED\_SYSTEM operational evidence exists  
AND evidence freshness is valid or emergency-acceptable  
AND time\_trust\_level \>= MEDIUM\_TIME\_TRUST  
AND target entity is bound  
AND emergency policy is matched

ATTESTED\_AI\_DERIVED evidence는 보조 evidence로 사용할 수 있다.

예:

Permit condition extracted from document  
→ ATTESTED\_AI\_DERIVED  
→ can support emergency context  
→ cannot be the sole emergency trigger

즉, AI 또는 문서 추출 evidence만으로 물리 emergency fast-path를 실행하면 안 된다.

---

## **18.3 금지 사항**

LLM output만으로 emergency fast-path를 실행하면 안 된다.

AI\_DERIVED\_ONLY evidence만으로 emergency fast-path를 실행하면 안 된다.

ATTESTED\_AI\_DERIVED evidence만으로 물리 emergency fast-path를 실행하면 안 된다.

unverified source만으로 emergency fast-path를 실행하면 안 된다.

target이 불명확하면 emergency fast-path를 실행하면 안 된다.

external adapter가 unavailable이면 emergency execution request를 만들면 안 된다.

heartbeat가 끊긴 외부 시스템에 execution request를 보내면 안 된다.

network latency가 허용 한계치를 초과하면 execution request를 만들면 안 된다. 단, fail-safe local action이 별도로 사전 정의되어 있으면 해당 경로로 전환한다.

---

## **18.4 Emergency Fast-Path 흐름**

Critical Event  
→ Minimum Evidence Bundle  
→ Emergency Policy Match  
→ Network / Heartbeat Check  
→ Decision Route: EMERGENCY\_FAST\_PATH  
→ EmergencyApprovedAction  
→ Safety Gate  
→ EmergencyExecutionRequest  
→ External Control System  
→ Feedback  
→ Post-hoc Audit

---

# **19\. Policy Engine / PDP / PEP 연결**

Decision / Approval Matrix는 policy engine과 연결된다.

## **19.1 구성 요소**

PAP \= Policy Administration Point  
PDP \= Policy Decision Point  
PEP \= Policy Enforcement Point  
PIP \= Policy Information Point

---

## **19.2 플랫폼 내 역할**

PAP  
→ policy registry, approval matrix, safety policy, emergency policy 관리

PDP  
→ OPA / Rego / policy evaluator가 allow / deny / require\_approval 판단

PEP  
→ API Gateway, Safety Gate, External Adapter에서 정책 집행

PIP  
→ World State, Ontology, Evidence Store, Role DB, Approval DB

---

## **19.3 Decision Matrix와 PDP 관계**

Decision Matrix는 workflow route를 정한다.

PDP는 특정 policy decision을 반환한다.

예:

Decision Matrix:  
ZoneRiskState.CRITICAL → EMERGENCY\_FAST\_PATH

PDP:  
EmergencyPolicy\_001 allows ACTION\_EMERGENCY\_EVACUATE\_ZONE

둘 다 필요하다.

---

# **20\. PolicyEngineAdapter Rule**

DecisionRouter가 올바르게 작동하려면 PolicyEngineAdapter interface가 초기에 정의되어야 한다.

PDP가 아직 완성되지 않았더라도 dummy PDP response를 먼저 정의해야 통합 테스트가 가능하다.

---

## **20.1 PolicyEngineAdapter 책임**

build policy context  
send request to PDP  
receive policy decision  
normalize allow / deny / require\_approval  
attach policy decision refs  
support dummy PDP for testing

---

## **20.2 PDP 호출 context 예시**

PolicyEngineAdapter는 PDP에 다음 context를 넘긴다.

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

## **20.3 PolicyDecisionResponse 기본 구조**

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

## **20.4 decision\_result 값**

ALLOW  
DENY  
REQUIRE\_APPROVAL  
REQUIRE\_EVIDENCE  
REQUIRE\_REVALIDATION  
REQUIRE\_FAIL\_SAFE

---

## **20.5 구현 원칙**

DecisionRouter must not hard-code policy logic.  
DecisionRouter calls PolicyEngineAdapter.  
PolicyEngineAdapter may use OPA / Rego / local rules / dummy PDP.

DecisionRouter가 policy logic을 직접 하드코딩하면 안 된다.  
DecisionRouter는 PolicyEngineAdapter를 호출한다.

---

# **21\. Approval Timeout and Escalation Rule**

Approval은 무한히 기다릴 수 없다.

## **21.1 Approval Timeout**

ApprovalRequest는 timeout\_policy를 가져야 한다.

권장 timeout 예시:

OPERATOR\_ACK → 30 seconds  
SUPERVISOR\_APPROVAL → 2 minutes  
SAFETY\_MANAGER\_APPROVAL → 5 minutes  
WAR\_ROOM\_APPROVAL → 15 minutes  
EXPERT\_REVIEW → policy-defined

---

## **21.2 Cascading Timeout Rule**

Approval이 escalation될 때 timeout은 단순히 새로 시작되면 안 된다.

상위 승인자는 이전 단계에서 이미 지연된 시간을 함께 받아야 한다.

ApprovalRequestDTO는 다음 정보를 유지해야 한다.

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

## **21.3 Timeout 계산 원칙**

current\_expires\_at \=  
  escalation\_started\_at \+ timeout\_for\_new\_level

단, audit에는 다음을 함께 남겨야 한다.

original\_requested\_at  
total\_elapsed\_time  
elapsed\_time\_before\_escalation  
previous\_approver\_response\_time  
escalation\_history

즉, 상위 승인 단계의 timeout은 동적으로 재계산되지만, 전체 지연 이력은 사라지면 안 된다.

---

## **21.4 Timeout 후 처리**

NO\_RESPONSE  
→ escalate

REJECTED  
→ deny or recovery route

TIMEOUT\_HIGH\_RISK  
→ escalate to safety manager

TIMEOUT\_CRITICAL  
→ emergency policy evaluation or fail-safe evaluation

TIMEOUT\_EXCEPTIONAL  
→ war room escalation

---

# **22\. Idempotency Rule**

물리 시스템에 대한 실행 요청은 중복 실행되면 안 된다.

네트워크 재시도, timeout, client retry, message broker 재전송이 발생해도 동일 명령이 여러 번 실행되면 안 된다.

따라서 ApprovalDecisionDTO와 ExecutionRequestDTO는 idempotency\_key를 가져야 한다.

---

## **22.1 idempotency\_key 생성 원칙**

권장 방식:

idempotency\_key \= hash(  
  approval\_decision\_id,  
  decision\_case\_id,  
  approved\_action\_type,  
  target\_entity\_refs,  
  trace\_id,  
  lifecycle\_version  
)

---

## **22.2 적용 범위**

ApprovalDecisionDTO  
ApprovedActionDTO  
ExecutionRequestDTO  
EmergencyExecutionRequestDTO  
ExternalControlRequestDTO

---

## **22.3 핵심 원칙**

Same approval decision must not create duplicate physical execution.  
Retry must be safe.

같은 approval decision이 중복 물리 실행을 만들면 안 된다.  
재시도는 안전해야 한다.

---

# **23\. AI Governance Trace Rule**

AI가 ActionCandidate, RiskInterpretation, EvidenceSummary, MappingProposal을 생성한 경우 DecisionCaseDTO 또는 DecisionContextDTO는 AI trace를 기록해야 한다.

---

## **23.1 AI Trace 필드**

권장 필드:

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

## **23.2 AI Trace 원칙**

AI output may influence candidate generation.  
AI trace must be auditable.  
AI output must not approve action.

AI output은 candidate 생성에 영향을 줄 수 있다.  
AI trace는 감사 가능해야 한다.  
AI output은 action을 승인할 수 없다.

---

# **24\. SafetyGatePrecheck**

SafetyGatePrecheck는 Approval 이후 ExecutionRequest 생성 전 최종 방어선이다.

## **24.1 필수 검증**

모든 ApprovedAction에 대해 수행한다.

approval\_valid\_until\_check  
idempotency\_key\_check  
target\_validity\_check  
policy\_decision\_still\_valid\_check  
conflict\_status\_check

---

## **24.2 High-risk 조건부 검증**

risk\_level이 HIGH\_RISK 이상인 경우 수행한다.

evidence\_freshness\_check  
state\_freshness\_check  
TOCTOU\_state\_delta\_check  
time\_trust\_check  
device\_health\_check  
source\_trust\_check

---

## **24.3 External system 조건부 검증**

외부 시스템, 로봇, PLC, SCADA, access control system이 관여하는 경우 수행한다.

network\_latency\_check  
heartbeat\_check  
external\_adapter\_availability\_check  
command\_ack\_timeout\_check

---

## **24.4 AI-derived 조건부 검증**

AI-derived 또는 attested AI-derived evidence가 action candidate에 영향을 준 경우 수행한다.

ai\_trace\_check  
trust\_upgrade\_status\_check  
attestation\_ref\_check  
evidence\_grounding\_check

---

## **24.5 고빈도 이벤트 처리 원칙**

고빈도 sensor telemetry에 대해 모든 SafetyGatePrecheck를 매번 수행하면 병목이 발생한다.

따라서 고빈도 telemetry는 먼저 stream layer와 evidence promotion rule을 통과해야 한다.

High-frequency telemetry  
→ stream aggregation  
→ threshold / anomaly / state change detection  
→ semantic event promotion  
→ decision evaluation

Decision / Approval Matrix는 semantic event 또는 promoted evidence를 대상으로 동작한다.

---

## **24.6 실패 시 처리**

approval expired  
→ deny execution, request re-approval

TOCTOU high-risk delta  
→ TOCTOU\_REVALIDATION\_REQUIRED

network latency exceeded  
→ NETWORK\_HEALTH\_REVIEW\_REQUIRED or FAIL\_SAFE\_REQUIRED

heartbeat lost  
→ block execution

adapter unavailable  
→ fallback route or fail-safe evaluation

idempotency collision  
→ return previous result or block duplicate execution

time trust insufficient  
→ EVIDENCE\_REVIEW\_REQUIRED

device health critical  
→ EVIDENCE\_REVIEW\_REQUIRED or FAIL\_SAFE\_REQUIRED

---

# **25\. DecisionTrace Rule**

DecisionCase → ApprovalRequest → ApprovalDecision → ApprovedAction → ExecutionRequest → Feedback → AuditRecord까지의 전체 흐름은 하나의 decision\_trace\_id로 연결되어야 한다.

---

## **25.1 decision\_trace\_id 적용 대상**

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

## **25.2 Decision Trace 원칙**

One decision path must be traceable end-to-end.

하나의 판단 경로는 끝까지 추적 가능해야 한다.

---

# **26\. Fallback Route Priority Rule**

fallback route가 여러 개일 경우 우선순위가 필요하다.

## **26.1 권장 우선순위**

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

## **26.2 핵심 원칙**

safety-critical 상황에서는 안전한 정지 또는 fail-safe가 우선이다.

operational convenience는 safety보다 우선할 수 없다.

---

# **27\. DecisionCaseDTO**

Decision 결과는 DecisionCaseDTO로 관리한다.

DecisionCaseDTO는 과도하게 무거워지지 않도록 상세 context를 직접 모두 보유하지 않고 snapshot\_ref를 중심으로 구성한다.

---

## **27.1 DecisionCaseDTO 필드**

권장 필드:

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

Approval 요청은 ApprovalRequestDTO로 관리한다.

## **28.1 ApprovalRequestDTO 필드**

권장 필드:

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

Approval 결과는 ApprovalDecisionDTO로 관리한다.

## **29.1 ApprovalDecisionDTO 필드**

권장 필드:

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

Decision Matrix는 DecisionMatrixSpecDTO로 관리한다.

DecisionMatrixSpecDTO는 Platform Core Registry 또는 Policy Module의 운영 registry에 속한다.

Ontology Module Boundary 기준으로 보면 DecisionMatrixSpecDTO는 Ontology 자체가 아니라 Registry에 속한다.

---

## **30.1 DecisionMatrixSpecDTO 필드**

권장 필드:

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

Approval Matrix는 ApprovalMatrixSpecDTO로 관리한다.

ApprovalMatrixSpecDTO는 Policy Module 또는 Platform Governance Registry에 속한다.

Ontology는 Approval이라는 의미를 정의한다.  
ApprovalMatrixSpecDTO는 실제 승인 운영 규칙을 정의한다.

---

## **31.1 ApprovalMatrixSpecDTO 필드**

권장 필드:

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

# **32\. Registry 운영 정책**

Decision / Approval Matrix는 governance 대상이다.

## **32.1 Registry Status**

권장 값:

DRAFT  
ACTIVE  
DEPRECATED  
RETIRED  
BLOCKED

---

## **32.2 Versioning**

Backward-compatible change:

새 low-risk route 추가  
optional metadata 추가  
approval timeout 보강  
description 보강  
audit requirement 보강  
network health requirement 추가  
AI trace metadata 추가  
snapshot\_ref 추가  
decision\_trace\_id 추가

Breaking change:

approval level 완화  
emergency bypass 조건 완화  
required evidence 제거  
required role 제거  
safety gate requirement 제거  
network health check 제거  
TOCTOU precheck 제거  
minimum time trust level 완화  
device health requirement 제거  
high-risk action route 변경  
fallback route 제거

Breaking change는 새 matrix version 또는 새 matrix로 분리하는 것이 원칙이다.

---

## **32.3 Approval Process**

Decision / Approval Matrix 변경은 다음 승인을 받아야 한다.

Policy Owner  
Safety Owner  
Domain Owner  
Ontology Steward  
Platform Architect

Emergency 관련 matrix는 다음 승인을 추가로 요구한다.

Audit Owner  
Legal / Compliance Owner  
External System Owner

---

# **33\. 핵심 시나리오**

## **33.1 시나리오 1: Gas Critical → Emergency Evacuation**

상황:

Zone\_A에서 gas critical threshold가 초과되었다.

입력:

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

결과:

EmergencyApprovedAction  
→ Safety Gate  
→ EmergencyExecutionRequest  
→ External Control System  
→ Feedback  
→ Post-hoc Audit

---

## **33.2 시나리오 2: Robot Mission Blocked → Supervisor Approval**

상황:

Robot\_07의 Mission\_991이 blocked 상태다.

입력:

event\_type \= robot.mission.blocked  
state \= MissionStatus.BLOCKED  
risk\_level \= WARNING  
action\_candidate \= ACTION\_DISABLE\_ROBOT\_MISSION  
evidence \= robot telemetry \+ fleet manager state

Decision:

decision\_route \= SUPERVISOR\_APPROVAL\_REQUIRED  
approval\_level\_required \= SUPERVISOR\_APPROVAL  
safety\_gate\_required \= true

결과:

ApprovalRequest  
→ Supervisor Approval  
→ ApprovedAction  
→ Safety Gate  
→ ExecutionRequest to FleetManager

---

## **33.3 시나리오 3: Stale Worker Location → Approval Hold**

상황:

WorkerLocationEvidence가 stale 상태다.

입력:

action\_candidate \= ACTION\_LOCK\_ZONE  
worker\_location\_state \= STALE  
risk\_level \= HIGH\_RISK

Decision:

decision\_route \= EVIDENCE\_REVIEW\_REQUIRED  
approval\_level\_required \= SAFETY\_MANAGER\_APPROVAL  
execution\_allowed \= false

결과:

Request fresh worker location evidence  
→ hold approval  
→ re-evaluate

---

## **33.4 시나리오 4: Evidence Conflict → Fail-Safe**

상황:

가스 센서 두 개가 충돌한다.

입력:

GasSensor\_A \= 87 ppm  
GasSensor\_B \= 0 ppm  
conflict\_status \= CONFLICT\_DETECTED  
risk\_level \= CRITICAL\_EMERGENCY

Decision:

decision\_route \= FAIL\_SAFE\_REQUIRED  
approval\_level\_required \= EMERGENCY\_POLICY\_BYPASS  
post\_hoc\_audit\_required \= true

결과:

Fail-safe evaluation  
→ Emergency action candidate  
→ Safety Gate  
→ EmergencyExecutionRequest

---

## **33.5 시나리오 5: LLM Proposed Action → Evidence Check**

상황:

LLM이 ACTION\_STOP\_WORK를 제안했다.

입력:

action\_candidate\_source \= AI\_DERIVED  
trust\_upgrade\_status \= NO\_UPGRADE  
evidence\_bundle \= missing  
risk\_level \= HIGH\_RISK

Decision:

decision\_route \= EVIDENCE\_REVIEW\_REQUIRED  
approval\_level\_required \= SAFETY\_MANAGER\_APPROVAL  
execution\_allowed \= false

결과:

LLM proposal stored as ActionCandidate  
→ request evidence grounding  
→ no approval until evidence bundle exists

---

## **33.6 시나리오 6: Approval Valid But TOCTOU State Changed**

상황:

Supervisor가 ACTION\_LOCK\_ZONE을 승인했다.  
하지만 승인 이후 Worker\_17이 Zone\_A에 진입했다.

입력:

approval\_status \= APPROVED  
state\_snapshot\_ref\_at\_approval \= no worker in Zone\_A  
state\_snapshot\_ref\_at\_execution \= Worker\_17 in Zone\_A  
risk\_level \= HIGH\_RISK

SafetyGatePrecheck:

TOCTOU\_state\_delta\_check \= HIGH\_RISK\_DELTA

Decision:

decision\_route \= TOCTOU\_REVALIDATION\_REQUIRED  
execution\_allowed \= false

결과:

Hold ExecutionRequest  
→ request fresh approval or emergency evaluation

---

## **33.7 시나리오 7: Network Latency Exceeded**

상황:

Robot mission disable은 승인되었지만 FleetManager heartbeat가 끊겼다.

입력:

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

결과:

Do not send ExecutionRequest  
→ escalate or use local fail-safe policy

---

# **34\. MVP Decision / Approval Matrix Set**

MVP에서는 범위를 줄여 다음 3개를 먼저 구현한다.

Safety Decision Matrix  
Evidence Conflict Matrix  
Emergency Fast-Path Matrix

이 3개를 먼저 구현하는 이유는 다음이다.

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

# **35\. 권장 파일 구조**

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

# **36\. 우선 구현 순서**

MVP 구현 순서는 다음이 좋다.

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

PolicyEngineAdapter와 DummyPDP는 DecisionRouter보다 먼저 정의하는 것이 좋다.

이유:

DecisionRouter integration test requires predictable PDP response.

---

# **37\. 최종 원칙**

Decision / Approval Matrix는 플랫폼의 판단 및 승인 언어다.

Event는 사건을 말한다.  
State는 현재 상태를 말한다.  
Evidence는 판단 근거를 말한다.  
ActionCandidate는 제안을 말한다.  
Decision은 판단 경로를 말한다.  
Approval은 권한 부여를 말한다.  
Safety Gate는 실행 가능성 검증을 말한다.  
ExecutionRequest는 외부 시스템에 대한 실행 요청을 말한다.

LLM은 ActionCandidate를 제안할 수 있다.  
LLM은 Decision을 단독으로 확정할 수 없다.  
LLM은 Approval을 할 수 없다.  
LLM은 ExecutionRequest를 만들 수 없다.

High-risk action은 evidence bundle 없이 승인되면 안 된다.  
Stale state 기반으로 high-risk action을 승인하면 안 된다.  
Low time trust evidence로 high-risk action을 승인하면 안 된다.  
Device health가 degraded된 evidence는 decision route를 상향시켜야 한다.  
Conflict가 unresolved이면 route를 상향해야 한다.  
Emergency fast-path는 사전 정책과 최소 verified operational evidence를 요구한다.  
ATTESTED\_AI\_DERIVED evidence는 emergency context를 보조할 수 있지만, 단독 emergency trigger가 될 수 없다.  
Emergency bypass는 post-hoc audit을 반드시 요구한다.  
Approval이 있어도 Safety Gate를 통과하지 못하면 ExecutionRequest를 만들 수 없다.  
Approval이 유효해도 실행 직전 world state가 바뀌면 TOCTOU revalidation이 필요하다.  
External adapter가 살아 있어도 heartbeat와 network latency가 기준을 넘으면 실행하면 안 된다.  
물리 실행 요청은 idempotency\_key로 중복 실행을 방지해야 한다.  
AI-derived decision support는 model version, prompt, retrieval snapshot, ontology mapping snapshot을 감사 가능하게 남겨야 한다.  
DecisionCase는 과도하게 무거워지지 않도록 DecisionContext와 snapshot\_ref로 분리한다.  
DecisionCase → ApprovalRequest → ApprovalDecision → ExecutionRequest → Feedback → AuditRecord는 decision\_trace\_id로 연결되어야 한다.  
Fallback route는 safety-first priority를 따라야 한다.

최종 원칙은 다음과 같다.

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

