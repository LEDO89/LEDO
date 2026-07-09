# 27th Ontology Module Boundary Class List Gaps

> Historical Review Artifact
>
> This document records a code and documentation correctness fix result.
> It is not an architecture source-of-truth document.
> If this document conflicts with AGENTS.md or 00_master_architecture/, AGENTS.md and 00_master_architecture/ take precedence.

## 1. Final Status

PATCH APPLIED

## 2. Scope

Continuing the structure sweep into previously-unreviewed areas, two Haiku sub-agents reviewed `04_ontology_foundation/` (7 files) and `05_domain_ontology_modules/` (12 subdirectories) plus `03_core_specifications/06_ontology_module_boundary/6_ontology_module_boundary.md`. `04_ontology_foundation/` was confirmed clean (no fix needed). `05_domain_ontology_modules/`'s own files are still placeholders (per `09_appendices/appendix_e_ontology_module_catalog/`'s own explicit note that no concrete classes exist yet there), but `6_ontology_module_boundary.md` was found to have two internal self-inconsistencies, both directly verified before fixing.

## 3. Modified Files

- `03_core_specifications/06_ontology_module_boundary/6_ontology_module_boundary.md`

## 4. Created Files

- `10_archive/review_artifacts/27th_ontology_module_boundary_class_list_gaps.md`

## 5. Finding 1: `DigitalSystem` Missing from Section 6.2

Section 6.2 ("core-crosscutting") and Section 8.2 ("Classes That Can Be Included") both list the classes allowed in the core-crosscutting module, and should be the same set. Section 8.2 included `DigitalSystem`; Section 6.2 did not. Section 11.3 (line 601) actively uses `core_cross:DigitalSystem` as the superclass of `robot:FleetManager`, confirming the class is real and required, not a leftover — Section 6.2 was the one missing it. Fixed by adding `DigitalSystem` to Section 6.2's list, matching Section 8.2 exactly.

## 6. Finding 2: `ClockSyncStatus`/`ClockDriftCalculationMethod` Missing from Section 14.3

Section 14.2 ("Explicit Connection to the Evidence Model") lists 18 concepts the Evidence Module must be able to represent, sourced directly from `05_evidence_model.md`'s field/enum names — these names match the actual Python enum class names built in the 23rd patch exactly (`SourceTrustLevel`, `TimeTrustLevel`, `ClockSyncStatus`, `ClockDriftCalculationMethod`, `TrustUpgradeStatus`, `ConflictResolutionStrategy`, `PrivacyLifecycleStatus`). Section 14.3 ("Classes That Can Be Included") proposes shortened OWL class names for most of these (`TimeTrust`, `TrustUpgrade`, `ConflictResolution`, `PrivacyLifecycle`, `CryptoShredding`, `LegalHold` — dropping the `Status`/`Level` suffix, a plausible intentional OWL class-vs-value-type naming convention, not necessarily a bug) but omitted `ClockSyncStatus` and `ClockDriftCalculationMethod` entirely, under any name. This is an unambiguous gap, not a naming-convention question. Fixed by adding `ClockSync` and `ClockDriftCalculation` to Section 14.3's list, matching that section's own established shortened-name convention.

## 7. Deliberately Not Changed

The broader question of whether Section 14.3's shortened class names (`TimeTrust` vs. Section 14.2's `TimeTrustLevel`, etc.) represent an intentional OWL class-vs-enumerated-value-type distinction, or a naming inconsistency that should be fully reconciled, was not resolved — only the unambiguous missing-entirely gap was fixed. `05_domain_ontology_modules/`'s own placeholder files were left untouched, since the catalog itself already documents them as intentionally unimplemented at this stage.

## 8. Verification Summary

This was a documentation-only fix (no `src/` or `tests/` files touched). `.venv/bin/python -m pytest tests/unit/ -q` — 104 passed, 0 failed (re-run to confirm no incidental impact).

## 9. Recommended Next Step

No further structural gaps are currently known from the completed sweep (`00_master_architecture`, `01_layer_architecture`, `02_layer_stack_mapping`, `03_core_specifications` in full, `04_ontology_foundation`, `05_domain_ontology_modules`, `06_registry_specs`, `07_implementation_plan` spot-checked, `08_runtime_validation` in full, `09_appendices`). Return to normal Step 1 code review per the established Codex-writes / Claude-reviews workflow, or commit the accumulated uncommitted work (22nd–27th patches) if the user wants to checkpoint before continuing further.

## 10. Modification Confirmation

The file listed in Section 3 was intentionally modified as part of this patch, per the user's explicit instruction to continue fixing. No other files were modified.
