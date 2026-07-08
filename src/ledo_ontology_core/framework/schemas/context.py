"""Context DTO contracts from 01_common_schema_dto Section 9."""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from ledo_ontology_core.framework.schemas.base import StrictDTO
from ledo_ontology_core.framework.schemas.enums import ValidationStatus


class TraceContextDTO(StrictDTO):
    trace_id: str
    correlation_id: str | None = None
    causation_id: str | None = None
    parent_span_id: str | None = None
    span_id: str | None = None
    request_id: str | None = None


class VersionContextDTO(StrictDTO):
    schema_version: str
    lifecycle_version: str
    ontology_version: str | None = None
    policy_bundle_version: str | None = None
    mapping_table_version: str | None = None
    adapter_version: str | None = None


class SourceMetadataDTO(StrictDTO):
    # DOMAIN_DECISION_REQUIRED: source_type has no closed value list in
    # 01_common_schema_dto.md Section 9.4 — kept as str, not an enum.
    source_type: str
    source_id: str
    source_name: str | None = None
    source_protocol: str | None = None
    source_system: str | None = None
    source_trust_level: str
    ingested_at_utc: datetime
    raw_ref: str | None = None


class FreshnessDTO(StrictDTO):
    timestamp_utc: datetime
    ingested_at_utc: datetime
    freshness_ms: int = Field(ge=0)
    valid_until: datetime | None = None
    is_stale: bool


class ConfidenceDTO(StrictDTO):
    confidence_score: float = Field(ge=0.0, le=1.0)
    # DOMAIN_DECISION_REQUIRED: confidence_level has no closed value list in
    # 01_common_schema_dto.md Section 9.6 — kept as str, not an enum.
    confidence_level: str
    confidence_reason: str | None = None
    source_quality: str | None = None
    validation_status: ValidationStatus
