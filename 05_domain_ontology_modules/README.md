**README.md — 05 Domain Ontology Modules**

## **1\. Purpose**

`05_domain_ontology_modules` is the area for extending domain-specific meaning on top of the LEDO Ontology Core.

This folder does not predefine the rules of a specific industry.  
This folder defines how domain ontology modules can safely extend the Core Ontology Foundation.

The core structure of LEDO must remain an industry-neutral platform core, while domain-specific meaning must be separated into independent Domain Modules or Domain Packs.

---

## **2\. Core Principles**

Framework defines structure.

Domain Module defines domain meaning.

Domain meaning must be governed.

LEDO is not fixed to a single industry.

Domain Modules enable industry-specific extension and must follow these principles.

Domain meaning must not be generated arbitrarily.

Domain rules must be reviewed by domain experts.

Domain modules must follow Foundation principles.

Domain modules must be connected to Registries.

Domain modules must not bypass Runtime Validation.

Domain modules must not define physical execution commands.

---

## **3\. Responsibilities of This Folder**

`05_domain_ontology_modules` is responsible for:

Defining the structure of Domain Modules

Defining the domain extension contract

Defining the Domain Pack template

Defining how domain-specific Classes and Properties are extended

Defining how domain-specific Events, States, and Actions are extended

Defining how domain-specific Evidence, Policy, and Runtime Validation requirements are connected

Defining the boundary between Foundation and Domain Modules

This folder defines the container for domains.  
It does not arbitrarily define actual domain rules.

---

## **4\. What This Folder Does Not Own**

This folder does not directly define:

Real industrial safety standards

Real equipment operation rules

Real work permit rules

Real risk thresholds

Real legal interpretations

Real emergency procedures

Real robot behavior rules

Real PLC / SCADA command semantics

Site-specific approval authority

These must be defined in separate Domain Packs through domain expert review and governance.

---

## **5\. Role of a Domain Module**

A Domain Module extends domain-specific meaning on top of the Ontology Foundation.

A Domain Module may define:

Domain-specific object types

Domain-specific state types

Domain-specific event types

Domain-specific action candidate types

Domain-specific Evidence types

Domain-specific Policy references

Domain-specific Runtime Validation requirements

Domain-specific external system integration requirements

However, a Domain Module must not violate the non-negotiable boundaries of LEDO.

AI output is not Evidence.

ActionCandidate is not an execution command.

ApprovedAction is not a physical command.

ExecutionRequest is not a physical command.

Safety Gate must not be bypassed.

Physical Execution belongs to External Systems.

---

## **6\. Relationship to Foundation**

`04_ontology_foundation` defines common semantic principles.

`05_domain_ontology_modules` extends domain-specific meaning on top of those principles.

Ontology Foundation

→ Common semantic contract

Domain Ontology Modules

→ Domain-specific semantic extension

A Domain Module must follow the Foundation principles for Classes, Properties, Axioms, Constraints, Reasoning, and Governance.

A Domain Module does not replace the Foundation.

---

## **7\. Relationship to Core Specifications**

`03_core_specifications` defines operational contracts.

A Domain Module may connect to the operational objects defined by Core Specifications.

Examples:

Domain Event

→ CoreEvent

Domain ActionCandidate

→ ActionCandidate

Domain Evidence Type

→ Evidence Model

Domain Approval Requirement

→ Decision / Approval Model

Domain Execution Requirement

→ ExecutionRequest Model

A Domain Module must not bypass the Core object lifecycle.

---

## **8\. Relationship to Registry**

Fixed vocabularies defined by Domain Modules must be connected to Registries.

Domain Action Type

→ Action Registry

Domain Event Type

→ Event Registry

Domain State Type

→ State Registry

Domain Evidence Type

→ Evidence Registry

Domain Policy Reference

→ Policy Registry

Domain Approval Requirement

→ Approval Registry

Registries prevent uncontrolled domain value creation and provide version control and validation support.

---

## **9\. Relationship to Runtime Validation**

A Domain Module may declare Runtime Validation requirements.

However, it must not directly extend the runtime hot path or insert heavy reasoning into the Safety Gate.

Domain-specific Runtime Validation requirements must follow this flow.

Domain Rule Requirement

→ Validation Specification

→ Registry Reference

→ Materialization Rule

→ Safety Snapshot

→ Safety Gate Lookup

Safety Gate must only read precomputed results.

---

## **10\. Recommended Structure**

At the initial stage, this folder should remain lightweight.

05\_domain\_ontology\_modules/

  README.md

  domain\_module\_contract.md

  domain\_pack\_template.md

Real industry-specific Domain Packs should be added after the Foundation, Registry, and Runtime Validation structures become stable.

Possible future extension structure:

05\_domain\_ontology\_modules/

  construction\_domain\_pack/

  manufacturing\_domain\_pack/

  logistics\_domain\_pack/

  energy\_domain\_pack/

  robotics\_domain\_pack/

Each Domain Pack must be managed independently and must not contaminate the common Framework.

---

## **11\. Minimum Domain Pack Structure**

Each Domain Pack should include at least:

domain\_name

domain\_scope

domain\_classes

domain\_properties

domain\_events

domain\_states

domain\_actions

domain\_evidence\_types

domain\_policy\_references

domain\_approval\_requirements

domain\_runtime\_validation\_requirements

domain\_registry\_extensions

external\_system\_assumptions

governance\_owner

version

Actual domain-specific values should be added only after expert review and approval.

---

## **12\. Final Principles**

`05_domain_ontology_modules` does not predefine a specific industry.

This folder defines the extension structure that allows multiple industry domains to safely build on top of the LEDO Core.

Platform first.

Domain later.

Structure first.

Meaning governed.

No domain guessing.

No safety shortcut.

Final principle:

Domain Modules extend meaning.

They do not override the architecture.

# **README.md — 05 Domain Ontology Modules**

