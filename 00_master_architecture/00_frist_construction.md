# **Master Architecture “First Constitution”**

## **1\. Purpose**

`00_ledo_first_constitution.md` is the first constitution of the LEDO project.

This document defines the highest-level principles that all architecture documents, specifications, models, validation structures, and implementation code in the LEDO Ontology Core must follow.

This document does not describe detailed implementation methods.  
This document does not define domain-specific operational rules.  
This document is not dependent on any specific tool or vendor.

This document defines the boundaries that the system must never cross and the principles that all lower-level structures must obey.

---

## **2\. Constitutional Authority**

This document has the highest priority within `00_master_architecture`.

All lower-level documents, designs, and implementations must not conflict with the principles defined here.

If a conflict occurs, the following rules apply.

This document takes precedence.  
Choose the safer interpretation.”  
If uncertain, do not execute.  
If domain knowledge is missing, do not guess.  
High-risk decisions must pass validation and approval.

---

## **3\. First Principle: Ontology Is the Authority of Meaning**

Ontology is the highest-level structure for defining meaning inside the system.

The meaning of objects, relationships, properties, events, states, actions, authority, evidence, policies, and execution boundaries must be defined through ontology and its connected specifications.

AI output, UI representation, temporary data, and external system responses cannot replace the semantic authority of the ontology.

Ontology defines meaning.

---

## **4\. Second Principle: AI Output Is a Candidate, Not Truth**

AI output may generate interpretation, proposals, summaries, classifications, mapping candidates, risk interpretations, and ActionCandidates.

However, AI output cannot determine truth.

AI output must never become:

Evidence  
ApprovedAction  
ExecutionRequest  
ExternalControlRequest  
Policy Decision  
Safety Gate Decision  
Physical Command

AI may propose.  
Ontology, Evidence, Policy, Approval, and Safety Gate must validate.

---

## **5\. Third Principle: No Evidence, No Trusted Decision**

Important decisions must be supported by Evidence.

Evidence must include source, time, trust metadata, traceability, and validation status.

AI-generated explanations or summaries are not Evidence.  
AI may summarize Evidence, but it cannot become Evidence by itself.

No evidence, no trusted decision.

---

## **6\. Fourth Principle: Meaning, Validation, Permission, Approval, and Execution Are Separated**

LEDO separates the following responsibilities.

Ontology     → Meaning definition  
Validation   → Structural and condition validation  
Policy       → Operational permission decision  
Approval     → High-risk authority granting  
Safety Gate  → Execution-readiness validation  
Execution    → Physical execution by external systems  
Audit        → Full path traceability

No layer may merge or bypass these responsibilities.

---

## **7\. Fifth Principle: Policy Determines Operational Permission**

Ontology defines meaning, but it does not determine operational permission by itself.

Operational permission must be determined through Policy, authority, approval state, Evidence, current state, risk level, and execution feasibility.

Policy decisions must be auditable, and high-risk decisions must be connected to approval workflows.

---

## **8\. Sixth Principle: Human Approval Controls High-Risk Authority**

High-risk actions, safety-related actions, and actions that may connect to physical execution must pass Human Approval or an explicitly defined approval structure.

AI, Agents, and automated reasoning results cannot grant high-risk authority to themselves.

Approval must be traceable, and the Evidence, state, and reason behind the approval must be recorded in Audit.

---

## **9\. Seventh Principle: ActionCandidate Is Not an Execution Command**

ActionCandidate is only an execution candidate.

ActionCandidate cannot be executed before passing the following stages.

Semantic Validation  
Evidence Check  
Policy Check  
Decision Routing  
Approval  
Safety Gate Validation

The existence of an ActionCandidate does not mean execution is allowed.

---

## **10\. Eighth Principle: ApprovedAction Is Not a Physical Command**

ApprovedAction is an approved intent or approved action unit.

ApprovedAction is not a direct command to physical equipment, robots, PLCs, SCADA systems, or access-control devices.

ApprovedAction may be transformed into an ExecutionRequest only after passing Safety Gate validation.

---

## **11\. Ninth Principle: ExecutionRequest Is Not a Physical Command**

ExecutionRequest is a request sent to an external system.

ExecutionRequest may contain:

intent  
target  
constraints  
approval reference  
evidence reference  
policy reference  
safety validation result  
trace id  
idempotency key

However, ExecutionRequest itself is not motor control, PLC write, SCADA command, robot joint control, or emergency stop command.

Physical execution belongs to external control systems.

---

## **12\. Tenth Principle: Physical Execution Belongs to External Systems**

LEDO defines physical execution intent, constraints, approval, validation results, and audit traceability.

Actual physical execution belongs to external systems such as:

Robot Middleware  
Fleet Manager  
PLC  
SCADA  
Access Control System  
Equipment Controller  
Site Operation System  
Safety-rated Controller

The internal reasoning layer, AI layer, and ontology layer of LEDO do not directly perform physical control.

---

## **13\. Eleventh Principle: Safety Gate Must Be Deterministic and Fail-Closed**

Safety Gate is the final validation layer before execution.

Safety Gate must be deterministic.  
If it fails or becomes uncertain, it must reject, hold, or escalate in the safer direction.

Unknown → Hold or Deny  
Stale Data → Hold or Deny  
Invalid Approval → Deny  
Missing Evidence → Deny  
Snapshot Failure → Fail Closed

Safety Gate is the final anti-bypass mechanism for safety.

---

## **14\. Twelfth Principle: Runtime Hot Path Reads Only Precomputed Results**

The runtime hot path must not perform heavy reasoning, dynamic graph queries, AI calls, or external network calls.

The runtime hot path must only read precomputed validation results and materialized snapshots.

The following are forbidden in the runtime hot path.

OWL Reasoner  
Full SHACL Validation  
SPARQL Query  
Graph DB Network Call  
LLM / SLM Call  
External API Call  
Disk I/O  
Unbounded Computation

The runtime hot path must be fast, bounded, and verifiable.

---

## **15\. Thirteenth Principle: Audit Preserves Every Important Decision Path**

Important decisions in LEDO must be traceable.

The following objects should be connected within a single trace flow whenever applicable.

Event  
Evidence  
State Update  
ActionCandidate  
Decision  
Approval  
ApprovedAction  
Safety Gate Result  
ExecutionRequest  
ExternalControlRequest  
Feedback  
AuditRecord

Audit is mandatory for post-hoc explanation, validation, accountability, and reproducibility.

---

## **16\. Fourteenth Principle: Source of Truth Must Be Separated**

Not all information in LEDO represents the same kind of truth.

Each area must have a distinct Source of Truth.

Semantic Meaning       → Ontology  
Current Runtime State  → World State  
Historical Evidence    → Evidence Store / Audit  
Operational Permission → Policy  
High-Risk Authority    → Approval  
Execution Readiness    → Safety Gate Snapshot  
Physical Execution     → External System  
Identity Resolution    → Canonical Identity / Registry

No single layer should monopolize every kind of truth.

---

## **17\. Fifteenth Principle: Standards Are Mapped, Not Copied**

External standards are used to strengthen interoperability and semantic alignment.

However, external standards must not be copied blindly into the internal structure.

LEDO uses standards through:

Reference  
Mapping  
Alignment  
Compatibility  
Governance

LEDO’s Core Ontology and internal contracts must preserve their own consistency.

---

## **18\. Sixteenth Principle: Domain Meaning Must Be Governed**

Domain meaning must not be generated arbitrarily.

Construction, industrial operation, robotics, safety, legal compliance, field operations, equipment control, approval authority, and risk criteria must be defined through domain expert review and governance.

The framework may generate structure.  
Domain meaning must be governed.

Structure can be generated.  
Meaning must be governed.

---

## **19\. Seventeenth Principle: If Uncertain, Do Not Execute**

Uncertainty cannot become a basis for execution in LEDO.

When uncertain, the system must choose one of the following actions.

Hold  
Deny  
Escalate  
Request Evidence  
Request Approval  
Request Domain Expert Review

Any design that ignores uncertainty and proceeds directly to execution is not allowed.

---

## **20\. Final Constitutional Declaration**

LEDO is an ontology-centric Cyber-Physical AI system.

LEDO separates meaning, evidence, state, judgment, approval, validation, execution, and audit.

AI may generate candidates, but it does not determine truth.  
Ontology defines meaning, but it does not determine operational permission by itself.  
Policy determines permission, but it does not perform physical execution.  
Approval grants authority, but it is not a physical command.  
Safety Gate validates execution readiness, but it is not a physical controller.  
ExecutionRequest is a request, not a physical command.  
Physical Execution is performed by External Systems.

The final principles are:

Meaning must be explicit.  
Evidence must be traceable.  
Policy must be enforceable.  
Approval must be auditable.  
Validation must be deterministic.  
Execution must be bounded.  
Safety must fail closed.

# **First Constitution**

## **1\. 목적**

`00_ledo_first_constitution.md`는 LEDO 프로젝트의 제1 헌법이다.

이 문서는 LEDO Ontology Core의 모든 아키텍처, 문서, 모델, 검증 구조, 구현 코드가 반드시 따라야 하는 최상위 원칙을 정의한다.

이 문서는 세부 구현 방법을 설명하지 않는다.  
이 문서는 도메인별 운영 규칙을 정의하지 않는다.  
이 문서는 특정 도구나 특정 벤더에 종속되지 않는다.

이 문서는 시스템이 절대 넘어서는 안 되는 경계와, 모든 하위 구조가 따라야 할 기준을 정의한다.

---

## **2\. 헌법의 지위**

이 문서는 `00_master_architecture` 안에서 가장 높은 우선순위를 가진다.

모든 하위 문서, 설계, 구현은 이 문서의 원칙과 충돌해서는 안 된다.

충돌이 발생할 경우, 다음 기준을 따른다.

이 문서가 우선한다.  
더 안전한 해석을 선택한다.  
불확실한 경우 실행하지 않는다.  
도메인 지식이 부족한 경우 추정하지 않는다.  
고위험 판단은 검증과 승인을 거친다.

---

## **3\. 제1원칙: Ontology는 의미의 권위다**

Ontology는 시스템 안에서 의미를 정의하는 최상위 구조다.

객체, 관계, 속성, 사건, 상태, 행동, 권한, 증거, 정책, 실행 경계의 의미는 Ontology와 그에 연결된 명세를 통해 정의되어야 한다.

AI output, UI 표현, 임시 데이터, 외부 시스템 응답은 Ontology의 의미 권위를 대체할 수 없다.

Ontology defines meaning.

---

## **4\. 제2원칙: AI output은 후보이지 진실이 아니다**

AI output은 해석, 제안, 요약, 분류, 매핑 후보, 위험 해석, ActionCandidate를 생성할 수 있다.

그러나 AI output은 진실을 결정할 수 없다.

AI output은 다음이 될 수 없다.

Evidence  
ApprovedAction  
ExecutionRequest  
ExternalControlRequest  
Policy Decision  
Safety Gate Decision  
Physical Command

AI는 제안할 수 있다.  
검증은 Ontology, Evidence, Policy, Approval, Safety Gate가 수행한다.

---

## **5\. 제3원칙: Evidence 없이는 판단도 실행도 없다**

중요한 판단은 Evidence에 의해 뒷받침되어야 한다.

Evidence는 출처, 시간, 신뢰도, 추적성, 검증 상태를 가져야 한다.

AI가 생성한 설명이나 요약은 Evidence가 아니다.  
AI는 Evidence를 요약할 수 있지만, Evidence 자체가 될 수 없다.

No evidence, no trusted decision.

---

## **6\. 제4원칙: 의미, 검증, 허가, 승인, 실행은 분리한다**

LEDO는 다음 책임을 분리한다.

Ontology     → 의미 정의  
Validation   → 구조와 조건 검증  
Policy       → 운영 허용 여부 판단  
Approval     → 고위험 권한 부여  
Safety Gate  → 실행 준비 상태 검증  
Execution    → 외부 시스템에 의한 물리 실행  
Audit        → 전체 경로 추적

어떤 계층도 이 책임들을 하나로 합쳐 우회해서는 안 된다.

---

## **7\. 제5원칙: Policy는 운영 허가의 기준이다**

Ontology는 의미를 정의하지만, 운영 허용 여부를 단독으로 결정하지 않는다.

운영 허가는 Policy, 권한, 승인 상태, Evidence, 현재 상태, 위험 수준, 실행 가능성에 의해 판단되어야 한다.

Policy 판단은 감사 가능해야 하며, 고위험 판단은 승인 절차와 연결되어야 한다.

---

## **8\. 제6원칙: Human Approval은 고위험 권한의 최종 통제 장치다**

고위험 작업, 안전 관련 작업, 물리 실행과 연결될 수 있는 작업은 Human Approval 또는 명시된 승인 체계를 거쳐야 한다.

AI, Agent, 자동화된 추론 결과는 고위험 권한을 스스로 획득할 수 없다.

승인은 추적 가능해야 하며, 어떤 근거와 어떤 상태에서 승인되었는지 Audit에 남아야 한다.

---

## **9\. 제7원칙: ActionCandidate는 실행 명령이 아니다**

ActionCandidate는 실행 후보일 뿐이다.

ActionCandidate는 다음 절차를 거치기 전까지 실행될 수 없다.

Semantic Validation  
Evidence Check  
Policy Check  
Decision Routing  
Approval  
Safety Gate Validation

ActionCandidate가 생성되었다는 사실은 실행이 허용되었다는 뜻이 아니다.

---

## **10\. 제8원칙: ApprovedAction은 물리 명령이 아니다**

ApprovedAction은 승인된 의도 또는 승인된 조치 단위다.

ApprovedAction은 물리 장비, 로봇, PLC, SCADA, 접근 제어 장치에 대한 직접 명령이 아니다.

ApprovedAction은 Safety Gate를 통과한 뒤에만 ExecutionRequest로 변환될 수 있다.

---

## **11\. 제9원칙: ExecutionRequest는 물리 명령이 아니다**

ExecutionRequest는 외부 시스템에 전달되는 실행 요청이다.

ExecutionRequest는 다음을 포함할 수 있다.

intent  
target  
constraints  
approval reference  
evidence reference  
policy reference  
safety validation result  
trace id  
idempotency key

그러나 ExecutionRequest 자체는 모터 제어, PLC write, SCADA command, robot joint control, emergency stop command가 아니다.

물리 실행은 외부 제어 시스템이 담당한다.

---

## **12\. 제10원칙: Physical Execution은 External System이 담당한다**

LEDO는 물리 실행 의도, 제약 조건, 승인, 검증 결과, 감사 추적을 정의한다.

실제 물리 실행은 다음과 같은 외부 시스템이 담당한다.

Robot Middleware  
Fleet Manager  
PLC  
SCADA  
Access Control System  
Equipment Controller  
Site Operation System  
Safety-rated Controller

LEDO 내부 reasoning layer, AI layer, ontology layer는 직접 물리 제어를 수행하지 않는다.

---

## **13\. 제11원칙: Safety Gate는 결정론적이고 fail-closed여야 한다**

Safety Gate는 실행 직전의 최종 검증 계층이다.

Safety Gate는 결정론적이어야 하며, 실패하거나 불확실할 경우 안전한 방향으로 거부하거나 보류해야 한다.

Unknown → Hold or Deny  
Stale Data → Hold or Deny  
Invalid Approval → Deny  
Missing Evidence → Deny  
Snapshot Failure → Fail Closed

Safety Gate는 안전을 위한 최종 우회 방지 장치다.

---

## **14\. 제12원칙: Runtime hot path는 사전 계산된 결과만 조회한다**

Runtime hot path에서는 무거운 추론, 동적 질의, AI 호출, 외부 네트워크 호출을 수행하지 않는다.

Runtime hot path는 사전 계산된 검증 결과와 materialized snapshot을 조회해야 한다.

Runtime hot path에서 금지되는 항목은 다음과 같다.

OWL Reasoner  
Full SHACL Validation  
SPARQL Query  
Graph DB Network Call  
LLM / SLM Call  
External API Call  
Disk I/O  
Unbounded Computation

Runtime hot path는 빠르고, 제한되어 있으며, 검증 가능해야 한다.

---

## **15\. 제13원칙: Audit은 모든 중요한 판단 경로를 보존한다**

LEDO의 중요한 판단은 추적 가능해야 한다.

다음 객체들은 가능한 경우 하나의 trace 흐름 안에서 연결되어야 한다.

Event  
Evidence  
State Update  
ActionCandidate  
Decision  
Approval  
ApprovedAction  
Safety Gate Result  
ExecutionRequest  
ExternalControlRequest  
Feedback  
AuditRecord

Audit은 사후 설명, 검증, 책임 추적, 재현 가능성을 위해 필수다.

---

## **16\. 제14원칙: Source of Truth는 분리되어야 한다**

LEDO에서 모든 정보가 같은 종류의 진실을 의미하지 않는다.

각 영역의 Source of Truth는 분리되어야 한다.

Semantic Meaning       → Ontology  
Current Runtime State  → World State  
Historical Evidence    → Evidence Store / Audit  
Operational Permission → Policy  
High-Risk Authority    → Approval  
Execution Readiness    → Safety Gate Snapshot  
Physical Execution     → External System  
Identity Resolution    → Canonical Identity / Registry

하나의 계층이 모든 진실을 독점해서는 안 된다.

---

## **17\. 제15원칙: Standards는 복사하지 않고 매핑한다**

외부 표준은 LEDO의 의미 체계와 상호운용성을 강화하기 위해 사용된다.

그러나 외부 표준을 그대로 복사하여 내부 구조를 종속시키지 않는다.

LEDO는 표준을 다음 방식으로 사용한다.

Reference  
Mapping  
Alignment  
Compatibility  
Governance

LEDO의 Core Ontology와 내부 계약은 자체적인 일관성을 가져야 한다.

---

## **18\. 제16원칙: Domain Meaning은 관리되어야 한다**

도메인 의미는 임의로 생성되어서는 안 된다.

건설, 산업, 로봇, 안전, 법규, 현장 운영, 장비 제어, 승인 권한, 위험 기준은 도메인 전문가의 검토와 거버넌스를 통해 정의되어야 한다.

프레임워크는 구조를 만들 수 있다.  
도메인 의미는 관리되어야 한다.

Structure can be generated.  
Meaning must be governed.

---

## **19\. 제17원칙: 불확실하면 실행하지 않는다**

LEDO에서 불확실성은 실행의 근거가 될 수 없다.

불확실한 경우 시스템은 다음 중 하나를 선택해야 한다.

Hold  
Deny  
Escalate  
Request Evidence  
Request Approval  
Request Domain Expert Review

불확실성을 무시하고 실행으로 넘어가는 설계는 허용되지 않는다.

---

## **20\. 최종 헌법 선언**

LEDO는 온톨로지 중심의 Cyber-Physical AI 시스템이다.

LEDO는 의미, 증거, 상태, 판단, 승인, 검증, 실행, 감사를 분리한다.

AI는 후보를 만들 수 있지만 진실을 결정하지 않는다.  
Ontology는 의미를 정의하지만 운영 허가를 단독으로 결정하지 않는다.  
Policy는 허가를 판단하지만 물리 실행을 수행하지 않는다.  
Approval은 권한을 부여하지만 물리 명령이 아니다.  
Safety Gate는 실행 준비를 검증하지만 물리 제어기가 아니다.  
ExecutionRequest는 요청이지 물리 명령이 아니다.  
Physical Execution은 External System이 수행한다.

최종 원칙은 다음과 같다.

Meaning must be explicit.  
Evidence must be traceable.  
Policy must be enforceable.  
Approval must be auditable.  
Validation must be deterministic.  
Execution must be bounded.  
Safety must fail closed.

