"""Evidence DTO contracts from 01_common_schema_dto Section 15."""

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
from ledo_ontology_core.framework.schemas.enums import ValidationStatus
from ledo_ontology_core.framework.schemas.refs import EntityRefDTO, LocationRefDTO


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

    @model_validator(mode="after")
    def reject_ai_as_evidence(self) -> "EvidenceDTO":
        if self.source_metadata.source_type.lower() in {"ai", "llm", "slm"}:
            raise ValueError("AI output may summarize evidence but cannot be Evidence")
        return self


class EvidenceBundleDTO(StrictDTO):
    bundle_id: str
    evidence_refs: list[str] = Field(default_factory=list)
    bundle_purpose: str
    summary: str | None = None
    minimum_required_evidence_met: bool
    conflicting_evidence_detected: bool
    created_at_utc: datetime
