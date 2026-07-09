# **Ontology Centric “Decision Router / Escalation” Stack Mapping**

## **Layer 8\. Decision Router / Escalation Layer**

─ Core Position  
└── Decision Router / Escalation Layer is the routing and prioritization layer of the ontology-centric system  
└── It classifies events, alerts, risk signals, action candidates, and decision cases by risk, urgency, approval requirement, operational impact, and escalation policy  
└── It determines whether something should be logged, displayed, notified, escalated, reviewed, approved, or routed to emergency handling  
└── It prevents the system from flooding humans, safety gates, and command centers with low-value events  
└── It does not generate raw perception  
└── It does not define ontology meaning  
└── It does not perform final safety approval  
└── It does not directly execute physical commands  
└── It routes structured candidates and cases to the correct next layer

---

## **Core Role**

└── Classify incoming events, alerts, action candidates, escalation cases, and decision cases  
└── Assign risk tier, urgency level, priority, and routing path  
└── Decide whether a case is routine, notice, warning, high risk, critical emergency, or exceptional  
└── Route approval-required cases to Human Approval Center and Safety Gate path  
└── Route supervisor-required cases to supervisor notification  
└── Route high-risk cases to War Room display and human approval workflow  
└── Route critical emergency cases to deterministic safety path when policy allows  
└── Route exceptional cases to expert review or strategic decision workflow  
└── Prioritize decision cases and prevent human attention overload  
└── Preserve routing trace, reason code, risk tier, escalation policy, and decision path

---

## **Core Technologies**

└── Rule-based Decision Table  
└── DMN  
└── BPMN  
└── Priority Queue  
└── Risk Tier Classifier  
└── Event Severity Classifier  
└── Escalation Policy Engine  
└── OPA / Rego  
└── State Machine  
└── Message Broker  
└── Kafka Topic Routing  
└── Async Queue  
└── Routing Rule Engine  
└── DecisionCase DTO  
└── EscalationCase DTO  
└── Priority Scheduler  
└── Event Correlation Engine

---

## **Optional Technologies**

└── Drools  
└── Camunda  
└── Temporal  
└── Prefect  
└── Celery  
└── Redis Queue  
└── NATS  
└── RabbitMQ  
└── Apache Airflow for non-runtime workflows  
└── Custom Python Rule Engine  
└── Lightweight State Machine Library  
└── ML-based Severity Classifier  
└── LLM-assisted Case Summarizer  
└── Human-in-the-loop Review Queue  
└── War Room Case Board

Boundary:  
└── Deterministic routing rules should be preferred for safety-critical paths  
└── ML or LLM assistance may help summarize or enrich cases, but must not replace deterministic escalation policy for high-risk routing

---

## **Input Stack**

└── Alert  
└── RiskSignal  
└── ActionCandidate  
└── EscalationCase  
└── DecisionCase Draft  
└── WorldStateChangeEvent  
└── AgentOutputEvent  
└── SensorAnomalyEvent  
└── SafetyRiskEvent  
└── EquipmentFailureEvent  
└── RobotStatusEvent  
└── ZoneRiskEvent  
└── WorkerRiskEvent  
└── ExecutionFeedbackEvent  
└── ManualOverrideRequest  
└── EmergencyEvent

Input Rule:  
└── Inputs must be structured, typed, traceable, and ontology-grounded before routing  
└── Free-form LLM output should not be routed directly without DTO conversion and validation  
└── Low-confidence or ungrounded inputs must be downgraded, quarantined, or routed to review

---

## **Output Stack**

└── RoutingDecision  
└── RoutedDecisionCase  
└── SupervisorNotification  
└── WarRoomCase  
└── HumanApprovalRequest  
└── EmergencyRoutingCase  
└── ExpertReviewCase  
└── StrategicDecisionCase  
└── LogOnlyEvent  
└── UIDisplayEvent  
└── SafetyGateReviewRequest  
└── EscalationNotification  
└── ConflictReviewCase  
└── DecisionPriorityUpdate

Output Rule:  
└── Outputs determine the next processing path  
└── Outputs are not execution commands  
└── Execution readiness requires ApprovedAction, RuntimeValidationResult, and SafetyGatePass before an ExecutionRequest can be created

---

## **Decision Tier Stack**

└── Routine  
└── Local Processing  
└── Log Only  
└── No human interruption  
└── No approval required

└── Notice  
└── UI Display  
└── Dashboard update  
└── Event timeline update  
└── Low urgency

└── Warning  
└── Supervisor Notification  
└── Alert Center update  
└── Follow-up may be required  
└── Medium urgency

└── High Risk  
└── War Room Display  
└── Human Approval  
└── Safety Gate path  
└── Evidence review required  
└── High urgency

└── Critical Emergency  
└── Deterministic Safety Action path if predefined by policy  
└── Immediate alert  
└── Post-execution report  
└── Emergency audit  
└── Recovery workflow

└── Exceptional  
└── Expert Review  
└── Strategic Decision  
└── Multi-party review  
└── Policy or ontology review may be required

---

## **Risk Tier Classification Stack**

└── Risk Tier Classifier  
└── Severity Score  
└── Urgency Score  
└── Human Safety Risk  
└── Legal Compliance Risk  
└── Robot Safety Risk  
└── Equipment Protection Risk  
└── Productivity Impact  
└── Zone Risk Level  
└── Worker Exposure Level  
└── Task Criticality  
└── Evidence Completeness  
└── State Freshness  
└── Confidence Score  
└── Policy Sensitivity  
└── Approval Requirement

Risk Tier Rule:  
└── Human safety risk has highest priority  
└── Legal compliance risk must not be downgraded for productivity  
└── Low-confidence high-impact cases should escalate rather than disappear  
└── Stale current state should increase uncertainty and may require escalation

---

## **Event Severity Classifier Stack**

└── Event Type  
└── Event Source  
└── Source Reliability  
└── Event Freshness  
└── Affected Object Type  
└── Affected Zone  
└── Affected Worker Count  
└── Affected Robot Count  
└── Affected Equipment Count  
└── Environmental Severity  
└── Operational Impact  
└── Escalation History  
└── Similar Incident History  
└── Emergency Indicator

Severity Examples:  
└── Sensor heartbeat lost in low-risk zone → Notice  
└── Worker near active crane zone → Warning or High Risk  
└── Gas sensor threshold exceeded with worker presence → Critical Emergency  
└── Equipment abnormal state without worker exposure → Warning  
└── Robot route blocked with no safety impact → Notice or Warning  
└── Missing evidence for high-risk action candidate → Expert Review or High Risk

---

## **Rule-based Decision Table Stack**

└── Condition  
└── Risk Tier  
└── Urgency  
└── Required Route  
└── Required Approval  
└── Required Notification  
└── Required Evidence  
└── Required Audit  
└── Escalation Deadline  
└── Fallback Route  
└── Rule Version  
└── Rule Reason Code

Decision Table Example:  
└── If action\_type \= ACTION\_NOTIFY\_MANAGER and risk\_tier \= Notice  
→ Route to UI Display and Notification Center

└── If action\_type \= ACTION\_LOCK\_ZONE and risk\_tier \= High Risk  
→ Route to Human Approval and War Room Display

└── If event\_type \= WorkerInsideRestrictedZone and worker\_exposure \= true  
→ Route to High Risk or Critical Emergency depending on zone policy

└── If event\_type \= GasThresholdExceeded and worker\_presence \= true  
→ Route to Critical Emergency

└── If evidence\_confidence \< threshold and risk\_tier \>= High Risk  
→ Route to Expert Review / Human Approval

---

## **DMN Stack**

└── Decision Model and Notation  
└── Decision Table  
└── Input Data  
└── Decision Rule  
└── Hit Policy  
└── Decision Requirement Diagram  
└── Risk Tier Decision  
└── Approval Requirement Decision  
└── Escalation Route Decision  
└── Notification Decision  
└── Emergency Path Decision

DMN Usage:  
└── Express routing and escalation policy in business-readable tables  
└── Support governance review of decision logic  
└── Support scenario testing for risk tier and escalation routing  
└── Useful when safety managers, engineers, or compliance teams need to inspect routing rules

---

## **BPMN Stack**

└── Business Process Model and Notation  
└── Escalation Workflow  
└── Approval Workflow  
└── Emergency Workflow  
└── Expert Review Workflow  
└── Manual Review Workflow  
└── Supervisor Notification Workflow  
└── War Room Case Workflow  
└── Incident Response Workflow

BPMN Usage:  
└── Model the workflow after routing decision is made  
└── Useful for approval chains, review loops, emergency workflows, and escalation procedures  
└── BPMN should model process flow, not replace ontology meaning or safety validation

---

## **Escalation Policy Engine Stack**

└── Escalation Rule  
└── Escalation Matrix  
└── Risk Tier Policy  
└── Approval Requirement Policy  
└── Notification Policy  
└── War Room Policy  
└── Emergency Policy  
└── Expert Review Policy  
└── Supervisor Assignment Policy  
└── Deadline Policy  
└── Re-escalation Policy  
└── Escalation Audit Log  
└── Escalation Reason Code

Escalation Policy Examples:  
└── High-risk worker safety case requires supervisor and safety manager review  
└── Critical emergency routes to deterministic safety path and post-execution report  
└── Unclear policy conflict routes to expert review  
└── Multiple repeated warnings in same zone escalate to high risk  
└── Failure to approve within deadline escalates to next authority level

---

## **OPA / Rego Integration Stack**

└── Policy Input DTO  
└── Rego Escalation Policy  
└── Authorization Context  
└── Risk Context  
└── Approval Requirement Context  
└── Emergency Rule Context  
└── Allow / Deny / Escalate Decision  
└── Required Approval Level  
└── Required Notification Target  
└── Required Review Type  
└── Policy Version  
└── Policy Decision Trace

OPA Usage:  
└── Check whether a route is allowed  
└── Determine required approval level  
└── Determine whether emergency path is permitted  
└── Determine whether supervisor notification is required  
└── Determine whether expert review is required

Boundary:  
└── Decision Router may call OPA / Rego for routing policy  
└── Governance Layer owns the policy definitions  
└── Safety Gate still performs final executable action validation

---

## **State Machine Stack**

└── DecisionCase State  
└── Routing State  
└── Escalation State  
└── Approval State  
└── Review State  
└── Emergency State  
└── Conflict State  
└── Timeout State  
└── Final Routing State  
└── State Transition Log

DecisionCase States:  
└── received  
└── classified  
└── routed\_to\_log  
└── routed\_to\_ui  
└── supervisor\_notified  
└── routed\_to\_human\_approval  
└── routed\_to\_war\_room  
└── routed\_to\_emergency\_path  
└── routed\_to\_expert\_review  
└── awaiting\_review  
└── escalated  
└── closed  
└── cancelled

State Machine Rule:  
└── Every decision case should have explicit state transitions  
└── State changes must be auditable and traceable  
└── Undefined state transitions must be rejected

---

## **Priority Queue Stack**

└── Priority Queue  
└── Risk-based Priority  
└── Urgency-based Priority  
└── Time-to-deadline Priority  
└── Human Safety Priority  
└── Emergency Priority  
└── Aging Policy  
└── Starvation Prevention  
└── Queue Partition by Site  
└── Queue Partition by Domain  
└── Queue Partition by Risk Tier  
└── Backpressure Handling

Priority Rule:  
└── Critical emergency cases outrank high-risk cases  
└── High-risk human safety cases outrank productivity-related cases  
└── Old unresolved cases may increase priority through aging policy  
└── Routine events should not block high-risk review queues

---

## **Message Routing Stack**

└── Message Broker  
└── Kafka Topic Routing  
└── Async Queue  
└── Routing Key  
└── Event Type Routing  
└── Risk Tier Routing  
└── Domain Routing  
└── Site Routing  
└── Priority Routing  
└── Dead Letter Queue  
└── Retry Queue  
└── Delayed Queue  
└── Escalation Queue

Topic Examples:  
└── decision.routine  
└── decision.notice  
└── decision.warning  
└── decision.high\_risk  
└── decision.critical\_emergency  
└── decision.exceptional  
└── approval.required  
└── warroom.cases  
└── supervisor.notifications  
└── expert.review  
└── safety\_gate.review

Routing Rule:  
└── Routing must be deterministic, observable, and replayable  
└── High-risk routing failures must be escalated, not silently dropped

---

## **Human Approval Routing Stack**

└── Approval Requirement Check  
└── Approval Level Determination  
└── Reviewer Assignment  
└── Approval Queue Routing  
└── Approval Deadline  
└── Approval Escalation  
└── Evidence Bundle Attachment  
└── DecisionCase Summary  
└── Approval Notification  
└── Approval Audit Record

Approval Routing Rule:  
└── Decision Router routes cases to approval workflow  
└── It does not approve the action itself  
└── ApprovalDecision produces ApprovedAction; Safety Gate later consumes ApprovedAction plus RuntimeValidationResult before any ExecutionRequest creation

---

## **Emergency Routing Stack**

└── Emergency Event Detection  
└── Emergency Tier Classification  
└── Deterministic Safety Path Check  
└── Emergency Policy Check  
└── Immediate Notification  
└── Emergency Execution Candidate Routing  
└── Post-execution Report Requirement  
└── Emergency Audit Record  
└── Recovery Workflow Trigger  
└── Manual Override Option

Emergency Rule:  
└── Critical emergency does not mean uncontrolled execution  
└── Emergency fast path must be predefined by policy  
└── Emergency routing must preserve trace ID, evidence, reason code, and post-execution audit  
└── If emergency path is not clearly defined, escalate to human emergency authority

---

## **War Room Case Stack**

└── WarRoomCase  
└── High-risk DecisionCase  
└── Critical Emergency Case  
└── Multi-entity Incident Case  
└── Site-level Risk Case  
└── Evidence Bundle  
└── Current World State Snapshot  
└── Risk Timeline  
└── Affected Node List  
└── Recommended Review Path  
└── Required Approval Level  
└── Assigned Owner  
└── War Room Display Status

War Room Rule:  
└── War Room should display high-risk, critical, exceptional, or multi-party cases  
└── It should not display every low-level event  
└── Human attention must be protected from noise

---

## **Conflict Routing Stack**

└── Policy Conflict  
└── State Conflict  
└── Evidence Conflict  
└── Entity Conflict  
└── Source Conflict  
└── Approval Conflict  
└── Agent Disagreement  
└── Ontology Mapping Conflict  
└── Risk Classification Conflict  
└── Conflict Quarantine  
└── Expert Review Routing  
└── Conflict Audit Record

Conflict Examples:  
└── One source reports worker inside zone, another reports outside  
└── Safety policy blocks action while productivity policy recommends continuation  
└── Agent A recommends evacuation while Agent B recommends inspection first  
└── Ontology entity mapping is ambiguous  
└── Evidence confidence is too low for high-risk candidate

Conflict Rule:  
└── High-risk conflicts should escalate to expert review or human approval  
└── Safety-first and more-restrictive routing should be used when uncertainty remains

---

## **DecisionCase Prioritization Stack**

└── Risk Tier  
└── Urgency  
└── Human Safety Impact  
└── Legal Impact  
└── Operational Impact  
└── Affected Entity Count  
└── Zone Criticality  
└── Time Sensitivity  
└── Confidence Level  
└── Evidence Completeness  
└── Repetition Frequency  
└── Escalation Age  
└── Required Approval Level  
└── Emergency Indicator

Prioritization Rule:  
└── Priority must be explainable  
└── Priority must not be based only on model confidence  
└── Human safety, legal compliance, and emergency status dominate productivity impact

---

## **Notification Stack**

└── Supervisor Notification  
└── Safety Manager Notification  
└── Operator Notification  
└── War Room Notification  
└── Expert Review Notification  
└── Emergency Notification  
└── Mobile Push  
└── Email  
└── SMS optional  
└── Dashboard Alert  
└── Notification Acknowledgment  
└── Notification Escalation

Notification Rule:  
└── Notifications must match risk tier and role  
└── High-risk notifications require acknowledgment tracking  
└── Repeated low-risk notifications should be aggregated to reduce noise

---

## **Decision Router DTO Stack**

└── RoutingInputDTO  
└── RoutingDecisionDTO  
└── RiskTierDTO  
└── EventSeverityDTO  
└── EscalationCaseDTO  
└── DecisionCaseDTO  
└── WarRoomCaseDTO  
└── ApprovalRoutingDTO  
└── EmergencyRoutingDTO  
└── ExpertReviewDTO  
└── NotificationRoutingDTO  
└── ConflictCaseDTO  
└── RoutingTraceDTO

RoutingDecisionDTO Fields:  
└── routing\_decision\_id  
└── source\_event\_id  
└── source\_candidate\_id  
└── decision\_case\_id  
└── input\_type  
└── risk\_tier  
└── urgency  
└── priority  
└── route  
└── required\_approval\_level  
└── notification\_targets  
└── escalation\_reason  
└── policy\_version  
└── rule\_version  
└── evidence\_refs  
└── trace\_id  
└── correlation\_id  
└── created\_at

---

## **Observability Stack**

└── Routing Latency  
└── Risk Classification Count  
└── Risk Tier Distribution  
└── Escalation Count  
└── Approval Routing Count  
└── Emergency Routing Count  
└── Supervisor Notification Count  
└── War Room Case Count  
└── Expert Review Count  
└── Conflict Case Count  
└── Routing Failure Count  
└── Queue Length  
└── Queue Delay  
└── Dropped Case Count  
└── Dead Letter Count  
└── Rule Hit Count  
└── Policy Evaluation Latency

Observability Rule:  
└── Routing decisions must be traceable, explainable, and measurable  
└── Missed high-risk routing is a critical system failure

---

## **Security & Governance Stack**

└── Routing Rule Permission  
└── Escalation Policy Permission  
└── Decision Table Change Approval  
└── DMN Version Control  
└── BPMN Version Control  
└── Policy Version Control  
└── Routing Audit  
└── Sensitive Case Redaction  
└── Role-based Case Visibility  
└── Site-based Case Visibility  
└── Expert Review Access Control  
└── War Room Access Control

Governance Rule:  
└── Routing and escalation rules must be versioned, reviewed, tested, and auditable  
└── Changes to emergency routing, high-risk routing, and approval routing require strong governance review

---

## **Runtime Boundary**

└── This layer is active in real-time and near-real-time decision routing paths  
└── It must classify and route quickly  
└── It should use bounded deterministic rules for high-risk and emergency paths  
└── It may use classifiers or models for non-final severity hints, but not as sole high-risk authority  
└── It must not perform long-running ontology reasoning, broad RAG, or heavy LLM reasoning in critical routing paths  
└── It must route uncertain high-risk cases to human review, expert review, or safe emergency policy path  
└── It must preserve traceability for every routing decision

---

## **Not Responsible For**

└── Raw sensor ingestion  
└── Defining ontology meaning  
└── Storing semantic memory  
└── Generating domain agent candidates  
└── Acting as an LLM reasoning layer  
└── Performing final policy authority alone  
└── Performing Safety Gate validation  
└── Approving high-risk actions  
└── Creating ApprovedAction independently  
└── Executing physical commands  
└── Controlling robots, PLCs, SCADA, equipment, or fleet managers  
└── Performing robot motion planning  
└── Performing fleet scheduling  
└── Replacing external control systems  
└── Replacing Human Approval Center  
└── Replacing Governance / Policy / Security Layer  
└── Replacing Unified Cyber-Physical Core

---

## **Recommended Initial Stack Mapping**

└── Routing Engine: Python rule-based decision table  
└── Policy Check: OPA / Rego for escalation and approval requirement  
└── State Machine: simple explicit state machine in Python  
└── Queue: Redis Queue or Kafka topic routing  
└── Event Bus: Kafka when multi-consumer routing is needed  
└── Priority Queue: Redis sorted set or PostgreSQL priority queue first  
└── DTOs: RoutingInputDTO, RoutingDecisionDTO, DecisionCaseDTO, EscalationCaseDTO  
└── Decision Tiers: Routine, Notice, Warning, High Risk, Critical Emergency, Exceptional  
└── Notification: FastAPI service \+ WebSocket/SSE to UI  
└── Audit: routing decision log to Layer 0  
└── UI Output: War Room Case, Approval Queue, Supervisor Notification  
└── Observability: routing latency, queue delay, risk tier counts, routing failures

Initial Rollout Rule:  
└── Start with deterministic decision table \+ OPA policy call \+ explicit DecisionCase state machine  
└── Add DMN/BPMN when routing logic needs business-readable governance  
└── Add Kafka topic routing when event volume and multi-service routing require it  
└── Add ML severity classifier only as a helper, not final high-risk authority  
└── Keep emergency routing deterministic and policy-defined

---

## **Decision Router / Escalation Core Principles**

1. Decision Router Routes; It Does Not Execute  
   └── It classifies and routes cases, but does not execute physical actions.  
2. It Protects Human Attention  
   └── Routine and notice events should not flood supervisors, War Room, or approval queues.  
3. Risk Tier Controls the Path  
   └── Routine, Notice, Warning, High Risk, Critical Emergency, and Exceptional cases must follow different processing paths.  
4. High-risk Cases Require Evidence  
   └── High-risk routing must include evidence references, current state snapshot, and reason code.  
5. Emergency Path Must Be Deterministic  
   └── Critical emergency routing must follow predefined safety policy, not open-ended LLM reasoning.  
6. Uncertainty Should Escalate, Not Disappear  
   └── Low confidence, stale state, conflicting evidence, or policy conflict should increase review or escalation.  
7. Human Safety Dominates Routing  
   └── Human safety risk outranks productivity, robot task efficiency, and schedule optimization.  
8. Legal Compliance Cannot Be Downgraded  
   └── Compliance-related risk must not be suppressed for operational convenience.  
9. Models May Assist but Must Not Govern High-risk Routing  
   └── ML or LLM outputs may enrich or summarize cases, but deterministic policy controls high-risk and emergency routes.  
10. Routing Rules Must Be Versioned  
    └── Decision tables, DMN rules, BPMN workflows, escalation policies, and OPA policies must be versioned and auditable.  
11. Every Routing Decision Needs a Reason Code  
    └── Users and auditors must know why a case was logged, displayed, notified, escalated, or sent to approval.  
12. Every Routed Case Needs Trace Context  
    └── Routing decisions must preserve event ID, candidate ID, decision case ID, trace ID, and correlation ID.  
13. Approval Routing Is Not Approval  
    └── Routing a case to approval workflow does not approve it; Governance validates authority, ApprovalDecision produces ApprovedAction, and Safety Gate validates execution readiness.  
14. War Room Is for High Signal, Not Noise  
    └── War Room should show high-risk, critical, exceptional, multi-party, or strategic cases only.  
15. Conflict Routing Must Prefer Safety  
    └── Policy conflict, evidence conflict, source conflict, or agent disagreement should route toward safer or more restrictive review.  
16. Queue Priority Must Be Explainable  
    └── Priority should be based on risk, urgency, safety impact, compliance impact, state freshness, evidence, and escalation age.  
17. Routing Must Be Observable  
    └── Routing latency, queue delay, risk distribution, escalation count, and routing failure must be monitored.  
18. Missed High-risk Routing Is Critical Failure  
    └── The system must detect and alert if high-risk events are dropped, delayed, or misrouted.  
19. Decision Router Must Not Become a Reasoning Bottleneck  
    └── It should use bounded rules, cached context, and lightweight policy calls instead of heavy reasoning in critical paths.  
20. Decision Router Enables Safe Scaling  
    └── Its purpose is to let many agents and many events exist without overwhelming humans, safety gates, or execution systems.
