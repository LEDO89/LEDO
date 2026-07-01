# STRUCTURE FEEDBACK

## 1. Executive Summary

현재 구조는 전체적으로 번호 기반 아키텍처 문서 체계가 있으나, 일부 파일명에 오타와 중복 확장자가 남아 있다.
전각 슬래시, 스마트 따옴표, 전각 따옴표, 파일명 앞 공백이 포함된 경로는 GitHub와 CLI 작업에서 혼동을 만들 수 있다.
`README.md`와 `readme.md`가 혼재되어 대소문자 민감 환경에서 문제가 될 수 있다.
`src/`, `tests/`, `templates/`는 삭제나 이동보다 저장소 목적 확정 후 별도 판단이 필요하다.
이번 단계에서는 rename 실행 없이, 사용자 승인 대상만 분리해 의사결정할 수 있게 정리한다.

## 2. Must Fix Before GitHub

| 현재 경로 | 문제 | 제안 이름 | 이유 |
|---|---|---|---|
| `00_master_architecture/00_frist_construction.md` | 명백한 오타 | `00_first_construction.md` | `frist`는 `first` 오타로 보임 |
| `10_archive/Generative strucrure.md` | 명백한 오타 | `generative_structure.md` | `strucrure`는 `structure` 오타로 보임 |
| `02_layer_stack_mapping/1. Expeience ／ Presentation Stack mapping.md` | 명백한 오타 및 전각 슬래시 | `01_experience_presentation_stack_mapping.md` | `Expeience` 오타와 전각 문자가 함께 있음 |
| `03_core_specifications/03_action_type_registry/3_action_type_registory.md` | 명백한 오타 | `03_action_type_registry.md` | `registory`는 `registry` 오타로 보임 |
| `03_core_specifications/07_decision_approval_matrix/7_decision_approveal_matrix.md` | 명백한 오타 | `07_decision_approval_matrix.md` | `approveal`은 `approval` 오타로 보임 |
| `03_core_specifications/08_policy_governance_model/8_policy_government_model.md` | 명칭 불일치 | `08_policy_governance_model.md` | 폴더의 `governance`와 파일의 `government`가 불일치함 |
| `AGENTS.md.md` | 중복 확장자 | `AGENTS.md` | `.md` 확장자가 중복됨 |
| `00_master_architecture/readme.md.md` | 중복 확장자 및 README 대소문자 문제 | `README.md` | `.md` 중복과 `readme` 소문자 문제가 동시에 있음 |
| `08_runtime_validation/readme.md` | README 대소문자 문제 | `README.md` | README는 대문자 `README.md`로 통일하는 것이 안전함 |
| `00_master_architecture/ 01_master_architecture.md` | 파일명 앞 공백 | `01_master_architecture.md` | 선행 공백은 CLI, 링크, 정렬에서 오류를 만들기 쉬움 |
| `01_layer_architecture／` | 전각 슬래시 | `01_layer_architecture` | 폴더명 끝 전각 슬래시가 경로 구분자처럼 보여 혼동됨 |
| `04_ontology_foundation/01_semantic_web_technology_stack／.md` | 전각 슬래시 | `01_semantic_web_technology_stack.md` | 파일명이 실제 주제명보다 `／.md` 형태로 보임 |
| `04_ontology_foundation/02_upper_ontology_and_standards／.md` | 전각 슬래시 | `02_upper_ontology_and_standards.md` | 파일명이 실제 주제명보다 `／.md` 형태로 보임 |
| `04_ontology_foundation/03_owl_modeling_principles／.md` | 전각 슬래시 | `03_owl_modeling_principles.md` | 파일명이 실제 주제명보다 `／.md` 형태로 보임 |
| `04_ontology_foundation/04_reasoning_and_constraint_model／.md` | 전각 슬래시 | `04_reasoning_and_constraint_model.md` | 파일명이 실제 주제명보다 `／.md` 형태로 보임 |
| `04_ontology_foundation/06_ontology_governance_and_versioning／.md` | 전각 슬래시 | `06_ontology_governance_and_versioning.md` | 파일명이 실제 주제명보다 `／.md` 형태로 보임 |

## 3. Recommended Rename Plan

| 현재 경로 | 변경 후 경로 | 변경 이유 | 우선순위 |
|---|---|---|---|
| `AGENTS.md.md` | `AGENTS.md` | 중복 확장자 제거 | 높음 |
| `00_master_architecture/readme.md.md` | `00_master_architecture/README.md` | 중복 확장자 제거 및 README 규칙 통일 | 높음 |
| `08_runtime_validation/readme.md` | `08_runtime_validation/README.md` | README 대소문자 통일 | 높음 |
| `00_master_architecture/00_frist_construction.md` | `00_master_architecture/00_first_construction.md` | 오타 수정 | 높음 |
| `00_master_architecture/ 01_master_architecture.md` | `00_master_architecture/01_master_architecture.md` | 파일명 앞 공백 제거 | 높음 |
| `01_layer_architecture／` | `01_layer_architecture` | 전각 슬래시 제거 | 높음 |
| `02_layer_stack_mapping/0. “Observability ／ Audit ／ Trace” Stack Mapping .md` | `02_layer_stack_mapping/00_observability_audit_trace_stack_mapping.md` | 번호 형식, 공백, 스마트 따옴표, 전각 슬래시 정리 | 중간 |
| `02_layer_stack_mapping/1. Expeience ／ Presentation Stack mapping.md` | `02_layer_stack_mapping/01_experience_presentation_stack_mapping.md` | 오타 수정 및 파일명 규칙 통일 | 높음 |
| `02_layer_stack_mapping/2.  “API Gateway” Stack Mapping.md` | `02_layer_stack_mapping/02_api_gateway_stack_mapping.md` | 중복 공백과 스마트 따옴표 제거 | 중간 |
| `02_layer_stack_mapping/3. “Governance ／ Policy ／ Security” Stack Mapping.md` | `02_layer_stack_mapping/03_governance_policy_security_stack_mapping.md` | 전각 슬래시와 스마트 따옴표 제거 | 중간 |
| `02_layer_stack_mapping/4. “Core Ontology Kernel” Stack Mapping.md` | `02_layer_stack_mapping/04_core_ontology_kernel_stack_mapping.md` | 파일명 규칙 통일 | 중간 |
| `02_layer_stack_mapping/5. “Knowledge & Semantic Memory” Stack Mapping.md` | `02_layer_stack_mapping/05_knowledge_semantic_memory_stack_mapping.md` | 특수문자 제거 및 파일명 규칙 통일 | 중간 |
| `02_layer_stack_mapping/6.  “Real-Time World State” Stack Mapping.md` | `02_layer_stack_mapping/06_real_time_world_state_stack_mapping.md` | 중복 공백, 하이픈, 스마트 따옴표 정리 | 중간 |
| `02_layer_stack_mapping/7. “Distributed Domain Agent” Stack Mapping.md` | `02_layer_stack_mapping/07_distributed_domain_agent_stack_mapping.md` | 파일명 규칙 통일 | 중간 |
| `02_layer_stack_mapping/8. “Decision Router ／ Escalation” Stack Mapping.md` | `02_layer_stack_mapping/08_decision_router_escalation_stack_mapping.md` | 전각 슬래시와 스마트 따옴표 제거 | 중간 |
| `02_layer_stack_mapping/9. ＂Approved Action ／ Safety Gate” Stack Mapping.md` | `02_layer_stack_mapping/09_approved_action_safety_gate_stack_mapping.md` | 전각 따옴표, 전각 슬래시, 스마트 따옴표 제거 | 중간 |
| `02_layer_stack_mapping/10. “Unified Cyber-Physical Core” Stack Mapping.md` | `02_layer_stack_mapping/10_unified_cyber_physical_core_stack_mapping.md` | 하이픈과 스마트 따옴표 정리 | 중간 |
| `02_layer_stack_mapping/11. “Execution Request & External Control Integration” Stack Mapping.md` | `02_layer_stack_mapping/11_execution_request_external_control_integration_stack_mapping.md` | 특수문자 제거 및 파일명 규칙 통일 | 중간 |
| `02_layer_stack_mapping/12. “Physical World” Stack Mapping.md` | `02_layer_stack_mapping/12_physical_world_stack_mapping.md` | 파일명 규칙 통일 | 중간 |
| `03_core_specifications/00_canonical_object_lifecycle/0_canonical_object_lifecycle.md` | `03_core_specifications/00_canonical_object_lifecycle/00_canonical_object_lifecycle.md` | 번호를 2자리로 통일 | 중간 |
| `03_core_specifications/01_common_schema_dto/1_common_schema_dto.md` | `03_core_specifications/01_common_schema_dto/01_common_schema_dto.md` | 번호를 2자리로 통일 | 중간 |
| `03_core_specifications/02_event_type_taxonomy/2_event_type_taxonomy.md` | `03_core_specifications/02_event_type_taxonomy/02_event_type_taxonomy.md` | 번호를 2자리로 통일 | 중간 |
| `03_core_specifications/03_action_type_registry/3_action_type_registory.md` | `03_core_specifications/03_action_type_registry/03_action_type_registry.md` | 오타 수정 및 번호를 2자리로 통일 | 높음 |
| `03_core_specifications/04_state_model_registry/4_state_model_registry.md` | `03_core_specifications/04_state_model_registry/04_state_model_registry.md` | 번호를 2자리로 통일 | 중간 |
| `03_core_specifications/05_evidence_model/5_evidence_model.md` | `03_core_specifications/05_evidence_model/05_evidence_model.md` | 번호를 2자리로 통일 | 중간 |
| `03_core_specifications/06_ontology_module_boundary/6_ontology_module_boundary.md` | `03_core_specifications/06_ontology_module_boundary/06_ontology_module_boundary.md` | 번호를 2자리로 통일 | 중간 |
| `03_core_specifications/07_decision_approval_matrix/7_decision_approveal_matrix.md` | `03_core_specifications/07_decision_approval_matrix/07_decision_approval_matrix.md` | 오타 수정 및 번호를 2자리로 통일 | 높음 |
| `03_core_specifications/08_policy_governance_model/8_policy_government_model.md` | `03_core_specifications/08_policy_governance_model/08_policy_governance_model.md` | 명칭 불일치 수정 및 번호를 2자리로 통일 | 높음 |
| `03_core_specifications/09_execution_adapter_model/9_execution_adapter_model.md` | `03_core_specifications/09_execution_adapter_model/09_execution_adapter_model.md` | 번호를 2자리로 통일 | 중간 |
| `04_ontology_foundation/01_semantic_web_technology_stack／.md` | `04_ontology_foundation/01_semantic_web_technology_stack.md` | 전각 슬래시 제거 | 높음 |
| `04_ontology_foundation/02_upper_ontology_and_standards／.md` | `04_ontology_foundation/02_upper_ontology_and_standards.md` | 전각 슬래시 제거 | 높음 |
| `04_ontology_foundation/03_owl_modeling_principles／.md` | `04_ontology_foundation/03_owl_modeling_principles.md` | 전각 슬래시 제거 | 높음 |
| `04_ontology_foundation/04_reasoning_and_constraint_model／.md` | `04_ontology_foundation/04_reasoning_and_constraint_model.md` | 전각 슬래시 제거 | 높음 |
| `04_ontology_foundation/06_ontology_governance_and_versioning／.md` | `04_ontology_foundation/06_ontology_governance_and_versioning.md` | 전각 슬래시 제거 | 높음 |
| `06_registry_specs/identity_registry/Identity_registry.md` | `06_registry_specs/identity_registry/identity_registry.md` | 대소문자 통일 | 중간 |
| `08_runtime_validation/idempotency/Idempotency Control.md` | `08_runtime_validation/idempotency/idempotency_control.md` | 제목형 파일명을 snake_case로 통일 | 중간 |
| `08_runtime_validation/network_health/Network Health.md` | `08_runtime_validation/network_health/network_health.md` | 제목형 파일명을 snake_case로 통일 | 중간 |
| `08_runtime_validation/safety_gate/Safety Gate.md` | `08_runtime_validation/safety_gate/safety_gate.md` | 제목형 파일명을 snake_case로 통일 | 중간 |
| `08_runtime_validation/shacl_shapes/SHACL Shapes.md` | `08_runtime_validation/shacl_shapes/shacl_shapes.md` | 제목형 파일명을 snake_case로 통일 | 중간 |
| `08_runtime_validation/validators/Validators.md` | `08_runtime_validation/validators/validators.md` | 대소문자 통일 | 중간 |
| `10_archive/Generative strucrure.md` | `10_archive/generative_structure.md` | 오타 수정 및 snake_case 적용 | 높음 |

## 4. Defer / Do Not Fix Now

| 항목 | 지금 수정하지 않는 이유 |
|---|---|
| `src/` | 문서 저장소에 포함된 구현 스캐폴드일 수 있으므로 저장소 목적 확정 전 이동하지 않는다. |
| `tests/` | `src/`와 함께 동작하는 검증 스캐폴드일 수 있으므로 현재 단계에서 이동하거나 삭제하지 않는다. |
| `templates/` | 문서 작성 템플릿으로 유효할 수 있으므로 부록 이동 여부는 나중에 결정한다. |
| `.gitkeep` | 빈 디렉터리를 Git에 유지하기 위한 파일이므로 삭제하지 않는다. |
| `pyproject.toml` | Python 패키지 설정 파일이므로 `src/`, `tests/` 처리 결정 전 수정하지 않는다. |
| `README.md` | 루트 진입 문서이므로 삭제하거나 이름을 바꾸지 않는다. |
| `제목 없는 스프레드시트.xlsx` | 용도 확인 전 삭제하거나 이동하지 않는다. |

## 5. Naming Rules To Apply

- 폴더명은 `snake_case`를 사용한다.
- 문서 파일명은 `snake_case.md`를 사용한다.
- 번호가 있는 문서는 2자리 번호를 사용한다: `00_`, `01_`, `02_`.
- README는 항상 `README.md`로 작성한다.
- 공백, 스마트 따옴표, 전각 슬래시, 전각 따옴표는 파일명과 폴더명에 사용하지 않는다.
- 제목형 파일명은 본문 제목으로만 사용하고 파일명에는 사용하지 않는다.

## 6. Final User Decision Checklist

- [ ] 오타 파일명 수정 승인
- [ ] 중복 확장자 제거 승인
- [ ] 전각 문자 제거 승인
- [ ] 파일명 앞 공백 제거 승인
- [ ] `README.md` 통일 승인
- [ ] `02_layer_stack_mapping` 문서명 snake_case 통일 승인
- [ ] `03_core_specifications` 문서 번호 2자리 통일 승인
- [ ] `08_runtime_validation` 문서명 snake_case 통일 승인
- [ ] `src/`, `tests/`, `templates/`는 현재 유지
- [ ] 스프레드시트 파일은 용도 확인 전 유지

## Applied Changes

- `git mv`로 명백한 오타 파일명을 수정했다.
- `git mv`로 중복 `.md` 확장자를 제거했다.
- `git mv`로 전각 슬래시가 포함된 폴더명과 파일명을 정리했다.
- `git mv`로 파일명 앞 선행 공백을 제거했다.
- `git mv`로 `README.md` 대소문자를 통일했다.
- `git mv`로 `02_layer_stack_mapping` 문서명을 `00_`부터 `12_`까지 `snake_case.md` 규칙으로 정리했다.
- `git mv`로 `08_runtime_validation` 하위 주요 문서명을 `snake_case.md`로 통일했다.
- 루트 `PROJECT_TREE.md`를 현재 실제 구조 기준으로 다시 생성했다.
- `src/`, `tests/`, `templates/`, `.gitkeep`, `pyproject.toml`, `.gitignore`, 루트 `README.md`, `제목 없는 스프레드시트.xlsx`는 수정하지 않았다.
