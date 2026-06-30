# **Safety Gate**

## **1\. Purpose**

This document defines the LEDO `08_runtime_validation/safety_gate/` area.

`safety_gate/` is the final execution-readiness gate between `ApprovedAction` and `ExecutionRequest`.

The Safety Gate consumes Runtime Validation results and decides whether an approved action may proceed to the execution request stage.

ApprovedAction  
    ↓  
Runtime Validation  
    ↓  
Safety Gate  
    ↓  
SafetyGatePass or SafetyGateBlock

The Safety Gate does not approve.

The Safety Gate does not execute.

The Safety Gate does not create physical commands.

The Safety Gate does not directly control external systems.

The Safety Gate only determines whether the current runtime condition is ready for execution request creation.

---

## **2\. Core Definition**

The Safety Gate is a deterministic runtime gate that produces one of two outcomes:

SafetyGatePass  
SafetyGateBlock

The core question of the Safety Gate is:

Given all Runtime Validation results,  
is this ApprovedAction ready to become an ExecutionRequest right now?

A Safety Gate pass means that LEDO may create an `ExecutionRequest`.

A Safety Gate block means that LEDO must not create an `ExecutionRequest`.

---

## **3\. Architectural Position**

`safety_gate/` is located at the end of Runtime Validation.

It sits after validators, TOCTOU control, SHACL pre-validation, network health checks, and idempotency checks.

ApprovedAction  
    ↓  
RuntimeValidationInput  
    ↓  
Validators  
    ↓  
TOCTOU Result  
    ↓  
SHACL Validation Result  
    ↓  
Network Health Result  
    ↓  
Idempotency Result  
    ↓  
RuntimeValidationResult  
    ↓  
Safety Gate  
    ↓  
SafetyGatePass or SafetyGateBlock  
    ↓  
ExecutionRequest

The Safety Gate is the final checkpoint before ExecutionRequest creation.

---

## **4\. Responsibility Boundary**

The Safety Gate is responsible for:

consuming RuntimeValidationResult  
checking required ValidatorResults  
checking SafetySnapshot validity  
checking TOCTOU status  
checking SHACL validation status  
checking NetworkHealthResult  
checking IdempotencyResult  
checking approval and policy validity status  
making final pass/block decision  
issuing SafetyGatePass lease  
creating SafetyGateBlock result  
producing auditable gate decision

The Safety Gate is not responsible for:

creating Approval  
creating ApprovedAction  
running full SHACL validation  
running OWL reasoning  
running SPARQL queries  
calling LLM / SLM  
directly controlling robots  
directly controlling PLC / SCADA  
creating PhysicalCommand  
performing physical execution

The Safety Gate decides execution readiness.

The External System performs actual physical execution.

---

## **5\. Safety Gate vs Runtime Validation**

Runtime Validation and Safety Gate are different.

Runtime Validation  
    → checks whether the current execution-time conditions are valid.

Safety Gate  
    → consumes validation results and makes the final pass/block decision.

Validators check individual conditions.

Runtime Validation aggregates those checks.

Safety Gate makes the final deterministic decision.

ValidatorResult  
    ↓  
RuntimeValidationResult  
    ↓  
SafetyGateResult

A single validator pass does not mean Safety Gate pass.

---

## **6\. Safety Gate Inputs**

The Safety Gate must consume precomputed or materialized validation results.

Recommended inputs:

SafetyGateInput  
    approved\_action\_id  
    action\_type  
    RuntimeValidationResult  
    ValidatorResultSummary  
    SafetySnapshot  
    TOCTOUResult  
    SHACLValidationResult  
    NetworkHealthResult  
    IdempotencyResult  
    ApprovalValidityResult  
    PolicyRevalidationResult  
    EvidenceValidityResult  
    CapabilityAvailabilityResult  
    trace\_id  
    correlation\_id

Safety Gate must not depend on missing or unknown required input.

For safety-critical actions, missing required input must result in block.

---

## **7\. Safety Gate Outputs**

The Safety Gate produces one of two outputs:

SafetyGatePass  
SafetyGateBlock

### **7.1 SafetyGatePass**

`SafetyGatePass` means the current Runtime Validation result is sufficient to allow `ExecutionRequest` creation.

It is not permanent authority.

It is a short-lived execution-readiness lease.

### **7.2 SafetyGateBlock**

`SafetyGateBlock` means the execution path must be stopped.

No `ExecutionRequest` may be created from a blocked result.

---

## **8\. SafetyGatePass Contract**

A SafetyGatePass must be short-lived and bound to a specific execution context.

Recommended fields:

SafetyGatePass  
    safety\_gate\_pass\_id  
    approved\_action\_id  
    action\_type  
    issued\_at  
    expires\_at  
    lease\_duration\_ms  
    lease\_started\_monotonic\_ms  
    lease\_expires\_monotonic\_ms  
    target\_external\_system  
    execution\_request\_scope  
    idempotency\_key  
    safety\_snapshot\_ref  
    runtime\_validation\_result\_ref  
    trace\_id  
    correlation\_id  
    terminal\_status

The SafetyGatePass must be bound to:

specific ApprovedAction  
specific action type  
specific target  
specific external system  
specific safety snapshot  
specific runtime validation result  
specific idempotency key

A SafetyGatePass must not be reused for another action, target, or external system.

---

## **9\. SafetyGatePass Lease Rule**

A SafetyGatePass is a short-lived execution-readiness lease.

SafetyGatePass  
    \= short-lived execution-readiness lease

It must expire quickly.

Example lease duration:

lease\_duration\_ms \= 500  
or  
lease\_duration\_ms \= 1000

The actual value must be defined by action criticality, site latency, external system protocol, and runtime policy.

Lease expiry rule:

if current\_time \> expires\_at:  
    block  
    require runtime revalidation

Monotonic time must be used for local duration and lease age calculation.

lease\_age\_ms  
lease\_duration\_ms  
timeout\_ms  
retry\_interval\_ms  
    → monotonic clock

Wall-clock UTC timestamps may be used for audit and cross-system records.

---

## **10\. SafetyGateBlock Contract**

A SafetyGateBlock records why execution request creation is not allowed.

Recommended fields:

SafetyGateBlock  
    safety\_gate\_block\_id  
    approved\_action\_id  
    action\_type  
    blocked\_at  
    block\_reasons  
    failed\_validator\_refs  
    failed\_runtime\_validation\_ref  
    safety\_snapshot\_ref  
    severity  
    tier  
    suggested\_next\_state  
    manual\_review\_required  
    trace\_id  
    correlation\_id  
    audit\_ref

Possible block reasons:

missing\_required\_validation  
invalid\_runtime\_validation\_result  
stale\_state  
stale\_snapshot  
toctou\_conflict  
critical\_condition\_changed  
invalid\_approval  
expired\_approval  
policy\_failed  
external\_system\_unreachable  
adapter\_unhealthy  
feedback\_channel\_unavailable  
idempotency\_failure  
terminal\_safety\_gate\_pass\_replay  
shacl\_validation\_failed  
clock\_skew\_exceeded  
unknown\_required\_condition

---

## **11\. Pass Conditions**

Safety Gate may issue a pass only when all required conditions are satisfied.

Required pass conditions:

RuntimeValidationResult is valid  
required ValidatorResults are pass or acceptable warning  
SafetySnapshot is valid and fresh  
TOCTOUResult is valid  
SHACLValidationResult is valid  
ApprovalValidityResult is valid  
PolicyRevalidationResult is valid  
NetworkHealthResult is acceptable  
IdempotencyResult is valid  
SafetyGatePass lease can be issued  
required audit context exists

For safety-critical actions, unknown cannot be treated as pass.

unknown  
    ≠  
pass

---

## **12\. Block Conditions**

Safety Gate must block when any required safety-critical condition is invalid, stale, unknown, or missing.

Block conditions:

missing RuntimeValidationResult  
missing required ValidatorResult  
stale SafetySnapshot  
stale required state  
TOCTOU conflict  
critical field changed  
expired approval  
revoked approval  
policy condition failed  
SHACL required shape violation  
external system unreachable  
adapter unhealthy  
feedback channel unavailable  
idempotency key missing  
terminal SafetyGatePass replay  
clock skew exceeded  
unknown required safety condition

For Tier 1 safety-critical actions, the default failure effect is block.

---

## **13\. Fail-Closed Rule**

The Safety Gate must fail closed.

unknown  
    → block

missing  
    → block

stale  
    → block

invalid  
    → block

conflict  
    → block or manual review

Safety Gate must never silently convert failure into allow.

failure  
    ≠  
allow

For human safety, robot path, hazard zone, emergency stop, restricted zone, and physical execution related actions, uncertain state must be blocked or escalated to manual review.

---

## **14\. Criticality Tier Handling**

Safety Gate must respect validation criticality tier.

Tier 1\. Safety-Critical  
Tier 2\. Operational-Critical  
Tier 3\. Informational

### **Tier 1\. Safety-Critical**

Examples:

worker location  
human presence  
robot path clearance  
hazard zone  
restricted zone  
emergency stop  
SafetyGatePass lease  
idempotency key

Handling:

fail  
    → block

stale  
    → block

unknown  
    → block

timeout  
    → block

### **Tier 2\. Operational-Critical**

Examples:

robot battery  
adapter latency  
fleet manager load  
mission queue  
equipment utilization

Handling:

fail  
    → hold / retry / block depending on context

stale  
    → soft revalidation / hold / retry

unknown  
    → hold or degraded mode

### **Tier 3\. Informational**

Examples:

dashboard KPI  
historical trend  
non-critical telemetry  
reporting metric

Handling:

fail  
    → warning

stale  
    → warning

unknown  
    → warning

Tier 3 data must not be required for Safety Gate pass.

---

## **15\. Hot Path Rule**

The Safety Gate hot path must be deterministic, bounded, and read-only.

The Safety Gate hot path must not perform:

LLM / SLM call  
OWL reasoning  
Full SHACL validation  
SPARQL query  
Graph DB network call  
unbounded external API call  
unbounded health probe  
disk I/O  
unbounded computation

The Safety Gate hot path may read:

materialized safety snapshot  
precomputed RuntimeValidationResult  
ValidatorResultSummary  
SHACLValidationResult  
NetworkHealthResult  
IdempotencyResult  
bounded health cache  
bounded idempotency ledger result  
immutable runtime context

Core rule:

Safety Gate reads precomputed results.  
Safety Gate does not perform heavy reasoning.

---

## **16\. Idempotency Relation**

Safety Gate must not issue reusable or duplicate execution authority.

Before pass issuance, Safety Gate must verify:

idempotency\_key exists  
approved\_action\_id matches  
target\_external\_system matches  
SafetyGatePass is not already terminal  
previous execution result does not conflict  
duplicate physical execution risk is not present

SafetyGatePass issued by the Safety Gate must be linked to an idempotency key.

No idempotency key,  
no SafetyGatePass.

SafetyGatePass terminalization is handled by idempotency / adapter / external system boundary rules, but Safety Gate must not issue a pass when terminal replay is detected.

---

## **17\. TOCTOU Relation**

Safety Gate must consume TOCTOU results.

Safety Gate must block when:

approval-time snapshot and execution-time snapshot conflict  
safety-critical field changed  
worker entered robot path  
zone became restricted  
hazard severity escalated  
robot became unavailable  
policy version changed incompatibly  
approval expired  
SafetyGatePass lease expired

TOCTOU pass does not automatically mean Safety Gate pass.

It is one required input.

---

## **18\. SHACL Relation**

Safety Gate must consume SHACL validation results.

Safety Gate must block when required shape validation fails.

Examples:

ApprovedActionShape invalid  
RuntimeValidationInputShape invalid  
SafetySnapshotShape invalid  
ValidatorResultShape invalid  
SafetyGatePassShape invalid  
ExecutionRequestShape invalid

Safety Gate must not run full SHACL validation in the hot path.

It must read materialized SHACLValidationResult.

---

## **19\. Network Health Relation**

Safety Gate must consume NetworkHealthResult.

Safety Gate must block or hold when:

external system unreachable  
adapter unhealthy  
heartbeat stale  
feedback channel unavailable  
circuit breaker open  
protocol incompatible

Important boundary:

external system reachable  
    ≠  
safe to execute

Network Health pass alone does not mean Safety Gate pass.

---

## **20\. ApprovedAction State Transition**

Safety Gate result affects the runtime state of the ApprovedAction.

Normal transition:

APPROVED  
    ↓  
RUNTIME\_VALIDATING  
    ↓  
RUNTIME\_VALIDATED  
    ↓  
SAFETY\_GATE\_PASSED  
    ↓  
EXECUTION\_REQUESTED

Blocked transition:

APPROVED  
    ↓  
RUNTIME\_VALIDATING  
    ↓  
RUNTIME\_VALIDATED  
    ↓  
SAFETY\_GATE\_BLOCKED

Possible next states after block:

SUSPENDED  
REVALIDATION\_PENDING  
REAPPROVAL\_REQUIRED  
REVOKED  
MANUAL\_REVIEW\_REQUIRED

Rules:

safety-critical condition changed  
    → REAPPROVAL\_REQUIRED or REVOKED

stale but recoverable data  
    → REVALIDATION\_PENDING

external system temporarily unavailable  
    → SUSPENDED or REVALIDATION\_PENDING

approval expired  
    → REAPPROVAL\_REQUIRED

target changed  
    → REVOKED

---

## **21\. MVP Scenario: STOP\_WORK**

For STOP\_WORK, the Safety Gate must consume the following results:

hazard\_still\_present\_validator  
zone\_accessible\_validator  
state\_freshness\_validator  
snapshot\_freshness\_validator  
approval\_validity\_validator  
policy\_revalidation\_validator  
external\_system\_health\_validator  
adapter\_health\_validator  
idempotency\_validator  
safety\_gate\_pass\_lease\_validator  
safety\_gate\_pass\_terminal\_status\_validator

Pass conditions:

hazard condition is valid  
target zone matches  
required state is fresh  
approval is valid or emergency condition is active  
policy is valid  
external notification path is available or fallback is defined  
idempotency key is valid  
SafetyGatePass lease can be issued

Block conditions:

required safety state stale  
hazard condition unknown  
target zone mismatch  
approval invalid  
policy failed  
no valid dispatch / notification path  
duplicate STOP\_WORK execution risk

STOP\_WORK is safety-critical.

Unknown required safety condition must block or escalate to manual review.

---

## **22\. MVP Scenario: DISPATCH\_ROBOT**

For DISPATCH\_ROBOT, the Safety Gate must consume the following results:

worker\_not\_in\_robot\_path\_validator  
zone\_accessible\_validator  
robot\_available\_validator  
state\_freshness\_validator  
snapshot\_freshness\_validator  
approval\_validity\_validator  
policy\_revalidation\_validator  
external\_system\_health\_validator  
adapter\_health\_validator  
idempotency\_validator  
safety\_gate\_pass\_lease\_validator  
safety\_gate\_pass\_terminal\_status\_validator

Pass conditions:

worker is not in robot path  
zone is accessible  
robot is available  
robot capability is valid  
fleet manager is reachable  
adapter is healthy  
feedback channel is available  
approval is valid  
policy is valid  
idempotency key is valid  
SafetyGatePass lease can be issued

Block conditions:

worker in robot path  
worker location stale  
zone restricted  
robot unavailable  
robot faulted  
fleet manager unreachable  
adapter unhealthy  
approval expired  
policy failed  
duplicate robot dispatch risk

LEDO must not send low-level robot motion commands.

LEDO only sends approved mission intent to the external fleet manager.

---

## **23\. SafetyGateResult Contract**

Safety Gate produces a standard result.

SafetyGateResult  
    result\_id  
    approved\_action\_id  
    action\_type  
    status  
    issued\_pass\_ref  
    block\_ref  
    checked\_at  
    runtime\_validation\_result\_ref  
    safety\_snapshot\_ref  
    validator\_summary\_ref  
    decision\_reasons  
    failure\_reasons  
    warning\_reasons  
    suggested\_next\_state  
    trace\_id  
    correlation\_id  
    audit\_ref

Possible status:

pass  
block  
manual\_review\_required  
hold  
requires\_revalidation  
requires\_reapproval

Only `pass` may allow ExecutionRequest creation.

---

## **24\. Audit Requirement**

Every Safety Gate decision must be auditable.

Audit targets:

safety\_gate\_result\_id  
approved\_action\_id  
action\_type  
runtime\_validation\_result\_ref  
validator\_result\_refs  
safety\_snapshot\_ref  
TOCTOUResult ref  
SHACLValidationResult ref  
NetworkHealthResult ref  
IdempotencyResult ref  
SafetyGatePass id  
SafetyGateBlock id  
block\_reasons  
pass\_reasons  
checked\_at  
trace\_id  
correlation\_id  
audit\_ref

If the Safety Gate blocks, the block reason must be traceable to the validator, runtime validation result, SHACL result, network health result, idempotency result, or TOCTOU result that caused it.

---

## **25\. Final Safety Gate Rule**

Safety Gate does not approve.  
Safety Gate does not execute.  
Safety Gate does not command.  
Safety Gate only gates execution readiness.

Final rules:

No valid RuntimeValidationResult,  
no Safety Gate pass.

No Safety Gate pass,  
no ExecutionRequest.

No valid SafetyGatePass lease,  
no valid dispatch.

No ExecutionRequest,  
no external execution.

No audit,  
no trust.

`safety_gate/` is the final deterministic runtime gate that determines whether an `ApprovedAction` may become an `ExecutionRequest`.

It protects LEDO from stale state, invalid validation results, TOCTOU conflicts, duplicate execution, invalid structure, unhealthy external paths, and unsafe execution readiness.

# **Safety Gate**

## **1\. 목적**

이 문서는 LEDO `08_runtime_validation/safety_gate/` 영역을 정의한다.

`safety_gate/`는 `ApprovedAction`과 `ExecutionRequest` 사이에 위치하는 최종 실행 준비 관문이다.

Safety Gate는 Runtime Validation 결과를 소비하고, 승인된 action이 실행 요청 단계로 넘어갈 수 있는지 최종 판단한다.

ApprovedAction  
    ↓  
Runtime Validation  
    ↓  
Safety Gate  
    ↓  
SafetyGatePass or SafetyGateBlock

Safety Gate는 승인하지 않는다.

Safety Gate는 실행하지 않는다.

Safety Gate는 physical command를 만들지 않는다.

Safety Gate는 외부 시스템을 직접 제어하지 않는다.

Safety Gate는 현재 runtime condition이 `ExecutionRequest` 생성 준비가 되었는지만 판단한다.

---

## **2\. Core Definition**

Safety Gate는 결정론적 runtime gate이다.

Safety Gate는 다음 둘 중 하나의 결과를 생성한다.

SafetyGatePass  
SafetyGateBlock

Safety Gate의 핵심 질문은 다음이다.

모든 Runtime Validation 결과를 고려했을 때,  
이 ApprovedAction은 지금 ExecutionRequest가 될 준비가 되었는가?

SafetyGatePass는 LEDO가 `ExecutionRequest`를 생성할 수 있음을 의미한다.

SafetyGateBlock은 LEDO가 `ExecutionRequest`를 생성하면 안 됨을 의미한다.

---

## **3\. Architectural Position**

`safety_gate/`는 Runtime Validation의 마지막에 위치한다.

Safety Gate는 validators, TOCTOU control, SHACL pre-validation, network health check, idempotency check 이후에 작동한다.

ApprovedAction  
    ↓  
RuntimeValidationInput  
    ↓  
Validators  
    ↓  
TOCTOU Result  
    ↓  
SHACL Validation Result  
    ↓  
Network Health Result  
    ↓  
Idempotency Result  
    ↓  
RuntimeValidationResult  
    ↓  
Safety Gate  
    ↓  
SafetyGatePass or SafetyGateBlock  
    ↓  
ExecutionRequest

Safety Gate는 ExecutionRequest 생성 직전의 마지막 검문소이다.

---

## **4\. Responsibility Boundary**

Safety Gate의 책임은 다음과 같다.

RuntimeValidationResult 소비  
필수 ValidatorResult 확인  
SafetySnapshot 유효성 확인  
TOCTOU 상태 확인  
SHACL validation 상태 확인  
NetworkHealthResult 확인  
IdempotencyResult 확인  
approval / policy validity 상태 확인  
최종 pass/block 결정  
SafetyGatePass lease 발급  
SafetyGateBlock 결과 생성  
audit 가능한 gate decision 생성

Safety Gate는 다음을 하지 않는다.

Approval 생성  
ApprovedAction 생성  
full SHACL validation 실행  
OWL reasoning 실행  
SPARQL query 실행  
LLM / SLM 호출  
로봇 직접 제어  
PLC / SCADA 직접 제어  
PhysicalCommand 생성  
실제 물리 실행 수행

Safety Gate는 실행 준비 상태를 판단한다.

External System은 실제 물리 실행을 수행한다.

---

## **5\. Safety Gate vs Runtime Validation**

Runtime Validation과 Safety Gate는 다르다.

Runtime Validation  
    → 현재 execution-time condition이 유효한지 검증한다.

Safety Gate  
    → validation 결과를 소비하고 최종 pass/block을 결정한다.

Validator는 개별 조건을 검사한다.

Runtime Validation은 이 검사 결과들을 집계한다.

Safety Gate는 최종 결정론적 판단을 수행한다.

ValidatorResult  
    ↓  
RuntimeValidationResult  
    ↓  
SafetyGateResult

하나의 validator가 pass를 반환했다고 해서 Safety Gate pass가 되는 것은 아니다.

---

## **6\. Safety Gate Inputs**

Safety Gate는 사전 계산되거나 materialized 된 validation result를 소비해야 한다.

권장 입력은 다음과 같다.

SafetyGateInput  
    approved\_action\_id  
    action\_type  
    RuntimeValidationResult  
    ValidatorResultSummary  
    SafetySnapshot  
    TOCTOUResult  
    SHACLValidationResult  
    NetworkHealthResult  
    IdempotencyResult  
    ApprovalValidityResult  
    PolicyRevalidationResult  
    EvidenceValidityResult  
    CapabilityAvailabilityResult  
    trace\_id  
    correlation\_id

Safety Gate는 필수 입력이 missing 또는 unknown인 상태에 의존하면 안 된다.

Safety-critical action에서 필수 입력이 누락되면 block해야 한다.

---

## **7\. Safety Gate Outputs**

Safety Gate는 다음 둘 중 하나를 출력한다.

SafetyGatePass  
SafetyGateBlock

### **7.1 SafetyGatePass**

`SafetyGatePass`는 현재 Runtime Validation 결과가 `ExecutionRequest` 생성을 허용하기에 충분하다는 의미이다.

SafetyGatePass는 영구 권한이 아니다.

SafetyGatePass는 짧은 유효기간을 가진 execution-readiness lease이다.

### **7.2 SafetyGateBlock**

`SafetyGateBlock`은 execution path를 차단해야 한다는 의미이다.

SafetyGateBlock 결과에서는 `ExecutionRequest`를 생성하면 안 된다.

---

## **8\. SafetyGatePass Contract**

SafetyGatePass는 짧은 수명의 lease이며 특정 execution context에 묶여야 한다.

권장 필드는 다음과 같다.

SafetyGatePass  
    safety\_gate\_pass\_id  
    approved\_action\_id  
    action\_type  
    issued\_at  
    expires\_at  
    lease\_duration\_ms  
    lease\_started\_monotonic\_ms  
    lease\_expires\_monotonic\_ms  
    target\_external\_system  
    execution\_request\_scope  
    idempotency\_key  
    safety\_snapshot\_ref  
    runtime\_validation\_result\_ref  
    trace\_id  
    correlation\_id  
    terminal\_status

SafetyGatePass는 다음과 묶여야 한다.

specific ApprovedAction  
specific action type  
specific target  
specific external system  
specific safety snapshot  
specific runtime validation result  
specific idempotency key

SafetyGatePass는 다른 action, target, external system에 재사용되면 안 된다.

---

## **9\. SafetyGatePass Lease Rule**

SafetyGatePass는 짧은 유효기간을 가진 execution-readiness lease이다.

SafetyGatePass  
    \= short-lived execution-readiness lease

SafetyGatePass는 빠르게 만료되어야 한다.

예시 lease duration:

lease\_duration\_ms \= 500  
or  
lease\_duration\_ms \= 1000

실제 값은 action criticality, site latency, external system protocol, runtime policy에 따라 정의한다.

Lease expiry rule:

if current\_time \> expires\_at:  
    block  
    require runtime revalidation

Local duration과 lease age 계산에는 monotonic time을 사용해야 한다.

lease\_age\_ms  
lease\_duration\_ms  
timeout\_ms  
retry\_interval\_ms  
    → monotonic clock

Wall-clock UTC timestamp는 audit과 cross-system record에 사용할 수 있다.

---

## **10\. SafetyGateBlock Contract**

SafetyGateBlock은 왜 `ExecutionRequest` 생성이 허용되지 않는지 기록한다.

권장 필드는 다음과 같다.

SafetyGateBlock  
    safety\_gate\_block\_id  
    approved\_action\_id  
    action\_type  
    blocked\_at  
    block\_reasons  
    failed\_validator\_refs  
    failed\_runtime\_validation\_ref  
    safety\_snapshot\_ref  
    severity  
    tier  
    suggested\_next\_state  
    manual\_review\_required  
    trace\_id  
    correlation\_id  
    audit\_ref

가능한 block reason:

missing\_required\_validation  
invalid\_runtime\_validation\_result  
stale\_state  
stale\_snapshot  
toctou\_conflict  
critical\_condition\_changed  
invalid\_approval  
expired\_approval  
policy\_failed  
external\_system\_unreachable  
adapter\_unhealthy  
feedback\_channel\_unavailable  
idempotency\_failure  
terminal\_safety\_gate\_pass\_replay  
shacl\_validation\_failed  
clock\_skew\_exceeded  
unknown\_required\_condition

---

## **11\. Pass Conditions**

Safety Gate는 모든 필수 조건이 충족된 경우에만 pass를 발급할 수 있다.

필수 pass 조건:

RuntimeValidationResult is valid  
required ValidatorResults are pass or acceptable warning  
SafetySnapshot is valid and fresh  
TOCTOUResult is valid  
SHACLValidationResult is valid  
ApprovalValidityResult is valid  
PolicyRevalidationResult is valid  
NetworkHealthResult is acceptable  
IdempotencyResult is valid  
SafetyGatePass lease can be issued  
required audit context exists

Safety-critical action에서 unknown은 pass로 취급할 수 없다.

unknown  
    ≠  
pass

---

## **12\. Block Conditions**

Safety Gate는 필수 safety-critical condition이 invalid, stale, unknown, missing인 경우 block해야 한다.

Block 조건:

missing RuntimeValidationResult  
missing required ValidatorResult  
stale SafetySnapshot  
stale required state  
TOCTOU conflict  
critical field changed  
expired approval  
revoked approval  
policy condition failed  
SHACL required shape violation  
external system unreachable  
adapter unhealthy  
feedback channel unavailable  
idempotency key missing  
terminal SafetyGatePass replay  
clock skew exceeded  
unknown required safety condition

Tier 1 safety-critical action에서는 기본 실패 효과가 block이다.

---

## **13\. Fail-Closed Rule**

Safety Gate는 fail-closed 방식으로 동작해야 한다.

unknown  
    → block

missing  
    → block

stale  
    → block

invalid  
    → block

conflict  
    → block or manual review

Safety Gate는 failure를 조용히 allow로 바꾸면 안 된다.

failure  
    ≠  
allow

사람 안전, robot path, hazard zone, emergency stop, restricted zone, physical execution과 관련된 action에서는 불확실한 상태를 block하거나 manual review로 escalate해야 한다.

---

## **14\. Criticality Tier Handling**

Safety Gate는 validation criticality tier를 존중해야 한다.

Tier 1\. Safety-Critical  
Tier 2\. Operational-Critical  
Tier 3\. Informational

### **Tier 1\. Safety-Critical**

예시:

worker location  
human presence  
robot path clearance  
hazard zone  
restricted zone  
emergency stop  
SafetyGatePass lease  
idempotency key

처리:

fail  
    → block

stale  
    → block

unknown  
    → block

timeout  
    → block

### **Tier 2\. Operational-Critical**

예시:

robot battery  
adapter latency  
fleet manager load  
mission queue  
equipment utilization

처리:

fail  
    → context에 따라 hold / retry / block

stale  
    → soft revalidation / hold / retry

unknown  
    → hold or degraded mode

### **Tier 3\. Informational**

예시:

dashboard KPI  
historical trend  
non-critical telemetry  
reporting metric

처리:

fail  
    → warning

stale  
    → warning

unknown  
    → warning

Tier 3 데이터는 Safety Gate pass의 필수 조건이 되어서는 안 된다.

---

## **15\. Hot Path Rule**

Safety Gate hot path는 deterministic, bounded, read-only여야 한다.

Safety Gate hot path에서는 다음을 수행하면 안 된다.

LLM / SLM call  
OWL reasoning  
Full SHACL validation  
SPARQL query  
Graph DB network call  
unbounded external API call  
unbounded health probe  
disk I/O  
unbounded computation

Safety Gate hot path는 다음만 읽을 수 있다.

materialized safety snapshot  
precomputed RuntimeValidationResult  
ValidatorResultSummary  
SHACLValidationResult  
NetworkHealthResult  
IdempotencyResult  
bounded health cache  
bounded idempotency ledger result  
immutable runtime context

핵심 규칙:

Safety Gate reads precomputed results.  
Safety Gate does not perform heavy reasoning.

---

## **16\. Idempotency Relation**

Safety Gate는 재사용 가능하거나 중복된 실행 권한을 발급하면 안 된다.

Pass 발급 전 Safety Gate는 다음을 확인해야 한다.

idempotency\_key exists  
approved\_action\_id matches  
target\_external\_system matches  
SafetyGatePass is not already terminal  
previous execution result does not conflict  
duplicate physical execution risk is not present

Safety Gate가 발급하는 SafetyGatePass는 idempotency key와 연결되어야 한다.

No idempotency key,  
no SafetyGatePass.

SafetyGatePass terminalization은 idempotency / adapter / external system boundary rule에서 처리하지만, terminal replay가 감지된 경우 Safety Gate는 pass를 발급하면 안 된다.

---

## **17\. TOCTOU Relation**

Safety Gate는 TOCTOU result를 소비해야 한다.

Safety Gate는 다음 경우 block해야 한다.

approval-time snapshot and execution-time snapshot conflict  
safety-critical field changed  
worker entered robot path  
zone became restricted  
hazard severity escalated  
robot became unavailable  
policy version changed incompatibly  
approval expired  
SafetyGatePass lease expired

TOCTOU pass가 곧바로 Safety Gate pass를 의미하는 것은 아니다.

TOCTOU result는 필수 입력 중 하나이다.

---

## **18\. SHACL Relation**

Safety Gate는 SHACL validation result를 소비해야 한다.

Required shape validation이 실패하면 Safety Gate는 block해야 한다.

예시:

ApprovedActionShape invalid  
RuntimeValidationInputShape invalid  
SafetySnapshotShape invalid  
ValidatorResultShape invalid  
SafetyGatePassShape invalid  
ExecutionRequestShape invalid

Safety Gate는 hot path에서 full SHACL validation을 실행하면 안 된다.

Safety Gate는 materialized SHACLValidationResult를 읽어야 한다.

---

## **19\. Network Health Relation**

Safety Gate는 NetworkHealthResult를 소비해야 한다.

Safety Gate는 다음 경우 block 또는 hold를 반환해야 한다.

external system unreachable  
adapter unhealthy  
heartbeat stale  
feedback channel unavailable  
circuit breaker open  
protocol incompatible

중요 경계:

external system reachable  
    ≠  
safe to execute

Network Health pass만으로는 Safety Gate pass가 되지 않는다.

---

## **20\. ApprovedAction State Transition**

Safety Gate 결과는 ApprovedAction의 runtime state에 영향을 준다.

정상 전이:

APPROVED  
    ↓  
RUNTIME\_VALIDATING  
    ↓  
RUNTIME\_VALIDATED  
    ↓  
SAFETY\_GATE\_PASSED  
    ↓  
EXECUTION\_REQUESTED

Block 전이:

APPROVED  
    ↓  
RUNTIME\_VALIDATING  
    ↓  
RUNTIME\_VALIDATED  
    ↓  
SAFETY\_GATE\_BLOCKED

Block 이후 가능한 상태:

SUSPENDED  
REVALIDATION\_PENDING  
REAPPROVAL\_REQUIRED  
REVOKED  
MANUAL\_REVIEW\_REQUIRED

규칙:

safety-critical condition changed  
    → REAPPROVAL\_REQUIRED or REVOKED

stale but recoverable data  
    → REVALIDATION\_PENDING

external system temporarily unavailable  
    → SUSPENDED or REVALIDATION\_PENDING

approval expired  
    → REAPPROVAL\_REQUIRED

target changed  
    → REVOKED

---

## **21\. MVP Scenario: STOP\_WORK**

STOP\_WORK에서 Safety Gate는 다음 결과를 소비해야 한다.

hazard\_still\_present\_validator  
zone\_accessible\_validator  
state\_freshness\_validator  
snapshot\_freshness\_validator  
approval\_validity\_validator  
policy\_revalidation\_validator  
external\_system\_health\_validator  
adapter\_health\_validator  
idempotency\_validator  
safety\_gate\_pass\_lease\_validator  
safety\_gate\_pass\_terminal\_status\_validator

Pass 조건:

hazard condition is valid  
target zone matches  
required state is fresh  
approval is valid or emergency condition is active  
policy is valid  
external notification path is available or fallback is defined  
idempotency key is valid  
SafetyGatePass lease can be issued

Block 조건:

required safety state stale  
hazard condition unknown  
target zone mismatch  
approval invalid  
policy failed  
no valid dispatch / notification path  
duplicate STOP\_WORK execution risk

STOP\_WORK는 safety-critical action이다.

Unknown required safety condition은 block 또는 manual review로 escalate해야 한다.

---

## **22\. MVP Scenario: DISPATCH\_ROBOT**

DISPATCH\_ROBOT에서 Safety Gate는 다음 결과를 소비해야 한다.

worker\_not\_in\_robot\_path\_validator  
zone\_accessible\_validator  
robot\_available\_validator  
state\_freshness\_validator  
snapshot\_freshness\_validator  
approval\_validity\_validator  
policy\_revalidation\_validator  
external\_system\_health\_validator  
adapter\_health\_validator  
idempotency\_validator  
safety\_gate\_pass\_lease\_validator  
safety\_gate\_pass\_terminal\_status\_validator

Pass 조건:

worker is not in robot path  
zone is accessible  
robot is available  
robot capability is valid  
fleet manager is reachable  
adapter is healthy  
feedback channel is available  
approval is valid  
policy is valid  
idempotency key is valid  
SafetyGatePass lease can be issued

Block 조건:

worker in robot path  
worker location stale  
zone restricted  
robot unavailable  
robot faulted  
fleet manager unreachable  
adapter unhealthy  
approval expired  
policy failed  
duplicate robot dispatch risk

LEDO는 low-level robot motion command를 보내면 안 된다.

LEDO는 approved mission intent를 external fleet manager에 보낸다.

---

## **23\. SafetyGateResult Contract**

Safety Gate는 표준 결과를 생성한다.

SafetyGateResult  
    result\_id  
    approved\_action\_id  
    action\_type  
    status  
    issued\_pass\_ref  
    block\_ref  
    checked\_at  
    runtime\_validation\_result\_ref  
    safety\_snapshot\_ref  
    validator\_summary\_ref  
    decision\_reasons  
    failure\_reasons  
    warning\_reasons  
    suggested\_next\_state  
    trace\_id  
    correlation\_id  
    audit\_ref

가능한 status:

pass  
block  
manual\_review\_required  
hold  
requires\_revalidation  
requires\_reapproval

오직 `pass`만이 ExecutionRequest 생성을 허용한다.

---

## **24\. Audit Requirement**

모든 Safety Gate decision은 audit 가능해야 한다.

Audit 대상:

safety\_gate\_result\_id  
approved\_action\_id  
action\_type  
runtime\_validation\_result\_ref  
validator\_result\_refs  
safety\_snapshot\_ref  
TOCTOUResult ref  
SHACLValidationResult ref  
NetworkHealthResult ref  
IdempotencyResult ref  
SafetyGatePass id  
SafetyGateBlock id  
block\_reasons  
pass\_reasons  
checked\_at  
trace\_id  
correlation\_id  
audit\_ref

Safety Gate가 block한 경우, block reason은 반드시 해당 원인을 만든 validator, runtime validation result, SHACL result, network health result, idempotency result, TOCTOU result와 연결되어야 한다.

---

## **25\. Final Safety Gate Rule**

Safety Gate does not approve.  
Safety Gate does not execute.  
Safety Gate does not command.  
Safety Gate only gates execution readiness.

한글 기준:

Safety Gate는 승인하지 않는다.  
Safety Gate는 실행하지 않는다.  
Safety Gate는 명령하지 않는다.  
Safety Gate는 실행 준비 상태만 관문 처리한다.

최종 규칙:

No valid RuntimeValidationResult,  
no Safety Gate pass.

No Safety Gate pass,  
no ExecutionRequest.

No valid SafetyGatePass lease,  
no valid dispatch.

No ExecutionRequest,  
no external execution.

No audit,  
no trust.

`safety_gate/`는 `ApprovedAction`이 `ExecutionRequest`가 될 수 있는지 판단하는 최종 결정론적 runtime gate이다.

Safety Gate는 stale state, invalid validation result, TOCTOU conflict, duplicate execution, invalid structure, unhealthy external path, unsafe execution readiness로부터 LEDO를 보호한다.

