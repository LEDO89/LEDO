**state\_registry Design Report**

## **1\. Overview**

`state_registry` is a core registry in the LEDO Ontology-Centric Cyber-Physical System. It defines and governs all State Types, State Keys, State Owners, State Sources, State Update Rules, State Transition Rules, Freshness Rules, Conflict Rules, Cache Rules, and Runtime Usage Boundaries used across the system.

The purpose of this module is to ensure that LEDO does not store or interpret real-time site state arbitrarily. It deterministically controls which states are recognized as official World State, which events may update those states, which services own those states, and which Decisions, Policies, and Safety Gates may reference those states.

`state_registry` is not a simple list of state variables.

It is an **operational contract registry for real-time state meaning, ownership, updates, storage, freshness, conflict handling, and usage boundaries** that defines the following:

Which State Types may exist?

Which entity’s current state does this State represent?

Which Events may update this State?

Which External System or Sensor provides this State?

Which service owns this State?

What is the freshness requirement for this State?

What should happen if this State becomes stale?

What should happen if this State becomes conflicting?

Can this State be used for Decision?

Can this State be used by the Safety Gate?

Can this State be frozen into a Snapshot?

Where is this State materialized: Redis, TimescaleDB, KG, or in-memory cache?

In other words, `state_registry` is the core registry that controls **“what is recognized as current state”** inside LEDO.

---

## **2\. Core Principle**

State represents current truth.

State is not an Event.

State is not a Snapshot.

State is not Evidence.

State is not Decision.

State is not Approval.

State is not an ExecutionRequest.

State is not a Physical Command.

The basic meaning of State is:

Event records what happened.

State represents what is currently true as a result.

Snapshot freezes that State at a specific point in time.

Evidence uses Snapshot or State as a basis for judgment.

Decision evaluates Evidence and State.

Safety Gate validates the latest State or Snapshot immediately before execution.

The core principle is:

Event records what happened.

State represents what is currently true.

Snapshot freezes State at a specific time.

Evidence uses State or Snapshot as judgment basis.

Policy evaluates whether the action is allowed.

Safety Gate validates fresh runtime State before execution.

The especially important LEDO principles are:

Current State must be explicitly registered.

Unregistered State must not be used for Decision or Safety Gate.

Stale State must not silently become valid State.

Conflicting State must not be ignored in safety-critical paths.

---

## **3\. Position in the LEDO Architecture**

`state_registry` is a core registry of the Real-Time World State Layer.

Event Stream / Sensor / External System

        ↓

Event Registry Validation

        ↓

State Update Rule Lookup

        ↓

state\_registry validation

        ↓

World State Store / Cache / Materialized View

        ↓

Snapshot Builder / Evidence / Decision / Policy / Safety Gate

In the full lifecycle, it is positioned as follows:

Event

    ↓

State Update

    ↓

Current State Materialization

    ↓

Snapshot Creation

    ↓

Evidence Binding

    ↓

DecisionCase

    ↓

ApprovalRequest

    ↓

Safety Gate Runtime State Check

    ↓

ExecutionRequest

`state_registry` is the critical bridge between Event and Snapshot.

event\_registry

    → What happened?

state\_registry

    → What is currently true as a result?

snapshot\_schema\_registry

    → How should that current state be frozen into a fixed structure?

---

## **4\. Purpose**

The purpose of `state_registry` is to ensure the following:

1. Prevent the use of unregistered States  
2. Define State Types  
3. Define State Keys  
4. Define State Owner Services  
5. Define State Sources  
6. Define State Update Events  
7. Define State Update Rules  
8. Define State Transition Rules  
9. Define State Freshness Requirements  
10. Define Stale State handling rules  
11. Define State Conflict handling rules  
12. Define State Storage / Cache locations  
13. Define whether State can be converted into Snapshot  
14. Define whether State can be used by Decision / Policy / Safety Gate  
15. Define State sensitivity and PII classification  
16. Manage State versioning and migration  
17. Manage State audit and replay capability  
18. Preserve the boundary between World State, Ontology, Knowledge Graph, and Snapshot

---

## **5\. Core Distinctions**

### **5.1 State**

`State` is a value recognized as currently true for a specific entity or system.

Examples:

worker\_location\_state

worker\_zone\_membership\_state

robot\_status\_state

robot\_mission\_state

zone\_status\_state

hazard\_state

equipment\_status\_state

external\_system\_health\_state

adapter\_health\_state

environment\_state

State is updated over time.

State is mutable over time.

Snapshot is immutable after creation.

---

### **5.2 State Type**

`State Type` defines what kind of current state it represents.

Recommended State Types:

WORKER\_LOCATION\_STATE

WORKER\_ZONE\_MEMBERSHIP\_STATE

WORKER\_PROXIMITY\_STATE

ZONE\_STATUS\_STATE

HAZARD\_STATE

ROBOT\_STATUS\_STATE

ROBOT\_MISSION\_STATE

ROBOT\_AVAILABILITY\_STATE

EQUIPMENT\_STATUS\_STATE

EXTERNAL\_SYSTEM\_HEALTH\_STATE

ADAPTER\_HEALTH\_STATE

ENVIRONMENT\_STATE

POLICY\_EVALUATION\_STATE

APPROVAL\_CONTEXT\_STATE

EXECUTION\_LIFECYCLE\_STATE

---

### **5.3 State Key**

`State Key` is the key structure used to retrieve a specific state instance.

Examples:

worker\_location\_state:{site\_id}:{worker\_id}

zone\_status\_state:{site\_id}:{zone\_id}

robot\_status\_state:{site\_id}:{robot\_id}

external\_system\_health\_state:{site\_id}:{external\_system\_id}

adapter\_health\_state:{site\_id}:{adapter\_id}

State Key must be deterministic.

Same entity \+ same state type must resolve to the same current state key.

---

### **5.4 State Owner**

`State Owner` is the service or module officially responsible for updating and managing that State.

Examples:

worker\_location\_state

    owner: world\_state\_service

robot\_status\_state

    owner: robot\_runtime\_state\_service

external\_system\_health\_state

    owner: execution\_integration\_service

adapter\_health\_state

    owner: adapter\_registry\_service

Core principle:

No owner,

no trusted state.

---

### **5.5 State Source**

`State Source` is the origin of state updates.

Examples:

UWB tracking gateway

vision location system

robot fleet manager

SCADA system

PLC gateway

weather service

manual operator input

safety inspection app

State Source must be connected to `external_system_registry`, `identity_registry`, and `event_registry`.

---

### **5.6 State Update Rule**

`State Update Rule` defines which event or input updates which State and how.

Examples:

WorkerLocationUpdated

    → updates worker\_location\_state

RobotStatusUpdated

    → updates robot\_status\_state

ExternalSystemStatusUpdated

    → updates external\_system\_health\_state

ZoneStatusChanged

    → updates zone\_status\_state

An Event occurring does not automatically update State.

Event must be valid.

Event producer must be trusted.

State update rule must exist.

State owner must accept the update.

---

### **5.7 State Transition Rule**

`State Transition Rule` defines the valid order in which State values may change.

Example:

robot\_mission\_state:

    idle → assigned → en\_route → executing → completed

    executing → paused

    executing → failed

    paused → resumed

    failed → recovery\_required

Invalid transitions must be rejected.

completed → executing

    invalid transition

failed → completed

    invalid unless recovery rule exists

---

### **5.8 Difference Between State and Snapshot**

They are different.

state\_registry:

    Defines the meaning, owner, update rule, freshness, and storage of current State items.

snapshot\_schema\_registry:

    Defines how a state bundle is frozen into a fixed structure at a specific point in time.

Example:

worker\_location\_state

    → continuously updated current state

worker\_location\_snapshot

    → immutable object that freezes worker\_location\_state at a specific point in time

---

## **6\. Scope**

`state_registry` controls the following fields:

state\_id: string

canonical\_name: string

display\_name: string

description: string

semantic\_iri: string

state\_type: string

state\_category: string

version: string

status: draft | active | deprecated | migration\_required | retired | blocked

entity\_type\_refs:

  \- string

state\_key\_pattern: string

owner\_service\_ref: string

owner\_module: string

source\_event\_type\_refs:

  \- string

source\_external\_system\_refs:

  \- string

source\_sensor\_refs:

  \- string

source\_agent\_type\_refs:

  \- string

allowed\_update\_producer\_refs:

  \- string

state\_value\_schema\_ref: string

state\_metadata\_schema\_ref: string

required\_fields:

  \- string

optional\_fields:

  \- string

update\_rule\_refs:

  \- string

transition\_rule\_refs:

  \- string

freshness\_requirement:

  max\_age\_seconds: integer

  freshness\_policy\_ref: string

stale\_policy\_ref: string

conflict\_policy\_ref: string

storage\_backend\_refs:

  \- redis

  \- timescaledb

  \- influxdb

  \- graphdb

  \- postgresql

  \- in\_memory\_cache

primary\_storage\_ref: string

cache\_policy\_ref: string | null

materialization\_policy\_ref: string

snapshot\_schema\_refs:

  \- string

runtime\_usable: boolean

decision\_usable: boolean

approval\_context\_usable: boolean

safety\_gate\_usable: boolean

hot\_path\_allowed: boolean

retention\_policy\_ref: string

replay\_policy\_ref: string | null

sensitivity\_level: public | internal | confidential | restricted | safety\_critical

pii\_classification: none | indirect | direct | sensitive

decision\_boundary: string

approval\_boundary: string

execution\_boundary: string

safety\_boundary: string

audit\_required: boolean

audit\_event\_refs:

  \- string

owner\_team: string

source\_document: string

created\_at: datetime

updated\_at: datetime

deprecated\_since: datetime | null

replacement\_state\_id: string | null

---

## **7\. Non-Scope**

`state_registry` does not directly define the following:

1. All Event payload schemas  
2. All Snapshot payload schemas  
3. All Evidence payload schemas  
4. Complete Redis key-value operation design  
5. Complete TimescaleDB table partition implementation  
6. Actual Sensor driver logic  
7. Internal state of the Robot Fleet Manager  
8. Actual PLC / SCADA control logic  
9. Complete Policy pass/fail logic  
10. Approval authority  
11. Complete Safety Gate final judgment logic  
12. Physical Command  
13. Robot motion planning  
14. External System protocol transformation  
15. Complete UI visualization logic

These responsibilities belong to the following modules or systems:

event\_registry

snapshot\_schema\_registry

evidence\_registry

world\_state\_store

runtime\_validation\_registry

policy\_registry

approval\_registry

safety\_gate

adapter\_registry

external\_system\_registry

robot\_fleet\_manager

PLC / SCADA

experience\_layer

`state_registry` defines the operational contract of State.

Actual state storage and updates are performed by the World State Service and each owner service.

---

## **8\. State Category Model**

Recommended State Categories are:

WORLD\_STATE

ENTITY\_STATE

WORKER\_STATE

ZONE\_STATE

ROBOT\_STATE

EQUIPMENT\_STATE

HAZARD\_STATE

EXTERNAL\_SYSTEM\_STATE

ADAPTER\_STATE

ENVIRONMENT\_STATE

RUNTIME\_VALIDATION\_STATE

EXECUTION\_LIFECYCLE\_STATE

AUDIT\_REPLAY\_STATE

### **8.1 WORKER\_STATE**

Represents worker location, zone membership, proximity, and on-site status.

Examples:

worker\_location\_state

worker\_zone\_membership\_state

worker\_proximity\_state

worker\_on\_site\_state

---

### **8.2 ZONE\_STATE**

Represents zone hazard status, accessibility, and lock status.

Examples:

zone\_status\_state

hazard\_zone\_state

locked\_zone\_state

restricted\_access\_zone\_state

---

### **8.3 ROBOT\_STATE**

Represents robot availability, mission, battery, and fault state.

Examples:

robot\_status\_state

robot\_availability\_state

robot\_mission\_state

robot\_battery\_state

robot\_fault\_state

---

### **8.4 EQUIPMENT\_STATE**

Represents equipment operational state, lockout, maintenance, and fault state.

Examples:

equipment\_status\_state

crane\_operation\_state

excavator\_availability\_state

equipment\_lockout\_state

---

### **8.5 EXTERNAL\_SYSTEM\_STATE**

Represents external system health, reachability, and heartbeat state.

Examples:

robot\_fleet\_manager\_health\_state

scada\_connection\_state

notification\_gateway\_health\_state

bim\_cde\_sync\_state

---

### **8.6 ADAPTER\_STATE**

Represents LEDO adapter health, connection, and protocol status.

Examples:

robot\_fleet\_adapter\_health\_state

scada\_adapter\_health\_state

notification\_adapter\_health\_state

---

### **8.7 EXECUTION\_LIFECYCLE\_STATE**

Represents the lifecycle state of ExecutionRequest, ExecutionCommand, and ExecutionResult.

Examples:

execution\_request\_state

execution\_command\_state

external\_control\_request\_state

execution\_result\_state

---

## **9\. Registry Entry Schema**

Each State Registry entry follows this structure:

state\_id: string

canonical\_name: string

display\_name: string

description: string

semantic\_iri: string

state\_type: string

state\_category: string

version: string

status: draft | active | deprecated | migration\_required | retired | blocked

entity\_type\_refs:

  \- string

state\_key\_pattern: string

owner\_service\_ref: string

owner\_module: string

source\_event\_type\_refs:

  \- string

source\_external\_system\_refs:

  \- string

source\_sensor\_refs:

  \- string

source\_agent\_type\_refs:

  \- string

allowed\_update\_producer\_refs:

  \- string

state\_value\_schema\_ref: string

state\_metadata\_schema\_ref: string

required\_fields:

  \- string

optional\_fields:

  \- string

update\_rule\_refs:

  \- string

transition\_rule\_refs:

  \- string

freshness\_requirement:

  max\_age\_seconds: integer

  freshness\_policy\_ref: string

stale\_policy\_ref: string

conflict\_policy\_ref: string

storage\_backend\_refs:

  \- string

primary\_storage\_ref: string

cache\_policy\_ref: string | null

materialization\_policy\_ref: string

snapshot\_schema\_refs:

  \- string

runtime\_usable: boolean

decision\_usable: boolean

approval\_context\_usable: boolean

safety\_gate\_usable: boolean

hot\_path\_allowed: boolean

retention\_policy\_ref: string

replay\_policy\_ref: string | null

sensitivity\_level: string

pii\_classification: string

decision\_boundary: string

approval\_boundary: string

execution\_boundary: string

safety\_boundary: string

audit\_required: boolean

audit\_event\_refs:

  \- string

owner\_team: string

source\_document: string

created\_at: datetime

updated\_at: datetime

deprecated\_since: datetime | null

replacement\_state\_id: string | null

---

## **10\. Registry Entry Example: Worker Location State**

state\_id: state:worker\_location\_state\_v1

canonical\_name: worker\_location\_state\_v1

display\_name: Worker Location State

description: A runtime state that represents the worker’s current location, zone membership, confidence, and source timestamp.

semantic\_iri: ledo:WorkerLocationState

state\_type: WORKER\_LOCATION\_STATE

state\_category: WORKER\_STATE

version: 1.0.0

status: draft

entity\_type\_refs:

  \- class:Worker

  \- class:WorkZone

  \- class:Location

state\_key\_pattern: worker\_location\_state:{site\_id}:{worker\_id}

owner\_service\_ref: service:world\_state\_service

owner\_module: real\_time\_world\_state\_module

source\_event\_type\_refs:

  \- event:WorkerLocationUpdated

  \- event:WorkerEnteredZone

  \- event:WorkerExitedZone

source\_external\_system\_refs:

  \- external\_system:worker\_tracking\_gateway\_site\_A

  \- external\_system:vision\_location\_system\_site\_A

source\_sensor\_refs:

  \- sensor:uwb\_tag

  \- sensor:camera\_zone

source\_agent\_type\_refs:

  \- agent\_type:WORKER\_MONITORING\_AGENT

allowed\_update\_producer\_refs:

  \- service:worker\_tracking\_gateway

  \- service:vision\_location\_service

  \- service:world\_state\_service

state\_value\_schema\_ref: schema:worker\_location\_state\_value\_v1

state\_metadata\_schema\_ref: schema:state\_metadata\_v1

required\_fields:

  \- worker\_id

  \- site\_id

  \- zone\_id

  \- observed\_at

  \- location\_confidence

  \- source\_system\_ref

optional\_fields:

  \- x

  \- y

  \- z

  \- floor\_id

  \- coordinate\_system\_ref

  \- tracking\_method

update\_rule\_refs:

  \- update\_rule:worker\_location\_event\_update\_v1

  \- update\_rule:worker\_zone\_membership\_update\_v1

transition\_rule\_refs:

  \- transition\_rule:worker\_zone\_transition\_v1

freshness\_requirement:

  max\_age\_seconds: 10

  freshness\_policy\_ref: policy:worker\_location\_state\_freshness\_v1

stale\_policy\_ref: stale:worker\_location\_state\_stale\_policy\_v1

conflict\_policy\_ref: conflict:worker\_location\_state\_conflict\_policy\_v1

storage\_backend\_refs:

  \- redis

  \- timescaledb

  \- graphdb

primary\_storage\_ref: redis:world\_state\_cache

cache\_policy\_ref: cache:worker\_location\_state\_cache\_v1

materialization\_policy\_ref: materialization:worker\_location\_state\_materialization\_v1

snapshot\_schema\_refs:

  \- snapshot\_schema:worker\_location\_snapshot\_v1

runtime\_usable: true

decision\_usable: true

approval\_context\_usable: true

safety\_gate\_usable: true

hot\_path\_allowed: true

retention\_policy\_ref: retention:worker\_location\_state\_retention\_v1

replay\_policy\_ref: replay:worker\_location\_state\_replay\_v1

sensitivity\_level: restricted

pii\_classification: direct

decision\_boundary: may\_support\_decision\_case\_but\_not\_decide

approval\_boundary: may\_support\_approval\_context\_but\_not\_approve

execution\_boundary: must\_not\_create\_execution\_request

safety\_boundary: stale\_or\_conflicting\_worker\_location\_state\_must\_block\_safety\_gate

audit\_required: true

audit\_event\_refs:

  \- audit:state\_updated

  \- audit:state\_validated

  \- audit:state\_stale\_detected

  \- audit:state\_conflict\_detected

  \- audit:state\_used\_by\_safety\_gate

owner\_team: LEDO Runtime State

source\_document: worker\_location\_state\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_state\_id: null

---

## **11\. Registry Entry Example: Robot Status State**

state\_id: state:robot\_status\_state\_v1

canonical\_name: robot\_status\_state\_v1

display\_name: Robot Status State

description: A runtime state that represents the robot’s current availability, mission state, battery, fault, and fleet manager connection status.

semantic\_iri: ledo:RobotStatusState

state\_type: ROBOT\_STATUS\_STATE

state\_category: ROBOT\_STATE

version: 1.0.0

status: draft

entity\_type\_refs:

  \- class:Robot

  \- class:RobotFleet

  \- class:RobotMission

  \- class:ExternalSystem

state\_key\_pattern: robot\_status\_state:{site\_id}:{robot\_id}

owner\_service\_ref: service:robot\_runtime\_state\_service

owner\_module: robot\_runtime\_state\_module

source\_event\_type\_refs:

  \- event:RobotStatusUpdated

  \- event:RobotMissionStateChanged

  \- event:RobotFaultDetected

  \- event:ExternalSystemStatusUpdated

source\_external\_system\_refs:

  \- external\_system:robot\_fleet\_manager\_site\_A

source\_sensor\_refs:

  \- sensor:robot\_telemetry

source\_agent\_type\_refs:

  \- agent\_type:ROBOT\_DISPATCH\_AGENT

allowed\_update\_producer\_refs:

  \- service:robot\_fleet\_gateway

  \- service:robot\_runtime\_state\_service

  \- service:execution\_feedback\_service

state\_value\_schema\_ref: schema:robot\_status\_state\_value\_v1

state\_metadata\_schema\_ref: schema:state\_metadata\_v1

required\_fields:

  \- robot\_id

  \- site\_id

  \- observed\_at

  \- availability\_status

  \- mission\_state

  \- battery\_level

  \- fault\_status

  \- fleet\_manager\_health

optional\_fields:

  \- current\_zone\_id

  \- current\_task\_id

  \- estimated\_available\_at

  \- maintenance\_status

update\_rule\_refs:

  \- update\_rule:robot\_status\_update\_v1

  \- update\_rule:robot\_mission\_state\_update\_v1

  \- update\_rule:robot\_fault\_update\_v1

transition\_rule\_refs:

  \- transition\_rule:robot\_mission\_lifecycle\_v1

  \- transition\_rule:robot\_availability\_transition\_v1

freshness\_requirement:

  max\_age\_seconds: 15

  freshness\_policy\_ref: policy:robot\_status\_state\_freshness\_v1

stale\_policy\_ref: stale:robot\_status\_state\_stale\_policy\_v1

conflict\_policy\_ref: conflict:robot\_status\_state\_conflict\_policy\_v1

storage\_backend\_refs:

  \- redis

  \- timescaledb

  \- postgresql

primary\_storage\_ref: redis:robot\_state\_cache

cache\_policy\_ref: cache:robot\_status\_state\_cache\_v1

materialization\_policy\_ref: materialization:robot\_status\_state\_materialization\_v1

snapshot\_schema\_refs:

  \- snapshot\_schema:robot\_availability\_snapshot\_v1

runtime\_usable: true

decision\_usable: true

approval\_context\_usable: true

safety\_gate\_usable: true

hot\_path\_allowed: true

retention\_policy\_ref: retention:robot\_status\_state\_retention\_v1

replay\_policy\_ref: replay:robot\_status\_state\_replay\_v1

sensitivity\_level: restricted

pii\_classification: none

decision\_boundary: may\_support\_robot\_dispatch\_decision\_but\_not\_decide

approval\_boundary: may\_support\_robot\_dispatch\_approval\_context\_but\_not\_approve

execution\_boundary: must\_not\_dispatch\_robot\_directly

safety\_boundary: stale\_or\_faulted\_robot\_state\_must\_block\_dispatch

audit\_required: true

audit\_event\_refs:

  \- audit:state\_updated

  \- audit:robot\_state\_validated

  \- audit:robot\_state\_stale\_detected

  \- audit:robot\_state\_used\_by\_safety\_gate

owner\_team: LEDO Robotics Runtime

source\_document: robot\_status\_state\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_state\_id: null

---

## **12\. Registry Entry Example: Zone Status State**

state\_id: state:zone\_status\_state\_v1

canonical\_name: zone\_status\_state\_v1

display\_name: Zone Status State

description: A runtime state that represents the current accessibility, hazard state, lock state, and active operation state of a Zone.

semantic\_iri: ledo:ZoneStatusState

state\_type: ZONE\_STATUS\_STATE

state\_category: ZONE\_STATE

version: 1.0.0

status: draft

entity\_type\_refs:

  \- class:WorkZone

  \- class:HazardZone

  \- class:SpatialRegion

  \- class:Operation

state\_key\_pattern: zone\_status\_state:{site\_id}:{zone\_id}

owner\_service\_ref: service:world\_state\_service

owner\_module: real\_time\_world\_state\_module

source\_event\_type\_refs:

  \- event:ZoneStatusChanged

  \- event:HazardDetected

  \- event:ZoneLocked

  \- event:ZoneUnlocked

  \- event:WorkOperationStarted

  \- event:WorkOperationCompleted

source\_external\_system\_refs:

  \- external\_system:site\_management\_platform\_site\_A

  \- external\_system:safety\_controller\_zone\_03

source\_sensor\_refs:

  \- sensor:camera\_zone

  \- sensor:gas\_sensor

  \- sensor:access\_control\_sensor

source\_agent\_type\_refs:

  \- agent\_type:ZONE\_MONITORING\_AGENT

  \- agent\_type:SAFETY\_RISK\_AGENT

allowed\_update\_producer\_refs:

  \- service:zone\_monitoring\_service

  \- service:safety\_event\_service

  \- service:world\_state\_service

state\_value\_schema\_ref: schema:zone\_status\_state\_value\_v1

state\_metadata\_schema\_ref: schema:state\_metadata\_v1

required\_fields:

  \- zone\_id

  \- site\_id

  \- observed\_at

  \- zone\_status

  \- access\_status

  \- hazard\_status

  \- lock\_status

optional\_fields:

  \- active\_operation\_id

  \- restriction\_reason

  \- hazard\_type

  \- locked\_by\_identity\_id

  \- unlock\_allowed\_at

update\_rule\_refs:

  \- update\_rule:zone\_status\_update\_v1

  \- update\_rule:hazard\_zone\_update\_v1

  \- update\_rule:zone\_lock\_update\_v1

transition\_rule\_refs:

  \- transition\_rule:zone\_access\_transition\_v1

  \- transition\_rule:zone\_lock\_transition\_v1

freshness\_requirement:

  max\_age\_seconds: 20

  freshness\_policy\_ref: policy:zone\_status\_state\_freshness\_v1

stale\_policy\_ref: stale:zone\_status\_state\_stale\_policy\_v1

conflict\_policy\_ref: conflict:zone\_status\_state\_conflict\_policy\_v1

storage\_backend\_refs:

  \- redis

  \- graphdb

  \- postgresql

primary\_storage\_ref: redis:zone\_state\_cache

cache\_policy\_ref: cache:zone\_status\_state\_cache\_v1

materialization\_policy\_ref: materialization:zone\_status\_state\_materialization\_v1

snapshot\_schema\_refs:

  \- snapshot\_schema:zone\_status\_snapshot\_v1

runtime\_usable: true

decision\_usable: true

approval\_context\_usable: true

safety\_gate\_usable: true

hot\_path\_allowed: true

retention\_policy\_ref: retention:zone\_status\_state\_retention\_v1

replay\_policy\_ref: replay:zone\_status\_state\_replay\_v1

sensitivity\_level: restricted

pii\_classification: none

decision\_boundary: may\_support\_zone\_decision\_but\_not\_decide

approval\_boundary: may\_support\_approval\_context\_but\_not\_approve

execution\_boundary: must\_not\_lock\_or\_unlock\_zone\_directly

safety\_boundary: stale\_or\_conflicting\_zone\_state\_must\_block\_execution\_path

audit\_required: true

audit\_event\_refs:

  \- audit:state\_updated

  \- audit:zone\_state\_validated

  \- audit:zone\_state\_stale\_detected

  \- audit:zone\_state\_conflict\_detected

  \- audit:zone\_state\_used\_by\_safety\_gate

owner\_team: LEDO Runtime State

source\_document: zone\_status\_state\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_state\_id: null

---

## **13\. Registry Entry Example: External System Health State**

state\_id: state:external\_system\_health\_state\_v1

canonical\_name: external\_system\_health\_state\_v1

display\_name: External System Health State

description: A runtime state that represents the current health, reachability, heartbeat, and degraded status of an external system.

semantic\_iri: ledo:ExternalSystemHealthState

state\_type: EXTERNAL\_SYSTEM\_HEALTH\_STATE

state\_category: EXTERNAL\_SYSTEM\_STATE

version: 1.0.0

status: draft

entity\_type\_refs:

  \- class:ExternalSystem

  \- class:IntegrationEndpoint

state\_key\_pattern: external\_system\_health\_state:{site\_id}:{external\_system\_id}

owner\_service\_ref: service:execution\_integration\_service

owner\_module: execution\_integration\_module

source\_event\_type\_refs:

  \- event:ExternalSystemStatusUpdated

  \- event:ExternalSystemHeartbeatReceived

  \- event:ExternalSystemConnectionFailed

source\_external\_system\_refs:

  \- external\_system:robot\_fleet\_manager\_site\_A

  \- external\_system:scada\_system\_site\_A

  \- external\_system:notification\_gateway\_site\_A

source\_sensor\_refs: \[\]

source\_agent\_type\_refs:

  \- agent\_type:SUPERVISOR\_AGENT

allowed\_update\_producer\_refs:

  \- service:external\_system\_monitor

  \- service:adapter\_health\_monitor

  \- service:execution\_integration\_service

state\_value\_schema\_ref: schema:external\_system\_health\_state\_value\_v1

state\_metadata\_schema\_ref: schema:state\_metadata\_v1

required\_fields:

  \- external\_system\_id

  \- site\_id

  \- observed\_at

  \- health\_status

  \- reachable

  \- last\_heartbeat\_at

  \- last\_successful\_request\_at

optional\_fields:

  \- response\_latency\_ms

  \- error\_code

  \- degraded\_reason

  \- maintenance\_window\_ref

update\_rule\_refs:

  \- update\_rule:external\_system\_health\_update\_v1

  \- update\_rule:external\_system\_heartbeat\_update\_v1

transition\_rule\_refs:

  \- transition\_rule:external\_system\_health\_transition\_v1

freshness\_requirement:

  max\_age\_seconds: 20

  freshness\_policy\_ref: policy:external\_system\_health\_state\_freshness\_v1

stale\_policy\_ref: stale:external\_system\_health\_state\_stale\_policy\_v1

conflict\_policy\_ref: conflict:external\_system\_health\_state\_conflict\_policy\_v1

storage\_backend\_refs:

  \- redis

  \- postgresql

  \- timescaledb

primary\_storage\_ref: redis:external\_system\_state\_cache

cache\_policy\_ref: cache:external\_system\_health\_state\_cache\_v1

materialization\_policy\_ref: materialization:external\_system\_health\_state\_materialization\_v1

snapshot\_schema\_refs:

  \- snapshot\_schema:external\_system\_health\_snapshot\_v1

runtime\_usable: true

decision\_usable: true

approval\_context\_usable: false

safety\_gate\_usable: true

hot\_path\_allowed: true

retention\_policy\_ref: retention:external\_system\_health\_state\_retention\_v1

replay\_policy\_ref: replay:external\_system\_health\_state\_replay\_v1

sensitivity\_level: restricted

pii\_classification: none

decision\_boundary: may\_support\_execution\_readiness\_decision\_but\_not\_decide

approval\_boundary: does\_not\_grant\_approval

execution\_boundary: must\_not\_create\_external\_control\_request

safety\_boundary: unreachable\_external\_system\_state\_must\_block\_execution\_path

audit\_required: true

audit\_event\_refs:

  \- audit:state\_updated

  \- audit:external\_system\_state\_validated

  \- audit:external\_system\_state\_stale\_detected

  \- audit:external\_system\_state\_used\_by\_safety\_gate

owner\_team: LEDO External Integration

source\_document: external\_system\_health\_state\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_state\_id: null

---

## **14\. State Lifecycle Alignment**

State is connected to the following lifecycle:

Source Event Received

        ↓

Event Validation

        ↓

State Update Rule Lookup

        ↓

State Registry Validation

        ↓

State Owner Service Accepts Update

        ↓

State Value Schema Validation

        ↓

State Transition Validation

        ↓

Conflict / Freshness Check

        ↓

Current State Materialized

        ↓

Cache / Store / KG Projection

        ↓

Snapshot Builder / Evidence / Decision / Safety Gate Usage

        ↓

Audit / Replay / Retention / Migration

The important point is that State may be updated, but it must not be changed arbitrarily.

State is mutable through controlled update rules.

Snapshot is immutable after creation.

---

## **15\. Validation Rules**

A State Registry Entry is valid only when the following conditions are satisfied:

1. `state_id` exists in the registry.  
2. Its status is `active`.  
3. State type is declared.  
4. State category is declared.  
5. Entity type references are declared.  
6. State key pattern is declared.  
7. Owner service is declared.  
8. Source event or source external system is declared.  
9. Allowed update producers are declared.  
10. State value schema is declared.  
11. State metadata schema is declared.  
12. Required fields are declared.  
13. Update rules are declared.  
14. Freshness requirement is declared.  
15. Stale policy is declared.  
16. Conflict policy is declared.  
17. Primary storage is declared.  
18. Materialization policy is declared.  
19. Snapshot schema reference is declared when required.  
20. Runtime / Decision / Safety Gate usability is declared.  
21. Sensitivity / PII classification is declared.  
22. Decision / approval / execution / safety boundaries are declared.  
23. Audit event references are declared.  
24. Owner team is declared.  
25. Version is valid.  
26. If deprecated, migration metadata exists.

If any of these conditions are missing, the State must not be used in the operational lifecycle.

---

## **16\. Runtime State Validation**

Before using State at runtime, the following validations are required:

Does the State exist in the registry?

Is the State active?

Does the State key match the pattern?

Is the State owner valid?

Does the State value satisfy the schema?

Does the State metadata satisfy the schema?

Are all required fields present?

Are observed\_at / updated\_at valid?

Does the State satisfy freshness requirements?

Is the State not stale?

Is the State not conflicting?

Does source event or source system lineage exist?

Is Decision / Safety Gate usage allowed?

If these conditions are not satisfied, the State must not be used by Decision, Policy, or Safety Gate.

---

## **17\. Freshness Rule**

Temporality is a core property of State.

Recommended freshness examples:

worker\_location\_state:

    max\_age\_seconds: 10

robot\_status\_state:

    max\_age\_seconds: 15

zone\_status\_state:

    max\_age\_seconds: 20

external\_system\_health\_state:

    max\_age\_seconds: 20

hazard\_state:

    max\_age\_seconds: 30

approval\_context\_state:

    max\_age\_seconds: 300

Core principle:

Stale State must not pass Safety Gate.

---

## **18\. State Update Rule**

State is updated by Events or External System Inputs.

Examples:

WorkerLocationUpdated

    → worker\_location\_state update

RobotStatusUpdated

    → robot\_status\_state update

ZoneStatusChanged

    → zone\_status\_state update

ExternalSystemHeartbeatReceived

    → external\_system\_health\_state update

Update validation conditions:

Event Type must be registered.

Event Producer Identity must be valid.

Event Payload Schema must be valid.

State Update Rule must exist.

State Owner Service must approve the update.

State Value Schema must be satisfied.

Transition Rule must not be violated.

---

## **19\. State Transition Rule**

Some States require transition rules.

Example: Robot Mission State

idle

    → assigned

    → en\_route

    → executing

    → completed

executing

    → paused

    → failed

paused

    → resumed

    → executing

failed

    → recovery\_required

Invalid transitions must be rejected.

completed → executing

    reject

faulted → dispatch\_ready

    reject unless recovery validation passed

---

## **20\. Conflict Rule**

State may come from multiple sources, so conflicts may occur.

Example:

UWB:

    worker\_123 in zone\_03

Vision:

    worker\_123 in zone\_04

Manual report:

    worker\_123 out of site

Conflict handling options:

prefer\_high\_trust\_source

prefer\_latest

merge\_if\_compatible

require\_manual\_review

hold\_for\_more\_evidence

trigger\_recompute

block\_safety\_gate

Safety-critical State conflicts must not be silently ignored.

Conflicting safety State must trigger review or block.

---

## **21\. Storage and Materialization Rule**

State may be materialized in different stores depending on its purpose.

Recommended distinction:

Redis:

    current hot state

    fast lookup

    Safety Gate runtime check

TimescaleDB / InfluxDB:

    time-series state history

    sensor trend

    telemetry

PostgreSQL:

    state metadata

    registry linkage

    lifecycle records

GraphDB / RDF Store:

    semantic fact projection

    ontology-grounded relationships

In-memory cache:

    hot path local process lookup

Core principle:

State Registry defines where state may live.

World State Store stores the actual current values.

---

## **22\. Relationship to Event Registry**

Event is the source that updates State.

event\_registry:

    Defines whether WorkerLocationUpdated is a valid event.

state\_registry:

    Defines whether this event may update worker\_location\_state.

Even if an Event is registered, it must not update State without a State Update Rule.

Valid Event ≠ Valid State Update

---

## **23\. Relationship to Snapshot Schema Registry**

State may be frozen into a Snapshot.

state\_registry:

    worker\_location\_state is the current worker location state.

snapshot\_schema\_registry:

    worker\_location\_snapshot is the structure that freezes that State at a specific point in time.

Core principle:

State changes over time.

Snapshot freezes State at one time.

---

## **24\. Relationship to Evidence Registry**

Evidence may use State or Snapshot as a basis.

state\_registry:

    Verifies whether worker\_location\_state is fresh.

evidence\_registry:

    Defines whether worker\_location\_snapshot\_evidence is sufficient as judgment basis.

The existence of State does not automatically make it Evidence.

State ≠ Valid Evidence

---

## **25\. Relationship to Decision Registry**

Decision may evaluate State directly or through Snapshot.

Example:

decision:dispatch\_robot\_v1

    requires:

        robot\_status\_state

        worker\_location\_state

        zone\_status\_state

        external\_system\_health\_state

Decision must check State freshness and conflict status.

---

## **26\. Relationship to Policy Registry**

Policy may require specific State conditions.

Example:

Robot Dispatch Policy:

    robot\_status\_state.availability\_status \== available

    worker\_location\_state not in robot\_path

    zone\_status\_state.access\_status \== accessible

    external\_system\_health\_state.reachable \== true

When Policy references State, that State must be registered, active, and fresh.

---

## **27\. Relationship to Runtime Validation Registry**

Runtime Validation uses State as input.

Examples:

runtime\_validation:worker\_not\_in\_robot\_path

    uses worker\_location\_state

runtime\_validation:robot\_available

    uses robot\_status\_state

runtime\_validation:zone\_accessible

    uses zone\_status\_state

runtime\_validation:external\_system\_reachable

    uses external\_system\_health\_state

`state_registry` provides the structure and freshness requirements for State used by runtime validation.

---

## **28\. Relationship to Safety Gate**

Safety Gate is the most important consumer of State.

Safety Gate:

    validates the latest State immediately before execution.

Example:

DISPATCH\_ROBOT Safety Gate:

    worker\_location\_state fresh?

    robot\_status\_state available?

    zone\_status\_state accessible?

    external\_system\_health\_state reachable?

    adapter\_health\_state healthy?

Core principle:

No fresh State,

no Safety Gate pass.

---

## **29\. Relationship to Ontology Registry**

State must be grounded in ontology IRIs.

Example:

state:worker\_location\_state\_v1

    semantic\_iri: ledo:WorkerLocationState

    entity\_type\_refs:

        class:Worker

        class:WorkZone

Ontology provides the meaning of the entities and relations represented by State.

State Registry provides the operational structure, key, source, update rule, and freshness requirement.

---

## **30\. Relationship to External System Registry**

External Systems may be State sources.

external\_system\_registry:

    robot\_fleet\_manager\_site\_A is a registered external system.

state\_registry:

    Defines whether robot\_fleet\_manager\_site\_A is an authorized source for updating robot\_status\_state.

Even if an External System is registered, it must not update State unless it is an allowed source for that State.

Registered External System ≠ Authorized State Source

---

## **31\. Relationship to Audit Registry**

State update and State usage must be auditable.

Audit targets:

state\_registered

state\_updated

state\_update\_rejected

state\_transition\_rejected

state\_validated

state\_stale\_detected

state\_conflict\_detected

state\_used\_by\_decision

state\_used\_by\_policy

state\_used\_by\_safety\_gate

state\_materialized

state\_replayed

Audit Record example:

state\_id: string

state\_key: string

state\_version: string

updated\_by\_identity\_id: string

source\_event\_ref: string

previous\_state\_hash: string | null

new\_state\_hash: string

freshness\_status: string

conflict\_status: string

trace\_id: string

timestamp: datetime

Core principle:

No State update without trace.

---

## **32\. Versioning and Migration**

State Registry Entries must be versioned.

A version change is required when any of the following changes:

1. State type changes  
2. State key pattern changes  
3. Owner service changes  
4. Source event type changes  
5. Source external system changes  
6. Allowed update producer changes  
7. State value schema changes  
8. State metadata schema changes  
9. Required fields change  
10. Update rules change  
11. Transition rules change  
12. Freshness requirement changes  
13. Stale policy changes  
14. Conflict policy changes  
15. Storage backend changes  
16. Snapshot schema reference changes  
17. `safety_gate_usable` changes  
18. `hot_path_allowed` changes  
19. Sensitivity / PII classification changes  
20. Decision / approval / execution / safety boundaries change

Status values:

draft

active

deprecated

migration\_required

retired

blocked

---

## **33\. Implementation Use**

`state_registry` is used to generate or validate:

1. `StateType` enum  
2. `StateCategory` enum  
3. `StateStatus` enum  
4. State metadata DTO  
5. State key pattern validation  
6. State owner lookup  
7. State source validation  
8. State update producer validation  
9. State value schema lookup  
10. State metadata schema lookup  
11. State update rule lookup  
12. State transition rule validation  
13. State freshness validation  
14. Stale State handling  
15. State conflict handling  
16. State storage backend routing  
17. State materialization rule lookup  
18. Snapshot schema binding  
19. Runtime validation state lookup  
20. Safety Gate state eligibility validation  
21. Audit log expectation  
22. Test case generation  
23. Migration rules

Implementation must not use unregistered State in World State or Safety Gate.

---

## **34\. Recommended Code Structure**

registries/

    state\_registry/

        state\_registry.py

        state\_entry.py

        state\_type.py

        state\_category.py

        state\_status.py

        state\_key.py

        state\_update\_rule.py

        state\_transition\_rule.py

        state\_freshness.py

        state\_storage\_ref.py

        state\_materialization.py

        state\_validation.py

        state\_errors.py

        state\_loader.py

        state\_migration.py

    event\_registry/

    snapshot\_schema\_registry/

    evidence\_registry/

    ontology\_registry/

    policy\_registry/

    decision\_registry/

    approval\_registry/

    runtime\_validation\_registry/

    safety\_gate\_registry/

    external\_system\_registry/

    audit\_event\_registry/

---

## **35\. Minimal Pydantic Model**

from enum import Enum

from pydantic import BaseModel, Field

from typing import Optional

from datetime import datetime

class StateStatus(str, Enum):

    DRAFT \= "draft"

    ACTIVE \= "active"

    DEPRECATED \= "deprecated"

    MIGRATION\_REQUIRED \= "migration\_required"

    RETIRED \= "retired"

    BLOCKED \= "blocked"

class StateCategory(str, Enum):

    WORLD\_STATE \= "world\_state"

    ENTITY\_STATE \= "entity\_state"

    WORKER\_STATE \= "worker\_state"

    ZONE\_STATE \= "zone\_state"

    ROBOT\_STATE \= "robot\_state"

    EQUIPMENT\_STATE \= "equipment\_state"

    HAZARD\_STATE \= "hazard\_state"

    EXTERNAL\_SYSTEM\_STATE \= "external\_system\_state"

    ADAPTER\_STATE \= "adapter\_state"

    ENVIRONMENT\_STATE \= "environment\_state"

    RUNTIME\_VALIDATION\_STATE \= "runtime\_validation\_state"

    EXECUTION\_LIFECYCLE\_STATE \= "execution\_lifecycle\_state"

    AUDIT\_REPLAY\_STATE \= "audit\_replay\_state"

class StorageBackend(str, Enum):

    REDIS \= "redis"

    TIMESCALEDB \= "timescaledb"

    INFLUXDB \= "influxdb"

    GRAPHDB \= "graphdb"

    POSTGRESQL \= "postgresql"

    IN\_MEMORY\_CACHE \= "in\_memory\_cache"

class SensitivityLevel(str, Enum):

    PUBLIC \= "public"

    INTERNAL \= "internal"

    CONFIDENTIAL \= "confidential"

    RESTRICTED \= "restricted"

    SAFETY\_CRITICAL \= "safety\_critical"

class PIIClassification(str, Enum):

    NONE \= "none"

    INDIRECT \= "indirect"

    DIRECT \= "direct"

    SENSITIVE \= "sensitive"

class FreshnessRequirement(BaseModel):

    max\_age\_seconds: int

    freshness\_policy\_ref: str

class StateRegistryEntry(BaseModel):

    state\_id: str

    canonical\_name: str

    display\_name: str

    description: str

    semantic\_iri: str

    state\_type: str

    state\_category: StateCategory

    version: str

    status: StateStatus \= StateStatus.DRAFT

    entity\_type\_refs: list\[str\] \= Field(default\_factory=list)

    state\_key\_pattern: str

    owner\_service\_ref: str

    owner\_module: str

    source\_event\_type\_refs: list\[str\] \= Field(default\_factory=list)

    source\_external\_system\_refs: list\[str\] \= Field(default\_factory=list)

    source\_sensor\_refs: list\[str\] \= Field(default\_factory=list)

    source\_agent\_type\_refs: list\[str\] \= Field(default\_factory=list)

    allowed\_update\_producer\_refs: list\[str\] \= Field(default\_factory=list)

    state\_value\_schema\_ref: str

    state\_metadata\_schema\_ref: str

    required\_fields: list\[str\] \= Field(default\_factory=list)

    optional\_fields: list\[str\] \= Field(default\_factory=list)

    update\_rule\_refs: list\[str\] \= Field(default\_factory=list)

    transition\_rule\_refs: list\[str\] \= Field(default\_factory=list)

    freshness\_requirement: FreshnessRequirement

    stale\_policy\_ref: str

    conflict\_policy\_ref: str

    storage\_backend\_refs: list\[StorageBackend\] \= Field(default\_factory=list)

    primary\_storage\_ref: str

    cache\_policy\_ref: Optional\[str\] \= None

    materialization\_policy\_ref: str

    snapshot\_schema\_refs: list\[str\] \= Field(default\_factory=list)

    runtime\_usable: bool \= True

    decision\_usable: bool \= False

    approval\_context\_usable: bool \= False

    safety\_gate\_usable: bool \= False

    hot\_path\_allowed: bool \= False

    retention\_policy\_ref: str

    replay\_policy\_ref: Optional\[str\] \= None

    sensitivity\_level: SensitivityLevel

    pii\_classification: PIIClassification \= PIIClassification.NONE

    decision\_boundary: str

    approval\_boundary: str

    execution\_boundary: str

    safety\_boundary: str

    audit\_required: bool \= True

    audit\_event\_refs: list\[str\] \= Field(default\_factory=list)

    owner\_team: str

    source\_document: str

    created\_at: datetime

    updated\_at: datetime

    deprecated\_since: Optional\[datetime\] \= None

    replacement\_state\_id: Optional\[str\] \= None

---

## **36\. Core Validation Function**

from datetime import datetime, timezone

def validate\_state\_for\_runtime\_use(

    entry: StateRegistryEntry,

    state\_key: str,

    state\_value: dict,

    observed\_at: datetime,

    require\_decision\_usable: bool \= False,

    require\_safety\_gate\_usable: bool \= False,

    require\_hot\_path\_allowed: bool \= False,

) \-\> None:

    if entry.status \!= StateStatus.ACTIVE:

        raise InvalidStateError(

            f"State is not active: {entry.state\_id}"

        )

    missing\_fields \= \[

        field for field in entry.required\_fields

        if field not in state\_value

    \]

    if missing\_fields:

        raise StateRequiredFieldMissingError(

            f"Missing required fields: {missing\_fields}"

        )

    now \= datetime.now(timezone.utc)

    age\_seconds \= (now \- observed\_at).total\_seconds()

    if age\_seconds \> entry.freshness\_requirement.max\_age\_seconds:

        raise StateStaleError(

            f"State is stale. age={age\_seconds}s, "

            f"max={entry.freshness\_requirement.max\_age\_seconds}s"

        )

    if require\_decision\_usable and not entry.decision\_usable:

        raise StateNotAllowedForDecisionError(

            f"State is not allowed for Decision: {entry.state\_id}"

        )

    if require\_safety\_gate\_usable and not entry.safety\_gate\_usable:

        raise StateNotAllowedForSafetyGateError(

            f"State is not allowed for Safety Gate: {entry.state\_id}"

        )

    if require\_hot\_path\_allowed and not entry.hot\_path\_allowed:

        raise StateNotAllowedForHotPathError(

            f"State is not allowed for hot path: {entry.state\_id}"

        )

    if not entry.owner\_service\_ref:

        raise InvalidStateError(

            "owner\_service\_ref must be declared"

        )

    if not entry.state\_key\_pattern:

        raise InvalidStateError(

            "state\_key\_pattern must be declared"

        )

    if not entry.stale\_policy\_ref:

        raise InvalidStateError(

            "stale\_policy\_ref must be declared"

        )

    if not entry.conflict\_policy\_ref:

        raise InvalidStateError(

            "conflict\_policy\_ref must be declared"

        )

    if not entry.primary\_storage\_ref:

        raise InvalidStateError(

            "primary\_storage\_ref must be declared"

        )

---

## **37\. Test Scenarios**

Required tests:

1\. Reject unregistered State.

2\. Reject inactive State.

3\. Reject runtime use of deprecated State.

4\. Reject blocked State.

5\. Reject state key pattern mismatch.

6\. Reject missing owner service.

7\. Reject missing source event.

8\. Reject unauthorized update producer.

9\. Reject missing required fields.

10\. Reject state value schema mismatch.

11\. Reject state metadata schema mismatch.

12\. Reject State that exceeds freshness requirement.

13\. Reject missing stale policy.

14\. Reject missing conflict policy.

15\. Reject invalid state transition.

16\. Verify block or review handling when conflicting State occurs.

17\. Reject Decision use when decision\_usable is false.

18\. Reject Safety Gate use when safety\_gate\_usable is false.

19\. Reject hot path use when hot\_path\_allowed is false.

20\. Verify Snapshot schema binding.

21\. Verify State update audit trace creation.

22\. Verify State migration rules.

---

## **38\. Final Rule**

No registered State,

no official Current State.

No valid State,

no trustworthy Snapshot.

No fresh State,

no Safety Gate pass.

State is not Event.

State is not Snapshot.

State is not Evidence.

State is not Approval.

State is not ExecutionRequest.

State is not PhysicalCommand.

State represents what is currently true.

State Registry defines the operational contract of that State.

`state_registry` is the core deterministic registry that governs the meaning, key, owner, source, update rule, transition rule, freshness, storage, snapshot binding, runtime usability, and Safety Gate usability of every current State item in the LEDO system.

This module controls whether changes coming from Events may be reflected as official World State, and prevents stale, conflicting, or unregistered State from being used in Decision, Policy, Safety Gate, and Execution flows.

The core definition is:

State Registry

\= not a simple list of state variables,

but an operational contract registry that controls

the type, key, owner, source, update rule, transition rule,

freshness, storage backend, snapshot binding, runtime usability,

Safety Gate eligibility, stale/conflict policy, and audit rule

of every current State used in LEDO.

