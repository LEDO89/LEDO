# **Network Health**

## **1\. Purpose**

This document defines the LEDO `08_runtime_validation/network_health/` area.

`network_health/` defines the health model and validation rules used to check the current state of external systems, adapters, gateways, fleet managers, notification systems, and feedback channels during Runtime Validation.

LEDO does not perform physical execution directly.

LEDO sends an `ExecutionRequest` to an external system, and the external system performs the actual physical execution.

Therefore, before an `ApprovedAction` becomes an `ExecutionRequest`, LEDO must verify whether the external execution path is currently usable.

The core principle is:

network reachable  
    ≠  
safe to execute

A reachable network does not mean execution is safe.

Network Health is only one input to Runtime Validation and does not automatically imply Safety Gate pass.

---

## **2\. Architectural Position**

`network_health/` defines the state of the external execution path inside `08_runtime_validation/`.

ApprovedAction  
    ↓  
Runtime Validation  
    ↓  
NetworkHealthResult  
    ↓  
ValidatorResult  
    ↓  
RuntimeValidationResult  
    ↓  
Safety Gate  
    ↓  
SafetyGatePass or SafetyGateBlock

`network_health/` does not directly mean the actual validators.

The actual checks are performed by the following validators in `validators/`:

external\_system\_health\_validator  
adapter\_health\_validator  
feedback\_channel\_validator  
heartbeat\_freshness\_validator  
circuit\_breaker\_status\_validator

Therefore, `network_health/` defines health rules, health status, heartbeat, timeout, retry, circuit breaker, and degraded mode, while `validators/` actually checks them.

---

## **3\. Responsibility Boundary**

The responsibilities of `network_health/` are:

define external system health model  
define adapter health model  
define heartbeat freshness rule  
define timeout rule  
define retry rule  
define circuit breaker state  
define feedback channel availability  
define degraded mode rule  
define NetworkHealthResult contract

`network_health/` does not perform:

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
make Safety Gate pass/block decision

Network Health reports the current state of the external execution path.

The Safety Gate makes the final execution-readiness decision.

---

## **4\. Why Network Health Is Needed**

Runtime Validation must verify execution paths connected to external systems.

If an external system is unreachable or an adapter is unhealthy, the ExecutionRequest may not be delivered, may be delivered incorrectly, or may not return feedback.

Examples:

Fleet Manager unreachable  
PLC gateway timeout  
SCADA connector degraded  
adapter version incompatible  
notification system unavailable  
feedback channel missing  
heartbeat stale  
circuit breaker open

Creating an ExecutionRequest under these conditions may break the closed loop.

Core principle:

No reliable external path,  
no reliable execution feedback.

---

## **5\. Network Health vs Safety**

Network Health is only one input to safety judgment.

Network Health  
    → checks whether the external execution path is currently usable.

Validator  
    → checks whether the health state satisfies action requirements.

Safety Gate  
    → makes the final pass/block decision based on the full Runtime Validation result.

Example:

external system reachable  
adapter healthy  
feedback channel available

Even if all of the above are true, execution is not automatically allowed.

The following conditions must also be validated:

worker\_not\_in\_robot\_path  
zone\_accessible  
approval\_valid  
policy\_valid  
snapshot\_fresh  
idempotency\_valid  
SafetyGatePass lease valid

---

## **6\. Health Targets**

For the MVP, `network_health/` targets the following:

external system  
adapter  
robot fleet manager  
PLC gateway  
SCADA connector  
notification system  
site operation system  
feedback channel  
heartbeat stream

Each target must be registered in the registry, and the action type must match the target external system.

---

## **7\. Health Status Model**

Network Health status may use the following values:

healthy  
degraded  
unreachable  
timeout  
circuit\_open  
unknown

State meanings:

healthy  
    → usable normally

degraded  
    → usable, but with reduced performance or reliability

unreachable  
    → not reachable

timeout  
    → response time exceeded the allowed threshold

circuit\_open  
    → requests are blocked due to repeated failures

unknown  
    → current state cannot be determined

Handling rules:

healthy  
    → usable as validation input

degraded  
    → hold / retry / degraded mode

unreachable  
    → block safety-critical action

timeout  
    → retry or block depending on tier

circuit\_open  
    → no dispatch

unknown  
    → block for Tier 1

---

## **8\. External System Health Rule**

External System Health verifies whether the target external system can currently receive the execution request.

Validation targets:

external\_system\_id  
external\_system\_type  
external\_system\_status  
last\_heartbeat\_at  
health\_status  
protocol\_status  
expected\_feedback\_channel  
registered\_action\_types

Validation rules:

external\_system\_id must exist  
external\_system must be registered  
external\_system must be active  
health\_status must not be unreachable  
last\_heartbeat must be fresh  
target action type must be supported  
expected feedback channel must exist

Failure handling:

external\_system\_unregistered  
    → block

external\_system\_inactive  
    → block

external\_system\_unreachable  
    → block

external\_system\_health\_stale  
    → block or hold depending on tier

unsupported\_action\_type  
    → block

---

## **9\. Adapter Health Rule**

Adapter Health verifies whether the adapter between LEDO and the external system is currently usable.

Validation targets:

adapter\_id  
adapter\_status  
adapter\_version  
last\_heartbeat\_at  
latency\_ms  
error\_rate  
protocol\_compatibility  
target\_external\_system

Validation rules:

adapter must be registered  
adapter must be active  
adapter version must be compatible  
adapter heartbeat must be fresh  
adapter latency must be within threshold  
adapter error rate must be within threshold  
protocol must be compatible

Failure handling:

adapter\_unregistered  
    → block

adapter\_inactive  
    → block

adapter\_unhealthy  
    → block

adapter\_degraded  
    → hold or retry

adapter\_version\_incompatible  
    → block

adapter\_latency\_exceeded  
    → hold or block depending on tier

---

## **10\. Heartbeat Freshness Rule**

Network Health must check heartbeat freshness.

Basic validation rule:

current\_time \- last\_heartbeat\_at \<= max\_heartbeat\_age

Clock skew tolerance must be applied.

current\_time \- last\_heartbeat\_at  
    \<= max\_heartbeat\_age \+ clock\_skew\_tolerance

Failure handling:

heartbeat\_stale  
    → block or hold depending on tier

heartbeat\_missing  
    → block

heartbeat\_future\_timestamp  
    → block

For safety-critical actions, stale heartbeat defaults to block.

---

## **11\. Timeout Rule**

If the external system or adapter response does not arrive within the allowed time, it is treated as timeout.

response\_time\_ms \> timeout\_ms  
    → timeout

Handling rules:

Tier 1 timeout  
    → block

Tier 2 timeout  
    → retry / hold / degraded mode

Tier 3 timeout  
    → warning

Timeout must not wait indefinitely.

No unbounded wait.

---

## **12\. Retry Rule**

Retry may be allowed, but it must be bounded.

retry\_count \<= max\_retry\_count  
retry\_interval\_ms is bounded  
retry must preserve idempotency\_key  
retry must not create duplicate physical execution

Failure handling:

retry\_exhausted  
    → block or hold

retry\_without\_idempotency\_key  
    → block

retry\_creates\_duplicate\_execution\_risk  
    → block

Important principles:

Retry must not bypass Runtime Validation.  
Retry must not bypass Safety Gate.  
Retry must not create duplicate physical execution.

---

## **13\. Circuit Breaker Rule**

When repeated failures occur, the circuit breaker must open and block downstream requests.

States:

closed  
open  
half\_open

State meanings:

closed  
    → normal requests allowed

open  
    → requests blocked

half\_open  
    → limited probes allowed

Example transitions:

repeated failure  
    → circuit\_open

cooldown elapsed  
    → half\_open

probe success  
    → closed

probe failure  
    → open

For safety-critical actions, dispatch must not be sent to an external system whose circuit is open.

circuit\_open  
    → no dispatch

---

## **14\. Feedback Channel Rule**

Before sending an ExecutionRequest to an external system, the feedback channel must also be available.

The feedback channel is required to receive execution results and maintain the closed loop.

No feedback channel,  
no reliable closed loop.

Validation targets:

feedback\_channel\_id  
feedback\_channel\_status  
last\_feedback\_received\_at  
expected\_feedback\_type  
correlation\_id\_support  
trace\_id\_support

Failure handling:

feedback\_channel\_missing  
    → block or hold

feedback\_channel\_unavailable  
    → block or hold

feedback\_correlation\_not\_supported  
    → block

feedback\_channel\_stale  
    → hold or block depending on tier

---

## **15\. Degraded Mode Rule**

Some external systems or adapters may be degraded.

A degraded state does not always mean block.

degraded  
    → hold / retry / limited execution / manual review

However, for safety-critical actions, degraded must not be treated as allow by default.

Tier 1 degraded  
    → block or manual review

Tier 2 degraded  
    → hold / retry / limited execution

Tier 3 degraded  
    → warning

Degraded mode is determined by policy and action context.

---

## **16\. NetworkHealthResult Contract**

`network_health/` must produce a standardized result.

NetworkHealthResult  
    result\_id  
    external\_system\_id  
    adapter\_id  
    health\_status  
    heartbeat\_status  
    latency\_ms  
    error\_rate  
    circuit\_breaker\_status  
    feedback\_channel\_status  
    checked\_at  
    status  
    failure\_reasons  
    warning\_reasons  
    tier  
    trace\_id  
    correlation\_id  
    audit\_ref

Possible statuses:

pass  
warning  
hold  
retry  
block  
unknown

---

## **17\. Validator Relation**

Network Health itself defines health rules and results.

Actual validation is performed by Validators.

Main Validators:

external\_system\_health\_validator  
adapter\_health\_validator  
heartbeat\_freshness\_validator  
feedback\_channel\_validator  
circuit\_breaker\_status\_validator

Validator results are aggregated into RuntimeValidationResult.

NetworkHealthResult  
    ↓  
ValidatorResult  
    ↓  
RuntimeValidationResult  
    ↓  
SafetyGateResult

---

## **18\. Hot Path Rule**

The runtime hot path must not perform unbounded external API calls.

Network Health should be precomputed or provided through bounded cache where possible.

Forbidden:

unbounded external API call  
unbounded health probe  
blocking network call without timeout  
direct graph DB network lookup  
LLM-based health judgment  
disk I/O in hot path

Allowed:

bounded health cache  
precomputed NetworkHealthResult  
heartbeat materialized status  
circuit breaker state  
adapter health snapshot  
external system health snapshot

Core rule:

Hot path reads bounded health result.  
Hot path does not perform unbounded health discovery.

---

## **19\. MVP Scenario: STOP\_WORK**

For STOP\_WORK, required Network Health checks are:

notification system reachable  
site operation system reachable  
feedback channel available  
adapter healthy  
heartbeat fresh  
idempotency key available

Failure handling:

notification system unreachable  
    → hold or fallback channel

site operation system unreachable  
    → block or manual escalation

feedback channel unavailable  
    → hold or manual escalation

adapter unhealthy  
    → block or fallback adapter

STOP\_WORK is a safety-critical action, so fallback path and manual escalation policy must be defined.

---

## **20\. MVP Scenario: DISPATCH\_ROBOT**

For DISPATCH\_ROBOT, required Network Health checks are:

robot fleet manager reachable  
fleet manager heartbeat fresh  
robot adapter healthy  
adapter latency within limit  
feedback channel available  
circuit breaker closed

Failure handling:

fleet\_manager\_unreachable  
    → block

robot\_adapter\_unhealthy  
    → block

adapter\_latency\_exceeded  
    → hold or block

feedback\_channel\_unavailable  
    → block or hold

circuit\_open  
    → block

For DISPATCH\_ROBOT, the external Fleet Manager performs the actual robot execution.

LEDO does not send low-level robot motion commands.

---

## **21\. Audit Requirement**

Every Network Health result must be auditable.

Audit targets:

external\_system\_id  
adapter\_id  
health\_status  
heartbeat\_status  
last\_heartbeat\_at  
latency\_ms  
error\_rate  
circuit\_breaker\_status  
feedback\_channel\_status  
checked\_at  
failure\_reasons  
warning\_reasons  
trace\_id  
correlation\_id  
audit\_ref

If a Network Health failure leads to a Safety Gate block, the following linkage must be preserved:

NetworkHealthResult  
    → ValidatorResult  
    → RuntimeValidationResult  
    → SafetyGateBlock  
    → AuditRecord

---

## **22\. Final Network Health Rule**

Network reachable  
does not mean  
safe to execute.

Final rules:

No healthy external path,  
no reliable dispatch.

No feedback channel,  
no closed loop.

No valid NetworkHealthResult,  
no RuntimeValidationResult.

No RuntimeValidationResult,  
no Safety Gate pass.

No Safety Gate pass,  
no ExecutionRequest.

`network_health/` defines the health model and rules for verifying current usability, reliability, responsiveness, and feedback availability of the external execution path during LEDO Runtime Validation.

Network Health is not Safety Gate pass.

Network Health is runtime validation input consumed by the Safety Gate.

# **Network Health**

## **1\. 목적**

이 문서는 LEDO `08_runtime_validation/network_health/` 영역을 정의한다.

`network_health/`는 Runtime Validation 과정에서 외부 시스템, adapter, gateway, fleet manager, notification system, feedback channel의 현재 상태를 확인하기 위한 health model과 validation rule을 정의한다.

LEDO는 직접 물리 실행을 수행하지 않는다.

LEDO는 `ExecutionRequest`를 외부 시스템에 전달하고, 외부 시스템이 실제 물리 실행을 수행한다.

따라서 `ApprovedAction`이 `ExecutionRequest`로 전환되기 전에 외부 실행 경로가 현재 사용할 수 있는 상태인지 확인해야 한다.

핵심 원칙은 다음과 같다.

network reachable  
    ≠  
safe to execute

즉, 네트워크가 연결되어 있다는 사실은 실행해도 안전하다는 뜻이 아니다.

Network Health는 Runtime Validation의 입력 중 하나이며, Safety Gate pass를 자동으로 의미하지 않는다.

---

## **2\. Architectural Position**

`network_health/`는 `08_runtime_validation/` 내부에서 외부 실행 경로의 상태를 정의한다.

ApprovedAction  
    ↓  
Runtime Validation  
    ↓  
NetworkHealthResult  
    ↓  
ValidatorResult  
    ↓  
RuntimeValidationResult  
    ↓  
Safety Gate  
    ↓  
SafetyGatePass or SafetyGateBlock

`network_health/`는 실제 검증기를 직접 의미하지 않는다.

실제 검사는 `validators/`의 다음 validator들이 수행한다.

external\_system\_health\_validator  
adapter\_health\_validator  
feedback\_channel\_validator  
heartbeat\_freshness\_validator  
circuit\_breaker\_status\_validator

따라서 `network_health/`는 health rule, health status, heartbeat, timeout, retry, circuit breaker, degraded mode를 정의하고, `validators/`는 이를 실제로 검사한다.

---

## **3\. Responsibility Boundary**

`network_health/`의 책임은 다음과 같다.

external system health model 정의  
adapter health model 정의  
heartbeat freshness rule 정의  
timeout rule 정의  
retry rule 정의  
circuit breaker state 정의  
feedback channel availability 정의  
degraded mode rule 정의  
network health result contract 정의

`network_health/`는 다음을 하지 않는다.

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
Safety Gate pass/block 직접 결정

Network Health는 외부 실행 경로의 현재 상태를 알려준다.

최종 실행 가능 여부는 Safety Gate가 결정한다.

---

## **4\. Why Network Health Is Needed**

Runtime Validation은 외부 시스템과 연결된 execution path를 검증해야 한다.

외부 시스템이 unreachable이거나 adapter가 unhealthy하면 ExecutionRequest가 전달되지 않거나, 잘못 전달되거나, feedback을 받을 수 없다.

예시:

Fleet Manager unreachable  
PLC gateway timeout  
SCADA connector degraded  
adapter version incompatible  
notification system unavailable  
feedback channel missing  
heartbeat stale  
circuit breaker open

이런 상태에서 ExecutionRequest를 생성하면 closed loop가 깨질 수 있다.

핵심 원칙:

No reliable external path,  
no reliable execution feedback.

한글 기준:

신뢰 가능한 외부 실행 경로가 없으면  
신뢰 가능한 실행 피드백도 없다.

---

## **5\. Network Health vs Safety**

Network Health는 안전 판단의 일부 입력일 뿐이다.

Network Health  
    → 외부 실행 경로가 현재 사용 가능한지 확인한다.

Validator  
    → health 상태가 action 조건에 맞는지 검사한다.

Safety Gate  
    → 전체 Runtime Validation 결과를 기반으로 최종 pass/block을 결정한다.

예시:

external system reachable  
adapter healthy  
feedback channel available

위 조건이 모두 true여도 이것만으로 실행은 허용되지 않는다.

다음 조건들도 함께 검증되어야 한다.

worker\_not\_in\_robot\_path  
zone\_accessible  
approval\_valid  
policy\_valid  
snapshot\_fresh  
idempotency\_valid  
SafetyGatePass lease valid

---

## **6\. Health Targets**

MVP 기준 `network_health/`의 검증 대상은 다음과 같다.

external system  
adapter  
robot fleet manager  
PLC gateway  
SCADA connector  
notification system  
site operation system  
feedback channel  
heartbeat stream

각 대상은 registry에 등록되어 있어야 하며, action type과 target external system이 일치해야 한다.

---

## **7\. Health Status Model**

Network Health status는 다음 값을 사용할 수 있다.

healthy  
degraded  
unreachable  
timeout  
circuit\_open  
unknown

상태 의미:

healthy  
    → 정상적으로 사용 가능한 상태

degraded  
    → 사용은 가능하지만 성능 또는 신뢰성이 낮은 상태

unreachable  
    → 연결 불가 상태

timeout  
    → 응답 시간이 허용 범위를 초과한 상태

circuit\_open  
    → 반복 실패로 인해 요청 차단 상태

unknown  
    → 현재 상태를 판단할 수 없는 상태

처리 원칙:

healthy  
    → validation input으로 사용 가능

degraded  
    → hold / retry / degraded mode 가능

unreachable  
    → safety-critical action block

timeout  
    → tier에 따라 retry 또는 block

circuit\_open  
    → dispatch 금지

unknown  
    → Tier 1에서는 block

---

## **8\. External System Health Rule**

External System Health는 target external system이 현재 실행 요청을 받을 수 있는지 확인한다.

검증 대상:

external\_system\_id  
external\_system\_type  
external\_system\_status  
last\_heartbeat\_at  
health\_status  
protocol\_status  
expected\_feedback\_channel  
registered\_action\_types

검증 규칙:

external\_system\_id must exist  
external\_system must be registered  
external\_system must be active  
health\_status must not be unreachable  
last\_heartbeat must be fresh  
target action type must be supported  
expected feedback channel must exist

실패 처리:

external\_system\_unregistered  
    → block

external\_system\_inactive  
    → block

external\_system\_unreachable  
    → block

external\_system\_health\_stale  
    → block or hold depending on tier

unsupported\_action\_type  
    → block

---

## **9\. Adapter Health Rule**

Adapter Health는 LEDO와 외부 시스템 사이의 adapter가 현재 사용할 수 있는지 확인한다.

검증 대상:

adapter\_id  
adapter\_status  
adapter\_version  
last\_heartbeat\_at  
latency\_ms  
error\_rate  
protocol\_compatibility  
target\_external\_system

검증 규칙:

adapter must be registered  
adapter must be active  
adapter version must be compatible  
adapter heartbeat must be fresh  
adapter latency must be within threshold  
adapter error rate must be within threshold  
protocol must be compatible

실패 처리:

adapter\_unregistered  
    → block

adapter\_inactive  
    → block

adapter\_unhealthy  
    → block

adapter\_degraded  
    → hold or retry

adapter\_version\_incompatible  
    → block

adapter\_latency\_exceeded  
    → hold or block depending on tier

---

## **10\. Heartbeat Freshness Rule**

Network Health는 heartbeat freshness를 반드시 확인해야 한다.

기본 검증 규칙:

current\_time \- last\_heartbeat\_at \<= max\_heartbeat\_age

Clock skew tolerance를 반영해야 한다.

current\_time \- last\_heartbeat\_at  
    \<= max\_heartbeat\_age \+ clock\_skew\_tolerance

실패 처리:

heartbeat\_stale  
    → block or hold depending on tier

heartbeat\_missing  
    → block

heartbeat\_future\_timestamp  
    → block

Safety-critical action에서 heartbeat가 stale이면 기본값은 block이다.

---

## **11\. Timeout Rule**

External system 또는 adapter 응답이 허용 시간 안에 도착하지 않으면 timeout으로 처리한다.

response\_time\_ms \> timeout\_ms  
    → timeout

처리 원칙:

Tier 1 timeout  
    → block

Tier 2 timeout  
    → retry / hold / degraded mode

Tier 3 timeout  
    → warning

Timeout은 무한정 기다리면 안 된다.

No unbounded wait.

---

## **12\. Retry Rule**

Retry는 허용될 수 있지만 bounded 해야 한다.

retry\_count \<= max\_retry\_count  
retry\_interval\_ms is bounded  
retry must preserve idempotency\_key  
retry must not create duplicate physical execution

실패 처리:

retry\_exhausted  
    → block or hold

retry\_without\_idempotency\_key  
    → block

retry\_creates\_duplicate\_execution\_risk  
    → block

중요 원칙:

Retry must not bypass Runtime Validation.  
Retry must not bypass Safety Gate.  
Retry must not create duplicate physical execution.

---

## **13\. Circuit Breaker Rule**

반복 실패가 발생하면 circuit breaker를 열어 downstream 요청을 차단해야 한다.

상태:

closed  
open  
half\_open

상태 의미:

closed  
    → 정상 요청 허용

open  
    → 요청 차단

half\_open  
    → 제한된 probe만 허용

전이 예시:

repeated failure  
    → circuit\_open

cooldown elapsed  
    → half\_open

probe success  
    → closed

probe failure  
    → open

Safety-critical action에서는 circuit\_open 상태의 외부 시스템으로 dispatch하면 안 된다.

circuit\_open  
    → no dispatch

---

## **14\. Feedback Channel Rule**

ExecutionRequest를 외부 시스템에 전달하려면 feedback channel도 사용 가능해야 한다.

Feedback channel은 실행 결과를 받아 closed loop를 구성하기 위해 필요하다.

No feedback channel,  
no reliable closed loop.

검증 대상:

feedback\_channel\_id  
feedback\_channel\_status  
last\_feedback\_received\_at  
expected\_feedback\_type  
correlation\_id\_support  
trace\_id\_support

실패 처리:

feedback\_channel\_missing  
    → block or hold

feedback\_channel\_unavailable  
    → block or hold

feedback\_correlation\_not\_supported  
    → block

feedback\_channel\_stale  
    → hold or block depending on tier

---

## **15\. Degraded Mode Rule**

일부 외부 시스템이나 adapter가 degraded 상태일 수 있다.

Degraded 상태는 무조건 block을 의미하지 않는다.

degraded  
    → hold / retry / limited execution / manual review

하지만 safety-critical action에서는 degraded 상태를 allow로 바로 처리하면 안 된다.

Tier 1 degraded  
    → block or manual review

Tier 2 degraded  
    → hold / retry / limited execution

Tier 3 degraded  
    → warning

Degraded mode는 policy와 action context에 따라 결정한다.

---

## **16\. NetworkHealthResult Contract**

`network_health/`는 표준화된 결과를 생성해야 한다.

NetworkHealthResult  
    result\_id  
    external\_system\_id  
    adapter\_id  
    health\_status  
    heartbeat\_status  
    latency\_ms  
    error\_rate  
    circuit\_breaker\_status  
    feedback\_channel\_status  
    checked\_at  
    status  
    failure\_reasons  
    warning\_reasons  
    tier  
    trace\_id  
    correlation\_id  
    audit\_ref

가능한 status:

pass  
warning  
hold  
retry  
block  
unknown

---

## **17\. Validator Relation**

Network Health 자체는 health rule과 result를 정의한다.

실제 검증은 Validator가 수행한다.

주요 Validator:

external\_system\_health\_validator  
adapter\_health\_validator  
heartbeat\_freshness\_validator  
feedback\_channel\_validator  
circuit\_breaker\_status\_validator

Validator 결과는 RuntimeValidationResult로 집계된다.

NetworkHealthResult  
    ↓  
ValidatorResult  
    ↓  
RuntimeValidationResult  
    ↓  
SafetyGateResult

---

## **18\. Hot Path Rule**

Runtime hot path에서는 외부 API를 무제한 호출하면 안 된다.

Network Health는 가능한 한 사전 계산되거나 bounded cache로 제공되어야 한다.

금지:

unbounded external API call  
unbounded health probe  
blocking network call without timeout  
direct graph DB network lookup  
LLM-based health judgment  
disk I/O in hot path

허용:

bounded health cache  
precomputed NetworkHealthResult  
heartbeat materialized status  
circuit breaker state  
adapter health snapshot  
external system health snapshot

핵심 규칙:

Hot path reads bounded health result.  
Hot path does not perform unbounded health discovery.

---

## **19\. MVP Scenario: STOP\_WORK**

STOP\_WORK에서 필요한 Network Health 검증은 다음과 같다.

notification system reachable  
site operation system reachable  
feedback channel available  
adapter healthy  
heartbeat fresh  
idempotency key available

실패 처리:

notification system unreachable  
    → hold or fallback channel

site operation system unreachable  
    → block or manual escalation

feedback channel unavailable  
    → hold or manual escalation

adapter unhealthy  
    → block or fallback adapter

STOP\_WORK는 safety-critical action이므로 fallback path와 manual escalation policy를 함께 정의해야 한다.

---

## **20\. MVP Scenario: DISPATCH\_ROBOT**

DISPATCH\_ROBOT에서 필요한 Network Health 검증은 다음과 같다.

robot fleet manager reachable  
fleet manager heartbeat fresh  
robot adapter healthy  
adapter latency within limit  
feedback channel available  
circuit breaker closed

실패 처리:

fleet\_manager\_unreachable  
    → block

robot\_adapter\_unhealthy  
    → block

adapter\_latency\_exceeded  
    → hold or block

feedback\_channel\_unavailable  
    → block or hold

circuit\_open  
    → block

DISPATCH\_ROBOT에서는 외부 Fleet Manager가 실제 robot execution을 수행한다.

LEDO는 low-level robot motion command를 보내지 않는다.

---

## **21\. Audit Requirement**

모든 Network Health 결과는 audit 가능해야 한다.

Audit 대상:

external\_system\_id  
adapter\_id  
health\_status  
heartbeat\_status  
last\_heartbeat\_at  
latency\_ms  
error\_rate  
circuit\_breaker\_status  
feedback\_channel\_status  
checked\_at  
failure\_reasons  
warning\_reasons  
trace\_id  
correlation\_id  
audit\_ref

Network Health 실패가 Safety Gate block으로 이어진 경우 다음 연결이 보존되어야 한다.

NetworkHealthResult  
    → ValidatorResult  
    → RuntimeValidationResult  
    → SafetyGateBlock  
    → AuditRecord

---

## **22\. Final Network Health Rule**

Network reachable  
does not mean  
safe to execute.

한글 기준:

네트워크가 연결되어 있다는 사실은  
실행해도 안전하다는 뜻이 아니다.

최종 규칙:

No healthy external path,  
no reliable dispatch.

No feedback channel,  
no closed loop.

No valid NetworkHealthResult,  
no RuntimeValidationResult.

No RuntimeValidationResult,  
no Safety Gate pass.

No Safety Gate pass,  
no ExecutionRequest.

`network_health/`는 LEDO Runtime Validation에서 외부 실행 경로의 현재 사용 가능성, 신뢰성, 응답성, feedback 가능성을 검증하기 위한 health model과 rule을 정의한다.

Network Health는 Safety Gate pass가 아니다.

Network Health는 Safety Gate가 사용할 runtime validation input이다.

