# **Ontology Centric “Unified Cyber-Physical Core” Stack Mapping**

## **Layer 10\. Unified Cyber-Physical Core Layer**

─ Core Position  
└── Unified Cyber-Physical Core is the execution lifecycle core of the ontology-centric system  
└── It converts ApprovedAction into common events, states, execution requests, execution commands, feedback loops, recovery flows, and audit records  
└── It provides one unified lifecycle language between semantic decision, cyber system state, external control systems, and physical execution feedback  
└── It does not generate action candidates  
└── It does not approve actions  
└── It does not directly control robots, PLCs, SCADA, equipment, or fleet managers  
└── It does not perform low-level protocol translation  
└── It owns command lifecycle, execution state, idempotency, event sourcing, feedback handling, recovery orchestration, and audit linkage

---

## **Core Role**

└── Receive ApprovedAction from Safety Gate  
└── Convert ApprovedAction into ExecutionRequest  
└── Initialize command lifecycle state  
└── Attach idempotency key, UUID, UTC timestamp, trace context, and correlation context  
└── Resolve execution target at the abstract system level  
└── Coordinate dispatch through Execution Request & External Control Integration Layer  
└── Track execution status, acknowledgment, feedback, failure, timeout, recovery, and completion  
└── Update world state through feedback events  
└── Store audit records and event history  
└── Manage recovery workflow when execution fails or becomes unsafe  
└── Preserve cyber-physical traceability from decision to physical feedback

---

## **Core Technologies**

└── CoreEvent Schema  
└── DecisionCase Schema  
└── ApprovedAction Schema  
└── ExecutionRequest Schema  
└── ExecutionCommand Schema  
└── ExecutionResult Schema  
└── FeedbackEvent Schema  
└── AuditRecord Schema  
└── RecoveryRequest Schema  
└── Command Lifecycle Manager  
└── Event Sourcing  
└── Transactional Outbox  
└── Saga / Compensating Action Orchestration  
└── Idempotency Key  
└── UUID  
└── UTC Timestamp  
└── State Machine  
└── CQRS  
└── OpenTelemetry Trace Context  
└── Correlation ID  
└── Causation ID  
└── Command Status Store

---

## **Optional Technologies**

└── Temporal  
└── Camunda  
└── Durable Task Framework  
└── Kafka  
└── PostgreSQL Event Store  
└── Redis for command state cache  
└── Outbox Relay Worker  
└── Dead Letter Queue  
└── Retry Queue  
└── Event Replay Tool  
└── Command Replay Tool  
└── Workflow Recovery Engine  
└── Distributed Lock  
└── Exactly-once Effect Simulation through idempotency  
└── CQRS Read Model Builder  
└── State Machine Library  
└── OpenTelemetry Collector

---

## **Core Object Stack**

└── CoreEvent  
└── PerceptionEvent  
└── BeliefState  
└── ActionCandidate  
└── DecisionCase  
└── ApprovedAction  
└── ExecutionRequest  
└── ExecutionCommand  
└── ExecutionResult  
└── FeedbackEvent  
└── AuditRecord  
└── RecoveryRequest  
└── CommandState  
└── CommandLifecycle  
└── ExternalDispatchRecord  
└── CompensationAction  
└── ManualOverrideRequest  
└── StateTransitionRecord

Object Rule:  
└── Every major system transition must be represented as a typed object  
└── Free-form action text must not enter cyber-physical execution lifecycle  
└── Objects must preserve trace ID, correlation ID, causation ID, version, timestamp, and source layer

---

## **CoreEvent Schema Stack**

└── event\_id  
└── event\_type  
└── source\_layer  
└── source\_service  
└── source\_actor  
└── target\_node\_id  
└── target\_node\_type  
└── payload  
└── event\_time  
└── ingestion\_time  
└── trace\_id  
└── correlation\_id  
└── causation\_id  
└── schema\_version  
└── ontology\_version  
└── policy\_version  
└── state\_version

CoreEvent Rule:  
└── CoreEvent is the common event language across perception, decision, approval, execution, feedback, recovery, and audit  
└── Every event must be typed, versioned, traceable, and replayable where appropriate

---

## **ApprovedAction Intake Stack**

└── ApprovedAction Received  
└── ApprovedAction Schema Validation  
└── Safety Gate Validation Report Check  
└── Approval Record Check  
└── Evidence Reference Check  
└── Policy Version Check  
└── Ontology Version Check  
└── World State Snapshot Check  
└── Validity Window Check  
└── Idempotency Key Check  
└── Duplicate Action Detection  
└── Execution Readiness Check

ApprovedAction Intake Rule:  
└── Only ApprovedAction from Safety Gate may enter Unified Cyber-Physical Core  
└── ActionCandidate cannot bypass Safety Gate and enter this layer directly  
└── Expired, duplicated, revoked, or invalid ApprovedAction must not create ExecutionRequest

---

## **ExecutionRequest Schema Stack**

└── execution\_request\_id  
└── approved\_action\_id  
└── decision\_case\_id  
└── action\_type  
└── target\_node\_id  
└── target\_node\_type  
└── external\_target\_type  
└── external\_target\_id  
└── requested\_intent  
└── execution\_constraints  
└── safety\_conditions  
└── expected\_feedback  
└── timeout\_policy  
└── retry\_policy  
└── recovery\_policy  
└── priority  
└── validity\_window  
└── idempotency\_key  
└── trace\_id  
└── correlation\_id  
└── created\_at\_utc

ExecutionRequest Rule:  
└── ExecutionRequest is a high-level approved execution request  
└── It is not a low-level robot motion command  
└── It must be sent to Layer 11 for external control integration and protocol-specific dispatch

---

## **ExecutionCommand Schema Stack**

└── execution\_command\_id  
└── execution\_request\_id  
└── external\_system\_id  
└── adapter\_type  
└── command\_type  
└── command\_payload  
└── command\_constraints  
└── command\_status  
└── dispatch\_time  
└── acknowledgment\_time  
└── timeout\_at  
└── retry\_count  
└── idempotency\_key  
└── trace\_id  
└── correlation\_id

ExecutionCommand Boundary:  
└── ExecutionCommand represents a dispatchable command object inside the cyber-physical lifecycle  
└── Protocol translation and system-specific command formatting belong to Layer 11  
└── Low-level motion planning, PLC logic, fleet scheduling, and behavior tree execution remain in external systems

---

## **ExecutionResult Schema Stack**

└── execution\_result\_id  
└── execution\_request\_id  
└── execution\_command\_id  
└── external\_system\_id  
└── result\_status  
└── result\_code  
└── result\_message  
└── started\_at  
└── completed\_at  
└── failed\_at  
└── failure\_code  
└── failure\_reason  
└── feedback\_refs  
└── recovery\_required  
└── final\_world\_state\_ref  
└── trace\_id  
└── correlation\_id

ExecutionResult Rule:  
└── ExecutionResult records what happened after dispatch  
└── It must be linked to feedback, audit, world state update, and recovery decision when needed

---

## **FeedbackEvent Schema Stack**

└── feedback\_event\_id  
└── execution\_request\_id  
└── execution\_command\_id  
└── external\_system\_id  
└── feedback\_type  
└── feedback\_status  
└── observed\_state  
└── source\_timestamp  
└── ingestion\_timestamp  
└── confidence\_score  
└── evidence\_refs  
└── world\_state\_update\_required  
└── recovery\_required  
└── trace\_id  
└── correlation\_id

FeedbackEvent Rule:  
└── Feedback from external control systems must update execution state and world state  
└── Missing, stale, conflicting, or failed feedback must trigger timeout, retry, recovery, or manual review according to policy

---

## **AuditRecord Schema Stack**

└── audit\_record\_id  
└── related\_event\_id  
└── related\_decision\_case\_id  
└── related\_approved\_action\_id  
└── related\_execution\_request\_id  
└── actor\_id  
└── action\_type  
└── target\_node\_id  
└── state\_transition  
└── result\_status  
└── evidence\_refs  
└── policy\_version  
└── ontology\_version  
└── approval\_record\_id  
└── timestamp\_utc  
└── trace\_id  
└── correlation\_id

AuditRecord Rule:  
└── Every important lifecycle transition must create or update an audit record  
└── Audit records must reconstruct the path from ApprovedAction to feedback and recovery

---

## **Command Lifecycle Manager Stack**

└── ApprovedAction Intake  
└── ExecutionRequest Creation  
└── Command State Initialization  
└── External Target Resolution  
└── Dispatch Preparation  
└── Dispatch Request  
└── Acknowledgment Tracking  
└── Execution Tracking  
└── Feedback Handling  
└── Timeout Handling  
└── Retry Handling  
└── Failure Handling  
└── Recovery Flow Trigger  
└── Completion Handling  
└── Audit Finalization  
└── World State Synchronization  
└── UI Synchronization

Lifecycle Rule:  
└── Every command must have an explicit lifecycle state  
└── Undefined state transitions are rejected  
└── Lifecycle state must be observable, auditable, and recoverable

---

## **Command State Machine Stack**

└── approved\_action\_received  
└── execution\_request\_created  
└── target\_resolved  
└── dispatch\_pending  
└── dispatched  
└── acknowledged  
└── executing  
└── feedback\_received  
└── completed  
└── failed  
└── timeout  
└── retry\_pending  
└── recovery\_required  
└── recovery\_in\_progress  
└── manually\_overridden  
└── cancelled  
└── closed

State Machine Rule:  
└── Command state transition must be deterministic and auditable  
└── Invalid transitions must be rejected  
└── Timeout, retry, failure, and recovery states must be explicitly modeled

---

## **Event Sourcing Stack**

└── Append-only Event Store  
└── Command Lifecycle Events  
└── ApprovedActionReceivedEvent  
└── ExecutionRequestCreatedEvent  
└── TargetResolvedEvent  
└── ExecutionDispatchedEvent  
└── AcknowledgmentReceivedEvent  
└── FeedbackReceivedEvent  
└── ExecutionCompletedEvent  
└── ExecutionFailedEvent  
└── RecoveryRequestedEvent  
└── ManualOverrideEvent  
└── AuditFinalizedEvent  
└── Event Replay  
└── Event Sequence Number  
└── Snapshotting optional

Event Sourcing Rule:  
└── Important lifecycle changes should be append-only events  
└── Event history must allow reconstruction of what happened  
└── Event replay must not accidentally re-execute physical actions; replay must be separated from live dispatch

---

## **Transactional Outbox Stack**

└── Outbox Table  
└── Outbox Event  
└── Database Transaction  
└── Outbox Relay Worker  
└── Dispatch Status  
└── Retry Count  
└── Dead Letter Queue  
└── Idempotency Key  
└── Exactly-once Effect Approximation  
└── Event Publication  
└── Failure Recovery

Transactional Outbox Rule:  
└── State changes and outbound events must not become inconsistent  
└── If ExecutionRequest is created, the event for dispatch must be reliably published  
└── Outbox prevents losing execution events between database commit and message broker publish

---

## **Idempotency Stack**

└── Idempotency Key  
└── Duplicate Request Detection  
└── Duplicate Dispatch Prevention  
└── Command Deduplication  
└── External System Idempotency Token  
└── Retry-safe Dispatch  
└── Idempotent Feedback Handling  
└── Idempotent State Update  
└── Idempotent Audit Append

Idempotency Rule:  
└── Retrying a failed network call must not execute the same physical action twice  
└── Idempotency key must travel from ApprovedAction to ExecutionRequest, ExecutionCommand, external dispatch, feedback, and audit

---

## **UUID / Timestamp Stack**

└── UUID  
└── Event ID  
└── Command ID  
└── Execution Request ID  
└── Correlation ID  
└── Causation ID  
└── UTC Timestamp  
└── Source Timestamp  
└── Ingestion Timestamp  
└── Dispatch Timestamp  
└── Acknowledgment Timestamp  
└── Completion Timestamp  
└── Failure Timestamp

Time Rule:  
└── All lifecycle timestamps must use UTC  
└── Source time and system ingestion time must be distinguished  
└── Time ordering matters for audit, replay, recovery, and incident analysis

---

## **CQRS Stack**

└── Command Model  
└── Query Model  
└── Write Side  
└── Read Side  
└── Execution Command Store  
└── Execution Status Read Model  
└── Decision Case Read Model  
└── Audit Read Model  
└── Digital Twin Read Model  
└── Projection Builder  
└── Event-to-Read-Model Projection

CQRS Rule:  
└── Write-side command lifecycle should be protected and strongly validated  
└── Read-side views should be optimized for dashboard, audit, search, and digital twin display  
└── Read models may lag slightly but must expose freshness and version

---

## **Saga / Compensating Action Orchestration Stack**

└── Saga Coordinator  
└── Compensation Workflow  
└── RecoveryRequest  
└── Safe-state Transition  
└── Manual Override Request  
└── External Recovery Request  
└── Retry Policy  
└── Timeout Policy  
└── Failure Policy  
└── Recovery State Machine  
└── Recovery Audit Record  
└── Post-failure Review

Saga Boundary:  
└── Saga in this architecture does not mean physical rollback  
└── Physical time cannot be reversed  
└── In cyber-physical execution, rollback means recovery orchestration, safe-state transition, manual override request, compensation workflow, and audit recovery  
└── Detailed recovery behavior is delegated to external control systems, fleet managers, robot controllers, behavior trees, PLC / SCADA systems, and equipment controllers

---

## **RecoveryRequest Stack**

└── recovery\_request\_id  
└── execution\_request\_id  
└── failed\_command\_id  
└── failure\_type  
└── failure\_reason  
└── target\_node\_id  
└── external\_system\_id  
└── recommended\_recovery\_type  
└── safe\_state\_required  
└── manual\_override\_required  
└── compensation\_action\_refs  
└── evidence\_refs  
└── trace\_id  
└── correlation\_id  
└── created\_at\_utc

Recovery Types:  
└── retry\_dispatch  
└── request\_external\_cancel  
└── request\_safe\_state  
└── request\_manual\_override  
└── escalate\_to\_supervisor  
└── escalate\_to\_emergency\_authority  
└── create\_incident\_case  
└── mark\_execution\_failed  
└── trigger\_reinspection  
└── update\_world\_state\_to\_unknown\_or\_unsafe

---

## **Failure Handling Stack**

└── Dispatch Failure  
└── Acknowledgment Timeout  
└── Execution Timeout  
└── External Control Error  
└── Feedback Missing  
└── Feedback Conflict  
└── World State Update Failure  
└── Safety Interlock Triggered  
└── Manual Override Required  
└── Recovery Required  
└── Dead Letter Handling  
└── Incident Case Generation

Failure Rule:  
└── Failure must not disappear as a log only  
└── Failure must update command state, audit record, world state, and recovery path  
└── High-risk execution failure must escalate

---

## **Feedback Loop Stack**

└── External Feedback Received  
└── Feedback Schema Validation  
└── Feedback Source Verification  
└── Feedback Freshness Check  
└── Execution State Update  
└── World State Update  
└── Audit Update  
└── Decision Case Update  
└── UI Synchronization  
└── Recovery Evaluation  
└── Completion Evaluation

Feedback Rule:  
└── Execution is not complete merely because a request was dispatched  
└── Completion requires feedback, state update, timeout resolution, or verified external result depending on action type

---

## **External Target Resolution Stack**

└── Target Node Resolution  
└── External System Mapping  
└── Adapter Selection  
└── Fleet Manager Target  
└── Robot Middleware Target  
└── PLC / SCADA Target  
└── Equipment Controller Target  
└── Site Operation Platform Target  
└── Notification System Target  
└── Capability Match  
└── Availability Check  
└── Routing Metadata

Target Resolution Rule:  
└── Unified Core resolves the abstract external target  
└── Layer 11 performs adapter-specific protocol integration  
└── If no valid external target exists, execution request must block or escalate

---

## **World State Update Stack**

└── Execution Status Update  
└── Target Node State Update  
└── Robot State Update  
└── Equipment State Update  
└── Zone State Update  
└── Task State Update  
└── Approval State Update  
└── Recovery State Update  
└── Redis World State Update  
└── Kafka State Change Event  
└── Historical Event Append  
└── Digital Twin Sync Event

World State Rule:  
└── Execution feedback must update Layer 6 Real-Time World State  
└── Finalized or meaningful events may be stored in Layer 5 Historical Event Store  
└── UI must receive state synchronization through API Gateway / realtime delivery

---

## **Audit & Trace Stack**

└── OpenTelemetry Trace Context  
└── Trace ID  
└── Correlation ID  
└── Causation ID  
└── Decision Trace  
└── Execution Trace  
└── Feedback Trace  
└── Recovery Trace  
└── Audit Record  
└── Event Lineage  
└── Evidence Link  
└── Policy Version  
└── Ontology Version  
└── Approval Record Link  
└── State Snapshot Link

Trace Rule:  
└── A full trace must connect DecisionCase → ApprovedAction → ExecutionRequest → ExecutionCommand → External Feedback → World State Update → AuditRecord

---

## **Command Lifecycle Flow**

└── ApprovedAction received  
└── ApprovedAction validity checked  
└── ExecutionRequest generated  
└── Command state initialized  
└── External control target resolved  
└── Execution request prepared  
└── Execution request dispatched through Layer 11  
└── Dispatch acknowledgment received  
└── Feedback received  
└── Failure or recovery state evaluated  
└── World state updated  
└── Audit record stored  
└── UI state synchronized  
└── Execution lifecycle closed or recovery continues

Flow Rule:  
└── Execution lifecycle is complete only when final status, feedback, world state update, and audit record are resolved

---

## **Command Lifecycle Status Stack**

└── pending  
└── prepared  
└── dispatched  
└── acknowledged  
└── executing  
└── succeeded  
└── failed  
└── timeout  
└── cancelled  
└── recovery\_required  
└── recovery\_in\_progress  
└── recovered  
└── manually\_overridden  
└── closed

Status Rule:  
└── Status must be explicit and machine-readable  
└── UI, audit, world state, and recovery logic must use the same command lifecycle status vocabulary

---

## **Observability Stack**

└── Execution Request Creation Count  
└── Command Dispatch Count  
└── Command Lifecycle Latency  
└── Dispatch Latency  
└── Acknowledgment Latency  
└── Execution Completion Latency  
└── Feedback Latency  
└── Timeout Count  
└── Retry Count  
└── Recovery Request Count  
└── Manual Override Count  
└── Duplicate Command Block Count  
└── Outbox Pending Count  
└── Outbox Failure Count  
└── Dead Letter Count  
└── State Transition Failure Count

Observability Rule:  
└── Every execution lifecycle must be measurable from ApprovedAction intake to final feedback or recovery state  
└── Silent command failure is unacceptable in cyber-physical systems

---

## **Security & Governance Stack**

└── ApprovedAction Source Verification  
└── Execution Request Permission Check  
└── External Target Permission Check  
└── Idempotency Enforcement  
└── Command Replay Protection  
└── Audit Access Control  
└── Recovery Authorization  
└── Manual Override Authorization  
└── Sensitive Payload Redaction  
└── Trace Access Control  
└── External Dispatch Audit

Security Rule:  
└── Only authorized, validated, and approved actions may enter execution lifecycle  
└── Retry, replay, recovery, and manual override must be permission-controlled and auditable

---

## **Runtime Boundary**

└── This layer is active after Safety Gate approval and before external control integration  
└── It owns execution lifecycle, command state, feedback, recovery, idempotency, event sourcing, and audit linkage  
└── It must not perform full ontology reasoning, broad RAG, or LLM decision-making in the critical path  
└── It must not perform low-level physical control logic  
└── It sends structured ExecutionRequest to Layer 11  
└── It receives feedback from Layer 11 and updates world state, audit, and lifecycle state  
└── It must be deterministic, traceable, idempotent, and recoverable

---

## **Not Responsible For**

└── Generating action candidates  
└── Classifying risk tiers  
└── Performing human approval UI  
└── Performing final Safety Gate validation  
└── Defining ontology meaning  
└── Managing policy definitions  
└── Running low-level robot control  
└── Running robot behavior trees directly  
└── Running fleet scheduling directly  
└── Running PLC logic directly  
└── Running SCADA control directly  
└── Translating every protocol directly  
└── Performing ROS2 / OPC-UA / Modbus implementation directly  
└── Replacing Layer 11 external control integration  
└── Guaranteeing physical rollback  
└── Treating dispatch as completion

---

## **Recommended MVP Stack Mapping**

└── Core Language: Pydantic schemas for CoreEvent, ApprovedAction, ExecutionRequest, ExecutionResult, FeedbackEvent, AuditRecord  
└── ID Strategy: UUID for all lifecycle objects  
└── Time Strategy: UTC timestamps  
└── Trace Strategy: trace\_id, correlation\_id, causation\_id on every object  
└── State Machine: explicit Python enum state machine  
└── Event Store: PostgreSQL append-only event table  
└── Command Store: PostgreSQL command lifecycle table  
└── Outbox: PostgreSQL transactional outbox table  
└── Idempotency: idempotency\_key table with duplicate protection  
└── Message Dispatch: internal async worker first, Kafka later  
└── Recovery: simple compensating workflow table first  
└── Audit: audit records emitted to Layer 0  
└── World State Update: Redis update through Layer 6 service  
└── UI Sync: WebSocket / SSE event through API Gateway  
└── Observability: OpenTelemetry traces \+ structured logs

MVP Rule:  
└── Start with strict schemas, explicit state machine, PostgreSQL event store, transactional outbox, idempotency key, and feedback handling  
└── Do not build complex Saga engine first  
└── Do not connect directly to robot / PLC / SCADA protocols from this layer  
└── Create one clean flow: ApprovedAction → ExecutionRequest → Dispatch → Feedback → WorldState Update → Audit  
└── Add Temporal, Kafka, CQRS read models, and advanced recovery only after lifecycle objects stabilize

---

## **Unified Cyber-Physical Core Principles**

1. ApprovedAction Is the Entry Point  
   └── Only Safety Gate-approved actions may enter this layer.  
2. ApprovedAction Is Not a Physical Command  
   └── It must first become an ExecutionRequest with lifecycle, constraints, target, trace, and idempotency.  
3. ExecutionRequest Is the Bridge Object  
   └── It connects semantic approval to external control integration without containing low-level device logic.  
4. Dispatch Is Not Completion  
   └── Execution is not complete until acknowledgment, feedback, final state, timeout, failure, or recovery is resolved.  
5. Every Command Needs a Lifecycle  
   └── Pending, dispatched, acknowledged, executing, completed, failed, timeout, and recovery states must be explicit.  
6. Idempotency Is Mandatory  
   └── Retries must not accidentally execute the same physical action twice.  
7. Event Sourcing Preserves History  
   └── Important lifecycle changes should be append-only, replayable, auditable events.  
8. Replay Must Not Re-execute Physical Actions  
   └── Historical replay is for reconstruction and debugging, not uncontrolled redispatch.  
9. Transactional Outbox Prevents Lost Dispatch  
   └── State changes and outbound execution events must be committed reliably.  
10. Saga Does Not Mean Physical Rollback  
    └── Cyber-physical rollback means recovery orchestration, safe-state transition, manual override, compensation, and audit recovery.  
11. Physical Time Cannot Be Reversed  
    └── The system must recover forward, not pretend to undo the physical past.  
12. Recovery Belongs to the Lifecycle  
    └── Failure, timeout, missing feedback, and unsafe state must create explicit recovery states or RecoveryRequests.  
13. External Systems Own Detailed Execution  
    └── Fleet managers, robot controllers, behavior trees, PLC / SCADA, and equipment controllers handle specialized execution details.  
14. Unified Core Owns Execution Traceability  
    └── It must connect decision, approval, execution request, dispatch, feedback, recovery, world state, and audit.  
15. Feedback Must Update World State  
    └── Physical execution results must update Layer 6 current state and Layer 5 history when meaningful.  
16. Every Transition Must Be Auditable  
    └── Approved, dispatched, acknowledged, failed, recovered, manually overridden, and completed states require audit trace.  
17. UTC Time Is Mandatory  
    └── Cyber-physical events across devices and systems must use UTC timestamps for ordering and audit.  
18. CQRS Separates Write Safety from Read Visibility  
    └── Command lifecycle writes must be protected; dashboard and audit read models may be optimized separately.  
19. Unified Core Must Stay Deterministic  
    └── It should avoid open-ended LLM reasoning, broad retrieval, or full ontology reasoning in execution lifecycle path.  
20. This Layer Standardizes the Cyber-Physical Language  
    └── Its purpose is to make every approved action, execution request, feedback event, recovery flow, and audit record speak the same lifecycle language.

