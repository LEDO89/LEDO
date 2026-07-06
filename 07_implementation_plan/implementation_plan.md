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
Reference Flow Scope  
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

# **9\. Reference Flow Scope**

**Non-normative note:** `STOP_WORK` and `DISPATCH_ROBOT` below (and the event/state/evidence names used in their flows) are reference fixtures, not approved domain content. They are used because they recur consistently across this document and several `06_registry_specs/*` documents, which reduces the risk of introducing new placeholder names. No document declares them normative; see `06_registry_specs/action_registry/action_registry.md` Sections 11–12 for the corresponding registry-level non-normative marking.

This scope must not implement everything.

This scope must prove that LEDO's end-to-end lifecycle works.

Canonical flow for the first formal reference implementation:

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

This scope includes two reference flows:

Reference Flow A: STOP\_WORK  
Reference Flow B: DISPATCH\_ROBOT

---

## **9.1 Reference Flow A: STOP\_WORK**

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

## **9.2 Reference Flow B: DISPATCH\_ROBOT**

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
First Formal Reference Flow

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
22\. STOP\_WORK reference flow defined?  
23\. DISPATCH\_ROBOT reference flow defined?  
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
→ First Formal Reference Flow  
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

