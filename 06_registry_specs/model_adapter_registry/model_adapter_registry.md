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

status: active

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

status: active

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

status: active

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

# **model\_adapter\_registry 설계 보고서**

## **1\. 개요**

`model_adapter_registry`는 LEDO Ontology-Centric Cyber-Physical System에서 사용되는 모든 AI / ML / LLM / SLM / Vision / TinyML / ONNX / TensorRT / vLLM / Ollama / API 기반 모델 호출 어댑터를 정의하고 통제하는 핵심 레지스트리이다.

이 모듈의 목적은 Agent, Service, Workflow가 검증되지 않은 모델을 임의로 호출하거나, 안전 경계를 벗어난 모델 출력을 Decision, Approval, Execution으로 오용하는 것을 방지하는 것이다.

`model_adapter_registry`는 단순한 모델 목록이 아니다.

이 레지스트리는 다음을 정의하는 **모델 호출 경로·런타임·입출력 계약·안전 경계 운영 계약 레지스트리**이다.

어떤 Model Adapter가 존재할 수 있는가?  
이 Adapter는 어떤 모델 또는 모델 런타임을 호출하는가?  
어떤 Agent Type이 이 Model Adapter를 사용할 수 있는가?  
어떤 입력 schema를 받아야 하는가?  
어떤 출력 schema를 반환해야 하는가?  
이 모델 출력은 ActionCandidate 생성에 사용할 수 있는가?  
이 모델 출력은 Evidence로 사용할 수 있는가?  
이 모델 출력은 Approval 또는 Execution에 직접 사용될 수 있는가?  
이 모델 호출에는 어떤 safety guard, ontology guard, policy guard가 필요한가?  
어떤 latency, cost, privacy, deployment boundary를 가져야 하는가?

즉, `model_adapter_registry`는 LEDO 시스템에서 모델 호출을 통제된 실행 경로로 만들기 위한 핵심 레지스트리이다.

---

## **2\. 핵심 원칙**

Model Adapter는 모델 호출 통로이다.

Model Adapter는 Agent가 아니다.

Model Adapter는 Decision Registry가 아니다.

Model Adapter는 Approval Authority가 아니다.

Model Adapter는 Safety Gate가 아니다.

Model Adapter는 ExecutionRequest를 만들 수 없다.

Model Adapter는 Physical Command를 만들 수 없다.

모델 출력의 기본 의미는 다음과 같다.

모델은 해석을 보조할 수 있다.  
모델은 분류를 보조할 수 있다.  
모델은 후보 생성을 보조할 수 있다.  
모델은 요약을 보조할 수 있다.  
모델은 위험 신호를 생성할 수 있다.

하지만 모델 출력은 곧 결정이 아니다.  
모델 출력은 곧 승인도 아니다.  
모델 출력은 곧 실행도 아니다.

핵심 원칙은 다음과 같다.

Model output supports interpretation.  
Ontology defines meaning.  
Policy defines permission.  
Decision Registry defines judgment flow.  
Approval Registry defines authority.  
Safety Gate validates execution readiness.

Model Adapter calls models.  
Model Adapter does not execute actions.

LEDO에서 모델은 **intent / classification / recommendation / extraction / summarization / candidate generation**을 도울 수 있지만, 결정론적 실행 경계를 대체하면 안 된다.

---

## **3\. LEDO 아키텍처 내 위치**

`model_adapter_registry`는 Distributed Domain Agent Layer와 Model Runtime / Inference Backend 사이에 위치한다.

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

LEDO 전체 흐름에서는 다음 위치에 있다.

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

## **4\. 목적**

`model_adapter_registry`의 목적은 다음과 같다.

1. 등록되지 않은 모델 호출 방지  
2. Agent별 사용 가능한 Model Adapter 제한  
3. Model Adapter별 호출 가능한 모델 및 runtime 정의  
4. 모델 입력 schema 정의  
5. 모델 출력 schema 정의  
6. 모델 출력의 사용 가능 범위 정의  
7. 모델 출력이 ActionCandidate로 전환될 수 있는 조건 정의  
8. 모델 출력이 Evidence로 사용될 수 있는 조건 정의  
9. 모델 출력이 직접 Approval 또는 Execution에 사용되는 것 방지  
10. LoRA / DAPT / fine-tuned model adapter 연결 관리  
11. local / edge / cloud / API runtime boundary 정의  
12. latency / cost / privacy / safety constraints 정의  
13. ontology guard 및 policy guard requirement 정의  
14. prompt template / system instruction reference 관리  
15. model evaluation score 및 safety rating reference 관리  
16. model adapter health check 및 fallback rule 정의  
17. audit 및 trace rule 정의  
18. versioning 및 migration 관리

---

## **5\. 핵심 구분**

### **5.1 Model**

`Model`은 실제 AI / ML 추론을 수행하는 모델이다.

예시:

qwen3\_coder\_30b  
safety\_slm\_v1  
hazard\_vision\_model\_v1  
worker\_proximity\_classifier\_v1  
robot\_dispatch\_slm\_v1  
tinyml\_vibration\_detector\_v1  
onnx\_hazard\_classifier\_v1  
tensorrt\_ppe\_detector\_v1

Model 자체의 metadata, eval score, training lineage, license, intended use는 `model_registry`가 관리할 수 있다.

---

### **5.2 Model Adapter**

`Model Adapter`는 LEDO 내부에서 특정 모델 또는 모델 런타임을 호출하기 위한 표준화된 통신·입출력 변환 계층이다.

예시:

ollama\_model\_adapter  
vllm\_model\_adapter  
onnx\_runtime\_adapter  
tensorrt\_inference\_adapter  
openai\_api\_model\_adapter  
local\_slm\_adapter  
tinyml\_edge\_adapter  
vision\_model\_adapter

Model Adapter는 다음을 수행한다.

표준 ModelRequest를 provider/runtime-specific request로 변환  
모델 응답을 표준 ModelOutput으로 변환  
timeout / retry / schema validation / logging 적용  
model output boundary 검증

---

### **5.3 Model Adapter Instance**

`Model Adapter Instance`는 실제 runtime에 등록된 개별 adapter이다.

예시:

model\_adapter:ollama\_qwen3\_site\_A  
model\_adapter:vllm\_safety\_slm\_site\_server\_A  
model\_adapter:onnx\_hazard\_edge\_camera\_03  
model\_adapter:tensorrt\_ppe\_edge\_gpu\_01  
model\_adapter:openai\_api\_reasoning\_gateway

Adapter Type은 설계 기준이고, Adapter Instance는 실제 호출 가능한 runtime endpoint이다.

---

### **5.4 Model Runtime**

`Model Runtime`은 모델이 실제로 실행되는 환경이다.

예시:

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

Model Adapter는 이 runtime을 호출한다.

---

### **5.5 Fine-tuning Adapter와 Model Adapter의 차이**

LoRA 같은 fine-tuning adapter와 `model_adapter_registry`의 adapter는 다르다.

LoRA Adapter:  
    모델 내부에 결합되는 parameter-efficient fine-tuning component

Model Adapter:  
    LEDO가 모델 또는 모델 runtime을 호출하기 위한 integration wrapper

예시:

lora:safety\_domain\_lora\_v1  
    → 모델 가중치에 결합되는 fine-tuning component

model\_adapter:vllm\_safety\_slm\_site\_A  
    → vLLM runtime을 통해 safety\_slm \+ LoRA 조합을 호출하는 LEDO 내부 adapter

LoRA, DAPT, fine-tuning lineage는 `model_registry` 또는 `model_component_registry`가 관리하고, `model_adapter_registry`는 그 모델 조합을 어떤 runtime path로 호출할지 관리한다.

---

### **5.6 Model Output Boundary**

Model Output Boundary는 모델 출력이 시스템 안에서 어디까지 사용될 수 있는지 정의한다.

허용 가능한 출력:

classification\_result  
extracted\_fact\_candidate  
risk\_signal  
recommendation  
summary  
evidence\_candidate  
action\_candidate\_draft  
natural\_language\_explanation

금지되는 출력:

ApprovedAction  
ApprovalDecision  
ExecutionRequest  
ExternalControlRequest  
PhysicalCommand  
PLCCommand  
RobotMotionPrimitive  
SafetyGatePass  
PolicyOverride

핵심 원칙:

Model Output ≠ Decision  
Model Output ≠ Approval  
Model Output ≠ Execution

---

## **6\. Scope**

`model_adapter_registry`는 다음 항목을 통제한다.

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

`model_adapter_registry`는 다음을 정의하지 않는다.

1. 모델의 전체 학습 데이터셋  
2. 모델 가중치 자체  
3. 전체 fine-tuning pipeline  
4. LoRA weight 파일 자체  
5. 전체 prompt text 원본  
6. policy pass/fail logic 전체  
7. ontology reasoning logic 전체  
8. Decision Rule 자체  
9. Approval Rule 자체  
10. Safety Gate 최종 판정  
11. physical execution command  
12. external system adapter 구현 전체  
13. GPU scheduler 전체  
14. Kubernetes deployment 전체  
15. 실제 API key / token / secret 값

이 책임들은 다음 모듈에 속한다.

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

## **8\. Model Adapter Type 모델**

권장 Model Adapter Type은 다음과 같다.

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

대형 언어 모델을 호출하는 adapter이다.

예시:

ollama\_qwen3\_adapter  
openai\_reasoning\_adapter  
vllm\_llm\_adapter

주로 다음 용도에 사용된다.

natural language interpretation  
summarization  
structured extraction  
planning support  
code assistance

Safety-critical execution 판단에는 직접 사용하면 안 된다.

---

### **8.2 SLM\_ADAPTER**

도메인 특화 소형 언어 모델을 호출하는 adapter이다.

예시:

safety\_slm\_adapter  
robot\_dispatch\_slm\_adapter  
inspection\_slm\_adapter

주로 edge 또는 site server에서 사용된다.

---

### **8.3 VISION\_MODEL\_ADAPTER**

카메라, 이미지, 비디오 기반 모델을 호출하는 adapter이다.

예시:

ppe\_detection\_adapter  
hazard\_detection\_vision\_adapter  
worker\_zone\_vision\_adapter

Vision output은 반드시 confidence, source frame, timestamp, model version을 가져야 한다.

---

### **8.4 ONNX\_RUNTIME\_ADAPTER**

ONNX Runtime 기반 모델을 호출하는 adapter이다.

예시:

onnx\_worker\_proximity\_classifier  
onnx\_hazard\_classifier

주로 portable inference에 사용된다.

---

### **8.5 TENSORRT\_ADAPTER**

NVIDIA TensorRT 기반 고속 inference adapter이다.

예시:

tensorrt\_ppe\_detector\_edge\_gpu\_01  
tensorrt\_hazard\_detector\_site\_gpu

주로 low-latency vision inference에 사용된다.

---

### **8.6 TINYML\_EDGE\_ADAPTER**

MCU 또는 edge device에서 TinyML 모델을 호출하는 adapter이다.

예시:

tinyml\_vibration\_detector  
tinyml\_sound\_anomaly\_detector  
tinyml\_gas\_pattern\_detector

TinyML output은 보통 event 또는 evidence candidate로 연결된다.

---

### **8.7 EMBEDDING\_MODEL\_ADAPTER**

문서, ontology label, event, evidence를 embedding하는 모델 adapter이다.

예시:

construction\_doc\_embedding\_adapter  
ontology\_label\_embedding\_adapter  
incident\_similarity\_embedding\_adapter

Embedding output은 safety decision의 단독 근거가 되면 안 된다.

---

### **8.8 RERANKER\_ADAPTER**

검색 결과나 RAG 후보를 재정렬하는 모델 adapter이다.

예시:

safety\_doc\_reranker  
bim\_issue\_reranker

Reranker는 retrieval quality를 높이는 보조 도구이다.

---

## **9\. Registry Entry Schema**

각 Model Adapter Registry entry는 다음 구조를 따른다.

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

## **10\. Registry Entry 예시: Safety SLM Adapter**

model\_adapter\_id: model\_adapter:safety\_slm\_vllm\_site\_A  
canonical\_name: safety\_slm\_vllm\_site\_A  
display\_name: Safety SLM Adapter \- Site A  
description: Site A의 safety risk analysis와 ActionCandidate draft 생성을 지원하는 vLLM 기반 Safety SLM adapter이다.  
semantic\_iri: ledo:SafetySLMAdapterSiteA

model\_adapter\_type: SLM\_ADAPTER  
model\_runtime\_type: vLLM  
model\_provider\_type: local\_site\_server

version: 1.0.0  
status: active

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

## **11\. Registry Entry 예시: Vision Hazard Detector Adapter**

model\_adapter\_id: model\_adapter:tensorrt\_hazard\_detector\_edge\_01  
canonical\_name: tensorrt\_hazard\_detector\_edge\_01  
display\_name: TensorRT Hazard Detector Adapter \- Edge 01  
description: Edge GPU 01에서 카메라 frame을 기반으로 hazard detection inference를 수행하는 TensorRT vision model adapter이다.  
semantic\_iri: ledo:TensorRTHazardDetectorAdapterEdge01

model\_adapter\_type: VISION\_MODEL\_ADAPTER  
model\_runtime\_type: TensorRT  
model\_provider\_type: edge\_gpu\_runtime

version: 1.0.0  
status: active

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

## **12\. Registry Entry 예시: Embedding Model Adapter**

model\_adapter\_id: model\_adapter:construction\_doc\_embedding\_site\_A  
canonical\_name: construction\_doc\_embedding\_site\_A  
display\_name: Construction Document Embedding Adapter \- Site A  
description: Site A의 문서, 안전 매뉴얼, BIM issue, incident report를 embedding하는 model adapter이다.  
semantic\_iri: ledo:ConstructionDocumentEmbeddingAdapterSiteA

model\_adapter\_type: EMBEDDING\_MODEL\_ADAPTER  
model\_runtime\_type: ONNX\_Runtime  
model\_provider\_type: local\_site\_server

version: 1.0.0  
status: active

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

Model Adapter는 다음 lifecycle과 연결된다.

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

중요한 점은 Model Adapter가 active라고 해서 모든 Agent가 사용할 수 있는 것은 아니라는 점이다.

Model Adapter가 active 상태여야 한다.  
Agent Type이 allowed\_agent\_type\_refs에 포함되어야 한다.  
Task Type이 허용되어야 한다.  
Input Schema가 일치해야 한다.  
Output Schema가 일치해야 한다.  
Privacy Boundary를 만족해야 한다.  
Required Guard가 적용되어야 한다.  
Model Output Boundary를 위반하지 않아야 한다.

---

## **14\. Validation Rules**

Model Adapter Entry는 다음 조건을 만족할 때만 유효하다.

1. `model_adapter_id`가 registry에 존재해야 한다.  
2. status가 `active`이어야 한다.  
3. model adapter type이 선언되어야 한다.  
4. model runtime type이 선언되어야 한다.  
5. model reference가 선언되어야 한다.  
6. allowed agent type 또는 allowed service가 선언되어야 한다.  
7. allowed task type이 선언되어야 한다.  
8. input schema reference가 선언되어야 한다.  
9. output schema reference가 선언되어야 한다.  
10. runtime endpoint reference가 선언되어야 한다.  
11. privacy boundary가 선언되어야 한다.  
12. model output usage boundary가 선언되어야 한다.  
13. required guard가 선언되어야 한다.  
14. eval requirement reference가 선언되어야 한다.  
15. safety rating reference가 선언되어야 한다.  
16. health check policy가 선언되어야 한다.  
17. decision / approval / execution / safety boundary가 선언되어야 한다.  
18. audit event reference가 선언되어야 한다.  
19. owner module이 선언되어야 한다.  
20. version이 유효해야 한다.  
21. deprecated 상태라면 migration metadata가 있어야 한다.

하나라도 누락되면 해당 Model Adapter는 operational lifecycle에 사용되면 안 된다.

---

## **15\. Runtime Model Invocation Validation**

Agent 또는 Service가 Model Adapter를 호출하기 전에는 다음 검증이 필요하다.

Model Adapter가 registry에 존재하는가?  
Model Adapter가 active 상태인가?  
호출 주체 identity가 유효한가?  
호출 주체의 Agent Type 또는 Service가 허용되어 있는가?  
Task Type이 allowed\_task\_types에 포함되어 있는가?  
Input Schema가 허용되어 있는가?  
Input sensitivity가 허용 범위 안에 있는가?  
PII 사용이 허용되어 있는가?  
Privacy Boundary를 위반하지 않는가?  
Runtime endpoint가 유효한가?  
Health Check가 통과되었는가?  
Required Guards가 적용되어 있는가?  
Timeout과 latency 정책을 만족하는가?

이 조건을 만족하지 못하면 모델 호출은 거부되어야 한다.

---

## **16\. Model Output Validation**

모델 출력은 반드시 검증되어야 한다.

검증 항목:

Output Schema가 일치하는가?  
출력에 금지된 lifecycle object가 포함되어 있지 않은가?  
ApprovedAction을 생성하려고 하지 않는가?  
ApprovalDecision을 생성하려고 하지 않는가?  
ExecutionRequest를 생성하려고 하지 않는가?  
PhysicalCommand 또는 low-level control instruction이 포함되어 있지 않은가?  
Ontology grounding이 가능한가?  
Policy reference가 필요한 경우 포함되어 있는가?  
Evidence로 사용할 경우 evidence\_registry 조건을 만족하는가?  
ActionCandidate로 전환할 경우 action\_registry 조건을 만족하는가?

모델 출력이 boundary를 위반하면 reject 또는 quarantine 처리해야 한다.

---

## **17\. Guard Rule**

Model Adapter는 필요한 guard를 명시해야 한다.

권장 guard:

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

입출력 schema를 검증한다.

---

### **17.2 ontology\_guard**

출력된 entity, relation, action, target이 ontology에 존재하는지 확인한다.

---

### **17.3 policy\_guard**

모델 출력이 policy boundary를 침범하지 않는지 확인한다.

---

### **17.4 safety\_guard**

safety-critical output이 안전 경계를 위반하지 않는지 확인한다.

---

### **17.5 pii\_guard**

PII가 외부 API 또는 허용되지 않은 runtime으로 전달되지 않도록 한다.

---

### **17.6 hallucination\_guard**

출력된 사실이 evidence, world state, ontology, retrieved source에 grounding되어 있는지 확인한다.

---

### **17.7 action\_boundary\_guard**

모델이 허용되지 않은 Action Type을 생성하지 못하도록 한다.

---

### **17.8 execution\_boundary\_guard**

모델이 ExecutionRequest 또는 PhysicalCommand를 생성하지 못하도록 한다.

---

## **18\. Privacy 및 Data Boundary Rule**

Model Adapter는 data boundary를 명확히 가져야 한다.

권장 privacy boundary:

local\_only  
site\_only  
enterprise  
external\_api\_allowed

### **18.1 local\_only**

데이터가 edge device 또는 local machine 밖으로 나가면 안 된다.

---

### **18.2 site\_only**

데이터가 특정 site server boundary 밖으로 나가면 안 된다.

---

### **18.3 enterprise**

기업 내부망 또는 approved enterprise environment 안에서만 처리 가능하다.

---

### **18.4 external\_api\_allowed**

외부 API 호출이 허용된다.

단, PII, safety-critical evidence, restricted site data는 별도 정책 없이는 외부 API로 전달하면 안 된다.

핵심 원칙:

PII and safety-critical site data must not be sent to external model APIs unless explicitly allowed by policy.

---

## **19\. Latency 및 Fallback Rule**

Model Adapter는 latency와 timeout 정책을 가져야 한다.

예시:

edge vision hazard detection: 200ms 이하  
worker proximity classifier: 100ms 이하  
safety SLM analysis: 3000ms 이하  
LLM report summarization: 10000ms 이하  
embedding generation: 500ms 이하

Fallback이 필요한 경우:

model runtime unavailable  
latency exceeded  
output schema invalid  
confidence too low  
guard failed  
external API unavailable

Fallback 결과는 task type에 따라 다르다.

Safety-critical:  
    block, hold, escalate, or use deterministic fallback

Low-risk summarization:  
    retry or defer

Robot dispatch:  
    hold\_for\_more\_evidence or supervisor review

Vision detection:  
    mark evidence as degraded or require secondary sensor

핵심 원칙:

Model failure must not silently become safe approval or execution.

---

## **20\. Evaluation Requirement Rule**

Model Adapter는 최소 evaluation requirement를 가져야 한다.

예시:

classification precision threshold  
false negative threshold  
hallucination rate threshold  
schema compliance rate  
ontology grounding rate  
latency threshold  
safety refusal correctness  
domain-specific benchmark score

Safety-critical model output에는 더 엄격한 평가 기준이 필요하다.

예시:

hazard detector:  
    false negative threshold must be extremely low

worker proximity classifier:  
    stale or low-confidence output must block dispatch

safety SLM:  
    must not generate ApprovedAction or ExecutionRequest

---

## **21\. Relationship to Model Registry**

`model_registry`는 모델 자체를 관리한다.

`model_adapter_registry`는 그 모델을 어떤 runtime과 endpoint를 통해 호출할지 관리한다.

model\_registry:  
    safety\_slm\_v1은 어떤 모델이고, 어떤 eval score와 model card를 가지는가?

model\_adapter\_registry:  
    safety\_slm\_v1을 vLLM site server에서 어떤 Agent가 어떤 task로 호출할 수 있는가?

모델이 등록되어 있어도 Model Adapter가 등록되어 있지 않으면 운영 시스템에서 호출하면 안 된다.

---

## **22\. Relationship to Agent Vocabulary Registry**

`agent_vocabulary_registry`는 Agent Type이 어떤 model reference 또는 model adapter reference를 사용할 수 있는지 정의한다.

`model_adapter_registry`는 해당 adapter가 실제로 그 Agent Type에게 허용되는지 검증한다.

agent\_vocabulary\_registry:  
    SAFETY\_RISK\_AGENT는 safety\_slm adapter를 사용할 수 있다.

model\_adapter\_registry:  
    safety\_slm\_vllm\_site\_A는 SAFETY\_RISK\_AGENT에게 허용되어 있는가?

Agent는 임의 Model Adapter를 호출하면 안 된다.

---

## **23\. Relationship to Evidence Registry**

Model output이 EvidenceCandidate로 사용될 경우 `evidence_registry` 검증을 받아야 한다.

model\_adapter\_registry:  
    이 model output은 evidence\_candidate를 생성할 수 있다.

evidence\_registry:  
    이 evidence\_candidate는 유효한 Evidence Type, schema, freshness, quality, lineage를 만족하는가?

모델 출력 자체가 곧 Evidence는 아니다.

Model Output ≠ Valid Evidence

---

## **24\. Relationship to Action Registry**

Model Adapter가 ActionCandidate draft를 생성할 수 있더라도, 실제 ActionCandidate는 `action_registry` 검증을 통과해야 한다.

model\_adapter\_registry:  
    safety\_slm은 STOP\_WORK ActionCandidate draft를 생성할 수 있다.

action\_registry:  
    STOP\_WORK Action Type은 등록되어 있고 active 상태인가?

모델은 등록되지 않은 Action Type을 생성하면 안 된다.

---

## **25\. Relationship to Decision Registry**

Model Output은 Decision Support가 될 수 있지만 Decision 그 자체는 아니다.

model\_adapter\_registry:  
    model output may support decision\_case analysis.

decision\_registry:  
    DecisionCase는 어떤 evidence, policy, risk, approval route를 따라야 하는가?

핵심 원칙:

Model Output ≠ DecisionCase  
Model Confidence ≠ Decision Outcome

---

## **26\. Relationship to Approval Registry**

Model Output은 approval support summary를 생성할 수 있지만 ApprovalDecision을 만들 수 없다.

model\_adapter\_registry:  
    model may summarize evidence for approver.

approval\_registry:  
    authorized human approver decides approval under rule and scope.

핵심 원칙:

Model must not approve.  
Agent must not approve.  
Only valid approval authority may approve.

---

## **27\. Relationship to Safety Gate**

Safety Gate는 모델 출력을 직접 신뢰하면 안 된다.

Safety Gate는 fresh runtime evidence, policy, capability, external system readiness를 검증해야 한다.

model\_adapter\_registry:  
    model may produce risk signal or evidence candidate.

safety\_gate:  
    verifies runtime conditions deterministically before ExecutionRequest.

핵심 원칙:

Model output must not replace Safety Gate validation.

---

## **28\. Relationship to Tool Registry**

Model Adapter는 사용할 수 있는 tool을 제한해야 한다.

예시 허용 tool:

ontology\_lookup\_readonly  
world\_state\_query\_readonly  
evidence\_bundle\_readonly  
document\_retrieval\_readonly  
schema\_validator

금지 tool:

execution\_dispatcher  
adapter\_direct\_call  
external\_system\_command\_sender  
approval\_decision\_writer  
policy\_override\_tool  
credential\_reader

모델은 실행계 tool을 직접 호출하면 안 된다.

---

## **29\. Relationship to Identity Registry**

Model Adapter 호출 주체는 identity를 가져야 한다.

identity\_registry:  
    agent:safety\_risk\_agent\_site\_A는 active identity인가?

model\_adapter\_registry:  
    이 identity의 Agent Type이 safety\_slm\_vllm\_site\_A를 호출할 수 있는가?

Identity 없는 모델 호출은 audit 불가능하므로 거부되어야 한다.

---

## **30\. Relationship to Audit Registry**

Model Adapter 호출과 출력은 audit 가능해야 한다.

Audit 대상:

model\_adapter\_invoked  
model\_input\_validated  
model\_output\_generated  
model\_output\_validated  
model\_output\_rejected  
model\_guard\_failed  
model\_latency\_exceeded  
model\_fallback\_used  
model\_adapter\_health\_changed

Audit Record는 다음을 포함해야 한다.

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

모든 중요한 Model Adapter는 semantic IRI를 가질 수 있다.

예시:

model\_adapter\_id: model\_adapter:safety\_slm\_vllm\_site\_A  
semantic\_iri: ledo:SafetySLMAdapterSiteA

Ontology에서는 다음과 같이 정의할 수 있다.

ledo:SafetySLMAdapterSiteA  
    rdf:type ledo:ModelAdapter ;  
    ledo:invokesModel ledo:SafetySLM ;  
    ledo:usesRuntime ledo:vLLM ;  
    ledo:allowedForAgent ledo:SafetyRiskAgent ;  
    ledo:mayGenerate ledo:ActionCandidateDraft ;  
    ledo:mustNotGenerate ledo:ExecutionRequest .

Ontology는 Model Adapter의 의미론적 기반을 제공한다.

Model Adapter Registry는 이를 운영 시스템에서 version, status, endpoint, schema, guard, privacy, latency, audit rule로 관리한다.

---

## **32\. Versioning 및 Migration**

Model Adapter Entry는 반드시 versioning되어야 한다.

다음 항목 중 하나라도 변경되면 version 변경이 필요하다.

1. model reference 변경  
2. model version 변경  
3. fine-tuning component 변경  
4. runtime endpoint 변경  
5. allowed agent type 변경  
6. allowed task type 변경  
7. input schema 변경  
8. output schema 변경  
9. prompt template 변경  
10. system instruction 변경  
11. tool access 변경  
12. privacy boundary 변경  
13. guard requirement 변경  
14. output usage boundary 변경  
15. latency / timeout 정책 변경  
16. fallback adapter 변경  
17. safety rating 변경  
18. decision / approval / execution / safety boundary 변경

Status 값:

draft  
active  
degraded  
maintenance  
deprecated  
retired  
blocked

### **32.1 degraded**

Model Adapter가 동작은 하지만 품질, latency, runtime health가 저하된 상태이다.

---

### **32.2 maintenance**

운영 유지보수 상태이다. Safety-critical task에는 사용하면 안 된다.

---

### **32.3 blocked**

보안, 안전, hallucination, schema violation, eval failure 등의 이유로 차단된 상태이다.

Blocked Model Adapter는 어떤 operational lifecycle에도 사용하면 안 된다.

---

## **33\. Implementation Use**

`model_adapter_registry`는 다음을 생성하거나 검증하는 데 사용된다.

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
20. Audit log expectation  
21. Test case generation  
22. Migration rules

Implementation은 등록되지 않은 Model Adapter를 호출하면 안 된다.

---

## **34\. 권장 Code Structure**

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

필수 테스트는 다음과 같다.

1\. 등록되지 않은 Model Adapter 거부  
2\. inactive Model Adapter 거부  
3\. degraded Model Adapter의 safety-critical task 사용 제한 검증  
4\. maintenance Model Adapter의 runtime 호출 거부  
5\. blocked Model Adapter 사용 거부  
6\. 허용되지 않은 Agent Type 호출 거부  
7\. 허용되지 않은 Service 호출 거부  
8\. 허용되지 않은 Task Type 거부  
9\. Input Schema 불일치 거부  
10\. Output Schema 불일치 거부  
11\. PII forbidden adapter에 PII 입력 거부  
12\. Privacy Boundary 위반 거부  
13\. Required Guard 누락 거부  
14\. Model output이 ApprovedAction 생성 시도 시 거부  
15\. Model output이 ApprovalDecision 생성 시도 시 거부  
16\. Model output이 ExecutionRequest 생성 시도 시 거부  
17\. Model output이 PhysicalCommand 생성 시도 시 거부  
18\. Output schema violation 처리 검증  
19\. Guard failure 시 output reject 검증  
20\. Fallback adapter 동작 검증  
21\. Audit trace 생성 검증  
22\. Model Adapter migration rule 검증

---

## **38\. Final Rule**

등록된 Model Adapter가 없으면,  
유효한 Model Invocation도 없다.

유효한 Model Adapter가 없으면,  
Agent는 모델을 호출할 수 없다.

허용된 Agent Type이 아니면,  
Model Adapter를 사용할 수 없다.

허용된 Task Type이 아니면,  
Model Adapter를 사용할 수 없다.

모델 출력은 Evidence가 아니다.  
모델 출력은 Decision이 아니다.  
모델 출력은 Approval이 아니다.  
모델 출력은 Safety Gate가 아니다.  
모델 출력은 ExecutionRequest가 아니다.  
모델 출력은 PhysicalCommand가 아니다.

Model Adapter는 모델 호출 통로이지,  
실행 권한자가 아니다.

`model_adapter_registry`는 LEDO 시스템에서 AI 모델 호출 경로, 런타임, 입력 schema, 출력 schema, guard, privacy boundary, latency, fallback, audit rule을 통제하는 핵심 결정론적 레지스트리이다.

이 모듈은 Agent와 Service가 검증되지 않은 모델을 호출하지 못하게 하고, 모델 출력이 Action, Decision, Approval, Execution의 경계를 침범하지 못하도록 보장한다.

핵심 정의는 다음과 같다.

Model Adapter Registry  
\= 모델 이름 목록이 아니라,  
LEDO에서 AI/ML 모델을 호출하는 모든 adapter의  
모델 참조, runtime, endpoint, 입력 schema, 출력 schema,  
Agent compatibility, task boundary, guard, privacy,  
latency, fallback, audit rule을 통제하는  
모델 호출 운영 계약 레지스트리

