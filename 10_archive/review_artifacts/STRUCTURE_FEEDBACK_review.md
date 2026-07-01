> Historical Review Artifact
>
> This document records an architecture review result.
> It is not an architecture source-of-truth document.
> If this document conflicts with AGENTS.md or 00_master_architecture/, AGENTS.md and 00_master_architecture/ take precedence.

# LEDO 전체 문서 아키텍처 검토 리포트

## 1. Executive Summary

- 전체 판단: **PASS WITH WARNINGS**.
- P0로 볼 만한 "LEDO가 기본적으로 실제 물리 명령을 직접 실행한다"는 문서 선언은 확인되지 않았다.
- 가장 중요한 위험은 `ApprovedAction`과 `Safety Gate`의 생성 순서가 일부 문서에서 뒤집혀 있다는 점이다.
- 본격 코드 구현 전 반드시 정리할 P1 영역:
  - `ApprovedAction` 생성 주체와 `SafetyGatePass`의 역할
  - `ExecutionCommand` 용어
  - Emergency/Failsafe fast-path의 Runtime Validation / Safety Gate 명시
  - Common DTO 문서의 Runtime Validation DTO 공백
- 진행 가능 여부: 아키텍처 방향은 진행 가능하지만, P1/P2 정리 없이 구현하면 Safety Gate와 Approval 경계가 코드에서 붕괴될 위험이 있다.

## 2. Repository Document Map

실제 확인한 주요 Markdown 구조:

- Root: `AGENTS.md`, `PROJECT_TREE.md`, `STRUCTURE_FEEDBACK.md`
- Root `README.md`: 현재 작업트리 기준 확인되지 않음.
- `00_master_architecture/`: `README.md`, `00_first_construction.md`, `01_master_architecture.md`
- `01_layer_architecture/`: `layer.md`
- `02_layer_stack_mapping/`: Layer 00-12 stack mapping 문서
- `03_core_specifications/`: canonical lifecycle, DTO, event/action/state/evidence/decision/policy/execution/audit 계열 문서
- `04_ontology_foundation/`: foundation report, semantic web stack, upper ontology, standards, OWL, reasoning/constraints, property design, governance/versioning
- `05_domain_ontology_modules/`: domain extension README 및 action/ai/core/event/evidence/industrial/robot 등 module specs와 implementation guides
- `06_registry_specs/`: action, adapter, approval, decision, event, evidence, external system, identity, model adapter, ontology, policy, snapshot schema, state registry
- `07_implementation_plan/`: implementation plan 및 MVP phase 문서
- `08_runtime_validation/`: validators, TOCTOU, SHACL shapes, network health, idempotency, safety gate

폴더별 역할은 대체로 AGENTS.md의 구조 의도와 정렬되어 있다. 단, source-of-truth 파일명 참조 불일치가 있다.

## 3. Canonical Architecture 기준

유지되어야 할 기준 flow:

`Physical World -> Real-Time World State -> Knowledge / Evidence Binding -> Distributed Domain Agents -> ActionCandidate -> Semantic Validation -> Evidence Check -> Policy Check -> Decision Router -> Approval -> ApprovedAction -> Runtime Validation -> Safety Gate -> SafetyGatePass/Block -> ExecutionRequest -> ExternalControlRequest -> External System -> Physical World -> Feedback -> Audit -> World State Update`

source-of-truth boundary:

- Ontology: meaning authority
- Evidence: judgment support, not AI output itself
- Policy: operational permission
- Approval: high-risk authority
- Runtime Validation: execution-time condition checks
- Safety Gate: final deterministic pass/block
- ExecutionRequest: physical command 아님
- External System: 실제 physical execution authority
- Audit: decision path accountability

execution boundary:

- `ApprovedAction`은 물리 명령이 아니다.
- `ExecutionRequest`도 물리 명령이 아니다.
- `ExternalControlRequest`도 외부 시스템에 전달되는 요청이지 LEDO 내부 physical command가 아니다.

## 4. Terminology Dictionary

| Preferred Term | Alternative Terms | Definition | Source Area | Related Layer | Stability |
|---|---|---|---|---|---|
| Ontology | Semantic authority | 의미, class, relation, property의 권위 | 04, 00 | Core Ontology | Stable |
| TBox | Terminology box | class/property/axiom 구조 | 04 | Ontology Foundation | Stable |
| ABox | Assertion box | instance assertion/data graph | 04 | Knowledge Memory | Stable |
| IRI | URI identifier | semantic object 식별자 | 04 | Ontology | Stable |
| Canonical Identity | canonical id | 동일성 해석 결과 | 03, 06 | Identity | Medium |
| Ontology Binding | semantic binding | canonical object를 ontology term에 연결 | 03, 04 | Semantic | Stable |
| Evidence Binding | evidence link | 판단 객체와 evidence refs 연결 | 03 | Evidence | Stable |
| World State | current state | 현재 운영 상태 표현 | 01, 02, 03 | Real-Time State | Stable |
| Event | signal/change | 상태 변화 후보/발생 기록 | 03, 06 | Event | Stable |
| State | live fact | 현재 조건/상태값 | 03, 06 | World State | Stable |
| Snapshot | materialized snapshot | runtime validation/Safety Gate용 고정 view | 08, 06 | Runtime | Stable |
| Evidence | validated support | provenance/trust/time/source 있는 판단 근거 | 03 | Evidence | Stable |
| EvidenceBundle | evidence refs bundle | 여러 evidence 참조 묶음; agent가 primary evidence로 만들면 안 됨 | 03, 02 | Evidence | Medium |
| Policy | permission rule | 운영 허용 여부 판단 | 03, 06 | Governance | Stable |
| ActionCandidate | proposed action | agent/router가 제안한 실행 후보 | 03 | Agent/Decision | Stable |
| DecisionCase | routed case | risk/priority/approval path 판단 케이스 | 03 | Decision Router | Stable |
| Approval | authority grant | 고위험 권한 부여 | 03 | Approval | Stable |
| ApprovedAction | approved intent | approval 이후의 승인된 의도; Safety Gate pass 아님 | 03, 08 | Approval | Needs clarification |
| Runtime Validation | condition validation | execution 직전 상태/TOCTOU/idempotency/network 검증 | 08 | Runtime | Stable |
| Safety Gate | final gate | precomputed 결과만 읽는 deterministic pass/block | 08 | Safety Gate | Stable |
| SafetyGatePass | pass lease | 짧은 수명, 재사용 불가 실행 준비 token | 08 | Safety Gate | Stable |
| ExecutionRequest | execution intent request | 외부 시스템 전달용 고수준 요청 | 03, 11 | Execution Integration | Stable |
| ExternalControlRequest | adapter request | 외부 제어 시스템에 전달되는 요청 | 03, 11 | External Integration | Stable |
| FeedbackEvent | feedback | 외부 결과/상태 회신 이벤트 | 03 | Feedback | Stable |
| AuditRecord | audit trace | 의미 있는 결정 경로 기록 | 03 | Audit | Stable |
| Materialized View | runtime map | hot path용 사전 계산 view | 04, 08 | Runtime | Stable |
| Safety Snapshot | SafetyGateSnapshot | Safety Gate가 읽는 precomputed snapshot | 08 | Safety Gate | Stable |
| SHACL Shape | data shape | 구조/필수 필드/shape 검증 | 04, 08 | Validation | Stable |
| SPARQL Query | graph query | graph 관계 조회/검증; hot path 금지 | 04 | Semantic Query | Stable |
| Reasoner | OWL reasoner | offline/background inference | 04 | Ontology | Stable |
| External System | physical executor | 실제 실행 권한을 가진 외부 시스템 | 02, 06 | Physical Boundary | Stable |
| Adapter | integration adapter | request 변환/전달 경계; physical executor 아님 | 06, 11 | Integration | Medium |

## 5. Key Issues

### LEDO-DOC-P1-01

- Severity: P1
- Category: Flow Consistency / Safety Gate Boundary
- Title: `ApprovedAction`과 `Safety Gate` 생성 순서가 문서마다 다름
- File Path: `02_layer_stack_mapping/09_approved_action_safety_gate_stack_mapping.md`, `03_core_specifications/00_canonical_object_lifecycle/0_canonical_object_lifecycle.md`, `03_core_specifications/01_common_schema_dto/1_common_schema_dto.md`
- Related File Path: `08_runtime_validation/safety_gate/safety_gate.md`
- Description: 일부 문서는 Safety Gate가 `ActionCandidate -> ApprovedAction`을 만든다고 설명하고, runtime 문서는 `ApprovedAction -> RuntimeValidationResult -> SafetyGatePass -> ExecutionRequest`로 설명한다.
- Evidence: `ApprovedActionDTO -> created by safety_gate`, `Safety Gate determines whether ActionCandidate can become ApprovedAction`, 반면 Safety Gate 문서는 `between ApprovedAction and ExecutionRequest`라고 정의.
- Why It Matters: Approval, Runtime Validation, Safety Gate 경계가 무너지면 "No approval, no ApprovedAction"과 "No Safety Gate pass, no ExecutionRequest"가 코드에서 충돌한다.
- Recommended Fix: canonical lifecycle을 `DecisionCase -> ApprovalRequest/Decision -> ApprovedAction -> RuntimeValidationResult -> SafetyGatePass/Block -> ExecutionRequest`로 고정.
- Auto-fix Safe: No
- Suggested Patch Scope: lifecycle, common DTO, layer 9 mapping, action registry 문서 정렬.

### LEDO-DOC-P1-02

- Severity: P1
- Category: Source of Truth / Markdown Structure
- Title: AGENTS.md의 master architecture 파일 참조가 실제 파일명과 다름
- File Path: `AGENTS.md`
- Related File Path: `00_master_architecture/00_first_construction.md`, `00_master_architecture/01_master_architecture.md`
- Description: AGENTS.md는 `00_ledo_first_constitution.md`, `01_ledo_master_architecture.md`를 source-of-truth로 지칭하지만 실제 파일은 다른 이름이다.
- Evidence: 실제 확인 파일은 `00_first_construction.md`, `01_master_architecture.md`.
- Why It Matters: Codex 또는 자동 검토 도구가 constitution을 찾지 못하면 안전 원칙 적용 누락으로 이어질 수 있다.
- Recommended Fix: 실제 파일명과 source-of-truth 참조를 한쪽으로 정렬.
- Auto-fix Safe: No
- Suggested Patch Scope: AGENTS.md와 master architecture index.

### LEDO-DOC-P1-03

- Severity: P1
- Category: External Execution Boundary / Emergency Flow
- Title: Emergency/Failsafe fast-path에서 Runtime Validation/Safety Gate 경계가 일부 생략됨
- File Path: `03_core_specifications/00_canonical_object_lifecycle/0_canonical_object_lifecycle.md`, `03_core_specifications/04_state_model_registry/4_state_model_registry.md`
- Related File Path: `08_runtime_validation/safety_gate/safety_gate.md`, `08_runtime_validation/toctou/toctou.md`
- Description: emergency flow가 `EmergencyApprovedAction -> EmergencyExecutionRequest -> ExternalControlRequest`로 바로 이어지는 표현이 있다.
- Evidence: lifecycle 문서의 emergency fast-path와 state fail-safe interception flow.
- Why It Matters: emergency path는 가장 안전 민감한 경로이므로 "fast"가 "Safety Gate bypass"로 구현되면 P0급 위험이 된다.
- Recommended Fix: emergency도 deterministic precomputed runtime validation과 emergency-specific SafetyGatePass/Block을 거치도록 명시.
- Auto-fix Safe: No
- Suggested Patch Scope: lifecycle emergency section, state model fail-safe section.

### LEDO-DOC-P1-04

- Severity: P1
- Category: Terminology / Execution Boundary
- Title: `ExecutionCommand` 용어가 physical command와 혼동될 수 있음
- File Path: `02_layer_stack_mapping/10_unified_cyber_physical_core_stack_mapping.md`
- Related File Path: `02_layer_stack_mapping/11_execution_request_external_control_integration_stack_mapping.md`, `00_master_architecture/00_first_construction.md`
- Description: Layer 10이 `ExecutionCommand Schema`, `Command Lifecycle`를 언급한다. 문서상 physical command가 아니라고 제한하지만 용어 자체가 execution boundary를 약화시킨다.
- Evidence: Unified Core가 `execution requests, execution commands`를 정규화한다고 설명.
- Why It Matters: 구현자가 `ExecutionCommand`를 외부 제어 payload 또는 physical command로 오해할 수 있다.
- Recommended Fix: `DispatchRecord`, `ExecutionLifecycleRecord`, `InternalExecutionIntentRecord` 등 비물리 용어로 제한하거나 강한 금지 정의 추가.
- Auto-fix Safe: No
- Suggested Patch Scope: Layer 10, execution model, glossary.

### LEDO-DOC-P1-05

- Severity: P1
- Category: Practicality / Implementability
- Title: Common DTO 문서에 Runtime Validation 핵심 DTO가 부족함
- File Path: `03_core_specifications/01_common_schema_dto/1_common_schema_dto.md`
- Related File Path: `08_runtime_validation/*`
- Description: runtime docs는 `RuntimeValidationResult`, `SafetyGatePass`, `SafetyGateBlock`, `SafetySnapshot`, `TOCTOUResult`, `IdempotencyResult` 등을 요구하지만 common DTO 필수 목록에는 충분히 반영되지 않았다.
- Evidence: implementation plan은 `BaseRuntimeValidation`, `BaseSafetyGateResult`를 언급하지만 common schema의 MVP DTO 정의와 불일치.
- Why It Matters: 코드 생성이 common DTO 기준으로 시작되면 Safety Gate 입력/출력 contract가 누락될 수 있다.
- Recommended Fix: runtime validation DTO contract를 common schema 또는 runtime schema 문서의 source-of-truth로 명확히 지정.
- Auto-fix Safe: No
- Suggested Patch Scope: common DTO, runtime validation schema appendix.

### LEDO-DOC-P1-06

- Severity: P1
- Category: Runtime Validation / Responsibility Conflict
- Title: Decision Matrix의 SafetyGatePrecheck가 Runtime Validation 책임과 중복됨
- File Path: `03_core_specifications/07_decision_approval_matrix/07_decision_approval_matrix.md`
- Related File Path: `08_runtime_validation/validators/validators.md`
- Description: Decision/Approval Matrix가 TOCTOU, network, idempotency 성격의 precheck를 포함한다.
- Evidence: `SafetyGatePrecheck`와 runtime validator류 조건이 decision 문서에 함께 등장.
- Why It Matters: precheck와 final validation이 서로 다른 결과를 내면 policy/approval/routing 경로가 divergence된다.
- Recommended Fix: Decision Matrix는 routing/precheck만 수행하고, executable validation result는 `08_runtime_validation`만 소유하도록 참조화.
- Auto-fix Safe: No
- Suggested Patch Scope: decision approval matrix, runtime validators.

### LEDO-DOC-P2-07

- Severity: P2
- Category: AI / LLM Governance / Evidence
- Title: Agent output의 `EvidenceBundle` 표현이 Evidence 생성 권한처럼 보일 수 있음
- File Path: `02_layer_stack_mapping/07_distributed_domain_agent_stack_mapping.md`
- Related File Path: `03_core_specifications/05_evidence_model/5_evidence_model.md`
- Description: Agent output stack에 `EvidenceBundle`이 포함되어 있다. 문맥상 evidence refs binding으로 보이나, agent가 evidence 자체를 만든다고 오해될 수 있다.
- Evidence: Layer 7 agent output 목록.
- Why It Matters: "AI output is not Evidence" 원칙과 충돌 가능.
- Recommended Fix: `EvidenceBundleRef`, `EvidenceBindingProposal`, `EvidenceReferenceSet`로 용어 정리.
- Auto-fix Safe: No
- Suggested Patch Scope: Layer 7, evidence glossary.

### LEDO-DOC-P2-08

- Severity: P2
- Category: Evidence / Audit
- Title: AI-derived evidence 용어가 안전하지만 혼동 가능
- File Path: `03_core_specifications/05_evidence_model/5_evidence_model.md`
- Related File Path: `05_domain_ontology_modules/ai/*`
- Description: 문서는 AI output이 primary evidence가 아니라고 분명히 말하지만 `AI_SUMMARY_EVIDENCE`, `AI_DERIVED` 같은 이름은 오용될 수 있다.
- Evidence: Evidence category naming.
- Why It Matters: 구현자가 AI summary를 원본 evidence처럼 저장할 위험.
- Recommended Fix: AI summary는 `EvidenceSummary` 또는 `DerivedEvidenceCandidate`로 구분하고, attestation/source refs 없이는 Evidence 불가를 명시.
- Auto-fix Safe: No
- Suggested Patch Scope: evidence model, AI ontology module.

### LEDO-DOC-P2-09

- Severity: P2
- Category: Concept Duplication / Registry Boundary
- Title: Core Specification과 Registry Spec이 action/state 책임을 중복 정의함
- File Path: `03_core_specifications/03_action_type_registry/03_action_type_registry.md`, `03_core_specifications/04_state_model_registry/4_state_model_registry.md`
- Related File Path: `06_registry_specs/action_registry/action_registry.md`, `06_registry_specs/state_registry/state_registry.md`
- Description: core 문서와 registry 문서가 모두 schema, lifecycle, examples, validation concerns를 정의한다.
- Evidence: action/state registry-like contract가 03과 06에 모두 존재.
- Why It Matters: 시간이 지나면 action type, state model, validation reference가 서로 달라질 수 있다.
- Recommended Fix: 03은 lifecycle/semantic contract, 06은 registry entry schema/version/loader/validator source-of-truth로 분리.
- Auto-fix Safe: No
- Suggested Patch Scope: core specs and registry specs cross-reference cleanup.

### LEDO-DOC-P2-10

- Severity: P2
- Category: Domain Module Boundary
- Title: Framework 문서에 domain-like 예시값이 많아 hard-code 위험이 있음
- File Path: `03_core_specifications/*`, `06_registry_specs/*`, `02_layer_stack_mapping/*`
- Related File Path: `05_domain_ontology_modules/README.md`
- Description: `STOP_WORK`, `DISPATCH_ROBOT`, worker/robot/path/gas/zone/role/freshness 같은 예시가 많다. 대부분 예시 의도로 보이나, 구현자가 실제 domain rule로 오인할 수 있다.
- Evidence: action registry/state registry/policy examples.
- Why It Matters: Codex가 domain meaning을 추측해 구현할 위험.
- Recommended Fix: 예시 섹션에 "non-normative placeholder, domain expert governed" 라벨을 반복하지 말고 한 source-of-truth로 연결.
- Auto-fix Safe: No
- Suggested Patch Scope: examples disclaimer and domain pack boundary.

### LEDO-DOC-P2-11

- Severity: P2
- Category: External Execution Boundary / Adapter Boundary
- Title: Adapter interface의 `execute()` 표현이 물리 실행처럼 보일 수 있음
- File Path: `06_registry_specs/adapter_registry/adapter_registry.md`
- Related File Path: `02_layer_stack_mapping/11_execution_request_external_control_integration_stack_mapping.md`
- Description: adapter는 external request boundary여야 하나 minimal interface가 `execute(request)` 형태다.
- Evidence: BaseAdapter execute signature.
- Why It Matters: mock-first와 no physical actuation default 원칙 약화.
- Recommended Fix: `submit_request`, `dispatch_external_request`, `dry_run_dispatch` 같은 용어와 mock/dry-run 기본값 명시.
- Auto-fix Safe: No
- Suggested Patch Scope: adapter registry, external integration spec.

### LEDO-DOC-P2-12

- Severity: P2
- Category: Runtime Validation / Snapshot
- Title: Snapshot/materialized view 책임이 여러 문서에 분산됨
- File Path: `04_ontology_foundation/*`, `06_registry_specs/snapshot_schema_registry/*`, `08_runtime_validation/*`
- Related File Path: `00_master_architecture/01_master_architecture.md`
- Description: snapshot, materialized view, runtime map, SafetyGateSnapshot 설명이 여러 곳에 반복된다.
- Evidence: reasoning model, governance/versioning, runtime safety gate, snapshot registry.
- Why It Matters: hot path input schema가 분산되면 Safety Gate 구현이 임의 해석을 하게 된다.
- Recommended Fix: `snapshot_schema_registry` 또는 `08_runtime_validation/safety_gate` 중 하나를 input/output schema source-of-truth로 지정.
- Auto-fix Safe: No
- Suggested Patch Scope: snapshot docs cross-reference.

### LEDO-DOC-P2-13

- Severity: P2
- Category: Evidence / Audit / Flow Consistency
- Title: 일부 emergency/common flow에서 Audit trace 대상이 충분히 명시되지 않음
- File Path: `03_core_specifications/00_canonical_object_lifecycle/0_canonical_object_lifecycle.md`, `03_core_specifications/01_common_schema_dto/1_common_schema_dto.md`
- Related File Path: `07_implementation_plan/implementation_plan.md`
- Description: implementation plan은 audit target을 강하게 정의하지만 일부 lifecycle/DTO emergency flow는 RuntimeValidation/SafetyGateResult audit refs가 약하다.
- Evidence: emergency flow가 post-hoc audit 중심으로 표현됨.
- Why It Matters: "No audit, no trust" 원칙상 emergency path도 trace completeness가 필요하다.
- Recommended Fix: AuditRecord refs에 Event, Evidence, Decision, Approval, RuntimeValidation, SafetyGate, ExecutionRequest, Feedback를 mandatory link로 정리.
- Auto-fix Safe: No
- Suggested Patch Scope: lifecycle, DTO, audit model.

### LEDO-DOC-P3-14

- Severity: P3
- Category: Markdown Structure
- Title: encoding/mojibake와 번호 누락은 구조 이슈는 아니나 가독성 저하
- File Path: multiple Markdown files
- Related File Path: N/A
- Description: 일부 문서에 깨진 문자와 번호 점프가 보인다.
- Evidence: registry README 등에서 garbled text 확인.
- Why It Matters: 현재는 architecture boundary를 깨지는 않지만 review 품질과 자동 문서 파싱에는 영향 가능.
- Recommended Fix: 나중에 formatting cleanup PR에서만 처리.
- Auto-fix Safe: No
- Suggested Patch Scope: dedicated low-risk cleanup only.

## 6. Concept Duplication Report

의도적 반복:

- "ExecutionRequest is not PhysicalCommand"
- "AI output is candidate, not truth"
- "Safety Gate reads precomputed results only"
- "External systems execute physical control"

이 반복은 안전 invariant로서 유익하다.

위험한 중복:

- `ApprovedAction` 정의가 core lifecycle, DTO, action registry, layer 9에서 다르게 반복됨.
- `Safety Gate`가 어떤 문서에서는 ApprovedAction 생성 전, runtime 문서에서는 ApprovedAction 이후로 배치됨.
- action/state registry 책임이 `03_core_specifications`와 `06_registry_specs`에 중복됨.

consolidation 후보:

- ApprovedAction lifecycle
- SafetyGatePass/Block DTO
- Snapshot schema and materialized runtime map
- emergency fast-path lifecycle

reference-link 후보:

- Core specs는 registry schema를 재정의하지 말고 `06_registry_specs` 참조.
- Layer mapping은 detailed validator를 재정의하지 말고 `08_runtime_validation` 참조.
- Domain modules는 실제 domain values를 정의하지 말고 governed domain pack 참조.

## 7. Layer Boundary & Responsibility Conflict Report

충돌 발견 사항:

- Layer 9가 `ApprovedAction`을 만드는 것처럼 표현된 부분은 Approval layer와 Safety Gate layer를 섞는다.
- Layer 10의 `ExecutionCommand`는 Unified Core와 External Control Integration 경계를 흐린다.
- Decision Matrix의 SafetyGatePrecheck는 Runtime Validation과 중복된다.
- Agent output의 EvidenceBundle은 Evidence 생성 권한과 혼동될 수 있다.

올바른 책임 경계:

- Agent: candidate/proposal only.
- Decision Router: route/classify only.
- Policy: permission only.
- Approval: authority only.
- Runtime Validation: current validity checks.
- Safety Gate: final pass/block only.
- External Integration: request translation/dispatch boundary.
- External System: physical execution.

권장 수정 방향:

- `ApprovedAction`은 approval 이후 객체로 고정.
- `SafetyGatePass`는 execution readiness lease로 고정.
- `ExecutionRequest`는 `SafetyGatePass` 없이는 생성 불가.
- `ExecutionCommand`는 제거 또는 internal non-physical lifecycle record로 제한.

## 8. Flow Consistency Report

canonical flow는 master architecture, layer architecture, implementation plan, runtime validation 문서에서는 대체로 유지된다.

문서별 alternative flow:

- `03_core_specifications/00_canonical_object_lifecycle`: 일부 standard/emergency flow에서 Safety Gate가 ApprovedAction보다 앞에 배치됨.
- `02_layer_stack_mapping/09`: Safety Gate가 ActionCandidate를 ApprovedAction으로 만드는 것으로 표현됨.
- `03_core_specifications/01_common_schema_dto`: `ApprovedActionDTO created by safety_gate` 표현.
- `07_implementation_plan/implementation_plan.md`: 구현 순서는 `Approval -> Runtime Validation -> Safety Gate -> ExecutionRequest`로 올바르게 정렬되어 있음.

누락 또는 순서 오류:

- 일부 emergency/fail-safe path에서 Runtime Validation/Safety Gate 명시 부족.
- 일부 audit 흐름에서 SafetyGateResult/RuntimeValidationResult 참조 부족.

수정 제안:

- 모든 flow diagram에서 `Approval -> ApprovedAction -> RuntimeValidationResult -> SafetyGatePass/Block -> ExecutionRequest` 순서를 강제.

## 9. Safety Gate / Runtime Hot Path Risk Report

준수 확인:

- `08_runtime_validation/safety_gate/safety_gate.md`는 OWL reasoning, full SHACL, SPARQL, graph DB call, LLM/SLM, external API, disk I/O, unbounded computation을 hot path에서 금지한다.
- `04_ontology_foundation/04_reasoning_and_constraint_model.md`도 heavy semantic operation을 precompute/materialize하는 방향이다.
- `08_runtime_validation/*` 문서는 RuntimeValidationResult를 Safety Gate 입력으로 두는 구조가 강하다.

위험:

- Layer 9와 일부 core specs가 Safety Gate 책임을 넓게 표현해 runtime validator/approval creation까지 흡수할 수 있다.
- snapshot/materialized map schema source-of-truth가 분산되어 구현자가 임의 필드셋을 만들 수 있다.

위험도: P1/P2.

## 10. Registry Boundary Report

역할 충돌:

- action type registry와 action registry가 core/registry 문서에 중복된다.
- state model registry와 state registry도 유사하게 중복된다.
- adapter registry와 external system registry는 대체로 잘 분리되어 있으나 `execute()` 용어가 경계 혼동을 만든다.

source-of-truth 침범 여부:

- `06_registry_specs/README.md`는 registry가 meaning을 정의하지 않는다고 명시해 안전하다.
- 실제 action/state examples가 많아 registry가 domain meaning source-of-truth처럼 보일 수 있는 부분은 P2.

권장:

- Registry spec = entry schema, versioning, validation reference, loader contract.
- Core spec = lifecycle and object responsibility.
- Domain module/domain pack = governed domain meaning.

## 11. Ontology Foundation & Standards Alignment Report

정렬 상태:

- Foundation은 small but strong upper structure를 지향한다.
- BFO는 copied ontology가 아니라 category discipline으로 쓰인다.
- RDF/RDFS/OWL/SHACL/SPARQL/SKOS/PROV-O/OWL-Time/GeoSPARQL 역할 분리는 강하다.
- OWL reasoning은 offline/background, SHACL은 data shape, SPARQL은 query/graph validation으로 분리된다.
- Safety Gate hot path에는 materialized map/snapshot만 들어가야 한다는 기준이 명확하다.
- governance/versioning 문서는 version, migration, rollback, audit, SLM/LoRA compatibility를 포함한다.

주의:

- relationship/property 문서에서 `controls`류 broad relation은 execution authority로 오해되지 않도록 세분 property 사용이 필요하다.
- external standards는 copied가 아니라 mapped라는 원칙은 잘 유지된다.

## 12. Domain Module Boundary Report

확인 결과:

- `05_domain_ontology_modules/README.md`는 domain guessing 금지, Runtime Validation 우회 금지, physical command 정의 금지, registry 연결을 명확히 둔다.
- industrial/robot 등 implementation guide는 "placeholder", "human domain expert must provide real meaning", "no physical robot/PLC/SCADA control"을 반복한다.
- domain modules가 Foundation을 override하거나 Safety Gate를 bypass한다는 직접 선언은 확인되지 않았다.

주의:

- framework/core/registry 쪽의 domain-like examples가 많아, domain module boundary와 반대로 core가 domain meaning을 흡수하는 것처럼 보일 수 있다.
- 실제 domain values는 domain expert review 후 domain pack/registry extension으로 이동해야 한다.

## 13. Implementation Practicality Report

바로 구현 가능한 수준 Strong:

- `08_runtime_validation/safety_gate`
- `08_runtime_validation/validators`
- `08_runtime_validation/toctou`
- `08_runtime_validation/idempotency`
- `04_ontology_foundation/04_reasoning_and_constraint_model`
- `07_implementation_plan/implementation_plan.md`의 phase order

Medium:

- common DTO: base fields는 강하지만 runtime validation DTO 보강 필요.
- registry specs: entry 구조와 governance는 강하지만 core spec과 책임 중복 정리 필요.
- external integration: boundary는 강하지만 adapter method naming 주의 필요.

Weak/Risky:

- `ApprovedAction` lifecycle 정의가 문서마다 달라 그대로 코드화하면 위험.
- emergency/fail-safe path는 빠른 경로와 Safety Gate의 관계를 더 구체화해야 한다.
- domain examples는 placeholder/non-normative 표시가 약하면 Codex가 domain meaning을 추측할 위험.

## 14. Test & Verification Gap Report

Test name: ActionCandidate cannot become ExecutionRequest without Decision/Approval/Safety Gate

- Purpose: candidate-to-execution shortcut 차단
- Input: ActionCandidate only
- Expected result: ExecutionRequest creation blocked
- Related document: `03_core_specifications/00_canonical_object_lifecycle`
- Related module: decision/runtime/safety_gate

Test name: Safety Gate blocks stale snapshot

- Purpose: stale SafetySnapshot 차단
- Input: ApprovedAction + stale snapshot
- Expected result: SafetyGateBlock
- Related document: `08_runtime_validation/safety_gate/safety_gate.md`
- Related module: validation/safety_gate

Test name: Safety Gate blocks missing idempotency key

- Purpose: duplicate physical intent 방지
- Input: ApprovedAction without idempotency key
- Expected result: SafetyGateBlock
- Related document: `08_runtime_validation/idempotency/idempotency_control.md`
- Related module: validation/idempotency

Test name: Safety Gate blocks terminal SafetyGatePass replay

- Purpose: pass lease 재사용 차단
- Input: consumed SafetyGatePass
- Expected result: blocked replay
- Related document: `08_runtime_validation/safety_gate/safety_gate.md`
- Related module: safety_gate

Test name: Runtime Validation blocks stale Tier 1 state

- Purpose: current state freshness 보장
- Input: expired runtime state
- Expected result: RuntimeValidationResult fail
- Related document: `08_runtime_validation/validators/validators.md`
- Related module: validation/state

Test name: Agent output cannot become Evidence

- Purpose: AI/Evidence boundary 보존
- Input: AI summary without original evidence refs
- Expected result: Evidence creation rejected
- Related document: `03_core_specifications/05_evidence_model/5_evidence_model.md`
- Related module: evidence/agent

Test name: Policy pass does not equal Approval pass

- Purpose: policy/approval 분리
- Input: policy allow without approval
- Expected result: no ApprovedAction
- Related document: `03_core_specifications/07_decision_approval_matrix`
- Related module: policy/approval

Test name: Approval pass does not equal Safety Gate pass

- Purpose: approval/runtime 분리
- Input: ApprovedAction with failing runtime validation
- Expected result: no ExecutionRequest
- Related document: `08_runtime_validation/safety_gate/safety_gate.md`
- Related module: approval/safety_gate

Test name: ExecutionRequest is not PhysicalCommand

- Purpose: execution boundary 보존
- Input: ExecutionRequest
- Expected result: no direct actuator command emitted
- Related document: `02_layer_stack_mapping/11_execution_request_external_control_integration_stack_mapping.md`
- Related module: adapters

Test name: ExternalControlRequest requires feedback correlation

- Purpose: closed-loop 보장
- Input: ExternalControlRequest without feedback correlation id
- Expected result: request invalid or audit warning/block
- Related document: `07_implementation_plan/implementation_plan.md`
- Related module: feedback/audit

Test name: Audit trace links Event to Feedback

- Purpose: accountability 보장
- Input: full lifecycle trace
- Expected result: AuditRecord links Event -> Evidence -> Decision -> Approval -> RuntimeValidation -> SafetyGate -> ExecutionRequest -> Feedback
- Related document: `03_core_specifications/10_audit_observability_model`
- Related module: audit

## 15. Risk Matrix

| Risk ID | Severity | Area | Summary | Fix Priority |
|---|---|---|---|---|
| R1 | P1 | Safety Gate | ApprovedAction/Safety Gate 순서 충돌 | 1 |
| R2 | P1 | Source of Truth | AGENTS.md 파일 참조 불일치 | 1 |
| R3 | P1 | Emergency Flow | emergency path validation boundary 약함 | 1 |
| R4 | P1 | Execution Boundary | ExecutionCommand 용어 위험 | 1 |
| R5 | P1 | DTO | Runtime validation DTO 공백 | 1 |
| R6 | P1 | Runtime Validation | Decision precheck와 validator 중복 | 2 |
| R7 | P2 | Evidence | Agent EvidenceBundle 용어 위험 | 2 |
| R8 | P2 | Registry | Core/Registry 중복 | 2 |
| R9 | P2 | Domain Boundary | domain examples hard-code 위험 | 3 |
| R10 | P2 | Adapter | execute() 용어 위험 | 3 |
| R11 | P3 | Markdown | encoding/번호/가독성 | 5 |

## 16. Prioritized Recommendation

- Priority 1: `ApprovedAction`, `RuntimeValidationResult`, `SafetyGatePass`, `ExecutionRequest` lifecycle을 먼저 단일화.
- Priority 2: AGENTS.md와 `00_master_architecture` source-of-truth 참조 정렬.
- Priority 3: Common DTO에 runtime validation/Safety Gate DTO contract 보강.
- Priority 4: Core specs와 Registry specs의 책임을 분리하고 중복 설명을 reference-link로 전환.
- Priority 5: emergency/fail-safe path에 deterministic runtime validation과 Safety Gate pass/block을 명시.
- Priority 6: `ExecutionCommand`, `EvidenceBundle`, `AI_*_EVIDENCE`, adapter `execute()` 용어 정리.
- Priority 7: domain examples는 non-normative placeholder로 분리.
- Priority 8: critical flow test/checklist 추가.
- Priority 9: formatting/encoding cleanup은 별도 낮은 위험 PR에서 처리.

## 17. Proposed PR Plan

### PR 1: Source-of-truth and boundary clarification

- Purpose: AGENTS.md와 master docs 참조 정렬
- Files likely affected: `AGENTS.md`, `00_master_architecture/*`
- Risk level: Medium
- Test / verification plan: doc link check, constitution path check
- Rollback plan: previous references restore
- Review notes: 파일명 스타일 논쟁이 아니라 broken source-of-truth 방지 목적

### PR 2: Terminology dictionary and canonical naming

- Purpose: ApprovedAction, SafetyGatePass, ExecutionRequest, ExternalControlRequest 용어 고정
- Files likely affected: glossary/index/core specs
- Risk level: Medium
- Test / verification plan: terminology grep
- Rollback plan: glossary revert
- Review notes: domain meaning 추가 금지

### PR 3: Flow consistency alignment

- Purpose: canonical lifecycle 순서 통일
- Files likely affected: lifecycle, layer 9, common DTO, action registry
- Risk level: High
- Test / verification plan: flow checklist
- Rollback plan: section-level revert
- Review notes: `Approval -> ApprovedAction -> Runtime Validation -> Safety Gate` 고정

### PR 4: Registry/Core Spec responsibility cleanup

- Purpose: core vs registry 중복 제거
- Files likely affected: `03_core_specifications/*`, `06_registry_specs/*`
- Risk level: Medium
- Test / verification plan: source-of-truth matrix
- Rollback plan: restore duplicated text
- Review notes: registry는 meaning source가 아니라 operational contract

### PR 5: Runtime Validation and Safety Gate boundary hardening

- Purpose: Safety Gate input/output DTO와 hot path 금지 강화
- Files likely affected: `08_runtime_validation/*`, common schema
- Risk level: High
- Test / verification plan: hot path forbidden operation checklist
- Rollback plan: runtime section revert
- Review notes: heavy operation 금지 유지

### PR 6: Domain Module no-guessing hardening

- Purpose: examples를 placeholder로 명확화
- Files likely affected: domain modules, action/state/policy examples
- Risk level: Medium
- Test / verification plan: domain value checklist
- Rollback plan: examples wording revert
- Review notes: domain rule 창작 금지

### PR 7: Implementation practicality checklist

- Purpose: DTO/validator/test readiness checklist 보강
- Files likely affected: `07_implementation_plan/*`
- Risk level: Low
- Test / verification plan: phase acceptance criteria review
- Rollback plan: checklist revert
- Review notes: architecture 재정의 금지

### PR 8: Test coverage plan

- Purpose: safety-critical flow tests 문서화
- Files likely affected: implementation plan, test strategy docs
- Risk level: Low
- Test / verification plan: listed tests map to docs
- Rollback plan: test plan revert
- Review notes: 실제 test code는 별도 구현 단계

### PR 9: Documentation index cleanup

- Purpose: root README 부재, index, encoding, numbering 같은 낮은 위험 정리
- Files likely affected: README/index docs
- Risk level: Low
- Test / verification plan: markdown link check
- Rollback plan: cleanup revert
- Review notes: owner의 tree 구조 의도 보존

### PR 10: Final architecture consistency review

- Purpose: PR 1-9 후 전체 재검토
- Files likely affected: all architecture docs
- Risk level: Low
- Test / verification plan: checklist 12문항 재실행
- Rollback plan: no content change unless separately approved
- Review notes: read-only review 가능

## 18. Final Approval Checklist

1. Architecture가 내부적으로 일관적인가?
   - 대체로 그렇다. 단, `ApprovedAction/Safety Gate` 순서 충돌은 P1.
2. Layer responsibility가 명확히 분리되어 있는가?
   - 대부분 명확하다. Layer 9/10 표현은 정리 필요.
3. Runtime flow가 문서 전체에서 일관적인가?
   - master/layer/runtime/implementation plan은 일관적이나 core lifecycle 일부가 다르다.
4. Ontology, Policy, Evidence, Approval, Safety Gate, Execution boundary가 보존되어 있는가?
   - 원칙은 보존되어 있다. 일부 용어와 flow가 구현 위험을 만든다.
5. Safety Gate hot path가 heavy operation에서 자유로운가?
   - runtime 문서 기준으로는 그렇다.
6. External standards는 copied가 아니라 mapped인가?
   - 그렇다.
7. AI output은 candidate interpretation으로만 취급되는가?
   - 원칙은 그렇다. `EvidenceBundle`, `AI_*_EVIDENCE` 용어는 보강 필요.
8. Evidence와 Audit path가 완전한가?
   - 일반 flow는 강하다. emergency/common DTO flow에서 trace refs 보강 필요.
9. Folder structure가 architecture와 정렬되어 있는가?
   - 대체로 정렬되어 있다. root README 부재와 source-of-truth 참조 불일치가 있다.
10. Implementation guide는 실행 가능한 수준인가?
    - implementation plan은 강하다. DTO/validator/test contract 보강이 필요하다.
11. Critical flow에 대한 test 제안이 충분한가?
    - 문서상 checklist는 강하지만 실제 test name/input/expected mapping을 더 명시해야 한다.
12. 이 repository는 다음 implementation stage로 넘어갈 수 있는가?
    - 제한적으로 가능하다. 단, P1 이슈를 먼저 정리한 후 code generation에 들어가는 것이 안전하다.

최종 상태:

**PASS WITH WARNINGS**

아키텍처 방향은 LEDO 원칙과 대체로 정렬되어 있다. 다만 `ApprovedAction -> Runtime Validation -> Safety Gate -> ExecutionRequest` 경계와 source-of-truth 참조를 정리하지 않으면, 구현 단계에서 Approval/Safety Gate/Execution Boundary가 붕괴될 위험이 있다.
