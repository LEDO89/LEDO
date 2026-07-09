"""Evidence DTO contracts from 01_common_schema_dto Section 15.

`EvidenceDTO`'s original 12-field shape matched `1_common_schema_dto.md` Section 15.1
exactly, but `05_evidence_model/5_evidence_model.md` Section 18.1 describes the same
object (there called `EvidenceRecordDTO`) with a much larger canonical field set: time
trust (Section 7.1), spatial validity (Section 8.1), device health (Section 8.4),
evidence validity/freshness (Section 9.2), attested extraction (Section 10), PROV-O
provenance (Section 13.2), privacy/PII lifecycle (Section 15.3), and conflict
resolution (Section 14.3). Per explicit user instruction to fully reflect this,
those fields have been merged in as additive fields, grouped into new nested DTOs
(`TimeTrustDTO`, `SpatialValidityDTO`, `DeviceHealthDTO`, `AttestationDTO`,
`AIExtractionMetadataDTO`, `PrivacyDTO`, `ConflictDTO`) that mirror the existing
`SourceMetadataDTO`/`ConfidenceDTO`/`FreshnessDTO` nested-DTO convention rather than
flattening ~80 fields directly onto `EvidenceDTO`.

Fields with no closed value list found anywhere in `05_evidence_model.md`
(`time_validation_status`, `calibration_status`, `parser_validation_status`,
`human_attestation_status`, `cross_check_status`, `extraction_method`, `freshness_status`)
remain plain `str | None`, per the project's ambiguity-handling standard — not invented.

`legal_hold_status` is modeled as `bool` on `PrivacyDTO` per Section 15.4's explicit
boolean usage ("If legal_hold_status = true..."), distinct from `PrivacyLifecycleStatus`'s
own `LEGAL_HOLD` enum member (a broader lifecycle state), and distinct again from
`EvidenceValidityStatus.LEGAL_HOLD` (Section 9.2's overlapping list, applied to
`EvidenceDTO.validity_status`).

`reject_unattested_ai_as_evidence` enforces Section 4.5's "LLM output must not replace
evidence" / "Prohibited LLM roles: Create Primary Evidence" principle, but is now
grounded in `source_metadata.source_trust_level` (the precise, canonical
`SourceTrustLevel` enum) rather than the previous fuzzy string match against the
still-undecided `source_type` field. Only raw, unattested `AI_DERIVED` evidence is
rejected. `ATTESTED_AI_DERIVED` — reached only via the Section 10 attestation/trust-
upgrade process (`AttestationDTO.trust_upgrade_status`) — is explicitly allowed, per
Section 6.1's own trust model and Section 10.6's worked example, which shows
`ATTESTED_AI_DERIVED` as the terminal trust level of a legitimate Evidence record.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field, model_validator

from ledo_ontology_core.framework.schemas.base import StrictDTO
from ledo_ontology_core.framework.schemas.context import (
    ConfidenceDTO,
    FreshnessDTO,
    SourceMetadataDTO,
    TraceContextDTO,
)
from ledo_ontology_core.framework.schemas.enums import (
    AttestationType,
    ClockDriftCalculationMethod,
    ClockSyncStatus,
    ConflictResolutionStrategy,
    ConflictStatus,
    EvidenceCategory,
    EvidenceValidityStatus,
    PrivacyLifecycleStatus,
    SourceTrustLevel,
    TimeSourceType,
    TimeTrustLevel,
    TrustUpgradeStatus,
    ValidationStatus,
)
from ledo_ontology_core.framework.schemas.refs import EntityRefDTO, LocationRefDTO


class TimeTrustDTO(StrictDTO):
    captured_at: datetime
    received_at: datetime
    validated_at: datetime | None = None
    source_clock_id: str | None = None
    time_source_type: TimeSourceType
    time_authority_ref: str | None = None
    clock_sync_status: ClockSyncStatus
    clock_drift_estimate_ms: float | None = None
    clock_drift_calculation_method: ClockDriftCalculationMethod | None = None
    capture_receive_delta_ms: float | None = None
    max_allowed_time_delta_ms: float | None = None
    time_trust_level: TimeTrustLevel
    # No closed value list found for time_validation_status anywhere in
    # 05_evidence_model.md. DOMAIN_DECISION_REQUIRED before this becomes an enum.
    time_validation_status: str | None = None
    offline_clock_trust_policy_ref: str | None = None


class SpatialValidityDTO(StrictDTO):
    geo_location: dict[str, Any] | None = None
    geo_crs: str | None = None
    spatial_context_ref: str | None = None
    spatial_bounds_ref: str | None = None


class DeviceHealthDTO(StrictDTO):
    device_health_snapshot: dict[str, Any] | None = None
    device_health_snapshot_version: str | None = None
    # No closed value list found for calibration_status anywhere in
    # 05_evidence_model.md (only an inline example value "VALID").
    # DOMAIN_DECISION_REQUIRED before this becomes an enum.
    calibration_status: str | None = None
    historical_reliability_score: float | None = None


class AttestationDTO(StrictDTO):
    attestation_type: AttestationType | None = None
    attestation_evidence_refs: list[str] = Field(default_factory=list)
    attestation_signature: str | None = None
    attestation_workflow_id: str | None = None
    attestation_hash: str | None = None
    attested_by: str | None = None
    attested_at: datetime | None = None
    trust_upgrade_status: TrustUpgradeStatus | None = None
    # No closed value list found for these three fields anywhere in
    # 05_evidence_model.md. DOMAIN_DECISION_REQUIRED before they become enums.
    parser_validation_status: str | None = None
    human_attestation_status: str | None = None
    cross_check_status: str | None = None


class AIExtractionMetadataDTO(StrictDTO):
    is_extracted_evidence: bool = False
    # No closed value list found for extraction_method anywhere in
    # 05_evidence_model.md. DOMAIN_DECISION_REQUIRED before this becomes an enum.
    extraction_method: str | None = None
    extracted_from_evidence_id: str | None = None
    source_document_ref: str | None = None
    source_location_ref: str | None = None
    model_name: str | None = None
    model_version: str | None = None
    prompt_hash: str | None = None
    retrieval_corpus_ref: str | None = None
    retrieval_snapshot_id: str | None = None
    temperature: float | None = None
    extraction_confidence: float | None = None


class PrivacyDTO(StrictDTO):
    contains_pii: bool = False
    pii_categories: list[str] = Field(default_factory=list)
    privacy_lifecycle_status: PrivacyLifecycleStatus | None = None
    retention_policy_ref: str | None = None
    retention_expires_at: datetime | None = None
    encryption_key_ref: str | None = None
    key_management_policy_ref: str | None = None
    key_destroyed_at: datetime | None = None
    legal_hold_status: bool = False
    redaction_policy_ref: str | None = None
    anonymization_method: str | None = None
    access_policy_ref: str | None = None

    @model_validator(mode="after")
    def legal_hold_blocks_key_destruction(self) -> "PrivacyDTO":
        if self.legal_hold_status and self.key_destroyed_at is not None:
            raise ValueError(
                "key_destroyed_at must remain null while legal_hold_status is true"
            )
        return self


class ConflictDTO(StrictDTO):
    conflict_status: ConflictStatus | None = None
    conflict_weight: float | None = None
    applied_conflict_weights: dict[str, float] = Field(default_factory=dict)
    resolution_timestamp: datetime | None = None
    resolved_by: str | None = None
    conflict_resolution_strategy: ConflictResolutionStrategy | None = None
    conflict_resolution_ref: str | None = None


class EvidenceDTO(StrictDTO):
    evidence_id: str
    evidence_type: str
    source_metadata: SourceMetadataDTO
    subject_ref: EntityRefDTO
    location_ref: LocationRefDTO | None = None
    payload: dict[str, Any]
    timestamp_utc: datetime
    confidence: ConfidenceDTO
    freshness: FreshnessDTO
    trace_context: TraceContextDTO
    provenance: dict[str, Any]
    validation_status: ValidationStatus

    evidence_category: EvidenceCategory | None = None
    target_entity_refs: list[str] = Field(default_factory=list)
    related_event_refs: list[str] = Field(default_factory=list)
    related_state_refs: list[str] = Field(default_factory=list)
    related_action_refs: list[str] = Field(default_factory=list)
    payload_hash: str | None = None
    validity_status: EvidenceValidityStatus | None = None
    # No closed value list found for freshness_status specifically (Section 7.7 only
    # says it "cannot be set to VALID" under drift, implying overlap with
    # validity_status's values but never giving its own list).
    # DOMAIN_DECISION_REQUIRED before this becomes an enum.
    freshness_status: str | None = None
    ontology_binding_ref: str | None = None
    prov_entity_ref: str | None = None
    activity_refs: list[str] = Field(default_factory=list)
    was_generated_by: str | None = None
    was_derived_from: str | None = None
    was_attributed_to: str | None = None
    hash: str | None = None
    signature: str | None = None
    created_by: str | None = None
    supersedes_evidence_id: str | None = None
    is_append_only: bool = True

    time_trust: TimeTrustDTO | None = None
    spatial_validity: SpatialValidityDTO | None = None
    device_health: DeviceHealthDTO | None = None
    attestation: AttestationDTO | None = None
    ai_extraction: AIExtractionMetadataDTO | None = None
    privacy: PrivacyDTO | None = None
    conflict: ConflictDTO | None = None

    @model_validator(mode="after")
    def reject_unattested_ai_as_evidence(self) -> "EvidenceDTO":
        if self.source_metadata.source_trust_level == SourceTrustLevel.AI_DERIVED:
            raise ValueError(
                "Raw AI_DERIVED output may summarize evidence but cannot be Evidence "
                "unless attested (source_trust_level=ATTESTED_AI_DERIVED per "
                "05_evidence_model.md Section 10)"
            )
        return self


class EvidenceBundleDTO(StrictDTO):
    bundle_id: str
    evidence_refs: list[str] = Field(default_factory=list)
    bundle_purpose: str
    summary: str | None = None
    minimum_required_evidence_met: bool
    conflicting_evidence_detected: bool
    created_at_utc: datetime
