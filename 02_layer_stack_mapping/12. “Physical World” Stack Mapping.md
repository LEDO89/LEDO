# **Ontology Centric “Physical World” Stack Mapping**

## **Layer 12\. Physical World Layer**

─ Core Position  
└── Physical World Layer is the real construction site and operational reality represented by the ontology-centric system  
└── It includes workers, supervisors, robots, machines, equipment, sensors, zones, materials, buildings, and external control systems  
└── It provides real-world data, feedback, execution status, operational events, failures, and recovery states to the ontology system  
└── It receives high-level execution requests, decision context, alerts, notifications, and approved operational intent from the ontology system  
└── It is not a software-only layer  
└── It is the actual physical environment where safety, execution, risk, and feedback occur  
└── Low-level control remains with specialized physical control systems

---

## **Core Role**

└── Represent the actual construction site and all real-world operational entities  
└── Provide live data from workers, robots, equipment, sensors, cameras, LiDAR, PLCs, SCADA, and fleet managers  
└── Execute physical behavior through specialized control systems  
└── Return feedback, status, telemetry, errors, failure events, and recovery states to the ontology system  
└── Allow the ontology system to maintain a live semantic representation of the field  
└── Provide the real-world grounding for world state, risk detection, decision cases, approved actions, execution requests, and audit records  
└── Preserve the boundary between semantic control and physical control

---

## **Physical Entity Stack**

└── Workers  
└── Supervisors  
└── Safety Managers  
└── Humanoid Robots  
└── AMR  
└── AGV  
└── Drones  
└── Excavators  
└── Cranes  
└── Heavy Equipment  
└── IoT Sensors  
└── Cameras  
└── LiDAR  
└── PLC  
└── SCADA  
└── Fleet Manager  
└── Robot Middleware  
└── Equipment Controller  
└── Construction Site  
└── Materials  
└── Resources  
└── Zones  
└── Buildings  
└── Temporary Structures  
└── Scaffolding  
└── Work Areas  
└── Restricted Areas  
└── Emergency Routes  
└── Storage Areas  
└── Loading Areas

---

## **Human Entity Stack**

└── Worker  
└── Supervisor  
└── Safety Manager  
└── Site Manager  
└── Equipment Operator  
└── Crane Operator  
└── Inspector  
└── Emergency Responder  
└── Subcontractor  
└── Visitor  
└── Auditor

Human Data Shared with Ontology System:  
└── location  
└── role  
└── certification status  
└── assigned task  
└── current zone  
└── risk exposure  
└── availability  
└── safety status  
└── notification acknowledgment  
└── emergency status  
└── incident involvement  
└── work permission status

Human Boundary:  
└── Human safety has the highest priority  
└── Worker data must be protected by privacy, access control, and audit policy  
└── The ontology system must assist human decision-making but not remove human authority from high-risk approvals where policy requires human approval

---

## **Robot Entity Stack**

└── Humanoid Robot  
└── AMR  
└── AGV  
└── Drone  
└── Inspection Robot  
└── Delivery Robot  
└── Monitoring Robot  
└── Robot Controller  
└── Robot Middleware  
└── Fleet Manager  
└── Behavior Tree Runtime  
└── Mission Controller

Robot Data Shared with Ontology System:  
└── robot location  
└── robot status  
└── mode  
└── availability  
└── battery state  
└── capability  
└── assigned task  
└── mission status  
└── route status  
└── error code  
└── heartbeat  
└── telemetry  
└── execution status  
└── failure event  
└── recovery status

Robot Boundary:  
└── Ontology system may send high-level approved execution requests  
└── Robot middleware, fleet managers, behavior trees, and robot controllers handle detailed robot execution  
└── Low-level motion control, collision avoidance, joint control, navigation, and behavior execution remain outside the ontology system

---

## **Equipment Entity Stack**

└── Excavator  
└── Crane  
└── Forklift  
└── Loader  
└── Concrete Pump  
└── Tower Crane  
└── Hoist  
└── Generator  
└── Compressor  
└── Welding Machine  
└── Lift  
└── Temporary Power System  
└── Equipment Controller  
└── PLC-controlled Equipment

Equipment Data Shared with Ontology System:  
└── location  
└── status  
└── operating mode  
└── availability  
└── active / inactive state  
└── load state  
└── maintenance state  
└── fault state  
└── error code  
└── sensor readings  
└── heartbeat  
└── equipment telemetry  
└── safety interlock state  
└── execution feedback  
└── failure event

Equipment Boundary:  
└── Ontology system represents equipment meaning, state, risk, and approved intent  
└── Equipment controllers and PLC systems execute machine-specific logic  
└── Ontology system must not directly implement machine control sequences

---

## **Sensor Entity Stack**

└── IoT Sensor  
└── Environmental Sensor  
└── Gas Sensor  
└── Temperature Sensor  
└── Humidity Sensor  
└── Vibration Sensor  
└── Proximity Sensor  
└── Wearable Sensor  
└── Smart Helmet Sensor  
└── Camera  
└── LiDAR  
└── RFID Reader  
└── UWB Tracker  
└── GPS Device  
└── IMU  
└── Edge Gateway

Sensor Data Shared with Ontology System:  
└── sensor value  
└── sensor type  
└── unit  
└── source timestamp  
└── ingestion timestamp  
└── signal quality  
└── confidence score  
└── calibration status  
└── heartbeat  
└── error code  
└── anomaly event  
└── threshold event  
└── detection event  
└── stale state  
└── offline state

Sensor Boundary:  
└── Sensor data is not automatically truth  
└── Sensor data must be normalized, timestamped, confidence-scored, and grounded before becoming world state  
└── Conflicting or stale sensor data must be flagged, blocked, or escalated depending on risk

---

## **Industrial Control Entity Stack**

└── PLC  
└── SCADA  
└── OPC-UA Server  
└── Modbus Device  
└── Industrial Gateway  
└── Equipment Controller  
└── Safety Controller  
└── Interlock Controller  
└── Machine Controller  
└── Alarm System  
└── Site Operation Platform

Industrial Data Shared with Ontology System:  
└── machine state  
└── operating mode  
└── alarm state  
└── interlock state  
└── tag value  
└── PLC signal  
└── SCADA event  
└── command acknowledgment  
└── execution status  
└── failure code  
└── safety stop state  
└── recovery status

Industrial Control Boundary:  
└── PLC logic remains inside PLC systems  
└── SCADA supervision remains inside SCADA systems  
└── Equipment sequence logic remains inside equipment controllers  
└── Ontology system may send approved high-level requests only through controlled adapters  
└── Industrial integrations require strict authentication, authorization, audit, testing, and safety review

---

## **Site Entity Stack**

└── Construction Site  
└── Building  
└── Floor  
└── Zone  
└── Work Area  
└── Restricted Zone  
└── Danger Zone  
└── Loading Zone  
└── Storage Zone  
└── Emergency Route  
└── Evacuation Area  
└── Temporary Structure  
└── Scaffold  
└── Crane Operation Area  
└── Equipment Operation Area  
└── Material Storage Area  
└── Inspection Area

Site Data Shared with Ontology System:  
└── zone status  
└── risk state  
└── access state  
└── active work state  
└── task state  
└── material state  
└── restriction state  
└── emergency route state  
└── environmental condition  
└── occupancy state  
└── schedule update  
└── BIM metadata  
└── inspection status  
└── permit status

Site Boundary:  
└── The physical site changes continuously  
└── The ontology system must maintain a live semantic representation but must not confuse representation with reality  
└── Field feedback must update world state and audit records

---

## **Material & Resource Entity Stack**

└── Material  
└── Resource  
└── Tool  
└── Component  
└── Prefabricated Element  
└── Concrete  
└── Rebar  
└── Formwork  
└── Scaffold Component  
└── Safety Equipment  
└── PPE  
└── Temporary Facility  
└── Storage Resource  
└── Energy Resource  
└── Fuel Resource

Material / Resource Data Shared with Ontology System:  
└── location  
└── quantity  
└── availability  
└── condition  
└── storage state  
└── delivery status  
└── usage status  
└── quality status  
└── inspection status  
└── risk state  
└── assigned task  
└── resource conflict

---

## **Data Shared with the Ontology System**

└── Location  
└── Status  
└── Mode  
└── Availability  
└── Capability  
└── Risk State  
└── Task State  
└── Error Code  
└── Heartbeat  
└── Telemetry  
└── Sensor Value  
└── Execution Status  
└── Failure Event  
└── Recovery Status  
└── Acknowledgment  
└── Warning Event  
└── Alarm Event  
└── Maintenance State  
└── Inspection State  
└── Permit State  
└── Worker Presence  
└── Zone Occupancy  
└── Environmental Condition  
└── Equipment Operation State  
└── Robot Mission State  
└── External System Health

Data Rule:  
└── Physical world data must include source, timestamp, identity, confidence, and freshness where relevant  
└── Data must be normalized before becoming ontology-grounded world state  
└── Missing, stale, conflicting, or low-confidence data must be treated as operationally meaningful

---

## **Data Received from the Ontology System**

└── High-level Execution Request  
└── Approved Action Context  
└── Safety Requirement  
└── Execution Constraint  
└── Target Entity Context  
└── Target Zone Context  
└── Approval State  
└── Decision Context  
└── Risk Context  
└── Expected Feedback Requirement  
└── Audit Context  
└── Notification Request  
└── Inspection Request  
└── Work Stop Request  
└── Work Resume Request  
└── Evacuation Request  
└── Robot Mission Request  
└── Equipment Status Request  
└── Site Operation Request

Request Rule:  
└── Ontology system sends high-level approved intent  
└── External control systems translate intent into detailed physical execution  
└── Physical systems must return feedback, status, acknowledgment, failure, or completion result

---

## **Control Boundary**

└── Physical world and external control systems provide data, feedback, execution status, and operational events to the ontology system  
└── Ontology system provides high-level execution requests and decision context  
└── Low-level control remains with specialized control systems  
└── Robot motion remains with robot controllers and robot middleware  
└── Fleet scheduling remains with fleet managers  
└── PLC logic remains with PLC systems  
└── SCADA supervision remains with SCADA systems  
└── Equipment sequences remain with equipment controllers  
└── Collision avoidance remains with robot / fleet / equipment safety systems  
└── Worker physical action remains with humans and field procedures

Control Rule:  
└── Ontology controls meaning, constraints, approval, and decision context  
└── Specialized systems control physical execution  
└── Physical feedback closes the loop

---

## **Feedback Loop Stack**

└── Physical Event Occurs  
└── Sensor / System Detects Event  
└── Event Data Sent to Ontology System  
└── Real-Time World State Updated  
└── Agent or Rule Detects Situation  
└── ActionCandidate Created  
└── Decision Router Classifies Risk  
└── Safety Gate Validates ApprovedAction  
└── Unified Core Creates ExecutionRequest  
└── External Integration Sends Request  
└── External System Executes Detailed Behavior  
└── Physical World Changes  
└── Feedback Returned  
└── World State Updated  
└── Audit Record Stored  
└── UI / Digital Twin Synchronized

Feedback Rule:  
└── The loop is not complete when a request is sent  
└── The loop is complete only when physical feedback, state update, and audit record are resolved

---

## **Physical Feedback Types**

└── Acknowledgment  
└── Accepted  
└── Rejected  
└── Started  
└── In Progress  
└── Completed  
└── Failed  
└── Timeout  
└── Cancelled  
└── Blocked  
└── Unsafe State Detected  
└── Recovery Required  
└── Recovery Started  
└── Recovery Completed  
└── Manual Override Required  
└── Manual Override Completed  
└── Sensor Offline  
└── External System Offline  
└── Equipment Fault  
└── Robot Fault  
└── Worker Acknowledged  
└── Zone Cleared  
└── Zone Not Cleared

---

## **Physical Risk State Stack**

└── Human Safety Risk  
└── Fall Risk  
└── Collision Risk  
└── Crushing Risk  
└── Electrical Risk  
└── Gas / Chemical Risk  
└── Fire Risk  
└── Structural Risk  
└── Equipment Failure Risk  
└── Robot Operation Risk  
└── Crane Operation Risk  
└── Restricted Zone Risk  
└── Environmental Risk  
└── Emergency Route Blockage Risk  
└── Communication Failure Risk  
└── Sensor Failure Risk

Risk Rule:  
└── Physical risk must be represented as live state, evidence, and events  
└── Human safety risk dominates all other operational priorities  
└── Unknown or unobservable risk may itself require warning, escalation, or work restriction

---

## **Physical Execution Examples**

└── ACTION\_STOP\_WORK  
└── Site operation platform updates work stop status  
└── Supervisors and workers receive notification  
└── Zone or task state changes  
└── Feedback confirms work stopped or not confirmed

└── ACTION\_EVACUATE  
└── Worker alert system notifies workers  
└── Smart helmets or mobile devices receive evacuation alert  
└── Site alarm may activate  
└── Worker location feedback confirms evacuation progress

└── ACTION\_LOCK\_ZONE  
└── Site operation system marks zone restricted  
└── Access control system may update zone access  
└── Digital twin and UI show locked zone  
└── Sensors confirm worker presence or clearance

└── ACTION\_NOTIFY\_MANAGER  
└── Supervisor notification delivered  
└── Acknowledgment tracked  
└── No physical machine execution required

└── ACTION\_DISPATCH\_ROBOT  
└── Fleet manager receives mission request  
└── Fleet manager assigns robot  
└── Robot middleware executes mission  
└── Robot telemetry and mission status return as feedback

└── ACTION\_REPLAN\_ROUTE  
└── Fleet manager or planning system replans route  
└── Restricted zones and risk zones are considered  
└── New route status returned

└── ACTION\_RESUME\_WORK  
└── Safety clearance and inspection result confirmed  
└── Site operation platform updates work state  
└── Workers and supervisors receive notification

└── ACTION\_REQUEST\_INSPECTION  
└── Inspection workflow is created  
└── Inspector or inspection robot receives request  
└── Inspection result returns as evidence

└── ACTION\_EMERGENCY\_STOP  
└── Emergency stop path follows predefined external safety system  
└── PLC / controller / robot system handles stop behavior  
└── Post-execution feedback and audit are required

---

## **External Control System Stack**

└── Fleet Manager  
└── Robot Middleware  
└── Robot Controller  
└── Behavior Tree Runtime  
└── PLC  
└── SCADA  
└── Equipment Controller  
└── Site Operation Platform  
└── Smart Helmet Alert System  
└── Worker Notification System  
└── Access Control System  
└── Alarm System  
└── Inspection System  
└── Permit System  
└── Maintenance System

External Control Rule:  
└── Each external system owns its specialized execution domain  
└── Ontology system must integrate through approved adapters  
└── External control systems must provide feedback for execution traceability

---

## **Physical World Data Quality Stack**

└── Source Identity  
└── Source Reliability  
└── Timestamp Accuracy  
└── Signal Quality  
└── Calibration Status  
└── Network Availability  
└── Heartbeat Status  
└── Sensor Freshness  
└── Device Health  
└── State Confidence  
└── Conflicting Source Detection  
└── Missing Data Detection  
└── Manual Confirmation  
└── Field Verification

Data Quality Rule:  
└── Bad physical data can cause bad cyber decisions  
└── The system must track whether physical data is fresh, reliable, complete, and consistent  
└── Low-quality physical data must reduce confidence or trigger review

---

## **Physical Safety Boundary Stack**

└── Human Safety Boundary  
└── Robot Safety Boundary  
└── Equipment Safety Boundary  
└── Industrial Safety Boundary  
└── Emergency Stop Boundary  
└── Manual Override Boundary  
└── Local Safety Interlock  
└── External Safety Controller  
└── Field Supervisor Authority  
└── Emergency Authority  
└── Physical Exclusion Zone  
└── Lockout / Tagout Procedure  
└── Permit-to-work Procedure

Safety Boundary Rule:  
└── Physical safety systems must not depend solely on the ontology system  
└── Local safety interlocks and emergency stop mechanisms must remain functional independently  
└── Ontology system supports decision and coordination but must not be the only safety mechanism

---

## **Runtime Boundary**

└── Physical World Layer is always active because reality continues even when software is offline  
└── It provides data and feedback to the ontology system  
└── It receives high-level approved requests from the ontology system through external control systems  
└── It does not guarantee that requested physical actions always succeed  
└── It may produce uncertainty, delay, failure, conflict, noise, and incomplete feedback  
└── The ontology system must handle physical uncertainty safely  
└── Field humans and local safety systems remain essential

---

## **Not Responsible For**

└── Defining ontology meaning  
└── Acting as API Gateway  
└── Acting as semantic memory store  
└── Acting as decision router  
└── Acting as safety gate  
└── Acting as unified cyber-physical lifecycle manager  
└── Guaranteeing clean data  
└── Guaranteeing perfect feedback  
└── Guaranteeing physical rollback  
└── Guaranteeing that all commands succeed  
└── Replacing human field judgment  
└── Replacing local emergency stop systems  
└── Replacing equipment safety systems  
└── Replacing robot safety controllers  
└── Replacing industrial safety interlocks

---

## **Recommended MVP Stack Mapping**

└── Physical Entities: workers, zones, equipment, sensors, simple robot or mock robot  
└── Sensor Input: MQTT-based IoT sensor events  
└── Worker Location: manual input first, then UWB / GPS / BLE / smart helmet later  
└── Equipment Status: mock status first, then equipment API / OPC-UA later  
└── Robot Integration: mock fleet manager first, ROS2 bridge later  
└── Notification System: mobile / web notification first, smart helmet later  
└── Site Model: zone map \+ BIM metadata reference first  
└── Feedback: acknowledgment, status, failure, completion DTOs  
└── Safety Boundary: manual supervisor confirmation \+ local emergency procedures first  
└── Audit: all physical feedback linked to execution lifecycle  
└── Digital Twin: display world state, not physical source of truth

MVP Rule:  
└── Start with simulated or mock physical systems  
└── Then connect simple sensors and notification systems  
└── Then connect one robot / fleet manager integration  
└── Then connect equipment and industrial control systems only after strict testing  
└── Do not connect directly to dangerous machinery in early MVP  
└── Always preserve human override and local safety mechanisms

---

## **Physical World Core Principles**

1. Reality Is the Final Ground  
   └── The ontology system represents the physical world, but the physical world is the real operational environment.  
2. Representation Is Not Reality  
   └── A digital state may be stale, wrong, delayed, or incomplete; physical feedback must continuously correct it.  
3. Physical Data Must Be Treated as Evidence  
   └── Location, status, telemetry, heartbeat, and sensor values must include source, timestamp, and confidence.  
4. Low-level Control Stays with Specialized Systems  
   └── Robot controllers, PLCs, SCADA, fleet managers, and equipment controllers own detailed control.  
5. Ontology System Sends Approved Intent  
   └── It provides high-level execution requests, constraints, approval state, and decision context.  
6. External Systems Perform Detailed Execution  
   └── Fleet managers schedule robots, PLCs execute machine logic, robot controllers handle motion, and equipment controllers execute machine behavior.  
7. Feedback Closes the Loop  
   └── Execution is not complete until physical feedback updates world state, audit, and lifecycle state.  
8. Dispatch Is Not Completion  
   └── Sending a request does not mean the physical task succeeded.  
9. Human Safety Is Highest Priority  
   └── All physical execution must preserve human safety above productivity, robot efficiency, or equipment protection.  
10. Physical Systems Can Fail  
    └── Robots, sensors, equipment, networks, and workers may fail to respond; the ontology system must handle this safely.  
11. Missing Data Is Operationally Important  
    └── Sensor offline, heartbeat lost, or missing feedback must be treated as meaningful state.  
12. Local Safety Must Remain Independent  
    └── Emergency stops, safety interlocks, lockout / tagout, and field procedures must not depend only on central ontology software.  
13. Human Override Must Remain Possible  
    └── Field supervisors and emergency authorities must be able to intervene according to policy and safety procedure.  
14. Physical Rollback Is Impossible  
    └── The system can only recover forward through safe-state transition, compensation, manual override, or recovery workflow.  
15. Industrial Control Requires Strong Boundaries  
    └── PLC / SCADA / equipment integrations must be restricted, tested, audited, and permission-controlled.  
16. Robots Are Operational Nodes, Not Magic Agents  
    └── Robots must be modeled with state, capability, availability, mode, task, risk, and feedback.  
17. Workers Are Safety-critical Nodes  
    └── Worker location, certification, task, risk exposure, and notification acknowledgment are critical state.  
18. Zones Are Operational Control Units  
    └── Risk, access, task, evacuation, lock, and restriction states should be represented at zone level.  
19. Physical Feedback Must Be Normalized  
    └── External systems return different formats; the ontology system must normalize them into common feedback events.  
20. Physical World Layer Completes the Architecture  
    └── All upper layers exist to understand, govern, approve, request, observe, and learn from this physical reality.

