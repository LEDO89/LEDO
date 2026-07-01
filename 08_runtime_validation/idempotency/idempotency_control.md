# **Idempotency Control**

## **1\. Purpose**

This document defines the LEDO `08_runtime_validation/idempotency/` area.

`idempotency/` prevents duplicate physical execution caused by duplicate requests, retries, replays, network delays, timeouts, or reused SafetyGatePass tokens.

In LEDO, the same request may be observed more than once.

However, the same physical execution must not occur more than once.

same request  
    ≠  
repeated physical execution

Idempotency is required because Runtime Validation operates in a distributed cyber-physical environment where retries and duplicated delivery are normal failure modes.

---

## **2\. Core Definition**

Idempotency means that processing the same logical request more than once must produce the same safe outcome without creating duplicate physical execution.

Idempotency  
    \= repeated processing of the same logical request  
      must not create repeated physical execution

The core question of Idempotency Control is:

Has this action, SafetyGatePass, ExecutionRequest,  
or ExternalControlRequest already been processed?

If the answer is yes, LEDO must not create a new physical execution path.

---

## **3\. Architectural Position**

`idempotency/` sits inside `08_runtime_validation/`.

It operates between `ApprovedAction` and `ExecutionRequest`.

ApprovedAction  
    ↓  
Runtime Validation  
    ↓  
Idempotency Check  
    ↓  
RuntimeValidationResult  
    ↓  
Safety Gate  
    ↓  
SafetyGatePass or SafetyGateBlock  
    ↓  
ExecutionRequest

Idempotency does not replace Safety Gate.

Idempotency provides a runtime safety condition that Safety Gate must consume.

---

## **4\. Responsibility Boundary**

`idempotency/` is responsible for:

idempotency key definition  
idempotency ledger model  
duplicate request detection  
retry safety rule  
replay prevention  
SafetyGatePass terminal token rule  
previous result return rule  
external request deduplication  
audit linkage for duplicate handling

`idempotency/` does not:

create Approval  
create ApprovedAction  
create SafetyGatePass  
create ExecutionRequest directly  
create PhysicalCommand  
perform physical rollback  
control external systems directly  
decide Safety Gate pass/block alone

Idempotency only determines whether a request or token has already been processed or can safely proceed.

---

## **5\. Why Idempotency Is Needed**

Distributed systems often retry messages.

Cyber-physical systems must treat retry carefully because a retry can become repeated physical execution.

Example:

ExecutionRequest sent to Fleet Manager  
    ↓  
network timeout occurs  
    ↓  
LEDO retries the same request  
    ↓  
Fleet Manager receives both messages

Without idempotency, the same robot dispatch, stop-work request, lock-zone request, or external control request may be executed twice.

This is not acceptable in LEDO.

network retry  
    ≠  
new execution authority

---

## **6\. Idempotency Scope**

Idempotency applies to the following objects:

ApprovedAction  
RuntimeValidationResult  
SafetyGatePass  
ExecutionRequest  
ExternalControlRequest  
FeedbackEvent  
AuditRecord

It must prevent duplicate processing in the following situations:

duplicate ApprovedAction processing  
duplicate RuntimeValidationResult consumption  
duplicate SafetyGatePass use  
duplicate ExecutionRequest dispatch  
replayed ExternalControlRequest  
timeout retry  
old token reuse  
previously consumed SafetyGatePass replay

---

## **7\. Idempotency Key Model**

Every execution path must carry an `idempotency_key`.

Recommended key components:

idempotency\_key \=  
    action\_type  
    approved\_action\_id  
    target\_id  
    target\_zone  
    safety\_gate\_pass\_id  
    execution\_request\_id  
    target\_external\_system  
    trace\_id

The exact key structure may differ by action type, but it must uniquely identify the logical execution attempt.

Core rule:

same logical execution attempt  
    → same idempotency\_key

A retry must reuse the same idempotency key.

A new idempotency key must not be used to bypass Runtime Validation or Safety Gate.

---

## **8\. Idempotency Ledger**

`idempotency/` must maintain or read an Idempotency Ledger.

The ledger records whether a logical request has already been observed, accepted, rejected, completed, blocked, expired, or terminalized.

Recommended ledger fields:

IdempotencyLedgerEntry  
    idempotency\_key  
    action\_type  
    approved\_action\_id  
    safety\_gate\_pass\_id  
    execution\_request\_id  
    target\_external\_system  
    first\_seen\_at  
    last\_seen\_at  
    status  
    previous\_result\_ref  
    terminal\_token\_ref  
    trace\_id  
    audit\_ref

Recommended statuses:

new  
in\_progress  
completed  
blocked  
rejected  
expired  
terminal  
unknown

If the ledger already contains a terminal result, the same request must not create a new physical execution.

---

## **9\. SafetyGatePass Terminal Token Rule**

SafetyGatePass is not reusable.

A SafetyGatePass must become terminal when it is first observed by the Adapter or External System.

consume-on-first-observation

The following statuses are terminal:

CONSUMED\_ACCEPTED  
CONSUMED\_REJECTED  
CONSUMED\_DROPPED  
EXPIRED  
REVOKED

Terminal SafetyGatePass tokens cannot be reused.

terminal SafetyGatePass replay  
    → block

Even if the request was dropped, rejected, expired, mismatched, or blocked, the SafetyGatePass token ID must not remain reusable.

A failed delivery must not revive a SafetyGatePass.

---

## **10\. Replay Rule**

Replay means an old approval, SafetyGatePass, ExecutionRequest, or ExternalControlRequest is presented again.

Replay must not create new execution authority.

replayed old approval  
    → block or require revalidation

replayed old SafetyGatePass  
    → block if terminal or expired

replayed old ExecutionRequest  
    → return previous result or block

replayed old ExternalControlRequest  
    → deduplicate or block

Important rule:

Past validity does not guarantee current validity.

A request that was valid in the past must not be automatically valid now.

---

## **11\. Retry Rule**

Retry is allowed only when it is bounded and idempotent.

retry\_count \<= max\_retry\_count  
retry\_interval\_ms is bounded  
retry uses the same idempotency\_key  
retry must not create duplicate physical execution

Retry must not bypass:

Runtime Validation  
Safety Gate  
SafetyGatePass lease validation  
SafetyGatePass terminal status validation

If retry creates uncertainty about physical execution state, the result must become hold, manual review, or block depending on action criticality.

---

## **12\. Previous Result Rule**

A duplicate request does not always require a new block.

If the same idempotency key has already been safely processed, LEDO may return the previous result.

duplicate request detected  
    → return previous result  
    or  
    → block

However, returning a previous result must not create a new physical execution.

Allowed behavior:

same idempotency\_key \+ completed result  
    → return previous result

same idempotency\_key \+ in\_progress  
    → return in\_progress or hold

same idempotency\_key \+ blocked  
    → return previous block result

same idempotency\_key \+ terminal token  
    → block replay

---

## **13\. ApprovedAction State Interaction**

Idempotency must respect the lifecycle of `ApprovedAction`.

`ApprovedAction` is not execution.

It is authority granted under a specific context.

If a duplicate or replay is detected, the ApprovedAction state may transition to:

SUSPENDED  
REVALIDATION\_PENDING  
REAPPROVAL\_REQUIRED  
REVOKED  
BLOCKED\_BY\_IDEMPOTENCY

Recommended transitions:

duplicate but safely completed  
    → return previous result

duplicate while in progress  
    → hold or return in\_progress

duplicate with conflicting target  
    → block

replayed old request after context changed  
    → REVALIDATION\_PENDING or REAPPROVAL\_REQUIRED

terminal token reused  
    → BLOCKED\_BY\_IDEMPOTENCY

---

## **14\. External System Boundary**

External systems may also receive duplicate messages.

Therefore, `ExecutionRequest` and `ExternalControlRequest` must carry the idempotency key.

External systems or adapters must verify:

idempotency\_key exists  
SafetyGatePass is not expired  
SafetyGatePass is not terminal  
target\_external\_system matches  
trace\_id matches expected request  
request has not already been processed

Important boundary:

ExecutionRequest  
    ≠  
PhysicalCommand

LEDO sends bounded execution intent.

The external system performs physical execution.

---

## **15\. Failure Policy**

Idempotency failure must not silently become allow.

missing idempotency\_key  
    → block

duplicate request with unsafe ambiguity  
    → block

terminal SafetyGatePass replay  
    → block

expired SafetyGatePass replay  
    → block

idempotency ledger unavailable  
    → block for Tier 1

conflicting previous result  
    → manual review or block

unknown processing status  
    → block for Tier 1

For safety-critical actions, unknown does not mean allow.

---

## **16\. Hot Path Rule**

Runtime hot path must not perform unbounded idempotency discovery.

Forbidden:

unbounded database scan  
unbounded graph query  
LLM-based duplicate judgment  
external API call without timeout  
disk I/O in Safety Gate hot path

Allowed:

bounded idempotency ledger lookup  
in-memory idempotency cache  
precomputed terminal token state  
materialized previous result  
bounded transaction/outbox status

Core rule:

Hot path reads bounded idempotency state.  
Hot path does not perform unbounded duplicate discovery.

---

## **17\. MVP Scenario: STOP\_WORK**

For STOP\_WORK, idempotency must prevent repeated stop-work execution for the same target zone.

Validation targets:

same action\_type  
same approved\_action\_id  
same target\_zone  
same hazard\_id  
same safety\_gate\_pass\_id  
same execution\_request\_id  
same idempotency\_key

Failure handling:

duplicate STOP\_WORK already active  
    → return previous result or block duplicate

conflicting STOP\_WORK target  
    → manual review or block

missing idempotency\_key  
    → block

terminal SafetyGatePass replay  
    → block

STOP\_WORK may use fallback channels, but fallback must preserve the same idempotency key.

---

## **18\. MVP Scenario: DISPATCH\_ROBOT**

For DISPATCH\_ROBOT, idempotency must prevent duplicate robot dispatch or duplicated mission creation.

Validation targets:

same robot\_id  
same mission\_target  
same target\_zone  
same approved\_action\_id  
same safety\_gate\_pass\_id  
same execution\_request\_id  
same idempotency\_key

Failure handling:

duplicate robot dispatch  
    → block or return previous result

same mission already in progress  
    → hold or return in\_progress

terminal SafetyGatePass replay  
    → block

missing idempotency\_key  
    → block

conflicting mission detected  
    → block

LEDO must not create a second robot mission because of network retry.

---

## **19\. Audit Requirement**

Every idempotency decision must be auditable.

Audit targets:

idempotency\_key  
approved\_action\_id  
safety\_gate\_pass\_id  
execution\_request\_id  
external\_control\_request\_id  
target\_external\_system  
first\_seen\_at  
last\_seen\_at  
ledger\_status  
previous\_result\_ref  
terminal\_token\_status  
failure\_reasons  
trace\_id  
correlation\_id  
audit\_ref

If an idempotency failure leads to Safety Gate block, the following linkage must be preserved:

IdempotencyResult  
    → ValidatorResult  
    → RuntimeValidationResult  
    → SafetyGateBlock  
    → AuditRecord

---

## **20\. Final Idempotency Rule**

Same logical request  
must not create  
repeated physical execution.

Final rules:

No idempotency key,  
no execution path.

No terminal token reuse.

No duplicate physical execution.

No valid IdempotencyResult,  
no RuntimeValidationResult.

No RuntimeValidationResult,  
no Safety Gate pass.

No Safety Gate pass,  
no ExecutionRequest.

`idempotency/` is the Runtime Validation control area that prevents duplicate execution, replay, retry misuse, and stale SafetyGatePass reuse.

It ensures that LEDO can safely tolerate retries and distributed message delivery without creating repeated physical execution.

# **Idempotency Control**

