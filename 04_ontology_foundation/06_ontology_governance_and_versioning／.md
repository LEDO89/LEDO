**Ontology Governance and Versioning**

## **1\. Purpose**

This document defines how ontology, classes, properties, axioms, SHACL shapes, SPARQL validation queries, policy references, external standard mappings, and Safety Gate snapshot schemas are changed and governed in the LEDO Industrial Ontology Foundation.

The LEDO ontology is not a static document created once and left unchanged. As industrial sites, sensors, robots, humanoids, policies, safety requirements, external systems, and standard mappings evolve, the ontology must also evolve.

However, uncontrolled ontology changes may cause the following problems.

Collapse of existing class meaning

Property meaning conflicts

SHACL validation failures

Broken SPARQL queries

Policy rule inconsistency

Safety Gate Snapshot generation failure

Contamination of Agent SLM training criteria

Audit trace inconsistency

External system mapping errors

Runtime rollback failure

Therefore, LEDO must version the ontology like code and apply governance review before changes are released.

The core principles are as follows.

Ontology evolves through governance.

Ontology changes must be versioned.

Meaning changes must be reviewed.

Runtime impact must be tested.

Safety-related changes must never be silent.

---

## **2\. Document Location**

This document belongs to the following location.

04\_ontology\_foundation/

  06\_ontology\_governance\_and\_versioning/

    ontology\_governance\_and\_versioning.md

This document is the final stabilizing mechanism of the ontology foundation.

Related documents include:

00\_ontology\_foundation\_report

01\_semantic\_web\_technology\_stack

02\_upper\_ontology\_and\_standards

03\_owl\_modeling\_principles

04\_reasoning\_and\_constraint\_model

05\_relationship\_and\_property\_design

03\_core\_specifications/

  01\_common\_schema\_dto

  05\_evidence\_model

  07\_decision\_approval\_matrix

  08\_policy\_governance\_model

  10\_audit\_observability\_model

06\_runtime\_validation/

  safety\_gate/

    safety\_gate\_validation\_rules.md

---

## **3\. Governance Scope**

In LEDO, governance does not apply only to ontology files.

The following are all governance targets.

Class

Object Property

Data Property

Annotation Property

Axiom

Restriction

Domain / Range

Disjointness

EquivalentClass

Use of sameAs

Property Chain

SHACL Shape

SPARQL Validation Query

Policy Reference

External Standard Mapping

Identifier Mapping Rule

Materialized Snapshot Schema

Safety Gate Runtime Map

Agent SLM Training Vocabulary

Agent LoRA Adapter Compatibility

Approved Release Package

Rollback Target

The core principle is as follows.

Ontology governance does not mean managing only OWL files.

Ontology governance is change management across meaning, validation, policy, execution, model training, audit, and rollback.

---

## **4\. Change Types**

Ontology changes are classified by impact level.

| Change Type | Description | Example | Default Impact |
| ----- | ----- | ----- | ----- |
| Editorial Change | Description change without meaning change | typo, label, comment update | Low |
| Vocabulary Change | Term, label, or SKOS change | adding altLabel | Low\~Medium |
| Additive Change | Addition without breaking existing meaning | adding class, adding property | Medium |
| Constraint Change | Change in validation condition | changing SHACL minCount | Medium\~High |
| Semantic Change | Change in existing meaning | domain/range change, hierarchy change | High |
| Breaking Change | Change that breaks existing data/query/policy | property deletion, disjointness addition | Very High |
| Safety-Critical Change | Impact on Safety Gate, policy, or execution | action\_permission\_map change | Critical |
| Identity Change | Impact on canonical identity | sameAs or external mapping change | Critical |
| Model-Compatibility Change | Impact on Agent SLM/LoRA training criteria | TBox structure change, action meaning change | High\~Critical |

Every change must declare its type.

change\_type:

  editorial

  vocabulary

  additive

  constraint

  semantic

  breaking

  safety\_critical

  identity

  model\_compatibility

---

## **5\. Versioning Principles**

The LEDO ontology follows semantic versioning.

MAJOR.MINOR.PATCH

Example:

ontology-v1.4.2

### **5.1 PATCH**

A PATCH change does not change meaning.

typo fix

comment update

label improvement

documentation link update

Example:

v1.4.2 → v1.4.3

### **5.2 MINOR**

A MINOR change is backward-compatible.

adding a new class

adding a new property

adding a new optional property

adding a new annotation

adding a new SKOS altLabel

adding a new SHACL shape

Example:

v1.4.2 → v1.5.0

### **5.3 MAJOR**

A MAJOR change breaks existing meaning or compatibility.

class hierarchy change

domain/range narrowing

property deletion

disjointness addition

sameAs policy change

Safety Gate snapshot schema change

fundamental TBox structure change

Agent SLM / LoRA adapter compatibility breakage

Example:

v1.4.2 → v2.0.0

The core principles are as follows.

If meaning breaks, it is MAJOR.

If validation criteria change, it is at least MINOR.

If the Safety Gate structure changes, explicit migration is required.

If the TBox structure changes significantly, Agent SLM / LoRA compatibility must be reviewed.

---

## **6\. Version Impact Decision Table**

The following table is used to decide whether a change is PATCH, MINOR, MAJOR, or Safety-Critical.

| Change | Version Impact | Migration Required | Governance Strength |
| ----- | ----- | ----- | ----- |
| label/comment/typo update | PATCH | No | Low |
| SKOS altLabel addition | PATCH or MINOR | No | Low |
| class addition | MINOR | Usually No | Medium |
| optional property addition | MINOR | No | Medium |
| new SHACL shape addition | MINOR | Usually No | Medium |
| required SHACL field addition | MINOR or MAJOR | Yes | High |
| property rename | MAJOR | Yes | High |
| domain/range narrowing | MAJOR | Yes | High |
| class hierarchy change | MAJOR | Possible | High |
| disjointness addition | MAJOR | Possible | High |
| property deletion | MAJOR | Yes | High |
| sameAs / identity mapping change | MAJOR | Yes | Critical |
| Safety Gate snapshot schema change | MAJOR | Yes | Critical |
| action\_permission\_map generation logic change | MAJOR / Safety-Critical | Yes | Critical |
| risk\_action\_matrix generation logic change | MAJOR / Safety-Critical | Yes | Critical |
| fundamental TBox structure change | MAJOR / Model-Critical | Yes | Critical |
| Agent SLM vocabulary or LoRA compatibility breakage | MAJOR / Model-Critical | Yes | Critical |

Decision rules:

If existing meaning is not broken, it is PATCH or MINOR.

If existing data, queries, policies, or snapshots are broken, it is MAJOR.

If Safety Gate decisions may change, it is Safety-Critical.

If identity interpretation changes, it is Critical.

If the Agent SLM semantic space or vocabulary breaks, it is Model-Critical.

---

## **7\. Module Versioning**

LEDO does not version only one entire ontology artifact.  
Each module must have its own independent version.

ontology\_core\_version

property\_registry\_version

class\_registry\_version

shacl\_shape\_version

sparql\_query\_version

policy\_reference\_version

mapping\_registry\_version

snapshot\_schema\_version

agent\_vocabulary\_version

agent\_adapter\_registry\_version

approved\_release\_package\_version

Example:

ontology\_version: "ontology-v1.5.0"

property\_registry\_version: "property-registry-v1.2.0"

class\_registry\_version: "class-registry-v1.1.0"

shacl\_shape\_version: "shacl-v1.3.1"

sparql\_query\_version: "sparql-validation-v0.8.0"

policy\_reference\_version: "policy-ref-v0.9.8"

mapping\_registry\_version: "mapping-v0.6.2"

snapshot\_schema\_version: "snapshot-schema-v0.4.0"

agent\_vocabulary\_version: "agent-vocab-v0.3.5"

agent\_adapter\_registry\_version: "adapter-registry-v0.2.0"

The Safety Gate Runtime Snapshot must record these versions together.

SafetyGateSnapshot

  ontology\_version

  policy\_version

  shacl\_shape\_version

  inference\_version

  snapshot\_schema\_version

  checksum

The core principle is as follows.

A Snapshot must know which ontology, policy, and shape versions produced it.

---

## **8\. Change Request Procedure**

Ontology changes begin with a Change Request.

The entire flow is managed in seven stages.

1\. Create Change Request

2\. Impact Classification

3\. Compatibility & Migration Review

4\. Test and Regression

5\. Governance Approval

6\. Versioned Release

7\. Audit and Rollback Registration

Responsibilities by stage:

| Stage | Purpose | Output |
| ----- | ----- | ----- |
| Create Change Request | Record target and reason for change | change request |
| Impact Classification | Determine change type and version impact | impact report |
| Compatibility & Migration Review | Review impact on data/query/policy/snapshot/SLM | migration requirement |
| Test and Regression | Test reasoner, SHACL, SPARQL, policy, snapshot, SLM compatibility | test result |
| Governance Approval | Decide whether to approve the change | approval record |
| Versioned Release | Bump version and create release package | release package |
| Audit and Rollback Registration | Record change history and rollback target | audit record / rollback plan |

A Change Request must include:

change\_id

change\_type

target\_module

target\_iri

current\_version

proposed\_version

change\_description

reason

expected\_impact

affected\_shapes

affected\_queries

affected\_policies

affected\_snapshots

affected\_agent\_vocabularies

affected\_adapters

migration\_required

rollback\_plan

review\_status

approved\_by

created\_at

The core principle is as follows.

An ontology change is not merely a document update; it may change runtime behavior and model behavior.

---

## **9\. Governance Review Criteria**

During review, the following questions must be answered.

Does it break the meaning of an existing class?

Does it change the meaning of an existing property?

Does domain/range inference change?

Does the SHACL validation result change?

Does the SPARQL query result change?

Does the Policy decision result change?

Does the Safety Gate Snapshot result change?

Does it affect Agent SLM training vocabulary?

Are existing LoRA adapters still semantically compatible?

Is ABox migration required?

Does external standard mapping break?

Does audit trace interpretation change?

Does a rollback target exist?

Safety-critical changes require stronger review.

Does it affect the Safety Gate hot path?

Does action\_permission\_map change?

Does risk\_action\_matrix change?

Does zone\_restriction\_map change?

Does the generation condition for evidence\_freshness\_map change?

Does approval\_state\_map change?

Is fallback possible if snapshot hot-swap fails?

Detailed Safety Gate runtime principles are handled in `safety_gate_validation_rules.md`.  
This document determines whether a change affects Safety Gate snapshots, schemas, materialized maps, or rollback packages.

The core principle is as follows.

Safety-related semantic changes must not be released silently.

---

## **10\. Compatibility Policy**

LEDO classifies changes into three compatibility categories.

### **10.1 Backward Compatible**

Existing data, queries, policies, and snapshots are not broken.

Examples:

adding a new subclass

adding a new annotation

adding a new optional property

adding a new SKOS altLabel

### **10.2 Backward Compatible with Migration**

The existing structure remains compatible, but migration is required.

Examples:

renaming a property

adding a new required field

splitting an existing class into more specific subclasses

### **10.3 Breaking Change**

The existing structure is directly broken.

Examples:

class deletion

property deletion

domain/range narrowing

disjointness addition

snapshot schema change

sameAs policy change

fundamental TBox structure change

A Breaking Change must always increase the MAJOR version.

---

## **11\. Deprecation Policy**

Deletion is not immediate.  
The target is first moved into a deprecated state.

active

→ deprecated

→ migration\_required

→ removed

A deprecated property or class must include:

deprecated\_since

removal\_target\_version

replacement\_iri

migration\_note

owner\_module

Example:

ot:connectedTo

  status: deprecated

  replacement: ot:affects / ot:supportedBy / ot:locatedIn

  removal\_target\_version: ontology-v2.0.0

The core principle is as follows.

Migration comes before deletion.

---

## **12\. Migration Policy**

If an ontology change affects existing ABox, SHACL, SPARQL, Policy, Snapshot, or Agent SLM, a migration plan is required.

Migration is not merely an ontology file change.

Ontology migration

\= ontology \+ ABox \+ SHACL \+ SPARQL \+ Policy \+ Snapshot Schema \+ Agent Vocabulary \+ Audit interpretation change

A migration plan includes:

source\_version

target\_version

affected\_classes

affected\_properties

affected\_individuals

affected\_agent\_vocabularies

affected\_adapters

mapping\_rule

data\_migration\_script

shacl\_update\_required

sparql\_update\_required

policy\_update\_required

snapshot\_regeneration\_required

adapter\_compatibility\_required

rollback\_plan

The migration sequence is as follows.

1\. Define Migration Scope

2\. Freeze Source / Target Versions

3\. Write Mapping Rules

4\. Perform Sample ABox Migration

5\. Update Shape / Query / Policy

6\. Run Snapshot Regeneration Test

7\. Review Agent SLM / Adapter Compatibility

8\. Run Regression Test

9\. Register Rollback Target

10\. Controlled Release

Meaning of each stage:

| Stage | Description |
| ----- | ----- |
| Define Migration Scope | Determine which classes, properties, ABox, shapes, queries, policies, snapshots, and agent vocabularies are affected |
| Freeze Source / Target Versions | Explicitly declare the versions before and after migration |
| Write Mapping Rules | Define rules to transform old structures into new ones |
| Perform Sample ABox Migration | Validate with sample data before full migration |
| Update Shape / Query / Policy | Update SHACL, SPARQL, and policy references |
| Run Snapshot Regeneration Test | Confirm that Safety Gate snapshots can be generated |
| Review Agent SLM / Adapter Compatibility | Determine vocabulary and LoRA adapter compatibility |
| Run Regression Test | Compare previous competency questions, query, policy, and snapshot results |
| Register Rollback Target | Specify approved release package to return to on failure |
| Controlled Release | Release in a limited scope before expansion |

The core principle is as follows.

Ontology migration cannot be separated from data migration and model compatibility migration.

---

## **13\. Test and Regression**

Ontology changes must pass testing before release.

Mandatory tests include:

TBox consistency test

Unsatisfiable class test

Sample ABox reasoning test

SHACL regression test

SPARQL query regression test

Policy impact test

Safety Gate Snapshot generation test

Materialized relation map test

Competency Question test

Audit trace consistency test

Agent vocabulary compatibility test

Adapter compatibility check

Examples of competency questions:

Is this ActionCandidate supported by an EvidenceBundle?

Does this GasRisk affect Zone\_A?

Can this Action mitigate the Risk?

Does this Agent have the capability to perform this Task?

Can this ExecutionRequest be delivered to an external system?

Which ontology\_version and snapshot\_version were used for this decision?

The core principle is as follows.

Ontology changes cannot be released without tests.

---

## **14\. Release Package**

An ontology release is distributed as a release package, not as a single file.

A release package includes:

ontology files

class registry

property registry

SHACL shapes

SPARQL validation queries

policy references

mapping registry

snapshot schema

agent vocabulary manifest

adapter compatibility report

migration notes

rollback plan

release notes

test results

checksum

Recommended folder structure:

release/

  ontology-v1.5.0/

    manifest.yaml

    ontology/

      core.ttl

      core.owl

      domain\_modules/

        safety.ttl

        robot.ttl

        evidence.ttl

        execution.ttl

    registry/

      class\_registry.yaml

      property\_registry.yaml

      mapping\_registry.yaml

    validation/

      shacl\_shapes.ttl

      sparql\_validation\_queries/

        evidence\_support.ask.rq

        risk\_affects\_zone.ask.rq

        action\_target\_compatibility.ask.rq

    policy/

      policy\_references.yaml

    snapshot/

      snapshot\_schema.yaml

      materialization\_manifest.yaml

      binary\_snapshot\_map.bin

      binary\_snapshot\_checksum.sha256

    agent\_slm/

      agent\_vocabulary\_manifest.yaml

      adapter\_compatibility\_report.yaml

    migration/

      migration\_notes.md

      migration\_plan.yaml

      rollback\_plan.yaml

    tests/

      test\_results.json

      competency\_question\_results.json

      shacl\_regression\_results.json

      sparql\_regression\_results.json

      snapshot\_generation\_results.json

      adapter\_compatibility\_results.json

    checksum.sha256

    release\_notes.md

`manifest.yaml` records the versions of all release package components.

Example:

release\_version: ontology-v1.5.0

ontology\_version: ontology-v1.5.0

class\_registry\_version: class-registry-v1.1.0

property\_registry\_version: property-registry-v1.2.0

shacl\_shape\_version: shacl-v1.3.1

sparql\_query\_version: sparql-validation-v0.8.0

policy\_reference\_version: policy-ref-v0.9.8

snapshot\_schema\_version: snapshot-schema-v0.4.0

agent\_vocabulary\_version: agent-vocab-v0.3.5

checksum: sha256:...

---

## **15\. Rollback Policy**

If a new ontology release causes problems, rollback must be possible.

Rollback conditions include:

Safety Snapshot generation failure

Increase in SHACL regression failures

Increase in SPARQL query failures

Policy decision mismatch

Critical class inference error

External mapping error

Drop in Agent SLM output quality

Snapshot hot-swap failure

Active snapshot checksum mismatch

Rollback targets:

| Rollback Target | Description |
| ----- | ----- |
| ontology\_version | class/property/axiom definitions |
| class\_registry\_version | class registry |
| property\_registry\_version | property registry |
| shacl\_shape\_version | validation shapes |
| sparql\_query\_version | graph validation queries |
| policy\_reference\_version | policy linkage |
| mapping\_registry\_version | external standard / ID mapping |
| snapshot\_schema\_version | Safety Gate snapshot schema |
| binary\_snapshot\_map\_version | compact runtime map read by C++ Safety Gate |
| agent\_vocabulary\_version | Agent SLM vocabulary criteria |
| adapter\_registry\_version | Agent LoRA adapter compatibility criteria |

The core principle is as follows.

Rollback is not just ontology file rollback.

Rollback is simultaneous recovery of meaning, validation, policy, mapping, snapshot, audit, and agent vocabulary criteria.

---

## **15.1 Shared Memory Snapshot Hot-Swap Failure Recovery**

A Safety Gate Runtime Snapshot is published to the active snapshot only after a newly generated shadow snapshot is validated.

Normal flow:

Create Shadow Snapshot

→ Verify checksum

→ Verify version compatibility

→ Verify schema compatibility

→ Verify materialized maps

→ Atomic publish

→ Replace Active Snapshot

Failure principles:

If shadow snapshot validation fails, do not replace the active snapshot.

If the existing active snapshot is valid, keep it.

Stop publishing the new snapshot, but do not immediately stop the Safety Gate kernel itself.

If the existing active snapshot is also invalid, enter fail-closed mode.

Recovery flow:

1\. Detect shadow snapshot load failure

2\. Block atomic publish

3\. Check existing active snapshot checksum / valid\_until

4\. If active snapshot is valid, keep last-known-good state

5\. If active snapshot is also invalid, enter fail-closed mode

6\. Load the previous approved binary snapshot map from the persistent approved release package

7\. Verify checksum / version / schema

8\. Restore it into memory-resident standby buffer or shared memory buffer

9\. Re-publish active pointer after verification

10\. Create rollback audit record

Important hardware and memory principles:

Huge Pages are RAM regions, not non-volatile storage.

The non-volatile approved release package is stored on disk / NVMe / artifact store.

For faster recovery, the previous approved binary snapshot map may be preloaded into a memory-resident standby buffer.

The C++ Safety Gate must never publish an unverified snapshot as active.

If no verified active snapshot exists, do not allow; enter fail-closed mode.

The core principle is as follows.

Hot-swap failure must not lead to unsafe publish.

Snapshot rollback must recover to the last-known-good approved binary map.

---

## **16\. External Standard Mapping Governance**

LEDO does not blindly copy external standards.  
External standards are mapped.

Examples include:

BFO

IFC

SOSA / SSN

SAREF

PROV-O

QUDT

GeoSPARQL

OWL-Time

ISA / IEC 62443

IEC 61508 related safety concepts

When mapping changes, check the following.

Has the external standard version changed?

Does the mapping to LEDO canonical classes break?

Does the connection between external identifiers and canonical identity change?

Are SHACL shapes affected?

Are SPARQL queries affected?

Is Safety Snapshot materialization affected?

The core principle is as follows.

Standards are mapped, not blindly copied.

---

## **17\. Agent SLM Impact Management**

Ontology changes may affect Agent SLMs.

Detailed SLM training loops are handled in the Agent-Specific SLM document.  
This document determines whether ontology changes require updates to agent vocabulary, training dataset versions, or LoRA adapter compatibility.

The following changes require Agent SLM impact review.

class name change

property name change

SKOS label change

Action type change

Evidence model change

Safety Gate boundary change

ExecutionRequest meaning change

TBox class hierarchy change

Property semantics change

Required actions include:

Update agent\_vocabulary\_version

Review SFT pairs

Update residual error test fixtures

Update Developer SLM prompt criteria

Update Synthetic Data Factory templates

Review LoRA adapter compatibility

The core principle is as follows.

An ontology change may also be a model training criteria change.

---

## **17.1 MAJOR TBox Change and Agent Adapter Compatibility**

A MAJOR version change that fundamentally alters the TBox structure may break the semantic space of existing Agent SLMs and LoRA adapters.

The following changes require full adapter compatibility review.

Reconstruction of upper class hierarchy

Core domain/range meaning change

ActionCandidate / ExecutionRequest meaning change

Evidence / Policy / Safety boundary change

Major property semantics change

Core SKOS vocabulary change

Meaning change in Safety Gate materialized maps

When a MAJOR TBox change is confirmed, follow this procedure.

1\. Exclude affected Agent LoRA adapters from production promotion.

2\. Move those adapters to incompatible or rejected status in the Adapter Registry.

3\. Update agent\_vocabulary\_version.

4\. Review tokenizer / domain token impact.

5\. Perform Mean Initialization or Embedding Adaptation if needed.

6\. Rebuild the DAPT dataset using the new ontology version.

7\. Rewrite SFT pairs and residual error fixtures according to the new meaning boundaries.

8\. Retrain agent-specific LoRA adapters.

9\. Re-run fixed eval / holdout eval / critical violation tests.

10\. Promote only passing adapters through candidate → validated → canary → approved.

Adapter state transition:

approved

→ incompatible

→ rejected\_for\_current\_ontology

→ retraining\_required

→ candidate

→ validated

→ canary

→ approved

The core principles are as follows.

A MAJOR ontology change can invalidate Agent SLM behavior.

Old LoRA adapters must not be reused without compatibility review.

Model retraining starts from updated vocabulary and updated meaning boundaries.

---

## **18\. Audit and Trace**

All important ontology changes are subject to audit.

AuditRecord must record:

change\_id

old\_version

new\_version

changed\_by

approved\_by

review\_result

test\_result

migration\_result

release\_time

rollback\_target

reason

affected\_adapters

affected\_snapshot\_schema

Runtime decisions must also record ontology versions.

DecisionCase\_01

  usedOntologyVersion: ontology-v1.5.0

  usedPolicyVersion: policy-v0.9.8

  usedSnapshotVersion: sgs-2026-06-25-0007

The core principle is as follows.

To understand why a decision was made later, the ontology version used at the time must be known.

---

## **19\. Anti-Patterns**

| Anti-pattern | Problem | Alternative |
| ----- | ----- | ----- |
| Editing ontology without versioning | Decision trace becomes impossible | Apply semantic versioning |
| Adding classes/properties without registry | Meaning conflicts occur | Use registry and governance review |
| Releasing breaking changes as MINOR | Existing system may collapse | Use MAJOR version bump |
| Deleting without deprecation period | Existing queries/data break | Use deprecation period |
| Skipping SHACL / SPARQL / Policy impact review | Validation and policy results may change suddenly | Require impact review |
| Skipping Safety Gate snapshot impact review | Runtime decision errors occur | Run snapshot generation test |
| Releasing without migration plan | Existing ABox/query/policy may be damaged | Require migration plan |
| Releasing without rollback plan | Recovery becomes impossible | Define rollback target |
| Reusing old LoRA adapters after MAJOR TBox change | Agent behavior becomes inconsistent | Run adapter compatibility review / retraining |
| Publishing failed hot-swap snapshot as active | Unsafe runtime state occurs | Verify checksum \+ rollback to last-known-good |

---

## **20\. Final Operating Principles**

Ontology is a versioned artifact.

Classes and properties are managed through registries.

Meaning changes go through governance review.

Breaking changes require MAJOR version bumps.

Do not delete without a deprecation period.

Review SHACL, SPARQL, Policy, and Snapshot impact together.

Safety-critical changes must not be released silently.

External standards are mapped, not copied.

Ontology changes may affect Agent SLM training criteria.

MAJOR TBox changes may invalidate existing LoRA adapter compatibility.

Runtime snapshot hot-swap failure must not result in unsafe publish.

Runtime decisions must record usedOntologyVersion.

---

## **21\. Final Conclusion**

The core of LEDO Ontology Governance and Versioning is not to prevent ontology from changing.

The core is to let ontology evolve safely.

The final structure is as follows.

Change Request

→ Impact Classification

→ Compatibility & Migration Review

→ Test and Regression

→ Governance Approval

→ Versioned Release

→ Audit and Rollback Registration

The final principles are as follows.

Ontology evolves.

Governance controls meaning change.

Versioning protects compatibility.

Testing protects runtime behavior.

Adapter compatibility protects model behavior.

Rollback protects operational continuity.

Audit protects accountability.

# **Ontology Governance and Versioning**

## **1\. 목적**

이 문서는 LEDO Industrial Ontology Foundation에서 ontology, class, property, axiom, SHACL shape, SPARQL validation query, policy reference, external standard mapping, Safety Gate snapshot schema를 어떻게 변경하고 관리할 것인지 정의한다.

LEDO의 ontology는 한 번 만들고 끝나는 정적 문서가 아니다. 산업 현장, 센서, 로봇, 휴머노이드, 정책, 안전 기준, 외부 시스템, 표준 mapping이 변하면 ontology도 진화해야 한다.

하지만 ontology가 무질서하게 바뀌면 다음 문제가 발생한다.

기존 class 의미 붕괴  
property 의미 충돌  
SHACL validation 실패  
SPARQL query 깨짐  
Policy rule 불일치  
Safety Gate Snapshot 생성 실패  
Agent SLM 학습 기준 오염  
Audit trace 불일치  
External system mapping 오류  
Runtime rollback 불가능

따라서 LEDO는 ontology를 코드처럼 versioning하고, governance review를 거쳐 변경해야 한다.

핵심 원칙은 다음과 같다.

Ontology evolves through governance.  
Ontology changes must be versioned.  
Meaning changes must be reviewed.  
Runtime impact must be tested.  
Safety-related changes must never be silent.

---

## **2\. 문서 위치**

이 문서는 다음 위치에 속한다.

04\_ontology\_foundation/  
  06\_ontology\_governance\_and\_versioning/  
    ontology\_governance\_and\_versioning.md

이 문서는 ontology foundation의 마지막 고정 장치다.

연결 문서는 다음과 같다.

00\_ontology\_foundation\_report  
01\_semantic\_web\_technology\_stack  
02\_upper\_ontology\_and\_standards  
03\_owl\_modeling\_principles  
04\_reasoning\_and\_constraint\_model  
05\_relationship\_and\_property\_design

03\_core\_specifications/  
  01\_common\_schema\_dto  
  05\_evidence\_model  
  07\_decision\_approval\_matrix  
  08\_policy\_governance\_model  
  10\_audit\_observability\_model

06\_runtime\_validation/  
  safety\_gate/  
    safety\_gate\_validation\_rules.md

---

## **3\. Governance 대상**

LEDO에서 governance 대상은 ontology 파일만이 아니다.

다음 전체가 governance 대상이다.

Class  
Object Property  
Data Property  
Annotation Property  
Axiom  
Restriction  
Domain / Range  
Disjointness  
EquivalentClass  
sameAs 사용  
Property Chain  
SHACL Shape  
SPARQL Validation Query  
Policy Reference  
External Standard Mapping  
Identifier Mapping Rule  
Materialized Snapshot Schema  
Safety Gate Runtime Map  
Agent SLM Training Vocabulary  
Agent LoRA Adapter Compatibility  
Approved Release Package  
Rollback Target

핵심 원칙은 다음과 같다.

Ontology governance는 OWL 파일 관리만 의미하지 않는다.  
Ontology governance는 의미, 검증, 정책, 실행, 학습, 감사, rollback까지 연결된 변경 관리다.

---

## **4\. 변경 유형**

Ontology 변경은 영향도에 따라 분류한다.

| 변경 유형 | 설명 | 예시 | 기본 영향도 |
| ----- | ----- | ----- | ----- |
| Editorial Change | 의미 변화 없는 설명 수정 | typo, label, comment 수정 | 낮음 |
| Vocabulary Change | 용어, label, SKOS 변경 | altLabel 추가 | 낮음\~중간 |
| Additive Change | 기존 의미를 깨지 않는 추가 | class 추가, property 추가 | 중간 |
| Constraint Change | validation 조건 변경 | SHACL minCount 변경 | 중간\~높음 |
| Semantic Change | 기존 의미 변경 | domain/range 변경, hierarchy 변경 | 높음 |
| Breaking Change | 기존 data/query/policy를 깨는 변경 | property 삭제, disjointness 추가 | 매우 높음 |
| Safety-Critical Change | Safety Gate, policy, execution에 영향 | action\_permission\_map 변경 | 최고 |
| Identity Change | canonical identity에 영향 | sameAs, external mapping 변경 | 최고 |
| Model-Compatibility Change | Agent SLM/LoRA 학습 기준에 영향 | TBox 구조 변경, action 의미 변경 | 높음\~최고 |

변경은 반드시 유형을 표시해야 한다.

change\_type:  
  editorial  
  vocabulary  
  additive  
  constraint  
  semantic  
  breaking  
  safety\_critical  
  identity  
  model\_compatibility

---

## **5\. Versioning 원칙**

LEDO ontology는 semantic versioning을 따른다.

MAJOR.MINOR.PATCH

예시:

ontology-v1.4.2

### **5.1 PATCH**

의미 변화가 없는 수정이다.

typo 수정  
comment 수정  
label 보완  
문서 링크 수정

예시:

v1.4.2 → v1.4.3

### **5.2 MINOR**

하위 호환 가능한 추가다.

새 class 추가  
새 property 추가  
새 optional property 추가  
새 annotation 추가  
새 SKOS altLabel 추가  
새 SHACL shape 추가

예시:

v1.4.2 → v1.5.0

### **5.3 MAJOR**

기존 의미나 호환성을 깨는 변경이다.

class hierarchy 변경  
domain/range 축소  
property 삭제  
disjointness 추가  
sameAs 정책 변경  
Safety Gate snapshot schema 변경  
TBox 구조의 근본적 변경  
Agent SLM / LoRA adapter 호환성 파손

예시:

v1.4.2 → v2.0.0

핵심 원칙은 다음과 같다.

의미가 깨지면 MAJOR다.  
검증 기준이 바뀌면 최소 MINOR 이상이다.  
Safety Gate 구조가 바뀌면 반드시 명시적 migration이 필요하다.  
TBox 구조가 크게 바뀌면 Agent SLM / LoRA 호환성 검토가 필요하다.

---

## **6\. Version Impact Decision Table**

변경이 PATCH, MINOR, MAJOR, Safety-Critical 중 어디에 해당하는지 판단하기 위해 다음 기준을 사용한다.

| 변경 내용 | Version Impact | Migration 필요 | Governance 강도 |
| ----- | ----- | ----- | ----- |
| label/comment/typo 수정 | PATCH | No | Low |
| SKOS altLabel 추가 | PATCH 또는 MINOR | No | Low |
| class 추가 | MINOR | Usually No | Medium |
| optional property 추가 | MINOR | No | Medium |
| 새 SHACL shape 추가 | MINOR | Usually No | Medium |
| required SHACL field 추가 | MINOR 또는 MAJOR | Yes | High |
| property 이름 변경 | MAJOR | Yes | High |
| domain/range 축소 | MAJOR | Yes | High |
| class hierarchy 변경 | MAJOR | Possible | High |
| disjointness 추가 | MAJOR | Possible | High |
| property 삭제 | MAJOR | Yes | High |
| sameAs / identity mapping 변경 | MAJOR | Yes | Critical |
| Safety Gate snapshot schema 변경 | MAJOR | Yes | Critical |
| action\_permission\_map 생성 로직 변경 | MAJOR / Safety-Critical | Yes | Critical |
| risk\_action\_matrix 생성 로직 변경 | MAJOR / Safety-Critical | Yes | Critical |
| TBox 구조의 근본적 변경 | MAJOR / Model-Critical | Yes | Critical |
| Agent SLM vocabulary 또는 LoRA 호환성 파손 | MAJOR / Model-Critical | Yes | Critical |

판단 규칙은 다음과 같다.

기존 의미를 깨지 않으면 PATCH 또는 MINOR다.  
기존 data, query, policy, snapshot을 깨면 MAJOR다.  
Safety Gate 판단 결과가 달라질 수 있으면 Safety-Critical이다.  
Identity 해석이 바뀌면 Critical이다.  
Agent SLM의 의미 공간과 vocabulary가 깨지면 Model-Critical이다.

---

## **7\. Module Versioning**

LEDO는 전체 ontology 하나만 versioning하지 않는다.  
각 module도 독립 version을 가져야 한다.

ontology\_core\_version  
property\_registry\_version  
class\_registry\_version  
shacl\_shape\_version  
sparql\_query\_version  
policy\_reference\_version  
mapping\_registry\_version  
snapshot\_schema\_version  
agent\_vocabulary\_version  
agent\_adapter\_registry\_version  
approved\_release\_package\_version

예시:

ontology\_version: "ontology-v1.5.0"  
property\_registry\_version: "property-registry-v1.2.0"  
class\_registry\_version: "class-registry-v1.1.0"  
shacl\_shape\_version: "shacl-v1.3.1"  
sparql\_query\_version: "sparql-validation-v0.8.0"  
policy\_reference\_version: "policy-ref-v0.9.8"  
mapping\_registry\_version: "mapping-v0.6.2"  
snapshot\_schema\_version: "snapshot-schema-v0.4.0"  
agent\_vocabulary\_version: "agent-vocab-v0.3.5"  
agent\_adapter\_registry\_version: "adapter-registry-v0.2.0"

Safety Gate Runtime Snapshot은 이 version들을 함께 기록해야 한다.

SafetyGateSnapshot  
  ontology\_version  
  policy\_version  
  shacl\_shape\_version  
  inference\_version  
  snapshot\_schema\_version  
  checksum

핵심 원칙은 다음과 같다.

Snapshot은 어떤 ontology와 policy와 shape로 생성되었는지 반드시 알아야 한다.

---

## **8\. Change Request 절차**

Ontology 변경은 Change Request로 시작한다.

전체 흐름은 7단계로 관리한다.

1\. Change Request 생성  
2\. Impact Classification  
3\. Compatibility & Migration Review  
4\. Test and Regression  
5\. Governance Approval  
6\. Versioned Release  
7\. Audit and Rollback Registration

각 단계의 책임은 다음과 같다.

| 단계 | 목적 | 산출물 |
| ----- | ----- | ----- |
| Change Request 생성 | 변경 대상과 이유 기록 | change request |
| Impact Classification | 변경 유형과 version impact 판단 | impact report |
| Compatibility & Migration Review | 기존 data/query/policy/snapshot/SLM 영향 검토 | migration requirement |
| Test and Regression | reasoner, SHACL, SPARQL, policy, snapshot, SLM compatibility 테스트 | test result |
| Governance Approval | 변경 승인 여부 결정 | approval record |
| Versioned Release | version bump 후 release package 생성 | release package |
| Audit and Rollback Registration | 변경 이력과 rollback target 기록 | audit record / rollback plan |

Change Request는 다음 정보를 포함해야 한다.

change\_id  
change\_type  
target\_module  
target\_iri  
current\_version  
proposed\_version  
change\_description  
reason  
expected\_impact  
affected\_shapes  
affected\_queries  
affected\_policies  
affected\_snapshots  
affected\_agent\_vocabularies  
affected\_adapters  
migration\_required  
rollback\_plan  
review\_status  
approved\_by  
created\_at

핵심 원칙은 다음과 같다.

Ontology 변경은 문서 수정이 아니라 runtime behavior와 model behavior 변경 가능성이다.

---

## **9\. Governance Review 기준**

변경 검토 시 다음 질문에 답해야 한다.

기존 class 의미를 깨는가?  
기존 property 의미를 바꾸는가?  
domain/range inference가 달라지는가?  
SHACL validation 결과가 달라지는가?  
SPARQL query 결과가 달라지는가?  
Policy decision 결과가 달라지는가?  
Safety Gate Snapshot 결과가 달라지는가?  
Agent SLM training vocabulary에 영향이 있는가?  
기존 LoRA adapter가 여전히 의미적으로 호환되는가?  
ABox migration이 필요한가?  
외부 표준 mapping이 깨지는가?  
Audit trace 해석이 바뀌는가?  
Rollback target이 존재하는가?

Safety-critical 변경은 더 강한 검토를 거친다.

Safety Gate hot path에 영향이 있는가?  
action\_permission\_map이 바뀌는가?  
risk\_action\_matrix가 바뀌는가?  
zone\_restriction\_map이 바뀌는가?  
evidence\_freshness\_map 생성 조건이 바뀌는가?  
approval\_state\_map이 바뀌는가?  
snapshot hot-swap 실패 시 fallback이 가능한가?

상세 Safety Gate runtime 원칙은 `safety_gate_validation_rules.md`에서 다룬다.  
이 문서에서는 변경이 Safety Gate snapshot, schema, materialized map, rollback package에 영향을 주는지 판단한다.

핵심 원칙은 다음과 같다.

Safety-related semantic change는 조용히 배포하지 않는다.

---

## **10\. Compatibility Policy**

LEDO는 변경을 세 종류로 본다.

### **10.1 Backward Compatible**

기존 data, query, policy, snapshot을 깨지 않는다.

예시:

새 subclass 추가  
새 annotation 추가  
새 optional property 추가  
새 SKOS altLabel 추가

### **10.2 Backward Compatible with Migration**

기존 구조와 호환 가능하지만 migration이 필요하다.

예시:

property 이름 변경  
새 required field 추가  
기존 class를 더 구체적 subclass로 분리

### **10.3 Breaking Change**

기존 구조를 직접 깨는 변경이다.

예시:

class 삭제  
property 삭제  
domain/range 축소  
disjointness 추가  
snapshot schema 변경  
sameAs 정책 변경  
TBox 구조의 근본적 변경

Breaking Change는 반드시 MAJOR version을 올려야 한다.

---

## **11\. Deprecation Policy**

삭제는 즉시 하지 않는다.  
먼저 deprecation 상태로 전환한다.

active  
→ deprecated  
→ migration\_required  
→ removed

Deprecated property나 class는 다음 정보를 가져야 한다.

deprecated\_since  
removal\_target\_version  
replacement\_iri  
migration\_note  
owner\_module

예시:

ot:connectedTo  
  status: deprecated  
  replacement: ot:affects / ot:supportedBy / ot:locatedIn  
  removal\_target\_version: ontology-v2.0.0

핵심 원칙은 다음과 같다.

삭제보다 migration이 먼저다.

---

## **12\. Migration Policy**

Ontology 변경이 기존 ABox, SHACL, SPARQL, Policy, Snapshot, Agent SLM에 영향을 주면 migration plan이 필요하다.

Migration은 ontology 파일만 바꾸는 것이 아니다.

Ontology migration  
\= ontology \+ ABox \+ SHACL \+ SPARQL \+ Policy \+ Snapshot Schema \+ Agent Vocabulary \+ Audit interpretation 변경

Migration plan은 다음을 포함한다.

source\_version  
target\_version  
affected\_classes  
affected\_properties  
affected\_individuals  
affected\_agent\_vocabularies  
affected\_adapters  
mapping\_rule  
data\_migration\_script  
shacl\_update\_required  
sparql\_update\_required  
policy\_update\_required  
snapshot\_regeneration\_required  
adapter\_compatibility\_required  
rollback\_plan

실제 migration 순서는 다음과 같다.

1\. Migration Scope 확정  
2\. Source / Target Version 고정  
3\. Mapping Rule 작성  
4\. Sample ABox Migration  
5\. Shape / Query / Policy Update  
6\. Snapshot Regeneration Test  
7\. Agent SLM / Adapter Compatibility Review  
8\. Regression Test  
9\. Rollback Target 등록  
10\. Controlled Release

각 단계의 의미는 다음과 같다.

| 단계 | 설명 |
| ----- | ----- |
| Migration Scope 확정 | 어떤 class, property, ABox, shape, query, policy, snapshot, agent vocabulary가 영향을 받는지 확정 |
| Source / Target Version 고정 | migration 전후 version을 명시 |
| Mapping Rule 작성 | 기존 구조를 새 구조로 변환하는 규칙 작성 |
| Sample ABox Migration | 전체 migration 전에 sample data로 검증 |
| Shape / Query / Policy Update | SHACL, SPARQL, Policy reference 갱신 |
| Snapshot Regeneration Test | Safety Gate snapshot 생성 가능 여부 확인 |
| Agent SLM / Adapter Compatibility Review | vocabulary와 LoRA adapter 호환성 판단 |
| Regression Test | 기존 competency question, query, policy, snapshot 결과 비교 |
| Rollback Target 등록 | 실패 시 돌아갈 approved release package 지정 |
| Controlled Release | 제한된 범위에서 release 후 확대 |

핵심 원칙은 다음과 같다.

Ontology migration은 data migration과 model compatibility migration과 분리될 수 없다.

---

## **13\. Test and Regression**

Ontology 변경은 반드시 테스트를 통과해야 한다.

필수 테스트는 다음과 같다.

TBox consistency test  
Unsatisfiable class test  
Sample ABox reasoning test  
SHACL regression test  
SPARQL query regression test  
Policy impact test  
Safety Gate Snapshot generation test  
Materialized relation map test  
Competency Question test  
Audit trace consistency test  
Agent vocabulary compatibility test  
Adapter compatibility check

Competency Question 예시는 다음과 같다.

이 ActionCandidate는 EvidenceBundle에 의해 support되는가?  
이 GasRisk는 Zone\_A에 영향을 주는가?  
이 Action은 해당 Risk를 mitigate할 수 있는가?  
이 Agent는 해당 Task를 수행할 capability가 있는가?  
이 ExecutionRequest는 external system으로 전달 가능한가?  
이 decision은 어떤 ontology\_version과 snapshot\_version을 사용했는가?

핵심 원칙은 다음과 같다.

테스트 없는 ontology 변경은 release할 수 없다.

---

## **14\. Release Package**

Ontology release는 단일 파일이 아니라 release package로 배포한다.

Release package는 다음을 포함한다.

ontology files  
class registry  
property registry  
SHACL shapes  
SPARQL validation queries  
policy references  
mapping registry  
snapshot schema  
agent vocabulary manifest  
adapter compatibility report  
migration notes  
rollback plan  
release notes  
test results  
checksum

권장 폴더 구조는 다음과 같다.

release/  
  ontology-v1.5.0/  
    manifest.yaml

    ontology/  
      core.ttl  
      core.owl  
      domain\_modules/  
        safety.ttl  
        robot.ttl  
        evidence.ttl  
        execution.ttl

    registry/  
      class\_registry.yaml  
      property\_registry.yaml  
      mapping\_registry.yaml

    validation/  
      shacl\_shapes.ttl  
      sparql\_validation\_queries/  
        evidence\_support.ask.rq  
        risk\_affects\_zone.ask.rq  
        action\_target\_compatibility.ask.rq

    policy/  
      policy\_references.yaml

    snapshot/  
      snapshot\_schema.yaml  
      materialization\_manifest.yaml  
      binary\_snapshot\_map.bin  
      binary\_snapshot\_checksum.sha256

    agent\_slm/  
      agent\_vocabulary\_manifest.yaml  
      adapter\_compatibility\_report.yaml

    migration/  
      migration\_notes.md  
      migration\_plan.yaml  
      rollback\_plan.yaml

    tests/  
      test\_results.json  
      competency\_question\_results.json  
      shacl\_regression\_results.json  
      sparql\_regression\_results.json  
      snapshot\_generation\_results.json  
      adapter\_compatibility\_results.json

    checksum.sha256  
    release\_notes.md

`manifest.yaml`은 release package의 version과 구성 요소를 기록한다.

예시:

release\_version: ontology-v1.5.0  
ontology\_version: ontology-v1.5.0  
class\_registry\_version: class-registry-v1.1.0  
property\_registry\_version: property-registry-v1.2.0  
shacl\_shape\_version: shacl-v1.3.1  
sparql\_query\_version: sparql-validation-v0.8.0  
policy\_reference\_version: policy-ref-v0.9.8  
snapshot\_schema\_version: snapshot-schema-v0.4.0  
agent\_vocabulary\_version: agent-vocab-v0.3.5  
checksum: sha256:...

---

## **15\. Rollback Policy**

새 ontology release가 문제를 일으키면 rollback 가능해야 한다.

Rollback 조건은 다음과 같다.

Safety Snapshot 생성 실패  
SHACL regression failure 증가  
SPARQL query failure 증가  
Policy decision mismatch 발생  
Critical class inference 오류  
External mapping 오류  
Agent SLM output 품질 급락  
Snapshot hot-swap 실패  
Active snapshot checksum mismatch

Rollback 대상은 다음과 같다.

| Rollback 대상 | 설명 |
| ----- | ----- |
| ontology\_version | class/property/axiom 정의 |
| class\_registry\_version | class registry |
| property\_registry\_version | property registry |
| shacl\_shape\_version | validation shape |
| sparql\_query\_version | graph validation query |
| policy\_reference\_version | policy linkage |
| mapping\_registry\_version | external standard / ID mapping |
| snapshot\_schema\_version | Safety Gate snapshot schema |
| binary\_snapshot\_map\_version | C++ Safety Gate가 읽는 compact runtime map |
| agent\_vocabulary\_version | Agent SLM vocabulary 기준 |
| adapter\_registry\_version | Agent LoRA adapter compatibility 기준 |

핵심 원칙은 다음과 같다.

Rollback은 ontology 파일 rollback이 아니다.  
Rollback은 meaning, validation, policy, mapping, snapshot, audit, agent vocabulary 기준의 동시 복구다.

---

## **15.1 Shared Memory Snapshot Hot-Swap Failure Recovery**

Safety Gate Runtime Snapshot은 shadow buffer에서 생성된 새 snapshot을 검증한 뒤 active snapshot으로 publish한다.

정상 흐름은 다음과 같다.

Shadow Snapshot 생성  
→ checksum 검증  
→ version compatibility 검증  
→ schema compatibility 검증  
→ materialized map 검증  
→ atomic publish  
→ Active Snapshot 교체

Hot-swap 실패 시 원칙은 다음과 같다.

Shadow snapshot 검증 실패 시 active snapshot을 교체하지 않는다.  
기존 active snapshot이 유효하면 그대로 유지한다.  
새 snapshot publish는 중단하지만 Safety Gate kernel 자체를 즉시 중단하지 않는다.  
기존 active snapshot도 유효하지 않으면 fail-closed mode로 전환한다.

복구 흐름은 다음과 같다.

1\. Shadow snapshot load 실패 감지  
2\. Atomic publish 차단  
3\. 기존 active snapshot checksum / valid\_until 확인  
4\. active snapshot 유효 시 last-known-good 상태 유지  
5\. active snapshot도 유효하지 않으면 fail-closed mode 진입  
6\. persistent approved release package에서 직전 approved binary snapshot map 로드  
7\. checksum / version / schema 검증  
8\. memory-resident standby buffer 또는 shared memory buffer에 복원  
9\. 검증 완료 후 active pointer 재게시  
10\. rollback audit record 생성

중요한 하드웨어/메모리 원칙은 다음과 같다.

Huge Pages는 RAM 영역이며 비휘발성 저장소가 아니다.  
비휘발성 approved release package는 disk / NVMe / artifact store에 보관한다.  
runtime 복구 속도를 위해 직전 approved binary snapshot map은 memory-resident standby buffer로 preload할 수 있다.  
C++ Safety Gate는 검증되지 않은 snapshot을 active로 publish하지 않는다.  
검증된 active snapshot이 없으면 allow하지 않고 fail-closed한다.

핵심 원칙은 다음과 같다.

Hot-swap 실패는 unsafe publish로 이어지면 안 된다.  
Snapshot rollback은 last-known-good approved binary map으로 복구해야 한다.

---

## **16\. External Standard Mapping Governance**

LEDO는 외부 표준을 그대로 복사하지 않는다.  
외부 표준은 mapping한다.

대상 예시는 다음과 같다.

BFO  
IFC  
SOSA / SSN  
SAREF  
PROV-O  
QUDT  
GeoSPARQL  
OWL-Time  
ISA / IEC 62443  
IEC 61508 related safety concepts

Mapping 변경 시 확인할 사항은 다음과 같다.

외부 표준 version이 바뀌었는가?  
LEDO canonical class와 mapping이 깨지는가?  
외부 identifier와 canonical identity 연결이 바뀌는가?  
SHACL shape가 영향을 받는가?  
SPARQL query가 영향을 받는가?  
Safety Snapshot materialization이 영향을 받는가?

핵심 원칙은 다음과 같다.

Standards are mapped, not blindly copied.

---

## **17\. Agent SLM 영향 관리**

Ontology 변경은 Agent SLM에도 영향을 줄 수 있다.

상세 SLM 학습 루프는 Agent-Specific SLM 문서에서 다룬다.  
이 문서에서는 ontology 변경이 agent vocabulary, training dataset version, LoRA adapter compatibility 갱신을 요구하는지 판단한다.

다음 변경은 Agent SLM 영향 검토 대상이다.

class name 변경  
property name 변경  
SKOS label 변경  
Action type 변경  
Evidence model 변경  
Safety Gate boundary 변경  
ExecutionRequest 의미 변경  
TBox class hierarchy 변경  
Property semantics 변경

필요한 조치는 다음과 같다.

agent\_vocabulary\_version 갱신  
SFT pair 검토  
Residual error test fixture 갱신  
Developer SLM prompt 기준 갱신  
Synthetic Data Factory template 갱신  
LoRA adapter compatibility review

핵심 원칙은 다음과 같다.

Ontology 변경은 모델 학습 기준 변경일 수 있다.

---

## **17.1 MAJOR TBox Change and Agent Adapter Compatibility**

TBox 구조가 근본적으로 바뀌는 MAJOR version 변경은 기존 Agent SLM / LoRA adapter의 의미 공간을 깨뜨릴 수 있다.

다음 변경은 기존 adapter 호환성을 전면 재검토해야 한다.

상위 class hierarchy 재구성  
핵심 domain/range 의미 변경  
ActionCandidate / ExecutionRequest 의미 변경  
Evidence / Policy / Safety boundary 변경  
주요 property semantics 변경  
핵심 SKOS vocabulary 변경  
Safety Gate materialized map 의미 변경

MAJOR TBox 변경이 확정되면 다음 절차를 따른다.

1\. 기존 관련 Agent LoRA adapter를 production promotion 대상에서 제외한다.  
2\. Adapter Registry에서 해당 adapter를 incompatible 또는 rejected 상태로 전환한다.  
3\. agent\_vocabulary\_version을 갱신한다.  
4\. tokenizer / domain token 영향 여부를 검토한다.  
5\. 필요한 경우 Mean Initialization 또는 Embedding Adaptation을 수행한다.  
6\. DAPT dataset을 새 ontology version 기준으로 재구성한다.  
7\. SFT pair와 residual error fixture를 새 meaning boundary 기준으로 재작성한다.  
8\. Agent-specific LoRA를 재학습한다.  
9\. fixed eval / holdout eval / critical violation test를 다시 수행한다.  
10\. 통과한 adapter만 candidate → validated → canary → approved 순으로 승격한다.

Adapter 상태 전이는 다음과 같다.

approved  
→ incompatible  
→ rejected\_for\_current\_ontology  
→ retraining\_required  
→ candidate  
→ validated  
→ canary  
→ approved

핵심 원칙은 다음과 같다.

MAJOR ontology change can invalidate Agent SLM behavior.  
Old LoRA adapters must not be reused without compatibility review.  
Model retraining starts from updated vocabulary and updated meaning boundaries.

---

## **18\. Audit and Trace**

모든 중요한 ontology 변경은 audit 대상이다.

AuditRecord는 다음을 기록해야 한다.

change\_id  
old\_version  
new\_version  
changed\_by  
approved\_by  
review\_result  
test\_result  
migration\_result  
release\_time  
rollback\_target  
reason  
affected\_adapters  
affected\_snapshot\_schema

Runtime decision도 ontology version을 기록해야 한다.

DecisionCase\_01  
  usedOntologyVersion: ontology-v1.5.0  
  usedPolicyVersion: policy-v0.9.8  
  usedSnapshotVersion: sgs-2026-06-25-0007

핵심 원칙은 다음과 같다.

나중에 왜 그런 decision이 나왔는지 추적하려면 당시 ontology version을 알아야 한다.

---

## **19\. Anti-Patterns**

| Anti-pattern | 문제 | 대안 |
| ----- | ----- | ----- |
| ontology를 version 없이 수정 | decision trace 불가능 | semantic versioning 적용 |
| registry 없이 class/property 추가 | 의미 충돌 발생 | registry와 governance review |
| breaking change를 MINOR로 배포 | 기존 시스템 붕괴 | MAJOR version bump |
| deprecated period 없이 삭제 | 기존 query/data 깨짐 | deprecation period 운영 |
| SHACL / SPARQL / Policy 영향 검토 누락 | validation과 policy 결과 급변 | impact review 필수 |
| Safety Gate snapshot 영향 검토 누락 | runtime decision 오류 | snapshot generation test |
| migration plan 없이 release | 기존 ABox/query/policy 손상 | migration plan 필수 |
| rollback plan 없이 release | 장애 시 복구 불가 | rollback target 지정 |
| MAJOR TBox 변경 후 기존 LoRA adapter 재사용 | agent behavior 불일치 | adapter compatibility review / retraining |
| hot-swap 실패 snapshot을 active로 publish | unsafe runtime 상태 발생 | checksum 검증 \+ last-known-good rollback |

---

## **20\. 최종 운영 원칙**

Ontology는 versioned artifact다.  
Class와 property는 registry로 관리한다.  
Meaning change는 governance review를 거친다.  
Breaking change는 MAJOR version을 올린다.  
Deprecated period 없이 삭제하지 않는다.  
SHACL, SPARQL, Policy, Snapshot 영향도를 함께 검토한다.  
Safety-critical change는 조용히 배포하지 않는다.  
External standard는 copy가 아니라 mapping한다.  
Ontology 변경은 Agent SLM training 기준에도 영향을 줄 수 있다.  
MAJOR TBox 변경은 기존 LoRA adapter compatibility를 무효화할 수 있다.  
Runtime snapshot hot-swap 실패 시 unsafe publish를 금지한다.  
Runtime decision은 usedOntologyVersion을 기록해야 한다.

---

## **21\. 최종 결론**

LEDO Ontology Governance and Versioning의 핵심은 ontology를 자유롭게 바꾸지 못하게 막는 것이 아니다.

핵심은 ontology를 안전하게 진화시키는 것이다.

최종 구조는 다음과 같다.

Change Request  
→ Impact Classification  
→ Compatibility & Migration Review  
→ Test and Regression  
→ Governance Approval  
→ Versioned Release  
→ Audit and Rollback Registration

최종 원칙은 다음과 같다.

Ontology evolves.  
Governance controls meaning change.  
Versioning protects compatibility.  
Testing protects runtime behavior.  
Adapter compatibility protects model behavior.  
Rollback protects operational continuity.  
Audit protects accountability.

