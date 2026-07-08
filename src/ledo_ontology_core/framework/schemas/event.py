"""Input and event DTO contracts from 01_common_schema_dto Section 12."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field

from ledo_ontology_core.framework.schemas.base import StrictDTO
from ledo_ontology_core.framework.schemas.context import (
    ConfidenceDTO,
    FreshnessDTO,
    SourceMetadataDTO,
    TraceContextDTO,
    VersionContextDTO,
)
from ledo_ontology_core.framework.schemas.enums import PathType
from ledo_ontology_core.framework.schemas.refs import EntityRefDTO, LocationRefDTO


class RawInputDTO(StrictDTO):
    raw_input_id: str
    source_metadata: SourceMetadataDTO
    raw_payload: dict[str, Any]
    received_at_utc: datetime
    raw_format: str
    encoding: str | None = None
    checksum: str | None = None
    trace_context: TraceContextDTO


class CanonicalEventEnvelopeDTO(StrictDTO):
    event_id: str
    event_type: str
    source_metadata: SourceMetadataDTO
    subject_ref: EntityRefDTO
    location_ref: LocationRefDTO | None = None
    timestamp_utc: datetime
    payload: dict[str, Any]
    confidence: ConfidenceDTO
    freshness: FreshnessDTO
    trace_context: TraceContextDTO
    version_context: VersionContextDTO
    emergency_hint: bool = False
    criticality_hint: str | None = None
    lifecycle_path_hint: str | None = None


class PathClassificationDTO(StrictDTO):
    path_type: PathType
    classification_reason: str
    risk_hint: str | None = None
    emergency_detected: bool
    monitoring_only_allowed: bool
    standard_path_required: bool
    classified_at_utc: datetime


class EventTypeDTO(StrictDTO):
    event_type: str
    event_category: str
    domain_module: str
    allowed_subject_types: list[str] = Field(default_factory=list)
    default_lifecycle_path: str
    requires_evidence: bool
    can_generate_candidate: bool
