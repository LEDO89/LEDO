# **AGENTS.md**

## **Project Identity**

This project is an ontology-centric cyber-physical AI platform core.

The goal is to build a reusable engineering framework for modeling industrial domains through ontology, evidence, state, event, action, decision, approval, validation, audit, and execution-boundary structures.

The platform must support construction, industrial, robotics, safety, AI governance, runtime validation, and external control integration use cases.

This project is not a domain-rule generator.  
This project is a framework for governing domain meaning safely.

---

## **Core Principle**

This project separates structure from domain meaning.

Codex may build the framework.  
The human domain expert owns the domain meaning.

Roles:

Codex \= framework builder  
Human domain expert \= domain authority

Core rule:

Structure can be generated.  
Meaning must be governed.

---

## **First Constitution Alignment**

Codex must follow the LEDO First Constitution when it exists under:

00\_master\_architecture/00\_ledo\_first\_constitution.md

The following principles are mandatory:

Ontology is the semantic authority.  
AI output is candidate, not truth.  
Evidence and provenance are mandatory.  
Policy determines operational permission.  
Human approval governs high-risk authority.  
Safety Gate is deterministic and fail-closed.  
ActionCandidate, ApprovedAction, ExecutionRequest, and physical control are separate.  
External systems execute physical control.  
Audit records every meaningful decision path.  
Runtime hot path must be precomputed, bounded, deterministic, and fail-closed.

If a generated artifact conflicts with these principles, prefer the safer interpretation and create a TODO instead of guessing.

---

## **Domain Authority Rule**

Codex must not invent domain-specific industrial, construction, safety, robotics, legal, operational, or field rules.

Codex may create:

folder structures  
schemas  
DTOs  
enums  
interfaces  
registry loaders  
validators  
routers  
services  
adapters  
mock implementations  
test scaffolds  
placeholder examples  
documentation templates

Codex must not invent:

construction safety rules  
robot behavior rules  
equipment operation rules  
industrial control rules  
PLC or SCADA command semantics  
worker safety thresholds  
legal compliance rules  
emergency procedures  
approval authority rules  
economic bottleneck assumptions  
field-specific ontology classes or properties beyond placeholders

When domain knowledge is missing, Codex must create one of the following instead of guessing:

TODO  
placeholder  
interface  
mock  
skipped test explaining what is missing  
failing test explaining required domain expert input

---

## **Safety Boundary Rule**

This project must not emit real physical commands by default.

The following must never be implemented without explicit human instruction:

real robot control  
real PLC control  
real SCADA write operation  
real machine control  
real emergency stop command  
real access-control lock command  
real production adapter that affects the physical world

Use one of the following instead:

interface  
mock adapter  
dry-run adapter  
simulation boundary  
test fixture  
placeholder adapter

Core rule:

No real physical actuation by default.

---

## **LLM Boundary Rule**

LLM output must never directly create approval or execution.

Allowed LLM roles:

Intent  
ActionCandidate  
EvidenceSummary  
MappingProposal  
RiskInterpretation  
Explanation  
DocumentSummary  
PolicyImpactSuggestion  
ValidationSuggestion

Forbidden LLM roles:

ApprovedAction  
EmergencyApprovedAction  
ExecutionRequest  
ExternalControlRequest  
PLC command  
robot command  
SCADA command  
safety bypass decision  
emergency execution decision  
physical control decision

Core rule:

LLM output may propose.  
Ontology, evidence, policy, approval, and Safety Gate must validate.

---

## **Execution Boundary Rule**

ApprovedAction is not a physical command.

ExecutionRequest is not a physical command.

ExternalControlRequest is still a request to an external system.

The external system owns actual physical execution.

Examples of external systems:

fleet manager  
robot middleware  
PLC system  
SCADA system  
access-control system  
equipment controller  
site operation platform

Core rule:

LEDO defines intent, constraints, approval, traceability, and validation.  
External systems own physical execution.

---

## **Architecture Control Plane**

The architecture control plane lives under:

00\_master\_architecture/

Recommended control documents:

00\_master\_architecture/  
  README.md  
  00\_ledo\_first\_constitution.md  
  01\_ledo\_master\_architecture.md  
  02\_document\_control\_map.md  
  03\_source\_of\_truth\_matrix.md  
  04\_code\_generation\_strategy.md  
  05\_codex\_architecture\_review\_prompt.md

These documents should remain short and directive.

They must not duplicate detailed Foundation, Core, or Runtime documents.

Their purpose is to define:

absolute principles  
architecture map  
document ownership  
source-of-truth boundaries  
code generation order  
Codex review criteria

---

## **Source of Truth**

The source of truth is ordered as follows:

1\. Root-level AGENTS.md  
2\. 00\_master\_architecture/00\_ledo\_first\_constitution.md  
3\. 00\_master\_architecture/01\_ledo\_master\_architecture.md  
4\. 00\_master\_architecture/02\_document\_control\_map.md  
5\. 00\_master\_architecture/03\_source\_of\_truth\_matrix.md  
6\. Module-level implementation\_guide.md  
7\. Module-level specification markdown file  
8\. Existing source code  
9\. Existing tests

If there is a conflict, prefer the safer interpretation.

If safety, execution, evidence, approval, policy, identity, or physical control is involved, Codex must fail closed or create a TODO instead of guessing.

---

## **Repository Structure**

Use the following high-level structure:

ledo\_ontology\_core/  
  AGENTS.md  
  README.md  
  pyproject.toml

  00\_master\_architecture/  
  01\_layer\_architecture/  
  02\_layer\_stack\_mapping/  
  03\_core\_specifications/  
  04\_ontology\_foundation/  
  05\_domain\_ontology\_modules/  
  06\_registry\_specs/  
  07\_implementation\_plan/  
  08\_runtime\_validation/  
  09\_appendices/  
  10\_archive/

  src/  
    ledo\_ontology\_core/

  tests/  
    unit/  
    integration/  
    fixtures/

Folder responsibilities:

00\_master\_architecture  
→ architecture control plane

01\_layer\_architecture  
→ system layer definitions

02\_layer\_stack\_mapping  
→ mapping between layers, technologies, and runtime responsibilities

03\_core\_specifications  
→ operational contracts, DTOs, lifecycle, evidence, approval, execution, audit

04\_ontology\_foundation  
→ semantic contracts, OWL, SHACL, reasoning, property design, governance

05\_domain\_ontology\_modules  
→ domain-specific ontology extensions governed by human domain authority

06\_registry\_specs  
→ class, property, action, state, event, policy, adapter registries

07\_implementation\_plan  
→ implementation order, milestones, module roadmap

08\_runtime\_validation  
→ Safety Gate, runtime snapshot, deterministic validation, hot path constraints

09\_appendices  
→ references, glossary, examples, external notes

10\_archive  
→ deprecated or superseded documents

src/  
→ implementation source code

tests/  
→ unit, integration, fixture, and regression tests

---

## **Coding Standards**

Use Python.

Use:

Pydantic v2 for DTOs  
Enums for fixed vocabularies  
Type hints  
pytest for tests  
Explicit validators  
Simple interfaces  
Mock-first external integrations

Prefer:

simple code  
explicit code  
readable code  
small modules  
clear responsibility boundaries  
testable design

Avoid:

hidden magic  
over-engineering  
domain-specific assumptions inside framework modules  
unsafe defaults  
implicit physical execution  
LLM-to-execution shortcuts

---

## **Suggested Source Layout**

Suggested source layout:

src/ledo\_ontology\_core/  
  schemas/  
  ontology/  
  registries/  
  validation/  
  decision/  
  policy/  
  adapters/  
  audit/  
  domain\_packs/

Framework code belongs in:

schemas/  
registries/  
validation/  
decision/  
policy/  
adapters/  
audit/  
ontology/

Domain-specific content belongs in:

domain\_packs/

---

## **Framework vs Domain Pack Rule**

Framework modules define reusable structure.

Domain packs define field-specific meaning.

Framework examples:

Base DTOs  
Event registry loader  
Action registry loader  
State registry loader  
Evidence registry loader  
Safety Gate validator  
TOCTOU validator  
Idempotency validator  
PolicyEngineAdapter interface  
MockPDP  
Graph export utility  
Audit record builder  
Snapshot schema validator

Domain pack examples:

example worker class placeholders  
example equipment state placeholders  
example sensor observation type placeholders  
example permit rule placeholders  
example robot mission state placeholders  
example site-specific approval placeholders  
example industrial domain property placeholders

Codex may scaffold domain packs.

Codex must not fill domain packs with assumed real-world rules.

---

## **Architecture Implementation Order**

Follow the project architecture in this order:

1\. Specification  
2\. DTO  
3\. Enum  
4\. Registry  
5\. Validator  
6\. Router or service  
7\. Adapter interface  
8\. Mock adapter  
9\. Test  
10\. UI or graph visualization

Do not skip validation.

Do not create runtime behavior before the corresponding schema and validator exist.

Do not create production external behavior before the mock adapter and tests exist.

---

## **Validation Rule**

All safety-critical behavior must have validators.

High-risk behavior must validate:

schema  
enum values  
required fields  
evidence presence  
source trust  
time trust  
state freshness  
conflict status  
approval validity  
TOCTOU delta  
idempotency  
network health  
adapter availability  
snapshot version  
policy version  
ontology version

Safety Gate hot path must not perform:

OWL reasoning  
full SHACL validation  
SPARQL query  
Graph DB network call  
LLM call  
external API call  
disk I/O  
large dynamic parsing  
unbounded computation

Safety Gate hot path may only use:

precomputed snapshot  
fixed enums  
compact maps  
bitsets  
version checks  
checksum checks  
freshness flags  
approval flags  
policy materialization results

---

## **Test Rule**

Every validator must have:

success tests  
failure tests  
edge-case tests

Every safety-critical module must have tests.

Do not mark work complete unless tests pass.

If a domain rule is missing, create:

skipped test with reason  
failing test with TODO  
placeholder fixture  
domain expert input requirement

---

## **Mock First Rule**

External behavior must be mocked before production integration.

Use mocks for:

robot middleware  
fleet manager  
PLC  
SCADA  
access-control systems  
OPA or policy engine  
message broker  
database  
graph database  
triple store  
external sensor gateway  
external equipment controller

Production integration must be added only after explicit human approval.

---

## **Audit Rule**

Safety-critical decisions must preserve traceability.

The following objects should be connected by trace IDs when applicable:

Event  
Evidence  
StateUpdate  
ActionCandidate  
DecisionCase  
ApprovalRequest  
ApprovalDecision  
ApprovedAction  
ExecutionRequest  
ExternalControlRequest  
FeedbackEvent  
AuditRecord

Audit records should include relevant version references:

ontology\_version  
policy\_version  
shacl\_shape\_version  
snapshot\_version  
adapter\_version  
registry\_version

Core rule:

No critical decision without traceability.

---

## **Idempotency Rule**

Any operation that may lead to external execution must use an idempotency key.

Retries must not create duplicate execution.

Objects that may require idempotency keys include:

ApprovedAction  
ExecutionRequest  
ExternalControlRequest  
AdapterDispatch  
FeedbackCorrelation

Core rule:

Retry must not duplicate physical intent.

---

## **Ontology and Reasoning Boundary Rule**

OWL defines meaning.

SHACL validates data shape.

SPARQL checks graph relationships.

Policy determines operational permission.

Safety Gate performs deterministic final pre-execution validation using precomputed snapshot data.

Codex must not move these responsibilities into the wrong layer.

Forbidden shortcuts:

using OWL as runtime Safety Gate validation  
using SHACL as ontology semantics  
using SPARQL directly in the Safety Gate hot path  
using Policy as ontology definition  
using LLM output as evidence  
using ExecutionRequest as physical control command

---

## **Evidence Rule**

AI output is not Evidence.

Evidence requires:

source  
timestamp  
provenance  
trust metadata  
traceability  
validation status

Allowed AI outputs include summaries or proposals.

Forbidden AI outputs include direct evidence creation, approval, and execution.

Core rule:

AI may summarize evidence.  
AI must not become evidence by itself.

---

## **Registry Rule**

Registries must be explicit and versioned when applicable.

Registry candidates include:

class registry  
property registry  
event type registry  
action type registry  
state model registry  
evidence type registry  
policy reference registry  
adapter registry  
snapshot schema registry  
agent vocabulary registry

Registry entries should include:

id  
name  
version  
status  
owner\_module  
description  
validation\_reference  
governance\_status

Codex may implement registry loaders, schemas, validators, and tests.

Codex must not invent real domain registry values beyond placeholders.

---

## **Domain No-Guessing Rule**

If a required rule, enum value, threshold, domain class, approval role, or external behavior is unclear, Codex must not guess.

Instead:

create a TODO  
create a placeholder  
create an interface  
create a mock  
create a skipped test explaining what is missing  
ask for domain expert input if interactive

Do not invent field-specific facts.

Do not invent safety thresholds.

Do not invent legal rules.

Do not invent emergency procedures.

Do not invent approval authority rules.

---

## **Codex Review Rule**

When asked to review the repository, Codex must:

read AGENTS.md first  
use 00\_master\_architecture as the architecture control plane  
review markdown documents for duplication  
identify source-of-truth conflicts  
identify unsafe responsibility shifts  
identify Safety Gate boundary violations  
identify AI/Evidence/Approval/Execution boundary violations  
identify Core vs Foundation vs Runtime responsibility overlap  
propose document consolidation  
propose code generation order  
avoid rewriting domain meaning

Codex must not convert placeholders into real domain rules.

---

## **Completion Rule**

A task is not complete unless the following are true:

schema exists  
validator exists  
tests exist  
unsafe assumptions are avoided  
domain-specific unknowns are marked  
external behavior is mocked  
audit implications are considered  
source-of-truth conflicts are resolved or documented

If tests are not created, the work is scaffolding only.

If validators are not created, runtime behavior must not be added.

If physical execution is possible, production behavior must not be implemented without explicit human approval.

---

## **Final Rule**

The goal is not to generate code quickly.

The goal is to build a reliable ontology-centric platform that preserves:

meaning  
validation  
safety  
traceability  
domain authority  
runtime determinism  
execution boundaries

Final principle:

Structure can be generated.  
Meaning must be governed.  
Safety must be validated.  
Execution must be bounded.  
Audit must preserve accountability.

