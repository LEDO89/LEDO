# PROJECT TREE

```text
ledo_ontology_core
├── 00_master_architecture
│   ├── 00_first_construction.md
│   ├── 01_master_architecture.md
│   └── README.md
├── 01_layer_architecture
│   ├── implementation_guide.md
│   └── layer.md
├── 02_layer_stack_mapping
│   ├── 00_observability_audit_trace_stack_mapping.md
│   ├── 01_experience_presentation_stack_mapping.md
│   ├── 02_api_gateway_stack_mapping.md
│   ├── 03_governance_policy_security_stack_mapping.md
│   ├── 04_core_ontology_kernel_stack_mapping.md
│   ├── 05_knowledge_semantic_memory_stack_mapping.md
│   ├── 06_real_time_world_state_stack_mapping.md
│   ├── 07_distributed_domain_agent_stack_mapping.md
│   ├── 08_decision_router_escalation_stack_mapping.md
│   ├── 09_approved_action_safety_gate_stack_mapping.md
│   ├── 10_unified_cyber_physical_core_stack_mapping.md
│   ├── 11_execution_request_external_control_integration_stack_mapping.md
│   ├── 12_physical_world_stack_mapping.md
│   ├── implementation_guide.md
│   └── ontology_semantic_reasoning_stack.md
├── 03_core_specifications
│   ├── 00_canonical_object_lifecycle
│   │   └── 0_canonical_object_lifecycle.md
│   ├── 01_common_schema_dto
│   │   ├── 1_common_schema_dto.md
│   │   └── implementation_guide.md
│   ├── 02_event_type_taxonomy
│   │   ├── 2_event_type_taxonomy.md
│   │   └── implementation_guide.md
│   ├── 03_action_type_registry
│   │   ├── 03_action_type_registry.md
│   │   └── implementation_guide.md
│   ├── 04_state_model_registry
│   │   └── 4_state_model_registry.md
│   ├── 05_evidence_model
│   │   └── 5_evidence_model.md
│   ├── 06_ontology_module_boundary
│   │   └── 6_ontology_module_boundary.md
│   ├── 07_decision_approval_matrix
│   │   └── 07_decision_approval_matrix.md
│   ├── 08_policy_governance_model
│   │   └── 08_policy_governance_model.md
│   ├── 09_execution_adapter_model
│   │   └── 9_execution_adapter_model.md
│   ├── 10_audit_observability_model
│   │   └── 10_audit_observability_model.md
│   └── README.md
├── 04_ontology_foundation
│   ├── 00_ontology_foundation_report.md
│   ├── 01_semantic_web_technology_stack.md
│   ├── 02_upper_ontology_and_standards.md
│   ├── 03_owl_modeling_principles.md
│   ├── 04_reasoning_and_constraint_model.md
│   ├── 05_relationship_and_property_design.md
│   └── 06_ontology_governance_and_versioning.md
├── 05_domain_ontology_modules
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
├── 06_registry_specs
│   ├── action_registry
│   │   ├── action_registry.md
│   │   └── implementation_guide.md
│   ├── adapter_registry
│   │   └── adapter_registry.md
│   ├── agent_vocabulary_registry
│   │   └── agent_vocabulary_registry.md
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
│   ├── external_system_registry
│   │   └── external_system_registry.md
│   ├── identity_registry
│   │   └── Identity_registry.md
│   ├── model_adapter_registry
│   │   └── model_adapter_registry.md
│   ├── ontology_registry
│   │   └── ontology_registry.md
│   ├── policy_registry
│   │   ├── implementation_guide.md
│   │   └── policy_registry.md
│   ├── snapshot_schema_registry
│   │   └── snapshot_schema_registry.md
│   ├── state_registry
│   │   ├── implementation_guide.md
│   │   └── state_registry.md
│   └── README.md
├── 07_implementation_plan
│   ├── mvp_phase_1
│   │   └── mvp_phase_1_plan.md
│   ├── mvp_phase_2
│   │   └── mvp_phase_2_plan.md
│   ├── mvp_phase_3
│   │   └── mvp_phase_3_plan.md
│   ├── implementation_plan.md
│   └── README.md
├── 08_runtime_validation
│   ├── idempotency
│   │   ├── idempotency_control.md
│   │   └── implementation_guide.md
│   ├── network_health
│   │   ├── implementation_guide.md
│   │   └── network_health.md
│   ├── safety_gate
│   │   └── safety_gate.md
│   ├── shacl_shapes
│   │   └── shacl_shapes.md
│   ├── toctou
│   │   ├── implementation_guide.md
│   │   └── toctou.md
│   ├── validators
│   │   ├── implementation_guide.md
│   │   └── validators.md
│   └── README.md
├── 09_appendices
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
│   ├── PROJECT_TREE.md
│   └── README.md
├── 10_archive
│   ├── generative_structure.md
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
├── PROJECT_TREE.md
├── pyproject.toml
├── README.md
├── STRUCTURE_FEEDBACK.md
└── 제목 없는 스프레드시트.xlsx
```
