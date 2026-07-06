# **README.md — 06 Registry Specs**

## **1. Purpose**

`06_registry_specs` is the area that defines the controlled vocabulary, identifiers, versions, statuses, and reference rules used across the entire LEDO Ontology Core.

Registries prevent the system from creating arbitrary names, arbitrary statuses, arbitrary Actions, arbitrary Events, arbitrary Adapters, or arbitrary Snapshot structures.

Registries do not define meaning directly.
Meaning is defined by Ontology and Specification.
Registries stably reference the defined meaning, version it, and fix it into a verifiable form.

The core principles are as follows.

Ontology defines meaning.
Core Specifications define operational contracts.
Registry controls names, identifiers, versions, and allowed vocabularies.
Runtime Validation uses Registry for deterministic validation.
Implementation uses Registry to generate enums, schemas, validators, and tests.

---

## **2. The Role of Registry**

Registries perform the following roles across LEDO.

Controlling fixed vocabulary
Controlling identifiers
Version management
Status management
Maintaining referential integrity
Preventing arbitrary creation
Ensuring verifiability
Maintaining consistency between code and documentation
Providing a registration procedure for domain extension values

A Registry is not a simple list.

A Registry is a control mechanism that connects documentation, Ontology, Runtime Validation, and Implementation.

---

## **3. What Registry Is Not**

Registries do not perform the following.

They do not directly define domain meaning.
They do not arbitrarily create real industrial rules.
They do not estimate safety criteria or risk thresholds.
They do not define physical execution commands.
They do not replace the Ontology Foundation.
They do not replace the Policy Engine.
They do not replace the Safety Gate.

Registry is not the owner of meaning.
Registry is the controller of the identifiers and vocabulary that reference meaning.

---

## **4. Overall Position of Registry**

Within the LEDO structure, Registry connects to every major layer.

Ontology Foundation
→ meaning definition

Core Specifications
→ operational object contract definition

Registry Specs
→ control of names, identifiers, vocabulary, and versions

Runtime Validation
→ Registry-based validation

Implementation
→ Registry-based generation of Enums, DTOs, Validators, and Tests

Domain Modules
→ provide domain-specific registry extensions

---

## **5. Recommended Folder Structure**

`06_registry_specs` is based on the following structure.

06_registry_specs/
  README.md

  action_registry/
  approval_registry/
  decision_registry/
  event_registry/
  evidence_registry/
  policy_registry/
  state_registry/

  adapter_registry/
  external_system_registry/
  snapshot_schema_registry/
  identity_registry/
  ontology_registry/

The following Registries may be added later, once the Agent and SLM structure has stabilized.

  agent_vocabulary_registry/
  model_adapter_registry/

---

## **6. Registry Classification**

Registries fall broadly into five categories.

| Category | Registry | Role |
| ----- | ----- | ----- |
| Operational Registry | `action_registry`, `event_registry`, `state_registry`, `decision_registry`, `approval_registry`, `evidence_registry`, `policy_registry` | Controls the fixed vocabulary used in operational objects and judgment flows |
| Integration Registry | `adapter_registry`, `external_system_registry` | Controls external system connection methods and actual external targets |
| Runtime Registry | `snapshot_schema_registry` | Controls the structure and version of the Safety Gate Snapshot |
| Semantic / Identity Registry | `ontology_registry`, `identity_registry` | Controls Ontology resource identifiers and Canonical Identity |
| AI / Agent Registry | `agent_vocabulary_registry`, `model_adapter_registry` | Controls future Agent / SLM vocabulary and adapter compatibility |

At the initial stage, priority is given to the Operational, Integration, Runtime, and Semantic / Identity Registries.

---

## **7. Core Operational Registries**

Core Operational Registries manage the fixed vocabulary used in LEDO's judgment flow.

### **7.1 Action Registry**

`action_registry` controls the Action Types the system can recognize.

Role:

Manage Action Type ID
Manage Action Type name
Manage the list of Actions usable in ActionCandidate and ApprovedAction
Connect target constraints per Action Type
Connect approval requirements per Action Type
Connect policy references per Action Type
Connect runtime validation requirements per Action Type

The Action Registry does not define actual physical commands.

---

### **7.2 Event Registry**

`event_registry` controls the Event Types the system can recognize.

Role:

Manage Event Type ID
Manage Event Type name
Connect Event severity
Connect Evidence requirement
Reference World State update rules
Reference Decision routing rules
Connect Audit trace

The Event Registry does not arbitrarily create the meaning of actual domain events.
Domain-specific Event Types are defined in Domain Modules and registered in the Registry.

---

### **7.3 State Registry**

`state_registry` controls the State Types and State Values used in the system.

Role:

Manage State Type ID
Manage State Value
Manage State transition references
Connect to World State
Connect to Safety Gate validation flags
Connect to Runtime freshness requirements

The State Registry is not the Source of Truth for the current state.
The Source of Truth for the current state is Real-Time World State.

**Boundary with the Snapshot Schema Registry:** `state_registry` and `snapshot_schema_registry` (Section 9.1) each define freshness/staleness-related fields (`freshness_requirement`, `stale_policy_ref`, `conflict_policy_ref`, etc.) in nearly identical form. This is not duplication; the two registries govern different targets. `state_registry` covers the freshness of **mutable current state** (values that World State keeps updating), while `snapshot_schema_registry` covers the freshness of **immutable point-in-time snapshots** (values that the Safety Gate fixes at approval time and reads as-is). In implementation, share the freshness-validation logic between the two registries through a common utility (e.g. `framework/validation/freshness.py`), but do not merge the two registries' entry schemas.

---

### **7.4 Decision Registry**

`decision_registry` controls DecisionCase, routing decisions, and escalation types.

Role:

Manage Decision Type ID
Manage Decision outcome
Manage Decision tier
Manage Escalation category
Manage Risk routing category
Connect Approval path references
Connect Audit requirement

The Decision Registry does not grant final execution authority.

---

### **7.5 Approval Registry**

`approval_registry` controls approval types and approval statuses.

Role:

Manage Approval Type
Manage Approval State
Manage Approval requirement references
Manage Approver role references
Manage Validity condition references
Manage Expiration rule references
Connect Audit requirement

The Approval Registry does not arbitrarily decide the actual approval authority.
Domain-specific approval authority is defined in the Domain Module and the Governance / Policy structure.

---

### **7.6 Evidence Registry**

`evidence_registry` controls Evidence Types and Evidence requirements.

Role:

Manage Evidence Type ID
Manage Evidence source type
Connect Evidence trust requirement
Connect Timestamp requirement
Connect Provenance requirement
Manage Validation status
Connect EvidenceBundle composition criteria

The Evidence Registry is not Evidence itself.
Evidence is the actual basis for judgment, carrying source, timestamp, trust metadata, provenance, and validation status.

---

### **7.7 Policy Registry**

`policy_registry` controls Policy References and Policy Categories.

Role:

Manage Policy ID
Manage Policy category
Manage Policy version reference
Manage Policy engine reference
Connect Action Type to Policy
Connect Approval requirement to Policy
Connect Runtime validation requirement to Policy

The Policy Registry does not replace the Policy Engine.
The Policy Registry controls which policy must be referenced.

---

## **8. Integration Registries**

Integration Registries control the structure of external system connections.

### **8.1 Adapter Registry**

`adapter_registry` manages the type, mode, protocol, and safety boundary of Adapters that connect to external systems.

Role:

Manage Adapter ID
Manage Adapter Type
Manage Protocol
Distinguish Mock / Dry-run / Production mode
Manage Supported Action Type
Manage Supported External System Type
Manage Health Check Contract
Manage Feedback Contract
Manage Safety Boundary
Manage Version

The Adapter Registry does not own the actual physical execution authority of the external system.

An Adapter is the boundary that delivers requests.

---

### **8.2 External System Registry**

`external_system_registry` manages the actual external systems that are connection targets.

Role:

Manage External System ID
Manage External System Type
Define Authority Boundary
Manage Allowed Request Type
Manage Operational Mode
Manage Health Status Reference
Manage Safety Responsibility Owner
Manage Feedback Contract
Connect Adapter Reference

The External System holds the actual physical execution authority.

LEDO can create an ExecutionRequest, but the actual physical execution is performed by the External System.

---

## **9. Runtime Registry**

### **9.1 Snapshot Schema Registry**

`snapshot_schema_registry` controls the structure and version of the Materialized Safety Snapshot that the Safety Gate reads.

Role:

Manage Snapshot Schema ID
Manage Snapshot Schema Version
Manage Compatible Ontology Version
Manage Compatible Policy Version
Manage Compatible SHACL Shape Version
Define Required Materialized Map
Define Required Field
Define Checksum Rule
Define Expiration Rule
Define Fail-closed Condition
Define Hot-swap Compatibility

In the runtime hot path, the Safety Gate must read only Snapshots validated against the Snapshot Schema Registry.

**Boundary with the State Registry:** see Section 7.3. `snapshot_schema_registry` controls the structure/version of immutable snapshots, while `state_registry` controls the type/transitions of mutable current state. Share the freshness-validation logic; keep the schemas separate.

If the Snapshot Schema does not match, the Safety Gate must fail closed.

---

## **10. Semantic / Identity Registries**

### **10.1 Identity Registry**

`identity_registry` controls the connection between external identifiers and internal Canonical Identity.

Role:

Manage Canonical ID
Manage External ID
Manage Source System
Manage Identifier Scheme
Manage Mapping Rule
Manage Resolution Evidence
Manage Confidence
Manage Validity Period
Manage Governance Status

The Identity Registry connects the following.

IFC GlobalId
OPC-UA NodeId
Robot ID
Sensor ID
Worker ID
Equipment ID
Zone ID
Canonical Object ID

The Identity Registry does not arbitrarily declare `sameAs`.
Identity judgments must be managed through Evidence and Governance.

---

### **10.2 Ontology Registry**

`ontology_registry` controls the identifiers, versions, and statuses of Ontology resources.

Role:

Manage Class IRI
Manage Property IRI
Manage Ontology Module
Manage Ontology Version
Manage Deprecation Status
Manage Replacement IRI
Connect SHACL Reference
Connect Policy Reference
Connect Runtime Materialization Reference
Manage Governance Status

The Ontology Registry does not directly define meaning.

Ontology Foundation = meaning definition
Ontology Registry = control of identifiers and versions for meaning resources

---

## **11. Future AI / Agent Registries**

The following Registries may be added once the Agent and SLM structure has stabilized.

**Status note:** this README specifies both Registries as "to be added later," and `agent_vocabulary_registry/agent_vocabulary_registry.md` and `model_adapter_registry/model_adapter_registry.md` are already written as fully fleshed-out specification documents, including field schemas and example code. The existence of the spec documents does not mean these two Registries may be implemented now.

This repository has adopted full deferral: no DTO, enum, loader, skeleton, or placeholder module is created for either registry until the Agent/SLM pipeline (Layer 7) is actually needed. This is recorded in `07_implementation_plan/implementation_slice_2/implementation_slice_2_plan.md` ("Out of Scope: Agent Vocabulary Registry and Model Adapter Registry"). Where another registry's schema references an agent or model concept (for example `decision_registry`'s `applicable_agent_type_refs` field), the reference is left as an explicit `TODO`-marked placeholder, not a resolved cross-reference and not a stub class. Revisiting this decision requires updating both this note and `implementation_slice_2_plan.md` together.

### **11.1 Agent Vocabulary Registry**

`agent_vocabulary_registry` manages the fixed vocabulary, action phrases, ontology labels, SKOS terms, and prompt-safe vocabulary used by Agents / SLMs.

Role:

Manage Agent vocabulary version
Manage Ontology label reference
Manage SKOS term reference
Manage Allowed output vocabulary
Manage Forbidden output role
Manage Agent-specific terminology

---

### **11.2 Model Adapter Registry**

`model_adapter_registry` manages LoRA, SFT, DAPT, and agent-specific adapter compatibility.

Role:

Manage Model adapter ID
Manage Base model reference
Manage LoRA adapter version
Manage Compatible ontology version
Manage Compatible vocabulary version
Manage Evaluation status
Manage Promotion status
Manage Rollback target

This Registry is added once the SLM / Agent operational structure becomes concrete.

---

## **12. Registry Entry Common Fields**

The list below is not a set of literal field names; it is the set of **conceptual categories** every Registry entry should conceptually include. Each Registry document maps these categories onto concrete field names suited to its own domain. Do not use this list directly as field names when implementing — always follow the actual field names in the corresponding Registry specification document (e.g. `action_registry/action_registry.md` Section 10, "Registry Entry Schema").

| Conceptual Category | Meaning | `action_registry` Mapping Example |
| --- | --- | --- |
| Identifier (registry_id role) | Uniquely identifies the entry within this Registry | `action_type_id` |
| name / description | Human-readable name and description | `canonical_name`, `display_name`, `description` |
| category | Broad classification of the item | `category` |
| version | Version | `version` |
| status | The status enum in Section 13 | `status` |
| owner_module | Owning module/team | `owner_module`, `owner_team` |
| source_document | The specification document of record | `source_document` |
| validation_reference | Reference to validation logic | `runtime_validation_refs`, `precondition_refs`, `postcondition_refs`, `invariant_refs` |
| policy_reference | Policy reference | `required_policy_refs`, `required_approval_level` |
| ontology_reference | Ontology reference | `allowed_target_ontology_classes`, `semantic_iri` |
| runtime_reference | Runtime integration reference | `supported_adapter_refs`, `external_system_type_refs` |
| governance_status | Governance approval status | If not a separate field, falls back to `status` (add an explicit field in the sub-document if governance approval history is required) |
| created_at / updated_at / deprecated_since / replacement_id | Lifecycle timestamps and replacement reference | `created_at`, `updated_at`, `deprecated_since`, `replacement_action_type_id` |

Structural exception: `adapter_registry` does not follow the category structure above. `adapter_registry` uses an availability-oriented `AdapterHealthStatus` (healthy/degraded/unavailable/maintenance/disabled/unknown) instead of the lifecycle `status`, and uses an implementation-oriented model in the form of `AdapterMetadata` instead of a declarative "Registry Entry Schema" section. Code that loads/validates `adapter_registry` must not reuse the common loader shared by the other Registries, and must be handled through a separate path.

Each Registry document defines any additional fields it needs.

---

## **12A. Boundary Fields (`decision_boundary` / `approval_boundary` / `execution_boundary` / `safety_boundary`)**

Across `action_registry`, `evidence_registry`, `agent_vocabulary_registry`, and others, entries carry one or more `*_boundary` fields (e.g. `execution_boundary: must_not_create_execution_request`, `safety_boundary: safety_gate_must_revalidate_runtime_conditions`). These are intentionally **not** a small closed enum — each value is a specific, human-readable invariant statement, and there are dozens of distinct statements in use across the registries. Forcing them into a small enum would lose meaning; leaving them fully free-form risks silent typos in safety-relevant text.

The resolution is a **controlled phrase pattern**, not a fixed value set. Every `*_boundary` value must start with one of the following sanctioned prefixes:

- `must_not_...` — an absolute prohibition (e.g. `must_not_create_execution_request`)
- `does_not_...` — a factual boundary statement about what this object does not do (e.g. `does_not_grant_approval`)
- `may_...` — a permitted-but-limited capability, always paired with what it may *not* do when relevant (e.g. `may_support_decision_case_but_not_decide`)
- `requires_...` — a precondition that must hold (e.g. `requires_additional_evidence`)
- `cannot_...` — synonym for `must_not_...`, used interchangeably in existing entries; prefer `must_not_...` in new entries

A registry loader/validator should reject any `*_boundary` value that does not start with one of these prefixes, rather than accepting arbitrary free text. This catches malformed or accidentally-weakened boundary statements (e.g. a typo that turns `must_not_create_execution_request` into `must_create_execution_request`) without constraining the actual invariant being expressed.

---

## **12B. Cross-Registry Reference Format**

Fields such as `required_policy_refs`, `required_evidence_types`, `supported_adapter_refs`, `runtime_validation_refs`, `precondition_refs`, `timeout_policy_ref`, and similar `*_ref` / `*_refs` fields already follow an informal `<prefix>:<snake_case_id>` convention across the existing registry examples (for example `policy:robot_dispatch_policy`, `evidence:worker_location_snapshot`, `adapter:robot_fleet_adapter`, `validation:robot_available`, `external_system:robot_fleet_manager`). This convention is made explicit here because it was previously only implicit in examples, and no loader currently validates it.

Recommended prefix-to-registry mapping:

| Prefix | Target Registry |
| --- | --- |
| `action:` | `action_registry` |
| `event:` | `event_registry` |
| `state:` | `state_registry` |
| `evidence:` | `evidence_registry` |
| `policy:` | `policy_registry` |
| `approval:` | `approval_registry` |
| `decision:` | `decision_registry` |
| `adapter:` | `adapter_registry` |
| `external_system:` | `external_system_registry` |
| `ontology:` | `ontology_registry` |
| `identity:` | `identity_registry` |
| `snapshot:` | `snapshot_schema_registry` |
| `validation:`, `precondition:`, `postcondition:`, `invariant:`, `timeout:`, `fallback:` | validator/policy specification referenced from `08_runtime_validation/` (not a `06_registry_specs/` registry by itself) |

Referential integrity rule: a registry loader must resolve every `*_ref` / `*_refs` value against its target registry (by prefix) and reject the entry if the target does not exist, or if the target's `status` is `retired` or `blocked` (see Section 13). No registry loader may treat an unresolved reference as a soft warning when the referencing entry's own `status` is `active`.

---

## **13. Registry Status**

A Registry entry may have the following statuses.

draft
active
deprecated
migration_required
retired
blocked

The meanings of the statuses are as follows.

| Status | Meaning |
| ----- | ----- |
| `draft` | Not yet finalized |
| `active` | Currently usable |
| `deprecated` | No longer recommended, but not yet removed |
| `migration_required` | Migration to a replacement item is required |
| `retired` | No longer in use |
| `blocked` | Prohibited from use due to safety, policy, or compatibility issues |

---

## **14. Relationship Between Registry and Domain Module**

A Domain Module may define new domain-specific values.

However, those values must be registered in the Registry.

Domain Action Type
→ Action Registry

Domain Event Type
→ Event Registry

Domain State Type
→ State Registry

Domain Evidence Type
→ Evidence Registry

Domain Policy Reference
→ Policy Registry

Domain Adapter Requirement
→ Adapter Registry

Domain External System
→ External System Registry

Domain Snapshot Requirement
→ Snapshot Schema Registry

A Domain Module cannot bypass the Registry.

---

## **15. Relationship Between Registry and Implementation**

Implementation must be generated based on the Registry.

The Registry is the basis for the following implementation artifacts.

Enum
DTO field constraint
Validator
State transition table
Failure mode table
Safety Gate input contract
Snapshot schema
Adapter interface
Interface-stub adapter behavior (`MockAdapter` / `DryRunAdapter`, per `09_execution_adapter_model` Section 8)
Test case
Migration rule

A value that has no Registry entry must not be arbitrarily created in the implementation.

---

## **16. Final Principle**

`06_registry_specs` is the controlled naming system for the whole of LEDO.

A Registry does not define meaning, but it controls the names, identifiers, versions, and statuses that reference meaning.

Ontology defines meaning.
Registry controls references.
Validation enforces contracts.
Implementation follows Registry.
Domain extensions must register.

The final principles are as follows.

No uncontrolled names.
No uncontrolled identifiers.
No uncontrolled action types.
No uncontrolled external adapters.
No uncontrolled snapshots.
No uncontrolled domain extensions.
