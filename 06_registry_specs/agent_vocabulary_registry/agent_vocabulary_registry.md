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

status: draft

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

status: draft

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

