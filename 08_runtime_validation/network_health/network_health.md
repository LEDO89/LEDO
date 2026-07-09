# **Network Health**

## **1\. Purpose**

This document defines the LEDO `08_runtime_validation/network_health/` area.

`network_health/` defines the health model and validation rules used to check the current state of external systems, adapters, gateways, fleet managers, notification systems, and feedback channels during Runtime Validation.

LEDO does not perform physical execution directly.

LEDO sends an `ExecutionRequest` to an external system, and the external system performs the actual physical execution.

Therefore, before an `ApprovedAction` becomes an `ExecutionRequest`, LEDO must verify whether the external execution path is currently usable.

The core principle is:

network reachable  
    →
safe to execute

A reachable network does not mean execution is safe.

Network Health is only one input to Runtime Validation and does not automatically imply Safety Gate pass.

---

## **2\. Architectural Position**

`network_health/` defines the state of the external execution path inside `08_runtime_validation/`.

ApprovedAction  
    →
Runtime Validation  
    →
NetworkHealthResult  
    →
ValidatorResult  
    →
RuntimeValidationResult  
    →
Safety Gate  
    →
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
    - checks whether the external execution path is currently usable.

Validator  
    - checks whether the health state satisfies action requirements.

Safety Gate  
    - makes the final pass/block decision based on the full Runtime Validation result.

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

For the initial implementation, `network_health/` targets the following:

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
    - usable normally

degraded  
    - usable, but with reduced performance or reliability

unreachable  
    - not reachable

timeout  
    - response time exceeded the allowed threshold

circuit\_open  
    - requests are blocked due to repeated failures

unknown  
    - current state cannot be determined

Handling rules:

healthy  
    - usable as validation input

degraded  
    - hold / retry / degraded mode

unreachable  
    - block safety-critical action

timeout  
    - retry or block depending on tier

circuit\_open  
    - no dispatch

unknown  
    - block for Tier 1

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
    - block

external\_system\_inactive  
    - block

external\_system\_unreachable  
    - block

external\_system\_health\_stale  
    - block or hold depending on tier

unsupported\_action\_type  
    - block

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
    - block

adapter\_inactive  
    - block

adapter\_unhealthy  
    - block

adapter\_degraded  
    - hold or retry

adapter\_version\_incompatible  
    - block

adapter\_latency\_exceeded  
    - hold or block depending on tier

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
    - block or hold depending on tier

heartbeat\_missing  
    - block

heartbeat\_future\_timestamp  
    - block

For safety-critical actions, stale heartbeat defaults to block.

---

## **11\. Timeout Rule**

If the external system or adapter response does not arrive within the allowed time, it is treated as timeout.

response\_time\_ms \> timeout\_ms  
    - timeout

Handling rules:

Tier 1 timeout  
    - block

Tier 2 timeout  
    - retry / hold / degraded mode

Tier 3 timeout  
    - warning

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
    - block or hold

retry\_without\_idempotency\_key  
    - block

retry\_creates\_duplicate\_execution\_risk  
    - block

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
    - normal requests allowed

open  
    - requests blocked

half\_open  
    - limited probes allowed

Example transitions:

repeated failure  
    - circuit\_open

cooldown elapsed  
    - half\_open

probe success  
    - closed

probe failure  
    - open

For safety-critical actions, dispatch must not be sent to an external system whose circuit is open.

circuit\_open  
    - no dispatch

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
    - block or hold

feedback\_channel\_unavailable  
    - block or hold

feedback\_correlation\_not\_supported  
    - block

feedback\_channel\_stale  
    - hold or block depending on tier

---

## **15\. Degraded Mode Rule**

Some external systems or adapters may be degraded.

A degraded state does not always mean block.

degraded  
    - hold / retry / limited execution / manual review

However, for safety-critical actions, degraded must not be treated as allow by default.

Tier 1 degraded  
    - block or manual review

Tier 2 degraded  
    - hold / retry / limited execution

Tier 3 degraded  
    - warning

Degraded mode is determined by policy and action context.

---

## **16\. NetworkHealthResult Contract**

`network_health/` must produce a standardized result.

Canonical Reference: implemented in code as `NetworkHealthResultDTO` (`01_common_schema_dto/1_common_schema_dto.md` Section 17.3A, "Specialized Runtime Result DTOs"), a subclass of `ValidatorResultDTO`. Fields already covered by that base class are not duplicated below.

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
    →
ValidatorResult  
    →
RuntimeValidationResult  
    →
SafetyGatePass or SafetyGateBlock

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

## **19\. Reference Scenario: STOP\_WORK**

For STOP\_WORK, required Network Health checks are:

notification system reachable  
site operation system reachable  
feedback channel available  
adapter healthy  
heartbeat fresh  
idempotency key available

Failure handling:

notification system unreachable  
    - hold or fallback channel

site operation system unreachable  
    - block or manual escalation

feedback channel unavailable  
    - hold or manual escalation

adapter unhealthy  
    - block or fallback adapter

STOP\_WORK is a safety-critical action, so fallback path and manual escalation policy must be defined.

---

## **20\. Reference Scenario: DISPATCH\_ROBOT**

For DISPATCH\_ROBOT, required Network Health checks are:

robot fleet manager reachable  
fleet manager heartbeat fresh  
robot adapter healthy  
adapter latency within limit  
feedback channel available  
circuit breaker closed

Failure handling:

fleet\_manager\_unreachable  
    - block

robot\_adapter\_unhealthy  
    - block

adapter\_latency\_exceeded  
    - hold or block

feedback\_channel\_unavailable  
    - block or hold

circuit\_open  
    - block

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
    - ValidatorResult  
    - RuntimeValidationResult  
    - SafetyGateBlock  
    - AuditRecord

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

