**TOCTOU** 

**1\. Purpose**

This document defines `TOCTOU Validation` within the LEDO Runtime Validation area.

TOCTOU stands for **Time-of-Check to Time-of-Use**.

In LEDO, TOCTOU refers to the risk that the physical site condition may change between the time an action is approved and the time it is actually executed.

Approval-time condition

    ≠

Execution-time condition

A condition that was safe at approval time may no longer be safe immediately before execution.

Therefore, in LEDO, an `ApprovedAction` must not automatically create an `ExecutionRequest` until it passes Runtime Validation and the Safety Gate.

---

## **2\. Core Definition**

TOCTOU Validation is a runtime validation procedure that verifies whether the state, snapshot, evidence, policy, and approval context used at approval time are still valid at execution time.

TOCTOU Validation

\= a procedure that validates the risk of state change

  between approval time and execution time

The core question of TOCTOU Validation is:

Are the conditions that were safe at approval time

still safe at the current execution time?

TOCTOU Validation is not merely a check for whether approval exists.

TOCTOU Validation checks whether the physical and operational conditions have changed between approval and execution.

---

## **3\. Why TOCTOU Matters**

LEDO is a Cyber-Physical System.

Therefore, there is always a time gap between digital decision and physical execution.

During this time gap, the following may change:

worker location

robot status

equipment status

zone status

hazard condition

external system health

adapter health

policy version

approval validity

capability availability

environmental condition

network availability

clock synchronization state

Example:

Approval time:

    worker is not in robot path

    zone is accessible

    robot is available

Execution time:

    worker enters robot path

    zone becomes restricted

    robot battery becomes low

In this case, execution must be blocked even if approval exists.

---

## **4\. Responsibility Boundary**

TOCTOU Validation is separate from Approval, Runtime Validation, Safety Gate, and ExecutionRequest.

Approval

    → grants authority.

TOCTOU Validation

    → validates whether conditions changed between approval time and execution time.

Runtime Validation

    → validates the overall execution-time condition.

Safety Gate

    → makes the final pass/block decision based on Runtime Validation results.

ExecutionRequest

    → is bounded execution intent sent to an external system after Safety Gate pass.

External System

    → performs actual physical execution.

TOCTOU Validation does not create:

Approval

ApprovedAction

SafetyGatePass

ExecutionRequest

ExternalControlRequest

PhysicalCommand

TOCTOU Validation only creates execution-time condition validation results.

---

## **5\. TOCTOU Risk Sources**

TOCTOU risks may arise from the following sources:

state changes after approval

snapshot becomes stale

evidence becomes outdated

approval expires

policy version changes

external system becomes unreachable

adapter becomes unhealthy

robot capability changes

worker enters hazard zone

worker enters robot path

zone status changes

hazard condition escalates

network delay causes late execution

duplicate request is replayed

old SafetyGatePass is reused

old ExecutionRequest is retried

clock drift causes incorrect freshness judgment

system clock moves backward

SafetyGatePass arrives after lease expiry

If any of these affects a safety-critical action, Runtime Validation must return block or manual review.

---

## **6\. Required Validation Inputs**

TOCTOU Validation may consume the following inputs depending on action type:

ApprovedAction

ApprovalRecord

Approval-time Snapshot

Execution-time State

Execution-time Snapshot

EvidenceBundle

PolicyEvaluationResult

PolicyVersion

StateFreshnessResult

SnapshotFreshnessResult

ExternalSystemHealth

AdapterHealth

CapabilityStatus

SafetyGatePassLease

IdempotencyKey

TraceContext

CorrelationId

If a required input is missing, the safety-critical execution path must be blocked.

missing required runtime input

    → block

---

## **7\. Snapshot Comparison Rule**

TOCTOU Validation must compare the approval-time snapshot and the execution-time snapshot.

approval\_snapshot

    vs

execution\_snapshot

Validation targets include:

same target entity

same action scope

same site

same zone

same actor

same robot or equipment

state age within max\_age

no critical field changed

no safety-critical conflict detected

If a safety-critical field has changed, the existing approval must not be reused as-is.

critical field changed

    → block or require re-approval

Example:

approval\_snapshot.worker\_in\_robot\_path \= false

execution\_snapshot.worker\_in\_robot\_path \= true

    → block

---

## **8\. Freshness Rule**

TOCTOU Validation must verify that execution-time state and snapshot are fresh.

Freshness requirements are defined in a registry or runtime validation rule.

Examples:

worker\_location\_state.max\_age\_seconds \= 10

robot\_status\_state.max\_age\_seconds \= 15

zone\_status\_state.max\_age\_seconds \= 20

external\_system\_health\_state.max\_age\_seconds \= 20

adapter\_health\_state.max\_age\_seconds \= 20

Basic validation rule:

current\_time \- observed\_at \<= max\_age\_seconds

Failure handling:

stale\_state

    → block

stale\_snapshot

    → block

unknown\_observed\_at

    → block

In safety-critical paths, stale data must not be treated as allow.

---

## **9\. Clock Synchronization and Clock Skew Tolerance**

Freshness Rule is based on timestamp comparison.

However, if the clocks of the LEDO Core Server, Adapter, Edge Device, Robot, and External System drift, freshness judgment may become incorrect.

clock drift

    → incorrect freshness judgment

Examples:

adapter clock is 5 seconds ahead

    → future timestamp may occur

adapter clock is 5 seconds behind

    → stale data may appear fresh

Therefore, the LEDO runtime environment must assume clock synchronization as an infrastructure requirement.

Recommended infrastructure prerequisites:

PTP / IEEE 1588 for high-precision industrial environments

NTP as minimum baseline synchronization

monotonic clock for local duration measurement

UTC timestamp for cross-system event time

A source whose clock synchronization cannot be trusted must not be trusted in a safety-critical path.

untrusted clock source

    → block or degraded trust

Freshness calculation must include clock skew tolerance.

Example:

clock\_skew\_tolerance\_ms \= 500

Validation rules:

if observed\_at \> current\_time \+ clock\_skew\_tolerance:

    block

if current\_time \- observed\_at \> max\_age\_seconds \+ clock\_skew\_tolerance:

    block

Future timestamps must not be allowed.

future timestamp beyond tolerance

    → block

Abnormally old timestamps must not be allowed either.

abnormally old timestamp

    → block

---

## **10\. Monotonic Clock Convention**

Runtime duration calculations must use a monotonic clock.

UTC wall-clock timestamps may be used for audit, ordering, and cross-system event records.

However, the following calculations must be based on monotonic time, not wall-clock time:

timeout

lease age

retry interval

elapsed duration

SafetyGatePass lease duration

adapter response duration

external system response timeout

Distinction:

Wall Clock / UTC Time

    → observed\_at

    → received\_at

    → issued\_at

    → expires\_at

    → audit timestamp

    → cross-system event record

Monotonic Clock

    → elapsed\_ms

    → lease\_age\_ms

    → timeout\_ms

    → retry\_interval\_ms

    → local duration measurement

Core rule:

System clock adjustment must not make a SafetyGatePass appear younger, fresher, or still valid.

---

## **11\. Timestamp Trust Fields**

Runtime Validation input must include metadata that can be used to determine timestamp trust.

observed\_at

received\_at

source\_clock\_id

source\_clock\_sync\_status

clock\_skew\_estimate\_ms

clock\_skew\_tolerance\_ms

time\_source

monotonic\_sequence\_id

Recommended time sources:

PTP

NTP

GPS time

trusted gateway timestamp

core ingestion timestamp

monotonic local timer

---

## **12\. Condition Change Rule**

TOCTOU Validation checks whether execution conditions changed after approval.

Examples of validation targets:

worker entered robot path

worker entered hazard zone

zone changed from accessible to restricted

hazard severity increased

robot changed from available to unavailable

external system changed from healthy to unreachable

adapter changed from healthy to degraded

approval expired

policy version changed

capability became unavailable

Failure handling:

condition\_changed

    → block

condition\_changed\_but\_non\_critical

    → warning or revalidation

condition\_unknown

    → block

---

## **13\. Approval Validity Rule**

TOCTOU Validation must verify whether the approval is still valid at execution time.

Validation targets:

approval\_id exists

approval status is active

approval scope matches action

approval target matches execution target

approval has not expired

approver identity is still valid

approval was not revoked

approval policy version is still compatible

Failure handling:

expired\_approval

    → block

revoked\_approval

    → block

scope\_mismatch

    → block

approver\_invalid

    → block

Approval grants authority, but it cannot be used in the execution path if its expiry or scope is no longer valid.

---

## **14\. Policy Revalidation Rule**

TOCTOU Validation must verify whether the policy is still valid at execution time.

Validation targets:

policy exists

policy is active

policy version is compatible

policy scope still matches action

policy conditions still hold

policy has not been superseded

emergency override condition still valid if used

Failure handling:

policy\_inactive

    → block

policy\_version\_mismatch

    → block or re-evaluate

policy\_condition\_failed

    → block

emergency\_condition\_expired

    → block

Policy pass is not Approval pass, and Approval pass is not Safety Gate pass.

---

## **15\. External System and Adapter Rule**

TOCTOU Validation must verify whether the external system and adapter are still usable at execution time.

Validation targets:

external system registered

external system active

external system reachable

external system health fresh

adapter registered

adapter active

adapter health fresh

protocol compatible

expected feedback channel available

Failure handling:

external\_system\_unreachable

    → block

adapter\_unhealthy

    → block

feedback\_channel\_unavailable

    → block or hold

Important boundary:

external system reachable

    ≠

safe to execute

Network health is only an input to TOCTOU Validation and does not automatically imply Safety Gate pass.

---

## **16\. Validation Criticality Tier**

If every freshness failure always results in block, safety increases but availability may decrease significantly.

Therefore, Runtime Validation must classify data and validation rules by criticality tier.

Core principle:

Safety-critical stale data

    → block

Operational stale data

    → hold / retry / soft revalidation

Informational stale data

    → warning / degraded mode

### **Tier 1\. Safety-Critical**

Data directly related to human safety, hazards, emergencies, robot paths, or restricted zones.

Examples:

worker\_location\_state

hazard\_zone\_state

emergency\_stop\_state

restricted\_zone\_state

robot\_path\_clearance\_state

human\_presence\_state

Handling rules:

stale

    → block

unknown

    → block

conflict

    → block or manual review

### **Tier 2\. Operational-Critical**

Data important for operations but not directly tied to human safety.

Examples:

robot\_battery\_level

robot\_mission\_queue

adapter\_latency\_metric

fleet\_manager\_load

equipment\_utilization\_state

Handling rules:

stale

    → soft revalidation / retry / hold

unknown

    → hold or degraded mode

conflict

    → retry or manual review

However, Tier 2 data may be promoted to Tier 1 if it becomes a safety-critical dependency for a specific action.

### **Tier 3\. Informational**

Data used for operational reference, dashboards, KPIs, or historical trends.

Examples:

dashboard\_kpi

historical\_performance\_metric

non-critical telemetry

reporting\_metric

Handling rules:

stale

    → warning

unknown

    → warning

conflict

    → warning or exclude from decision

Tier 3 data must not be a required condition for Safety Gate pass.

### **Tier Escalation Rule**

The tier of data is not fixed and may be elevated depending on action context.

Example:

robot\_battery\_level

    normally → Tier 2

robot\_battery\_level during evacuation support mission

    → Tier 1

Rule:

if data affects human safety:

    tier \= Tier 1

---

## **17\. Idempotency Relation**

TOCTOU Validation is connected to idempotency.

In network delay, retry, replay, or timeout scenarios, the same request may be processed multiple times.

Important rules from the TOCTOU perspective:

replayed old approval

    → must not create new physical execution

replayed old safety gate pass

    → must be checked against current runtime condition

replayed old execution request

    → must be deduplicated or blocked

An approval, SafetyGatePass, or ExecutionRequest that was valid in the past must not be considered automatically valid now.

---

## **18\. Meta-TOCTOU and SafetyGatePass Lease**

TOCTOU risk does not exist only between Approval and Execution.

There is also a micro time window between the moment the Safety Gate issues a pass and the moment the External System receives the ExecutionRequest.

This window is defined as the **Meta-TOCTOU Window**.

SafetyGatePass issued time

    ≠

External System received time

Even immediately after SafetyGatePass issuance, the site condition may change.

Example:

SafetyGatePass issued:

    worker not in robot path

500ms later:

    worker enters robot path

External System receives request:

    old SafetyGatePass still attached

In this case, execution may be dangerous even though a SafetyGatePass exists.

---

## **19\. SafetyGatePass is a Lease**

SafetyGatePass is not permanent authority.

SafetyGatePass is a short-lived **execution-readiness lease**.

SafetyGatePass

    \= short-lived execution readiness lease

SafetyGatePass should contain the following fields:

safety\_gate\_pass\_id

approved\_action\_id

issued\_at

expires\_at

lease\_duration\_ms

lease\_started\_monotonic\_ms

lease\_expires\_monotonic\_ms

max\_dispatch\_latency\_ms

target\_external\_system

execution\_request\_id

idempotency\_key

trace\_id

consumed\_at

terminal\_status

---

## **20\. Lease Expiry Rule**

SafetyGatePass must not be used after `expires_at`.

if current\_time \> safety\_gate\_pass.expires\_at:

    block

    require runtime revalidation

Default policy:

expired SafetyGatePass

    → block

expired SafetyGatePass replay

    → block

expired SafetyGatePass attached to ExecutionRequest

    → drop or reject

SafetyGatePass not consumed within lease duration

    → require revalidation

Example lease duration:

safety\_gate\_pass.lease\_duration\_ms \= 500

or

safety\_gate\_pass.lease\_duration\_ms \= 1000

The actual value must be defined in a registry or runtime validation rule according to action criticality, network latency, site topology, and external system protocol.

---

## **21\. Lease Consumption Rule**

SafetyGatePass is not consumed only when execution succeeds.

SafetyGatePass must become terminal at the moment it is first observed by the Adapter or External System.

consume-on-first-observation

This means that the SafetyGatePass token ID must not remain reusable in the following cases:

accepted

rejected

dropped

expired

mismatched

blocked

timeout after first observation

Recommended states:

ISSUED

DISPATCHING

CONSUMED\_ACCEPTED

CONSUMED\_REJECTED

CONSUMED\_DROPPED

EXPIRED

REVOKED

Terminal states:

CONSUMED\_ACCEPTED

CONSUMED\_REJECTED

CONSUMED\_DROPPED

EXPIRED

REVOKED

Rules:

terminal SafetyGatePass

    → cannot be reused

failed delivery

    → must not revive SafetyGatePass

consumed SafetyGatePass replay

    → block

A SafetyGatePass must become terminal when it is first observed by the Adapter or External System.

Even if the request is dropped, rejected, expired, mismatched, or blocked, the SafetyGatePass token ID must not remain reusable.

A failed delivery must not revive a SafetyGatePass.

This rule prevents replay attacks, duplicate execution, and stale pass reuse.

---

## **22\. External System Drop Rule**

The External System or Adapter must drop or reject requests containing an expired SafetyGatePass.

External System receives ExecutionRequest

    ↓

check SafetyGatePass lease

    ↓

if expired:

    drop / reject / request revalidation

The External System must verify:

SafetyGatePass exists

SafetyGatePass target matches external system

SafetyGatePass not expired

SafetyGatePass idempotency key valid

SafetyGatePass trace\_id matches ExecutionRequest

SafetyGatePass not already terminal

---

## **23\. ApprovedAction Runtime State Transition**

When TOCTOU Validation returns blocked or requires\_reapproval, the lifecycle of the existing ApprovedAction must be clearly defined.

ApprovedAction is not executed merely because it has been approved.

ApprovedAction must pass Runtime Validation and Safety Gate.

Normal flow:

APPROVED

    ↓

RUNTIME\_VALIDATING

    ↓

RUNTIME\_VALIDATED

    ↓

SAFETY\_GATE\_PASSED

    ↓

EXECUTION\_REQUESTED

    ↓

EXTERNAL\_SYSTEM\_ACCEPTED

    ↓

COMPLETED

TOCTOU Validation failure flow:

APPROVED

    ↓

RUNTIME\_VALIDATING

    ↓

BLOCKED\_BY\_TOCTOU

Possible transitions after block:

BLOCKED\_BY\_TOCTOU

    → SUSPENDED

BLOCKED\_BY\_TOCTOU

    → REVALIDATION\_PENDING

BLOCKED\_BY\_TOCTOU

    → REAPPROVAL\_REQUIRED

BLOCKED\_BY\_TOCTOU

    → REVOKED

State meanings:

SUSPENDED

    → temporarily held.

      Revalidation is possible if conditions recover.

REVALIDATION\_PENDING

    → runtime condition must be checked again.

REAPPROVAL\_REQUIRED

    → existing approval is insufficient and new approval is required.

REVOKED

    → existing ApprovedAction is discarded.

      It cannot be reused.

BLOCKED\_BY\_TOCTOU

    → currently not executable due to TOCTOU risk.

Transition Rules:

If safety-critical condition changed:

    BLOCKED\_BY\_TOCTOU → REAPPROVAL\_REQUIRED or REVOKED

If data stale but recoverable:

    BLOCKED\_BY\_TOCTOU → REVALIDATION\_PENDING

If external system temporarily unreachable:

    BLOCKED\_BY\_TOCTOU → SUSPENDED or REVALIDATION\_PENDING

If approval expired:

    BLOCKED\_BY\_TOCTOU → REAPPROVAL\_REQUIRED

If target changed:

    BLOCKED\_BY\_TOCTOU → REVOKED

If duplicate execution detected:

    BLOCKED\_BY\_TOCTOU → SUSPENDED or REVOKED

Resume Rule:

SUSPENDED

    ↓

REVALIDATION\_PENDING

    ↓

RUNTIME\_VALIDATING

    ↓

RUNTIME\_VALIDATED

    ↓

SAFETY\_GATE\_PASSED

Therefore:

Resume requires revalidation.

Revocation Rule:

REVOKED ApprovedAction

    → cannot be resumed

    → cannot create ExecutionRequest

    → requires new approval flow

Final ApprovedAction rule:

ApprovedAction is not execution.

ApprovedAction is authority granted under a context.

If that context changes, the ApprovedAction must be revalidated, suspended, reapproved, or revoked.

---

## **24\. TOCTOU Validation Result**

TOCTOU Validation produces the following result:

TOCTOUValidationResult

    result\_id

    approved\_action\_id

    approval\_snapshot\_ref

    execution\_snapshot\_ref

    checked\_at

    status

    changed\_fields

    stale\_fields

    conflict\_fields

    block\_reasons

    warnings

    required\_reapproval

    safety\_gate\_eligible

    trace\_id

    audit\_ref

Possible statuses:

valid

invalid

stale

conflict

requires\_reapproval

manual\_review\_required

blocked

---

## **25\. Failure Effects**

TOCTOU Validation failure must not silently become allow.

unknown

    → block

stale

    → block

conflict

    → block or manual review

critical condition changed

    → block or require re-approval

approval expired

    → block

policy invalid

    → block

external system unavailable

    → block

expired SafetyGatePass

    → block

terminal SafetyGatePass replay

    → block

For safety-critical actions, the default failure effect must be block.

default failure effect \= block

---

## **26\. MVP Scenario: STOP\_WORK**

For STOP\_WORK, TOCTOU Validation checks:

hazard still present

hazard severity not downgraded incorrectly

worker location fresh

zone status fresh

approval still valid or emergency condition active

policy still valid

notification or site operation system reachable

same stop-work target zone

no duplicate stop-work execution

SafetyGatePass lease valid

SafetyGatePass not terminal

Flow:

ApprovedAction: STOP\_WORK

    ↓

Approval-time Snapshot Check

    ↓

Execution-time State / Snapshot Refresh

    ↓

TOCTOU Validation

    ↓

RuntimeValidationResult

    ↓

Safety Gate

    ↓

SafetyGatePass Lease

    ↓

ExecutionRequest or SafetyGateBlock

If STOP\_WORK is already active for the same target zone, duplicate execution must be prevented through the idempotency rule.

---

## **27\. MVP Scenario: DISPATCH\_ROBOT**

For DISPATCH\_ROBOT, TOCTOU Validation checks:

robot still available

worker not in robot path

zone still accessible

robot mission target unchanged

approval not expired

policy still valid

fleet manager reachable

adapter health valid

robot capability still available

no conflicting mission assigned

no duplicate dispatch request

SafetyGatePass lease valid

SafetyGatePass not terminal

Flow:

ApprovedAction: DISPATCH\_ROBOT

    ↓

Approval-time Snapshot Check

    ↓

Execution-time State / Snapshot Refresh

    ↓

TOCTOU Validation

    ↓

RuntimeValidationResult

    ↓

Safety Gate

    ↓

SafetyGatePass Lease

    ↓

ExecutionRequest or SafetyGateBlock

Important principle:

LEDO does not send low-level robot motion command.

LEDO sends approved mission intent to external fleet manager.

If a worker newly enters the robot path, execution must be blocked even if approval exists.

---

## **28\. Audit Requirement**

TOCTOU Validation must be auditable.

Audit targets:

approved\_action\_id

approval\_snapshot\_ref

execution\_snapshot\_ref

checked\_at

state\_versions\_used

snapshot\_versions\_used

policy\_version\_used

approval\_record\_used

changed\_fields

failure\_reasons

decision outcome

trace\_id

correlation\_id

validator\_id

SafetyGatePass id

SafetyGatePass lease status

SafetyGatePass terminal status

clock\_skew\_estimate\_ms

time\_source

If TOCTOU Validation returns block, the block reason must be traceable.

If a SafetyGatePass is consumed, rejected, dropped, expired, or revoked, an audit record must be preserved.

---

## **29\. Final TOCTOU Rule**

Approval-time validity

does not guarantee

execution-time validity.

Final rules:

No fresh execution-time state,

no Safety Gate pass.

No valid execution-time snapshot,

no Safety Gate pass.

No TOCTOU validation,

no ExecutionRequest.

No valid SafetyGatePass lease,

no valid ExecutionRequest.

No Safety Gate pass,

no external execution.

No audit,

no trust.

TOCTOU Validation is a core runtime safety mechanism that prevents LEDO from requesting physical execution based on old approval, old snapshot, stale state, changed site conditions, expired approval, invalid policy, clock drift, replayed SafetyGatePass, or expired lease.

# 

# **TOCTOU** 

# **1\. Purpose**

이 문서는 LEDO Runtime Validation 영역에서 `TOCTOU Validation`을 정의한다.

TOCTOU는 **Time-of-Check to Time-of-Use**의 약자이다.

LEDO에서 TOCTOU는 어떤 action이 승인된 시점과 실제 실행되는 시점 사이에 현장 상태가 바뀌는 위험을 의미한다.

Approval-time condition  
    ≠  
Execution-time condition

즉, 승인 시점에는 안전했던 조건이 실행 직전에는 더 이상 안전하지 않을 수 있다.

따라서 LEDO에서는 `ApprovedAction`이 존재하더라도 Runtime Validation과 Safety Gate를 통과하기 전까지 `ExecutionRequest`를 생성하면 안 된다.

---

## **2\. Core Definition**

TOCTOU Validation은 승인 시점에 사용된 state, snapshot, evidence, policy, approval context가 실행 시점에도 여전히 유효한지 검증하는 runtime validation 절차이다.

TOCTOU Validation  
\= 승인 시점과 실행 시점 사이의 상태 변화 위험을 검증하는 절차

TOCTOU Validation의 핵심 질문은 다음이다.

승인 당시 안전했던 조건이  
지금 실행 시점에도 여전히 안전한가?

TOCTOU Validation은 단순히 “승인이 있는가?”를 확인하는 절차가 아니다.

TOCTOU Validation은 “승인 이후 실행 직전까지 현장 조건이 바뀌지 않았는가?”를 확인하는 절차이다.

---

## **3\. Why TOCTOU Matters**

LEDO는 Cyber-Physical System이다.

따라서 digital decision과 physical execution 사이에는 시간 차이가 존재한다.

이 시간 차이 동안 다음이 바뀔 수 있다.

worker location  
robot status  
equipment status  
zone status  
hazard condition  
external system health  
adapter health  
policy version  
approval validity  
capability availability  
environmental condition  
network availability  
clock synchronization state

예시:

Approval time:  
    worker is not in robot path  
    zone is accessible  
    robot is available

Execution time:  
    worker enters robot path  
    zone becomes restricted  
    robot battery becomes low

이 경우 approval이 존재하더라도 실행은 막혀야 한다.

---

## **4\. Responsibility Boundary**

TOCTOU Validation은 Approval, Runtime Validation, Safety Gate, ExecutionRequest와 구분된다.

Approval  
    → 권한을 부여한다.

TOCTOU Validation  
    → 승인 시점과 실행 시점 사이의 조건 변화 여부를 검증한다.

Runtime Validation  
    → 실행 시점의 전체 조건 유효성을 검증한다.

Safety Gate  
    → Runtime Validation 결과를 기반으로 최종 pass/block을 결정한다.

ExecutionRequest  
    → Safety Gate pass 이후 외부 시스템에 전달되는 bounded execution intent이다.

External System  
    → 실제 물리 실행을 수행한다.

TOCTOU Validation은 다음을 생성하지 않는다.

Approval  
ApprovedAction  
SafetyGatePass  
ExecutionRequest  
ExternalControlRequest  
PhysicalCommand

TOCTOU Validation은 오직 실행 시점 조건 검증 결과를 생성한다.

---

## **5\. TOCTOU Risk Sources**

TOCTOU 위험은 다음 원인에서 발생한다.

state changes after approval  
snapshot becomes stale  
evidence becomes outdated  
approval expires  
policy version changes  
external system becomes unreachable  
adapter becomes unhealthy  
robot capability changes  
worker enters hazard zone  
worker enters robot path  
zone status changes  
hazard condition escalates  
network delay causes late execution  
duplicate request is replayed  
old SafetyGatePass is reused  
old ExecutionRequest is retried  
clock drift causes incorrect freshness judgment  
system clock moves backward  
SafetyGatePass arrives after lease expiry

이 중 하나라도 safety-critical action에 영향을 주면 Runtime Validation은 block 또는 manual review를 반환해야 한다.

---

## **6\. Required Validation Inputs**

TOCTOU Validation은 action type에 따라 다음 입력을 사용할 수 있다.

ApprovedAction  
ApprovalRecord  
Approval-time Snapshot  
Execution-time State  
Execution-time Snapshot  
EvidenceBundle  
PolicyEvaluationResult  
PolicyVersion  
StateFreshnessResult  
SnapshotFreshnessResult  
ExternalSystemHealth  
AdapterHealth  
CapabilityStatus  
SafetyGatePassLease  
IdempotencyKey  
TraceContext  
CorrelationId

필수 입력이 누락되면 safety-critical execution path는 block되어야 한다.

missing required runtime input  
    → block

---

## **7\. Snapshot Comparison Rule**

TOCTOU Validation은 approval-time snapshot과 execution-time snapshot의 차이를 검증해야 한다.

approval\_snapshot  
    vs  
execution\_snapshot

검증 대상은 다음이다.

same target entity  
same action scope  
same site  
same zone  
same actor  
same robot or equipment  
state age within max\_age  
no critical field changed  
no safety-critical conflict detected

만약 safety-critical field가 변경되었다면 기존 approval을 그대로 사용할 수 없다.

critical field changed  
    → block or require re-approval

예시:

approval\_snapshot.worker\_in\_robot\_path \= false  
execution\_snapshot.worker\_in\_robot\_path \= true  
    → block

---

## **8\. Freshness Rule**

TOCTOU Validation은 실행 시점의 state와 snapshot이 fresh한지 검증해야 한다.

Freshness 기준은 registry 또는 runtime validation rule에서 정의한다.

예시:

worker\_location\_state.max\_age\_seconds \= 10  
robot\_status\_state.max\_age\_seconds \= 15  
zone\_status\_state.max\_age\_seconds \= 20  
external\_system\_health\_state.max\_age\_seconds \= 20  
adapter\_health\_state.max\_age\_seconds \= 20

기본 검증 규칙:

current\_time \- observed\_at \<= max\_age\_seconds

실패 처리:

stale\_state  
    → block

stale\_snapshot  
    → block

unknown\_observed\_at  
    → block

Safety-critical path에서는 stale data를 allow로 취급하면 안 된다.

---

## **9\. Clock Synchronization and Clock Skew Tolerance**

Freshness Rule은 timestamp 비교를 기반으로 한다.

그러나 LEDO Core Server, Adapter, Edge Device, Robot, External System 간 시계가 어긋나면 freshness 판단이 잘못될 수 있다.

clock drift  
    → incorrect freshness judgment

예시:

adapter clock is 5 seconds ahead  
    → future timestamp 발생 가능

adapter clock is 5 seconds behind  
    → stale data가 fresh하게 보일 수 있음

따라서 LEDO runtime environment는 clock synchronization을 전제로 해야 한다.

권장 인프라 전제:

PTP / IEEE 1588 for high-precision industrial environments  
NTP as minimum baseline synchronization  
monotonic clock for local duration measurement  
UTC timestamp for cross-system event time

시계 동기화가 보장되지 않는 source는 safety-critical path에서 신뢰하면 안 된다.

untrusted clock source  
    → block or degraded trust

Freshness 계산에는 clock skew tolerance를 반영해야 한다.

예시:

clock\_skew\_tolerance\_ms \= 500

검증 규칙:

if observed\_at \> current\_time \+ clock\_skew\_tolerance:  
    block

if current\_time \- observed\_at \> max\_age\_seconds \+ clock\_skew\_tolerance:  
    block

미래 timestamp는 허용하면 안 된다.

future timestamp beyond tolerance  
    → block

비정상적으로 오래된 timestamp도 허용하면 안 된다.

abnormally old timestamp  
    → block

---

## **10\. Monotonic Clock Convention**

Runtime duration 계산은 반드시 monotonic clock을 사용해야 한다.

UTC wall-clock timestamp는 audit, ordering, cross-system event record에 사용할 수 있다.

하지만 다음 계산은 wall-clock이 아니라 monotonic time을 기준으로 해야 한다.

timeout  
lease age  
retry interval  
elapsed duration  
SafetyGatePass lease duration  
adapter response duration  
external system response timeout

구분:

Wall Clock / UTC Time  
    → observed\_at  
    → received\_at  
    → issued\_at  
    → expires\_at  
    → audit timestamp  
    → cross-system event record

Monotonic Clock  
    → elapsed\_ms  
    → lease\_age\_ms  
    → timeout\_ms  
    → retry\_interval\_ms  
    → local duration measurement

핵심 규칙:

System clock adjustment must not make a SafetyGatePass appear younger, fresher, or still valid.

한글 기준:

시스템 시계 조정으로 인해 SafetyGatePass가 더 젊거나,  
더 fresh하거나,  
아직 유효한 것처럼 보이면 안 된다.

---

## **11\. Timestamp Trust Fields**

Runtime Validation input에는 timestamp trust를 판단할 수 있는 metadata가 포함되어야 한다.

observed\_at  
received\_at  
source\_clock\_id  
source\_clock\_sync\_status  
clock\_skew\_estimate\_ms  
clock\_skew\_tolerance\_ms  
time\_source  
monotonic\_sequence\_id

권장 time source:

PTP  
NTP  
GPS time  
trusted gateway timestamp  
core ingestion timestamp  
monotonic local timer

---

## **12\. Condition Change Rule**

TOCTOU Validation은 승인 이후 실행 조건이 바뀌었는지 검증한다.

검증 대상 예시:

worker entered robot path  
worker entered hazard zone  
zone changed from accessible to restricted  
hazard severity increased  
robot changed from available to unavailable  
external system changed from healthy to unreachable  
adapter changed from healthy to degraded  
approval expired  
policy version changed  
capability became unavailable

실패 처리:

condition\_changed  
    → block

condition\_changed\_but\_non\_critical  
    → warning or revalidation

condition\_unknown  
    → block

---

## **13\. Approval Validity Rule**

TOCTOU Validation은 approval이 실행 시점에도 유효한지 검증해야 한다.

검증 대상:

approval\_id exists  
approval status is active  
approval scope matches action  
approval target matches execution target  
approval has not expired  
approver identity is still valid  
approval was not revoked  
approval policy version is still compatible

실패 처리:

expired\_approval  
    → block

revoked\_approval  
    → block

scope\_mismatch  
    → block

approver\_invalid  
    → block

Approval은 권한을 부여하지만, 유효기간과 scope를 벗어나면 execution path에서 사용할 수 없다.

---

## **14\. Policy Revalidation Rule**

TOCTOU Validation은 policy가 실행 시점에도 유효한지 확인해야 한다.

검증 대상:

policy exists  
policy is active  
policy version is compatible  
policy scope still matches action  
policy conditions still hold  
policy has not been superseded  
emergency override condition still valid if used

실패 처리:

policy\_inactive  
    → block

policy\_version\_mismatch  
    → block or re-evaluate

policy\_condition\_failed  
    → block

emergency\_condition\_expired  
    → block

Policy pass는 Approval pass가 아니며, Approval pass는 Safety Gate pass가 아니다.

---

## **15\. External System and Adapter Rule**

TOCTOU Validation은 실행 시점에 외부 시스템과 adapter가 여전히 사용할 수 있는지 확인해야 한다.

검증 대상:

external system registered  
external system active  
external system reachable  
external system health fresh  
adapter registered  
adapter active  
adapter health fresh  
protocol compatible  
expected feedback channel available

실패 처리:

external\_system\_unreachable  
    → block

adapter\_unhealthy  
    → block

feedback\_channel\_unavailable  
    → block or hold

중요한 경계:

external system reachable  
    ≠  
safe to execute

Network health는 TOCTOU Validation의 입력일 뿐이며 Safety Gate pass를 자동으로 의미하지 않는다.

---

## **16\. Validation Criticality Tier**

모든 freshness 실패를 무조건 block으로 처리하면 safety는 강화되지만 availability가 크게 떨어질 수 있다.

따라서 Runtime Validation은 data와 validation rule을 criticality tier로 분류해야 한다.

핵심 원칙:

Safety-critical stale data  
    → block

Operational stale data  
    → hold / retry / soft revalidation

Informational stale data  
    → warning / degraded mode

### **Tier 1\. Safety-Critical**

사람 안전, hazard, emergency, robot path, restricted zone과 직접 연결되는 데이터이다.

예시:

worker\_location\_state  
hazard\_zone\_state  
emergency\_stop\_state  
restricted\_zone\_state  
robot\_path\_clearance\_state  
human\_presence\_state

처리 규칙:

stale  
    → block

unknown  
    → block

conflict  
    → block or manual review

### **Tier 2\. Operational-Critical**

운영 수행에 중요하지만 사람 안전과 직접 연결되지 않는 데이터이다.

예시:

robot\_battery\_level  
robot\_mission\_queue  
adapter\_latency\_metric  
fleet\_manager\_load  
equipment\_utilization\_state

처리 규칙:

stale  
    → soft revalidation / retry / hold

unknown  
    → hold or degraded mode

conflict  
    → retry or manual review

단, Tier 2 데이터라도 특정 action에서 safety-critical dependency로 사용되면 Tier 1로 승격될 수 있다.

### **Tier 3\. Informational**

운영 참고, dashboard, KPI, historical trend에 사용되는 데이터이다.

예시:

dashboard\_kpi  
historical\_performance\_metric  
non-critical telemetry  
reporting\_metric

처리 규칙:

stale  
    → warning

unknown  
    → warning

conflict  
    → warning or exclude from decision

Tier 3 데이터는 Safety Gate pass의 필수 조건이 되어서는 안 된다.

### **Tier Escalation Rule**

데이터의 tier는 고정이 아니라 action context에 따라 상승할 수 있다.

예시:

robot\_battery\_level  
    normally → Tier 2

robot\_battery\_level during evacuation support mission  
    → Tier 1

규칙:

if data affects human safety:  
    tier \= Tier 1

---

## **17\. Idempotency Relation**

TOCTOU Validation은 idempotency와 연결된다.

네트워크 지연, retry, replay, timeout 상황에서는 같은 request가 여러 번 처리될 수 있다.

TOCTOU 관점에서 중요한 규칙은 다음이다.

replayed old approval  
    → must not create new physical execution

replayed old safety gate pass  
    → must be checked against current runtime condition

replayed old execution request  
    → must be deduplicated or blocked

즉, 과거에 유효했던 approval, SafetyGatePass, ExecutionRequest가 현재도 자동으로 유효하다고 보면 안 된다.

---

## **18\. Meta-TOCTOU and SafetyGatePass Lease**

TOCTOU 위험은 Approval과 Execution 사이에만 존재하지 않는다.

Safety Gate가 pass를 발급한 직후부터 External System이 ExecutionRequest를 수신하기 전까지도 미세한 시간창이 존재한다.

이 시간창을 **Meta-TOCTOU Window**라고 정의한다.

SafetyGatePass issued time  
    ≠  
External System received time

즉, SafetyGatePass가 발급된 직후에도 현장 상태는 변할 수 있다.

예시:

SafetyGatePass issued:  
    worker not in robot path

500ms later:  
    worker enters robot path

External System receives request:  
    old SafetyGatePass still attached

이 경우 SafetyGatePass가 존재하더라도 실행은 위험할 수 있다.

---

## **19\. SafetyGatePass is a Lease**

SafetyGatePass는 영구 권한이 아니다.

SafetyGatePass는 아주 짧은 유효기간을 가진 **execution-readiness lease**이다.

SafetyGatePass  
    \= short-lived execution readiness lease

SafetyGatePass는 다음 필드를 가져야 한다.

safety\_gate\_pass\_id  
approved\_action\_id  
issued\_at  
expires\_at  
lease\_duration\_ms  
lease\_started\_monotonic\_ms  
lease\_expires\_monotonic\_ms  
max\_dispatch\_latency\_ms  
target\_external\_system  
execution\_request\_id  
idempotency\_key  
trace\_id  
consumed\_at  
terminal\_status

---

## **20\. Lease Expiry Rule**

SafetyGatePass는 `expires_at` 이후에는 사용할 수 없다.

if current\_time \> safety\_gate\_pass.expires\_at:  
    block  
    require runtime revalidation

기본 정책:

expired SafetyGatePass  
    → block

expired SafetyGatePass replay  
    → block

expired SafetyGatePass attached to ExecutionRequest  
    → drop or reject

SafetyGatePass not consumed within lease duration  
    → require revalidation

예시 lease duration:

safety\_gate\_pass.lease\_duration\_ms \= 500  
or  
safety\_gate\_pass.lease\_duration\_ms \= 1000

실제 값은 action criticality, network latency, site topology, external system protocol에 따라 registry 또는 runtime validation rule에서 정의한다.

---

## **21\. Lease Consumption Rule**

SafetyGatePass는 성공적으로 실행되었을 때만 consumed 되는 것이 아니다.

SafetyGatePass는 Adapter 또는 External System에서 최초로 관측되는 순간 terminal 상태로 전환되어야 한다.

consume-on-first-observation

즉, 다음 상황에서도 SafetyGatePass token ID는 재사용 가능 상태로 남아 있으면 안 된다.

accepted  
rejected  
dropped  
expired  
mismatched  
blocked  
timeout after first observation

권장 상태:

ISSUED  
DISPATCHING  
CONSUMED\_ACCEPTED  
CONSUMED\_REJECTED  
CONSUMED\_DROPPED  
EXPIRED  
REVOKED

Terminal states:

CONSUMED\_ACCEPTED  
CONSUMED\_REJECTED  
CONSUMED\_DROPPED  
EXPIRED  
REVOKED

규칙:

terminal SafetyGatePass  
    → cannot be reused

failed delivery  
    → must not revive SafetyGatePass

consumed SafetyGatePass replay  
    → block

한글 기준:

SafetyGatePass는 Adapter 또는 External System에서 최초로 관측되는 순간 terminal 상태로 전환되어야 한다.

요청이 drop, reject, expired, mismatch, block 되더라도 해당 SafetyGatePass token ID는 재사용 가능 상태로 남아 있으면 안 된다.

실패한 전송은 SafetyGatePass를 되살리지 않는다.

이 규칙은 replay attack, duplicate execution, stale pass reuse를 방지한다.

---

## **22\. External System Drop Rule**

External System 또는 Adapter는 expired SafetyGatePass가 포함된 request를 drop하거나 reject해야 한다.

External System receives ExecutionRequest  
    ↓  
check SafetyGatePass lease  
    ↓  
if expired:  
    drop / reject / request revalidation

External System은 다음을 확인해야 한다.

SafetyGatePass exists  
SafetyGatePass target matches external system  
SafetyGatePass not expired  
SafetyGatePass idempotency key valid  
SafetyGatePass trace\_id matches ExecutionRequest  
SafetyGatePass not already terminal

---

## **23\. ApprovedAction Runtime State Transition**

TOCTOU Validation이 blocked 또는 requires\_reapproval을 반환했을 때, 기존 ApprovedAction을 어떻게 처리할지 명확히 정의해야 한다.

ApprovedAction은 승인되었다고 해서 즉시 실행되는 객체가 아니다.

ApprovedAction은 Runtime Validation과 Safety Gate를 거쳐야 한다.

정상 흐름:

APPROVED  
    ↓  
RUNTIME\_VALIDATING  
    ↓  
RUNTIME\_VALIDATED  
    ↓  
SAFETY\_GATE\_PASSED  
    ↓  
EXECUTION\_REQUESTED  
    ↓  
EXTERNAL\_SYSTEM\_ACCEPTED  
    ↓  
COMPLETED

TOCTOU Validation 실패 흐름:

APPROVED  
    ↓  
RUNTIME\_VALIDATING  
    ↓  
BLOCKED\_BY\_TOCTOU

이후 상태 전이 선택지:

BLOCKED\_BY\_TOCTOU  
    → SUSPENDED

BLOCKED\_BY\_TOCTOU  
    → REVALIDATION\_PENDING

BLOCKED\_BY\_TOCTOU  
    → REAPPROVAL\_REQUIRED

BLOCKED\_BY\_TOCTOU  
    → REVOKED

상태 의미:

SUSPENDED  
    → 일시 보류 상태.  
      조건 회복 시 재검증 가능.

REVALIDATION\_PENDING  
    → runtime condition을 다시 확인해야 하는 상태.

REAPPROVAL\_REQUIRED  
    → 기존 approval로는 부족하며 재승인이 필요한 상태.

REVOKED  
    → 기존 ApprovedAction을 폐기한 상태.  
      재사용 불가.

BLOCKED\_BY\_TOCTOU  
    → TOCTOU 위험으로 인해 현재 실행 불가 상태.

Transition Rules:

If safety-critical condition changed:  
    BLOCKED\_BY\_TOCTOU → REAPPROVAL\_REQUIRED or REVOKED

If data stale but recoverable:  
    BLOCKED\_BY\_TOCTOU → REVALIDATION\_PENDING

If external system temporarily unreachable:  
    BLOCKED\_BY\_TOCTOU → SUSPENDED or REVALIDATION\_PENDING

If approval expired:  
    BLOCKED\_BY\_TOCTOU → REAPPROVAL\_REQUIRED

If target changed:  
    BLOCKED\_BY\_TOCTOU → REVOKED

If duplicate execution detected:  
    BLOCKED\_BY\_TOCTOU → SUSPENDED or REVOKED

Resume Rule:

SUSPENDED  
    ↓  
REVALIDATION\_PENDING  
    ↓  
RUNTIME\_VALIDATING  
    ↓  
RUNTIME\_VALIDATED  
    ↓  
SAFETY\_GATE\_PASSED

즉:

Resume requires revalidation.

Revocation Rule:

REVOKED ApprovedAction  
    → cannot be resumed  
    → cannot create ExecutionRequest  
    → requires new approval flow

ApprovedAction 최종 규칙:

ApprovedAction is not execution.  
ApprovedAction is authority granted under a context.  
If that context changes, the ApprovedAction must be revalidated, suspended, reapproved, or revoked.

한글 기준:

ApprovedAction은 실행이 아니다.  
ApprovedAction은 특정 조건 아래 부여된 권한이다.  
그 조건이 바뀌면 ApprovedAction은 재검증, 보류, 재승인, 또는 폐기되어야 한다.

---

## **24\. TOCTOU Validation Result**

TOCTOU Validation은 다음 결과를 생성한다.

TOCTOUValidationResult  
    result\_id  
    approved\_action\_id  
    approval\_snapshot\_ref  
    execution\_snapshot\_ref  
    checked\_at  
    status  
    changed\_fields  
    stale\_fields  
    conflict\_fields  
    block\_reasons  
    warnings  
    required\_reapproval  
    safety\_gate\_eligible  
    trace\_id  
    audit\_ref

가능한 status:

valid  
invalid  
stale  
conflict  
requires\_reapproval  
manual\_review\_required  
blocked

---

## **25\. Failure Effects**

TOCTOU Validation 실패는 조용히 allow가 되면 안 된다.

unknown  
    → block

stale  
    → block

conflict  
    → block or manual review

critical condition changed  
    → block or require re-approval

approval expired  
    → block

policy invalid  
    → block

external system unavailable  
    → block

expired SafetyGatePass  
    → block

terminal SafetyGatePass replay  
    → block

Safety-critical action에서는 기본값이 block이어야 한다.

default failure effect \= block

---

## **26\. MVP Scenario: STOP\_WORK**

STOP\_WORK에서 TOCTOU Validation은 다음을 확인한다.

hazard still present  
hazard severity not downgraded incorrectly  
worker location fresh  
zone status fresh  
approval still valid or emergency condition active  
policy still valid  
notification or site operation system reachable  
same stop-work target zone  
no duplicate stop-work execution  
SafetyGatePass lease valid  
SafetyGatePass not terminal

흐름:

ApprovedAction: STOP\_WORK  
    ↓  
Approval-time Snapshot Check  
    ↓  
Execution-time State / Snapshot Refresh  
    ↓  
TOCTOU Validation  
    ↓  
RuntimeValidationResult  
    ↓  
Safety Gate  
    ↓  
SafetyGatePass Lease  
    ↓  
ExecutionRequest or SafetyGateBlock

STOP\_WORK가 이미 같은 target zone에 대해 실행 중이라면 idempotency rule에 따라 중복 실행을 막아야 한다.

---

## **27\. MVP Scenario: DISPATCH\_ROBOT**

DISPATCH\_ROBOT에서 TOCTOU Validation은 다음을 확인한다.

robot still available  
worker not in robot path  
zone still accessible  
robot mission target unchanged  
approval not expired  
policy still valid  
fleet manager reachable  
adapter health valid  
robot capability still available  
no conflicting mission assigned  
no duplicate dispatch request  
SafetyGatePass lease valid  
SafetyGatePass not terminal

흐름:

ApprovedAction: DISPATCH\_ROBOT  
    ↓  
Approval-time Snapshot Check  
    ↓  
Execution-time State / Snapshot Refresh  
    ↓  
TOCTOU Validation  
    ↓  
RuntimeValidationResult  
    ↓  
Safety Gate  
    ↓  
SafetyGatePass Lease  
    ↓  
ExecutionRequest or SafetyGateBlock

중요한 원칙:

LEDO does not send low-level robot motion command.  
LEDO sends approved mission intent to external fleet manager.

Robot path에 worker가 새로 들어온 경우 approval이 있어도 실행은 block되어야 한다.

---

## **28\. Audit Requirement**

TOCTOU Validation은 반드시 audit 가능해야 한다.

Audit 대상:

approved\_action\_id  
approval\_snapshot\_ref  
execution\_snapshot\_ref  
checked\_at  
state\_versions\_used  
snapshot\_versions\_used  
policy\_version\_used  
approval\_record\_used  
changed\_fields  
failure\_reasons  
decision outcome  
trace\_id  
correlation\_id  
validator\_id  
SafetyGatePass id  
SafetyGatePass lease status  
SafetyGatePass terminal status  
clock\_skew\_estimate\_ms  
time\_source

TOCTOU Validation이 block을 반환한 경우, block reason은 반드시 추적 가능해야 한다.

SafetyGatePass가 consumed, rejected, dropped, expired, revoked 된 경우에도 반드시 audit record가 남아야 한다.

---

## **29\. Final TOCTOU Rule**

Approval-time validity  
does not guarantee  
execution-time validity.

한글 기준:

승인 시점의 유효성은  
실행 시점의 유효성을 보장하지 않는다.

최종 규칙:

No fresh execution-time state,  
no Safety Gate pass.

No valid execution-time snapshot,  
no Safety Gate pass.

No TOCTOU validation,  
no ExecutionRequest.

No valid SafetyGatePass lease,  
no valid ExecutionRequest.

No Safety Gate pass,  
no external execution.

No audit,  
no trust.

TOCTOU Validation은 LEDO가 오래된 승인, 오래된 snapshot, stale state, 바뀐 현장 조건, expired approval, invalid policy, clock drift, replayed SafetyGatePass, expired lease를 기반으로 물리 실행을 요청하지 않도록 막는 핵심 runtime safety mechanism이다.

