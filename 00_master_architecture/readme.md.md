**Master Architecture** **README.md** 

## **1\. Purpose**

`00_master_architecture` is the top-level architecture control layer of the LEDO project.

This folder defines the system’s core philosophy, non-negotiable boundaries, responsibility separation, Source of Truth, and the highest-level principles required to maintain architectural consistency across the entire project.

This folder does not describe detailed implementation methods.  
This folder does not define domain-specific operational rules.  
This folder is not dependent on any specific tool or vendor.

This folder controls the direction in which the system must be designed.

---

## **2\. System Identity**

LEDO is an ontology-centric Cyber-Physical AI architecture.

This system is designed to structure industrial judgment, approval, validation, execution requests, and audit processes in a safe and traceable way.

LEDO clearly separates the following concepts.

Ontology   → Meaning definition

Evidence   → Basis for judgment

State      → Current condition

Event      → Occurred fact

Action     → Execution candidate

Decision   → Judgment path

Approval   → Authority granting

Validation → Execution-readiness validation

Audit      → Full path traceability

Execution  → Physical execution by external systems

This separation must be preserved across the entire architecture.

---

## **3\. Core Architectural Principles**

The LEDO architecture is based on the following principles.

Meaning and validation are separated.

Validation and permission are separated.

Permission and execution are separated.

Execution and audit are separated.

AI may generate candidates, but it cannot determine truth.

Physical execution is performed by external control systems, not by internal reasoning layers.

No layer may merge these responsibilities into a single shortcut.

---

## **4\. Non-Negotiable Boundaries**

The following boundaries must never be violated in LEDO.

AI output is a candidate, not truth.

AI output is not Evidence.

ActionCandidate is not an execution command.

ApprovedAction is not a physical command.

ExecutionRequest is a request to an external system.

ExternalControlRequest is also a request, not a physical command.

Physical execution belongs to the External System.

Safety Gate must be deterministic and fail-closed.

The runtime hot path must only read precomputed validation results.

Any design that violates these boundaries must be rejected or revised.

---

## **5\. Repository Responsibility Structure**

The LEDO repository follows the responsibility structure below.

ledo\_ontology\_core/

  00\_master\_architecture/

  01\_layer\_architecture/

  02\_layer\_stack\_mapping/

  03\_core\_specifications/

  04\_ontology\_foundation/

  05\_domain\_ontology\_modules/

  06\_registry\_specs/

  07\_implementation\_plan/

  08\_runtime\_validation/

  09\_appendices/

  10\_archive/

Each folder has the following responsibility.

| Area | Role |
| ----- | ----- |
| `00_master_architecture/` | Top-level philosophy, boundaries, and responsibility control |
| `01_layer_architecture/` | System layer definitions |
| `02_layer_stack_mapping/` | Mapping between layers, technologies, and responsibilities |
| `03_core_specifications/` | Operational contracts |
| `04_ontology_foundation/` | Semantic contracts |
| `05_domain_ontology_modules/` | Domain-specific semantic extensions |
| `06_registry_specs/` | Controlled vocabularies and version management |
| `07_implementation_plan/` | Implementation order and roadmap |
| `08_runtime_validation/` | Runtime validation, Safety Gate, and Snapshot rules |
| `09_appendices/` | References and supporting documents |
| `10_archive/` | Deprecated or superseded materials |

---

## **6\. Core Responsibility Separation**

The most important architectural separation is as follows.

Core Specifications \= Operational contracts

Ontology Foundation \= Semantic contracts

Runtime Validation \= Execution-readiness validation contracts

Registry Specs \= Controlled vocabularies and identifier management

Implementation Plan \= Implementation sequence

Source Code \= Implementation of approved specifications

This separation must be preserved across all documents and code.

---

## **7\. Master Architecture Document Set**

`00_master_architecture` contains the following top-level documents.

00\_master\_architecture/

  README.md

  00\_ledo\_first\_constitution.md

  01\_ledo\_master\_architecture.md

  02\_document\_control\_map.md

  03\_source\_of\_truth\_matrix.md

  04\_code\_generation\_strategy.md

Each document has the following role.

| Document | Role |
| ----- | ----- |
| `README.md` | Explains the purpose and architectural role of this folder |
| `00_ledo_first_constitution.md` | Defines the highest-level principles that must never be violated |
| `01_ledo_master_architecture.md` | Defines the full system architecture and layer relationships |
| `02_document_control_map.md` | Defines which document owns which concept |
| `03_source_of_truth_matrix.md` | Defines authority over meaning, evidence, state, policy, validation, execution, and audit |
| `04_code_generation_strategy.md` | Defines how architecture documents are transformed into implementation artifacts |
| `05_codex_architecture_review_prompt.md` | Defines the architecture review criteria before implementation begins |

---

## **8\. Source of Truth Principle**

The same concept must not be defined differently across multiple documents.

The Master Architecture defines the original source location of major concepts.

| Concept | Source of Truth |
| ----- | ----- |
| Non-negotiable principles and boundaries | `00_ledo_first_constitution.md` |
| Full architecture and layer relationships | `01_ledo_master_architecture.md` |
| Concept ownership by document | `02_document_control_map.md` |
| Authority over meaning, evidence, state, policy, and execution | `03_source_of_truth_matrix.md` |
| Code generation order | `04_code_generation_strategy.md` |
| Detailed ontology modeling principles | `04_ontology_foundation/` |
| Operational object and lifecycle contracts | `03_core_specifications/` |
| Runtime Validation and Safety Gate rules | `08_runtime_validation/` |
| Registry structure and version management | `06_registry_specs/` |

Lower-level documents may reference these principles.  
However, they must not redefine them differently.

---

## **9\. Relationship to Lower Layers**

`00_master_architecture` does not repeat the detailed contents of lower-level documents.

Detailed semantic modeling       → 04\_ontology\_foundation/

Detailed operational contracts   → 03\_core\_specifications/

Detailed registry specifications → 06\_registry\_specs/

Detailed execution validation    → 08\_runtime\_validation/

Detailed implementation planning → 07\_implementation\_plan/

Domain-specific semantic modules → 05\_domain\_ontology\_modules/

The role of this folder is to control the direction and boundaries so that lower-level documents do not conflict with one another.

---

## **10\. Public Architecture Principle**

Documents in this folder must remain suitable for public, export-ready architecture use.

They must follow these principles.

Write in a vendor-neutral way.

Write in a tool-neutral way.

Avoid dependency on a specific implementation.

Do not include arbitrary real domain-specific rules.

Prioritize architectural boundaries and responsibilities over detailed technical explanations.

Detailed implementation methods, tool usage, and internal workflows should be handled in separate operational documents.

---

## **11\. Final Principle**

The purpose of `00_master_architecture` is to give the entire project one clear architectural direction.

This folder controls the architecture.

Lower folders define the details.

Principles must remain strong.

Boundaries must remain clear.

Meaning and execution must remain separated.

All implementation must follow these boundaries.

Final rule:

This folder defines the architecture.

Lower folders define the details.

# 

# 

# 

# 

# 

# 

# **README.md — 00 Master Architecture**

## **1\. 목적**

`00_master_architecture`는 LEDO 프로젝트의 최상위 아키텍처 통제 계층이다.

이 폴더는 시스템의 핵심 철학, 절대 경계, 책임 분리, Source of Truth, 그리고 전체 아키텍처의 일관성을 유지하기 위한 최상위 기준을 정의한다.

이 폴더는 세부 구현 방법을 설명하는 곳이 아니다.  
이 폴더는 도메인별 운영 규칙을 정의하는 곳이 아니다.  
이 폴더는 특정 도구나 특정 벤더에 종속되는 문서가 아니다.

이 폴더는 시스템이 어떤 방향으로 설계되어야 하는지를 통제하는 곳이다.

---

## **2\. 시스템 정체성**

LEDO는 온톨로지 중심의 Cyber-Physical AI 아키텍처다.

이 시스템은 산업 현장의 판단, 승인, 검증, 실행 요청, 감사 과정을 안전하고 추적 가능한 방식으로 구조화하기 위해 설계된다.

LEDO는 다음 개념을 명확히 분리한다.

Ontology   → 의미 정의  
Evidence   → 판단 근거  
State      → 현재 상태  
Event      → 발생 사실  
Action     → 실행 후보  
Decision   → 판단 경로  
Approval   → 권한 부여  
Validation → 실행 준비 검증  
Audit      → 전체 경로 추적  
Execution  → 외부 시스템에 의한 물리 실행

이 분리는 아키텍처 전체에서 유지되어야 한다.

---

## **3\. 핵심 아키텍처 원칙**

LEDO 아키텍처는 다음 원칙을 기반으로 한다.

의미와 검증은 분리한다.  
검증과 허가는 분리한다.  
허가와 실행은 분리한다.  
실행과 감사는 분리한다.  
AI는 후보를 생성할 수 있지만, 진실을 결정할 수 없다.  
물리 실행은 내부 추론 계층이 아니라 외부 제어 시스템이 담당한다.

어떤 계층도 위 책임을 하나로 합쳐 우회해서는 안 된다.

---

## **4\. 절대 경계**

LEDO에서 절대 위반해서는 안 되는 경계는 다음과 같다.

AI output은 후보이지 진실이 아니다.  
AI output은 Evidence가 아니다.  
ActionCandidate는 실행 명령이 아니다.  
ApprovedAction은 물리 명령이 아니다.  
ExecutionRequest는 외부 시스템에 대한 요청이다.  
ExternalControlRequest도 물리 명령이 아니라 외부 시스템에 대한 요청이다.  
물리 실행은 External System이 담당한다.  
Safety Gate는 결정론적이며 fail-closed 원칙을 따른다.  
Runtime hot path는 사전 계산된 검증 결과만 조회한다.

이 경계를 위반하는 설계는 거부하거나 수정해야 한다.

---

## **5\. Repository 책임 구조**

LEDO repository는 다음 책임 구조를 따른다.

ledo\_ontology\_core/  
  00\_master\_architecture/  
  01\_layer\_architecture/  
  02\_layer\_stack\_mapping/  
  03\_core\_specifications/  
  04\_ontology\_foundation/  
  05\_domain\_ontology\_modules/  
  06\_registry\_specs/  
  07\_implementation\_plan/  
  08\_runtime\_validation/  
  09\_appendices/  
  10\_archive/

각 폴더의 책임은 다음과 같다.

| 영역 | 역할 |
| ----- | ----- |
| `00_master_architecture/` | 최상위 철학, 경계, 책임 통제 |
| `01_layer_architecture/` | 시스템 레이어 정의 |
| `02_layer_stack_mapping/` | 레이어와 기술, 레이어와 책임의 매핑 |
| `03_core_specifications/` | 운영 계약 |
| `04_ontology_foundation/` | 의미 계약 |
| `05_domain_ontology_modules/` | 도메인별 의미 확장 |
| `06_registry_specs/` | 통제된 어휘와 버전 관리 |
| `07_implementation_plan/` | 구현 순서와 로드맵 |
| `08_runtime_validation/` | 런타임 검증, Safety Gate, Snapshot 규칙 |
| `09_appendices/` | 참고 자료와 보조 문서 |
| `10_archive/` | 폐기되었거나 대체된 자료 |

---

## **6\. 핵심 책임 분리**

가장 중요한 아키텍처 분리는 다음과 같다.

Core Specifications \= 운영 계약  
Ontology Foundation \= 의미 계약  
Runtime Validation \= 실행 준비 검증 계약  
Registry Specs \= 통제된 어휘와 식별자 관리  
Implementation Plan \= 구현 순서  
Source Code \= 승인된 사양의 구현

이 분리는 모든 문서와 코드에서 유지되어야 한다.

---

## **7\. Master Architecture 문서 구성**

`00_master_architecture`는 다음 최상위 문서를 포함한다.

00\_master\_architecture/  
  README.md  
  00\_ledo\_first\_constitution.md  
  01\_ledo\_master\_architecture.md  
  02\_document\_control\_map.md  
  03\_source\_of\_truth\_matrix.md  
  04\_code\_generation\_strategy.md

문서별 역할은 다음과 같다.

| 문서 | 역할 |
| ----- | ----- |
| `README.md` | 이 폴더의 목적과 아키텍처 역할을 설명한다 |
| `00_ledo_first_constitution.md` | 시스템에서 절대 깨면 안 되는 최상위 원칙을 정의한다 |
| `01_ledo_master_architecture.md` | 전체 시스템 아키텍처와 레이어 관계를 정의한다 |
| `02_document_control_map.md` | 어떤 문서가 어떤 개념의 원본인지 정의한다 |
| `03_source_of_truth_matrix.md` | 의미, 증거, 상태, 정책, 검증, 실행, 감사의 권한 주체를 정의한다 |
| `04_code_generation_strategy.md` | 아키텍처 문서를 구현 산출물로 변환하는 순서를 정의한다 |
| `05_codex_architecture_review_prompt.md` | 구현 전 전체 아키텍처 검토 기준을 정의한다 |

---

## **8\. Source of Truth 원칙**

동일한 개념이 여러 문서에서 다르게 정의되면 안 된다.

Master Architecture는 주요 개념의 원본 위치를 지정한다.

| 개념 | Source of Truth |
| ----- | ----- |
| 절대 원칙과 경계 | `00_ledo_first_constitution.md` |
| 전체 아키텍처와 레이어 관계 | `01_ledo_master_architecture.md` |
| 문서별 개념 소유권 | `02_document_control_map.md` |
| 의미, 증거, 상태, 정책, 실행 권한 | `03_source_of_truth_matrix.md` |
| 코드 생성 순서 | `04_code_generation_strategy.md` |
| 온톨로지 모델링 상세 원칙 | `04_ontology_foundation/` |
| 운영 객체와 생명주기 계약 | `03_core_specifications/` |
| Runtime Validation과 Safety Gate 규칙 | `08_runtime_validation/` |
| Registry 구조와 버전 관리 | `06_registry_specs/` |

하위 문서는 이 원칙을 참조할 수 있다.  
그러나 서로 다르게 재정의해서는 안 된다.

---

## **9\. 하위 계층과의 관계**

`00_master_architecture`는 하위 문서의 세부 내용을 반복하지 않는다.

의미 모델링 상세       → 04\_ontology\_foundation/  
운영 계약 상세         → 03\_core\_specifications/  
Registry 상세          → 06\_registry\_specs/  
실행 검증 상세         → 08\_runtime\_validation/  
구현 계획 상세         → 07\_implementation\_plan/  
도메인별 의미 확장     → 05\_domain\_ontology\_modules/

이 폴더의 역할은 하위 문서가 서로 충돌하지 않도록 방향과 경계를 통제하는 것이다.

---

## **10\. 공용 아키텍처 원칙**

이 폴더의 문서는 공용 수출형 아키텍처로 유지되어야 한다.

벤더 중립적으로 작성한다.  
도구 중립적으로 작성한다.  
특정 구현체에 종속되지 않도록 작성한다.  
도메인별 실제 규칙을 임의로 포함하지 않는다.  
세부 기술 설명보다 아키텍처 경계와 책임을 우선한다.

세부 구현 방식, 특정 도구 사용법, 내부 작업 지시는 별도 운영 문서에서 다룬다.

---

## **11\. 최종 원칙**

`00_master_architecture`의 목적은 전체 프로젝트에 하나의 명확한 아키텍처 방향을 부여하는 것이다.

이 폴더는 아키텍처를 통제한다.  
하위 폴더는 세부 내용을 정의한다.  
원칙은 강하게 유지한다.  
경계는 명확하게 유지한다.  
의미와 실행은 분리한다.  
모든 구현은 이 경계를 따라야 한다.

최종 원칙은 다음과 같다.

이 폴더는 아키텍처를 정의한다.  
하위 폴더는 세부 내용을 정의한다.

