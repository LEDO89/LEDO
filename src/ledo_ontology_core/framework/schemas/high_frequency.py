"""High-frequency / monitoring DTO contracts from 01_common_schema_dto Section 13.

Individual samples intentionally do not carry a full TraceContextDTO / VersionContextDTO
per the spec's Section 7.4 Monitoring Path Strategy — trace context is bundle-level only.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field

from ledo_ontology_core.framework.schemas.base import StrictDTO
from ledo_ontology_core.framework.schemas.context import (
    FreshnessDTO,
    SourceMetadataDTO,
    TraceContextDTO,
    VersionContextDTO,
)
from ledo_ontology_core.framework.schemas.enums import AggregationType, PathType
from ledo_ontology_core.framework.schemas.refs import EntityRefDTO, OntologyRefDTO


class TimeSeriesSampleDTO(StrictDTO):
    timestamp_utc: datetime
    value: Any
    unit: str | None = None
    quality: str
    sequence_number: int = Field(ge=0)
    sample_status: str


class TimeSeriesBundleInputDTO(StrictDTO):
    bundle_id: str
    source_metadata: SourceMetadataDTO
    subject_ref: EntityRefDTO
    signal_name: str
    unit: str | None = None
    samples: list[TimeSeriesSampleDTO] = Field(default_factory=list)
    window_start_utc: datetime
    window_end_utc: datetime
    sample_count: int = Field(ge=0)
    sampling_rate_hz: float | None = None
    trace_context: TraceContextDTO
    version_context: VersionContextDTO


class WindowedInputDTO(StrictDTO):
    window_id: str
    source_metadata: SourceMetadataDTO
    window_start_utc: datetime
    window_end_utc: datetime
    events: list[str] = Field(default_factory=list)
    aggregation_type: AggregationType
    statistics: dict[str, Any] = Field(default_factory=dict)
    trace_context: TraceContextDTO


class MonitoringPayloadDTO(StrictDTO):
    metric_name: str
    metric_value: float
    unit: str | None = None
    timestamp_utc: datetime
    quality: str
    is_threshold_crossed: bool
    threshold_ref: str | None = None
    summary_status: str


class MonitoringOnlyEventDTO(StrictDTO):
    monitoring_event_id: str
    source_metadata: SourceMetadataDTO
    subject_ref: EntityRefDTO
    monitoring_payload: MonitoringPayloadDTO
    freshness: FreshnessDTO
    trace_context: TraceContextDTO
    optional_ontology_ref: OntologyRefDTO | None = None
    path_type: PathType = PathType.MONITORING_ONLY


class EscalationTriggerDTO(StrictDTO):
    trigger_id: str
    source_event_ref: str
    trigger_reason: str
    from_path: PathType
    to_path: PathType
    threshold_ref: str | None = None
    detected_at_utc: datetime
    trace_context: TraceContextDTO
