# **Ontology-Centric “Evidence Model”**

# **1\. Purpose**

This document defines the core rules of the Evidence Model used in an ontology-centric cyber-physical platform.

The Evidence Model is a structure for standardizing “what the basis of a judgment is” when the platform creates a judgment, state change, ActionCandidate, ApprovedAction, ReconciliationResult, or AuditRecord.

If an Event Type expresses “what happened,” an Action Type expresses “what response can be taken,” and a State Model expresses “what is currently in what state,” then the Evidence Model expresses “what proves that judgment.”

This document focuses on the following:

Define what Evidence is.  
Distinguish Evidence from Raw Input, Event, State, Feedback, and LLM Output.  
Define Evidence Types and Evidence Categories.  
Define Evidence Source Trust, Time Trust, Spatial Validity, and Device Health Trust.  
Define Clock Drift, Offline Clock Trust, and Time Authority policies.  
Define Attested Extraction and Trust Upgrade rules for values extracted through AI/RAG/OCR.  
Define an automatic Evidence Conflict resolution matrix.  
Define Evidence Freshness, Validity, and Privacy Lifecycle.  
Define Evidence Bundle, Evidence Chain, Evidence Graph, and PROV-O integration.  
Define what Evidence is required by ActionCandidate, ApprovedAction, State Transition, and Reconciliation.  
Restrict the scope in which LLM/RAG output may be used as evidence.  
Define the append-only audit principle together with personal data de-identification / crypto-shredding policies.  
Define the operating policy of the Evidence Model Registry.

The full list of evidence types is managed in a separate document: Appendix D: Evidence Type Catalog.

---

# **2\. Document Separation Principle**

The Evidence Model document is divided into two parts.

## **2.1 Core Evidence Model Specification**

This is the present document.

It covers:

Evidence definition  
Distinction between Evidence and Raw Input / Event / State / Feedback / LLM Output  
Evidence taxonomy  
Source trust model  
Time trust model  
Spatial validity model  
Device health trust model  
Evidence freshness and validity rules  
Attested extraction rule  
Evidence conflict resolution rule  
Evidence bundle rule  
Evidence chain and provenance rule  
Evidence graph rule  
Privacy-safe append-only rule  
Evidence requirement rule  
LLM/RAG evidence boundary  
Registry governance  
Initial reference evidence model set  
Core scenario flows

## **2.2 Appendix D: Evidence Type Catalog**

This is a separate appendix document.

It covers:

sensor evidence list  
robot telemetry evidence list  
worker location evidence list  
equipment telemetry evidence list  
external feedback evidence list  
human confirmation evidence list  
document evidence list  
permit evidence list  
inspection evidence list  
policy evidence list  
AI-derived evidence list  
audit evidence list

By separating the documents this way, the core document can remain short and stable, while the evidence catalog can continue to expand according to field data and domain expansion.

---

# **3\. Definition of Evidence**

Evidence is verifiable ground truth that the platform references to justify a judgment or state change.

Evidence must answer the following questions:

What is the basis of this judgment?  
Where did this evidence come from?  
Is the source of this evidence trustworthy?  
When was this evidence actually captured?  
When was this evidence received by the platform?  
Is the source clock trustworthy?  
Does clock drift exist?  
In which physical space is this evidence valid?  
What was the health state of the device that generated this evidence?  
Is this evidence still valid?  
Which entity, event, state, and action is this evidence connected to?  
Is this evidence original data, a summary, an extracted value, or an inference result?  
If AI extracted it, from what original source and through what validation method was it verified?  
Can this evidence be protected from tampering or traced for audit?  
Does this evidence contain personal information?  
Is this evidence sufficient by itself, or is an evidence bundle required?  
Can this evidence be used for Safety Gate judgment?  
Is this evidence LLM output, or actual observational data?

Example:

GasSensor\_17 reported 87 ppm at 2026-06-21T10:03:12Z.

This can become evidence for a gas risk judgment.

Example:

FleetManager reported Mission\_991 disabled.

This can become evidence for the confirmed\_state of MissionStatus.DISABLED.

Example:

Supervisor Kim confirmed Zone\_A evacuation completed.

This can become human confirmation evidence for EvacuationState.EVACUATED.

---

# **4\. Core Distinctions**

## **4.1 Distinction Between Evidence and Raw Input**

Raw Input is an input that has not yet been validated.

Evidence is ground that has passed at least schema validation, source validation, timestamp validation, and ontology binding or target binding.

Example:

Raw Input:

{ "sensor": "G17", "value": 87 }

Evidence:

GasSensor\_17 measured gas concentration 87 ppm,  
source validated,  
timestamp checked,  
bound to Zone\_A,  
device health snapshot attached,  
classified as SENSOR\_OBSERVATION\_EVIDENCE.

Raw Input is not immediately Evidence.

---

## **4.2 Distinction Between Evidence and Event**

An Event is something that happened.

Evidence is the ground that supports the fact that the event occurred.

Example:

Event Type:

safety.gas.critical\_threshold\_exceeded

Evidence:

GasSensor\_17 reading \= 87 ppm  
Gas threshold policy \= 50 ppm  
Sensor health \= OK  
Timestamp freshness \= valid  
Spatial bounds \= Zone\_A

An Event is a semanticized occurrence.  
Evidence is the ground supporting that occurrence.

---

## **4.3 Distinction Between Evidence and State**

State is the current condition of an entity.

Evidence is the ground that allows the state to be accepted.

Example:

State:

MissionStatus.DISABLED

Evidence:

FleetManager feedback: Mission\_991 disabled.  
Robot telemetry: Mission\_991 no longer active.  
ExecutionRequest status: completed.

State is the result.  
Evidence is the ground supporting that result.

---

## **4.4 Distinction Between Evidence and Feedback**

Feedback is an execution result returned by an external system or a human.

Feedback can become evidence, but not all feedback automatically becomes evidence.

For feedback to become evidence, it must pass the following:

source validation  
timestamp validation  
schema validation  
target binding  
correlation with ExecutionRequest  
freshness validation  
time trust validation  
device or system trust validation

Example:

Feedback:

FleetManager says mission disabled.

Evidence:

FleetManager feedback validated,  
correlated with ExecutionRequest\_991,  
target Mission\_991 matched,  
timestamp within valid window,  
source trust level \= TRUSTED\_SYSTEM.

---

## **4.5 Distinction Between Evidence and LLM Output**

LLM Output is not primary evidence by principle.

An LLM may summarize, interpret, or propose a candidate based on evidence.

However, LLM output alone cannot confirm a state or create an ApprovedAction.

Allowed LLM roles:

Create EvidenceSummary  
Create RiskInterpretation  
Create MappingProposal  
Propose ActionCandidate  
Create Explanation  
Create document extraction candidate

Prohibited LLM roles:

Create Primary Evidence  
Confirm Confirmed State  
Directly create ApprovedAction  
Directly create EmergencyApprovedAction  
Directly create ExecutionRequest  
Create Physical command

Core principle:

LLM output may explain evidence.  
LLM output must not replace evidence.

---

# **5\. Evidence Taxonomy**

Evidence is managed by category and type.

## **5.1 Evidence Category**

Recommended Evidence Categories:

SENSOR\_RAW  
SENSOR\_DERIVED  
ROBOT\_TELEMETRY  
WORKER\_LOCATION  
EQUIPMENT\_TELEMETRY  
EXTERNAL\_SYSTEM\_FEEDBACK  
HUMAN\_REPORT  
DOCUMENT\_VERIFIED  
DOCUMENT\_EXTRACTED  
PERMIT\_RECORD  
INSPECTION\_RECORD  
SYSTEM\_LOG  
POLICY\_DECISION  
ONTOLOGY\_BINDING  
ONTOLOGY\_INFERENCE  
DERIVED\_AI  
AUDIT\_RECORD  
THIRD\_PARTY\_API

## **5.2 Core Evidence Types**

Recommended Evidence Types:

SENSOR\_OBSERVATION\_EVIDENCE  
ROBOT\_TELEMETRY\_EVIDENCE  
WORKER\_LOCATION\_EVIDENCE  
EQUIPMENT\_TELEMETRY\_EVIDENCE  
EXTERNAL\_FEEDBACK\_EVIDENCE  
HUMAN\_CONFIRMATION\_EVIDENCE  
DOCUMENT\_EVIDENCE  
PERMIT\_EVIDENCE  
INSPECTION\_EVIDENCE  
SYSTEM\_LOG\_EVIDENCE  
AUDIT\_RECORD\_EVIDENCE  
POLICY\_DECISION\_EVIDENCE  
ONTOLOGY\_BINDING\_EVIDENCE  
INFERENCE\_EVIDENCE  
AI\_SUMMARY\_EVIDENCE  
DOCUMENT\_EXTRACTED\_EVIDENCE  
THIRD\_PARTY\_API\_EVIDENCE

---

# **6\. Evidence Source Trust Model**

Evidence has different trust levels depending on its source.

The Evidence Model must explicitly define source trust.

## **6.1 Source Trust Level**

Recommended values:

TRUSTED\_SYSTEM  
VERIFIED\_DEVICE  
VERIFIED\_HUMAN  
VERIFIED\_DOCUMENT  
THIRD\_PARTY\_VERIFIED  
AI\_DERIVED  
ATTESTED\_AI\_DERIVED  
UNVERIFIED\_SOURCE  
UNKNOWN\_SOURCE

## **6.2 Source Trust Examples**

FleetManager  
→ TRUSTED\_SYSTEM

GasSensor\_17 with valid calibration  
→ VERIFIED\_DEVICE

Supervisor with authenticated identity  
→ VERIFIED\_HUMAN

Uploaded permit PDF with verified document hash  
→ VERIFIED\_DOCUMENT

LLM-generated explanation  
→ AI\_DERIVED

LLM-extracted permit value verified by rule engine and human steward  
→ ATTESTED\_AI\_DERIVED

Unknown mobile input  
→ UNVERIFIED\_SOURCE

## **6.3 Source Trust Rule**

High-risk actions must not be approved using only UNVERIFIED\_SOURCE evidence.

Emergency actions must require at least one trusted or verified evidence item.

AI\_DERIVED evidence cannot pass the Safety Gate by itself.

ATTESTED\_AI\_DERIVED evidence may be used for a limited purpose, but it must include original evidence\_refs and attestation records.

UNKNOWN\_SOURCE evidence can generally be used only for decision support, not for action approval.

---

# **7\. Time Trust and Clock Drift Policy**

Evidence must have time trust.

In field CPS environments, the time of sensors, tablets, robots, edge gateways, and closed-network servers may not perfectly match.

Clock drift can occur especially in the following situations:

underground sites  
network shadow areas  
closed intranets  
delayed upload after offline collection  
device system clock error  
sensor firmware time contamination  
edge gateway buffering

Therefore, evidence freshness must not be judged only by captured\_at.

## **7.1 Time Fields**

EvidenceRecordDTO must have the following time-related fields:

captured\_at  
received\_at  
validated\_at  
source\_clock\_id  
time\_source\_type  
time\_authority\_ref  
clock\_sync\_status  
clock\_drift\_estimate\_ms  
clock\_drift\_calculation\_method  
capture\_receive\_delta\_ms  
max\_allowed\_time\_delta\_ms  
time\_trust\_level  
time\_validation\_status  
offline\_clock\_trust\_policy\_ref

## **7.2 time\_source\_type Values**

PTP  
NTP  
DEVICE\_INTERNAL  
EDGE\_GATEWAY  
RELATIVE  
MANUAL  
UNKNOWN

## **7.3 clock\_sync\_status Values**

SYNCED  
PARTIALLY\_SYNCED  
UNSYNCED  
DRIFT\_DETECTED  
OFFLINE\_ESTIMATED  
UNKNOWN

## **7.4 clock\_drift\_calculation\_method Values**

PTP\_SYNC  
NTP\_SYNC  
EDGE\_GATEWAY\_COMPARISON  
NEIGHBOR\_COMPARISON  
SERVER\_RECEIVE\_DELTA  
LAST\_KNOWN\_GOOD  
MANUAL\_ESTIMATION  
UNKNOWN

## **7.5 time\_trust\_level Values**

HIGH\_TIME\_TRUST  
MEDIUM\_TIME\_TRUST  
LOW\_TIME\_TRUST  
UNTRUSTED\_TIME  
UNKNOWN\_TIME\_TRUST

## **7.6 Time Authority Registry**

time\_authority\_ref must be connected to a separate Time Authority Registry.

Example:

time\_authority\_ref \= Site\_PTP\_Clock\_001  
time\_source\_type \= PTP  
clock\_sync\_status \= SYNCED

In closed-network or offline environments, offline\_clock\_trust\_policy\_ref is used.

Example:

offline\_clock\_trust\_policy\_ref \= OfflineClockPolicy\_B2\_Tunnel  
clock\_drift\_calculation\_method \= LAST\_KNOWN\_GOOD  
time\_trust\_level \= MEDIUM\_TIME\_TRUST

## **7.7 Enhanced Freshness Rule**

Evidence freshness is not judged only by captured\_at.

The following values must be evaluated together:

captured\_at  
received\_at  
source\_clock\_status  
clock\_drift\_estimate\_ms  
capture\_receive\_delta\_ms  
time\_authority\_ref  
offline\_clock\_trust\_policy\_ref

If the source clock is contaminated or drift exceeds the allowed range, freshness\_status cannot be set to VALID.

---

# **8\. Spatial Validity and Device Health Policy**

Evidence depends not only on time but also on space and device state.

For example, GasSensor\_17 is a sensor installed in Zone\_A.

The value from this sensor must not be used for risk judgment in Zone\_B.

Also, even if two sensors report the same value, the trust of the evidence must differ depending on whether the sensor health is OK or WARNING.

## **8.1 Spatial Fields**

EvidenceModelSpecDTO includes the following fields:

allowed\_spatial\_bounds  
spatial\_validity\_rule

EvidenceRecordDTO includes the following fields:

geo\_location  
geo\_crs  
spatial\_context\_ref  
spatial\_bounds\_ref

## **8.2 Definition of allowed\_spatial\_bounds**

allowed\_spatial\_bounds means the physical spatial range in which the evidence type or source is valid.

Example:

GasSensor\_17 evidence is valid only for:  
Zone\_A  
or radius 5m around sensor location.

## **8.3 Definition of geo\_location**

geo\_location is the physical coordinate or site coordinate where the evidence was captured.

Example:

geo\_location \= {  
  site\_id: Site\_001,  
  building\_id: Building\_A,  
  floor: B2,  
  zone\_id: Zone\_A,  
  x: 14.2,  
  y: 8.1,  
  z: \-2.0  
}

geo\_crs \= LOCAL\_SITE

When using a public coordinate reference system:

geo\_crs \= EPSG:5186

## **8.4 Device Health Fields**

EvidenceRecordDTO includes the following fields:

device\_health\_snapshot  
device\_health\_snapshot\_version  
calibration\_status  
historical\_reliability\_score

Example of device\_health\_snapshot:

device\_health\_snapshot \= {  
  battery\_level: 82,  
  signal\_quality: GOOD,  
  calibration\_status: VALID,  
  self\_diagnosis: OK,  
  last\_maintenance\_at: 2026-06-10  
}

## **8.5 Performance Optimization Principle**

For high-frequency sensor data, including device\_health\_snapshot in every EvidenceRecord can become costly.

Therefore, the following hybrid approach is allowed:

High-risk evidence  
→ include device\_health\_snapshot inline

High-frequency normal telemetry  
→ include only device\_health\_snapshot\_version or HealthEvent reference

Device health change detected  
→ create separate DeviceHealthEvidence

---

# **9\. Evidence Freshness and Validity Rule**

Evidence can become stale over time.

Freshness management is especially important for sensor, robot telemetry, worker location, gas level, and equipment state evidence.

## **9.1 Freshness TTL Examples**

GasSensorEvidence → 1 second to 5 seconds  
RobotPoseEvidence → 2 seconds  
WorkerLocationEvidence → 5 seconds  
EquipmentTelemetryEvidence → 10 seconds  
PermitEvidence → permit validity period  
InspectionEvidence → inspection validity period  
HumanConfirmationEvidence → context-dependent  
ExecutionFeedbackEvidence → lifecycle controlled  
AuditEvidence → permanent

## **9.2 Evidence Validity Status**

Recommended values:

VALID  
STALE  
EXPIRED  
REVOKED  
CONFLICTED  
UNVERIFIED  
SUPERSEDED  
INVALID  
ANONYMIZED  
PSEUDONYMIZED  
PII\_REDACTED  
CRYPTO\_SHREDDED  
RETENTION\_EXPIRED  
ACCESS\_RESTRICTED  
LEGAL\_HOLD

## **9.3 Freshness Rule**

High-risk actions must not be approved based on stale evidence.

Emergency actions may use stale evidence, but they must require fail-safe policy and post-hoc audit.

Document evidence must check not only the timestamp of the document itself, but also the business validity period described by the document.

Example:

Permit PDF uploaded today,  
but permit expired yesterday.

In this case, document freshness may be valid, but permit validity is expired.

---

# **10\. Attested Extraction Policy**

Values extracted from documents, drawings, PDFs, or images through AI/RAG/OCR require a separate validation process.

Even if the original document is VERIFIED\_DOCUMENT, the value extracted by AI does not automatically become VERIFIED\_DOCUMENT.

## **10.1 Basic Principle**

Values extracted by AI are AI\_DERIVED by default.

However, if the following conditions are met, the trust level may be upgraded for a limited purpose.

The original document is VERIFIED\_DOCUMENT.  
The extraction location is linked to a page / section / bounding box.  
A deterministic parser or rule validator verified the extracted value.  
A human steward confirmed the extracted value.  
The extracted value was cross-checked against another trusted system record.

## **10.2 Attestation Type**

Recommended values:

HUMAN\_STEWARD  
RULE\_ENGINE  
CROSS\_SYSTEM  
MULTI\_PARTY  
DETERMINISTIC\_PARSER  
DOCUMENT\_HASH\_MATCH

## **10.3 Trust Upgrade Status**

Recommended values:

NO\_UPGRADE  
TRUST\_UPGRADE\_PENDING  
TRUST\_UPGRADED\_BY\_RULE  
TRUST\_UPGRADED\_BY\_HUMAN  
TRUST\_UPGRADED\_BY\_CROSS\_CHECK  
TRUST\_UPGRADED\_BY\_MULTI\_PARTY  
TRUST\_UPGRADE\_REJECTED

## **10.4 AI Extraction Metadata**

LLM/RAG/OCR extracted evidence should optionally have the following metadata:

model\_name  
model\_version  
prompt\_hash  
retrieval\_corpus\_ref  
retrieval\_snapshot\_id  
temperature  
extraction\_confidence  
source\_location\_ref

These fields are required for auditability and reproducibility.

## **10.5 Attestation Evidence Fields**

EvidenceRecordDTO includes the following fields:

attestation\_type  
attestation\_evidence\_refs  
attestation\_signature  
attestation\_workflow\_id  
attestation\_hash  
attested\_by  
attested\_at

## **10.6 Example**

Original Evidence:

PermitDocument\_001  
source\_trust\_level \= VERIFIED\_DOCUMENT  
document\_hash \= abc123

AI Extracted Evidence:

Permit expiry time \= 15:00  
source\_trust\_level \= AI\_DERIVED  
extracted\_from\_evidence\_id \= PermitDocument\_001  
source\_location\_ref \= page 3, table 2, cell B4

Rule Check:

Regex confirms time format.  
Permit section matches expected field.

Human Attestation:

Safety steward confirmed extraction.

Final:

trust\_upgrade\_status \= TRUST\_UPGRADED\_BY\_HUMAN  
source\_trust\_level \= ATTESTED\_AI\_DERIVED  
usable\_for \= PermitStatus validation

---

# **11\. Evidence Grounding and Requirement Rule**

Grounding means that a judgment, state, action candidate, or explanation is connected to actual evidence.

The core of the Evidence Model is that every important judgment must have evidence\_refs.

## **11.1 Objects That Require Evidence**

The following objects must have evidence\_refs:

OntologyBoundEvent  
WorldStateUpdate  
StateTransition  
ActionCandidate  
DecisionCase  
ApprovalRequest  
ApprovedAction  
ExecutionRequest  
FeedbackEvent  
ReconciliationResult  
AuditRecord

## **11.2 EvidenceRequirementSpecDTO Fields**

Recommended fields:

requirement\_id  
target\_object\_type  
target\_action\_type  
target\_state\_transition  
required\_evidence\_types  
minimum\_source\_trust\_level  
minimum\_evidence\_count  
freshness\_requirement  
time\_trust\_requirement  
spatial\_validity\_requirement  
device\_health\_requirement  
requires\_bundle  
requires\_human\_confirmation  
requires\_policy\_decision  
requires\_audit  
valid\_from  
valid\_until  
version

## **11.3 Evidence Requirement Example**

ACTION\_EMERGENCY\_EVACUATE\_ZONE:

required\_evidence\_types:  
  \- SENSOR\_OBSERVATION\_EVIDENCE  
  \- WORKER\_LOCATION\_EVIDENCE  
  \- POLICY\_DECISION\_EVIDENCE

minimum\_source\_trust\_level:  
  VERIFIED\_DEVICE

freshness\_requirement:  
  within 5 seconds

time\_trust\_requirement:  
  MEDIUM\_TIME\_TRUST or higher

requires\_bundle:  
  true

requires\_post\_hoc\_audit:  
  true

---

# **12\. Evidence Bundle Rule**

A single piece of evidence is often not enough.

An Evidence Bundle groups multiple evidence records into one basis of judgment.

## **12.1 Cases That Require an Evidence Bundle**

Evidence bundles are required in the following cases:

High-risk action  
Emergency action  
State reconciliation  
Human approval  
Policy exception  
Ontology mapping review  
Legal or compliance decision  
Post-hoc audit

## **12.2 Evidence Bundle Example**

Emergency evacuation bundle:

EvidenceBundle:  
  \- GasSensor\_17 reading \= 87 ppm  
  \- GasSensor\_17 health \= OK  
  \- Zone\_A occupancy \= 5 workers  
  \- Zone\_A ventilation state \= FAILED  
  \- Gas threshold policy \= 50 ppm  
  \- Timestamp freshness \= valid  
  \- Time trust \= HIGH\_TIME\_TRUST  
  \- Spatial validity \= Zone\_A

This bundle can support the following ActionCandidate:

ACTION\_EMERGENCY\_EVACUATE\_ZONE

---

# **13\. Evidence Chain, PROV-O, and Evidence Graph**

Evidence must be traceable by source and transformation process.

This is called an Evidence Chain or Provenance.

In the long term, it is desirable to standardize this using W3C PROV-O.

## **13.1 Evidence Chain Example**

Raw Sensor Packet  
→ CanonicalEventEnvelope  
→ OntologyBoundEvent  
→ Evidence  
→ EvidenceBundle  
→ ActionCandidate  
→ ApprovedAction  
→ ExecutionRequest  
→ FeedbackEvent  
→ AuditRecord

## **13.2 PROV-O Integration Fields**

EvidenceRecordDTO includes the following fields:

prov\_entity\_ref  
activity\_refs  
was\_generated\_by  
was\_derived\_from  
was\_attributed\_to

## **13.3 Evidence Graph**

Evidence can be managed not only as a list of DTOs but also as a graph.

Recommended relationships:

derived\_from  
conflicts\_with  
supports  
attests  
supersedes  
corroborates  
invalidates

Example:

AI\_Extracted\_PermitTime  
→ derived\_from → PermitDocument\_001

HumanStewardConfirmation  
→ attests → AI\_Extracted\_PermitTime

GasSensor\_A\_Reading  
→ conflicts\_with → GasSensor\_B\_Reading

GasRiskEvidenceBundle  
→ supports → ACTION\_EMERGENCY\_EVACUATE\_ZONE

## **13.4 Immutability Rule**

Evidence must not be arbitrarily modified after creation.

If correction is required, the existing evidence must not be changed; instead, new evidence must be created.

Principles:

Evidence is append-only.  
Evidence is not overwritten.  
Evidence correction creates a new evidence record.

---

# **14\. Evidence Conflict Resolution Policy**

Evidence can conflict with other evidence.

Example:

GasSensor\_A \= 87 ppm, Health \= OK  
GasSensor\_B \= 0 ppm, Health \= Warning  
Worker report \= no gas smell

Conflict is not deleted.

Conflict is explicitly recorded, and it is resolved according to policy or connected to fail-safe.

## **14.1 Conflict Status**

Recommended values:

NO\_CONFLICT  
CONFLICT\_DETECTED  
CONFLICT\_UNDER\_REVIEW  
CONFLICT\_RESOLVED  
CONFLICT\_ESCALATED  
FAIL\_SAFE\_ON\_CONFLICT

## **14.2 Conflict Resolution Strategy**

Recommended values:

MANUAL\_REVIEW\_ONLY  
TRUST\_WEIGHTED\_SELECTION  
DEVICE\_HEALTH\_WEIGHTED\_SELECTION  
SPATIAL\_VOTING  
TEMPORAL\_FRESHNESS\_PRIORITY  
SAFETY\_CONSERVATIVE\_PRIORITY  
MAJORITY\_VOTE  
FAIL\_SAFE\_ON\_CONFLICT

## **14.3 Applied Conflict Weights**

The actual weights applied in the conflict resolution result must be recorded for audit reproducibility.

EvidenceRecordDTO or ConflictResolutionRecordDTO includes the following fields:

applied\_conflict\_weights  
resolution\_timestamp  
resolved\_by  
conflict\_resolution\_strategy  
conflict\_resolution\_ref

Example:

applied\_conflict\_weights \= {  
  source\_trust\_weight: 0.30,  
  device\_health\_weight: 0.30,  
  spatial\_proximity\_weight: 0.20,  
  freshness\_weight: 0.15,  
  historical\_reliability\_weight: 0.05  
}

## **14.4 FAIL\_SAFE\_ON\_CONFLICT Conditions**

In safety-critical situations, if a conflict is not resolved, it must be connected to fail-safe.

Recommended condition:

risk\_level \>= HIGH\_RISK  
AND conflict\_status \!= CONFLICT\_RESOLVED  
AND required\_evidence\_missing \= true

Or:

risk\_level \= CRITICAL\_EMERGENCY  
AND evidence\_conflict\_detected \= true

Result:

conflict\_resolution\_strategy \= FAIL\_SAFE\_ON\_CONFLICT  
EmergencyActionCandidate generated  
Post-hoc audit required

## **14.5 Example: Gas Sensor Conflict**

Situation:

GasSensor\_A:  
  value \= 87 ppm  
  health \= OK  
  source\_trust\_level \= VERIFIED\_DEVICE  
  distance\_to\_zone\_center \= 3 m

GasSensor\_B:  
  value \= 0 ppm  
  health \= WARNING  
  source\_trust\_level \= VERIFIED\_DEVICE  
  distance\_to\_zone\_center \= 18 m

Judgment:

GasSensor\_A has higher health score.  
GasSensor\_A is spatially closer.  
GasSensor\_A is fresher.  
GasSensor\_B has degraded health.

Result:

conflict\_resolution\_strategy \= DEVICE\_HEALTH\_WEIGHTED\_SELECTION  
selected\_evidence \= GasSensor\_A  
conflict\_status \= CONFLICT\_RESOLVED  
safety\_action\_allowed \= true

---

# **15\. Privacy-Safe Append-only Policy**

The Evidence Model follows the append-only principle.

However, worker location, voice, images, biometric data, mobile input, and similar data can contain personal information.

Therefore, the system needs a structure that protects personal information without deleting the evidence itself.

## **15.1 Core Principle**

The audit shell is preserved.  
PII payload may be subject to encryption, masking, de-identification, or crypto-shredding.  
When a deletion request is made or the retention period expires, the decryption key for the payload may be destroyed.  
The Evidence record itself remains, but personally identifiable information can be made unrecoverable.

## **15.2 Privacy Lifecycle Status**

Recommended values:

PII\_NOT\_PRESENT  
PII\_PRESENT  
PII\_MASKED  
PII\_PSEUDONYMIZED  
PII\_ANONYMIZED  
PII\_CRYPTO\_SHREDDED  
PII\_RETENTION\_EXPIRED  
LEGAL\_HOLD

## **15.3 Key Management Fields**

EvidenceRecordDTO includes the following fields:

contains\_pii  
pii\_categories  
privacy\_lifecycle\_status  
retention\_policy\_ref  
retention\_expires\_at  
encryption\_key\_ref  
key\_management\_policy\_ref  
key\_destroyed\_at  
legal\_hold\_status  
redaction\_policy\_ref  
anonymization\_method  
access\_policy\_ref  
payload\_hash

## **15.4 Legal Hold Rule**

In LEGAL\_HOLD status, crypto-shredding or payload destruction cannot be performed.

Principle:

If legal\_hold\_status \= true,  
then key\_destroyed\_at must remain null  
until legal hold is released.

## **15.5 Payload Hash Rule**

Even after crypto-shredding, the system must be able to prove that “this evidence existed.”

Therefore, the audit shell preserves the cryptographic hash of the original payload.

Principles:

PII payload may be destroyed.  
Payload hash must remain in audit shell.  
Evidence existence remains provable.  
PII must not remain recoverable.

---

# **16\. LLM / RAG Evidence Boundary**

LLM and RAG can handle evidence, but they are not primary evidence.

## **16.1 Allowed Roles**

LLM / RAG may perform the following:

summarize evidence  
classify evidence  
extract evidence candidates from documents  
suggest ontology mapping  
generate risk interpretation  
generate explanation  
propose ActionCandidate

## **16.2 Prohibited Roles**

LLM / RAG may not perform the following:

create primary evidence without source  
confirm state directly  
approve action directly  
create EmergencyApprovedAction directly  
replace sensor evidence  
replace human confirmation  
replace policy decision

## **16.3 AI-Derived Evidence Rule**

AI-generated summaries or interpretations must have original evidence\_refs.

Example:

AI Summary:  
Zone\_A appears dangerous.

Required grounding:  
evidence\_refs \= \[  
  GasSensor\_17 reading,  
  WorkerLocation\_Zone\_A,  
  VentilationState\_Zone\_A,  
  GasThresholdPolicy  
\]

AI Summary can explain evidence.  
AI Summary cannot replace evidence.

---

# **17\. EvidenceModelSpecDTO**

The Evidence Model is managed through EvidenceModelSpecDTO.

## **17.1 EvidenceModelSpecDTO Fields**

Recommended fields:

evidence\_type  
evidence\_category  
description

allowed\_source\_types  
minimum\_source\_trust\_level

requires\_ontology\_binding  
requires\_shacl\_validation  
requires\_prov\_o\_binding  
requires\_timestamp  
requires\_signature  
requires\_hash

freshness\_ttl  
validity\_rule  
conflict\_policy

allowed\_spatial\_bounds  
spatial\_validity\_rule

allowed\_target\_object\_types  
can\_support\_event\_types  
can\_support\_state\_transitions  
can\_support\_action\_types  
can\_support\_approval  
can\_support\_reconciliation  
can\_support\_audit

is\_primary\_evidence  
is\_ai\_derived  
requires\_original\_evidence\_refs

supports\_trust\_upgrade  
trust\_upgrade\_policy  
attestation\_required

contains\_pii\_possible  
privacy\_policy\_ref  
retention\_policy\_ref  
anonymization\_policy\_ref  
key\_management\_policy\_ref

time\_authority\_policy\_ref  
offline\_clock\_trust\_policy\_ref

owner  
version  
status  
valid\_from  
valid\_until  
deprecated\_at  
replacement\_evidence\_type  
change\_reason

---

# **18\. EvidenceRecordDTO**

An individual evidence record is represented as EvidenceRecordDTO.

Canonical Reference: this object is implemented in code as `EvidenceDTO`
(`01_common_schema_dto/1_common_schema_dto.md` Section 15.1), not under the name
`EvidenceRecordDTO`. Section 15.1 is the field-level implementation contract — it
groups the fields below into nested DTOs (`TimeTrustDTO`, `SpatialValidityDTO`,
`DeviceHealthDTO`, `AttestationDTO`, `AIExtractionMetadataDTO`, `PrivacyDTO`,
`ConflictDTO`) rather than a single flat object; the field names and values are
unchanged.

## **18.1 EvidenceRecordDTO Fields**

Recommended fields:

evidence\_id  
evidence\_type  
evidence\_category

source\_id  
source\_type  
source\_trust\_level

target\_entity\_refs  
related\_event\_refs  
related\_state\_refs  
related\_action\_refs

payload  
payload\_hash

captured\_at  
received\_at  
validated\_at

time\_source\_type  
time\_authority\_ref  
source\_clock\_id  
clock\_sync\_status  
clock\_drift\_estimate\_ms  
clock\_drift\_calculation\_method  
capture\_receive\_delta\_ms  
max\_allowed\_time\_delta\_ms  
time\_trust\_level  
time\_validation\_status  
offline\_clock\_trust\_policy\_ref

geo\_location  
geo\_crs  
spatial\_context\_ref  
spatial\_bounds\_ref

device\_health\_snapshot  
device\_health\_snapshot\_version  
calibration\_status  
historical\_reliability\_score

freshness\_status  
validity\_status  
confidence\_score

ontology\_binding\_ref  
prov\_entity\_ref  
activity\_refs

hash  
signature  
trace\_id  
correlation\_id

is\_extracted\_evidence  
extraction\_method  
extracted\_from\_evidence\_id  
source\_document\_ref  
source\_location\_ref

model\_name  
model\_version  
prompt\_hash  
retrieval\_corpus\_ref  
retrieval\_snapshot\_id  
temperature  
extraction\_confidence

parser\_validation\_status  
human\_attestation\_status  
cross\_check\_status  
trust\_upgrade\_status

attestation\_type  
attestation\_evidence\_refs  
attestation\_signature  
attestation\_workflow\_id  
attestation\_hash  
attested\_by  
attested\_at

contains\_pii  
pii\_categories  
privacy\_lifecycle\_status  
retention\_policy\_ref  
retention\_expires\_at  
encryption\_key\_ref  
key\_management\_policy\_ref  
key\_destroyed\_at  
legal\_hold\_status  
redaction\_policy\_ref  
anonymization\_method  
access\_policy\_ref

conflict\_status  
conflict\_weight  
applied\_conflict\_weights  
resolution\_timestamp  
resolved\_by  
conflict\_resolution\_ref

created\_by  
created\_at  
supersedes\_evidence\_id  
is\_append\_only

---

# **19\. EvidenceBundleDTO**

An Evidence Bundle is represented as EvidenceBundleDTO.

## **19.1 EvidenceBundleDTO Fields**

Recommended fields:

bundle\_id  
bundle\_purpose  
evidence\_refs  
target\_entity\_refs  
supported\_event\_types  
supported\_state\_transitions  
supported\_action\_types  
minimum\_required\_evidence  
missing\_evidence  
conflict\_status  
confidence\_score  
freshness\_status  
validity\_status  
time\_trust\_status  
spatial\_validity\_status  
created\_at  
expires\_at  
created\_by  
trace\_id  
correlation\_id

---

# **20\. Policy Specification**

The Evidence Model operates together with multiple policy documents.

Each policy must have version, effective\_from, and superseded\_by.

## **20.1 Evidence Conflict Policy**

conflict\_policy\_id  
applicable\_evidence\_types  
conflict\_resolution\_strategy  
source\_trust\_weight  
device\_health\_weight  
spatial\_proximity\_weight  
freshness\_weight  
historical\_reliability\_weight  
majority\_vote\_required  
minimum\_sensor\_count  
spatial\_voting\_radius  
safety\_conservative\_default  
manual\_review\_threshold  
fail\_safe\_threshold  
effective\_from  
superseded\_by  
owner  
version  
status

## **20.2 Attested Extraction Policy**

extraction\_policy\_id  
allowed\_extraction\_methods  
requires\_source\_document\_ref  
requires\_source\_location\_ref  
requires\_parser\_validation  
requires\_human\_attestation  
requires\_cross\_check  
default\_source\_trust\_level  
allowed\_trust\_upgrade\_levels  
trust\_upgrade\_conditions  
effective\_from  
superseded\_by  
owner  
version  
status

## **20.3 Privacy and Append-only Policy**

privacy\_policy\_id  
applicable\_evidence\_types  
contains\_pii\_possible  
pii\_categories  
retention\_period  
masking\_required  
pseudonymization\_required  
anonymization\_required  
crypto\_shredding\_allowed  
legal\_hold\_blocks\_shredding  
audit\_shell\_retention\_required  
payload\_hash\_required  
payload\_destruction\_policy  
access\_policy\_ref  
effective\_from  
superseded\_by  
owner  
version  
status

## **20.4 Time Trust Policy**

time\_trust\_policy\_id  
applicable\_source\_types  
allowed\_time\_source\_types  
required\_time\_authority  
max\_allowed\_clock\_drift\_ms  
max\_allowed\_capture\_receive\_delta\_ms  
offline\_clock\_trust\_policy\_ref  
clock\_drift\_calculation\_method  
effective\_from  
superseded\_by  
owner  
version  
status

---

# **21\. Registry Operating Policy**

The Evidence Model Registry is not a simple evidence list.

The Evidence Model Registry is a governance-controlled registry that connects decision quality, safety validation, auditability, hallucination control, and privacy compliance.

## **21.1 Registry Status**

Evidence Types may have the following statuses:

DRAFT  
ACTIVE  
DEPRECATED  
RETIRED  
BLOCKED

## **21.2 Versioning**

Backward-compatible changes:

Add new allowed\_source\_type  
Enhance freshness\_ttl  
Enhance validity\_rule  
Add allowed target  
Add metadata  
Enhance conflict\_policy  
Enhance time\_trust\_policy  
Add privacy\_policy\_ref

Breaking changes:

Change evidence\_type name  
Relax minimum\_source\_trust\_level  
Remove requires\_signature  
Remove requires\_hash  
Remove payload\_hash\_required  
Change meaning of is\_primary\_evidence  
Change meaning of freshness\_ttl  
Change validity\_rule  
Remove conflict\_policy  
Change meaning of privacy lifecycle

As a rule, breaking changes must be separated into a new evidence\_type version or a new evidence\_type.

## **21.3 Approval Process**

Evidence Type changes must be approved by the owner and the domain steward.

High-risk evidence models require approval from the following authorities:

Ontology Steward  
Safety Owner  
Policy Owner  
Audit Owner  
Privacy / Compliance Owner  
Platform Architect  
Domain Owner

## **21.4 Deprecation Policy**

Evidence Types should not be deleted immediately.

Recommended process:

Change status to DEPRECATED  
Specify replacement\_evidence\_type  
Operate a dual-read / dual-write period  
Migrate downstream consumers  
Verify audit compatibility  
Verify privacy compatibility  
Change status to RETIRED  
Remove in a major version if necessary

## **21.5 Compatibility Rule**

Past evidence records must always remain interpretable.

Therefore, EvidenceRecordDTO, EvidenceBundleDTO, and AuditRecordDTO must reference not only evidence\_type, but also evidence\_type\_version.

Policies must also have effective\_from and superseded\_by.

---

# **22\. Core Scenarios**

## **22.1 Scenario 1: Gas Risk Detection → Evacuation ActionCandidate**

Situation:

GasSensor\_17 exceeded the critical threshold in Zone\_A.

Flow:

Raw Input:  
GasSensor\_17 value \= 87 ppm

Validated Evidence:  
SENSOR\_OBSERVATION\_EVIDENCE

Additional Evidence:  
GasSensor\_17 health \= OK  
Zone\_A worker occupancy \= 5  
Gas threshold policy \= 50 ppm  
Time trust \= HIGH\_TIME\_TRUST  
Spatial validity \= Zone\_A

EvidenceBundle:  
GasRiskEvidenceBundle\_001

Event:  
safety.gas.critical\_threshold\_exceeded

State:  
ZoneRiskState.CRITICAL

ActionCandidate:  
ACTION\_EMERGENCY\_EVACUATE\_ZONE

Safety Gate:  
requires verified sensor evidence \+ worker location evidence \+ policy decision evidence

## **22.2 Scenario 2: Robot Mission Disable Confirmation**

Situation:

FleetManager feedback arrived after a robot mission disable request.

Flow:

ExecutionRequest:  
disable Mission\_991

Feedback:  
FleetManager reports Mission\_991 disabled

Validated Evidence:  
EXTERNAL\_FEEDBACK\_EVIDENCE

State Transition:  
MissionStatus.DISABLE\_REQUESTED  
→ MissionStatus.DISABLED

Reconciliation:  
SUCCESS

Audit:  
Evidence linked to ApprovedAction and ExecutionRequest

## **22.3 Scenario 3: LLM Risk Summary**

Situation:

An LLM summarized that Zone\_A is dangerous.

Flow:

LLM Output:  
Zone\_A appears dangerous.

Classification:  
AI\_SUMMARY\_EVIDENCE

Required Grounding:  
GasSensor\_17 reading  
WorkerLocation\_Zone\_A  
VentilationState\_Zone\_A  
PermitStatus  
GasThresholdPolicy

Rule:  
AI summary cannot approve action.  
AI summary can support explanation only if original evidence\_refs are attached.

## **22.4 Scenario 4: Hot Work Permit AI Extraction \+ PII \+ Sensor Conflict**

Situation:

AI extracted the permit expiration time from a Hot Work Permit PDF.  
At the same time, WorkerLocationEvidence contains PII, and two gas sensor values conflict.

Flow:

Document:  
HotWorkPermit\_001.pdf  
source\_trust\_level \= VERIFIED\_DOCUMENT  
payload\_hash \= abc123

AI Extraction:  
permit\_expiry\_time \= 15:00  
source\_trust\_level \= AI\_DERIVED  
source\_location\_ref \= page 2, section 4

Attestation:  
RULE\_ENGINE validates time format.  
HUMAN\_STEWARD confirms extracted value.  
trust\_upgrade\_status \= TRUST\_UPGRADED\_BY\_HUMAN

WorkerLocationEvidence:  
contains\_pii \= true  
privacy\_lifecycle\_status \= PII\_PRESENT  
access\_policy\_ref \= WorkerLocationAccessPolicy

Sensor Conflict:  
GasSensor\_A \= 87 ppm, health \= OK  
GasSensor\_B \= 0 ppm, health \= WARNING

Conflict Resolution:  
strategy \= DEVICE\_HEALTH\_WEIGHTED\_SELECTION  
applied\_conflict\_weights recorded  
selected\_evidence \= GasSensor\_A

Decision:  
ZoneRiskState.CRITICAL  
ActionCandidate \= ACTION\_EMERGENCY\_EVACUATE\_ZONE

This scenario validates the following at the same time:

AI-extracted value trust upgrade  
Document evidence provenance  
PII evidence privacy lifecycle  
Sensor conflict resolution  
Safety Gate grounding  
Emergency action evidence bundle

---

# **23\. Initial Reference Evidence Model Set**

For the initial implementation, the following evidence models should be registered first.

## **23.1 Sensor / Telemetry**

SENSOR\_OBSERVATION\_EVIDENCE  
ROBOT\_TELEMETRY\_EVIDENCE  
WORKER\_LOCATION\_EVIDENCE  
EQUIPMENT\_TELEMETRY\_EVIDENCE  
DEVICE\_HEALTH\_EVIDENCE

## **23.2 External System**

EXTERNAL\_FEEDBACK\_EVIDENCE  
SYSTEM\_LOG\_EVIDENCE  
POLICY\_DECISION\_EVIDENCE

## **23.3 Human / Document**

HUMAN\_CONFIRMATION\_EVIDENCE  
DOCUMENT\_EVIDENCE  
DOCUMENT\_EXTRACTED\_EVIDENCE  
PERMIT\_EVIDENCE  
INSPECTION\_EVIDENCE

## **23.4 AI / Semantic**

AI\_SUMMARY\_EVIDENCE  
ATTESTED\_AI\_DERIVED\_EVIDENCE  
ONTOLOGY\_BINDING\_EVIDENCE  
INFERENCE\_EVIDENCE

## **23.5 Audit / Privacy**

AUDIT\_RECORD\_EVIDENCE  
PRIVACY\_LIFECYCLE\_EVIDENCE

---

# **24\. Separation Criteria for Appendix D: Evidence Type Catalog**

Detailed evidence type lists are not included in the main body.

The following items are managed in Appendix D:

sensor evidence catalog  
robot telemetry evidence catalog  
worker location evidence catalog  
device health evidence catalog  
external feedback evidence catalog  
human confirmation evidence catalog  
document evidence catalog  
permit evidence catalog  
inspection evidence catalog  
policy evidence catalog  
AI-derived evidence catalog  
privacy lifecycle evidence catalog  
audit evidence catalog

This prevents the Core document from becoming too long.

---

# **25\. Recommended File Structure**

## **25.1 Core Evidence Registry**

evidence\_registry/  
  \_\_init\_\_.py  
  core.py  
  evidence\_model\_spec.py  
  evidence\_record.py  
  evidence\_bundle.py  
  requirement\_spec.py  
  source\_trust.py  
  time\_trust\_policy.py  
  spatial\_validity\_policy.py  
  device\_health\_policy.py  
  freshness\_policy.py  
  validity\_policy.py  
  conflict\_policy.py  
  provenance\_policy.py  
  grounding\_policy.py  
  attested\_extraction\_policy.py  
  privacy\_policy.py  
  ai\_evidence\_boundary.py

## **25.2 Evidence Catalog**

evidence\_registry/catalog/  
  sensor\_evidence.py  
  robot\_telemetry\_evidence.py  
  worker\_location\_evidence.py  
  device\_health\_evidence.py  
  external\_feedback\_evidence.py  
  human\_confirmation\_evidence.py  
  document\_evidence.py  
  permit\_evidence.py  
  inspection\_evidence.py  
  ai\_derived\_evidence.py  
  privacy\_lifecycle\_evidence.py  
  audit\_evidence.py

## **25.3 Mapping Tables**

evidence\_registry/mappings/  
  event\_to\_evidence\_requirement.py  
  action\_to\_evidence\_requirement.py  
  state\_transition\_to\_evidence\_requirement.py  
  evidence\_to\_ontology\_binding.py  
  evidence\_to\_policy\_requirement.py  
  evidence\_conflict\_rules.py  
  evidence\_graph\_relations.py

---

# **26\. Recommended Implementation Order**

The implementation order should be as follows.

EvidenceCategory enum  
EvidenceType enum  
SourceTrustLevel enum  
TimeTrustLevel enum  
ClockSyncStatus enum  
ClockDriftCalculationMethod enum  
EvidenceValidityStatus enum  
EvidenceFreshnessStatus enum  
EvidenceConflictStatus enum  
PrivacyLifecycleStatus enum  
AttestationType enum  
TrustUpgradeStatus enum  
EvidenceModelSpecDTO  
EvidenceRecordDTO  
EvidenceBundleDTO  
EvidenceRequirementSpecDTO  
EvidenceRegistry  
EvidenceRequirementRegistry  
Source Trust Policy  
Time Trust Policy  
Spatial Validity Policy  
Device Health Policy  
Freshness Policy  
Validity Policy  
Conflict Policy  
Attested Extraction Policy  
Privacy-safe Append-only Policy  
Grounding Policy  
AI Evidence Boundary Policy  
Initial reference evidence type constants  
Event-to-Evidence Requirement Mapping  
Action-to-Evidence Requirement Mapping  
StateTransition-to-Evidence Requirement Mapping  
Evidence-to-Ontology Mapping  
Evidence Graph Relation Mapping  
Connection to WorldStateUpdateDTO  
Connection to ActionCandidateDTO  
Connection to ApprovedActionDTO  
Connection to ReconciliationResultDTO  
Connection to AuditRecordDTO

---

# **28\. Final Principle**

The Evidence Model is the evidence language of the platform.

Evidence is not simple data.  
Evidence is verifiable ground.

Evidence must have the following:

source trust  
time trust  
spatial validity  
device health context  
freshness  
validity  
provenance  
privacy lifecycle  
conflict policy  
audit chain

AI output can explain evidence.  
AI output cannot replace primary evidence.  
AI-extracted values can be trust-upgraded in a limited way through validation and attestation.

Conflict is not deleted.  
Conflict is explicitly recorded and resolved according to policy or connected to fail-safe.

Append-only applies to the audit shell.  
PII payload must be protectable through de-identification, masking, or encryption key destruction.  
Payload shredding must be blocked under legal hold.

High-frequency evidence does not inline all information every time.  
When needed, device health snapshot version or HealthEvent reference is used.

In the long term, Evidence should be managed not merely as DTOs but as an Evidence Graph.

The final principles are as follows:

Different inputs, one evidence discipline.  
Different clocks, one time trust policy.  
Different locations, one spatial validity model.  
Different devices, one health-aware evidence model.  
Different AI extractions, one attestation pipeline.  
Different conflicts, one resolution matrix.  
Different privacy risks, one protected audit shell.  
Different provenance paths, one evidence graph.  
Different evidence, one semantic backbone.

# **Ontology Centric Evidence Mode**

