**External System registry**

## **1\. Overview**

`external_system_registry` is a core registry in the LEDO Ontology-Centric Cyber-Physical System. It defines and governs the types, identities, roles, connection methods, supported capabilities, authority boundaries, safety levels, data direction, communication contracts, feedback contracts, and audit rules of all external systems connected to LEDO.

The purpose of this module is to verify that an external system is registered, trusted, and allowed to communicate only within an approved scope before LEDO sends an approved Action or ExecutionRequest to that external system.

`external_system_registry` is not a simple list of external systems.

It is an **operational contract registry for external system identity, authority, connection, and safety boundaries** that defines the following:

Which external systems may connect to LEDO?

What type of system is each external system?

Is the system read-only or command-capable?

Which Action Types or ExecutionRequests can the system receive?

Through which adapters may the system be accessed?

Which protocol does the system use?

Is the system safety-critical?

Does the system have physical control authority?

To what level may LEDO send requests to the system?

Which feedback schema must be used when receiving feedback from the system?

If the system is unavailable, which fallback or fail-safe policy must be followed?

In other words, `external_system_registry` is the **official system contract** between LEDO’s internal world and external physical or operational systems.

---

## **2\. Core Principle**

An External System is not an internal LEDO module.

An External System is different from an Adapter.

An External System is not the Action Registry.

An External System is not the Safety Gate.

An External System is not Approval Authority.

An External System may be responsible for actual physical execution or external business execution.

However, LEDO does not own or replace the internal control logic of the external system.

The core principle is:

LEDO defines intent, constraints, approval, safety boundary, and audit.

Adapter translates LEDO requests into an external integration protocol.

External System performs domain-specific execution or returns authoritative external state.

For systems such as robots, PLCs, SCADA, and safety controllers, the following principles are especially important:

LEDO must not bypass external safety-rated systems.

LEDO must not directly generate low-level physical control commands.

LEDO must interact with external systems through registered adapters and approved integration contracts.

---

## **3\. Position in the LEDO Architecture**

`external_system_registry` belongs to the Execution Request & External Control Integration Layer.

ApprovedAction

        ↓

Safety Gate

        ↓

ExecutionRequest

        ↓

adapter\_registry

        ↓

external\_system\_registry validation

        ↓

ExternalControlRequest

        ↓

External Adapter

        ↓

External System

        ↓

ExecutionResult / FeedbackEvent

Within the overall flow, `external_system_registry` answers the following questions:

Is this external system registered?

Can this system receive this Action?

Is this adapter allowed to connect to this external system?

Is this protocol allowed?

Is this system currently active?

Does this request violate the system’s safety boundary?

Which feedback must this system return?

---

## **4\. Purpose**

The purpose of `external_system_registry` is to ensure the following:

1. Prevent connection to unregistered external systems  
2. Define the identity and type of each external system  
3. Define supported functions and capabilities for each external system  
4. Define read / write / command authority for each external system  
5. Define protocol and integration contracts for each external system  
6. Restrict which adapters may connect to each external system  
7. Define supported Action Types and ExecutionRequest types for each external system  
8. Distinguish safety-critical systems from non-safety systems  
9. Define physical control authority boundaries  
10. Define feedback events and result schemas  
11. Define health check and availability rules  
12. Define fallback and fail-safe policies  
13. Define credential references and security boundaries  
14. Define audit and trace rules for external systems  
15. Manage versioning and migration

---

## **5\. Core Distinctions**

### **5.1 External System**

An `External System` is a system outside LEDO that provides data, reports state, processes business operations, performs physical execution, sends notifications, or integrates with site platforms.

Examples:

robot\_fleet\_manager

robot\_middleware

plc\_system

scada\_system

safety\_controller

bim\_cde\_platform

site\_management\_platform

notification\_system

inspection\_system

erp\_system

cmms\_system

weather\_api

camera\_vms

iot\_platform

---

### **5.2 External System Type**

External System Type defines the kind of external system.

Examples:

ROBOT\_FLEET\_MANAGER

ROBOT\_MIDDLEWARE

PLC\_SYSTEM

SCADA\_SYSTEM

SAFETY\_CONTROLLER

BIM\_CDE\_PLATFORM

SITE\_MANAGEMENT\_PLATFORM

NOTIFICATION\_SYSTEM

INSPECTION\_SYSTEM

ERP\_SYSTEM

CMMS\_SYSTEM

IOT\_PLATFORM

VISION\_SYSTEM

WEATHER\_SERVICE

External System Type determines the integration boundary, protocol, safety level, action support, and feedback contract.

---

### **5.3 External System Instance**

External System Instance is an individual external system that exists in an actual operational environment.

Examples:

robot\_fleet\_manager\_site\_A

scada\_system\_tower\_B

plc\_gateway\_crane\_01

bim\_cde\_project\_alpha

notification\_system\_kakao\_site\_A

External System Type is the design-level definition.

External System Instance is the actual connection target.

---

### **5.4 Difference Between Adapter and External System**

An Adapter is an internal LEDO integration module.

An External System is an actual system outside LEDO.

adapter\_registry:

    Which adapter instance can translate an ExecutionRequest into an external protocol?

external\_system\_registry:

    Which external system exists, and within what authority and boundary may it be connected?

Example:

robot\_fleet\_adapter

    → internal LEDO adapter

robot\_fleet\_manager\_site\_A

    → actual external robot fleet system

The Adapter is the communication translator.

The External System is the external authority system.

---

### **5.5 External Control Authority**

External Control Authority indicates whether the external system has physical or operational execution authority.

Recommended values:

read\_only

write\_data

request\_only

command\_capable

safety\_rated\_control

physical\_control\_authority

Even if LEDO does not directly generate physical commands, the external system may have physical control authority.

Examples:

robot\_fleet\_manager:

    command\_capable

plc\_system:

    physical\_control\_authority

safety\_controller:

    safety\_rated\_control

bim\_cde\_platform:

    write\_data

weather\_api:

    read\_only

---

## **6\. Scope**

`external_system_registry` controls the following fields:

external\_system\_id: string

canonical\_name: string

display\_name: string

description: string

semantic\_iri: string

external\_system\_type: string

system\_category: string

version: string

status: draft | active | maintenance | degraded | deprecated | retired | blocked

site\_scope:

  \- string

zone\_scope:

  \- string

owner\_organization: string

operator\_team: string

vendor\_name: string | null

supported\_protocols:

  \- string

supported\_adapter\_refs:

  \- string

supported\_action\_type\_refs:

  \- string

supported\_execution\_request\_types:

  \- string

supported\_feedback\_event\_refs:

  \- string

supported\_capability\_refs:

  \- string

integration\_mode: read\_only | write\_only | read\_write | request\_response | event\_stream | command\_gateway

data\_direction: inbound | outbound | bidirectional

control\_authority\_level: read\_only | write\_data | request\_only | command\_capable | safety\_rated\_control | physical\_control\_authority

safety\_criticality: non\_critical | operational | safety\_relevant | safety\_critical | safety\_rated

connection\_contract\_ref: string

payload\_contract\_refs:

  \- string

feedback\_schema\_refs:

  \- string

health\_check\_policy\_ref: string

heartbeat\_required: boolean

availability\_requirement: string

fallback\_policy\_ref: string | null

fail\_safe\_policy\_ref: string | null

credential\_ref: string

secret\_storage\_ref: string

network\_zone: string

security\_level: internal | confidential | restricted | safety\_critical

pii\_classification: none | indirect | direct | sensitive

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

replacement\_external\_system\_id: string | null

---

## **7\. Non-Scope**

`external_system_registry` does not define the following:

1. Actual adapter implementation code  
2. Adapter instance selection logic  
3. Low-level robot motion planning  
4. PLC ladder logic  
5. Internal SCADA control logic  
6. Internal safety-rated controller logic  
7. Actual password, token, or private key values  
8. Complete vendor-internal external system data models  
9. Complete user account management of external systems  
10. Complete policy pass/fail logic  
11. Final Safety Gate decision  
12. Approval authority  
13. Raw sensor driver logic  
14. Internal firmware logic of physical equipment

These responsibilities belong to the following modules or systems:

adapter\_registry

adapter implementation

vault / secret manager

policy\_registry

approval\_registry

safety\_gate

identity\_registry

external vendor system

robot fleet manager

PLC / SCADA

safety-rated controller

sensor gateway

---

## **8\. External System Type Model**

Recommended External System Types are:

ROBOT\_FLEET\_MANAGER

ROBOT\_MIDDLEWARE

PLC\_SYSTEM

SCADA\_SYSTEM

SAFETY\_CONTROLLER

BIM\_CDE\_PLATFORM

SITE\_MANAGEMENT\_PLATFORM

NOTIFICATION\_SYSTEM

INSPECTION\_SYSTEM

ERP\_SYSTEM

CMMS\_SYSTEM

IOT\_PLATFORM

VISION\_SYSTEM

WEATHER\_SERVICE

GIS\_SYSTEM

DOCUMENT\_MANAGEMENT\_SYSTEM

### **8.1 ROBOT\_FLEET\_MANAGER**

An external system that manages robot fleet missions, dispatch, routes, status, and feedback.

Example:

robot\_fleet\_manager\_site\_A

LEDO may send high-level mission requests to this system, but it must not generate low-level motion primitives.

---

### **8.2 PLC\_SYSTEM**

An external system responsible for equipment or facility control.

Examples:

plc\_gateway\_crane\_01

plc\_gateway\_batching\_plant\_01

LEDO does not directly control PLC internal logic.

When needed, LEDO may send only restricted requests through registered adapters and safety validation.

---

### **8.3 SCADA\_SYSTEM**

An external system that monitors site facilities or industrial control states and may manage certain operational commands.

Example:

scada\_system\_site\_A

SCADA is mainly connected to monitoring, alerts, and operator workflows.

---

### **8.4 SAFETY\_CONTROLLER**

A system responsible for emergency stop, safety interlocks, and safety-rated logic.

Example:

safety\_controller\_zone\_03

LEDO must not bypass the safety controller.

---

### **8.5 BIM\_CDE\_PLATFORM**

An external platform that manages BIM, CDE, drawings, models, documents, issues, and revisions.

Examples:

autodesk\_construction\_cloud\_project\_A

bim360\_project\_A

open\_cde\_project\_A

---

### **8.6 SITE\_MANAGEMENT\_PLATFORM**

A platform that manages site work, schedules, issues, daily reports, inspection requests, and safety instructions.

Example:

site\_management\_platform\_A

---

### **8.7 NOTIFICATION\_SYSTEM**

A system that sends notifications to workers, managers, and safety personnel.

Examples:

sms\_gateway

kakao\_notification\_gateway

email\_service

push\_notification\_service

---

### **8.8 INSPECTION\_SYSTEM**

A system that manages inspections, checks, quality control, and safety inspection records.

Examples:

inspection\_platform\_site\_A

quality\_inspection\_system\_A

---

## **9\. Integration Mode Model**

Recommended integration modes are:

read\_only

write\_only

read\_write

request\_response

event\_stream

command\_gateway

### **9.1 read\_only**

LEDO only reads data from the external system.

Examples:

weather\_api

bim\_model\_viewer

read\_only\_scada\_monitor

---

### **9.2 write\_only**

LEDO only writes records to the external system.

Examples:

audit\_export\_sink

notification\_sink

---

### **9.3 read\_write**

LEDO can both read and write.

Examples:

site\_management\_platform

inspection\_platform

---

### **9.4 request\_response**

LEDO sends a request and receives a result.

Examples:

robot\_fleet\_manager

inspection\_system

---

### **9.5 event\_stream**

The external system is connected through an event stream.

Examples:

iot\_platform

robot\_status\_stream

scada\_event\_stream

---

### **9.6 command\_gateway**

A system that provides a physical control or operational command path.

This mode must be controlled with the strictest rules.

Examples:

plc\_gateway

robot\_fleet\_manager

safety\_controller\_interface

---

## **10\. Registry Entry Schema**

Each External System Registry entry follows this structure:

external\_system\_id: string

canonical\_name: string

display\_name: string

description: string

semantic\_iri: string

external\_system\_type: string

system\_category: string

version: string

status: draft | active | maintenance | degraded | deprecated | retired | blocked

site\_scope:

  \- string

zone\_scope:

  \- string

owner\_organization: string

operator\_team: string

vendor\_name: string | null

supported\_protocols:

  \- string

supported\_adapter\_refs:

  \- string

supported\_action\_type\_refs:

  \- string

supported\_execution\_request\_types:

  \- string

supported\_feedback\_event\_refs:

  \- string

supported\_capability\_refs:

  \- string

integration\_mode: string

data\_direction: string

control\_authority\_level: string

safety\_criticality: string

connection\_contract\_ref: string

payload\_contract\_refs:

  \- string

feedback\_schema\_refs:

  \- string

health\_check\_policy\_ref: string

heartbeat\_required: boolean

availability\_requirement: string

fallback\_policy\_ref: string | null

fail\_safe\_policy\_ref: string | null

credential\_ref: string

secret\_storage\_ref: string

network\_zone: string

security\_level: string

pii\_classification: string

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

replacement\_external\_system\_id: string | null

---

## **11\. Registry Entry Example: Robot Fleet Manager**

external\_system\_id: external\_system:robot\_fleet\_manager\_site\_A

canonical\_name: robot\_fleet\_manager\_site\_A

display\_name: Robot Fleet Manager \- Site A

description: An external robot fleet system that manages robot mission dispatch, fleet status, and mission feedback at Site A.

semantic\_iri: ledo:RobotFleetManagerSiteA

external\_system\_type: ROBOT\_FLEET\_MANAGER

system\_category: ROBOTICS\_SYSTEM

version: 1.0.0

status: active

site\_scope:

  \- site\_A

zone\_scope:

  \- zone\_01

  \- zone\_02

  \- zone\_03

owner\_organization: robot\_vendor\_or\_site\_operator

operator\_team: robot\_operations\_team

vendor\_name: ExampleRobotVendor

supported\_protocols:

  \- REST

  \- WebSocket

  \- MQTT

supported\_adapter\_refs:

  \- adapter:robot\_fleet\_adapter\_site\_A

supported\_action\_type\_refs:

  \- action:DISPATCH\_ROBOT

  \- action:REPLAN\_ROUTE

  \- action:PAUSE\_MISSION

  \- action:RETURN\_TO\_BASE

supported\_execution\_request\_types:

  \- execution\_request:robot\_mission\_request

  \- execution\_request:robot\_route\_replan\_request

  \- execution\_request:robot\_pause\_request

supported\_feedback\_event\_refs:

  \- event:RobotMissionFeedbackReceived

  \- event:ExecutionResultReceived

  \- event:RobotStatusUpdated

supported\_capability\_refs:

  \- capability:robot\_dispatch

  \- capability:mission\_status\_reporting

  \- capability:route\_replan

  \- capability:return\_to\_base

integration\_mode: request\_response

data\_direction: bidirectional

control\_authority\_level: command\_capable

safety\_criticality: safety\_relevant

connection\_contract\_ref: contract:robot\_fleet\_manager\_site\_A\_connection\_v1

payload\_contract\_refs:

  \- contract:robot\_mission\_request\_payload\_v1

  \- contract:robot\_feedback\_payload\_v1

feedback\_schema\_refs:

  \- schema:robot\_mission\_feedback\_v1

  \- schema:execution\_result\_received\_payload\_v1

health\_check\_policy\_ref: health:robot\_fleet\_manager\_health\_check\_v1

heartbeat\_required: true

availability\_requirement: high

fallback\_policy\_ref: fallback:robot\_dispatch\_fallback\_v1

fail\_safe\_policy\_ref: failsafe:robot\_mission\_fail\_safe\_v1

credential\_ref: credential:robot\_fleet\_manager\_site\_A\_api

secret\_storage\_ref: vault:robot\_fleet\_manager\_site\_A

network\_zone: site\_secure\_network

security\_level: restricted

pii\_classification: none

decision\_boundary: may\_receive\_approved\_robot\_mission\_intent\_only

approval\_boundary: does\_not\_grant\_approval

execution\_boundary: accepts\_high\_level\_mission\_request\_not\_motion\_primitives

safety\_boundary: must\_enforce\_robot\_vendor\_safety\_and\_site\_safety\_constraints

audit\_event\_refs:

  \- audit:external\_system\_registered

  \- audit:external\_system\_request\_sent

  \- audit:external\_system\_feedback\_received

  \- audit:external\_system\_health\_changed

owner\_module: execution\_integration\_module

owner\_team: LEDO Robotics Integration

source\_document: robot\_external\_system\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_external\_system\_id: null

---

## **12\. Registry Entry Example: SCADA System**

external\_system\_id: external\_system:scada\_system\_site\_A

canonical\_name: scada\_system\_site\_A

display\_name: SCADA System \- Site A

description: An external SCADA system that provides facility status, alarms, and certain operational state information for Site A.

semantic\_iri: ledo:SCADASystemSiteA

external\_system\_type: SCADA\_SYSTEM

system\_category: INDUSTRIAL\_CONTROL\_SYSTEM

version: 1.0.0

status: active

site\_scope:

  \- site\_A

zone\_scope:

  \- plant\_zone

  \- equipment\_zone

owner\_organization: site\_operator

operator\_team: control\_room\_team

vendor\_name: ExampleSCADAVendor

supported\_protocols:

  \- OPC-UA

  \- MQTT

  \- REST

supported\_adapter\_refs:

  \- adapter:scada\_adapter\_site\_A

supported\_action\_type\_refs:

  \- action:NOTIFY\_MANAGER

  \- action:REQUEST\_INSPECTION

  \- action:LOCK\_ZONE

supported\_execution\_request\_types:

  \- execution\_request:scada\_notification\_request

  \- execution\_request:inspection\_request

supported\_feedback\_event\_refs:

  \- event:SCADAStatusFeedbackReceived

  \- event:EquipmentStatusChanged

  \- event:ExecutionResultReceived

supported\_capability\_refs:

  \- capability:equipment\_status\_reporting

  \- capability:alarm\_reporting

  \- capability:scada\_notification

integration\_mode: read\_write

data\_direction: bidirectional

control\_authority\_level: request\_only

safety\_criticality: safety\_relevant

connection\_contract\_ref: contract:scada\_system\_site\_A\_connection\_v1

payload\_contract\_refs:

  \- contract:scada\_status\_query\_payload\_v1

  \- contract:scada\_notification\_payload\_v1

feedback\_schema\_refs:

  \- schema:scada\_status\_feedback\_v1

  \- schema:equipment\_status\_changed\_payload\_v1

health\_check\_policy\_ref: health:scada\_health\_check\_v1

heartbeat\_required: true

availability\_requirement: high

fallback\_policy\_ref: fallback:scada\_unavailable\_fallback\_v1

fail\_safe\_policy\_ref: failsafe:scada\_fail\_safe\_v1

credential\_ref: credential:scada\_site\_A\_api

secret\_storage\_ref: vault:scada\_site\_A

network\_zone: industrial\_secure\_network

security\_level: safety\_critical

pii\_classification: none

decision\_boundary: may\_provide\_status\_and\_alarm\_data\_for\_decision

approval\_boundary: does\_not\_grant\_approval

execution\_boundary: does\_not\_allow\_direct\_low\_level\_control\_from\_LEDO

safety\_boundary: must\_not\_bypass\_scada\_or\_safety\_controller\_interlocks

audit\_event\_refs:

  \- audit:external\_system\_registered

  \- audit:external\_system\_status\_read

  \- audit:external\_system\_request\_sent

  \- audit:external\_system\_feedback\_received

owner\_module: execution\_integration\_module

owner\_team: LEDO Industrial Integration

source\_document: scada\_external\_system\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_external\_system\_id: null

---

## **13\. Registry Entry Example: BIM / CDE Platform**

external\_system\_id: external\_system:bim\_cde\_project\_A

canonical\_name: bim\_cde\_project\_A

display\_name: BIM CDE Platform \- Project A

description: An external CDE system that manages BIM models, drawings, issues, documents, and revision information for Project A.

semantic\_iri: ledo:BIMCDEPlatformProjectA

external\_system\_type: BIM\_CDE\_PLATFORM

system\_category: CONSTRUCTION\_INFORMATION\_SYSTEM

version: 1.0.0

status: active

site\_scope:

  \- site\_A

zone\_scope:

  \- "\*"

owner\_organization: project\_owner\_or\_general\_contractor

operator\_team: bim\_management\_team

vendor\_name: ExampleCDEVendor

supported\_protocols:

  \- REST

  \- GraphQL

  \- Webhook

supported\_adapter\_refs:

  \- adapter:bim\_cde\_adapter\_project\_A

supported\_action\_type\_refs:

  \- action:REQUEST\_INSPECTION

  \- action:NOTIFY\_MANAGER

  \- action:UPDATE\_MODEL\_ISSUE

  \- action:CREATE\_DOCUMENT\_RECORD

supported\_execution\_request\_types:

  \- execution\_request:bim\_issue\_create\_request

  \- execution\_request:document\_record\_create\_request

  \- execution\_request:model\_query\_request

supported\_feedback\_event\_refs:

  \- event:BIMIssueCreated

  \- event:DocumentRecordCreated

  \- event:ExternalSystemStatusUpdated

supported\_capability\_refs:

  \- capability:model\_query

  \- capability:issue\_creation

  \- capability:document\_record\_write

  \- capability:webhook\_event\_receive

integration\_mode: read\_write

data\_direction: bidirectional

control\_authority\_level: write\_data

safety\_criticality: operational

connection\_contract\_ref: contract:bim\_cde\_project\_A\_connection\_v1

payload\_contract\_refs:

  \- contract:bim\_issue\_create\_payload\_v1

  \- contract:bim\_model\_query\_payload\_v1

feedback\_schema\_refs:

  \- schema:bim\_issue\_created\_payload\_v1

  \- schema:external\_system\_status\_updated\_payload\_v1

health\_check\_policy\_ref: health:bim\_cde\_health\_check\_v1

heartbeat\_required: false

availability\_requirement: medium

fallback\_policy\_ref: fallback:bim\_cde\_unavailable\_fallback\_v1

fail\_safe\_policy\_ref: null

credential\_ref: credential:bim\_cde\_project\_A\_api

secret\_storage\_ref: vault:bim\_cde\_project\_A

network\_zone: enterprise\_network

security\_level: confidential

pii\_classification: indirect

decision\_boundary: may\_provide\_model\_and\_document\_context\_for\_decision

approval\_boundary: does\_not\_grant\_approval

execution\_boundary: may\_write\_project\_records\_but\_not\_physical\_commands

safety\_boundary: model\_information\_must\_not\_override\_runtime\_safety\_evidence

audit\_event\_refs:

  \- audit:external\_system\_registered

  \- audit:bim\_query\_performed

  \- audit:bim\_issue\_created

  \- audit:external\_system\_feedback\_received

owner\_module: knowledge\_integration\_module

owner\_team: LEDO BIM Integration

source\_document: bim\_cde\_external\_system\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_external\_system\_id: null

---

## **14\. Registry Entry Example: Notification System**

external\_system\_id: external\_system:notification\_gateway\_site\_A

canonical\_name: notification\_gateway\_site\_A

display\_name: Notification Gateway \- Site A

description: An external notification system that sends SMS, push, email, or messenger notifications to workers, managers, and safety personnel at Site A.

semantic\_iri: ledo:NotificationGatewaySiteA

external\_system\_type: NOTIFICATION\_SYSTEM

system\_category: COMMUNICATION\_SYSTEM

version: 1.0.0

status: active

site\_scope:

  \- site\_A

zone\_scope:

  \- "\*"

owner\_organization: site\_operator

operator\_team: communication\_operations\_team

vendor\_name: ExampleNotificationVendor

supported\_protocols:

  \- REST

  \- Webhook

supported\_adapter\_refs:

  \- adapter:notification\_adapter\_site\_A

supported\_action\_type\_refs:

  \- action:NOTIFY\_MANAGER

  \- action:NOTIFY\_WORKER

  \- action:REQUEST\_ACKNOWLEDGEMENT

  \- action:BROADCAST\_ALERT

supported\_execution\_request\_types:

  \- execution\_request:notification\_send\_request

  \- execution\_request:acknowledgement\_request

supported\_feedback\_event\_refs:

  \- event:NotificationSent

  \- event:NotificationFailed

  \- event:OperatorAcknowledgementReceived

supported\_capability\_refs:

  \- capability:send\_sms

  \- capability:send\_push

  \- capability:send\_email

  \- capability:send\_messenger\_message

  \- capability:receive\_acknowledgement

integration\_mode: request\_response

data\_direction: bidirectional

control\_authority\_level: request\_only

safety\_criticality: operational

connection\_contract\_ref: contract:notification\_gateway\_site\_A\_connection\_v1

payload\_contract\_refs:

  \- contract:notification\_send\_payload\_v1

  \- contract:acknowledgement\_request\_payload\_v1

feedback\_schema\_refs:

  \- schema:notification\_result\_payload\_v1

  \- schema:operator\_acknowledgement\_payload\_v1

health\_check\_policy\_ref: health:notification\_gateway\_health\_check\_v1

heartbeat\_required: false

availability\_requirement: high

fallback\_policy\_ref: fallback:notification\_fallback\_v1

fail\_safe\_policy\_ref: failsafe:notification\_fail\_safe\_v1

credential\_ref: credential:notification\_gateway\_site\_A\_api

secret\_storage\_ref: vault:notification\_gateway\_site\_A

network\_zone: enterprise\_network

security\_level: restricted

pii\_classification: direct

decision\_boundary: may\_deliver\_decision\_or\_approval\_notifications\_only

approval\_boundary: does\_not\_grant\_approval

execution\_boundary: sends\_notification\_not\_physical\_command

safety\_boundary: emergency\_notification\_must\_have\_fallback\_channel

audit\_event\_refs:

  \- audit:external\_system\_registered

  \- audit:notification\_requested

  \- audit:notification\_sent

  \- audit:notification\_failed

owner\_module: communication\_integration\_module

owner\_team: LEDO Notification Integration

source\_document: notification\_external\_system\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_external\_system\_id: null

---

## **15\. External System Lifecycle Alignment**

External Systems are connected to the following lifecycle:

External System Registration

        ↓

Contract Validation

        ↓

Security / Credential Reference Validation

        ↓

Adapter Compatibility Validation

        ↓

Health Check

        ↓

Activation

        ↓

Runtime Request / Event / Feedback

        ↓

Monitoring / Audit / Versioning

        ↓

Maintenance / Degradation / Deprecation / Retirement

The important point is that an external system being registered does not mean it can receive every Action.

The External System must be active.

It must support the Action Type.

It must be compatible with the Adapter.

The Protocol must be allowed.

The Safety Boundary must be satisfied.

The Health Check must pass.

---

## **16\. Validation Rules**

An External System Entry is valid only when the following conditions are satisfied:

1. `external_system_id` exists in the registry.  
2. Its status is `active` or another allowed runtime status.  
3. External system type is declared.  
4. Site scope or zone scope is declared.  
5. Supported protocols are declared.  
6. Supported adapter references are declared.  
7. Supported Action Types or ExecutionRequest types are declared.  
8. Connection contract is declared.  
9. Payload contract is declared.  
10. Feedback schema is declared.  
11. Control authority level is declared.  
12. Safety criticality is declared.  
13. Health check policy is declared.  
14. Credential reference is declared.  
15. Security level is declared.  
16. Decision / approval / execution / safety boundaries are declared.  
17. Audit event references are declared.  
18. Owner module is declared.  
19. Version is valid.  
20. If deprecated, migration metadata exists.

If any of these conditions are missing, the External System must not be used in the operational lifecycle.

---

## **17\. Execution Compatibility Validation**

Before an ExecutionRequest is delivered to an External System, the following validations are required:

Is the External System registered?

Is the External System active?

Does it support the Action Type of the ExecutionRequest?

Is the selected Adapter allowed for this External System?

Is the Protocol included in supported\_protocols?

Is the ExecutionRequest Type supported?

Does the Payload Contract match?

Is the Feedback Schema defined?

Does the Site / Zone Scope match?

Does it violate the Control Authority Boundary?

Does it violate the Safety Boundary?

Has the Health Check passed?

If these conditions are not satisfied, the ExecutionRequest must not be converted into an ExternalControlRequest.

---

## **18\. Health Check Rule**

External Systems must have runtime health status.

Recommended health statuses:

unknown

healthy

degraded

unavailable

maintenance

blocked

A health check may verify the following:

network reachability

authentication validity

API response latency

heartbeat freshness

protocol-level connection status

external system reported status

adapter connection status

last successful request time

last feedback received time

If health is degraded or unavailable, the following policies should be applied:

low-risk request: retry or fallback

high-risk request: hold or escalate

safety-critical request: block or fail-safe

---

## **19\. Fallback and Fail-Safe Rule**

When an External System is unavailable, fallback or fail-safe policies are required.

Fallback examples:

notification\_system unavailable

    → use secondary notification channel

robot\_fleet\_manager unavailable

    → hold dispatch and escalate to supervisor

BIM CDE unavailable

    → use cached model context and hold write operations

SCADA unavailable

    → request manual verification from control room

Fail-safe examples:

safety\_controller unreachable

    → block physical execution path

robot fleet feedback lost

    → mark mission status as unknown and request supervisor review

worker location source stale

    → prohibit Safety Gate pass

Core principle:

External System failure must not silently degrade into unsafe execution.

---

## **20\. Data Direction Rule**

External Systems must have explicit data direction.

Recommended values:

inbound

outbound

bidirectional

### **20.1 inbound**

LEDO receives data from the external system.

Examples:

weather\_api

iot\_platform

scada\_status\_stream

---

### **20.2 outbound**

LEDO sends data to the external system.

Examples:

notification\_gateway

audit\_export\_sink

---

### **20.3 bidirectional**

LEDO sends requests and receives feedback.

Examples:

robot\_fleet\_manager

site\_management\_platform

inspection\_system

---

## **21\. Control Authority Rule**

The control authority of an External System must be explicitly declared.

Recommended values:

read\_only

write\_data

request\_only

command\_capable

safety\_rated\_control

physical\_control\_authority

The important distinctions are:

write\_data:

    Can write records to the external system.

request\_only:

    Can send operational requests to the external system.

command\_capable:

    The external system can perform execution commands on its own.

safety\_rated\_control:

    Has safety-rated control logic.

physical\_control\_authority:

    Has authority to control physical equipment.

LEDO must understand the authority of each External System and must not cross its boundary.

---

## **22\. Security and Credential Rule**

`external_system_registry` must not store actual secret values.

It should store references only.

credential\_ref: credential:robot\_fleet\_manager\_site\_A\_api

secret\_storage\_ref: vault:robot\_fleet\_manager\_site\_A

Actual tokens, passwords, certificates, and private keys must be stored in Vault or a Secret Manager.

Security principles:

No raw secrets in external\_system\_registry.

mTLS or signed request should be used for safety-critical integrations.

Credential rotation must be supported.

Access to external systems must be auditable.

---

## **23\. Relationship to Adapter Registry**

`adapter_registry` and `external_system_registry` are strongly connected.

adapter\_registry:

    Which adapter instance can handle which request?

external\_system\_registry:

    Is the external system targeted by that adapter registered,

    and does it allow the action, protocol, and scope?

Flow:

ExecutionRequest

    ↓

adapter\_registry selects compatible adapter

    ↓

external\_system\_registry validates target external system

    ↓

ExternalControlRequest

    ↓

Adapter sends request to External System

Even if an Adapter is registered, the execution path is not valid if the External System is not registered.

---

## **24\. Relationship to Action Registry**

`action_registry` declares which Action Types may have an external execution path.

`external_system_registry` defines whether the actual external system can receive that Action Type.

action\_registry:

    DISPATCH\_ROBOT may have an external execution path.

external\_system\_registry:

    robot\_fleet\_manager\_site\_A supports DISPATCH\_ROBOT.

Even if an Action Type is registered, an execution request cannot be sent if the External System does not support that Action Type.

---

## **25\. Relationship to Approval Registry**

Even if approval exists, that does not mean the request can be sent to an External System.

approval\_registry:

    Who may approve an Action, under what conditions?

external\_system\_registry:

    Does an external system exist that can actually receive the approved Action?

Approval does not replace External System compatibility.

Approval pass ≠ External System compatibility pass

---

## **26\. Relationship to Safety Gate**

The Safety Gate performs final validation before the ExecutionRequest.

External System Registry provides external-system-related conditions that the Safety Gate should verify.

Examples:

Is the external system active?

Has the health check passed?

Is the external system safety-critical?

Does a fail-safe policy exist?

Is the feedback schema defined?

Is the safety boundary explicit?

Core principle:

Safety Gate must validate external system readiness before execution preparation.

---

## **27\. Relationship to Event Registry**

An External System may be an event producer or event consumer.

Examples:

RobotStatusUpdated

ExecutionResultReceived

SCADAStatusFeedbackReceived

NotificationSent

ExternalSystemStatusUpdated

`event_registry` defines the Event Type and schema.

`external_system_registry` defines which external system may produce or consume that event.

---

## **28\. Relationship to Evidence Registry**

An External System may be an evidence source.

Examples:

robot\_availability\_snapshot

equipment\_status\_snapshot

scada\_status\_feedback\_evidence

execution\_result\_evidence

external\_system\_reachable\_snapshot

`evidence_registry` defines the Evidence Type and quality rules.

`external_system_registry` provides the basis for determining which external system the evidence came from and whether that source is trustworthy.

---

## **29\. Relationship to Runtime Validation Registry**

Runtime Validation may verify the status of an external system.

Examples:

external\_system\_reachable

adapter\_health\_valid

robot\_fleet\_manager\_available

scada\_connection\_valid

safety\_controller\_reachable

`runtime_validation_registry` defines which validation should be performed.

`external_system_registry` provides the target external system and health policy for validation.

---

## **30\. Relationship to Ontology**

Every important External System should have a semantic IRI.

Example:

external\_system\_id: external\_system:robot\_fleet\_manager\_site\_A

semantic\_iri: ledo:RobotFleetManagerSiteA

In the ontology, it may be defined as follows:

ledo:RobotFleetManagerSiteA

    rdf:type ledo:ExternalSystem ;

    rdfs:subClassOf ledo:RobotFleetManager ;

    ledo:supportsAction ledo:DispatchRobotAction ;

    ledo:usesProtocol ledo:REST ;

    ledo:hasControlAuthority ledo:CommandCapable ;

    ledo:hasSafetyBoundary ledo:RobotVendorSafetyBoundary .

Ontology provides the semantic foundation of External Systems.

External System Registry manages this foundation in the operational system through version, status, protocol, adapter, health, credential, safety boundary, and audit rules.

---

## **31\. Versioning and Migration**

External System Entries must be versioned.

A version change is required when any of the following changes:

1. External system type changes  
2. Supported protocols change  
3. Supported adapters change  
4. Supported Action Types change  
5. Supported ExecutionRequest Types change  
6. Payload contracts change  
7. Feedback schemas change  
8. Control authority level changes  
9. Safety criticality changes  
10. Credential reference changes  
11. Health check policy changes  
12. Fallback / fail-safe policy changes  
13. Decision / approval / execution / safety boundaries change

Status values:

draft

active

maintenance

degraded

deprecated

retired

blocked

A deprecated External System must declare:

deprecated\_since: datetime

replacement\_external\_system\_id: string | null

migration\_notes: string

A blocked External System must not be used as the target of a new ExecutionRequest.

---

## **32\. Implementation Use**

`external_system_registry` is used to generate or validate:

1. `ExternalSystemType` enum  
2. `ExternalSystemStatus` enum  
3. `IntegrationMode` enum  
4. External system metadata DTO  
5. External system compatibility validation  
6. Adapter-to-external-system compatibility validation  
7. ExecutionRequest external target validation  
8. Protocol compatibility validation  
9. Site / zone scope validation  
10. Control authority boundary validation  
11. Safety criticality validation  
12. Health check lookup  
13. Credential reference lookup  
14. Feedback schema lookup  
15. Fallback / fail-safe policy lookup  
16. Audit log expectations  
17. Test case generation  
18. Migration rules

Implementation must prevent ExecutionRequests from being sent to unregistered External Systems.

---

## **33\. Recommended Code Structure**

registries/

    external\_system\_registry/

        external\_system\_registry.py

        external\_system\_entry.py

        external\_system\_type.py

        external\_system\_status.py

        integration\_mode.py

        control\_authority.py

        safety\_criticality.py

        external\_system\_validation.py

        external\_system\_errors.py

        external\_system\_loader.py

        external\_system\_migration.py

    adapter\_registry/

    action\_registry/

    event\_registry/

    evidence\_registry/

    runtime\_validation\_registry/

    schema\_registry/

    audit\_event\_registry/

---

## **34\. Minimal Pydantic Model**

from enum import Enum

from pydantic import BaseModel, Field

from typing import Optional

from datetime import datetime

class ExternalSystemStatus(str, Enum):

    DRAFT \= "draft"

    ACTIVE \= "active"

    MAINTENANCE \= "maintenance"

    DEGRADED \= "degraded"

    DEPRECATED \= "deprecated"

    RETIRED \= "retired"

    BLOCKED \= "blocked"

class ExternalSystemType(str, Enum):

    ROBOT\_FLEET\_MANAGER \= "robot\_fleet\_manager"

    ROBOT\_MIDDLEWARE \= "robot\_middleware"

    PLC\_SYSTEM \= "plc\_system"

    SCADA\_SYSTEM \= "scada\_system"

    SAFETY\_CONTROLLER \= "safety\_controller"

    BIM\_CDE\_PLATFORM \= "bim\_cde\_platform"

    SITE\_MANAGEMENT\_PLATFORM \= "site\_management\_platform"

    NOTIFICATION\_SYSTEM \= "notification\_system"

    INSPECTION\_SYSTEM \= "inspection\_system"

    ERP\_SYSTEM \= "erp\_system"

    CMMS\_SYSTEM \= "cmms\_system"

    IOT\_PLATFORM \= "iot\_platform"

    VISION\_SYSTEM \= "vision\_system"

    WEATHER\_SERVICE \= "weather\_service"

    GIS\_SYSTEM \= "gis\_system"

    DOCUMENT\_MANAGEMENT\_SYSTEM \= "document\_management\_system"

class IntegrationMode(str, Enum):

    READ\_ONLY \= "read\_only"

    WRITE\_ONLY \= "write\_only"

    READ\_WRITE \= "read\_write"

    REQUEST\_RESPONSE \= "request\_response"

    EVENT\_STREAM \= "event\_stream"

    COMMAND\_GATEWAY \= "command\_gateway"

class DataDirection(str, Enum):

    INBOUND \= "inbound"

    OUTBOUND \= "outbound"

    BIDIRECTIONAL \= "bidirectional"

class ControlAuthorityLevel(str, Enum):

    READ\_ONLY \= "read\_only"

    WRITE\_DATA \= "write\_data"

    REQUEST\_ONLY \= "request\_only"

    COMMAND\_CAPABLE \= "command\_capable"

    SAFETY\_RATED\_CONTROL \= "safety\_rated\_control"

    PHYSICAL\_CONTROL\_AUTHORITY \= "physical\_control\_authority"

class SafetyCriticality(str, Enum):

    NON\_CRITICAL \= "non\_critical"

    OPERATIONAL \= "operational"

    SAFETY\_RELEVANT \= "safety\_relevant"

    SAFETY\_CRITICAL \= "safety\_critical"

    SAFETY\_RATED \= "safety\_rated"

class SecurityLevel(str, Enum):

    INTERNAL \= "internal"

    CONFIDENTIAL \= "confidential"

    RESTRICTED \= "restricted"

    SAFETY\_CRITICAL \= "safety\_critical"

class PIIClassification(str, Enum):

    NONE \= "none"

    INDIRECT \= "indirect"

    DIRECT \= "direct"

    SENSITIVE \= "sensitive"

class ExternalSystemRegistryEntry(BaseModel):

    external\_system\_id: str

    canonical\_name: str

    display\_name: str

    description: str

    semantic\_iri: str

    external\_system\_type: ExternalSystemType

    system\_category: str

    version: str

    status: ExternalSystemStatus \= ExternalSystemStatus.DRAFT

    site\_scope: list\[str\] \= Field(default\_factory=list)

    zone\_scope: list\[str\] \= Field(default\_factory=list)

    owner\_organization: str

    operator\_team: str

    vendor\_name: Optional\[str\] \= None

    supported\_protocols: list\[str\] \= Field(default\_factory=list)

    supported\_adapter\_refs: list\[str\] \= Field(default\_factory=list)

    supported\_action\_type\_refs: list\[str\] \= Field(default\_factory=list)

    supported\_execution\_request\_types: list\[str\] \= Field(default\_factory=list)

    supported\_feedback\_event\_refs: list\[str\] \= Field(default\_factory=list)

    supported\_capability\_refs: list\[str\] \= Field(default\_factory=list)

    integration\_mode: IntegrationMode

    data\_direction: DataDirection

    control\_authority\_level: ControlAuthorityLevel

    safety\_criticality: SafetyCriticality

    connection\_contract\_ref: str

    payload\_contract\_refs: list\[str\] \= Field(default\_factory=list)

    feedback\_schema\_refs: list\[str\] \= Field(default\_factory=list)

    health\_check\_policy\_ref: str

    heartbeat\_required: bool \= False

    availability\_requirement: str

    fallback\_policy\_ref: Optional\[str\] \= None

    fail\_safe\_policy\_ref: Optional\[str\] \= None

    credential\_ref: str

    secret\_storage\_ref: str

    network\_zone: str

    security\_level: SecurityLevel

    pii\_classification: PIIClassification \= PIIClassification.NONE

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

    replacement\_external\_system\_id: Optional\[str\] \= None

---

## **35\. Core Validation Function**

def validate\_external\_system\_for\_execution(

    entry: ExternalSystemRegistryEntry,

    action\_type\_ref: str,

    execution\_request\_type: str,

    adapter\_ref: str,

    protocol: str,

    site\_id: str,

    zone\_id: str | None \= None,

) \-\> None:

    if entry.status \!= ExternalSystemStatus.ACTIVE:

        raise InvalidExternalSystemError(

            f"External System is not active: {entry.external\_system\_id}"

        )

    if action\_type\_ref not in entry.supported\_action\_type\_refs:

        raise ExternalSystemActionNotSupportedError(

            f"Action Type '{action\_type\_ref}' is not supported by "

            f"External System '{entry.external\_system\_id}'"

        )

    if execution\_request\_type not in entry.supported\_execution\_request\_types:

        raise ExternalSystemExecutionRequestNotSupportedError(

            f"ExecutionRequest Type '{execution\_request\_type}' is not supported by "

            f"External System '{entry.external\_system\_id}'"

        )

    if adapter\_ref not in entry.supported\_adapter\_refs:

        raise ExternalSystemAdapterNotAllowedError(

            f"Adapter '{adapter\_ref}' is not allowed for "

            f"External System '{entry.external\_system\_id}'"

        )

    if protocol not in entry.supported\_protocols:

        raise ExternalSystemProtocolNotSupportedError(

            f"Protocol '{protocol}' is not supported by "

            f"External System '{entry.external\_system\_id}'"

        )

    if site\_id not in entry.site\_scope and "\*" not in entry.site\_scope:

        raise ExternalSystemScopeViolationError(

            f"Site '{site\_id}' is not within allowed site scope"

        )

    if zone\_id is not None:

        if zone\_id not in entry.zone\_scope and "\*" not in entry.zone\_scope:

            raise ExternalSystemScopeViolationError(

                f"Zone '{zone\_id}' is not within allowed zone scope"

            )

    if not entry.connection\_contract\_ref:

        raise InvalidExternalSystemError(

            "connection\_contract\_ref must be declared"

        )

    if not entry.payload\_contract\_refs:

        raise InvalidExternalSystemError(

            "payload\_contract\_refs must be declared"

        )

    if not entry.feedback\_schema\_refs:

        raise InvalidExternalSystemError(

            "feedback\_schema\_refs must be declared"

        )

    if not entry.health\_check\_policy\_ref:

        raise InvalidExternalSystemError(

            "health\_check\_policy\_ref must be declared"

        )

    if not entry.credential\_ref or not entry.secret\_storage\_ref:

        raise InvalidExternalSystemError(

            "credential\_ref and secret\_storage\_ref must be declared"

        )

    if not entry.execution\_boundary:

        raise InvalidExternalSystemError(

            "execution\_boundary must be declared"

        )

    if not entry.safety\_boundary:

        raise InvalidExternalSystemError(

            "safety\_boundary must be declared"

        )

---

## **36\. Test Scenarios**

Required tests:

1\. Reject unregistered External System.

2\. Reject inactive External System.

3\. Reject high-risk requests to an External System in maintenance status.

4\. Reject safety-critical requests to a degraded External System.

5\. Reject blocked External System usage.

6\. Reject unsupported Action Type.

7\. Reject unsupported ExecutionRequest Type.

8\. Reject unauthorized Adapter connection.

9\. Reject unsupported Protocol.

10\. Reject site scope mismatch.

11\. Reject zone scope mismatch.

12\. Reject missing connection contract.

13\. Reject missing payload contract.

14\. Reject missing feedback schema.

15\. Reject missing health check policy.

16\. Reject missing credential reference.

17\. Verify that raw secrets are not stored.

18\. Reject missing safety boundary.

19\. Verify Safety Gate validation is required for command-capable systems.

20\. Verify External System migration rules.

---

## **37\. Final Rule**

No registered External System,

no valid ExternalControlRequest.

If the External System is not active,

the ExecutionRequest cannot be delivered.

If the External System does not support the Action Type,

the ExecutionRequest cannot be delivered.

If the External System does not allow the Adapter,

the connection is invalid.

If the External System does not support the Protocol,

the request cannot be sent.

If the External System has no Safety Boundary,

it cannot be used as a physical execution path.

External System is not Adapter.

External System is not Approval.

External System is not Safety Gate.

External System is not LEDO internal control logic.

`external_system_registry` is the core deterministic registry that governs identity, authority, connection, and safety boundaries between LEDO and external physical or operational systems.

This module prevents connection to unregistered external systems and clearly defines each external system’s protocol, adapter compatibility, capability, action support, feedback schema, health check, credential reference, and safety boundary.

The core definition is:

External System Registry

\= not a list of external system names,

but an operational contract registry that controls

the identity, type, authority, protocol, adapter compatibility,

capability, health, security, feedback, and safety boundary

of every external system connected to LEDO.

# 

# **external\_system\_registry 설계 보고서**

## **1\. 개요**

`external_system_registry`는 LEDO Ontology-Centric Cyber-Physical System과 연결되는 모든 외부 시스템의 종류, 신원, 역할, 연결 방식, 지원 기능, 권한 경계, 안전 등급, 데이터 방향, 통신 계약, 피드백 계약, 감사 규칙을 정의하고 통제하는 핵심 레지스트리이다.

이 모듈의 목적은 LEDO가 승인된 Action 또는 ExecutionRequest를 외부 시스템으로 전달하기 전에, 해당 외부 시스템이 실제로 등록되어 있고, 신뢰 가능하며, 허용된 범위 안에서만 통신 가능한지 검증하는 것이다.

`external_system_registry`는 단순한 외부 시스템 목록이 아니다.

이 레지스트리는 다음을 정의하는 **외부 시스템 신원·권한·연결·안전 경계 운영 계약 레지스트리**이다.

어떤 외부 시스템이 LEDO와 연결될 수 있는가?  
그 외부 시스템은 어떤 종류의 시스템인가?  
그 시스템은 read-only인가, command-capable인가?  
어떤 Action Type 또는 ExecutionRequest를 받을 수 있는가?  
어떤 adapter를 통해서만 연결될 수 있는가?  
어떤 protocol을 사용하는가?  
그 시스템은 safety-critical인가?  
그 시스템은 physical control authority를 가지는가?  
LEDO는 그 시스템에 어느 수준까지 요청할 수 있는가?  
그 시스템의 feedback은 어떤 schema로 수신해야 하는가?  
그 시스템이 unavailable하면 어떤 fallback 또는 fail-safe 정책을 따라야 하는가?

즉, `external_system_registry`는 LEDO 내부 세계와 외부 물리·운영 시스템 사이의 **공식 시스템 계약서**이다.

---

## **2\. 핵심 원칙**

External System은 LEDO 내부 모듈이 아니다.

External System은 Adapter와 다르다.

External System은 Action Registry가 아니다.

External System은 Safety Gate가 아니다.

External System은 Approval Authority가 아니다.

External System은 실제 물리 실행 또는 외부 업무 실행을 담당할 수 있다.

하지만 LEDO는 외부 시스템의 내부 제어 로직을 소유하거나 대체하지 않는다.

핵심 원칙은 다음과 같다.

LEDO defines intent, constraints, approval, safety boundary, and audit.

Adapter translates LEDO request into an external integration protocol.

External System performs domain-specific execution or returns authoritative external state.

특히 로봇, PLC, SCADA, 안전 컨트롤러와 같은 시스템에서는 다음 원칙이 중요하다.

LEDO must not bypass external safety-rated systems.

LEDO must not directly generate low-level physical control commands.

LEDO must interact with external systems through registered adapters and approved integration contracts.

---

## **3\. LEDO 아키텍처 내 위치**

`external_system_registry`는 Execution Request & External Control Integration Layer에 위치한다.

ApprovedAction  
        ↓  
Safety Gate  
        ↓  
ExecutionRequest  
        ↓  
adapter\_registry  
        ↓  
external\_system\_registry validation  
        ↓  
ExternalControlRequest  
        ↓  
External Adapter  
        ↓  
External System  
        ↓  
ExecutionResult / FeedbackEvent

전체 흐름에서 `external_system_registry`는 다음 질문에 답한다.

이 외부 시스템은 등록되어 있는가?  
이 Action을 받을 수 있는 시스템인가?  
이 adapter가 이 외부 시스템에 연결해도 되는가?  
이 protocol은 허용되어 있는가?  
이 시스템은 현재 active 상태인가?  
이 시스템의 safety boundary를 침범하지 않는가?  
이 시스템은 어떤 feedback을 반환해야 하는가?

---

## **4\. 목적**

`external_system_registry`의 목적은 다음과 같다.

1. 등록되지 않은 외부 시스템 연결 방지  
2. 외부 시스템의 신원과 종류 정의  
3. 외부 시스템별 지원 기능 및 capability 정의  
4. 외부 시스템별 read/write/command 권한 정의  
5. 외부 시스템별 protocol 및 integration contract 정의  
6. 외부 시스템별 연결 가능한 adapter 제한  
7. 외부 시스템별 Action Type / ExecutionRequest 지원 범위 정의  
8. safety-critical system과 non-safety system 구분  
9. physical control authority 경계 정의  
10. feedback event 및 result schema 정의  
11. health check 및 availability rule 정의  
12. fallback / fail-safe 정책 정의  
13. credential reference 및 security boundary 정의  
14. external system audit 및 trace rule 정의  
15. versioning 및 migration 관리

---

## **5\. 핵심 구분**

### **5.1 External System**

`External System`은 LEDO 외부에 존재하며, 데이터 제공, 상태 보고, 업무 처리, 물리 실행, 알림 발송, 현장 플랫폼 연동 등을 담당하는 시스템이다.

예시:

robot\_fleet\_manager  
robot\_middleware  
plc\_system  
scada\_system  
safety\_controller  
bim\_cde\_platform  
site\_management\_platform  
notification\_system  
inspection\_system  
erp\_system  
cmms\_system  
weather\_api  
camera\_vms  
iot\_platform

---

### **5.2 External System Type**

External System Type은 외부 시스템의 종류이다.

예시:

ROBOT\_FLEET\_MANAGER  
ROBOT\_MIDDLEWARE  
PLC\_SYSTEM  
SCADA\_SYSTEM  
SAFETY\_CONTROLLER  
BIM\_CDE\_PLATFORM  
SITE\_MANAGEMENT\_PLATFORM  
NOTIFICATION\_SYSTEM  
INSPECTION\_SYSTEM  
ERP\_SYSTEM  
CMMS\_SYSTEM  
IOT\_PLATFORM  
VISION\_SYSTEM  
WEATHER\_SERVICE

External System Type은 integration boundary, protocol, safety level, action support, feedback contract를 결정하는 기준이다.

---

### **5.3 External System Instance**

External System Instance는 실제 운영 환경에 존재하는 개별 외부 시스템이다.

예시:

robot\_fleet\_manager\_site\_A  
scada\_system\_tower\_B  
plc\_gateway\_crane\_01  
bim\_cde\_project\_alpha  
notification\_system\_kakao\_site\_A

External System Type은 설계 기준이고, External System Instance는 실제 연결 대상이다.

---

### **5.4 Adapter와 External System의 차이**

Adapter는 LEDO 내부 integration module이다.

External System은 LEDO 외부의 실제 시스템이다.

adapter\_registry:  
    어떤 adapter instance가 ExecutionRequest를 외부 protocol로 변환할 수 있는가?

external\_system\_registry:  
    어떤 외부 시스템이 존재하고, 어떤 권한과 경계 안에서 연결 가능한가?

예시:

robot\_fleet\_adapter  
    → LEDO 내부 adapter

robot\_fleet\_manager\_site\_A  
    → 실제 외부 로봇 fleet system

Adapter는 통신 번역자이고, External System은 외부 권한 시스템이다.

---

### **5.5 External Control Authority**

External Control Authority는 외부 시스템이 물리 또는 운영 실행 권한을 가지는지 나타낸다.

권장 값:

read\_only  
write\_data  
request\_only  
command\_capable  
safety\_rated\_control  
physical\_control\_authority

LEDO가 직접 physical command를 생성하지 않더라도, 외부 시스템은 physical control authority를 가질 수 있다.

예시:

robot\_fleet\_manager:  
    command\_capable

plc\_system:  
    physical\_control\_authority

safety\_controller:  
    safety\_rated\_control

bim\_cde\_platform:  
    write\_data

weather\_api:  
    read\_only

---

## **6\. Scope**

`external_system_registry`는 다음 항목을 통제한다.

external\_system\_id: string  
canonical\_name: string  
display\_name: string  
description: string  
semantic\_iri: string

external\_system\_type: string  
system\_category: string

version: string  
status: draft | active | maintenance | degraded | deprecated | retired | blocked

site\_scope:  
  \- string

zone\_scope:  
  \- string

owner\_organization: string  
operator\_team: string  
vendor\_name: string | null

supported\_protocols:  
  \- string

supported\_adapter\_refs:  
  \- string

supported\_action\_type\_refs:  
  \- string

supported\_execution\_request\_types:  
  \- string

supported\_feedback\_event\_refs:  
  \- string

supported\_capability\_refs:  
  \- string

integration\_mode: read\_only | write\_only | read\_write | request\_response | event\_stream | command\_gateway

data\_direction: inbound | outbound | bidirectional

control\_authority\_level: read\_only | write\_data | request\_only | command\_capable | safety\_rated\_control | physical\_control\_authority

safety\_criticality: non\_critical | operational | safety\_relevant | safety\_critical | safety\_rated

connection\_contract\_ref: string  
payload\_contract\_refs:  
  \- string

feedback\_schema\_refs:  
  \- string

health\_check\_policy\_ref: string  
heartbeat\_required: boolean  
availability\_requirement: string

fallback\_policy\_ref: string | null  
fail\_safe\_policy\_ref: string | null

credential\_ref: string  
secret\_storage\_ref: string

network\_zone: string  
security\_level: internal | confidential | restricted | safety\_critical  
pii\_classification: none | indirect | direct | sensitive

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
replacement\_external\_system\_id: string | null

---

## **7\. Non-Scope**

`external_system_registry`는 다음을 정의하지 않는다.

1. 실제 adapter 구현 코드  
2. adapter instance 선택 로직  
3. low-level robot motion planning  
4. PLC ladder logic  
5. SCADA 내부 control logic  
6. safety-rated controller 내부 로직  
7. 실제 password, token, private key 값  
8. 외부 시스템 vendor 내부 데이터 모델 전체  
9. 외부 시스템 자체의 user account 관리 전체  
10. policy pass/fail logic 전체  
11. Safety Gate 최종 판정  
12. approval authority  
13. raw sensor driver logic  
14. 물리 장비 내부 firmware logic

이 책임들은 각각 다음 모듈 또는 시스템에 속한다.

adapter\_registry  
adapter implementation  
vault / secret manager  
policy\_registry  
approval\_registry  
safety\_gate  
identity\_registry  
external vendor system  
robot fleet manager  
PLC / SCADA  
safety-rated controller  
sensor gateway

---

## **8\. External System Type 모델**

권장 External System Type은 다음과 같다.

ROBOT\_FLEET\_MANAGER  
ROBOT\_MIDDLEWARE  
PLC\_SYSTEM  
SCADA\_SYSTEM  
SAFETY\_CONTROLLER  
BIM\_CDE\_PLATFORM  
SITE\_MANAGEMENT\_PLATFORM  
NOTIFICATION\_SYSTEM  
INSPECTION\_SYSTEM  
ERP\_SYSTEM  
CMMS\_SYSTEM  
IOT\_PLATFORM  
VISION\_SYSTEM  
WEATHER\_SERVICE  
GIS\_SYSTEM  
DOCUMENT\_MANAGEMENT\_SYSTEM

### **8.1 ROBOT\_FLEET\_MANAGER**

로봇 fleet의 mission, dispatch, route, status, feedback을 관리하는 외부 시스템이다.

예시:

robot\_fleet\_manager\_site\_A

LEDO는 이 시스템에 high-level mission request를 보낼 수 있지만, low-level motion primitive를 생성하면 안 된다.

---

### **8.2 PLC\_SYSTEM**

장비 또는 설비 제어를 담당하는 외부 시스템이다.

예시:

plc\_gateway\_crane\_01  
plc\_gateway\_batching\_plant\_01

LEDO는 PLC 내부 logic을 직접 제어하지 않는다.  
필요한 경우 등록된 adapter와 안전 검증을 통해 제한된 요청만 전달한다.

---

### **8.3 SCADA\_SYSTEM**

현장 설비 또는 산업 제어 상태를 모니터링하고 일부 운영 명령을 관리하는 외부 시스템이다.

예시:

scada\_system\_site\_A

SCADA는 주로 monitoring, alert, operator workflow와 연결된다.

---

### **8.4 SAFETY\_CONTROLLER**

비상정지, 안전 인터락, safety-rated logic을 담당하는 시스템이다.

예시:

safety\_controller\_zone\_03

LEDO는 safety controller를 우회하면 안 된다.

---

### **8.5 BIM\_CDE\_PLATFORM**

BIM, CDE, 도면, 모델, 문서, 이슈, 변경 정보를 관리하는 외부 플랫폼이다.

예시:

autodesk\_construction\_cloud\_project\_A  
bim360\_project\_A  
open\_cde\_project\_A

---

### **8.6 SITE\_MANAGEMENT\_PLATFORM**

현장 작업, 일정, 이슈, 작업일보, 검사 요청, 안전 지시 등을 관리하는 플랫폼이다.

예시:

site\_management\_platform\_A

---

### **8.7 NOTIFICATION\_SYSTEM**

작업자, 관리자, 안전 담당자에게 알림을 발송하는 시스템이다.

예시:

sms\_gateway  
kakao\_notification\_gateway  
email\_service  
push\_notification\_service

---

### **8.8 INSPECTION\_SYSTEM**

검사, 점검, 품질 관리, 안전 점검 기록을 관리하는 시스템이다.

예시:

inspection\_platform\_site\_A  
quality\_inspection\_system\_A

---

## **9\. Integration Mode 모델**

권장 integration mode는 다음과 같다.

read\_only  
write\_only  
read\_write  
request\_response  
event\_stream  
command\_gateway

### **9.1 read\_only**

LEDO가 외부 시스템에서 데이터만 읽는다.

예시:

weather\_api  
bim\_model\_viewer  
read\_only\_scada\_monitor

---

### **9.2 write\_only**

LEDO가 외부 시스템에 기록만 보낸다.

예시:

audit\_export\_sink  
notification\_sink

---

### **9.3 read\_write**

LEDO가 읽기와 쓰기를 모두 수행할 수 있다.

예시:

site\_management\_platform  
inspection\_platform

---

### **9.4 request\_response**

LEDO가 요청을 보내고 결과를 받는다.

예시:

robot\_fleet\_manager  
inspection\_system

---

### **9.5 event\_stream**

외부 시스템과 event stream 방식으로 연결된다.

예시:

iot\_platform  
robot\_status\_stream  
scada\_event\_stream

---

### **9.6 command\_gateway**

물리 제어 또는 운영 명령 경로를 제공하는 시스템이다.

이 mode는 가장 엄격히 통제되어야 한다.

예시:

plc\_gateway  
robot\_fleet\_manager  
safety\_controller\_interface

---

## **10\. Registry Entry Schema**

각 External System Registry entry는 다음 구조를 따른다.

external\_system\_id: string  
canonical\_name: string  
display\_name: string  
description: string  
semantic\_iri: string

external\_system\_type: string  
system\_category: string

version: string  
status: draft | active | maintenance | degraded | deprecated | retired | blocked

site\_scope:  
  \- string

zone\_scope:  
  \- string

owner\_organization: string  
operator\_team: string  
vendor\_name: string | null

supported\_protocols:  
  \- string

supported\_adapter\_refs:  
  \- string

supported\_action\_type\_refs:  
  \- string

supported\_execution\_request\_types:  
  \- string

supported\_feedback\_event\_refs:  
  \- string

supported\_capability\_refs:  
  \- string

integration\_mode: string  
data\_direction: string  
control\_authority\_level: string  
safety\_criticality: string

connection\_contract\_ref: string  
payload\_contract\_refs:  
  \- string

feedback\_schema\_refs:  
  \- string

health\_check\_policy\_ref: string  
heartbeat\_required: boolean  
availability\_requirement: string

fallback\_policy\_ref: string | null  
fail\_safe\_policy\_ref: string | null

credential\_ref: string  
secret\_storage\_ref: string

network\_zone: string  
security\_level: string  
pii\_classification: string

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
replacement\_external\_system\_id: string | null

---

## **11\. Registry Entry 예시: Robot Fleet Manager**

external\_system\_id: external\_system:robot\_fleet\_manager\_site\_A  
canonical\_name: robot\_fleet\_manager\_site\_A  
display\_name: Robot Fleet Manager \- Site A  
description: Site A에서 로봇 mission dispatch, fleet status, mission feedback을 관리하는 외부 로봇 fleet 시스템이다.  
semantic\_iri: ledo:RobotFleetManagerSiteA

external\_system\_type: ROBOT\_FLEET\_MANAGER  
system\_category: ROBOTICS\_SYSTEM

version: 1.0.0  
status: active

site\_scope:  
  \- site\_A

zone\_scope:  
  \- zone\_01  
  \- zone\_02  
  \- zone\_03

owner\_organization: robot\_vendor\_or\_site\_operator  
operator\_team: robot\_operations\_team  
vendor\_name: ExampleRobotVendor

supported\_protocols:  
  \- REST  
  \- WebSocket  
  \- MQTT

supported\_adapter\_refs:  
  \- adapter:robot\_fleet\_adapter\_site\_A

supported\_action\_type\_refs:  
  \- action:DISPATCH\_ROBOT  
  \- action:REPLAN\_ROUTE  
  \- action:PAUSE\_MISSION  
  \- action:RETURN\_TO\_BASE

supported\_execution\_request\_types:  
  \- execution\_request:robot\_mission\_request  
  \- execution\_request:robot\_route\_replan\_request  
  \- execution\_request:robot\_pause\_request

supported\_feedback\_event\_refs:  
  \- event:RobotMissionFeedbackReceived  
  \- event:ExecutionResultReceived  
  \- event:RobotStatusUpdated

supported\_capability\_refs:  
  \- capability:robot\_dispatch  
  \- capability:mission\_status\_reporting  
  \- capability:route\_replan  
  \- capability:return\_to\_base

integration\_mode: request\_response  
data\_direction: bidirectional  
control\_authority\_level: command\_capable  
safety\_criticality: safety\_relevant

connection\_contract\_ref: contract:robot\_fleet\_manager\_site\_A\_connection\_v1

payload\_contract\_refs:  
  \- contract:robot\_mission\_request\_payload\_v1  
  \- contract:robot\_feedback\_payload\_v1

feedback\_schema\_refs:  
  \- schema:robot\_mission\_feedback\_v1  
  \- schema:execution\_result\_received\_payload\_v1

health\_check\_policy\_ref: health:robot\_fleet\_manager\_health\_check\_v1  
heartbeat\_required: true  
availability\_requirement: high

fallback\_policy\_ref: fallback:robot\_dispatch\_fallback\_v1  
fail\_safe\_policy\_ref: failsafe:robot\_mission\_fail\_safe\_v1

credential\_ref: credential:robot\_fleet\_manager\_site\_A\_api  
secret\_storage\_ref: vault:robot\_fleet\_manager\_site\_A

network\_zone: site\_secure\_network  
security\_level: restricted  
pii\_classification: none

decision\_boundary: may\_receive\_approved\_robot\_mission\_intent\_only  
approval\_boundary: does\_not\_grant\_approval  
execution\_boundary: accepts\_high\_level\_mission\_request\_not\_motion\_primitives  
safety\_boundary: must\_enforce\_robot\_vendor\_safety\_and\_site\_safety\_constraints

audit\_event\_refs:  
  \- audit:external\_system\_registered  
  \- audit:external\_system\_request\_sent  
  \- audit:external\_system\_feedback\_received  
  \- audit:external\_system\_health\_changed

owner\_module: execution\_integration\_module  
owner\_team: LEDO Robotics Integration  
source\_document: robot\_external\_system\_contract\_v1  
created\_at: 2026-06-26T00:00:00Z  
updated\_at: 2026-06-26T00:00:00Z  
deprecated\_since: null  
replacement\_external\_system\_id: null

---

## **12\. Registry Entry 예시: SCADA System**

external\_system\_id: external\_system:scada\_system\_site\_A  
canonical\_name: scada\_system\_site\_A  
display\_name: SCADA System \- Site A  
description: Site A의 설비 상태, alarm, 일부 운영 상태 정보를 제공하는 SCADA 외부 시스템이다.  
semantic\_iri: ledo:SCADASystemSiteA

external\_system\_type: SCADA\_SYSTEM  
system\_category: INDUSTRIAL\_CONTROL\_SYSTEM

version: 1.0.0  
status: active

site\_scope:  
  \- site\_A

zone\_scope:  
  \- plant\_zone  
  \- equipment\_zone

owner\_organization: site\_operator  
operator\_team: control\_room\_team  
vendor\_name: ExampleSCADAVendor

supported\_protocols:  
  \- OPC-UA  
  \- MQTT  
  \- REST

supported\_adapter\_refs:  
  \- adapter:scada\_adapter\_site\_A

supported\_action\_type\_refs:  
  \- action:NOTIFY\_MANAGER  
  \- action:REQUEST\_INSPECTION  
  \- action:LOCK\_ZONE

supported\_execution\_request\_types:  
  \- execution\_request:scada\_notification\_request  
  \- execution\_request:inspection\_request

supported\_feedback\_event\_refs:  
  \- event:SCADAStatusFeedbackReceived  
  \- event:EquipmentStatusChanged  
  \- event:ExecutionResultReceived

supported\_capability\_refs:  
  \- capability:equipment\_status\_reporting  
  \- capability:alarm\_reporting  
  \- capability:scada\_notification

integration\_mode: read\_write  
data\_direction: bidirectional  
control\_authority\_level: request\_only  
safety\_criticality: safety\_relevant

connection\_contract\_ref: contract:scada\_system\_site\_A\_connection\_v1

payload\_contract\_refs:  
  \- contract:scada\_status\_query\_payload\_v1  
  \- contract:scada\_notification\_payload\_v1

feedback\_schema\_refs:  
  \- schema:scada\_status\_feedback\_v1  
  \- schema:equipment\_status\_changed\_payload\_v1

health\_check\_policy\_ref: health:scada\_health\_check\_v1  
heartbeat\_required: true  
availability\_requirement: high

fallback\_policy\_ref: fallback:scada\_unavailable\_fallback\_v1  
fail\_safe\_policy\_ref: failsafe:scada\_fail\_safe\_v1

credential\_ref: credential:scada\_site\_A\_api  
secret\_storage\_ref: vault:scada\_site\_A

network\_zone: industrial\_secure\_network  
security\_level: safety\_critical  
pii\_classification: none

decision\_boundary: may\_provide\_status\_and\_alarm\_data\_for\_decision  
approval\_boundary: does\_not\_grant\_approval  
execution\_boundary: does\_not\_allow\_direct\_low\_level\_control\_from\_LEDO  
safety\_boundary: must\_not\_bypass\_scada\_or\_safety\_controller\_interlocks

audit\_event\_refs:  
  \- audit:external\_system\_registered  
  \- audit:external\_system\_status\_read  
  \- audit:external\_system\_request\_sent  
  \- audit:external\_system\_feedback\_received

owner\_module: execution\_integration\_module  
owner\_team: LEDO Industrial Integration  
source\_document: scada\_external\_system\_contract\_v1  
created\_at: 2026-06-26T00:00:00Z  
updated\_at: 2026-06-26T00:00:00Z  
deprecated\_since: null  
replacement\_external\_system\_id: null

---

## **13\. Registry Entry 예시: BIM / CDE Platform**

external\_system\_id: external\_system:bim\_cde\_project\_A  
canonical\_name: bim\_cde\_project\_A  
display\_name: BIM CDE Platform \- Project A  
description: Project A의 BIM model, drawing, issue, document, revision 정보를 관리하는 외부 CDE 시스템이다.  
semantic\_iri: ledo:BIMCDEPlatformProjectA

external\_system\_type: BIM\_CDE\_PLATFORM  
system\_category: CONSTRUCTION\_INFORMATION\_SYSTEM

version: 1.0.0  
status: active

site\_scope:  
  \- site\_A

zone\_scope:  
  \- "\*"

owner\_organization: project\_owner\_or\_general\_contractor  
operator\_team: bim\_management\_team  
vendor\_name: ExampleCDEVendor

supported\_protocols:  
  \- REST  
  \- GraphQL  
  \- Webhook

supported\_adapter\_refs:  
  \- adapter:bim\_cde\_adapter\_project\_A

supported\_action\_type\_refs:  
  \- action:REQUEST\_INSPECTION  
  \- action:NOTIFY\_MANAGER  
  \- action:UPDATE\_MODEL\_ISSUE  
  \- action:CREATE\_DOCUMENT\_RECORD

supported\_execution\_request\_types:  
  \- execution\_request:bim\_issue\_create\_request  
  \- execution\_request:document\_record\_create\_request  
  \- execution\_request:model\_query\_request

supported\_feedback\_event\_refs:  
  \- event:BIMIssueCreated  
  \- event:DocumentRecordCreated  
  \- event:ExternalSystemStatusUpdated

supported\_capability\_refs:  
  \- capability:model\_query  
  \- capability:issue\_creation  
  \- capability:document\_record\_write  
  \- capability:webhook\_event\_receive

integration\_mode: read\_write  
data\_direction: bidirectional  
control\_authority\_level: write\_data  
safety\_criticality: operational

connection\_contract\_ref: contract:bim\_cde\_project\_A\_connection\_v1

payload\_contract\_refs:  
  \- contract:bim\_issue\_create\_payload\_v1  
  \- contract:bim\_model\_query\_payload\_v1

feedback\_schema\_refs:  
  \- schema:bim\_issue\_created\_payload\_v1  
  \- schema:external\_system\_status\_updated\_payload\_v1

health\_check\_policy\_ref: health:bim\_cde\_health\_check\_v1  
heartbeat\_required: false  
availability\_requirement: medium

fallback\_policy\_ref: fallback:bim\_cde\_unavailable\_fallback\_v1  
fail\_safe\_policy\_ref: null

credential\_ref: credential:bim\_cde\_project\_A\_api  
secret\_storage\_ref: vault:bim\_cde\_project\_A

network\_zone: enterprise\_network  
security\_level: confidential  
pii\_classification: indirect

decision\_boundary: may\_provide\_model\_and\_document\_context\_for\_decision  
approval\_boundary: does\_not\_grant\_approval  
execution\_boundary: may\_write\_project\_records\_but\_not\_physical\_commands  
safety\_boundary: model\_information\_must\_not\_override\_runtime\_safety\_evidence

audit\_event\_refs:  
  \- audit:external\_system\_registered  
  \- audit:bim\_query\_performed  
  \- audit:bim\_issue\_created  
  \- audit:external\_system\_feedback\_received

owner\_module: knowledge\_integration\_module  
owner\_team: LEDO BIM Integration  
source\_document: bim\_cde\_external\_system\_contract\_v1  
created\_at: 2026-06-26T00:00:00Z  
updated\_at: 2026-06-26T00:00:00Z  
deprecated\_since: null  
replacement\_external\_system\_id: null

---

## **14\. Registry Entry 예시: Notification System**

external\_system\_id: external\_system:notification\_gateway\_site\_A  
canonical\_name: notification\_gateway\_site\_A  
display\_name: Notification Gateway \- Site A  
description: Site A의 작업자, 관리자, 안전 담당자에게 SMS, push, email, messenger 알림을 전달하는 외부 알림 시스템이다.  
semantic\_iri: ledo:NotificationGatewaySiteA

external\_system\_type: NOTIFICATION\_SYSTEM  
system\_category: COMMUNICATION\_SYSTEM

version: 1.0.0  
status: active

site\_scope:  
  \- site\_A

zone\_scope:  
  \- "\*"

owner\_organization: site\_operator  
operator\_team: communication\_operations\_team  
vendor\_name: ExampleNotificationVendor

supported\_protocols:  
  \- REST  
  \- Webhook

supported\_adapter\_refs:  
  \- adapter:notification\_adapter\_site\_A

supported\_action\_type\_refs:  
  \- action:NOTIFY\_MANAGER  
  \- action:NOTIFY\_WORKER  
  \- action:REQUEST\_ACKNOWLEDGEMENT  
  \- action:BROADCAST\_ALERT

supported\_execution\_request\_types:  
  \- execution\_request:notification\_send\_request  
  \- execution\_request:acknowledgement\_request

supported\_feedback\_event\_refs:  
  \- event:NotificationSent  
  \- event:NotificationFailed  
  \- event:OperatorAcknowledgementReceived

supported\_capability\_refs:  
  \- capability:send\_sms  
  \- capability:send\_push  
  \- capability:send\_email  
  \- capability:send\_messenger\_message  
  \- capability:receive\_acknowledgement

integration\_mode: request\_response  
data\_direction: bidirectional  
control\_authority\_level: request\_only  
safety\_criticality: operational

connection\_contract\_ref: contract:notification\_gateway\_site\_A\_connection\_v1

payload\_contract\_refs:  
  \- contract:notification\_send\_payload\_v1  
  \- contract:acknowledgement\_request\_payload\_v1

feedback\_schema\_refs:  
  \- schema:notification\_result\_payload\_v1  
  \- schema:operator\_acknowledgement\_payload\_v1

health\_check\_policy\_ref: health:notification\_gateway\_health\_check\_v1  
heartbeat\_required: false  
availability\_requirement: high

fallback\_policy\_ref: fallback:notification\_fallback\_v1  
fail\_safe\_policy\_ref: failsafe:notification\_fail\_safe\_v1

credential\_ref: credential:notification\_gateway\_site\_A\_api  
secret\_storage\_ref: vault:notification\_gateway\_site\_A

network\_zone: enterprise\_network  
security\_level: restricted  
pii\_classification: direct

decision\_boundary: may\_deliver\_decision\_or\_approval\_notifications\_only  
approval\_boundary: does\_not\_grant\_approval  
execution\_boundary: sends\_notification\_not\_physical\_command  
safety\_boundary: emergency\_notification\_must\_have\_fallback\_channel

audit\_event\_refs:  
  \- audit:external\_system\_registered  
  \- audit:notification\_requested  
  \- audit:notification\_sent  
  \- audit:notification\_failed

owner\_module: communication\_integration\_module  
owner\_team: LEDO Notification Integration  
source\_document: notification\_external\_system\_contract\_v1  
created\_at: 2026-06-26T00:00:00Z  
updated\_at: 2026-06-26T00:00:00Z  
deprecated\_since: null  
replacement\_external\_system\_id: null

---

## **15\. External System Lifecycle Alignment**

External System은 다음 lifecycle과 연결된다.

External System Registration  
        ↓  
Contract Validation  
        ↓  
Security / Credential Reference Validation  
        ↓  
Adapter Compatibility Validation  
        ↓  
Health Check  
        ↓  
Activation  
        ↓  
Runtime Request / Event / Feedback  
        ↓  
Monitoring / Audit / Versioning  
        ↓  
Maintenance / Degradation / Deprecation / Retirement

중요한 점은 External System이 등록되어 있다고 해서 모든 Action을 받을 수 있는 것은 아니라는 점이다.

External System이 active 상태여야 한다.  
해당 Action Type을 지원해야 한다.  
해당 Adapter와 호환되어야 한다.  
해당 Protocol이 허용되어야 한다.  
해당 Safety Boundary를 만족해야 한다.  
Health Check를 통과해야 한다.

---

## **16\. Validation Rules**

External System Entry는 다음 조건을 만족할 때만 유효하다.

1. `external_system_id`가 registry에 존재해야 한다.  
2. status가 `active` 또는 허용된 runtime 상태여야 한다.  
3. external system type이 선언되어야 한다.  
4. site scope 또는 zone scope가 선언되어야 한다.  
5. supported protocol이 선언되어야 한다.  
6. supported adapter reference가 선언되어야 한다.  
7. supported action type 또는 execution request type이 선언되어야 한다.  
8. connection contract가 선언되어야 한다.  
9. payload contract가 선언되어야 한다.  
10. feedback schema가 선언되어야 한다.  
11. control authority level이 선언되어야 한다.  
12. safety criticality가 선언되어야 한다.  
13. health check policy가 선언되어야 한다.  
14. credential reference가 선언되어야 한다.  
15. security level이 선언되어야 한다.  
16. decision / approval / execution / safety boundary가 선언되어야 한다.  
17. audit event reference가 선언되어야 한다.  
18. owner module이 선언되어야 한다.  
19. version이 유효해야 한다.  
20. deprecated 상태라면 migration metadata가 있어야 한다.

하나라도 누락되면 해당 External System은 operational lifecycle에 사용되면 안 된다.

---

## **17\. Execution Compatibility Validation**

ExecutionRequest가 External System으로 전달되기 전에는 다음 검증이 필요하다.

External System이 등록되어 있는가?  
External System이 active 상태인가?  
ExecutionRequest의 Action Type을 지원하는가?  
선택된 Adapter가 해당 External System에 허용되어 있는가?  
Protocol이 supported\_protocols에 포함되는가?  
ExecutionRequest Type이 지원되는가?  
Payload Contract가 일치하는가?  
Feedback Schema가 정의되어 있는가?  
Site / Zone Scope가 일치하는가?  
Control Authority Boundary를 위반하지 않는가?  
Safety Boundary를 위반하지 않는가?  
Health Check가 통과되었는가?

이 조건을 만족하지 못하면 ExecutionRequest는 ExternalControlRequest로 변환되면 안 된다.

---

## **18\. Health Check Rule**

External System은 runtime health 상태를 가져야 한다.

권장 health status:

unknown  
healthy  
degraded  
unavailable  
maintenance  
blocked

Health check는 다음을 확인할 수 있다.

network reachability  
authentication validity  
API response latency  
heartbeat freshness  
protocol-level connection status  
external system reported status  
adapter connection status  
last successful request time  
last feedback received time

Health가 degraded 또는 unavailable이면 다음 정책을 따른다.

low-risk request: retry 또는 fallback  
high-risk request: hold 또는 escalate  
safety-critical request: block 또는 fail-safe

---

## **19\. Fallback 및 Fail-Safe Rule**

External System이 unavailable한 경우 fallback 또는 fail-safe 정책이 필요하다.

Fallback 예시:

notification\_system unavailable  
    → secondary notification channel 사용

robot\_fleet\_manager unavailable  
    → dispatch 보류 및 supervisor에게 escalate

BIM CDE unavailable  
    → cached model context 사용, write operation 보류

SCADA unavailable  
    → control room manual verification 요청

Fail-safe 예시:

safety\_controller unreachable  
    → physical execution path block

robot fleet feedback lost  
    → mission status unknown으로 표시하고 supervisor review 요청

worker location source stale  
    → Safety Gate pass 금지

핵심 원칙:

External System failure must not silently degrade into unsafe execution.

---

## **20\. Data Direction Rule**

External System은 데이터 방향을 명확히 가져야 한다.

권장 값:

inbound  
outbound  
bidirectional

### **20.1 inbound**

LEDO가 외부 시스템으로부터 데이터를 받는다.

예시:

weather\_api  
iot\_platform  
scada\_status\_stream

---

### **20.2 outbound**

LEDO가 외부 시스템으로 데이터를 보낸다.

예시:

notification\_gateway  
audit\_export\_sink

---

### **20.3 bidirectional**

LEDO가 요청을 보내고 feedback을 받는다.

예시:

robot\_fleet\_manager  
site\_management\_platform  
inspection\_system

---

## **21\. Control Authority Rule**

External System의 control authority는 반드시 명확히 선언되어야 한다.

권장 값:

read\_only  
write\_data  
request\_only  
command\_capable  
safety\_rated\_control  
physical\_control\_authority

중요한 구분은 다음과 같다.

write\_data:  
    외부 시스템에 기록을 남길 수 있다.

request\_only:  
    외부 시스템에 업무 요청을 전달할 수 있다.

command\_capable:  
    외부 시스템이 자체적으로 실행 명령을 수행할 수 있다.

safety\_rated\_control:  
    safety-rated control logic을 가진다.

physical\_control\_authority:  
    물리 장비 제어 권한을 가진다.

LEDO는 External System의 authority를 알고 있어야 하며, 그 경계를 넘지 않아야 한다.

---

## **22\. Security 및 Credential Rule**

`external_system_registry`는 실제 secret 값을 저장하면 안 된다.

저장해야 하는 것은 reference이다.

credential\_ref: credential:robot\_fleet\_manager\_site\_A\_api  
secret\_storage\_ref: vault:robot\_fleet\_manager\_site\_A

실제 token, password, certificate, private key는 Vault 또는 Secret Manager에 있어야 한다.

보안 원칙:

No raw secrets in external\_system\_registry.  
mTLS or signed request should be used for safety-critical integrations.  
Credential rotation must be supported.  
Access to external systems must be auditable.

---

## **23\. Relationship to Adapter Registry**

`adapter_registry`와 `external_system_registry`는 강하게 연결된다.

adapter\_registry:  
    어떤 adapter instance가 어떤 request를 처리할 수 있는가?

external\_system\_registry:  
    그 adapter가 연결하려는 외부 시스템이 등록되어 있고,  
    해당 action/protocol/scope를 허용하는가?

흐름:

ExecutionRequest  
    ↓  
adapter\_registry selects compatible adapter  
    ↓  
external\_system\_registry validates target external system  
    ↓  
ExternalControlRequest  
    ↓  
Adapter sends request to External System

Adapter가 등록되어 있어도 External System이 등록되어 있지 않으면 실행 경로는 유효하지 않다.

---

## **24\. Relationship to Action Registry**

`action_registry`는 Action Type이 어떤 외부 실행 경로를 가질 수 있는지 선언한다.

`external_system_registry`는 실제 외부 시스템이 그 Action Type을 받을 수 있는지 정의한다.

action\_registry:  
    DISPATCH\_ROBOT은 external execution path를 가질 수 있다.

external\_system\_registry:  
    robot\_fleet\_manager\_site\_A는 DISPATCH\_ROBOT을 지원한다.

Action Type이 등록되어 있어도 External System이 해당 Action Type을 지원하지 않으면 실행 요청을 보낼 수 없다.

---

## **25\. Relationship to Approval Registry**

Approval이 있더라도 External System에 요청할 수 있는 것은 아니다.

approval\_registry:  
    누가 어떤 조건에서 Action을 승인할 수 있는가?

external\_system\_registry:  
    승인된 Action을 실제로 받을 수 있는 외부 시스템이 존재하는가?

Approval은 External System compatibility를 대체하지 않는다.

Approval pass ≠ External System compatibility pass

---

## **26\. Relationship to Safety Gate**

Safety Gate는 ExecutionRequest 이전에 최종 검증을 수행한다.

External System Registry는 Safety Gate가 확인해야 할 외부 시스템 관련 조건을 제공한다.

예시:

external system active 상태인가?  
health check가 통과되었는가?  
external system이 safety-critical인가?  
fail-safe policy가 존재하는가?  
feedback schema가 정의되어 있는가?  
safety boundary가 명확한가?

핵심 원칙:

Safety Gate must validate external system readiness before execution preparation.

---

## **27\. Relationship to Event Registry**

External System은 event producer 또는 event consumer가 될 수 있다.

예시:

RobotStatusUpdated  
ExecutionResultReceived  
SCADAStatusFeedbackReceived  
NotificationSent  
ExternalSystemStatusUpdated

`event_registry`는 event type과 schema를 정의한다.

`external_system_registry`는 어떤 외부 시스템이 해당 event를 produce 또는 consume할 수 있는지 정의한다.

---

## **28\. Relationship to Evidence Registry**

External System은 evidence source가 될 수 있다.

예시:

robot\_availability\_snapshot  
equipment\_status\_snapshot  
scada\_status\_feedback\_evidence  
execution\_result\_evidence  
external\_system\_reachable\_snapshot

`evidence_registry`는 evidence type과 quality rule을 정의한다.

`external_system_registry`는 해당 evidence가 어떤 외부 시스템에서 온 것인지, 그 source가 신뢰 가능한지 판단하는 기준을 제공한다.

---

## **29\. Relationship to Runtime Validation Registry**

Runtime Validation은 외부 시스템의 상태를 검증할 수 있다.

예시:

external\_system\_reachable  
adapter\_health\_valid  
robot\_fleet\_manager\_available  
scada\_connection\_valid  
safety\_controller\_reachable

`runtime_validation_registry`는 어떤 validation을 수행할지 정의한다.

`external_system_registry`는 validation 대상 외부 시스템과 health policy를 제공한다.

---

## **30\. Relationship to Ontology**

모든 중요한 External System은 semantic IRI를 가져야 한다.

예시:

external\_system\_id: external\_system:robot\_fleet\_manager\_site\_A  
semantic\_iri: ledo:RobotFleetManagerSiteA

Ontology에서는 다음과 같이 정의할 수 있다.

ledo:RobotFleetManagerSiteA  
    rdf:type ledo:ExternalSystem ;  
    rdfs:subClassOf ledo:RobotFleetManager ;  
    ledo:supportsAction ledo:DispatchRobotAction ;  
    ledo:usesProtocol ledo:REST ;  
    ledo:hasControlAuthority ledo:CommandCapable ;  
    ledo:hasSafetyBoundary ledo:RobotVendorSafetyBoundary .

Ontology는 External System의 의미론적 기반을 제공한다.

External System Registry는 이를 운영 시스템에서 version, status, protocol, adapter, health, credential, safety boundary, audit rule로 관리한다.

---

## **31\. Versioning 및 Migration**

External System Entry는 반드시 versioning되어야 한다.

다음 항목 중 하나라도 변경되면 version 변경이 필요하다.

1. external system type 변경  
2. supported protocol 변경  
3. supported adapter 변경  
4. supported Action Type 변경  
5. supported ExecutionRequest Type 변경  
6. payload contract 변경  
7. feedback schema 변경  
8. control authority level 변경  
9. safety criticality 변경  
10. credential reference 변경  
11. health check policy 변경  
12. fallback / fail-safe policy 변경  
13. decision / approval / execution / safety boundary 변경

Status 값:

draft  
active  
maintenance  
degraded  
deprecated  
retired  
blocked

Deprecated External System은 다음을 선언해야 한다.

deprecated\_since: datetime  
replacement\_external\_system\_id: string | null  
migration\_notes: string

Blocked External System은 새로운 ExecutionRequest target으로 사용되면 안 된다.

---

## **32\. Implementation Use**

`external_system_registry`는 다음을 생성하거나 검증하는 데 사용된다.

1. `ExternalSystemType` enum  
2. `ExternalSystemStatus` enum  
3. `IntegrationMode` enum  
4. External system metadata DTO  
5. External system compatibility validation  
6. Adapter-to-external-system compatibility validation  
7. ExecutionRequest external target validation  
8. Protocol compatibility validation  
9. Site / zone scope validation  
10. Control authority boundary validation  
11. Safety criticality validation  
12. Health check lookup  
13. Credential reference lookup  
14. Feedback schema lookup  
15. Fallback / fail-safe policy lookup  
16. Audit log expectation  
17. Test case generation  
18. Migration rules

Implementation은 등록되지 않은 External System으로 ExecutionRequest를 보낼 수 없어야 한다.

---

## **33\. 권장 Code Structure**

registries/  
    external\_system\_registry/  
        external\_system\_registry.py  
        external\_system\_entry.py  
        external\_system\_type.py  
        external\_system\_status.py  
        integration\_mode.py  
        control\_authority.py  
        safety\_criticality.py  
        external\_system\_validation.py  
        external\_system\_errors.py  
        external\_system\_loader.py  
        external\_system\_migration.py

    adapter\_registry/  
    action\_registry/  
    event\_registry/  
    evidence\_registry/  
    runtime\_validation\_registry/  
    schema\_registry/  
    audit\_event\_registry/

---

## **34\. Minimal Pydantic Model**

from enum import Enum  
from pydantic import BaseModel, Field  
from typing import Optional  
from datetime import datetime

class ExternalSystemStatus(str, Enum):  
    DRAFT \= "draft"  
    ACTIVE \= "active"  
    MAINTENANCE \= "maintenance"  
    DEGRADED \= "degraded"  
    DEPRECATED \= "deprecated"  
    RETIRED \= "retired"  
    BLOCKED \= "blocked"

class ExternalSystemType(str, Enum):  
    ROBOT\_FLEET\_MANAGER \= "robot\_fleet\_manager"  
    ROBOT\_MIDDLEWARE \= "robot\_middleware"  
    PLC\_SYSTEM \= "plc\_system"  
    SCADA\_SYSTEM \= "scada\_system"  
    SAFETY\_CONTROLLER \= "safety\_controller"  
    BIM\_CDE\_PLATFORM \= "bim\_cde\_platform"  
    SITE\_MANAGEMENT\_PLATFORM \= "site\_management\_platform"  
    NOTIFICATION\_SYSTEM \= "notification\_system"  
    INSPECTION\_SYSTEM \= "inspection\_system"  
    ERP\_SYSTEM \= "erp\_system"  
    CMMS\_SYSTEM \= "cmms\_system"  
    IOT\_PLATFORM \= "iot\_platform"  
    VISION\_SYSTEM \= "vision\_system"  
    WEATHER\_SERVICE \= "weather\_service"  
    GIS\_SYSTEM \= "gis\_system"  
    DOCUMENT\_MANAGEMENT\_SYSTEM \= "document\_management\_system"

class IntegrationMode(str, Enum):  
    READ\_ONLY \= "read\_only"  
    WRITE\_ONLY \= "write\_only"  
    READ\_WRITE \= "read\_write"  
    REQUEST\_RESPONSE \= "request\_response"  
    EVENT\_STREAM \= "event\_stream"  
    COMMAND\_GATEWAY \= "command\_gateway"

class DataDirection(str, Enum):  
    INBOUND \= "inbound"  
    OUTBOUND \= "outbound"  
    BIDIRECTIONAL \= "bidirectional"

class ControlAuthorityLevel(str, Enum):  
    READ\_ONLY \= "read\_only"  
    WRITE\_DATA \= "write\_data"  
    REQUEST\_ONLY \= "request\_only"  
    COMMAND\_CAPABLE \= "command\_capable"  
    SAFETY\_RATED\_CONTROL \= "safety\_rated\_control"  
    PHYSICAL\_CONTROL\_AUTHORITY \= "physical\_control\_authority"

class SafetyCriticality(str, Enum):  
    NON\_CRITICAL \= "non\_critical"  
    OPERATIONAL \= "operational"  
    SAFETY\_RELEVANT \= "safety\_relevant"  
    SAFETY\_CRITICAL \= "safety\_critical"  
    SAFETY\_RATED \= "safety\_rated"

class SecurityLevel(str, Enum):  
    INTERNAL \= "internal"  
    CONFIDENTIAL \= "confidential"  
    RESTRICTED \= "restricted"  
    SAFETY\_CRITICAL \= "safety\_critical"

class PIIClassification(str, Enum):  
    NONE \= "none"  
    INDIRECT \= "indirect"  
    DIRECT \= "direct"  
    SENSITIVE \= "sensitive"

class ExternalSystemRegistryEntry(BaseModel):  
    external\_system\_id: str  
    canonical\_name: str  
    display\_name: str  
    description: str  
    semantic\_iri: str

    external\_system\_type: ExternalSystemType  
    system\_category: str

    version: str  
    status: ExternalSystemStatus \= ExternalSystemStatus.DRAFT

    site\_scope: list\[str\] \= Field(default\_factory=list)  
    zone\_scope: list\[str\] \= Field(default\_factory=list)

    owner\_organization: str  
    operator\_team: str  
    vendor\_name: Optional\[str\] \= None

    supported\_protocols: list\[str\] \= Field(default\_factory=list)  
    supported\_adapter\_refs: list\[str\] \= Field(default\_factory=list)  
    supported\_action\_type\_refs: list\[str\] \= Field(default\_factory=list)  
    supported\_execution\_request\_types: list\[str\] \= Field(default\_factory=list)  
    supported\_feedback\_event\_refs: list\[str\] \= Field(default\_factory=list)  
    supported\_capability\_refs: list\[str\] \= Field(default\_factory=list)

    integration\_mode: IntegrationMode  
    data\_direction: DataDirection  
    control\_authority\_level: ControlAuthorityLevel  
    safety\_criticality: SafetyCriticality

    connection\_contract\_ref: str  
    payload\_contract\_refs: list\[str\] \= Field(default\_factory=list)  
    feedback\_schema\_refs: list\[str\] \= Field(default\_factory=list)

    health\_check\_policy\_ref: str  
    heartbeat\_required: bool \= False  
    availability\_requirement: str

    fallback\_policy\_ref: Optional\[str\] \= None  
    fail\_safe\_policy\_ref: Optional\[str\] \= None

    credential\_ref: str  
    secret\_storage\_ref: str

    network\_zone: str  
    security\_level: SecurityLevel  
    pii\_classification: PIIClassification \= PIIClassification.NONE

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
    replacement\_external\_system\_id: Optional\[str\] \= None

---

## **35\. Core Validation Function**

def validate\_external\_system\_for\_execution(  
    entry: ExternalSystemRegistryEntry,  
    action\_type\_ref: str,  
    execution\_request\_type: str,  
    adapter\_ref: str,  
    protocol: str,  
    site\_id: str,  
    zone\_id: str | None \= None,  
) \-\> None:  
    if entry.status \!= ExternalSystemStatus.ACTIVE:  
        raise InvalidExternalSystemError(  
            f"External System is not active: {entry.external\_system\_id}"  
        )

    if action\_type\_ref not in entry.supported\_action\_type\_refs:  
        raise ExternalSystemActionNotSupportedError(  
            f"Action Type '{action\_type\_ref}' is not supported by "  
            f"External System '{entry.external\_system\_id}'"  
        )

    if execution\_request\_type not in entry.supported\_execution\_request\_types:  
        raise ExternalSystemExecutionRequestNotSupportedError(  
            f"ExecutionRequest Type '{execution\_request\_type}' is not supported by "  
            f"External System '{entry.external\_system\_id}'"  
        )

    if adapter\_ref not in entry.supported\_adapter\_refs:  
        raise ExternalSystemAdapterNotAllowedError(  
            f"Adapter '{adapter\_ref}' is not allowed for "  
            f"External System '{entry.external\_system\_id}'"  
        )

    if protocol not in entry.supported\_protocols:  
        raise ExternalSystemProtocolNotSupportedError(  
            f"Protocol '{protocol}' is not supported by "  
            f"External System '{entry.external\_system\_id}'"  
        )

    if site\_id not in entry.site\_scope and "\*" not in entry.site\_scope:  
        raise ExternalSystemScopeViolationError(  
            f"Site '{site\_id}' is not within allowed site scope"  
        )

    if zone\_id is not None:  
        if zone\_id not in entry.zone\_scope and "\*" not in entry.zone\_scope:  
            raise ExternalSystemScopeViolationError(  
                f"Zone '{zone\_id}' is not within allowed zone scope"  
            )

    if not entry.connection\_contract\_ref:  
        raise InvalidExternalSystemError(  
            "connection\_contract\_ref must be declared"  
        )

    if not entry.payload\_contract\_refs:  
        raise InvalidExternalSystemError(  
            "payload\_contract\_refs must be declared"  
        )

    if not entry.feedback\_schema\_refs:  
        raise InvalidExternalSystemError(  
            "feedback\_schema\_refs must be declared"  
        )

    if not entry.health\_check\_policy\_ref:  
        raise InvalidExternalSystemError(  
            "health\_check\_policy\_ref must be declared"  
        )

    if not entry.credential\_ref or not entry.secret\_storage\_ref:  
        raise InvalidExternalSystemError(  
            "credential\_ref and secret\_storage\_ref must be declared"  
        )

    if not entry.execution\_boundary:  
        raise InvalidExternalSystemError(  
            "execution\_boundary must be declared"  
        )

    if not entry.safety\_boundary:  
        raise InvalidExternalSystemError(  
            "safety\_boundary must be declared"  
        )

---

## **36\. Test Scenarios**

필수 테스트는 다음과 같다.

1\. 등록되지 않은 External System 거부  
2\. inactive External System 거부  
3\. maintenance 상태 External System에 대한 high-risk request 거부  
4\. degraded 상태 External System에 대한 safety-critical request 거부  
5\. blocked External System 사용 거부  
6\. 지원하지 않는 Action Type 거부  
7\. 지원하지 않는 ExecutionRequest Type 거부  
8\. 허용되지 않은 Adapter 연결 거부  
9\. 지원하지 않는 Protocol 거부  
10\. site scope 불일치 거부  
11\. zone scope 불일치 거부  
12\. connection contract 누락 거부  
13\. payload contract 누락 거부  
14\. feedback schema 누락 거부  
15\. health check policy 누락 거부  
16\. credential reference 누락 거부  
17\. raw secret 저장 여부 검증  
18\. safety boundary 누락 거부  
19\. command-capable system에 대한 Safety Gate 검증 필수 확인  
20\. External System migration rule 검증

---

## **37\. Final Rule**

등록된 External System이 없으면,  
유효한 ExternalControlRequest도 없다.

External System이 active 상태가 아니면,  
ExecutionRequest를 전달할 수 없다.

External System이 해당 Action Type을 지원하지 않으면,  
ExecutionRequest를 전달할 수 없다.

External System이 해당 Adapter를 허용하지 않으면,  
연결할 수 없다.

External System이 해당 Protocol을 지원하지 않으면,  
요청을 보낼 수 없다.

External System의 Safety Boundary가 없으면,  
물리 실행 경로로 사용할 수 없다.

External System은 Adapter가 아니다.

External System은 Approval이 아니다.

External System은 Safety Gate가 아니다.

External System은 LEDO 내부 제어 로직이 아니다.

`external_system_registry`는 LEDO와 외부 물리·운영 시스템 사이의 신원, 권한, 연결, 안전 경계를 통제하는 핵심 결정론적 레지스트리이다.

이 모듈은 등록되지 않은 외부 시스템 연결을 방지하고, 외부 시스템별 protocol, adapter, capability, action support, feedback schema, health check, credential reference, safety boundary를 명확히 정의한다.

핵심 정의는 다음과 같다.

External System Registry  
\= 외부 시스템 이름 목록이 아니라,  
LEDO와 연결되는 모든 외부 시스템의 신원, 종류, 권한,  
protocol, adapter compatibility, capability, health,  
security, feedback, safety boundary를 통제하는  
외부 시스템 운영 계약 레지스트리

