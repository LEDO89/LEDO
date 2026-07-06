---
title: Layered Semantic Architecture Implementation Guide
version: 1.0
status: draft
owner: platform-ontology
language: en
last_updated: 2026-06-22
---

# Layered Semantic Architecture Implementation Guide

## Goal

Implement the module described by the specification files in this folder.

The implementation must follow the architecture, DTO definitions, enum values, validation rules, registry boundaries, safety constraints, and implementation scope defined in the module specification.

## Module Focus

Translate the architectural specification into implementation-ready module boundaries, without adding runtime code unless explicitly required.

## Source of Truth

1. Root-level `AGENTS.md`
2. This `implementation_guide.md`
3. The module specification markdown file in this folder
4. Existing source code
5. Existing tests

## Default Implementation Order

1. Enums
2. DTOs
3. Interfaces
4. Registry specs
5. Registry loaders
6. Validators
7. Mock adapters
8. Routers or services
9. Unit tests
10. Integration tests

## Explicit Non-Goals

Do not implement:
- production external system integrations
- physical robot, PLC, SCADA, or machine control
- emergency execution without a mock or simulation boundary
- cloud deployment or production infrastructure
- invented domain-specific rules, thresholds, or ontology content

## Acceptance Criteria

- DTOs are type-safe.
- Fixed vocabularies use enums.
- Domain-specific meaning is not invented.
- Validators have success and failure tests.
- No physical command is emitted.
- No LLM output can directly create approval or execution.
- External systems are represented by interfaces or mocks.
- Tests pass.
