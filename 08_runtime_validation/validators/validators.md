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

