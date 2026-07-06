# **Ontology Centric “Execution Request & External Control Integration” Stack Mapping**

## **Layer 11\. Execution Request & External Control Integration Layer**

─ Core Position  
└── Execution Request & External Control Integration Layer is the external control integration boundary of the ontology-centric system  
└── It converts approved ontology actions and execution requests into high-level requests for external control systems  
└── It connects the ontology-centric core to fleet managers, robot middleware, PLC / SCADA systems, equipment controllers, smart helmets, site operation platforms, and other external systems  
└── It does not directly control low-level robot motion  
└── It does not perform fleet scheduling internally  
└── It does not implement PLC logic  
└── It does not implement machine sequences  
└── It does not perform collision avoidance directly  
└── It does not replace robot controllers, fleet managers, behavior trees, PLCs, SCADA, or equipment controllers  
└── It translates approved execution intent into controlled, auditable, external system requests

---

## **Core Role**

└── Receive ExecutionRequest from Unified Cyber-Physical Core  
└── Resolve the correct external control system or operation platform  
└── Select the correct adapter for fleet manager, robot middleware, PLC / SCADA, equipment controller, notification system, or site operation platform  
└── Convert ontology-defined execution intent into external system request format  
└── Preserve constraints, approval state, safety requirements, audit context, trace ID, idempotency key, and expected feedback  
└── Dispatch high-level execution requests to external systems  
└── Receive acknowledgment, status, failure, and feedback from external systems  
└── Normalize external feedback into FeedbackEvent and ExecutionResult  
└── Send feedback back to Unified Cyber-Physical Core and Real-Time World State Layer  
└── Maintain integration reliability, protocol boundaries, error handling, retries, timeouts, and adapter observability

---

## **Core Technologies**

└── Execution Request Builder  
└── Workflow Engine  
└── Task Dispatcher  
└── Fleet Manager Adapter  
└── Robot Middleware Adapter  
└── ROS2 Bridge  
└── MQTT Adapter  
└── OPC-UA Adapter  
└── PLC Adapter  
└── Modbus Adapter  
└── REST Adapter  
└── WebSocket Adapter  
└── gRPC Hub  
└── Kafka Hub  
└── SCADA Connector  
└── External System Connector  
└── Behavior Tree Runtime Interface  
└── Mission Request Adapter  
└── Adapter Registry  
└── Protocol Gateway  
└── Feedback Normalizer  
└── External System Health Monitor

---

## **Optional Technologies**

└── ROS2 Action Server / Client  
└── ROS2 Services  
└── DDS Bridge  
└── OPC-UA PubSub  
└── Sparkplug B over MQTT  
└── Industrial Edge Gateway  
└── Edge Agent Connector  
└── RTPS / DDS integration  
└── ONVIF camera control integration  
└── ISA-95 / ISA-88 mapping optional  
└── Digital Twin Connector  
└── BIM Platform Connector  
└── ERP / CMMS Connector  
└── Webhook Adapter  
└── External API Gateway  
└── Adapter Sandbox  
└── Integration Test Harness  
└── Hardware-in-the-loop Test Environment

---

## **Integration Boundary**

└── Ontology system defines execution intent  
└── Ontology system defines constraints  
└── Ontology system defines approval state  
└── Ontology system defines target entities  
└── Ontology system defines safety requirements  
└── Ontology system defines expected feedback  
└── Ontology system preserves audit context

External systems execute detailed behavior:  
└── Fleet Manager handles fleet scheduling and robot assignment  
└── Robot Middleware handles robot communication and robot-level execution  
└── Robot Controller handles motion control, behavior execution, and local safety  
└── Behavior Tree Runtime handles robot task logic when applicable  
└── PLC handles machine logic  
└── SCADA handles industrial supervision and plant-level control  
└── Equipment Controller handles machine-specific sequences  
└── Smart Helmet / Notification System handles worker alerts  
└── Site Operation Platform handles operational task execution

Boundary Rule:  
└── The ontology system requests approved intent  
└── External control systems perform specialized execution  
└── Feedback returns to ontology system for state update, audit, and decision continuity

---

## **Input Stack**

└── ExecutionRequest  
└── ApprovedAction Reference  
└── DecisionCase Reference  
└── Action Type  
└── Target Node  
└── Target Zone  
└── Target External System  
└── Execution Constraints  
└── Safety Conditions  
└── Approval Context  
└── Evidence References  
└── Expected Feedback Contract  
└── Timeout Policy  
└── Retry Policy  
└── Recovery Policy  
└── Idempotency Key  
└── Trace Context  
└── Correlation ID

Input Rule:  
└── This layer receives only structured ExecutionRequest objects from Unified Cyber-Physical Core  
└── ActionCandidate or unapproved user command must not enter this layer directly  
└── Every request must include trace ID, idempotency key, target, constraints, and expected feedback

---

## **Output Stack**

└── ExternalControlRequest  
└── AdapterRequest  
└── MissionRequest  
└── TaskDispatchRequest  
└── RobotTaskRequest  
└── FleetManagerRequest  
└── PLCRequest  
└── SCADARequest  
└── EquipmentControlRequest  
└── NotificationRequest  
└── ExternalAcknowledgment  
└── ExternalFeedback  
└── FeedbackEvent  
└── ExecutionResult  
└── AdapterError  
└── RecoveryRequiredSignal

Output Rule:  
└── External requests are high-level requests, not uncontrolled low-level commands  
└── External feedback must be normalized before returning to Unified Cyber-Physical Core  
└── Dispatch success does not equal execution completion

---

## **Execution Request Builder Stack**

└── ExecutionRequest Parser  
└── Action Type Mapper  
└── Target Mapper  
└── Constraint Mapper  
└── Safety Requirement Mapper  
└── Approval Context Mapper  
└── Expected Feedback Mapper  
└── External System Selector  
└── Adapter Selector  
└── Request Payload Builder  
└── Idempotency Key Injector  
└── Trace Context Injector  
└── Timeout Policy Injector  
└── Retry Policy Injector

Builder Rule:  
└── Execution Request Builder converts ontology-level approved intent into external-system-level request structure  
└── It must not remove safety constraints, approval context, trace context, or expected feedback requirements

---

## **Task Dispatcher Stack**

└── Dispatch Queue  
└── Adapter Dispatch  
└── Priority Dispatch  
└── Retry Dispatch  
└── Timeout Tracking  
└── Dispatch Acknowledgment  
└── External System Availability Check  
└── External System Health Check  
└── Load-aware Dispatch optional  
└── Dead Letter Queue  
└── Dispatch Audit Record

Dispatch Rule:  
└── Dispatch must be idempotent  
└── Dispatch must be traceable  
└── Dispatch failure must return structured failure status  
└── Retry must not duplicate physical execution

---

## **Adapter Registry Stack**

└── Adapter ID  
└── Adapter Type  
└── External System ID  
└── Supported Action Types  
└── Supported Target Types  
└── Protocol Type  
└── Endpoint Configuration  
└── Authentication Method  
└── Capability Declaration  
└── Health Status  
└── Version  
└── Owner  
└── Site Scope  
└── Permission Scope  
└── Last Heartbeat  
└── Failure Rate

Adapter Registry Rule:  
└── Only registered adapters may receive execution requests  
└── Adapter capabilities must match the ExecutionRequest action type and target  
└── Adapter version and health status must be checked before dispatch when required

---

## **Fleet Manager Adapter Stack**

└── Fleet Manager API Client  
└── Mission Request Adapter  
└── Robot Assignment Request  
└── Task Dispatch Request  
└── Route Request  
└── Route Replan Request  
└── Robot Availability Query  
└── Fleet Status Query  
└── Mission Status Query  
└── Fleet Feedback Normalizer  
└── Fleet Error Mapper  
└── Fleet Acknowledgment Handler

Usage:  
└── Dispatch robot mission requests  
└── Request route replanning  
└── Request robot task assignment  
└── Query fleet availability  
└── Receive mission execution status

Boundary:  
└── Fleet manager performs robot assignment, scheduling, and fleet coordination  
└── Ontology system does not implement fleet scheduling internally

---

## **Robot Middleware Adapter Stack**

└── ROS2 Bridge  
└── Robot Middleware API  
└── ROS2 Topic Interface  
└── ROS2 Service Interface  
└── ROS2 Action Interface  
└── Robot Task Request  
└── Robot Status Request  
└── Robot Feedback Listener  
└── Robot Error Mapper  
└── Robot State Feedback Normalizer

Usage:  
└── Send high-level robot task requests  
└── Receive robot status and task feedback  
└── Bridge approved mission requests to robot middleware

Boundary:  
└── Robot middleware controls robot communication and execution flow  
└── Robot controller handles low-level motion and behavior  
└── Ontology system must not directly drive motors or motion loops

---

## **Behavior Tree Runtime Interface Stack**

└── Behavior Tree Task Request  
└── Behavior Tree ID  
└── Behavior Tree Parameters  
└── Precondition Context  
└── Safety Constraint Context  
└── Start Request  
└── Pause Request  
└── Cancel Request  
└── Status Query  
└── Node Status Feedback  
└── Behavior Failure Feedback  
└── Behavior Completion Feedback

Usage:  
└── Request execution of predefined behavior trees  
└── Pass approved constraints and target context  
└── Receive structured task status feedback

Boundary:  
└── Ontology system may request a predefined behavior tree mission  
└── Behavior tree runtime owns detailed execution logic  
└── Ontology system must not dynamically invent low-level behavior tree logic without validation and governance

---

## **PLC / SCADA Adapter Stack**

└── OPC-UA Adapter  
└── PLC Adapter  
└── Modbus Adapter  
└── SCADA Connector  
└── Tag Mapping  
└── Command Mapping  
└── Alarm Mapping  
└── Machine State Mapping  
└── Interlock Status Query  
└── Command Permission Check  
└── SCADA Event Feedback  
└── PLC Acknowledgment  
└── Industrial Error Mapper

Usage:  
└── Send approved high-level industrial requests where allowed  
└── Query machine state and interlock status  
└── Receive PLC / SCADA feedback  
└── Update execution result and world state

Boundary:  
└── PLC logic remains inside PLC  
└── SCADA supervision remains inside SCADA  
└── Ontology system does not implement machine sequence control  
└── Industrial command integration must be extremely restricted, permission-controlled, and audited

---

## **Equipment Controller Adapter Stack**

└── Equipment API Client  
└── Equipment Status Query  
└── Equipment Command Request  
└── Equipment Mode Request  
└── Equipment Lockout Request  
└── Maintenance Request  
└── Equipment Health Feedback  
└── Equipment Error Mapper  
└── Equipment Feedback Normalizer

Usage:  
└── Request equipment status  
└── Request approved equipment-related actions  
└── Receive equipment feedback and failure states

Boundary:  
└── Equipment controller owns machine-specific logic  
└── Ontology system sends approved requests and receives feedback

---

## **Notification / Worker Alert Adapter Stack**

└── Smart Helmet Alert Adapter  
└── Mobile Push Adapter  
└── SMS Adapter optional  
└── Email Adapter  
└── Site Alarm Adapter  
└── Speaker / Siren Adapter optional  
└── Worker Notification Request  
└── Supervisor Notification Request  
└── Notification Acknowledgment  
└── Delivery Status Feedback  
└── Escalation on No Acknowledgment

Usage:  
└── Send evacuation alerts  
└── Send restricted zone warnings  
└── Notify supervisors  
└── Notify safety managers  
└── Notify War Room  
└── Confirm alert delivery status

Boundary:  
└── Notification delivery is an external system interaction  
└── Safety-critical notifications require acknowledgment tracking and audit

---

## **Site Operation Platform Adapter Stack**

└── Site Operation API  
└── Work Order Request  
└── Inspection Request  
└── Permit Status Request  
└── Task Update Request  
└── Zone Status Request  
└── Work Stop Request  
└── Work Resume Request  
└── Site Operation Feedback  
└── Work Order Status Feedback

Usage:  
└── Request site-level operational actions  
└── Update construction workflow status  
└── Request inspection or permit review  
└── Synchronize task and execution status

Boundary:  
└── Site operation platform owns its own workflow execution  
└── Ontology system provides approved intent and receives operational feedback

---

## **Protocol Adapter Stack**

└── REST Adapter  
└── WebSocket Adapter  
└── gRPC Adapter  
└── MQTT Adapter  
└── Kafka Adapter  
└── ROS2 Bridge  
└── OPC-UA Adapter  
└── Modbus Adapter  
└── SCADA Connector  
└── Webhook Adapter  
└── File / Batch Integration Adapter optional

Protocol Rule:  
└── Protocol adapters translate communication format  
└── They do not change approved intent  
└── They must preserve trace ID, idempotency, constraints, and expected feedback where possible

---

## **External Control Request Stack**

└── external\_request\_id  
└── execution\_request\_id  
└── approved\_action\_id  
└── adapter\_id  
└── external\_system\_id  
└── action\_type  
└── target\_external\_id  
└── request\_payload  
└── constraints  
└── safety\_requirements  
└── expected\_feedback  
└── timeout\_policy  
└── retry\_policy  
└── idempotency\_key  
└── trace\_id  
└── correlation\_id  
└── created\_at\_utc

ExternalControlRequest Rule:  
└── ExternalControlRequest must be derived from ExecutionRequest  
└── It must not bypass Safety Gate or Unified Core  
└── It must remain auditable and replay-safe

---

## **Feedback Normalization Stack**

└── External Acknowledgment  
└── External Status Update  
└── External Completion Event  
└── External Failure Event  
└── External Error Code  
└── External Timeout  
└── Adapter-specific Payload  
└── Normalized FeedbackEvent  
└── ExecutionResult Mapping  
└── World State Update Mapping  
└── Recovery Signal Mapping  
└── Audit Event Mapping

Feedback Rule:  
└── External systems return different feedback formats  
└── This layer normalizes them into common FeedbackEvent and ExecutionResult structures  
└── Missing or conflicting feedback must trigger timeout, retry, recovery, or manual review

---

## **Error Handling Stack**

└── Adapter Connection Failure  
└── Authentication Failure  
└── Authorization Failure  
└── Target Not Found  
└── External System Unavailable  
└── Timeout  
└── Invalid Payload  
└── Unsupported Action Type  
└── Capability Mismatch  
└── External Rejection  
└── Command Conflict  
└── Feedback Missing  
└── Feedback Conflict  
└── Retry Exhausted  
└── Dead Letter Queue  
└── RecoveryRequired

Error Rule:  
└── Adapter failure must return structured error to Unified Core  
└── Adapter failure must not silently disappear as a log only  
└── High-risk dispatch failure must escalate and trigger recovery evaluation

---

## **Idempotency & Retry Stack**

└── Idempotency Key  
└── External Idempotency Token  
└── Retry Policy  
└── Retry Count  
└── Backoff Strategy  
└── Duplicate Dispatch Detection  
└── Duplicate Feedback Detection  
└── Timeout Policy  
└── Retry-safe Adapter Logic  
└── Dead Letter Queue  
└── Manual Review after Retry Exhaustion

Idempotency Rule:  
└── Network retry must not cause duplicate physical execution  
└── Idempotency key must travel from ExecutionRequest to external adapter when supported  
└── If external system does not support idempotency, adapter must implement duplicate protection as much as possible and escalate uncertainty

---

## **Security Stack**

└── External System Authentication  
└── Service Account  
└── API Key Management  
└── OAuth Client Credentials  
└── mTLS  
└── Certificate Management  
└── Request Signature  
└── Webhook Signature Verification  
└── Adapter Permission Scope  
└── External System Permission Scope  
└── Secret Manager  
└── Credential Rotation  
└── Network Segmentation  
└── Industrial Firewall Boundary  
└── Audit Log

Security Rule:  
└── External system access must be authenticated, authorized, scoped, encrypted, and audited  
└── Credentials must not be stored in code or frontend  
└── Industrial control integrations require stricter boundaries than ordinary REST APIs

---

## **Observability Stack**

└── Adapter Health Status  
└── External System Heartbeat  
└── Dispatch Latency  
└── Acknowledgment Latency  
└── Feedback Latency  
└── Adapter Error Rate  
└── External Timeout Count  
└── Retry Count  
└── Failed Dispatch Count  
└── Unsupported Action Count  
└── Capability Mismatch Count  
└── Feedback Missing Count  
└── External System Availability  
└── Protocol Error Count  
└── Dead Letter Count  
└── Recovery Required Count

Observability Rule:  
└── Every external dispatch and feedback path must be observable  
└── External control integration failure can directly affect physical safety and must be visible

---

## **Execution Request Example Stack**

Example: ACTION\_EVACUATE\_ZONE

└── ApprovedAction  
└── action\_type: ACTION\_EVACUATE  
└── target: Zone\_A  
└── reason: human safety risk  
└── approval: supervisor approval required or emergency policy path  
└── evidence: worker presence, zone risk, sensor evidence

└── ExecutionRequest  
└── target: Zone\_A  
└── constraints: Human safety priority  
└── constraints: Use approved fleet manager  
└── constraints: Avoid restricted zones  
└── constraints: Supervisor approval required  
└── expected\_feedback: report execution status

└── External Systems  
└── Fleet Manager  
└── Robot Middleware  
└── PLC / SCADA  
└── Smart Helmet Alert System  
└── Site Operation Platform

└── Adapter Dispatch  
└── Fleet manager receives mission or evacuation support request  
└── Smart helmet system receives worker evacuation alert  
└── SCADA / PLC receives allowed high-level safety request if applicable  
└── Site operation platform receives zone evacuation status update

└── Feedback  
└── acknowledgment received  
└── notification delivered  
└── fleet mission accepted or rejected  
└── zone evacuation status updated  
└── failed feedback triggers recovery or escalation

---

## **Integration Model Stack**

└── Ontology System  
→ ApprovedAction / ExecutionRequest  
→ External Control Adapter  
→ Fleet Manager / Robot Middleware / PLC / SCADA / Site Platform  
→ Robot / AGV / AMR / Crane / Equipment / Worker Alert System  
→ Feedback / Status / Failure / Completion  
→ Unified Core  
→ Real-Time World State  
→ Audit / UI / Decision Continuity

Integration Rule:  
└── The ontology system provides high-level approved intent  
└── External systems perform specialized execution  
└── Feedback closes the loop

---

## **Runtime Boundary**

└── This layer is active after Unified Cyber-Physical Core creates ExecutionRequest  
└── It performs adapter selection, protocol translation, dispatch, acknowledgment tracking, feedback normalization, and external error mapping  
└── It does not approve action candidates  
└── It does not own command lifecycle state as the source of truth  
└── It does not perform low-level robot or machine control  
└── It must preserve safety constraints, traceability, idempotency, expected feedback, and audit context  
└── It must return all feedback and failure states to Unified Cyber-Physical Core

---

## **Not Responsible For**

└── Generating action candidates  
└── Classifying risk tiers  
└── Performing final Safety Gate validation  
└── Owning the command lifecycle source of truth  
└── Defining ontology meaning  
└── Managing human approval workflow  
└── Running full policy governance  
└── Performing robot motion planning  
└── Performing collision avoidance  
└── Performing fleet scheduling internally  
└── Executing PLC ladder logic  
└── Executing SCADA supervisory logic  
└── Executing machine sequences directly  
└── Running robot behavior trees internally  
└── Guaranteeing physical rollback  
└── Treating dispatch acknowledgment as final completion

---

## **Recommended Initial Stack Mapping**

└── Execution Adapter Service: Python FastAPI or async service  
└── Request Schema: Pydantic ExecutionRequestDTO and ExternalControlRequestDTO  
└── Adapter Registry: PostgreSQL table  
└── Dispatch Queue: PostgreSQL outbox or Redis queue first  
└── Protocols: REST Adapter first  
└── Realtime Feedback: WebSocket or webhook receiver first  
└── MQTT Adapter: for smart helmet / sensor / simple field notification integration  
└── ROS2 Bridge: later when robot middleware integration begins  
└── OPC-UA / PLC Adapter: later and only with strict industrial safety boundary  
└── Fleet Manager Adapter: mock adapter first, real adapter later  
└── Feedback Normalizer: common FeedbackEventDTO  
└── Idempotency: idempotency\_key on every request  
└── Observability: OpenTelemetry trace \+ adapter health metrics  
└── Audit: external dispatch and feedback audit records

Initial Rollout Rule:  
└── Start with mock external control adapter  
└── Then build REST adapter and MQTT notification adapter  
└── Add real fleet manager or ROS2 bridge only after ExecutionRequest schema is stable  
└── Add PLC / SCADA integration last, with strict safety, permission, test, and audit boundaries  
└── Do not build low-level robot control inside this system  
└── Do not let adapters bypass Unified Core or Safety Gate

---

## **Execution Request & External Control Integration Core Principles**

1. This Layer Integrates; It Does Not Control Everything  
   └── It connects to external control systems but does not replace them.  
2. Approved Execution Intent Must Be Preserved  
   └── Constraints, approval state, target, safety requirements, expected feedback, trace ID, and idempotency must survive protocol translation.  
3. External Systems Own Detailed Execution  
   └── Fleet managers, robot middleware, PLC / SCADA, behavior trees, and equipment controllers handle specialized execution details.  
4. Ontology System Does Not Drive Motors  
   └── It does not directly control robot joints, motors, collision avoidance, PLC logic, or machine sequences.  
5. Adapter Output Is a Request, Not Guaranteed Completion  
   └── Dispatch or acknowledgment does not mean the physical task is complete.  
6. Feedback Closes the Loop  
   └── Execution status, failure, acknowledgment, and completion feedback must return to Unified Core and World State.  
7. Protocol Translation Must Not Change Meaning  
   └── REST, ROS2, MQTT, OPC-UA, Modbus, WebSocket, gRPC, or Kafka adapters must preserve approved intent and constraints.  
8. Every External System Must Be Registered  
   └── External systems need identity, endpoint, supported actions, capability, permission scope, version, and health status.  
9. Adapter Capability Must Match Action Type  
   └── An adapter may receive only action types and target types it is approved to handle.  
10. Idempotency Is Mandatory  
    └── Retries and network failures must not cause duplicate physical execution.  
11. External Failure Must Become Structured Feedback  
    └── Timeout, rejection, unavailable system, invalid payload, or feedback conflict must return as structured failure status.  
12. PLC / SCADA Integration Requires Strong Boundary  
    └── Industrial control integration must be limited, permission-controlled, safety-validated, and auditable.  
13. Robot Middleware Is Not the Ontology System  
    └── Robot middleware handles robot execution; ontology system sends approved mission or task requests.  
14. Fleet Manager Is Not Rebuilt Here  
    └── Fleet manager performs scheduling and coordination; ontology system sends approved high-level requests.  
15. Behavior Trees Are External Execution Logic  
    └── Ontology may request a predefined behavior tree execution, but does not dynamically invent low-level behavior logic at runtime.  
16. Security Must Be Stronger at Physical Boundaries  
    └── External control adapters require authentication, authorization, encryption, credential management, and audit.  
17. Adapter Health Affects Dispatch Safety  
    └── Unhealthy, stale, disconnected, or unsupported adapters must block or escalate execution requests.  
18. Integration Must Be Observable  
    └── Dispatch latency, acknowledgment latency, failure rate, timeout count, and feedback latency must be monitored.  
19. Testing Must Precede Real Physical Dispatch  
    └── Mock adapters, simulation adapters, sandbox tests, and hardware-in-the-loop tests should precede real-world integration.  
20. This Layer Protects the Control Boundary  
    └── Its purpose is to connect ontology-approved intent to external physical systems without collapsing into unsafe direct control.

