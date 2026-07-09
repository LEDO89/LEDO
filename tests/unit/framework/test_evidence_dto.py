from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from ledo_ontology_core.framework.schemas import (
    AIExtractionMetadataDTO,
    AttestationDTO,
    ConflictDTO,
    ConfidenceDTO,
    DeviceHealthDTO,
    EntityRefDTO,
    EvidenceCategory,
    EvidenceDTO,
    EvidenceValidityStatus,
    FreshnessDTO,
    PrivacyDTO,
    PrivacyLifecycleStatus,
    SourceMetadataDTO,
    SourceTrustLevel,
    SpatialValidityDTO,
    TimeTrustDTO,
    TraceContextDTO,
)


def now() -> datetime:
    return datetime.now(timezone.utc)


def source() -> SourceMetadataDTO:
    return SourceMetadataDTO(
        source_type="sensor",
        source_id="src-1",
        source_trust_level="VERIFIED_DEVICE",
        ingested_at_utc=now(),
    )


def confidence() -> ConfidenceDTO:
    return ConfidenceDTO(
        confidence_score=0.9,
        confidence_level="high",
        validation_status="PASSED",
    )


def freshness() -> FreshnessDTO:
    t = now()
    return FreshnessDTO(
        timestamp_utc=t,
        ingested_at_utc=t,
        freshness_ms=1,
        is_stale=False,
    )


def evidence_kwargs(**overrides: object) -> dict:
    base = dict(
        evidence_id="ev-1",
        evidence_type="SENSOR_OBSERVATION_EVIDENCE",
        source_metadata=source(),
        subject_ref=EntityRefDTO(entity_id="zone-1", entity_type="zone"),
        location_ref=None,
        payload={"value": 87},
        timestamp_utc=now(),
        confidence=confidence(),
        freshness=freshness(),
        trace_context=TraceContextDTO(trace_id="trace-1"),
        provenance={},
        validation_status="PASSED",
    )
    base.update(overrides)
    return base


def test_evidence_dto_constructs_with_only_required_fields() -> None:
    dto = EvidenceDTO(**evidence_kwargs())

    assert dto.evidence_category is None
    assert dto.time_trust is None


def test_evidence_dto_carries_time_trust_spatial_and_device_health() -> None:
    t = now()
    dto = EvidenceDTO(
        **evidence_kwargs(
            evidence_category="SENSOR_RAW",
            validity_status="VALID",
            time_trust=TimeTrustDTO(
                captured_at=t,
                received_at=t + timedelta(milliseconds=50),
                time_source_type="PTP",
                clock_sync_status="SYNCED",
                time_trust_level="HIGH_TIME_TRUST",
            ),
            spatial_validity=SpatialValidityDTO(
                geo_location={"zone_id": "Zone_A", "x": 14.2, "y": 8.1},
                geo_crs="LOCAL_SITE",
            ),
            device_health=DeviceHealthDTO(
                device_health_snapshot={"battery_level": 82},
                historical_reliability_score=0.97,
            ),
        )
    )

    assert dto.evidence_category == EvidenceCategory.SENSOR_RAW
    assert dto.validity_status == EvidenceValidityStatus.VALID
    assert dto.time_trust.time_trust_level == "HIGH_TIME_TRUST"
    assert dto.spatial_validity.geo_crs == "LOCAL_SITE"
    assert dto.device_health.historical_reliability_score == 0.97


def test_evidence_dto_carries_attestation_and_ai_extraction_metadata() -> None:
    dto = EvidenceDTO(
        **evidence_kwargs(
            attestation=AttestationDTO(
                attestation_type="HUMAN_STEWARD",
                trust_upgrade_status="TRUST_UPGRADED_BY_HUMAN",
                attested_by="safety_steward_1",
                attested_at=now(),
            ),
            ai_extraction=AIExtractionMetadataDTO(
                is_extracted_evidence=True,
                extracted_from_evidence_id="ev-permit-doc-1",
                model_name="fixture-ocr-model",
                extraction_confidence=0.88,
            ),
        )
    )

    assert dto.attestation.trust_upgrade_status == "TRUST_UPGRADED_BY_HUMAN"
    assert dto.ai_extraction.is_extracted_evidence is True


def test_evidence_dto_rejects_invalid_evidence_category() -> None:
    with pytest.raises(ValidationError):
        EvidenceDTO(**evidence_kwargs(evidence_category="NOT_A_REAL_CATEGORY"))


def test_evidence_dto_rejects_invalid_validity_status() -> None:
    with pytest.raises(ValidationError):
        EvidenceDTO(**evidence_kwargs(validity_status="NOT_A_REAL_STATUS"))


def test_privacy_dto_blocks_key_destruction_under_legal_hold() -> None:
    with pytest.raises(ValidationError, match="legal_hold_status"):
        PrivacyDTO(
            contains_pii=True,
            privacy_lifecycle_status="PII_PRESENT",
            legal_hold_status=True,
            key_destroyed_at=now(),
        )

    dto = PrivacyDTO(
        contains_pii=True,
        privacy_lifecycle_status=PrivacyLifecycleStatus.PII_PRESENT,
        legal_hold_status=True,
    )
    assert dto.key_destroyed_at is None


def test_conflict_dto_carries_applied_weights() -> None:
    dto = ConflictDTO(
        conflict_status="CONFLICT_RESOLVED",
        conflict_resolution_strategy="DEVICE_HEALTH_WEIGHTED_SELECTION",
        applied_conflict_weights={"source_trust_weight": 0.3, "device_health_weight": 0.3},
    )

    assert dto.applied_conflict_weights["device_health_weight"] == 0.3


def test_source_metadata_rejects_invalid_source_trust_level() -> None:
    with pytest.raises(ValidationError):
        SourceMetadataDTO(
            source_type="sensor",
            source_id="src-1",
            source_trust_level="NOT_A_REAL_TRUST_LEVEL",
            ingested_at_utc=now(),
        )


def test_source_trust_level_has_exactly_the_nine_canonical_members() -> None:
    # Canonical source: 05_evidence_model.md Section 6.1.
    assert {member.value for member in SourceTrustLevel} == {
        "TRUSTED_SYSTEM",
        "VERIFIED_DEVICE",
        "VERIFIED_HUMAN",
        "VERIFIED_DOCUMENT",
        "THIRD_PARTY_VERIFIED",
        "AI_DERIVED",
        "ATTESTED_AI_DERIVED",
        "UNVERIFIED_SOURCE",
        "UNKNOWN_SOURCE",
    }


def test_evidence_validity_status_has_exactly_the_fifteen_canonical_members() -> None:
    # Canonical source: 05_evidence_model.md Section 9.2.
    assert {member.value for member in EvidenceValidityStatus} == {
        "VALID",
        "STALE",
        "EXPIRED",
        "REVOKED",
        "CONFLICTED",
        "UNVERIFIED",
        "SUPERSEDED",
        "INVALID",
        "ANONYMIZED",
        "PSEUDONYMIZED",
        "PII_REDACTED",
        "CRYPTO_SHREDDED",
        "RETENTION_EXPIRED",
        "ACCESS_RESTRICTED",
        "LEGAL_HOLD",
    }
