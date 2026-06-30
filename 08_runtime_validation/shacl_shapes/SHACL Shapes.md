# **SHACL Shapes**

## **1\. Purpose**

This document defines the LEDO `08_runtime_validation/shacl_shapes/` area.

`shacl_shapes/` is responsible for SHACL Shape specifications that validate the structure and constraints of data entering Runtime Validation.

If Runtime Validation is the checkpoint that verifies execution-time condition validity, `shacl_shapes/` is the schema / constraint layer that ensures the validation inputs are structurally valid.

Runtime Validation  
    \= pre-execution condition validation checkpoint

Validators  
    \= validators that actually check runtime conditions

SHACL Shapes  
    \= specifications that define input structure and constraints

The core question of SHACL Shapes is:

Does the data entering Runtime Validation  
satisfy the required structure and constraints?

---

## **2\. Architectural Position**

`shacl_shapes/` is responsible for schema validation and constraint validation inside `08_runtime_validation/`.

ApprovedAction  
    ↓  
SHACL Shape Validation / Pre-validation  
    ↓  
RuntimeValidationInput  
    ↓  
Validators  
    ↓  
RuntimeValidationResult  
    ↓  
Safety Gate  
    ↓  
SafetyGatePass or SafetyGateBlock

SHACL Shapes are not a competing concept against Validators.

SHACL Shapes ensure the structural trustworthiness of the data read by Validators.

SHACL Shapes  
    → validate data structure and constraints.

Validators  
    → actually check execution-time conditions.

Safety Gate  
    → makes the final pass/block decision based on validation results.

---

## **3\. Responsibility Boundary**

The responsibilities of `shacl_shapes/` are:

required field validation  
datatype validation  
value range validation  
relationship constraint validation  
reference integrity validation  
shape version validation  
action input structure validation  
snapshot structure validation  
validator result structure validation  
SafetyGatePass structure validation

`shacl_shapes/` does not perform:

create Approval  
create ApprovedAction  
execute Validators  
create SafetyGatePass  
create ExecutionRequest  
create ExternalControlRequest  
create PhysicalCommand  
directly control external systems  
perform real-time OWL reasoning  
make Safety Gate pass/block decisions

SHACL Shapes validate structure.

The Safety Gate decides execution readiness.

The External System performs actual physical execution.

---

## **4\. Why SHACL Shapes Are Needed**

Runtime Validation consumes multiple data sources.

ApprovedAction  
ApprovalRecord  
PolicyEvaluationResult  
EvidenceBundle  
CurrentState  
SafetySnapshot  
ExternalSystemHealth  
AdapterHealth  
IdempotencyKey  
SafetyGatePass  
ValidatorResult

If these data objects are structurally incomplete or incorrectly linked, Validators may make incorrect judgments.

Examples:

approved\_action\_id is missing  
approval\_ref points to wrong approval  
snapshot\_version is unknown  
observed\_at is missing  
SafetyGatePass expires\_at is missing  
target\_external\_system mismatch  
validator status is not allowed value

Finding these errors immediately before Safety Gate is too late.

Therefore, SHACL Shapes must validate structure and constraints before Runtime Validation or during the materialization stage.

---

## **5\. SHACL vs Validator**

The difference between SHACL Shape and Validator must be clear.

SHACL Shape  
    → validates whether data has the correct structure.

Validator  
    → validates whether the current execution condition is valid.

Example:

SHACL Shape:  
    Does worker\_location\_state have an observed\_at field?  
    Is observed\_at an xsd:dateTime?

Validator:  
    Is worker\_location\_state not stale at execution time?

Another example:

SHACL Shape:  
    Does SafetyGatePass contain expires\_at, lease\_duration\_ms, and terminal\_status?

Validator:  
    Is the SafetyGatePass lease still valid?  
    Is the SafetyGatePass already terminal?

In short, SHACL checks structure and Validator judges condition.

---

## **6\. Hot Path Rule**

Full SHACL validation must not run inside the runtime hot path.

The hot path immediately before the Safety Gate must be fast and deterministic.

Forbidden:

full SHACL validation in Safety Gate hot path  
SPARQL-heavy validation in hot path  
graph database network call in hot path  
unbounded shape traversal  
ontology reasoning during hot path

Allowed:

precomputed SHACLValidationResult  
materialized shape validation flag  
snapshot\_schema\_version  
constraint\_validation\_status  
shape\_version\_compatibility flag

Core rule:

Hot path reads SHACL result.  
Hot path does not run full SHACL.

---

## **7\. SHACL Validation Timing**

SHACL validation may run at the following stages:

1\. design-time validation  
2\. registry update validation  
3\. ontology module update validation  
4\. snapshot materialization validation  
5\. RuntimeValidationInput assembly validation  
6\. pre-SafetyGate materialized check

In safety-critical hot paths, only precomputed results may be read.

SHACL validation stage  
    → compute and materialize result

Safety Gate hot path  
    → read materialized result only

---

## **8\. Core Shape Categories**

For the MVP, SHACL Shapes are divided into the following categories:

Action Shapes  
Runtime Input Shapes  
Snapshot Shapes  
Validator Shapes  
Health Shapes  
Idempotency Shapes  
SafetyGatePass Shapes  
ExecutionRequest Shapes  
Audit Shapes

---

## **9\. Action Shapes**

Action Shapes validate whether `ApprovedAction` and action scope are structurally valid before entering Runtime Validation.

### **9.1 ApprovedActionShape**

Validation targets:

approved\_action\_id  
action\_type  
approval\_ref  
target\_ref  
action\_scope  
created\_at  
status  
policy\_ref  
trace\_id

Required conditions:

approved\_action\_id must exist  
action\_type must be registered  
approval\_ref must exist  
target\_ref must exist  
action\_scope must exist  
status must be APPROVED or RUNTIME\_VALIDATING

Failure handling:

missing approved\_action\_id  
    → block

unknown action\_type  
    → block

missing approval\_ref  
    → block

invalid action\_scope  
    → block

---

## **10\. Runtime Input Shapes**

Runtime Input Shapes validate whether the input bundle passed to Runtime Validation is complete.

### **10.1 RuntimeValidationInputShape**

Validation targets:

approved\_action\_ref  
current\_state\_ref  
snapshot\_ref  
policy\_ref  
approval\_ref  
evidence\_ref  
external\_system\_ref  
adapter\_ref  
idempotency\_key  
trace\_id  
correlation\_id

Required conditions:

approved\_action\_ref must exist  
snapshot\_ref must exist  
approval\_ref must exist  
policy\_ref must exist  
trace\_id must exist

For safety-critical actions, missing required input must result in block.

missing required runtime input  
    → block

---

## **11\. Snapshot Shapes**

Snapshot Shapes validate the structure of snapshots read by Runtime Validation and Safety Gate.

### **11.1 SafetySnapshotShape**

Validation targets:

snapshot\_id  
snapshot\_version  
created\_at  
valid\_until  
source\_state\_versions  
target\_scope  
site\_ref  
zone\_ref  
critical\_state\_refs  
schema\_version

Required conditions:

snapshot\_id must exist  
snapshot\_version must exist  
created\_at must exist  
valid\_until must exist  
target\_scope must match action\_scope  
schema\_version must be compatible

Failure handling:

missing snapshot\_id  
    → block

snapshot\_schema\_version\_mismatch  
    → block or migration required

snapshot\_scope\_mismatch  
    → block

missing critical\_state\_ref  
    → block

---

## **12\. Validator Shapes**

Validator Shapes validate the structure of Validator inputs and outputs.

### **12.1 ValidatorInputShape**

Validation targets:

validator\_id  
validator\_version  
action\_type  
approved\_action\_id  
runtime\_context\_ref  
snapshot\_ref  
trace\_id  
correlation\_id

Required conditions:

validator\_id must exist  
validator\_version must exist  
approved\_action\_id must exist  
trace\_id must exist

### **12.2 ValidatorResultShape**

Validation targets:

result\_id  
validator\_id  
validator\_version  
status  
severity  
tier  
checked\_at  
failure\_reasons  
warning\_reasons  
safety\_gate\_eligible  
trace\_id  
audit\_ref

Allowed statuses:

pass  
fail  
warning  
hold  
retry  
requires\_revalidation  
requires\_reapproval  
manual\_review\_required  
block

Failure handling:

unknown validator status  
    → block

missing checked\_at  
    → block

missing trace\_id  
    → block

invalid tier  
    → block

---

## **13\. Health Shapes**

Health Shapes validate the structure of external system and adapter health records.

### **13.1 ExternalSystemHealthShape**

Validation targets:

external\_system\_id  
system\_type  
health\_status  
last\_heartbeat\_at  
protocol\_status  
expected\_feedback\_channel  
checked\_at

Allowed health statuses:

healthy  
degraded  
unreachable  
timeout  
circuit\_open  
unknown

### **13.2 AdapterHealthShape**

Validation targets:

adapter\_id  
adapter\_version  
adapter\_status  
last\_heartbeat\_at  
latency\_ms  
error\_rate  
protocol\_compatibility

Failure handling:

missing external\_system\_id  
    → block

unknown health\_status  
    → block

missing heartbeat timestamp  
    → block or hold depending on tier

adapter\_version\_incompatible  
    → block

---

## **14\. Idempotency Shapes**

Idempotency Shapes validate the key and ledger entry structure required to prevent duplicate execution.

### **14.1 IdempotencyKeyShape**

Validation targets:

idempotency\_key  
approved\_action\_id  
action\_type  
target\_id  
target\_zone  
safety\_gate\_pass\_id  
execution\_request\_id  
trace\_id

Required conditions:

idempotency\_key must exist  
approved\_action\_id must exist  
action\_type must exist  
trace\_id must exist

### **14.2 IdempotencyLedgerEntryShape**

Validation targets:

idempotency\_key  
first\_seen\_at  
last\_seen\_at  
status  
previous\_result\_ref  
terminal\_token\_ref  
trace\_id

Failure handling:

missing idempotency\_key  
    → block

invalid ledger status  
    → block

missing terminal\_token\_ref for terminal pass  
    → block

---

## **15\. SafetyGatePass Shapes**

SafetyGatePass Shapes validate the structure of SafetyGatePass lease and terminal status.

### **15.1 SafetyGatePassShape**

Validation targets:

safety\_gate\_pass\_id  
approved\_action\_id  
issued\_at  
expires\_at  
lease\_duration\_ms  
lease\_started\_monotonic\_ms  
lease\_expires\_monotonic\_ms  
target\_external\_system  
idempotency\_key  
trace\_id  
terminal\_status

Required conditions:

safety\_gate\_pass\_id must exist  
approved\_action\_id must exist  
issued\_at must exist  
expires\_at must exist  
lease\_duration\_ms must exist  
target\_external\_system must exist  
idempotency\_key must exist  
terminal\_status must exist

Allowed terminal statuses:

ISSUED  
DISPATCHING  
CONSUMED\_ACCEPTED  
CONSUMED\_REJECTED  
CONSUMED\_DROPPED  
EXPIRED  
REVOKED

Failure handling:

missing expires\_at  
    → block

missing lease\_duration\_ms  
    → block

unknown terminal\_status  
    → block

target\_external\_system\_missing  
    → block

---

## **16\. ExecutionRequest Shapes**

ExecutionRequest Shapes validate the structure of execution intent created after SafetyGatePass.

### **16.1 ExecutionRequestShape**

Validation targets:

execution\_request\_id  
approved\_action\_id  
safety\_gate\_pass\_id  
action\_type  
target\_external\_system  
execution\_intent  
constraints  
idempotency\_key  
trace\_id  
created\_at

Required conditions:

execution\_request\_id must exist  
safety\_gate\_pass\_id must exist  
target\_external\_system must exist  
idempotency\_key must exist  
execution\_intent must exist

Important boundary:

ExecutionRequest is not PhysicalCommand.

ExecutionRequest is bounded execution intent sent to an external system.

---

## **17\. Audit Shapes**

Audit Shapes validate the structure required to make Runtime Validation and SHACL validation results traceable.

### **17.1 SHACLValidationResultShape**

Validation targets:

shape\_result\_id  
shape\_id  
shape\_version  
target\_node  
validation\_status  
checked\_at  
violations  
warnings  
trace\_id  
audit\_ref

Allowed validation statuses:

valid  
invalid  
warning  
skipped  
not\_applicable

Failure handling:

invalid required shape  
    → block

warning optional shape  
    → warning

shape version mismatch  
    → block or migration required

---

## **18\. Shape Versioning**

Every SHACL Shape must have a version.

shape\_id  
shape\_version  
compatible\_schema\_version  
created\_at  
deprecated\_at  
migration\_required

If the shape version does not match the Runtime Validation schema version, it must be handled as block or migration required.

shape\_version\_mismatch  
    → block or migration required

---

## **19\. Failure Policy**

SHACL validation failures are handled according to criticality.

required safety-critical shape violation  
    → block

required operational shape violation  
    → hold or block

optional informational shape violation  
    → warning

shape version mismatch  
    → block or migration required

unknown shape result  
    → block for Tier 1

For safety-critical paths, missing required fields must always block execution.

---

## **20\. Audit Requirement**

Every SHACL validation result must be auditable.

Audit targets:

shape\_id  
shape\_version  
target\_node  
target\_type  
validation\_status  
violations  
warnings  
checked\_at  
trace\_id  
correlation\_id  
audit\_ref

If a SHACL validation failure leads to a Safety Gate block, the following linkage must be preserved:

SHACLValidationResult  
    → RuntimeValidationResult  
    → SafetyGateBlock  
    → AuditRecord

---

## **21\. MVP Scope**

The MVP must prioritize the following SHACL Shapes:

ApprovedActionShape  
RuntimeValidationInputShape  
SafetySnapshotShape  
ValidatorResultShape  
ExternalSystemHealthShape  
AdapterHealthShape  
IdempotencyKeyShape  
SafetyGatePassShape  
ExecutionRequestShape  
SHACLValidationResultShape

These MVP Shapes must support the STOP\_WORK and DISPATCH\_ROBOT runtime validation flows.

---

## **22\. Final SHACL Shape Rule**

SHACL Shapes do not execute.  
SHACL Shapes do not approve.  
SHACL Shapes do not command.  
SHACL Shapes validate structure and constraints.

Final rules:

No valid shape,  
no valid RuntimeValidationInput.

No valid RuntimeValidationInput,  
no valid ValidatorResult.

No valid ValidatorResult,  
no RuntimeValidationResult.

No RuntimeValidationResult,  
no Safety Gate pass.

No Safety Gate pass,  
no ExecutionRequest.

`shacl_shapes/` is the schema / constraint validation area that ensures structural trust for data entering LEDO Runtime Validation.

SHACL Shapes do not run as heavy validation inside the runtime hot path. Instead, they generate results during pre-validation or materialization stages so that Validators and the Safety Gate can rely on trusted inputs.

# **SHACL Shapes**

## **1\. 목적**

이 문서는 LEDO `08_runtime_validation/shacl_shapes/` 영역을 정의한다.

`shacl_shapes/`는 Runtime Validation에 들어오는 데이터 구조와 제약 조건을 검증하기 위한 SHACL Shape 명세를 담당한다.

Runtime Validation이 실행 직전의 조건 유효성을 검증하는 구간이라면, `shacl_shapes/`는 그 검증에 사용되는 입력 데이터가 구조적으로 올바른지 확인하는 schema / constraint layer이다.

Runtime Validation  
    \= 실행 직전 조건 검증 구간

Validators  
    \= 실제 조건을 검사하는 검증기

SHACL Shapes  
    \= 검증 입력의 구조와 제약 조건을 정의하는 명세

SHACL Shapes의 핵심 질문은 다음이다.

Runtime Validation에 들어오는 데이터는  
정해진 구조와 제약 조건을 만족하는가?

---

## **2\. Architectural Position**

`shacl_shapes/`는 `08_runtime_validation/` 내부에서 schema validation과 constraint validation을 담당한다.

ApprovedAction  
    ↓  
SHACL Shape Validation / Pre-validation  
    ↓  
RuntimeValidationInput  
    ↓  
Validators  
    ↓  
RuntimeValidationResult  
    ↓  
Safety Gate  
    ↓  
SafetyGatePass or SafetyGateBlock

SHACL Shapes는 Validator와 경쟁하는 개념이 아니다.

SHACL Shapes는 Validator가 읽을 입력 데이터의 구조적 신뢰성을 보장한다.

SHACL Shapes  
    → 데이터 구조와 constraint를 검증한다.

Validators  
    → 실행 시점 조건을 실제로 검사한다.

Safety Gate  
    → 검증 결과를 기반으로 최종 pass/block을 결정한다.

---

## **3\. Responsibility Boundary**

`shacl_shapes/`의 책임은 다음과 같다.

required field 검증  
datatype 검증  
value range 검증  
relationship constraint 검증  
reference integrity 검증  
shape version 검증  
action input structure 검증  
snapshot structure 검증  
validator result structure 검증  
SafetyGatePass structure 검증

`shacl_shapes/`는 다음을 하지 않는다.

Approval 생성  
ApprovedAction 생성  
Validator 실행  
SafetyGatePass 생성  
ExecutionRequest 생성  
ExternalControlRequest 생성  
PhysicalCommand 생성  
외부 시스템 직접 제어  
실시간 OWL reasoning 수행  
Safety Gate pass/block 결정

SHACL Shapes는 구조를 검증한다.

Safety Gate는 실행 가능 여부를 결정한다.

External System은 실제 물리 실행을 수행한다.

---

## **4\. Why SHACL Shapes Are Needed**

Runtime Validation은 여러 데이터 소스를 사용한다.

ApprovedAction  
ApprovalRecord  
PolicyEvaluationResult  
EvidenceBundle  
CurrentState  
SafetySnapshot  
ExternalSystemHealth  
AdapterHealth  
IdempotencyKey  
SafetyGatePass  
ValidatorResult

이 데이터들이 구조적으로 불완전하거나 잘못 연결되어 있으면 Validator가 잘못된 판단을 할 수 있다.

예시:

approved\_action\_id is missing  
approval\_ref points to wrong approval  
snapshot\_version is unknown  
observed\_at is missing  
SafetyGatePass expires\_at is missing  
target\_external\_system mismatch  
validator status is not allowed value

이런 오류는 Safety Gate 직전에 발견하면 늦다.

따라서 SHACL Shapes는 Runtime Validation 이전 또는 materialization 단계에서 구조와 제약을 검증해야 한다.

---

## **5\. SHACL vs Validator**

SHACL Shape와 Validator의 차이는 명확해야 한다.

SHACL Shape  
    → 데이터가 올바른 구조를 갖는지 검증한다.

Validator  
    → 현재 실행 조건이 유효한지 검증한다.

예시:

SHACL Shape:  
    worker\_location\_state에 observed\_at 필드가 존재하는가?  
    observed\_at은 xsd:dateTime인가?

Validator:  
    worker\_location\_state가 현재 실행 시점에 stale하지 않은가?

다른 예시:

SHACL Shape:  
    SafetyGatePass에 expires\_at, lease\_duration\_ms, terminal\_status가 있는가?

Validator:  
    SafetyGatePass lease가 아직 유효한가?  
    SafetyGatePass가 이미 terminal 상태는 아닌가?

즉, SHACL은 구조를 확인하고 Validator는 상태를 판단한다.

---

## **6\. Hot Path Rule**

Runtime hot path에서 full SHACL validation을 수행하면 안 된다.

Safety Gate 직전의 hot path는 빠르고 결정론적이어야 한다.

금지 항목:

full SHACL validation in Safety Gate hot path  
SPARQL-heavy validation in hot path  
graph database network call in hot path  
unbounded shape traversal  
ontology reasoning during hot path

허용 항목:

precomputed SHACLValidationResult  
materialized shape validation flag  
snapshot\_schema\_version  
constraint\_validation\_status  
shape\_version\_compatibility flag

핵심 규칙:

Hot path reads SHACL result.  
Hot path does not run full SHACL.

---

## **7\. SHACL Validation Timing**

SHACL validation은 다음 시점에 수행될 수 있다.

1\. design-time validation  
2\. registry update validation  
3\. ontology module update validation  
4\. snapshot materialization validation  
5\. RuntimeValidationInput assembly validation  
6\. pre-SafetyGate materialized check

Safety-critical hot path에서는 사전에 계산된 결과만 읽는다.

SHACL validation stage  
    → compute and materialize result

Safety Gate hot path  
    → read materialized result only

---

## **8\. Core Shape Categories**

MVP 기준 SHACL Shape는 다음 범주로 나눈다.

Action Shapes  
Runtime Input Shapes  
Snapshot Shapes  
Validator Shapes  
Health Shapes  
Idempotency Shapes  
SafetyGatePass Shapes  
ExecutionRequest Shapes  
Audit Shapes

---

## **9\. Action Shapes**

Action Shape는 `ApprovedAction`과 action scope가 Runtime Validation에 들어오기 전에 구조적으로 올바른지 검증한다.

### **9.1 ApprovedActionShape**

검증 대상:

approved\_action\_id  
action\_type  
approval\_ref  
target\_ref  
action\_scope  
created\_at  
status  
policy\_ref  
trace\_id

필수 조건:

approved\_action\_id must exist  
action\_type must be registered  
approval\_ref must exist  
target\_ref must exist  
action\_scope must exist  
status must be APPROVED or RUNTIME\_VALIDATING

실패 처리:

missing approved\_action\_id  
    → block

unknown action\_type  
    → block

missing approval\_ref  
    → block

invalid action\_scope  
    → block

---

## **10\. Runtime Input Shapes**

Runtime Input Shape는 Runtime Validation에 전달되는 입력 묶음이 완전한지 검증한다.

### **10.1 RuntimeValidationInputShape**

검증 대상:

approved\_action\_ref  
current\_state\_ref  
snapshot\_ref  
policy\_ref  
approval\_ref  
evidence\_ref  
external\_system\_ref  
adapter\_ref  
idempotency\_key  
trace\_id  
correlation\_id

필수 조건:

approved\_action\_ref must exist  
snapshot\_ref must exist  
approval\_ref must exist  
policy\_ref must exist  
trace\_id must exist

Safety-critical action에서는 필수 입력 누락이 block이다.

missing required runtime input  
    → block

---

## **11\. Snapshot Shapes**

Snapshot Shape는 Runtime Validation과 Safety Gate가 읽는 snapshot 구조를 검증한다.

### **11.1 SafetySnapshotShape**

검증 대상:

snapshot\_id  
snapshot\_version  
created\_at  
valid\_until  
source\_state\_versions  
target\_scope  
site\_ref  
zone\_ref  
critical\_state\_refs  
schema\_version

필수 조건:

snapshot\_id must exist  
snapshot\_version must exist  
created\_at must exist  
valid\_until must exist  
target\_scope must match action\_scope  
schema\_version must be compatible

실패 처리:

missing snapshot\_id  
    → block

snapshot\_schema\_version\_mismatch  
    → block or migration required

snapshot\_scope\_mismatch  
    → block

missing critical\_state\_ref  
    → block

---

## **12\. Validator Shapes**

Validator Shape는 Validator 입력과 출력 구조를 검증한다.

### **12.1 ValidatorInputShape**

검증 대상:

validator\_id  
validator\_version  
action\_type  
approved\_action\_id  
runtime\_context\_ref  
snapshot\_ref  
trace\_id  
correlation\_id

필수 조건:

validator\_id must exist  
validator\_version must exist  
approved\_action\_id must exist  
trace\_id must exist

### **12.2 ValidatorResultShape**

검증 대상:

result\_id  
validator\_id  
validator\_version  
status  
severity  
tier  
checked\_at  
failure\_reasons  
warning\_reasons  
safety\_gate\_eligible  
trace\_id  
audit\_ref

허용 status:

pass  
fail  
warning  
hold  
retry  
requires\_revalidation  
requires\_reapproval  
manual\_review\_required  
block

실패 처리:

unknown validator status  
    → block

missing checked\_at  
    → block

missing trace\_id  
    → block

invalid tier  
    → block

---

## **13\. Health Shapes**

Health Shape는 외부 시스템과 adapter 상태 record의 구조를 검증한다.

### **13.1 ExternalSystemHealthShape**

검증 대상:

external\_system\_id  
system\_type  
health\_status  
last\_heartbeat\_at  
protocol\_status  
expected\_feedback\_channel  
checked\_at

허용 health status:

healthy  
degraded  
unreachable  
timeout  
circuit\_open  
unknown

### **13.2 AdapterHealthShape**

검증 대상:

adapter\_id  
adapter\_version  
adapter\_status  
last\_heartbeat\_at  
latency\_ms  
error\_rate  
protocol\_compatibility

실패 처리:

missing external\_system\_id  
    → block

unknown health\_status  
    → block

missing heartbeat timestamp  
    → block or hold depending on tier

adapter\_version\_incompatible  
    → block

---

## **14\. Idempotency Shapes**

Idempotency Shape는 중복 실행 방지에 필요한 key와 ledger entry 구조를 검증한다.

### **14.1 IdempotencyKeyShape**

검증 대상:

idempotency\_key  
approved\_action\_id  
action\_type  
target\_id  
target\_zone  
safety\_gate\_pass\_id  
execution\_request\_id  
trace\_id

필수 조건:

idempotency\_key must exist  
approved\_action\_id must exist  
action\_type must exist  
trace\_id must exist

### **14.2 IdempotencyLedgerEntryShape**

검증 대상:

idempotency\_key  
first\_seen\_at  
last\_seen\_at  
status  
previous\_result\_ref  
terminal\_token\_ref  
trace\_id

실패 처리:

missing idempotency\_key  
    → block

invalid ledger status  
    → block

missing terminal\_token\_ref for terminal pass  
    → block

---

## **15\. SafetyGatePass Shapes**

SafetyGatePass Shape는 SafetyGatePass lease와 terminal status 구조를 검증한다.

### **15.1 SafetyGatePassShape**

검증 대상:

safety\_gate\_pass\_id  
approved\_action\_id  
issued\_at  
expires\_at  
lease\_duration\_ms  
lease\_started\_monotonic\_ms  
lease\_expires\_monotonic\_ms  
target\_external\_system  
idempotency\_key  
trace\_id  
terminal\_status

필수 조건:

safety\_gate\_pass\_id must exist  
approved\_action\_id must exist  
issued\_at must exist  
expires\_at must exist  
lease\_duration\_ms must exist  
target\_external\_system must exist  
idempotency\_key must exist  
terminal\_status must exist

허용 terminal status:

ISSUED  
DISPATCHING  
CONSUMED\_ACCEPTED  
CONSUMED\_REJECTED  
CONSUMED\_DROPPED  
EXPIRED  
REVOKED

실패 처리:

missing expires\_at  
    → block

missing lease\_duration\_ms  
    → block

unknown terminal\_status  
    → block

target\_external\_system\_missing  
    → block

---

## **16\. ExecutionRequest Shapes**

ExecutionRequest Shape는 SafetyGatePass 이후 생성되는 execution intent의 구조를 검증한다.

### **16.1 ExecutionRequestShape**

검증 대상:

execution\_request\_id  
approved\_action\_id  
safety\_gate\_pass\_id  
action\_type  
target\_external\_system  
execution\_intent  
constraints  
idempotency\_key  
trace\_id  
created\_at

필수 조건:

execution\_request\_id must exist  
safety\_gate\_pass\_id must exist  
target\_external\_system must exist  
idempotency\_key must exist  
execution\_intent must exist

중요 경계:

ExecutionRequest is not PhysicalCommand.

ExecutionRequest는 외부 시스템에 전달되는 bounded execution intent이다.

---

## **17\. Audit Shapes**

Audit Shape는 Runtime Validation과 SHACL validation 결과가 추적 가능하도록 구조를 검증한다.

### **17.1 SHACLValidationResultShape**

검증 대상:

shape\_result\_id  
shape\_id  
shape\_version  
target\_node  
validation\_status  
checked\_at  
violations  
warnings  
trace\_id  
audit\_ref

허용 validation status:

valid  
invalid  
warning  
skipped  
not\_applicable

실패 처리:

invalid required shape  
    → block

warning optional shape  
    → warning

shape version mismatch  
    → block or migration required

---

## **18\. Shape Versioning**

모든 SHACL Shape는 version을 가져야 한다.

shape\_id  
shape\_version  
compatible\_schema\_version  
created\_at  
deprecated\_at  
migration\_required

Shape version이 Runtime Validation schema version과 맞지 않으면 block 또는 migration required로 처리한다.

shape\_version\_mismatch  
    → block or migration required

---

## **19\. Failure Policy**

SHACL validation failure는 criticality에 따라 처리한다.

required safety-critical shape violation  
    → block

required operational shape violation  
    → hold or block

optional informational shape violation  
    → warning

shape version mismatch  
    → block or migration required

unknown shape result  
    → block for Tier 1

Safety-critical path에서 required field가 누락되면 반드시 block이다.

---

## **20\. Audit Requirement**

모든 SHACL validation 결과는 audit 가능해야 한다.

Audit 대상:

shape\_id  
shape\_version  
target\_node  
target\_type  
validation\_status  
violations  
warnings  
checked\_at  
trace\_id  
correlation\_id  
audit\_ref

SHACL validation failure가 Safety Gate block으로 이어진 경우 다음 연결이 보존되어야 한다.

SHACLValidationResult  
    → RuntimeValidationResult  
    → SafetyGateBlock  
    → AuditRecord

---

## **21\. MVP Scope**

MVP에서 우선 구현해야 할 SHACL Shape는 다음과 같다.

ApprovedActionShape  
RuntimeValidationInputShape  
SafetySnapshotShape  
ValidatorResultShape  
ExternalSystemHealthShape  
AdapterHealthShape  
IdempotencyKeyShape  
SafetyGatePassShape  
ExecutionRequestShape  
SHACLValidationResultShape

이 MVP Shape들은 STOP\_WORK와 DISPATCH\_ROBOT runtime validation flow를 지원해야 한다.

---

## **22\. Final SHACL Shape Rule**

SHACL Shapes do not execute.  
SHACL Shapes do not approve.  
SHACL Shapes do not command.  
SHACL Shapes validate structure and constraints.

한글 기준:

SHACL Shape는 실행하지 않는다.  
SHACL Shape는 승인하지 않는다.  
SHACL Shape는 명령하지 않는다.  
SHACL Shape는 구조와 제약 조건을 검증한다.

최종 규칙:

No valid shape,  
no valid RuntimeValidationInput.

No valid RuntimeValidationInput,  
no valid ValidatorResult.

No valid ValidatorResult,  
no RuntimeValidationResult.

No RuntimeValidationResult,  
no Safety Gate pass.

No Safety Gate pass,  
no ExecutionRequest.

`shacl_shapes/`는 LEDO Runtime Validation에 들어오는 데이터의 구조적 신뢰성을 보장하는 schema / constraint validation 영역이다.

SHACL Shapes는 Runtime hot path에서 무겁게 실행되지 않고, 사전 검증 또는 materialization 단계에서 결과를 생성하여 Validators와 Safety Gate가 신뢰할 수 있는 입력을 사용하도록 만든다.

