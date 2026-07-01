# **Approval\_registry** 

## **1\. Overview**

`approval_registry` is a core registry in the LEDO Ontology-Centric Cyber-Physical System. It defines and governs Approval Types, Approval Levels, Approval Authorities, Approval Conditions, Approval Scopes, Approval Expiration, Approval Delegation, and Approval Audit Rules.

The purpose of this registry is to clearly define the approval conditions required before an `ActionCandidate` or `DecisionCase` can be converted into an `ApprovedAction`, and to prevent unauthorized actors from approving actions arbitrarily.

`approval_registry` is not a simple list of approvers.

It is an **operational contract registry for approval authority and approval conditions** that defines the following:

Which approval level is required for each Action Type?  
Who is allowed to approve it?  
Within what scope is the approval valid?  
When does the approval expire?  
Can the approval be delegated?  
Is multi-party approval or quorum required?  
What approval override is allowed in emergency situations?  
What audit record must be created for the approval result?

In other words, `approval_registry` is a core registry that deterministically controls approval authority and approval conditions in the Human-in-the-loop structure.

---

## **2\. Core Principle**

Approval is not execution.

Approval is not a physical command.

Approval does not replace the Safety Gate.

Approval does not mean adapter selection.

Approval does not mean execution by an External System.

The meaning of approval is:

This action may proceed to the next validation stage  
within the specified conditions and scope.

Approval is therefore a required condition for creating an `ApprovedAction`, but approval itself does not guarantee physical execution.

The final principle is:

No valid approval,  
no ApprovedAction.

No Safety Gate pass,  
no ExecutionRequest.

No External System,  
no physical execution.

---

## **3\. Position in the LEDO Architecture**

`approval_registry` sits between the Action Registry, Policy Registry, Identity Registry, and Safety Gate.

ActionCandidate  
        →
DecisionCase  
        →
Policy Evaluation  
        →
approval\_registry lookup  
        →
ApprovalRequest  
        →
Human / Role / Authority Approval  
        →
ApprovedAction  
        →
RuntimeValidationInput  
        →
RuntimeValidationResult  
        →
Safety Gate  
        →
SafetyGatePass or SafetyGateBlock  
        →
ExecutionRequest

`approval_registry` determines which actions require approval, who may approve them, and under what conditions approval is valid.

---

## **4\. Purpose**

The purpose of `approval_registry` is to ensure the following:

1. Define the required approval level for each Action Type  
2. Define approval authority and roles  
3. Define the target scope in which approval is valid  
4. Define approval validity period and expiration conditions  
5. Define multi-party approval or quorum requirements  
6. Define delegated approval conditions  
7. Define emergency approval and override conditions  
8. Define approval revocation conditions  
9. Define the boundary between approval, policy validation, and safety validation  
10. Define audit rules for approval results  
11. Manage approval object versioning and lifecycle  
12. Prevent creation of `ApprovedAction` without approval  
13. Prevent agents or LLMs from becoming direct approvers

---

## **5\. Core Distinctions**

### **5.1 Approval Requirement**

`Approval Requirement` defines the approval condition required before a specific Action Type can be converted into an `ApprovedAction`.

Examples:

STOP\_WORK → requires safety\_supervisor\_approval  
DISPATCH\_ROBOT → requires supervisor\_approval  
LOCK\_ZONE → requires safety\_manager\_approval  
NOTIFY\_MANAGER → requires no approval or may use auto\_approval

---

### **5.2 Approval Level**

`Approval Level` means the required level of approval.

Examples:

none  
auto\_approval  
operator\_acknowledgement  
supervisor\_approval  
safety\_supervisor\_approval  
site\_manager\_approval  
compliance\_officer\_approval  
multi\_party\_approval  
emergency\_override\_approval

The Approval Level may vary depending on Action Type, risk class, target scope, and current world state.

---

### **5.3 Approval Authority**

`Approval Authority` refers to the actor or role that can perform a specific approval level.

Examples:

site\_supervisor  
safety\_supervisor  
site\_manager  
robot\_operations\_manager  
compliance\_officer  
emergency\_controller  
human\_operator

Approval Authority must be connected to identity, role, site scope, zone scope, shift, certification, and delegation status.

---

### **5.4 Approval Request**

`ApprovalRequest` is a lifecycle object that requests approval for a specific `ActionCandidate` or `DecisionCase`.

An `ApprovalRequest` must include:

action\_type\_id  
decision\_case\_id  
target\_scope  
risk\_class  
required\_approval\_level  
required\_authority  
evidence\_summary  
policy\_evaluation\_result  
expiration\_time

---

### **5.5 Approval Decision**

`ApprovalDecision` is the decision made by an approval authority.

Possible decision values include:

approved  
rejected  
needs\_more\_evidence  
escalated  
expired  
revoked  
delegated

---

### **5.6 ApprovedAction**

`ApprovedAction` can be created only after the required approval requirements are satisfied.

However, `ApprovedAction` is still not a physical command.

ApprovedAction \= approved operational intent  
ApprovedAction ≠ execution command

---

## **6\. Scope**

`approval_registry` controls the following fields:

approval\_rule\_id: string  
canonical\_name: string  
display\_name: string  
description: string  
semantic\_iri: string

version: string  
status: draft | active | deprecated | migration\_required | retired | blocked

applicable\_action\_type\_refs:  
  \- string

applicable\_risk\_classes:  
  \- string

applicable\_target\_types:  
  \- string

required\_approval\_level: string

required\_authority\_roles:  
  \- string

required\_identity\_attributes:  
  \- string

required\_certifications:  
  \- string

required\_policy\_refs:  
  \- string

required\_evidence\_refs:  
  \- string

approval\_scope:  
  site\_scope:  
    \- string  
  zone\_scope:  
    \- string  
  equipment\_scope:  
    \- string  
  operation\_scope:  
    \- string

quorum\_requirement:  
  required\_count: integer  
  required\_roles:  
    \- string

delegation\_allowed: boolean  
delegation\_policy\_ref: string | null

expiration\_policy\_ref: string  
default\_expiration\_seconds: integer

revocation\_policy\_ref: string | null  
emergency\_override\_allowed: boolean  
emergency\_override\_policy\_ref: string | null

decision\_boundary: string  
execution\_boundary: string  
safety\_boundary: string

audit\_event\_refs:  
  \- string

owner\_module: string  
owner\_team: string  
source\_document: string

created\_at: datetime  
updated\_at: datetime  
deprecated\_since: datetime | null  
replacement\_approval\_rule\_id: string | null

---

## **7\. Non-Scope**

`approval_registry` does not define the following:

1. Actual user account information  
2. Passwords or authentication tokens  
3. Organization-wide HR information  
4. Complete policy pass/fail logic  
5. Final Safety Gate decision  
6. Physical equipment execution logic  
7. PLC / SCADA / Robot commands  
8. Adapter instance selection  
9. All site-specific detailed thresholds  
10. Internal emergency stop controller logic  
11. Complete external system authority model

These responsibilities belong to the following modules or systems:

identity\_registry  
access\_control\_registry  
policy\_registry  
safety\_gate  
adapter\_registry  
external\_system\_registry  
runtime\_validation\_registry  
site\_authority\_registry  
safety-rated controller  
PLC / SCADA / robot middleware

---

## **8\. Approval Level Model**

Recommended approval levels are:

none  
auto\_approval  
operator\_acknowledgement  
supervisor\_approval  
safety\_supervisor\_approval  
site\_manager\_approval  
compliance\_officer\_approval  
robot\_operations\_approval  
multi\_party\_approval  
emergency\_override\_approval

### **8.1 none**

No approval is required.

This is mainly used for simple notifications or low-risk record creation.

Example: NOTIFY\_MANAGER

---

### **8.2 auto\_approval**

Approval is automatically granted if both policy and runtime validation pass.

However, it must not be used for safety-critical actions.

Example: low-risk workflow update

---

### **8.3 operator\_acknowledgement**

A worker or operator must acknowledge the action.

Example: low-risk alert acknowledgement

---

### **8.4 supervisor\_approval**

Approval from a site supervisor or work supervisor is required.

Example: DISPATCH\_ROBOT

---

### **8.5 safety\_supervisor\_approval**

Approval from a safety supervisor or safety authority is required.

Example: STOP\_WORK, LOCK\_ZONE

---

### **8.6 site\_manager\_approval**

Approval from the overall site manager is required.

Example: high-impact operation suspension

---

### **8.7 compliance\_officer\_approval**

Approval from a compliance or legal authority is required.

Example: legal compliance exception

---

### **8.8 multi\_party\_approval**

Approval from multiple roles is required.

Example: critical equipment restart

---

### **8.9 emergency\_override\_approval**

This is a limited override approval allowed in emergency situations.

Even in this case, audit, post-review, and safety boundaries are mandatory.

---

## **9\. Approval Authority Model**

Approval Authority is not a simple user name. It must include role, identity, site scope, certification, shift, and delegation status.

Recommended authority roles:

human\_operator  
site\_supervisor  
safety\_supervisor  
site\_manager  
robot\_operations\_manager  
equipment\_manager  
compliance\_officer  
emergency\_controller  
audit\_officer

Approval Authority must be connected to `identity_registry`.

approval\_registry:  
    Which role is allowed to perform this approval?

identity\_registry:  
    Does this user currently have the required role and scope?

---

## **10\. Approval Scope**

Approval must always have a scope.

Approval without scope is dangerous.

Recommended scopes:

site\_scope  
zone\_scope  
equipment\_scope  
worker\_group\_scope  
operation\_scope  
task\_scope  
time\_scope  
risk\_scope

Example:

approval\_scope:  
  site\_scope:  
    \- site\_A  
  zone\_scope:  
    \- zone\_03  
  equipment\_scope:  
    \- crane\_01

This approval is valid only for `site_A`, `zone_03`, and `crane_01`.

It must not be reused for another site or zone.

---

## **11\. Registry Entry Schema**

Each Approval Registry entry should follow this structure:

approval\_rule\_id: string  
canonical\_name: string  
display\_name: string  
description: string  
semantic\_iri: string

version: string  
status: draft | active | deprecated | migration\_required | retired | blocked

applicable\_action\_type\_refs:  
  \- string

applicable\_risk\_classes:  
  \- string

applicable\_target\_types:  
  \- string

required\_approval\_level: string

required\_authority\_roles:  
  \- string

required\_identity\_attributes:  
  \- string

required\_certifications:  
  \- string

required\_policy\_refs:  
  \- string

required\_evidence\_refs:  
  \- string

approval\_scope:  
  site\_scope:  
    \- string  
  zone\_scope:  
    \- string  
  equipment\_scope:  
    \- string  
  operation\_scope:  
    \- string

quorum\_requirement:  
  required\_count: integer  
  required\_roles:  
    \- string

delegation\_allowed: boolean  
delegation\_policy\_ref: string | null

expiration\_policy\_ref: string  
default\_expiration\_seconds: integer

revocation\_policy\_ref: string | null

emergency\_override\_allowed: boolean  
emergency\_override\_policy\_ref: string | null

decision\_boundary: string  
execution\_boundary: string  
safety\_boundary: string

audit\_event\_refs:  
  \- string

owner\_module: string  
owner\_team: string  
source\_document: string

created\_at: datetime  
updated\_at: datetime  
deprecated\_since: datetime | null  
replacement\_approval\_rule\_id: string | null

---

## **12\. Example Registry Entry: STOP\_WORK Approval**

approval\_rule\_id: approval:stop\_work\_safety\_supervisor\_v1  
canonical\_name: stop\_work\_safety\_supervisor\_approval  
display\_name: Stop Work Safety Supervisor Approval  
description: Requires safety supervisor approval before a STOP\_WORK Action Type can be converted into an ApprovedAction.  
semantic\_iri: ledo:StopWorkApprovalRule

version: 1.0.0  
status: active

applicable\_action\_type\_refs:  
  \- action:STOP\_WORK

applicable\_risk\_classes:  
  \- high\_risk  
  \- critical  
  \- emergency

applicable\_target\_types:  
  \- worker\_group  
  \- work\_zone  
  \- task  
  \- operation

required\_approval\_level: safety\_supervisor\_approval

required\_authority\_roles:  
  \- safety\_supervisor  
  \- site\_safety\_manager

required\_identity\_attributes:  
  \- active\_employee  
  \- assigned\_to\_site  
  \- on\_shift

required\_certifications:  
  \- construction\_safety\_supervisor\_certification

required\_policy\_refs:  
  \- policy:stop\_work\_policy  
  \- policy:safety\_escalation\_policy

required\_evidence\_refs:  
  \- evidence:hazard\_detection\_snapshot  
  \- evidence:worker\_location\_snapshot  
  \- evidence:risk\_assessment\_snapshot

approval\_scope:  
  site\_scope:  
    \- site\_A  
  zone\_scope:  
    \- "\*"  
  equipment\_scope: \[\]  
  operation\_scope:  
    \- construction\_operation

quorum\_requirement:  
  required\_count: 1  
  required\_roles:  
    \- safety\_supervisor

delegation\_allowed: true  
delegation\_policy\_ref: policy:safety\_supervisor\_delegation\_policy

expiration\_policy\_ref: policy:stop\_work\_approval\_expiration  
default\_expiration\_seconds: 900

revocation\_policy\_ref: policy:approval\_revocation\_policy

emergency\_override\_allowed: true  
emergency\_override\_policy\_ref: policy:emergency\_stop\_work\_override\_policy

decision\_boundary: approves\_operational\_stop\_request\_only  
execution\_boundary: does\_not\_issue\_physical\_machine\_stop  
safety\_boundary: safety\_gate\_must\_still\_pass\_before\_execution\_request

audit\_event\_refs:  
  \- audit:approval\_requested  
  \- audit:approval\_granted  
  \- audit:approval\_rejected  
  \- audit:approval\_expired  
  \- audit:approval\_revoked

owner\_module: safety\_domain\_module  
owner\_team: LEDO Safety Governance  
source\_document: safety\_approval\_contract\_v1  
created\_at: 2026-06-26T00:00:00Z  
updated\_at: 2026-06-26T00:00:00Z  
deprecated\_since: null  
replacement\_approval\_rule\_id: null

---

## **13\. Example Registry Entry: DISPATCH\_ROBOT Approval**

approval\_rule\_id: approval:dispatch\_robot\_supervisor\_v1  
canonical\_name: dispatch\_robot\_supervisor\_approval  
display\_name: Dispatch Robot Supervisor Approval  
description: Requires supervisor approval before a DISPATCH\_ROBOT Action Type can be converted into an ApprovedAction.  
semantic\_iri: ledo:DispatchRobotApprovalRule

version: 1.0.0  
status: active

applicable\_action\_type\_refs:  
  \- action:DISPATCH\_ROBOT

applicable\_risk\_classes:  
  \- warning  
  \- high\_risk

applicable\_target\_types:  
  \- robot  
  \- robot\_fleet  
  \- task\_location  
  \- work\_zone

required\_approval\_level: supervisor\_approval

required\_authority\_roles:  
  \- site\_supervisor  
  \- robot\_operations\_manager

required\_identity\_attributes:  
  \- active\_employee  
  \- assigned\_to\_site  
  \- on\_shift

required\_certifications:  
  \- robot\_operation\_supervisor\_training

required\_policy\_refs:  
  \- policy:robot\_dispatch\_policy  
  \- policy:worker\_proximity\_policy  
  \- policy:zone\_access\_policy

required\_evidence\_refs:  
  \- evidence:robot\_availability\_snapshot  
  \- evidence:zone\_accessibility\_snapshot  
  \- evidence:worker\_proximity\_snapshot  
  \- evidence:mission\_context\_snapshot

approval\_scope:  
  site\_scope:  
    \- site\_A  
  zone\_scope:  
    \- zone\_01  
    \- zone\_02  
    \- zone\_03  
  equipment\_scope: \[\]  
  operation\_scope:  
    \- robotic\_support\_operation

quorum\_requirement:  
  required\_count: 1  
  required\_roles:  
    \- site\_supervisor

delegation\_allowed: false  
delegation\_policy\_ref: null

expiration\_policy\_ref: policy:robot\_dispatch\_approval\_expiration  
default\_expiration\_seconds: 300

revocation\_policy\_ref: policy:approval\_revocation\_policy

emergency\_override\_allowed: false  
emergency\_override\_policy\_ref: null

decision\_boundary: approves\_robot\_dispatch\_intent\_only  
execution\_boundary: does\_not\_generate\_robot\_motion\_or\_fleet\_command  
safety\_boundary: safety\_gate\_and\_robot\_fleet\_manager\_validation\_required

audit\_event\_refs:  
  \- audit:approval\_requested  
  \- audit:approval\_granted  
  \- audit:approval\_rejected  
  \- audit:approval\_expired  
  \- audit:approval\_revoked

owner\_module: robot\_domain\_module  
owner\_team: LEDO Robotics Integration  
source\_document: robot\_approval\_contract\_v1  
created\_at: 2026-06-26T00:00:00Z  
updated\_at: 2026-06-26T00:00:00Z  
deprecated\_since: null  
replacement\_approval\_rule\_id: null

---

## **14\. Approval Lifecycle Alignment**

Approval is connected to the following lifecycle objects:

ActionCandidate  
    →
DecisionCase  
    →
ApprovalRequirement  
    →
ApprovalRequest  
    →
ApprovalDecision  
    →
ApprovedAction  
    →
SafetyGatePass or SafetyGateBlock  
    →
ExecutionRequest  
    →
AuditRecord

Approval Type must remain a reference throughout the lifecycle.

An `ApprovalDecision` may enable the creation of an `ApprovedAction`, but it must not directly create an `ExecutionRequest`.

---

## **15\. Validation Rules**

An Approval Rule is valid only when the following conditions are satisfied:

1. `approval_rule_id` exists in the registry.  
2. Its status is `active`.  
3. Applicable Action Types are declared.  
4. Required approval level is declared.  
5. Required authority roles are declared.  
6. Required policy references are declared.  
7. Required evidence references are declared.  
8. Approval scope is declared.  
9. Expiration policy is declared.  
10. Decision boundary is declared.  
11. Execution boundary is declared.  
12. Safety boundary is declared.  
13. Audit event references are declared.  
14. Owner module is declared.  
15. Version is valid.  
16. If deprecated, migration metadata exists.

If any of these conditions are missing, the Approval Rule must not be used in the operational lifecycle.

---

## **16\. Approval Decision Validation**

An Approval Decision is valid only when the following conditions are satisfied:

Is the Approval Rule active?  
Is the Action Type included in applicable\_action\_type\_refs?  
Is the Risk Class included in applicable\_risk\_classes?  
Is the Target Type included in applicable\_target\_types?  
Does the approver have one of the required\_authority\_roles?  
Are the approver's identity attributes valid?  
Is the approver's certification valid?  
Does the approver's site/zone scope match the target scope?  
Does the required evidence exist?  
Has the required policy evaluation been completed?  
Has the approval not expired?  
Has the approval not been revoked?

Only after passing these conditions can an `ApprovalDecision` be recognized as `approved`.

---

## **17\. Expiration Rule**

Approval must not be valid indefinitely.

In a cyber-physical system where real-time world state changes continuously, approval must always have an expiration condition.

Examples:

DISPATCH\_ROBOT approval: valid for 5 minutes  
STOP\_WORK approval: valid for 15 minutes  
LOCK\_ZONE approval: valid for 10 minutes  
NOTIFY\_MANAGER approval: no expiration required or short TTL

When approval expires, its state becomes:

ApprovalDecision \= expired  
ApprovedAction cannot be created  
If an ApprovedAction already exists, Safety Gate must revalidate it

---

## **18\. Revocation Rule**

Approval must be revocable.

Revocation may be required when:

The approver loses authority  
World state changes  
Evidence is invalidated  
Policy result changes  
Target scope changes  
A higher-level manager revokes the approval  
Emergency condition is cleared

Revoked approval must not be used to create a new `ApprovedAction`.

If an `ApprovedAction` has already been created, it must be stopped by the Safety Gate or Execution Request Builder.

---

## **19\. Delegation Rule**

Approval authority may be delegated only under restricted conditions.

Delegation is allowed only when:

1. `delegation_allowed = true` in the Approval Rule  
2. Delegation policy exists  
3. Both delegator and delegate have valid identities  
4. The delegate has the required role or certification  
5. Delegation scope is explicit  
6. Delegation expiration exists  
7. Delegation audit record is created

Example:

If the Safety Supervisor is absent,  
the Site Safety Manager may receive delegated approval authority  
only within a specific site and shift scope.

---

## **20\. Emergency Override Rule**

Emergency override must be allowed only under highly restricted conditions.

Emergency override requires:

1. `emergency_override_allowed = true` in the Approval Rule  
2. Emergency condition confirmed by runtime validation  
3. Valid override authority role  
4. Limited override scope  
5. Mandatory post-incident review  
6. Immediate audit record creation  
7. Preservation of the Safety Gate or safety-rated external system boundary

Emergency override is also not a physical command.

Emergency Override Approval ≠ Emergency Stop Command

The emergency stop command is the responsibility of a safety-rated controller or external safety system.

---

## **21\. Relationship to Action Registry**

`action_registry` declares which approval level an Action Type requires.

`approval_registry` defines which rule and authority can satisfy that approval level.

action\_registry:  
    Which approval level is required for this Action Type?

approval\_registry:  
    Who can perform that approval level, under what conditions and scope?

Example:

Action Type: STOP\_WORK  
required\_approval\_level: safety\_supervisor\_approval

Approval Registry defines:

required\_authority\_roles:  
  \- safety\_supervisor  
  \- site\_safety\_manager

---

## **22\. Relationship to Identity Registry**

`identity_registry` manages whether an actual user has a specific role, certification, site assignment, and shift status.

approval\_registry:  
    Defines the required approval role and conditions

identity\_registry:  
    Verifies whether the current approver actually satisfies those conditions

Approval Registry must not directly store user account information.

---

## **23\. Relationship to Policy Registry**

Policy Registry defines policies.

Approval Registry defines which policy references must be associated with each approval rule.

Policy Registry:  
    Manages the pass/fail logic of stop\_work\_policy

Approval Registry:  
    Declares that STOP\_WORK approval requires the result of stop\_work\_policy

Approval does not replace policy.

An `ApprovedAction` must not be created from approval alone without policy pass.

---

## **24\. Relationship to Safety Gate**

The Safety Gate must still exist after approval.

Even if approval exists, execution must not proceed if the current world state has changed.

Approval:  
    A human conditionally approves the action

Safety Gate:  
    Revalidates world state, policy, capability, and boundary immediately before execution

Core principle:

Approval pass → RuntimeValidationResult → SafetyGatePass or SafetyGateBlock

---

## **25\. Relationship to Agent Vocabulary Registry**

Agents must not directly perform approval.

Agents may only do the following:

Generate ApprovalRequest  
Recommend that approval is needed  
Build approval evidence bundle  
Generate notification for approvers

Agents must not directly create `ApprovalDecision = approved`.

Agent Recommendation → Approval Decision

---

## **26\. Relationship to Adapter Registry**

Approval Registry does not directly select adapters.

However, if an Action may lead to external execution, the approval rule must clearly define the execution boundary.

approval\_registry:  
    Even if this Action is approved, only execution preparation is allowed,  
    not physical execution.

adapter\_registry:  
    After Safety Gate, selects the actual compatible adapter instance.

---

## **27\. Relationship to Ontology**

Every Approval Rule may have a semantic IRI.

Example:

approval\_rule\_id: approval:stop\_work\_safety\_supervisor\_v1  
semantic\_iri: ledo:StopWorkSafetySupervisorApprovalRule

In the ontology, it may be defined as follows:

ledo:StopWorkSafetySupervisorApprovalRule  
    rdf:type ledo:ApprovalRule ;  
    ledo:appliesToAction ledo:StopWorkAction ;  
    ledo:requiresAuthorityRole ledo:SafetySupervisor ;  
    ledo:requiresEvidence ledo:HazardDetectionSnapshot ;  
    ledo:hasApprovalLevel ledo:SafetySupervisorApproval .

Ontology provides the semantic foundation of approval.

Approval Registry manages it in the operational system through version, status, authority, expiration, scope, and audit rules.

---

## **28\. Versioning and Migration**

Approval Rules must be versioned.

A version change is required when any of the following changes:

1. Applicable Action Type  
2. Required approval level  
3. Required authority role  
4. Required certification  
5. Required evidence  
6. Required policy reference  
7. Approval scope  
8. Quorum requirement  
9. Delegation rule  
10. Expiration rule  
11. Emergency override rule  
12. Decision / execution / safety boundary

Status values:

draft  
active  
deprecated  
migration\_required  
retired  
blocked

A deprecated Approval Rule must declare:

deprecated\_since: datetime  
replacement\_approval\_rule\_id: string | null  
migration\_notes: string

A blocked Approval Rule must not be used in new `ApprovalRequest` objects.

---

## **29\. Implementation Use**

`approval_registry` is used to generate or validate:

1. `ApprovalLevel` enum  
2. `ApprovalRule` DTO  
3. `ApprovalRequest` DTO constraints  
4. `ApprovalDecision` validation  
5. Conditions for creating `ApprovedAction`  
6. Role-based approval validation  
7. Scope-based approval validation  
8. Quorum validation  
9. Delegation validation  
10. Expiration validation  
11. Revocation validation  
12. Emergency override validation  
13. Safety Gate lookup support  
14. Audit log expectations  
15. Test case generation  
16. Migration rules

Implementation must not use unregistered Approval Rules.

---

## **30\. Recommended Code Structure**

registries/  
    approval\_registry/  
        approval\_registry.py  
        approval\_registry\_entry.py  
        approval\_level.py  
        approval\_status.py  
        approval\_decision.py  
        approval\_scope.py  
        approval\_validation.py  
        approval\_errors.py  
        approval\_loader.py  
        approval\_migration.py

    action\_registry/  
    identity\_registry/  
    policy\_registry/  
    agent\_vocabulary\_registry/  
    adapter\_registry/  
    external\_system\_registry/

---

## **31\. Minimal Pydantic Model**

from enum import Enum  
from pydantic import BaseModel, Field  
from typing import Optional  
from datetime import datetime

class ApprovalStatus(str, Enum):  
    DRAFT \= "draft"  
    ACTIVE \= "active"  
    DEPRECATED \= "deprecated"  
    MIGRATION\_REQUIRED \= "migration\_required"  
    RETIRED \= "retired"  
    BLOCKED \= "blocked"

class ApprovalLevel(str, Enum):  
    NONE \= "none"  
    AUTO\_APPROVAL \= "auto\_approval"  
    OPERATOR\_ACKNOWLEDGEMENT \= "operator\_acknowledgement"  
    SUPERVISOR\_APPROVAL \= "supervisor\_approval"  
    SAFETY\_SUPERVISOR\_APPROVAL \= "safety\_supervisor\_approval"  
    SITE\_MANAGER\_APPROVAL \= "site\_manager\_approval"  
    COMPLIANCE\_OFFICER\_APPROVAL \= "compliance\_officer\_approval"  
    ROBOT\_OPERATIONS\_APPROVAL \= "robot\_operations\_approval"  
    MULTI\_PARTY\_APPROVAL \= "multi\_party\_approval"  
    EMERGENCY\_OVERRIDE\_APPROVAL \= "emergency\_override\_approval"

class ApprovalDecisionStatus(str, Enum):  
    APPROVED \= "approved"  
    REJECTED \= "rejected"  
    NEEDS\_MORE\_EVIDENCE \= "needs\_more\_evidence"  
    ESCALATED \= "escalated"  
    EXPIRED \= "expired"  
    REVOKED \= "revoked"  
    DELEGATED \= "delegated"

class QuorumRequirement(BaseModel):  
    required\_count: int \= 1  
    required\_roles: list\[str\] \= Field(default\_factory=list)

class ApprovalScope(BaseModel):  
    site\_scope: list\[str\] \= Field(default\_factory=list)  
    zone\_scope: list\[str\] \= Field(default\_factory=list)  
    equipment\_scope: list\[str\] \= Field(default\_factory=list)  
    operation\_scope: list\[str\] \= Field(default\_factory=list)

class ApprovalRegistryEntry(BaseModel):  
    approval\_rule\_id: str  
    canonical\_name: str  
    display\_name: str  
    description: str  
    semantic\_iri: str

    version: str  
    status: ApprovalStatus \= ApprovalStatus.DRAFT

    applicable\_action\_type\_refs: list\[str\] \= Field(default\_factory=list)  
    applicable\_risk\_classes: list\[str\] \= Field(default\_factory=list)  
    applicable\_target\_types: list\[str\] \= Field(default\_factory=list)

    required\_approval\_level: ApprovalLevel

    required\_authority\_roles: list\[str\] \= Field(default\_factory=list)  
    required\_identity\_attributes: list\[str\] \= Field(default\_factory=list)  
    required\_certifications: list\[str\] \= Field(default\_factory=list)

    required\_policy\_refs: list\[str\] \= Field(default\_factory=list)  
    required\_evidence\_refs: list\[str\] \= Field(default\_factory=list)

    approval\_scope: ApprovalScope  
    quorum\_requirement: QuorumRequirement \= Field(default\_factory=QuorumRequirement)

    delegation\_allowed: bool \= False  
    delegation\_policy\_ref: Optional\[str\] \= None

    expiration\_policy\_ref: str  
    default\_expiration\_seconds: int

    revocation\_policy\_ref: Optional\[str\] \= None

    emergency\_override\_allowed: bool \= False  
    emergency\_override\_policy\_ref: Optional\[str\] \= None

    decision\_boundary: str  
    execution\_boundary: str  
    safety\_boundary: str

    audit\_event\_refs: list\[str\] \= Field(default\_factory=list)

    owner\_module: str  
    owner\_team: str  
    source\_document: str

    created\_at: datetime  
    updated\_at: datetime  
    deprecated\_since: Optional\[datetime\] \= None  
    replacement\_approval\_rule\_id: Optional\[str\] \= None

---

## **32\. Core Validation Function**

def validate\_approval\_rule\_for\_action(  
    entry: ApprovalRegistryEntry,  
    action\_type\_ref: str,  
    risk\_class: str,  
    target\_type: str,  
) \-\> None:  
    if entry.status \!= ApprovalStatus.ACTIVE:  
        raise InvalidApprovalRuleError(  
            f"Approval Rule is not active: {entry.approval\_rule\_id}"  
        )

    if action\_type\_ref not in entry.applicable\_action\_type\_refs:  
        raise ApprovalActionTypeMismatchError(  
            f"Action Type '{action\_type\_ref}' is not applicable to "  
            f"Approval Rule '{entry.approval\_rule\_id}'"  
        )

    if risk\_class not in entry.applicable\_risk\_classes:  
        raise ApprovalRiskClassMismatchError(  
            f"Risk class '{risk\_class}' is not applicable to "  
            f"Approval Rule '{entry.approval\_rule\_id}'"  
        )

    if target\_type not in entry.applicable\_target\_types:  
        raise ApprovalTargetTypeMismatchError(  
            f"Target type '{target\_type}' is not applicable to "  
            f"Approval Rule '{entry.approval\_rule\_id}'"  
        )

    if not entry.required\_authority\_roles:  
        raise InvalidApprovalRuleError(  
            "required\_authority\_roles must be declared"  
        )

    if not entry.required\_policy\_refs:  
        raise InvalidApprovalRuleError(  
            "required\_policy\_refs must be declared"  
        )

    if not entry.required\_evidence\_refs:  
        raise InvalidApprovalRuleError(  
            "required\_evidence\_refs must be declared"  
        )

    if not entry.expiration\_policy\_ref:  
        raise InvalidApprovalRuleError(  
            "expiration\_policy\_ref must be declared"  
        )

    if not entry.decision\_boundary:  
        raise InvalidApprovalRuleError(  
            "decision\_boundary must be declared"  
        )

    if not entry.execution\_boundary:  
        raise InvalidApprovalRuleError(  
            "execution\_boundary must be declared"  
        )

    if not entry.safety\_boundary:  
        raise InvalidApprovalRuleError(  
            "safety\_boundary must be declared"  
        )

---

## **33\. Test Scenarios**

Required tests:

1\. Reject unregistered Approval Rule.  
2\. Reject inactive Approval Rule.  
3\. Reject deprecated Approval Rule.  
4\. Reject blocked Approval Rule.  
5\. Reject applicable Action Type mismatch.  
6\. Reject risk class mismatch.  
7\. Reject target type mismatch.  
8\. Reject approval without authority role.  
9\. Reject approval with identity attribute mismatch.  
10\. Reject approval without required certification.  
11\. Reject approval scope mismatch.  
12\. Reject approval with missing required evidence.  
13\. Reject approval with missing required policy result.  
14\. Reject expired approval.  
15\. Reject revoked approval.  
16\. Reject approval when quorum is not satisfied.  
17\. Reject delegated approval without delegation policy.  
18\. Reject emergency override when conditions are not satisfied.  
19\. Verify that ApprovedAction cannot be created without approval.  
20\. Verify that ExecutionRequest cannot be created from approval pass alone.

---

## **34\. Final Rule**

No registered Approval Rule,  
no valid ApprovalRequest.

No valid ApprovalRequest,  
no valid ApprovalDecision.

No valid ApprovalDecision,  
no ApprovedAction.

If approval expires,  
it cannot be used to create ApprovedAction.

If approval is revoked,  
it cannot be used to create ApprovedAction.

Even if approval exists,  
there is no ExecutionRequest without Safety Gate pass.

Approval is not execution.

Approval is not a physical command.

Approval is not External System control.

`approval_registry` is a core deterministic control point in the LEDO Human-in-the-loop Governance Layer.

This module clearly defines approval authority, prevents action execution without approval, and prevents agents, LLMs, or operators from creating `ApprovedAction` beyond their authority.

The core definition is:

Approval Registry  
\= not a list of approvers,  
but an operational contract registry that controls  
the approval authority, conditions, scope, expiration,  
delegation, and audit rules required for an Action  
to become an ApprovedAction.

