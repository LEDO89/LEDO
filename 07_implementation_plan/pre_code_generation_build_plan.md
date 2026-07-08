---
title: LEDO Ontology Core Step-by-Step Code Generation Build Plan
version: 2.0
status: draft_for_review
owner: platform-ontology
language: ko
last_updated: 2026-07-06
---

# LEDO Ontology Core 코드 생성 단계별 구축 계획서

## 1. 목적

이 문서는 `LEDO_ONTOLOGY_CORE`의 Markdown 사양을 코드로 생성하기 전, 각 단계에서 다음 네 가지를 즉시 확인할 수 있도록 만든 실행 계획서이다.

- 어떤 Markdown 문서를 source of truth로 읽는가
- 어떤 Python 코드와 테스트를 생성하는가
- 그 단계의 전체 방향성이 무엇인가
- 무엇을 만들면 안 되는가

이 문서는 새 아키텍처가 아니다.
이 문서는 기존 Markdown 사양을 코드 생성 순서로 정렬한 작업 지시서이다.

## 2. 절대 실행 규칙

모든 코드 생성 step은 아래 순서를 반복한다.

1. `AGENTS.md`를 읽는다.
2. `00_master_architecture/00_first_construction.md`를 읽는다.
3. `00_master_architecture/01_master_architecture.md`를 읽는다.
4. 해당 step의 `Primary source markdown` 하나를 읽는다.
5. 필요한 경우에만 `Supporting source markdown`을 읽는다.
6. 해당 step에 적힌 코드와 테스트만 생성한다.
7. domain meaning이 비어 있으면 `DOMAIN_DECISION_REQUIRED` 또는 `status: draft`, `NotImplementedError`, skipped/xfail test로 남긴다.
8. affected pytest scope를 실행한다.

Core rule:

하나의 Markdown 사양 파일은 하나의 bounded implementation step이 된다.

## 3. 공통 금지 경계

어떤 step에서도 아래 항목은 만들지 않는다.

- 실제 robot, PLC, SCADA, access-control 제어
- 실제 emergency stop 명령
- 실제 physical command
- LLM 출력에서 직접 `Evidence`, `ApprovedAction`, `ExecutionRequest`, `ExternalControlRequest` 생성
- 도메인별 안전 임계값, 승인 권한, 법규, 현장 규칙 추정
- Safety Gate hot path 안의 OWL reasoning, full SHACL validation, SPARQL, Graph DB call, LLM call, external API call, disk I/O
- `agent_vocabulary_registry` 또는 `model_adapter_registry` 구현

## 4. 모호함 처리 표준

불명확한 domain rule, enum value, threshold, domain class, approval role, external behavior는 추정하지 않는다.

허용되는 표식과 구현 형태:

- `# DOMAIN_DECISION_REQUIRED: <missing decision> — see <source markdown/section>`
- registry content gap: `status: draft`
- executable behavior gap: `NotImplementedError` with docstring
- pytest skip: `@pytest.mark.skip(reason="domain expert input required: <specific missing input> — see <source document/section>")`
- pytest xfail: `@pytest.mark.xfail(reason="<specific missing input or unresolved boundary> — see <source document/section>", strict=True)`

## 5. 코드 배치 기준

Framework code:

- `src/ledo_ontology_core/framework/schemas/`
- `src/ledo_ontology_core/framework/registries/`
- `src/ledo_ontology_core/framework/validation/`
- `src/ledo_ontology_core/framework/runtime/`
- `src/ledo_ontology_core/framework/policy/`
- `src/ledo_ontology_core/framework/decision/`
- `src/ledo_ontology_core/framework/audit/`
- `src/ledo_ontology_core/framework/adapters/`
- `src/ledo_ontology_core/framework/ontology/`
- `src/ledo_ontology_core/framework/graph/`

Domain pack placeholders and fixtures:

- `src/ledo_ontology_core/domain_packs/`
- `tests/fixtures/`

Tests:

- `tests/unit/framework/`
- `tests/unit/domain_packs/`
- `tests/integration/registry_loading/`
- `tests/integration/decision_flow/`
- `tests/integration/safety_gate_flow/`
- `tests/integration/graph_export/`

Do not place shared framework modules directly under `src/ledo_ontology_core/`.

## 6. Step-by-Step Build Matrix

### Step 0. Architecture Index Verification

전체 방향성:

코드 생성 전에 구현 대상 문서와 제외 대상을 고정한다. 이 step은 코드를 만들지 않는다.

Primary source markdown:

- `AGENTS.md`

Supporting source markdown:

- `00_master_architecture/00_first_construction.md`
- `00_master_architecture/01_master_architecture.md`
- `03_core_specifications/README.md`
- `06_registry_specs/README.md`
- `07_implementation_plan/implementation_plan.md`
- `07_implementation_plan/implementation_slice_1/implementation_slice_1_plan.md`
- `07_implementation_plan/implementation_slice_2/implementation_slice_2_plan.md`
- `07_implementation_plan/implementation_slice_3/implementation_slice_3_plan.md`

Generate code:

- None

Generate tests:

- None

Verification output:

- Confirm implementation starts at Step 1.
- Confirm `agent_vocabulary_registry` and `model_adapter_registry` remain deferred.
- Confirm source-of-truth priority is understood.

Stop condition:

- Any conflict involving safety, execution, evidence, approval, policy, identity, or physical control is unresolved.

### Step 1. Common Schema and Full DTO Contracts

전체 방향성:

모든 downstream registry, validator, runtime object가 의존할 DTO 계약을 만든다. `01_common_schema_dto`는 base/context DTO만이 아니라 lifecycle DTO 필드, recommended file structure, full DTO catalog까지 정의하므로 DTO 필드의 primary source of truth는 이 문서이다. DTO는 계약이며 실행 책임을 갖지 않는다.

**Full-surface build policy**: DTO는 순수 구조(pure structure)이고 "DTO는 실행하지 않는다"(§3.1)는 원칙에 따라, `01_common_schema_dto.md`에 정의된 DTO 전체(Emergency/Monitoring/Runtime Validation/Safety Gate 계약 포함)를 이 Step에서 한 번에 구축한다. Registry/step별로 나눠서 짓지 않는다 — 이는 스키마 레이어를 가장 먼저 안정화시켜 이후 스텝들이 반복적으로 스키마 파일을 재작업하지 않도록 하기 위함이다. 단, **구조(structure)를 미리 만드는 것과 그 구조에 실제 값을 채우는 것(governed content)은 분리된다**: Emergency Action Registry에 실제 `emergency_action_type`을 등록하는 일, 실제 정책 판단을 내리는 일, 실제 어댑터를 배선하는 일은 여전히 각자의 governing step(및 `0_canonical_object_lifecycle.md` §5의 Safety Committee/Ontology Steward 승인 절차)까지 보류된다. 이 Step은 그 구조를 담을 그릇만 만든다.

Primary source markdown:

- `03_core_specifications/01_common_schema_dto/1_common_schema_dto.md`

Supporting source markdown:

- `03_core_specifications/00_canonical_object_lifecycle/0_canonical_object_lifecycle.md` — lifecycle ordering/boundary context, and §4.8 as the source for the `DecisionTier` enum
- `03_core_specifications/09_execution_adapter_model/9_execution_adapter_model.md` §20 "Dispatch Lifecycle" — the sole canonical source for the `DispatchStatus` enum used by `ExecutionStateDTO.state`. Do not derive this enum from `01_common_schema_dto.md` §18.3's shorter illustrative list.

Generate code:

- `src/ledo_ontology_core/framework/schemas/enums.py` (shared enum types — see Required objects)
- `src/ledo_ontology_core/framework/schemas/base.py`
- `src/ledo_ontology_core/framework/schemas/context.py`
- `src/ledo_ontology_core/framework/schemas/validation.py`
- `src/ledo_ontology_core/framework/schemas/refs.py`
- `src/ledo_ontology_core/framework/schemas/payloads.py`
- `src/ledo_ontology_core/framework/schemas/event.py`
- `src/ledo_ontology_core/framework/schemas/ontology.py`
- `src/ledo_ontology_core/framework/schemas/evidence.py`
- `src/ledo_ontology_core/framework/schemas/world_state.py` (incl. `StateSnapshotDTO`)
- `src/ledo_ontology_core/framework/schemas/action.py` (incl. `IntentDTO`)
- `src/ledo_ontology_core/framework/schemas/decision.py`
- `src/ledo_ontology_core/framework/schemas/approval.py`
- `src/ledo_ontology_core/framework/schemas/execution.py` (incl. `TimeoutPolicyDTO`, `RetryPolicyDTO`, `RecoveryPolicyDTO`, `IdempotencyContextDTO`)
- `src/ledo_ontology_core/framework/schemas/feedback.py` (incl. `WorldStateReconciliationDTO`, `ExecutionStateDTO`)
- `src/ledo_ontology_core/framework/schemas/audit.py`
- `src/ledo_ontology_core/framework/schemas/registry.py`
- `src/ledo_ontology_core/framework/schemas/governance.py`
- `src/ledo_ontology_core/framework/schemas/observability.py`
- `src/ledo_ontology_core/framework/schemas/source_inputs.py` (all 8 §20 source-specific DTOs)
- `src/ledo_ontology_core/framework/schemas/emergency.py` (`EmergencyActionSpecDTO`, `EmergencyApprovedActionDTO`, `PostHocAuditDTO`)
- `src/ledo_ontology_core/framework/schemas/high_frequency.py` (`TimeSeriesSampleDTO`, `TimeSeriesBundleInputDTO`, `WindowedInputDTO`, `MonitoringPayloadDTO`, `MonitoringOnlyEventDTO`, `EscalationTriggerDTO`)
- `src/ledo_ontology_core/framework/schemas/runtime_validation.py` (§17.3A validator result DTOs)
- `src/ledo_ontology_core/framework/schemas/safety_gate.py` (§17.3A `SafetySnapshotDTO`/`SafetyGateInputDTO`/`SafetyGatePassDTO`/`SafetyGateBlockDTO`)
- update `src/ledo_ontology_core/framework/schemas/__init__.py`

Required objects:

Core (originally-scoped) DTOs — `BaseDTO`, `TraceContextDTO`, `VersionContextDTO`, `SourceMetadataDTO`, `FreshnessDTO`, `ConfidenceDTO`, `GenericPayloadDTO`, `ValidationResultDTO`, `SanitizedInputDTO`, `RateLimitContextDTO`, `EntityRefDTO`, `LocationRefDTO`, `OntologyRefDTO`, `EvidenceRefDTO`, `PolicyRefDTO`, `ActorRefDTO`, `CanonicalEventEnvelopeDTO`, `PathClassificationDTO`, `CanonicalIdentityDTO`, `OntologyBindingDTO`, `OntologyBoundEventDTO`, `EvidenceDTO`, `WorldStateDTO`, `WorldStateUpdateDTO`, `ActionCandidateDTO`, `DecisionCaseDTO`, `ApprovalRequestDTO`, `ApprovedActionDTO`, `ExecutionRequestDTO`, `ExternalControlRequestDTO`, `FeedbackEventDTO`, `AuditRecordDTO`.

Shared enums (`schemas/enums.py`) — `ValidationStatus`, `PathType`, `BindingStatus`, `PolicyDecisionResult`, `DecisionTier`, `PostAuditStatus`, `ReviewStatus`, `AggregationType`, `DispatchStatus`.

Remaining full-catalog DTOs (built now under the full-surface build policy above) — `RawInputDTO`, `EventTypeDTO`, `IntentDTO`, `EvidenceBundleDTO`, `StateSnapshotDTO`, `ApprovalDecisionDTO`, `PolicyDecisionDTO`, `TimeoutPolicyDTO`, `RetryPolicyDTO`, `RecoveryPolicyDTO`, `IdempotencyContextDTO`, `WorldStateReconciliationDTO`, `ExecutionStateDTO`, `ActionTypeSpecDTO`, `EmergencyActionSpecDTO`, `EmergencyApprovedActionDTO`, `PostHocAuditDTO`, `EventTypeSpecDTO`, `StateTypeSpecDTO`, `CapabilitySpecDTO`, `AdapterSpecDTO`, `MappingReviewDTO`, `LifecycleMetricDTO`, `TimeSeriesSampleDTO`, `TimeSeriesBundleInputDTO`, `WindowedInputDTO`, `MonitoringPayloadDTO`, `MonitoringOnlyEventDTO`, `EscalationTriggerDTO`, `RuntimeValidationInputDTO`, `RuntimeValidationResultDTO`, `ValidatorResultDTO`, `TOCTOUResultDTO`, `SHACLValidationResultDTO`, `NetworkHealthResultDTO`, `IdempotencyResultDTO`, `ApprovalValidityResultDTO`, `PolicyRevalidationResultDTO`, `EvidenceValidityResultDTO`, `SafetySnapshotDTO`, `SafetyGateInputDTO`, `SafetyGatePassDTO`, `SafetyGateBlockDTO`, `IndustrialRawInputDTO`, `IndustrialTimeSeriesInputDTO`, `RobotTelemetryInputDTO`, `RobotTelemetryBundleInputDTO`, `ConstructionProcessInputDTO`, `LLMOutputInputDTO`, `MobileContextInputDTO`, `DocumentParseInputDTO`.

Generate tests:

- `tests/unit/framework/test_common_schema_dto.py`
- `tests/unit/framework/test_initial_dto_contracts.py`
- `tests/unit/framework/test_enums.py`
- `tests/unit/framework/test_emergency_dto.py`
- `tests/unit/framework/test_high_frequency_dto.py`
- `tests/unit/framework/test_runtime_validation_dto.py`
- `tests/unit/framework/test_safety_gate_dto.py`
- `tests/unit/framework/test_registry_governance_observability_dto.py`
- `tests/unit/framework/test_execution_policy_and_source_input_dto.py`

Test requirements:

- valid DTO construction
- required field failures
- invalid timestamp/version/source failures
- trace/correlation/causation id edge cases
- initial required DTOs from `01_common_schema_dto` Section 23 exist
- `ExecutionRequestDTO` requires a Safety Gate reference path per the DTO contract
- AI output input DTO cannot satisfy evidence by itself
- every enum field rejects a value outside its enum (e.g. `PathClassificationDTO(path_type=...)`, `ConfidenceDTO(validation_status=...)`)
- `DispatchStatus` has exactly the 20 canonical members from `09_execution_adapter_model.md` §20, and a value from `01_common_schema_dto.md` §18.3's shorter illustrative list that isn't in the canonical 20 (e.g. `"BLOCKED"`) is rejected

Do not create:

- lifecycle services
- registry loaders
- runtime validation logic (behavior — validator interfaces/aggregation functions are Step 17+, not this step; the *result DTOs* they consume are built here)
- domain-specific subclasses
- real registry content, real emergency action registrations, or any other instance/value data — DTO structures only

Completion command:

- `pytest tests/unit/framework/`

### Step 2. Canonical Lifecycle Flow and Boundary Rules

전체 방향성:

LEDO canonical flow의 순서, 상태 전이, 금지 경계, AI/Evidence/Approval/Execution 분리를 코드 검증 규칙으로 만든다. DTO 필드 자체는 Step 1에서 `01_common_schema_dto`를 기준으로 생성되었으므로, 이 step은 lifecycle orchestration service가 아니라 lifecycle boundary validator와 tests를 만든다.

Primary source markdown:

- `03_core_specifications/00_canonical_object_lifecycle/0_canonical_object_lifecycle.md`

Supporting source markdown:

- `03_core_specifications/01_common_schema_dto/1_common_schema_dto.md`

Generate code:

- `src/ledo_ontology_core/framework/validation/lifecycle.py`
- `src/ledo_ontology_core/framework/schemas/lifecycle_state.py`
- update `src/ledo_ontology_core/framework/validation/__init__.py`

Required objects:

- lifecycle path enum or equivalent fixed vocabulary for Standard, Emergency, and Monitoring-only paths as defined by the source markdown
- canonical lifecycle stage enum
- lifecycle transition validator
- AI boundary validator
- evidence boundary validator
- approval/execution boundary validator
- audit trace path validator

Generate tests:

- `tests/unit/framework/test_canonical_lifecycle_boundaries.py`

Test requirements:

- standard path DTO chain can carry trace ids
- `ActionCandidate` cannot be treated as approval
- `ApprovedAction` cannot be treated as physical command
- `ExecutionRequest` cannot be treated as physical command
- AI-origin field cannot satisfy evidence requirement by itself
- no `ExecutionRequest` without Runtime Validation and SafetyGatePass
- compressed `ApprovedAction -> ExecutionRequest` path fails

Do not create:

- execution dispatch
- approval service
- Safety Gate service
- physical command class
- new DTO field definitions that conflict with `01_common_schema_dto`

Completion command:

- `pytest tests/unit/framework/test_canonical_lifecycle_boundaries.py`

### Step 3. Ontology Module Boundary Scaffolding

전체 방향성:

Ontology module boundaries, namespace rules, and dependency direction을 코드로 표현한다. 의미 자체를 새로 만들지 않는다.

Primary source markdown:

- `03_core_specifications/06_ontology_module_boundary/6_ontology_module_boundary.md`

Supporting source markdown:

- `04_ontology_foundation/00_ontology_foundation_report.md`
- `04_ontology_foundation/01_semantic_web_technology_stack.md`
- `04_ontology_foundation/03_owl_modeling_principles.md`
- `04_ontology_foundation/05_relationship_and_property_design.md`

Generate code:

- `src/ledo_ontology_core/framework/ontology/namespaces.py`
- `src/ledo_ontology_core/framework/ontology/modules.py`
- `src/ledo_ontology_core/framework/ontology/iri.py`
- `src/ledo_ontology_core/framework/ontology/boundary.py`
- create/update `src/ledo_ontology_core/framework/ontology/__init__.py`

Required objects:

- namespace constants
- `OntologyModuleRef`
- `OntologyModuleBoundary`
- `build_versioned_iri`
- `validate_module_dependency_direction`

Generate tests:

- `tests/unit/framework/test_ontology_boundary.py`

Test requirements:

- valid namespace and IRI construction
- invalid dependency direction fails
- domain module cannot import peer domain module without governed mediation
- no domain class/property meaning is created by framework code

Do not create:

- real construction/industrial/robot classes
- OWL reasoning runtime
- graph database integration

Completion command:

- `pytest tests/unit/framework/test_ontology_boundary.py`

### Step 4. Registry Base System

전체 방향성:

모든 registry가 공유할 entry base, status, loader, cross-reference resolver를 만든다.

Primary source markdown:

- `06_registry_specs/README.md`

Supporting source markdown:

- `03_core_specifications/01_common_schema_dto/1_common_schema_dto.md`

Generate code:

- `src/ledo_ontology_core/framework/registries/base.py`
- `src/ledo_ontology_core/framework/registries/status.py`
- `src/ledo_ontology_core/framework/registries/loader.py`
- `src/ledo_ontology_core/framework/registries/resolver.py`
- `src/ledo_ontology_core/framework/validation/registry.py`
- update `src/ledo_ontology_core/framework/registries/__init__.py`

Required objects:

- `RegistryStatus`
- `RegistryEntryBase`
- `RegistryLoadResult`
- `RegistryLoader`
- `InMemoryRegistry`
- `RegistryReference`
- `RegistryReferenceResolver`
- boundary prefix validator for `must_not_`, `does_not_`, `may_`, `requires_`, `cannot_`

Generate tests:

- `tests/unit/framework/test_registry_base.py`
- `tests/integration/registry_loading/test_registry_base_loading.py`

Test requirements:

- load valid draft/active/deprecated/retired/blocked entries
- duplicate id fails
- malformed `prefix:id` fails
- reference to retired/blocked target fails when runtime path requires active
- draft entry is not available for active runtime use

Do not create:

- concrete action/event/state/evidence registry models
- domain-specific registry values

Completion command:

- `pytest tests/unit/framework/test_registry_base.py tests/integration/registry_loading/test_registry_base_loading.py`

### Step 5. Action Registry

전체 방향성:

Action type vocabulary contract를 구현한다. Action type은 physical command가 아니다.

Primary source markdown:

- `06_registry_specs/action_registry/action_registry.md`

Supporting source markdown:

- `03_core_specifications/03_action_type_registry/03_action_type_registry.md`
- `06_registry_specs/README.md`

Generate code:

- `src/ledo_ontology_core/framework/registries/action.py`
- `tests/fixtures/sample_domain_packs/action_registry.yaml`

Required objects:

- `ActionCategory`
- `ActionRegistryEntry`
- `ActionRegistry`
- action registry validator

Generate tests:

- `tests/unit/framework/test_action_registry.py`
- `tests/integration/registry_loading/test_action_registry_loading.py`

Test requirements:

- valid non-normative fixture loads as `draft`
- missing evidence/policy/approval/runtime validation references fail
- action entry cannot define physical command semantics
- active runtime lookup rejects draft fixture unless explicitly allowed for tests

Do not create:

- real `STOP_WORK` or `DISPATCH_ROBOT` as approved domain content
- robot/PLC/SCADA command mapping

Completion command:

- `pytest tests/unit/framework/test_action_registry.py tests/integration/registry_loading/test_action_registry_loading.py`

### Step 6. Identity Registry and Policy Access Skeleton

전체 방향성:

Identity, actor, role, clearance, permission 구조를 구현하되 실제 권한 부여는 만들지 않는다.

Primary source markdown:

- `06_registry_specs/identity_registry/Identity_registry.md`

Supporting source markdown:

- `03_core_specifications/08_policy_governance_model/08_policy_governance_model.md`
- `06_registry_specs/README.md`

Generate code:

- `src/ledo_ontology_core/framework/registries/identity.py`
- `src/ledo_ontology_core/framework/policy/access.py`
- `tests/fixtures/sample_domain_packs/identity_registry.yaml`

Required objects:

- `IdentityRegistryEntry`
- `IdentityRegistry`
- `RoleRef`
- `ClearanceRef`
- `PermissionRef`
- access skeleton DTOs only

Generate tests:

- `tests/unit/framework/test_identity_registry.py`
- `tests/unit/framework/test_policy_access_skeleton.py`

Test requirements:

- valid draft identity fixture loads
- missing actor identity fails for audit-relevant object
- no real role assignment exists
- no clearance rule is inferred

Do not create:

- real user roles
- real approval authority
- authentication service

Completion command:

- `pytest tests/unit/framework/test_identity_registry.py tests/unit/framework/test_policy_access_skeleton.py`

### Step 7. Ontology Registry

전체 방향성:

Ontology resource identifiers and versions를 registry로 관리한다. Registry는 의미를 정의하지 않고 의미 리소스를 참조한다.

Primary source markdown:

- `06_registry_specs/ontology_registry/ontology_registry.md`

Supporting source markdown:

- `04_ontology_foundation/06_ontology_governance_and_versioning.md`
- `06_registry_specs/README.md`

Generate code:

- `src/ledo_ontology_core/framework/registries/ontology.py`
- `tests/fixtures/sample_domain_packs/ontology_registry.yaml`

Required objects:

- `OntologyRegistryEntry`
- `OntologyRegistry`
- ontology version validator

Generate tests:

- `tests/unit/framework/test_ontology_registry.py`

Test requirements:

- valid ontology resource id/version loads
- invalid IRI/version fails
- registry entry does not define OWL class meaning directly

Do not create:

- OWL file generation
- SHACL shapes
- reasoning service

Completion command:

- `pytest tests/unit/framework/test_ontology_registry.py`

### Step 8. Event Registry

전체 방향성:

Event type vocabulary와 event validation contract를 구현한다. Event registry는 current state source of truth가 아니다.

Primary source markdown:

- `06_registry_specs/event_registry/event_registry.md`

Supporting source markdown:

- `03_core_specifications/02_event_type_taxonomy/2_event_type_taxonomy.md`
- `09_appendices/appendix_b_event_catalog/event_catalog.md`

Generate code:

- `src/ledo_ontology_core/framework/registries/event.py`
- `tests/fixtures/sample_events/event_registry.yaml`

Required objects:

- `EventRegistryEntry`
- `EventRegistry`
- event payload field validator
- event idempotency requirement validator

Generate tests:

- `tests/unit/framework/test_event_registry.py`
- `tests/integration/registry_loading/test_event_registry_loading.py`

Test requirements:

- valid non-normative event fixture loads
- missing required payload field fails
- missing idempotency requirement fails where required
- event examples remain non-normative

Do not create:

- event ingestion service
- event detection runtime
- domain event semantics beyond fixture labels

Completion command:

- `pytest tests/unit/framework/test_event_registry.py tests/integration/registry_loading/test_event_registry_loading.py`

### Step 9. State Registry

전체 방향성:

State type, state value, freshness and transition references를 registry로 구현한다. Current state 자체는 별도 world state가 소유한다.

Primary source markdown:

- `06_registry_specs/state_registry/state_registry.md`

Supporting source markdown:

- `03_core_specifications/04_state_model_registry/4_state_model_registry.md`
- `09_appendices/appendix_c_state_catalog/state_catalog.md`

Generate code:

- `src/ledo_ontology_core/framework/registries/state.py`
- `src/ledo_ontology_core/framework/validation/freshness.py`
- `tests/fixtures/sample_states/state_registry.yaml`

Required objects:

- `StateRegistryEntry`
- `StateRegistry`
- `FreshnessRequirement`
- state transition reference validator

Generate tests:

- `tests/unit/framework/test_state_registry.py`
- `tests/unit/framework/test_freshness_validation.py`

Test requirements:

- valid non-normative state fixture loads
- stale policy reference required where specified
- invalid transition reference fails
- freshness utility is shared but state and snapshot schemas remain separate

Do not create:

- world state store
- live sensor processing
- domain state thresholds

Completion command:

- `pytest tests/unit/framework/test_state_registry.py tests/unit/framework/test_freshness_validation.py`

### Step 10. Snapshot Schema Registry

전체 방향성:

Safety Gate가 읽을 immutable point-in-time snapshot schema registry를 구현한다. `SafetySnapshotDTO`는 Step 1(`schemas/safety_gate.py`)에서 이미 구조가 만들어졌으므로, 이 step은 그 DTO를 소비하는 registry만 만든다.

Primary source markdown:

- `06_registry_specs/snapshot_schema_registry/snapshot_schema_registry.md`

Supporting source markdown:

- `08_runtime_validation/safety_gate/safety_gate.md`
- `03_core_specifications/04_state_model_registry/4_state_model_registry.md`

Generate code:

- `src/ledo_ontology_core/framework/registries/snapshot_schema.py`
- `tests/fixtures/sample_states/snapshot_schema_registry.yaml`

Required objects:

- `SnapshotSchemaRegistryEntry`
- `SnapshotSchemaRegistry`
- `SafetySnapshotDTO` (already defined in Step 1, `schemas/safety_gate.py`; this step just references it)
- snapshot schema version validator
- snapshot immutability/provenance validator

Generate tests:

- `tests/unit/framework/test_snapshot_schema_registry.py`
- `tests/unit/framework/test_safety_snapshot_dto.py`

Test requirements:

- valid snapshot schema loads
- missing observed_at/provenance/lineage fails
- stale/conflict policy refs required where specified
- snapshot is treated as immutable point-in-time object

Do not create:

- Safety Gate service
- graph query for snapshot construction
- disk-based snapshot store

Completion command:

- `pytest tests/unit/framework/test_snapshot_schema_registry.py tests/unit/framework/test_safety_snapshot_dto.py`

### Step 11. Evidence Registry and Evidence Bundle Contracts

전체 방향성:

Evidence type registry와 evidence bundle contract를 구현한다. AI output은 evidence가 아니다. `EvidenceDTO`/`EvidenceBundleDTO`는 Step 1(`schemas/evidence.py`)에서 이미 구조가 만들어졌으므로, 이 step은 그 DTO들을 소비하는 registry만 만든다.

Primary source markdown:

- `06_registry_specs/evidence_registry/evidence_registry.md`

Supporting source markdown:

- `03_core_specifications/05_evidence_model/5_evidence_model.md`
- `09_appendices/appendix_d_evidence_catalog/evidence_catalog.md`

Generate code:

- `src/ledo_ontology_core/framework/registries/evidence.py`
- `tests/fixtures/sample_evidence/evidence_registry.yaml`

Required objects:

- `EvidenceRegistryEntry`
- `EvidenceRegistry`
- `EvidenceDTO`, `EvidenceBundleDTO` (already defined in Step 1, `schemas/evidence.py`)
- evidence lineage validator
- evidence trust/freshness validator

Generate tests:

- `tests/unit/framework/test_evidence_registry.py`
- `tests/unit/framework/test_evidence_bundle.py`

Test requirements:

- valid evidence fixture loads
- missing source/timestamp/provenance/trust validation fails
- AI summary cannot satisfy evidence requirement
- required evidence missing blocks downstream approval path

Do not create:

- evidence store backend
- document parser
- domain evidence thresholds

Completion command:

- `pytest tests/unit/framework/test_evidence_registry.py tests/unit/framework/test_evidence_bundle.py`

### Step 12. Adapter Registry

전체 방향성:

Adapter capability, protocol, mode, and boundary를 registry로 구현한다. Executable dispatch는 아직 만들지 않는다.

Primary source markdown:

- `06_registry_specs/adapter_registry/adapter_registry.md`

Supporting source markdown:

- `03_core_specifications/09_execution_adapter_model/9_execution_adapter_model.md`

Generate code:

- `src/ledo_ontology_core/framework/registries/adapter.py`
- `tests/fixtures/sample_domain_packs/adapter_registry.yaml`

Required objects:

- `AdapterRegistryEntry`
- `AdapterRegistry`
- adapter mode enum
- adapter capability validator

Generate tests:

- `tests/unit/framework/test_adapter_registry.py`

Test requirements:

- mock/dry-run adapter registry entries load
- production-capable adapter entry is not dispatchable by registry alone
- LLM cannot select adapter
- unsupported capability reference fails

Do not create:

- `ExecutionAdapter.dispatch`
- real robot/PLC/SCADA adapter implementation

Completion command:

- `pytest tests/unit/framework/test_adapter_registry.py`

### Step 13. External System Registry

전체 방향성:

External system targets and data direction을 registry로 구현한다. External system은 LEDO 내부 physical executor가 아니다.

Primary source markdown:

- `06_registry_specs/external_system_registry/external_system_registry.md`

Supporting source markdown:

- `00_master_architecture/00_first_construction.md`
- `03_core_specifications/09_execution_adapter_model/9_execution_adapter_model.md`

Generate code:

- `src/ledo_ontology_core/framework/registries/external_system.py`
- `tests/fixtures/sample_domain_packs/external_system_registry.yaml`

Required objects:

- `ExternalSystemRegistryEntry`
- `ExternalSystemRegistry`
- external system direction validator
- external system availability reference validator

Generate tests:

- `tests/unit/framework/test_external_system_registry.py`

Test requirements:

- valid external system fixture loads as draft/non-production
- missing data direction fails
- physical execution ownership remains external
- no physical command can be represented

Do not create:

- external API client
- control protocol writer
- production external system dispatch

Completion command:

- `pytest tests/unit/framework/test_external_system_registry.py`

### Step 14. Decision Registry

전체 방향성:

DecisionCase routing vocabulary, decision tiers, escalation categories, and boundary references를 구현한다.

Primary source markdown:

- `06_registry_specs/decision_registry/decision_registry.md`

Supporting source markdown:

- `03_core_specifications/07_decision_approval_matrix/07_decision_approval_matrix.md`
- `09_appendices/appendix_f_decision_approval_catalog/decision_approval_catalog.md`

Generate code:

- `src/ledo_ontology_core/framework/registries/decision.py`
- `src/ledo_ontology_core/framework/decision/routing.py`
- `tests/fixtures/sample_domain_packs/decision_registry.yaml`

Required objects:

- `DecisionRegistryEntry`
- `DecisionRegistry`
- `DecisionCaseDTO` (already defined in Step 1, `schemas/decision.py`)
- decision boundary validator
- escalation route placeholder using `DOMAIN_DECISION_REQUIRED` where agent/model refs are deferred

Generate tests:

- `tests/unit/framework/test_decision_registry.py`
- `tests/unit/framework/test_decision_routing_contract.py`

Test requirements:

- valid decision fixture loads
- missing evidence/policy/runtime snapshot requirement fails
- approval/execution/safety boundary missing fails
- `applicable_agent_type_refs` is not resolved while agent registry is deferred

Do not create:

- autonomous decision authority
- real escalation policy
- agent vocabulary registry

Completion command:

- `pytest tests/unit/framework/test_decision_registry.py tests/unit/framework/test_decision_routing_contract.py`

### Step 15. Policy Registry and DummyPDP Interface

전체 방향성:

Policy registry contract와 policy engine adapter boundary를 만든다. Policy determines permission, but mock/stub does not define real policy.

Primary source markdown:

- `06_registry_specs/policy_registry/policy_registry.md`

Supporting source markdown:

- `03_core_specifications/08_policy_governance_model/08_policy_governance_model.md`

Generate code:

- `src/ledo_ontology_core/framework/registries/policy.py`
- `src/ledo_ontology_core/framework/policy/engine.py`
- `src/ledo_ontology_core/framework/policy/dummy_pdp.py`
- `tests/fixtures/sample_domain_packs/policy_registry.yaml`

Required objects:

- `PolicyRegistryEntry`
- `PolicyRegistry`
- `PolicyEffect`
- `PolicyEngineAdapter`
- `DummyPDP`
- `PolicyDecisionResponseDTO`

Generate tests:

- `tests/unit/framework/test_policy_registry.py`
- `tests/unit/framework/test_policy_engine_adapter.py`

Test requirements:

- valid policy fixture loads as non-normative/draft
- missing condition/default effect/failure effect fails
- deny/hold/escalate/block effects are fail-closed where required
- `DummyPDP` cannot invent real policy permission

Do not create:

- OPA/Rego production policy
- real emergency policy
- real role authority

Completion command:

- `pytest tests/unit/framework/test_policy_registry.py tests/unit/framework/test_policy_engine_adapter.py`

### Step 16. Approval Registry and Approval DTO Boundary

전체 방향성:

Approval type/status/validity contract를 구현한다. Approval grants authority but does not execute.

Primary source markdown:

- `06_registry_specs/approval_registry/approval_registry.md`

Supporting source markdown:

- `03_core_specifications/07_decision_approval_matrix/07_decision_approval_matrix.md`
- `03_core_specifications/08_policy_governance_model/08_policy_governance_model.md`

Generate code:

- `src/ledo_ontology_core/framework/registries/approval.py`
- `src/ledo_ontology_core/framework/decision/approval.py`
- `tests/fixtures/sample_domain_packs/approval_registry.yaml`

Required objects:

- `ApprovalRegistryEntry`
- `ApprovalRegistry`
- `ApprovalRequestDTO`, `ApprovalDecisionDTO` (already defined in Step 1, `schemas/approval.py`)
- approval validity validator
- approval expiration validator

Generate tests:

- `tests/unit/framework/test_approval_registry.py`
- `tests/unit/framework/test_approval_contract.py`

Test requirements:

- valid approval fixture loads
- missing approver role ref fails
- expired approval fails runtime use
- approval cannot create physical command or execution request by itself

Do not create:

- real approver roles
- emergency approval shortcut
- execution dispatch

Completion command:

- `pytest tests/unit/framework/test_approval_registry.py tests/unit/framework/test_approval_contract.py`

### Step 17. Runtime Validator Contracts

전체 방향성:

Runtime validation result model and validator interface를 만든다. Validators are deterministic, bounded, side-effect free, and fail-closed. `RuntimeValidationInputDTO`/`RuntimeValidationResultDTO`/`ValidatorResultDTO`와 그 특화 DTO들(TOCTOU/SHACL/NetworkHealth/Idempotency/ApprovalValidity/PolicyRevalidation/EvidenceValidity)은 Step 1(`schemas/runtime_validation.py`)에서 이미 구조가 만들어졌으므로, 이 step은 그 DTO들을 소비하는 `RuntimeValidator` 인터페이스와 집계 로직만 만든다.

Primary source markdown:

- `08_runtime_validation/validators/validators.md`

Supporting source markdown:

- `03_core_specifications/01_common_schema_dto/1_common_schema_dto.md`
- `08_runtime_validation/safety_gate/safety_gate.md`

Generate code:

- `src/ledo_ontology_core/framework/validation/runtime.py`
- update `src/ledo_ontology_core/framework/validation/__init__.py`

Required objects:

- `RuntimeValidationInputDTO`, `RuntimeValidationResultDTO`, `ValidatorResultDTO` (already defined in Step 1, `schemas/runtime_validation.py`)
- `RuntimeValidator`
- validator aggregation function

Generate tests:

- `tests/unit/framework/test_runtime_validator_contracts.py`

Test requirements:

- all validator pass aggregates to pass
- missing required validator result fails closed
- unknown required input fails closed
- validator has no external side effect

Do not create:

- Safety Gate decision service
- network call
- disk read
- LLM call

Completion command:

- `pytest tests/unit/framework/test_runtime_validator_contracts.py`

### Step 18. TOCTOU Control

전체 방향성:

Approval-time snapshot and execution-time snapshot 사이의 time-of-check/time-of-use risk를 검증한다.

Primary source markdown:

- `08_runtime_validation/toctou/toctou.md`

Supporting source markdown:

- `03_core_specifications/04_state_model_registry/4_state_model_registry.md`
- `08_runtime_validation/safety_gate/safety_gate.md`

Generate code:

- `src/ledo_ontology_core/framework/validation/toctou.py`
- `src/ledo_ontology_core/framework/runtime/lease.py`

Required objects:

- `TOCTOUValidationInput`
- `TOCTOUValidationResult`
- `SafetyGateLease`
- snapshot comparison function
- lease expiry/consumption validator

Note: `TOCTOUResultDTO` (the architecture-level validator-result contract from `schemas/runtime_validation.py`, Step 1) already exists — `TOCTOUValidationInput`/`TOCTOUValidationResult` above are this step's own function-level input/result types for the comparison logic, not a redefinition of that DTO.

Generate tests:

- `tests/unit/framework/test_toctou_validation.py`
- `tests/unit/framework/test_safety_gate_lease.py`

Test requirements:

- unchanged fresh snapshot passes
- stale snapshot fails
- changed safety-critical condition fails
- expired lease fails
- consumed lease cannot be reused

Do not create:

- live state polling
- graph query
- external system drop handling beyond result contract

Completion command:

- `pytest tests/unit/framework/test_toctou_validation.py tests/unit/framework/test_safety_gate_lease.py`

### Step 19. Idempotency Control

전체 방향성:

Execution-related retry가 duplicate physical intent를 만들지 않도록 idempotency contract를 구현한다.

Primary source markdown:

- `08_runtime_validation/idempotency/idempotency_control.md`

Supporting source markdown:

- `03_core_specifications/09_execution_adapter_model/9_execution_adapter_model.md`

Generate code:

- `src/ledo_ontology_core/framework/validation/idempotency.py`
- `src/ledo_ontology_core/framework/runtime/idempotency.py`

Required objects:

- `IdempotencyContextDTO` (already defined in Step 1, `schemas/execution.py`)
- `IdempotencyValidationResult`
- in-memory idempotency record for tests
- duplicate request detector

Generate tests:

- `tests/unit/framework/test_idempotency_control.py`

Test requirements:

- missing idempotency key fails
- duplicate key with same payload is treated deterministically
- duplicate key with different payload fails
- retry cannot create duplicate execution intent

Do not create:

- production database idempotency store
- external dispatch

Completion command:

- `pytest tests/unit/framework/test_idempotency_control.py`

### Step 20. Network Health and SHACL Prevalidation Result Contracts

전체 방향성:

Safety Gate가 읽을 network health and SHACL prevalidation result contracts를 만든다. Hot path에서 full SHACL validation은 수행하지 않는다.

Primary source markdown:

- `08_runtime_validation/network_health/network_health.md`

Supporting source markdown:

- `08_runtime_validation/shacl_shapes/shacl_shapes.md`
- `08_runtime_validation/validators/validators.md`

Generate code:

- `src/ledo_ontology_core/framework/validation/network_health.py`
- `src/ledo_ontology_core/framework/validation/shacl_result.py`

Required objects:

- `NetworkHealthResult`
- `AdapterAvailabilityResult`
- `SHACLValidationResult`
- precomputed result validator

Note: `NetworkHealthResultDTO`/`SHACLValidationResultDTO` (the architecture-level validator-result contracts from `schemas/runtime_validation.py`, Step 1) already exist — the names above are this step's own precomputed-result-consumption types, not a redefinition of those DTOs.

Generate tests:

- `tests/unit/framework/test_network_health_validation.py`
- `tests/unit/framework/test_shacl_result_contract.py`

Test requirements:

- unavailable adapter fails closed
- stale network health result fails
- missing SHACL prevalidation result fails when required
- no full SHACL validation is executed in hot path

Do not create:

- network client
- SHACL engine invocation in Safety Gate path
- graph database call

Completion command:

- `pytest tests/unit/framework/test_network_health_validation.py tests/unit/framework/test_shacl_result_contract.py`

### Step 21. Safety Gate Service

전체 방향성:

RuntimeValidationResult를 소비해 `SafetyGatePass` 또는 `SafetyGateBlock`만 생성한다. Safety Gate는 승인하지 않고 실행하지 않는다. `SafetyGateInputDTO`/`SafetyGatePassDTO`/`SafetyGateBlockDTO`는 Step 1(`schemas/safety_gate.py`)에서 이미 구조가 만들어졌으므로, 이 step은 그 DTO들을 소비하는 `SafetyGate` 서비스 로직만 만든다.

Primary source markdown:

- `08_runtime_validation/safety_gate/safety_gate.md`

Supporting source markdown:

- `08_runtime_validation/validators/validators.md`
- `08_runtime_validation/toctou/toctou.md`
- `08_runtime_validation/idempotency/idempotency_control.md`

Generate code:

- `src/ledo_ontology_core/framework/runtime/safety_gate.py`

Required objects:

- `SafetyGateInputDTO`, `SafetyGatePassDTO`, `SafetyGateBlockDTO` (already defined in Step 1, `schemas/safety_gate.py`)
- `SafetyGate`
- fail-closed decision function

Generate tests:

- `tests/unit/framework/test_safety_gate.py`
- `tests/integration/safety_gate_flow/test_safety_gate_block_paths.py`

Test requirements:

- all required validation results pass -> `SafetyGatePassDTO`
- any required validator fail -> `SafetyGateBlockDTO`
- missing required input -> block
- unknown required input -> block
- SafetyGatePass is a short-lived lease

Do not create:

- `ExecutionRequest` directly from `ApprovedAction` without pass
- physical command
- external dispatch

Completion command:

- `pytest tests/unit/framework/test_safety_gate.py tests/integration/safety_gate_flow/test_safety_gate_block_paths.py`

### Step 22. Execution Adapter Interface and Non-Production Adapters

전체 방향성:

Execution boundary를 interface, mock, dry-run으로만 구현한다. External systems own actual physical execution.

Primary source markdown:

- `03_core_specifications/09_execution_adapter_model/9_execution_adapter_model.md`

Supporting source markdown:

- `06_registry_specs/adapter_registry/adapter_registry.md`
- `06_registry_specs/external_system_registry/external_system_registry.md`

Generate code:

- `src/ledo_ontology_core/framework/adapters/base.py`
- `src/ledo_ontology_core/framework/adapters/mock.py`
- `src/ledo_ontology_core/framework/adapters/dry_run.py`
- `src/ledo_ontology_core/framework/adapters/blocked.py`
- update `src/ledo_ontology_core/framework/adapters/__init__.py`

Required objects:

- `ExecutionAdapter`
- `MockAdapter`
- `DryRunAdapter`
- blocked adapter stubs for robot middleware, fleet manager, PLC, SCADA, access control
- `ExternalControlRequestDTO` (already defined in Step 1, `schemas/execution.py`)
- `AdapterDispatchResult`

Generate tests:

- `tests/unit/framework/test_execution_adapter_interface.py`
- `tests/unit/framework/test_non_production_adapters.py`

Test requirements:

- mock adapter records request without physical effect
- dry-run adapter returns dry-run result
- blocked production adapter raises `NotImplementedError`
- dispatch requires idempotency key
- no physical command object exists

Do not create:

- real robot/PLC/SCADA/access-control API client
- real emergency stop
- production dispatch

Completion command:

- `pytest tests/unit/framework/test_execution_adapter_interface.py tests/unit/framework/test_non_production_adapters.py`

### Step 23. Audit and Observability Contracts

전체 방향성:

Traceability를 보존하는 audit record builder를 구현한다. Observability infrastructure deployment는 만들지 않는다. `AuditRecordDTO`는 Step 1(`schemas/audit.py`)에서 이미 구조가 만들어졌으므로, 이 step은 그 DTO를 조립하는 builder 로직만 만든다.

Primary source markdown:

- `03_core_specifications/10_audit_observability_model/10_audit_observability_model.md`

Supporting source markdown:

- `03_core_specifications/00_canonical_object_lifecycle/0_canonical_object_lifecycle.md`

Generate code:

- `src/ledo_ontology_core/framework/audit/builder.py`
- update `src/ledo_ontology_core/framework/audit/__init__.py`

Required objects:

- `AuditRecordDTO` (already defined in Step 1, `schemas/audit.py`)
- `AuditRecordBuilder`
- trace linkage validator
- version reference collector

Generate tests:

- `tests/unit/framework/test_audit_record_builder.py`

Test requirements:

- Event, Evidence, StateUpdate, ActionCandidate, DecisionCase, ApprovalDecision, ApprovedAction, SafetyGateResult, ExecutionRequest, ExternalControlRequest, FeedbackEvent can be linked by trace id
- ontology/policy/shacl/snapshot/adapter/registry version refs are preserved when present
- missing trace id fails for safety-critical path

Do not create:

- Prometheus/Grafana/Jaeger deployment
- database audit store

Completion command:

- `pytest tests/unit/framework/test_audit_record_builder.py`

### Step 24. Feedback and World State Reconciliation Boundary

전체 방향성:

External system feedback를 world state reconciliation boundary로 받는 계약을 만든다. Live world state engine은 아직 만들지 않는다. `FeedbackEventDTO`/`WorldStateReconciliationDTO`/`ExecutionStateDTO`는 Step 1(`schemas/feedback.py`)에서 이미 구조가 만들어졌으므로, 이 step은 그 DTO들을 소비하는 reconciliation 로직만 만든다.

Primary source markdown:

- `03_core_specifications/04_state_model_registry/4_state_model_registry.md`

Supporting source markdown:

- `03_core_specifications/09_execution_adapter_model/9_execution_adapter_model.md`
- `03_core_specifications/10_audit_observability_model/10_audit_observability_model.md`

Generate code:

- `src/ledo_ontology_core/framework/runtime/feedback.py`
- `src/ledo_ontology_core/framework/runtime/reconciliation.py`

Required objects:

- `FeedbackEventDTO`, `WorldStateReconciliationDTO`, `ExecutionStateDTO` (already defined in Step 1, `schemas/feedback.py`)
- reconciliation result contract
- fail-safe reconciliation status

Generate tests:

- `tests/unit/framework/test_feedback_reconciliation.py`

Test requirements:

- successful feedback can produce reconciliation result
- missing feedback produces explicit failure/recovery state
- conflicting feedback does not silently update state
- audit trace is preserved

Do not create:

- live world state database
- external sensor gateway
- automatic physical recovery action

Completion command:

- `pytest tests/unit/framework/test_feedback_reconciliation.py`

### Step 25. First End-to-End Reference Flow

전체 방향성:

이전 step들의 DTO, registry, validator, Safety Gate, mock/dry-run adapter, audit boundary가 함께 동작하는지 검증한다. 제품 기능이 아니라 architecture verification flow이다.

Primary source markdown:

- `07_implementation_plan/implementation_slice_3/implementation_slice_3_plan.md`

Supporting source markdown:

- `03_core_specifications/00_canonical_object_lifecycle/0_canonical_object_lifecycle.md`
- `08_runtime_validation/safety_gate/safety_gate.md`
- `03_core_specifications/09_execution_adapter_model/9_execution_adapter_model.md`
- `03_core_specifications/10_audit_observability_model/10_audit_observability_model.md`

Generate code:

- `tests/integration/safety_gate_flow/test_reference_flow.py`
- optional `apps/cli/reference_flow.py` only if the selected source markdown explicitly requires CLI execution

Reference flow:

`Event -> State -> Snapshot -> Evidence -> Decision -> Policy -> Approval -> RuntimeValidation -> SafetyGate -> ExecutionRequest -> Mock/DryRun External System -> Feedback -> Audit -> WorldStateUpdate`

Generate tests:

- `tests/integration/safety_gate_flow/test_reference_flow.py`

Test requirements:

- standard path succeeds with mock/dry-run only
- stale state path blocks at Safety Gate
- missing evidence path blocks before approval or at runtime validation
- missing idempotency key blocks
- trace id and correlation id survive the full path
- no physical command object is created

Do not create:

- UI
- API server
- production external integration
- physical command

Completion command:

- `pytest tests/integration/safety_gate_flow/test_reference_flow.py`

## 7. Step Dependency Order

Implementation order is strict unless a human reviewer explicitly changes it.

1. Step 0: Architecture Index Verification
2. Step 1: Common Schema and Initial DTO Contracts
3. Step 2: Canonical Lifecycle Flow and Boundary Rules
4. Step 3: Ontology Module Boundary Scaffolding
5. Step 4: Registry Base System
6. Step 5: Action Registry
7. Step 6: Identity Registry and Policy Access Skeleton
8. Step 7: Ontology Registry
9. Step 8: Event Registry
10. Step 9: State Registry
11. Step 10: Snapshot Schema Registry
12. Step 11: Evidence Registry and Evidence Bundle Contracts
13. Step 12: Adapter Registry
14. Step 13: External System Registry
15. Step 14: Decision Registry
16. Step 15: Policy Registry and DummyPDP Interface
17. Step 16: Approval Registry and Approval DTO Boundary
18. Step 17: Runtime Validator Contracts
19. Step 18: TOCTOU Control
20. Step 19: Idempotency Control
21. Step 20: Network Health and SHACL Prevalidation Result Contracts
22. Step 21: Safety Gate Service
23. Step 22: Execution Adapter Interface and Non-Production Adapters
24. Step 23: Audit and Observability Contracts
25. Step 24: Feedback and World State Reconciliation Boundary
26. Step 25: First End-to-End Reference Flow

## 8. Per-Step Completion Checklist

Each step is complete only when all items below are true.

- Primary source markdown was read.
- Supporting source markdown was read only as needed.
- Generated code is limited to the files listed for the step.
- Tests listed for the step exist.
- Affected pytest command passes.
- No domain-specific rule was invented.
- No physical execution path was created.
- Any unresolved domain input uses `DOMAIN_DECISION_REQUIRED`, `status: draft`, `NotImplementedError`, skipped test, or strict xfail.
- Final summary cites the primary source markdown and generated files.

## 9. Current First Implementation Target

The first code-generation target is:

`03_core_specifications/01_common_schema_dto/1_common_schema_dto.md`

Reason:

- It defines shared DTO foundations.
- It has the least domain-meaning risk.
- Every registry and runtime validator depends on its base/context/reference contracts.

Start with Step 1 only.

## 10. Final Boundary Statement

Structure can be generated.
Meaning must be governed.
Safety must be validated.
Execution must be bounded.
Audit must preserve accountability.
