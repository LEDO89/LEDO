# PROJECT TREE

This file is a repository structure map only. It is not an architecture source-of-truth document.

If this file conflicts with `AGENTS.md` or `00_master_architecture/`, `AGENTS.md` and `00_master_architecture/` take precedence.

```text
ledo_ontology_core/
|-- AGENTS.md
|-- README.md
|-- PROJECT_TREE.md
|-- pyproject.toml
|-- 00_master_architecture/
|   |-- README.md
|   |-- 00_first_construction.md
|   `-- 01_master_architecture.md
|-- 01_layer_architecture/
|   |-- implementation_guide.md
|   `-- layer.md
|-- 02_layer_stack_mapping/
|   |-- 00_observability_audit_trace_stack_mapping.md
|   |-- 01_experience_presentation_stack_mapping.md
|   |-- 02_api_gateway_stack_mapping.md
|   |-- 03_governance_policy_security_stack_mapping.md
|   |-- 04_core_ontology_kernel_stack_mapping.md
|   |-- 05_knowledge_semantic_memory_stack_mapping.md
|   |-- 06_real_time_world_state_stack_mapping.md
|   |-- 07_distributed_domain_agent_stack_mapping.md
|   |-- 08_decision_router_escalation_stack_mapping.md
|   |-- 09_approved_action_safety_gate_stack_mapping.md
|   |-- 10_unified_cyber_physical_core_stack_mapping.md
|   |-- 11_execution_request_external_control_integration_stack_mapping.md
|   |-- 12_physical_world_stack_mapping.md
|   |-- implementation_guide.md
|   `-- ontology_semantic_reasoning_stack.md
|-- 03_core_specifications/
|   |-- README.md
|   |-- 00_canonical_object_lifecycle/
|   |-- 01_common_schema_dto/
|   |-- 02_event_type_taxonomy/
|   |-- 03_action_type_registry/
|   |-- 04_state_model_registry/
|   |-- 05_evidence_model/
|   |-- 06_ontology_module_boundary/
|   |-- 07_decision_approval_matrix/
|   |-- 08_policy_governance_model/
|   |-- 09_execution_adapter_model/
|   `-- 10_audit_observability_model/
|-- 04_ontology_foundation/
|   |-- 00_ontology_foundation_report.md
|   |-- 01_semantic_web_technology_stack.md
|   |-- 02_upper_ontology_and_standards.md
|   |-- 03_owl_modeling_principles.md
|   |-- 04_reasoning_and_constraint_model.md
|   |-- 05_relationship_and_property_design.md
|   `-- 06_ontology_governance_and_versioning.md
|-- 05_domain_ontology_modules/
|   |-- README.md
|   |-- action/
|   |-- ai/
|   |-- construction/
|   |-- core_crosscutting/
|   |-- core_upper/
|   |-- event/
|   |-- evidence/
|   |-- industrial/
|   |-- mapping/
|   |-- policy/
|   |-- robot/
|   `-- state/
|-- 06_registry_specs/
|   |-- README.md
|   |-- action_registry/
|   |-- adapter_registry/
|   |-- agent_vocabulary_registry/
|   |-- approval_registry/
|   |-- decision_registry/
|   |-- event_registry/
|   |-- evidence_registry/
|   |-- external_system_registry/
|   |-- identity_registry/
|   |-- model_adapter_registry/
|   |-- ontology_registry/
|   |-- policy_registry/
|   |-- snapshot_schema_registry/
|   `-- state_registry/
|-- 07_implementation_plan/
|   |-- README.md
|   |-- implementation_plan.md
|   |-- mvp_phase_1/
|   |-- mvp_phase_2/
|   `-- mvp_phase_3/
|-- 08_runtime_validation/
|   |-- README.md
|   |-- idempotency/
|   |-- network_health/
|   |-- safety_gate/
|   |-- shacl_shapes/
|   |-- toctou/
|   `-- validators/
|-- 09_appendices/
|   |-- README.md
|   |-- PROJECT_TREE.md
|   |-- appendix_a_stack_catalog/
|   |-- appendix_b_event_catalog/
|   |-- appendix_c_state_catalog/
|   |-- appendix_d_evidence_catalog/
|   |-- appendix_e_ontology_module_catalog/
|   `-- appendix_f_decision_approval_catalog/
|-- 10_archive/
|   |-- README.md
|   |-- generative_structure.md
|   `-- review_artifacts/
|       |-- README.md
|       |-- STRUCTURE_FEEDBACK.md
|       |-- STRUCTURE_FEEDBACK_review.md
|       |-- 1st_p0_review.md
|       |-- 2st_p0_review.md
|       |-- 3rd_p1_cleanup_patch.md
|       |-- 4th_p0_p1_verification_review.md
|       |-- 5th_p1_micro_cleanup_patch.md
|       |-- 6th_p0_p1_verification_review.md
|       |-- 7th_remaining_p1_cleanup_patch.md
|       |-- 8th_p0_p1_verification_review.md
|       |-- 9th_p2_documentation_hygiene_cleanup.md
|       |-- 10th_p2_p3_bulk_documentation_cleanup.md
|       |-- 11th_architecture_v1_final_hygiene_verification.md
|       |-- 12th_encoding_mojibake_cleanup.md
|       `-- 13th_project_tree_readme_alignment.md
|-- src/
|   `-- ledo_ontology_core/
|       |-- __init__.py
|       |-- domain_packs/
|       |   |-- README.md
|       |   |-- __init__.py
|       |   |-- action/
|       |   |   `-- __init__.py
|       |   |-- ai/
|       |   |   `-- __init__.py
|       |   |-- construction/
|       |   |   |-- __init__.py
|       |   |-- core_crosscutting/
|       |   |   `-- __init__.py
|       |   |-- core_upper/
|       |   |   `-- __init__.py
|       |   |-- event/
|       |   |   `-- __init__.py
|       |   |-- evidence/
|       |   |   `-- __init__.py
|       |   |-- industrial/
|       |   |   |-- __init__.py
|       |   |-- mapping/
|       |   |   |-- __init__.py
|       |   |-- policy/
|       |   |   |-- __init__.py
|       |   |-- robot/
|       |   |   |-- __init__.py
|       |   `-- state/
|       |       `-- __init__.py
|       `-- framework/
|           |-- __init__.py
|           |-- adapters/
|           |   `-- __init__.py
|           |-- audit/
|           |   `-- __init__.py
|           |-- decision/
|           |   `-- __init__.py
|           |-- graph/
|           |   `-- __init__.py
|           |-- policy/
|           |   `-- __init__.py
|           |-- registries/
|           |   `-- __init__.py
|           |-- runtime/
|           |   |-- README.md
|           |   `-- __init__.py
|           |-- schemas/
|           |   `-- __init__.py
|           `-- validation/
|               `-- __init__.py
|-- apps/
|   |-- README.md
|   |-- api/
|   |   `-- README.md
|   |-- cli/
|   |   `-- README.md
|   `-- worker/
|       `-- README.md
|-- frontend/
|   |-- README.md
|   |-- public/
|   |-- src/
|   |   |-- app/
|   |   |-- components/
|   |   |-- features/
|   |   |   |-- README.md
|   |   |   |-- command_center/
|   |   |   |-- ontology_explorer/
|   |   |   |-- knowledge_graph_explorer/
|   |   |   |-- digital_twin/
|   |   |   |-- safety_operations/
|   |   |   |-- approval_center/
|   |   |   |-- evidence_audit/
|   |   |   |-- agent_operations/
|   |   |   |-- workflow_visualization/
|   |   |   |-- resource_heatmap/
|   |   |   |-- compliance_dashboard/
|   |   |   `-- external_system_status/
|   |   |-- lib/
|   |   `-- styles/
|   `-- tests/
|-- contracts/
|   |-- README.md
|   |-- pydantic_models/
|   |   `-- README.md
|   |-- json_schema/
|   |   `-- README.md
|   |-- examples/
|   |   `-- README.md
|   |-- openapi/
|   |   `-- README.md
|   |-- asyncapi/
|   |   `-- README.md
|   `-- protobuf/
|       `-- README.md
|-- infra/
|   |-- README.md
|   |-- docker/
|   |   `-- README.md
|   |-- k8s/
|   |   `-- README.md
|   |-- observability/
|   |   `-- README.md
|   `-- local_dev/
|       `-- README.md
|-- templates/
|   |-- codex_task_prompt_template.md
|   |-- implementation_guide_template.md
|   `-- spec_metadata_template.md
`-- tests/
    |-- fixtures/
    |   |-- sample_domain_packs/
    |   |-- sample_events/
    |   |-- sample_evidence/
    |   `-- sample_states/
    |-- integration/
    |   |-- decision_flow/
    |   |-- graph_export/
    |   |-- registry_loading/
    |   `-- safety_gate_flow/
    `-- unit/
        |-- domain_packs/
        `-- framework/
```

## Notes

- `PROJECT_TREE.md` is a repository structure map only.
- `AGENTS.md` and `00_master_architecture/` take precedence.
- `05_domain_ontology_modules/` is the human-readable ontology module specification area.
- `src/ledo_ontology_core/domain_packs/` mirrors `05_domain_ontology_modules/` top-level module names for semantic traceability.
- `src/ledo_ontology_core/framework/` contains the shared backend implementation kernel.
- `apps/api/` is the backend service entrypoint.
- `apps/cli/` is for local deterministic operation.
- `apps/worker/` is for background processing.
- `frontend/` is the root-level first-class operator UI product surface.
- `frontend/` must consume backend contracts and must not become the ontology source of truth.
- `contracts/` follows: Pydantic Models -> JSON Schema -> Examples -> OpenAPI -> AsyncAPI -> Protobuf.
- `infra/` stores deployment and operations scaffolding.
- Technical layers such as API, frontend, backend, runtime, audit, validation, adapters, contracts, and observability must not be duplicated inside every domain pack.
- Runtime must not bypass Policy, Safety Gate, Evidence, or Audit.
- No LLM call is allowed in the Safety Gate hot path.
