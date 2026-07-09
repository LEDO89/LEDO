# **Ontology Centric “Approved Action / Safety Gate” Stack Mapping**

## **Layer 9\. Approved Action / Safety Gate Layer**

─ Core Position  
└── Approved Action / Safety Gate is the final pre-execution readiness layer after approval has produced an ApprovedAction  
└── It determines whether an ApprovedAction with RuntimeValidationResult can receive a SafetyGatePass or SafetyGateBlock  
└── It consumes ontology-defined action type, constraints, policy, capability, human approval, authorization, emergency rules, current operational state, and Runtime Validation results  
└── It is the last safety boundary before the Unified Cyber-Physical Core creates an ExecutionRequest  
└── It does not generate action candidates  
└── It does not classify routing tiers  
└── It does not directly execute physical commands  
└── It does not control robots, PLCs, SCADA, equipment, or fleet managers  
└── It passes or blocks execution readiness; it does not grant approval or create physical commands

---

## **Core Role**

└── Validate whether an ApprovedAction is eligible to receive a SafetyGatePass  
└── Ensure only ontology-defined Action Types enter the execution lifecycle  
└── Validate action target, capability, constraints, policy, current state, approval, authorization, and emergency rules  
└── Block unsafe, unauthorized, stale, ungrounded, or insufficiently evidenced ApprovedActions  
└── Issue SafetyGatePass or SafetyGateBlock based on RuntimeValidationResult  
└── Attach validation result, evidence, approval record, policy decision, state snapshot, and trace context  
└── Provide a fail-secure boundary before execution requests are created  
└── Preserve audit records for every approved, rejected, blocked, or escalated candidate

---

## **Core Technologies**

└── Constraint Validation  
└── Policy Validation  
└── Capability Validation  
└── Human Approval Validation  
└── SHACL Validation  
└── OPA / Rego  
└── Rule Engine  
└── Safety Interlock  
└── Approval Workflow  
└── State Machine  
└── Permission Engine  
└── Safety Policy Engine  
└── Freshness Validator  
└── Evidence Validator  
└── Action Registry  
└── Capability Registry  
└── Approval Matrix  
└── Validation Report DTO

---

## **Optional Technologies**

└── pySHACL for initial target validation  
└── Apache Jena SHACL for shared validation  
└── GraphDB / Stardog validation for production-scale RDF validation  
└── DMN for approval requirement rules  
└── BPMN for approval workflow visualization  
└── Temporal / Camunda for complex approval workflows  
└── Formal Methods for high-criticality safety constraints  
└── Runtime Safety Monitor  
└── Digital Twin Simulation Check optional  
└── Scenario Test Engine  
└── Policy Simulation Engine  
└── Human-in-the-loop Review Queue  
└── Emergency Safety Rule Table

---

## **Input Stack**

└── ActionCandidate  
└── DecisionCase  
└── RoutingDecision  
└── HumanApprovalDecision  
└── PolicyDecision  
└── Current World State Snapshot  
└── EvidenceBundle  
└── Capability Context  
└── Ontology Action Type Definition  
└── Constraint Definition  
└── Approval Requirement  
└── Emergency Rule Context  
└── Authorization Context  
└── Trace Context

Input Rule:  
└── Safety Gate accepts only structured, ontology-grounded ApprovedAction objects with RuntimeValidationResult  
└── Free-form agent output or ActionCandidate cannot enter Safety Gate directly  
└── ApprovedAction must include action type, target node, source candidate, decision case, approval decision, evidence, current state reference, and trace ID

---

## **Related Lifecycle Objects and Gate Outputs**

└── ApprovedAction  
└── RejectedActionCandidate  
└── BlockedActionCandidate  
└── EscalationRequired  
└── MoreEvidenceRequired  
└── HumanApprovalRequired  
└── EmergencyApprovalPathResult  
└── SafetyValidationReport  
└── PolicyValidationReport  
└── ConstraintValidationReport  
└── ApprovalValidationReport  
└── AuditRecord

Output Rule:  
└── ApprovedAction is an input authority object produced by ApprovalDecision, not a Safety Gate-created output  
└── Safety Gate does not create ApprovedAction  
└── SafetyGatePass and SafetyGateBlock are Safety Gate outputs  
└── SafetyGatePass is the only Safety Gate output that may allow ExecutionRequest creation  
└── SafetyGateBlock, rejected, blocked, or escalation-required results must not create execution requests  
└── Every output must be auditable and traceable

---

## **ApprovedAction Stack**

└── approved\_action\_id  
└── source\_action\_candidate\_id  
└── decision\_case\_id  
└── action\_type  
└── target\_node\_id  
└── target\_node\_type  
└── approved\_by  
└── approval\_record\_id  
└── approval\_level  
└── policy\_decision\_id  
└── validation\_report\_id  
└── evidence\_refs  
└── world\_state\_snapshot\_id  
└── required\_capability  
└── execution\_constraints  
└── expected\_feedback  
└── safety\_conditions  
└── emergency\_mode  
└── validity\_window  
└── idempotency\_key  
└── trace\_id  
└── correlation\_id  
└── created\_at

ApprovedAction Rule:  
└── ApprovedAction is not yet a physical command  
└── It is an authority object produced by ApprovalDecision and ready to enter runtime validation  
└── ApprovedAction requires RuntimeValidationResult and a valid SafetyGatePass before Unified Cyber-Physical Core may create an ExecutionRequest

---

## **Validation Rule Stack**

└── Ontology-defined Action Type Validation  
└── Constraint Validation  
└── Policy Validation  
└── Capability Validation  
└── Human Approval Validation  
└── Authorization Validation  
└── Emergency Rule Validation  
└── Operational State Validation  
└── Evidence Validation  
└── Freshness Validation  
└── Target Node Validation  
└── Conflict Validation  
└── Validity Window Validation  
└── Idempotency Validation

Master Rule:  
└── Only ontology-defined Action Types can become ApprovedAction  
└── Unknown action types must be rejected or sent to ontology governance review  
└── No candidate may bypass validation because it came from a trusted agent

---

## **Ontology Action Type Validation Stack**

└── Action Type Registry Lookup  
└── Canonical Action IRI Check  
└── Target Object Type Check  
└── Required Property Check  
└── Domain / Range Check  
└── Allowed Action Target Check  
└── Required Capability Check  
└── Required Approval Type Check  
└── Expected Feedback Type Check  
└── Action Preconditions Check  
└── SHACL ActionCandidate Shape Check

Examples:  
└── ACTION\_STOP\_WORK  
└── ACTION\_EVACUATE  
└── ACTION\_LOCK\_ZONE  
└── ACTION\_NOTIFY\_MANAGER  
└── ACTION\_DISPATCH\_ROBOT  
└── ACTION\_REPLAN\_ROUTE  
└── ACTION\_RESUME\_WORK  
└── ACTION\_REQUEST\_INSPECTION  
└── ACTION\_EMERGENCY\_STOP

Ontology Validation Rule:  
└── If the action type is not defined in the ontology, it cannot become ApprovedAction  
└── If the target node does not match the action type domain, the candidate must be rejected or escalated

---

## **Constraint Validation Stack**

└── Safety Constraint  
└── Zone Constraint  
└── Task Constraint  
└── Equipment Constraint  
└── Robot Constraint  
└── Worker Constraint  
└── Environmental Constraint  
└── Permit Constraint  
└── Time Constraint  
└── Location Constraint  
└── Dependency Constraint  
└── Operational Constraint  
└── Legal Constraint  
└── Conflict Constraint

Constraint Examples:  
└── Do not dispatch robot into restricted zone without approval  
└── Do not resume work until inspection is completed  
└── Do not lock zone if emergency evacuation route would be blocked  
└── Do not send worker into high-risk zone without permit and certification  
└── Do not replan route through active crane operation area  
└── Do not execute action if current state is stale beyond safety threshold

Constraint Rule:  
└── Any hard safety constraint violation blocks approval  
└── Soft constraints may require escalation, warning, or additional approval depending on policy

---

## **Policy Validation Stack**

└── OPA / Rego Policy Evaluation  
└── Safety Policy Check  
└── Authorization Policy Check  
└── Approval Policy Check  
└── Emergency Policy Check  
└── Compliance Policy Check  
└── Data Access Policy Check  
└── Manual Override Policy Check  
└── Robot Operation Policy Check  
└── Equipment Protection Policy Check  
└── Policy Version Check  
└── Policy Decision Log

Policy Input Context:  
└── subject\_id  
└── subject\_role  
└── action\_type  
└── target\_node\_id  
└── target\_node\_type  
└── risk\_tier  
└── site\_id  
└── project\_id  
└── approval\_status  
└── emergency\_mode  
└── evidence\_status  
└── current\_state\_status

Policy Rule:  
└── Governance Layer owns policy definitions  
└── Safety Gate consumes policy decisions and validates execution eligibility  
└── Policy allow does not automatically mean execution approval; all validations must pass

---

## **Capability Validation Stack**

└── Required Capability Check  
└── Provided Capability Check  
└── Capability Level Check  
└── Certification Check  
└── Interface Contract Check  
└── Availability Check  
└── Operational Mode Check  
└── Equipment Readiness Check  
└── Robot Readiness Check  
└── Worker Certification Check  
└── External System Capability Check  
└── Fleet Manager Availability Check

Capability Examples:  
└── ACTION\_DISPATCH\_ROBOT requires target robot or fleet manager to support dispatch interface  
└── ACTION\_REQUEST\_INSPECTION requires inspector or inspection robot capability  
└── ACTION\_REPLAN\_ROUTE requires route planning capability from external fleet or planning system  
└── ACTION\_LOCK\_ZONE requires authorized zone control interface or site operation system

Capability Rule:  
└── Having capability is necessary but not sufficient  
└── Capability must be available, current, authorized, and safe under current state

---

## **Human Approval Validation Stack**

└── Approval Requirement Check  
└── Approval Record Lookup  
└── Approval Level Check  
└── Approver Identity Check  
└── Approver Role Check  
└── Approver Scope Check  
└── Approval Timestamp Check  
└── Approval Expiration Check  
└── Approval Comment Check  
└── Multi-party Approval Check  
└── Conditional Approval Check  
└── Rejection Check  
└── Revocation Check

Approval Rule:  
└── If human approval is required and missing, governance must not create an ApprovedAction  
└── Approval must match required role, scope, site, risk tier, and action type  
└── Expired or revoked approval is invalid  
└── Approval UI submission alone is not enough; Safety Gate must validate the approval record before SafetyGatePass

---

## **Authorization Validation Stack**

└── Subject Permission Check  
└── Role Permission Check  
└── Site Scope Check  
└── Project Scope Check  
└── Object Permission Check  
└── Action Permission Check  
└── Emergency Authority Check  
└── Manual Override Authority Check  
└── External System Scope Check  
└── Agent Permission Scope Check

Authorization Rule:  
└── User, agent, service, or external system must be authorized for the specific action, target object, site, and risk level  
└── Agents cannot approve their own high-risk candidates  
└── External systems cannot expand their authority beyond registered scope

---

## **Emergency Rule Validation Stack**

└── Emergency Mode Check  
└── Emergency Action Type Check  
└── Predefined Emergency Policy Check  
└── Deterministic Safety Path Check  
└── Emergency Authority Check  
└── Emergency Evidence Requirement  
└── Immediate Notification Requirement  
└── Post-execution Audit Requirement  
└── Recovery Workflow Requirement  
└── Manual Review Requirement

Emergency Rule:  
└── Critical emergency may allow a deterministic safety fast path only when predefined by policy  
└── Emergency does not mean uncontrolled execution  
└── Emergency path must preserve trace ID, evidence, reason code, and post-execution review

---

## **Operational State Validation Stack**

└── Current World State Check  
└── State Freshness Check  
└── State Version Check  
└── Target Node State Check  
└── Zone State Check  
└── Worker State Check  
└── Robot State Check  
└── Equipment State Check  
└── Approval State Check  
└── Execution State Check  
└── External System State Check  
└── Stale State Rejection  
└── Conflict State Detection  
└── Missing State Detection

Operational State Rule:  
└── High-risk actions require fresh current state  
└── Stale, missing, conflicting, or low-confidence state must block, degrade, or escalate  
└── Safety Gate should prefer Layer 6 Real-Time World State for current operational facts

---

## **Evidence Validation Stack**

└── Evidence Bundle Check  
└── Sensor Evidence Check  
└── Graph Evidence Check  
└── Log Evidence Check  
└── Document Evidence Check  
└── World State Evidence Check  
└── Historical Event Evidence Check  
└── Inspection Evidence Check  
└── Source Reliability Check  
└── Confidence Score Check  
└── Evidence Freshness Check  
└── Evidence Completeness Check  
└── Evidence Conflict Check  
└── Evidence Provenance Check

Evidence Rule:  
└── High-risk actions require evidence-bound validation  
└── Model output alone is not sufficient evidence  
└── Vector-only evidence must not approve action  
└── Conflicting evidence must escalate or block depending on risk level

---

## **SHACL Validation Stack**

└── ActionCandidate Shape  
└── ApprovedAction Shape  
└── ExecutionRequest Pre-shape  
└── Required Property Validation  
└── Datatype Validation  
└── Cardinality Validation  
└── Target Class Validation  
└── Action Type Shape  
└── Target Node Shape  
└── Evidence Bundle Shape  
└── Constraint Shape  
└── Validation Report

SHACL Usage:  
└── Validate structure of ActionCandidate  
└── Validate required fields for ApprovedAction  
└── Validate ontology-grounded action target consistency  
└── Validate evidence bundle shape  
└── Validate execution request readiness before Unified Core

SHACL Rule:  
└── Target-specific SHACL validation is appropriate for runtime  
└── Full graph validation belongs to offline or batch validation paths

---

## **Safety Interlock Stack**

└── Hard Safety Block  
└── Emergency Stop Interlock  
└── Zone Lock Interlock  
└── Worker Presence Interlock  
└── Equipment Active State Interlock  
└── Robot Unsafe State Interlock  
└── Stale State Interlock  
└── Conflicting Evidence Interlock  
└── Missing Approval Interlock  
└── Policy Violation Interlock  
└── Manual Override Interlock  
└── External System Unavailable Interlock

Safety Interlock Rule:  
└── If a hard interlock is active, Safety Gate must block SafetyGatePass and ExecutionRequest readiness  
└── Interlock release must be explicit, authorized, and audited  
└── Safety interlocks should fail secure

---

## **State Machine Stack**

└── candidate\_received  
└── ontology\_validating  
└── constraint\_validating  
└── policy\_validating  
└── capability\_validating  
└── approval\_validating  
└── state\_validating  
└── evidence\_validating  
└── approved  
└── rejected  
└── blocked  
└── escalation\_required  
└── more\_evidence\_required  
└── human\_approval\_required  
└── expired  
└── cancelled

State Machine Rule:  
└── Every candidate must have explicit validation state  
└── Undefined transitions are rejected  
└── State transitions must be auditable

---

## **Approval Workflow Integration Stack**

└── ApprovalRequest  
└── ApprovalDecision  
└── ApprovalRecord  
└── ApprovalLevel  
└── ApprovalMatrix  
└── ReviewerIdentity  
└── ReviewerScope  
└── ApprovalCondition  
└── ApprovalExpiration  
└── ApprovalRevocation  
└── ApprovalAuditTrail

Integration Rule:  
└── Decision Router routes cases to approval  
└── Experience Layer presents approval UI  
└── Governance defines who can approve  
└── Safety Gate validates whether approval is sufficient  
└── ApprovalDecision creates ApprovedAction before Safety Gate  
└── Safety Gate does not create ApprovedAction

---

## **Permission Engine Stack**

└── Subject Permission  
└── Role Permission  
└── Attribute Permission  
└── Object Permission  
└── Action Permission  
└── Site Permission  
└── Project Permission  
└── Emergency Permission  
└── Manual Override Permission  
└── Agent Permission  
└── External System Permission

Permission Rule:  
└── Permission must be specific to subject, action, object, risk tier, site, and project  
└── General access does not imply execution approval

---

## **Safety Policy Engine Stack**

└── Human Safety Policy  
└── Legal Compliance Policy  
└── Robot Safety Policy  
└── Equipment Protection Policy  
└── Productivity Policy  
└── Emergency Policy  
└── Zone Safety Policy  
└── Worker Exposure Policy  
└── Equipment Operation Policy  
└── Robot Dispatch Policy  
└── Resume Work Policy  
└── Stop Work Policy  
└── Evacuation Policy

Decision Priority:  
└── Human Safety Priority  
└── Legal Compliance Priority  
└── Robot Safety Priority  
└── Equipment Protection Priority  
└── Productivity Priority

Safety Policy Rule:  
└── Productivity must never override safety or legal compliance  
└── When uncertainty remains, choose block, escalate, or more restrictive path

---

## **Approved Action Examples Stack**

└── ACTION\_STOP\_WORK  
└── Requires target zone / task  
└── Requires safety reason  
└── May require supervisor or safety manager approval depending on risk  
└── Must produce audit record

└── ACTION\_EVACUATE  
└── Requires target zone  
└── Requires worker presence / risk evidence  
└── Requires emergency or safety approval policy  
└── Must define notification and feedback requirements

└── ACTION\_LOCK\_ZONE  
└── Requires zone control authority  
└── Requires zone state and access impact validation  
└── Must not block emergency evacuation route

└── ACTION\_NOTIFY\_MANAGER  
└── Low-risk notification action  
└── May require no approval  
└── Must still be ontology-defined and auditable

└── ACTION\_DISPATCH\_ROBOT  
└── Requires robot or fleet manager capability  
└── Requires target zone safety validation  
└── Requires robot availability and external system readiness

└── ACTION\_REPLAN\_ROUTE  
└── Requires route planning capability  
└── Requires target route constraints  
└── Must avoid unsafe zones and restricted areas

└── ACTION\_RESUME\_WORK  
└── Requires prior stop-work or lock-zone context  
└── Requires inspection or safety clearance evidence  
└── Usually requires supervisor or safety manager approval

└── ACTION\_REQUEST\_INSPECTION  
└── Requires inspection target  
└── Requires inspector, robot, or workflow capability  
└── Creates inspection request, not direct physical execution

└── ACTION\_EMERGENCY\_STOP  
└── Requires predefined emergency policy  
└── May follow deterministic fast path  
└── Requires post-execution audit and review

---

## **ApprovedAction DTO Stack**

└── ApprovedActionDTO  
└── RejectedActionDTO  
└── BlockedActionDTO  
└── SafetyValidationReportDTO  
└── ConstraintValidationResultDTO  
└── PolicyValidationResultDTO  
└── CapabilityValidationResultDTO  
└── ApprovalValidationResultDTO  
└── OperationalStateValidationResultDTO  
└── EvidenceValidationResultDTO  
└── SafetyInterlockStatusDTO

ApprovedActionDTO Fields:  
└── approved\_action\_id  
└── action\_type  
└── target\_node\_id  
└── target\_node\_type  
└── source\_candidate\_id  
└── decision\_case\_id  
└── validation\_report\_id  
└── policy\_decision\_id  
└── approval\_record\_id  
└── evidence\_refs  
└── world\_state\_snapshot\_id  
└── constraints  
└── expected\_feedback  
└── validity\_window  
└── idempotency\_key  
└── trace\_id  
└── correlation\_id  
└── created\_at

---

## **Observability Stack**

└── Safety Gate Validation Latency  
└── Candidate Approval Rate  
└── Candidate Rejection Rate  
└── Candidate Block Rate  
└── Escalation Required Count  
└── Missing Approval Count  
└── Policy Block Count  
└── Constraint Violation Count  
└── Capability Failure Count  
└── Stale State Block Count  
└── Evidence Insufficiency Count  
└── Emergency Fast Path Count  
└── Interlock Activation Count  
└── Validation Error Count  
└── SafetyGatePass Issued Count

Observability Rule:  
└── Every validation outcome must be measurable and traceable  
└── A failed or bypassed safety gate is a critical system failure

---

## **Security & Audit Stack**

└── Validation Audit Record  
└── ApprovedAction Audit Record  
└── Rejection Audit Record  
└── Block Audit Record  
└── Human Approval Audit Record  
└── Emergency Action Audit Record  
└── Manual Override Audit Record  
└── Policy Decision Audit Record  
└── Interlock Audit Record  
└── Permission Check Audit Record  
└── Trace ID  
└── Correlation ID  
└── Reviewer Identity  
└── Policy Version  
└── Ontology Version  
└── World State Version

Audit Rule:  
└── Every approved, rejected, blocked, or escalated candidate must produce an audit record  
└── High-risk approvals must preserve evidence, reviewer, policy, ontology version, and state snapshot

---

## **Runtime Boundary**

└── This layer is active in the final pre-execution validation path  
└── It must be deterministic, bounded, evidence-bound, and fail-secure  
└── It should use target-specific validation, not full graph reasoning  
└── It should prefer fresh Layer 6 world state for current operational facts  
└── It should use Layer 4 ontology contracts for action meaning and constraints  
└── It should use Layer 3 policy decisions for authorization and approval authority  
└── It should use Layer 5 memory and evidence for supporting context  
└── It does not create ApprovedAction; Approval creates ApprovedAction before this layer  
└── It passes SafetyGatePass or SafetyGateBlock to Layer 10 Unified Cyber-Physical Core

---

## **Not Responsible For**

└── Generating action candidates  
└── Performing raw sensor ingestion  
└── Defining ontology meaning  
└── Acting as API Gateway  
└── Managing all governance policy definitions alone  
└── Replacing Decision Router  
└── Replacing Human Approval UI  
└── Replacing Real-Time World State  
└── Running full OWL reasoning in runtime path  
└── Performing broad RAG search as final authority  
└── Creating execution requests directly without Unified Core lifecycle  
└── Directly executing physical commands  
└── Controlling robots, PLCs, SCADA, equipment, or fleet managers  
└── Performing robot motion planning  
└── Performing fleet scheduling  
└── Bypassing external control systems

---

## **Recommended Initial Stack Mapping**

└── Validation Engine: Python service  
└── DTOs: Pydantic ApprovedActionDTO, RuntimeValidationResultDTO, SafetyGatePassDTO, SafetyGateBlockDTO  
└── Ontology Action Registry: Python registry generated or synchronized from ontology  
└── SHACL: pySHACL for target-specific ActionCandidate validation  
└── Policy: OPA / Rego policy decision call  
└── Capability Validation: simple capability registry \+ current availability check  
└── Human Approval Validation: PostgreSQL approval records  
└── State Validation: Redis world state freshness check  
└── Evidence Validation: evidence\_refs \+ source / timestamp / confidence check  
└── State Machine: explicit Python enum state machine  
└── Audit: PostgreSQL audit event \+ OpenTelemetry trace  
└── Interlock: hard-coded safety interlock table first, policy-backed later  
└── Output: SafetyGatePass only when all required runtime validation passes; otherwise SafetyGateBlock

Initial Rollout Rule:  
└── Start with a strict ApprovedAction → RuntimeValidationInput → RuntimeValidationResult → Safety Gate → SafetyGatePass/SafetyGateBlock validation pipeline  
└── Define 5 to 9 approved action types only  
└── Validate action type, target node, state freshness, approval, policy, capability, and evidence  
└── Use fail-secure defaults  
└── Do not allow agents, UI, or external systems to bypass Safety Gate  
└── Do not connect Safety Gate directly to robot or PLC execution

---

## **Approved Action / Safety Gate Core Principles**

1. ActionCandidate Is Not ApprovedAction  
   └── A candidate is only a proposal; it becomes ApprovedAction only after policy, decision, and approval.  
2. Only Ontology-defined Action Types Can Be Executed  
   └── Unknown action types must be rejected or sent to ontology governance review.  
3. Safety Gate Is the Final Pre-execution Boundary  
   └── No ExecutionRequest should be created without a valid SafetyGatePass.  
4. Validation Must Be Multi-dimensional  
   └── Constraint, policy, capability, approval, authorization, emergency rule, evidence, and current state must all be validated where required.  
5. Human Approval Alone Is Not Enough  
   └── Approval must still be checked against policy, authority, current state, evidence, and action constraints.  
6. Policy Allow Is Not Enough  
   └── Policy permission does not automatically mean the action is safe, fresh, capable, or executable.  
7. Capability Is Not Permission  
   └── A robot, worker, equipment, or external system may have capability, but execution still requires state, policy, approval, and safety validation.  
8. Fresh State Is Required for High-risk Actions  
   └── Stale, missing, conflicting, or low-confidence current state must block, degrade, or escalate.  
9. Evidence Is Required for High-risk Approval  
   └── High-risk actions must include sensor, graph, document, log, world state, or inspection evidence.  
10. Model Output Is Not Evidence  
    └── LLM, SLM, vision, or classifier output cannot approve action by itself.  
11. Vector-only Retrieval Cannot Approve Action  
    └── Similarity search may support context, but cannot be final approval evidence.  
12. Emergency Fast Path Must Be Predefined  
    └── Emergency execution is allowed only through predefined deterministic policy, minimum Runtime Validation, emergency Safety Gate decision, and post-execution audit.  
13. Safety Interlocks Must Fail Secure  
    └── Active hard interlocks must block approval until explicitly released through authorized and audited process.  
14. Every Rejection Needs a Reason  
    └── Blocked or rejected candidates should produce reason codes, validation results, and audit records.  
15. Every Approval Needs a Trace  
    └── ApprovedAction must preserve candidate ID, decision case ID, evidence, policy version, approval record, world state snapshot, and trace ID.  
16. Safety Gate Must Be Deterministic and Bounded  
    └── It should avoid long-running LLM reasoning, broad RAG, full graph scans, or full OWL reasoning in the critical path.  
17. Safety Gate Depends on Other Layers but Owns Final Execution-readiness Decision  
    └── It consumes ontology, policy, world state, memory, approval, evidence, and RuntimeValidationResult, but owns only the final pass/block decision.  
18. ApprovedAction Is Still Not a Physical Command  
    └── ApprovedAction requires Runtime Validation and a valid SafetyGatePass before Unified Cyber-Physical Core creates an ExecutionRequest.  
19. No Actor Can Bypass Safety Gate  
    └── Agents, UI, supervisors, external systems, and automated workflows must all pass through Safety Gate for executable actions.  
20. Safety Gate Protects the Physical World  
    └── Its purpose is to prevent unsafe, unauthorized, stale, ungrounded, or insufficiently evidenced candidates from reaching execution.
