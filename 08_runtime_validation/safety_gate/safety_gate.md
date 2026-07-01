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

