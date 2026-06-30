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

## **1\. 목적**

이 문서는 LEDO `08_runtime_validation/idempotency/` 영역을 정의한다.

`idempotency/`는 중복 요청, retry, replay, network delay, timeout, SafetyGatePass token 재사용으로 인해 같은 물리 실행이 반복되는 것을 방지한다.

LEDO에서는 같은 요청이 여러 번 관측될 수 있다.

하지만 같은 물리 실행이 여러 번 발생하면 안 된다.

same request  
    ≠  
repeated physical execution

Idempotency는 Runtime Validation이 분산 cyber-physical 환경에서 동작하기 때문에 필요하다.

분산 환경에서는 retry와 중복 전달이 정상적인 failure mode로 발생할 수 있다.

---

## **2\. Core Definition**

Idempotency는 같은 논리적 요청이 여러 번 처리되더라도 같은 안전한 결과를 반환하고, 중복 물리 실행을 만들지 않는 성질이다.

Idempotency  
    \= 같은 논리적 요청이 반복 처리되어도  
      중복 물리 실행을 만들지 않는 성질

Idempotency Control의 핵심 질문은 다음이다.

이 action, SafetyGatePass, ExecutionRequest,  
또는 ExternalControlRequest는 이미 처리된 적이 있는가?

이미 처리된 요청이라면 LEDO는 새로운 물리 실행 경로를 만들면 안 된다.

---

## **3\. Architectural Position**

`idempotency/`는 `08_runtime_validation/` 내부에 위치한다.

Idempotency는 `ApprovedAction`과 `ExecutionRequest` 사이에서 작동한다.

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

Idempotency는 Safety Gate를 대체하지 않는다.

Idempotency는 Safety Gate가 반드시 소비해야 하는 runtime safety condition을 제공한다.

---

## **4\. Responsibility Boundary**

`idempotency/`의 책임은 다음과 같다.

idempotency key 정의  
idempotency ledger model 정의  
duplicate request detection  
retry safety rule  
replay prevention  
SafetyGatePass terminal token rule  
previous result return rule  
external request deduplication  
duplicate handling audit linkage

`idempotency/`는 다음을 하지 않는다.

Approval 생성  
ApprovedAction 생성  
SafetyGatePass 생성  
ExecutionRequest 직접 생성  
PhysicalCommand 생성  
물리 rollback 수행  
외부 시스템 직접 제어  
Safety Gate pass/block 단독 결정

Idempotency는 요청 또는 token이 이미 처리되었는지, 그리고 안전하게 진행 가능한지를 판단할 뿐이다.

---

## **5\. Why Idempotency Is Needed**

분산 시스템에서는 메시지가 재시도될 수 있다.

Cyber-physical system에서는 retry가 물리 실행 반복으로 이어질 수 있기 때문에 매우 조심해야 한다.

예시:

ExecutionRequest sent to Fleet Manager  
    ↓  
network timeout occurs  
    ↓  
LEDO retries the same request  
    ↓  
Fleet Manager receives both messages

Idempotency가 없으면 같은 robot dispatch, stop-work request, lock-zone request, external control request가 두 번 실행될 수 있다.

LEDO에서는 이것이 허용되지 않는다.

network retry  
    ≠  
new execution authority

---

## **6\. Idempotency Scope**

Idempotency는 다음 객체에 적용된다.

ApprovedAction  
RuntimeValidationResult  
SafetyGatePass  
ExecutionRequest  
ExternalControlRequest  
FeedbackEvent  
AuditRecord

Idempotency는 다음 상황을 방지해야 한다.

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

모든 execution path는 `idempotency_key`를 가져야 한다.

권장 key 구성은 다음과 같다.

idempotency\_key \=  
    action\_type  
    approved\_action\_id  
    target\_id  
    target\_zone  
    safety\_gate\_pass\_id  
    execution\_request\_id  
    target\_external\_system  
    trace\_id

정확한 key 구조는 action type에 따라 달라질 수 있다.

하지만 idempotency key는 논리적 execution attempt를 유일하게 식별해야 한다.

핵심 규칙:

same logical execution attempt  
    → same idempotency\_key

Retry는 같은 idempotency key를 재사용해야 한다.

새로운 idempotency key를 만들어 Runtime Validation이나 Safety Gate를 우회하면 안 된다.

---

## **8\. Idempotency Ledger**

`idempotency/`는 Idempotency Ledger를 유지하거나 읽어야 한다.

Ledger는 논리적 요청이 이미 관측되었는지, 승인되었는지, 거절되었는지, 완료되었는지, 차단되었는지, 만료되었는지, terminal 처리되었는지를 기록한다.

권장 ledger 필드:

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

권장 status:

new  
in\_progress  
completed  
blocked  
rejected  
expired  
terminal  
unknown

Ledger에 이미 terminal result가 있다면 같은 요청은 새로운 물리 실행을 만들 수 없다.

---

## **9\. SafetyGatePass Terminal Token Rule**

SafetyGatePass는 재사용될 수 없다.

SafetyGatePass는 Adapter 또는 External System에서 최초로 관측되는 순간 terminal 상태가 되어야 한다.

consume-on-first-observation

다음 상태는 terminal이다.

CONSUMED\_ACCEPTED  
CONSUMED\_REJECTED  
CONSUMED\_DROPPED  
EXPIRED  
REVOKED

Terminal SafetyGatePass token은 재사용할 수 없다.

terminal SafetyGatePass replay  
    → block

요청이 dropped, rejected, expired, mismatched, blocked 되었더라도 SafetyGatePass token ID는 재사용 가능 상태로 남아 있으면 안 된다.

실패한 전송은 SafetyGatePass를 되살리지 않는다.

---

## **10\. Replay Rule**

Replay는 오래된 approval, SafetyGatePass, ExecutionRequest, ExternalControlRequest가 다시 제시되는 상황을 의미한다.

Replay는 새로운 실행 권한을 만들면 안 된다.

replayed old approval  
    → block or require revalidation

replayed old SafetyGatePass  
    → block if terminal or expired

replayed old ExecutionRequest  
    → return previous result or block

replayed old ExternalControlRequest  
    → deduplicate or block

중요 규칙:

Past validity does not guarantee current validity.

과거에 유효했던 요청이 현재도 자동으로 유효하다고 보면 안 된다.

---

## **11\. Retry Rule**

Retry는 허용될 수 있지만 bounded하고 idempotent해야 한다.

retry\_count \<= max\_retry\_count  
retry\_interval\_ms is bounded  
retry uses the same idempotency\_key  
retry must not create duplicate physical execution

Retry는 다음을 우회하면 안 된다.

Runtime Validation  
Safety Gate  
SafetyGatePass lease validation  
SafetyGatePass terminal status validation

Retry로 인해 물리 실행 상태가 불확실해지면 action criticality에 따라 hold, manual review, block으로 처리해야 한다.

---

## **12\. Previous Result Rule**

중복 요청이라고 항상 새롭게 block해야 하는 것은 아니다.

같은 idempotency key가 이미 안전하게 처리되었다면 LEDO는 previous result를 반환할 수 있다.

duplicate request detected  
    → return previous result  
    or  
    → block

그러나 previous result를 반환하더라도 새로운 물리 실행이 발생하면 안 된다.

허용 동작:

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

Idempotency는 `ApprovedAction`의 lifecycle을 존중해야 한다.

`ApprovedAction`은 실행이 아니다.

`ApprovedAction`은 특정 조건 아래 부여된 권한이다.

Duplicate 또는 replay가 탐지되면 ApprovedAction 상태는 다음으로 전이될 수 있다.

SUSPENDED  
REVALIDATION\_PENDING  
REAPPROVAL\_REQUIRED  
REVOKED  
BLOCKED\_BY\_IDEMPOTENCY

권장 전이:

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

External System도 중복 메시지를 받을 수 있다.

따라서 `ExecutionRequest`와 `ExternalControlRequest`는 반드시 idempotency key를 포함해야 한다.

External System 또는 Adapter는 다음을 확인해야 한다.

idempotency\_key exists  
SafetyGatePass is not expired  
SafetyGatePass is not terminal  
target\_external\_system matches  
trace\_id matches expected request  
request has not already been processed

중요 경계:

ExecutionRequest  
    ≠  
PhysicalCommand

LEDO는 bounded execution intent를 보낸다.

External System은 실제 물리 실행을 수행한다.

---

## **15\. Failure Policy**

Idempotency failure가 조용히 allow가 되면 안 된다.

missing idempotency\_key  
    → block

duplicate request with unsafe ambiguity  
    → block

terminal SafetyGatePass replay  
    → block

expired SafetyGatePass replay  
    → block

idempotency ledger unavailable  
    → Tier 1에서는 block

conflicting previous result  
    → manual review or block

unknown processing status  
    → Tier 1에서는 block

Safety-critical action에서 unknown은 allow가 아니다.

---

## **16\. Hot Path Rule**

Runtime hot path는 무제한 idempotency discovery를 수행하면 안 된다.

금지:

unbounded database scan  
unbounded graph query  
LLM-based duplicate judgment  
external API call without timeout  
disk I/O in Safety Gate hot path

허용:

bounded idempotency ledger lookup  
in-memory idempotency cache  
precomputed terminal token state  
materialized previous result  
bounded transaction/outbox status

핵심 규칙:

Hot path reads bounded idempotency state.  
Hot path does not perform unbounded duplicate discovery.

---

## **17\. MVP Scenario: STOP\_WORK**

STOP\_WORK에서는 같은 target zone에 대한 stop-work 실행이 반복되지 않도록 idempotency를 적용해야 한다.

검증 대상:

same action\_type  
same approved\_action\_id  
same target\_zone  
same hazard\_id  
same safety\_gate\_pass\_id  
same execution\_request\_id  
same idempotency\_key

실패 처리:

duplicate STOP\_WORK already active  
    → return previous result or block duplicate

conflicting STOP\_WORK target  
    → manual review or block

missing idempotency\_key  
    → block

terminal SafetyGatePass replay  
    → block

STOP\_WORK는 fallback channel을 사용할 수 있지만, fallback도 같은 idempotency key를 보존해야 한다.

---

## **18\. MVP Scenario: DISPATCH\_ROBOT**

DISPATCH\_ROBOT에서는 중복 robot dispatch 또는 중복 mission 생성을 방지해야 한다.

검증 대상:

same robot\_id  
same mission\_target  
same target\_zone  
same approved\_action\_id  
same safety\_gate\_pass\_id  
same execution\_request\_id  
same idempotency\_key

실패 처리:

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

LEDO는 network retry 때문에 두 번째 robot mission을 만들면 안 된다.

---

## **19\. Audit Requirement**

모든 idempotency decision은 audit 가능해야 한다.

Audit 대상:

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

Idempotency failure가 Safety Gate block으로 이어진 경우 다음 연결이 보존되어야 한다.

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

한글 기준:

같은 논리적 요청은  
반복된 물리 실행을 만들면 안 된다.

최종 규칙:

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

`idempotency/`는 LEDO Runtime Validation에서 중복 실행, replay, retry 오용, stale SafetyGatePass 재사용을 방지하는 control 영역이다.

이 영역은 LEDO가 retry와 분산 메시지 전달을 안전하게 허용하면서도 반복 물리 실행을 만들지 않도록 보장한다.

