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

Enum (`ValidationStatus`, `schemas/enums.py`):

PASSED  
FAILED  
PARTIALLY\_PASSED  
QUARANTINED  
REJECTED

Also used by `ConfidenceDTO.validation_status`, `EvidenceDTO.validation_status`, and `GenericPayloadDTO.validation_status` — all four fields share this one enum.

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

If event A causes candidate B to be created, then B's causation\_id is A's event\_id.

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

## **7.2 Initial Implementation Strategy**

In the initial implementation, prioritize the following:

payload: dict  
metadata: dict  
Use GenericPayloadDTO  
Strictly validate only core DTO structures  
Strongly validate Action / Execution / Emergency DTOs

Typed Generics are optional in the initial implementation.

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

## **8.1 Shared Enum Types**

Fields with a closed value set use a shared enum class from `src/ledo_ontology_core/framework/schemas/enums.py`, not a plain string. Each field's definition below states which enum it uses. The enum module is the single source of truth for member names; sections in this document state the canonical enum for each field but do not redefine membership independently.

Enums defined there: `ValidationStatus`, `PathType`, `BindingStatus`, `PolicyDecisionResult`, `RiskLevel`, `ApprovalAuthority`, `DecisionTier`, `PostAuditStatus`, `ReviewStatus`, `AggregationType`, `DispatchStatus`.

Three exceptions are sourced from a different document than this one, not from this document's own field-level "Examples of X" lists:

- `DispatchStatus` is sourced from `09_execution_adapter_model.md` Section 20 — see Section 18.3 below.
- `PolicyDecisionResult` is sourced from `08_policy_governance_model.md` Section 7 ("Policy Decision Result"), not from this document's Section 19.7, which lists an illustrative and now-superseded 5-member subset.
- `RiskLevel` is sourced from `07_decision_approval_matrix.md` Section 9.1 ("Risk Level"), cross-confirmed by usage in `08_policy_governance_model.md`. `ApprovalAuthority` is sourced from `08_policy_governance_model.md` Section 13 ("Approval Authority Model"), independently cross-confirmed by `09_appendices/appendix_f_decision_approval_catalog/decision_approval_catalog.md`.

In all three cases, do not add members from this document's own shorter illustrative lists, or from a registry document's illustrative Pydantic model (e.g. `06_registry_specs/approval_registry/approval_registry.md` Section 8's non-matching 10-member set), without updating the actual canonical source document first.

---

## **8.2 Fields That Intentionally Stay `str`**

Not every categorical-looking field is an enum. Two different reasons keep a field as plain `str` instead of a `schemas/enums.py` member, and they are not the same thing — conflating them is what made this ambiguous before, so this section makes the distinction explicit.

**Registry-managed vocabulary.** `action_type`, `event_type`, `entity_type`, `state_type`, and `evidence_type` are governed by their own registries (`06_registry_specs/action_registry`, `event_registry`, `state_registry`, `evidence_registry`, and ontology/domain-module entity typing respectively), loaded at runtime with `draft`/`active`/`deprecated` lifecycle status per `06_registry_specs/README.md`. New domain packs add new values by adding registry entries, not by editing a Python enum and redeploying. Hardcoding these into `enums.py` would defeat the extensibility the registry layer (Steps 5/7/8/9/11) exists to provide. This is a deliberate architecture choice, not an oversight.

**Genuinely undecided fields.** `urgency`, `confidence_level`, and `source_type` have no closed value list anywhere in this document or its supporting specs — unlike `validation_status`, `path_type`, etc., there is no "Examples of X" list to draw an enum from. Per Section 4 of `07_implementation_plan/pre_code_generation_build_plan.md` ("모호함 처리 표준"), enum membership is not invented without a source. These fields are marked `# DOMAIN_DECISION_REQUIRED` at their declaration sites in `schemas/`. A future step that pins down the actual value set should convert these to enums and remove the marker at that point — not before.

`risk_level` was previously listed here as genuinely undecided. That was incorrect: a full read of `03_core_specifications/07_decision_approval_matrix.md` and `08_policy_governance_model.md` found a closed 6-member value set (see Section 9.1 above). `risk_level` is now `RiskLevel` at every declaration site in `schemas/` and is no longer `DOMAIN_DECISION_REQUIRED`.

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

Enum (`PathType`, `schemas/enums.py`):

STANDARD  
EMERGENCY\_FAST\_PATH  
MONITORING\_ONLY

Also used by `MonitoringOnlyEventDTO.path_type`, `EscalationTriggerDTO.from_path`/`to_path`, and `LifecycleMetricDTO.path_type`.

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

Enum (`AggregationType`, `schemas/enums.py`):

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

Enum (`BindingStatus`, `schemas/enums.py`):

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

Canonical Reference: `05_evidence_model/5_evidence_model.md` Section 18.1 describes this same object (there called `EvidenceRecordDTO`) with a much larger field set covering time trust, spatial validity, device health, attestation, AI extraction metadata, privacy/PII lifecycle, and conflict resolution. Those fields have been merged in below as additive fields, grouped into nested DTOs that mirror the existing `SourceMetadataDTO`/`ConfidenceDTO`/`FreshnessDTO` convention, rather than flattened directly onto `EvidenceDTO`.

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
evidence\_category  
target\_entity\_refs  
related\_event\_refs  
related\_state\_refs  
related\_action\_refs  
payload\_hash  
validity\_status  
freshness\_status  
ontology\_binding\_ref  
prov\_entity\_ref  
activity\_refs  
was\_generated\_by  
was\_derived\_from  
was\_attributed\_to  
hash  
signature  
created\_by  
supersedes\_evidence\_id  
is\_append\_only  
time\_trust  
spatial\_validity  
device\_health  
attestation  
ai\_extraction  
privacy  
conflict

`source_metadata.source_trust_level` uses the `SourceTrustLevel` enum (`schemas/enums.py`: TRUSTED_SYSTEM, VERIFIED_DEVICE, VERIFIED_HUMAN, VERIFIED_DOCUMENT, THIRD_PARTY_VERIFIED, AI_DERIVED, ATTESTED_AI_DERIVED, UNVERIFIED_SOURCE, UNKNOWN_SOURCE), sourced from `05_evidence_model.md` Section 6.1. `evidence_category` uses `EvidenceCategory` (18 members, Section 5.1) — distinct from `evidence_type`, which remains registry-managed vocabulary per Section 8.2 above. `validity_status` uses `EvidenceValidityStatus` (15 members, Section 9.2) — a separate, larger enum from `ValidationStatus` (which governs `validation_status`, sourced from Section 5.2 above).

`time_trust` is a `TimeTrustDTO` (Section 7.1: `captured_at`, `received_at`, `validated_at`, `source_clock_id`, `time_source_type` — `TimeSourceType`, Section 7.2 — `time_authority_ref`, `clock_sync_status` — `ClockSyncStatus` — `clock_drift_estimate_ms`, `clock_drift_calculation_method` — `ClockDriftCalculationMethod`, Section 7.4 — `capture_receive_delta_ms`, `max_allowed_time_delta_ms`, `time_trust_level` — `TimeTrustLevel` — `time_validation_status`, `offline_clock_trust_policy_ref`).

`spatial_validity` is a `SpatialValidityDTO` (Section 8.1: `geo_location`, `geo_crs`, `spatial_context_ref`, `spatial_bounds_ref`). `device_health` is a `DeviceHealthDTO` (Section 8.4: `device_health_snapshot`, `device_health_snapshot_version`, `calibration_status`, `historical_reliability_score`).

`attestation` is an `AttestationDTO` (Section 10.5: `attestation_type` — `AttestationType`, Section 10.2 — `attestation_evidence_refs`, `attestation_signature`, `attestation_workflow_id`, `attestation_hash`, `attested_by`, `attested_at`, plus `trust_upgrade_status` — `TrustUpgradeStatus`, Section 10.3 — and `parser_validation_status`/`human_attestation_status`/`cross_check_status` from the Section 18.1 consolidated list). `ai_extraction` is an `AIExtractionMetadataDTO` (Section 10.4: `is_extracted_evidence`, `extraction_method`, `extracted_from_evidence_id`, `source_document_ref`, `source_location_ref`, `model_name`, `model_version`, `prompt_hash`, `retrieval_corpus_ref`, `retrieval_snapshot_id`, `temperature`, `extraction_confidence`).

`privacy` is a `PrivacyDTO` (Section 15.3: `contains_pii`, `pii_categories`, `privacy_lifecycle_status` — `PrivacyLifecycleStatus`, Section 15.2 — `retention_policy_ref`, `retention_expires_at`, `encryption_key_ref`, `key_management_policy_ref`, `key_destroyed_at`, `legal_hold_status`, `redaction_policy_ref`, `anonymization_method`, `access_policy_ref`; `legal_hold_status` is modeled as `bool` per Section 15.4's explicit boolean usage, and blocks `key_destroyed_at` from being set while true). `conflict` is a `ConflictDTO` (Section 14.3: `conflict_status` — `ConflictStatus`, Section 14.1 — `conflict_weight`, `applied_conflict_weights`, `resolution_timestamp`, `resolved_by`, `conflict_resolution_strategy` — `ConflictResolutionStrategy`, Section 14.2 — `conflict_resolution_ref`).

`time_validation_status`, `calibration_status`, `parser_validation_status`, `human_attestation_status`, `cross_check_status`, `extraction_method`, and `freshness_status` remain plain `str`: no closed value list was found for any of them anywhere in `05_evidence_model.md`.

`EvidenceDTO`'s `reject_unattested_ai_as_evidence` validator rejects only `source_trust_level=AI_DERIVED` (raw, unattested AI output, per Section 4.5's "Prohibited LLM roles: Create Primary Evidence"). `ATTESTED_AI_DERIVED` — reached via the Section 10 attestation/trust-upgrade process — is explicitly allowed, per Section 6.1's trust model and Section 10.6's worked example.

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

`risk_level` uses the `RiskLevel` enum (`schemas/enums.py`: INFO, NOTICE, WARNING, HIGH_RISK, CRITICAL_EMERGENCY, EXCEPTIONAL), sourced from `07_decision_approval_matrix.md` Section 9.1 ("Risk Level").

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

`decision_tier` uses the `DecisionTier` enum (`schemas/enums.py`: ROUTINE, NOTICE, WARNING, HIGH_RISK, CRITICAL_EMERGENCY, EXCEPTIONAL), sourced from `0_canonical_object_lifecycle.md` Section 4.8 "Decision Tiers". `risk_level` is a separate field using the `RiskLevel` enum (INFO, NOTICE, WARNING, HIGH_RISK, CRITICAL_EMERGENCY, EXCEPTIONAL), sourced from `07_decision_approval_matrix.md` Section 9.1 — the two enums share 5 of 6 members but are not the same field. `urgency` remains `str` (`DOMAIN_DECISION_REQUIRED`, no closed value list found).

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

ApprovedActionDTO is created after the required policy, decision, and approval path grants authority.

It is not created by the Safety Gate.

It is not a SafetyGatePass and cannot create an ExecutionRequest without Runtime Validation and a valid SafetyGatePass.

`risk_level` uses the `RiskLevel` enum (`schemas/enums.py`: INFO, NOTICE, WARNING, HIGH_RISK, CRITICAL_EMERGENCY, EXCEPTIONAL), sourced from `07_decision_approval_matrix.md` Section 9.1 ("Risk Level").

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

EmergencyApprovedActionDTO is a deterministic emergency authority object.

It is not a Safety Gate bypass and cannot create an ExecutionRequest without minimum emergency Runtime Validation and an emergency SafetyGatePass.

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

Enum (`PostAuditStatus`, `schemas/enums.py`):

PENDING  
REVIEWED  
APPROVED  
REJECTED  
ESCALATED

Also used by `AuditRecordDTO.post_audit_status`.

---

## **17.3 ExecutionRequestDTO**

ExecutionRequestDTO may be created only after a valid SafetyGatePass or emergency SafetyGatePass is issued.

No SafetyGatePass, no ExecutionRequestDTO.

Canonical Reference: this is the canonical field-level contract for `ExecutionRequestDTO`. `09_execution_adapter_model/9_execution_adapter_model.md` Section 7.2 previously showed a competing reference-only field list (`safety_gate_result_ref`, `execution_context_snapshot_ref`, `target_entity_refs`, `execution_mode`, `required_adapter_type`, `required_capability`, `decision_trace_id`); that list has been rewritten to match this section. Do not implement `ExecutionRequestDTO` against any earlier version of Section 7.2.

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

## **17.3A Runtime Validation and Safety Gate DTO Contracts**

These DTOs define architecture-level contracts only. They do not define domain thresholds, legal rules, robot behavior rules, PLC semantics, or SCADA write semantics.

`ValidatorResultDTO` (inherited by all Specialized Runtime Result DTOs below) and `SafetyGatePassDTO`/`SafetyGateBlockDTO`/`SafetyGateResultDTO` match the canonical field lists in `08_runtime_validation/validators/validators.md` Section 7 and `08_runtime_validation/safety_gate/safety_gate.md` Sections 8, 10, and 23 exactly — field names included, not just value types. `RuntimeValidationResultDTO` and `RuntimeValidationInputDTO` have no separate canonical field-level contract of their own in `08_runtime_validation/` and keep their prior shape.

`ValidatorResultDTO.status` and `RuntimeValidationResultDTO.result` use the `ValidatorStatus` enum (`schemas/enums.py`: PASS, FAIL, WARNING, HOLD, RETRY, REQUIRES_REVALIDATION, REQUIRES_REAPPROVAL, MANUAL_REVIEW_REQUIRED, BLOCK), sourced from `validators.md` Section 7. `ValidatorResultDTO.severity` uses `Severity` (INFO, WARNING, ERROR, CRITICAL). `ValidatorResultDTO.tier` and `SafetyGateBlockDTO.tier` use `CriticalityTier` (TIER_1_SAFETY_CRITICAL, TIER_2_OPERATIONAL_CRITICAL, TIER_3_INFORMATIONAL), sourced from `safety_gate.md` Section 14, cross-confirmed by `toctou.md` Section 16.

`SafetyGatePassDTO.terminal_status` uses the `SafetyGatePassTerminalStatus` enum (`schemas/enums.py`: ISSUED, DISPATCHING, CONSUMED_ACCEPTED, CONSUMED_REJECTED, CONSUMED_DROPPED, EXPIRED, REVOKED), sourced from `toctou.md` Section 21. `SafetyGateBlockDTO.block_reasons` uses the `BlockReason` enum (17 members), sourced from `safety_gate.md` Section 10's "Possible block reasons" list. `SafetyGateResultDTO.status` uses its own `SafetyGateResultStatus` enum (PASS, BLOCK, MANUAL_REVIEW_REQUIRED, HOLD, REQUIRES_REVALIDATION, REQUIRES_REAPPROVAL) — a distinct, smaller list from `ValidatorStatus`, per `safety_gate.md` Section 23's own "Possible status" list.

`SafetySnapshotDTO` and `SafetyGateInputDTO` were reconciled against `safety_gate.md` Section 6's fuller input list, `shacl_shapes.md` Section 11.1, and `validators.md` Section 10.2 (see the per-DTO field lists below). `SafetySnapshotDTO.status` remains `str`: no closed value list was found for this field anywhere.

The Emergency Fast-Path mirrors of these DTOs (`EmergencyRuntimeValidationInputDTO`, `EmergencyRuntimeValidationResultDTO`, `EmergencySafetyGatePassDTO`, `EmergencySafetyGateBlockDTO`) live in `schemas/emergency.py`, not here, per Section 12 "Recommended Code Mapping" in `0_canonical_object_lifecycle.md`, and mirror the same corrected shapes.

### **RuntimeValidationInputDTO**

Minimum fields:

id  
approved_action_id  
action_type  
input_refs  
trace_id  
correlation_id  
created_at_utc

### **RuntimeValidationResultDTO**

Minimum fields:

id  
approved_action_id  
action_type  
result  
checked_at  
input_refs  
validator_result_refs  
failure_reasons  
trace_id  
correlation_id  
audit_ref

### **ValidatorResultDTO**

Canonical fields (`validators.md` Section 7):

result_id  
validator_id  
validator_version  
approved_action_id  
action_type  
status  
severity  
tier  
checked_at  
input_refs  
failure_reasons  
warning_reasons  
suggested_next_state  
safety_gate_eligible  
trace_id  
correlation_id  
audit_ref

### **Specialized Runtime Result DTOs**

The following DTOs follow the ValidatorResultDTO pattern and add the fields required by their own dedicated contract section:

TOCTOUResultDTO  
SHACLValidationResultDTO  
NetworkHealthResultDTO  
IdempotencyResultDTO  
ApprovalValidityResultDTO  
PolicyRevalidationResultDTO  
EvidenceValidityResultDTO

`TOCTOUResultDTO` matches `toctou.md` Section 24 ("TOCTOU Validation Result"): adds `approval_snapshot_ref`, `execution_snapshot_ref`, `changed_fields`, `stale_fields`, `conflict_fields`, `block_reasons` (`BlockReason`), `required_reapproval`.

`SHACLValidationResultDTO` matches `shacl_shapes.md` Sections 17.1 and 20: adds `shape_id`, `shape_version`, `target_node`, `target_type`, `validation_status` (`SHACLValidationStatus`: VALID, INVALID, WARNING, SKIPPED, NOT_APPLICABLE), `violations`.

`NetworkHealthResultDTO` matches `network_health.md` Section 16 ("NetworkHealthResult Contract"): adds `external_system_id`, `adapter_id`, `health_status` (`NetworkHealthStatus`: HEALTHY, DEGRADED, UNREACHABLE, TIMEOUT, CIRCUIT_OPEN, UNKNOWN, sourced from Section 7), `heartbeat_status` (`str`, no closed value list found), `latency_ms`, `error_rate`, `circuit_breaker_status` (`CircuitBreakerStatus`: CLOSED, OPEN, HALF_OPEN, sourced from Section 13), `feedback_channel_status` (`str`, no closed value list found).

`IdempotencyResultDTO` matches `idempotency_control.md` Sections 8 and 19: adds `safety_gate_pass_id`, `execution_request_id`, `external_control_request_id`, `target_external_system`, `first_seen_at`, `last_seen_at`, `ledger_status` (`IdempotencyLedgerStatus`: NEW, IN_PROGRESS, COMPLETED, BLOCKED, REJECTED, EXPIRED, TERMINAL, UNKNOWN), `previous_result_ref`, `terminal_token_ref`, `terminal_token_status` (`str`, no closed value list found).

`ApprovalValidityResultDTO`, `PolicyRevalidationResultDTO`, and `EvidenceValidityResultDTO` were not found to have a dedicated contract section of their own in `08_runtime_validation/` beyond the `ValidatorResultDTO` base pattern; they keep their prior single-reference-field shape.

### **SafetySnapshotDTO**

Minimum fields:

snapshot_id  
snapshot_version  
ontology_version  
policy_version  
registry_version  
status  
created_at  
valid_until  
source_state_versions  
target_scope  
site_ref  
zone_ref  
critical_state_refs  
schema_version  
checksum  
trace_id  
audit_ref

`snapshot_id`, `valid_until`, `source_state_versions`, `target_scope`, `site_ref`,
`zone_ref`, `critical_state_refs`, and `schema_version` are cross-confirmed by both
`08_runtime_validation/shacl_shapes/shacl_shapes.md` Section 11.1
(`SafetySnapshotShape`) and `08_runtime_validation/validators/validators.md`
Section 10.2 (`snapshot_freshness_validator`). `status` remains plain `str`: no
closed value list for this field was found anywhere.

### **SafetyGateInputDTO**

Canonical fields (`safety_gate.md` Section 6, "Recommended inputs"):

safety_gate_input_id  
approved_action_id  
action_type  
runtime_validation_result_ref  
safety_snapshot_ref  
validator_result_summary_ref  
toctou_result_ref  
shacl_validation_result_ref  
network_health_result_ref  
idempotency_result_ref  
approval_validity_result_ref  
policy_revalidation_result_ref  
evidence_validity_result_ref  
capability_availability_result_ref  
trace_id  
correlation_id

Only `approved_action_id`, `action_type`, `runtime_validation_result_ref`, and
`safety_snapshot_ref` are required; the remaining validator-category result refs are
optional, since not every action type exercises every validator category. `input_refs`
is kept as a generic overflow field for any additional references beyond this list.

### **SafetyGatePassDTO**

Canonical fields (`safety_gate.md` Section 8):

safety_gate_pass_id  
approved_action_id  
action_type  
issued_at  
expires_at  
lease_duration_ms  
lease_started_monotonic_ms  
lease_expires_monotonic_ms  
target_external_system  
execution_request_scope  
idempotency_key  
safety_snapshot_ref  
runtime_validation_result_ref  
trace_id  
correlation_id  
terminal_status

### **SafetyGateBlockDTO**

Canonical fields (`safety_gate.md` Section 10):

safety_gate_block_id  
approved_action_id  
action_type  
blocked_at  
block_reasons  
failed_validator_refs  
failed_runtime_validation_ref  
safety_snapshot_ref  
severity  
tier  
suggested_next_state  
manual_review_required  
trace_id  
correlation_id  
audit_ref

### **SafetyGateResultDTO**

Canonical fields (`safety_gate.md` Section 23):

result_id  
approved_action_id  
action_type  
status  
issued_pass_ref  
block_ref  
checked_at  
runtime_validation_result_ref  
safety_snapshot_ref  
validator_summary_ref  
decision_reasons  
failure_reasons  
warning_reasons  
suggested_next_state  
trace_id  
correlation_id  
audit_ref

---

## **17.4 ExternalControlRequestDTO**

Canonical Reference: this is the canonical field-level contract for `ExternalControlRequestDTO`. `09_execution_adapter_model/9_execution_adapter_model.md` Section 16 describes the same object under the same name with a differently-shaped field list; that section's real, non-redundant fields (adapter type/mode, dispatch tracking, ACK/ACCEPT/feedback deadlines, adapter-local timing, clock sync) have been merged in below. `sent_at`/`platform_sent_at` and `trace_id`/`correlation_id` from that section are the same concepts as `sent_at_utc` and `trace_context` below, not separate fields.

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
execution\_context\_snapshot\_ref  
adapter\_type  
adapter\_mode  
external\_request\_type  
external\_payload\_ref  
external\_payload\_hash  
idempotency\_expires\_at  
dispatch\_context\_ref  
dispatch\_attempt  
dispatch\_status  
ack\_deadline  
acceptance\_deadline  
feedback\_deadline  
adapter\_local\_received\_at  
adapter\_local\_accepted\_at  
clock\_sync\_status  
clock\_drift\_estimate\_ms  
decision\_trace\_id

`dispatch_status` uses the `DispatchStatus` enum (Section 20 below). `clock_sync_status` uses `ClockSyncStatus` (`05_evidence_model.md` Section 7.3).

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

Canonical Reference: this is the canonical field-level contract for `FeedbackEventDTO`. `09_execution_adapter_model/9_execution_adapter_model.md` Section 17 describes the same object under the same name with a differently-shaped field list; that section's real, non-redundant fields (result detail, actual execution timing, reconciliation/audit routing flags, decision trace correlation) have been merged in below. `external_control_request_ref` and `external_system_id` from that section are the same concepts as `external_request_ref` and `source_system` below, not separate fields.

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
feedback\_status  
result\_status  
result\_message  
external\_reference\_id  
actual\_started\_at  
actual\_completed\_at  
observed\_state\_refs  
feedback\_payload\_ref  
error\_detail\_ref  
requires\_reconciliation  
requires\_audit  
decision\_trace\_id

`feedback_status` and `result_status` remain plain `str`: no closed value list was found for either in any document.

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

Canonical Reference: `state` is NOT a locally-defined value set. The single canonical, implementation-authoritative enum (`DispatchStatus`, `schemas/enums.py`) is defined in `03_core_specifications/09_execution_adapter_model/9_execution_adapter_model.md` Section 20 "Dispatch Lifecycle" (20 members: CREATED, READY_TO_DISPATCH, DISPATCHED, ACKNOWLEDGED, ACCEPTANCE_PENDING, ACCEPTED, REJECTED, IN_PROGRESS, PARTIAL_SUCCESS, COMPLETED, FAILED, TIMEOUT, ACK_TIMEOUT, ACCEPTANCE_TIMEOUT, FEEDBACK_TIMEOUT, CANCELLED, FEEDBACK_MISSING, RECOVERY_REQUIRED, MANUAL_OVERRIDE_REQUIRED, CLOSED). Do not implement `ExecutionStateDTO.state` against any shorter illustrative list, including a prior version of this section — this mirrors `0_canonical_object_lifecycle.md` Section 8.2's own "Command State Machine" canonical-reference note.

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

Enum (`ReviewStatus`, `schemas/enums.py`):

PENDING  
REVIEWED  
APPROVED  
REJECTED  
ESCALATED  
REQUIRES\_POLICY\_UPDATE  
REQUIRES\_ONTOLOGY\_UPDATE

Also used by `MappingReviewDTO.review_status` (Section 19.8).

---

## **18.5 AuditRecordDTO**

Canonical Reference: this is the canonical field-level contract for `AuditRecordDTO`. `10_audit_observability_model/10_audit_observability_model.md` Section 9.1 previously showed a competing reference-only redesign (delegating stage context to a separate `AuditContextSnapshotDTO`); that redesign was not adopted, for the same reason documented for `ExecutionRequestDTO` in Section 17.3. However, Section 9.1 also named real capability this section's original field list lacked entirely — a tamper-evident hash chain and multi-causality trace correlation — which has been merged in below as additive, optional fields.

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
audit\_event\_type  
severity  
audit\_reason  
occurred\_at  
time\_trust\_level  
clock\_sync\_status  
source\_system\_ref  
correlation\_id  
decision\_trace\_id  
primary\_causality\_id  
causality\_ids  
integrity\_policy\_ref  
content\_hash  
previous\_record\_hash  
integrity\_status

`severity` uses the `Severity` enum (`schemas/enums.py`: INFO, WARNING, ERROR, CRITICAL). `time_trust_level` uses `TimeTrustLevel` (HIGH_TIME_TRUST, MEDIUM_TIME_TRUST, LOW_TIME_TRUST, UNTRUSTED_TIME, UNKNOWN_TIME_TRUST), sourced from `05_evidence_model.md` Section 7.5. `clock_sync_status` uses `ClockSyncStatus` (SYNCED, PARTIALLY_SYNCED, UNSYNCED, DRIFT_DETECTED, OFFLINE_ESTIMATED, UNKNOWN), sourced from `05_evidence_model.md` Section 7.3. `audit_event_type` and `integrity_status` remain plain `str`: no complete closed value list was found for either (`10_audit_observability_model.md` Section 16.1 gives only a partial dispatch-stage mapping for `audit_event_type`).

Fields from Section 9.1 that duplicate existing capability were not added: `actor_ref`/`actor_role` (redundant with the existing plural `actor_refs`), `result_status` (redundant with the existing `final_status`), `action_type`/`target_entity_refs` (already reachable via the existing stage refs), and `audit_context_snapshot_ref`/`decision_trace_ref` (assume the rejected reference-delegation design; `decision_trace_id` — a plain correlation string, not a reference to the not-yet-built `DecisionTraceDTO` object — was kept).

---

# **19\. Registry / Governance / Observability DTO**

## **19.1 ActionTypeSpecDTO**

`default_risk_level` uses the `RiskLevel` enum (`schemas/enums.py`: INFO, NOTICE, WARNING, HIGH_RISK, CRITICAL_EMERGENCY, EXCEPTIONAL), sourced from `07_decision_approval_matrix.md` Section 9.1 ("Risk Level").

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

`risk_level` uses the `RiskLevel` enum (`schemas/enums.py`: INFO, NOTICE, WARNING, HIGH_RISK, CRITICAL_EMERGENCY, EXCEPTIONAL), sourced from `07_decision_approval_matrix.md` Section 9.1 ("Risk Level").

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

Canonical Reference: this is the canonical field-level contract for `PolicyDecisionDTO`. `08_policy_governance_model.md` Section 23 describes the same object under a different name (`PolicyDecisionResponseDTO`) with a larger field list; that section's real, non-redundant fields have been merged in below. Section 23's `decision_reason` and `created_at` are the same concepts as `reason` and `evaluated_at_utc` below, not separate fields.

Fields:

policy\_decision\_id  
policy\_refs  
input\_context  
decision\_result  
reason  
obligations  
denial\_reasons  
evaluated\_at\_utc  
policy\_engine  
policy\_engine\_version  
policy\_bundle\_version  
input\_context\_hash  
policy\_context\_ref  
resolution\_context\_ref  
audit\_context\_ref  
required\_approval\_level  
matched\_policy\_refs  
denied\_policy\_refs  
resolved\_policy\_refs  
suppressed\_policy\_refs  
policy\_resolution\_ref  
required\_evidence\_types  
required\_roles  
required\_clearance  
requires\_safety\_gate  
requires\_post\_hoc\_audit  
requires\_revalidation  
requires\_fail\_safe  
trace\_id  
correlation\_id  
decision\_trace\_id

`required_approval_level` uses the `ApprovalAuthority` enum (`schemas/enums.py`; canonical source: `08_policy_governance_model.md` Section 13) — its first DTO field application.

Enum (`PolicyDecisionResult`, `schemas/enums.py`; canonical source: `08_policy_governance_model.md` Section 7):

ALLOW  
DENY  
REQUIRE\_APPROVAL  
REQUIRE\_EVIDENCE  
REQUIRE\_REVALIDATION  
REQUIRE\_FAIL\_SAFE  
REQUIRE\_MANUAL\_OVERRIDE  
REQUIRE\_POLICY\_EXCEPTION\_REVIEW

Also used by `PolicyRefDTO.decision_result` (Section 11.5).

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
enums.py  
base.py  
context.py  
validation.py  
refs.py  
payloads.py  
high\_frequency.py  
event.py  
ontology.py  
evidence.py  
world\_state.py  
action.py (includes IntentDTO)  
decision.py  
approval.py  
execution.py (includes TimeoutPolicyDTO/RetryPolicyDTO/RecoveryPolicyDTO/IdempotencyContextDTO)  
feedback.py (includes WorldStateReconciliationDTO/ExecutionStateDTO)  
audit.py  
registry.py  
governance.py  
observability.py  
emergency.py  
runtime\_validation.py  
safety\_gate.py  
source\_inputs.py

Note: `input.py` and `intent.py` from earlier drafts of this structure are consolidated into `event.py` and `action.py` respectively — see `07_implementation_plan/pre_code_generation_build_plan.md` Step 1 for the authoritative file list.

---

# **22\. Recommended Implementation Order**

The implementation order should be as follows:

enums.py  
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
governance.py  
observability.py  
emergency.py  
high\_frequency.py  
runtime\_validation.py  
safety\_gate.py  
source\_inputs.py

---

# **23\. Required DTOs for the Initial Implementation**

Every DTO defined in this document (Sections 9 through 20, including the Emergency Fast-Path, Monitoring-Only, and Runtime Validation/Safety Gate groups) is built in the initial implementation pass, as structure only.

**Structure vs. governed content.** Building a DTO class now means only that its field names and types exist and are importable — it does not mean the object is populated, registered, or used at runtime. In particular:

- Defining `EmergencyActionSpecDTO`/`EmergencyApprovedActionDTO`/`PostHocAuditDTO` now does not register any real emergency action. A real `emergency_action_type` entry still requires the full governance process in `0_canonical_object_lifecycle.md` Section 5 (Safety Committee, Ontology Steward, Policy Owner, Site Operations Owner, Control System Owner, Security Owner approval) before it is populated with real values and wired into the Emergency Action Registry.
- Defining the Monitoring-Only DTOs (`TimeSeriesSampleDTO`, `MonitoringOnlyEventDTO`, etc.) now does not stand up any live monitoring pipeline — that remains a later implementation step's responsibility.
- Defining the Runtime Validation / Safety Gate DTOs (Section 17.3A) now does not implement the Safety Gate decision logic — those are architecture-level contracts only, per that section's own note.

This "structure now, content later" split is why building the whole DTO catalog up front does not weaken the platform's safety governance: nothing here grants authority, defines a real threshold, or creates an execution path. See `07_implementation_plan/pre_code_generation_build_plan.md` Step 1 for the concrete file layout and the per-step Required Objects list.

Implementation can start from:

schemas/enums.py  
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
→ PolicyDecisionDTO  
→ ApprovalRequestDTO  
→ ApprovalDecisionDTO  
→ ApprovedActionDTO  
→ RuntimeValidationInputDTO  
→ RuntimeValidationResultDTO  
→ SafetyGateInputDTO  
→ SafetyGatePassDTO or SafetyGateBlockDTO  
→ ExecutionRequestDTO  
→ ExternalControlRequestDTO  
→ FeedbackEventDTO  
→ AuditRecordDTO
→ WorldStateUpdateDTO

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
→ RuntimeValidationInputDTO  
→ RuntimeValidationResultDTO  
→ SafetyGateInputDTO  
→ SafetyGatePassDTO or SafetyGateBlockDTO  
→ ExecutionRequestDTO only after SafetyGatePassDTO  
→ FeedbackEventDTO  
→ PostHocAuditDTO  
→ AuditRecordDTO

One-line summary:

Different sources, one schema contract.  
Different frequencies, one lifecycle discipline.  
Different domains, one semantic backbone.  
Different actions, one execution boundary.  
Different feedback, one audit trail.

