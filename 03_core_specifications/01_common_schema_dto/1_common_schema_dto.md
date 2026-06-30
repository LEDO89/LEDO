# **1\. Purpose**

This document defines the common Schema / DTO list used in the ontology-centric cyber-physical platform.

DTO stands for Data Transfer Object, and it is the standard object format used to move data inside the system.

This document does not provide a long explanation of why this lifecycle is necessary.

That topic is covered in a separate Lifecycle document.

The role of this document is to focus on the following:

Which DTOs are required  
Which fields each DTO should contain  
Which DTO moves between which layers  
Which DTO requires trace, version, idempotency, and validation information  
Which lightweight DTOs should be used for high-frequency data  
How untrusted external inputs should be validated  
Which DTOs should become typed models in Pydantic implementation, and which DTOs should keep flexible payloads

---

# **2\. Document Boundary**

## **2.1 What This Document Covers**

This document covers the following:

DTO list  
DTO fields  
Reference structure between DTOs  
Common context  
Trace context  
Version context  
Source metadata  
Reference DTOs  
Event DTOs  
Ontology binding DTOs  
Evidence DTOs  
World state DTOs  
Action / decision / approval DTOs  
Execution / feedback / audit DTOs  
Registry / governance DTOs  
High-frequency DTOs  
Validation DTOs  
Pydantic implementation strategy

## **2.2 What This Document Does Not Cover**

This document does not explain the following topics in detail:

Overall lifecycle philosophy  
Why only ApprovedAction can be executed  
Full operating philosophy of the Emergency Fast-Path  
Full purpose of the Monitoring-Only Path  
Full execution model of Saga / Event Sourcing  
Internal policy decision logic of the Safety Gate  
Ontology reasoning strategy  
OPA / OpenFGA policy engine design

These topics are covered in separate Lifecycle / Architecture / Governance documents.

---

# **3\. Core Principles**

## **3.1 DTOs Do Not Execute**

A DTO is a data structure.

A DTO does not make decisions.  
A DTO does not execute actions.  
A DTO does not call external systems.  
A DTO does not evaluate policies.  
A DTO does not directly perform ontology reasoning.

The role of a DTO is as follows:

It holds data.  
It provides a verifiable format.  
It maintains trace information.  
It maintains version information.  
It provides a standard structure that other layers can process.

---

## **3.2 The Schema Layer Must Be at the Bottom**

`schemas/` may be imported by every layer.

However, `schemas/` must not import business layers.

Allowed direction:

schemas  
→ common enum  
→ primitive type  
→ standard library  
→ pydantic

Forbidden direction:

schemas  
→ safety\_gate

schemas  
→ agents

schemas  
→ execution\_core

schemas  
→ external\_adapters

schemas  
→ ontology\_core runtime service

Schema is the common language of the entire platform, so it must be the most stable and independent layer.

---

## **3.3 DTOs Are Contracts, and Services Perform Processing**

A DTO defines structure.

Processing is performed by each service.

Examples:

CanonicalEventEnvelopeDTO  
→ created by event\_normalizer.py

OntologyBindingDTO  
→ created by semantic\_binder.py

WorldStateUpdateDTO  
→ applied by state\_store.py

ActionCandidateDTO  
→ created by an agent or rule engine

ApprovedActionDTO  
→ created by safety\_gate

ExecutionRequestDTO  
→ created by execution\_core

FeedbackEventDTO  
→ created by an external adapter or feedback handler

AuditRecordDTO  
→ created by the audit layer

---

# **4\. Schema Versioning Policy**

DTOs may change over time.

Therefore, all major DTOs should have version context.

## **4.1 Basic Version Fields**

Major DTOs should include the following fields:

schema\_version  
lifecycle\_version  
ontology\_version  
policy\_bundle\_version  
mapping\_table\_version  
adapter\_version

Not every DTO must include every version field.

However, version context is strongly recommended for the following DTOs:

CanonicalEventEnvelopeDTO  
OntologyBoundEventDTO  
EvidenceDTO  
WorldStateUpdateDTO  
ActionCandidateDTO  
DecisionCaseDTO  
ApprovedActionDTO  
ExecutionRequestDTO  
FeedbackEventDTO  
AuditRecordDTO

---

## **4.2 Backward-Compatible Change**

The following changes are generally considered backward-compatible changes:

Adding an optional field  
Adding a new enum value  
Adding a new event type  
Adding new optional metadata  
Adding a new monitoring metric  
Adding a new source-specific DTO  
Strengthening a validator while preserving existing fields

Example:

v1.2 → v1.3

Adding an optional field to WorldStateUpdateDTO  
Adding an optional label field to MonitoringOnlyEventDTO

---

## **4.3 Breaking Change**

The following changes are considered breaking changes:

Removing a required field  
Renaming a required field  
Changing a field type  
Changing the meaning of an enum value  
Changing idempotency semantics  
Changing execution boundary semantics  
Changing the structure of ApprovedAction / ExecutionRequest  
Changing the audit trace linkage model

Example:

v1.x → v2.0

Forcefully changing ExecutionRequestDTO.required\_feedback to expected\_feedback\_contract  
Changing the structure of ApprovedActionDTO.target\_ref

---

## **4.4 Deprecation Policy**

Fields should not be deleted immediately.

Recommended process:

Mark the field as deprecated  
Add a replacement field  
Operate a dual-write period  
Migrate downstream consumers  
Verify audit compatibility  
Remove the field in a major version

---

## **4.5 Schema Compatibility Rule**

Older event, audit, feedback, and execution records must remain interpretable.

Therefore, the following principles should be followed:

AuditRecordDTO preserves the schema\_version at the time of creation.  
ExecutionRequestDTO preserves the policy\_bundle\_version at the time of creation.  
WorldStateUpdateDTO preserves the ontology\_version at the time of creation.  
FeedbackEventDTO preserves the external adapter version.

---

# **5\. Untrusted Input Validation Layer**

Inputs coming from outside are untrusted by default.

RawInputDTO, MobileContextInputDTO, LLMOutputInputDTO, DocumentParseInputDTO, and IndustrialRawInputDTO are all treated as untrusted inputs.

## **5.1 Validation Stages**

Input must pass through the following validation layers:

Transport validation  
Schema validation  
Size limit validation  
Encoding validation  
Checksum validation  
Source authentication  
Source authorization  
Rate limiting  
Replay detection  
Timestamp sanity check  
Payload sanitization  
Prompt injection filtering  
Document provenance check  
Media integrity check

---

## **5.2 ValidationResultDTO**

Represents the result of input validation.

Fields:

validation\_id  
input\_ref  
validation\_status  
validation\_errors  
sanitized  
sanitization\_notes  
rate\_limited  
replay\_detected  
source\_authenticated  
source\_authorized  
validated\_at\_utc

Examples of validation\_status:

PASSED  
FAILED  
PARTIALLY\_PASSED  
QUARANTINED  
REJECTED

---

## **5.3 SanitizedInputDTO**

This is an input that has passed validation and sanitization.

Fields:

sanitized\_input\_id  
raw\_input\_ref  
sanitized\_payload  
removed\_fields  
normalization\_notes  
validation\_result\_ref  
trace\_context  
created\_at\_utc

Purpose:

Instead of sending RawInputDTO directly to CanonicalEventEnvelopeDTO, the input passes through SanitizedInputDTO when needed.

---

## **5.4 RateLimitContextDTO**

Represents input rate limiting by source.

Fields:

source\_id  
limit\_key  
allowed\_rate  
observed\_rate  
window\_start\_utc  
window\_end\_utc  
rate\_limited  
action\_taken

Purpose:

Applied to high-frequency data, external API input, mobile input, LLM tool output, and similar sources.

---

## **5.5 Rule**

Untrusted input does not enter the semantic pipeline directly.

RawInputDTO  
→ ValidationResultDTO  
→ SanitizedInputDTO  
→ CanonicalEventEnvelopeDTO

Or, for high-frequency data:

RawInputDTO  
→ ValidationResultDTO  
→ TimeSeriesBundleInputDTO  
→ MonitoringOnlyEventDTO

---

# **6\. TraceContext Standard Mapping Rules**

TraceContextDTO can easily be misunderstood during development, so it must have clear meanings.

## **6.1 trace\_id**

The top-level trace ID that groups one entire lifecycle.

Example:

A full flow starting from a gas sensor alarm and continuing through ActionCandidate, ApprovedAction, ExecutionRequest, FeedbackEvent, and AuditRecord shares the same trace\_id.

---

## **6.2 correlation\_id**

Connects objects that are not in a direct causal relationship but belong to the same incident group or operation.

Example:

GasSensorReadingEvent and WorkerLocationChangedEvent may not have a direct causal relationship.

However, because they are used in the same risk decision, they may share the same correlation\_id.

---

## **6.3 causation\_id**

The ID of the direct causal object.

Standard rule:

If event A causes candidate B to be created, then B’s causation\_id is A’s event\_id.

Example:

GasSensorReadingEvent\_001  
→ ActionCandidate\_001 is created

ActionCandidate\_001.causation\_id \= GasSensorReadingEvent\_001.event\_id

ActionCandidate\_001  
→ DecisionCase\_001 is created

DecisionCase\_001.causation\_id \= ActionCandidate\_001.candidate\_id

ApprovedAction\_001  
→ ExecutionRequest\_001 is created

ExecutionRequest\_001.causation\_id \= ApprovedAction\_001.approved\_action\_id

---

## **6.4 span\_id / parent\_span\_id**

Used to track stage-level processing in distributed tracing.

Examples:

ingestion span  
validation span  
canonicalization span  
ontology binding span  
safety gate span  
execution dispatch span

---

## **6.5 request\_id**

The ID of an external API call or user request.

---

# **7\. Pydantic Payload Strategy**

## **7.1 Practical Principle**

Do not apply Generics to every DTO.

Generics are powerful, but applying them everywhere can reduce development productivity.

Therefore, they should be applied differently depending on the path.

---

## **7.2 MVP Strategy**

In the MVP, prioritize the following:

payload: dict  
metadata: dict  
Use GenericPayloadDTO  
Strictly validate only core DTO structures  
Strongly validate Action / Execution / Emergency DTOs

Typed Generics are optional in the MVP.

---

## **7.3 Production Strategy**

In production, apply typed payloads mainly to high-risk paths.

Priority targets for Typed Generics:

EmergencyApprovedActionDTO  
ExecutionRequestDTO  
ExternalControlRequestDTO  
FeedbackEventDTO  
EvidenceDTO  
ApprovedActionDTO  
CanonicalEventEnvelopeDTO for safety-critical events

DTOs where Typed Generics can be delayed:

MonitoringOnlyEventDTO  
TimeSeriesSampleDTO  
low-risk telemetry  
experimental source adapter  
UnclassifiedEntityDTO  
LLM draft output

---

## **7.4 Monitoring Path Strategy**

The monitoring path should remain as lightweight as possible.

Recommended:

bundle-level trace\_context  
bundle-level source\_metadata  
sample-level timestamp  
sample-level sequence\_number  
sample-level value  
sample-level quality

Not recommended:

full TraceContextDTO for every sample  
VersionContextDTO for every sample  
OntologyBindingDTO for every sample  
EvidenceDTO for every sample

---

## **7.5 Generic Usage Examples**

Conceptual structure:

CanonicalEventEnvelopeDTO\[T\]  
RawInputDTO\[T\]  
EvidenceDTO\[T\]  
FeedbackEventDTO\[T\]

Examples:

CanonicalEventEnvelopeDTO\[GasSensorPayloadDTO\]  
CanonicalEventEnvelopeDTO\[RobotMissionPayloadDTO\]  
EvidenceDTO\[InspectionEvidencePayloadDTO\]  
FeedbackEventDTO\[SmartHelmetAckPayloadDTO\]

---

# **8\. Full DTO Groups**

Common DTOs are divided into 11 groups.

Base / Context DTO  
Validation DTO  
Reference DTO  
Input / Event DTO  
High-Frequency / Monitoring DTO  
Ontology Binding DTO  
Evidence / World State DTO  
Candidate / Decision / Approval DTO  
Approved Action / Execution DTO  
Feedback / Audit DTO  
Registry / Governance / Observability DTO

---

# **9\. Base / Context DTO**

## **9.1 BaseDTO**

Fields:

id  
created\_at\_utc  
updated\_at\_utc  
schema\_version  
lifecycle\_version  
metadata

---

## **9.2 TraceContextDTO**

Fields:

trace\_id  
correlation\_id  
causation\_id  
parent\_span\_id  
span\_id  
request\_id

---

## **9.3 VersionContextDTO**

Fields:

schema\_version  
lifecycle\_version  
ontology\_version  
policy\_bundle\_version  
mapping\_table\_version  
adapter\_version

---

## **9.4 SourceMetadataDTO**

Fields:

source\_type  
source\_id  
source\_name  
source\_protocol  
source\_system  
source\_trust\_level  
ingested\_at\_utc  
raw\_ref

---

## **9.5 FreshnessDTO**

Fields:

timestamp\_utc  
ingested\_at\_utc  
freshness\_ms  
valid\_until  
is\_stale

---

## **9.6 ConfidenceDTO**

Fields:

confidence\_score  
confidence\_level  
confidence\_reason  
source\_quality  
validation\_status

---

## **9.7 GenericPayloadDTO**

Fields:

payload\_type  
payload\_schema\_version  
payload  
payload\_hash  
validation\_status

---

# **10\. Validation DTO**

## **10.1 ValidationResultDTO**

Fields:

validation\_id  
input\_ref  
validation\_status  
validation\_errors  
sanitized  
sanitization\_notes  
rate\_limited  
replay\_detected  
source\_authenticated  
source\_authorized  
validated\_at\_utc

---

## **10.2 SanitizedInputDTO**

Fields:

sanitized\_input\_id  
raw\_input\_ref  
sanitized\_payload  
removed\_fields  
normalization\_notes  
validation\_result\_ref  
trace\_context  
created\_at\_utc

---

## **10.3 RateLimitContextDTO**

Fields:

source\_id  
limit\_key  
allowed\_rate  
observed\_rate  
window\_start\_utc  
window\_end\_utc  
rate\_limited  
action\_taken

---

# **11\. Reference DTO**

## **11.1 EntityRefDTO**

Fields:

entity\_id  
entity\_type  
canonical\_id  
display\_name  
ontology\_iri  
runtime\_key

---

## **11.2 LocationRefDTO**

Fields:

location\_id  
location\_type  
site\_id  
zone\_id  
floor\_id  
coordinates  
ontology\_iri

---

## **11.3 OntologyRefDTO**

Fields:

ontology\_iri  
ontology\_class  
ontology\_property  
domain\_module  
runtime\_key  
label

---

## **11.4 EvidenceRefDTO**

Fields:

evidence\_id  
evidence\_type  
source\_id  
timestamp\_utc  
confidence\_score  
summary

---

## **11.5 PolicyRefDTO**

Fields:

policy\_id  
policy\_type  
policy\_version  
policy\_bundle\_version  
decision\_result

---

## **11.6 ActorRefDTO**

Fields:

actor\_id  
actor\_type  
role  
organization  
clearance\_level  
ontology\_iri

---

# **12\. Input / Event DTO**

## **12.1 RawInputDTO**

Fields:

raw\_input\_id  
source\_metadata  
raw\_payload  
received\_at\_utc  
raw\_format  
encoding  
checksum  
trace\_context

---

## **12.2 CanonicalEventEnvelopeDTO**

Fields:

event\_id  
event\_type  
source\_metadata  
subject\_ref  
location\_ref  
timestamp\_utc  
payload  
confidence  
freshness  
trace\_context  
version\_context  
emergency\_hint  
criticality\_hint  
lifecycle\_path\_hint

---

## **12.3 PathClassificationDTO**

Fields:

path\_type  
classification\_reason  
risk\_hint  
emergency\_detected  
monitoring\_only\_allowed  
standard\_path\_required  
classified\_at\_utc

Examples of path\_type:

STANDARD  
EMERGENCY\_FAST\_PATH  
MONITORING\_ONLY

---

## **12.4 EventTypeDTO**

Fields:

event\_type  
event\_category  
domain\_module  
allowed\_subject\_types  
default\_lifecycle\_path  
requires\_evidence  
can\_generate\_candidate

---

# **13\. High-Frequency / Monitoring DTO**

## **13.1 TimeSeriesSampleDTO**

Fields:

timestamp\_utc  
value  
unit  
quality  
sequence\_number  
sample\_status

Important:

Individual samples do not include full trace\_context.

---

## **13.2 TimeSeriesBundleInputDTO**

Fields:

bundle\_id  
source\_metadata  
subject\_ref  
signal\_name  
unit  
samples  
window\_start\_utc  
window\_end\_utc  
sample\_count  
sampling\_rate\_hz  
trace\_context  
version\_context

Important:

trace\_context is maintained at the bundle level.  
Sample-level trace is prohibited by default.

---

## **13.3 WindowedInputDTO**

Fields:

window\_id  
source\_metadata  
window\_start\_utc  
window\_end\_utc  
events  
aggregation\_type  
statistics  
trace\_context

Examples of aggregation\_type:

RAW\_SAMPLES  
AVERAGE  
MIN\_MAX  
COUNT  
LAST\_VALUE  
THRESHOLD\_CROSSING

---

## **13.4 MonitoringPayloadDTO**

Fields:

metric\_name  
metric\_value  
unit  
timestamp\_utc  
quality  
is\_threshold\_crossed  
threshold\_ref  
summary\_status

---

## **13.5 MonitoringOnlyEventDTO**

Fields:

monitoring\_event\_id  
source\_metadata  
subject\_ref  
monitoring\_payload  
freshness  
trace\_context  
optional\_ontology\_ref  
path\_type

Note:

MonitoringOnlyEventDTO does not directly create ActionCandidate.

---

## **13.6 EscalationTriggerDTO**

Fields:

trigger\_id  
source\_event\_ref  
trigger\_reason  
from\_path  
to\_path  
threshold\_ref  
detected\_at\_utc  
trace\_context

---

# **14\. Ontology Binding DTO**

## **14.1 CanonicalIdentityDTO**

Fields:

raw\_identifier  
canonical\_id  
canonical\_iri  
runtime\_key  
alias\_matched  
mapping\_confidence  
mapping\_table\_version

---

## **14.2 OntologyBindingDTO**

Fields:

binding\_id  
entity\_ref  
ontology\_class  
ontology\_property  
ontology\_individual  
domain\_module  
runtime\_key  
binding\_confidence  
binding\_status  
binding\_errors

Examples of binding\_status:

BOUND  
PARTIALLY\_BOUND  
BINDING\_FAILED  
UNCLASSIFIED

---

## **14.3 OntologyBoundEventDTO**

Fields:

event\_id  
canonical\_event  
ontology\_bindings  
subject\_ref  
state\_type  
event\_semantics  
evidence\_candidate  
trace\_context

---

## **14.4 UnclassifiedEntityDTO**

Fields:

unclassified\_id  
raw\_identifier  
source\_metadata  
observed\_payload  
possible\_entity\_types  
reason  
risk\_blocked  
mapping\_review\_required  
created\_at\_utc

---

## **14.5 MappingProposalDTO**

Fields:

proposal\_id  
unclassified\_entity\_id  
proposed\_canonical\_id  
proposed\_ontology\_class  
proposed\_domain\_module  
reasoning\_summary  
supporting\_evidence\_refs  
confidence\_score  
requires\_human\_approval

---

# **15\. Evidence / World State DTO**

## **15.1 EvidenceDTO**

Fields:

evidence\_id  
evidence\_type  
source\_metadata  
subject\_ref  
location\_ref  
payload  
timestamp\_utc  
confidence  
freshness  
trace\_context  
provenance  
validation\_status

---

## **15.2 EvidenceBundleDTO**

Fields:

bundle\_id  
evidence\_refs  
bundle\_purpose  
summary  
minimum\_required\_evidence\_met  
conflicting\_evidence\_detected  
created\_at\_utc

---

## **15.3 WorldStateDTO**

Fields:

state\_id  
entity\_ref  
state\_type  
state\_value  
source\_ref  
evidence\_ref  
timestamp\_utc  
freshness  
confidence  
valid\_until  
trace\_context  
version

---

## **15.4 WorldStateUpdateDTO**

Fields:

update\_id  
entity\_ref  
previous\_state  
new\_state  
change\_reason  
evidence\_refs  
updated\_by  
updated\_at\_utc  
trace\_context  
idempotency\_key  
state\_version  
expected\_previous\_version  
deduplication\_window\_ms

---

## **15.5 StateSnapshotDTO**

Fields:

snapshot\_id  
site\_id  
snapshot\_time\_utc  
states  
ontology\_version  
policy\_context\_version  
created\_at\_utc

---

# **16\. Candidate / Decision / Approval DTO**

## **16.1 IntentDTO**

Fields:

intent\_id  
intent\_type  
requested\_by  
target\_ref  
reason  
source\_event\_ref  
confidence  
trace\_context

---

## **16.2 ActionCandidateDTO**

Fields:

candidate\_id  
action\_type  
target\_ref  
target\_location  
proposed\_by  
reason  
risk\_level  
evidence\_refs  
confidence  
constraints  
required\_capabilities  
requires\_approval  
created\_at\_utc  
trace\_context

---

## **16.3 DecisionCaseDTO**

Fields:

decision\_case\_id  
candidate\_ref  
decision\_tier  
risk\_level  
urgency  
routing\_result  
required\_approval  
policy\_precheck\_result  
evidence\_summary  
state\_freshness\_result  
recommended\_next\_step  
trace\_context

---

## **16.4 ApprovalRequestDTO**

Fields:

approval\_request\_id  
decision\_case\_ref  
action\_type  
target\_ref  
required\_role  
required\_clearance  
approver\_ref  
approval\_status  
approval\_reason  
expires\_at\_utc  
created\_at\_utc  
approved\_at\_utc  
trace\_context

---

## **16.5 ApprovalDecisionDTO**

Fields:

approval\_decision\_id  
approval\_request\_ref  
decision  
decided\_by  
decision\_reason  
decision\_time\_utc  
policy\_refs  
trace\_context

---

# **17\. Approved Action / Execution DTO**

## **17.1 ApprovedActionDTO**

Fields:

approved\_action\_id  
candidate\_ref  
decision\_case\_ref  
action\_type  
target\_ref  
constraints  
approval\_context  
policy\_result  
evidence\_refs  
risk\_level  
valid\_until  
idempotency\_key  
trace\_context  
created\_at\_utc

---

## **17.2 EmergencyApprovedActionDTO**

Fields:

emergency\_approved\_action\_id  
emergency\_policy\_id  
emergency\_condition\_id  
action\_type  
target\_ref  
minimal\_evidence\_refs  
local\_rule\_result  
idempotency\_key  
timeout\_policy  
expected\_feedback  
post\_hoc\_audit\_required  
is\_emergency\_bypass  
post\_audit\_status  
trace\_context  
created\_at\_utc

Examples of post\_audit\_status:

PENDING  
REVIEWED  
APPROVED  
REJECTED  
ESCALATED

---

## **17.3 ExecutionRequestDTO**

Fields:

execution\_request\_id  
approved\_action\_ref  
action\_type  
target\_ref  
external\_system\_type  
external\_system\_id  
execution\_constraints  
expected\_feedback  
timeout\_policy  
retry\_policy  
recovery\_policy  
idempotency\_key  
execution\_lease  
trace\_context  
created\_at\_utc

---

## **17.4 ExternalControlRequestDTO**

Fields:

external\_request\_id  
execution\_request\_ref  
adapter\_id  
external\_system\_type  
protocol  
endpoint  
payload  
idempotency\_key  
timeout\_policy  
expected\_feedback  
trace\_context  
sent\_at\_utc

---

## **17.5 TimeoutPolicyDTO**

Fields:

timeout\_ms  
on\_timeout\_action  
max\_wait\_ms  
requires\_recovery  
notify\_actor\_refs

---

## **17.6 RetryPolicyDTO**

Fields:

max\_retries  
retry\_interval\_ms  
backoff\_strategy  
retryable\_errors  
non\_retryable\_errors

---

## **17.7 RecoveryPolicyDTO**

Fields:

recovery\_policy\_id  
recovery\_type  
safe\_state\_target  
compensating\_action\_type  
manual\_override\_required  
notify\_actor\_refs

---

## **17.8 IdempotencyContextDTO**

Fields:

idempotency\_key  
deduplication\_window\_ms  
original\_request\_id  
duplicate\_detected  
dedupe\_strategy

Used by:

WorldStateUpdateDTO  
ApprovedActionDTO  
EmergencyApprovedActionDTO  
ExecutionRequestDTO  
ExternalControlRequestDTO

---

# **18\. Feedback / Audit DTO**

## **18.1 FeedbackEventDTO**

Fields:

feedback\_event\_id  
execution\_request\_ref  
external\_request\_ref  
source\_system  
feedback\_type  
status  
payload  
timestamp\_utc  
confidence  
trace\_context  
correlation\_id  
error\_code  
recovery\_required  
is\_emergency\_bypass  
post\_audit\_required

---

## **18.2 WorldStateReconciliationDTO**

Fields:

reconciliation\_id  
feedback\_event\_ref  
affected\_state\_refs  
previous\_states  
reconciled\_states  
conflict\_detected  
reconciliation\_result  
created\_at\_utc  
trace\_context

---

## **18.3 ExecutionStateDTO**

Fields:

execution\_state\_id  
execution\_request\_ref  
state  
last\_feedback\_ref  
updated\_at\_utc  
timeout\_at\_utc  
recovery\_required  
trace\_context

Examples of state:

CREATED  
DISPATCH\_PENDING  
DISPATCHED  
ACKNOWLEDGED  
ACCEPTED  
STARTED  
IN\_PROGRESS  
COMPLETED  
FAILED  
TIMEOUT  
FEEDBACK\_MISSING  
RECOVERY\_REQUIRED  
CLOSED

---

## **18.4 PostHocAuditDTO**

Fields:

post\_hoc\_audit\_id  
emergency\_approved\_action\_ref  
execution\_request\_ref  
feedback\_event\_refs  
review\_status  
reviewer\_ref  
review\_comment  
reviewed\_at\_utc  
required\_followup\_actions  
trace\_context

Examples of review\_status:

PENDING  
REVIEWED  
APPROVED  
REJECTED  
ESCALATED  
REQUIRES\_POLICY\_UPDATE  
REQUIRES\_ONTOLOGY\_UPDATE

---

## **18.5 AuditRecordDTO**

Fields:

audit\_record\_id  
trace\_id  
lifecycle\_path  
event\_refs  
evidence\_refs  
candidate\_ref  
decision\_case\_ref  
approval\_request\_ref  
approved\_action\_ref  
execution\_request\_ref  
external\_request\_ref  
feedback\_event\_ref  
policy\_refs  
actor\_refs  
final\_status  
created\_at\_utc  
is\_emergency\_bypass  
post\_audit\_status  
post\_hoc\_audit\_ref

---

# **19\. Registry / Governance / Observability DTO**

## **19.1 ActionTypeSpecDTO**

Fields:

action\_type  
description  
allowed\_target\_types  
required\_evidence\_types  
required\_roles  
default\_risk\_level  
requires\_approval  
allowed\_external\_systems  
expected\_feedback\_types

---

## **19.2 EmergencyActionSpecDTO**

Fields:

emergency\_action\_type  
emergency\_condition\_type  
allowed\_target\_types  
required\_minimal\_evidence  
local\_rule\_id  
policy\_id  
allowed\_external\_systems  
required\_feedback  
timeout\_policy  
recovery\_policy  
audit\_level  
approval\_model  
post\_hoc\_audit\_required  
version  
owner  
valid\_from  
valid\_until

---

## **19.3 EventTypeSpecDTO**

Fields:

event\_type  
domain\_module  
allowed\_sources  
allowed\_subject\_types  
default\_lifecycle\_path  
can\_generate\_evidence  
can\_generate\_candidate  
monitoring\_only\_allowed  
emergency\_trigger\_allowed  
supports\_batching  
supports\_windowing

---

## **19.4 StateTypeSpecDTO**

Fields:

state\_type  
entity\_type  
value\_type  
allowed\_values  
freshness\_requirement\_ms  
confidence\_requirement  
is\_safety\_critical  
requires\_idempotent\_update

---

## **19.5 CapabilitySpecDTO**

Fields:

capability\_id  
capability\_type  
owner\_entity\_type  
constraints  
required\_conditions  
risk\_level  
ontology\_iri

---

## **19.6 AdapterSpecDTO**

Fields:

adapter\_id  
adapter\_type  
external\_system\_type  
supported\_action\_types  
protocol  
endpoint\_ref  
timeout\_policy  
retry\_policy  
health\_status

---

## **19.7 PolicyDecisionDTO**

Fields:

policy\_decision\_id  
policy\_refs  
input\_context  
decision\_result  
reason  
obligations  
denial\_reasons  
evaluated\_at\_utc

Examples of decision\_result:

ALLOW  
DENY  
REQUIRE\_APPROVAL  
ESCALATE  
EMERGENCY\_ALLOW

---

## **19.8 MappingReviewDTO**

Fields:

mapping\_review\_id  
mapping\_proposal\_ref  
reviewer\_ref  
review\_status  
review\_comment  
approved\_mapping  
created\_at\_utc  
reviewed\_at\_utc

---

## **19.9 LifecycleMetricDTO**

Fields:

metric\_id  
metric\_name  
metric\_value  
stage\_name  
path\_type  
timestamp\_utc  
trace\_id  
labels

---

# **20\. Source-Specific Input DTO**

Source-specific raw inputs may differ from one another.

However, internally they must be converted into CanonicalEventEnvelopeDTO or TimeSeriesBundleInputDTO.

## **20.1 IndustrialRawInputDTO**

Fields:

device\_id  
tag  
register\_address  
value  
unit  
protocol  
timestamp\_utc  
raw\_payload

---

## **20.2 IndustrialTimeSeriesInputDTO**

Fields:

device\_id  
tag  
unit  
protocol  
samples  
sampling\_rate\_hz  
window\_start\_utc  
window\_end\_utc  
quality\_summary  
raw\_ref

---

## **20.3 RobotTelemetryInputDTO**

Fields:

robot\_id  
mission\_id  
mission\_status  
battery\_level  
pose  
velocity  
fault\_code  
timestamp\_utc

---

## **20.4 RobotTelemetryBundleInputDTO**

Fields:

robot\_id  
mission\_id  
telemetry\_type  
samples  
window\_start\_utc  
window\_end\_utc  
sampling\_rate\_hz  
quality\_summary

---

## **20.5 ConstructionProcessInputDTO**

Fields:

task\_id  
work\_package\_id  
zone\_id  
status  
permit\_id  
worker\_group\_id  
updated\_by  
timestamp\_utc

---

## **20.6 LLMOutputInputDTO**

Fields:

model\_id  
prompt\_id  
output\_type  
structured\_output  
retrieved\_doc\_refs  
confidence  
created\_at\_utc

Examples of output\_type:

Intent  
ActionCandidate  
EvidenceSummary  
MappingProposal  
Explanation

---

## **20.7 MobileContextInputDTO**

Fields:

user\_id  
device\_id  
location  
qr\_scan\_result  
ble\_proximity  
biometric\_status  
photo\_ref  
manual\_confirmation  
timestamp\_utc

---

## **20.8 DocumentParseInputDTO**

Fields:

document\_id  
document\_type  
parsed\_sections  
metadata  
version  
source\_uri  
parsed\_at\_utc

---

# **21\. Recommended File Structure**

schemas/  
init.py  
base.py  
context.py  
validation.py  
refs.py  
payloads.py  
input.py  
high\_frequency.py  
event.py  
ontology.py  
evidence.py  
world\_state.py  
intent.py  
action.py  
decision.py  
approval.py  
execution.py  
feedback.py  
audit.py  
registry.py  
governance.py  
observability.py  
source\_inputs.py

---

# **22\. Recommended Implementation Order**

The MVP implementation order should be as follows:

base.py  
context.py  
validation.py  
refs.py  
payloads.py  
event.py  
ontology.py  
evidence.py  
world\_state.py  
action.py  
decision.py  
approval.py  
execution.py  
feedback.py  
audit.py  
registry.py  
high\_frequency.py  
source\_inputs.py

---

# **23\. Required DTOs for MVP**

The following DTOs are required in the initial MVP:

BaseDTO  
TraceContextDTO  
VersionContextDTO  
SourceMetadataDTO  
ValidationResultDTO  
SanitizedInputDTO  
EntityRefDTO  
OntologyRefDTO  
EvidenceRefDTO  
CanonicalEventEnvelopeDTO  
PathClassificationDTO  
CanonicalIdentityDTO  
OntologyBindingDTO  
OntologyBoundEventDTO  
EvidenceDTO  
WorldStateDTO  
WorldStateUpdateDTO  
ActionCandidateDTO  
DecisionCaseDTO  
ApprovalRequestDTO  
ApprovedActionDTO  
ExecutionRequestDTO  
ExternalControlRequestDTO  
FeedbackEventDTO  
AuditRecordDTO

If the Emergency MVP is included, the following DTOs are additionally required:

EmergencyApprovedActionDTO  
EmergencyActionSpecDTO  
TimeoutPolicyDTO  
RecoveryPolicyDTO  
IdempotencyContextDTO  
PostHocAuditDTO

If the Monitoring MVP is included, the following DTOs are additionally required:

TimeSeriesSampleDTO  
TimeSeriesBundleInputDTO  
MonitoringPayloadDTO  
MonitoringOnlyEventDTO  
EscalationTriggerDTO  
LifecycleMetricDTO  
StateTypeSpecDTO  
EventTypeSpecDTO

Implementation can start from:

schemas/base.py  
schemas/context.py  
schemas/validation.py  
schemas/refs.py

---

# **24\. Final Principle**

Common Schema / DTO is the internal common language of the platform.

Sources may differ.  
Stacks may differ.  
Domain modules may differ.  
External systems may differ.  
Data frequency may differ.

However, inside the platform, every object must follow the common DTO contract.

The final standard flow is as follows:

RawInputDTO  
→ ValidationResultDTO  
→ SanitizedInputDTO  
→ CanonicalEventEnvelopeDTO  
→ OntologyBoundEventDTO  
→ EvidenceDTO  
→ WorldStateUpdateDTO  
→ ActionCandidateDTO  
→ DecisionCaseDTO  
→ ApprovalRequestDTO  
→ ApprovedActionDTO  
→ ExecutionRequestDTO  
→ ExternalControlRequestDTO  
→ FeedbackEventDTO  
→ AuditRecordDTO

High-frequency data may follow this path:

TimeSeriesSampleDTO  
→ TimeSeriesBundleInputDTO  
→ MonitoringOnlyEventDTO  
→ WorldStateUpdateDTO  
→ Metric / Trend Update  
→ EscalationTriggerDTO if needed

Emergency situations may follow this path:

CanonicalEventEnvelopeDTO  
→ EmergencyApprovedActionDTO  
→ ExecutionRequestDTO  
→ FeedbackEventDTO  
→ PostHocAuditDTO  
→ AuditRecordDTO

One-line summary:

Different sources, one schema contract.  
Different frequencies, one lifecycle discipline.  
Different domains, one semantic backbone.  
Different actions, one execution boundary.  
Different feedback, one audit trail.

# **1\. 목적**

본 문서는 온톨로지 중심 사이버-물리 플랫폼에서 사용되는 공통 Schema / DTO 목록을 정의한다.

DTO는 Data Transfer Object의 약자이며, 시스템 내부에서 데이터를 이동시키기 위한 표준 객체 형식이다.

본 문서는 “왜 이런 생명주기가 필요한가”를 길게 설명하지 않는다.  
그 내용은 별도의 Lifecycle 문서에서 다룬다.

본 문서의 역할은 다음에 집중한다.

1. 어떤 DTO가 필요한가  
2. 각 DTO는 어떤 필드를 가져야 하는가  
3. 어떤 DTO가 어떤 layer 사이에서 이동하는가  
4. 어떤 DTO에 trace, version, idempotency, validation 정보가 필요한가  
5. 고주기 데이터는 어떤 경량 DTO를 사용하는가  
6. 신뢰할 수 없는 외부 입력은 어떻게 검증되는가  
7. Pydantic 구현 시 어떤 DTO를 typed model로 만들고, 어떤 DTO는 flexible payload로 둘 것인가

---

# **2\. 문서 경계**

## **2.1 본 문서가 다루는 것**

본 문서는 다음을 다룬다.

DTO 목록  
DTO 필드  
DTO 간 참조 구조  
공통 context  
trace context  
version context  
source metadata  
reference DTO  
event DTO  
ontology binding DTO  
evidence DTO  
world state DTO  
action / decision / approval DTO  
execution / feedback / audit DTO  
registry / governance DTO  
high-frequency DTO  
validation DTO  
Pydantic 구현 전략

## **2.2 본 문서가 다루지 않는 것**

본 문서는 다음을 자세히 설명하지 않는다.

전체 lifecycle 철학  
왜 ApprovedAction만 실행 가능한가  
Emergency Fast-Path의 전체 운영 철학  
Monitoring-Only Path의 전체 목적  
Saga / Event Sourcing의 전체 실행 모델  
Safety Gate 내부 정책 판단 방식  
Ontology reasoning 방식  
OPA / OpenFGA 정책 엔진 설계

이 항목들은 별도 Lifecycle / Architecture / Governance 문서에서 다룬다.

---

# **3\. 핵심 원칙**

## **3.1 DTO는 실행하지 않는다**

DTO는 데이터 구조다.

DTO는 판단하지 않는다.  
DTO는 실행하지 않는다.  
DTO는 외부 시스템을 호출하지 않는다.  
DTO는 policy를 평가하지 않는다.  
DTO는 ontology reasoning을 직접 수행하지 않는다.

DTO의 역할은 다음이다.

데이터를 담는다.  
검증 가능한 형식을 제공한다.  
trace를 유지한다.  
version을 유지한다.  
다른 layer가 처리할 수 있도록 표준 구조를 제공한다.

---

## **3.2 Schema Layer는 가장 아래에 있어야 한다**

`schemas/`는 모든 layer가 import할 수 있다.

하지만 `schemas/`는 business layer를 import하면 안 된다.

허용되는 방향:

schemas  
→ common enum  
→ primitive type  
→ standard library  
→ pydantic

금지되는 방향:

schemas  
→ safety\_gate  
schemas  
→ agents  
schemas  
→ execution\_core  
schemas  
→ external\_adapters  
schemas  
→ ontology\_core runtime service

Schema는 플랫폼 전체의 공통 언어이므로 가장 안정적이고 독립적이어야 한다.

---

## **3.3 DTO는 계약이고, 처리는 service가 한다**

DTO는 구조를 정의한다.  
처리는 각 service가 한다.

예:

CanonicalEventEnvelopeDTO  
→ event\_normalizer.py가 생성한다.

OntologyBindingDTO  
→ semantic\_binder.py가 생성한다.

WorldStateUpdateDTO  
→ state\_store.py가 적용한다.

ActionCandidateDTO  
→ agent 또는 rule engine이 생성한다.

ApprovedActionDTO  
→ safety\_gate가 생성한다.

ExecutionRequestDTO  
→ execution\_core가 생성한다.

FeedbackEventDTO  
→ external adapter 또는 feedback handler가 생성한다.

AuditRecordDTO  
→ audit layer가 생성한다.

---

# **4\. Schema Versioning 정책**

DTO는 시간이 지나면서 변경될 수 있다.

따라서 모든 주요 DTO는 version context를 가져야 한다.

## **4.1 기본 버전 필드**

주요 DTO는 다음 필드를 포함해야 한다.

schema\_version  
lifecycle\_version  
ontology\_version  
policy\_bundle\_version  
mapping\_table\_version  
adapter\_version

모든 DTO가 모든 version 필드를 반드시 가져야 하는 것은 아니다.

하지만 다음 DTO는 version context가 강하게 권장된다.

CanonicalEventEnvelopeDTO  
OntologyBoundEventDTO  
EvidenceDTO  
WorldStateUpdateDTO  
ActionCandidateDTO  
DecisionCaseDTO  
ApprovedActionDTO  
ExecutionRequestDTO  
FeedbackEventDTO  
AuditRecordDTO

---

## **4.2 Backward-Compatible Change**

다음 변경은 일반적으로 backward-compatible change로 본다.

optional field 추가  
새로운 enum value 추가  
새로운 event type 추가  
새로운 optional metadata 추가  
새로운 monitoring metric 추가  
새로운 source-specific DTO 추가  
기존 필드를 유지한 상태에서 validator 강화

예:

v1.2 → v1.3

WorldStateUpdateDTO에 optional field 추가  
MonitoringOnlyEventDTO에 optional label 추가

---

## **4.3 Breaking Change**

다음 변경은 breaking change로 본다.

required field 삭제  
required field 이름 변경  
field type 변경  
enum value 의미 변경  
idempotency semantics 변경  
execution boundary semantics 변경  
ApprovedAction / ExecutionRequest 구조 변경  
audit trace 연결 방식 변경

예:

v1.x → v2.0

ExecutionRequestDTO.required\_feedback 필드를 expected\_feedback\_contract로 강제 변경  
ApprovedActionDTO의 target\_ref 구조 변경

---

## **4.4 Deprecation Policy**

필드를 바로 삭제하지 않는다.

권장 절차:

1. deprecated field 표시  
2. replacement field 추가  
3. dual-write 기간 운영  
4. downstream consumer migration  
5. audit compatibility 확인  
6. major version에서 제거

---

## **4.5 Schema Compatibility Rule**

구버전 event, audit, feedback, execution record는 재해석 가능해야 한다.

따라서 다음 원칙을 지킨다.

AuditRecordDTO는 생성 당시 schema\_version을 보존한다.  
ExecutionRequestDTO는 생성 당시 policy\_bundle\_version을 보존한다.  
WorldStateUpdateDTO는 생성 당시 ontology\_version을 보존한다.  
FeedbackEventDTO는 external adapter version을 보존한다.

---

# **5\. Untrusted Input Validation Layer**

외부에서 들어오는 입력은 기본적으로 신뢰하지 않는다.

RawInputDTO, MobileContextInputDTO, LLMOutputInputDTO, DocumentParseInputDTO, IndustrialRawInputDTO는 모두 untrusted input으로 취급한다.

## **5.1 Validation 단계**

입력은 다음 validation layer를 통과해야 한다.

Transport validation  
Schema validation  
Size limit validation  
Encoding validation  
Checksum validation  
Source authentication  
Source authorization  
Rate limiting  
Replay detection  
Timestamp sanity check  
Payload sanitization  
Prompt injection filtering  
Document provenance check  
Media integrity check

---

## **5.2 ValidationResultDTO**

입력 검증 결과를 표현한다.

필드:

validation\_id  
input\_ref  
validation\_status  
validation\_errors  
sanitized  
sanitization\_notes  
rate\_limited  
replay\_detected  
source\_authenticated  
source\_authorized  
validated\_at\_utc

validation\_status 예:

PASSED  
FAILED  
PARTIALLY\_PASSED  
QUARANTINED  
REJECTED

---

## **5.3 SanitizedInputDTO**

검증과 sanitization을 거친 입력이다.

필드:

sanitized\_input\_id  
raw\_input\_ref  
sanitized\_payload  
removed\_fields  
normalization\_notes  
validation\_result\_ref  
trace\_context  
created\_at\_utc

용도:

RawInputDTO를 바로 CanonicalEventEnvelopeDTO로 보내지 않고, 필요 시 SanitizedInputDTO를 거친다.

---

## **5.4 RateLimitContextDTO**

source별 입력 제한을 표현한다.

필드:

source\_id  
limit\_key  
allowed\_rate  
observed\_rate  
window\_start\_utc  
window\_end\_utc  
rate\_limited  
action\_taken

용도:

고주기 데이터, 외부 API 입력, 모바일 입력, LLM tool output 등에 적용한다.

---

## **5.5 Rule**

Untrusted input은 바로 semantic pipeline으로 들어가지 않는다.

RawInputDTO  
→ ValidationResultDTO  
→ SanitizedInputDTO  
→ CanonicalEventEnvelopeDTO

또는 고주기 데이터의 경우:

RawInputDTO  
→ ValidationResultDTO  
→ TimeSeriesBundleInputDTO  
→ MonitoringOnlyEventDTO

---

# **6\. TraceContext 표준 매핑 룰**

TraceContextDTO는 개발 단계에서 혼동되기 쉬우므로 명확한 의미를 가져야 한다.

## **6.1 trace\_id**

하나의 전체 lifecycle을 묶는 최상위 추적 ID다.

예:

하나의 gas sensor alarm에서 시작하여 ActionCandidate, ApprovedAction, ExecutionRequest, FeedbackEvent, AuditRecord까지 이어지는 전체 흐름은 같은 trace\_id를 가진다.

---

## **6.2 correlation\_id**

직접적인 원인 관계는 아니지만 같은 사건군 또는 같은 operation에 속하는 객체들을 연결한다.

예:

GasSensorReadingEvent와 WorkerLocationChangedEvent는 직접 원인 관계는 아닐 수 있다.

하지만 같은 위험 판단에 사용되므로 같은 correlation\_id를 가질 수 있다.

---

## **6.3 causation\_id**

직접적인 원인 객체의 ID다.

표준 룰:

A 이벤트로 인해 B 후보가 생성되었다면, B의 causation\_id는 A의 event\_id이다.

예:

GasSensorReadingEvent\_001  
→ ActionCandidate\_001 생성

ActionCandidate\_001.causation\_id \= GasSensorReadingEvent\_001.event\_id

ActionCandidate\_001  
→ DecisionCase\_001 생성

DecisionCase\_001.causation\_id \= ActionCandidate\_001.candidate\_id

ApprovedAction\_001  
→ ExecutionRequest\_001 생성

ExecutionRequest\_001.causation\_id \= ApprovedAction\_001.approved\_action\_id

---

## **6.4 span\_id / parent\_span\_id**

분산 tracing에서 stage-level 처리를 추적한다.

예:

ingestion span  
validation span  
canonicalization span  
ontology binding span  
safety gate span  
execution dispatch span

---

## **6.5 request\_id**

외부 API 호출 또는 사용자 요청 단위의 ID다.

---

# **7\. Pydantic Payload 전략**

## **7.1 현실적 원칙**

모든 DTO에 Generic을 적용하지 않는다.

Generic은 강력하지만, 모든 곳에 적용하면 개발 생산성을 떨어뜨릴 수 있다.

따라서 path별로 다르게 적용한다.

---

## **7.2 MVP 전략**

MVP에서는 다음을 우선한다.

payload: dict  
metadata: dict  
GenericPayloadDTO 사용  
핵심 DTO 구조만 엄격히 검증  
Action / Execution / Emergency DTO는 강하게 검증

MVP에서 Typed Generic은 선택사항이다.

---

## **7.3 Production 전략**

Production에서는 high-risk path 중심으로 typed payload를 적용한다.

Typed Generic 우선 적용 대상:

EmergencyApprovedActionDTO  
ExecutionRequestDTO  
ExternalControlRequestDTO  
FeedbackEventDTO  
EvidenceDTO  
ApprovedActionDTO  
CanonicalEventEnvelopeDTO for safety-critical events

Typed Generic을 늦게 적용해도 되는 대상:

MonitoringOnlyEventDTO  
TimeSeriesSampleDTO  
low-risk telemetry  
experimental source adapter  
UnclassifiedEntityDTO  
LLM draft output

---

## **7.4 Monitoring Path 전략**

Monitoring path는 가능한 한 경량 유지한다.

권장:

bundle-level trace\_context  
bundle-level source\_metadata  
sample-level timestamp  
sample-level sequence\_number  
sample-level value  
sample-level quality

비권장:

sample마다 full TraceContextDTO  
sample마다 VersionContextDTO  
sample마다 OntologyBindingDTO  
sample마다 EvidenceDTO

---

## **7.5 Generic 사용 예**

개념적 구조:

CanonicalEventEnvelopeDTO\[T\]  
RawInputDTO\[T\]  
EvidenceDTO\[T\]  
FeedbackEventDTO\[T\]

예:

CanonicalEventEnvelopeDTO\[GasSensorPayloadDTO\]  
CanonicalEventEnvelopeDTO\[RobotMissionPayloadDTO\]  
EvidenceDTO\[InspectionEvidencePayloadDTO\]  
FeedbackEventDTO\[SmartHelmetAckPayloadDTO\]

---

# **8\. 전체 DTO 그룹**

공통 DTO는 크게 11개 그룹으로 나눈다.

1. Base / Context DTO  
2. Validation DTO  
3. Reference DTO  
4. Input / Event DTO  
5. High-Frequency / Monitoring DTO  
6. Ontology Binding DTO  
7. Evidence / World State DTO  
8. Candidate / Decision / Approval DTO  
9. Approved Action / Execution DTO  
10. Feedback / Audit DTO  
11. Registry / Governance / Observability DTO

---

# **9\. Base / Context DTO**

## **9.1 BaseDTO**

필드:

id  
created\_at\_utc  
updated\_at\_utc  
schema\_version  
lifecycle\_version  
metadata

---

## **9.2 TraceContextDTO**

필드:

trace\_id  
correlation\_id  
causation\_id  
parent\_span\_id  
span\_id  
request\_id

---

## **9.3 VersionContextDTO**

필드:

schema\_version  
lifecycle\_version  
ontology\_version  
policy\_bundle\_version  
mapping\_table\_version  
adapter\_version

---

## **9.4 SourceMetadataDTO**

필드:

source\_type  
source\_id  
source\_name  
source\_protocol  
source\_system  
source\_trust\_level  
ingested\_at\_utc  
raw\_ref

---

## **9.5 FreshnessDTO**

필드:

timestamp\_utc  
ingested\_at\_utc  
freshness\_ms  
valid\_until  
is\_stale

---

## **9.6 ConfidenceDTO**

필드:

confidence\_score  
confidence\_level  
confidence\_reason  
source\_quality  
validation\_status

---

## **9.7 GenericPayloadDTO**

필드:

payload\_type  
payload\_schema\_version  
payload  
payload\_hash  
validation\_status

---

# **10\. Validation DTO**

## **10.1 ValidationResultDTO**

필드:

validation\_id  
input\_ref  
validation\_status  
validation\_errors  
sanitized  
sanitization\_notes  
rate\_limited  
replay\_detected  
source\_authenticated  
source\_authorized  
validated\_at\_utc

---

## **10.2 SanitizedInputDTO**

필드:

sanitized\_input\_id  
raw\_input\_ref  
sanitized\_payload  
removed\_fields  
normalization\_notes  
validation\_result\_ref  
trace\_context  
created\_at\_utc

---

## **10.3 RateLimitContextDTO**

필드:

source\_id  
limit\_key  
allowed\_rate  
observed\_rate  
window\_start\_utc  
window\_end\_utc  
rate\_limited  
action\_taken

---

# **11\. Reference DTO**

## **11.1 EntityRefDTO**

필드:

entity\_id  
entity\_type  
canonical\_id  
display\_name  
ontology\_iri  
runtime\_key

---

## **11.2 LocationRefDTO**

필드:

location\_id  
location\_type  
site\_id  
zone\_id  
floor\_id  
coordinates  
ontology\_iri

---

## **11.3 OntologyRefDTO**

필드:

ontology\_iri  
ontology\_class  
ontology\_property  
domain\_module  
runtime\_key  
label

---

## **11.4 EvidenceRefDTO**

필드:

evidence\_id  
evidence\_type  
source\_id  
timestamp\_utc  
confidence\_score  
summary

---

## **11.5 PolicyRefDTO**

필드:

policy\_id  
policy\_type  
policy\_version  
policy\_bundle\_version  
decision\_result

---

## **11.6 ActorRefDTO**

필드:

actor\_id  
actor\_type  
role  
organization  
clearance\_level  
ontology\_iri

---

# **12\. Input / Event DTO**

## **12.1 RawInputDTO**

필드:

raw\_input\_id  
source\_metadata  
raw\_payload  
received\_at\_utc  
raw\_format  
encoding  
checksum  
trace\_context

---

## **12.2 CanonicalEventEnvelopeDTO**

필드:

event\_id  
event\_type  
source\_metadata  
subject\_ref  
location\_ref  
timestamp\_utc  
payload  
confidence  
freshness  
trace\_context  
version\_context  
emergency\_hint  
criticality\_hint  
lifecycle\_path\_hint

---

## **12.3 PathClassificationDTO**

필드:

path\_type  
classification\_reason  
risk\_hint  
emergency\_detected  
monitoring\_only\_allowed  
standard\_path\_required  
classified\_at\_utc

path\_type 예:

STANDARD  
EMERGENCY\_FAST\_PATH  
MONITORING\_ONLY

---

## **12.4 EventTypeDTO**

필드:

event\_type  
event\_category  
domain\_module  
allowed\_subject\_types  
default\_lifecycle\_path  
requires\_evidence  
can\_generate\_candidate

---

# **13\. High-Frequency / Monitoring DTO**

## **13.1 TimeSeriesSampleDTO**

필드:

timestamp\_utc  
value  
unit  
quality  
sequence\_number  
sample\_status

중요:

개별 sample에는 full trace\_context를 넣지 않는다.

---

## **13.2 TimeSeriesBundleInputDTO**

필드:

bundle\_id  
source\_metadata  
subject\_ref  
signal\_name  
unit  
samples  
window\_start\_utc  
window\_end\_utc  
sample\_count  
sampling\_rate\_hz  
trace\_context  
version\_context

중요:

trace\_context는 bundle 단위로 유지한다.  
sample 단위 trace는 기본적으로 금지한다.

---

## **13.3 WindowedInputDTO**

필드:

window\_id  
source\_metadata  
window\_start\_utc  
window\_end\_utc  
events  
aggregation\_type  
statistics  
trace\_context

aggregation\_type 예:

RAW\_SAMPLES  
AVERAGE  
MIN\_MAX  
COUNT  
LAST\_VALUE  
THRESHOLD\_CROSSING

---

## **13.4 MonitoringPayloadDTO**

필드:

metric\_name  
metric\_value  
unit  
timestamp\_utc  
quality  
is\_threshold\_crossed  
threshold\_ref  
summary\_status

---

## **13.5 MonitoringOnlyEventDTO**

필드:

monitoring\_event\_id  
source\_metadata  
subject\_ref  
monitoring\_payload  
freshness  
trace\_context  
optional\_ontology\_ref  
path\_type

주의:

MonitoringOnlyEventDTO는 ActionCandidate를 직접 만들지 않는다.

---

## **13.6 EscalationTriggerDTO**

필드:

trigger\_id  
source\_event\_ref  
trigger\_reason  
from\_path  
to\_path  
threshold\_ref  
detected\_at\_utc  
trace\_context

---

# **14\. Ontology Binding DTO**

## **14.1 CanonicalIdentityDTO**

필드:

raw\_identifier  
canonical\_id  
canonical\_iri  
runtime\_key  
alias\_matched  
mapping\_confidence  
mapping\_table\_version

---

## **14.2 OntologyBindingDTO**

필드:

binding\_id  
entity\_ref  
ontology\_class  
ontology\_property  
ontology\_individual  
domain\_module  
runtime\_key  
binding\_confidence  
binding\_status  
binding\_errors

binding\_status 예:

BOUND  
PARTIALLY\_BOUND  
BINDING\_FAILED  
UNCLASSIFIED

---

## **14.3 OntologyBoundEventDTO**

필드:

event\_id  
canonical\_event  
ontology\_bindings  
subject\_ref  
state\_type  
event\_semantics  
evidence\_candidate  
trace\_context

---

## **14.4 UnclassifiedEntityDTO**

필드:

unclassified\_id  
raw\_identifier  
source\_metadata  
observed\_payload  
possible\_entity\_types  
reason  
risk\_blocked  
mapping\_review\_required  
created\_at\_utc

---

## **14.5 MappingProposalDTO**

필드:

proposal\_id  
unclassified\_entity\_id  
proposed\_canonical\_id  
proposed\_ontology\_class  
proposed\_domain\_module  
reasoning\_summary  
supporting\_evidence\_refs  
confidence\_score  
requires\_human\_approval

---

# **15\. Evidence / World State DTO**

## **15.1 EvidenceDTO**

필드:

evidence\_id  
evidence\_type  
source\_metadata  
subject\_ref  
location\_ref  
payload  
timestamp\_utc  
confidence  
freshness  
trace\_context  
provenance  
validation\_status

---

## **15.2 EvidenceBundleDTO**

필드:

bundle\_id  
evidence\_refs  
bundle\_purpose  
summary  
minimum\_required\_evidence\_met  
conflicting\_evidence\_detected  
created\_at\_utc

---

## **15.3 WorldStateDTO**

필드:

state\_id  
entity\_ref  
state\_type  
state\_value  
source\_ref  
evidence\_ref  
timestamp\_utc  
freshness  
confidence  
valid\_until  
trace\_context  
version

---

## **15.4 WorldStateUpdateDTO**

필드:

update\_id  
entity\_ref  
previous\_state  
new\_state  
change\_reason  
evidence\_refs  
updated\_by  
updated\_at\_utc  
trace\_context  
idempotency\_key  
state\_version  
expected\_previous\_version  
deduplication\_window\_ms

---

## **15.5 StateSnapshotDTO**

필드:

snapshot\_id  
site\_id  
snapshot\_time\_utc  
states  
ontology\_version  
policy\_context\_version  
created\_at\_utc

---

# **16\. Candidate / Decision / Approval DTO**

## **16.1 IntentDTO**

필드:

intent\_id  
intent\_type  
requested\_by  
target\_ref  
reason  
source\_event\_ref  
confidence  
trace\_context

---

## **16.2 ActionCandidateDTO**

필드:

candidate\_id  
action\_type  
target\_ref  
target\_location  
proposed\_by  
reason  
risk\_level  
evidence\_refs  
confidence  
constraints  
required\_capabilities  
requires\_approval  
created\_at\_utc  
trace\_context

---

## **16.3 DecisionCaseDTO**

필드:

decision\_case\_id  
candidate\_ref  
decision\_tier  
risk\_level  
urgency  
routing\_result  
required\_approval  
policy\_precheck\_result  
evidence\_summary  
state\_freshness\_result  
recommended\_next\_step  
trace\_context

---

## **16.4 ApprovalRequestDTO**

필드:

approval\_request\_id  
decision\_case\_ref  
action\_type  
target\_ref  
required\_role  
required\_clearance  
approver\_ref  
approval\_status  
approval\_reason  
expires\_at\_utc  
created\_at\_utc  
approved\_at\_utc  
trace\_context

---

## **16.5 ApprovalDecisionDTO**

필드:

approval\_decision\_id  
approval\_request\_ref  
decision  
decided\_by  
decision\_reason  
decision\_time\_utc  
policy\_refs  
trace\_context

---

# **17\. Approved Action / Execution DTO**

## **17.1 ApprovedActionDTO**

필드:

approved\_action\_id  
candidate\_ref  
decision\_case\_ref  
action\_type  
target\_ref  
constraints  
approval\_context  
policy\_result  
evidence\_refs  
risk\_level  
valid\_until  
idempotency\_key  
trace\_context  
created\_at\_utc

---

## **17.2 EmergencyApprovedActionDTO**

필드:

emergency\_approved\_action\_id  
emergency\_policy\_id  
emergency\_condition\_id  
action\_type  
target\_ref  
minimal\_evidence\_refs  
local\_rule\_result  
idempotency\_key  
timeout\_policy  
expected\_feedback  
post\_hoc\_audit\_required  
is\_emergency\_bypass  
post\_audit\_status  
trace\_context  
created\_at\_utc

post\_audit\_status 예:

PENDING  
REVIEWED  
APPROVED  
REJECTED  
ESCALATED

---

## **17.3 ExecutionRequestDTO**

필드:

execution\_request\_id  
approved\_action\_ref  
action\_type  
target\_ref  
external\_system\_type  
external\_system\_id  
execution\_constraints  
expected\_feedback  
timeout\_policy  
retry\_policy  
recovery\_policy  
idempotency\_key  
execution\_lease  
trace\_context  
created\_at\_utc

---

## **17.4 ExternalControlRequestDTO**

필드:

external\_request\_id  
execution\_request\_ref  
adapter\_id  
external\_system\_type  
protocol  
endpoint  
payload  
idempotency\_key  
timeout\_policy  
expected\_feedback  
trace\_context  
sent\_at\_utc

---

## **17.5 TimeoutPolicyDTO**

필드:

timeout\_ms  
on\_timeout\_action  
max\_wait\_ms  
requires\_recovery  
notify\_actor\_refs

---

## **17.6 RetryPolicyDTO**

필드:

max\_retries  
retry\_interval\_ms  
backoff\_strategy  
retryable\_errors  
non\_retryable\_errors

---

## **17.7 RecoveryPolicyDTO**

필드:

recovery\_policy\_id  
recovery\_type  
safe\_state\_target  
compensating\_action\_type  
manual\_override\_required  
notify\_actor\_refs

---

## **17.8 IdempotencyContextDTO**

필드:

idempotency\_key  
deduplication\_window\_ms  
original\_request\_id  
duplicate\_detected  
dedupe\_strategy

사용 대상:

WorldStateUpdateDTO  
ApprovedActionDTO  
EmergencyApprovedActionDTO  
ExecutionRequestDTO  
ExternalControlRequestDTO

---

# **18\. Feedback / Audit DTO**

## **18.1 FeedbackEventDTO**

필드:

feedback\_event\_id  
execution\_request\_ref  
external\_request\_ref  
source\_system  
feedback\_type  
status  
payload  
timestamp\_utc  
confidence  
trace\_context  
correlation\_id  
error\_code  
recovery\_required  
is\_emergency\_bypass  
post\_audit\_required

---

## **18.2 WorldStateReconciliationDTO**

필드:

reconciliation\_id  
feedback\_event\_ref  
affected\_state\_refs  
previous\_states  
reconciled\_states  
conflict\_detected  
reconciliation\_result  
created\_at\_utc  
trace\_context

---

## **18.3 ExecutionStateDTO**

필드:

execution\_state\_id  
execution\_request\_ref  
state  
last\_feedback\_ref  
updated\_at\_utc  
timeout\_at\_utc  
recovery\_required  
trace\_context

state 예:

CREATED  
DISPATCH\_PENDING  
DISPATCHED  
ACKNOWLEDGED  
ACCEPTED  
STARTED  
IN\_PROGRESS  
COMPLETED  
FAILED  
TIMEOUT  
FEEDBACK\_MISSING  
RECOVERY\_REQUIRED  
CLOSED

---

## **18.4 PostHocAuditDTO**

필드:

post\_hoc\_audit\_id  
emergency\_approved\_action\_ref  
execution\_request\_ref  
feedback\_event\_refs  
review\_status  
reviewer\_ref  
review\_comment  
reviewed\_at\_utc  
required\_followup\_actions  
trace\_context

review\_status 예:

PENDING  
REVIEWED  
APPROVED  
REJECTED  
ESCALATED  
REQUIRES\_POLICY\_UPDATE  
REQUIRES\_ONTOLOGY\_UPDATE

---

## **18.5 AuditRecordDTO**

필드:

audit\_record\_id  
trace\_id  
lifecycle\_path  
event\_refs  
evidence\_refs  
candidate\_ref  
decision\_case\_ref  
approval\_request\_ref  
approved\_action\_ref  
execution\_request\_ref  
external\_request\_ref  
feedback\_event\_ref  
policy\_refs  
actor\_refs  
final\_status  
created\_at\_utc  
is\_emergency\_bypass  
post\_audit\_status  
post\_hoc\_audit\_ref

---

# **19\. Registry / Governance / Observability DTO**

## **19.1 ActionTypeSpecDTO**

필드:

action\_type  
description  
allowed\_target\_types  
required\_evidence\_types  
required\_roles  
default\_risk\_level  
requires\_approval  
allowed\_external\_systems  
expected\_feedback\_types

---

## **19.2 EmergencyActionSpecDTO**

필드:

emergency\_action\_type  
emergency\_condition\_type  
allowed\_target\_types  
required\_minimal\_evidence  
local\_rule\_id  
policy\_id  
allowed\_external\_systems  
required\_feedback  
timeout\_policy  
recovery\_policy  
audit\_level  
approval\_model  
post\_hoc\_audit\_required  
version  
owner  
valid\_from  
valid\_until

---

## **19.3 EventTypeSpecDTO**

필드:

event\_type  
domain\_module  
allowed\_sources  
allowed\_subject\_types  
default\_lifecycle\_path  
can\_generate\_evidence  
can\_generate\_candidate  
monitoring\_only\_allowed  
emergency\_trigger\_allowed  
supports\_batching  
supports\_windowing

---

## **19.4 StateTypeSpecDTO**

필드:

state\_type  
entity\_type  
value\_type  
allowed\_values  
freshness\_requirement\_ms  
confidence\_requirement  
is\_safety\_critical  
requires\_idempotent\_update

---

## **19.5 CapabilitySpecDTO**

필드:

capability\_id  
capability\_type  
owner\_entity\_type  
constraints  
required\_conditions  
risk\_level  
ontology\_iri

---

## **19.6 AdapterSpecDTO**

필드:

adapter\_id  
adapter\_type  
external\_system\_type  
supported\_action\_types  
protocol  
endpoint\_ref  
timeout\_policy  
retry\_policy  
health\_status

---

## **19.7 PolicyDecisionDTO**

필드:

policy\_decision\_id  
policy\_refs  
input\_context  
decision\_result  
reason  
obligations  
denial\_reasons  
evaluated\_at\_utc

decision\_result 예:

ALLOW  
DENY  
REQUIRE\_APPROVAL  
ESCALATE  
EMERGENCY\_ALLOW

---

## **19.8 MappingReviewDTO**

필드:

mapping\_review\_id  
mapping\_proposal\_ref  
reviewer\_ref  
review\_status  
review\_comment  
approved\_mapping  
created\_at\_utc  
reviewed\_at\_utc

---

## **19.9 LifecycleMetricDTO**

필드:

metric\_id  
metric\_name  
metric\_value  
stage\_name  
path\_type  
timestamp\_utc  
trace\_id  
labels

---

# **20\. Source-Specific Input DTO**

출처별 raw input은 서로 다를 수 있다.

하지만 내부에서는 CanonicalEventEnvelopeDTO 또는 TimeSeriesBundleInputDTO로 변환되어야 한다.

## **20.1 IndustrialRawInputDTO**

필드:

device\_id  
tag  
register\_address  
value  
unit  
protocol  
timestamp\_utc  
raw\_payload

---

## **20.2 IndustrialTimeSeriesInputDTO**

필드:

device\_id  
tag  
unit  
protocol  
samples  
sampling\_rate\_hz  
window\_start\_utc  
window\_end\_utc  
quality\_summary  
raw\_ref

---

## **20.3 RobotTelemetryInputDTO**

필드:

robot\_id  
mission\_id  
mission\_status  
battery\_level  
pose  
velocity  
fault\_code  
timestamp\_utc

---

## **20.4 RobotTelemetryBundleInputDTO**

필드:

robot\_id  
mission\_id  
telemetry\_type  
samples  
window\_start\_utc  
window\_end\_utc  
sampling\_rate\_hz  
quality\_summary

---

## **20.5 ConstructionProcessInputDTO**

필드:

task\_id  
work\_package\_id  
zone\_id  
status  
permit\_id  
worker\_group\_id  
updated\_by  
timestamp\_utc

---

## **20.6 LLMOutputInputDTO**

필드:

model\_id  
prompt\_id  
output\_type  
structured\_output  
retrieved\_doc\_refs  
confidence  
created\_at\_utc

output\_type 예:

Intent  
ActionCandidate  
EvidenceSummary  
MappingProposal  
Explanation

---

## **20.7 MobileContextInputDTO**

필드:

user\_id  
device\_id  
location  
qr\_scan\_result  
ble\_proximity  
biometric\_status  
photo\_ref  
manual\_confirmation  
timestamp\_utc

---

## **20.8 DocumentParseInputDTO**

필드:

document\_id  
document\_type  
parsed\_sections  
metadata  
version  
source\_uri  
parsed\_at\_utc

---

# **21\. 권장 파일 구조**

schemas/  
**init**.py  
base.py  
context.py  
validation.py  
refs.py  
payloads.py  
input.py  
high\_frequency.py  
event.py  
ontology.py  
evidence.py  
world\_state.py  
intent.py  
action.py  
decision.py  
approval.py  
execution.py  
feedback.py  
audit.py  
registry.py  
governance.py  
observability.py  
source\_inputs.py

---

# **22\. 우선 작성 순서**

MVP 작성 순서는 다음이 좋다.

1. base.py  
2. context.py  
3. validation.py  
4. refs.py  
5. payloads.py  
6. event.py  
7. ontology.py  
8. evidence.py  
9. world\_state.py  
10. action.py  
11. decision.py  
12. approval.py  
13. execution.py  
14. feedback.py  
15. audit.py  
16. registry.py  
17. high\_frequency.py  
18. source\_inputs.py

---

# **23\. MVP 필수 DTO**

초기 MVP에서 반드시 필요한 DTO는 다음이다.

BaseDTO  
TraceContextDTO  
VersionContextDTO  
SourceMetadataDTO  
ValidationResultDTO  
SanitizedInputDTO  
EntityRefDTO  
OntologyRefDTO  
EvidenceRefDTO  
CanonicalEventEnvelopeDTO  
PathClassificationDTO  
CanonicalIdentityDTO  
OntologyBindingDTO  
OntologyBoundEventDTO  
EvidenceDTO  
WorldStateDTO  
WorldStateUpdateDTO  
ActionCandidateDTO  
DecisionCaseDTO  
ApprovalRequestDTO  
ApprovedActionDTO  
ExecutionRequestDTO  
ExternalControlRequestDTO  
FeedbackEventDTO  
AuditRecordDTO

Emergency MVP까지 포함한다면 추가로 필요하다.

EmergencyApprovedActionDTO  
EmergencyActionSpecDTO  
TimeoutPolicyDTO  
RecoveryPolicyDTO  
IdempotencyContextDTO  
PostHocAuditDTO

Monitoring MVP까지 포함한다면 추가로 필요하다.

TimeSeriesSampleDTO  
TimeSeriesBundleInputDTO  
MonitoringPayloadDTO  
MonitoringOnlyEventDTO  
EscalationTriggerDTO  
LifecycleMetricDTO  
StateTypeSpecDTO  
EventTypeSpecDTO

`schemas/base.py`, `schemas/context.py`, `schemas/validation.py`, `schemas/refs.py`부터 구현 가능하다.

---

# **24\. 최종 원칙**

Common Schema / DTO는 플랫폼의 내부 공통 언어다.

출처는 다를 수 있다.  
stack은 다를 수 있다.  
도메인 모듈은 다를 수 있다.  
외부 시스템은 다를 수 있다.  
데이터 빈도는 다를 수 있다.

하지만 플랫폼 내부에서는 모든 객체가 공통 DTO 계약을 따라야 한다.

최종 표준 흐름은 다음과 같다.

RawInputDTO  
→ ValidationResultDTO  
→ SanitizedInputDTO  
→ CanonicalEventEnvelopeDTO  
→ OntologyBoundEventDTO  
→ EvidenceDTO  
→ WorldStateUpdateDTO  
→ ActionCandidateDTO  
→ DecisionCaseDTO  
→ ApprovalRequestDTO  
→ ApprovedActionDTO  
→ ExecutionRequestDTO  
→ ExternalControlRequestDTO  
→ FeedbackEventDTO  
→ AuditRecordDTO

고주기 데이터는 다음 경로를 가질 수 있다.

TimeSeriesSampleDTO  
→ TimeSeriesBundleInputDTO  
→ MonitoringOnlyEventDTO  
→ WorldStateUpdateDTO  
→ Metric / Trend Update  
→ EscalationTriggerDTO if needed

비상 상황은 다음 경로를 가질 수 있다.

CanonicalEventEnvelopeDTO  
→ EmergencyApprovedActionDTO  
→ ExecutionRequestDTO  
→ FeedbackEventDTO  
→ PostHocAuditDTO  
→ AuditRecordDTO

한 줄로 정리하면 다음과 같다.

Different sources, one schema contract.  
Different frequencies, one lifecycle discipline.  
Different domains, one semantic backbone.  
Different actions, one execution boundary.  
Different feedback, one audit trail.

