# 23rd EvidenceDTO Full Field Expansion

> Historical Review Artifact
>
> This document records a code and documentation correctness fix result.
> It is not an architecture source-of-truth document.
> If this document conflicts with AGENTS.md or 00_master_architecture/, AGENTS.md and 00_master_architecture/ take precedence.

## 1. Final Status

PATCH APPLIED

## 2. Scope

The 8-way parallel structure scan (see the 22nd patch) found that `EvidenceDTO` (`1_common_schema_dto.md` Section 15.1, 12 fields, matches code exactly) and `EvidenceRecordDTO` (`05_evidence_model/5_evidence_model.md` Section 18.1, ~90 fields under a different name) describe the same object with a massive field-completeness gap — the same two-document-fork pattern as `ExecutionRequestDTO`, `AuditRecordDTO`, `FeedbackEventDTO`, and `ExternalControlRequestDTO`, but far larger in scope. Per explicit user instruction ("전체 다 반영해서 진행해" — reflect everything, proceed), every field group in `05_evidence_model.md` Section 18.1 was merged into `EvidenceDTO`, including the AI/extraction metadata group (which was offered as an optional exclusion but the user chose to include in full).

## 3. Modified Files

- `03_core_specifications/01_common_schema_dto/1_common_schema_dto.md`
- `03_core_specifications/05_evidence_model/5_evidence_model.md`
- `src/ledo_ontology_core/framework/schemas/__init__.py`
- `src/ledo_ontology_core/framework/schemas/context.py`
- `src/ledo_ontology_core/framework/schemas/enums.py`
- `src/ledo_ontology_core/framework/schemas/evidence.py`
- `tests/unit/framework/test_common_schema_dto.py`
- `tests/unit/framework/test_high_frequency_dto.py`
- `tests/unit/framework/test_initial_dto_contracts.py`

## 4. Created Files

- `10_archive/review_artifacts/23rd_evidence_dto_full_field_expansion.md`
- `tests/unit/framework/test_evidence_dto.py`

## 5. New Enums (10)

All sourced directly from `05_evidence_model.md`, no invented values:

- `SourceTrustLevel` (9 members) — Section 6.1. Applies to the pre-existing `SourceMetadataDTO.source_trust_level` field, previously plain `str`.
- `EvidenceCategory` (18 members) — Section 5.1. Distinct from `evidence_type`, which remains registry-managed vocabulary per Section 8.2's established distinction.
- `TimeSourceType` (7 members) — Section 7.2.
- `ClockDriftCalculationMethod` (8 members) — Section 7.4.
- `EvidenceValidityStatus` (15 members) — Section 9.2. A separate, larger enum from the pre-existing `ValidationStatus` (which continues to govern `EvidenceDTO.validation_status`, per Section 5.2).
- `AttestationType` (6 members) — Section 10.2.
- `TrustUpgradeStatus` (7 members) — Section 10.3.
- `ConflictStatus` (6 members) — Section 14.1.
- `ConflictResolutionStrategy` (8 members) — Section 14.2.
- `PrivacyLifecycleStatus` (8 members) — Section 15.2.

## 6. New Nested DTOs (7)

Rather than flattening ~80 new fields directly onto `EvidenceDTO`, they were grouped into 7 new optional nested DTOs in `evidence.py`, mirroring the existing `SourceMetadataDTO`/`ConfidenceDTO`/`FreshnessDTO` convention already used by `EvidenceDTO`:

- `TimeTrustDTO` (Section 7.1, 14 fields)
- `SpatialValidityDTO` (Section 8.1, 4 fields)
- `DeviceHealthDTO` (Section 8.4, 4 fields)
- `AttestationDTO` (Section 10.5 + Section 18.1's trust-tracking fields, 11 fields)
- `AIExtractionMetadataDTO` (Section 10.4, 12 fields)
- `PrivacyDTO` (Section 15.3, 12 fields) — includes a validator enforcing Section 15.4's rule that `key_destroyed_at` must remain null while `legal_hold_status` is true.
- `ConflictDTO` (Section 14.3, 7 fields)

## 7. EvidenceDTO Top-Level Additions

`evidence_category`, `target_entity_refs`, `related_event_refs`, `related_state_refs`, `related_action_refs`, `payload_hash`, `validity_status`, `freshness_status`, `ontology_binding_ref`, `prov_entity_ref`, `activity_refs`, `was_generated_by`, `was_derived_from`, `was_attributed_to` (the last three from Section 13.2's PROV-O field list, which is more complete than Section 18.1's own consolidated list — the more complete, dedicated section was used), `hash`, `signature`, `created_by`, `supersedes_evidence_id`, `is_append_only`, plus the 7 nested DTO references above. All new fields are optional/defaulted — purely additive, no breaking renames.

## 8. Fields Left as Plain `str` (No Invented Enums)

`time_validation_status`, `calibration_status`, `parser_validation_status`, `human_attestation_status`, `cross_check_status`, `extraction_method`, `freshness_status` — each appears only in Section 18.1's consolidated field list with no dedicated "Values" section anywhere in the document, so none were given invented enum values, per the project's ambiguity-handling standard.

## 9. Flagged, Not Resolved: `reject_ai_as_evidence` Tension

Section 6.1 explicitly allows `AI_DERIVED`/`ATTESTED_AI_DERIVED` as legitimate (if restricted — "AI_DERIVED evidence cannot pass the Safety Gate by itself") `source_trust_level` values, meaning an AI-extracted evidence record backed by `AIExtractionMetadataDTO`/`AttestationDTO` is not automatically invalid per the source document. This is in tension with the existing `EvidenceDTO.reject_ai_as_evidence` validator, which rejects any evidence whose `source_metadata.source_type` is "ai"/"llm"/"slm" outright — a stricter rule than the source document states. The validator was deliberately left unchanged in this patch (documented via a module-docstring note in `evidence.py` and a doc note in `1_common_schema_dto.md` Section 15.1) since loosening it is a behavior change, not a structural field-completeness gap, and was not what this patch was scoped to fix.

## 10. Verification Summary

`.venv/bin/python -m pytest tests/unit/ -q` — 91 passed, 0 failed (81 before this patch; 10 new tests added covering nested-DTO construction, enum rejection, and the `PrivacyDTO` legal-hold validator). Three pre-existing test fixtures (`test_common_schema_dto.py`, `test_high_frequency_dto.py`, `test_initial_dto_contracts.py`) used the placeholder string `"test_fixture"` for `source_trust_level`, which is not one of the 9 canonical `SourceTrustLevel` values — updated to `"TRUSTED_SYSTEM"`.

## 11. Recommended Next Step

Continue the Tier 1 backlog from the 22nd patch, in order: `FeedbackEventDTO`, `ExternalControlRequestDTO`, `PolicyDecisionDTO`/`PolicyDecisionResponseDTO` (found during the 22nd patch's investigation), and the four underdeveloped Runtime Validation specialized result DTOs (`NetworkHealthResultDTO`, `TOCTOUResultDTO`, `SHACLValidationResultDTO`, `IdempotencyResultDTO`).

## 12. Modification Confirmation

All files listed in Section 3 were intentionally modified as part of this patch, following the user's explicit instruction to fully reflect `05_evidence_model.md`'s complete `EvidenceRecordDTO` field set into `EvidenceDTO`. No other files were modified.
