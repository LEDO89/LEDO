# **Ontology Centric “Distributed Domain Agent” Stack Mapping**

## **Layer 7\. Distributed Domain Agent Layer**

─ Core Position  
└── Distributed Domain Agent Layer is the distributed intelligence layer of the ontology-centric system  
└── It contains domain-specific agents that interpret site conditions and generate structured alerts, action candidates, escalation cases, and decision cases  
└── It uses SLMs, local models, classifiers, rules, ontology guards, policy guards, and evidence binders  
└── It does not act as a central Chief LLM  
└── It does not make final execution decisions  
└── It does not approve high-risk actions  
└── It does not directly control robots, machines, PLCs, SCADA, or fleet managers  
└── It proposes structured candidates that must pass Decision Router, Governance, Safety Gate, and approved cyber-physical lifecycle

---

## **Core Role**

└── Interpret current site conditions using domain-specific logic and models  
└── Read verified current state from Real-Time World State Layer  
└── Retrieve context from Knowledge & Semantic Memory Layer when needed  
└── Ground entities, actions, risks, tasks, capabilities, and evidence to ontology definitions  
└── Generate structured alerts, action candidates, escalation cases, and decision cases  
└── Bind evidence from sensors, graphs, logs, documents, historical events, and world state  
└── Apply ontology guard and policy guard before emitting candidates  
└── Maintain lightweight BDI-style internal state for domain reasoning  
└── Send structured outputs to Decision Router / Escalation Layer  
└── Support distributed domain intelligence without creating one central LLM bottleneck

---

## **Core Technologies**

└── SLM  
└── LoRA  
└── TinyML  
└── Vision Models  
└── Local Classifiers  
└── ONNX Runtime  
└── TensorRT  
└── Ollama  
└── vLLM  
└── LangGraph-style Runtime  
└── BDI-lite  
└── Rule Engine  
└── Ontology Guard  
└── Policy Guard  
└── Evidence Binder  
└── Agent Registry  
└── Agent Scheduler  
└── Agent Lifecycle Manager  
└── Agent Communication Bus  
└── Pydantic DTOs  
└── Async Runtime  
└── Message Broker

---

## **Optional Model Serving Infrastructure**

└── vLLM Multi-LoRA Serving  
└── Centralized Adapter Serving  
└── S-LoRA-style Adapter Serving  
└── Multi-tenant Model Serving  
└── Model Router  
└── Adapter Registry  
└── Model Version Registry  
└── Prompt Template Registry  
└── Model Evaluation Pipeline  
└── Model Monitoring

Boundary:  
└── LoRA is used for domain-specific agent specialization  
└── It does not imply that every edge robot or machine dynamically swaps LoRA adapters  
└── Multi-LoRA serving is an infrastructure optimization when centralized model serving requires many domain adapters  
└── Edge devices should use stable local models, TinyML, classifiers, or narrow SLMs when appropriate

---

## **Domain Agent Stack**

└── Safety Agent  
└── Worker Agent  
└── Equipment Agent  
└── Robot Agent  
└── Planning Agent  
└── Compliance Agent  
└── Resource Agent  
└── Supervisor Agent  
└── Audit Agent  
└── Inspection Agent  
└── Risk Agent  
└── Zone Agent  
└── Schedule Agent  
└── Document Agent  
└── Emergency Agent

Agent Role Examples:  
└── Safety Agent detects unsafe situations and creates safety-related ActionCandidates  
└── Worker Agent interprets worker state, location, certification, and risk exposure  
└── Equipment Agent interprets equipment status, abnormal signals, and maintenance risk  
└── Robot Agent interprets robot telemetry, task state, capability, and external fleet feedback  
└── Planning Agent proposes task replanning candidates  
└── Compliance Agent checks permit, inspection, and regulation context  
└── Audit Agent checks whether decisions, approvals, and execution events are traceable  
└── Inspection Agent supports inspection workflow and evidence collection

---

## **Agent Internal Structure Stack**

└── Domain Model  
└── BDI-lite  
└── Ontology Guard  
└── Policy Guard  
└── Evidence Binder  
└── Output Formatter  
└── Agent State Store  
└── Agent Memory Access  
└── Agent Tool Interface  
└── Agent Runtime Context  
└── Agent Observability Hook

Internal Flow:  
└── Receive event or state update  
└── Load current world state  
└── Retrieve required semantic memory  
└── Ground involved entities to ontology IRIs  
└── Interpret condition using local model, rule, classifier, or SLM  
└── Build belief snapshot  
└── Evaluate policy-based goal  
└── Generate candidate intention  
└── Validate through ontology guard  
└── Check policy guard  
└── Bind evidence  
└── Emit structured output

---

## **Domain Model Stack**

└── SLM  
└── LoRA Adapter  
└── Local Model  
└── TinyML Model  
└── Vision Model  
└── Local Classifier  
└── Rule-based Classifier  
└── Anomaly Detector  
└── Risk Classifier  
└── Intent Classifier  
└── Summarizer  
└── Candidate Generator  
└── Natural Language Interpreter  
└── Model Version  
└── Model Confidence Score

Domain Model Usage:  
└── Classification  
└── Summarization  
└── Candidate generation  
└── Natural language interpretation  
└── Vision-based detection  
└── Similar pattern recognition  
└── Incident summarization  
└── Risk signal interpretation

Boundary:  
└── Domain models generate interpretations and candidates  
└── Model output is not evidence by itself  
└── Model output is not semantic truth  
└── Model output is not execution authority

---

## **BDI-lite Stack**

└── Belief  
└── Desire  
└── Intention  
└── Belief Snapshot  
└── Goal Context  
└── Candidate Intention  
└── Policy-based Goal  
└── Evidence-linked Belief  
└── Freshness-aware Belief  
└── Confidence-aware Belief  
└── Intention Validation

BDI-lite Meaning:  
└── Belief \= verified current state  
└── Desire \= policy-based goal  
└── Intention \= candidate action

Example:  
└── Belief: Worker\_17 is currently inside Zone\_A and Zone\_A has high risk  
└── Desire: Reduce human safety risk according to safety policy  
└── Intention: Propose ACTION\_EVACUATE or ACTION\_LOCK\_ZONE as ActionCandidate

Boundary:  
└── BDI-lite is an internal agent reasoning pattern  
└── It is not a central BDI decision engine  
└── Intention is only a candidate, not an execution command

---

## **Ontology Guard Stack**

└── Object Type Validation  
└── Action Type Validation  
└── Capability Validation  
└── Relation Validation  
└── Constraint Validation  
└── IRI Grounding Check  
└── Target Node Validation  
└── Required Property Check  
└── Domain / Range Check  
└── Action Preconditions Check  
└── Interface Contract Check  
└── World State Binding Check  
└── SHACL Target Validation optional

Ontology Guard Rule:  
└── Agent output must use ontology-defined object types, link types, event types, action types, capability types, and interface contracts  
└── Unknown or ungrounded entity references must be blocked, quarantined, or escalated  
└── Unknown action types must not enter the execution pipeline

---

## **Policy Guard Stack**

└── Safety Rule  
└── Authorization Rule  
└── Approval Rule  
└── Emergency Rule  
└── Compliance Rule  
└── Privacy Rule  
└── Zone Access Rule  
└── Robot Operation Rule  
└── Equipment Protection Rule  
└── Human Safety Priority Rule  
└── Required Approval Check  
└── Policy Sensitivity Check  
└── Escalation Requirement Check  
└── OPA / Rego Policy Call optional

Policy Guard Boundary:  
└── Policy Guard performs pre-checks before emitting candidates  
└── It does not replace Governance / Policy / Security Layer  
└── It does not replace Safety Gate final validation  
└── It helps prevent obviously invalid or unsafe candidates from being emitted

---

## **Evidence Binder Stack**

└── Sensor Evidence  
└── Graph Evidence  
└── Log Evidence  
└── Document Evidence  
└── World State Evidence  
└── Historical Event Evidence  
└── Inspection Evidence  
└── Incident Evidence  
└── Policy Evidence  
└── Source Reliability  
└── Confidence Score  
└── Evidence Timestamp  
└── Evidence Freshness  
└── Evidence Chain  
└── Evidence Reference ID  
└── Provenance Link

Evidence Binder Rule:  
└── Every high-risk candidate must include evidence references  
└── Agent output without sufficient evidence must be downgraded, blocked, or escalated  
└── LLM text is not evidence unless linked to source evidence and ontology grounding

---

## **Agent Output Stack**

└── Alert  
└── ActionCandidate  
└── EscalationCase  
└── DecisionCase  
└── EvidenceBundle  
└── RiskSignalInterpretation  
└── RecommendationSummary  
└── InspectionFinding  
└── ComplianceFinding  
└── AnomalyReport  
└── HumanReviewRequest

Output Rule:  
└── Agent outputs are structured candidates, not execution commands  
└── Outputs must include ontology references, target nodes, evidence, confidence, risk hint, and trace context  
└── Outputs are routed to Decision Router / Escalation Layer, not directly to physical systems

---

## **ActionCandidate Stack**

└── action\_candidate\_id  
└── action\_type  
└── target\_node\_id  
└── target\_node\_type  
└── source\_agent\_id  
└── source\_event\_id  
└── belief\_snapshot\_id  
└── risk\_hint  
└── priority\_hint  
└── required\_capability  
└── required\_approval\_hint  
└── precondition\_summary  
└── constraint\_summary  
└── evidence\_refs  
└── confidence\_score  
└── ontology\_validation\_status  
└── policy\_precheck\_status  
└── freshness\_status  
└── created\_at  
└── trace\_id  
└── correlation\_id

ActionCandidate Rule:  
└── ActionCandidate is not ApprovedAction  
└── ActionCandidate must pass Decision Router, Governance, Safety Gate, and approved lifecycle before execution

---

## **DecisionCase Generation Stack**

└── DecisionCase Draft  
└── Candidate Actions  
└── Risk Context  
└── Evidence Bundle  
└── Target Entity Context  
└── Policy Context  
└── World State Snapshot  
└── Graph Context  
└── Historical Incident Context  
└── Required Approval Hint  
└── Escalation Hint  
└── Agent Explanation  
└── Trace Context

DecisionCase Rule:  
└── Agents may create draft decision cases  
└── Decision Router classifies routing tier  
└── Governance and approval determine whether candidate actions can become ApprovedAction records  
└── Safety Gate later determines whether an ApprovedAction can receive SafetyGatePass for execution readiness

---

## **Agent Registry Stack**

└── Agent ID  
└── Agent Name  
└── Agent Type  
└── Domain Scope  
└── Site Scope  
└── Capability Scope  
└── Input Event Types  
└── Output Types  
└── Model Version  
└── Policy Version  
└── Ontology Version  
└── Health Status  
└── Owner  
└── Permission Scope  
└── Deployment Location  
└── Runtime Status

Registry Rule:  
└── Every agent must be registered, versioned, scoped, monitored, and permission-controlled  
└── Unknown agents must not submit operational candidates

---

## **Agent Scheduler Stack**

└── Event-triggered Scheduling  
└── Time-based Scheduling  
└── Priority Queue  
└── Risk-based Scheduling  
└── Agent Task Queue  
└── Backpressure Control  
└── Concurrency Limit  
└── Timeout Policy  
└── Retry Policy  
└── Dead Letter Queue  
└── Escalation on Failure  
└── Workload Balancing

Scheduling Rule:  
└── High-risk events should be prioritized  
└── Low-risk enrichment tasks should not block critical safety agent processing  
└── Agents must respect runtime latency budgets

---

## **Agent Lifecycle Manager Stack**

└── Agent Start  
└── Agent Stop  
└── Agent Pause  
└── Agent Resume  
└── Agent Health Check  
└── Agent Heartbeat  
└── Agent Version Upgrade  
└── Agent Rollback  
└── Agent Configuration Update  
└── Model Version Update  
└── Policy Version Update  
└── Ontology Version Compatibility Check  
└── Agent Failure Recovery  
└── Agent Deactivation

Lifecycle Rule:  
└── Agents must be lifecycle-managed like operational services  
└── Model, policy, ontology, and prompt versions must be tracked  
└── Agent upgrade should not silently change safety-critical behavior

---

## **Agent Communication Bus Stack**

└── Message Broker  
└── Kafka Topic  
└── Redis Stream optional  
└── NATS optional  
└── Pub/Sub  
└── Agent Event  
└── Agent Command  
└── Agent Status  
└── Agent Output Event  
└── Agent Heartbeat Event  
└── Agent Task Event  
└── Correlation ID  
└── Causation ID

Communication Rule:  
└── Agents communicate through typed events and service APIs  
└── Free-form agent-to-agent text should not directly drive operational decisions  
└── Agent communication must be observable and auditable

---

## **Model Serving Stack**

└── Ollama for local model serving  
└── vLLM for centralized high-throughput inference  
└── ONNX Runtime for optimized local inference  
└── TensorRT for GPU-optimized inference  
└── TinyML runtime for edge models  
└── Model Router  
└── Model Registry  
└── Adapter Registry  
└── Inference API  
└── Model Version Tracking  
└── Inference Latency Monitoring  
└── Model Output Logging  
└── Safety Filter optional

Model Serving Rule:  
└── Use the smallest sufficient model for the domain task  
└── Use local classifiers or TinyML when simple detection is enough  
└── Use SLM / LoRA when domain language or reasoning is needed  
└── Use larger model serving only when the task justifies the cost and latency

---

## **Vision Agent Stack**

└── Camera Input  
└── Frame Sampling  
└── Object Detection  
└── PPE Detection  
└── Worker Detection  
└── Equipment Detection  
└── Zone Intrusion Detection  
└── Hazard Detection  
└── Pose Estimation optional  
└── Vision Confidence Score  
└── Vision Evidence Snapshot  
└── Event Generation  
└── Evidence Binding

Vision Boundary:  
└── Vision model output is a detection signal  
└── It must be fused with world state, ontology grounding, confidence, and policy before high-risk use  
└── Vision model output alone must not trigger physical execution

---

## **TinyML / Edge Agent Stack**

└── Edge Sensor Model  
└── TinyML Classifier  
└── On-device Anomaly Detection  
└── Local Threshold Detection  
└── Edge MQTT Publisher  
└── Edge Confidence Score  
└── Edge Event Summary  
└── Edge Power Constraint  
└── Edge Latency Constraint  
└── Edge Model Version  
└── Edge Update Policy

TinyML Rule:  
└── TinyML should detect simple, local, low-latency patterns  
└── Edge outputs must still be normalized and grounded by central world state pipeline  
└── Edge output is not final operational authority

---

## **Rule Engine Stack**

└── Domain Rule  
└── Safety Rule  
└── Risk Rule  
└── Threshold Rule  
└── Pattern Rule  
└── Candidate Generation Rule  
└── Escalation Rule  
└── Rule Version  
└── Rule Test  
└── Rule Explanation  
└── Rule Evaluation Trace

Rule Engine Usage:  
└── Fast deterministic checks  
└── Safety condition detection  
└── Candidate generation for known scenarios  
└── Pre-filtering before model inference  
└── Reducing unnecessary LLM / SLM calls

Rule Engine Boundary:  
└── Agent rule engine supports candidate generation  
└── Governance policy and Safety Gate validation remain separate authority layers

---

## **Agent Memory Access Stack**

└── Current World State Access  
└── Belief Cache Access  
└── Knowledge Graph Context Access  
└── Semantic Memory Retrieval  
└── Similar Incident Retrieval  
└── Document Evidence Retrieval  
└── Policy Context Retrieval  
└── Prior Action Candidate History  
└── Prior Decision Case History  
└── Execution Feedback History

Memory Access Rule:  
└── Agents must prefer fresh Layer 6 current state for operational facts  
└── Agents may retrieve Layer 5 memory for context and evidence  
└── Agents must not rely on stale or ungrounded memory for high-risk candidates

---

## **Agent Observability Stack**

└── Agent Heartbeat  
└── Agent Status  
└── Agent Latency  
└── Candidate Generation Count  
└── Invalid Candidate Rate  
└── Evidence Binding Success Rate  
└── Grounding Failure Rate  
└── Policy Precheck Block Rate  
└── Escalation Rate  
└── Model Inference Latency  
└── Model Version Tracking  
└── Agent Error Count  
└── Agent Timeout Count  
└── Agent Output Trace  
└── Agent Decision Explanation

Observability Rule:  
└── Every agent must be monitored, traced, versioned, and auditable  
└── High-risk agent outputs must preserve evidence, model version, ontology version, and policy version

---

## **Security & Governance Stack**

└── Agent Identity  
└── Agent Authentication  
└── Agent Authorization  
└── Agent Permission Scope  
└── Agent Tool Permission  
└── Agent Data Access Policy  
└── Agent Output Policy  
└── Agent Model Approval  
└── Agent Version Approval  
└── Agent Prompt Version  
└── Agent Audit Record  
└── Agent Deactivation Policy

Security Rule:  
└── Agents must have scoped identity and permissions  
└── Agents must not access data, tools, or action types outside their domain scope  
└── Agents must not approve their own high-risk candidates

---

## **Runtime Boundary**

└── This layer is active in real-time and near-real-time interpretation paths  
└── Agents consume current state, events, memory, rules, models, ontology contracts, and policy context  
└── Agents generate structured outputs only  
└── Agents must not become final decision authority  
└── Agents must not directly dispatch execution requests to external control systems  
└── High-risk agent outputs must pass Decision Router, Governance, Safety Gate, and approved execution lifecycle  
└── Agent runtime must be bounded by latency, confidence, evidence, and policy rules

---

## **Not Responsible For**

└── Defining ontology meaning  
└── Replacing Core Ontology Kernel  
└── Storing current operational state as source of truth  
└── Replacing Real-Time World State Layer  
└── Replacing Knowledge & Semantic Memory Layer  
└── Acting as API Gateway  
└── Acting as Governance / Policy / Security authority  
└── Performing final risk routing authority alone  
└── Approving high-risk actions  
└── Creating ApprovedAction independently  
└── Directly executing physical commands  
└── Directly controlling robots, PLCs, SCADA, equipment, or fleet managers  
└── Performing robot motion planning  
└── Performing fleet scheduling  
└── Bypassing Safety Gate  
└── Treating LLM / SLM output as truth  
└── Treating model confidence as sufficient evidence by itself

---

## **Recommended Initial Stack Mapping**

└── Agent Runtime: Python async services \+ LangGraph-style workflow where useful  
└── Local LLM / SLM Serving: Ollama  
└── Model Optimization: ONNX Runtime later  
└── Vision: simple classifier / detection pipeline first  
└── TinyML: Arduino / edge sensor model for simple anomaly or threshold detection  
└── Rules: Python rule engine or simple declarative rule table first  
└── Agent State: Redis belief cache  
└── Agent Communication: Kafka or internal async message broker  
└── Agent Registry: PostgreSQL table first  
└── Agent Lifecycle: service health check \+ version metadata  
└── Ontology Guard: Pydantic \+ ontology action registry \+ SHACL target validation  
└── Policy Guard: OPA / Rego precheck where needed  
└── Evidence Binder: evidence\_refs from world state, graph, documents, logs, and events  
└── Output DTOs: AlertDTO, ActionCandidateDTO, EscalationCaseDTO, DecisionCaseDTO  
└── Observability: OpenTelemetry \+ structured logs \+ agent metrics

Initial Rollout Rule:  
└── Start with 2 or 3 agents only: Safety Agent, Equipment Agent, Robot Agent  
└── Use deterministic rules first where possible  
└── Add SLM / LoRA only where language understanding, summarization, or candidate generation truly helps  
└── Do not build a central Chief LLM  
└── Do not allow agents to issue direct execution commands  
└── Every candidate must be ontology-grounded and evidence-bound

---

## **Distributed Domain Agent Core Principles**

1. Agents Generate Candidates, Not Commands  
   └── Agent outputs are structured candidates, alerts, escalation cases, or decision cases, not execution commands.  
2. No Chief LLM Bottleneck  
   └── Intelligence should be distributed across domain agents instead of relying on one central LLM as final judge.  
3. Use the Smallest Sufficient Model  
   └── Use rules, classifiers, TinyML, SLMs, LoRA, or vision models according to task complexity, latency, and cost.  
4. BDI-lite Is Internal, Not Central Authority  
   └── Belief, Desire, and Intention help each agent structure reasoning, but final authority remains outside the agent.  
5. Belief Must Be Verified Current State  
   └── Agent belief must come from fresh world state, evidence, and grounded memory, not unsupported model output.  
6. Desire Must Be Policy-based  
   └── Agent goals must align with safety, compliance, approval rules, and operational policy.  
7. Intention Is Only a Candidate  
   └── An intended action is not executable until routed, validated, approved, and converted into approved execution lifecycle.  
8. Ontology Guard Is Mandatory  
   └── Agents must use ontology-defined object types, action types, relations, capabilities, constraints, and canonical IRIs.  
9. Policy Guard Blocks Obvious Violations  
   └── Agents should not emit candidates that clearly violate safety, authorization, approval, or emergency rules.  
10. Evidence Binder Is Required for High-risk Output  
    └── High-risk outputs must include sensor, graph, log, document, world state, or historical evidence.  
11. Model Output Is Not Evidence  
    └── LLM, SLM, vision, or classifier output must be linked to source evidence and validation before operational use.  
12. LoRA Means Domain Specialization  
    └── LoRA is for domain-specific model specialization, not automatic adapter swapping on every robot or machine.  
13. Multi-LoRA Serving Is Infrastructure Optimization  
    └── vLLM Multi-LoRA or S-LoRA-style serving should be introduced only when centralized serving requires many domain adapters.  
14. Agents Must Be Registered and Versioned  
    └── Every agent needs identity, domain scope, model version, ontology version, policy version, and runtime status.  
15. Agents Must Be Permission-scoped  
    └── Agents may access only the data, tools, action types, and domains they are authorized to use.  
16. Agents Must Not Approve Themselves  
    └── Agents cannot approve their own high-risk candidates or bypass human approval requirements.  
17. Agent Communication Must Be Typed  
    └── Agents should communicate through typed DTOs, events, and service APIs, not uncontrolled free-form messages.  
18. Freshness Controls Agent Trust  
    └── Agents must not generate high-risk candidates from stale world state or expired evidence.  
19. Agent Failures Must Be Observable  
    └── Heartbeat, latency, grounding failure, invalid candidates, model errors, and evidence failures must be monitored.  
20. Deterministic Rules Should Come Before LLM Calls  
    └── Known safety patterns and threshold checks should use deterministic rules before expensive model inference.  
21. Vision Output Must Be Fused  
    └── Vision detections must be combined with world state, ontology grounding, confidence, and evidence before high-risk use.  
22. TinyML Is Edge Signal Intelligence  
    └── TinyML detects simple local patterns but does not become final operational authority.  
23. Agent Outputs Must Be Reproducible  
    └── Candidate generation should record input state, evidence, model version, rule version, and trace ID.  
24. Agents Must Degrade Safely  
    └── If model inference, evidence retrieval, ontology grounding, or policy precheck fails, the agent must block, downgrade, or escalate.  
25. Execution Authority Belongs Outside the Agent  
    └── Execution readiness belongs to Runtime Validation and Safety Gate; actual physical execution remains outside LEDO in external control systems.
