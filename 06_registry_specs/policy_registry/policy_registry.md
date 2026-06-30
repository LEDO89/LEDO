# **Policy registry**

## **1\. Overview**

`policy_registry` is a core registry in the LEDO Ontology-Centric Cyber-Physical System. It defines and governs all Policy Types, Policy Rules, Permission Conditions, Prohibition Conditions, Constraints, Escalation Rules, Emergency Rules, Access Rules, Safety Rules, Compliance Rules, and Runtime Policy References used across the system.

The purpose of this module is to verify that every major action attempted by an Agent, Human, Service, Adapter, or External System has passed a clearly defined policy basis.

`policy_registry` is not a simple list of policy documents.

It is an **operational contract registry for policy meaning, conditions, permissions, prohibitions, constraints, and priorities** that defines the following:

Which Policies may exist?

To which targets does this Policy apply?

What does this Policy allow?

What does this Policy prohibit?

Under which conditions does this Policy require hold or escalation?

Which Identity / Role / Scope / Certification does this Policy require?

Which Action Type, Event Type, Evidence Type, or Decision Rule does this Policy apply to?

Must this Policy be evaluated before the Safety Gate?

Must this Policy be revalidated at runtime?

If this Policy fails, should the system reject, hold, escalate, or block?

In other words, `policy_registry` is the core deterministic registry that controls **“whether this action is allowed under the rules”** in the LEDO system.

---

## **2\. Core Principle**

Policy defines permission conditions and prohibition conditions.

Policy is not Identity.

Policy is not Approval.

Policy is not Decision.

Policy is not the Safety Gate.

Policy is not an ExecutionRequest.

Policy is not a Physical Command.

The basic meaning of Policy is:

Is this action allowed?

Is this action prohibited?

Does this action require additional evidence?

Does this action require higher-level approval?

Is this action exceptionally allowed under emergency conditions?

Must this action be revalidated at runtime?

The core principle is:

Identity proves who.

Policy decides whether allowed.

Decision evaluates what should happen.

Approval authorizes within policy.

Safety Gate validates runtime execution readiness.

ExecutionRequest prepares external execution.

External System performs physical execution.

The important distinction is:

Policy pass ≠ Approval pass

Approval pass ≠ Safety Gate pass

Safety Gate pass ≠ Physical execution

Even if Policy passes, Approval may still be required.

Even if Approval exists, execution must not proceed if runtime conditions fail at the Safety Gate.

---

## **3\. Position in the LEDO Architecture**

`policy_registry` belongs to the Governance / Policy / Security Layer, but it is also a cross-cutting registry used across the entire LEDO lifecycle.

Identity / Event / Evidence / ActionCandidate

        ↓

Policy Lookup

        ↓

Policy Evaluation

        ↓

allow / deny / hold / escalate / require\_approval / require\_revalidation

        ↓

Decision / Approval / Safety Gate / Execution

Its position in the full system flow is as follows:

Agent Output

    ↓

ActionCandidate

    ↓

action\_registry validation

    ↓

decision\_registry evaluation

    ↓

policy\_registry evaluation

    ↓

approval\_registry routing

    ↓

ApprovedAction

    ↓

Safety Gate runtime policy check

    ↓

ExecutionRequest

`policy_registry` answers the following questions:

Is this ActionCandidate allowed by policy?

Is this Identity allowed to propose this Action?

Can this Approver approve under these conditions?

Is this Evidence sufficient under the policy?

Can an ExecutionRequest be created under the current runtime state?

Can a request be sent to this External System?

---

## **4\. Purpose**

The purpose of `policy_registry` is to ensure the following:

1. Prevent the use of unregistered Policies  
2. Define Policy Types and Policy Rules  
3. Define permission conditions  
4. Define prohibition conditions  
5. Define constraints  
6. Define Identity / Role / Scope / Certification conditions  
7. Define applicable scopes for Action / Event / Evidence / Decision / Approval  
8. Define emergency override policies  
9. Define escalation policies  
10. Define runtime revalidation policies  
11. Define fail-safe / fallback policies  
12. Standardize Policy Evaluation Results  
13. Define integration with OPA/Rego or Rule Engines  
14. Manage Policy versioning and migration  
15. Manage Policy change audit  
16. Prevent Agents, Models, Humans, and Services from bypassing policy boundaries

---

## **5\. Core Distinctions**

### **5.1 Policy Type**

`Policy Type` is the kind of policy.

Recommended values:

ACCESS\_POLICY

SAFETY\_POLICY

ACTION\_POLICY

APPROVAL\_POLICY

DECISION\_POLICY

EVIDENCE\_POLICY

EXECUTION\_POLICY

EXTERNAL\_SYSTEM\_POLICY

DATA\_POLICY

PRIVACY\_POLICY

COMPLIANCE\_POLICY

EMERGENCY\_POLICY

ESCALATION\_POLICY

RUNTIME\_VALIDATION\_POLICY

FALLBACK\_POLICY

AUDIT\_POLICY

---

### **5.2 Policy Rule**

`Policy Rule` is the actual policy unit that contains conditions and effects.

Examples:

stop\_work\_policy\_v1

robot\_dispatch\_policy\_v1

worker\_location\_privacy\_policy\_v1

external\_system\_access\_policy\_v1

emergency\_override\_policy\_v1

A Policy Rule defines: “Under which conditions is this allowed / denied / held / escalated?”

---

### **5.3 Policy Condition**

`Policy Condition` is a condition used in policy evaluation.

Examples:

actor\_has\_role

actor\_has\_certification

actor\_within\_site\_scope

risk\_class\_at\_least\_high

evidence\_bundle\_complete

worker\_location\_fresh

external\_system\_healthy

safety\_gate\_required

approval\_required

---

### **5.4 Policy Effect**

`Policy Effect` is the result of policy evaluation.

Recommended values:

allow

deny

hold

escalate

require\_approval

require\_more\_evidence

require\_runtime\_revalidation

require\_manual\_review

block

The important point is that `allow` does not mean execution.

allow \= permitted under policy

approve \= authorized by an approver

execute \= may be sent as an execution request to an external system

---

### **5.5 Policy Scope**

`Policy Scope` is the boundary to which the policy applies.

Examples:

site\_scope

zone\_scope

operation\_scope

equipment\_scope

worker\_group\_scope

identity\_scope

action\_scope

risk\_scope

time\_scope

system\_scope

A policy without scope is dangerous.

---

### **5.6 Policy Priority**

Policies may conflict with one another, so priority is required.

Recommended priorities:

human\_safety

legal\_compliance

security

robot\_safety

equipment\_protection

operational\_continuity

productivity

cost\_efficiency

Core principle:

Human safety policy overrides productivity policy.

Legal compliance overrides operational convenience.

Safety-critical block overrides model recommendation.

---

## **6\. Scope**

`policy_registry` controls the following fields:

policy\_id: string

canonical\_name: string

display\_name: string

description: string

semantic\_iri: string

policy\_type: string

policy\_category: string

version: string

status: draft | active | deprecated | migration\_required | retired | blocked

applicable\_identity\_type\_refs:

  \- string

applicable\_role\_refs:

  \- string

applicable\_action\_type\_refs:

  \- string

applicable\_event\_type\_refs:

  \- string

applicable\_evidence\_type\_refs:

  \- string

applicable\_decision\_rule\_refs:

  \- string

applicable\_approval\_rule\_refs:

  \- string

applicable\_external\_system\_refs:

  \- string

applicable\_site\_scope:

  \- string

applicable\_zone\_scope:

  \- string

condition\_refs:

  \- string

constraint\_refs:

  \- string

required\_identity\_attribute\_refs:

  \- string

required\_certification\_refs:

  \- string

required\_evidence\_refs:

  \- string

required\_runtime\_validation\_refs:

  \- string

policy\_engine\_ref: string

policy\_language: rego | python\_rule | decision\_table | dmn | shacl | custom\_rule

policy\_artifact\_ref: string

default\_effect: allow | deny | hold | escalate | block

allowed\_effects:

  \- string

failure\_effect: deny | hold | escalate | require\_more\_evidence | block

priority\_level: human\_safety | legal\_compliance | security | robot\_safety | equipment\_protection | operational\_continuity | productivity | cost\_efficiency

runtime\_evaluation\_required: boolean

pre\_approval\_evaluation\_required: boolean

pre\_execution\_evaluation\_required: boolean

emergency\_override\_allowed: boolean

emergency\_override\_policy\_ref: string | null

fallback\_policy\_ref: string | null

escalation\_policy\_ref: string | null

decision\_boundary: string

approval\_boundary: string

execution\_boundary: string

safety\_boundary: string

audit\_required: boolean

audit\_event\_refs:

  \- string

owner\_module: string

owner\_team: string

source\_document: string

created\_at: datetime

updated\_at: datetime

deprecated\_since: datetime | null

replacement\_policy\_id: string | null

---

## **7\. Non-Scope**

`policy_registry` does not directly define the following:

1. Raw user identity records  
2. Actual passwords / tokens / secrets  
3. ApprovalDecision itself  
4. The complete DecisionCase judgment procedure  
5. Final Safety Gate runtime result  
6. Physical Command  
7. PLC / SCADA / Robot low-level control  
8. Complete Event payload schemas  
9. Complete Evidence payload schemas  
10. External System adapter implementation  
11. Full legal document text  
12. All site-specific domain threshold values  
13. Complete UI access screen configuration

These responsibilities belong to the following modules:

identity\_registry

access\_control\_registry

approval\_registry

decision\_registry

safety\_gate

event\_registry

evidence\_registry

adapter\_registry

external\_system\_registry

legal\_compliance\_module

domain\_module

vault / secret\_manager

`policy_registry` defines the operational contract of a policy.

Actual policy execution may be performed by a `policy_engine`, `OPA/Rego`, `Rule Engine`, `Decision Table`, or `SHACL Validator`.

---

## **8\. Policy Category Model**

Recommended Policy Categories are:

ACCESS\_POLICY

SAFETY\_POLICY

ACTION\_POLICY

APPROVAL\_POLICY

DECISION\_POLICY

EVIDENCE\_POLICY

EXECUTION\_POLICY

EXTERNAL\_SYSTEM\_POLICY

DATA\_POLICY

PRIVACY\_POLICY

COMPLIANCE\_POLICY

EMERGENCY\_POLICY

ESCALATION\_POLICY

RUNTIME\_VALIDATION\_POLICY

FALLBACK\_POLICY

AUDIT\_POLICY

### **8.1 ACCESS\_POLICY**

Defines who can access what.

Examples:

safety\_dashboard\_access\_policy

approval\_ui\_access\_policy

world\_state\_read\_policy

audit\_log\_access\_policy

---

### **8.2 SAFETY\_POLICY**

A policy related to site safety.

Examples:

stop\_work\_policy

hazard\_zone\_entry\_policy

worker\_proximity\_policy

ppe\_required\_policy

---

### **8.3 ACTION\_POLICY**

Defines under which conditions an ActionCandidate or Action Type is allowed.

Examples:

dispatch\_robot\_policy

lock\_zone\_policy

request\_inspection\_policy

notify\_manager\_policy

---

### **8.4 APPROVAL\_POLICY**

Defines conditions for ApprovalRequest and ApprovalDecision.

Examples:

stop\_work\_approval\_policy

robot\_dispatch\_approval\_policy

emergency\_override\_approval\_policy

---

### **8.5 EXECUTION\_POLICY**

Defines conditions for ExecutionRequest creation and external system delivery.

Examples:

execution\_dispatch\_policy

external\_control\_request\_policy

robot\_mission\_execution\_policy

---

### **8.6 DATA\_POLICY**

Defines data access, storage, transmission, and retention conditions.

Examples:

worker\_location\_data\_policy

sensor\_data\_retention\_policy

audit\_data\_retention\_policy

---

### **8.7 PRIVACY\_POLICY**

Defines conditions for processing PII, personal data, and sensitive information.

Examples:

worker\_location\_privacy\_policy

identity\_pii\_masking\_policy

external\_api\_pii\_transfer\_policy

---

### **8.8 EMERGENCY\_POLICY**

Defines conditions that are applied differently from normal policy during emergencies.

Examples:

emergency\_stop\_policy

emergency\_evacuation\_policy

emergency\_override\_policy

Emergency policy is powerful, but it must not be unlimited.

---

## **9\. Registry Entry Schema**

Each Policy Registry entry follows this structure:

policy\_id: string

canonical\_name: string

display\_name: string

description: string

semantic\_iri: string

policy\_type: string

policy\_category: string

version: string

status: draft | active | deprecated | migration\_required | retired | blocked

applicable\_identity\_type\_refs:

  \- string

applicable\_role\_refs:

  \- string

applicable\_action\_type\_refs:

  \- string

applicable\_event\_type\_refs:

  \- string

applicable\_evidence\_type\_refs:

  \- string

applicable\_decision\_rule\_refs:

  \- string

applicable\_approval\_rule\_refs:

  \- string

applicable\_external\_system\_refs:

  \- string

applicable\_site\_scope:

  \- string

applicable\_zone\_scope:

  \- string

condition\_refs:

  \- string

constraint\_refs:

  \- string

required\_identity\_attribute\_refs:

  \- string

required\_certification\_refs:

  \- string

required\_evidence\_refs:

  \- string

required\_runtime\_validation\_refs:

  \- string

policy\_engine\_ref: string

policy\_language: string

policy\_artifact\_ref: string

default\_effect: string

allowed\_effects:

  \- string

failure\_effect: string

priority\_level: string

runtime\_evaluation\_required: boolean

pre\_approval\_evaluation\_required: boolean

pre\_execution\_evaluation\_required: boolean

emergency\_override\_allowed: boolean

emergency\_override\_policy\_ref: string | null

fallback\_policy\_ref: string | null

escalation\_policy\_ref: string | null

decision\_boundary: string

approval\_boundary: string

execution\_boundary: string

safety\_boundary: string

audit\_required: boolean

audit\_event\_refs:

  \- string

owner\_module: string

owner\_team: string

source\_document: string

created\_at: datetime

updated\_at: datetime

deprecated\_since: datetime | null

replacement\_policy\_id: string | null

---

## **10\. Registry Entry Example: STOP\_WORK Policy**

policy\_id: policy:stop\_work\_policy\_v1

canonical\_name: stop\_work\_policy\_v1

display\_name: STOP\_WORK Policy

description: A safety policy that allows STOP\_WORK ActionCandidates and ApprovalRequests under high-risk or emergency hazard conditions.

semantic\_iri: ledo:StopWorkPolicy

policy\_type: SAFETY\_POLICY

policy\_category: ACTION\_POLICY

version: 1.0.0

status: active

applicable\_identity\_type\_refs:

  \- identity\_type:HUMAN\_IDENTITY

  \- identity\_type:AGENT\_IDENTITY

applicable\_role\_refs:

  \- role:safety\_supervisor

  \- role:site\_supervisor

  \- role:safety\_risk\_agent

applicable\_action\_type\_refs:

  \- action:STOP\_WORK

applicable\_event\_type\_refs:

  \- event:HazardDetected

  \- event:WorkerEnteredHazardZone

  \- event:EmergencyConditionDetected

applicable\_evidence\_type\_refs:

  \- evidence:hazard\_detection\_snapshot

  \- evidence:worker\_location\_snapshot

  \- evidence:risk\_assessment\_snapshot

  \- evidence:sensor\_freshness\_snapshot

applicable\_decision\_rule\_refs:

  \- decision:stop\_work\_safety\_risk\_v1

applicable\_approval\_rule\_refs:

  \- approval:stop\_work\_safety\_supervisor\_v1

applicable\_external\_system\_refs: \[\]

applicable\_site\_scope:

  \- "\*"

applicable\_zone\_scope:

  \- "\*"

condition\_refs:

  \- condition:risk\_class\_high\_or\_above

  \- condition:evidence\_bundle\_complete

  \- condition:worker\_exposure\_detected

constraint\_refs:

  \- constraint:human\_safety\_priority

  \- constraint:no\_direct\_execution\_without\_safety\_gate

required\_identity\_attribute\_refs:

  \- attribute:active\_identity

required\_certification\_refs:

  \- certification:construction\_safety\_supervisor\_certification

required\_evidence\_refs:

  \- evidence:hazard\_detection\_snapshot

  \- evidence:worker\_location\_snapshot

  \- evidence:risk\_assessment\_snapshot

required\_runtime\_validation\_refs:

  \- runtime\_validation:hazard\_still\_present

  \- runtime\_validation:worker\_location\_fresh

  \- runtime\_validation:zone\_status\_valid

policy\_engine\_ref: policy\_engine:opa

policy\_language: rego

policy\_artifact\_ref: artifact:stop\_work\_policy\_rego\_v1

default\_effect: hold

allowed\_effects:

  \- allow

  \- deny

  \- hold

  \- escalate

  \- require\_approval

  \- require\_runtime\_revalidation

  \- block

failure\_effect: block

priority\_level: human\_safety

runtime\_evaluation\_required: true

pre\_approval\_evaluation\_required: true

pre\_execution\_evaluation\_required: true

emergency\_override\_allowed: true

emergency\_override\_policy\_ref: policy:emergency\_override\_policy\_v1

fallback\_policy\_ref: fallback:stop\_work\_policy\_fallback\_v1

escalation\_policy\_ref: escalation:safety\_supervisor\_escalation\_v1

decision\_boundary: may\_allow\_stop\_work\_decision\_to\_proceed\_to\_approval

approval\_boundary: policy\_pass\_does\_not\_grant\_approval

execution\_boundary: policy\_pass\_does\_not\_create\_execution\_request

safety\_boundary: safety\_gate\_must\_revalidate\_runtime\_conditions

audit\_required: true

audit\_event\_refs:

  \- audit:policy\_evaluated

  \- audit:policy\_failed

  \- audit:policy\_allowed

  \- audit:policy\_blocked

  \- audit:policy\_escalated

owner\_module: governance\_policy\_module

owner\_team: LEDO Safety Governance

source\_document: stop\_work\_policy\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_policy\_id: null

---

## **11\. Registry Entry Example: Robot Dispatch Policy**

policy\_id: policy:robot\_dispatch\_policy\_v1

canonical\_name: robot\_dispatch\_policy\_v1

display\_name: Robot Dispatch Policy

description: A policy that defines the conditions under which robot dispatch ActionCandidates and ExecutionRequests are allowed.

semantic\_iri: ledo:RobotDispatchPolicy

policy\_type: ACTION\_POLICY

policy\_category: EXECUTION\_POLICY

version: 1.0.0

status: active

applicable\_identity\_type\_refs:

  \- identity\_type:HUMAN\_IDENTITY

  \- identity\_type:AGENT\_IDENTITY

  \- identity\_type:SERVICE\_IDENTITY

applicable\_role\_refs:

  \- role:robot\_operations\_manager

  \- role:site\_supervisor

  \- role:robot\_dispatch\_agent

  \- role:execution\_service

applicable\_action\_type\_refs:

  \- action:DISPATCH\_ROBOT

  \- action:REPLAN\_ROUTE

  \- action:PAUSE\_MISSION

  \- action:RETURN\_TO\_BASE

applicable\_event\_type\_refs:

  \- event:RobotStatusUpdated

  \- event:WorkerLocationUpdated

  \- event:ZoneStatusChanged

  \- event:RobotMissionStateChanged

applicable\_evidence\_type\_refs:

  \- evidence:robot\_availability\_snapshot

  \- evidence:worker\_location\_snapshot

  \- evidence:zone\_accessibility\_snapshot

  \- evidence:mission\_context\_snapshot

applicable\_decision\_rule\_refs:

  \- decision:dispatch\_robot\_v1

applicable\_approval\_rule\_refs:

  \- approval:dispatch\_robot\_supervisor\_v1

applicable\_external\_system\_refs:

  \- external\_system:robot\_fleet\_manager\_site\_A

applicable\_site\_scope:

  \- site\_A

applicable\_zone\_scope:

  \- zone\_01

  \- zone\_02

  \- zone\_03

condition\_refs:

  \- condition:robot\_available

  \- condition:worker\_not\_in\_robot\_path

  \- condition:zone\_accessible

  \- condition:fleet\_manager\_healthy

constraint\_refs:

  \- constraint:no\_robot\_dispatch\_into\_hazard\_zone

  \- constraint:no\_low\_level\_motion\_command\_from\_LEDO

  \- constraint:external\_fleet\_manager\_required

required\_identity\_attribute\_refs:

  \- attribute:active\_identity

  \- attribute:site\_scoped

required\_certification\_refs:

  \- certification:robot\_operation\_supervisor\_training

required\_evidence\_refs:

  \- evidence:robot\_availability\_snapshot

  \- evidence:worker\_location\_snapshot

  \- evidence:zone\_accessibility\_snapshot

required\_runtime\_validation\_refs:

  \- runtime\_validation:robot\_available

  \- runtime\_validation:worker\_not\_in\_path

  \- runtime\_validation:external\_system\_reachable

  \- runtime\_validation:adapter\_health\_valid

policy\_engine\_ref: policy\_engine:opa

policy\_language: rego

policy\_artifact\_ref: artifact:robot\_dispatch\_policy\_rego\_v1

default\_effect: hold

allowed\_effects:

  \- allow

  \- deny

  \- hold

  \- escalate

  \- require\_approval

  \- require\_runtime\_revalidation

  \- block

failure\_effect: hold

priority\_level: robot\_safety

runtime\_evaluation\_required: true

pre\_approval\_evaluation\_required: true

pre\_execution\_evaluation\_required: true

emergency\_override\_allowed: false

emergency\_override\_policy\_ref: null

fallback\_policy\_ref: fallback:robot\_dispatch\_unavailable\_fallback\_v1

escalation\_policy\_ref: escalation:robot\_operations\_manager\_escalation\_v1

decision\_boundary: may\_allow\_robot\_dispatch\_decision\_to\_proceed\_to\_approval

approval\_boundary: policy\_pass\_does\_not\_grant\_approval

execution\_boundary: policy\_pass\_does\_not\_dispatch\_robot

safety\_boundary: safety\_gate\_and\_fleet\_manager\_must\_validate\_before\_execution

audit\_required: true

audit\_event\_refs:

  \- audit:policy\_evaluated

  \- audit:robot\_policy\_allowed

  \- audit:robot\_policy\_blocked

  \- audit:robot\_policy\_escalated

owner\_module: governance\_policy\_module

owner\_team: LEDO Robot Governance

source\_document: robot\_dispatch\_policy\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_policy\_id: null

---

## **12\. Registry Entry Example: Worker Location Privacy Policy**

policy\_id: policy:worker\_location\_privacy\_policy\_v1

canonical\_name: worker\_location\_privacy\_policy\_v1

display\_name: Worker Location Privacy Policy

description: A privacy policy that restricts the collection, access, use, storage, and external transfer of worker location data.

semantic\_iri: ledo:WorkerLocationPrivacyPolicy

policy\_type: PRIVACY\_POLICY

policy\_category: DATA\_POLICY

version: 1.0.0

status: active

applicable\_identity\_type\_refs:

  \- identity\_type:HUMAN\_IDENTITY

  \- identity\_type:AGENT\_IDENTITY

  \- identity\_type:SERVICE\_IDENTITY

applicable\_role\_refs:

  \- role:safety\_supervisor

  \- role:site\_supervisor

  \- role:safety\_risk\_agent

  \- role:world\_state\_service

  \- role:audit\_service

applicable\_action\_type\_refs:

  \- action:STOP\_WORK

  \- action:LOCK\_ZONE

  \- action:DISPATCH\_ROBOT

  \- action:NOTIFY\_MANAGER

applicable\_event\_type\_refs:

  \- event:WorkerLocationUpdated

  \- event:WorkerEnteredZone

  \- event:WorkerExitedZone

applicable\_evidence\_type\_refs:

  \- evidence:worker\_location\_snapshot

applicable\_decision\_rule\_refs:

  \- decision:stop\_work\_safety\_risk\_v1

  \- decision:dispatch\_robot\_v1

applicable\_approval\_rule\_refs:

  \- approval:stop\_work\_safety\_supervisor\_v1

  \- approval:dispatch\_robot\_supervisor\_v1

applicable\_external\_system\_refs: \[\]

applicable\_site\_scope:

  \- "\*"

applicable\_zone\_scope:

  \- "\*"

condition\_refs:

  \- condition:purpose\_is\_safety\_or\_runtime\_validation

  \- condition:identity\_has\_need\_to\_know

  \- condition:data\_minimization\_required

constraint\_refs:

  \- constraint:no\_unnecessary\_worker\_tracking

  \- constraint:no\_external\_api\_transfer\_without\_policy

  \- constraint:mask\_worker\_identity\_when\_possible

required\_identity\_attribute\_refs:

  \- attribute:active\_identity

required\_certification\_refs: \[\]

required\_evidence\_refs: \[\]

required\_runtime\_validation\_refs: \[\]

policy\_engine\_ref: policy\_engine:opa

policy\_language: rego

policy\_artifact\_ref: artifact:worker\_location\_privacy\_policy\_rego\_v1

default\_effect: deny

allowed\_effects:

  \- allow

  \- deny

  \- hold

  \- escalate

  \- require\_manual\_review

  \- block

failure\_effect: deny

priority\_level: legal\_compliance

runtime\_evaluation\_required: true

pre\_approval\_evaluation\_required: false

pre\_execution\_evaluation\_required: true

emergency\_override\_allowed: true

emergency\_override\_policy\_ref: policy:emergency\_privacy\_override\_policy\_v1

fallback\_policy\_ref: null

escalation\_policy\_ref: escalation:privacy\_officer\_escalation\_v1

decision\_boundary: may\_allow\_worker\_location\_use\_for\_safety\_decision\_only

approval\_boundary: policy\_pass\_does\_not\_grant\_approval

execution\_boundary: policy\_pass\_does\_not\_create\_execution\_request

safety\_boundary: privacy\_policy\_must\_not\_override\_life\_safety\_but\_must\_be\_audited

audit\_required: true

audit\_event\_refs:

  \- audit:privacy\_policy\_evaluated

  \- audit:worker\_location\_accessed

  \- audit:privacy\_policy\_denied

  \- audit:privacy\_override\_used

owner\_module: governance\_policy\_module

owner\_team: LEDO Privacy Governance

source\_document: worker\_location\_privacy\_policy\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_policy\_id: null

---

## **13\. Registry Entry Example: Emergency Override Policy**

policy\_id: policy:emergency\_override\_policy\_v1

canonical\_name: emergency\_override\_policy\_v1

display\_name: Emergency Override Policy

description: Defines emergency override conditions under which normal approvals or certain procedures may be limitedly bypassed for life safety.

semantic\_iri: ledo:EmergencyOverridePolicy

policy\_type: EMERGENCY\_POLICY

policy\_category: SAFETY\_POLICY

version: 1.0.0

status: active

applicable\_identity\_type\_refs:

  \- identity\_type:HUMAN\_IDENTITY

  \- identity\_type:SERVICE\_IDENTITY

applicable\_role\_refs:

  \- role:emergency\_controller

  \- role:safety\_supervisor

  \- role:site\_manager

  \- role:safety\_gate\_service

applicable\_action\_type\_refs:

  \- action:EVACUATE

  \- action:EMERGENCY\_STOP

  \- action:LOCK\_ZONE

  \- action:BROADCAST\_ALERT

applicable\_event\_type\_refs:

  \- event:EmergencyConditionDetected

  \- event:CriticalHazardDetected

  \- event:EvacuationTriggered

applicable\_evidence\_type\_refs:

  \- evidence:emergency\_condition\_snapshot

  \- evidence:hazard\_detection\_snapshot

  \- evidence:worker\_location\_snapshot

applicable\_decision\_rule\_refs:

  \- decision:emergency\_escalation\_decision\_v1

applicable\_approval\_rule\_refs:

  \- approval:emergency\_override\_approval\_v1

applicable\_external\_system\_refs:

  \- external\_system:notification\_gateway\_site\_A

  \- external\_system:safety\_controller\_zone\_03

applicable\_site\_scope:

  \- "\*"

applicable\_zone\_scope:

  \- "\*"

condition\_refs:

  \- condition:risk\_class\_emergency

  \- condition:life\_safety\_immediate\_threat

  \- condition:emergency\_evidence\_available

constraint\_refs:

  \- constraint:override\_must\_be\_audited

  \- constraint:override\_scope\_must\_be\_minimal

  \- constraint:post\_event\_review\_required

  \- constraint:must\_not\_disable\_safety\_rated\_controller

required\_identity\_attribute\_refs:

  \- attribute:active\_identity

required\_certification\_refs:

  \- certification:emergency\_response\_training

required\_evidence\_refs:

  \- evidence:emergency\_condition\_snapshot

required\_runtime\_validation\_refs:

  \- runtime\_validation:emergency\_condition\_present

  \- runtime\_validation:notification\_channel\_available

policy\_engine\_ref: policy\_engine:opa

policy\_language: rego

policy\_artifact\_ref: artifact:emergency\_override\_policy\_rego\_v1

default\_effect: block

allowed\_effects:

  \- allow

  \- deny

  \- escalate

  \- require\_runtime\_revalidation

  \- block

failure\_effect: block

priority\_level: human\_safety

runtime\_evaluation\_required: true

pre\_approval\_evaluation\_required: true

pre\_execution\_evaluation\_required: true

emergency\_override\_allowed: false

emergency\_override\_policy\_ref: null

fallback\_policy\_ref: fallback:emergency\_override\_fallback\_v1

escalation\_policy\_ref: escalation:war\_room\_escalation\_v1

decision\_boundary: may\_allow\_emergency\_decision\_to\_bypass\_normal\_queue

approval\_boundary: may\_reduce\_approval\_steps\_only\_under\_emergency\_rule

execution\_boundary: does\_not\_create\_physical\_command\_directly

safety\_boundary: must\_not\_bypass\_safety\_rated\_hardware\_interlock

audit\_required: true

audit\_event\_refs:

  \- audit:emergency\_policy\_evaluated

  \- audit:emergency\_override\_allowed

  \- audit:emergency\_override\_denied

  \- audit:post\_event\_review\_required

owner\_module: governance\_policy\_module

owner\_team: LEDO Emergency Governance

source\_document: emergency\_override\_policy\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_policy\_id: null

---

## **14\. Policy Lifecycle Alignment**

Policy is connected to the following lifecycle:

Policy Draft Created

        ↓

Ontology Grounding Validation

        ↓

Condition / Constraint Definition

        ↓

Policy Artifact Validation

        ↓

Simulation / Test Evaluation

        ↓

Registry Dependency Impact Analysis

        ↓

Approval for Policy Release

        ↓

Active Policy Version

        ↓

Runtime Policy Evaluation

        ↓

Audit / Monitoring / Migration

        ↓

Deprecation / Retirement

The important point is that an active Policy does not automatically mean `allow` in every situation.

The Policy must be active.

The target Action / Identity / Evidence / Scope must match.

The Policy Engine artifact must be valid.

The Conditions must be satisfied.

The Constraints must not be violated.

If runtime evaluation is required, the Policy must be re-evaluated.

---

## **15\. Validation Rules**

A Policy Registry Entry is valid only when the following conditions are satisfied:

1. `policy_id` exists in the registry.  
2. Its status is `active`.  
3. Policy type is declared.  
4. Policy category is declared.  
5. At least one applicable target is declared.  
6. Condition references are declared.  
7. Constraint references are declared.  
8. Policy engine reference is declared.  
9. Policy language is declared.  
10. Policy artifact reference is declared.  
11. Default effect is declared.  
12. Allowed effects are declared.  
13. Failure effect is declared.  
14. Priority level is declared.  
15. Runtime / pre-approval / pre-execution evaluation requirements are declared.  
16. Decision / approval / execution / safety boundaries are declared.  
17. Audit event references are declared.  
18. Owner module is declared.  
19. Version is valid.  
20. If deprecated, migration metadata exists.

If any of these conditions are missing, the Policy must not be used in the operational lifecycle.

---

## **16\. Runtime Policy Evaluation Validation**

Before evaluating a Policy at runtime, the following validations are required:

Does the Policy exist in the registry?

Is the Policy active?

Does the Policy apply to this action / identity / event / evidence / external system?

Is the Actor identity valid?

Do Role / Scope / Certification conditions match?

Does Required Evidence exist?

Does Required Runtime Validation exist?

Is the Policy Engine artifact available?

Does the Policy input schema match?

Is the Policy output effect included in allowed\_effects?

If Policy evaluation fails, is failure\_effect applied?

Is an audit trace created?

If these conditions are not satisfied, policy evaluation must be handled in a fail-secure manner.

Core principle:

Policy evaluation failure must not silently become allow.

---

## **17\. Policy Effect Rule**

Policy effects must be clearly standardized.

Recommended effects:

allow

deny

hold

escalate

require\_approval

require\_more\_evidence

require\_runtime\_revalidation

require\_manual\_review

block

### **17.1 allow**

Allowed under policy.

However, this does not mean approval or execution.

---

### **17.2 deny**

Denied under policy.

---

### **17.3 hold**

Held because conditions are insufficient.

Examples:

EvidenceBundle is incomplete.

Runtime World State is stale.

External System health status is unknown.

---

### **17.4 escalate**

Escalate to a higher-level actor.

Examples:

risk\_class is critical.

There is a policy conflict.

Approval timeout occurred.

---

### **17.5 require\_approval**

Approval is required to proceed under policy.

---

### **17.6 require\_more\_evidence**

Required evidence is missing.

---

### **17.7 require\_runtime\_revalidation**

Revalidation is required immediately before execution.

---

### **17.8 require\_manual\_review**

Human manual review is required.

---

### **17.9 block**

Hard block.

Used for safety-critical hard failures.

---

## **18\. Policy Priority Rule**

Policy conflicts require priority.

Recommended priority levels:

human\_safety

legal\_compliance

security

robot\_safety

equipment\_protection

operational\_continuity

productivity

cost\_efficiency

Conflict example:

Productivity policy:

    Allow robot dispatch to reduce work delay.

Safety policy:

    Dispatch is prohibited because a worker is in the robot path.

Result:

Safety policy wins.

Robot dispatch is blocked or held.

Core principle:

Higher-priority safety policy overrides lower-priority productivity policy.

---

## **19\. Policy Conflict Rule**

Policy conflicts must be handled explicitly.

Conflict types:

allow\_vs\_deny

allow\_vs\_hold

approval\_required\_vs\_auto\_allow

privacy\_vs\_safety

productivity\_vs\_safety

local\_policy\_vs\_global\_policy

emergency\_policy\_vs\_normal\_policy

Recommended conflict outcomes:

prefer\_deny

prefer\_higher\_priority

require\_manual\_review

escalate

block

use\_emergency\_policy

In safety-critical domains, conflicts must not be silently ignored.

Policy conflict must be visible, auditable, and resolvable.

---

## **20\. Emergency Policy Rule**

Emergency Policy may have higher priority than normal policy.

However, it is not unlimited authority.

Emergency Policy must include the following:

emergency\_condition

allowed\_override\_scope

minimum\_required\_identity

required\_runtime\_evidence

audit\_required

post\_event\_review\_required

valid\_time\_window

Core principle:

Emergency override reduces delay.

Emergency override does not remove audit.

Emergency override does not bypass safety-rated hardware.

---

## **21\. Relationship to Ontology Registry**

`ontology_registry` defines the meaning of concepts referenced by policies.

`policy_registry` defines under which conditions those concepts are allowed.

ontology\_registry:

    Defines the meaning of StopWorkAction, SafetySupervisor, and HazardZone.

policy\_registry:

    Defines under which conditions StopWorkAction is allowed.

Actions, Roles, Evidence, Events, Zones, and Equipment used by Policy must be grounded in an active ontology version.

---

## **22\. Relationship to Identity Registry**

`identity_registry` provides who the actor is and which role/scope/certification the actor has.

`policy_registry` evaluates whether those identity claims satisfy the policy conditions.

identity\_registry:

    human:safety\_supervisor\_001 has safety\_supervisor role and site\_A scope.

policy\_registry:

    STOP\_WORK policy requires site\_A safety\_supervisor certification.

Identity is an input to Policy.

---

## **23\. Relationship to Access Control Registry**

`access_control_registry` defines what can be accessed.

`policy_registry` decides under which conditions access is allowed.

access\_control\_registry:

    safety\_supervisor can access the safety dashboard.

policy\_registry:

    Access is allowed only when the actor is on-shift and site\_scope matches.

Access control is not complete without policy evaluation.

---

## **24\. Relationship to Action Registry**

`action_registry` defines the operational contract of Action Types.

`policy_registry` defines under which conditions those Action Types are allowed.

action\_registry:

    STOP\_WORK is a high-risk safety action.

policy\_registry:

    STOP\_WORK can proceed only when hazard evidence and safety supervisor approval exist.

Even if an Action is registered, it cannot proceed if Policy denies it.

---

## **25\. Relationship to Decision Registry**

`decision_registry` defines judgment procedures.

`policy_registry` evaluates which conditions are allowed / prohibited / escalated during the judgment flow.

decision\_registry:

    STOP\_WORK Decision evaluates risk, evidence, priority, and approval route.

policy\_registry:

    If risk\_class is critical, escalation is required.

Decision must include policy evaluation.

---

## **26\. Relationship to Approval Registry**

`approval_registry` defines who can approve under which conditions.

`policy_registry` verifies whether approval is allowed under the policy.

approval\_registry:

    A safety\_supervisor may approve STOP\_WORK.

policy\_registry:

    That safety\_supervisor must be on-shift and within matching site\_scope.

Core principle:

Approval authority requires Policy pass.

---

## **27\. Relationship to Evidence Registry**

`evidence_registry` defines Evidence Types, freshness, and quality.

`policy_registry` defines which evidence is required for specific policy evaluation.

evidence\_registry:

    hazard\_detection\_snapshot must have confidence \>= 0.80.

policy\_registry:

    STOP\_WORK policy requires hazard\_detection\_snapshot and worker\_location\_snapshot.

If evidence is missing, Policy must not allow.

---

## **28\. Relationship to Event Registry**

Events may trigger policy evaluation.

Example:

HazardDetected

    ↓

STOP\_WORK policy evaluation

    ↓

allow / hold / escalate / block

However, Event itself is not policy pass.

Event triggers evaluation.

Policy decides effect.

---

## **29\. Relationship to Model Adapter Registry**

Model output must pass policy boundaries.

model\_adapter\_registry:

    safety\_slm generates a STOP\_WORK ActionCandidate draft.

policy\_registry:

    Evaluates whether this ActionCandidate is allowed under policy.

Even if a model recommends something, the flow must not proceed if Policy denies it.

Model recommendation ≠ Policy pass

---

## **30\. Relationship to Safety Gate**

Safety Gate performs runtime validation immediately before execution.

`policy_registry` may define policies that must be re-evaluated at the Safety Gate.

Example:

pre\_execution\_evaluation\_required: true

required\_runtime\_validation\_refs:

  \- runtime\_validation:worker\_location\_fresh

  \- runtime\_validation:external\_system\_reachable

Core principle:

Policy may allow earlier.

Safety Gate must re-check runtime conditions before execution.

---

## **31\. Relationship to External System Registry**

A request can be sent to an External System only after policy pass.

external\_system\_registry:

    robot\_fleet\_manager\_site\_A supports DISPATCH\_ROBOT.

policy\_registry:

    Dispatch is allowed only when no worker is in the robot path and the fleet manager is healthy.

External System compatibility and Policy pass are different.

External System compatibility pass ≠ Policy pass

---

## **32\. Relationship to Audit Registry**

Policy evaluation must be auditable.

Audit targets:

policy\_created

policy\_updated

policy\_deprecated

policy\_evaluated

policy\_allowed

policy\_denied

policy\_held

policy\_escalated

policy\_blocked

policy\_conflict\_detected

emergency\_override\_policy\_used

Audit Record should include the following:

policy\_id: string

policy\_version: string

actor\_identity\_id: string

target\_object\_ref: string

input\_context\_ref: string

policy\_effect: string

reason\_codes:

  \- string

trace\_id: string

timestamp: datetime

Core principle:

No policy decision without audit.

---

## **33\. Relationship to OPA / Rego / Rule Engine**

`policy_registry` references policy artifacts.

Actual evaluation may be performed by OPA/Rego, Python Rule Engine, DMN, Decision Tables, SHACL, or similar engines.

Example:

policy\_registry:

    policy\_id: policy:stop\_work\_policy\_v1

    policy\_engine\_ref: policy\_engine:opa

    policy\_language: rego

    policy\_artifact\_ref: artifact:stop\_work\_policy\_rego\_v1

OPA:

    Evaluates the actual Rego policy and returns allow / deny / hold / escalate.

Important distinction:

policy\_registry \= manages policy contracts and metadata

policy\_engine \= executes and evaluates policy

---

## **34\. Versioning and Migration**

Policies must be versioned.

A version change is required when any of the following changes:

1. Policy conditions change  
2. Constraints change  
3. Applicable actions change  
4. Applicable identities / roles change  
5. Applicable evidence changes  
6. Applicable decision rules change  
7. Applicable approval rules change  
8. Default effect changes  
9. Failure effect changes  
10. Priority level changes  
11. Policy artifact changes  
12. Runtime evaluation requirement changes  
13. Emergency override rule changes  
14. Fallback / escalation policy changes  
15. Decision / approval / execution / safety boundaries change

Status values:

draft

active

deprecated

migration\_required

retired

blocked

### **34.1 draft**

A policy under authoring. It must not be used in the operational lifecycle.

### **34.2 active**

A policy that may be evaluated in the operational system.

### **34.3 deprecated**

A policy that is no longer recommended but preserved for migration.

### **34.4 migration\_required**

Registry, rule artifact, and service dependencies must be migrated to a new policy version.

### **34.5 retired**

A policy removed from operational references.

### **34.6 blocked**

A policy prohibited from use due to security, safety, legal, or similar errors.

---

## **35\. Implementation Use**

`policy_registry` is used to generate or validate:

1. `PolicyType` enum  
2. `PolicyStatus` enum  
3. `PolicyEffect` enum  
4. `PolicyPriority` enum  
5. Policy metadata DTO  
6. Policy applicability lookup  
7. Policy artifact lookup  
8. Policy engine routing  
9. Identity condition validation  
10. Evidence requirement lookup  
11. Runtime validation requirement lookup  
12. Approval requirement support  
13. Decision policy evaluation support  
14. Safety Gate policy revalidation  
15. Policy conflict detection  
16. Emergency override lookup  
17. Fallback / escalation lookup  
18. Audit log expectations  
19. Test case generation  
20. Migration rules

Implementation must not use unregistered or inactive policies in the operational lifecycle.

---

## **36\. Recommended Code Structure**

registries/

    policy\_registry/

        policy\_registry.py

        policy\_entry.py

        policy\_type.py

        policy\_status.py

        policy\_effect.py

        policy\_priority.py

        policy\_condition.py

        policy\_constraint.py

        policy\_evaluation.py

        policy\_conflict.py

        policy\_validation.py

        policy\_errors.py

        policy\_loader.py

        policy\_migration.py

    access\_control\_registry/

    identity\_registry/

    ontology\_registry/

    action\_registry/

    event\_registry/

    evidence\_registry/

    decision\_registry/

    approval\_registry/

    runtime\_validation\_registry/

    audit\_event\_registry/

---

## **37\. Minimal Pydantic Model**

from enum import Enum

from pydantic import BaseModel, Field

from typing import Optional

from datetime import datetime

class PolicyStatus(str, Enum):

    DRAFT \= "draft"

    ACTIVE \= "active"

    DEPRECATED \= "deprecated"

    MIGRATION\_REQUIRED \= "migration\_required"

    RETIRED \= "retired"

    BLOCKED \= "blocked"

class PolicyType(str, Enum):

    ACCESS\_POLICY \= "access\_policy"

    SAFETY\_POLICY \= "safety\_policy"

    ACTION\_POLICY \= "action\_policy"

    APPROVAL\_POLICY \= "approval\_policy"

    DECISION\_POLICY \= "decision\_policy"

    EVIDENCE\_POLICY \= "evidence\_policy"

    EXECUTION\_POLICY \= "execution\_policy"

    EXTERNAL\_SYSTEM\_POLICY \= "external\_system\_policy"

    DATA\_POLICY \= "data\_policy"

    PRIVACY\_POLICY \= "privacy\_policy"

    COMPLIANCE\_POLICY \= "compliance\_policy"

    EMERGENCY\_POLICY \= "emergency\_policy"

    ESCALATION\_POLICY \= "escalation\_policy"

    RUNTIME\_VALIDATION\_POLICY \= "runtime\_validation\_policy"

    FALLBACK\_POLICY \= "fallback\_policy"

    AUDIT\_POLICY \= "audit\_policy"

class PolicyEffect(str, Enum):

    ALLOW \= "allow"

    DENY \= "deny"

    HOLD \= "hold"

    ESCALATE \= "escalate"

    REQUIRE\_APPROVAL \= "require\_approval"

    REQUIRE\_MORE\_EVIDENCE \= "require\_more\_evidence"

    REQUIRE\_RUNTIME\_REVALIDATION \= "require\_runtime\_revalidation"

    REQUIRE\_MANUAL\_REVIEW \= "require\_manual\_review"

    BLOCK \= "block"

class PolicyPriority(str, Enum):

    HUMAN\_SAFETY \= "human\_safety"

    LEGAL\_COMPLIANCE \= "legal\_compliance"

    SECURITY \= "security"

    ROBOT\_SAFETY \= "robot\_safety"

    EQUIPMENT\_PROTECTION \= "equipment\_protection"

    OPERATIONAL\_CONTINUITY \= "operational\_continuity"

    PRODUCTIVITY \= "productivity"

    COST\_EFFICIENCY \= "cost\_efficiency"

class PolicyLanguage(str, Enum):

    REGO \= "rego"

    PYTHON\_RULE \= "python\_rule"

    DECISION\_TABLE \= "decision\_table"

    DMN \= "dmn"

    SHACL \= "shacl"

    CUSTOM\_RULE \= "custom\_rule"

class PolicyRegistryEntry(BaseModel):

    policy\_id: str

    canonical\_name: str

    display\_name: str

    description: str

    semantic\_iri: str

    policy\_type: PolicyType

    policy\_category: str

    version: str

    status: PolicyStatus \= PolicyStatus.DRAFT

    applicable\_identity\_type\_refs: list\[str\] \= Field(default\_factory=list)

    applicable\_role\_refs: list\[str\] \= Field(default\_factory=list)

    applicable\_action\_type\_refs: list\[str\] \= Field(default\_factory=list)

    applicable\_event\_type\_refs: list\[str\] \= Field(default\_factory=list)

    applicable\_evidence\_type\_refs: list\[str\] \= Field(default\_factory=list)

    applicable\_decision\_rule\_refs: list\[str\] \= Field(default\_factory=list)

    applicable\_approval\_rule\_refs: list\[str\] \= Field(default\_factory=list)

    applicable\_external\_system\_refs: list\[str\] \= Field(default\_factory=list)

    applicable\_site\_scope: list\[str\] \= Field(default\_factory=list)

    applicable\_zone\_scope: list\[str\] \= Field(default\_factory=list)

    condition\_refs: list\[str\] \= Field(default\_factory=list)

    constraint\_refs: list\[str\] \= Field(default\_factory=list)

    required\_identity\_attribute\_refs: list\[str\] \= Field(default\_factory=list)

    required\_certification\_refs: list\[str\] \= Field(default\_factory=list)

    required\_evidence\_refs: list\[str\] \= Field(default\_factory=list)

    required\_runtime\_validation\_refs: list\[str\] \= Field(default\_factory=list)

    policy\_engine\_ref: str

    policy\_language: PolicyLanguage

    policy\_artifact\_ref: str

    default\_effect: PolicyEffect

    allowed\_effects: list\[PolicyEffect\] \= Field(default\_factory=list)

    failure\_effect: PolicyEffect

    priority\_level: PolicyPriority

    runtime\_evaluation\_required: bool \= False

    pre\_approval\_evaluation\_required: bool \= False

    pre\_execution\_evaluation\_required: bool \= False

    emergency\_override\_allowed: bool \= False

    emergency\_override\_policy\_ref: Optional\[str\] \= None

    fallback\_policy\_ref: Optional\[str\] \= None

    escalation\_policy\_ref: Optional\[str\] \= None

    decision\_boundary: str

    approval\_boundary: str

    execution\_boundary: str

    safety\_boundary: str

    audit\_required: bool \= True

    audit\_event\_refs: list\[str\] \= Field(default\_factory=list)

    owner\_module: str

    owner\_team: str

    source\_document: str

    created\_at: datetime

    updated\_at: datetime

    deprecated\_since: Optional\[datetime\] \= None

    replacement\_policy\_id: Optional\[str\] \= None

---

## **38\. Core Validation Function**

def validate\_policy\_applicability(

    entry: PolicyRegistryEntry,

    action\_type\_ref: str | None,

    identity\_type\_ref: str | None,

    role\_ref: str | None,

    site\_id: str | None,

    zone\_id: str | None,

) \-\> None:

    if entry.status \!= PolicyStatus.ACTIVE:

        raise InvalidPolicyError(

            f"Policy is not active: {entry.policy\_id}"

        )

    if action\_type\_ref is not None:

        if entry.applicable\_action\_type\_refs:

            if action\_type\_ref not in entry.applicable\_action\_type\_refs:

                raise PolicyApplicabilityError(

                    f"Action Type '{action\_type\_ref}' is not applicable to "

                    f"Policy '{entry.policy\_id}'"

                )

    if identity\_type\_ref is not None:

        if entry.applicable\_identity\_type\_refs:

            if identity\_type\_ref not in entry.applicable\_identity\_type\_refs:

                raise PolicyApplicabilityError(

                    f"Identity Type '{identity\_type\_ref}' is not applicable to "

                    f"Policy '{entry.policy\_id}'"

                )

    if role\_ref is not None:

        if entry.applicable\_role\_refs:

            if role\_ref not in entry.applicable\_role\_refs:

                raise PolicyApplicabilityError(

                    f"Role '{role\_ref}' is not applicable to "

                    f"Policy '{entry.policy\_id}'"

                )

    if site\_id is not None:

        if entry.applicable\_site\_scope:

            if site\_id not in entry.applicable\_site\_scope and "\*" not in entry.applicable\_site\_scope:

                raise PolicyScopeViolationError(

                    f"Site '{site\_id}' is not within policy scope"

                )

    if zone\_id is not None:

        if entry.applicable\_zone\_scope:

            if zone\_id not in entry.applicable\_zone\_scope and "\*" not in entry.applicable\_zone\_scope:

                raise PolicyScopeViolationError(

                    f"Zone '{zone\_id}' is not within policy scope"

                )

    if not entry.policy\_engine\_ref:

        raise InvalidPolicyError(

            "policy\_engine\_ref must be declared"

        )

    if not entry.policy\_artifact\_ref:

        raise InvalidPolicyError(

            "policy\_artifact\_ref must be declared"

        )

    if not entry.allowed\_effects:

        raise InvalidPolicyError(

            "allowed\_effects must be declared"

        )

    if entry.default\_effect not in entry.allowed\_effects:

        raise InvalidPolicyError(

            "default\_effect must be included in allowed\_effects"

        )

    if entry.failure\_effect not in entry.allowed\_effects:

        raise InvalidPolicyError(

            "failure\_effect must be included in allowed\_effects"

        )

    if not entry.decision\_boundary:

        raise InvalidPolicyError(

            "decision\_boundary must be declared"

        )

    if not entry.approval\_boundary:

        raise InvalidPolicyError(

            "approval\_boundary must be declared"

        )

    if not entry.execution\_boundary:

        raise InvalidPolicyError(

            "execution\_boundary must be declared"

        )

    if not entry.safety\_boundary:

        raise InvalidPolicyError(

            "safety\_boundary must be declared"

        )

---

## **39\. Test Scenarios**

Required tests:

1\. Reject unregistered Policy.

2\. Reject inactive Policy.

3\. Reject runtime use of deprecated Policy.

4\. Reject blocked Policy.

5\. Reject applicable Action Type mismatch.

6\. Reject applicable Identity Type mismatch.

7\. Reject applicable Role mismatch.

8\. Reject site scope mismatch.

9\. Reject zone scope mismatch.

10\. Reject missing condition reference.

11\. Reject missing constraint reference.

12\. Reject missing policy engine reference.

13\. Reject missing policy artifact reference.

14\. Reject missing default effect.

15\. Reject missing failure effect.

16\. Reject if default effect is not included in allowed\_effects.

17\. Verify that policy evaluation failure is not treated as allow.

18\. Verify conflict handling between privacy policy and safety policy.

19\. Verify emergency override audit creation.

20\. Verify Safety Gate pre-execution policy revalidation.

21\. Verify Policy migration rules.

22\. Verify Policy change audit trace.

---

## **40\. Final Rule**

No registered Policy,

no valid Policy Evaluation.

No active Policy,

no trustworthy permission judgment.

Policy pass is not Approval pass.

Approval pass is not Safety Gate pass.

Safety Gate pass is not Physical Execution.

Policy is not Identity.

Policy is not Decision.

Policy is not Approval.

Policy is not Safety Gate.

Policy is not PhysicalCommand.

Policy defines permission conditions.

Policy Engine evaluates those conditions.

Registry controls whether that Policy is operationally valid.

`policy_registry` is the core deterministic registry that governs the operational validity of every permission, prohibition, hold, escalation, emergency override, and runtime revalidation used in the LEDO system.

This module verifies that every major action attempted by an Agent, Human, Service, Adapter, or External System passes a clearly defined policy basis, and ensures that policy failure is not silently converted into unsafe execution.

The core definition is:

Policy Registry

\= not a list of policy documents,

but an operational contract registry that controls

the type, condition, constraint, applicable scope,

policy engine artifact, effect, priority,

emergency override, fallback, runtime revalidation,

and audit rule of every policy used in LEDO.

# **policy\_registry 설계 보고서**

## **1\. 개요**

`policy_registry`는 LEDO Ontology-Centric Cyber-Physical System에서 사용되는 모든 Policy Type, Policy Rule, Permission Condition, Prohibition Condition, Constraint, Escalation Rule, Emergency Rule, Access Rule, Safety Rule, Compliance Rule, Runtime Policy Reference를 정의하고 통제하는 핵심 레지스트리이다.

이 모듈의 목적은 Agent, Human, Service, Adapter, External System이 수행하려는 모든 주요 행위가 명확한 정책 기준을 통과했는지 검증하는 것이다.

`policy_registry`는 단순한 정책 문서 목록이 아니다.

이 레지스트리는 다음을 정의하는 **정책 의미·조건·허용·금지·제약·우선순위 운영 계약 레지스트리**이다.

어떤 Policy가 존재할 수 있는가?  
이 Policy는 어떤 대상에 적용되는가?  
이 Policy는 무엇을 허용하는가?  
이 Policy는 무엇을 금지하는가?  
이 Policy는 어떤 조건에서 보류 또는 escalation을 요구하는가?  
이 Policy는 어떤 Identity / Role / Scope / Certification을 요구하는가?  
이 Policy는 어떤 Action Type, Event Type, Evidence Type, Decision Rule에 적용되는가?  
이 Policy는 Safety Gate 이전에 평가되어야 하는가?  
이 Policy는 runtime에서 재검증되어야 하는가?  
이 Policy가 실패하면 reject, hold, escalate, block 중 무엇을 해야 하는가?

즉, `policy_registry`는 LEDO 시스템에서 “이 행위가 규칙상 가능한가?”를 결정론적으로 통제하는 핵심 레지스트리이다.

---

## **2\. 핵심 원칙**

Policy는 허용 조건과 금지 조건을 정의한다.

Policy는 Identity가 아니다.

Policy는 Approval이 아니다.

Policy는 Decision이 아니다.

Policy는 Safety Gate가 아니다.

Policy는 ExecutionRequest가 아니다.

Policy는 Physical Command가 아니다.

Policy의 기본 의미는 다음과 같다.

이 행위는 허용되는가?  
이 행위는 금지되는가?  
이 행위는 추가 증거가 필요한가?  
이 행위는 상위 승인자가 필요한가?  
이 행위는 emergency condition에서 예외적으로 허용되는가?  
이 행위는 runtime에서 다시 검증되어야 하는가?

핵심 원칙은 다음과 같다.

Identity proves who.  
Policy decides whether allowed.  
Decision evaluates what should happen.  
Approval authorizes within policy.  
Safety Gate validates runtime execution readiness.  
ExecutionRequest prepares external execution.  
External System performs physical execution.

중요한 구분은 다음이다.

Policy pass ≠ Approval pass  
Approval pass ≠ Safety Gate pass  
Safety Gate pass ≠ Physical execution

Policy가 통과되어도 Approval이 필요할 수 있다.  
Approval이 있어도 Safety Gate에서 runtime 조건이 실패하면 실행하면 안 된다.

---

## **3\. LEDO 아키텍처 내 위치**

`policy_registry`는 Governance / Policy / Security Layer에 위치하지만, LEDO 전체 lifecycle에 걸쳐 사용되는 cross-cutting registry이다.

Identity / Event / Evidence / ActionCandidate  
        ↓  
Policy Lookup  
        ↓  
Policy Evaluation  
        ↓  
allow / deny / hold / escalate / require\_approval / require\_revalidation  
        ↓  
Decision / Approval / Safety Gate / Execution

전체 흐름에서 위치는 다음과 같다.

Agent Output  
    ↓  
ActionCandidate  
    ↓  
action\_registry validation  
    ↓  
decision\_registry evaluation  
    ↓  
policy\_registry evaluation  
    ↓  
approval\_registry routing  
    ↓  
ApprovedAction  
    ↓  
Safety Gate runtime policy check  
    ↓  
ExecutionRequest

`policy_registry`는 다음 질문에 답한다.

이 ActionCandidate는 정책상 가능한가?  
이 Identity는 이 Action을 제안할 수 있는가?  
이 Approver는 이 조건에서 승인할 수 있는가?  
이 Evidence는 정책상 충분한가?  
이 Runtime 상태에서 ExecutionRequest를 만들 수 있는가?  
이 External System으로 요청을 보내도 되는가?

---

## **4\. 목적**

`policy_registry`의 목적은 다음과 같다.

1. 등록되지 않은 정책 사용 방지  
2. Policy Type 및 Policy Rule 정의  
3. 허용 조건 정의  
4. 금지 조건 정의  
5. 제약 조건 정의  
6. Identity / Role / Scope / Certification 조건 정의  
7. Action / Event / Evidence / Decision / Approval 적용 범위 정의  
8. Emergency override policy 정의  
9. Escalation policy 정의  
10. Runtime revalidation policy 정의  
11. Fail-safe / fallback policy 정의  
12. Policy evaluation result 표준화  
13. OPA/Rego 또는 Rule Engine과의 연결 정의  
14. Policy versioning 및 migration 관리  
15. Policy change audit 관리  
16. Agent, Model, Human, Service가 policy boundary를 우회하지 못하도록 방지

---

## **5\. 핵심 구분**

### **5.1 Policy Type**

`Policy Type`은 정책의 종류이다.

권장 값:

ACCESS\_POLICY  
SAFETY\_POLICY  
ACTION\_POLICY  
APPROVAL\_POLICY  
DECISION\_POLICY  
EVIDENCE\_POLICY  
EXECUTION\_POLICY  
EXTERNAL\_SYSTEM\_POLICY  
DATA\_POLICY  
PRIVACY\_POLICY  
COMPLIANCE\_POLICY  
EMERGENCY\_POLICY  
ESCALATION\_POLICY  
RUNTIME\_VALIDATION\_POLICY  
FALLBACK\_POLICY  
AUDIT\_POLICY

---

### **5.2 Policy Rule**

`Policy Rule`은 실제 조건과 결과를 가진 정책 단위이다.

예시:

stop\_work\_policy\_v1  
robot\_dispatch\_policy\_v1  
worker\_location\_privacy\_policy\_v1  
external\_system\_access\_policy\_v1  
emergency\_override\_policy\_v1

Policy Rule은 “어떤 조건이면 허용 / 금지 / 보류 / escalation인가?”를 정의한다.

---

### **5.3 Policy Condition**

`Policy Condition`은 정책 판단에 사용되는 조건이다.

예시:

actor\_has\_role  
actor\_has\_certification  
actor\_within\_site\_scope  
risk\_class\_at\_least\_high  
evidence\_bundle\_complete  
worker\_location\_fresh  
external\_system\_healthy  
safety\_gate\_required  
approval\_required

---

### **5.4 Policy Effect**

`Policy Effect`는 정책 평가 결과이다.

권장 값:

allow  
deny  
hold  
escalate  
require\_approval  
require\_more\_evidence  
require\_runtime\_revalidation  
require\_manual\_review  
block

중요한 점은 `allow`가 곧 실행을 의미하지 않는다는 것이다.

allow \= 정책상 허용 가능  
approve \= 승인자가 승인함  
execute \= 외부 시스템으로 실행 요청 가능

---

### **5.5 Policy Scope**

`Policy Scope`는 정책이 적용되는 범위이다.

예시:

site\_scope  
zone\_scope  
operation\_scope  
equipment\_scope  
worker\_group\_scope  
identity\_scope  
action\_scope  
risk\_scope  
time\_scope  
system\_scope

Scope 없는 정책은 위험하다.

---

### **5.6 Policy Priority**

정책 간 충돌이 있을 수 있으므로 priority가 필요하다.

권장 우선순위:

human\_safety  
legal\_compliance  
security  
robot\_safety  
equipment\_protection  
operational\_continuity  
productivity  
cost\_efficiency

핵심 원칙:

Human safety policy overrides productivity policy.  
Legal compliance overrides operational convenience.  
Safety-critical block overrides model recommendation.

---

## **6\. Scope**

`policy_registry`는 다음 항목을 통제한다.

policy\_id: string  
canonical\_name: string  
display\_name: string  
description: string  
semantic\_iri: string

policy\_type: string  
policy\_category: string

version: string  
status: draft | active | deprecated | migration\_required | retired | blocked

applicable\_identity\_type\_refs:  
  \- string

applicable\_role\_refs:  
  \- string

applicable\_action\_type\_refs:  
  \- string

applicable\_event\_type\_refs:  
  \- string

applicable\_evidence\_type\_refs:  
  \- string

applicable\_decision\_rule\_refs:  
  \- string

applicable\_approval\_rule\_refs:  
  \- string

applicable\_external\_system\_refs:  
  \- string

applicable\_site\_scope:  
  \- string

applicable\_zone\_scope:  
  \- string

condition\_refs:  
  \- string

constraint\_refs:  
  \- string

required\_identity\_attribute\_refs:  
  \- string

required\_certification\_refs:  
  \- string

required\_evidence\_refs:  
  \- string

required\_runtime\_validation\_refs:  
  \- string

policy\_engine\_ref: string  
policy\_language: rego | python\_rule | decision\_table | dmn | shacl | custom\_rule

policy\_artifact\_ref: string

default\_effect: allow | deny | hold | escalate | block

allowed\_effects:  
  \- string

failure\_effect: deny | hold | escalate | require\_more\_evidence | block

priority\_level: human\_safety | legal\_compliance | security | robot\_safety | equipment\_protection | operational\_continuity | productivity | cost\_efficiency

runtime\_evaluation\_required: boolean  
pre\_approval\_evaluation\_required: boolean  
pre\_execution\_evaluation\_required: boolean

emergency\_override\_allowed: boolean  
emergency\_override\_policy\_ref: string | null

fallback\_policy\_ref: string | null  
escalation\_policy\_ref: string | null

decision\_boundary: string  
approval\_boundary: string  
execution\_boundary: string  
safety\_boundary: string

audit\_required: boolean  
audit\_event\_refs:  
  \- string

owner\_module: string  
owner\_team: string  
source\_document: string

created\_at: datetime  
updated\_at: datetime  
deprecated\_since: datetime | null  
replacement\_policy\_id: string | null

---

## **7\. Non-Scope**

`policy_registry`는 다음을 직접 정의하지 않는다.

1. 실제 사용자 identity 원본  
2. 실제 password / token / secret  
3. ApprovalDecision 자체  
4. DecisionCase 판단 절차 전체  
5. Safety Gate 최종 runtime 결과  
6. Physical Command  
7. PLC / SCADA / Robot low-level control  
8. Event payload schema 전체  
9. Evidence payload schema 전체  
10. External System adapter 구현  
11. 모든 법률 문서 원문  
12. 모든 현장 domain threshold 세부값  
13. 모든 UI access 화면 구성

이 책임들은 다음 모듈에 속한다.

identity\_registry  
access\_control\_registry  
approval\_registry  
decision\_registry  
safety\_gate  
event\_registry  
evidence\_registry  
adapter\_registry  
external\_system\_registry  
legal\_compliance\_module  
domain\_module  
vault / secret\_manager

`policy_registry`는 정책의 운영 계약을 정의한다.  
실제 정책 실행은 `policy_engine`, `OPA/Rego`, `Rule Engine`, `Decision Table`, `SHACL Validator`가 수행할 수 있다.

---

## **8\. Policy Category 모델**

권장 Policy Category는 다음과 같다.

ACCESS\_POLICY  
SAFETY\_POLICY  
ACTION\_POLICY  
APPROVAL\_POLICY  
DECISION\_POLICY  
EVIDENCE\_POLICY  
EXECUTION\_POLICY  
EXTERNAL\_SYSTEM\_POLICY  
DATA\_POLICY  
PRIVACY\_POLICY  
COMPLIANCE\_POLICY  
EMERGENCY\_POLICY  
ESCALATION\_POLICY  
RUNTIME\_VALIDATION\_POLICY  
FALLBACK\_POLICY  
AUDIT\_POLICY

### **8.1 ACCESS\_POLICY**

누가 무엇에 접근할 수 있는지 정의한다.

예시:

safety\_dashboard\_access\_policy  
approval\_ui\_access\_policy  
world\_state\_read\_policy  
audit\_log\_access\_policy

---

### **8.2 SAFETY\_POLICY**

현장 안전과 관련된 정책이다.

예시:

stop\_work\_policy  
hazard\_zone\_entry\_policy  
worker\_proximity\_policy  
ppe\_required\_policy

---

### **8.3 ACTION\_POLICY**

ActionCandidate 또는 Action Type이 어떤 조건에서 허용되는지 정의한다.

예시:

dispatch\_robot\_policy  
lock\_zone\_policy  
request\_inspection\_policy  
notify\_manager\_policy

---

### **8.4 APPROVAL\_POLICY**

ApprovalRequest와 ApprovalDecision 조건을 정의한다.

예시:

stop\_work\_approval\_policy  
robot\_dispatch\_approval\_policy  
emergency\_override\_approval\_policy

---

### **8.5 EXECUTION\_POLICY**

ExecutionRequest 생성 및 외부 시스템 전달 조건을 정의한다.

예시:

execution\_dispatch\_policy  
external\_control\_request\_policy  
robot\_mission\_execution\_policy

---

### **8.6 DATA\_POLICY**

데이터 접근, 저장, 전송, retention 조건을 정의한다.

예시:

worker\_location\_data\_policy  
sensor\_data\_retention\_policy  
audit\_data\_retention\_policy

---

### **8.7 PRIVACY\_POLICY**

PII, 개인정보, 민감정보 처리 조건을 정의한다.

예시:

worker\_location\_privacy\_policy  
identity\_pii\_masking\_policy  
external\_api\_pii\_transfer\_policy

---

### **8.8 EMERGENCY\_POLICY**

비상 상황에서 일반 정책과 다르게 적용되는 조건을 정의한다.

예시:

emergency\_stop\_policy  
emergency\_evacuation\_policy  
emergency\_override\_policy

Emergency policy는 강력하지만 무제한이어서는 안 된다.

---

## **9\. Registry Entry Schema**

각 Policy Registry entry는 다음 구조를 따른다.

policy\_id: string  
canonical\_name: string  
display\_name: string  
description: string  
semantic\_iri: string

policy\_type: string  
policy\_category: string

version: string  
status: draft | active | deprecated | migration\_required | retired | blocked

applicable\_identity\_type\_refs:  
  \- string

applicable\_role\_refs:  
  \- string

applicable\_action\_type\_refs:  
  \- string

applicable\_event\_type\_refs:  
  \- string

applicable\_evidence\_type\_refs:  
  \- string

applicable\_decision\_rule\_refs:  
  \- string

applicable\_approval\_rule\_refs:  
  \- string

applicable\_external\_system\_refs:  
  \- string

applicable\_site\_scope:  
  \- string

applicable\_zone\_scope:  
  \- string

condition\_refs:  
  \- string

constraint\_refs:  
  \- string

required\_identity\_attribute\_refs:  
  \- string

required\_certification\_refs:  
  \- string

required\_evidence\_refs:  
  \- string

required\_runtime\_validation\_refs:  
  \- string

policy\_engine\_ref: string  
policy\_language: string  
policy\_artifact\_ref: string

default\_effect: string

allowed\_effects:  
  \- string

failure\_effect: string

priority\_level: string

runtime\_evaluation\_required: boolean  
pre\_approval\_evaluation\_required: boolean  
pre\_execution\_evaluation\_required: boolean

emergency\_override\_allowed: boolean  
emergency\_override\_policy\_ref: string | null

fallback\_policy\_ref: string | null  
escalation\_policy\_ref: string | null

decision\_boundary: string  
approval\_boundary: string  
execution\_boundary: string  
safety\_boundary: string

audit\_required: boolean  
audit\_event\_refs:  
  \- string

owner\_module: string  
owner\_team: string  
source\_document: string

created\_at: datetime  
updated\_at: datetime  
deprecated\_since: datetime | null  
replacement\_policy\_id: string | null

---

## **10\. Registry Entry 예시: STOP\_WORK Policy**

policy\_id: policy:stop\_work\_policy\_v1  
canonical\_name: stop\_work\_policy\_v1  
display\_name: STOP\_WORK Policy  
description: 고위험 또는 긴급 위험 상황에서 STOP\_WORK ActionCandidate와 ApprovalRequest를 허용하기 위한 안전 정책이다.  
semantic\_iri: ledo:StopWorkPolicy

policy\_type: SAFETY\_POLICY  
policy\_category: ACTION\_POLICY

version: 1.0.0  
status: active

applicable\_identity\_type\_refs:  
  \- identity\_type:HUMAN\_IDENTITY  
  \- identity\_type:AGENT\_IDENTITY

applicable\_role\_refs:  
  \- role:safety\_supervisor  
  \- role:site\_supervisor  
  \- role:safety\_risk\_agent

applicable\_action\_type\_refs:  
  \- action:STOP\_WORK

applicable\_event\_type\_refs:  
  \- event:HazardDetected  
  \- event:WorkerEnteredHazardZone  
  \- event:EmergencyConditionDetected

applicable\_evidence\_type\_refs:  
  \- evidence:hazard\_detection\_snapshot  
  \- evidence:worker\_location\_snapshot  
  \- evidence:risk\_assessment\_snapshot  
  \- evidence:sensor\_freshness\_snapshot

applicable\_decision\_rule\_refs:  
  \- decision:stop\_work\_safety\_risk\_v1

applicable\_approval\_rule\_refs:  
  \- approval:stop\_work\_safety\_supervisor\_v1

applicable\_external\_system\_refs: \[\]

applicable\_site\_scope:  
  \- "\*"

applicable\_zone\_scope:  
  \- "\*"

condition\_refs:  
  \- condition:risk\_class\_high\_or\_above  
  \- condition:evidence\_bundle\_complete  
  \- condition:worker\_exposure\_detected

constraint\_refs:  
  \- constraint:human\_safety\_priority  
  \- constraint:no\_direct\_execution\_without\_safety\_gate

required\_identity\_attribute\_refs:  
  \- attribute:active\_identity

required\_certification\_refs:  
  \- certification:construction\_safety\_supervisor\_certification

required\_evidence\_refs:  
  \- evidence:hazard\_detection\_snapshot  
  \- evidence:worker\_location\_snapshot  
  \- evidence:risk\_assessment\_snapshot

required\_runtime\_validation\_refs:  
  \- runtime\_validation:hazard\_still\_present  
  \- runtime\_validation:worker\_location\_fresh  
  \- runtime\_validation:zone\_status\_valid

policy\_engine\_ref: policy\_engine:opa  
policy\_language: rego  
policy\_artifact\_ref: artifact:stop\_work\_policy\_rego\_v1

default\_effect: hold

allowed\_effects:  
  \- allow  
  \- deny  
  \- hold  
  \- escalate  
  \- require\_approval  
  \- require\_runtime\_revalidation  
  \- block

failure\_effect: block

priority\_level: human\_safety

runtime\_evaluation\_required: true  
pre\_approval\_evaluation\_required: true  
pre\_execution\_evaluation\_required: true

emergency\_override\_allowed: true  
emergency\_override\_policy\_ref: policy:emergency\_override\_policy\_v1

fallback\_policy\_ref: fallback:stop\_work\_policy\_fallback\_v1  
escalation\_policy\_ref: escalation:safety\_supervisor\_escalation\_v1

decision\_boundary: may\_allow\_stop\_work\_decision\_to\_proceed\_to\_approval  
approval\_boundary: policy\_pass\_does\_not\_grant\_approval  
execution\_boundary: policy\_pass\_does\_not\_create\_execution\_request  
safety\_boundary: safety\_gate\_must\_revalidate\_runtime\_conditions

audit\_required: true

audit\_event\_refs:  
  \- audit:policy\_evaluated  
  \- audit:policy\_failed  
  \- audit:policy\_allowed  
  \- audit:policy\_blocked  
  \- audit:policy\_escalated

owner\_module: governance\_policy\_module  
owner\_team: LEDO Safety Governance  
source\_document: stop\_work\_policy\_contract\_v1  
created\_at: 2026-06-26T00:00:00Z  
updated\_at: 2026-06-26T00:00:00Z  
deprecated\_since: null  
replacement\_policy\_id: null

---

## **11\. Registry Entry 예시: Robot Dispatch Policy**

policy\_id: policy:robot\_dispatch\_policy\_v1  
canonical\_name: robot\_dispatch\_policy\_v1  
display\_name: Robot Dispatch Policy  
description: 로봇 dispatch ActionCandidate와 ExecutionRequest가 허용되기 위한 정책이다.  
semantic\_iri: ledo:RobotDispatchPolicy

policy\_type: ACTION\_POLICY  
policy\_category: EXECUTION\_POLICY

version: 1.0.0  
status: active

applicable\_identity\_type\_refs:  
  \- identity\_type:HUMAN\_IDENTITY  
  \- identity\_type:AGENT\_IDENTITY  
  \- identity\_type:SERVICE\_IDENTITY

applicable\_role\_refs:  
  \- role:robot\_operations\_manager  
  \- role:site\_supervisor  
  \- role:robot\_dispatch\_agent  
  \- role:execution\_service

applicable\_action\_type\_refs:  
  \- action:DISPATCH\_ROBOT  
  \- action:REPLAN\_ROUTE  
  \- action:PAUSE\_MISSION  
  \- action:RETURN\_TO\_BASE

applicable\_event\_type\_refs:  
  \- event:RobotStatusUpdated  
  \- event:WorkerLocationUpdated  
  \- event:ZoneStatusChanged  
  \- event:RobotMissionStateChanged

applicable\_evidence\_type\_refs:  
  \- evidence:robot\_availability\_snapshot  
  \- evidence:worker\_location\_snapshot  
  \- evidence:zone\_accessibility\_snapshot  
  \- evidence:mission\_context\_snapshot

applicable\_decision\_rule\_refs:  
  \- decision:dispatch\_robot\_v1

applicable\_approval\_rule\_refs:  
  \- approval:dispatch\_robot\_supervisor\_v1

applicable\_external\_system\_refs:  
  \- external\_system:robot\_fleet\_manager\_site\_A

applicable\_site\_scope:  
  \- site\_A

applicable\_zone\_scope:  
  \- zone\_01  
  \- zone\_02  
  \- zone\_03

condition\_refs:  
  \- condition:robot\_available  
  \- condition:worker\_not\_in\_robot\_path  
  \- condition:zone\_accessible  
  \- condition:fleet\_manager\_healthy

constraint\_refs:  
  \- constraint:no\_robot\_dispatch\_into\_hazard\_zone  
  \- constraint:no\_low\_level\_motion\_command\_from\_LEDO  
  \- constraint:external\_fleet\_manager\_required

required\_identity\_attribute\_refs:  
  \- attribute:active\_identity  
  \- attribute:site\_scoped

required\_certification\_refs:  
  \- certification:robot\_operation\_supervisor\_training

required\_evidence\_refs:  
  \- evidence:robot\_availability\_snapshot  
  \- evidence:worker\_location\_snapshot  
  \- evidence:zone\_accessibility\_snapshot

required\_runtime\_validation\_refs:  
  \- runtime\_validation:robot\_available  
  \- runtime\_validation:worker\_not\_in\_path  
  \- runtime\_validation:external\_system\_reachable  
  \- runtime\_validation:adapter\_health\_valid

policy\_engine\_ref: policy\_engine:opa  
policy\_language: rego  
policy\_artifact\_ref: artifact:robot\_dispatch\_policy\_rego\_v1

default\_effect: hold

allowed\_effects:  
  \- allow  
  \- deny  
  \- hold  
  \- escalate  
  \- require\_approval  
  \- require\_runtime\_revalidation  
  \- block

failure\_effect: hold

priority\_level: robot\_safety

runtime\_evaluation\_required: true  
pre\_approval\_evaluation\_required: true  
pre\_execution\_evaluation\_required: true

emergency\_override\_allowed: false  
emergency\_override\_policy\_ref: null

fallback\_policy\_ref: fallback:robot\_dispatch\_unavailable\_fallback\_v1  
escalation\_policy\_ref: escalation:robot\_operations\_manager\_escalation\_v1

decision\_boundary: may\_allow\_robot\_dispatch\_decision\_to\_proceed\_to\_approval  
approval\_boundary: policy\_pass\_does\_not\_grant\_approval  
execution\_boundary: policy\_pass\_does\_not\_dispatch\_robot  
safety\_boundary: safety\_gate\_and\_fleet\_manager\_must\_validate\_before\_execution

audit\_required: true

audit\_event\_refs:  
  \- audit:policy\_evaluated  
  \- audit:robot\_policy\_allowed  
  \- audit:robot\_policy\_blocked  
  \- audit:robot\_policy\_escalated

owner\_module: governance\_policy\_module  
owner\_team: LEDO Robot Governance  
source\_document: robot\_dispatch\_policy\_contract\_v1  
created\_at: 2026-06-26T00:00:00Z  
updated\_at: 2026-06-26T00:00:00Z  
deprecated\_since: null  
replacement\_policy\_id: null

---

## **12\. Registry Entry 예시: Worker Location Privacy Policy**

policy\_id: policy:worker\_location\_privacy\_policy\_v1  
canonical\_name: worker\_location\_privacy\_policy\_v1  
display\_name: Worker Location Privacy Policy  
description: 작업자 위치 데이터의 수집, 조회, 사용, 저장, 외부 전송을 제한하는 privacy policy이다.  
semantic\_iri: ledo:WorkerLocationPrivacyPolicy

policy\_type: PRIVACY\_POLICY  
policy\_category: DATA\_POLICY

version: 1.0.0  
status: active

applicable\_identity\_type\_refs:  
  \- identity\_type:HUMAN\_IDENTITY  
  \- identity\_type:AGENT\_IDENTITY  
  \- identity\_type:SERVICE\_IDENTITY

applicable\_role\_refs:  
  \- role:safety\_supervisor  
  \- role:site\_supervisor  
  \- role:safety\_risk\_agent  
  \- role:world\_state\_service  
  \- role:audit\_service

applicable\_action\_type\_refs:  
  \- action:STOP\_WORK  
  \- action:LOCK\_ZONE  
  \- action:DISPATCH\_ROBOT  
  \- action:NOTIFY\_MANAGER

applicable\_event\_type\_refs:  
  \- event:WorkerLocationUpdated  
  \- event:WorkerEnteredZone  
  \- event:WorkerExitedZone

applicable\_evidence\_type\_refs:  
  \- evidence:worker\_location\_snapshot

applicable\_decision\_rule\_refs:  
  \- decision:stop\_work\_safety\_risk\_v1  
  \- decision:dispatch\_robot\_v1

applicable\_approval\_rule\_refs:  
  \- approval:stop\_work\_safety\_supervisor\_v1  
  \- approval:dispatch\_robot\_supervisor\_v1

applicable\_external\_system\_refs: \[\]

applicable\_site\_scope:  
  \- "\*"

applicable\_zone\_scope:  
  \- "\*"

condition\_refs:  
  \- condition:purpose\_is\_safety\_or\_runtime\_validation  
  \- condition:identity\_has\_need\_to\_know  
  \- condition:data\_minimization\_required

constraint\_refs:  
  \- constraint:no\_unnecessary\_worker\_tracking  
  \- constraint:no\_external\_api\_transfer\_without\_policy  
  \- constraint:mask\_worker\_identity\_when\_possible

required\_identity\_attribute\_refs:  
  \- attribute:active\_identity

required\_certification\_refs: \[\]

required\_evidence\_refs: \[\]

required\_runtime\_validation\_refs: \[\]

policy\_engine\_ref: policy\_engine:opa  
policy\_language: rego  
policy\_artifact\_ref: artifact:worker\_location\_privacy\_policy\_rego\_v1

default\_effect: deny

allowed\_effects:  
  \- allow  
  \- deny  
  \- hold  
  \- escalate  
  \- require\_manual\_review  
  \- block

failure\_effect: deny

priority\_level: legal\_compliance

runtime\_evaluation\_required: true  
pre\_approval\_evaluation\_required: false  
pre\_execution\_evaluation\_required: true

emergency\_override\_allowed: true  
emergency\_override\_policy\_ref: policy:emergency\_privacy\_override\_policy\_v1

fallback\_policy\_ref: null  
escalation\_policy\_ref: escalation:privacy\_officer\_escalation\_v1

decision\_boundary: may\_allow\_worker\_location\_use\_for\_safety\_decision\_only  
approval\_boundary: policy\_pass\_does\_not\_grant\_approval  
execution\_boundary: policy\_pass\_does\_not\_create\_execution\_request  
safety\_boundary: privacy\_policy\_must\_not\_override\_life\_safety\_but\_must\_be\_audited

audit\_required: true

audit\_event\_refs:  
  \- audit:privacy\_policy\_evaluated  
  \- audit:worker\_location\_accessed  
  \- audit:privacy\_policy\_denied  
  \- audit:privacy\_override\_used

owner\_module: governance\_policy\_module  
owner\_team: LEDO Privacy Governance  
source\_document: worker\_location\_privacy\_policy\_contract\_v1  
created\_at: 2026-06-26T00:00:00Z  
updated\_at: 2026-06-26T00:00:00Z  
deprecated\_since: null  
replacement\_policy\_id: null

---

## **13\. Registry Entry 예시: Emergency Override Policy**

policy\_id: policy:emergency\_override\_policy\_v1  
canonical\_name: emergency\_override\_policy\_v1  
display\_name: Emergency Override Policy  
description: 생명 안전을 위해 제한적으로 일반 승인 또는 일부 절차를 우회할 수 있는 emergency override 조건을 정의한다.  
semantic\_iri: ledo:EmergencyOverridePolicy

policy\_type: EMERGENCY\_POLICY  
policy\_category: SAFETY\_POLICY

version: 1.0.0  
status: active

applicable\_identity\_type\_refs:  
  \- identity\_type:HUMAN\_IDENTITY  
  \- identity\_type:SERVICE\_IDENTITY

applicable\_role\_refs:  
  \- role:emergency\_controller  
  \- role:safety\_supervisor  
  \- role:site\_manager  
  \- role:safety\_gate\_service

applicable\_action\_type\_refs:  
  \- action:EVACUATE  
  \- action:EMERGENCY\_STOP  
  \- action:LOCK\_ZONE  
  \- action:BROADCAST\_ALERT

applicable\_event\_type\_refs:  
  \- event:EmergencyConditionDetected  
  \- event:CriticalHazardDetected  
  \- event:EvacuationTriggered

applicable\_evidence\_type\_refs:  
  \- evidence:emergency\_condition\_snapshot  
  \- evidence:hazard\_detection\_snapshot  
  \- evidence:worker\_location\_snapshot

applicable\_decision\_rule\_refs:  
  \- decision:emergency\_escalation\_decision\_v1

applicable\_approval\_rule\_refs:  
  \- approval:emergency\_override\_approval\_v1

applicable\_external\_system\_refs:  
  \- external\_system:notification\_gateway\_site\_A  
  \- external\_system:safety\_controller\_zone\_03

applicable\_site\_scope:  
  \- "\*"

applicable\_zone\_scope:  
  \- "\*"

condition\_refs:  
  \- condition:risk\_class\_emergency  
  \- condition:life\_safety\_immediate\_threat  
  \- condition:emergency\_evidence\_available

constraint\_refs:  
  \- constraint:override\_must\_be\_audited  
  \- constraint:override\_scope\_must\_be\_minimal  
  \- constraint:post\_event\_review\_required  
  \- constraint:must\_not\_disable\_safety\_rated\_controller

required\_identity\_attribute\_refs:  
  \- attribute:active\_identity

required\_certification\_refs:  
  \- certification:emergency\_response\_training

required\_evidence\_refs:  
  \- evidence:emergency\_condition\_snapshot

required\_runtime\_validation\_refs:  
  \- runtime\_validation:emergency\_condition\_present  
  \- runtime\_validation:notification\_channel\_available

policy\_engine\_ref: policy\_engine:opa  
policy\_language: rego  
policy\_artifact\_ref: artifact:emergency\_override\_policy\_rego\_v1

default\_effect: block

allowed\_effects:  
  \- allow  
  \- deny  
  \- escalate  
  \- require\_runtime\_revalidation  
  \- block

failure\_effect: block

priority\_level: human\_safety

runtime\_evaluation\_required: true  
pre\_approval\_evaluation\_required: true  
pre\_execution\_evaluation\_required: true

emergency\_override\_allowed: false  
emergency\_override\_policy\_ref: null

fallback\_policy\_ref: fallback:emergency\_override\_fallback\_v1  
escalation\_policy\_ref: escalation:war\_room\_escalation\_v1

decision\_boundary: may\_allow\_emergency\_decision\_to\_bypass\_normal\_queue  
approval\_boundary: may\_reduce\_approval\_steps\_only\_under\_emergency\_rule  
execution\_boundary: does\_not\_create\_physical\_command\_directly  
safety\_boundary: must\_not\_bypass\_safety\_rated\_hardware\_interlock

audit\_required: true

audit\_event\_refs:  
  \- audit:emergency\_policy\_evaluated  
  \- audit:emergency\_override\_allowed  
  \- audit:emergency\_override\_denied  
  \- audit:post\_event\_review\_required

owner\_module: governance\_policy\_module  
owner\_team: LEDO Emergency Governance  
source\_document: emergency\_override\_policy\_contract\_v1  
created\_at: 2026-06-26T00:00:00Z  
updated\_at: 2026-06-26T00:00:00Z  
deprecated\_since: null  
replacement\_policy\_id: null

---

## **14\. Policy Lifecycle Alignment**

Policy는 다음 lifecycle과 연결된다.

Policy Draft Created  
        ↓  
Ontology Grounding Validation  
        ↓  
Condition / Constraint Definition  
        ↓  
Policy Artifact Validation  
        ↓  
Simulation / Test Evaluation  
        ↓  
Registry Dependency Impact Analysis  
        ↓  
Approval for Policy Release  
        ↓  
Active Policy Version  
        ↓  
Runtime Policy Evaluation  
        ↓  
Audit / Monitoring / Migration  
        ↓  
Deprecation / Retirement

중요한 점은 Policy가 active라고 해서 모든 상황에서 자동 allow가 되는 것이 아니라는 점이다.

Policy가 active여야 한다.  
적용 대상 Action / Identity / Evidence / Scope가 맞아야 한다.  
Policy Engine artifact가 유효해야 한다.  
Condition이 충족되어야 한다.  
Constraint를 위반하지 않아야 한다.  
Runtime evaluation이 필요한 경우 재평가되어야 한다.

---

## **15\. Validation Rules**

Policy Registry Entry는 다음 조건을 만족할 때만 유효하다.

1. `policy_id`가 registry에 존재해야 한다.  
2. status가 `active`이어야 한다.  
3. policy type이 선언되어야 한다.  
4. policy category가 선언되어야 한다.  
5. applicable target이 하나 이상 선언되어야 한다.  
6. condition reference가 선언되어야 한다.  
7. constraint reference가 선언되어야 한다.  
8. policy engine reference가 선언되어야 한다.  
9. policy language가 선언되어야 한다.  
10. policy artifact reference가 선언되어야 한다.  
11. default effect가 선언되어야 한다.  
12. allowed effects가 선언되어야 한다.  
13. failure effect가 선언되어야 한다.  
14. priority level이 선언되어야 한다.  
15. runtime / pre-approval / pre-execution evaluation requirement가 선언되어야 한다.  
16. decision / approval / execution / safety boundary가 선언되어야 한다.  
17. audit event reference가 선언되어야 한다.  
18. owner module이 선언되어야 한다.  
19. version이 유효해야 한다.  
20. deprecated 상태라면 migration metadata가 있어야 한다.

하나라도 누락되면 해당 Policy는 operational lifecycle에 사용되면 안 된다.

---

## **16\. Runtime Policy Evaluation Validation**

Runtime에서 Policy를 평가하기 전에는 다음 검증이 필요하다.

Policy가 registry에 존재하는가?  
Policy가 active 상태인가?  
Policy가 이 action / identity / event / evidence / external system에 적용되는가?  
Actor identity가 유효한가?  
Role / Scope / Certification 조건이 맞는가?  
Required Evidence가 존재하는가?  
Required Runtime Validation이 존재하는가?  
Policy Engine artifact가 사용 가능한가?  
Policy input schema가 맞는가?  
Policy output effect가 allowed\_effects 안에 있는가?  
Policy failure 시 failure\_effect가 적용되는가?  
Audit trace가 생성되는가?

이 조건을 만족하지 못하면 policy evaluation은 fail-secure 방식으로 처리해야 한다.

핵심 원칙:

Policy evaluation failure must not silently become allow.

---

## **17\. Policy Effect Rule**

Policy effect는 명확하게 표준화되어야 한다.

권장 effect:

allow  
deny  
hold  
escalate  
require\_approval  
require\_more\_evidence  
require\_runtime\_revalidation  
require\_manual\_review  
block

### **17.1 allow**

정책상 허용 가능하다.

하지만 이것은 승인이나 실행을 의미하지 않는다.

---

### **17.2 deny**

정책상 거부한다.

---

### **17.3 hold**

조건이 불충분하므로 보류한다.

예시:

EvidenceBundle이 incomplete이다.  
Runtime World State가 stale이다.  
External System health 상태가 unknown이다.

---

### **17.4 escalate**

상위 주체에게 escalation한다.

예시:

risk\_class가 critical이다.  
policy conflict가 있다.  
approval timeout이 발생했다.

---

### **17.5 require\_approval**

정책상 진행하려면 Approval이 필요하다.

---

### **17.6 require\_more\_evidence**

필수 증거가 부족하다.

---

### **17.7 require\_runtime\_revalidation**

실행 직전 다시 검증해야 한다.

---

### **17.8 require\_manual\_review**

사람의 수동 검토가 필요하다.

---

### **17.9 block**

강제 차단한다.

Safety-critical hard fail에 사용한다.

---

## **18\. Policy Priority Rule**

정책 충돌 시 우선순위가 필요하다.

권장 priority:

human\_safety  
legal\_compliance  
security  
robot\_safety  
equipment\_protection  
operational\_continuity  
productivity  
cost\_efficiency

충돌 예시:

Productivity policy:  
    작업 지연을 줄이기 위해 robot dispatch를 허용

Safety policy:  
    worker가 robot path에 있으므로 dispatch 금지

결과:

Safety policy wins.  
Robot dispatch is blocked or held.

핵심 원칙:

Higher-priority safety policy overrides lower-priority productivity policy.

---

## **19\. Policy Conflict Rule**

정책 간 충돌은 명시적으로 처리해야 한다.

충돌 유형:

allow\_vs\_deny  
allow\_vs\_hold  
approval\_required\_vs\_auto\_allow  
privacy\_vs\_safety  
productivity\_vs\_safety  
local\_policy\_vs\_global\_policy  
emergency\_policy\_vs\_normal\_policy

권장 conflict outcome:

prefer\_deny  
prefer\_higher\_priority  
require\_manual\_review  
escalate  
block  
use\_emergency\_policy

Safety-critical domain에서는 conflict를 조용히 무시하면 안 된다.

Policy conflict must be visible, auditable, and resolvable.

---

## **20\. Emergency Policy Rule**

Emergency Policy는 일반 정책보다 높은 우선순위를 가질 수 있다.

하지만 무제한 권한이 아니다.

Emergency Policy는 반드시 다음을 가져야 한다.

emergency\_condition  
allowed\_override\_scope  
minimum\_required\_identity  
required\_runtime\_evidence  
audit\_required  
post\_event\_review\_required  
valid\_time\_window

핵심 원칙:

Emergency override reduces delay.  
Emergency override does not remove audit.  
Emergency override does not bypass safety-rated hardware.

---

## **21\. Relationship to Ontology Registry**

`ontology_registry`는 policy가 참조하는 개념의 의미를 정의한다.

`policy_registry`는 그 개념이 어떤 조건에서 허용되는지 정의한다.

ontology\_registry:  
    StopWorkAction, SafetySupervisor, HazardZone의 의미를 정의한다.

policy\_registry:  
    어떤 조건에서 StopWorkAction이 허용되는지 정의한다.

Policy에서 사용하는 Action, Role, Evidence, Event, Zone, Equipment는 active ontology version에 grounding되어야 한다.

---

## **22\. Relationship to Identity Registry**

`identity_registry`는 actor가 누구인지와 어떤 role/scope/certification을 가지는지 제공한다.

`policy_registry`는 그 identity claim이 조건을 만족하는지 평가한다.

identity\_registry:  
    human:safety\_supervisor\_001은 safety\_supervisor role과 site\_A scope를 가진다.

policy\_registry:  
    STOP\_WORK policy는 site\_A safety\_supervisor certification을 요구한다.

Identity는 Policy의 입력이다.

---

## **23\. Relationship to Access Control Registry**

`access_control_registry`는 무엇에 접근할 수 있는지 정의한다.

`policy_registry`는 어떤 조건에서 접근이 허용되는지 판단한다.

access\_control\_registry:  
    safety\_supervisor는 safety dashboard에 접근 가능하다.

policy\_registry:  
    on\_shift 상태이고 site\_scope가 맞을 때만 접근 가능하다.

Access control은 policy evaluation 없이 완성되지 않는다.

---

## **24\. Relationship to Action Registry**

`action_registry`는 Action Type의 운영 계약을 정의한다.

`policy_registry`는 그 Action Type이 어떤 조건에서 허용되는지 정의한다.

action\_registry:  
    STOP\_WORK는 high-risk safety action이다.

policy\_registry:  
    STOP\_WORK는 hazard evidence와 safety supervisor approval이 있을 때만 진행 가능하다.

Action이 등록되어 있어도 policy가 deny하면 진행할 수 없다.

---

## **25\. Relationship to Decision Registry**

`decision_registry`는 판단 절차를 정의한다.

`policy_registry`는 판단 과정에서 어떤 조건이 허용 / 금지 / escalation인지 평가한다.

decision\_registry:  
    STOP\_WORK Decision은 risk, evidence, priority, approval route를 평가한다.

policy\_registry:  
    risk\_class가 critical이면 escalation이 필요하다.

Decision은 policy evaluation을 포함해야 한다.

---

## **26\. Relationship to Approval Registry**

`approval_registry`는 누가 어떤 조건에서 승인할 수 있는지 정의한다.

`policy_registry`는 approval이 정책상 가능한지 검증한다.

approval\_registry:  
    safety\_supervisor가 STOP\_WORK를 승인할 수 있다.

policy\_registry:  
    해당 safety\_supervisor가 on\_shift이고 site\_scope가 맞아야 한다.

핵심 원칙:

Approval authority requires Policy pass.

---

## **27\. Relationship to Evidence Registry**

`evidence_registry`는 Evidence Type, freshness, quality를 정의한다.

`policy_registry`는 특정 정책 평가에 어떤 evidence가 필요한지 정의한다.

evidence\_registry:  
    hazard\_detection\_snapshot은 confidence \>= 0.80이어야 한다.

policy\_registry:  
    STOP\_WORK policy는 hazard\_detection\_snapshot과 worker\_location\_snapshot을 요구한다.

Evidence가 없으면 policy는 allow하면 안 된다.

---

## **28\. Relationship to Event Registry**

Event는 policy evaluation을 trigger할 수 있다.

예시:

HazardDetected  
    ↓  
STOP\_WORK policy evaluation  
    ↓  
allow / hold / escalate / block

하지만 Event 자체가 policy pass는 아니다.

Event triggers evaluation.  
Policy decides effect.

---

## **29\. Relationship to Model Adapter Registry**

Model output은 policy boundary를 통과해야 한다.

model\_adapter\_registry:  
    safety\_slm이 STOP\_WORK ActionCandidate draft를 생성한다.

policy\_registry:  
    이 ActionCandidate가 정책상 허용 가능한지 평가한다.

모델 추천이 있어도 policy deny이면 진행하면 안 된다.

Model recommendation ≠ Policy pass

---

## **30\. Relationship to Safety Gate**

Safety Gate는 실행 직전 runtime 검증을 수행한다.

`policy_registry`는 Safety Gate에서 다시 평가해야 할 policy를 정의할 수 있다.

예시:

pre\_execution\_evaluation\_required: true  
required\_runtime\_validation\_refs:  
  \- runtime\_validation:worker\_location\_fresh  
  \- runtime\_validation:external\_system\_reachable

핵심 원칙:

Policy may allow earlier.  
Safety Gate must re-check runtime conditions before execution.

---

## **31\. Relationship to External System Registry**

External System으로 요청을 보내려면 policy를 통과해야 한다.

external\_system\_registry:  
    robot\_fleet\_manager\_site\_A는 DISPATCH\_ROBOT을 지원한다.

policy\_registry:  
    worker가 robot path에 없고 fleet manager가 healthy일 때만 dispatch 허용.

External System compatibility와 Policy pass는 다르다.

External System compatibility pass ≠ Policy pass

---

## **32\. Relationship to Audit Registry**

Policy evaluation은 반드시 audit 가능해야 한다.

Audit 대상:

policy\_created  
policy\_updated  
policy\_deprecated  
policy\_evaluated  
policy\_allowed  
policy\_denied  
policy\_held  
policy\_escalated  
policy\_blocked  
policy\_conflict\_detected  
emergency\_override\_policy\_used

Audit Record는 다음을 포함해야 한다.

policy\_id: string  
policy\_version: string  
actor\_identity\_id: string  
target\_object\_ref: string  
input\_context\_ref: string  
policy\_effect: string  
reason\_codes:  
  \- string  
trace\_id: string  
timestamp: datetime

핵심 원칙:

No policy decision without audit.

---

## **33\. Relationship to OPA / Rego / Rule Engine**

`policy_registry`는 policy artifact를 참조한다.

실제 평가는 OPA/Rego, Python Rule Engine, DMN, Decision Table, SHACL 등으로 수행될 수 있다.

예시:

policy\_registry:  
    policy\_id: policy:stop\_work\_policy\_v1  
    policy\_engine\_ref: policy\_engine:opa  
    policy\_language: rego  
    policy\_artifact\_ref: artifact:stop\_work\_policy\_rego\_v1

OPA:  
    실제 Rego policy를 평가하고 allow / deny / hold / escalate를 반환

중요한 구분:

policy\_registry \= 정책 계약과 metadata 관리  
policy\_engine \= 정책 실행 및 평가

---

## **34\. Versioning 및 Migration**

Policy는 반드시 versioning되어야 한다.

다음 항목 중 하나라도 변경되면 version 변경이 필요하다.

1. policy condition 변경  
2. constraint 변경  
3. applicable action 변경  
4. applicable identity / role 변경  
5. applicable evidence 변경  
6. applicable decision rule 변경  
7. applicable approval rule 변경  
8. default effect 변경  
9. failure effect 변경  
10. priority level 변경  
11. policy artifact 변경  
12. runtime evaluation requirement 변경  
13. emergency override rule 변경  
14. fallback / escalation policy 변경  
15. decision / approval / execution / safety boundary 변경

Status 값:

draft  
active  
deprecated  
migration\_required  
retired  
blocked

### **34.1 draft**

작성 중인 policy이다. 운영 lifecycle에 사용하면 안 된다.

### **34.2 active**

운영 시스템에서 평가 가능한 policy이다.

### **34.3 deprecated**

더 이상 권장되지 않지만 migration을 위해 남겨둔 policy이다.

### **34.4 migration\_required**

새 policy version으로 registry, rule artifact, service dependency migration이 필요하다.

### **34.5 retired**

운영 참조에서 제거된 policy이다.

### **34.6 blocked**

보안, 안전, 법적 오류 등으로 사용 금지된 policy이다.

---

## **35\. Implementation Use**

`policy_registry`는 다음을 생성하거나 검증하는 데 사용된다.

1. `PolicyType` enum  
2. `PolicyStatus` enum  
3. `PolicyEffect` enum  
4. `PolicyPriority` enum  
5. Policy metadata DTO  
6. Policy applicability lookup  
7. Policy artifact lookup  
8. Policy engine routing  
9. Identity condition validation  
10. Evidence requirement lookup  
11. Runtime validation requirement lookup  
12. Approval requirement support  
13. Decision policy evaluation support  
14. Safety Gate policy revalidation  
15. Policy conflict detection  
16. Emergency override lookup  
17. Fallback / escalation lookup  
18. Audit log expectation  
19. Test case generation  
20. Migration rules

Implementation은 등록되지 않은 policy나 inactive policy를 operational lifecycle에 사용하면 안 된다.

---

## **36\. 권장 Code Structure**

registries/  
    policy\_registry/  
        policy\_registry.py  
        policy\_entry.py  
        policy\_type.py  
        policy\_status.py  
        policy\_effect.py  
        policy\_priority.py  
        policy\_condition.py  
        policy\_constraint.py  
        policy\_evaluation.py  
        policy\_conflict.py  
        policy\_validation.py  
        policy\_errors.py  
        policy\_loader.py  
        policy\_migration.py

    access\_control\_registry/  
    identity\_registry/  
    ontology\_registry/  
    action\_registry/  
    event\_registry/  
    evidence\_registry/  
    decision\_registry/  
    approval\_registry/  
    runtime\_validation\_registry/  
    audit\_event\_registry/

---

## **37\. Minimal Pydantic Model**

from enum import Enum  
from pydantic import BaseModel, Field  
from typing import Optional  
from datetime import datetime

class PolicyStatus(str, Enum):  
    DRAFT \= "draft"  
    ACTIVE \= "active"  
    DEPRECATED \= "deprecated"  
    MIGRATION\_REQUIRED \= "migration\_required"  
    RETIRED \= "retired"  
    BLOCKED \= "blocked"

class PolicyType(str, Enum):  
    ACCESS\_POLICY \= "access\_policy"  
    SAFETY\_POLICY \= "safety\_policy"  
    ACTION\_POLICY \= "action\_policy"  
    APPROVAL\_POLICY \= "approval\_policy"  
    DECISION\_POLICY \= "decision\_policy"  
    EVIDENCE\_POLICY \= "evidence\_policy"  
    EXECUTION\_POLICY \= "execution\_policy"  
    EXTERNAL\_SYSTEM\_POLICY \= "external\_system\_policy"  
    DATA\_POLICY \= "data\_policy"  
    PRIVACY\_POLICY \= "privacy\_policy"  
    COMPLIANCE\_POLICY \= "compliance\_policy"  
    EMERGENCY\_POLICY \= "emergency\_policy"  
    ESCALATION\_POLICY \= "escalation\_policy"  
    RUNTIME\_VALIDATION\_POLICY \= "runtime\_validation\_policy"  
    FALLBACK\_POLICY \= "fallback\_policy"  
    AUDIT\_POLICY \= "audit\_policy"

class PolicyEffect(str, Enum):  
    ALLOW \= "allow"  
    DENY \= "deny"  
    HOLD \= "hold"  
    ESCALATE \= "escalate"  
    REQUIRE\_APPROVAL \= "require\_approval"  
    REQUIRE\_MORE\_EVIDENCE \= "require\_more\_evidence"  
    REQUIRE\_RUNTIME\_REVALIDATION \= "require\_runtime\_revalidation"  
    REQUIRE\_MANUAL\_REVIEW \= "require\_manual\_review"  
    BLOCK \= "block"

class PolicyPriority(str, Enum):  
    HUMAN\_SAFETY \= "human\_safety"  
    LEGAL\_COMPLIANCE \= "legal\_compliance"  
    SECURITY \= "security"  
    ROBOT\_SAFETY \= "robot\_safety"  
    EQUIPMENT\_PROTECTION \= "equipment\_protection"  
    OPERATIONAL\_CONTINUITY \= "operational\_continuity"  
    PRODUCTIVITY \= "productivity"  
    COST\_EFFICIENCY \= "cost\_efficiency"

class PolicyLanguage(str, Enum):  
    REGO \= "rego"  
    PYTHON\_RULE \= "python\_rule"  
    DECISION\_TABLE \= "decision\_table"  
    DMN \= "dmn"  
    SHACL \= "shacl"  
    CUSTOM\_RULE \= "custom\_rule"

class PolicyRegistryEntry(BaseModel):  
    policy\_id: str  
    canonical\_name: str  
    display\_name: str  
    description: str  
    semantic\_iri: str

    policy\_type: PolicyType  
    policy\_category: str

    version: str  
    status: PolicyStatus \= PolicyStatus.DRAFT

    applicable\_identity\_type\_refs: list\[str\] \= Field(default\_factory=list)  
    applicable\_role\_refs: list\[str\] \= Field(default\_factory=list)  
    applicable\_action\_type\_refs: list\[str\] \= Field(default\_factory=list)  
    applicable\_event\_type\_refs: list\[str\] \= Field(default\_factory=list)  
    applicable\_evidence\_type\_refs: list\[str\] \= Field(default\_factory=list)  
    applicable\_decision\_rule\_refs: list\[str\] \= Field(default\_factory=list)  
    applicable\_approval\_rule\_refs: list\[str\] \= Field(default\_factory=list)  
    applicable\_external\_system\_refs: list\[str\] \= Field(default\_factory=list)

    applicable\_site\_scope: list\[str\] \= Field(default\_factory=list)  
    applicable\_zone\_scope: list\[str\] \= Field(default\_factory=list)

    condition\_refs: list\[str\] \= Field(default\_factory=list)  
    constraint\_refs: list\[str\] \= Field(default\_factory=list)

    required\_identity\_attribute\_refs: list\[str\] \= Field(default\_factory=list)  
    required\_certification\_refs: list\[str\] \= Field(default\_factory=list)  
    required\_evidence\_refs: list\[str\] \= Field(default\_factory=list)  
    required\_runtime\_validation\_refs: list\[str\] \= Field(default\_factory=list)

    policy\_engine\_ref: str  
    policy\_language: PolicyLanguage  
    policy\_artifact\_ref: str

    default\_effect: PolicyEffect  
    allowed\_effects: list\[PolicyEffect\] \= Field(default\_factory=list)  
    failure\_effect: PolicyEffect

    priority\_level: PolicyPriority

    runtime\_evaluation\_required: bool \= False  
    pre\_approval\_evaluation\_required: bool \= False  
    pre\_execution\_evaluation\_required: bool \= False

    emergency\_override\_allowed: bool \= False  
    emergency\_override\_policy\_ref: Optional\[str\] \= None

    fallback\_policy\_ref: Optional\[str\] \= None  
    escalation\_policy\_ref: Optional\[str\] \= None

    decision\_boundary: str  
    approval\_boundary: str  
    execution\_boundary: str  
    safety\_boundary: str

    audit\_required: bool \= True  
    audit\_event\_refs: list\[str\] \= Field(default\_factory=list)

    owner\_module: str  
    owner\_team: str  
    source\_document: str

    created\_at: datetime  
    updated\_at: datetime  
    deprecated\_since: Optional\[datetime\] \= None  
    replacement\_policy\_id: Optional\[str\] \= None

---

## **38\. Core Validation Function**

def validate\_policy\_applicability(  
    entry: PolicyRegistryEntry,  
    action\_type\_ref: str | None,  
    identity\_type\_ref: str | None,  
    role\_ref: str | None,  
    site\_id: str | None,  
    zone\_id: str | None,  
) \-\> None:  
    if entry.status \!= PolicyStatus.ACTIVE:  
        raise InvalidPolicyError(  
            f"Policy is not active: {entry.policy\_id}"  
        )

    if action\_type\_ref is not None:  
        if entry.applicable\_action\_type\_refs:  
            if action\_type\_ref not in entry.applicable\_action\_type\_refs:  
                raise PolicyApplicabilityError(  
                    f"Action Type '{action\_type\_ref}' is not applicable to "  
                    f"Policy '{entry.policy\_id}'"  
                )

    if identity\_type\_ref is not None:  
        if entry.applicable\_identity\_type\_refs:  
            if identity\_type\_ref not in entry.applicable\_identity\_type\_refs:  
                raise PolicyApplicabilityError(  
                    f"Identity Type '{identity\_type\_ref}' is not applicable to "  
                    f"Policy '{entry.policy\_id}'"  
                )

    if role\_ref is not None:  
        if entry.applicable\_role\_refs:  
            if role\_ref not in entry.applicable\_role\_refs:  
                raise PolicyApplicabilityError(  
                    f"Role '{role\_ref}' is not applicable to "  
                    f"Policy '{entry.policy\_id}'"  
                )

    if site\_id is not None:  
        if entry.applicable\_site\_scope:  
            if site\_id not in entry.applicable\_site\_scope and "\*" not in entry.applicable\_site\_scope:  
                raise PolicyScopeViolationError(  
                    f"Site '{site\_id}' is not within policy scope"  
                )

    if zone\_id is not None:  
        if entry.applicable\_zone\_scope:  
            if zone\_id not in entry.applicable\_zone\_scope and "\*" not in entry.applicable\_zone\_scope:  
                raise PolicyScopeViolationError(  
                    f"Zone '{zone\_id}' is not within policy scope"  
                )

    if not entry.policy\_engine\_ref:  
        raise InvalidPolicyError(  
            "policy\_engine\_ref must be declared"  
        )

    if not entry.policy\_artifact\_ref:  
        raise InvalidPolicyError(  
            "policy\_artifact\_ref must be declared"  
        )

    if not entry.allowed\_effects:  
        raise InvalidPolicyError(  
            "allowed\_effects must be declared"  
        )

    if entry.default\_effect not in entry.allowed\_effects:  
        raise InvalidPolicyError(  
            "default\_effect must be included in allowed\_effects"  
        )

    if entry.failure\_effect not in entry.allowed\_effects:  
        raise InvalidPolicyError(  
            "failure\_effect must be included in allowed\_effects"  
        )

    if not entry.decision\_boundary:  
        raise InvalidPolicyError(  
            "decision\_boundary must be declared"  
        )

    if not entry.approval\_boundary:  
        raise InvalidPolicyError(  
            "approval\_boundary must be declared"  
        )

    if not entry.execution\_boundary:  
        raise InvalidPolicyError(  
            "execution\_boundary must be declared"  
        )

    if not entry.safety\_boundary:  
        raise InvalidPolicyError(  
            "safety\_boundary must be declared"  
        )

---

## **39\. Test Scenarios**

필수 테스트는 다음과 같다.

1\. 등록되지 않은 Policy 거부  
2\. inactive Policy 거부  
3\. deprecated Policy runtime 사용 거부  
4\. blocked Policy 사용 거부  
5\. applicable Action Type 불일치 거부  
6\. applicable Identity Type 불일치 거부  
7\. applicable Role 불일치 거부  
8\. site scope 불일치 거부  
9\. zone scope 불일치 거부  
10\. condition reference 누락 거부  
11\. constraint reference 누락 거부  
12\. policy engine reference 누락 거부  
13\. policy artifact reference 누락 거부  
14\. default effect 누락 거부  
15\. failure effect 누락 거부  
16\. default effect가 allowed\_effects에 없으면 거부  
17\. policy evaluation failure 시 allow로 처리되지 않는지 검증  
18\. privacy policy와 safety policy conflict 처리 검증  
19\. emergency override audit 생성 검증  
20\. Safety Gate pre-execution policy revalidation 검증  
21\. Policy migration rule 검증  
22\. Policy change audit trace 검증

---

## **40\. Final Rule**

등록된 Policy가 없으면,  
유효한 Policy Evaluation도 없다.

Active Policy가 없으면,  
허용 판단도 신뢰할 수 없다.

Policy pass는 Approval pass가 아니다.

Approval pass는 Safety Gate pass가 아니다.

Safety Gate pass는 Physical Execution이 아니다.

Policy는 Identity가 아니다.  
Policy는 Decision이 아니다.  
Policy는 Approval이 아니다.  
Policy는 Safety Gate가 아니다.  
Policy는 PhysicalCommand가 아니다.

Policy는 허용 조건을 정의한다.  
Policy Engine은 그 조건을 평가한다.  
Registry는 그 Policy가 운영상 유효한지 통제한다.

`policy_registry`는 LEDO 시스템에서 모든 허용, 금지, 보류, escalation, emergency override, runtime revalidation의 운영 유효성을 통제하는 핵심 결정론적 레지스트리이다.

이 모듈은 Agent, Human, Service, Adapter, External System이 수행하려는 모든 주요 행위가 명확한 정책 기준을 통과했는지 검증하고, 정책 실패가 안전하지 않은 실행으로 조용히 변환되지 않도록 보장한다.

핵심 정의는 다음과 같다.

Policy Registry  
\= 정책 문서 목록이 아니라,  
LEDO에서 사용되는 모든 policy의 type, condition,  
constraint, applicable scope, policy engine artifact,  
effect, priority, emergency override, fallback,  
runtime revalidation, audit rule을 통제하는  
정책 운영 계약 레지스트리

