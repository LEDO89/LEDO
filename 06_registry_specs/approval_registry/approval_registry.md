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
        ↓  
DecisionCase  
        ↓  
Policy Evaluation  
        ↓  
approval\_registry lookup  
        ↓  
ApprovalRequest  
        ↓  
Human / Role / Authority Approval  
        ↓  
ApprovedAction  
        ↓  
Safety Gate  
        ↓  
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
    ↓  
DecisionCase  
    ↓  
ApprovalRequirement  
    ↓  
ApprovalRequest  
    ↓  
ApprovalDecision  
    ↓  
ApprovedAction  
    ↓  
SafetyGateResult  
    ↓  
ExecutionRequest  
    ↓  
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
Are the approver’s identity attributes valid?  
Is the approver’s certification valid?  
Does the approver’s site/zone scope match the target scope?  
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

Approval pass ≠ Safety Gate pass

---

## **25\. Relationship to Agent Vocabulary Registry**

Agents must not directly perform approval.

Agents may only do the following:

Generate ApprovalRequest  
Recommend that approval is needed  
Build approval evidence bundle  
Generate notification for approvers

Agents must not directly create `ApprovalDecision = approved`.

Agent Recommendation ≠ Approval Decision

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

# **approval\_registry 설계 보고서**

## **1\. 개요**

`approval_registry`는 LEDO Ontology-Centric Cyber-Physical System에서 사용되는 Approval Type, Approval Level, Approval Authority, Approval Condition, Approval Scope, Approval Expiration, Approval Delegation, Approval Audit Rule을 정의하고 통제하는 핵심 레지스트리이다.

이 모듈의 목적은 `ActionCandidate` 또는 `DecisionCase`가 `ApprovedAction`으로 전환되기 전에 필요한 승인 조건을 명확히 정의하고, 승인 권한이 없는 주체가 임의로 Action을 승인하지 못하도록 방지하는 것이다.

`approval_registry`는 단순한 승인자 목록이 아니다.

이 레지스트리는 다음을 정의하는 **승인 권한 및 승인 조건 운영 계약 레지스트리**이다.

어떤 Action Type에는 어떤 승인 수준이 필요한가?  
누가 해당 승인을 할 수 있는가?  
승인은 어떤 범위에서만 유효한가?  
승인은 언제 만료되는가?  
승인은 위임 가능한가?  
복수 승인 또는 quorum이 필요한가?  
비상 상황에서는 어떤 approval override가 허용되는가?  
승인 결과는 어떤 audit record로 남아야 하는가?

즉, `approval_registry`는 Human-in-the-loop 구조에서 승인 권한과 승인 조건을 결정론적으로 통제하는 핵심 레지스트리이다.

---

## **2\. 핵심 원칙**

Approval은 실행이 아니다.

Approval은 physical command가 아니다.

Approval은 Safety Gate를 대체하지 않는다.

Approval은 Adapter 선택을 의미하지 않는다.

Approval은 External System 실행을 의미하지 않는다.

Approval의 의미는 다음과 같다.

해당 Action은 지정된 조건과 범위 안에서  
다음 검증 단계로 진행될 수 있다.

즉, approval은 `ApprovedAction`을 생성할 수 있는 필수 조건이지만, approval 자체가 물리 실행을 보장하지는 않는다.

최종 원칙은 다음과 같다.

No valid approval,  
no ApprovedAction.

No Safety Gate pass,  
no ExecutionRequest.

No External System,  
no physical execution.

---

## **3\. LEDO 아키텍처 내 위치**

`approval_registry`는 Action Registry, Policy Registry, Identity Registry, Safety Gate 사이에 위치한다.

ActionCandidate  
        ↓  
DecisionCase  
        ↓  
Policy Evaluation  
        ↓  
approval\_registry lookup  
        ↓  
ApprovalRequest  
        ↓  
Human / Role / Authority Approval  
        ↓  
ApprovedAction  
        ↓  
Safety Gate  
        ↓  
ExecutionRequest

`approval_registry`는 어떤 Action이 승인되어야 하는지, 누가 승인할 수 있는지, 어떤 조건에서 승인 가능한지를 결정한다.

---

## **4\. 목적**

`approval_registry`의 목적은 다음과 같다.

1. Action Type별 필요한 approval level 정의  
2. Approval authority와 role 정의  
3. 승인 가능한 target scope 정의  
4. 승인 유효 시간 및 만료 조건 정의  
5. 복수 승인 또는 quorum requirement 정의  
6. 위임 승인 조건 정의  
7. emergency approval 및 override 조건 정의  
8. approval revocation 조건 정의  
9. approval과 policy/safety validation의 경계 정의  
10. 승인 결과의 audit rule 정의  
11. 승인 객체의 version 및 lifecycle 관리  
12. 승인 없는 ApprovedAction 생성을 방지  
13. Agent 또는 LLM이 직접 승인자가 되는 것을 방지

---

## **5\. 핵심 구분**

### **5.1 Approval Requirement**

`Approval Requirement`는 특정 Action Type이 ApprovedAction으로 전환되기 전에 필요한 승인 조건이다.

예시:

STOP\_WORK → safety\_supervisor\_approval 필요  
DISPATCH\_ROBOT → supervisor\_approval 필요  
LOCK\_ZONE → safety\_manager\_approval 필요  
NOTIFY\_MANAGER → approval 없음 또는 auto\_approval 가능

---

### **5.2 Approval Level**

`Approval Level`은 필요한 승인 수준을 의미한다.

예시:

none  
auto\_approval  
operator\_acknowledgement  
supervisor\_approval  
safety\_supervisor\_approval  
site\_manager\_approval  
compliance\_officer\_approval  
multi\_party\_approval  
emergency\_override\_approval

Approval Level은 Action Type, risk class, target scope, current world state에 따라 달라질 수 있다.

---

### **5.3 Approval Authority**

`Approval Authority`는 특정 approval level을 수행할 수 있는 주체 또는 role이다.

예시:

site\_supervisor  
safety\_supervisor  
site\_manager  
robot\_operations\_manager  
compliance\_officer  
emergency\_controller  
human\_operator

Approval Authority는 identity, role, site scope, zone scope, shift, certification, delegation status와 연결되어야 한다.

---

### **5.4 Approval Request**

`ApprovalRequest`는 특정 ActionCandidate 또는 DecisionCase에 대해 필요한 승인을 요청하는 lifecycle object이다.

ApprovalRequest는 다음을 포함해야 한다.

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

`ApprovalDecision`은 승인 주체가 내린 결과이다.

가능한 decision은 다음과 같다.

approved  
rejected  
needs\_more\_evidence  
escalated  
expired  
revoked  
delegated

---

### **5.6 ApprovedAction**

`ApprovedAction`은 필요한 approval requirement가 충족된 후 생성될 수 있는 객체이다.

하지만 `ApprovedAction`은 여전히 physical command가 아니다.

ApprovedAction \= 승인된 운영 의도  
ApprovedAction ≠ 실행 명령

---

## **6\. Scope**

`approval_registry`는 다음 항목을 통제한다.

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

`approval_registry`는 다음을 정의하지 않는다.

1. 실제 사용자 계정 정보  
2. 비밀번호 또는 인증 토큰  
3. 조직 전체의 HR 인사 정보  
4. policy pass/fail logic 전체  
5. Safety Gate 최종 판정  
6. 물리 장비 실행 로직  
7. PLC / SCADA / Robot command  
8. adapter instance 선택  
9. 현장별 모든 세부 임계값  
10. emergency stop controller 내부 로직  
11. 외부 시스템의 실제 권한 체계 전체

이러한 책임은 각각 다음 모듈에 속한다.

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

## **8\. Approval Level 모델**

권장 approval level은 다음과 같다.

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

승인이 필요하지 않다.

주로 단순 알림, low-risk record creation 등에 사용된다.

예: NOTIFY\_MANAGER

---

### **8.2 auto\_approval**

정책과 runtime validation이 모두 통과하면 자동 승인된다.

단, safety-critical action에는 사용하면 안 된다.

예: low-risk workflow update

---

### **8.3 operator\_acknowledgement**

작업자 또는 운영자가 확인해야 한다.

예: low-risk alert acknowledgement

---

### **8.4 supervisor\_approval**

현장 관리자 또는 작업 감독자의 승인이 필요하다.

예: DISPATCH\_ROBOT

---

### **8.5 safety\_supervisor\_approval**

안전관리자 또는 안전 책임자의 승인이 필요하다.

예: STOP\_WORK, LOCK\_ZONE

---

### **8.6 site\_manager\_approval**

현장 총괄 관리자의 승인이 필요하다.

예: high-impact operation suspension

---

### **8.7 compliance\_officer\_approval**

컴플라이언스 또는 법규 관련 승인자가 필요하다.

예: legal compliance exception

---

### **8.8 multi\_party\_approval**

복수 role의 승인이 필요하다.

예: critical equipment restart

---

### **8.9 emergency\_override\_approval**

비상 상황에서 제한적으로 허용되는 override approval이다.

단, 이 경우도 audit, post-review, safety boundary가 필수이다.

---

## **9\. Approval Authority 모델**

Approval Authority는 단순 사용자 이름이 아니라 role, identity, site scope, certification, shift, delegation status를 포함해야 한다.

권장 authority role:

human\_operator  
site\_supervisor  
safety\_supervisor  
site\_manager  
robot\_operations\_manager  
equipment\_manager  
compliance\_officer  
emergency\_controller  
audit\_officer

Approval Authority는 `identity_registry`와 연결되어야 한다.

approval\_registry:  
    어떤 role이 이 approval을 할 수 있는가?

identity\_registry:  
    현재 이 사용자가 해당 role과 scope를 실제로 가지고 있는가?

---

## **10\. Approval Scope**

Approval은 반드시 scope를 가져야 한다.

Scope 없는 approval은 위험하다.

권장 scope:

site\_scope  
zone\_scope  
equipment\_scope  
worker\_group\_scope  
operation\_scope  
task\_scope  
time\_scope  
risk\_scope

예시:

approval\_scope:  
  site\_scope:  
    \- site\_A  
  zone\_scope:  
    \- zone\_03  
  equipment\_scope:  
    \- crane\_01

이 approval은 `site_A`, `zone_03`, `crane_01`에만 유효하다.

다른 site나 zone에서 재사용되면 안 된다.

---

## **11\. Registry Entry Schema**

각 Approval Registry entry는 다음 구조를 따른다.

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

## **12\. Registry Entry 예시: STOP\_WORK Approval**

approval\_rule\_id: approval:stop\_work\_safety\_supervisor\_v1  
canonical\_name: stop\_work\_safety\_supervisor\_approval  
display\_name: Stop Work Safety Supervisor Approval  
description: STOP\_WORK Action Type이 ApprovedAction으로 전환되기 전에 safety supervisor approval을 요구한다.  
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

## **13\. Registry Entry 예시: DISPATCH\_ROBOT Approval**

approval\_rule\_id: approval:dispatch\_robot\_supervisor\_v1  
canonical\_name: dispatch\_robot\_supervisor\_approval  
display\_name: Dispatch Robot Supervisor Approval  
description: DISPATCH\_ROBOT Action Type이 ApprovedAction으로 전환되기 전에 supervisor approval을 요구한다.  
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

Approval은 다음 lifecycle object들과 연결된다.

ActionCandidate  
    ↓  
DecisionCase  
    ↓  
ApprovalRequirement  
    ↓  
ApprovalRequest  
    ↓  
ApprovalDecision  
    ↓  
ApprovedAction  
    ↓  
SafetyGateResult  
    ↓  
ExecutionRequest  
    ↓  
AuditRecord

Approval Type은 전체 lifecycle에서 reference로 유지되어야 한다.

ApprovalDecision은 `ApprovedAction` 생성을 가능하게 할 수 있지만, 직접 `ExecutionRequest`를 만들 수는 없다.

---

## **15\. Validation Rules**

Approval Rule은 다음 조건을 만족할 때만 유효하다.

1. `approval_rule_id`가 registry에 존재해야 한다.  
2. status가 `active`이어야 한다.  
3. applicable action type이 선언되어야 한다.  
4. required approval level이 선언되어야 한다.  
5. required authority role이 선언되어야 한다.  
6. required policy reference가 선언되어야 한다.  
7. required evidence reference가 선언되어야 한다.  
8. approval scope가 선언되어야 한다.  
9. expiration policy가 선언되어야 한다.  
10. decision boundary가 선언되어야 한다.  
11. execution boundary가 선언되어야 한다.  
12. safety boundary가 선언되어야 한다.  
13. audit event reference가 선언되어야 한다.  
14. owner module이 선언되어야 한다.  
15. version이 유효해야 한다.  
16. deprecated 상태라면 migration metadata가 있어야 한다.

하나라도 누락되면 해당 Approval Rule은 operational lifecycle에 사용되면 안 된다.

---

## **16\. Approval Decision Validation**

Approval Decision은 다음 조건을 만족할 때만 유효하다.

Approval Rule이 active인가?  
Action Type이 applicable\_action\_type\_refs에 포함되어 있는가?  
Risk Class가 applicable\_risk\_classes에 포함되어 있는가?  
Target Type이 applicable\_target\_types에 포함되어 있는가?  
승인자가 required\_authority\_roles 중 하나를 가지고 있는가?  
승인자의 identity attribute가 유효한가?  
승인자의 certification이 유효한가?  
승인자의 site/zone scope가 target scope와 일치하는가?  
필요한 evidence가 존재하는가?  
필요한 policy evaluation이 완료되었는가?  
Approval이 만료되지 않았는가?  
Approval이 revoked 상태가 아닌가?

이 조건을 통과해야만 ApprovalDecision은 `approved`로 인정될 수 있다.

---

## **17\. Expiration Rule**

Approval은 무기한 유효하면 안 된다.

특히 real-time world state가 바뀌는 cyber-physical system에서는 approval이 반드시 expiration을 가져야 한다.

예시:

DISPATCH\_ROBOT approval: 5분 유효  
STOP\_WORK approval: 15분 유효  
LOCK\_ZONE approval: 10분 유효  
NOTIFY\_MANAGER approval: 만료 필요 없음 또는 짧은 TTL

Approval이 만료되면 다음 상태가 된다.

ApprovalDecision \= expired  
ApprovedAction 생성 불가  
이미 생성된 ApprovedAction은 Safety Gate에서 재검증 필요

---

## **18\. Revocation Rule**

승인은 취소될 수 있어야 한다.

Revocation이 필요한 경우:

승인자가 권한을 상실한 경우  
world state가 변경된 경우  
evidence가 invalidated 된 경우  
policy result가 변경된 경우  
target scope가 변경된 경우  
상위 관리자가 승인을 취소한 경우  
emergency condition이 해제된 경우

Revoked approval은 새로운 ApprovedAction 생성에 사용되면 안 된다.

이미 생성된 ApprovedAction이 있다면 Safety Gate 또는 Execution Request Builder에서 중단되어야 한다.

---

## **19\. Delegation Rule**

Approval authority는 제한적으로 위임될 수 있다.

Delegation이 허용되려면 다음 조건이 필요하다.

1. 해당 Approval Rule에서 `delegation_allowed = true`  
2. delegation policy가 존재  
3. 위임자와 수임자의 identity가 모두 유효  
4. 수임자가 필요한 role 또는 certification을 보유  
5. delegation scope가 명확함  
6. delegation expiration이 존재  
7. delegation audit record가 생성됨

예시:

Safety Supervisor가 부재 중일 경우,  
Site Safety Manager가 특정 site와 shift 범위에서만 승인 권한을 위임할 수 있다.

---

## **20\. Emergency Override Rule**

Emergency override는 매우 제한적으로 허용되어야 한다.

Emergency override가 허용되려면 다음 조건이 필요하다.

1. 해당 Approval Rule에서 `emergency_override_allowed = true`  
2. emergency condition이 runtime validation으로 확인됨  
3. override authority role이 유효함  
4. override scope가 제한됨  
5. post-incident review가 필수  
6. audit record가 즉시 생성됨  
7. Safety Gate 또는 safety-rated external system 경계가 유지됨

Emergency override도 physical command가 아니다.

Emergency Override Approval ≠ Emergency Stop Command

Emergency stop command는 safety-rated controller 또는 외부 안전 시스템의 책임이다.

---

## **21\. Relationship to Action Registry**

`action_registry`는 Action Type이 어떤 approval level을 요구하는지 선언한다.

`approval_registry`는 그 approval level을 어떤 rule과 authority로 만족할 수 있는지 정의한다.

action\_registry:  
    이 Action Type은 어떤 approval level이 필요한가?

approval\_registry:  
    그 approval level을 누가, 어떤 조건과 범위에서 수행할 수 있는가?

예시:

Action Type: STOP\_WORK  
required\_approval\_level: safety\_supervisor\_approval

Approval Registry는 다음을 정의한다.

required\_authority\_roles:  
  \- safety\_supervisor  
  \- site\_safety\_manager

---

## **22\. Relationship to Identity Registry**

`identity_registry`는 실제 사용자가 어떤 role, certification, site assignment, shift status를 가지고 있는지 관리한다.

approval\_registry:  
    필요한 approval role과 condition 정의

identity\_registry:  
    현재 승인자가 그 조건을 실제로 만족하는지 검증

Approval Registry는 사용자 계정 정보를 직접 저장하면 안 된다.

---

## **23\. Relationship to Policy Registry**

Policy Registry는 정책을 정의한다.

Approval Registry는 어떤 approval rule이 어떤 policy reference에 묶여야 하는지 정의한다.

Policy Registry:  
    stop\_work\_policy의 pass/fail logic 관리

Approval Registry:  
    STOP\_WORK approval에는 stop\_work\_policy 결과가 필요하다고 선언

Approval은 policy를 대체하지 않는다.

Policy pass 없이 approval만으로 ApprovedAction을 만들면 안 된다.

---

## **24\. Relationship to Safety Gate**

Safety Gate는 Approval 이후에도 반드시 존재해야 한다.

Approval이 있더라도 현재 world state가 바뀌면 실행하면 안 된다.

Approval:  
    사람이 조건부로 승인함

Safety Gate:  
    실행 직전 world state, policy, capability, boundary를 다시 검증함

핵심 원칙:

Approval pass ≠ Safety Gate pass

---

## **25\. Relationship to Agent Vocabulary Registry**

Agent는 approval을 직접 수행할 수 없다.

Agent는 다음까지만 가능하다.

ApprovalRequest 생성  
Approval 필요성 추천  
Approval evidence bundle 구성  
Approval 대상자에게 알림 생성

Agent가 직접 `ApprovalDecision = approved`를 만들면 안 된다.

Agent Recommendation ≠ Approval Decision

---

## **26\. Relationship to Adapter Registry**

Approval Registry는 adapter를 직접 선택하지 않는다.

그러나 어떤 Action이 external execution으로 이어질 가능성이 있다면, approval rule은 execution boundary를 명확히 해야 한다.

approval\_registry:  
    이 Action은 승인되더라도 물리 실행이 아니라 실행 준비만 허용된다.

adapter\_registry:  
    Safety Gate 이후 실제 호환 adapter instance를 선택한다.

---

## **27\. Ontology와의 관계**

모든 Approval Rule은 semantic IRI를 가질 수 있다.

예시:

approval\_rule\_id: approval:stop\_work\_safety\_supervisor\_v1  
semantic\_iri: ledo:StopWorkSafetySupervisorApprovalRule

Ontology에서는 다음과 같이 정의할 수 있다.

ledo:StopWorkSafetySupervisorApprovalRule  
    rdf:type ledo:ApprovalRule ;  
    ledo:appliesToAction ledo:StopWorkAction ;  
    ledo:requiresAuthorityRole ledo:SafetySupervisor ;  
    ledo:requiresEvidence ledo:HazardDetectionSnapshot ;  
    ledo:hasApprovalLevel ledo:SafetySupervisorApproval .

Ontology는 approval의 의미론적 기반을 제공한다.

Approval Registry는 이를 운영 시스템에서 version, status, authority, expiration, scope, audit rule로 관리한다.

---

## **28\. Versioning 및 Migration**

Approval Rule은 반드시 versioning되어야 한다.

다음 항목 중 하나라도 변경되면 version 변경이 필요하다.

1. applicable action type 변경  
2. required approval level 변경  
3. required authority role 변경  
4. required certification 변경  
5. required evidence 변경  
6. required policy reference 변경  
7. approval scope 변경  
8. quorum requirement 변경  
9. delegation rule 변경  
10. expiration rule 변경  
11. emergency override rule 변경  
12. decision / execution / safety boundary 변경

Status 값:

draft  
active  
deprecated  
migration\_required  
retired  
blocked

Deprecated Approval Rule은 다음을 선언해야 한다.

deprecated\_since: datetime  
replacement\_approval\_rule\_id: string | null  
migration\_notes: string

Blocked Approval Rule은 새로운 ApprovalRequest에 사용되면 안 된다.

---

## **29\. Implementation Use**

`approval_registry`는 다음을 생성하거나 검증하는 데 사용된다.

1. `ApprovalLevel` enum  
2. `ApprovalRule` DTO  
3. `ApprovalRequest` DTO constraints  
4. `ApprovalDecision` validation  
5. `ApprovedAction` 생성 조건 검증  
6. Role-based approval validation  
7. Scope-based approval validation  
8. Quorum validation  
9. Delegation validation  
10. Expiration validation  
11. Revocation validation  
12. Emergency override validation  
13. Safety Gate lookup support  
14. Audit log expectation  
15. Test case generation  
16. Migration rules

Implementation은 등록되지 않은 Approval Rule을 사용하면 안 된다.

---

## **30\. 권장 Code Structure**

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

필수 테스트는 다음과 같다.

1\. 등록되지 않은 Approval Rule 거부  
2\. inactive Approval Rule 거부  
3\. deprecated Approval Rule 사용 거부  
4\. blocked Approval Rule 사용 거부  
5\. applicable action type 불일치 거부  
6\. risk class 불일치 거부  
7\. target type 불일치 거부  
8\. authority role 없는 승인 거부  
9\. identity attribute 불일치 승인 거부  
10\. certification 없는 승인 거부  
11\. approval scope 불일치 승인 거부  
12\. required evidence 누락 승인 거부  
13\. required policy result 누락 승인 거부  
14\. expired approval 거부  
15\. revoked approval 거부  
16\. quorum 미충족 승인 거부  
17\. delegation policy 없는 위임 승인 거부  
18\. emergency override 조건 미충족 승인 거부  
19\. approval 없이 ApprovedAction 생성 불가 검증  
20\. approval pass만으로 ExecutionRequest 생성 불가 검증

---

## **34\. Final Rule**

등록된 Approval Rule이 없으면,  
유효한 ApprovalRequest도 없다.

유효한 ApprovalRequest가 없으면,  
유효한 ApprovalDecision도 없다.

유효한 ApprovalDecision이 없으면,  
ApprovedAction도 없다.

Approval이 만료되면,  
ApprovedAction 생성에 사용할 수 없다.

Approval이 취소되면,  
ApprovedAction 생성에 사용할 수 없다.

Approval이 있어도,  
Safety Gate 통과 없이는 ExecutionRequest가 없다.

Approval은 실행이 아니다.

Approval은 물리 명령이 아니다.

Approval은 External System 제어가 아니다.

`approval_registry`는 LEDO Human-in-the-loop Governance Layer의 핵심 결정론적 통제 지점이다.

이 모듈은 승인 권한을 명확히 정의하고, 승인 없는 Action 실행을 방지하며, agent·LLM·operator가 자신의 권한을 넘어 ApprovedAction을 생성하지 못하도록 제한한다.

핵심 정의는 다음과 같다.

Approval Registry  
\= 승인자 목록이 아니라,  
Action이 ApprovedAction으로 전환되기 위한  
승인 권한, 조건, 범위, 만료, 위임, 감사 규칙을 통제하는  
운영 계약 레지스트리

