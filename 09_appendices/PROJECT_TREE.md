# Project Tree

```text
ledo_ontology_core/
├── 00_master_architecture
│   ├── implementation_guide.md
│   └── unified_cyber_physical_core.md
├── 01_layer_architecture
│   ├── implementation_guide.md
│   └── layered_semantic_architecture.md
├── 02_stack_blueprint
│   ├── 01_platform_runtime_devops_stack
│   │   ├── implementation_guide.md
│   │   └── platform_runtime_devops_stack.md
│   ├── 02_ontology_semantic_reasoning_stack
│   │   ├── implementation_guide.md
│   │   └── ontology_semantic_reasoning_stack.md
│   ├── 03_data_ingestion_mapping_stack
│   │   ├── data_ingestion_mapping_stack.md
│   │   └── implementation_guide.md
│   ├── 04_storage_knowledge_memory_stack
│   │   ├── implementation_guide.md
│   │   └── storage_knowledge_memory_stack.md
│   ├── 05_streaming_messaging_stack
│   │   ├── implementation_guide.md
│   │   └── streaming_messaging_stack.md
│   ├── 06_api_service_integration_stack
│   │   ├── api_service_integration_stack.md
│   │   └── implementation_guide.md
│   ├── 07_agent_llm_orchestration_stack
│   │   ├── agent_llm_orchestration_stack.md
│   │   └── implementation_guide.md
│   ├── 08_policy_security_governance_stack
│   │   ├── implementation_guide.md
│   │   └── policy_security_governance_stack.md
│   ├── 09_runtime_validation_safety_stack
│   │   ├── implementation_guide.md
│   │   └── runtime_validation_safety_stack.md
│   ├── 10_execution_adapter_cps_stack
│   │   ├── execution_adapter_cps_stack.md
│   │   └── implementation_guide.md
│   ├── 11_observability_audit_trace_stack
│   │   ├── implementation_guide.md
│   │   └── observability_audit_trace_stack.md
│   ├── 12_ui_graph_digital_twin_stack
│   │   ├── implementation_guide.md
│   │   └── ui_graph_digital_twin_stack.md
│   ├── implementation_guide.md
│   ├── README.md
│   └── technology_stack_blueprint.md
├── 03_core_specifications
│   ├── 01_common_schema_dto
│   │   ├── common_schema_dto.md
│   │   └── implementation_guide.md
│   ├── 02_event_type_taxonomy
│   │   ├── event_type_taxonomy.md
│   │   └── implementation_guide.md
│   ├── 03_action_type_registry
│   │   ├── action_type_registry.md
│   │   └── implementation_guide.md
│   ├── 04_state_model_registry
│   │   ├── implementation_guide.md
│   │   └── state_model_registry.md
│   ├── 05_evidence_model
│   │   ├── evidence_model.md
│   │   └── implementation_guide.md
│   ├── 06_ontology_module_boundary
│   │   ├── implementation_guide.md
│   │   └── ontology_module_boundary.md
│   ├── 07_decision_approval_matrix
│   │   ├── decision_approval_matrix.md
│   │   └── implementation_guide.md
│   ├── 08_policy_governance_model
│   │   ├── implementation_guide.md
│   │   └── policy_governance_model.md
│   ├── 09_execution_adapter_model
│   │   ├── execution_adapter_model.md
│   │   └── implementation_guide.md
│   ├── 10_audit_observability_model
│   │   ├── audit_observability_model.md
│   │   └── implementation_guide.md
│   └── README.md
├── 04_domain_ontology_modules
│   ├── action
│   │   ├── action_ontology.md
│   │   └── implementation_guide.md
│   ├── ai
│   │   ├── ai_ontology.md
│   │   └── implementation_guide.md
│   ├── construction
│   │   ├── construction_ontology.md
│   │   └── implementation_guide.md
│   ├── core_crosscutting
│   │   ├── core_crosscutting_ontology.md
│   │   └── implementation_guide.md
│   ├── core_upper
│   │   ├── core_upper_ontology.md
│   │   └── implementation_guide.md
│   ├── event
│   │   ├── event_ontology.md
│   │   └── implementation_guide.md
│   ├── evidence
│   │   ├── evidence_ontology.md
│   │   └── implementation_guide.md
│   ├── industrial
│   │   ├── implementation_guide.md
│   │   └── industrial_ontology.md
│   ├── mapping
│   │   ├── implementation_guide.md
│   │   └── mapping_ontology.md
│   ├── policy
│   │   ├── implementation_guide.md
│   │   └── policy_ontology.md
│   ├── robot
│   │   ├── implementation_guide.md
│   │   └── robot_ontology.md
│   ├── state
│   │   ├── implementation_guide.md
│   │   └── state_ontology.md
│   └── README.md
├── 05_registry_specs
│   ├── action_registry
│   │   ├── action_registry.md
│   │   └── implementation_guide.md
│   ├── approval_registry
│   │   ├── approval_registry.md
│   │   └── implementation_guide.md
│   ├── decision_registry
│   │   ├── decision_registry.md
│   │   └── implementation_guide.md
│   ├── event_registry
│   │   ├── event_registry.md
│   │   └── implementation_guide.md
│   ├── evidence_registry
│   │   ├── evidence_registry.md
│   │   └── implementation_guide.md
│   ├── policy_registry
│   │   ├── implementation_guide.md
│   │   └── policy_registry.md
│   ├── state_registry
│   │   ├── implementation_guide.md
│   │   └── state_registry.md
│   └── README.md
├── 06_runtime_validation
│   ├── idempotency
│   │   ├── idempotency_validation.md
│   │   └── implementation_guide.md
│   ├── network_health
│   │   ├── implementation_guide.md
│   │   └── network_health_validation.md
│   ├── safety_gate
│   │   ├── implementation_guide.md
│   │   └── safety_gate.md
│   ├── shacl_shapes
│   │   ├── implementation_guide.md
│   │   └── shacl_shapes.md
│   ├── toctou
│   │   ├── implementation_guide.md
│   │   └── toctou_validation.md
│   ├── validators
│   │   ├── implementation_guide.md
│   │   └── runtime_validators.md
│   └── README.md
├── 07_implementation_plan
│   ├── mvp_phase_1
│   │   └── mvp_phase_1_plan.md
│   ├── mvp_phase_2
│   │   └── mvp_phase_2_plan.md
│   ├── mvp_phase_3
│   │   └── mvp_phase_3_plan.md
│   └── README.md
├── 08_appendices
│   ├── appendix_a_stack_catalog
│   │   └── stack_catalog.md
│   ├── appendix_b_event_catalog
│   │   └── event_catalog.md
│   ├── appendix_c_state_catalog
│   │   └── state_catalog.md
│   ├── appendix_d_evidence_catalog
│   │   └── evidence_catalog.md
│   ├── appendix_e_ontology_module_catalog
│   │   └── ontology_module_catalog.md
│   ├── appendix_f_decision_approval_catalog
│   │   └── decision_approval_catalog.md
│   └── README.md
├── 09_archive
│   ├── drafts
│   ├── old_versions
│   └── README.md
├── src
│   └── ledo_ontology_core
│       ├── domain_packs
│       │   ├── construction
│       │   │   ├── __init__.py
│       │   │   ├── action_types.yaml
│       │   │   ├── classes.yaml
│       │   │   ├── decision_rules.yaml
│       │   │   ├── event_types.yaml
│       │   │   ├── evidence_rules.yaml
│       │   │   ├── properties.yaml
│       │   │   └── state_models.yaml
│       │   ├── industrial
│       │   │   ├── __init__.py
│       │   │   ├── action_types.yaml
│       │   │   ├── classes.yaml
│       │   │   ├── decision_rules.yaml
│       │   │   ├── event_types.yaml
│       │   │   ├── evidence_rules.yaml
│       │   │   ├── properties.yaml
│       │   │   └── state_models.yaml
│       │   ├── mapping
│       │   │   ├── __init__.py
│       │   │   ├── external_schema_mappings.yaml
│       │   │   └── ontology_mappings.yaml
│       │   ├── policy
│       │   │   ├── __init__.py
│       │   │   ├── approval_rules.yaml
│       │   │   ├── permissions.yaml
│       │   │   ├── policy_rules.yaml
│       │   │   └── roles.yaml
│       │   ├── robot
│       │   │   ├── __init__.py
│       │   │   ├── action_types.yaml
│       │   │   ├── capabilities.yaml
│       │   │   ├── classes.yaml
│       │   │   ├── decision_rules.yaml
│       │   │   ├── event_types.yaml
│       │   │   ├── evidence_rules.yaml
│       │   │   ├── mission_states.yaml
│       │   │   └── properties.yaml
│       │   └── __init__.py
│       ├── framework
│       │   ├── adapters
│       │   │   └── __init__.py
│       │   ├── audit
│       │   │   └── __init__.py
│       │   ├── decision
│       │   │   └── __init__.py
│       │   ├── graph
│       │   │   └── __init__.py
│       │   ├── policy
│       │   │   └── __init__.py
│       │   ├── registries
│       │   │   └── __init__.py
│       │   ├── schemas
│       │   │   └── __init__.py
│       │   ├── validation
│       │   │   └── __init__.py
│       │   └── __init__.py
│       └── __init__.py
├── templates
│   ├── codex_task_prompt_template.md
│   ├── implementation_guide_template.md
│   └── spec_metadata_template.md
├── tests
│   ├── fixtures
│   │   ├── sample_domain_packs
│   │   │   └── .gitkeep
│   │   ├── sample_events
│   │   │   └── .gitkeep
│   │   ├── sample_evidence
│   │   │   └── .gitkeep
│   │   └── sample_states
│   │       └── .gitkeep
│   ├── integration
│   │   ├── decision_flow
│   │   │   └── .gitkeep
│   │   ├── graph_export
│   │   │   └── .gitkeep
│   │   ├── registry_loading
│   │   │   └── .gitkeep
│   │   └── safety_gate_flow
│   │       └── .gitkeep
│   └── unit
│       ├── domain_packs
│       │   └── .gitkeep
│       └── framework
│           └── .gitkeep
├── .gitignore
├── AGENTS.md
├── pyproject.toml
└── README.md
```
