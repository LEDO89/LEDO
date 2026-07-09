 **Model Adapter registry** 

## **1\. Overview**

`model_adapter_registry` is a core registry in the LEDO Ontology-Centric Cyber-Physical System. It defines and governs all AI / ML / LLM / SLM / Vision / TinyML / ONNX / TensorRT / vLLM / Ollama / API-based model invocation adapters used across the system.

The purpose of this module is to prevent Agents, Services, and Workflows from arbitrarily invoking unverified models or misusing model outputs outside their safety boundaries for Decision, Approval, or Execution.

`model_adapter_registry` is not a simple list of models.

It is an **operational contract registry for model invocation paths, runtimes, input/output contracts, and safety boundaries** that defines the following:

Which Model Adapters may exist?

Which model or model runtime does this Adapter invoke?

Which Agent Type may use this Model Adapter?

Which input schema must be accepted?

Which output schema must be returned?

Can this model output be used to generate an ActionCandidate?

Can this model output be used as Evidence?

Can this model output be used directly for Approval or Execution?

Which safety guard, ontology guard, and policy guard are required for this model invocation?

Which latency, cost, privacy, and deployment boundaries must be enforced?

In other words, `model_adapter_registry` is the core registry that turns model invocation into a controlled operational path inside LEDO.

---

## **2\. Core Principle**

A Model Adapter is a model invocation path.

A Model Adapter is not an Agent.

A Model Adapter is not the Decision Registry.

A Model Adapter is not Approval Authority.

A Model Adapter is not the Safety Gate.

A Model Adapter must not create an ExecutionRequest.

A Model Adapter must not create a Physical Command.

The basic meaning of model output is:

A model may support interpretation.

A model may support classification.

A model may support candidate generation.

A model may support summarization.

A model may generate risk signals.

However, model output is not a decision.

Model output is not approval.

Model output is not execution.

The core principle is:

Model output supports interpretation.

Ontology defines meaning.

Policy defines permission.

Decision Registry defines judgment flow.

Approval Registry defines authority.

Safety Gate validates execution readiness.

Model Adapter calls models.

Model Adapter does not execute actions.

In LEDO, models may support **intent, classification, recommendation, extraction, summarization, and candidate generation**, but they must not replace deterministic execution boundaries.

---

## **3\. Position in the LEDO Architecture**

`model_adapter_registry` sits between the Distributed Domain Agent Layer and the Model Runtime / Inference Backend.

Agent / Service / Workflow

        ↓

model\_adapter\_registry validation

        ↓

ModelAdapter

        ↓

Model Runtime / Inference Backend

        ↓

ModelOutput

        ↓

Output Validation

        ↓

Agent Output / Evidence / ActionCandidate / RiskSignal

In the full LEDO flow, it is positioned as follows:

Event / Evidence / World State

        ↓

Domain Agent

        ↓

model\_adapter\_registry

        ↓

LLM / SLM / Vision Model / TinyML / ONNX / TensorRT / vLLM / Ollama

        ↓

Model Output

        ↓

Ontology Guard / Policy Guard / Output Schema Validation

        ↓

ActionCandidate / EvidenceBundle / RiskSignal / Recommendation

        ↓

Decision Registry

        ↓

Approval Registry

        ↓

Safety Gate

---

## **4\. Purpose**

The purpose of `model_adapter_registry` is to ensure the following:

1. Prevent unregistered model invocations  
2. Restrict which Model Adapters each Agent may use  
3. Define which models and runtimes each Model Adapter may invoke  
4. Define model input schemas  
5. Define model output schemas  
6. Define the allowed usage scope of model outputs  
7. Define conditions under which model output may become an ActionCandidate  
8. Define conditions under which model output may become Evidence  
9. Prevent model output from being used directly as Approval or Execution  
10. Manage LoRA / DAPT / fine-tuned model adapter connections  
11. Define local / edge / cloud / API runtime boundaries  
12. Define latency / cost / privacy / safety constraints  
13. Define ontology guard and policy guard requirements  
14. Manage prompt template and system instruction references  
15. Manage model evaluation score and safety rating references  
16. Define model adapter health check and fallback rules  
17. Define audit and trace rules  
18. Manage versioning and migration

---

## **5\. Core Distinctions**

### **5.1 Model**

`Model` is the actual AI / ML model that performs inference.

Examples:

qwen3\_coder\_30b

safety\_slm\_v1

hazard\_vision\_model\_v1

worker\_proximity\_classifier\_v1

robot\_dispatch\_slm\_v1

tinyml\_vibration\_detector\_v1

onnx\_hazard\_classifier\_v1

tensorrt\_ppe\_detector\_v1

Model metadata, evaluation scores, training lineage, license, and intended use may be managed by `model_registry`.

---

### **5.2 Model Adapter**

`Model Adapter` is a standardized communication and input/output transformation layer used by LEDO to call a specific model or model runtime.

Examples:

ollama\_model\_adapter

vllm\_model\_adapter

onnx\_runtime\_adapter

tensorrt\_inference\_adapter

openai\_api\_model\_adapter

local\_slm\_adapter

tinyml\_edge\_adapter

vision\_model\_adapter

A Model Adapter performs the following:

Transforms a standard ModelRequest into a provider/runtime-specific request.

Transforms the model response into a standard ModelOutput.

Applies timeout, retry, schema validation, and logging.

Validates model output boundaries.

---

### **5.3 Model Adapter Instance**

`Model Adapter Instance` is an individual adapter registered in the actual runtime environment.

Examples:

model\_adapter:ollama\_qwen3\_site\_A

model\_adapter:vllm\_safety\_slm\_site\_server\_A

model\_adapter:onnx\_hazard\_edge\_camera\_03

model\_adapter:tensorrt\_ppe\_edge\_gpu\_01

model\_adapter:openai\_api\_reasoning\_gateway

Adapter Type is the design-level definition, while Adapter Instance is the actual runtime endpoint that can be invoked.

---

### **5.4 Model Runtime**

`Model Runtime` is the environment where the model actually runs.

Examples:

Ollama

vLLM

ONNX Runtime

TensorRT

PyTorch

TensorFlow Lite

OpenAI API

Local HTTP inference server

Edge device runtime

GPU inference server

Model Adapter invokes this runtime.

---

### **5.5 Difference Between Fine-tuning Adapter and Model Adapter**

Fine-tuning adapters such as LoRA are different from adapters in `model_adapter_registry`.

LoRA Adapter:

    A parameter-efficient fine-tuning component attached inside a model.

Model Adapter:

    An integration wrapper used by LEDO to invoke a model or model runtime.

Example:

lora:safety\_domain\_lora\_v1

    → a fine-tuning component attached to model weights

model\_adapter:vllm\_safety\_slm\_site\_A

    → an internal LEDO adapter that invokes the safety\_slm \+ LoRA combination through a vLLM runtime

LoRA, DAPT, and fine-tuning lineage should be managed by `model_registry` or `model_component_registry`, while `model_adapter_registry` manages which runtime path is used to invoke that model combination.

---

### **5.6 Model Output Boundary**

Model Output Boundary defines how far model output may be used inside the system.

Allowed outputs:

classification\_result

extracted\_fact\_candidate

risk\_signal

recommendation

summary

evidence\_candidate

action\_candidate\_draft

natural\_language\_explanation

Forbidden outputs:

ApprovedAction

ApprovalDecision

ExecutionRequest

ExternalControlRequest

PhysicalCommand

PLCCommand

RobotMotionPrimitive

SafetyGatePass

PolicyOverride

Core principle:

Model Output ≠ Decision

Model Output ≠ Approval

Model Output ≠ Execution

---

## **6\. Scope**

`model_adapter_registry` controls the following fields:

model\_adapter\_id: string

canonical\_name: string

display\_name: string

description: string

semantic\_iri: string

model\_adapter\_type: string

model\_runtime\_type: string

model\_provider\_type: string

version: string

status: draft | active | degraded | maintenance | deprecated | retired | blocked

model\_refs:

  \- string

model\_version\_refs:

  \- string

fine\_tuning\_component\_refs:

  \- string

allowed\_agent\_type\_refs:

  \- string

allowed\_service\_refs:

  \- string

allowed\_task\_types:

  \- string

allowed\_input\_schema\_refs:

  \- string

allowed\_output\_schema\_refs:

  \- string

prompt\_template\_refs:

  \- string

system\_instruction\_refs:

  \- string

tool\_access\_refs:

  \- string

runtime\_endpoint\_ref: string

deployment\_environment: edge | site\_server | central | cloud | hybrid

hardware\_profile\_ref: string | null

max\_latency\_ms: integer

timeout\_ms: integer

retry\_policy\_ref: string | null

fallback\_model\_adapter\_ref: string | null

privacy\_boundary: local\_only | site\_only | enterprise | external\_api\_allowed

data\_residency\_requirement: string

pii\_allowed: boolean

input\_sensitivity\_allowed:

  \- string

output\_sensitivity\_level: public | internal | confidential | restricted | safety\_critical

model\_output\_usage:

  may\_generate\_evidence\_candidate: boolean

  may\_generate\_action\_candidate: boolean

  may\_generate\_risk\_signal: boolean

  may\_generate\_decision\_support: boolean

  may\_generate\_approval\_support: boolean

  may\_generate\_execution\_request: boolean

required\_guards:

  \- ontology\_guard

  \- policy\_guard

  \- schema\_guard

  \- safety\_guard

  \- pii\_guard

  \- hallucination\_guard

eval\_requirement\_refs:

  \- string

safety\_rating\_ref: string

model\_card\_ref: string

license\_ref: string

health\_check\_policy\_ref: string

audit\_required: boolean

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

replacement\_model\_adapter\_id: string | null

---

## **7\. Non-Scope**

`model_adapter_registry` does not define the following:

1. The complete model training dataset  
2. The model weights themselves  
3. The complete fine-tuning pipeline  
4. LoRA weight files themselves  
5. The full raw prompt text  
6. Complete policy pass/fail logic  
7. Complete ontology reasoning logic  
8. Decision Rules themselves  
9. Approval Rules themselves  
10. Final Safety Gate decision  
11. Physical execution commands  
12. Complete external system adapter implementation  
13. Complete GPU scheduler  
14. Complete Kubernetes deployment  
15. Actual API keys, tokens, or secret values

These responsibilities belong to the following modules:

model\_registry

model\_component\_registry

prompt\_registry

tool\_registry

policy\_registry

ontology\_registry

decision\_registry

approval\_registry

safety\_gate

adapter\_registry

external\_system\_registry

vault / secret manager

runtime\_orchestration\_layer

---

## **8\. Model Adapter Type Model**

Recommended Model Adapter Types are:

LLM\_ADAPTER

SLM\_ADAPTER

VISION\_MODEL\_ADAPTER

CLASSIFIER\_ADAPTER

EMBEDDING\_MODEL\_ADAPTER

RERANKER\_ADAPTER

ONNX\_RUNTIME\_ADAPTER

TENSORRT\_ADAPTER

TINYML\_EDGE\_ADAPTER

MULTIMODAL\_MODEL\_ADAPTER

RULE\_AUGMENTED\_MODEL\_ADAPTER

API\_MODEL\_ADAPTER

LOCAL\_MODEL\_ADAPTER

### **8.1 LLM\_ADAPTER**

An adapter that invokes a large language model.

Examples:

ollama\_qwen3\_adapter

openai\_reasoning\_adapter

vllm\_llm\_adapter

Common use cases:

natural language interpretation

summarization

structured extraction

planning support

code assistance

It must not be used directly for safety-critical execution decisions.

---

### **8.2 SLM\_ADAPTER**

An adapter that invokes a domain-specific small language model.

Examples:

safety\_slm\_adapter

robot\_dispatch\_slm\_adapter

inspection\_slm\_adapter

It is mainly used at the edge or site server level.

---

### **8.3 VISION\_MODEL\_ADAPTER**

An adapter that invokes camera, image, or video-based models.

Examples:

ppe\_detection\_adapter

hazard\_detection\_vision\_adapter

worker\_zone\_vision\_adapter

Vision output must include confidence, source frame, timestamp, and model version.

---

### **8.4 ONNX\_RUNTIME\_ADAPTER**

An adapter that invokes ONNX Runtime-based models.

Examples:

onnx\_worker\_proximity\_classifier

onnx\_hazard\_classifier

It is mainly used for portable inference.

---

### **8.5 TENSORRT\_ADAPTER**

A high-speed inference adapter based on NVIDIA TensorRT.

Examples:

tensorrt\_ppe\_detector\_edge\_gpu\_01

tensorrt\_hazard\_detector\_site\_gpu

It is mainly used for low-latency vision inference.

---

### **8.6 TINYML\_EDGE\_ADAPTER**

An adapter that invokes TinyML models running on MCUs or edge devices.

Examples:

tinyml\_vibration\_detector

tinyml\_sound\_anomaly\_detector

tinyml\_gas\_pattern\_detector

TinyML output is usually connected to events or evidence candidates.

---

### **8.7 EMBEDDING\_MODEL\_ADAPTER**

An adapter that embeds documents, ontology labels, events, or evidence.

Examples:

construction\_doc\_embedding\_adapter

ontology\_label\_embedding\_adapter

incident\_similarity\_embedding\_adapter

Embedding output must not become the sole basis for a safety decision.

---

### **8.8 RERANKER\_ADAPTER**

An adapter that reranks search results or RAG candidates.

Examples:

safety\_doc\_reranker

bim\_issue\_reranker

A reranker is a supporting tool that improves retrieval quality.

---

## **9\. Registry Entry Schema**

Each Model Adapter Registry entry follows this structure:

model\_adapter\_id: string

canonical\_name: string

display\_name: string

description: string

semantic\_iri: string

model\_adapter\_type: string

model\_runtime\_type: string

model\_provider\_type: string

version: string

status: draft | active | degraded | maintenance | deprecated | retired | blocked

model\_refs:

  \- string

model\_version\_refs:

  \- string

fine\_tuning\_component\_refs:

  \- string

allowed\_agent\_type\_refs:

  \- string

allowed\_service\_refs:

  \- string

allowed\_task\_types:

  \- string

allowed\_input\_schema\_refs:

  \- string

allowed\_output\_schema\_refs:

  \- string

prompt\_template\_refs:

  \- string

system\_instruction\_refs:

  \- string

tool\_access\_refs:

  \- string

runtime\_endpoint\_ref: string

deployment\_environment: string

hardware\_profile\_ref: string | null

max\_latency\_ms: integer

timeout\_ms: integer

retry\_policy\_ref: string | null

fallback\_model\_adapter\_ref: string | null

privacy\_boundary: string

data\_residency\_requirement: string

pii\_allowed: boolean

input\_sensitivity\_allowed:

  \- string

output\_sensitivity\_level: string

model\_output\_usage:

  may\_generate\_evidence\_candidate: boolean

  may\_generate\_action\_candidate: boolean

  may\_generate\_risk\_signal: boolean

  may\_generate\_decision\_support: boolean

  may\_generate\_approval\_support: boolean

  may\_generate\_execution\_request: boolean

required\_guards:

  \- string

eval\_requirement\_refs:

  \- string

safety\_rating\_ref: string

model\_card\_ref: string

license\_ref: string

health\_check\_policy\_ref: string

audit\_required: boolean

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

replacement\_model\_adapter\_id: string | null

---

## **10\. Registry Entry Example: Safety SLM Adapter**

model\_adapter\_id: model\_adapter:safety\_slm\_vllm\_site\_A

canonical\_name: safety\_slm\_vllm\_site\_A

display\_name: Safety SLM Adapter \- Site A

description: A vLLM-based Safety SLM adapter that supports safety risk analysis and ActionCandidate draft generation at Site A.

semantic\_iri: ledo:SafetySLMAdapterSiteA

model\_adapter\_type: SLM\_ADAPTER

model\_runtime\_type: vLLM

model\_provider\_type: local\_site\_server

version: 1.0.0

status: draft

model\_refs:

  \- model:safety\_slm

model\_version\_refs:

  \- model\_version:safety\_slm\_v1.0.0

fine\_tuning\_component\_refs:

  \- lora:safety\_domain\_lora\_v1

  \- dapt:construction\_safety\_dapt\_v1

allowed\_agent\_type\_refs:

  \- agent\_type:SAFETY\_RISK\_AGENT

  \- agent\_type:INSPECTION\_AGENT

allowed\_service\_refs:

  \- service:evidence\_binder

  \- service:decision\_engine

allowed\_task\_types:

  \- task:safety\_risk\_classification

  \- task:hazard\_summary

  \- task:action\_candidate\_draft\_generation

  \- task:evidence\_summary

allowed\_input\_schema\_refs:

  \- schema:safety\_model\_input\_v1

  \- schema:evidence\_bundle\_summary\_input\_v1

allowed\_output\_schema\_refs:

  \- schema:risk\_signal\_output\_v1

  \- schema:action\_candidate\_draft\_output\_v1

  \- schema:evidence\_summary\_output\_v1

prompt\_template\_refs:

  \- prompt:safety\_risk\_analysis\_prompt\_v1

  \- prompt:action\_candidate\_draft\_prompt\_v1

system\_instruction\_refs:

  \- instruction:model\_must\_not\_approve\_or\_execute\_v1

  \- instruction:safety\_output\_boundary\_v1

tool\_access\_refs:

  \- tool:ontology\_lookup\_readonly

  \- tool:world\_state\_query\_readonly

  \- tool:evidence\_bundle\_readonly

runtime\_endpoint\_ref: endpoint:vllm\_site\_A\_safety\_slm

deployment\_environment: site\_server

hardware\_profile\_ref: hardware:site\_A\_gpu\_server

max\_latency\_ms: 3000

timeout\_ms: 5000

retry\_policy\_ref: retry:model\_adapter\_standard\_retry\_v1

fallback\_model\_adapter\_ref: model\_adapter:safety\_rule\_based\_fallback\_site\_A

privacy\_boundary: site\_only

data\_residency\_requirement: site\_A\_only

pii\_allowed: true

input\_sensitivity\_allowed:

  \- restricted

  \- safety\_critical

output\_sensitivity\_level: safety\_critical

model\_output\_usage:

  may\_generate\_evidence\_candidate: true

  may\_generate\_action\_candidate: true

  may\_generate\_risk\_signal: true

  may\_generate\_decision\_support: true

  may\_generate\_approval\_support: false

  may\_generate\_execution\_request: false

required\_guards:

  \- ontology\_guard

  \- policy\_guard

  \- schema\_guard

  \- safety\_guard

  \- pii\_guard

  \- hallucination\_guard

eval\_requirement\_refs:

  \- eval:safety\_slm\_min\_precision\_v1

  \- eval:safety\_action\_candidate\_quality\_v1

safety\_rating\_ref: safety\_rating:safety\_relevant\_model

model\_card\_ref: model\_card:safety\_slm\_v1

license\_ref: license:internal\_model\_license\_v1

health\_check\_policy\_ref: health:model\_adapter\_health\_check\_v1

audit\_required: true

decision\_boundary: may\_support\_decision\_case\_but\_not\_decide

approval\_boundary: must\_not\_grant\_approval

execution\_boundary: must\_not\_create\_execution\_request

safety\_boundary: model\_output\_must\_pass\_ontology\_policy\_and\_safety\_guards

audit\_event\_refs:

  \- audit:model\_adapter\_invoked

  \- audit:model\_output\_validated

  \- audit:model\_output\_rejected

  \- audit:model\_adapter\_health\_changed

owner\_module: model\_runtime\_module

owner\_team: LEDO Model Governance

source\_document: safety\_model\_adapter\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_model\_adapter\_id: null

---

## **11\. Registry Entry Example: Vision Hazard Detector Adapter**

model\_adapter\_id: model\_adapter:tensorrt\_hazard\_detector\_edge\_01

canonical\_name: tensorrt\_hazard\_detector\_edge\_01

display\_name: TensorRT Hazard Detector Adapter \- Edge 01

description: A TensorRT vision model adapter that performs hazard detection inference from camera frames on Edge GPU 01\.

semantic\_iri: ledo:TensorRTHazardDetectorAdapterEdge01

model\_adapter\_type: VISION\_MODEL\_ADAPTER

model\_runtime\_type: TensorRT

model\_provider\_type: edge\_gpu\_runtime

version: 1.0.0

status: draft

model\_refs:

  \- model:hazard\_vision\_model

model\_version\_refs:

  \- model\_version:hazard\_vision\_model\_v1.2.0

fine\_tuning\_component\_refs: \[\]

allowed\_agent\_type\_refs:

  \- agent\_type:SAFETY\_RISK\_AGENT

  \- agent\_type:ZONE\_MONITORING\_AGENT

allowed\_service\_refs:

  \- service:camera\_frame\_ingestion

  \- service:evidence\_binder

  \- service:world\_state\_service

allowed\_task\_types:

  \- task:hazard\_detection

  \- task:zone\_risk\_detection

  \- task:persistent\_hazard\_tracking

allowed\_input\_schema\_refs:

  \- schema:camera\_frame\_input\_v1

  \- schema:video\_clip\_input\_v1

allowed\_output\_schema\_refs:

  \- schema:hazard\_detection\_output\_v1

  \- schema:vision\_detection\_evidence\_candidate\_v1

prompt\_template\_refs: \[\]

system\_instruction\_refs:

  \- instruction:vision\_model\_output\_boundary\_v1

tool\_access\_refs:

  \- tool:camera\_frame\_reader

  \- tool:zone\_context\_lookup\_readonly

runtime\_endpoint\_ref: endpoint:edge\_gpu\_01\_tensorrt

deployment\_environment: edge

hardware\_profile\_ref: hardware:edge\_gpu\_01

max\_latency\_ms: 200

timeout\_ms: 1000

retry\_policy\_ref: retry:edge\_model\_retry\_v1

fallback\_model\_adapter\_ref: null

privacy\_boundary: local\_only

data\_residency\_requirement: edge\_device\_only

pii\_allowed: true

input\_sensitivity\_allowed:

  \- restricted

  \- safety\_critical

output\_sensitivity\_level: safety\_critical

model\_output\_usage:

  may\_generate\_evidence\_candidate: true

  may\_generate\_action\_candidate: false

  may\_generate\_risk\_signal: true

  may\_generate\_decision\_support: true

  may\_generate\_approval\_support: false

  may\_generate\_execution\_request: false

required\_guards:

  \- schema\_guard

  \- pii\_guard

  \- safety\_guard

  \- evidence\_quality\_guard

eval\_requirement\_refs:

  \- eval:hazard\_detector\_precision\_recall\_v1

  \- eval:vision\_false\_negative\_threshold\_v1

safety\_rating\_ref: safety\_rating:safety\_relevant\_model

model\_card\_ref: model\_card:hazard\_vision\_model\_v1

license\_ref: license:internal\_vision\_model\_license\_v1

health\_check\_policy\_ref: health:edge\_vision\_model\_health\_check\_v1

audit\_required: true

decision\_boundary: may\_generate\_hazard\_evidence\_candidate\_only

approval\_boundary: must\_not\_grant\_approval

execution\_boundary: must\_not\_create\_execution\_request

safety\_boundary: low\_confidence\_detection\_requires\_additional\_evidence

audit\_event\_refs:

  \- audit:model\_adapter\_invoked

  \- audit:vision\_detection\_created

  \- audit:model\_output\_rejected

  \- audit:model\_adapter\_health\_changed

owner\_module: vision\_runtime\_module

owner\_team: LEDO Edge Vision

source\_document: vision\_model\_adapter\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_model\_adapter\_id: null

---

## **12\. Registry Entry Example: Embedding Model Adapter**

model\_adapter\_id: model\_adapter:construction\_doc\_embedding\_site\_A

canonical\_name: construction\_doc\_embedding\_site\_A

display\_name: Construction Document Embedding Adapter \- Site A

description: A model adapter that embeds documents, safety manuals, BIM issues, and incident reports for Site A.

semantic\_iri: ledo:ConstructionDocumentEmbeddingAdapterSiteA

model\_adapter\_type: EMBEDDING\_MODEL\_ADAPTER

model\_runtime\_type: ONNX\_Runtime

model\_provider\_type: local\_site\_server

version: 1.0.0

status: draft

model\_refs:

  \- model:construction\_embedding\_model

model\_version\_refs:

  \- model\_version:construction\_embedding\_model\_v1.0.0

fine\_tuning\_component\_refs: \[\]

allowed\_agent\_type\_refs:

  \- agent\_type:SAFETY\_RISK\_AGENT

  \- agent\_type:INSPECTION\_AGENT

  \- agent\_type:COMPLIANCE\_AGENT

allowed\_service\_refs:

  \- service:semantic\_search\_service

  \- service:rag\_retrieval\_service

  \- service:knowledge\_indexer

allowed\_task\_types:

  \- task:document\_embedding

  \- task:semantic\_retrieval

  \- task:incident\_similarity\_search

allowed\_input\_schema\_refs:

  \- schema:document\_chunk\_input\_v1

  \- schema:ontology\_label\_input\_v1

allowed\_output\_schema\_refs:

  \- schema:embedding\_vector\_output\_v1

prompt\_template\_refs: \[\]

system\_instruction\_refs: \[\]

tool\_access\_refs:

  \- tool:document\_store\_reader

  \- tool:ontology\_label\_reader

runtime\_endpoint\_ref: endpoint:onnx\_embedding\_site\_A

deployment\_environment: site\_server

hardware\_profile\_ref: hardware:site\_A\_cpu\_server

max\_latency\_ms: 500

timeout\_ms: 2000

retry\_policy\_ref: retry:model\_adapter\_standard\_retry\_v1

fallback\_model\_adapter\_ref: null

privacy\_boundary: site\_only

data\_residency\_requirement: site\_A\_only

pii\_allowed: false

input\_sensitivity\_allowed:

  \- internal

  \- confidential

output\_sensitivity\_level: internal

model\_output\_usage:

  may\_generate\_evidence\_candidate: false

  may\_generate\_action\_candidate: false

  may\_generate\_risk\_signal: false

  may\_generate\_decision\_support: true

  may\_generate\_approval\_support: false

  may\_generate\_execution\_request: false

required\_guards:

  \- schema\_guard

  \- pii\_guard

  \- retrieval\_grounding\_guard

eval\_requirement\_refs:

  \- eval:retrieval\_quality\_eval\_v1

safety\_rating\_ref: safety\_rating:non\_decision\_support\_model

model\_card\_ref: model\_card:construction\_embedding\_model\_v1

license\_ref: license:internal\_embedding\_model\_license\_v1

health\_check\_policy\_ref: health:model\_adapter\_health\_check\_v1

audit\_required: true

decision\_boundary: may\_support\_retrieval\_but\_not\_decide

approval\_boundary: must\_not\_grant\_approval

execution\_boundary: must\_not\_create\_execution\_request

safety\_boundary: vector\_similarity\_must\_not\_be\_used\_as\_sole\_safety\_basis

audit\_event\_refs:

  \- audit:model\_adapter\_invoked

  \- audit:embedding\_created

  \- audit:model\_adapter\_health\_changed

owner\_module: knowledge\_runtime\_module

owner\_team: LEDO Knowledge Integration

source\_document: embedding\_model\_adapter\_contract\_v1

created\_at: 2026-06-26T00:00:00Z

updated\_at: 2026-06-26T00:00:00Z

deprecated\_since: null

replacement\_model\_adapter\_id: null

---

## **13\. Model Adapter Lifecycle Alignment**

Model Adapter is connected to the following lifecycle:

Model Adapter Registered

        ↓

Model / Runtime / Endpoint Contract Validation

        ↓

Prompt / Input / Output Schema Validation

        ↓

Guard Requirement Validation

        ↓

Evaluation Requirement Check

        ↓

Health Check

        ↓

Activation

        ↓

Runtime Model Invocation

        ↓

Model Output Validation

        ↓

Agent Output / Evidence Candidate / ActionCandidate Draft

        ↓

Audit / Monitoring / Migration

The important point is that an active Model Adapter is not automatically available to every Agent.

The Model Adapter must be active.

The Agent Type must be included in allowed\_agent\_type\_refs.

The Task Type must be allowed.

The Input Schema must match.

The Output Schema must match.

The Privacy Boundary must be satisfied.

Required Guards must be applied.

The Model Output Boundary must not be violated.

---

## **14\. Validation Rules**

A Model Adapter Entry is valid only when the following conditions are satisfied:

1. `model_adapter_id` exists in the registry.  
2. Its status is `active`.  
3. Model adapter type is declared.  
4. Model runtime type is declared.  
5. Model reference is declared.  
6. Allowed agent type or allowed service is declared.  
7. Allowed task type is declared.  
8. Input schema reference is declared.  
9. Output schema reference is declared.  
10. Runtime endpoint reference is declared.  
11. Privacy boundary is declared.  
12. Model output usage boundary is declared.  
13. Required guards are declared.  
14. Evaluation requirement reference is declared.  
15. Safety rating reference is declared.  
16. Health check policy is declared.  
17. Decision / approval / execution / safety boundaries are declared.  
18. Audit event references are declared.  
19. Owner module is declared.  
20. Version is valid.  
21. If deprecated, migration metadata exists.

If any of these conditions are missing, the Model Adapter must not be used in the operational lifecycle.

---

## **15\. Runtime Model Invocation Validation**

Before an Agent or Service invokes a Model Adapter, the following validations are required:

Does the Model Adapter exist in the registry?

Is the Model Adapter active?

Is the caller identity valid?

Is the caller’s Agent Type or Service allowed?

Is the Task Type included in allowed\_task\_types?

Is the Input Schema allowed?

Is the input sensitivity within the allowed range?

Is PII usage allowed?

Does it comply with the Privacy Boundary?

Is the Runtime endpoint valid?

Has the Health Check passed?

Are the Required Guards applied?

Does it satisfy timeout and latency policies?

If these conditions are not satisfied, the model invocation must be rejected.

---

## **16\. Model Output Validation**

Model output must always be validated.

Validation items:

Does the Output Schema match?

Does the output contain any forbidden lifecycle object?

Is it attempting to create ApprovedAction?

Is it attempting to create ApprovalDecision?

Is it attempting to create ExecutionRequest?

Does it contain PhysicalCommand or low-level control instructions?

Can it be grounded in the ontology?

If policy references are required, are they included?

If it will be used as Evidence, does it satisfy evidence\_registry conditions?

If it will be converted into ActionCandidate, does it satisfy action\_registry conditions?

If model output violates boundaries, it must be rejected or quarantined.

---

## **17\. Guard Rule**

Model Adapter must declare required guards.

Recommended guards:

schema\_guard

ontology\_guard

policy\_guard

safety\_guard

pii\_guard

hallucination\_guard

retrieval\_grounding\_guard

evidence\_quality\_guard

action\_boundary\_guard

execution\_boundary\_guard

### **17.1 schema\_guard**

Validates input and output schemas.

---

### **17.2 ontology\_guard**

Checks whether generated entities, relations, actions, and targets exist in the ontology.

---

### **17.3 policy\_guard**

Checks whether model output violates policy boundaries.

---

### **17.4 safety\_guard**

Checks whether safety-critical output violates safety boundaries.

---

### **17.5 pii\_guard**

Prevents PII from being sent to external APIs or unauthorized runtimes.

---

### **17.6 hallucination\_guard**

Checks whether generated facts are grounded in evidence, world state, ontology, or retrieved sources.

---

### **17.7 action\_boundary\_guard**

Prevents the model from generating unauthorized Action Types.

---

### **17.8 execution\_boundary\_guard**

Prevents the model from generating ExecutionRequests or PhysicalCommands.

---

## **18\. Privacy and Data Boundary Rule**

Model Adapter must have an explicit data boundary.

Recommended privacy boundaries:

local\_only

site\_only

enterprise

external\_api\_allowed

### **18.1 local\_only**

Data must not leave the edge device or local machine.

---

### **18.2 site\_only**

Data must not leave the specific site server boundary.

---

### **18.3 enterprise**

Data may be processed only inside the enterprise network or approved enterprise environment.

---

### **18.4 external\_api\_allowed**

External API calls are allowed.

However, PII, safety-critical evidence, and restricted site data must not be sent to external APIs unless explicitly allowed by policy.

Core principle:

PII and safety-critical site data must not be sent to external model APIs unless explicitly allowed by policy.

---

## **19\. Latency and Fallback Rule**

Model Adapter must have latency and timeout policies.

Examples:

edge vision hazard detection: under 200ms

worker proximity classifier: under 100ms

safety SLM analysis: under 3000ms

LLM report summarization: under 10000ms

embedding generation: under 500ms

Fallback is required when:

model runtime unavailable

latency exceeded

output schema invalid

confidence too low

guard failed

external API unavailable

Fallback outcomes differ by task type.

Safety-critical:

    block, hold, escalate, or use deterministic fallback

Low-risk summarization:

    retry or defer

Robot dispatch:

    hold\_for\_more\_evidence or supervisor review

Vision detection:

    mark evidence as degraded or require secondary sensor

Core principle:

Model failure must not silently become safe approval or execution.

---

## **20\. Evaluation Requirement Rule**

Model Adapter must have minimum evaluation requirements.

Examples:

classification precision threshold

false negative threshold

hallucination rate threshold

schema compliance rate

ontology grounding rate

latency threshold

safety refusal correctness

domain-specific benchmark score

Safety-critical model outputs require stricter evaluation requirements.

Examples:

hazard detector:

    false negative threshold must be extremely low

worker proximity classifier:

    stale or low-confidence output must block dispatch

safety SLM:

    must not generate ApprovedAction or ExecutionRequest

---

## **21\. Relationship to Model Registry**

`model_registry` manages the model itself.

`model_adapter_registry` manages which runtime and endpoint may be used to invoke that model.

model\_registry:

    What kind of model is safety\_slm\_v1, and what eval score and model card does it have?

model\_adapter\_registry:

    Which Agent may call safety\_slm\_v1 through the vLLM site server, and for which task?

Even if a model is registered, it must not be invoked in the operational system unless a Model Adapter is registered.

---

## **22\. Relationship to Agent Vocabulary Registry**

`agent_vocabulary_registry` defines which model reference or model adapter reference an Agent Type may use.

`model_adapter_registry` verifies whether that adapter is actually allowed for the Agent Type.

agent\_vocabulary\_registry:

    SAFETY\_RISK\_AGENT may use the safety\_slm adapter.

model\_adapter\_registry:

    Is safety\_slm\_vllm\_site\_A allowed for SAFETY\_RISK\_AGENT?

Agents must not invoke arbitrary Model Adapters.

---

## **23\. Relationship to Evidence Registry**

If model output is used as an EvidenceCandidate, it must be validated by `evidence_registry`.

model\_adapter\_registry:

    This model output may generate evidence\_candidate.

evidence\_registry:

    Does this evidence\_candidate satisfy a valid Evidence Type, schema, freshness, quality, and lineage?

Model output itself is not automatically valid Evidence.

Model Output ≠ Valid Evidence

---

## **24\. Relationship to Action Registry**

Even if a Model Adapter may generate an ActionCandidate draft, the actual ActionCandidate must pass `action_registry` validation.

model\_adapter\_registry:

    safety\_slm may generate a STOP\_WORK ActionCandidate draft.

action\_registry:

    Is STOP\_WORK registered and active as an Action Type?

The model must not generate unregistered Action Types.

---

## **25\. Relationship to Decision Registry**

Model Output may support Decision, but it is not the Decision itself.

model\_adapter\_registry:

    model output may support decision\_case analysis.

decision\_registry:

    Which evidence, policy, risk, and approval route must the DecisionCase follow?

Core principle:

Model Output ≠ DecisionCase

Model Confidence ≠ Decision Outcome

---

## **26\. Relationship to Approval Registry**

Model Output may generate an approval support summary, but it must not create an ApprovalDecision.

model\_adapter\_registry:

    model may summarize evidence for the approver.

approval\_registry:

    an authorized human approver decides approval under rule and scope.

Core principle:

Model must not approve.

Agent must not approve.

Only valid approval authority may approve.

---

## **27\. Relationship to Safety Gate**

Safety Gate must not directly trust model output.

Safety Gate must verify fresh runtime evidence, policy, capability, and external system readiness.

model\_adapter\_registry:

    model may produce risk signal or evidence candidate.

safety\_gate:

    verifies runtime conditions deterministically before ExecutionRequest.

Core principle:

Model output must not replace Safety Gate validation.

---

## **28\. Relationship to Tool Registry**

Model Adapter must restrict which tools can be used.

Allowed tool examples:

ontology\_lookup\_readonly

world\_state\_query\_readonly

evidence\_bundle\_readonly

document\_retrieval\_readonly

schema\_validator

Forbidden tools:

execution\_dispatcher

adapter\_direct\_call

external\_system\_command\_sender

approval\_decision\_writer

policy\_override\_tool

credential\_reader

Models must not directly call execution tools.

---

## **29\. Relationship to Identity Registry**

The caller invoking a Model Adapter must have an identity.

identity\_registry:

    Is agent:safety\_risk\_agent\_site\_A an active identity?

model\_adapter\_registry:

    Is this identity’s Agent Type allowed to call safety\_slm\_vllm\_site\_A?

Model invocations without Identity are not auditable and must be rejected.

---

## **30\. Relationship to Audit Registry**

Model Adapter invocations and outputs must be auditable.

Audit targets:

model\_adapter\_invoked

model\_input\_validated

model\_output\_generated

model\_output\_validated

model\_output\_rejected

model\_guard\_failed

model\_latency\_exceeded

model\_fallback\_used

model\_adapter\_health\_changed

Audit Record should include the following:

model\_adapter\_id: string

model\_ref: string

model\_version\_ref: string

caller\_identity\_id: string

agent\_type\_ref: string | null

task\_type: string

input\_schema\_ref: string

output\_schema\_ref: string

guard\_results:

  \- string

latency\_ms: integer

trace\_id: string

---

## **31\. Relationship to Ontology**

Every important Model Adapter may have a semantic IRI.

Example:

model\_adapter\_id: model\_adapter:safety\_slm\_vllm\_site\_A

semantic\_iri: ledo:SafetySLMAdapterSiteA

In the ontology, it may be defined as follows:

ledo:SafetySLMAdapterSiteA

    rdf:type ledo:ModelAdapter ;

    ledo:invokesModel ledo:SafetySLM ;

    ledo:usesRuntime ledo:vLLM ;

    ledo:allowedForAgent ledo:SafetyRiskAgent ;

    ledo:mayGenerate ledo:ActionCandidateDraft ;

    ledo:mustNotGenerate ledo:ExecutionRequest .

Ontology provides the semantic foundation of Model Adapters.

Model Adapter Registry manages this foundation in the operational system through version, status, endpoint, schema, guard, privacy, latency, and audit rules.

---

## **32\. Versioning and Migration**

Model Adapter Entries must be versioned.

A version change is required when any of the following changes:

1. Model reference changes  
2. Model version changes  
3. Fine-tuning component changes  
4. Runtime endpoint changes  
5. Allowed agent type changes  
6. Allowed task type changes  
7. Input schema changes  
8. Output schema changes  
9. Prompt template changes  
10. System instruction changes  
11. Tool access changes  
12. Privacy boundary changes  
13. Guard requirements change  
14. Output usage boundary changes  
15. Latency / timeout policies change  
16. Fallback adapter changes  
17. Safety rating changes  
18. Decision / approval / execution / safety boundaries change

Status values:

draft

active

degraded

maintenance

deprecated

retired

blocked

### **32.1 degraded**

The Model Adapter is still operational, but quality, latency, or runtime health has degraded.

---

### **32.2 maintenance**

The Model Adapter is under operational maintenance.  
It must not be used for safety-critical tasks.

---

### **32.3 blocked**

The Model Adapter is blocked due to security, safety, hallucination, schema violation, evaluation failure, or similar issues.

Blocked Model Adapters must not be used in any operational lifecycle.

---

## **33\. Implementation Use**

`model_adapter_registry` is used to generate or validate:

1. `ModelAdapterType` enum  
2. `ModelAdapterStatus` enum  
3. `ModelRuntimeType` enum  
4. `ModelProviderType` enum  
5. ModelAdapter metadata DTO  
6. Model invocation permission validation  
7. Agent-to-model-adapter compatibility validation  
8. Service-to-model-adapter compatibility validation  
9. Task type validation  
10. Input schema validation  
11. Output schema validation  
12. Runtime endpoint lookup  
13. Prompt template reference lookup  
14. Guard requirement lookup  
15. Privacy boundary validation  
16. PII policy validation  
17. Output usage boundary validation  
18. Model fallback lookup  
19. Health check lookup  
20. Audit log expectations  
21. Test case generation  
22. Migration rules

Implementation must not invoke unregistered Model Adapters.

---

## **34\. Recommended Code Structure**

registries/

    model\_adapter\_registry/

        model\_adapter\_registry.py

        model\_adapter\_entry.py

        model\_adapter\_type.py

        model\_adapter\_status.py

        model\_runtime\_type.py

        model\_provider\_type.py

        model\_output\_usage.py

        model\_guard.py

        model\_adapter\_validation.py

        model\_adapter\_errors.py

        model\_adapter\_loader.py

        model\_adapter\_migration.py

    model\_registry/

    model\_component\_registry/

    prompt\_registry/

    tool\_registry/

    agent\_vocabulary\_registry/

    identity\_registry/

    evidence\_registry/

    action\_registry/

    decision\_registry/

    approval\_registry/

    runtime\_validation\_registry/

    audit\_event\_registry/

---

## **35\. Minimal Pydantic Model**

from enum import Enum

from pydantic import BaseModel, Field

from typing import Optional

from datetime import datetime

class ModelAdapterStatus(str, Enum):

    DRAFT \= "draft"

    ACTIVE \= "active"

    DEGRADED \= "degraded"

    MAINTENANCE \= "maintenance"

    DEPRECATED \= "deprecated"

    RETIRED \= "retired"

    BLOCKED \= "blocked"

class ModelAdapterType(str, Enum):

    LLM\_ADAPTER \= "llm\_adapter"

    SLM\_ADAPTER \= "slm\_adapter"

    VISION\_MODEL\_ADAPTER \= "vision\_model\_adapter"

    CLASSIFIER\_ADAPTER \= "classifier\_adapter"

    EMBEDDING\_MODEL\_ADAPTER \= "embedding\_model\_adapter"

    RERANKER\_ADAPTER \= "reranker\_adapter"

    ONNX\_RUNTIME\_ADAPTER \= "onnx\_runtime\_adapter"

    TENSORRT\_ADAPTER \= "tensorrt\_adapter"

    TINYML\_EDGE\_ADAPTER \= "tinyml\_edge\_adapter"

    MULTIMODAL\_MODEL\_ADAPTER \= "multimodal\_model\_adapter"

    RULE\_AUGMENTED\_MODEL\_ADAPTER \= "rule\_augmented\_model\_adapter"

    API\_MODEL\_ADAPTER \= "api\_model\_adapter"

    LOCAL\_MODEL\_ADAPTER \= "local\_model\_adapter"

class ModelRuntimeType(str, Enum):

    OLLAMA \= "ollama"

    VLLM \= "vllm"

    ONNX\_RUNTIME \= "onnx\_runtime"

    TENSORRT \= "tensorrt"

    PYTORCH \= "pytorch"

    TENSORFLOW\_LITE \= "tensorflow\_lite"

    OPENAI\_API \= "openai\_api"

    LOCAL\_HTTP\_SERVER \= "local\_http\_server"

    EDGE\_RUNTIME \= "edge\_runtime"

class ModelProviderType(str, Enum):

    LOCAL\_MACHINE \= "local\_machine"

    EDGE\_DEVICE \= "edge\_device"

    SITE\_SERVER \= "site\_server"

    CENTRAL\_SERVER \= "central\_server"

    CLOUD\_API \= "cloud\_api"

    EXTERNAL\_API \= "external\_api"

class DeploymentEnvironment(str, Enum):

    EDGE \= "edge"

    SITE\_SERVER \= "site\_server"

    CENTRAL \= "central"

    CLOUD \= "cloud"

    HYBRID \= "hybrid"

class PrivacyBoundary(str, Enum):

    LOCAL\_ONLY \= "local\_only"

    SITE\_ONLY \= "site\_only"

    ENTERPRISE \= "enterprise"

    EXTERNAL\_API\_ALLOWED \= "external\_api\_allowed"

class SensitivityLevel(str, Enum):

    PUBLIC \= "public"

    INTERNAL \= "internal"

    CONFIDENTIAL \= "confidential"

    RESTRICTED \= "restricted"

    SAFETY\_CRITICAL \= "safety\_critical"

class ModelOutputUsage(BaseModel):

    may\_generate\_evidence\_candidate: bool \= False

    may\_generate\_action\_candidate: bool \= False

    may\_generate\_risk\_signal: bool \= False

    may\_generate\_decision\_support: bool \= False

    may\_generate\_approval\_support: bool \= False

    may\_generate\_execution\_request: bool \= False

class ModelAdapterRegistryEntry(BaseModel):

    model\_adapter\_id: str

    canonical\_name: str

    display\_name: str

    description: str

    semantic\_iri: str

    model\_adapter\_type: ModelAdapterType

    model\_runtime\_type: ModelRuntimeType

    model\_provider\_type: ModelProviderType

    version: str

    status: ModelAdapterStatus \= ModelAdapterStatus.DRAFT

    model\_refs: list\[str\] \= Field(default\_factory=list)

    model\_version\_refs: list\[str\] \= Field(default\_factory=list)

    fine\_tuning\_component\_refs: list\[str\] \= Field(default\_factory=list)

    allowed\_agent\_type\_refs: list\[str\] \= Field(default\_factory=list)

    allowed\_service\_refs: list\[str\] \= Field(default\_factory=list)

    allowed\_task\_types: list\[str\] \= Field(default\_factory=list)

    allowed\_input\_schema\_refs: list\[str\] \= Field(default\_factory=list)

    allowed\_output\_schema\_refs: list\[str\] \= Field(default\_factory=list)

    prompt\_template\_refs: list\[str\] \= Field(default\_factory=list)

    system\_instruction\_refs: list\[str\] \= Field(default\_factory=list)

    tool\_access\_refs: list\[str\] \= Field(default\_factory=list)

    runtime\_endpoint\_ref: str

    deployment\_environment: DeploymentEnvironment

    hardware\_profile\_ref: Optional\[str\] \= None

    max\_latency\_ms: int

    timeout\_ms: int

    retry\_policy\_ref: Optional\[str\] \= None

    fallback\_model\_adapter\_ref: Optional\[str\] \= None

    privacy\_boundary: PrivacyBoundary

    data\_residency\_requirement: str

    pii\_allowed: bool \= False

    input\_sensitivity\_allowed: list\[SensitivityLevel\] \= Field(default\_factory=list)

    output\_sensitivity\_level: SensitivityLevel \= SensitivityLevel.INTERNAL

    model\_output\_usage: ModelOutputUsage

    required\_guards: list\[str\] \= Field(default\_factory=list)

    eval\_requirement\_refs: list\[str\] \= Field(default\_factory=list)

    safety\_rating\_ref: str

    model\_card\_ref: str

    license\_ref: str

    health\_check\_policy\_ref: str

    audit\_required: bool \= True

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

    replacement\_model\_adapter\_id: Optional\[str\] \= None

---

## **36\. Core Validation Function**

def validate\_model\_adapter\_invocation(

    entry: ModelAdapterRegistryEntry,

    caller\_agent\_type\_ref: str | None,

    caller\_service\_ref: str | None,

    task\_type: str,

    input\_schema\_ref: str,

    output\_schema\_ref: str,

    input\_sensitivity: SensitivityLevel,

    contains\_pii: bool,

) \-\> None:

    if entry.status \!= ModelAdapterStatus.ACTIVE:

        raise InvalidModelAdapterError(

            f"Model Adapter is not active: {entry.model\_adapter\_id}"

        )

    if caller\_agent\_type\_ref is not None:

        if caller\_agent\_type\_ref not in entry.allowed\_agent\_type\_refs:

            raise ModelAdapterCallerNotAllowedError(

                f"Agent Type '{caller\_agent\_type\_ref}' is not allowed to use "

                f"Model Adapter '{entry.model\_adapter\_id}'"

            )

    if caller\_service\_ref is not None:

        if caller\_service\_ref not in entry.allowed\_service\_refs:

            raise ModelAdapterCallerNotAllowedError(

                f"Service '{caller\_service\_ref}' is not allowed to use "

                f"Model Adapter '{entry.model\_adapter\_id}'"

            )

    if task\_type not in entry.allowed\_task\_types:

        raise ModelAdapterTaskNotAllowedError(

            f"Task Type '{task\_type}' is not allowed for "

            f"Model Adapter '{entry.model\_adapter\_id}'"

        )

    if input\_schema\_ref not in entry.allowed\_input\_schema\_refs:

        raise ModelAdapterSchemaMismatchError(

            f"Input schema '{input\_schema\_ref}' is not allowed"

        )

    if output\_schema\_ref not in entry.allowed\_output\_schema\_refs:

        raise ModelAdapterSchemaMismatchError(

            f"Output schema '{output\_schema\_ref}' is not allowed"

        )

    if input\_sensitivity not in entry.input\_sensitivity\_allowed:

        raise ModelAdapterSensitivityViolationError(

            f"Input sensitivity '{input\_sensitivity}' is not allowed"

        )

    if contains\_pii and not entry.pii\_allowed:

        raise ModelAdapterPIIViolationError(

            f"PII is not allowed for Model Adapter '{entry.model\_adapter\_id}'"

        )

    if entry.model\_output\_usage.may\_generate\_execution\_request:

        raise InvalidModelAdapterError(

            "Model Adapter must not be allowed to generate ExecutionRequest"

        )

    if not entry.required\_guards:

        raise InvalidModelAdapterError(

            "required\_guards must be declared"

        )

    if not entry.runtime\_endpoint\_ref:

        raise InvalidModelAdapterError(

            "runtime\_endpoint\_ref must be declared"

        )

    if not entry.decision\_boundary:

        raise InvalidModelAdapterError(

            "decision\_boundary must be declared"

        )

    if not entry.execution\_boundary:

        raise InvalidModelAdapterError(

            "execution\_boundary must be declared"

        )

    if not entry.safety\_boundary:

        raise InvalidModelAdapterError(

            "safety\_boundary must be declared"

        )

---

## **37\. Test Scenarios**

Required tests:

1\. Reject unregistered Model Adapter.

2\. Reject inactive Model Adapter.

3\. Verify restricted usage of degraded Model Adapter for safety-critical tasks.

4\. Reject runtime invocation of Model Adapter in maintenance status.

5\. Reject blocked Model Adapter.

6\. Reject unauthorized Agent Type invocation.

7\. Reject unauthorized Service invocation.

8\. Reject unauthorized Task Type.

9\. Reject Input Schema mismatch.

10\. Reject Output Schema mismatch.

11\. Reject PII input to an Adapter where PII is forbidden.

12\. Reject Privacy Boundary violation.

13\. Reject missing Required Guard.

14\. Reject model output attempting to create ApprovedAction.

15\. Reject model output attempting to create ApprovalDecision.

16\. Reject model output attempting to create ExecutionRequest.

17\. Reject model output attempting to create PhysicalCommand.

18\. Verify output schema violation handling.

19\. Verify output rejection on Guard failure.

20\. Verify fallback adapter behavior.

21\. Verify audit trace creation.

22\. Verify Model Adapter migration rules.

---

## **38\. Final Rule**

No registered Model Adapter,

no valid Model Invocation.

No valid Model Adapter,

no model invocation by Agent.

If the Agent Type is not allowed,

the Model Adapter cannot be used.

If the Task Type is not allowed,

the Model Adapter cannot be used.

Model output is not Evidence.

Model output is not Decision.

Model output is not Approval.

Model output is not Safety Gate.

Model output is not ExecutionRequest.

Model output is not PhysicalCommand.

Model Adapter is a model invocation path,

not an execution authority.

`model_adapter_registry` is the core deterministic registry that governs AI model invocation paths, runtimes, input schemas, output schemas, guards, privacy boundaries, latency, fallback, and audit rules in the LEDO system.

This module prevents Agents and Services from invoking unverified models and ensures that model outputs cannot cross Action, Decision, Approval, or Execution boundaries.

The core definition is:

Model Adapter Registry

\= not a list of model names,

but an operational contract registry that controls

the model references, runtime, endpoint, input schema,

output schema, Agent compatibility, task boundary,

guards, privacy, latency, fallback, and audit rules

of every adapter used to invoke AI/ML models in LEDO.

# 

