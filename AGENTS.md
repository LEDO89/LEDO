# AGENTS.md

## Project Identity

This project is an ontology-centric cyber-physical AI platform core.

The goal is to build a reusable engineering framework for modeling industrial domains through ontology, evidence, state, event, action, decision, approval, validation, audit, and execution-boundary structures.

The platform must support construction, industrial, robotics, safety, AI governance, runtime validation, and external control integration use cases.

This project is not a domain-rule generator.
This project is a framework for governing domain meaning safely.

---

## Core Principle

This project separates structure from domain meaning.

Codex may build the framework.
The human domain expert owns the domain meaning.

Roles:

Codex = framework builder
Human domain expert = domain authority

Core rule:

Structure can be generated.
Meaning must be governed.

---

## First Constitution Alignment

Codex must follow the LEDO First Constitution when it exists under the current repository path:

00_master_architecture/00_first_construction.md

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

## Source of Truth

The source of truth is ordered as follows:

1. Root-level AGENTS.md
2. 00_master_architecture/00_first_construction.md
3. 00_master_architecture/01_master_architecture.md
4. Module-level specification markdown file (the specific document under `03_core_specifications/`, `06_registry_specs/`, or `08_runtime_validation/` that defines the concept being implemented)
5. Module-level implementation_guide.md
6. Existing source code
7. Existing tests

Module-level `implementation_guide.md` is an orientation guide only. It defines build order, non-goals, and the shape of acceptance criteria. It must never outrank a specification markdown file on a factual question — field names, enum values, DTO shape, state machines, or validation rules. If an `implementation_guide.md` conflicts with the specification markdown file it accompanies, the specification markdown file wins.

Within specification markdown files, the following domain-specific priority applies:

- Lifecycle and DTO contracts: `03_core_specifications/`
- Registry contracts (entry schema, fields, status, cross-references): `06_registry_specs/`
- Validation and Safety Gate contracts: `08_runtime_validation/`
- Technology and responsibility mapping: `02_layer_stack_mapping/` (reference only; does not define contracts)
- Catalog and index convenience: `09_appendices/` (non-authoritative index; useful only for values already sourced from the documents above)
- Historical record: `10_archive/` (historical reference only; never a code-generation source)
- Build sequencing roadmap: `07_implementation_plan/` (sequencing reference only; defines what order to build things in, and does not override the contract documents above on field-level content)

PROJECT_TREE.md is only a repository structure map.
PROJECT_TREE.md is not an architecture source-of-truth document.

If there is a conflict, prefer the safer interpretation.

If safety, execution, evidence, approval, policy, identity, or physical control is involved, Codex must fail closed or create a TODO instead of guessing.

---

## Markdown-to-Code Implementation Rule

Codex must implement one markdown specification file at a time.

For every implementation task, Codex must:

1. Read AGENTS.md first.
2. Read 00_master_architecture/00_first_construction.md.
3. Read 00_master_architecture/01_master_architecture.md.
4. Read the selected markdown specification file for the task.
5. Treat PROJECT_TREE.md only as a repository map.
6. Create code only for concepts explicitly defined in the selected markdown file.
7. Create tests for the implemented schema, registry, validator, interface, adapter, or service.
8. Stop and create TODOs when the selected markdown file is ambiguous.
9. Never expand the task into neighboring folders unless explicitly instructed.
10. Never create UI, API, runtime behavior, or domain rules unless the selected markdown file explicitly requires them.

Core rule:

One markdown file becomes one bounded implementation step.

---

## Domain Authority Rule

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

## Safety Boundary Rule

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

## LLM Boundary Rule

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

## Execution Boundary Rule

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

## Architecture Control Plane

The architecture control plane lives under:

00_master_architecture/

Current control documents:

00_master_architecture/
  README.md
  00_first_construction.md
  01_master_architecture.md

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

## Repository Structure

Use the following high-level structure:

ledo_ontology_core/
  AGENTS.md
  README.md
  PROJECT_TREE.md
  pyproject.toml

  00_master_architecture/
  01_layer_architecture/
  02_layer_stack_mapping/
  03_core_specifications/
  04_ontology_foundation/
  05_domain_ontology_modules/
  06_registry_specs/
  07_implementation_plan/
  08_runtime_validation/
  09_appendices/
  10_archive/

  src/
    ledo_ontology_core/
      domain_packs/
      framework/

  apps/
  contracts/
  frontend/
  infra/
  templates/
  tests/

AGENTS.md is the repository-level operational entry document.
00_master_architecture/README.md is the master architecture entry document.
PROJECT_TREE.md is the repository structure map only.
Root README.md is optional and is not required as an architecture source-of-truth.

Folder responsibilities:

00_master_architecture
→ architecture control plane

01_layer_architecture
→ system layer definitions

02_layer_stack_mapping
→ mapping between layers, technologies, and runtime responsibilities

03_core_specifications
→ operational contracts, DTOs, lifecycle, evidence, approval, execution, audit

04_ontology_foundation
→ semantic contracts, OWL, SHACL, reasoning, property design, governance

05_domain_ontology_modules
→ domain-specific ontology extensions governed by human domain authority

06_registry_specs
→ class, property, action, state, event, policy, adapter registries

07_implementation_plan
→ implementation order, milestones, module roadmap

08_runtime_validation
→ Safety Gate, runtime snapshot, deterministic validation, hot path constraints

09_appendices
→ references, glossary, examples, external notes

10_archive
→ deprecated or superseded documents

src/
→ implementation source code

apps/
→ executable application entrypoints

contracts/
→ exported contracts and interoperability schemas

frontend/
→ operator UI product surface

infra/
→ deployment and operations scaffolding

templates/
→ reusable specification and Codex task templates

tests/
→ unit, integration, fixture, and regression tests

---

## Coding Standards

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

## Source Layout

Use the actual repository source layout:

src/ledo_ontology_core/
  domain_packs/
  framework/
    adapters/
    audit/
    decision/
    graph/
    ontology/
    policy/
    registries/
    runtime/
    schemas/
    validation/

Framework code belongs under:

src/ledo_ontology_core/framework/

Domain-specific content belongs under:

src/ledo_ontology_core/domain_packs/

Do not place shared framework modules directly under src/ledo_ontology_core/ unless explicitly instructed.

---

## Framework vs Domain Pack Rule

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

## Architecture Implementation Order

Follow the project architecture in this order:

1. Specification
2. DTO
3. Enum
4. Registry
5. Validator
6. Router or service
7. Adapter interface
8. Mock adapter
9. Test
10. UI or graph visualization

Do not skip validation.

Do not create runtime behavior before the corresponding schema and validator exist.

Do not create production external behavior before the mock adapter and tests exist.

Do not create UI before framework, contracts, validation, and API boundaries exist.

---

## Validation Rule

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

## Test Rule

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

## Mock First Rule

This rule has two distinct categories with two distinct rationales. Codex must not treat them as one undifferentiated "mock everything" instruction.

### Category 1: Physical and External Control Systems (safety-critical, non-negotiable)

Use mocks, dry-run adapters, or simulation boundaries for:

robot middleware
fleet manager
PLC
SCADA
access-control systems
external sensor gateway
external equipment controller

This category exists because of the Safety Boundary Rule: this project must not emit real physical commands by default. These integrations must remain mocked, dry-run, or interface-only until explicit human approval is given, regardless of how mature the rest of the implementation is. This is a Constitution-level constraint, not a convenience.

### Category 2: Infrastructure Backing Stores (pragmatic sequencing, not a safety rule)

Use lightweight or in-memory implementations first for:

OPA or policy engine
message broker
database
graph database
triple store

This category exists only to let schemas, DTOs, registries, and validators stabilize before paying the cost of real infrastructure setup. It is not a safety requirement, and it must not be treated as one.

Do not leave these mocked indefinitely. Replace each with its real implementation as soon as the corresponding schema or contract is stable enough to test against, and before the module is considered complete for production use. Prolonged mocking of policy engines, databases, message brokers, or triple stores creates real integration risk: schema drift, missed transactional or consistency edge cases, and tests that pass against a mock but fail against the real system. If a module's completion is blocked only by swapping in real infrastructure, that dependency must be tracked explicitly, not silently left as a mock.

### Common Rule

Production integration for Category 1 must be added only after explicit human approval. Category 2 items should graduate from mock to real implementation as part of normal implementation progress, without requiring the same approval gate as physical execution systems.

---

## Audit Rule

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

ontology_version
policy_version
shacl_shape_version
snapshot_version
adapter_version
registry_version

Core rule:

No critical decision without traceability.

---

## Idempotency Rule

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

## Ontology and Reasoning Boundary Rule

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

## Evidence Rule

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

## Registry Rule

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
owner_module
description
validation_reference
governance_status
source_md

Codex may implement registry loaders, schemas, validators, and tests.

Codex must not invent real domain registry values beyond placeholders.

---

## Domain No-Guessing Rule

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

## Codex Review Rule

When asked to review the repository, Codex must:

read AGENTS.md first
use 00_master_architecture as the architecture control plane
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

## Completion Rule

A task is not complete unless the following are true:

schema exists when required
validator exists when required
tests exist
unsafe assumptions are avoided
domain-specific unknowns are marked
external behavior is mocked
audit implications are considered
source-of-truth conflicts are resolved or documented
selected markdown file traceability is preserved

If tests are not created, the work is scaffolding only.

If validators are not created, runtime behavior must not be added.

If physical execution is possible, production behavior must not be implemented without explicit human approval.

---

## Git Completion Rule

Do not push incomplete work.

A task may be committed only after:

the selected markdown file was implemented within scope
no neighboring scope was expanded without instruction
tests were added or explicitly marked as skipped with reason
pytest passes for the affected test scope
unsafe assumptions are documented as TODOs
external behavior remains mocked or dry-run
source-of-truth conflicts are resolved or documented

A task may be pushed only after:

the user has reviewed the diff
the user has confirmed the work is complete
the branch is clean except for the intended changes
the commit message describes the implemented markdown specification

Core rule:

Perfectly bounded completion first.
Git push second.

---

## Final Rule

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
