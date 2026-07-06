---
title: Implementation Plan Index
version: 1.1
status: populated
owner: platform-ontology
language: en
last_updated: 2026-07-06
---

# Implementation Plan Index

## Purpose

Index the implementation sequencing roadmap and the three formal implementation slices.

This folder is a sequencing reference only (see `AGENTS.md` Source of Truth). It defines what order to build things in; it does not override `03_core_specifications`, `06_registry_specs`, or `08_runtime_validation` on field-level content.

## Contents

- `implementation_plan.md` — the full Phase 0–19 build sequence and dependency map.
- `implementation_slice_1/implementation_slice_1_plan.md` — Foundation slice (`implementation_plan.md` Phase 0–4).
- `implementation_slice_2/implementation_slice_2_plan.md` — Registry slice (`implementation_plan.md` Phase 5–14, excluding Agent Vocabulary Registry and Model Adapter Registry, which are out of scope for this implementation stage).
- `implementation_slice_3/implementation_slice_3_plan.md` — Runtime and Execution slice (`implementation_plan.md` Phase 15–19).

## Notes

This document is intentionally written in English so that Codex and other coding agents can use it as an implementation source.

"MVP" terminology is not used anywhere in this repository outside of `10_archive/` (historical, frozen) and direct quotations of that history. Several `03_core_specifications/` documents use their own internal "Rollout Stage 1/2/3" labels (formerly "MVP Phase"); where that numbering could be confused with the slices listed above, a disambiguation note has been added at the point of use.
