# **Agent Vocabulary registry**

## **1\. Overview**

`agent_vocabulary_registry` is a core registry in the LEDO Ontology-Centric Cyber-Physical System. It defines and governs the controlled vocabulary for Agent Types, Agent Roles, Agent Capabilities, Agent Responsibilities, Agent Authority, and Agent Output Boundaries.

The purpose of this registry is to prevent uncontrolled agent creation, prevent agents from exceeding their authority, and ensure that agents do not behave as if they are final approvers, execution controllers, or physical command generators.

`agent_vocabulary_registry` is not a simple list of agent names.

It is an **Agent operational vocabulary and responsibility contract registry** that defines the following:

What kinds of agents may exist?

What role does each agent type have?

What inputs may the agent consume?

What outputs may the agent generate?

Which ActionCandidate types may the agent propose?

Within which policy and ontology boundaries must the agent operate?

What may the agent decide, and what must the agent never decide?

In other words, `agent_vocabulary_registry` does not turn agents into executors. It controls the meaning, responsibility, authority, and output boundary of every agent type.

---

## **2\. Core Principle**

Agent Type is a controlled operational vocabulary.

An Agent is not a physical executor.

An Agent is not a final approver.

An Agent is not the Safety Gate.

An Agent does not directly select adapters.

An Agent does not directly control external systems.

The basic role of an agent is one or more of the following:

Observe

Analyze

Interpret

Recommend

Propose candidates

Detect risk

Collect evidence

Request policy review

Generate approval requests

Generate notifications

Support audit records

The most important outputs an agent may generate are usually:

ObservationEvent

RiskSignal

EvidenceBundle

Recommendation

ActionCandidate

DecisionCaseInput

ApprovalRequest

ValidationSupportResult

AuditSupportRecord

NotificationDraft

However, agent output is not execution.

Agent Output ≠ ApprovedAction

Agent Output ≠ ExecutionRequest

Agent Output ≠ Physical Command

The final principle is:

Agents support judgment.

Ontology, Policy, Safety Gate, and Human Approval determine executability.

External Systems perform physical execution.

---

## **3\. Position in the LEDO Architecture**

`agent_vocabulary_registry` sits between the Distributed Domain Agent Layer and the Governance / Ontology / Action Registry layers.

Core Ontology Kernel Layer

        ↓

Knowledge & Semantic Memory Layer

        ↓

Real-Time World State Layer

        ↓

Distributed Domain Agent Layer

        ↓

agent\_vocabulary\_registry validation

        ↓

ActionCandidate / RiskSignal / EvidenceBundle generation

        ↓

Decision Router / Escalation Layer

        ↓

Policy / Approval / Safety Gate

        ↓

ApprovedAction

        ↓

ExecutionRequest

Before an agent can operate inside the system, its Agent Type must be registered in `agent_vocabulary_registry`.

---

## **4\. Purpose**

The purpose of `agent_vocabulary_registry` is to ensure the following:

1. Prevent the use of unregistered Agent Types  
2. Control the meaning and role of each Agent Type  
3. Define allowed input scopes per Agent Type  
4. Define allowed output scopes per Agent Type  
5. Restrict which Action Types each Agent Type may propose  
6. Restrict ontology scopes accessible by each Agent Type  
7. Restrict evidence types each Agent Type may reference  
8. Restrict tools, models, and runtime environments each Agent Type may use  
9. Define the decision authority boundary of each Agent Type  
10. Prevent agents from crossing into the physical execution boundary  
11. Manage Agent Type lifecycle and versioning  
12. Provide traceability for audit of agent output  
13. Prevent Domain Modules from creating arbitrary agents outside the registry

---

## **5\. Core Distinctions**

### **5.1 Agent Vocabulary**

Agent Vocabulary is the controlled vocabulary of Agent Types and Roles allowed in the system.

Examples:

SAFETY\_AGENT

ROBOT\_AGENT

EQUIPMENT\_AGENT

WORKER\_AGENT

INSPECTION\_AGENT

PLANNING\_AGENT

COMPLIANCE\_AGENT

SUPERVISOR\_AGENT

AUDIT\_AGENT

NOTIFICATION\_AGENT

This is not a runtime agent instance. It defines what kinds of agents are allowed to exist.

---

### **5.2 Agent Type**

`Agent Type` refers to a class of agents with a defined role and responsibility.

Examples:

Safety Risk Detection Agent

Robot Dispatch Recommendation Agent

Equipment Status Monitoring Agent

Worker Proximity Analysis Agent

Inspection Request Agent

Compliance Review Agent

Agent Type defines what kind of function an agent may perform.

---

### **5.3 Agent Instance**

`Agent Instance` is an individual agent running at runtime.

Examples:

safety\_agent\_site\_A\_001

robot\_agent\_zone\_03\_002

inspection\_agent\_tower\_B\_001

`agent_vocabulary_registry` defines the controlled vocabulary for Agent Types and Roles.

The runtime status, heartbeat, deployment, health, and scaling information of actual agent instances should be managed by a separate `agent_runtime_registry` or `agent_instance_registry`.

---

### **5.4 Agent Role**

Agent Role defines the functional role performed by the agent.

Examples:

observer

analyzer

recommender

validator

escalator

evidence\_collector

risk\_detector

workflow\_assistant

audit\_assistant

One Agent Type may have multiple roles.

However, having a role does not mean that the agent has execution authority.

---

### **5.5 Agent Capability**

Agent Capability defines what the agent can do.

Examples:

detect\_hazard

analyze\_worker\_proximity

recommend\_stop\_work

collect\_sensor\_evidence

generate\_action\_candidate

classify\_risk\_level

summarize\_incident

request\_inspection

Capabilities must be explicitly registered.

An agent must not use unregistered capabilities.

---

## **6\. Scope**

`agent_vocabulary_registry` controls the following fields:

agent\_type\_id: string

canonical\_name: string

display\_name: string

description: string

semantic\_iri: string

agent\_category: string

agent\_roles:

  \- string

version: string

status: draft | active | deprecated | migration\_required | retired | blocked

allowed\_input\_event\_types:

  \- string

allowed\_observation\_types:

  \- string

allowed\_evidence\_types:

  \- string

allowed\_output\_types:

  \- string

allowed\_action\_type\_refs:

  \- string

allowed\_decision\_case\_refs:

  \- string

allowed\_policy\_refs:

  \- string

allowed\_ontology\_scopes:

  \- string

allowed\_tool\_refs:

  \- string

allowed\_model\_refs:

  \- string

runtime\_environment: edge | site\_server | central | cloud | hybrid

authority\_level: observe\_only | analyze\_only | recommend | propose\_action | request\_approval | validate\_support | audit\_only

human\_approval\_required: boolean

execution\_boundary: string

decision\_boundary: string

safety\_boundary: string

owner\_module: string

owner\_team: string

source\_document: string

created\_at: datetime

updated\_at: datetime

deprecated\_since: datetime | null

replacement\_agent\_type\_id: string | null

---

## **7\. Non-Scope**

`agent_vocabulary_registry` does not define the following:

1. Runtime health of actual agent instances  
2. Deployment status of agent processes  
3. Container orchestration state  
4. GPU / CPU resource allocation  
5. Full LLM prompt content  
6. Complete model training datasets  
7. Low-level robot control  
8. PLC / SCADA commands  
9. Physical emergency stop logic  
10. Human approval authority itself  
11. Adapter instance selection  
12. External system execution logic  
13. Full raw sensor data processing algorithms  
14. Site-specific threshold values

These responsibilities belong to the following modules or systems:

agent\_runtime\_registry

model\_registry

tool\_registry

policy\_registry

approval\_registry

adapter\_registry

external\_system\_registry

runtime\_validation\_registry

domain\_module

safety-rated controller

PLC / SCADA / robot middleware

---

## **8\. Agent Category Model**

Agent Types should be classified by category.

Recommended categories:

SAFETY\_AGENT

ROBOT\_AGENT

EQUIPMENT\_AGENT

WORKER\_AGENT

ZONE\_AGENT

INSPECTION\_AGENT

PLANNING\_AGENT

COMPLIANCE\_AGENT

RESOURCE\_AGENT

NOTIFICATION\_AGENT

SUPERVISOR\_AGENT

AUDIT\_AGENT

DATA\_AGENT

DIGITAL\_TWIN\_AGENT

Examples:

agent\_type\_id: SAFETY\_RISK\_AGENT

agent\_category: SAFETY\_AGENT

agent\_type\_id: ROBOT\_DISPATCH\_AGENT

agent\_category: ROBOT\_AGENT

agent\_type\_id: EQUIPMENT\_STATUS\_AGENT

agent\_category: EQUIPMENT\_AGENT

agent\_type\_id: INSPECTION\_REQUEST\_AGENT

agent\_category: INSPECTION\_AGENT

Agent Category is important because it determines the ontology scope, evidence types, policy references, Action Types, and runtime validation references the agent may access.

---

## **9\. Authority Level Model**

Agents must be strictly limited by authority level.

Recommended authority levels:

observe\_only

analyze\_only

recommend

propose\_action

request\_approval

validate\_support

audit\_only

### **9.1 observe\_only**

The agent may only observe.

May generate ObservationEvent

Must not generate ActionCandidate

---

### **9.2 analyze\_only**

The agent may generate analysis results.

May generate RiskSignal

May generate Recommendation

Must not generate ActionCandidate

---

### **9.3 recommend**

The agent may generate recommendations.

May generate Recommendation

May generate ActionCandidate only under restricted conditions

---

### **9.4 propose\_action**

The agent may propose ActionCandidates.

May generate ActionCandidate

Must not generate ApprovedAction

Must not generate ExecutionRequest

---

### **9.5 request\_approval**

The agent may generate approval requests.

May generate ApprovalRequest

Human approval is required

---

### **9.6 validate\_support**

The agent may support validation.

May generate ValidationSupportResult

Must not make the final Safety Gate decision

---

### **9.7 audit\_only**

The agent may only support audit and traceability.

May generate AuditSupportRecord

Must not generate ActionCandidate

---

## **10\. Agent Output Boundary**

The outputs an agent may generate must be explicitly restricted.

Allowed output examples:

ObservationEvent

RiskSignal

EvidenceBundle

Recommendation

ActionCandidate

DecisionCaseInput

ApprovalRequest

ValidationSupportResult

AuditSupportRecord

NotificationDraft

Forbidden outputs:

ApprovedAction

ExecutionRequest

ExternalControlRequest

PhysicalCommand

PLCCommand

RobotMotionPrimitive

SCADACommand

EmergencyStopCommand

The core rule is:

Agents may create candidates and evidence.

Agents must not create approvals or execution commands.

---

## **11\. Registry Entry Schema**

Each Agent Vocabulary Registry entry should follow this structure:

agent\_type\_id: string

canonical\_name: string

display\_name: string

description: string

semantic\_iri: string

agent\_category: string

agent\_roles:

  \- string

version: string

status: draft | active | deprecated | migration\_required | retired | blocked

authority\_level: string

human\_approval\_required: boolean

allowed\_input\_event\_types:

  \- string

allowed\_observation\_types:

  \- string

allowed\_evidence\_types:

  \- string

allowed\_output\_types:

  \- string

allowed\_action\_type\_refs:

  \- string

allowed\_policy\_refs:

  \- string

allowed\_ontology\_scopes:

  \- string

allowed\_tool\_refs:

  \- string

allowed\_model\_refs:

  \- string

runtime\_environment: edge | site\_server | central | cloud | hybrid

decision\_boundary: string

execution\_boundary: string

safety\_boundary: string

precondition\_refs:

  \- string

invariant\_refs:

  \- string

audit\_event\_refs:

  \- string

owner\_module: string

owner\_team: string

source\_document: string

created\_at: datetime

updated\_at: datetime

deprecated\_since: datetime | null

replacement\_agent\_type\_id: string | null

---

## **12\. Example Registry Entry: SAFETY\_RISK\_AGENT**

agent\_type\_id: SAFETY\_RISK\_AGENT

canonical\_name: safety\_risk\_agent

display\_name: Safety Risk Agent

description: An agent type that analyzes site world state, sensor snapshots, worker locations, and hazard signals to detect safety risks and propose RiskSignals or ActionCandidates.

semantic\_iri: ledo:SafetyRiskAgent

agent\_category: SAFETY\_AGENT

agent\_roles:

  \- observer

  \- analyzer

  \- risk\_detector

  \- action\_candidate\_proposer

version: 1.0.0

status: active

authority\_level: propose\_action

human\_approval\_required: true

allowed\_input\_event\_types:

  \- WorkerLocationUpdated

  \- HazardDetected

  \- ZoneStatusChanged

  \- EquipmentStatusChanged

  \- SensorSnapshotUpdated

allowed\_observation\_types:

  \- worker\_location\_observation

  \- hazard\_observation

  \- zone\_condition\_observation

  \- equipment\_condition\_observation

allowed\_evidence\_types:

  \- hazard\_detection\_snapshot

  \- worker\_location\_snapshot

  \- risk\_assessment\_snapshot

  \- sensor\_freshness\_snapshot

allowed\_output\_types:

  \- ObservationEvent

  \- RiskSignal

  \- EvidenceBundle

  \- Recommendation

  \- ActionCandidate

allowed\_action\_type\_refs:

  \- action:STOP\_WORK

  \- action:LOCK\_ZONE

  \- action:NOTIFY\_MANAGER

  \- action:REQUEST\_INSPECTION

allowed\_policy\_refs:

  \- policy:worker\_safety\_policy

  \- policy:hazard\_zone\_policy

  \- policy:stop\_work\_policy

  \- policy:safety\_escalation\_policy

allowed\_ontology\_scopes:

  \- ledo:Worker

  \- ledo:WorkZone

  \- ledo:Hazard

  \- ledo:Equipment

  \- ledo:SafetyEvent

allowed\_tool\_refs:

  \- tool:world\_state\_query

  \- tool:risk\_score\_calculator

  \- tool:evidence\_binder

  \- tool:ontology\_lookup

allowed\_model\_refs:

  \- model:safety\_slm

  \- model:hazard\_classifier

  \- model:worker\_proximity\_model

runtime\_environment: site\_server

decision\_boundary: may\_propose\_safety\_action\_candidates\_only

execution\_boundary: no\_execution\_request\_generation

safety\_boundary: must\_not\_bypass\_safety\_gate\_or\_human\_approval

precondition\_refs:

  \- precondition:world\_state\_available

  \- precondition:sensor\_data\_fresh

  \- precondition:ontology\_scope\_valid

invariant\_refs:

  \- invariant:must\_not\_create\_approved\_action

  \- invariant:must\_not\_create\_execution\_request

  \- invariant:must\_not\_issue\_physical\_command

  \- invariant:must\_reference\_registered\_action\_type

audit\_event\_refs:

  \- audit:agent\_observation\_created

  \- audit:agent\_risk\_signal\_created

  \- audit:agent\_action\_candidate\_created

owner\_module: safety\_domain\_module

owner\_team: LEDO Safety Governance

source\_document: safety\_agent\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_agent\_type\_id: null

---

## **13\. Example Registry Entry: ROBOT\_DISPATCH\_AGENT**

agent\_type\_id: ROBOT\_DISPATCH\_AGENT

canonical\_name: robot\_dispatch\_agent

display\_name: Robot Dispatch Agent

description: An agent type that analyzes robot availability, task requirements, zone accessibility, and worker proximity to propose robot dispatch-related ActionCandidates.

semantic\_iri: ledo:RobotDispatchAgent

agent\_category: ROBOT\_AGENT

agent\_roles:

  \- analyzer

  \- recommender

  \- action\_candidate\_proposer

version: 1.0.0

status: active

authority\_level: propose\_action

human\_approval\_required: true

allowed\_input\_event\_types:

  \- RobotStatusUpdated

  \- TaskCreated

  \- ZoneStatusChanged

  \- WorkerLocationUpdated

  \- MissionContextUpdated

allowed\_observation\_types:

  \- robot\_availability\_observation

  \- task\_requirement\_observation

  \- zone\_accessibility\_observation

  \- worker\_proximity\_observation

allowed\_evidence\_types:

  \- robot\_availability\_snapshot

  \- zone\_accessibility\_snapshot

  \- worker\_proximity\_snapshot

  \- mission\_context\_snapshot

allowed\_output\_types:

  \- Recommendation

  \- EvidenceBundle

  \- ActionCandidate

allowed\_action\_type\_refs:

  \- action:DISPATCH\_ROBOT

  \- action:REPLAN\_ROUTE

  \- action:PAUSE\_MISSION

  \- action:RETURN\_TO\_BASE

  \- action:NOTIFY\_MANAGER

allowed\_policy\_refs:

  \- policy:robot\_dispatch\_policy

  \- policy:worker\_proximity\_policy

  \- policy:zone\_access\_policy

  \- policy:robot\_safety\_policy

allowed\_ontology\_scopes:

  \- ledo:Robot

  \- ledo:RobotFleet

  \- ledo:WorkZone

  \- ledo:TaskLocation

  \- ledo:Mission

allowed\_tool\_refs:

  \- tool:robot\_status\_query

  \- tool:world\_state\_query

  \- tool:ontology\_lookup

  \- tool:mission\_context\_builder

allowed\_model\_refs:

  \- model:robot\_dispatch\_slm

  \- model:route\_risk\_classifier

runtime\_environment: site\_server

decision\_boundary: may\_recommend\_robot\_mission\_intent\_only

execution\_boundary: must\_not\_generate\_robot\_motion\_primitives

safety\_boundary: must\_use\_robot\_fleet\_manager\_and\_safety\_gate

precondition\_refs:

  \- precondition:robot\_status\_available

  \- precondition:target\_zone\_identified

  \- precondition:mission\_goal\_valid

invariant\_refs:

  \- invariant:must\_not\_bypass\_robot\_fleet\_manager

  \- invariant:must\_not\_generate\_motion\_primitives

  \- invariant:must\_not\_create\_execution\_request

  \- invariant:must\_reference\_registered\_action\_type

audit\_event\_refs:

  \- audit:robot\_recommendation\_created

  \- audit:robot\_action\_candidate\_created

owner\_module: robot\_domain\_module

owner\_team: LEDO Robotics Integration

source\_document: robot\_agent\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_agent\_type\_id: null

---

## **14\. Agent Lifecycle Alignment**

Agent Type is connected to the following lifecycle objects:

AgentType

    ↓

AgentConfiguration

    ↓

AgentInstance

    ↓

ObservationEvent

    ↓

RiskSignal / EvidenceBundle / Recommendation

    ↓

ActionCandidate

    ↓

DecisionCase

    ↓

Approval / SafetyGate

    ↓

ApprovedAction

    ↓

ExecutionRequest

Agent Type must remain a reference throughout the lifecycle.

Agent Type must not turn into execution authority.

Even if an Agent Instance has a high confidence score, it must not create an `ApprovedAction` or `ExecutionRequest` by itself.

---

## **15\. Validation Rules**

An Agent Type is valid only when the following conditions are satisfied:

1. `agent_type_id` exists in the registry.  
2. Its status is `active`.  
3. Agent category is declared.  
4. Agent role is declared.  
5. Authority level is declared.  
6. Allowed input event types are declared.  
7. Allowed output types are declared.  
8. Allowed ontology scope is declared.  
9. Allowed Action Type references are declared when required.  
10. Allowed evidence types are declared.  
11. Allowed policy references are declared.  
12. Decision boundary is explicit.  
13. Execution boundary is explicit.  
14. Safety boundary is explicit.  
15. Invariants are declared.  
16. Owner module is declared.  
17. Version is valid.  
18. If deprecated, replacement or migration metadata exists.

If any of these conditions are missing, the Agent Type must not be used in the operational lifecycle.

---

## **16\. Agent Output Validation**

When an agent generates output, the following validations are required:

Is the Agent Type active?

Is the Agent Instance registered under that Agent Type?

Is the Output Type allowed?

Does the referenced Action Type exist in the Action Registry?

Is the Agent allowed to propose that Action Type?

Is the required Evidence Type allowed?

Is the output within the allowed Ontology Scope?

Is the Policy Reference valid?

Does the agent exceed its authority level?

Example rule:

SAFETY\_RISK\_AGENT may propose a STOP\_WORK ActionCandidate.

However, it must not create an ApprovedAction.

It must not create an ExecutionRequest.

It must not create a PhysicalCommand.

---

## **17\. Relationship to Action Registry**

`agent_vocabulary_registry` restricts which Action Types an Agent Type may propose.

`action_registry` validates whether the Action Type itself is valid.

agent\_vocabulary\_registry:

    Is this Agent Type allowed to propose this Action Type?

action\_registry:

    Is this Action Type registered, active, and valid with respect to target, evidence, policy, and approval requirements?

Example:

agent\_type\_id: SAFETY\_RISK\_AGENT

allowed\_action\_type\_refs:

  \- action:STOP\_WORK

  \- action:LOCK\_ZONE

  \- action:NOTIFY\_MANAGER

In this case, `SAFETY_RISK_AGENT` must not propose `DISPATCH_ROBOT`.

---

## **18\. Relationship to Policy Registry**

Agents do not replace policy.

Agents may reference policy and request policy review.

However, final policy decisions must be handled by `policy_registry`, `policy_engine`, `OPA/Rego`, or the Safety Gate.

Agent:

    Detects risk and proposes the need for policy checks

Policy Engine:

    Performs actual policy pass / fail evaluation

Safety Gate:

    Performs final pre-execution safety validation

---

## **19\. Relationship to Ontology**

Every Agent Type should have a semantic IRI.

Example:

agent\_type\_id: SAFETY\_RISK\_AGENT

semantic\_iri: ledo:SafetyRiskAgent

In the ontology, it may be defined as follows:

ledo:SafetyRiskAgent

    rdf:type ledo:AgentType ;

    rdfs:subClassOf ledo:SafetyAgent ;

    ledo:hasRole ledo:RiskDetector ;

    ledo:mayProposeAction ledo:StopWorkAction ;

    ledo:usesEvidenceType ledo:HazardDetectionSnapshot ;

    ledo:hasDecisionBoundary ledo:MayProposeOnly .

The ontology provides the semantic definition of the agent.

`agent_vocabulary_registry` manages this semantic definition in the operational system through versioning, validation, boundaries, authority, and allowed output rules.

---

## **20\. Relationship to Model Registry**

Agent Types must declare which model references they are allowed to use.

Example:

allowed\_model\_refs:

  \- model:safety\_slm

  \- model:hazard\_classifier

Agent Types must not be allowed to use arbitrary models.

This is especially important in safety-critical domains.

Safety Agents must not directly generate ActionCandidates using unvalidated general LLMs.

Robot Agents must not directly invoke models that generate motion primitives.

Edge Agents must not directly use models restricted to site\_server environments.

The Model Registry manages model version, capability, evaluation score, deployment status, and safety constraints.

The Agent Vocabulary Registry references which models each Agent Type may use.

---

## **21\. Relationship to Tool Registry**

Agent Types must also be restricted by allowed tools.

Example:

allowed\_tool\_refs:

  \- tool:world\_state\_query

  \- tool:ontology\_lookup

  \- tool:evidence\_binder

Agents must not call unregistered tools.

The following tools must be strictly restricted:

execution\_dispatcher

adapter\_direct\_call

external\_system\_command\_sender

credential\_reader

policy\_override\_tool

If agents directly call execution-layer tools, the architecture collapses.

---

## **22\. Runtime Environment**

Agent Types must declare their allowed runtime environment.

Recommended values:

edge

site\_server

central

cloud

hybrid

Examples:

agent\_type\_id: WORKER\_PROXIMITY\_AGENT

runtime\_environment: edge

agent\_type\_id: PLANNING\_AGENT

runtime\_environment: central

agent\_type\_id: SAFETY\_RISK\_AGENT

runtime\_environment: site\_server

Runtime environment affects latency, privacy, safety, availability, compute resource requirements, and network dependency.

---

## **23\. Versioning and Migration**

Agent Types must be versioned.

A version change is required when any of the following changes:

1. Agent role  
2. Authority level  
3. Allowed output type  
4. Allowed Action Type  
5. Allowed policy reference  
6. Allowed ontology scope  
7. Allowed model reference  
8. Allowed tool reference  
9. Decision boundary  
10. Execution boundary  
11. Safety boundary  
12. Invariant

Status values:

draft

active

deprecated

migration\_required

retired

blocked

A deprecated Agent Type must declare:

deprecated\_since: datetime

replacement\_agent\_type\_id: string | null

migration\_notes: string

A blocked Agent Type must not be used in a new Agent Configuration or Agent Instance.

---

## **24\. Domain Extension Rule**

Domain Modules may propose new Agent Types.

However, a new Agent Type must not be used until it has gone through registration, review, versioning, boundary mapping, action mapping, policy mapping, model/tool mapping, and test generation.

Recommended flow:

Domain Module

    ↓

Agent Type Proposal

    ↓

Semantic Review

    ↓

Registry Review

    ↓

Role / Authority Mapping

    ↓

Action Type Mapping

    ↓

Evidence Mapping

    ↓

Policy Mapping

    ↓

Ontology Scope Mapping

    ↓

Model / Tool Mapping

    ↓

Boundary Review

    ↓

Test Case Generation

    ↓

Activation

Domain Modules must not bypass `agent_vocabulary_registry`.

---

## **25\. Implementation Use**

`agent_vocabulary_registry` is used to generate or validate:

1. `AgentType` enum  
2. `AgentCategory` enum  
3. `AgentRole` enum  
4. `AgentAuthorityLevel` enum  
5. Agent configuration validation  
6. Agent instance registration validation  
7. Agent output validation  
8. Permission to generate ActionCandidates  
9. Permission to generate EvidenceBundles  
10. Policy reference validation  
11. Ontology scope validation  
12. Tool access validation  
13. Model access validation  
14. Agent audit event expectations  
15. Test case generation  
16. Migration rules

Implementation must not create or run unregistered Agent Types.

---

## **26\. Recommended Code Structure**

registries/

    agent\_vocabulary\_registry/

        agent\_vocabulary\_registry.py

        agent\_vocabulary\_entry.py

        agent\_category.py

        agent\_role.py

        agent\_authority.py

        agent\_status.py

        agent\_validation.py

        agent\_errors.py

        agent\_loader.py

        agent\_migration.py

    agent\_runtime\_registry/

    action\_registry/

    evidence\_registry/

    policy\_registry/

    approval\_registry/

    model\_registry/

    tool\_registry/

    ontology\_registry/

---

## **27\. Minimal Pydantic Model**

from enum import Enum

from pydantic import BaseModel, Field

from typing import Optional

from datetime import datetime

class AgentStatus(str, Enum):

    DRAFT \= "draft"

    ACTIVE \= "active"

    DEPRECATED \= "deprecated"

    MIGRATION\_REQUIRED \= "migration\_required"

    RETIRED \= "retired"

    BLOCKED \= "blocked"

class AgentCategory(str, Enum):

    SAFETY\_AGENT \= "safety\_agent"

    ROBOT\_AGENT \= "robot\_agent"

    EQUIPMENT\_AGENT \= "equipment\_agent"

    WORKER\_AGENT \= "worker\_agent"

    ZONE\_AGENT \= "zone\_agent"

    INSPECTION\_AGENT \= "inspection\_agent"

    PLANNING\_AGENT \= "planning\_agent"

    COMPLIANCE\_AGENT \= "compliance\_agent"

    RESOURCE\_AGENT \= "resource\_agent"

    NOTIFICATION\_AGENT \= "notification\_agent"

    SUPERVISOR\_AGENT \= "supervisor\_agent"

    AUDIT\_AGENT \= "audit\_agent"

    DATA\_AGENT \= "data\_agent"

    DIGITAL\_TWIN\_AGENT \= "digital\_twin\_agent"

class AgentAuthorityLevel(str, Enum):

    OBSERVE\_ONLY \= "observe\_only"

    ANALYZE\_ONLY \= "analyze\_only"

    RECOMMEND \= "recommend"

    PROPOSE\_ACTION \= "propose\_action"

    REQUEST\_APPROVAL \= "request\_approval"

    VALIDATE\_SUPPORT \= "validate\_support"

    AUDIT\_ONLY \= "audit\_only"

class RuntimeEnvironment(str, Enum):

    EDGE \= "edge"

    SITE\_SERVER \= "site\_server"

    CENTRAL \= "central"

    CLOUD \= "cloud"

    HYBRID \= "hybrid"

class AgentVocabularyEntry(BaseModel):

    agent\_type\_id: str

    canonical\_name: str

    display\_name: str

    description: str

    semantic\_iri: str

    agent\_category: AgentCategory

    agent\_roles: list\[str\] \= Field(default\_factory=list)

    version: str

    status: AgentStatus \= AgentStatus.DRAFT

    authority\_level: AgentAuthorityLevel

    human\_approval\_required: bool \= False

    allowed\_input\_event\_types: list\[str\] \= Field(default\_factory=list)

    allowed\_observation\_types: list\[str\] \= Field(default\_factory=list)

    allowed\_evidence\_types: list\[str\] \= Field(default\_factory=list)

    allowed\_output\_types: list\[str\] \= Field(default\_factory=list)

    allowed\_action\_type\_refs: list\[str\] \= Field(default\_factory=list)

    allowed\_policy\_refs: list\[str\] \= Field(default\_factory=list)

    allowed\_ontology\_scopes: list\[str\] \= Field(default\_factory=list)

    allowed\_tool\_refs: list\[str\] \= Field(default\_factory=list)

    allowed\_model\_refs: list\[str\] \= Field(default\_factory=list)

    runtime\_environment: RuntimeEnvironment

    decision\_boundary: str

    execution\_boundary: str

    safety\_boundary: str

    precondition\_refs: list\[str\] \= Field(default\_factory=list)

    invariant\_refs: list\[str\] \= Field(default\_factory=list)

    audit\_event\_refs: list\[str\] \= Field(default\_factory=list)

    owner\_module: str

    owner\_team: str

    source\_document: str

    created\_at: datetime

    updated\_at: datetime

    deprecated\_since: Optional\[datetime\] \= None

    replacement\_agent\_type\_id: Optional\[str\] \= None

---

## **28\. Core Validation Function**

def validate\_agent\_output\_permission(

    entry: AgentVocabularyEntry,

    output\_type: str,

    action\_type\_ref: str | None \= None,

) \-\> None:

    if entry.status \!= AgentStatus.ACTIVE:

        raise InvalidAgentTypeError(

            f"Agent Type is not active: {entry.agent\_type\_id}"

        )

    if output\_type not in entry.allowed\_output\_types:

        raise AgentOutputNotAllowedError(

            f"Output type '{output\_type}' is not allowed for "

            f"Agent Type '{entry.agent\_type\_id}'"

        )

    forbidden\_outputs \= {

        "ApprovedAction",

        "ExecutionRequest",

        "ExternalControlRequest",

        "PhysicalCommand",

        "PLCCommand",

        "SCADACommand",

        "RobotMotionPrimitive",

        "EmergencyStopCommand",

    }

    if output\_type in forbidden\_outputs:

        raise AgentBoundaryViolationError(

            f"Agent Type '{entry.agent\_type\_id}' must not create '{output\_type}'"

        )

    if action\_type\_ref is not None:

        if action\_type\_ref not in entry.allowed\_action\_type\_refs:

            raise AgentActionTypeNotAllowedError(

                f"Action Type '{action\_type\_ref}' is not allowed for "

                f"Agent Type '{entry.agent\_type\_id}'"

            )

---

## **29\. Test Scenarios**

Required tests:

1\. Reject unregistered Agent Type.

2\. Reject inactive Agent Type.

3\. Reject deprecated Agent Type.

4\. Reject blocked Agent Type.

5\. Reject creation of an unauthorized output type.

6\. Reject creation of ApprovedAction.

7\. Reject creation of ExecutionRequest.

8\. Reject creation of PhysicalCommand.

9\. Reject proposal of unauthorized Action Type.

10\. Reject reference to unauthorized evidence type.

11\. Reject access to unauthorized ontology scope.

12\. Reject unauthorized tool call.

13\. Reject unauthorized model usage.

14\. Reject behavior exceeding authority level.

15\. Verify creation of agent output audit records.

---

## **30\. Final Rule**

No registered Agent Type,

no valid Agent Configuration.

No valid Agent Configuration,

no valid Agent Instance.

No valid Agent Instance,

no valid Agent Output.

If the Output Type is not allowed for the Agent,

the Output must not be created.

If the Action Type is not allowed for the Agent,

the Agent must not propose the ActionCandidate.

Agents must not create ApprovedAction.

Agents must not create ExecutionRequest.

Agents must not create PhysicalCommand.

Agents must not directly control External Systems.

`agent_vocabulary_registry` is the first deterministic control point of the LEDO Agent Layer.

This module prevents uncontrolled agent expansion, prevents agents from exceeding their role, authority, and output boundaries, and ensures that every agent behavior is aligned with the ontology, policy, action registry, evidence registry, model registry, tool registry, and audit system.

The core definition is:

Agent Vocabulary Registry

\= not a list of agent names,

but an operational contract registry that controls

agent meaning, role, authority, output, and boundary.

# **agent\_vocabulary\_registry 설계 보고서**

## **1\. 개요**

`agent_vocabulary_registry`는 LEDO Ontology-Centric Cyber-Physical System에서 사용되는 Agent Type, Agent Role, Agent Capability, Agent Responsibility, Agent Authority, Agent Output Boundary를 정의하고 통제하는 핵심 레지스트리이다.

이 모듈의 목적은 시스템 내부에서 무분별하게 agent가 생성되거나, agent가 자신의 권한을 넘어 Action을 제안하거나, 실행 책임을 가진 것처럼 동작하는 것을 방지하는 것이다.

`agent_vocabulary_registry`는 단순한 agent 이름 목록이 아니다.

이 레지스트리는 다음을 정의하는 **Agent 운영 어휘 및 책임 계약 레지스트리**이다.

어떤 종류의 Agent가 존재할 수 있는가?  
그 Agent는 어떤 역할을 가지는가?  
그 Agent는 어떤 입력을 받을 수 있는가?  
그 Agent는 어떤 출력을 생성할 수 있는가?  
그 Agent는 어떤 ActionCandidate를 제안할 수 있는가?  
그 Agent는 어떤 정책과 온톨로지 경계 안에서 동작해야 하는가?  
그 Agent는 어디까지 판단할 수 있고, 어디부터는 판단하면 안 되는가?

즉, `agent_vocabulary_registry`는 Agent를 “실행자”로 만드는 레지스트리가 아니라, **Agent의 의미, 책임, 권한, 출력 경계를 통제하는 운영 계약 레지스트리**이다.

---

## **2\. 핵심 원칙**

Agent Type은 통제된 운영 어휘이다.

Agent는 물리 실행자가 아니다.

Agent는 최종 승인자가 아니다.

Agent는 Safety Gate가 아니다.

Agent는 Adapter를 직접 선택하지 않는다.

Agent는 External System을 직접 제어하지 않는다.

Agent의 기본 역할은 다음 중 하나이다.

관찰  
분석  
해석  
후보 제안  
위험 감지  
증거 수집  
정책 검토 요청  
승인 요청 생성  
알림 생성  
감사 기록 보조

Agent가 생성할 수 있는 가장 중요한 출력은 보통 `ActionCandidate`, `DecisionCaseInput`, `RiskSignal`, `EvidenceBundle`, `Recommendation`, `Alert`, `ObservationEvent`이다.

하지만 Agent 출력은 실행이 아니다.

Agent Output ≠ ApprovedAction  
Agent Output ≠ ExecutionRequest  
Agent Output ≠ Physical Command

최종 원칙은 다음과 같다.

Agent는 판단 보조자이고,  
Ontology / Policy / Safety Gate / Human Approval이 실행 가능성을 결정하며,  
External System이 물리 실행을 수행한다.

---

## **3\. LEDO 아키텍처 내 위치**

`agent_vocabulary_registry`는 Distributed Domain Agent Layer와 Governance / Ontology / Action Registry 사이에 위치한다.

Core Ontology Kernel Layer  
        ↓  
Knowledge & Semantic Memory Layer  
        ↓  
Real-Time World State Layer  
        ↓  
Distributed Domain Agent Layer  
        ↓  
agent\_vocabulary\_registry validation  
        ↓  
ActionCandidate / RiskSignal / EvidenceBundle 생성  
        ↓  
Decision Router / Escalation Layer  
        ↓  
Policy / Approval / Safety Gate  
        ↓  
ApprovedAction  
        ↓  
ExecutionRequest

Agent가 시스템 안에서 동작하기 전에, 해당 Agent Type은 반드시 `agent_vocabulary_registry`에 등록되어 있어야 한다.

---

## **4\. 목적**

`agent_vocabulary_registry`의 목적은 다음과 같다.

1. 등록되지 않은 Agent Type 사용 방지  
2. Agent Type의 의미와 역할 통제  
3. Agent별 허용 입력 범위 정의  
4. Agent별 허용 출력 범위 정의  
5. Agent별 제안 가능한 Action Type 제한  
6. Agent별 접근 가능한 ontology scope 제한  
7. Agent별 참조 가능한 evidence type 제한  
8. Agent별 사용할 수 있는 tool / model / runtime 제한  
9. Agent별 decision authority 한계 정의  
10. Agent가 물리 실행 경계를 침범하지 못하도록 제한  
11. Agent lifecycle 및 version 관리  
12. Agent output이 audit 가능하도록 trace 기준 제공  
13. Domain Module이 임의 agent를 생성하지 못하도록 통제

---

## **5\. 핵심 구분**

### **5.1 Agent Vocabulary**

Agent Vocabulary는 시스템에서 허용되는 Agent Type과 Role의 통제된 어휘이다.

예시:

SAFETY\_AGENT  
ROBOT\_AGENT  
EQUIPMENT\_AGENT  
WORKER\_AGENT  
INSPECTION\_AGENT  
PLANNING\_AGENT  
COMPLIANCE\_AGENT  
SUPERVISOR\_AGENT  
AUDIT\_AGENT  
NOTIFICATION\_AGENT

이것은 실제 실행 중인 개별 agent instance가 아니라, 어떤 종류의 agent가 존재할 수 있는지를 정의하는 기준이다.

---

### **5.2 Agent Type**

`Agent Type`은 특정 역할과 책임을 가진 agent의 종류이다.

예시:

Safety Risk Detection Agent  
Robot Dispatch Recommendation Agent  
Equipment Status Monitoring Agent  
Worker Proximity Analysis Agent  
Inspection Request Agent  
Compliance Review Agent

Agent Type은 해당 agent가 어떤 역할을 수행할 수 있는지 정의한다.

---

### **5.3 Agent Instance**

`Agent Instance`는 실제 런타임에서 동작하는 개별 agent이다.

예시:

safety\_agent\_site\_A\_001  
robot\_agent\_zone\_03\_002  
inspection\_agent\_tower\_B\_001

`agent_vocabulary_registry`는 Agent Type과 Role의 통제 어휘를 정의한다.

실제 실행 중인 agent instance의 상태, heartbeat, deployment, health, scaling 정보는 별도의 `agent_runtime_registry` 또는 `agent_instance_registry`에서 관리하는 것이 좋다.

---

### **5.4 Agent Role**

Agent Role은 Agent가 수행하는 기능적 역할이다.

예시:

observer  
analyzer  
recommender  
validator  
escalator  
evidence\_collector  
risk\_detector  
workflow\_assistant  
audit\_assistant

하나의 Agent Type은 여러 Role을 가질 수 있다.

하지만 Role이 있다고 해서 실행 권한이 생기는 것은 아니다.

---

### **5.5 Agent Capability**

Agent Capability는 Agent가 수행할 수 있는 기능이다.

예시:

detect\_hazard  
analyze\_worker\_proximity  
recommend\_stop\_work  
collect\_sensor\_evidence  
generate\_action\_candidate  
classify\_risk\_level  
summarize\_incident  
request\_inspection

Capability는 반드시 명시적으로 등록되어야 한다.

Agent는 등록되지 않은 capability를 사용할 수 없다.

---

## **6\. Scope**

`agent_vocabulary_registry`는 다음 항목을 통제한다.

agent\_type\_id: string  
canonical\_name: string  
display\_name: string  
description: string  
semantic\_iri: string

agent\_category: string  
agent\_roles:  
  \- string

version: string  
status: draft | active | deprecated | migration\_required | retired | blocked

allowed\_input\_event\_types:  
  \- string

allowed\_observation\_types:  
  \- string

allowed\_evidence\_types:  
  \- string

allowed\_output\_types:  
  \- string

allowed\_action\_type\_refs:  
  \- string

allowed\_decision\_case\_refs:  
  \- string

allowed\_policy\_refs:  
  \- string

allowed\_ontology\_scopes:  
  \- string

allowed\_tool\_refs:  
  \- string

allowed\_model\_refs:  
  \- string

runtime\_environment: edge | site\_server | central | cloud | hybrid  
authority\_level: observe\_only | recommend | propose\_action | request\_approval | validate\_support | audit\_only  
human\_approval\_required: boolean

execution\_boundary: string  
decision\_boundary: string  
safety\_boundary: string

owner\_module: string  
owner\_team: string  
source\_document: string

created\_at: datetime  
updated\_at: datetime  
deprecated\_since: datetime | null  
replacement\_agent\_type\_id: string | null

---

## **7\. Non-Scope**

`agent_vocabulary_registry`는 다음을 정의하지 않는다.

1. 실제 agent instance의 runtime health  
2. agent process의 배포 상태  
3. container orchestration 상태  
4. GPU / CPU resource allocation  
5. 개별 LLM prompt 전문  
6. 모델 학습 데이터셋 전체  
7. low-level robot control  
8. PLC / SCADA command  
9. physical emergency stop logic  
10. human approval authority 자체  
11. adapter instance selection  
12. external system execution logic  
13. sensor raw data processing algorithm 전체  
14. 현장별 구체적 threshold 값

이러한 책임은 각각 다음 모듈에 속한다.

agent\_runtime\_registry  
model\_registry  
tool\_registry  
policy\_registry  
approval\_registry  
adapter\_registry  
external\_system\_registry  
runtime\_validation\_registry  
domain\_module  
safety-rated controller  
PLC / SCADA / robot middleware

---

## **8\. Agent Category 모델**

Agent Type은 category로 분류되어야 한다.

권장 category는 다음과 같다.

SAFETY\_AGENT  
ROBOT\_AGENT  
EQUIPMENT\_AGENT  
WORKER\_AGENT  
ZONE\_AGENT  
INSPECTION\_AGENT  
PLANNING\_AGENT  
COMPLIANCE\_AGENT  
RESOURCE\_AGENT  
NOTIFICATION\_AGENT  
SUPERVISOR\_AGENT  
AUDIT\_AGENT  
DATA\_AGENT  
DIGITAL\_TWIN\_AGENT

예시:

agent\_type\_id: SAFETY\_RISK\_AGENT  
agent\_category: SAFETY\_AGENT

agent\_type\_id: ROBOT\_DISPATCH\_AGENT  
agent\_category: ROBOT\_AGENT

agent\_type\_id: EQUIPMENT\_STATUS\_AGENT  
agent\_category: EQUIPMENT\_AGENT

agent\_type\_id: INSPECTION\_REQUEST\_AGENT  
agent\_category: INSPECTION\_AGENT

Agent Category는 agent가 참조할 수 있는 ontology scope, evidence type, policy, action type, runtime validation 범위를 결정하는 중요한 기준이 된다.

---

## **9\. Authority Level 모델**

Agent는 권한 수준에 따라 엄격히 제한되어야 한다.

권장 authority level은 다음과 같다.

observe\_only  
analyze\_only  
recommend  
propose\_action  
request\_approval  
validate\_support  
audit\_only

### **9.1 observe\_only**

관찰만 가능하다.

ObservationEvent 생성 가능  
ActionCandidate 생성 불가

---

### **9.2 analyze\_only**

분석 결과를 생성할 수 있다.

RiskSignal 생성 가능  
Recommendation 생성 가능  
ActionCandidate 생성 불가

---

### **9.3 recommend**

권고를 생성할 수 있다.

Recommendation 생성 가능  
ActionCandidate 생성은 제한적으로 가능

---

### **9.4 propose\_action**

ActionCandidate를 제안할 수 있다.

ActionCandidate 생성 가능  
ApprovedAction 생성 불가  
ExecutionRequest 생성 불가

---

### **9.5 request\_approval**

승인 요청을 생성할 수 있다.

ApprovalRequest 생성 가능  
Human Approval 필요

---

### **9.6 validate\_support**

검증 보조 역할을 수행한다.

ValidationSupportResult 생성 가능  
최종 Safety Gate 판정 불가

---

### **9.7 audit\_only**

감사 및 추적 보조만 수행한다.

AuditSupportRecord 생성 가능  
ActionCandidate 생성 불가

---

## **10\. Agent Output Boundary**

Agent가 생성할 수 있는 출력은 명확히 제한되어야 한다.

허용 가능한 출력 예시는 다음과 같다.

ObservationEvent  
RiskSignal  
EvidenceBundle  
Recommendation  
ActionCandidate  
DecisionCaseInput  
ApprovalRequest  
ValidationSupportResult  
AuditSupportRecord  
NotificationDraft

허용되면 안 되는 출력은 다음과 같다.

ApprovedAction  
ExecutionRequest  
ExternalControlRequest  
PhysicalCommand  
PLCCommand  
RobotMotionPrimitive  
SCADACommand  
EmergencyStopCommand

핵심 원칙은 다음과 같다.

Agent는 후보와 증거를 만들 수 있지만,  
승인과 실행은 만들 수 없다.

---

## **11\. Registry Entry Schema**

각 Agent Vocabulary Registry entry는 다음 구조를 따른다.

agent\_type\_id: string  
canonical\_name: string  
display\_name: string  
description: string  
semantic\_iri: string

agent\_category: string  
agent\_roles:  
  \- string

version: string  
status: draft | active | deprecated | migration\_required | retired | blocked

authority\_level: string  
human\_approval\_required: boolean

allowed\_input\_event\_types:  
  \- string

allowed\_observation\_types:  
  \- string

allowed\_evidence\_types:  
  \- string

allowed\_output\_types:  
  \- string

allowed\_action\_type\_refs:  
  \- string

allowed\_policy\_refs:  
  \- string

allowed\_ontology\_scopes:  
  \- string

allowed\_tool\_refs:  
  \- string

allowed\_model\_refs:  
  \- string

runtime\_environment: edge | site\_server | central | cloud | hybrid

decision\_boundary: string  
execution\_boundary: string  
safety\_boundary: string

precondition\_refs:  
  \- string

invariant\_refs:  
  \- string

audit\_event\_refs:  
  \- string

owner\_module: string  
owner\_team: string  
source\_document: string

created\_at: datetime  
updated\_at: datetime  
deprecated\_since: datetime | null  
replacement\_agent\_type\_id: string | null

---

## **12\. Registry Entry 예시: SAFETY\_RISK\_AGENT**

agent\_type\_id: SAFETY\_RISK\_AGENT  
canonical\_name: safety\_risk\_agent  
display\_name: Safety Risk Agent  
description: 현장 world state, sensor snapshot, worker location, hazard signal을 분석하여 안전 리스크를 감지하고 ActionCandidate 또는 RiskSignal을 제안하는 agent type이다.  
semantic\_iri: ledo:SafetyRiskAgent

agent\_category: SAFETY\_AGENT  
agent\_roles:  
  \- observer  
  \- analyzer  
  \- risk\_detector  
  \- action\_candidate\_proposer

version: 1.0.0  
status: active

authority\_level: propose\_action  
human\_approval\_required: true

allowed\_input\_event\_types:  
  \- WorkerLocationUpdated  
  \- HazardDetected  
  \- ZoneStatusChanged  
  \- EquipmentStatusChanged  
  \- SensorSnapshotUpdated

allowed\_observation\_types:  
  \- worker\_location\_observation  
  \- hazard\_observation  
  \- zone\_condition\_observation  
  \- equipment\_condition\_observation

allowed\_evidence\_types:  
  \- hazard\_detection\_snapshot  
  \- worker\_location\_snapshot  
  \- risk\_assessment\_snapshot  
  \- sensor\_freshness\_snapshot

allowed\_output\_types:  
  \- ObservationEvent  
  \- RiskSignal  
  \- EvidenceBundle  
  \- Recommendation  
  \- ActionCandidate

allowed\_action\_type\_refs:  
  \- action:STOP\_WORK  
  \- action:LOCK\_ZONE  
  \- action:NOTIFY\_MANAGER  
  \- action:REQUEST\_INSPECTION

allowed\_policy\_refs:  
  \- policy:worker\_safety\_policy  
  \- policy:hazard\_zone\_policy  
  \- policy:stop\_work\_policy  
  \- policy:safety\_escalation\_policy

allowed\_ontology\_scopes:  
  \- ledo:Worker  
  \- ledo:WorkZone  
  \- ledo:Hazard  
  \- ledo:Equipment  
  \- ledo:SafetyEvent

allowed\_tool\_refs:  
  \- tool:world\_state\_query  
  \- tool:risk\_score\_calculator  
  \- tool:evidence\_binder  
  \- tool:ontology\_lookup

allowed\_model\_refs:  
  \- model:safety\_slm  
  \- model:hazard\_classifier  
  \- model:worker\_proximity\_model

runtime\_environment: site\_server

decision\_boundary: may\_propose\_safety\_action\_candidates\_only  
execution\_boundary: no\_execution\_request\_generation  
safety\_boundary: must\_not\_bypass\_safety\_gate\_or\_human\_approval

precondition\_refs:  
  \- precondition:world\_state\_available  
  \- precondition:sensor\_data\_fresh  
  \- precondition:ontology\_scope\_valid

invariant\_refs:  
  \- invariant:must\_not\_create\_approved\_action  
  \- invariant:must\_not\_create\_execution\_request  
  \- invariant:must\_not\_issue\_physical\_command  
  \- invariant:must\_reference\_registered\_action\_type

audit\_event\_refs:  
  \- audit:agent\_observation\_created  
  \- audit:agent\_risk\_signal\_created  
  \- audit:agent\_action\_candidate\_created

owner\_module: safety\_domain\_module  
owner\_team: LEDO Safety Governance  
source\_document: safety\_agent\_contract\_v1  
created\_at: 2026-06-26T00:00:00Z  
updated\_at: 2026-06-26T00:00:00Z  
deprecated\_since: null  
replacement\_agent\_type\_id: null

---

## **13\. Registry Entry 예시: ROBOT\_DISPATCH\_AGENT**

agent\_type\_id: ROBOT\_DISPATCH\_AGENT  
canonical\_name: robot\_dispatch\_agent  
display\_name: Robot Dispatch Agent  
description: robot availability, task requirement, zone accessibility, worker proximity를 분석하여 로봇 dispatch 관련 ActionCandidate를 제안하는 agent type이다.  
semantic\_iri: ledo:RobotDispatchAgent

agent\_category: ROBOT\_AGENT  
agent\_roles:  
  \- analyzer  
  \- recommender  
  \- action\_candidate\_proposer

version: 1.0.0  
status: active

authority\_level: propose\_action  
human\_approval\_required: true

allowed\_input\_event\_types:  
  \- RobotStatusUpdated  
  \- TaskCreated  
  \- ZoneStatusChanged  
  \- WorkerLocationUpdated  
  \- MissionContextUpdated

allowed\_observation\_types:  
  \- robot\_availability\_observation  
  \- task\_requirement\_observation  
  \- zone\_accessibility\_observation  
  \- worker\_proximity\_observation

allowed\_evidence\_types:  
  \- robot\_availability\_snapshot  
  \- zone\_accessibility\_snapshot  
  \- worker\_proximity\_snapshot  
  \- mission\_context\_snapshot

allowed\_output\_types:  
  \- Recommendation  
  \- EvidenceBundle  
  \- ActionCandidate

allowed\_action\_type\_refs:  
  \- action:DISPATCH\_ROBOT  
  \- action:REPLAN\_ROUTE  
  \- action:PAUSE\_MISSION  
  \- action:RETURN\_TO\_BASE  
  \- action:NOTIFY\_MANAGER

allowed\_policy\_refs:  
  \- policy:robot\_dispatch\_policy  
  \- policy:worker\_proximity\_policy  
  \- policy:zone\_access\_policy  
  \- policy:robot\_safety\_policy

allowed\_ontology\_scopes:  
  \- ledo:Robot  
  \- ledo:RobotFleet  
  \- ledo:WorkZone  
  \- ledo:TaskLocation  
  \- ledo:Mission

allowed\_tool\_refs:  
  \- tool:robot\_status\_query  
  \- tool:world\_state\_query  
  \- tool:ontology\_lookup  
  \- tool:mission\_context\_builder

allowed\_model\_refs:  
  \- model:robot\_dispatch\_slm  
  \- model:route\_risk\_classifier

runtime\_environment: site\_server

decision\_boundary: may\_recommend\_robot\_mission\_intent\_only  
execution\_boundary: must\_not\_generate\_robot\_motion\_primitives  
safety\_boundary: must\_use\_robot\_fleet\_manager\_and\_safety\_gate

precondition\_refs:  
  \- precondition:robot\_status\_available  
  \- precondition:target\_zone\_identified  
  \- precondition:mission\_goal\_valid

invariant\_refs:  
  \- invariant:must\_not\_bypass\_robot\_fleet\_manager  
  \- invariant:must\_not\_generate\_motion\_primitives  
  \- invariant:must\_not\_create\_execution\_request  
  \- invariant:must\_reference\_registered\_action\_type

audit\_event\_refs:  
  \- audit:robot\_recommendation\_created  
  \- audit:robot\_action\_candidate\_created

owner\_module: robot\_domain\_module  
owner\_team: LEDO Robotics Integration  
source\_document: robot\_agent\_contract\_v1  
created\_at: 2026-06-26T00:00:00Z  
updated\_at: 2026-06-26T00:00:00Z  
deprecated\_since: null  
replacement\_agent\_type\_id: null

---

## **14\. Agent Lifecycle Alignment**

Agent Type은 다음 lifecycle object들과 연결된다.

AgentType  
    ↓  
AgentConfiguration  
    ↓  
AgentInstance  
    ↓  
ObservationEvent  
    ↓  
RiskSignal / EvidenceBundle / Recommendation  
    ↓  
ActionCandidate  
    ↓  
DecisionCase  
    ↓  
Approval / SafetyGate  
    ↓  
ApprovedAction  
    ↓  
ExecutionRequest

Agent Type은 lifecycle 전체에서 reference로 유지되어야 한다.

Agent Type은 실행 권한으로 변하면 안 된다.

Agent Instance가 아무리 높은 confidence score를 가지더라도, 그것만으로 `ApprovedAction`이나 `ExecutionRequest`를 만들 수 없다.

---

## **15\. Validation Rules**

Agent Type은 다음 조건을 만족할 때만 유효하다.

1. `agent_type_id`가 registry에 존재해야 한다.  
2. status가 `active`이어야 한다.  
3. agent category가 선언되어야 한다.  
4. agent role이 선언되어야 한다.  
5. authority level이 선언되어야 한다.  
6. allowed input event type이 선언되어야 한다.  
7. allowed output type이 선언되어야 한다.  
8. allowed ontology scope가 선언되어야 한다.  
9. allowed action type reference가 필요한 경우 명시되어야 한다.  
10. allowed evidence type이 선언되어야 한다.  
11. allowed policy reference가 선언되어야 한다.  
12. decision boundary가 명시되어야 한다.  
13. execution boundary가 명시되어야 한다.  
14. safety boundary가 명시되어야 한다.  
15. invariant가 선언되어야 한다.  
16. owner module이 선언되어야 한다.  
17. version이 유효해야 한다.  
18. deprecated 상태라면 replacement 또는 migration metadata가 있어야 한다.

하나라도 누락되면 해당 Agent Type은 operational lifecycle에 사용되면 안 된다.

---

## **16\. Agent Output Validation**

Agent가 output을 생성할 때는 다음 검증이 필요하다.

Agent Type이 active인가?  
Agent Instance가 해당 Agent Type으로 등록되어 있는가?  
Output Type이 허용되어 있는가?  
참조한 Action Type이 Action Registry에 존재하는가?  
해당 Agent가 그 Action Type을 제안할 권한이 있는가?  
필요한 Evidence Type이 허용되어 있는가?  
Ontology Scope를 벗어나지 않았는가?  
Policy Reference가 유효한가?  
Agent가 자신의 authority level을 초과하지 않았는가?

예시 규칙:

SAFETY\_RISK\_AGENT는 STOP\_WORK ActionCandidate를 제안할 수 있다.  
그러나 ApprovedAction을 생성할 수 없다.  
ExecutionRequest를 생성할 수 없다.  
PhysicalCommand를 생성할 수 없다.

---

## **17\. Action Registry와의 관계**

`agent_vocabulary_registry`는 Agent가 어떤 Action Type을 제안할 수 있는지 제한한다.

`action_registry`는 해당 Action Type 자체가 유효한지 검증한다.

agent\_vocabulary\_registry:  
    이 Agent Type이 이 Action Type을 제안할 권한이 있는가?

action\_registry:  
    이 Action Type은 등록되어 있고, active이며, target/evidence/policy/approval 조건을 만족하는가?

예시:

agent\_type\_id: SAFETY\_RISK\_AGENT  
allowed\_action\_type\_refs:  
  \- action:STOP\_WORK  
  \- action:LOCK\_ZONE  
  \- action:NOTIFY\_MANAGER

이 경우 `SAFETY_RISK_AGENT`는 `DISPATCH_ROBOT`을 제안하면 안 된다.

---

## **18\. Policy Registry와의 관계**

Agent는 policy를 직접 대체하지 않는다.

Agent는 policy reference를 참조할 수 있고, policy 검토를 요청할 수 있다.

그러나 최종 policy decision은 `policy_registry`, `policy_engine`, `OPA/Rego`, 또는 Safety Gate가 담당해야 한다.

Agent:  
    위험을 감지하고 policy check 필요성을 제안

Policy Engine:  
    실제 policy pass / fail 판정

Safety Gate:  
    실행 전 최종 안전 검증

---

## **19\. Ontology와의 관계**

모든 Agent Type은 semantic IRI를 가져야 한다.

예시:

agent\_type\_id: SAFETY\_RISK\_AGENT  
semantic\_iri: ledo:SafetyRiskAgent

Ontology에서는 다음과 같이 정의할 수 있다.

ledo:SafetyRiskAgent  
    rdf:type ledo:AgentType ;  
    rdfs:subClassOf ledo:SafetyAgent ;  
    ledo:hasRole ledo:RiskDetector ;  
    ledo:mayProposeAction ledo:StopWorkAction ;  
    ledo:usesEvidenceType ledo:HazardDetectionSnapshot ;  
    ledo:hasDecisionBoundary ledo:MayProposeOnly .

Ontology는 Agent의 의미론적 정의를 제공한다.

`agent_vocabulary_registry`는 이 의미론적 정의를 운영 시스템에서 사용할 수 있도록 version, validation, boundary, authority, allowed output 형태로 관리한다.

---

## **20\. Model Registry와의 관계**

Agent Type은 사용할 수 있는 model reference를 가져야 한다.

예시:

allowed\_model\_refs:  
  \- model:safety\_slm  
  \- model:hazard\_classifier

Agent Type이 아무 모델이나 사용할 수 있으면 안 된다.

특히 safety-critical domain에서는 model 사용 범위가 제한되어야 한다.

Safety Agent는 검증되지 않은 general LLM으로 직접 ActionCandidate를 생성하면 안 된다.  
Robot Agent는 motion primitive를 생성하는 모델을 직접 호출하면 안 된다.  
Edge Agent는 site\_server 전용 모델을 직접 사용하면 안 된다.

Model Registry는 모델의 version, capability, eval score, deployment status, safety constraints를 관리한다.

Agent Vocabulary Registry는 해당 Agent Type이 어떤 model을 사용할 수 있는지 참조한다.

---

## **21\. Tool Registry와의 관계**

Agent Type은 사용할 수 있는 tool도 제한되어야 한다.

예시:

allowed\_tool\_refs:  
  \- tool:world\_state\_query  
  \- tool:ontology\_lookup  
  \- tool:evidence\_binder

Agent는 등록되지 않은 tool을 호출하면 안 된다.

특히 다음 tool은 엄격히 제한되어야 한다.

execution\_dispatcher  
adapter\_direct\_call  
external\_system\_command\_sender  
credential\_reader  
policy\_override\_tool

Agent가 실행계 tool을 직접 호출하면 구조가 무너진다.

---

## **22\. Runtime Environment**

Agent Type은 실행 가능한 runtime environment를 선언해야 한다.

권장 값:

edge  
site\_server  
central  
cloud  
hybrid

예시:

agent\_type\_id: WORKER\_PROXIMITY\_AGENT  
runtime\_environment: edge

agent\_type\_id: PLANNING\_AGENT  
runtime\_environment: central

agent\_type\_id: SAFETY\_RISK\_AGENT  
runtime\_environment: site\_server

Runtime environment는 latency, privacy, safety, availability, compute resource, network dependency에 영향을 준다.

---

## **23\. Versioning 및 Migration**

Agent Type은 반드시 versioning되어야 한다.

다음 항목 중 하나라도 변경되면 version 변경이 필요하다.

1. Agent role 변경  
2. authority level 변경  
3. allowed output type 변경  
4. allowed action type 변경  
5. allowed policy reference 변경  
6. allowed ontology scope 변경  
7. allowed model reference 변경  
8. allowed tool reference 변경  
9. decision boundary 변경  
10. execution boundary 변경  
11. safety boundary 변경  
12. invariant 변경

Status 값:

draft  
active  
deprecated  
migration\_required  
retired  
blocked

Deprecated Agent Type은 다음을 선언해야 한다.

deprecated\_since: datetime  
replacement\_agent\_type\_id: string | null  
migration\_notes: string

Blocked Agent Type은 새로운 Agent Configuration이나 Agent Instance에서 사용되면 안 된다.

---

## **24\. Domain Extension Rule**

Domain Module은 새로운 Agent Type을 제안할 수 있다.

그러나 새로운 Agent Type은 등록, 검토, versioning, boundary mapping, action mapping, policy mapping, model/tool mapping, test generation을 거치기 전까지 사용할 수 없다.

권장 흐름:

Domain Module  
    ↓  
Agent Type Proposal  
    ↓  
Semantic Review  
    ↓  
Registry Review  
    ↓  
Role / Authority Mapping  
    ↓  
Action Type Mapping  
    ↓  
Evidence Mapping  
    ↓  
Policy Mapping  
    ↓  
Ontology Scope Mapping  
    ↓  
Model / Tool Mapping  
    ↓  
Boundary Review  
    ↓  
Test Case Generation  
    ↓  
Activation

Domain Module은 `agent_vocabulary_registry`를 우회하면 안 된다.

---

## **25\. Implementation Use**

`agent_vocabulary_registry`는 다음을 생성하거나 검증하는 데 사용된다.

1. `AgentType` enum  
2. `AgentCategory` enum  
3. `AgentRole` enum  
4. `AgentAuthorityLevel` enum  
5. Agent configuration validation  
6. Agent instance registration validation  
7. Agent output validation  
8. ActionCandidate 생성 권한 검증  
9. EvidenceBundle 생성 권한 검증  
10. Policy reference validation  
11. Ontology scope validation  
12. Tool access validation  
13. Model access validation  
14. Agent audit event expectation  
15. Test case generation  
16. Migration rules

Implementation은 등록되지 않은 Agent Type을 생성하거나 실행하면 안 된다.

---

## **26\. 권장 Code Structure**

registries/  
    agent\_vocabulary\_registry/  
        agent\_vocabulary\_registry.py  
        agent\_vocabulary\_entry.py  
        agent\_category.py  
        agent\_role.py  
        agent\_authority.py  
        agent\_status.py  
        agent\_validation.py  
        agent\_errors.py  
        agent\_loader.py  
        agent\_migration.py

    agent\_runtime\_registry/  
    action\_registry/  
    evidence\_registry/  
    policy\_registry/  
    approval\_registry/  
    model\_registry/  
    tool\_registry/  
    ontology\_registry/

---

## **27\. Minimal Pydantic Model**

from enum import Enum  
from pydantic import BaseModel, Field  
from typing import Optional  
from datetime import datetime

class AgentStatus(str, Enum):  
    DRAFT \= "draft"  
    ACTIVE \= "active"  
    DEPRECATED \= "deprecated"  
    MIGRATION\_REQUIRED \= "migration\_required"  
    RETIRED \= "retired"  
    BLOCKED \= "blocked"

class AgentCategory(str, Enum):  
    SAFETY\_AGENT \= "safety\_agent"  
    ROBOT\_AGENT \= "robot\_agent"  
    EQUIPMENT\_AGENT \= "equipment\_agent"  
    WORKER\_AGENT \= "worker\_agent"  
    ZONE\_AGENT \= "zone\_agent"  
    INSPECTION\_AGENT \= "inspection\_agent"  
    PLANNING\_AGENT \= "planning\_agent"  
    COMPLIANCE\_AGENT \= "compliance\_agent"  
    RESOURCE\_AGENT \= "resource\_agent"  
    NOTIFICATION\_AGENT \= "notification\_agent"  
    SUPERVISOR\_AGENT \= "supervisor\_agent"  
    AUDIT\_AGENT \= "audit\_agent"  
    DATA\_AGENT \= "data\_agent"  
    DIGITAL\_TWIN\_AGENT \= "digital\_twin\_agent"

class AgentAuthorityLevel(str, Enum):  
    OBSERVE\_ONLY \= "observe\_only"  
    ANALYZE\_ONLY \= "analyze\_only"  
    RECOMMEND \= "recommend"  
    PROPOSE\_ACTION \= "propose\_action"  
    REQUEST\_APPROVAL \= "request\_approval"  
    VALIDATE\_SUPPORT \= "validate\_support"  
    AUDIT\_ONLY \= "audit\_only"

class RuntimeEnvironment(str, Enum):  
    EDGE \= "edge"  
    SITE\_SERVER \= "site\_server"  
    CENTRAL \= "central"  
    CLOUD \= "cloud"  
    HYBRID \= "hybrid"

class AgentVocabularyEntry(BaseModel):  
    agent\_type\_id: str  
    canonical\_name: str  
    display\_name: str  
    description: str  
    semantic\_iri: str

    agent\_category: AgentCategory  
    agent\_roles: list\[str\] \= Field(default\_factory=list)

    version: str  
    status: AgentStatus \= AgentStatus.DRAFT

    authority\_level: AgentAuthorityLevel  
    human\_approval\_required: bool \= False

    allowed\_input\_event\_types: list\[str\] \= Field(default\_factory=list)  
    allowed\_observation\_types: list\[str\] \= Field(default\_factory=list)  
    allowed\_evidence\_types: list\[str\] \= Field(default\_factory=list)  
    allowed\_output\_types: list\[str\] \= Field(default\_factory=list)

    allowed\_action\_type\_refs: list\[str\] \= Field(default\_factory=list)  
    allowed\_policy\_refs: list\[str\] \= Field(default\_factory=list)  
    allowed\_ontology\_scopes: list\[str\] \= Field(default\_factory=list)  
    allowed\_tool\_refs: list\[str\] \= Field(default\_factory=list)  
    allowed\_model\_refs: list\[str\] \= Field(default\_factory=list)

    runtime\_environment: RuntimeEnvironment

    decision\_boundary: str  
    execution\_boundary: str  
    safety\_boundary: str

    precondition\_refs: list\[str\] \= Field(default\_factory=list)  
    invariant\_refs: list\[str\] \= Field(default\_factory=list)  
    audit\_event\_refs: list\[str\] \= Field(default\_factory=list)

    owner\_module: str  
    owner\_team: str  
    source\_document: str

    created\_at: datetime  
    updated\_at: datetime  
    deprecated\_since: Optional\[datetime\] \= None  
    replacement\_agent\_type\_id: Optional\[str\] \= None

---

## **28\. Core Validation Function**

def validate\_agent\_output\_permission(  
    entry: AgentVocabularyEntry,  
    output\_type: str,  
    action\_type\_ref: str | None \= None,  
) \-\> None:  
    if entry.status \!= AgentStatus.ACTIVE:  
        raise InvalidAgentTypeError(  
            f"Agent Type is not active: {entry.agent\_type\_id}"  
        )

    if output\_type not in entry.allowed\_output\_types:  
        raise AgentOutputNotAllowedError(  
            f"Output type '{output\_type}' is not allowed for "  
            f"Agent Type '{entry.agent\_type\_id}'"  
        )

    forbidden\_outputs \= {  
        "ApprovedAction",  
        "ExecutionRequest",  
        "ExternalControlRequest",  
        "PhysicalCommand",  
        "PLCCommand",  
        "SCADACommand",  
        "RobotMotionPrimitive",  
        "EmergencyStopCommand",  
    }

    if output\_type in forbidden\_outputs:  
        raise AgentBoundaryViolationError(  
            f"Agent Type '{entry.agent\_type\_id}' must not create '{output\_type}'"  
        )

    if action\_type\_ref is not None:  
        if action\_type\_ref not in entry.allowed\_action\_type\_refs:  
            raise AgentActionTypeNotAllowedError(  
                f"Action Type '{action\_type\_ref}' is not allowed for "  
                f"Agent Type '{entry.agent\_type\_id}'"  
            )

---

## **29\. Test Scenarios**

필수 테스트는 다음과 같다.

1\. 등록되지 않은 Agent Type 거부  
2\. inactive Agent Type 거부  
3\. deprecated Agent Type 사용 거부  
4\. blocked Agent Type 사용 거부  
5\. 허용되지 않은 output type 생성 거부  
6\. ApprovedAction 생성 시도 거부  
7\. ExecutionRequest 생성 시도 거부  
8\. PhysicalCommand 생성 시도 거부  
9\. 허용되지 않은 Action Type 제안 거부  
10\. 허용되지 않은 evidence type 참조 거부  
11\. 허용되지 않은 ontology scope 접근 거부  
12\. 허용되지 않은 tool 호출 거부  
13\. 허용되지 않은 model 사용 거부  
14\. authority level 초과 행위 거부  
15\. agent output audit record 생성 검증

---

## **30\. Final Rule**

등록된 Agent Type이 없으면,  
유효한 Agent Configuration도 없다.

유효한 Agent Configuration이 없으면,  
유효한 Agent Instance도 없다.

유효한 Agent Instance가 없으면,  
유효한 Agent Output도 없다.

Agent에게 허용된 Output Type이 아니면,  
그 Output은 생성될 수 없다.

Agent에게 허용된 Action Type이 아니면,  
ActionCandidate를 제안할 수 없다.

Agent는 ApprovedAction을 만들 수 없다.

Agent는 ExecutionRequest를 만들 수 없다.

Agent는 PhysicalCommand를 만들 수 없다.

Agent는 External System을 직접 제어할 수 없다.

`agent_vocabulary_registry`는 LEDO Agent Layer의 첫 번째 결정론적 통제 지점이다.

이 모듈은 agent의 무분별한 확장을 방지하고, agent가 자신의 역할·권한·출력 경계를 넘지 못하게 하며, 모든 agent behavior가 ontology, policy, action registry, evidence registry, model registry, tool registry, audit system과 정렬되도록 보장한다.

핵심 정의는 다음과 같다.

Agent Vocabulary Registry  
\= Agent 이름 목록이 아니라,  
Agent의 의미, 역할, 권한, 출력, 경계를 통제하는 운영 계약 레지스트리

