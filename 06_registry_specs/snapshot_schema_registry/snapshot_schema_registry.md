**Snapshot Schema registry**

## **1\. Overview**

`snapshot_schema_registry` is a core registry in the LEDO Ontology-Centric Cyber-Physical System. It defines and governs all Snapshot Types, Snapshot Schemas, Runtime State Snapshots, Evidence Snapshots, Safety Gate Snapshots, World State Snapshots, Native Memory Layouts, Serialization Contracts, Freshness Rules, Immutability Rules, and Version Rules used across the system.

The purpose of this module is to allow LEDO to safely freeze World State, Evidence, Sensor State, Robot State, Worker State, Zone State, and External System State at a specific point in time, so that Decision, Approval, Safety Gate, and Execution flows can validate against the same reproducible state basis.

`snapshot_schema_registry` is not a simple list of JSON schemas.

It is an **operational contract registry for state snapshot structure, temporality, immutability, memory layout, and validation** that defines the following:

Which Snapshot Types may exist?

Which World State or Evidence does this Snapshot freeze?

Which schema must this Snapshot follow?

How fresh must this Snapshot be?

Can this Snapshot be used for Decision?

Can this Snapshot be used for Approval?

Can this Snapshot be used on the Safety Gate hot path?

Is this Snapshot exchanged through an Arrow schema?

Is this Snapshot queried through a C++ native fixed layout?

Is this Snapshot immutable?

Can this Snapshot be replayed, audited, and migrated?

In other words, `snapshot_schema_registry` is the core registry that controls **“how a specific point-in-time state is frozen and validated”** inside LEDO.

---

## **2\. Core Principle**

A Snapshot is a frozen slice of current state.

A Snapshot is not an Event.

A Snapshot is not Evidence itself.

A Snapshot is not World State itself.

A Snapshot is not Approval.

A Snapshot is not an ExecutionRequest.

A Snapshot is not a Physical Command.

The basic meaning of Snapshot is:

World State continuously changes.

Snapshot freezes World State at a specific point in time.

Event records what happened.

Snapshot freezes the state bundle at that moment.

Evidence is a basis for judgment.

Snapshot is a state structure that Evidence may reference.

The core principle is:

Event records what happened.

World State stores current facts.

Snapshot freezes selected state at a specific time.

Evidence uses Snapshot as a basis for judgment.

Decision evaluates Evidence and Snapshot.

Safety Gate revalidates fresh runtime Snapshot.

ExecutionRequest must not be created from stale Snapshot.

The especially important LEDO principle is:

Approval-time Snapshot must not be blindly reused at execution time.

Safety Gate must use fresh runtime Snapshot.

Stale Snapshot must not pass Safety Gate.

---

## **3\. Position in the LEDO Architecture**

`snapshot_schema_registry` is a cross-cutting registry located between the Real-Time World State Layer, Knowledge & Semantic Memory Layer, Evidence Registry, Decision Registry, and Safety Gate Layer.

Event Stream / Sensor / External System / Agent

        ↓

World State Update

        ↓

Snapshot Builder

        ↓

snapshot\_schema\_registry validation

        ↓

Immutable Snapshot

        ↓

Evidence / Decision / Approval / Safety Gate

In the full lifecycle, it is positioned as follows:

Event

    ↓

World State Update

    ↓

Snapshot Created

    ↓

Snapshot Schema Validation

    ↓

Evidence Instance / EvidenceBundle

    ↓

DecisionCase

    ↓

ApprovalRequest

    ↓

ApprovedAction

    ↓

Fresh Runtime Snapshot Revalidation

    ↓

Safety Gate

    ↓

ExecutionRequest

---

## **4\. Purpose**

The purpose of `snapshot_schema_registry` is to ensure the following:

1. Prevent the use of unregistered Snapshot Types  
2. Define schemas for each Snapshot  
3. Define required fields for each Snapshot  
4. Define freshness requirements for each Snapshot  
5. Define source event / world state dependencies for each Snapshot  
6. Define immutability rules for each Snapshot  
7. Define serialization formats for each Snapshot  
8. Define runtime usability for each Snapshot  
9. Define whether each Snapshot may be used on the Safety Gate hot path  
10. Define the boundary between Arrow schema and native layout  
11. Define C++ native fixed layout references  
12. Define whether shared memory / mmap may be used  
13. Define usage scope for Decision / Approval / Safety Gate  
14. Manage Snapshot versioning and migration  
15. Define Snapshot replay and audit rules  
16. Define how to handle stale, conflicting, or incomplete Snapshots

---

## **5\. Core Distinctions**

### **5.1 Snapshot**

`Snapshot` is an immutable object that freezes selected state information at a specific point in time.

Examples:

worker\_location\_snapshot

zone\_status\_snapshot

robot\_availability\_snapshot

equipment\_status\_snapshot

hazard\_state\_snapshot

external\_system\_health\_snapshot

adapter\_health\_snapshot

world\_state\_consistency\_snapshot

safety\_gate\_runtime\_snapshot

A Snapshot must not be modified.

If new state is required, a new Snapshot must be created instead of modifying the existing Snapshot.

Snapshot is immutable.

Updated state requires a new Snapshot.

---

### **5.2 Snapshot Type**

`Snapshot Type` defines what kind of state slice the Snapshot represents.

Examples:

WORKER\_LOCATION\_SNAPSHOT

ZONE\_STATUS\_SNAPSHOT

ROBOT\_STATUS\_SNAPSHOT

EQUIPMENT\_STATUS\_SNAPSHOT

HAZARD\_STATE\_SNAPSHOT

EXTERNAL\_SYSTEM\_HEALTH\_SNAPSHOT

ADAPTER\_HEALTH\_SNAPSHOT

WORLD\_STATE\_SNAPSHOT

SAFETY\_GATE\_RUNTIME\_SNAPSHOT

---

### **5.3 Snapshot Schema**

`Snapshot Schema` defines the structure that a Snapshot payload must follow.

Example:

snapshot\_id: string

snapshot\_type: string

created\_at: datetime

observed\_at: datetime

valid\_until: datetime

entity\_refs:

  \- string

payload:

  worker\_id: string

  zone\_id: string

  location\_confidence: float

  source\_system\_ref: string

Snapshot Schema may be expressed as JSON Schema, Pydantic Model, Protobuf Schema, Arrow Schema, or Native Layout Contract.

---

### **5.4 Runtime Snapshot**

`Runtime Snapshot` is the latest state Snapshot used by Safety Gate or runtime validation.

Examples:

worker\_location\_fresh\_snapshot

robot\_available\_runtime\_snapshot

external\_system\_reachable\_snapshot

adapter\_health\_runtime\_snapshot

Runtime Snapshots have very strict freshness requirements.

---

### **5.5 Evidence Snapshot**

`Evidence Snapshot` is a Snapshot referenced by an Evidence Instance as a basis for judgment.

Examples:

hazard\_detection\_snapshot

worker\_location\_snapshot

risk\_assessment\_snapshot

sensor\_freshness\_snapshot

Evidence Snapshot is connected to `evidence_registry`.

---

### **5.6 Safety Gate Snapshot**

`Safety Gate Snapshot` is the Snapshot used by the Safety Gate for final validation immediately before creating an ExecutionRequest.

Examples:

safety\_gate\_runtime\_snapshot

worker\_not\_in\_hazard\_zone\_snapshot

robot\_path\_clear\_snapshot

external\_system\_ready\_snapshot

adapter\_healthy\_snapshot

Core principle:

Safety Gate Snapshot must be fresh.

Safety Gate Snapshot must be immutable.

Safety Gate Snapshot must be generated after approval and before execution.

---

### **5.7 Difference Between Snapshot Schema and Evidence Schema**

They are different.

snapshot\_schema\_registry:

    Defines the structure of a point-in-time state bundle.

evidence\_registry:

    Defines Evidence Type, quality, freshness, and lineage that may be used as a basis for judgment.

Example:

worker\_location\_snapshot

    → Snapshot Schema

worker\_location\_snapshot\_evidence

    → Evidence Type

A Snapshot may become material for Evidence, but a Snapshot itself is not always Evidence.

---

## **6\. Scope**

`snapshot_schema_registry` controls the following fields:

snapshot\_schema\_id: string

canonical\_name: string

display\_name: string

description: string

semantic\_iri: string

snapshot\_type: string

snapshot\_category: string

version: string

status: draft | active | deprecated | migration\_required | retired | blocked

applicable\_entity\_type\_refs:

  \- string

applicable\_event\_type\_refs:

  \- string

applicable\_evidence\_type\_refs:

  \- string

applicable\_decision\_rule\_refs:

  \- string

applicable\_safety\_gate\_refs:

  \- string

source\_world\_state\_refs:

  \- string

source\_event\_refs:

  \- string

source\_external\_system\_refs:

  \- string

payload\_schema\_ref: string

metadata\_schema\_ref: string

required\_fields:

  \- string

optional\_fields:

  \- string

freshness\_requirement:

  max\_age\_seconds: integer

  freshness\_policy\_ref: string

immutability\_required: boolean

lineage\_required: boolean

provenance\_required: boolean

serialization\_formats:

  \- json

  \- protobuf

  \- arrow

  \- native\_fixed\_layout

arrow\_schema\_ref: string | null

native\_layout\_ref: string | null

shared\_memory\_layout\_ref: string | null

runtime\_usable: boolean

safety\_gate\_usable: boolean

hot\_path\_allowed: boolean

cache\_policy\_ref: string | null

retention\_policy\_ref: string

conflict\_policy\_ref: string

stale\_policy\_ref: string

sensitivity\_level: public | internal | confidential | restricted | safety\_critical

pii\_classification: none | indirect | direct | sensitive

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

replacement\_snapshot\_schema\_id: string | null

---

## **7\. Non-Scope**

`snapshot_schema_registry` does not directly define the following:

1. All Event payload schemas  
2. All Evidence payload schemas  
3. Complete World State storage structure  
4. Complete Redis key design  
5. Complete TimescaleDB / InfluxDB schemas  
6. Complete Triple Store internal schema  
7. Sensor driver logic  
8. Model inference logic  
9. Policy pass/fail logic  
10. Approval authority  
11. Complete Safety Gate final judgment logic  
12. External System adapter implementation  
13. Physical Command  
14. Robot motion planning  
15. PLC / SCADA low-level control

These responsibilities belong to the following modules or systems:

event\_registry

evidence\_registry

world\_state\_store

runtime\_validation\_registry

policy\_registry

approval\_registry

safety\_gate

adapter\_registry

external\_system\_registry

model\_adapter\_registry

sensor\_gateway

robot\_fleet\_manager

PLC / SCADA

`snapshot_schema_registry` defines Snapshot structure and usability.  
Actual Snapshot creation is performed by Snapshot Builder or World State Service.

---

## **8\. Snapshot Category Model**

Recommended Snapshot Categories are:

WORLD\_STATE\_SNAPSHOT

ENTITY\_STATE\_SNAPSHOT

WORKER\_STATE\_SNAPSHOT

ZONE\_STATE\_SNAPSHOT

ROBOT\_STATE\_SNAPSHOT

EQUIPMENT\_STATE\_SNAPSHOT

HAZARD\_STATE\_SNAPSHOT

EXTERNAL\_SYSTEM\_STATE\_SNAPSHOT

ADAPTER\_STATE\_SNAPSHOT

RUNTIME\_VALIDATION\_SNAPSHOT

SAFETY\_GATE\_SNAPSHOT

EVIDENCE\_SUPPORT\_SNAPSHOT

AUDIT\_REPLAY\_SNAPSHOT

### **8.1 WORLD\_STATE\_SNAPSHOT**

Freezes part or all of the World State at a specific point in time.

Example:

world\_state\_snapshot\_site\_A\_20260626T120000Z

---

### **8.2 WORKER\_STATE\_SNAPSHOT**

Freezes worker location, status, zone membership, and proximity state.

Examples:

worker\_location\_snapshot

worker\_zone\_membership\_snapshot

worker\_proximity\_snapshot

---

### **8.3 ZONE\_STATE\_SNAPSHOT**

Freezes zone accessibility, hazard state, and lock state.

Examples:

zone\_status\_snapshot

hazard\_zone\_snapshot

locked\_zone\_snapshot

---

### **8.4 ROBOT\_STATE\_SNAPSHOT**

Freezes robot availability, battery, mission state, and fault state.

Examples:

robot\_availability\_snapshot

robot\_mission\_state\_snapshot

robot\_battery\_snapshot

---

### **8.5 EXTERNAL\_SYSTEM\_STATE\_SNAPSHOT**

Freezes external system reachability, health, and last heartbeat state.

Examples:

robot\_fleet\_manager\_health\_snapshot

scada\_connection\_snapshot

notification\_gateway\_health\_snapshot

---

### **8.6 SAFETY\_GATE\_SNAPSHOT**

A Snapshot used by Safety Gate immediately before creating an ExecutionRequest.

Examples:

safety\_gate\_runtime\_snapshot

pre\_execution\_worker\_location\_snapshot

pre\_execution\_external\_system\_ready\_snapshot

---

## **9\. Registry Entry Schema**

Each Snapshot Schema Registry entry follows this structure:

snapshot\_schema\_id: string

canonical\_name: string

display\_name: string

description: string

semantic\_iri: string

snapshot\_type: string

snapshot\_category: string

version: string

status: draft | active | deprecated | migration\_required | retired | blocked

applicable\_entity\_type\_refs:

  \- string

applicable\_event\_type\_refs:

  \- string

applicable\_evidence\_type\_refs:

  \- string

applicable\_decision\_rule\_refs:

  \- string

applicable\_safety\_gate\_refs:

  \- string

source\_world\_state\_refs:

  \- string

source\_event\_refs:

  \- string

source\_external\_system\_refs:

  \- string

payload\_schema\_ref: string

metadata\_schema\_ref: string

required\_fields:

  \- string

optional\_fields:

  \- string

freshness\_requirement:

  max\_age\_seconds: integer

  freshness\_policy\_ref: string

immutability\_required: boolean

lineage\_required: boolean

provenance\_required: boolean

serialization\_formats:

  \- string

arrow\_schema\_ref: string | null

native\_layout\_ref: string | null

shared\_memory\_layout\_ref: string | null

runtime\_usable: boolean

safety\_gate\_usable: boolean

hot\_path\_allowed: boolean

cache\_policy\_ref: string | null

retention\_policy\_ref: string

conflict\_policy\_ref: string

stale\_policy\_ref: string

sensitivity\_level: string

pii\_classification: string

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

replacement\_snapshot\_schema\_id: string | null

---

## **10\. Registry Entry Example: Worker Location Snapshot Schema**

snapshot\_schema\_id: snapshot\_schema:worker\_location\_snapshot\_v1

canonical\_name: worker\_location\_snapshot\_v1

display\_name: Worker Location Snapshot Schema

description: A snapshot schema that freezes worker location, zone membership, confidence, and source timestamp at a specific point in time.

semantic\_iri: ledo:WorkerLocationSnapshotSchema

snapshot\_type: WORKER\_LOCATION\_SNAPSHOT

snapshot\_category: WORKER\_STATE\_SNAPSHOT

version: 1.0.0

status: active

applicable\_entity\_type\_refs:

  \- class:Worker

  \- class:WorkZone

  \- class:Location

applicable\_event\_type\_refs:

  \- event:WorkerLocationUpdated

  \- event:WorkerEnteredZone

  \- event:WorkerExitedZone

applicable\_evidence\_type\_refs:

  \- evidence:worker\_location\_snapshot

applicable\_decision\_rule\_refs:

  \- decision:stop\_work\_safety\_risk\_v1

  \- decision:dispatch\_robot\_v1

applicable\_safety\_gate\_refs:

  \- safety\_gate:worker\_not\_in\_hazard\_zone\_validation

  \- safety\_gate:worker\_not\_in\_robot\_path\_validation

source\_world\_state\_refs:

  \- world\_state:worker\_location\_state

  \- world\_state:zone\_membership\_state

source\_event\_refs:

  \- event:WorkerLocationUpdated

source\_external\_system\_refs:

  \- external\_system:worker\_tracking\_gateway\_site\_A

  \- external\_system:vision\_location\_system\_site\_A

payload\_schema\_ref: schema:worker\_location\_snapshot\_payload\_v1

metadata\_schema\_ref: schema:snapshot\_metadata\_v1

required\_fields:

  \- worker\_id

  \- observed\_at

  \- zone\_id

  \- location\_confidence

  \- source\_system\_ref

optional\_fields:

  \- x

  \- y

  \- z

  \- floor\_id

  \- coordinate\_system\_ref

  \- tracking\_method

freshness\_requirement:

  max\_age\_seconds: 10

  freshness\_policy\_ref: policy:worker\_location\_snapshot\_freshness\_v1

immutability\_required: true

lineage\_required: true

provenance\_required: true

serialization\_formats:

  \- json

  \- protobuf

  \- arrow

  \- native\_fixed\_layout

arrow\_schema\_ref: arrow\_schema:worker\_location\_snapshot\_v1

native\_layout\_ref: native\_layout:worker\_location\_snapshot\_fixed\_v1

shared\_memory\_layout\_ref: shm\_layout:worker\_location\_snapshot\_site\_A\_v1

runtime\_usable: true

safety\_gate\_usable: true

hot\_path\_allowed: true

cache\_policy\_ref: cache:worker\_location\_snapshot\_cache\_v1

retention\_policy\_ref: retention:worker\_location\_snapshot\_retention\_v1

conflict\_policy\_ref: conflict:worker\_location\_conflict\_policy\_v1

stale\_policy\_ref: stale:worker\_location\_stale\_policy\_v1

sensitivity\_level: restricted

pii\_classification: direct

decision\_boundary: may\_support\_decision\_case\_but\_not\_decide

approval\_boundary: may\_support\_approval\_context\_but\_not\_approve

execution\_boundary: must\_not\_create\_execution\_request

safety\_boundary: stale\_or\_conflicting\_snapshot\_must\_block\_safety\_gate

audit\_required: true

audit\_event\_refs:

  \- audit:snapshot\_created

  \- audit:snapshot\_validated

  \- audit:snapshot\_stale\_detected

  \- audit:snapshot\_conflict\_detected

  \- audit:snapshot\_used\_by\_safety\_gate

owner\_module: real\_time\_world\_state\_module

owner\_team: LEDO Runtime State

source\_document: worker\_location\_snapshot\_schema\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_snapshot\_schema\_id: null

---

## **11\. Registry Entry Example: Robot Availability Snapshot Schema**

snapshot\_schema\_id: snapshot\_schema:robot\_availability\_snapshot\_v1

canonical\_name: robot\_availability\_snapshot\_v1

display\_name: Robot Availability Snapshot Schema

description: A snapshot schema that freezes robot availability, mission state, battery, fault, and fleet manager state at a specific point in time.

semantic\_iri: ledo:RobotAvailabilitySnapshotSchema

snapshot\_type: ROBOT\_AVAILABILITY\_SNAPSHOT

snapshot\_category: ROBOT\_STATE\_SNAPSHOT

version: 1.0.0

status: active

applicable\_entity\_type\_refs:

  \- class:Robot

  \- class:RobotFleet

  \- class:RobotMission

  \- class:ExternalSystem

applicable\_event\_type\_refs:

  \- event:RobotStatusUpdated

  \- event:RobotMissionStateChanged

  \- event:ExternalSystemStatusUpdated

applicable\_evidence\_type\_refs:

  \- evidence:robot\_availability\_snapshot

applicable\_decision\_rule\_refs:

  \- decision:dispatch\_robot\_v1

applicable\_safety\_gate\_refs:

  \- safety\_gate:robot\_available\_validation

  \- safety\_gate:fleet\_manager\_reachable\_validation

source\_world\_state\_refs:

  \- world\_state:robot\_status\_state

  \- world\_state:robot\_mission\_state

  \- world\_state:external\_system\_health\_state

source\_event\_refs:

  \- event:RobotStatusUpdated

  \- event:RobotMissionStateChanged

source\_external\_system\_refs:

  \- external\_system:robot\_fleet\_manager\_site\_A

payload\_schema\_ref: schema:robot\_availability\_snapshot\_payload\_v1

metadata\_schema\_ref: schema:snapshot\_metadata\_v1

required\_fields:

  \- robot\_id

  \- fleet\_id

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

freshness\_requirement:

  max\_age\_seconds: 15

  freshness\_policy\_ref: policy:robot\_availability\_snapshot\_freshness\_v1

immutability\_required: true

lineage\_required: true

provenance\_required: true

serialization\_formats:

  \- json

  \- protobuf

  \- arrow

  \- native\_fixed\_layout

arrow\_schema\_ref: arrow\_schema:robot\_availability\_snapshot\_v1

native\_layout\_ref: native\_layout:robot\_availability\_snapshot\_fixed\_v1

shared\_memory\_layout\_ref: shm\_layout:robot\_availability\_snapshot\_site\_A\_v1

runtime\_usable: true

safety\_gate\_usable: true

hot\_path\_allowed: true

cache\_policy\_ref: cache:robot\_availability\_snapshot\_cache\_v1

retention\_policy\_ref: retention:robot\_availability\_snapshot\_retention\_v1

conflict\_policy\_ref: conflict:robot\_availability\_conflict\_policy\_v1

stale\_policy\_ref: stale:robot\_availability\_stale\_policy\_v1

sensitivity\_level: restricted

pii\_classification: none

decision\_boundary: may\_support\_robot\_dispatch\_decision\_but\_not\_decide

approval\_boundary: may\_support\_robot\_dispatch\_approval\_context\_but\_not\_approve

execution\_boundary: must\_not\_dispatch\_robot

safety\_boundary: stale\_or\_unavailable\_robot\_snapshot\_must\_block\_dispatch

audit\_required: true

audit\_event\_refs:

  \- audit:snapshot\_created

  \- audit:snapshot\_validated

  \- audit:snapshot\_stale\_detected

  \- audit:snapshot\_used\_by\_safety\_gate

owner\_module: robot\_runtime\_state\_module

owner\_team: LEDO Robotics Runtime

source\_document: robot\_availability\_snapshot\_schema\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_snapshot\_schema\_id: null

---

## **12\. Registry Entry Example: External System Health Snapshot Schema**

snapshot\_schema\_id: snapshot\_schema:external\_system\_health\_snapshot\_v1

canonical\_name: external\_system\_health\_snapshot\_v1

display\_name: External System Health Snapshot Schema

description: A snapshot schema that freezes external system health, reachability, heartbeat, and last response state at a specific point in time.

semantic\_iri: ledo:ExternalSystemHealthSnapshotSchema

snapshot\_type: EXTERNAL\_SYSTEM\_HEALTH\_SNAPSHOT

snapshot\_category: EXTERNAL\_SYSTEM\_STATE\_SNAPSHOT

version: 1.0.0

status: active

applicable\_entity\_type\_refs:

  \- class:ExternalSystem

  \- class:Adapter

  \- class:IntegrationEndpoint

applicable\_event\_type\_refs:

  \- event:ExternalSystemStatusUpdated

  \- event:AdapterHealthChanged

  \- event:ExecutionResultReceived

applicable\_evidence\_type\_refs:

  \- evidence:external\_system\_reachable\_snapshot

  \- evidence:adapter\_health\_snapshot

applicable\_decision\_rule\_refs:

  \- decision:dispatch\_robot\_v1

applicable\_safety\_gate\_refs:

  \- safety\_gate:external\_system\_reachable\_validation

  \- safety\_gate:adapter\_health\_valid\_validation

source\_world\_state\_refs:

  \- world\_state:external\_system\_health\_state

  \- world\_state:adapter\_health\_state

source\_event\_refs:

  \- event:ExternalSystemStatusUpdated

  \- event:AdapterHealthChanged

source\_external\_system\_refs:

  \- external\_system:robot\_fleet\_manager\_site\_A

  \- external\_system:scada\_system\_site\_A

  \- external\_system:notification\_gateway\_site\_A

payload\_schema\_ref: schema:external\_system\_health\_snapshot\_payload\_v1

metadata\_schema\_ref: schema:snapshot\_metadata\_v1

required\_fields:

  \- external\_system\_id

  \- observed\_at

  \- health\_status

  \- reachable

  \- last\_heartbeat\_at

  \- last\_successful\_request\_at

  \- adapter\_id

optional\_fields:

  \- response\_latency\_ms

  \- error\_code

  \- degraded\_reason

  \- maintenance\_window\_ref

freshness\_requirement:

  max\_age\_seconds: 20

  freshness\_policy\_ref: policy:external\_system\_health\_freshness\_v1

immutability\_required: true

lineage\_required: true

provenance\_required: true

serialization\_formats:

  \- json

  \- protobuf

  \- arrow

  \- native\_fixed\_layout

arrow\_schema\_ref: arrow\_schema:external\_system\_health\_snapshot\_v1

native\_layout\_ref: native\_layout:external\_system\_health\_snapshot\_fixed\_v1

shared\_memory\_layout\_ref: shm\_layout:external\_system\_health\_snapshot\_site\_A\_v1

runtime\_usable: true

safety\_gate\_usable: true

hot\_path\_allowed: true

cache\_policy\_ref: cache:external\_system\_health\_snapshot\_cache\_v1

retention\_policy\_ref: retention:external\_system\_health\_snapshot\_retention\_v1

conflict\_policy\_ref: conflict:external\_system\_health\_conflict\_policy\_v1

stale\_policy\_ref: stale:external\_system\_health\_stale\_policy\_v1

sensitivity\_level: restricted

pii\_classification: none

decision\_boundary: may\_support\_execution\_readiness\_decision\_but\_not\_decide

approval\_boundary: does\_not\_grant\_approval

execution\_boundary: must\_not\_create\_external\_control\_request

safety\_boundary: unreachable\_external\_system\_snapshot\_must\_block\_execution\_path

audit\_required: true

audit\_event\_refs:

  \- audit:snapshot\_created

  \- audit:snapshot\_validated

  \- audit:external\_system\_snapshot\_stale\_detected

  \- audit:snapshot\_used\_by\_safety\_gate

owner\_module: execution\_integration\_module

owner\_team: LEDO External Integration

source\_document: external\_system\_health\_snapshot\_schema\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_snapshot\_schema\_id: null

---

## **13\. Snapshot Lifecycle Alignment**

Snapshot is connected to the following lifecycle:

Source Event / World State Updated

        ↓

Snapshot Build Request

        ↓

Snapshot Schema Lookup

        ↓

Payload Extraction

        ↓

Schema Validation

        ↓

Freshness Validation

        ↓

Lineage / Provenance Binding

        ↓

Immutable Snapshot Created

        ↓

Snapshot Stored / Cached / Published

        ↓

Evidence / Decision / Approval / Safety Gate Usage

        ↓

Audit / Replay / Retention / Migration

The important point is that a Snapshot is not modified after creation.

Snapshot is not updated.

Snapshot is replaced by a new Snapshot.

---

## **14\. Validation Rules**

A Snapshot Schema Registry Entry is valid only when the following conditions are satisfied:

1. `snapshot_schema_id` exists in the registry.  
2. Its status is `active`.  
3. Snapshot type is declared.  
4. Snapshot category is declared.  
5. Payload schema reference is declared.  
6. Metadata schema reference is declared.  
7. Required fields are declared.  
8. Freshness requirement is declared.  
9. Immutability rule is declared.  
10. Lineage / provenance requirement is declared.  
11. Serialization format is declared.  
12. Safety Gate usability is declared.  
13. Hot path permission is declared.  
14. Stale policy is declared.  
15. Conflict policy is declared.  
16. Sensitivity / PII classification is declared.  
17. Decision / approval / execution / safety boundaries are declared.  
18. Audit event references are declared.  
19. Owner module is declared.  
20. Version is valid.  
21. If deprecated, migration metadata exists.

If any of these conditions are missing, the Snapshot Schema must not be used in the operational lifecycle.

---

## **15\. Runtime Snapshot Validation**

Before using a Snapshot at runtime, the following validations are required:

Does the Snapshot Schema exist in the registry?

Is the Snapshot Schema active?

Does the Snapshot payload satisfy the schema?

Does the Snapshot metadata satisfy the schema?

Are all required fields present?

Are observed\_at / created\_at valid?

Does the Snapshot satisfy freshness requirements?

Does lineage exist?

Does provenance exist?

Is the Snapshot stored immutably?

Is the Snapshot not stale?

Is the Snapshot not conflicting?

Is the schema allowed for Safety Gate usage?

Is hot path usage allowed?

If these conditions are not satisfied, the Snapshot must not be used by Decision, Approval, or Safety Gate.

---

## **16\. Freshness Rule**

Temporality is a core property of Snapshot.

Recommended freshness examples:

worker\_location\_snapshot:

    max\_age\_seconds: 10

robot\_availability\_snapshot:

    max\_age\_seconds: 15

external\_system\_health\_snapshot:

    max\_age\_seconds: 20

hazard\_detection\_snapshot:

    max\_age\_seconds: 30

approval\_context\_snapshot:

    max\_age\_seconds: 300

audit\_replay\_snapshot:

    freshness not required, replay context only

Core principle:

Stale Snapshot must not pass Safety Gate.

---

## **17\. Immutability Rule**

Snapshot must be immutable.

The payload of the same snapshot\_id must not be modified.

If the state changes, a new Snapshot with a new snapshot\_id must be created.

Recommended metadata:

snapshot\_id: string

snapshot\_schema\_id: string

snapshot\_version: string

created\_at: datetime

observed\_at: datetime

valid\_until: datetime | null

source\_event\_refs:

  \- string

source\_world\_state\_refs:

  \- string

lineage\_refs:

  \- string

content\_hash: string

signature\_ref: string | null

Core principle:

Mutable Snapshot breaks audit.

Immutable Snapshot enables replay.

---

## **18\. Conflict Rule**

Conflicts may occur between Snapshots.

Example:

UWB system:

    worker\_123 is in zone\_03

Vision system:

    worker\_123 is in zone\_04

Manual report:

    worker\_123 left the area

Conflict handling options:

prefer\_high\_trust\_source

prefer\_latest

require\_manual\_review

hold\_for\_more\_evidence

trigger\_recompute

block\_safety\_gate

In safety-critical situations, conflicts must not be ignored.

Conflicting safety Snapshot must trigger review or block.

---

## **19\. Arrow Schema and Native Layout Rule**

Snapshot performance is important in LEDO.

The recommended structure is:

Arrow:

    Python ↔ C++ snapshot exchange

    schema validation

    zero-copy interchange

    batch processing

Native Fixed Layout:

    Safety Gate hot path lookup

    cache-aligned immutable snapshot

    bitset / flat array / fixed key layout

    C++ fast validation

Shared Memory / mmap:

    process isolation

    active / shadow snapshot switching

    low-latency runtime access

Core principle:

Arrow is exchange and schema boundary.

Native fixed layout is hot path lookup boundary.

In other words, Arrow should not be used as the internal lookup structure of the Safety Gate hot path. Arrow is better used for transfer, validation, and exchange, while the final hot path should use a C++ native fixed layout.

---

## **20\. Hot Path Rule**

Snapshot Schemas used on the Safety Gate hot path must be stricter.

Conditions:

A fixed layout must exist.

Field count and field types must be fixed.

Optional fields must not affect hot path judgment.

Freshness requirement must be explicit.

Stale policy must be block.

Conflict policy must be block or manual review.

Allocation-free lookup must be possible.

Core principle:

Hot path Snapshot must be fixed, fresh, immutable, and deterministic.

---

## **21\. Relationship to Event Registry**

Event may become the source of Snapshot creation.

event\_registry:

    WorkerLocationUpdated event occurs.

snapshot\_schema\_registry:

    Defines whether worker\_location\_snapshot may be created from WorkerLocationUpdated event.

However, Event and Snapshot are different.

Event \= what happened

Snapshot \= state frozen at a specific time

---

## **22\. Relationship to Evidence Registry**

Evidence may use Snapshot as a basis.

snapshot\_schema\_registry:

    Defines the structure of worker\_location\_snapshot.

evidence\_registry:

    Defines the conditions under which worker\_location\_snapshot\_evidence is valid as a basis for judgment.

The existence of a Snapshot does not automatically make it Evidence.

Snapshot ≠ Valid Evidence

---

## **23\. Relationship to Decision Registry**

DecisionCase may evaluate Snapshots.

Example:

decision:dispatch\_robot\_v1

    requires:

        robot\_availability\_snapshot

        worker\_location\_snapshot

        zone\_accessibility\_snapshot

Decision must check Snapshot freshness and completeness.

---

## **24\. Relationship to Approval Registry**

ApprovalRequest may use Snapshot as context.

However, a Snapshot from approval time must not be assumed valid until execution time.

Approval Snapshot supports human judgment.

Safety Gate Snapshot validates execution readiness.

Core principle:

Approval-time Snapshot ≠ Execution-time Snapshot

---

## **25\. Relationship to Policy Registry**

Policy may require specific Snapshots.

Example:

STOP\_WORK policy:

    requires hazard\_detection\_snapshot

    requires worker\_location\_snapshot

Robot Dispatch policy:

    requires robot\_availability\_snapshot

    requires worker\_location\_snapshot

    requires external\_system\_health\_snapshot

If policy evaluation fails due to stale Snapshot, it must not be treated as allow.

---

## **26\. Relationship to Runtime Validation Registry**

Runtime Validation uses Snapshot as input.

Examples:

runtime\_validation:worker\_location\_fresh

    uses worker\_location\_snapshot

runtime\_validation:external\_system\_reachable

    uses external\_system\_health\_snapshot

runtime\_validation:robot\_available

    uses robot\_availability\_snapshot

`snapshot_schema_registry` provides the Snapshot structure required by runtime validation.

---

## **27\. Relationship to Safety Gate**

Safety Gate is the most important consumer of Snapshots.

Safety Gate:

    performs immediate pre-execution validation based on fresh runtime Snapshots.

Example:

DISPATCH\_ROBOT Safety Gate:

    worker\_location\_snapshot fresh?

    robot\_availability\_snapshot fresh?

    zone\_status\_snapshot valid?

    external\_system\_health\_snapshot healthy?

    adapter\_health\_snapshot healthy?

Core principle:

No fresh Snapshot,

no Safety Gate pass.

---

## **28\. Relationship to Ontology Registry**

Snapshot Schema must be grounded in ontology IRIs.

Example:

snapshot\_schema:worker\_location\_snapshot\_v1

    semantic\_iri: ledo:WorkerLocationSnapshotSchema

    applicable\_entity\_type\_refs:

        class:Worker

        class:WorkZone

Ontology provides the meaning of Snapshot fields.

Snapshot Schema Registry provides the operational structure and validation rules.

---

## **29\. Relationship to Model Adapter Registry**

If model output creates or references a Snapshot, schema validation is required.

Example:

vision\_model\_adapter:

    generates hazard detection output

snapshot\_schema\_registry:

    validates hazard\_detection\_snapshot schema

evidence\_registry:

    validates whether it may be promoted to hazard\_detection\_snapshot\_evidence

Model output must not directly become a Safety Gate Snapshot.

Model Output must be validated before becoming Snapshot.

---

## **30\. Relationship to Audit Registry**

Snapshot creation and usage must be auditable.

Audit targets:

snapshot\_schema\_created

snapshot\_schema\_updated

snapshot\_created

snapshot\_validated

snapshot\_rejected

snapshot\_stale\_detected

snapshot\_conflict\_detected

snapshot\_used\_by\_decision

snapshot\_used\_by\_approval

snapshot\_used\_by\_safety\_gate

snapshot\_replayed

Audit Record example:

snapshot\_id: string

snapshot\_schema\_id: string

snapshot\_version: string

created\_by\_identity\_id: string

used\_by\_object\_ref: string

freshness\_status: string

quality\_status: string

trace\_id: string

timestamp: datetime

Core principle:

No Snapshot use without trace.

---

## **31\. Versioning and Migration**

Snapshot Schema must be versioned.

A version change is required when any of the following changes:

1. Required fields change  
2. Optional fields change  
3. Payload schema changes  
4. Metadata schema changes  
5. Freshness requirement changes  
6. Serialization format changes  
7. Arrow schema changes  
8. Native layout changes  
9. Shared memory layout changes  
10. `safety_gate_usable` changes  
11. `hot_path_allowed` changes  
12. Stale policy changes  
13. Conflict policy changes  
14. Sensitivity / PII classification changes  
15. Decision / approval / execution / safety boundaries change

Status values:

draft

active

deprecated

migration\_required

retired

blocked

---

## **32\. Implementation Use**

`snapshot_schema_registry` is used to generate or validate:

1. `SnapshotType` enum  
2. `SnapshotCategory` enum  
3. `SnapshotSchemaStatus` enum  
4. Snapshot metadata DTO  
5. Snapshot payload schema lookup  
6. Snapshot freshness validation  
7. Snapshot immutability validation  
8. Snapshot lineage validation  
9. Snapshot provenance validation  
10. Snapshot conflict handling  
11. Snapshot stale handling  
12. Arrow schema lookup  
13. Native layout lookup  
14. Shared memory layout lookup  
15. Safety Gate hot path eligibility validation  
16. Evidence snapshot binding  
17. Decision snapshot requirement lookup  
18. Runtime validation snapshot lookup  
19. Audit log expectation  
20. Test case generation  
21. Migration rules

Implementation must not use unregistered Snapshot Schemas in the runtime lifecycle.

---

## **33\. Recommended Code Structure**

registries/

    snapshot\_schema\_registry/

        snapshot\_schema\_registry.py

        snapshot\_schema\_entry.py

        snapshot\_type.py

        snapshot\_category.py

        snapshot\_schema\_status.py

        freshness\_requirement.py

        snapshot\_metadata.py

        serialization\_format.py

        native\_layout\_ref.py

        arrow\_schema\_ref.py

        snapshot\_validation.py

        snapshot\_errors.py

        snapshot\_loader.py

        snapshot\_migration.py

    event\_registry/

    evidence\_registry/

    ontology\_registry/

    policy\_registry/

    decision\_registry/

    approval\_registry/

    runtime\_validation\_registry/

    safety\_gate\_registry/

    audit\_event\_registry/

---

## **34\. Minimal Pydantic Model**

from enum import Enum

from pydantic import BaseModel, Field

from typing import Optional

from datetime import datetime

class SnapshotSchemaStatus(str, Enum):

    DRAFT \= "draft"

    ACTIVE \= "active"

    DEPRECATED \= "deprecated"

    MIGRATION\_REQUIRED \= "migration\_required"

    RETIRED \= "retired"

    BLOCKED \= "blocked"

class SnapshotCategory(str, Enum):

    WORLD\_STATE\_SNAPSHOT \= "world\_state\_snapshot"

    ENTITY\_STATE\_SNAPSHOT \= "entity\_state\_snapshot"

    WORKER\_STATE\_SNAPSHOT \= "worker\_state\_snapshot"

    ZONE\_STATE\_SNAPSHOT \= "zone\_state\_snapshot"

    ROBOT\_STATE\_SNAPSHOT \= "robot\_state\_snapshot"

    EQUIPMENT\_STATE\_SNAPSHOT \= "equipment\_state\_snapshot"

    HAZARD\_STATE\_SNAPSHOT \= "hazard\_state\_snapshot"

    EXTERNAL\_SYSTEM\_STATE\_SNAPSHOT \= "external\_system\_state\_snapshot"

    ADAPTER\_STATE\_SNAPSHOT \= "adapter\_state\_snapshot"

    RUNTIME\_VALIDATION\_SNAPSHOT \= "runtime\_validation\_snapshot"

    SAFETY\_GATE\_SNAPSHOT \= "safety\_gate\_snapshot"

    EVIDENCE\_SUPPORT\_SNAPSHOT \= "evidence\_support\_snapshot"

    AUDIT\_REPLAY\_SNAPSHOT \= "audit\_replay\_snapshot"

class SerializationFormat(str, Enum):

    JSON \= "json"

    PROTOBUF \= "protobuf"

    ARROW \= "arrow"

    NATIVE\_FIXED\_LAYOUT \= "native\_fixed\_layout"

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

class SnapshotSchemaRegistryEntry(BaseModel):

    snapshot\_schema\_id: str

    canonical\_name: str

    display\_name: str

    description: str

    semantic\_iri: str

    snapshot\_type: str

    snapshot\_category: SnapshotCategory

    version: str

    status: SnapshotSchemaStatus \= SnapshotSchemaStatus.DRAFT

    applicable\_entity\_type\_refs: list\[str\] \= Field(default\_factory=list)

    applicable\_event\_type\_refs: list\[str\] \= Field(default\_factory=list)

    applicable\_evidence\_type\_refs: list\[str\] \= Field(default\_factory=list)

    applicable\_decision\_rule\_refs: list\[str\] \= Field(default\_factory=list)

    applicable\_safety\_gate\_refs: list\[str\] \= Field(default\_factory=list)

    source\_world\_state\_refs: list\[str\] \= Field(default\_factory=list)

    source\_event\_refs: list\[str\] \= Field(default\_factory=list)

    source\_external\_system\_refs: list\[str\] \= Field(default\_factory=list)

    payload\_schema\_ref: str

    metadata\_schema\_ref: str

    required\_fields: list\[str\] \= Field(default\_factory=list)

    optional\_fields: list\[str\] \= Field(default\_factory=list)

    freshness\_requirement: FreshnessRequirement

    immutability\_required: bool \= True

    lineage\_required: bool \= True

    provenance\_required: bool \= True

    serialization\_formats: list\[SerializationFormat\] \= Field(default\_factory=list)

    arrow\_schema\_ref: Optional\[str\] \= None

    native\_layout\_ref: Optional\[str\] \= None

    shared\_memory\_layout\_ref: Optional\[str\] \= None

    runtime\_usable: bool \= True

    safety\_gate\_usable: bool \= False

    hot\_path\_allowed: bool \= False

    cache\_policy\_ref: Optional\[str\] \= None

    retention\_policy\_ref: str

    conflict\_policy\_ref: str

    stale\_policy\_ref: str

    sensitivity\_level: SensitivityLevel

    pii\_classification: PIIClassification \= PIIClassification.NONE

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

    replacement\_snapshot\_schema\_id: Optional\[str\] \= None

---

## **35\. Core Validation Function**

from datetime import datetime, timezone

def validate\_snapshot\_for\_runtime\_use(

    entry: SnapshotSchemaRegistryEntry,

    snapshot\_payload: dict,

    observed\_at: datetime,

    require\_safety\_gate\_usable: bool \= False,

    require\_hot\_path\_allowed: bool \= False,

) \-\> None:

    if entry.status \!= SnapshotSchemaStatus.ACTIVE:

        raise InvalidSnapshotSchemaError(

            f"Snapshot Schema is not active: {entry.snapshot\_schema\_id}"

        )

    missing\_fields \= \[

        field for field in entry.required\_fields

        if field not in snapshot\_payload

    \]

    if missing\_fields:

        raise SnapshotRequiredFieldMissingError(

            f"Missing required fields: {missing\_fields}"

        )

    now \= datetime.now(timezone.utc)

    age\_seconds \= (now \- observed\_at).total\_seconds()

    if age\_seconds \> entry.freshness\_requirement.max\_age\_seconds:

        raise SnapshotStaleError(

            f"Snapshot is stale. age={age\_seconds}s, "

            f"max={entry.freshness\_requirement.max\_age\_seconds}s"

        )

    if require\_safety\_gate\_usable and not entry.safety\_gate\_usable:

        raise SnapshotNotAllowedForSafetyGateError(

            f"Snapshot Schema is not allowed for Safety Gate: "

            f"{entry.snapshot\_schema\_id}"

        )

    if require\_hot\_path\_allowed and not entry.hot\_path\_allowed:

        raise SnapshotNotAllowedForHotPathError(

            f"Snapshot Schema is not allowed for hot path: "

            f"{entry.snapshot\_schema\_id}"

        )

    if require\_hot\_path\_allowed:

        if not entry.native\_layout\_ref:

            raise SnapshotNativeLayoutMissingError(

                "native\_layout\_ref is required for hot path snapshot"

            )

    if entry.immutability\_required is False:

        raise InvalidSnapshotSchemaError(

            "Runtime Snapshot must require immutability"

        )

    if entry.lineage\_required and not entry.source\_world\_state\_refs and not entry.source\_event\_refs:

        raise InvalidSnapshotSchemaError(

            "lineage is required but no source refs are declared"

        )

    if not entry.stale\_policy\_ref:

        raise InvalidSnapshotSchemaError(

            "stale\_policy\_ref must be declared"

        )

    if not entry.conflict\_policy\_ref:

        raise InvalidSnapshotSchemaError(

            "conflict\_policy\_ref must be declared"

        )

---

## **36\. Test Scenarios**

Required tests:

1\. Reject unregistered Snapshot Schema.

2\. Reject inactive Snapshot Schema.

3\. Reject runtime use of deprecated Snapshot Schema.

4\. Reject blocked Snapshot Schema.

5\. Reject missing required fields.

6\. Reject payload schema mismatch.

7\. Reject metadata schema mismatch.

8\. Reject Snapshot that exceeds freshness requirement.

9\. Reject Snapshot missing observed\_at.

10\. Reject missing immutability requirement.

11\. Reject missing lineage.

12\. Reject missing provenance.

13\. Reject Safety Gate use when safety\_gate\_usable is false.

14\. Reject hot path use without native\_layout\_ref.

15\. Reject missing stale policy.

16\. Reject missing conflict policy.

17\. Reject missing PII classification.

18\. Verify block or review handling when Snapshot conflict occurs.

19\. Reject reuse of Approval-time Snapshot as Execution-time Snapshot.

20\. Verify Snapshot audit trace creation.

21\. Verify Snapshot migration rules.

22\. Verify Arrow schema and native layout version mismatch.

---

## **37\. Final Rule**

No registered Snapshot Schema,

no valid Snapshot.

No valid Snapshot,

no trustworthy Evidence.

No fresh Snapshot,

no Safety Gate pass.

Snapshot is not Event.

Snapshot is not Evidence itself.

Snapshot is not Approval.

Snapshot is not ExecutionRequest.

Snapshot is not PhysicalCommand.

Snapshot freezes state at a specific point in time.

Snapshot Schema defines the operational contract of that state structure.

`snapshot_schema_registry` is the core deterministic registry that governs how LEDO freezes and validates World State, Worker State, Robot State, Zone State, External System State, Adapter State, and Safety Gate Runtime State at a specific point in time.

This module prevents stale, conflicting, or unvalidated Snapshots from being used in Decision, Approval, Safety Gate, and Execution flows.

The core definition is:

Snapshot Schema Registry

\= not a simple list of JSON schemas,

but an operational contract registry that controls

the type, payload schema, metadata schema, freshness,

immutability, lineage, serialization, Arrow schema,

native layout, shared memory layout, hot path eligibility,

stale/conflict policy, and audit rule

of every runtime Snapshot used in LEDO.

