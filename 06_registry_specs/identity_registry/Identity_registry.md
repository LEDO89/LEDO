# **Identity registry**

## **1\. Overview**

`identity_registry` is a core registry in the LEDO Ontology-Centric Cyber-Physical System. It defines and governs all Human Identities, Agent Identities, Service Identities, System Identities, External System Identities, Roles, Attributes, Certifications, Site Assignments, Zone Scopes, Shift Statuses, Delegation Statuses, and Identity Trust Levels used across the system.

The purpose of this module is to ensure that every Action proposal, Decision creation, Approval execution, Safety Gate validation, External System request, and Audit Trace can clearly identify **who performed the action**.

`identity_registry` is not a simple user list.

It is an **operational contract registry for identity, role, attributes, scope, delegation, and traceability** that defines the following:

Who is this actor?

Is this actor a human, agent, service, adapter, device, or external system?

Which roles does this actor have?

In which site and zone is this actor valid?

Is this actor currently on shift or on duty?

Which certifications does this actor have?

Can this actor hold approval authority?

Can this actor propose an ActionCandidate?

What system access may this actor have?

Is this authority delegated or original?

Can this actor's behavior be audited?

In other words, `identity_registry` is the core deterministic registry that controls **"who performed this action, and under what authority?"** in the LEDO system.

---

## **2\. Core Principle**

Identity proves who the actor is.

Identity itself is not authority.

Identity is not Approval.

Identity is not Policy.

Identity is not the Safety Gate.

Identity is not a Physical Command.

The basic meaning of Identity is:

Who performed this action?

Is this actor a human, agent, service, adapter, device, or external system?

Which roles and attributes does this actor have?

Within which site, zone, and shift is this role valid?

Is this actor qualified to approve, review, propose, or request execution?

The core principle is:

No valid Identity,

no trusted action.

No valid Role,

no authority.

No valid Scope,

no approval authority.

No valid Certification,

no safety-critical authority.

Identity proves who.

Policy decides whether.

Approval authorizes.

Safety Gate validates execution readiness.

`identity_registry` provides "who this actor is" and "which attributes this actor has."
The final decision of whether the actor may perform an operation is determined together by `policy_registry`, `approval_registry`, `access_control_registry`, and `safety_gate`.

---

## **3\. Position in the LEDO Architecture**

`identity_registry` belongs to the Governance / Policy / Security Layer, but it is also a cross-cutting registry across the entire LEDO lifecycle.

Human / Agent / Service / External System

        →
identity\_registry validation

        →
Role / Attribute / Scope / Certification verification

        →
Policy Evaluation

        →
Decision / Approval / Execution / Audit

`identity_registry` must be used in the following flows:

Agent Output

    - verify Agent Identity

ActionCandidate

    - verify proposed\_by identity

DecisionCase

    - verify decision actor identity

ApprovalRequest

    - verify approver identity / role / scope / certification

SafetyGatePass or SafetyGateBlock

    - verify validator identity

ExecutionRequest

    - verify service identity / adapter identity

ExternalControlRequest

    - verify external system identity

AuditRecord

    - record all actor identities

---

## **4\. Purpose**

The purpose of `identity_registry` is to ensure the following:

1. Prevent the use of unregistered identities  
2. Distinguish Human / Agent / Service / Adapter / External System / Device identities  
3. Define roles for each identity  
4. Define attributes for each identity  
5. Define site / zone / operation scopes for each identity  
6. Define shift / duty status for each identity  
7. Define certification / training status for each identity  
8. Define identity trust levels  
9. Support approval authority validation  
10. Support agent authority validation  
11. Support service-to-service request validation  
12. Support external system trust validation  
13. Manage delegation and temporary authority  
14. Manage PII and sensitivity rules  
15. Preserve actor traceability in audit records  
16. Manage identity lifecycle and revocation

---

## **5\. Core Distinctions**

### **5.1 Identity**

`Identity` is the unique identity of an actor in the LEDO system.

Examples:

human:safety\_supervisor\_001

human:site\_manager\_001

agent:safety\_risk\_agent\_site\_A

agent:robot\_dispatch\_agent\_site\_A

service:approval\_service

service:execution\_dispatcher

external\_system:robot\_fleet\_manager\_site\_A

adapter:robot\_fleet\_adapter\_site\_A

Identity expresses "who the actor is."

---

### **5.2 Identity Type**

`Identity Type` defines the kind of actor.

Recommended values:

HUMAN\_IDENTITY

AGENT\_IDENTITY

SERVICE\_IDENTITY

ADAPTER\_IDENTITY

EXTERNAL\_SYSTEM\_IDENTITY

DEVICE\_IDENTITY

ORGANIZATION\_IDENTITY

TEMPORARY\_IDENTITY

Each Identity Type has different authority boundaries and validation requirements.

---

### **5.3 Role**

`Role` is the organizational or system role that an identity can perform.

Examples:

worker

operator

site\_supervisor

safety\_supervisor

site\_manager

robot\_operations\_manager

equipment\_manager

compliance\_officer

auditor

domain\_agent

approval\_service

execution\_service

external\_system

Role is an input to authority evaluation.  
However, Role itself is not final authority.

Role → Permission

Role → Approval

Role → Execution Authority

---

### **5.4 Attribute**

`Attribute` represents the current state or condition of an identity.

Examples:

active\_employee

assigned\_to\_site

on\_shift

trained\_for\_robot\_operation

certified\_safety\_supervisor

delegated\_authority\_active

mfa\_verified

service\_account

system\_managed

Attributes are used for ABAC, Approval, and Policy Evaluation.

---

### **5.5 Scope**

Scope is the boundary within which an identity's role or authority is valid.

Recommended scopes:

site\_scope

zone\_scope

operation\_scope

equipment\_scope

worker\_group\_scope

task\_scope

time\_scope

shift\_scope

system\_scope

Example:

site\_scope:

  \- site\_A

zone\_scope:

  \- zone\_01

  \- zone\_02

shift\_scope:

  \- day\_shift

Authority without scope is dangerous.

---

### **5.6 Certification**

`Certification` is a qualification required for specific high-risk work, approval, robot operation, or safety judgment.

Examples:

construction\_safety\_supervisor\_certification

robot\_operation\_supervisor\_training

crane\_operation\_authorization

electrical\_safety\_certification

confined\_space\_work\_certification

emergency\_response\_training

Certification verification is mandatory for safety-critical approval.

---

### **5.7 Delegation**

`Delegation` is the limited transfer of authority from one identity to another.

Example:

When the Safety Supervisor is absent,

the Site Safety Manager may receive delegated safety approval authority

within a specific site and shift scope.

Delegation must include the following:

delegator

delegate

delegated\_role

delegated\_scope

valid\_from

valid\_until

delegation\_policy\_ref

audit\_trace

---

## **6\. Scope**

`identity_registry` controls the following fields:

identity\_id: string

canonical\_name: string

display\_name: string

description: string

semantic\_iri: string

identity\_type: human | agent | service | adapter | external\_system | device | organization | temporary

version: string

status: draft | active | suspended | revoked | expired | deprecated | retired | blocked

auth\_provider\_ref: string | null

external\_subject\_ref: string | null

role\_refs:

  \- string

attribute\_refs:

  \- string

certification\_refs:

  \- string

training\_refs:

  \- string

site\_scope:

  \- string

zone\_scope:

  \- string

operation\_scope:

  \- string

equipment\_scope:

  \- string

system\_scope:

  \- string

shift\_scope:

  \- string

authority\_level: observe\_only | operate | propose\_action | review | approve | administer | service\_execute | external\_system

trust\_level: unverified | basic | verified | privileged | safety\_critical | system\_trusted

mfa\_required: boolean

mfa\_status: unknown | not\_required | required | verified | failed

delegation\_allowed: boolean

delegation\_refs:

  \- string

valid\_from: datetime

valid\_until: datetime | null

pii\_classification: none | indirect | direct | sensitive

sensitivity\_level: internal | confidential | restricted | safety\_critical

access\_control\_refs:

  \- string

policy\_refs:

  \- string

approval\_authority\_refs:

  \- string

allowed\_agent\_type\_refs:

  \- string

allowed\_service\_refs:

  \- string

decision\_boundary: string

approval\_boundary: string

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

replacement\_identity\_id: string | null

---

## **7\. Non-Scope**

`identity_registry` does not define the following:

1. Actual password values  
2. Actual token values  
3. Private key values  
4. Raw biometric data  
5. Complete HR system data  
6. Raw personal data of all workers  
7. Complete policy pass/fail logic  
8. Complete approval rules  
9. Final Safety Gate decision  
10. Low-level physical commands  
11. Adapter execution logic  
12. Complete internal account system of external systems  
13. Complete access control rule set  
14. Complete session management implementation

These responsibilities belong to the following modules or systems:

identity\_provider

access\_control\_registry

policy\_registry

approval\_registry

safety\_gate

vault / secret manager

HR system

IAM / SSO / OIDC provider

audit\_event\_registry

external\_system\_registry

adapter\_registry

`identity_registry` must not store actual passwords or tokens.  
When needed, it should connect to external Identity Providers, IAM, SSO, OIDC, and Vault through references.

---

## **8\. Identity Type Model**

Recommended Identity Types are:

HUMAN\_IDENTITY

AGENT\_IDENTITY

SERVICE\_IDENTITY

ADAPTER\_IDENTITY

EXTERNAL\_SYSTEM\_IDENTITY

DEVICE\_IDENTITY

ORGANIZATION\_IDENTITY

TEMPORARY\_IDENTITY

### **8.1 HUMAN\_IDENTITY**

Represents a human actor.

Examples:

worker

operator

site\_supervisor

safety\_supervisor

site\_manager

compliance\_officer

auditor

Human Identity must consider PII, role, certification, shift, and site assignment.

---

### **8.2 AGENT\_IDENTITY**

Represents an Agent operating inside LEDO or at the edge.

Examples:

agent:safety\_risk\_agent\_site\_A

agent:robot\_dispatch\_agent\_site\_A

agent:inspection\_agent\_site\_A

Agent Identity must be connected to `agent_vocabulary_registry`.

An Agent is not a human and must not become Approval Authority.

---

### **8.3 SERVICE\_IDENTITY**

Represents an internal backend service or runtime component in LEDO.

Examples:

service:decision\_engine

service:approval\_service

service:safety\_gate\_service

service:execution\_dispatcher

Service Identity is used for service-to-service authorization, audit, mTLS, and signed requests.

---

### **8.4 ADAPTER\_IDENTITY**

Represents an internal LEDO external integration adapter.

Examples:

adapter:robot\_fleet\_adapter\_site\_A

adapter:scada\_adapter\_site\_A

adapter:notification\_adapter\_site\_A

Adapter Identity is connected to `adapter_registry`.

---

### **8.5 EXTERNAL\_SYSTEM\_IDENTITY**

Represents the identity of an external system connected to LEDO.

Examples:

external\_system:robot\_fleet\_manager\_site\_A

external\_system:scada\_system\_site\_A

external\_system:bim\_cde\_project\_A

External System Identity is connected to `external_system_registry`.

---

### **8.6 DEVICE\_IDENTITY**

Represents a sensor, gateway, camera, IoT device, PLC gateway, or similar device identity.

Examples:

device:uwb\_tag\_worker\_123

device:camera\_zone\_03

device:gas\_sensor\_01

device:plc\_gateway\_crane\_01

Device Identity is used for event producer and evidence source validation.

---

### **8.7 ORGANIZATION\_IDENTITY**

Represents a company, subcontractor, vendor, or external operating entity.

Examples:

organization:general\_contractor\_A

organization:robot\_vendor\_B

organization:inspection\_company\_C

Organization Identity is connected to ownership, vendor responsibility, liability, and contract scope.

---

### **8.8 TEMPORARY\_IDENTITY**

Represents temporary access authority or an identity valid only for a limited time.

Examples:

temporary:visitor\_inspector\_001

temporary:vendor\_technician\_001

temporary:emergency\_responder\_001

Temporary Identity must always have an expiration time and scope.

---

## **9\. Authority Level Model**

Recommended Authority Levels are:

observe\_only

operate

propose\_action

review

approve

administer

service\_execute

external\_system

### **9.1 observe\_only**

Can only view or observe.

---

### **9.2 operate**

Can perform operational tasks.  
However, this does not mean approval or execution command authority.

---

### **9.3 propose\_action**

Can propose an ActionCandidate.

This is mainly used by Agents or supervisor workflows.

---

### **9.4 review**

Can review DecisionCases, EvidenceBundles, RiskSignals, and related objects.

---

### **9.5 approve**

Can perform an ApprovalDecision.

However, the actor must still satisfy the relevant rule, scope, and certification conditions defined by `approval_registry`.

---

### **9.6 administer**

Can perform administrative functions such as system configuration, registry management, or user management.

---

### **9.7 service\_execute**

Allows an internal service to process system lifecycle objects.

Examples:

decision\_engine

approval\_service

safety\_gate\_service

execution\_dispatcher

---

### **9.8 external\_system**

Allows an external system to provide events, feedback, or execution results.

---

## **10\. Registry Entry Schema**

Each Identity Registry entry follows this structure:

identity\_id: string

canonical\_name: string

display\_name: string

description: string

semantic\_iri: string

identity\_type: string

version: string

status: draft | active | suspended | revoked | expired | deprecated | retired | blocked

auth\_provider\_ref: string | null

external\_subject\_ref: string | null

role\_refs:

  \- string

attribute\_refs:

  \- string

certification\_refs:

  \- string

training\_refs:

  \- string

site\_scope:

  \- string

zone\_scope:

  \- string

operation\_scope:

  \- string

equipment\_scope:

  \- string

system\_scope:

  \- string

shift\_scope:

  \- string

authority\_level: string

trust\_level: string

mfa\_required: boolean

mfa\_status: string

delegation\_allowed: boolean

delegation\_refs:

  \- string

valid\_from: datetime

valid\_until: datetime | null

pii\_classification: string

sensitivity\_level: string

access\_control\_refs:

  \- string

policy\_refs:

  \- string

approval\_authority\_refs:

  \- string

allowed\_agent\_type\_refs:

  \- string

allowed\_service\_refs:

  \- string

decision\_boundary: string

approval\_boundary: string

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

replacement\_identity\_id: string | null

---

## **11\. Registry Entry Example: Safety Supervisor**

identity\_id: human:safety\_supervisor\_001

canonical\_name: safety\_supervisor\_001

display\_name: Safety Supervisor 001

description: A safety manager identity that can perform safety-critical approval and safety review for Site A.

semantic\_iri: ledo:SafetySupervisorIdentity001

identity\_type: HUMAN\_IDENTITY

version: 1.0.0

status: active

auth\_provider\_ref: idp:company\_oidc

external\_subject\_ref: oidc:sub:abc123

role\_refs:

  \- role:safety\_supervisor

  \- role:site\_safety\_manager

attribute\_refs:

  \- attribute:active\_employee

  \- attribute:assigned\_to\_site

  \- attribute:on\_shift

certification\_refs:

  \- certification:construction\_safety\_supervisor\_certification

  \- certification:emergency\_response\_training

training\_refs:

  \- training:stop\_work\_authority\_training

  \- training:site\_safety\_protocol\_training

site\_scope:

  \- site\_A

zone\_scope:

  \- "\*"

operation\_scope:

  \- construction\_operation

  \- safety\_operation

equipment\_scope:

  \- "\*"

system\_scope:

  \- approval\_service

  \- safety\_dashboard

  \- audit\_viewer

shift\_scope:

  \- day\_shift

authority\_level: approve

trust\_level: safety\_critical

mfa\_required: true

mfa\_status: verified

delegation\_allowed: true

delegation\_refs:

  \- delegation:safety\_supervisor\_site\_A\_day\_shift\_v1

valid\_from: 2026-06-26T00:00:00Z

valid\_until: null

pii\_classification: direct

sensitivity\_level: restricted

access\_control\_refs:

  \- access:safety\_supervisor\_access\_policy

policy\_refs:

  \- policy:stop\_work\_policy

  \- policy:safety\_escalation\_policy

approval\_authority\_refs:

  \- approval:stop\_work\_safety\_manager\_v1

  \- approval:lock\_zone\_safety\_supervisor\_v1

allowed\_agent\_type\_refs: \[\]

allowed\_service\_refs:

  \- service:approval\_service

  \- service:safety\_gate\_service

decision\_boundary: may\_review\_safety\_decision\_cases

approval\_boundary: may\_approve\_safety\_actions\_within\_scope

execution\_boundary: does\_not\_create\_execution\_request

safety\_boundary: approval\_does\_not\_replace\_safety\_gate

audit\_event\_refs:

  \- audit:identity\_validated

  \- audit:approval\_authority\_checked

  \- audit:approval\_decision\_recorded

  \- audit:identity\_scope\_violation

owner\_module: identity\_governance\_module

owner\_team: LEDO Governance

source\_document: identity\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_identity\_id: null

---

## **12\. Registry Entry Example: Robot Dispatch Agent Identity**

identity\_id: agent:robot\_dispatch\_agent\_site\_A

canonical\_name: robot\_dispatch\_agent\_site\_A

display\_name: Robot Dispatch Agent \- Site A

description: An Agent identity that can generate robot dispatch-related ActionCandidates and EvidenceBundles at Site A.

semantic\_iri: ledo:RobotDispatchAgentIdentitySiteA

identity\_type: AGENT\_IDENTITY

version: 1.0.0

status: active

auth\_provider\_ref: service\_identity\_provider

external\_subject\_ref: service\_account:robot\_dispatch\_agent\_site\_A

role\_refs:

  \- role:domain\_agent

  \- role:robot\_analysis\_agent

attribute\_refs:

  \- attribute:system\_managed

  \- attribute:registered\_agent

  \- attribute:site\_scoped

certification\_refs: \[\]

training\_refs:

  \- training:robot\_dispatch\_agent\_validation\_v1

site\_scope:

  \- site\_A

zone\_scope:

  \- zone\_01

  \- zone\_02

  \- zone\_03

operation\_scope:

  \- robotic\_support\_operation

equipment\_scope:

  \- robot\_fleet\_site\_A

system\_scope:

  \- world\_state\_service

  \- evidence\_binder

  \- decision\_engine

shift\_scope:

  \- "\*"

authority\_level: propose\_action

trust\_level: verified

mfa\_required: false

mfa\_status: not\_required

delegation\_allowed: false

delegation\_refs: \[\]

valid\_from: 2026-06-26T00:00:00Z

valid\_until: null

pii\_classification: none

sensitivity\_level: internal

access\_control\_refs:

  \- access:robot\_agent\_access\_policy

policy\_refs:

  \- policy:robot\_dispatch\_policy

  \- policy:worker\_proximity\_policy

approval\_authority\_refs: \[\]

allowed\_agent\_type\_refs:

  \- agent\_type:ROBOT\_DISPATCH\_AGENT

allowed\_service\_refs:

  \- service:world\_state\_service

  \- service:evidence\_binder

  \- service:decision\_engine

decision\_boundary: may\_generate\_robot\_dispatch\_decision\_inputs

approval\_boundary: must\_not\_grant\_approval

execution\_boundary: must\_not\_create\_execution\_request

safety\_boundary: must\_not\_bypass\_safety\_gate\_or\_fleet\_manager

audit\_event\_refs:

  \- audit:identity\_validated

  \- audit:agent\_output\_created

  \- audit:agent\_scope\_violation

  \- audit:action\_candidate\_created

owner\_module: agent\_governance\_module

owner\_team: LEDO Agent Runtime

source\_document: agent\_identity\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_identity\_id: null

---

## **13\. Registry Entry Example: Execution Dispatcher Service Identity**

identity\_id: service:execution\_dispatcher

canonical\_name: execution\_dispatcher

display\_name: Execution Dispatcher Service

description: An internal service identity that delivers Safety Gate-passed ExecutionRequests to adapters.

semantic\_iri: ledo:ExecutionDispatcherServiceIdentity

identity\_type: SERVICE\_IDENTITY

version: 1.0.0

status: active

auth\_provider\_ref: service\_identity\_provider

external\_subject\_ref: service\_account:execution\_dispatcher

role\_refs:

  \- role:execution\_service

  \- role:system\_service

attribute\_refs:

  \- attribute:system\_managed

  \- attribute:service\_account

  \- attribute:mTLS\_required

certification\_refs: \[\]

training\_refs: \[\]

site\_scope:

  \- "\*"

zone\_scope:

  \- "\*"

operation\_scope:

  \- execution\_integration\_operation

equipment\_scope:

  \- "\*"

system\_scope:

  \- adapter\_registry

  \- external\_system\_registry

  \- audit\_service

shift\_scope:

  \- "\*"

authority\_level: service\_execute

trust\_level: system\_trusted

mfa\_required: false

mfa\_status: not\_required

delegation\_allowed: false

delegation\_refs: \[\]

valid\_from: 2026-06-26T00:00:00Z

valid\_until: null

pii\_classification: none

sensitivity\_level: restricted

access\_control\_refs:

  \- access:execution\_dispatcher\_service\_policy

policy\_refs:

  \- policy:execution\_dispatch\_policy

  \- policy:external\_system\_access\_policy

approval\_authority\_refs: \[\]

allowed\_agent\_type\_refs: \[\]

allowed\_service\_refs:

  \- service:safety\_gate\_service

  \- service:adapter\_registry\_service

  \- service:audit\_service

decision\_boundary: does\_not\_create\_decision\_case

approval\_boundary: does\_not\_grant\_approval

execution\_boundary: may\_dispatch\_safety\_gate\_passed\_execution\_request\_only

safety\_boundary: must\_not\_dispatch\_without\_safety\_gate\_pass

audit\_event\_refs:

  \- audit:identity\_validated

  \- audit:execution\_request\_dispatched

  \- audit:service\_scope\_violation

  \- audit:external\_system\_request\_sent

owner\_module: execution\_integration\_module

owner\_team: LEDO Execution Integration

source\_document: service\_identity\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_identity\_id: null

---

## **14\. Registry Entry Example: External System Identity**

identity\_id: external\_system:robot\_fleet\_manager\_site\_A

canonical\_name: robot\_fleet\_manager\_site\_A

display\_name: Robot Fleet Manager Identity \- Site A

description: The identity of the robot fleet manager external system for Site A.

semantic\_iri: ledo:RobotFleetManagerIdentitySiteA

identity\_type: EXTERNAL\_SYSTEM\_IDENTITY

version: 1.0.0

status: active

auth\_provider\_ref: external\_system\_trust\_store

external\_subject\_ref: external\_system\_cert:robot\_fleet\_manager\_site\_A

role\_refs:

  \- role:external\_system

  \- role:robot\_fleet\_manager

attribute\_refs:

  \- attribute:registered\_external\_system

  \- attribute:mTLS\_verified

  \- attribute:command\_capable\_external\_system

certification\_refs: \[\]

training\_refs: \[\]

site\_scope:

  \- site\_A

zone\_scope:

  \- zone\_01

  \- zone\_02

  \- zone\_03

operation\_scope:

  \- robotic\_support\_operation

equipment\_scope:

  \- robot\_fleet\_site\_A

system\_scope:

  \- execution\_feedback\_stream

  \- robot\_status\_stream

shift\_scope:

  \- "\*"

authority\_level: external\_system

trust\_level: system\_trusted

mfa\_required: false

mfa\_status: not\_required

delegation\_allowed: false

delegation\_refs: \[\]

valid\_from: 2026-06-26T00:00:00Z

valid\_until: null

pii\_classification: none

sensitivity\_level: restricted

access\_control\_refs:

  \- access:robot\_fleet\_external\_system\_policy

policy\_refs:

  \- policy:external\_system\_feedback\_policy

  \- policy:robot\_fleet\_integration\_policy

approval\_authority\_refs: \[\]

allowed\_agent\_type\_refs: \[\]

allowed\_service\_refs:

  \- service:execution\_dispatcher

  \- service:world\_state\_service

  \- service:audit\_service

decision\_boundary: may\_provide\_status\_for\_decision\_but\_not\_create\_decision

approval\_boundary: does\_not\_grant\_approval

execution\_boundary: may\_return\_execution\_feedback\_only

safety\_boundary: must\_enforce\_vendor\_robot\_safety\_boundary

audit\_event\_refs:

  \- audit:identity\_validated

  \- audit:external\_system\_feedback\_received

  \- audit:external\_system\_identity\_failed

owner\_module: external\_system\_governance\_module

owner\_team: LEDO External Integration

source\_document: external\_system\_identity\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_identity\_id: null

---

## **15\. Identity Lifecycle Alignment**

Identity is connected to the following lifecycle:

Identity Registered

        →
Identity Verification

        →
Role / Attribute / Scope Assignment

        →
Certification / Training Validation

        →
Activation

        →
Runtime Identity Check

        →
Policy / Approval / Execution / Audit Usage

        →
Suspension / Revocation / Expiration / Retirement

The important point is that an active Identity does not automatically have all authority.

The Identity must be active.

It must have the required role.

It must have the required attributes.

It must have the required certifications.

Its site / zone / shift scope must match.

It must satisfy the relevant action, approval, service, or external request boundary.

---

## **16\. Validation Rules**

An Identity Entry is valid only when the following conditions are satisfied:

1. `identity_id` exists in the registry.  
2. Its status is `active`.  
3. Identity type is declared.  
4. Role references are declared.  
5. Authority level is declared.  
6. Trust level is declared.  
7. Site / zone / system scope is declared.  
8. `valid_from` / `valid_until` are declared.  
9. PII classification is declared.  
10. Sensitivity level is declared.  
11. Decision / approval / execution / safety boundaries are declared.  
12. Audit event references are declared.  
13. Owner module is declared.  
14. Version is valid.  
15. If deprecated, migration metadata exists.

If any of these conditions are missing, the Identity must not be used in the operational lifecycle.

---

## **17\. Runtime Identity Validation**

When an identity is used at runtime, the following validations are required:

Does the Identity exist in the registry?

Is the Identity active?

Has the Identity not expired?

Is the Identity not revoked or suspended?

Does it have the required role?

Does it have the required attributes?

Does it have the required certification?

Does its site scope match?

Does its zone scope match?

Does its shift scope match?

If MFA is required, is it verified?

If delegation is required, is the delegation valid?

Does it comply with the boundary?

Is an audit trace created?

If these conditions are not satisfied, the identity must not perform the requested operation.

---

## **18\. Role Rule**

Roles must be managed through a registry-based model.

Recommended role categories:

site\_role

safety\_role

robotics\_role

equipment\_role

compliance\_role

audit\_role

agent\_role

service\_role

external\_system\_role

Role is an input to authority evaluation, but final permission is determined by Policy and Scope.

Role alone is not enough.

Role \+ Attribute \+ Scope \+ Policy \+ Approval Rule are required.

Example:

Even if an actor has the safety\_supervisor role,

they cannot approve STOP\_WORK for site\_A without site\_A scope.

---

## **19\. Attribute Rule**

Attributes represent the current state of an identity.

Examples:

active\_employee

assigned\_to\_site

on\_shift

off\_shift

mfa\_verified

system\_managed

registered\_agent

registered\_external\_system

delegated\_authority\_active

training\_valid

certification\_valid

Attributes may change frequently.  
Therefore, long-term identity records and runtime attribute snapshots may be separated.

Identity Registry:

    Defines the base identity and allowed attributes.

Runtime Attribute Store:

    Manages dynamic states such as on\_shift, active\_session, and mfa\_verified.

---

## **20\. Scope Rule**

Scope limits the boundary within which an identity is valid.

Scope must be applied to the following:

ApprovalDecision

ActionCandidate proposal

DecisionCase review

Evidence access

World State query

ExecutionRequest dispatch

External System access

Audit record access

Recommended scopes:

site\_scope

zone\_scope

operation\_scope

equipment\_scope

worker\_group\_scope

task\_scope

system\_scope

time\_scope

shift\_scope

Core principle:

No scope,

no authority.

---

## **21\. Certification Rule**

Certification verification is required for safety-critical actions or approvals.

Examples:

STOP\_WORK approval:

    requires construction\_safety\_supervisor\_certification

DISPATCH\_ROBOT approval:

    requires robot\_operation\_supervisor\_training

Electrical isolation approval:

    requires electrical\_safety\_certification

Certification can expire.

Certification expired,

no safety-critical authority.

---

## **22\. Delegation Rule**

Delegation must be allowed only under restricted conditions.

A delegation is valid only when the following conditions are satisfied:

1. The delegator identity is active.  
2. The delegate identity is active.  
3. The delegator has authority that may be delegated.  
4. The delegate has the minimum required role or certification.  
5. The delegation scope is explicit.  
6. `valid_until` exists.  
7. A delegation policy exists.  
8. An audit record is created.

Delegation example:

delegation\_id: delegation:safety\_supervisor\_site\_A\_day\_shift\_v1

delegator\_identity\_id: human:safety\_supervisor\_001

delegate\_identity\_id: human:site\_safety\_manager\_002

delegated\_role\_ref: role:safety\_supervisor\_delegate

site\_scope:

  \- site\_A

zone\_scope:

  \- zone\_03

valid\_from: 2026-06-26T08:00:00Z

valid\_until: 2026-06-26T18:00:00Z

delegation\_policy\_ref: policy:safety\_supervisor\_delegation\_policy

---

## **23\. PII and Privacy Rule**

Identity Registry must not store excessive sensitive personal information.

Recommended principles:

Store only the minimum identity references required for operation.

Keep actual personal information in the HR system or IAM provider.

Store only operational identity metadata in LEDO.

PII requires masking, encryption, access control, and audit.

PII classifications:

none

indirect

direct

sensitive

Examples:

human identity:

    pii\_classification: direct

agent identity:

    pii\_classification: none

external system identity:

    pii\_classification: none

device identity linked to a worker:

    pii\_classification: indirect or direct

---

## **24\. Relationship to Access Control Registry**

`identity_registry` defines "who the actor is" and "which attributes the actor has."

`access_control_registry` defines "what the actor can access."

identity\_registry:

    safety\_supervisor\_001 has safety\_supervisor role and site\_A scope.

access\_control\_registry:

    safety\_supervisor role can access the safety dashboard and approval UI.

Identity is an input to Access Control.

---

## **25\. Relationship to Policy Registry**

`policy_registry` defines policy evaluation.

`identity_registry` provides identity claims needed for policy evaluation.

identity\_registry:

    This user is an on-shift safety\_supervisor for site\_A.

policy\_registry:

    STOP\_WORK approval requires an on-shift safety supervisor with matching site scope.

Identity does not replace Policy.

---

## **26\. Relationship to Approval Registry**

`approval_registry` defines which role, certification, and scope are required for each approval.

`identity_registry` verifies whether the current approver satisfies those conditions.

approval\_registry:

    STOP\_WORK requires safety\_supervisor\_approval.

identity\_registry:

    Does this approver have the safety\_supervisor role, site\_A scope, and required certification?

Core principle:

Approval Authority requires valid Identity.

---

## **27\. Relationship to Agent Vocabulary Registry**

`agent_vocabulary_registry` defines which Agent Type may create which output.

`identity_registry` verifies whether the runtime Agent Instance has a registered identity.

agent\_vocabulary\_registry:

    ROBOT\_DISPATCH\_AGENT may propose DISPATCH\_ROBOT ActionCandidate.

identity\_registry:

    Is agent:robot\_dispatch\_agent\_site\_A an active registered agent identity?

Without Agent Identity, Agent Output cannot be trusted.

---

## **28\. Relationship to Event Registry**

An Event must have a producer identity.

event\_registry:

    WorkerLocationUpdated may be produced by a registered sensor gateway.

identity\_registry:

    Is the producer device or service a registered identity?

Events produced by unregistered producers must be rejected or quarantined.

---

## **29\. Relationship to Evidence Registry**

Evidence must have a producer identity and source identity.

evidence\_registry:

    worker\_location\_snapshot may be created by worker\_tracking\_gateway.

identity\_registry:

    Is that gateway identity active and trusted?

Evidence with unclear identity must not be used for judgment.

---

## **30\. Relationship to Adapter Registry**

Adapters must have identities.

adapter\_registry:

    robot\_fleet\_adapter\_site\_A can handle robot mission requests.

identity\_registry:

    Is adapter:robot\_fleet\_adapter\_site\_A an active registered adapter identity?

If the Adapter Identity is invalid, requests must not be sent to the External System.

---

## **31\. Relationship to External System Registry**

External Systems must also have identities.

external\_system\_registry:

    robot\_fleet\_manager\_site\_A is a registered external system.

identity\_registry:

    Is external\_system:robot\_fleet\_manager\_site\_A a trusted external system identity?

External System Identity may be used for mTLS, certificate validation, and signed feedback validation.

---

## **32\. Relationship to Audit Registry**

Every important action must have an actor identity.

Audit targets:

identity\_created

identity\_validated

identity\_suspended

identity\_revoked

role\_assigned

role\_removed

scope\_changed

delegation\_created

delegation\_expired

approval\_authority\_checked

identity\_scope\_violation

identity\_policy\_violation

Audit Records should include the following:

actor\_identity\_id: string

actor\_identity\_type: string

actor\_role\_refs:

  \- string

actor\_scope:

  site\_scope:

    \- string

  zone\_scope:

    \- string

action\_performed: string

timestamp: datetime

trace\_id: string

Core principle:

No actor identity,

no trustworthy audit.

---

## **33\. Relationship to Ontology**

Every important Identity Type and Role should have a semantic IRI.

Example:

identity\_id: human:safety\_supervisor\_001

semantic\_iri: ledo:SafetySupervisorIdentity001

In the ontology, it may be defined as follows:

ledo:SafetySupervisorIdentity001

    rdf:type ledo:HumanIdentity ;

    ledo:hasRole ledo:SafetySupervisor ;

    ledo:assignedToSite ledo:SiteA ;

    ledo:hasCertification ledo:ConstructionSafetySupervisorCertification ;

    ledo:mayApprove ledo:StopWorkAction .

Ontology provides the semantic foundation of Identity and Role.

Identity Registry manages this foundation in the operational system through version, status, scope, certification, delegation, and audit rules.

---

## **34\. Versioning and Migration**

Identity Entries must be versioned.

A version change is required when any of the following changes:

1. Identity type changes  
2. Role references change  
3. Authority level changes  
4. Trust level changes  
5. Site / zone / operation scope changes  
6. Certification requirements change  
7. Delegation rules change  
8. Access control references change  
9. Policy references change  
10. Approval authority references change  
11. Decision / approval / execution / safety boundaries change  
12. PII classification changes

Status values:

draft

active

suspended

revoked

expired

deprecated

retired

blocked

### **34.1 suspended**

An identity temporarily disabled from use.

---

### **34.2 revoked**

An identity whose authority has been revoked.  
It must not be used for new lifecycle actions.

---

### **34.3 expired**

An identity whose `valid_until` time has passed.

---

### **34.4 blocked**

An identity blocked for security, safety, or audit reasons.

Blocked Identity must not be used in any operational lifecycle.

---

## **35\. Implementation Use**

`identity_registry` is used to generate or validate:

1. `IdentityType` enum  
2. `IdentityStatus` enum  
3. `AuthorityLevel` enum  
4. `TrustLevel` enum  
5. Identity metadata DTO  
6. Role assignment validation  
7. Attribute validation  
8. Scope validation  
9. Certification validation  
10. Delegation validation  
11. Approval authority validation  
12. Agent identity validation  
13. Service identity validation  
14. Adapter identity validation  
15. External system identity validation  
16. Event producer validation  
17. Evidence producer validation  
18. Audit actor validation  
19. Test case generation  
20. Migration rules

Implementation must not use an unregistered identity as an operational actor.

---

## **36\. Recommended Code Structure**

registries/

    identity\_registry/

        identity\_registry.py

        identity\_entry.py

        identity\_type.py

        identity\_status.py

        authority\_level.py

        trust\_level.py

        role\_ref.py

        scope.py

        certification.py

        delegation.py

        identity\_validation.py

        identity\_errors.py

        identity\_loader.py

        identity\_migration.py

    access\_control\_registry/

    approval\_registry/

    policy\_registry/

    agent\_vocabulary\_registry/

    event\_registry/

    evidence\_registry/

    adapter\_registry/

    external\_system\_registry/

    audit\_event\_registry/

---

## **37\. Minimal Pydantic Model**

from enum import Enum

from pydantic import BaseModel, Field

from typing import Optional

from datetime import datetime

class IdentityStatus(str, Enum):

    DRAFT \= "draft"

    ACTIVE \= "active"

    SUSPENDED \= "suspended"

    REVOKED \= "revoked"

    EXPIRED \= "expired"

    DEPRECATED \= "deprecated"

    RETIRED \= "retired"

    BLOCKED \= "blocked"

class IdentityType(str, Enum):

    HUMAN\_IDENTITY \= "human\_identity"

    AGENT\_IDENTITY \= "agent\_identity"

    SERVICE\_IDENTITY \= "service\_identity"

    ADAPTER\_IDENTITY \= "adapter\_identity"

    EXTERNAL\_SYSTEM\_IDENTITY \= "external\_system\_identity"

    DEVICE\_IDENTITY \= "device\_identity"

    ORGANIZATION\_IDENTITY \= "organization\_identity"

    TEMPORARY\_IDENTITY \= "temporary\_identity"

class AuthorityLevel(str, Enum):

    OBSERVE\_ONLY \= "observe\_only"

    OPERATE \= "operate"

    PROPOSE\_ACTION \= "propose\_action"

    REVIEW \= "review"

    APPROVE \= "approve"

    ADMINISTER \= "administer"

    SERVICE\_EXECUTE \= "service\_execute"

    EXTERNAL\_SYSTEM \= "external\_system"

class TrustLevel(str, Enum):

    UNVERIFIED \= "unverified"

    BASIC \= "basic"

    VERIFIED \= "verified"

    PRIVILEGED \= "privileged"

    SAFETY\_CRITICAL \= "safety\_critical"

    SYSTEM\_TRUSTED \= "system\_trusted"

class MFAStatus(str, Enum):

    UNKNOWN \= "unknown"

    NOT\_REQUIRED \= "not\_required"

    REQUIRED \= "required"

    VERIFIED \= "verified"

    FAILED \= "failed"

class SensitivityLevel(str, Enum):

    INTERNAL \= "internal"

    CONFIDENTIAL \= "confidential"

    RESTRICTED \= "restricted"

    SAFETY\_CRITICAL \= "safety\_critical"

class PIIClassification(str, Enum):

    NONE \= "none"

    INDIRECT \= "indirect"

    DIRECT \= "direct"

    SENSITIVE \= "sensitive"

class IdentityScope(BaseModel):

    site\_scope: list\[str\] \= Field(default\_factory=list)

    zone\_scope: list\[str\] \= Field(default\_factory=list)

    operation\_scope: list\[str\] \= Field(default\_factory=list)

    equipment\_scope: list\[str\] \= Field(default\_factory=list)

    system\_scope: list\[str\] \= Field(default\_factory=list)

    shift\_scope: list\[str\] \= Field(default\_factory=list)

class IdentityRegistryEntry(BaseModel):

    identity\_id: str

    canonical\_name: str

    display\_name: str

    description: str

    semantic\_iri: str

    identity\_type: IdentityType

    version: str

    status: IdentityStatus \= IdentityStatus.DRAFT

    auth\_provider\_ref: Optional\[str\] \= None

    external\_subject\_ref: Optional\[str\] \= None

    role\_refs: list\[str\] \= Field(default\_factory=list)

    attribute\_refs: list\[str\] \= Field(default\_factory=list)

    certification\_refs: list\[str\] \= Field(default\_factory=list)

    training\_refs: list\[str\] \= Field(default\_factory=list)

    scope: IdentityScope \= Field(default\_factory=IdentityScope)

    authority\_level: AuthorityLevel

    trust\_level: TrustLevel

    mfa\_required: bool \= False

    mfa\_status: MFAStatus \= MFAStatus.UNKNOWN

    delegation\_allowed: bool \= False

    delegation\_refs: list\[str\] \= Field(default\_factory=list)

    valid\_from: datetime

    valid\_until: Optional\[datetime\] \= None

    pii\_classification: PIIClassification \= PIIClassification.NONE

    sensitivity\_level: SensitivityLevel \= SensitivityLevel.INTERNAL

    access\_control\_refs: list\[str\] \= Field(default\_factory=list)

    policy\_refs: list\[str\] \= Field(default\_factory=list)

    approval\_authority\_refs: list\[str\] \= Field(default\_factory=list)

    allowed\_agent\_type\_refs: list\[str\] \= Field(default\_factory=list)

    allowed\_service\_refs: list\[str\] \= Field(default\_factory=list)

    decision\_boundary: str

    approval\_boundary: str

    execution\_boundary: str

    safety\_boundary: str

    audit\_event\_refs: list\[str\] \= Field(default\_factory=list)

    owner\_module: str

    owner\_team: str

    source\_document: str

    created\_at: datetime

    updated\_at: datetime

    deprecated\_since: Optional\[datetime\] \= None

    replacement\_identity\_id: Optional\[str\] \= None

---

## **38\. Core Validation Function**

from datetime import datetime, timezone

def validate\_identity\_for\_scope(

    entry: IdentityRegistryEntry,

    required\_role\_ref: str | None,

    required\_site\_id: str | None,

    required\_zone\_id: str | None,

    required\_authority\_level: AuthorityLevel | None,

    require\_mfa: bool \= False,

) \-\> None:

    if entry.status \!= IdentityStatus.ACTIVE:

        raise InvalidIdentityError(

            f"Identity is not active: {entry.identity\_id}"

        )

    now \= datetime.now(timezone.utc)

    if entry.valid\_until is not None and now \> entry.valid\_until:

        raise IdentityExpiredError(

            f"Identity is expired: {entry.identity\_id}"

        )

    if required\_role\_ref is not None:

        if required\_role\_ref not in entry.role\_refs:

            raise IdentityRoleMismatchError(

                f"Identity '{entry.identity\_id}' does not have required role "

                f"'{required\_role\_ref}'"

            )

    if required\_site\_id is not None:

        if required\_site\_id not in entry.scope.site\_scope and "\*" not in entry.scope.site\_scope:

            raise IdentityScopeViolationError(

                f"Identity '{entry.identity\_id}' is not valid for site "

                f"'{required\_site\_id}'"

            )

    if required\_zone\_id is not None:

        if required\_zone\_id not in entry.scope.zone\_scope and "\*" not in entry.scope.zone\_scope:

            raise IdentityScopeViolationError(

                f"Identity '{entry.identity\_id}' is not valid for zone "

                f"'{required\_zone\_id}'"

            )

    if required\_authority\_level is not None:

        if entry.authority\_level \!= required\_authority\_level:

            raise IdentityAuthorityMismatchError(

                f"Identity '{entry.identity\_id}' does not have required authority "

                f"'{required\_authority\_level}'"

            )

    if require\_mfa:

        if entry.mfa\_status \!= MFAStatus.VERIFIED:

            raise IdentityMFARequiredError(

                f"MFA is required but not verified for identity '{entry.identity\_id}'"

            )

    if not entry.decision\_boundary:

        raise InvalidIdentityError(

            "decision\_boundary must be declared"

        )

    if not entry.approval\_boundary:

        raise InvalidIdentityError(

            "approval\_boundary must be declared"

        )

    if not entry.execution\_boundary:

        raise InvalidIdentityError(

            "execution\_boundary must be declared"

        )

    if not entry.safety\_boundary:

        raise InvalidIdentityError(

            "safety\_boundary must be declared"

        )

---

## **39\. Test Scenarios**

Required tests:

1\. Reject unregistered Identity.

2\. Reject inactive Identity.

3\. Reject suspended Identity.

4\. Reject revoked Identity.

5\. Reject expired Identity.

6\. Reject blocked Identity.

7\. Reject missing required role.

8\. Reject missing required attribute.

9\. Reject missing required certification.

10\. Reject site scope mismatch.

11\. Reject zone scope mismatch.

12\. Reject shift scope mismatch.

13\. Reject identity when MFA is required but not verified.

14\. Reject expired delegation.

15\. Reject delegation scope mismatch.

16\. Reject Agent Identity attempting to create ApprovalDecision.

17\. Reject Service Identity being used as Approval Authority.

18\. Reject External System Identity being used as internal Approval Authority.

19\. Reject Event Producer without Identity.

20\. Reject Evidence Producer without Identity.

21\. Reject AuditRecord missing actor\_identity\_id.

22\. Verify Identity migration rules.

---

## **40\. Final Rule**

No registered Identity,

no trustworthy Actor.

No valid Identity,

no trustworthy ActionCandidate.

No valid Identity,

no trustworthy DecisionCase.

No valid Identity,

no trustworthy ApprovalDecision.

No valid Identity,

no trustworthy ExecutionRequest.

Role alone is not enough.

Role \+ Attribute \+ Scope \+ Certification \+ Policy are required.

Identity is not Approval.

Identity is not Policy.

Identity is not Safety Gate.

Identity is not PhysicalCommand.

`identity_registry` is the core deterministic registry that governs the identity, role, attributes, scope, certification, delegation, and trust level of every actor in the LEDO system.

This module clearly traces **"who performed this action, and under what qualification?"** and ensures that no identity-less action can occur in decision, approval, execution, or audit flows.

The core definition is:

Identity Registry

\= not a user list,

but an operational contract registry that controls

the identity, role, attributes, scope, certification,

delegation, trust level, and audit trace

of every Human, Agent, Service, Adapter, External System,

and Device acting inside LEDO.

