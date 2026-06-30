# **Validators**

## **1\. Purpose**

This document defines the LEDO `08_runtime_validation/validators/` area.

`validators/` is the set of individual validators that perform actual checks during Runtime Validation.

If Runtime Validation is the overall checkpoint that verifies execution-time conditions before an `ApprovedAction` becomes an `ExecutionRequest`, a Validator is the execution unit that deterministically checks one specific condition within that checkpoint.

Runtime Validation  
    \= overall pre-execution validation checkpoint

Validator  
    \= validator that checks one specific condition before execution

The core question of a Validator is:

Is this condition valid for execution right now?

A Validator does not approve.

A Validator does not execute.

A Validator does not create physical commands.

A Validator does not directly control external systems.

A Validator only produces validation results.

---

## **2\. Architectural Position**

`validators/` is the executable validation-unit area inside `08_runtime_validation/`.

Each area inside Runtime Validation is responsible for a different risk or validation concern.

toctou/  
    → defines the risk of condition changes between approval time and execution time.

shacl\_shapes/  
    → defines the structure and constraints of Runtime Validation inputs.

network\_health/  
    → defines the state of external systems, adapters, gateways, and feedback channels.

idempotency/  
    → defines risks related to duplicate execution, replay, retry, and terminal token reuse.

safety\_gate/  
    → makes the final pass/block decision based on Runtime Validation results.

validators/  
    → is the set of validators that actually check those conditions.

Therefore, Validator is not a competing concept against TOCTOU, SHACL, Network Health, Idempotency, or Safety Gate.

Validator is the tool that actually checks the conditions required by those areas.

---

## **3\. Responsibility Boundary**

The responsibility of a Validator is to check a specific runtime condition and return a standardized result.

Validator  
    → checks one specific condition.

Runtime Validation  
    → aggregates multiple ValidatorResults.

Safety Gate  
    → makes the final pass/block decision based on RuntimeValidationResult.

ExecutionRequest  
    → is bounded execution intent created after SafetyGatePass.

External System  
    → performs actual physical execution.

A `pass` result from a Validator does not directly create an `ExecutionRequest`.

Validator results are aggregated by Runtime Validation, and the Safety Gate makes the final execution-readiness decision.

---

## **4\. What Validators Do**

Validators check the following conditions:

state freshness  
snapshot freshness  
clock skew tolerance  
timestamp trust  
approval validity  
policy validity  
evidence validity  
capability availability  
worker location safety  
robot path clearance  
zone accessibility  
hazard condition  
external system health  
adapter health  
idempotency status  
SafetyGatePass lease validity  
SafetyGatePass terminal status

For each condition, a Validator returns one of the following results:

pass  
fail  
warning  
hold  
retry  
requires\_revalidation  
requires\_reapproval  
manual\_review\_required  
block

---

## **5\. What Validators Must Not Do**

A Validator must not perform the following:

create Approval  
create ApprovedAction  
create SafetyGatePass  
create ExecutionRequest  
create ExternalControlRequest  
create PhysicalCommand  
directly control external systems  
directly control robots  
directly control PLC  
directly control SCADA  
call LLM judgment  
perform non-deterministic reasoning  
perform unbounded computation

A Validator is a validator, not an executor.

A Validator is not the Safety Gate.

A Validator is not the Policy Engine.

A Validator is not an External System Adapter.

---

## **6\. Validator Input Contract**

Every Validator must have a clear input contract.

The basic input structure is:

ValidatorInput  
    validator\_id  
    validator\_version  
    action\_type  
    approved\_action\_id  
    runtime\_context\_ref  
    current\_state\_ref  
    snapshot\_ref  
    approval\_ref  
    policy\_ref  
    evidence\_ref  
    external\_system\_ref  
    adapter\_ref  
    capability\_ref  
    idempotency\_key  
    safety\_gate\_pass\_ref  
    trace\_id  
    correlation\_id

A Validator must read only the inputs it needs.

For example, `worker_not_in_robot_path_validator` reads:

worker\_location\_state  
robot\_path\_state  
zone\_state  
execution\_snapshot\_ref  
action\_scope

On the other hand, `approval_validity_validator` reads:

approval\_id  
approval\_status  
approval\_scope  
approval\_target  
approval\_expiry  
approval\_policy\_version  
approver\_identity

---

## **7\. Validator Output Contract**

Every Validator must return a standardized result.

ValidatorResult  
    result\_id  
    validator\_id  
    validator\_version  
    approved\_action\_id  
    action\_type  
    status  
    severity  
    tier  
    checked\_at  
    input\_refs  
    failure\_reasons  
    warning\_reasons  
    suggested\_next\_state  
    safety\_gate\_eligible  
    trace\_id  
    correlation\_id  
    audit\_ref

`status` must be one of the following:

pass  
fail  
warning  
hold  
retry  
requires\_revalidation  
requires\_reapproval  
manual\_review\_required  
block

`severity` is classified as:

info  
warning  
error  
critical

`tier` is classified as:

Tier 1\. Safety-Critical  
Tier 2\. Operational-Critical  
Tier 3\. Informational

---

## **8\. Validator Design Principles**

Every Validator follows these principles:

deterministic  
bounded  
auditable  
side-effect free  
fail-closed  
schema-aware  
policy-aware  
traceable  
hot-path safe

### **8.1 Deterministic**

The same input must produce the same result.

same input  
    → same ValidatorResult

A Validator must not rely on non-deterministic LLM/SLM responses.

### **8.2 Bounded**

A Validator must finish within a bounded time.

validator timeout exists  
validator execution is bounded  
validator does not wait forever

If a safety-critical Validator times out, the default result is block.

### **8.3 Side-Effect Free**

A Validator must not change the state of external systems.

Validator reads.  
Validator checks.  
Validator returns result.  
Validator does not mutate physical world.

### **8.4 Fail-Closed**

In a safety-critical path, if a Validator cannot return a clear pass, the result must be treated as block.

unknown  
    → block

timeout  
    → block

missing required input  
    → block

invalid input  
    → block

stale required state  
    → block

---

## **9\. Validator Categories**

For the MVP, Validators are divided into the following categories:

Freshness Validators  
Time Validators  
Approval / Policy Validators  
TOCTOU Validators  
Safety Validators  
Network / Adapter Validators  
Idempotency Validators  
Lease Validators

---

## **10\. Freshness Validators**

Freshness Validators check whether state and snapshot are fresh enough at execution time.

### **10.1 state\_freshness\_validator**

Validation question:

Is the current state fresh enough to execute this action?

Input:

state\_id  
state\_type  
observed\_at  
received\_at  
max\_age\_seconds  
clock\_skew\_tolerance\_ms  
source\_clock\_sync\_status

Failure handling:

stale\_state  
    → block for Tier 1

unknown\_observed\_at  
    → block for Tier 1

future\_timestamp\_beyond\_tolerance  
    → block

### **10.2 snapshot\_freshness\_validator**

Validation question:

Is the current snapshot still valid at execution time?

Input:

snapshot\_id  
snapshot\_version  
created\_at  
valid\_until  
source\_state\_versions  
action\_scope

Failure handling:

stale\_snapshot  
    → block

snapshot\_scope\_mismatch  
    → block

snapshot\_version\_conflict  
    → block

---

## **11\. Time Validators**

Time Validators check whether timestamps and clock skew are trustworthy.

### **11.1 clock\_skew\_validator**

Validation question:

Is this timestamp source within the allowable clock skew range for runtime validation?

Input:

source\_clock\_id  
source\_clock\_sync\_status  
clock\_skew\_estimate\_ms  
clock\_skew\_tolerance\_ms  
time\_source

Failure handling:

clock\_skew\_exceeded  
    → block for Tier 1

unsynchronized\_clock  
    → block or degraded trust

future\_timestamp  
    → block

### **11.2 timestamp\_trust\_validator**

Validation question:

Does this timestamp come from a trusted source?

Input:

observed\_at  
received\_at  
source\_clock\_id  
source\_clock\_sync\_status  
time\_source  
monotonic\_sequence\_id

Failure handling:

missing\_timestamp  
    → block for Tier 1

untrusted\_time\_source  
    → block or degraded trust

monotonic\_sequence\_invalid  
    → block

---

## **12\. Approval / Policy Validators**

Approval / Policy Validators check whether approval and policy are still valid at execution time.

### **12.1 approval\_validity\_validator**

Validation question:

Is this approval still valid in the current execution context?

Input:

approval\_id  
approval\_status  
approval\_scope  
approval\_target  
approval\_expiry  
approver\_identity  
approval\_policy\_version  
approved\_action\_id  
action\_type

Failure handling:

expired\_approval  
    → block

revoked\_approval  
    → block

scope\_mismatch  
    → block

target\_mismatch  
    → block

approver\_invalid  
    → block

### **12.2 policy\_revalidation\_validator**

Validation question:

Does the active policy still allow this action under current conditions?

Input:

policy\_id  
policy\_version  
policy\_status  
policy\_scope  
action\_type  
current\_state\_ref  
approved\_action\_id  
emergency\_override\_context

Failure handling:

policy\_inactive  
    → block

policy\_version\_mismatch  
    → block or re-evaluate

policy\_condition\_failed  
    → block

emergency\_condition\_expired  
    → block

---

## **13\. TOCTOU Validators**

TOCTOU Validators check whether conditions changed between approval time and execution time.

### **13.1 snapshot\_comparison\_validator**

Validation question:

Is there any safety-critical change between the approval-time snapshot and the execution-time snapshot?

Input:

approval\_snapshot\_ref  
execution\_snapshot\_ref  
action\_scope  
target\_entity  
critical\_fields

Failure handling:

critical\_field\_changed  
    → block or requires\_reapproval

snapshot\_target\_mismatch  
    → block

snapshot\_scope\_mismatch  
    → block

### **13.2 condition\_change\_validator**

Validation question:

Have execution conditions changed after approval?

Validation targets:

worker entered robot path  
worker entered hazard zone  
zone became restricted  
hazard severity increased  
robot became unavailable  
external system became unreachable  
adapter became unhealthy  
capability became unavailable

Failure handling:

condition\_changed  
    → block

condition\_changed\_but\_non\_critical  
    → warning or revalidation

condition\_unknown  
    → block

---

## **14\. Safety Validators**

Safety Validators check conditions directly related to human safety, restricted zones, robot paths, and hazards.

### **14.1 worker\_not\_in\_robot\_path\_validator**

Validation question:

Is any worker currently inside the robot path?

Input:

worker\_location\_state  
robot\_path\_state  
zone\_state  
execution\_snapshot\_ref  
action\_scope

Failure handling:

worker\_in\_robot\_path  
    → block

worker\_location\_stale  
    → block

robot\_path\_unknown  
    → block

zone\_state\_unknown  
    → block

### **14.2 zone\_accessible\_validator**

Validation question:

Is the target zone currently available for this action?

Input:

zone\_id  
zone\_status  
zone\_restriction\_status  
hazard\_status  
access\_policy  
action\_type

Failure handling:

zone\_restricted  
    → block

zone\_locked  
    → block

zone\_hazard\_active  
    → block

zone\_status\_stale  
    → block

### **14.3 hazard\_still\_present\_validator**

Validation question:

For a hazard-based action, is the hazard still present?

Input:

hazard\_id  
hazard\_type  
hazard\_status  
hazard\_severity  
observed\_at  
evidence\_ref  
zone\_id

Failure handling:

hazard\_not\_present  
    → revalidation or cancel action

hazard\_status\_stale  
    → block

hazard\_severity\_conflict  
    → manual\_review\_required or block

### **14.4 robot\_available\_validator**

Validation question:

Is the robot currently available for this mission?

Input:

robot\_id  
robot\_status  
battery\_level  
mission\_queue  
fault\_status  
capability\_status  
fleet\_manager\_status

Failure handling:

robot\_unavailable  
    → block

robot\_faulted  
    → block

robot\_battery\_low  
    → hold or block depending on action tier

conflicting\_mission\_assigned  
    → block

---

## **15\. Network / Adapter Validators**

Network / Adapter Validators check whether the external execution path is currently usable.

### **15.1 external\_system\_health\_validator**

Validation question:

Is the target external system currently reachable and healthy?

Input:

external\_system\_id  
external\_system\_status  
last\_heartbeat\_at  
health\_status  
protocol\_status  
expected\_feedback\_channel

Failure handling:

external\_system\_unreachable  
    → block

external\_system\_health\_stale  
    → block or hold

feedback\_channel\_unavailable  
    → block or hold

Important boundary:

external system reachable  
    ≠  
safe to execute

### **15.2 adapter\_health\_validator**

Validation question:

Is the adapter healthy enough to deliver the ExecutionRequest?

Input:

adapter\_id  
adapter\_status  
adapter\_version  
last\_heartbeat\_at  
latency\_ms  
error\_rate  
protocol\_compatibility

Failure handling:

adapter\_unhealthy  
    → block

adapter\_degraded  
    → hold or retry

adapter\_version\_incompatible  
    → block

adapter\_latency\_exceeded  
    → hold or block depending on tier

---

## **16\. Idempotency Validators**

Idempotency Validators prevent duplicate execution and replay.

### **16.1 idempotency\_validator**

Validation question:

Has this action or request already been processed?

Input:

idempotency\_key  
approved\_action\_id  
safety\_gate\_pass\_id  
execution\_request\_id  
external\_control\_request\_id  
previous\_result\_ref

Failure handling:

duplicate\_request\_detected  
    → return previous result or block

replayed\_old\_request  
    → block

idempotency\_key\_missing  
    → block

### **16.2 safety\_gate\_pass\_terminal\_status\_validator**

Validation question:

Is this SafetyGatePass already consumed, rejected, dropped, expired, or revoked?

Input:

safety\_gate\_pass\_id  
terminal\_status  
consumed\_at  
idempotency\_key  
trace\_id

Failure handling:

terminal\_safety\_gate\_pass\_replay  
    → block

consumed\_safety\_gate\_pass\_reuse  
    → block

revoked\_safety\_gate\_pass  
    → block

Core rule:

SafetyGatePass is consumed or terminalized on first observation.

---

## **17\. Lease Validators**

Lease Validators check whether the short validity window of a SafetyGatePass is still alive.

### **17.1 safety\_gate\_pass\_lease\_validator**

Validation question:

Is this SafetyGatePass lease still valid?

Input:

safety\_gate\_pass\_id  
issued\_at  
expires\_at  
lease\_duration\_ms  
lease\_started\_monotonic\_ms  
lease\_expires\_monotonic\_ms  
current\_monotonic\_ms  
target\_external\_system

Failure handling:

expired\_safety\_gate\_pass  
    → block

lease\_duration\_exceeded  
    → block

target\_external\_system\_mismatch  
    → block

Important rule:

No valid SafetyGatePass lease,  
no valid ExecutionRequest.

---

## **18\. Validator Execution Order**

Recommended execution order for the MVP:

1\. timestamp\_trust\_validator  
2\. clock\_skew\_validator  
3\. state\_freshness\_validator  
4\. snapshot\_freshness\_validator  
5\. approval\_validity\_validator  
6\. policy\_revalidation\_validator  
7\. snapshot\_comparison\_validator  
8\. condition\_change\_validator  
9\. worker\_not\_in\_robot\_path\_validator  
10\. zone\_accessible\_validator  
11\. hazard\_still\_present\_validator  
12\. robot\_available\_validator  
13\. external\_system\_health\_validator  
14\. adapter\_health\_validator  
15\. idempotency\_validator  
16\. safety\_gate\_pass\_lease\_validator  
17\. safety\_gate\_pass\_terminal\_status\_validator

The execution order may vary by action type.

Safety-critical Validators should run as early as possible.

If a Tier 1 block condition is detected, early block is allowed.

Tier 1 block condition detected  
    → early block allowed

However, the minimum audit record must still be preserved.

---

## **19\. Hot Path Restrictions**

In the Runtime Validation hot path, a Validator must not perform:

OWL reasoning  
Full SHACL validation  
SPARQL query  
Graph DB network call  
LLM / SLM call  
External API call without timeout  
Disk I/O  
Unbounded computation

Hot path Validators may only read:

materialized safety snapshot  
precomputed validation result  
immutable runtime context  
in-memory state cache  
bounded health cache  
idempotency ledger result  
SafetyGatePass lease state

---

## **20\. Failure Policy**

Validator failure policy depends on criticality tier.

Tier 1 failure  
    → block

Tier 2 failure  
    → hold / retry / soft revalidation / block depending on action context

Tier 3 failure  
    → warning / degraded mode

Common failure policy:

missing required input  
    → block

invalid input  
    → block

schema mismatch  
    → block

clock trust failure  
    → block for Tier 1

terminal SafetyGatePass replay  
    → block

expired SafetyGatePass  
    → block

---

## **21\. Audit Requirement**

Every Validator result must be auditable.

Audit targets:

validator\_id  
validator\_version  
approved\_action\_id  
action\_type  
input\_refs  
checked\_at  
status  
severity  
tier  
failure\_reasons  
warning\_reasons  
trace\_id  
correlation\_id  
runtime\_context\_ref  
snapshot\_ref  
policy\_ref  
approval\_ref  
evidence\_ref

If a Validator failure leads to a Safety Gate block, the following linkage must be preserved:

ValidatorResult  
    → RuntimeValidationResult  
    → SafetyGateBlock  
    → AuditRecord

---

## **22\. MVP Scenario: STOP\_WORK**

For STOP\_WORK, the main required Validators are:

timestamp\_trust\_validator  
clock\_skew\_validator  
state\_freshness\_validator  
snapshot\_freshness\_validator  
approval\_validity\_validator  
policy\_revalidation\_validator  
hazard\_still\_present\_validator  
zone\_accessible\_validator  
external\_system\_health\_validator  
adapter\_health\_validator  
idempotency\_validator  
safety\_gate\_pass\_lease\_validator  
safety\_gate\_pass\_terminal\_status\_validator

STOP\_WORK is directly related to human safety and site control, so most of its Validators should be treated as Tier 1 or Tier 2\.

---

## **23\. MVP Scenario: DISPATCH\_ROBOT**

For DISPATCH\_ROBOT, the main required Validators are:

timestamp\_trust\_validator  
clock\_skew\_validator  
state\_freshness\_validator  
snapshot\_freshness\_validator  
approval\_validity\_validator  
policy\_revalidation\_validator  
worker\_not\_in\_robot\_path\_validator  
zone\_accessible\_validator  
robot\_available\_validator  
external\_system\_health\_validator  
adapter\_health\_validator  
idempotency\_validator  
safety\_gate\_pass\_lease\_validator  
safety\_gate\_pass\_terminal\_status\_validator

For DISPATCH\_ROBOT, `worker_not_in_robot_path_validator` is a Tier 1 Safety-Critical Validator.

If a worker is inside the robot path or worker location is stale, execution must be blocked.

---

## **24\. Final Validator Rule**

Validator does not execute.  
Validator does not approve.  
Validator does not command.  
Validator only validates.

Final rules:

No valid ValidatorResult,  
no RuntimeValidationResult.

No valid RuntimeValidationResult,  
no Safety Gate pass.

No Safety Gate pass,  
no ExecutionRequest.

No ExecutionRequest,  
no external execution.

`validators/` is the actual validator set of LEDO Runtime Validation.

Each Validator deterministically checks a condition required before an `ApprovedAction` becomes an `ExecutionRequest`, and returns a standardized result that can be consumed by `RuntimeValidationResult` and the Safety Gate.

# **Runtime Validators**

## **1\. Purpose**

이 문서는 LEDO `08_runtime_validation/validators/` 영역을 정의한다.

`validators/`는 Runtime Validation 과정에서 실제 검증을 수행하는 개별 검증기 집합이다.

Runtime Validation이 `ApprovedAction`이 `ExecutionRequest`로 전환되기 전에 실행 시점 조건을 검증하는 전체 구간이라면, Validator는 그 구간 안에서 특정 조건 하나를 결정론적으로 검사하는 실행 단위이다.

Runtime Validation  
    \= 실행 직전 전체 검증 구간

Validator  
    \= 실행 직전 특정 조건을 실제로 검사하는 검증기

Validator의 핵심 질문은 다음이다.

지금 이 조건은 실행 가능한 상태인가?

Validator는 승인하지 않는다.

Validator는 실행하지 않는다.

Validator는 physical command를 만들지 않는다.

Validator는 외부 시스템을 직접 제어하지 않는다.

Validator는 오직 검증 결과를 생성한다.

---

## **2\. Architectural Position**

`validators/`는 `08_runtime_validation/` 내부의 실행 가능한 검증 단위 계층이다.

Runtime Validation 내부의 각 영역은 서로 다른 위험 또는 검증 주제를 담당한다.

toctou/  
    → 승인 시점과 실행 시점 사이의 상태 변화 위험을 정의한다.

shacl\_shapes/  
    → Runtime Validation 입력 구조와 제약 조건을 정의한다.

network\_health/  
    → 외부 시스템, adapter, gateway, feedback channel 상태를 정의한다.

idempotency/  
    → 중복 실행, replay, retry, terminal token 재사용 위험을 정의한다.

safety\_gate/  
    → Runtime Validation 결과를 기반으로 최종 pass/block을 결정한다.

validators/  
    → 위 조건들을 실제로 검사하는 검증기 집합이다.

따라서 Validator는 TOCTOU, SHACL, Network Health, Idempotency, Safety Gate와 경쟁하는 개념이 아니다.

Validator는 이 영역들이 요구하는 조건을 실제로 검사하는 도구이다.

---

## **3\. Responsibility Boundary**

Validator의 책임은 특정 runtime condition을 검사하고 표준화된 결과를 반환하는 것이다.

Validator  
    → 특정 조건을 검사한다.

Runtime Validation  
    → 여러 ValidatorResult를 조합한다.

Safety Gate  
    → RuntimeValidationResult를 기반으로 최종 pass/block을 결정한다.

ExecutionRequest  
    → SafetyGatePass 이후 생성되는 bounded execution intent이다.

External System  
    → 실제 물리 실행을 수행한다.

Validator가 `pass`를 반환했다고 해서 곧바로 `ExecutionRequest`가 생성되는 것은 아니다.

Validator 결과는 Runtime Validation에 의해 모아지고, Safety Gate가 최종적으로 실행 가능 여부를 결정한다.

---

## **4\. What Validators Do**

Validator는 다음 조건들을 검사한다.

state freshness  
snapshot freshness  
clock skew tolerance  
timestamp trust  
approval validity  
policy validity  
evidence validity  
capability availability  
worker location safety  
robot path clearance  
zone accessibility  
hazard condition  
external system health  
adapter health  
idempotency status  
SafetyGatePass lease validity  
SafetyGatePass terminal status

Validator는 각 조건에 대해 다음 중 하나의 결과를 반환한다.

pass  
fail  
warning  
hold  
retry  
requires\_revalidation  
requires\_reapproval  
manual\_review\_required  
block

---

## **5\. What Validators Must Not Do**

Validator는 다음을 수행하면 안 된다.

Approval 생성  
ApprovedAction 생성  
SafetyGatePass 생성  
ExecutionRequest 생성  
ExternalControlRequest 생성  
PhysicalCommand 생성  
외부 시스템 직접 제어  
로봇 직접 제어  
PLC 직접 제어  
SCADA 직접 제어  
LLM 판단 호출  
비결정론적 추론  
무제한 계산

Validator는 검증기이지 executor가 아니다.

Validator는 Safety Gate가 아니다.

Validator는 Policy Engine이 아니다.

Validator는 External System Adapter가 아니다.

---

## **6\. Validator Input Contract**

모든 Validator는 명확한 입력 계약을 가져야 한다.

기본 입력 구조는 다음과 같다.

ValidatorInput  
    validator\_id  
    validator\_version  
    action\_type  
    approved\_action\_id  
    runtime\_context\_ref  
    current\_state\_ref  
    snapshot\_ref  
    approval\_ref  
    policy\_ref  
    evidence\_ref  
    external\_system\_ref  
    adapter\_ref  
    capability\_ref  
    idempotency\_key  
    safety\_gate\_pass\_ref  
    trace\_id  
    correlation\_id

Validator는 자신이 필요한 입력만 읽어야 한다.

예를 들어 `worker_not_in_robot_path_validator`는 다음 입력을 읽는다.

worker\_location\_state  
robot\_path\_state  
zone\_state  
execution\_snapshot\_ref  
action\_scope

반면 `approval_validity_validator`는 다음 입력을 읽는다.

approval\_id  
approval\_status  
approval\_scope  
approval\_target  
approval\_expiry  
approval\_policy\_version  
approver\_identity

---

## **7\. Validator Output Contract**

모든 Validator는 표준 결과를 반환해야 한다.

ValidatorResult  
    result\_id  
    validator\_id  
    validator\_version  
    approved\_action\_id  
    action\_type  
    status  
    severity  
    tier  
    checked\_at  
    input\_refs  
    failure\_reasons  
    warning\_reasons  
    suggested\_next\_state  
    safety\_gate\_eligible  
    trace\_id  
    correlation\_id  
    audit\_ref

`status`는 다음 중 하나여야 한다.

pass  
fail  
warning  
hold  
retry  
requires\_revalidation  
requires\_reapproval  
manual\_review\_required  
block

`severity`는 다음과 같이 분류한다.

info  
warning  
error  
critical

`tier`는 다음과 같이 분류한다.

Tier 1\. Safety-Critical  
Tier 2\. Operational-Critical  
Tier 3\. Informational

---

## **8\. Validator Design Principles**

모든 Validator는 다음 원칙을 따른다.

deterministic  
bounded  
auditable  
side-effect free  
fail-closed  
schema-aware  
policy-aware  
traceable  
hot-path safe

### **8.1 Deterministic**

같은 입력이 들어오면 같은 결과를 반환해야 한다.

same input  
    → same ValidatorResult

Validator는 LLM/SLM의 비결정론적 응답에 의존하면 안 된다.

### **8.2 Bounded**

Validator는 제한된 시간 안에 종료되어야 한다.

validator timeout exists  
validator execution is bounded  
validator does not wait forever

Safety-critical validator가 timeout되면 기본값은 block이다.

### **8.3 Side-Effect Free**

Validator는 외부 시스템 상태를 변경하면 안 된다.

Validator reads.  
Validator checks.  
Validator returns result.  
Validator does not mutate physical world.

### **8.4 Fail-Closed**

Safety-critical path에서 Validator가 확실한 pass를 반환하지 못하면 block으로 처리한다.

unknown  
    → block

timeout  
    → block

missing required input  
    → block

invalid input  
    → block

stale required state  
    → block

---

## **9\. Validator Categories**

MVP 기준 Validator는 다음 범주로 나눈다.

Freshness Validators  
Time Validators  
Approval / Policy Validators  
TOCTOU Validators  
Safety Validators  
Network / Adapter Validators  
Idempotency Validators  
Lease Validators

---

## **10\. Freshness Validators**

Freshness Validator는 state와 snapshot이 실행 시점에 충분히 최신인지 검사한다.

### **10.1 state\_freshness\_validator**

검증 질문:

현재 state는 이 action을 실행하기에 충분히 fresh한가?

입력:

state\_id  
state\_type  
observed\_at  
received\_at  
max\_age\_seconds  
clock\_skew\_tolerance\_ms  
source\_clock\_sync\_status

실패 처리:

stale\_state  
    → Tier 1에서는 block

unknown\_observed\_at  
    → Tier 1에서는 block

future\_timestamp\_beyond\_tolerance  
    → block

### **10.2 snapshot\_freshness\_validator**

검증 질문:

현재 snapshot은 실행 시점에 여전히 유효한가?

입력:

snapshot\_id  
snapshot\_version  
created\_at  
valid\_until  
source\_state\_versions  
action\_scope

실패 처리:

stale\_snapshot  
    → block

snapshot\_scope\_mismatch  
    → block

snapshot\_version\_conflict  
    → block

---

## **11\. Time Validators**

Time Validator는 timestamp와 clock skew가 신뢰 가능한지 검사한다.

### **11.1 clock\_skew\_validator**

검증 질문:

이 timestamp source는 runtime validation에 사용할 만큼 시계 오차가 허용 범위 안에 있는가?

입력:

source\_clock\_id  
source\_clock\_sync\_status  
clock\_skew\_estimate\_ms  
clock\_skew\_tolerance\_ms  
time\_source

실패 처리:

clock\_skew\_exceeded  
    → Tier 1에서는 block

unsynchronized\_clock  
    → block or degraded trust

future\_timestamp  
    → block

### **11.2 timestamp\_trust\_validator**

검증 질문:

이 timestamp는 신뢰 가능한 source에서 온 것인가?

입력:

observed\_at  
received\_at  
source\_clock\_id  
source\_clock\_sync\_status  
time\_source  
monotonic\_sequence\_id

실패 처리:

missing\_timestamp  
    → Tier 1에서는 block

untrusted\_time\_source  
    → block or degraded trust

monotonic\_sequence\_invalid  
    → block

---

## **12\. Approval / Policy Validators**

Approval / Policy Validator는 승인과 정책이 실행 시점에도 유효한지 검사한다.

### **12.1 approval\_validity\_validator**

검증 질문:

이 approval은 현재 execution context에서 여전히 유효한가?

입력:

approval\_id  
approval\_status  
approval\_scope  
approval\_target  
approval\_expiry  
approver\_identity  
approval\_policy\_version  
approved\_action\_id  
action\_type

실패 처리:

expired\_approval  
    → block

revoked\_approval  
    → block

scope\_mismatch  
    → block

target\_mismatch  
    → block

approver\_invalid  
    → block

### **12.2 policy\_revalidation\_validator**

검증 질문:

현재 활성 policy는 현재 조건에서 이 action을 여전히 허용하는가?

입력:

policy\_id  
policy\_version  
policy\_status  
policy\_scope  
action\_type  
current\_state\_ref  
approved\_action\_id  
emergency\_override\_context

실패 처리:

policy\_inactive  
    → block

policy\_version\_mismatch  
    → block or re-evaluate

policy\_condition\_failed  
    → block

emergency\_condition\_expired  
    → block

---

## **13\. TOCTOU Validators**

TOCTOU Validator는 승인 시점과 실행 시점 사이에 상태가 바뀌었는지 검사한다.

### **13.1 snapshot\_comparison\_validator**

검증 질문:

approval-time snapshot과 execution-time snapshot 사이에 safety-critical change가 있는가?

입력:

approval\_snapshot\_ref  
execution\_snapshot\_ref  
action\_scope  
target\_entity  
critical\_fields

실패 처리:

critical\_field\_changed  
    → block or requires\_reapproval

snapshot\_target\_mismatch  
    → block

snapshot\_scope\_mismatch  
    → block

### **13.2 condition\_change\_validator**

검증 질문:

승인 이후 실행 조건이 바뀌었는가?

검사 대상:

worker entered robot path  
worker entered hazard zone  
zone became restricted  
hazard severity increased  
robot became unavailable  
external system became unreachable  
adapter became unhealthy  
capability became unavailable

실패 처리:

condition\_changed  
    → block

condition\_changed\_but\_non\_critical  
    → warning or revalidation

condition\_unknown  
    → block

---

## **14\. Safety Validators**

Safety Validator는 사람 안전, 위험구역, 로봇 경로, hazard와 직접 연결된 조건을 검사한다.

### **14.1 worker\_not\_in\_robot\_path\_validator**

검증 질문:

현재 작업자가 robot path 안에 있는가?

입력:

worker\_location\_state  
robot\_path\_state  
zone\_state  
execution\_snapshot\_ref  
action\_scope

실패 처리:

worker\_in\_robot\_path  
    → block

worker\_location\_stale  
    → block

robot\_path\_unknown  
    → block

zone\_state\_unknown  
    → block

### **14.2 zone\_accessible\_validator**

검증 질문:

target zone은 현재 이 action을 수행할 수 있는 상태인가?

입력:

zone\_id  
zone\_status  
zone\_restriction\_status  
hazard\_status  
access\_policy  
action\_type

실패 처리:

zone\_restricted  
    → block

zone\_locked  
    → block

zone\_hazard\_active  
    → block

zone\_status\_stale  
    → block

### **14.3 hazard\_still\_present\_validator**

검증 질문:

hazard 기반 action에서 해당 hazard가 아직 존재하는가?

입력:

hazard\_id  
hazard\_type  
hazard\_status  
hazard\_severity  
observed\_at  
evidence\_ref  
zone\_id

실패 처리:

hazard\_not\_present  
    → revalidation or cancel action

hazard\_status\_stale  
    → block

hazard\_severity\_conflict  
    → manual\_review\_required or block

### **14.4 robot\_available\_validator**

검증 질문:

robot은 현재 mission 수행 가능한 상태인가?

입력:

robot\_id  
robot\_status  
battery\_level  
mission\_queue  
fault\_status  
capability\_status  
fleet\_manager\_status

실패 처리:

robot\_unavailable  
    → block

robot\_faulted  
    → block

robot\_battery\_low  
    → hold or block depending on action tier

conflicting\_mission\_assigned  
    → block

---

## **15\. Network / Adapter Validators**

Network / Adapter Validator는 외부 실행 경로가 현재 사용할 수 있는지 검사한다.

### **15.1 external\_system\_health\_validator**

검증 질문:

target external system은 현재 reachable하고 healthy한가?

입력:

external\_system\_id  
external\_system\_status  
last\_heartbeat\_at  
health\_status  
protocol\_status  
expected\_feedback\_channel

실패 처리:

external\_system\_unreachable  
    → block

external\_system\_health\_stale  
    → block or hold

feedback\_channel\_unavailable  
    → block or hold

주의:

external system reachable  
    ≠  
safe to execute

### **15.2 adapter\_health\_validator**

검증 질문:

adapter는 ExecutionRequest를 전달할 만큼 정상인가?

입력:

adapter\_id  
adapter\_status  
adapter\_version  
last\_heartbeat\_at  
latency\_ms  
error\_rate  
protocol\_compatibility

실패 처리:

adapter\_unhealthy  
    → block

adapter\_degraded  
    → hold or retry

adapter\_version\_incompatible  
    → block

adapter\_latency\_exceeded  
    → hold or block depending on tier

---

## **16\. Idempotency Validators**

Idempotency Validator는 중복 실행과 replay를 방지한다.

### **16.1 idempotency\_validator**

검증 질문:

이 action 또는 request는 이미 처리된 적이 있는가?

입력:

idempotency\_key  
approved\_action\_id  
safety\_gate\_pass\_id  
execution\_request\_id  
external\_control\_request\_id  
previous\_result\_ref

실패 처리:

duplicate\_request\_detected  
    → return previous result or block

replayed\_old\_request  
    → block

idempotency\_key\_missing  
    → block

### **16.2 safety\_gate\_pass\_terminal\_status\_validator**

검증 질문:

이 SafetyGatePass는 이미 consumed, rejected, dropped, expired, revoked 상태인가?

입력:

safety\_gate\_pass\_id  
terminal\_status  
consumed\_at  
idempotency\_key  
trace\_id

실패 처리:

terminal\_safety\_gate\_pass\_replay  
    → block

consumed\_safety\_gate\_pass\_reuse  
    → block

revoked\_safety\_gate\_pass  
    → block

핵심 규칙:

SafetyGatePass is consumed or terminalized on first observation.

---

## **17\. Lease Validators**

Lease Validator는 SafetyGatePass의 짧은 유효기간이 아직 살아 있는지 검사한다.

### **17.1 safety\_gate\_pass\_lease\_validator**

검증 질문:

이 SafetyGatePass lease는 아직 유효한가?

입력:

safety\_gate\_pass\_id  
issued\_at  
expires\_at  
lease\_duration\_ms  
lease\_started\_monotonic\_ms  
lease\_expires\_monotonic\_ms  
current\_monotonic\_ms  
target\_external\_system

실패 처리:

expired\_safety\_gate\_pass  
    → block

lease\_duration\_exceeded  
    → block

target\_external\_system\_mismatch  
    → block

중요 규칙:

No valid SafetyGatePass lease,  
no valid ExecutionRequest.

---

## **18\. Validator Execution Order**

MVP 기준 권장 실행 순서는 다음과 같다.

1\. timestamp\_trust\_validator  
2\. clock\_skew\_validator  
3\. state\_freshness\_validator  
4\. snapshot\_freshness\_validator  
5\. approval\_validity\_validator  
6\. policy\_revalidation\_validator  
7\. snapshot\_comparison\_validator  
8\. condition\_change\_validator  
9\. worker\_not\_in\_robot\_path\_validator  
10\. zone\_accessible\_validator  
11\. hazard\_still\_present\_validator  
12\. robot\_available\_validator  
13\. external\_system\_health\_validator  
14\. adapter\_health\_validator  
15\. idempotency\_validator  
16\. safety\_gate\_pass\_lease\_validator  
17\. safety\_gate\_pass\_terminal\_status\_validator

실행 순서는 action type에 따라 달라질 수 있다.

Safety-critical validator는 가능한 한 빠르게 실행되어야 한다.

Tier 1 block 조건이 발견되면 early block이 가능하다.

Tier 1 block condition detected  
    → early block allowed

단, audit에 필요한 최소 기록은 반드시 남겨야 한다.

---

## **19\. Hot Path Restrictions**

Runtime Validation hot path에서 Validator는 다음을 수행하면 안 된다.

OWL reasoning  
Full SHACL validation  
SPARQL query  
Graph DB network call  
LLM / SLM call  
External API call without timeout  
Disk I/O  
Unbounded computation

Hot path Validator는 다음만 읽어야 한다.

materialized safety snapshot  
precomputed validation result  
immutable runtime context  
in-memory state cache  
bounded health cache  
idempotency ledger result  
SafetyGatePass lease state

---

## **20\. Failure Policy**

Validator 실패 정책은 criticality tier에 따라 다르다.

Tier 1 failure  
    → block

Tier 2 failure  
    → hold / retry / soft revalidation / block depending on action context

Tier 3 failure  
    → warning / degraded mode

공통 실패 정책:

missing required input  
    → block

invalid input  
    → block

schema mismatch  
    → block

clock trust failure  
    → Tier 1에서는 block

terminal SafetyGatePass replay  
    → block

expired SafetyGatePass  
    → block

---

## **21\. Audit Requirement**

모든 Validator 결과는 audit 가능해야 한다.

Audit 대상:

validator\_id  
validator\_version  
approved\_action\_id  
action\_type  
input\_refs  
checked\_at  
status  
severity  
tier  
failure\_reasons  
warning\_reasons  
trace\_id  
correlation\_id  
runtime\_context\_ref  
snapshot\_ref  
policy\_ref  
approval\_ref  
evidence\_ref

Validator 실패가 Safety Gate block으로 이어진 경우 다음 연결이 보존되어야 한다.

ValidatorResult  
    → RuntimeValidationResult  
    → SafetyGateBlock  
    → AuditRecord

---

## **22\. MVP Scenario: STOP\_WORK**

STOP\_WORK에서 필요한 주요 Validator는 다음과 같다.

timestamp\_trust\_validator  
clock\_skew\_validator  
state\_freshness\_validator  
snapshot\_freshness\_validator  
approval\_validity\_validator  
policy\_revalidation\_validator  
hazard\_still\_present\_validator  
zone\_accessible\_validator  
external\_system\_health\_validator  
adapter\_health\_validator  
idempotency\_validator  
safety\_gate\_pass\_lease\_validator  
safety\_gate\_pass\_terminal\_status\_validator

STOP\_WORK는 사람 안전과 현장 통제에 직접 연결되므로 대부분 Tier 1 또는 Tier 2로 처리한다.

---

## **23\. MVP Scenario: DISPATCH\_ROBOT**

DISPATCH\_ROBOT에서 필요한 주요 Validator는 다음과 같다.

timestamp\_trust\_validator  
clock\_skew\_validator  
state\_freshness\_validator  
snapshot\_freshness\_validator  
approval\_validity\_validator  
policy\_revalidation\_validator  
worker\_not\_in\_robot\_path\_validator  
zone\_accessible\_validator  
robot\_available\_validator  
external\_system\_health\_validator  
adapter\_health\_validator  
idempotency\_validator  
safety\_gate\_pass\_lease\_validator  
safety\_gate\_pass\_terminal\_status\_validator

DISPATCH\_ROBOT에서 `worker_not_in_robot_path_validator`는 Tier 1 Safety-Critical validator이다.

Robot path에 worker가 있거나 worker location이 stale하면 실행은 block되어야 한다.

---

## **24\. Final Validator Rule**

Validator does not execute.  
Validator does not approve.  
Validator does not command.  
Validator only validates.

한글 기준:

Validator는 실행하지 않는다.  
Validator는 승인하지 않는다.  
Validator는 명령하지 않는다.  
Validator는 검증만 한다.

최종 규칙:

No valid ValidatorResult,  
no RuntimeValidationResult.

No valid RuntimeValidationResult,  
no Safety Gate pass.

No Safety Gate pass,  
no ExecutionRequest.

No ExecutionRequest,  
no external execution.

`validators/`는 LEDO Runtime Validation의 실제 검증기 집합이다.

각 Validator는 ApprovedAction이 ExecutionRequest로 넘어가기 전에 필요한 조건을 결정론적으로 검사하고, 그 결과를 RuntimeValidationResult와 Safety Gate가 사용할 수 있도록 표준화된 형태로 반환한다.

