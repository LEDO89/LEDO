# **Implementation Plan**

## **0\. Document Status**

Document Name: LEDO Implementation Plan  
Document Type: Implementation and Runtime Build Plan  
Scope: Pre-Code Architecture-to-Implementation Plan  
Status: Draft for Review  
Primary Rule: Do not alter existing architecture. Only organize it into implementation order.

This document defines how the existing LEDO architecture will be implemented and operated.

This is not a new architecture document.

This document is an implementation alignment document that organizes the already completed LEDO design assets into a concrete build sequence.

The implementation plan must include and preserve the following existing design assets:

00\_master\_architecture/  
01\_layer\_architecture/  
02\_layer\_stack\_mapping/  
03\_core\_specifications/  
04\_ontology\_foundation/  
05\_domain\_ontology\_modules/  
06\_registry\_specs/  
07\_implementation\_plan/  
08\_runtime\_validation/

The purpose of this plan is to prevent architectural drift before code implementation begins.

---

# **1\. Implementation Plan Mission**

## **1.1 Mission**

The mission of this document is to convert LEDO’s completed architecture into a safe, deterministic, implementation-ready plan.

LEDO is not a simple agent application.

LEDO is an ontology-centric Cyber-Physical AI architecture that separates meaning, state, evidence, policy, approval, runtime validation, safety gate, execution request, external physical execution, feedback, and audit across clear responsibility boundaries.

Therefore, implementation must follow the same responsibility boundaries.

Architecture defines responsibility.  
Registry defines operational validity.  
Implementation must preserve both.

---

## **1.2 Implementation Plan Must Not Do**

This implementation plan must not redefine the architecture.

It must not rename layers.

It must not insert new layers into the 13-layer structure.

It must not collapse Policy, Approval, Runtime Validation, Safety Gate, and Execution into one shortcut.

It must not turn Agent output into truth.

It must not turn ExecutionRequest into PhysicalCommand.

It must not treat External System as an internal LEDO component.

It must not treat deployment infrastructure as Layer 12\.

The following rule is fixed:

Layer 12 \= Physical World Layer

Deployment, Kubernetes, CI/CD, runtime operations, and DevOps tooling may appear as supporting implementation infrastructure, but they are not Layer 12\.

---

# **2\. Source Architecture Assets**

The implementation plan is based on the following completed LEDO design assets.

---

## **2.1 Master Architecture**

Repository area:

00\_master\_architecture/  
    01\_master\_architecture  
    00\_frist\_construction  
    readme.md

Master Architecture defines the highest-level thesis of LEDO.

Core thesis:

Ontology defines meaning.  
Evidence supports judgment.  
World State represents current condition.  
Agents generate candidates.  
Policy determines operational permission.  
Approval grants high-risk authority.  
Safety Gate validates execution readiness.  
External Systems perform physical execution.  
Audit preserves accountability.

Implementation meaning:

Every implemented object must preserve its responsibility boundary.

Ontology is not policy.  
Policy is not approval.  
Approval is not safety validation.  
Safety validation is not physical execution.  
ExecutionRequest is not PhysicalCommand.  
External System performs physical execution.

---

## **2.2 Layer Architecture**

Repository area:

01\_layer\_architecture/

Final LEDO layer structure:

Layer 0\. Observability / Audit / Trace Layer  
Layer 1\. Experience / Presentation Layer  
Layer 2\. API Gateway Layer  
Layer 3\. Governance / Policy / Security Layer  
Layer 4\. Core Ontology Kernel Layer  
Layer 5\. Knowledge & Semantic Memory Layer  
Layer 6\. Real-Time World State Layer  
Layer 7\. Distributed Domain Agent Layer  
Layer 8\. Decision Router / Escalation Layer  
Layer 9\. Approved Action / Safety Gate Layer  
Layer 10\. Unified Cyber-Physical Core Layer  
Layer 11\. Execution Request & External Control Integration Layer  
Layer 12\. Physical World Layer

This layer structure is fixed.

Implementation must preserve the layer order and layer responsibility.

---

## **2.3 Layer Stack Mapping**

Repository area:

02\_layer\_stack\_mapping/

Confirmed mapping documents:

0\. "Observability / Audit / Trace" Stack Mapping  
1\. "Experience / Presentation" Stack Mapping  
2\. "API Gateway" Stack Mapping  
3\. "Governance / Policy / Security" Stack Mapping  
4\. "Core Ontology Kernel" Stack Mapping  
5\. "Knowledge & Semantic Memory" Stack Mapping  
6\. "Real-Time World State" Stack Mapping  
7\. "Distributed Domain Agent" Stack Mapping  
8\. "Decision Router / Escalation" Stack Mapping  
9\. "Approved Action / Safety Gate" Stack Mapping  
10\. "Unified Cyber-Physical Core" Stack Mapping  
11\. "Execution Request & External Control Integration" Stack Mapping  
12\. "Physical World" Stack Mapping

Implementation rule:

Layer Stack Mapping must remain 1:1 with Layer Architecture.

Therefore:

Layer 12 Stack Mapping \= Physical World Stack Mapping

---

## **2.4 Core Specifications**

Repository area:

03\_core\_specifications/

Confirmed structure:

03\_core\_specifications/  
    00\_canonical\_object\_lifecycle/  
    01\_common\_schema\_dto/  
    02\_event\_type\_taxonomy/  
    03\_action\_type\_registry/  
    04\_state\_model\_registry/  
    05\_evidence\_model/  
    06\_ontology\_module\_boundary/  
    07\_decision\_approval\_matrix/  
    08\_policy\_governance\_model/  
    09\_execution\_adapter\_model/  
    10\_audit\_observability\_model/  
    README.md

Implementation meaning:

03\_core\_specifications/ is the detailed specification area for Layer 10\.

Layer 10 does not need to become a separate root-level folder.

Layer 10 is expressed through these core specifications.

Layer 10 connects the canonical operational lifecycle:

Event  
State Update  
Evidence  
ActionCandidate  
DecisionCase  
Approval  
ApprovedAction  
SafetyGateResult  
ExecutionRequest  
ExternalControlRequest  
FeedbackEvent  
AuditRecord

---

## **2.5 Ontology Foundation**

Repository area:

04\_ontology\_foundation/

Confirmed structure:

04\_ontology\_foundation/  
    00\_ontology\_foundation\_report  
    01\_semantic\_web\_technology\_stack/  
    02\_upper\_ontology\_and\_standards/  
    03\_owl\_modeling\_principles/  
    04\_reasoning\_and\_constraint\_model/  
    05\_relationship\_and\_property\_design  
    06\_ontology\_governance\_and\_versioning/

Implementation meaning:

04\_ontology\_foundation/ defines the Semantic Foundation.

It governs:

OWL  
RDF  
RDFS  
SHACL  
SPARQL  
BFO  
SOSA / SSN  
SAREF  
PROV-O  
QUDT  
GeoSPARQL  
Reasoning  
Constraint Model  
Relationship and Property Design  
Ontology Governance  
Ontology Versioning

Implementation must never treat ontology as a simple label list.

Ontology is the semantic authority.

---

## **2.6 Domain Ontology Modules**

Repository area:

05\_domain\_ontology\_modules/

Domain ontology modules represent construction and industrial domain extension.

Implementation must include the following domain objects:

Worker  
Equipment  
Robot / Humanoid  
Zone  
WorkZone  
HazardZone  
Task  
WorkProcess  
Hazard  
Risk  
Sensor  
Observation  
Event  
State  
Snapshot  
Evidence  
Decision  
Policy  
Approval  
Action  
ExternalSystem  
ExecutionRequest  
AuditRecord

Implementation rule:

Domain object must be grounded in ontology.  
Domain event must be registered.  
Domain state must be registered.  
Domain snapshot must have a schema.  
Domain evidence must be validated.  
Domain decision must follow decision registry.  
Domain policy must pass policy registry.  
Domain approval must pass approval registry.  
Domain execution must pass safety gate and external system boundary.

---

## **2.7 Registry Specifications**

Repository area:

06\_registry\_specs/

Confirmed registry folders:

06\_registry\_specs/  
    agent\_vocabulary\_registry/  
    approval\_registry/  
    decision\_registry/  
    event\_registry/  
    evidence\_registry/  
    external\_system\_registry/  
    identity\_registry/  
    model\_adapter\_registry/  
    ontology\_registry/  
    policy\_registry/  
    snapshot\_schema\_registry/  
    state\_registry/

These are the controlled registry specifications currently present in the repository.

Implementation must preserve this actual registry set.

Additional registry concepts may exist in Core Specifications or future expansion, but the implementation plan must not pretend they already exist inside `06_registry_specs/` unless they are actually created there.

---

## **2.8 Implementation Plan**

Repository area:

07\_implementation\_plan/

This document belongs here.

Purpose:

Convert completed architecture into implementation and runtime build order.

This folder must not redefine architecture.

It must reference and organize:

Master Architecture  
Layer Architecture  
Layer Stack Mapping  
Core Specifications  
Ontology Foundation  
Domain Ontology Modules  
Registry Specifications  
Runtime Validation  
MVP Plan  
Pre-Code Checklist

---

## **2.9 Runtime Validation**

Repository area:

08\_runtime\_validation/

Purpose:

Define execution-time validation before Safety Gate pass.

Runtime Validation is not the same as Safety Gate.

Runtime Validation checks current validity.  
Safety Gate makes final pre-execution pass/block decision.

---

# **3\. Fixed Architecture Invariants**

The following invariants must be enforced in implementation.

Ontology is the semantic authority.  
AI output is candidate, not truth.  
Evidence is required for trusted decisions.  
Policy determines operational permission.  
Approval grants high-risk authority.  
Safety Gate validates execution readiness.  
ExecutionRequest is not a physical command.  
External Systems perform physical execution.  
Runtime hot path reads precomputed results only.  
Audit preserves traceability.

Any implementation violating these invariants is not LEDO.

---

# **4\. Responsibility Boundary Rules**

## **4.1 Candidate Boundary**

Candidate ≠ Decision

Agent or model output may produce:

Intent Interpretation  
Situation Summary  
Risk Interpretation  
MappingProposal  
EvidenceSummary  
ActionCandidate  
EscalationCase  
DecisionCase draft  
PolicyImpactSuggestion  
Explanation

Agent or model output must not directly produce:

Evidence  
Policy Decision  
Approval  
Safety Gate Decision  
Final ExecutionRequest  
Final ExternalControlRequest  
Physical Command

---

## **4.2 Decision Boundary**

Decision ≠ Approval

Decision evaluates what should happen based on evidence, risk, policy, and route.

Decision does not grant authority.

---

## **4.3 Policy Boundary**

Policy pass ≠ Approval pass

Policy determines whether a proposed action is conditionally allowed.

Policy does not grant human authority.

---

## **4.4 Approval Boundary**

Approval ≠ Safety Gate pass

Approval grants authority.

Approval does not prove that execution-time physical conditions are still safe.

---

## **4.5 Safety Gate Boundary**

Safety Gate pass ≠ Physical Execution

Safety Gate validates readiness.

It does not perform physical execution.

---

## **4.6 Execution Boundary**

ExecutionRequest ≠ PhysicalCommand  
ExternalControlRequest ≠ PhysicalCommand  
External System \= Physical Execution Authority

LEDO sends bounded, approved, validated execution intent.

Actual physical execution belongs to external systems.

---

# **5\. End-to-End Architecture Flow**

The canonical LEDO flow is fixed as follows:

Physical World  
→ Real-Time World State  
→ Knowledge / Evidence Binding  
→ Distributed Domain Agents  
→ ActionCandidate  
→ Semantic Validation  
→ Evidence Check  
→ Policy Check  
→ Decision Router  
→ Approval  
→ Safety Gate  
→ ExecutionRequest  
→ External Control Integration  
→ External System  
→ Physical World  
→ Feedback  
→ Audit  
→ World State Update

Implementation must preserve this flow.

---

# **6\. Source of Truth Boundaries**

The implementation must preserve the following source of truth boundaries.

Semantic Meaning  
    → Ontology

Class / Property / Axiom  
    → Ontology Foundation

Current Runtime State  
    → Real-Time World State

Historical Evidence  
    → Evidence Store / Audit

Operational Permission  
    → Policy

High-Risk Authority  
    → Approval

Execution Readiness  
    → Safety Gate Snapshot

Physical Execution  
    → External System

Identity Resolution  
    → Canonical Identity / Registry

User View  
    → Presentation Layer

AI Interpretation  
    → Agent Output as Candidate

---

# **7\. Implementation Strategy**

## **7.1 Strategy**

Implementation must proceed from stable meaning to physical execution boundary.

Correct implementation order:

Meaning  
→ Registry  
→ Event  
→ State  
→ Snapshot  
→ Evidence  
→ Decision  
→ Policy  
→ Approval  
→ Runtime Validation  
→ Safety Gate  
→ ExecutionRequest  
→ External Integration  
→ Feedback  
→ Audit

Wrong implementation order:

Agent first  
UI first  
LLM first  
Execution first  
External system first

These are dangerous because they create behavior before operational validity.

---

## **7.2 Implementation Philosophy**

Implement contracts before behavior.  
Implement validation before execution.  
Implement registry before runtime use.  
Implement state before snapshot.  
Implement snapshot before evidence.  
Implement evidence before decision.  
Implement policy before approval.  
Implement runtime validation before Safety Gate.  
Implement Safety Gate before ExecutionRequest.  
Implement audit across all lifecycle stages.

---

# **8\. Implementation Phases**

---

## **Phase 0\. Architecture Freeze and Index Verification**

### **Goal**

Freeze all existing architecture assets before code begins.

### **Inputs**

00\_master\_architecture/  
01\_layer\_architecture/  
02\_layer\_stack\_mapping/  
03\_core\_specifications/  
04\_ontology\_foundation/  
05\_domain\_ontology\_modules/  
06\_registry\_specs/

### **Tasks**

Verify Layer 0-12 names.  
Verify Layer 12 \= Physical World Layer.  
Verify Layer Stack Mapping matches Layer Architecture 1:1.  
Verify Core Specifications folder list.  
Verify Ontology Foundation folder list.  
Verify Registry Specs folder list.  
Verify End-to-End Architecture Flow.  
Verify Safety Gate Rule.  
Verify Execution Boundary Rule.  
Verify Agent Boundary Rule.  
Verify Architecture Invariants.

### **Output**

architecture\_freeze\_checklist.md  
repository\_index.md  
implementation\_dependency\_map.md

### **Completion Criteria**

No layer mismatch.  
No missing core specification section.  
No missing registry folder from implementation plan.  
No unauthorized new layer.  
No collapse of responsibility boundaries.

---

## **Phase 1\. Common Contract Foundation**

### **Goal**

Create common implementation contracts that every registry and core object will share.

### **Implementation Area**

03\_core\_specifications/01\_common\_schema\_dto/

### **Core Objects**

BaseEntity  
BaseRegistryEntry  
BaseCoreObject  
BaseEvent  
BaseState  
BaseSnapshot  
BaseEvidence  
BaseDecisionCase  
BasePolicyEvaluation  
BaseApproval  
BaseRuntimeValidation  
BaseSafetyGateResult  
BaseExecutionRequest  
BaseAuditRecord

### **Common Fields**

id  
canonical\_name  
semantic\_iri  
version  
status  
created\_at  
updated\_at  
trace\_id  
correlation\_id  
source\_ref  
owner\_module  
owner\_team  
audit\_refs  
dependency\_refs

### **Completion Criteria**

All core objects share consistent ID, version, status, timestamp, trace, and audit structure.

---

## **Phase 2\. Semantic Foundation Implementation**

### **Goal**

Implement the semantic foundation before operational runtime behavior.

### **Implementation Area**

04\_ontology\_foundation/  
06\_registry\_specs/ontology\_registry/

### **Tasks**

Implement ontology module reference model.  
Implement namespace and IRI validation.  
Implement ontology version validation.  
Implement class/property semantic reference validation.  
Implement upper ontology alignment reference.  
Implement reasoning profile metadata.  
Implement SHACL shape reference metadata.  
Implement ontology governance and versioning rule.

### **Must Preserve**

Ontology defines meaning.  
Ontology is not World State.  
Ontology is not Evidence.  
Ontology is not Policy.  
Ontology is not Approval.  
Ontology is not Safety Gate.  
Ontology is not PhysicalCommand.

### **Completion Criteria**

Unregistered semantic IRI is rejected.  
Deprecated ontology module is rejected.  
Unsupported ontology version is rejected.  
Class/property references must resolve to active ontology references.

---

## **Phase 3\. Registry Base System**

### **Goal**

Implement a consistent registry system before implementing individual registries.

### **Implementation Area**

06\_registry\_specs/

### **Common Registry Interfaces**

load()  
get()  
exists()  
validate()  
resolve()  
is\_active()  
check\_version()  
check\_dependency()  
check\_status()  
check\_boundary()

### **Common Registry Status**

draft  
active  
deprecated  
migration\_required  
retired  
blocked

### **Required Components**

RegistryLoader  
RegistryStore  
RegistryResolver  
RegistryValidator  
RegistryDependencyChecker  
RegistryMigrationChecker  
RegistryAuditHook

### **Completion Criteria**

Every registry entry can be loaded, resolved, validated, version-checked, and dependency-checked through the same base interface.

---

## **Phase 4\. Identity and Access Foundation**

### **Goal**

Implement identity and access boundary before policy, approval, or action.

### **Implementation Area**

06\_registry\_specs/identity\_registry/

### **Tasks**

Define actor identity.  
Define service identity.  
Define agent identity.  
Define role.  
Define scope.  
Define certification.  
Define identity status.  
Define identity validity check.

### **Related Layer**

Layer 3\. Governance / Policy / Security Layer

### **Completion Criteria**

No actor can propose, approve, validate, or execute anything without registered identity.

---

## **Phase 5\. Event Registry Implementation**

### **Goal**

Implement valid event types before state update.

### **Implementation Area**

06\_registry\_specs/event\_registry/  
03\_core\_specifications/02\_event\_type\_taxonomy/

### **Tasks**

Define CoreEvent schema.  
Define event type taxonomy.  
Define event producer boundary.  
Define event payload schema reference.  
Define event source reference.  
Define event-to-state update eligibility.  
Define event audit requirement.

### **Completion Criteria**

Unregistered event type is rejected.  
Invalid event producer is rejected.  
Event without payload schema is rejected.  
Valid Event does not automatically update State.

---

## **Phase 6\. State Registry Implementation**

### **Goal**

Implement official current state contract.

### **Implementation Area**

06\_registry\_specs/state\_registry/  
03\_core\_specifications/04\_state\_model\_registry/

### **Tasks**

Define State Type.  
Define State Key.  
Define State Owner.  
Define State Source.  
Define State Update Rule.  
Define State Transition Rule.  
Define State Freshness Rule.  
Define State Conflict Rule.  
Define State Storage Reference.  
Define State Snapshot Binding.

### **Must Preserve**

State represents what is currently true.  
State is not Event.  
State is not Snapshot.  
State is not Evidence.  
State is mutable only through controlled update rules.

### **Completion Criteria**

Unregistered State is rejected.  
State without owner is rejected.  
State update without rule is rejected.  
Stale State is rejected for Safety Gate.  
Conflicting safety State triggers block or review.

---

## **Phase 7\. Snapshot Schema Registry Implementation**

### **Goal**

Implement immutable state-freezing contract.

### **Implementation Area**

06\_registry\_specs/snapshot\_schema\_registry/

### **Tasks**

Define Snapshot Type.  
Define Snapshot Schema.  
Define Snapshot Metadata.  
Define Snapshot Freshness.  
Define Snapshot Immutability.  
Define Snapshot Lineage.  
Define Snapshot Provenance.  
Define Snapshot Serialization.  
Define Snapshot Safety Gate Usability.  
Define Snapshot Hot Path Eligibility.

### **Must Preserve**

Snapshot freezes State at a specific time.  
Snapshot is immutable.  
Snapshot is not Event.  
Snapshot is not Evidence itself.  
Approval-time Snapshot is not Execution-time Snapshot.

### **Completion Criteria**

Unregistered Snapshot Schema is rejected.  
Mutable Snapshot is rejected.  
Stale Snapshot is rejected for Safety Gate.  
Safety Gate cannot use snapshot\_schema with safety\_gate\_usable=false.

---

## **Phase 8\. Evidence Registry Implementation**

### **Goal**

Implement trusted judgment basis.

### **Implementation Area**

06\_registry\_specs/evidence\_registry/  
03\_core\_specifications/05\_evidence\_model/

### **Tasks**

Define Evidence Type.  
Define Evidence Source.  
Define Evidence Quality.  
Define Evidence Freshness.  
Define Evidence Lineage.  
Define Evidence Bundle.  
Define Evidence-to-Decision dependency.

### **Must Preserve**

Evidence supports judgment.  
Evidence is not Decision.  
Snapshot does not automatically become Evidence.  
State does not automatically become Evidence.

### **Completion Criteria**

Unregistered Evidence Type is rejected.  
Evidence without lineage is rejected.  
Evidence below quality threshold is rejected.  
Stale Evidence is rejected for safety-critical decision.

---

## **Phase 9\. Agent Vocabulary Registry Implementation**

### **Goal**

Constrain what agents can say, generate, and request.

### **Implementation Area**

06\_registry\_specs/agent\_vocabulary\_registry/

### **Tasks**

Define allowed agent vocabulary.  
Define allowed candidate types.  
Define prohibited output types.  
Define ontology grounding requirement.  
Define policy boundary.  
Define action candidate boundary.

### **Must Preserve**

Agent output is candidate, not truth.  
Agent must not create final Evidence.  
Agent must not create Policy Decision.  
Agent must not create Approval.  
Agent must not create Safety Gate Decision.  
Agent must not create Final ExecutionRequest.  
Agent must not create Physical Command.

### **Completion Criteria**

Agent output outside allowed vocabulary is rejected.  
Agent-generated PhysicalCommand is rejected.  
Agent-generated final approval or execution is rejected.

---

## **Phase 10\. Model Adapter Registry Implementation**

### **Goal**

Constrain model invocation and output boundaries.

### **Implementation Area**

06\_registry\_specs/model\_adapter\_registry/

### **Tasks**

Define model adapter type.  
Define runtime provider.  
Define input schema.  
Define output schema.  
Define allowed task.  
Define prohibited output.  
Define guard requirement.  
Define privacy boundary.  
Define model output validation.

### **Must Preserve**

Model output is not Decision.  
Model output is not Approval.  
Model output is not Safety Gate pass.  
Model output is not ExecutionRequest.  
Model output is not PhysicalCommand.

### **Completion Criteria**

Unregistered model adapter cannot be invoked.  
Model output must pass schema guard.  
Model output must pass ontology guard.  
Model output must pass policy boundary before downstream use.

---

## **Phase 11\. Decision Registry Implementation**

### **Goal**

Implement controlled judgment flow.

### **Implementation Area**

06\_registry\_specs/decision\_registry/  
03\_core\_specifications/07\_decision\_approval\_matrix/

### **Tasks**

Define Decision Rule.  
Define DecisionCase.  
Define required Evidence.  
Define required State or Snapshot.  
Define risk classification.  
Define escalation route.  
Define policy dependency.  
Define approval dependency.

### **Must Preserve**

Decision evaluates what should happen.  
Decision is not Approval.  
Decision is not ExecutionRequest.

### **Completion Criteria**

Decision without required Evidence is rejected.  
Decision cannot bypass Policy.  
Decision cannot create ExecutionRequest.  
Decision route must be auditable.

---

## **Phase 12\. Policy Registry Implementation**

### **Goal**

Implement operational permission.

### **Implementation Area**

06\_registry\_specs/policy\_registry/  
03\_core\_specifications/08\_policy\_governance\_model/

### **Tasks**

Define Policy Type.  
Define Policy Condition.  
Define Policy Constraint.  
Define Policy Effect.  
Define Policy Priority.  
Define Policy Scope.  
Define Policy Engine Reference.  
Define emergency override rule.  
Define fallback and escalation rule.

### **Must Preserve**

Policy determines operational permission.  
Policy pass is not Approval pass.  
Policy evaluation failure must not silently become allow.

### **Completion Criteria**

Unregistered Policy is rejected.  
Inactive Policy is rejected.  
Policy failure is fail-secure.  
Policy conflict is visible and auditable.

---

## **Phase 13\. Approval Registry Implementation**

### **Goal**

Implement high-risk authority and approval boundary.

### **Implementation Area**

06\_registry\_specs/approval\_registry/  
03\_core\_specifications/07\_decision\_approval\_matrix/

### **Tasks**

Define Approval Type.  
Define Approver Role.  
Define Approval Scope.  
Define Approval Condition.  
Define Approval Expiry.  
Define Approval Evidence Requirement.  
Define Approval Audit Requirement.

### **Must Preserve**

Approval grants authority.  
Approval does not validate runtime safety.  
Approval does not create PhysicalCommand.  
Approval-time Snapshot is not Execution-time Snapshot.

### **Completion Criteria**

Unauthorized approver is rejected.  
Expired approval is rejected.  
Approval without policy pass is rejected.  
Approval cannot bypass Safety Gate.

---

## **Phase 14\. External System Registry Implementation**

### **Goal**

Implement external physical execution boundary.

### **Implementation Area**

06\_registry\_specs/external\_system\_registry/  
03\_core\_specifications/09\_execution\_adapter\_model/

### **Tasks**

Define External System.  
Define supported action intent.  
Define supported protocol.  
Define health check requirement.  
Define feedback expectation.  
Define physical execution boundary.  
Define safety-rated controller boundary.

### **Must Preserve**

External System performs physical execution.  
LEDO does not perform physical execution directly.  
External System compatibility pass is not Safety Gate pass.

### **Completion Criteria**

Unregistered External System cannot receive ExecutionRequest.  
External System without health validation is blocked.  
External System cannot be treated as internal LEDO authority.

---

## **Phase 15\. Runtime Validation Design and Implementation**

### **Goal**

Verify current execution-time validity before Safety Gate decision.

### **Implementation Area**

08\_runtime\_validation/

### **Tasks**

Define runtime validation concept.  
Define runtime validation rule structure.  
Define state freshness validation.  
Define snapshot freshness validation.  
Define evidence validity validation.  
Define approval validity validation.  
Define policy revalidation.  
Define external system readiness check.  
Define adapter health check.  
Define capability availability check.  
Define conflict state check.

### **Must Preserve**

Runtime Validation is not Approval.  
Runtime Validation is not Safety Gate itself.  
Runtime Validation checks whether current conditions are still valid.  
Safety Gate uses runtime validation result to pass or block.

### **Completion Criteria**

Stale State blocks execution path.  
Stale Snapshot blocks execution path.  
Expired Approval blocks execution path.  
Invalid Policy blocks execution path.  
Unhealthy External System blocks execution path.  
Unhealthy Adapter blocks execution path.

---

## **Phase 16\. Safety Gate Implementation**

### **Goal**

Implement deterministic final execution readiness validation.

### **Implementation Area**

Layer 9\. Approved Action / Safety Gate Layer  
08\_runtime\_validation/  
03\_core\_specifications/

### **Safety Gate Rule**

Safety Gate validates execution readiness for approved actions.

Safety Gate does not grant approval.

Approval grants authority.

Safety Gate validates execution readiness.

### **Runtime Hot Path Must Not Perform**

OWL Reasoning  
Full SHACL Validation  
SPARQL Query  
Graph DB Network Call  
LLM / SLM Call  
External API Call  
Disk I/O  
Unbounded Computation

### **Runtime Hot Path May Only Read**

Materialized Safety Snapshot  
Precomputed validation result  
Immutable runtime validation summary  
Fixed layout safety data

### **Completion Criteria**

No Safety Gate pass without ApprovedAction.  
No Safety Gate pass without fresh runtime validation.  
No Safety Gate pass from LLM / SLM output.  
No Safety Gate pass from stale State.  
No Safety Gate pass from stale Snapshot.  
No ExecutionRequest without Safety Gate pass.

---

## **Phase 17\. Execution Request and External Control Integration**

### **Goal**

Convert approved and validated intent into bounded request for external systems.

### **Implementation Area**

Layer 11\. Execution Request & External Control Integration Layer  
03\_core\_specifications/09\_execution\_adapter\_model/  
06\_registry\_specs/external\_system\_registry/

### **LEDO Defines**

intent  
target  
constraints  
approval reference  
evidence reference  
policy reference  
safety validation result  
trace id  
idempotency key  
expected feedback

### **External Systems Perform**

Robot Middleware  
Fleet Manager  
PLC  
SCADA  
Access Control System  
Equipment Controller  
Site Operation System  
Safety-rated Controller

### **Must Preserve**

ExecutionRequest is not PhysicalCommand.  
ExternalControlRequest is not PhysicalCommand.  
External System performs physical execution.

### **Completion Criteria**

ExecutionRequest can only be created after Safety Gate pass.  
ExecutionRequest must include approval reference.  
ExecutionRequest must include evidence reference.  
ExecutionRequest must include policy reference.  
ExecutionRequest must include safety validation result.  
ExecutionRequest must include trace id and idempotency key.

---

## **Phase 18\. Feedback and World State Update**

### **Goal**

Close the cyber-physical loop.

### **Flow**

ExecutionRequest  
→ External System  
→ Physical World  
→ ExecutionResult  
→ FeedbackEvent  
→ Audit  
→ World State Update

### **Tasks**

Define ExecutionResult schema.  
Define FeedbackEvent schema.  
Define feedback-to-state update rule.  
Define success / failure / timeout handling.  
Define compensating action request.  
Define audit trace.

### **Completion Criteria**

Every execution request must expect feedback.  
Missing feedback must be detected.  
Execution result must update audit.  
Execution result may update world state only through valid event-state rule.

---

## **Phase 19\. Observability and Audit Implementation**

### **Goal**

Make every lifecycle step traceable.

### **Implementation Area**

Layer 0\. Observability / Audit / Trace Layer  
03\_core\_specifications/10\_audit\_observability\_model/

### **Required Audit Targets**

event\_received  
event\_validated  
state\_updated  
snapshot\_created  
evidence\_created  
decision\_created  
policy\_evaluated  
approval\_requested  
approval\_granted  
approval\_rejected  
runtime\_validation\_executed  
safety\_gate\_passed  
safety\_gate\_blocked  
execution\_request\_created  
external\_control\_request\_sent  
execution\_result\_received  
feedback\_event\_created  
world\_state\_updated  
registry\_changed  
ontology\_changed

### **Completion Criteria**

No lifecycle step without trace\_id.  
No high-risk action without audit.  
No Safety Gate result without audit.  
No execution request without audit.

---

# **9\. MVP Implementation Scope**

The MVP must not implement everything.

The MVP must prove that LEDO’s end-to-end lifecycle works.

MVP canonical flow:

Event  
→ State  
→ Snapshot  
→ Evidence  
→ Decision  
→ Policy  
→ Approval  
→ Runtime Validation  
→ Safety Gate  
→ ExecutionRequest  
→ External System  
→ Feedback  
→ Audit  
→ World State Update

MVP must include two flows:

MVP Flow A: STOP\_WORK  
MVP Flow B: DISPATCH\_ROBOT

---

## **9.1 MVP Flow A: STOP\_WORK**

Purpose:

Validate safety-critical decision, policy, approval, runtime validation, and Safety Gate.

Flow:

HazardDetected  
WorkerLocationUpdated  
ZoneStatusChanged  
    ↓  
hazard\_state  
worker\_location\_state  
zone\_status\_state  
    ↓  
hazard\_detection\_snapshot  
worker\_location\_snapshot  
zone\_status\_snapshot  
    ↓  
EvidenceBundle  
    ↓  
DecisionCase: stop\_work\_safety\_risk\_v1  
    ↓  
PolicyEvaluation: stop\_work\_policy\_v1  
    ↓  
ApprovalRequest: stop\_work\_safety\_supervisor\_v1  
    ↓  
ApprovedAction: STOP\_WORK  
    ↓  
RuntimeValidation:  
        hazard\_still\_present  
        worker\_location\_fresh  
        zone\_status\_valid  
    ↓  
SafetyGateResult  
    ↓  
ExecutionRequest:  
        action\_type: STOP\_WORK  
        target: WorkZone  
        external\_system: site\_operation\_system or notification system  
    ↓  
FeedbackEvent  
    ↓  
Audit  
    ↓  
World State Update

Hard boundary:

STOP\_WORK ExecutionRequest is not PhysicalCommand.  
External System performs actual site control, notification, or work stop workflow.

---

## **9.2 MVP Flow B: DISPATCH\_ROBOT**

Purpose:

Validate cyber-physical execution boundary and external fleet manager integration.

Flow:

RobotStatusUpdated  
WorkerLocationUpdated  
ZoneStatusChanged  
ExternalSystemStatusUpdated  
    ↓  
robot\_status\_state  
worker\_location\_state  
zone\_status\_state  
external\_system\_health\_state  
adapter\_health\_state  
    ↓  
robot\_availability\_snapshot  
worker\_location\_snapshot  
zone\_status\_snapshot  
external\_system\_health\_snapshot  
adapter\_health\_snapshot  
    ↓  
EvidenceBundle  
    ↓  
DecisionCase: dispatch\_robot\_v1  
    ↓  
PolicyEvaluation: robot\_dispatch\_policy\_v1  
    ↓  
ApprovalRequest: dispatch\_robot\_supervisor\_v1  
    ↓  
ApprovedAction: DISPATCH\_ROBOT  
    ↓  
RuntimeValidation:  
        robot\_available  
        worker\_not\_in\_robot\_path  
        zone\_accessible  
        external\_system\_reachable  
        adapter\_health\_valid  
    ↓  
SafetyGateResult  
    ↓  
ExecutionRequest:  
        action\_type: DISPATCH\_ROBOT  
        target: RobotMission  
        external\_system: robot\_fleet\_manager\_site\_A  
    ↓  
External System:  
        Fleet Manager  
    ↓  
FeedbackEvent  
    ↓  
Audit  
    ↓  
World State Update

Hard boundary:

LEDO does not send low-level robot motion command.  
LEDO sends approved mission intent to external fleet manager.  
Fleet Manager performs physical robot execution.

---

# **10\. Implementation Dependency Map**

Implementation must follow this dependency map.

Master Architecture  
    ↓  
Layer Architecture  
    ↓  
Layer Stack Mapping  
    ↓  
Core Specifications  
    ↓  
Ontology Foundation  
    ↓  
Registry Base  
    ↓  
Ontology Registry  
    ↓  
Identity Registry  
    ↓  
Event Registry  
    ↓  
State Registry  
    ↓  
Snapshot Schema Registry  
    ↓  
Evidence Registry  
    ↓  
Agent Vocabulary Registry  
    ↓  
Model Adapter Registry  
    ↓  
Decision Registry  
    ↓  
Policy Registry  
    ↓  
Approval Registry  
    ↓  
External System Registry  
    ↓  
Runtime Validation  
    ↓  
Safety Gate  
    ↓  
Execution Request / External Control Integration  
    ↓  
Feedback / Audit / World State Update  
    ↓  
MVP Runtime Flow

---

# **11\. Pre-Code Architecture Checklist**

Before writing implementation code, the following checklist must pass.

1\. 00\_master\_architecture included?  
2\. 01\_layer\_architecture included?  
3\. Layer 12 fixed as Physical World Layer?  
4\. 02\_layer\_stack\_mapping aligned 1:1 with Layer Architecture?  
5\. 03\_core\_specifications included?  
6\. 04\_ontology\_foundation included?  
7\. 05\_domain\_ontology\_modules included?  
8\. 06\_registry\_specs included?  
9\. Actual registry folder list verified?  
10\. Safety Gate Rule included?  
11\. Execution Boundary Rule included?  
12\. Agent Boundary Rule included?  
13\. Architecture Invariants included?  
14\. Runtime hot path restrictions included?  
15\. External System as physical execution authority preserved?  
16\. Candidate ≠ Decision preserved?  
17\. Decision ≠ Approval preserved?  
18\. Approval ≠ Safety Gate pass preserved?  
19\. Safety Gate pass ≠ Physical Execution preserved?  
20\. ExecutionRequest ≠ PhysicalCommand preserved?  
21\. Runtime Validation separated from Safety Gate?  
22\. STOP\_WORK MVP flow defined?  
23\. DISPATCH\_ROBOT MVP flow defined?  
24\. Audit required across all lifecycle steps?  
25\. Feedback loop returns to World State Update?

If this checklist fails, code implementation must not begin.

---

# **12\. Final Implementation Rule**

No ontology,  
no meaning.

No registry,  
no operational validity.

No valid event,  
no state update.

No valid state,  
no trustworthy snapshot.

No valid snapshot,  
no trusted evidence.

No valid evidence,  
no trusted decision.

No policy pass,  
no approval route.

No approval,  
no approved action.

No runtime validation,  
no Safety Gate pass.

No Safety Gate pass,  
no ExecutionRequest.

No ExecutionRequest,  
no external execution.

No feedback,  
no closed loop.

No audit,  
no trust.

---

# **13\. Final Implementation Statement**

LEDO implementation must begin from the completed architecture, not from code impulse.

The correct order is:

Master Architecture  
→ Layer Architecture  
→ Layer Stack Mapping  
→ Core Specifications  
→ Ontology Foundation  
→ Domain Ontology Modules  
→ Registry Specifications  
→ Implementation Plan  
→ Runtime Validation  
→ MVP Runtime Flow  
→ Code

The implementation plan must preserve the existing LEDO architecture exactly.

It must not invent a new Layer 12\.

It must not collapse Safety Gate into Approval.

It must not collapse ExecutionRequest into PhysicalCommand.

It must not treat AI output as truth.

It must not treat External System as internal execution logic.

The final implementation direction is:

Meaning  
→ Current State  
→ Frozen Snapshot  
→ Trusted Evidence  
→ Controlled Decision  
→ Policy Permission  
→ Human Approval  
→ Runtime Validation  
→ Safety Gate  
→ Execution Request  
→ External Physical Execution  
→ Feedback  
→ Audit  
→ Updated World State

This is the LEDO implementation path.

# **Implementation Plan**

## **0\. 문서 상태**

문서명: LEDO Implementation Plan  
문서 유형: 구현 및 구동 계획서  
범위: 코드 작성 전 아키텍처-구현 정렬 문서  
상태: 검토용 초안  
핵심 원칙: 기존 아키텍처를 변경하지 않고 구현 순서로만 정렬한다.

이 문서는 LEDO 아키텍처를 실제로 어떻게 구현하고 구동할 것인지 정의한다.

이 문서는 새로운 아키텍처 문서가 아니다.

이 문서는 지금까지 완성한 LEDO 설계 자산을 실제 구현 순서로 정렬하는 구현 정렬 문서이다.

이 구현 계획서는 다음 기존 설계 자산을 반드시 포함하고 보존해야 한다.

00\_master\_architecture/  
01\_layer\_architecture/  
02\_layer\_stack\_mapping/  
03\_core\_specifications/  
04\_ontology\_foundation/  
05\_domain\_ontology\_modules/  
06\_registry\_specs/  
07\_implementation\_plan/  
08\_runtime\_validation/

이 계획서의 목적은 코드 구현이 시작되기 전에 아키텍처가 흐트러지는 것을 방지하는 것이다.

---

# **1\. 구현 계획의 임무**

이 문서의 임무는 완성된 LEDO 아키텍처를 안전하고 결정론적인 구현 계획으로 전환하는 것이다.

LEDO는 단순한 Agent 애플리케이션이 아니다.

LEDO는 의미, 상태, 증거, 정책, 승인, 런타임 검증, 안전 관문, 실행 요청, 외부 물리 실행, 피드백, 감사를 명확한 책임 경계로 분리하는 온톨로지 중심 Cyber-Physical AI 아키텍처이다.

따라서 구현도 동일한 책임 경계를 따라야 한다.

Architecture defines responsibility.  
Registry defines operational validity.  
Implementation must preserve both.

즉:

아키텍처는 책임을 정의한다.  
레지스트리는 운영 유효성을 정의한다.  
구현은 이 둘을 보존해야 한다.

---

# **2\. 기준 아키텍처 자산**

이 구현 계획서는 다음 완성된 LEDO 설계 자산을 기준으로 한다.

---

## **2.1 Master Architecture**

Repository 영역:

00\_master\_architecture/  
    01\_master\_architecture  
    00\_frist\_construction  
    readme.md

Master Architecture는 LEDO의 최상위 명제를 정의한다.

핵심 명제:

Ontology defines meaning.  
Evidence supports judgment.  
World State represents current condition.  
Agents generate candidates.  
Policy determines operational permission.  
Approval grants high-risk authority.  
Safety Gate validates execution readiness.  
External Systems perform physical execution.  
Audit preserves accountability.

한글 기준:

Ontology는 의미를 정의한다.  
Evidence는 판단 근거를 제공한다.  
World State는 현재 상태를 표현한다.  
Agent는 후보를 생성한다.  
Policy는 운영 허용 여부를 판단한다.  
Approval은 고위험 권한을 부여한다.  
Safety Gate는 실행 준비 상태를 검증한다.  
External System은 물리 실행을 수행한다.  
Audit은 책임 추적성을 보존한다.

구현상 의미:

구현되는 모든 객체는 자기 책임 경계를 보존해야 한다.

Ontology는 Policy가 아니다.  
Policy는 Approval이 아니다.  
Approval은 Safety Validation이 아니다.  
Safety Validation은 Physical Execution이 아니다.  
ExecutionRequest는 PhysicalCommand가 아니다.  
External System이 물리 실행을 수행한다.

---

## **2.2 Layer Architecture**

Repository 영역:

01\_layer\_architecture/

최종 LEDO Layer 구조:

Layer 0\. Observability / Audit / Trace Layer  
Layer 1\. Experience / Presentation Layer  
Layer 2\. API Gateway Layer  
Layer 3\. Governance / Policy / Security Layer  
Layer 4\. Core Ontology Kernel Layer  
Layer 5\. Knowledge & Semantic Memory Layer  
Layer 6\. Real-Time World State Layer  
Layer 7\. Distributed Domain Agent Layer  
Layer 8\. Decision Router / Escalation Layer  
Layer 9\. Approved Action / Safety Gate Layer  
Layer 10\. Unified Cyber-Physical Core Layer  
Layer 11\. Execution Request & External Control Integration Layer  
Layer 12\. Physical World Layer

이 Layer 구조는 고정이다.

구현은 Layer 순서와 Layer 책임을 보존해야 한다.

---

## **2.3 Layer Stack Mapping**

Repository 영역:

02\_layer\_stack\_mapping/

확인된 Stack Mapping 문서:

0\. "Observability / Audit / Trace" Stack Mapping  
1\. "Experience / Presentation" Stack Mapping  
2\. "API Gateway" Stack Mapping  
3\. "Governance / Policy / Security" Stack Mapping  
4\. "Core Ontology Kernel" Stack Mapping  
5\. "Knowledge & Semantic Memory" Stack Mapping  
6\. "Real-Time World State" Stack Mapping  
7\. "Distributed Domain Agent" Stack Mapping  
8\. "Decision Router / Escalation" Stack Mapping  
9\. "Approved Action / Safety Gate" Stack Mapping  
10\. "Unified Cyber-Physical Core" Stack Mapping  
11\. "Execution Request & External Control Integration" Stack Mapping  
12\. "Physical World" Stack Mapping

구현 규칙:

Layer Stack Mapping은 Layer Architecture와 1:1로 대응해야 한다.

따라서:

Layer 12 Stack Mapping \= Physical World Stack Mapping

---

## **2.4 Core Specifications**

Repository 영역:

03\_core\_specifications/

확인된 구조:

03\_core\_specifications/  
    00\_canonical\_object\_lifecycle/  
    01\_common\_schema\_dto/  
    02\_event\_type\_taxonomy/  
    03\_action\_type\_registry/  
    04\_state\_model\_registry/  
    05\_evidence\_model/  
    06\_ontology\_module\_boundary/  
    07\_decision\_approval\_matrix/  
    08\_policy\_governance\_model/  
    09\_execution\_adapter\_model/  
    10\_audit\_observability\_model/  
    README.md

구현상 의미:

03\_core\_specifications/는 Layer 10의 상세 specification 영역이다.

Layer 10은 별도의 root-level folder로 만들 필요가 없다.

Layer 10은 `03_core_specifications/` 전체를 통해 표현된다.

Layer 10은 다음 canonical operational lifecycle을 연결한다.

Event  
State Update  
Evidence  
ActionCandidate  
DecisionCase  
Approval  
ApprovedAction  
SafetyGateResult  
ExecutionRequest  
ExternalControlRequest  
FeedbackEvent  
AuditRecord

---

## **2.5 Ontology Foundation**

Repository 영역:

04\_ontology\_foundation/

확인된 구조:

04\_ontology\_foundation/  
    00\_ontology\_foundation\_report  
    01\_semantic\_web\_technology\_stack/  
    02\_upper\_ontology\_and\_standards/  
    03\_owl\_modeling\_principles/  
    04\_reasoning\_and\_constraint\_model/  
    05\_relationship\_and\_property\_design  
    06\_ontology\_governance\_and\_versioning/

구현상 의미:

04\_ontology\_foundation/은 Semantic Foundation을 정의한다.

이 영역은 다음을 담당한다.

OWL  
RDF  
RDFS  
SHACL  
SPARQL  
BFO  
SOSA / SSN  
SAREF  
PROV-O  
QUDT  
GeoSPARQL  
Reasoning  
Constraint Model  
Relationship and Property Design  
Ontology Governance  
Ontology Versioning

구현은 Ontology를 단순한 label list로 취급하면 안 된다.

Ontology는 의미 권위이다.

---

## **2.6 Domain Ontology Modules**

Repository 영역:

05\_domain\_ontology\_modules/

Domain Ontology Modules는 construction / industrial domain 확장 영역이다.

구현은 다음 domain object를 포함해야 한다.

Worker  
Equipment  
Robot / Humanoid  
Zone  
WorkZone  
HazardZone  
Task  
WorkProcess  
Hazard  
Risk  
Sensor  
Observation  
Event  
State  
Snapshot  
Evidence  
Decision  
Policy  
Approval  
Action  
ExternalSystem  
ExecutionRequest  
AuditRecord

구현 규칙:

Domain object는 ontology에 grounding되어야 한다.  
Domain event는 registry에 등록되어야 한다.  
Domain state는 registry에 등록되어야 한다.  
Domain snapshot은 schema를 가져야 한다.  
Domain evidence는 검증되어야 한다.  
Domain decision은 decision registry를 따라야 한다.  
Domain policy는 policy registry를 통과해야 한다.  
Domain approval은 approval registry를 통과해야 한다.  
Domain execution은 safety gate와 external system boundary를 통과해야 한다.

---

## **2.7 Registry Specifications**

Repository 영역:

06\_registry\_specs/

확인된 registry folder:

06\_registry\_specs/  
    agent\_vocabulary\_registry/  
    approval\_registry/  
    decision\_registry/  
    event\_registry/  
    evidence\_registry/  
    external\_system\_registry/  
    identity\_registry/  
    model\_adapter\_registry/  
    ontology\_registry/  
    policy\_registry/  
    snapshot\_schema\_registry/  
    state\_registry/

이것이 현재 repository에 존재하는 controlled registry specification이다.

구현은 이 실제 registry set을 보존해야 한다.

추가 registry 개념은 Core Specifications 또는 future expansion에서 존재할 수 있다.

하지만 실제로 `06_registry_specs/` 안에 만들어져 있지 않은 것을 이미 존재하는 것처럼 implementation plan에 넣으면 안 된다.

---

## **2.8 Implementation Plan**

Repository 영역:

07\_implementation\_plan/

이 문서는 이 영역에 속한다.

목적:

완성된 아키텍처를 구현 및 구동 순서로 전환한다.

이 folder는 아키텍처를 다시 정의하면 안 된다.

이 folder는 다음을 참조하고 정렬해야 한다.

Master Architecture  
Layer Architecture  
Layer Stack Mapping  
Core Specifications  
Ontology Foundation  
Domain Ontology Modules  
Registry Specifications  
Runtime Validation  
MVP Plan  
Pre-Code Checklist

---

## **2.9 Runtime Validation**

Repository 영역:

08\_runtime\_validation/

목적:

Safety Gate pass 이전의 execution-time validation을 정의한다.

Runtime Validation은 Safety Gate와 같지 않다.

Runtime Validation checks current validity.  
Safety Gate makes final pre-execution pass/block decision.

한글 기준:

Runtime Validation은 현재 조건이 유효한지 검증한다.  
Safety Gate는 최종 실행 전 pass/block 판단을 수행한다.

---

# **3\. 고정된 Architecture Invariants**

다음 불변 조건은 구현에서 반드시 강제되어야 한다.

Ontology is the semantic authority.  
AI output is candidate, not truth.  
Evidence is required for trusted decisions.  
Policy determines operational permission.  
Approval grants high-risk authority.  
Safety Gate validates execution readiness.  
ExecutionRequest is not a physical command.  
External Systems perform physical execution.  
Runtime hot path reads precomputed results only.  
Audit preserves traceability.

한글 기준:

Ontology는 의미 권위이다.  
AI output은 후보이지 truth가 아니다.  
신뢰 가능한 판단에는 Evidence가 필요하다.  
Policy는 운영 허용 여부를 판단한다.  
Approval은 고위험 권한을 부여한다.  
Safety Gate는 실행 준비 상태를 검증한다.  
ExecutionRequest는 PhysicalCommand가 아니다.  
External System이 물리 실행을 수행한다.  
Runtime hot path는 사전 계산된 결과만 읽는다.  
Audit은 추적 가능성을 보존한다.

이 불변 조건을 위반하는 구현은 LEDO가 아니다.

---

# **4\. 책임 경계 규칙**

## **4.1 Candidate Boundary**

Candidate ≠ Decision

Agent 또는 Model Output이 생성할 수 있는 것:

Intent Interpretation  
Situation Summary  
Risk Interpretation  
MappingProposal  
EvidenceSummary  
ActionCandidate  
EscalationCase  
DecisionCase draft  
PolicyImpactSuggestion  
Explanation

Agent 또는 Model Output이 직접 생성하면 안 되는 것:

Evidence  
Policy Decision  
Approval  
Safety Gate Decision  
Final ExecutionRequest  
Final ExternalControlRequest  
Physical Command

---

## **4.2 Decision Boundary**

Decision ≠ Approval

Decision은 evidence, risk, policy, route를 기반으로 무엇이 일어나야 하는지를 평가한다.

Decision은 권한을 부여하지 않는다.

---

## **4.3 Policy Boundary**

Policy pass ≠ Approval pass

Policy는 제안된 action이 조건상 허용되는지 판단한다.

Policy는 human authority를 부여하지 않는다.

---

## **4.4 Approval Boundary**

Approval ≠ Safety Gate pass

Approval은 권한을 부여한다.

Approval은 execution-time physical condition이 여전히 안전하다는 것을 증명하지 않는다.

---

## **4.5 Safety Gate Boundary**

Safety Gate pass ≠ Physical Execution

Safety Gate는 readiness를 검증한다.

Safety Gate는 물리 실행을 수행하지 않는다.

---

## **4.6 Execution Boundary**

ExecutionRequest ≠ PhysicalCommand  
ExternalControlRequest ≠ PhysicalCommand  
External System \= Physical Execution Authority

LEDO는 bounded, approved, validated execution intent를 보낸다.

실제 물리 실행은 External System이 수행한다.

---

# **5\. End-to-End Architecture Flow**

LEDO의 canonical flow는 다음과 같이 고정된다.

Physical World  
→ Real-Time World State  
→ Knowledge / Evidence Binding  
→ Distributed Domain Agents  
→ ActionCandidate  
→ Semantic Validation  
→ Evidence Check  
→ Policy Check  
→ Decision Router  
→ Approval  
→ Safety Gate  
→ ExecutionRequest  
→ External Control Integration  
→ External System  
→ Physical World  
→ Feedback  
→ Audit  
→ World State Update

구현은 이 흐름을 보존해야 한다.

---

# **6\. Source of Truth Boundaries**

구현은 다음 Source of Truth 경계를 보존해야 한다.

Semantic Meaning  
    → Ontology

Class / Property / Axiom  
    → Ontology Foundation

Current Runtime State  
    → Real-Time World State

Historical Evidence  
    → Evidence Store / Audit

Operational Permission  
    → Policy

High-Risk Authority  
    → Approval

Execution Readiness  
    → Safety Gate Snapshot

Physical Execution  
    → External System

Identity Resolution  
    → Canonical Identity / Registry

User View  
    → Presentation Layer

AI Interpretation  
    → Agent Output as Candidate

---

# **7\. 구현 전략**

## **7.1 전략**

구현은 stable meaning에서 physical execution boundary 방향으로 진행되어야 한다.

올바른 구현 순서:

Meaning  
→ Registry  
→ Event  
→ State  
→ Snapshot  
→ Evidence  
→ Decision  
→ Policy  
→ Approval  
→ Runtime Validation  
→ Safety Gate  
→ ExecutionRequest  
→ External Integration  
→ Feedback  
→ Audit

잘못된 구현 순서:

Agent first  
UI first  
LLM first  
Execution first  
External system first

이런 순서는 operational validity보다 behavior를 먼저 만들기 때문에 위험하다.

---

## **7.2 구현 철학**

Implement contracts before behavior.  
Implement validation before execution.  
Implement registry before runtime use.  
Implement state before snapshot.  
Implement snapshot before evidence.  
Implement evidence before decision.  
Implement policy before approval.  
Implement runtime validation before Safety Gate.  
Implement Safety Gate before ExecutionRequest.  
Implement audit across all lifecycle stages.

한글 기준:

행동보다 계약을 먼저 구현한다.  
실행보다 검증을 먼저 구현한다.  
runtime 사용보다 registry를 먼저 구현한다.  
snapshot보다 state를 먼저 구현한다.  
evidence보다 snapshot을 먼저 구현한다.  
decision보다 evidence를 먼저 구현한다.  
approval보다 policy를 먼저 구현한다.  
Safety Gate보다 runtime validation을 먼저 구현한다.  
ExecutionRequest보다 Safety Gate를 먼저 구현한다.  
모든 lifecycle 단계에 audit을 붙인다.

---

# **8\. 구현 단계**

---

## **Phase 0\. Architecture Freeze and Index Verification**

### **목표**

코드 작성 전 기존 아키텍처 자산을 고정한다.

### **입력**

00\_master\_architecture/  
01\_layer\_architecture/  
02\_layer\_stack\_mapping/  
03\_core\_specifications/  
04\_ontology\_foundation/  
05\_domain\_ontology\_modules/  
06\_registry\_specs/

### **작업**

Layer 0-12 이름 검증  
Layer 12 \= Physical World Layer 검증  
Layer Stack Mapping이 Layer Architecture와 1:1인지 검증  
Core Specifications folder list 검증  
Ontology Foundation folder list 검증  
Registry Specs folder list 검증  
End-to-End Architecture Flow 검증  
Safety Gate Rule 검증  
Execution Boundary Rule 검증  
Agent Boundary Rule 검증  
Architecture Invariants 검증

### **산출물**

architecture\_freeze\_checklist.md  
repository\_index.md  
implementation\_dependency\_map.md

### **완료 기준**

Layer mismatch 없음  
누락된 core specification section 없음  
implementation plan에서 누락된 registry folder 없음  
허가되지 않은 신규 layer 없음  
책임 경계 붕괴 없음

---

## **Phase 1\. Common Contract Foundation**

### **목표**

모든 registry와 core object가 공유할 공통 구현 계약을 만든다.

### **구현 영역**

03\_core\_specifications/01\_common\_schema\_dto/

### **Core Objects**

BaseEntity  
BaseRegistryEntry  
BaseCoreObject  
BaseEvent  
BaseState  
BaseSnapshot  
BaseEvidence  
BaseDecisionCase  
BasePolicyEvaluation  
BaseApproval  
BaseRuntimeValidation  
BaseSafetyGateResult  
BaseExecutionRequest  
BaseAuditRecord

### **공통 필드**

id  
canonical\_name  
semantic\_iri  
version  
status  
created\_at  
updated\_at  
trace\_id  
correlation\_id  
source\_ref  
owner\_module  
owner\_team  
audit\_refs  
dependency\_refs

### **완료 기준**

모든 core object가 ID, version, status, timestamp, trace, audit 구조를 일관되게 공유한다.

---

## **Phase 2\. Semantic Foundation Implementation**

### **목표**

운영 runtime behavior보다 먼저 semantic foundation을 구현한다.

### **구현 영역**

04\_ontology\_foundation/  
06\_registry\_specs/ontology\_registry/

### **작업**

ontology module reference model 구현  
namespace 및 IRI validation 구현  
ontology version validation 구현  
class/property semantic reference validation 구현  
upper ontology alignment reference 구현  
reasoning profile metadata 구현  
SHACL shape reference metadata 구현  
ontology governance 및 versioning rule 구현

### **반드시 보존할 것**

Ontology defines meaning.  
Ontology is not World State.  
Ontology is not Evidence.  
Ontology is not Policy.  
Ontology is not Approval.  
Ontology is not Safety Gate.  
Ontology is not PhysicalCommand.

### **완료 기준**

등록되지 않은 semantic IRI 거부  
deprecated ontology module 거부  
지원되지 않는 ontology version 거부  
class/property reference는 active ontology reference로 resolve되어야 함

---

## **Phase 3\. Registry Base System**

### **목표**

개별 registry 구현 전에 일관된 registry system을 만든다.

### **구현 영역**

06\_registry\_specs/

### **공통 Registry Interface**

load()  
get()  
exists()  
validate()  
resolve()  
is\_active()  
check\_version()  
check\_dependency()  
check\_status()  
check\_boundary()

### **공통 Registry Status**

draft  
active  
deprecated  
migration\_required  
retired  
blocked

### **필수 구성요소**

RegistryLoader  
RegistryStore  
RegistryResolver  
RegistryValidator  
RegistryDependencyChecker  
RegistryMigrationChecker  
RegistryAuditHook

### **완료 기준**

모든 registry entry가 동일한 base interface를 통해 load, resolve, validate, version-check, dependency-check될 수 있다.

---

## **Phase 4\. Identity and Access Foundation**

### **목표**

Policy, Approval, Action 이전에 identity와 access boundary를 구현한다.

### **구현 영역**

06\_registry\_specs/identity\_registry/

### **작업**

actor identity 정의  
service identity 정의  
agent identity 정의  
role 정의  
scope 정의  
certification 정의  
identity status 정의  
identity validity check 정의

### **관련 Layer**

Layer 3\. Governance / Policy / Security Layer

### **완료 기준**

등록된 identity 없이 어떤 actor도 propose, approve, validate, execute할 수 없다.

---

## **Phase 5\. Event Registry Implementation**

### **목표**

State update 이전에 valid event type을 구현한다.

### **구현 영역**

06\_registry\_specs/event\_registry/  
03\_core\_specifications/02\_event\_type\_taxonomy/

### **작업**

CoreEvent schema 정의  
event type taxonomy 정의  
event producer boundary 정의  
event payload schema reference 정의  
event source reference 정의  
event-to-state update eligibility 정의  
event audit requirement 정의

### **완료 기준**

등록되지 않은 event type 거부  
유효하지 않은 event producer 거부  
payload schema 없는 event 거부  
Valid Event가 자동으로 State를 update하지 않음

---

## **Phase 6\. State Registry Implementation**

### **목표**

공식 current state contract를 구현한다.

### **구현 영역**

06\_registry\_specs/state\_registry/  
03\_core\_specifications/04\_state\_model\_registry/

### **작업**

State Type 정의  
State Key 정의  
State Owner 정의  
State Source 정의  
State Update Rule 정의  
State Transition Rule 정의  
State Freshness Rule 정의  
State Conflict Rule 정의  
State Storage Reference 정의  
State Snapshot Binding 정의

### **반드시 보존할 것**

State represents what is currently true.  
State is not Event.  
State is not Snapshot.  
State is not Evidence.  
State is mutable only through controlled update rules.

### **완료 기준**

등록되지 않은 State 거부  
owner 없는 State 거부  
rule 없는 State update 거부  
stale State는 Safety Gate에서 거부  
conflicting safety State는 block 또는 review trigger

---

## **Phase 7\. Snapshot Schema Registry Implementation**

### **목표**

Immutable state-freezing contract를 구현한다.

### **구현 영역**

06\_registry\_specs/snapshot\_schema\_registry/

### **작업**

Snapshot Type 정의  
Snapshot Schema 정의  
Snapshot Metadata 정의  
Snapshot Freshness 정의  
Snapshot Immutability 정의  
Snapshot Lineage 정의  
Snapshot Provenance 정의  
Snapshot Serialization 정의  
Snapshot Safety Gate Usability 정의  
Snapshot Hot Path Eligibility 정의

### **반드시 보존할 것**

Snapshot freezes State at a specific time.  
Snapshot is immutable.  
Snapshot is not Event.  
Snapshot is not Evidence itself.  
Approval-time Snapshot is not Execution-time Snapshot.

### **완료 기준**

등록되지 않은 Snapshot Schema 거부  
mutable Snapshot 거부  
stale Snapshot은 Safety Gate에서 거부  
safety\_gate\_usable=false인 snapshot\_schema는 Safety Gate에서 사용 불가

---

## **Phase 8\. Evidence Registry Implementation**

### **목표**

신뢰 가능한 판단 근거를 구현한다.

### **구현 영역**

06\_registry\_specs/evidence\_registry/  
03\_core\_specifications/05\_evidence\_model/

### **작업**

Evidence Type 정의  
Evidence Source 정의  
Evidence Quality 정의  
Evidence Freshness 정의  
Evidence Lineage 정의  
Evidence Bundle 정의  
Evidence-to-Decision dependency 정의

### **반드시 보존할 것**

Evidence supports judgment.  
Evidence is not Decision.  
Snapshot does not automatically become Evidence.  
State does not automatically become Evidence.

### **완료 기준**

등록되지 않은 Evidence Type 거부  
lineage 없는 Evidence 거부  
quality threshold 미달 Evidence 거부  
safety-critical decision에서 stale Evidence 거부

---

## **Phase 9\. Agent Vocabulary Registry Implementation**

### **목표**

Agent가 말하고 생성하고 요청할 수 있는 범위를 제한한다.

### **구현 영역**

06\_registry\_specs/agent\_vocabulary\_registry/

### **작업**

allowed agent vocabulary 정의  
allowed candidate type 정의  
prohibited output type 정의  
ontology grounding requirement 정의  
policy boundary 정의  
action candidate boundary 정의

### **반드시 보존할 것**

Agent output is candidate, not truth.  
Agent must not create final Evidence.  
Agent must not create Policy Decision.  
Agent must not create Approval.  
Agent must not create Safety Gate Decision.  
Agent must not create Final ExecutionRequest.  
Agent must not create Physical Command.

### **완료 기준**

허용 vocabulary 밖 Agent output 거부  
Agent-generated PhysicalCommand 거부  
Agent-generated final approval 또는 execution 거부

---

## **Phase 10\. Model Adapter Registry Implementation**

### **목표**

Model 호출과 output boundary를 제한한다.

### **구현 영역**

06\_registry\_specs/model\_adapter\_registry/

### **작업**

model adapter type 정의  
runtime provider 정의  
input schema 정의  
output schema 정의  
allowed task 정의  
prohibited output 정의  
guard requirement 정의  
privacy boundary 정의  
model output validation 정의

### **반드시 보존할 것**

Model output is not Decision.  
Model output is not Approval.  
Model output is not Safety Gate pass.  
Model output is not ExecutionRequest.  
Model output is not PhysicalCommand.

### **완료 기준**

등록되지 않은 model adapter 호출 불가  
Model output은 schema guard 통과 필요  
Model output은 ontology guard 통과 필요  
Model output은 downstream 사용 전 policy boundary 통과 필요

---

## **Phase 11\. Decision Registry Implementation**

### **목표**

Controlled judgment flow를 구현한다.

### **구현 영역**

06\_registry\_specs/decision\_registry/  
03\_core\_specifications/07\_decision\_approval\_matrix/

### **작업**

Decision Rule 정의  
DecisionCase 정의  
required Evidence 정의  
required State 또는 Snapshot 정의  
risk classification 정의  
escalation route 정의  
policy dependency 정의  
approval dependency 정의

### **반드시 보존할 것**

Decision evaluates what should happen.  
Decision is not Approval.  
Decision is not ExecutionRequest.

### **완료 기준**

required Evidence 없는 Decision 거부  
Decision은 Policy를 우회할 수 없음  
Decision은 ExecutionRequest를 생성할 수 없음  
Decision route는 audit 가능해야 함

---

## **Phase 12\. Policy Registry Implementation**

### **목표**

Operational permission을 구현한다.

### **구현 영역**

06\_registry\_specs/policy\_registry/  
03\_core\_specifications/08\_policy\_governance\_model/

### **작업**

Policy Type 정의  
Policy Condition 정의  
Policy Constraint 정의  
Policy Effect 정의  
Policy Priority 정의  
Policy Scope 정의  
Policy Engine Reference 정의  
emergency override rule 정의  
fallback 및 escalation rule 정의

### **반드시 보존할 것**

Policy determines operational permission.  
Policy pass is not Approval pass.  
Policy evaluation failure must not silently become allow.

### **완료 기준**

등록되지 않은 Policy 거부  
inactive Policy 거부  
Policy failure는 fail-secure  
Policy conflict는 visible and auditable

---

## **Phase 13\. Approval Registry Implementation**

### **목표**

High-risk authority와 approval boundary를 구현한다.

### **구현 영역**

06\_registry\_specs/approval\_registry/  
03\_core\_specifications/07\_decision\_approval\_matrix/

### **작업**

Approval Type 정의  
Approver Role 정의  
Approval Scope 정의  
Approval Condition 정의  
Approval Expiry 정의  
Approval Evidence Requirement 정의  
Approval Audit Requirement 정의

### **반드시 보존할 것**

Approval grants authority.  
Approval does not validate runtime safety.  
Approval does not create PhysicalCommand.  
Approval-time Snapshot is not Execution-time Snapshot.

### **완료 기준**

권한 없는 approver 거부  
expired approval 거부  
policy pass 없는 approval 거부  
Approval은 Safety Gate를 우회할 수 없음

---

## **Phase 14\. External System Registry Implementation**

### **목표**

External physical execution boundary를 구현한다.

### **구현 영역**

06\_registry\_specs/external\_system\_registry/  
03\_core\_specifications/09\_execution\_adapter\_model/

### **작업**

External System 정의  
supported action intent 정의  
supported protocol 정의  
health check requirement 정의  
feedback expectation 정의  
physical execution boundary 정의  
safety-rated controller boundary 정의

### **반드시 보존할 것**

External System performs physical execution.  
LEDO does not perform physical execution directly.  
External System compatibility pass is not Safety Gate pass.

### **완료 기준**

등록되지 않은 External System은 ExecutionRequest 수신 불가  
health validation 없는 External System은 block  
External System을 내부 LEDO authority로 취급하면 안 됨

---

## **Phase 15\. Runtime Validation Design and Implementation**

### **목표**

Safety Gate decision 이전에 current execution-time validity를 검증한다.

### **구현 영역**

08\_runtime\_validation/

### **작업**

runtime validation concept 정의  
runtime validation rule structure 정의  
state freshness validation 정의  
snapshot freshness validation 정의  
evidence validity validation 정의  
approval validity validation 정의  
policy revalidation 정의  
external system readiness check 정의  
adapter health check 정의  
capability availability check 정의  
conflict state check 정의

### **반드시 보존할 것**

Runtime Validation is not Approval.  
Runtime Validation is not Safety Gate itself.  
Runtime Validation checks whether current conditions are still valid.  
Safety Gate uses runtime validation result to pass or block.

### **완료 기준**

Stale State는 execution path block  
Stale Snapshot은 execution path block  
Expired Approval은 execution path block  
Invalid Policy는 execution path block  
Unhealthy External System은 execution path block  
Unhealthy Adapter는 execution path block

---

## **Phase 16\. Safety Gate Implementation**

### **목표**

결정론적 final execution readiness validation을 구현한다.

### **구현 영역**

Layer 9\. Approved Action / Safety Gate Layer  
08\_runtime\_validation/  
03\_core\_specifications/

### **Safety Gate Rule**

Safety Gate는 승인된 action의 execution readiness를 검증한다.

Safety Gate는 approval을 부여하지 않는다.

Approval이 권한을 부여한다.

Safety Gate는 실행 준비 상태를 검증한다.

### **Runtime Hot Path에서 하면 안 되는 것**

OWL Reasoning  
Full SHACL Validation  
SPARQL Query  
Graph DB Network Call  
LLM / SLM Call  
External API Call  
Disk I/O  
Unbounded Computation

### **Runtime Hot Path에서 읽을 수 있는 것**

Materialized Safety Snapshot  
Precomputed validation result  
Immutable runtime validation summary  
Fixed layout safety data

### **완료 기준**

ApprovedAction 없이 Safety Gate pass 불가  
fresh runtime validation 없이 Safety Gate pass 불가  
LLM / SLM output으로 Safety Gate pass 불가  
stale State로 Safety Gate pass 불가  
stale Snapshot으로 Safety Gate pass 불가  
Safety Gate pass 없이 ExecutionRequest 생성 불가

---

## **Phase 17\. Execution Request and External Control Integration**

### **목표**

승인되고 검증된 intent를 외부 시스템용 bounded request로 전환한다.

### **구현 영역**

Layer 11\. Execution Request & External Control Integration Layer  
03\_core\_specifications/09\_execution\_adapter\_model/  
06\_registry\_specs/external\_system\_registry/

### **LEDO가 정의하는 것**

intent  
target  
constraints  
approval reference  
evidence reference  
policy reference  
safety validation result  
trace id  
idempotency key  
expected feedback

### **External System이 수행하는 것**

Robot Middleware  
Fleet Manager  
PLC  
SCADA  
Access Control System  
Equipment Controller  
Site Operation System  
Safety-rated Controller

### **반드시 보존할 것**

ExecutionRequest is not PhysicalCommand.  
ExternalControlRequest is not PhysicalCommand.  
External System performs physical execution.

### **완료 기준**

ExecutionRequest는 Safety Gate pass 이후에만 생성 가능  
ExecutionRequest는 approval reference 포함 필요  
ExecutionRequest는 evidence reference 포함 필요  
ExecutionRequest는 policy reference 포함 필요  
ExecutionRequest는 safety validation result 포함 필요  
ExecutionRequest는 trace id와 idempotency key 포함 필요

---

## **Phase 18\. Feedback and World State Update**

### **목표**

Cyber-Physical loop를 닫는다.

### **흐름**

ExecutionRequest  
→ External System  
→ Physical World  
→ ExecutionResult  
→ FeedbackEvent  
→ Audit  
→ World State Update

### **작업**

ExecutionResult schema 정의  
FeedbackEvent schema 정의  
feedback-to-state update rule 정의  
success / failure / timeout handling 정의  
compensating action request 정의  
audit trace 정의

### **완료 기준**

모든 ExecutionRequest는 feedback을 기대해야 함  
missing feedback은 감지되어야 함  
ExecutionResult는 audit을 update해야 함  
ExecutionResult는 valid event-state rule을 통해서만 world state를 update할 수 있음

---

## **Phase 19\. Observability and Audit Implementation**

### **목표**

모든 lifecycle step을 trace 가능하게 만든다.

### **구현 영역**

Layer 0\. Observability / Audit / Trace Layer  
03\_core\_specifications/10\_audit\_observability\_model/

### **필수 Audit 대상**

event\_received  
event\_validated  
state\_updated  
snapshot\_created  
evidence\_created  
decision\_created  
policy\_evaluated  
approval\_requested  
approval\_granted  
approval\_rejected  
runtime\_validation\_executed  
safety\_gate\_passed  
safety\_gate\_blocked  
execution\_request\_created  
external\_control\_request\_sent  
execution\_result\_received  
feedback\_event\_created  
world\_state\_updated  
registry\_changed  
ontology\_changed

### **완료 기준**

trace\_id 없는 lifecycle step 없음  
audit 없는 high-risk action 없음  
audit 없는 Safety Gate result 없음  
audit 없는 ExecutionRequest 없음

---

# **9\. MVP 구현 범위**

MVP는 모든 것을 구현하는 것이 아니다.

MVP는 LEDO의 end-to-end lifecycle이 작동한다는 것을 증명해야 한다.

MVP canonical flow:

Event  
→ State  
→ Snapshot  
→ Evidence  
→ Decision  
→ Policy  
→ Approval  
→ Runtime Validation  
→ Safety Gate  
→ ExecutionRequest  
→ External System  
→ Feedback  
→ Audit  
→ World State Update

MVP는 두 개의 flow를 포함해야 한다.

MVP Flow A: STOP\_WORK  
MVP Flow B: DISPATCH\_ROBOT

---

## **9.1 MVP Flow A: STOP\_WORK**

목적:

Safety-critical decision, policy, approval, runtime validation, Safety Gate를 검증한다.

흐름:

HazardDetected  
WorkerLocationUpdated  
ZoneStatusChanged  
    ↓  
hazard\_state  
worker\_location\_state  
zone\_status\_state  
    ↓  
hazard\_detection\_snapshot  
worker\_location\_snapshot  
zone\_status\_snapshot  
    ↓  
EvidenceBundle  
    ↓  
DecisionCase: stop\_work\_safety\_risk\_v1  
    ↓  
PolicyEvaluation: stop\_work\_policy\_v1  
    ↓  
ApprovalRequest: stop\_work\_safety\_supervisor\_v1  
    ↓  
ApprovedAction: STOP\_WORK  
    ↓  
RuntimeValidation:  
        hazard\_still\_present  
        worker\_location\_fresh  
        zone\_status\_valid  
    ↓  
SafetyGateResult  
    ↓  
ExecutionRequest:  
        action\_type: STOP\_WORK  
        target: WorkZone  
        external\_system: site\_operation\_system or notification system  
    ↓  
FeedbackEvent  
    ↓  
Audit  
    ↓  
World State Update

강한 경계:

STOP\_WORK ExecutionRequest는 PhysicalCommand가 아니다.  
External System이 실제 site control, notification, work stop workflow를 수행한다.

---

## **9.2 MVP Flow B: DISPATCH\_ROBOT**

목적:

Cyber-physical execution boundary와 external fleet manager integration을 검증한다.

흐름:

RobotStatusUpdated  
WorkerLocationUpdated  
ZoneStatusChanged  
ExternalSystemStatusUpdated  
    ↓  
robot\_status\_state  
worker\_location\_state  
zone\_status\_state  
external\_system\_health\_state  
adapter\_health\_state  
    ↓  
robot\_availability\_snapshot  
worker\_location\_snapshot  
zone\_status\_snapshot  
external\_system\_health\_snapshot  
adapter\_health\_snapshot  
    ↓  
EvidenceBundle  
    ↓  
DecisionCase: dispatch\_robot\_v1  
    ↓  
PolicyEvaluation: robot\_dispatch\_policy\_v1  
    ↓  
ApprovalRequest: dispatch\_robot\_supervisor\_v1  
    ↓  
ApprovedAction: DISPATCH\_ROBOT  
    ↓  
RuntimeValidation:  
        robot\_available  
        worker\_not\_in\_robot\_path  
        zone\_accessible  
        external\_system\_reachable  
        adapter\_health\_valid  
    ↓  
SafetyGateResult  
    ↓  
ExecutionRequest:  
        action\_type: DISPATCH\_ROBOT  
        target: RobotMission  
        external\_system: robot\_fleet\_manager\_site\_A  
    ↓  
External System:  
        Fleet Manager  
    ↓  
FeedbackEvent  
    ↓  
Audit  
    ↓  
World State Update

강한 경계:

LEDO는 low-level robot motion command를 보내지 않는다.  
LEDO는 approved mission intent를 external fleet manager에 보낸다.  
Fleet Manager가 물리 robot execution을 수행한다.

---

# **10\. 구현 Dependency Map**

구현은 다음 dependency map을 따라야 한다.

Master Architecture  
    ↓  
Layer Architecture  
    ↓  
Layer Stack Mapping  
    ↓  
Core Specifications  
    ↓  
Ontology Foundation  
    ↓  
Registry Base  
    ↓  
Ontology Registry  
    ↓  
Identity Registry  
    ↓  
Event Registry  
    ↓  
State Registry  
    ↓  
Snapshot Schema Registry  
    ↓  
Evidence Registry  
    ↓  
Agent Vocabulary Registry  
    ↓  
Model Adapter Registry  
    ↓  
Decision Registry  
    ↓  
Policy Registry  
    ↓  
Approval Registry  
    ↓  
External System Registry  
    ↓  
Runtime Validation  
    ↓  
Safety Gate  
    ↓  
Execution Request / External Control Integration  
    ↓  
Feedback / Audit / World State Update  
    ↓  
MVP Runtime Flow

---

# **11\. Pre-Code Architecture Checklist**

코드를 작성하기 전에 다음 checklist를 통과해야 한다.

1\. 00\_master\_architecture 포함되었는가?  
2\. 01\_layer\_architecture 포함되었는가?  
3\. Layer 12가 Physical World Layer로 고정되었는가?  
4\. 02\_layer\_stack\_mapping이 Layer Architecture와 1:1로 정렬되었는가?  
5\. 03\_core\_specifications 포함되었는가?  
6\. 04\_ontology\_foundation 포함되었는가?  
7\. 05\_domain\_ontology\_modules 포함되었는가?  
8\. 06\_registry\_specs 포함되었는가?  
9\. 실제 registry folder list가 검증되었는가?  
10\. Safety Gate Rule이 포함되었는가?  
11\. Execution Boundary Rule이 포함되었는가?  
12\. Agent Boundary Rule이 포함되었는가?  
13\. Architecture Invariants가 포함되었는가?  
14\. Runtime hot path restrictions가 포함되었는가?  
15\. External System이 physical execution authority라는 원칙이 보존되었는가?  
16\. Candidate ≠ Decision이 보존되었는가?  
17\. Decision ≠ Approval이 보존되었는가?  
18\. Approval ≠ Safety Gate pass가 보존되었는가?  
19\. Safety Gate pass ≠ Physical Execution이 보존되었는가?  
20\. ExecutionRequest ≠ PhysicalCommand가 보존되었는가?  
21\. Runtime Validation이 Safety Gate와 분리되었는가?  
22\. STOP\_WORK MVP flow가 정의되었는가?  
23\. DISPATCH\_ROBOT MVP flow가 정의되었는가?  
24\. 모든 lifecycle step에 audit이 요구되는가?  
25\. Feedback loop가 World State Update로 돌아오는가?

이 checklist가 실패하면 코드 구현을 시작하면 안 된다.

---

# **12\. 최종 구현 규칙**

No ontology,  
no meaning.

No registry,  
no operational validity.

No valid event,  
no state update.

No valid state,  
no trustworthy snapshot.

No valid snapshot,  
no trusted evidence.

No valid evidence,  
no trusted decision.

No policy pass,  
no approval route.

No approval,  
no approved action.

No runtime validation,  
no Safety Gate pass.

No Safety Gate pass,  
no ExecutionRequest.

No ExecutionRequest,  
no external execution.

No feedback,  
no closed loop.

No audit,  
no trust.

한글 기준:

Ontology가 없으면 의미도 없다.

Registry가 없으면 운영 유효성도 없다.

유효한 Event가 없으면 State Update도 없다.

유효한 State가 없으면 신뢰 가능한 Snapshot도 없다.

유효한 Snapshot이 없으면 신뢰 가능한 Evidence도 없다.

유효한 Evidence가 없으면 신뢰 가능한 Decision도 없다.

Policy Pass가 없으면 Approval Route도 없다.

Approval이 없으면 ApprovedAction도 없다.

Runtime Validation이 없으면 Safety Gate Pass도 없다.

Safety Gate Pass가 없으면 ExecutionRequest도 없다.

ExecutionRequest가 없으면 External Execution도 없다.

Feedback이 없으면 Closed Loop도 없다.

Audit이 없으면 Trust도 없다.

---

# **13\. 최종 구현 선언**

LEDO 구현은 code impulse에서 시작하면 안 된다.

LEDO 구현은 완성된 아키텍처에서 시작해야 한다.

올바른 순서는 다음이다.

Master Architecture  
→ Layer Architecture  
→ Layer Stack Mapping  
→ Core Specifications  
→ Ontology Foundation  
→ Domain Ontology Modules  
→ Registry Specifications  
→ Implementation Plan  
→ Runtime Validation  
→ MVP Runtime Flow  
→ Code

Implementation Plan은 기존 LEDO 아키텍처를 정확히 보존해야 한다.

새로운 Layer 12를 만들면 안 된다.

Safety Gate를 Approval에 합치면 안 된다.

ExecutionRequest를 PhysicalCommand로 합치면 안 된다.

AI output을 truth로 취급하면 안 된다.

External System을 내부 execution logic으로 취급하면 안 된다.

최종 구현 방향은 다음이다.

Meaning  
→ Current State  
→ Frozen Snapshot  
→ Trusted Evidence  
→ Controlled Decision  
→ Policy Permission  
→ Human Approval  
→ Runtime Validation  
→ Safety Gate  
→ Execution Request  
→ External Physical Execution  
→ Feedback  
→ Audit  
→ Updated World State

이것이 LEDO 구현 경로이다.

