# **Master Architecture “First Constitution”**

## **1\. Purpose**

`00_first_construction.md` is the first constitution of the LEDO project.

This document defines the highest-level principles that all architecture documents, specifications, models, validation structures, and implementation code in the LEDO Ontology Core must follow.

This document does not describe detailed implementation methods.  
This document does not define domain-specific operational rules.  
This document is not dependent on any specific tool or vendor.

This document defines the boundaries that the system must never cross and the principles that all lower-level structures must obey.

---

## **2\. Constitutional Authority**

This document has the highest priority within `00_master_architecture`.

All lower-level documents, designs, and implementations must not conflict with the principles defined here.

If a conflict occurs, the following rules apply.

This document takes precedence.  
Choose the safer interpretation.”  
If uncertain, do not execute.  
If domain knowledge is missing, do not guess.  
High-risk decisions must pass validation and approval.

---

## **3\. First Principle: Ontology Is the Authority of Meaning**

Ontology is the highest-level structure for defining meaning inside the system.

The meaning of objects, relationships, properties, events, states, actions, authority, evidence, policies, and execution boundaries must be defined through ontology and its connected specifications.

AI output, UI representation, temporary data, and external system responses cannot replace the semantic authority of the ontology.

Ontology defines meaning.

---

## **4\. Second Principle: AI Output Is a Candidate, Not Truth**

AI output may generate interpretation, proposals, summaries, classifications, mapping candidates, risk interpretations, and ActionCandidates.

However, AI output cannot determine truth.

AI output must never become:

Evidence  
ApprovedAction  
ExecutionRequest  
ExternalControlRequest  
Policy Decision  
Safety Gate Decision  
Physical Command

AI may propose.  
Ontology, Evidence, Policy, Approval, and Safety Gate must validate.

---

## **5\. Third Principle: No Evidence, No Trusted Decision**

Important decisions must be supported by Evidence.

Evidence must include source, time, trust metadata, traceability, and validation status.

AI-generated explanations or summaries are not Evidence.  
AI may summarize Evidence, but it cannot become Evidence by itself.

No evidence, no trusted decision.

---

## **6\. Fourth Principle: Meaning, Validation, Permission, Approval, and Execution Are Separated**

LEDO separates the following responsibilities.

Ontology     → Meaning definition  
Validation   → Structural and condition validation  
Policy       → Operational permission decision  
Approval     → High-risk authority granting  
Safety Gate  → Execution-readiness validation  
Execution    → Physical execution by external systems  
Audit        → Full path traceability

No layer may merge or bypass these responsibilities.

---

## **7\. Fifth Principle: Policy Determines Operational Permission**

Ontology defines meaning, but it does not determine operational permission by itself.

Operational permission must be determined through Policy, authority, approval state, Evidence, current state, risk level, and execution feasibility.

Policy decisions must be auditable, and high-risk decisions must be connected to approval workflows.

---

## **8\. Sixth Principle: Human Approval Controls High-Risk Authority**

High-risk actions, safety-related actions, and actions that may connect to physical execution must pass Human Approval or an explicitly defined approval structure.

AI, Agents, and automated reasoning results cannot grant high-risk authority to themselves.

Approval must be traceable, and the Evidence, state, and reason behind the approval must be recorded in Audit.

---

## **9\. Seventh Principle: ActionCandidate Is Not an Execution Command**

ActionCandidate is only an execution candidate.

ActionCandidate cannot be executed before passing the following stages.

Semantic Validation  
Evidence Check  
Policy Check  
Decision Routing  
Approval  
Safety Gate Validation

The existence of an ActionCandidate does not mean execution is allowed.

---

## **10\. Eighth Principle: ApprovedAction Is Not a Physical Command**

ApprovedAction is an approved intent or approved action unit.

ApprovedAction is not a direct command to physical equipment, robots, PLCs, SCADA systems, or access-control devices.

ApprovedAction may be transformed into an ExecutionRequest only after passing Safety Gate validation.

---

## **11\. Ninth Principle: ExecutionRequest Is Not a Physical Command**

ExecutionRequest is a request sent to an external system.

ExecutionRequest may contain:

intent  
target  
constraints  
approval reference  
evidence reference  
policy reference  
safety validation result  
trace id  
idempotency key

However, ExecutionRequest itself is not motor control, PLC write, SCADA command, robot joint control, or emergency stop command.

Physical execution belongs to external control systems.

---

## **12\. Tenth Principle: Physical Execution Belongs to External Systems**

LEDO defines physical execution intent, constraints, approval, validation results, and audit traceability.

Actual physical execution belongs to external systems such as:

Robot Middleware  
Fleet Manager  
PLC  
SCADA  
Access Control System  
Equipment Controller  
Site Operation System  
Safety-rated Controller

The internal reasoning layer, AI layer, and ontology layer of LEDO do not directly perform physical control.

---

## **13\. Eleventh Principle: Safety Gate Must Be Deterministic and Fail-Closed**

Safety Gate is the final validation layer before execution.

Safety Gate must be deterministic.  
If it fails or becomes uncertain, it must reject, hold, or escalate in the safer direction.

Unknown → Hold or Deny  
Stale Data → Hold or Deny  
Invalid Approval → Deny  
Missing Evidence → Deny  
Snapshot Failure → Fail Closed

Safety Gate is the final anti-bypass mechanism for safety.

---

## **14\. Twelfth Principle: Runtime Hot Path Reads Only Precomputed Results**

The runtime hot path must not perform heavy reasoning, dynamic graph queries, AI calls, or external network calls.

The runtime hot path must only read precomputed validation results and materialized snapshots.

The following are forbidden in the runtime hot path.

OWL Reasoner  
Full SHACL Validation  
SPARQL Query  
Graph DB Network Call  
LLM / SLM Call  
External API Call  
Disk I/O  
Unbounded Computation

The runtime hot path must be fast, bounded, and verifiable.

---

## **15\. Thirteenth Principle: Audit Preserves Every Important Decision Path**

Important decisions in LEDO must be traceable.

The following objects should be connected within a single trace flow whenever applicable.

Event  
Evidence  
State Update  
ActionCandidate  
Decision  
Approval  
ApprovedAction  
Safety Gate Result  
ExecutionRequest  
ExternalControlRequest  
Feedback  
AuditRecord

Audit is mandatory for post-hoc explanation, validation, accountability, and reproducibility.

---

## **16\. Fourteenth Principle: Source of Truth Must Be Separated**

Not all information in LEDO represents the same kind of truth.

Each area must have a distinct Source of Truth.

Semantic Meaning       → Ontology  
Current Runtime State  → World State  
Historical Evidence    → Evidence Store / Audit  
Operational Permission → Policy  
High-Risk Authority    → Approval  
Execution Readiness    → Safety Gate Snapshot  
Physical Execution     → External System  
Identity Resolution    → Canonical Identity / Registry

No single layer should monopolize every kind of truth.

---

## **17\. Fifteenth Principle: Standards Are Mapped, Not Copied**

External standards are used to strengthen interoperability and semantic alignment.

However, external standards must not be copied blindly into the internal structure.

LEDO uses standards through:

Reference  
Mapping  
Alignment  
Compatibility  
Governance

LEDO’s Core Ontology and internal contracts must preserve their own consistency.

---

## **18\. Sixteenth Principle: Domain Meaning Must Be Governed**

Domain meaning must not be generated arbitrarily.

Construction, industrial operation, robotics, safety, legal compliance, field operations, equipment control, approval authority, and risk criteria must be defined through domain expert review and governance.

The framework may generate structure.  
Domain meaning must be governed.

Structure can be generated.  
Meaning must be governed.

---

## **19\. Seventeenth Principle: If Uncertain, Do Not Execute**

Uncertainty cannot become a basis for execution in LEDO.

When uncertain, the system must choose one of the following actions.

Hold  
Deny  
Escalate  
Request Evidence  
Request Approval  
Request Domain Expert Review

Any design that ignores uncertainty and proceeds directly to execution is not allowed.

---

## **20\. Final Constitutional Declaration**

LEDO is an ontology-centric Cyber-Physical AI system.

LEDO separates meaning, evidence, state, judgment, approval, validation, execution, and audit.

AI may generate candidates, but it does not determine truth.  
Ontology defines meaning, but it does not determine operational permission by itself.  
Policy determines permission, but it does not perform physical execution.  
Approval grants authority, but it is not a physical command.  
Safety Gate validates execution readiness, but it is not a physical controller.  
ExecutionRequest is a request, not a physical command.  
Physical Execution is performed by External Systems.

The final principles are:

Meaning must be explicit.  
Evidence must be traceable.  
Policy must be enforceable.  
Approval must be auditable.  
Validation must be deterministic.  
Execution must be bounded.  
Safety must fail closed.

# **First Constitution**

