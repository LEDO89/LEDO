"""Observability DTO contracts from 01_common_schema_dto Section 19."""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from ledo_ontology_core.framework.schemas.base import StrictDTO
from ledo_ontology_core.framework.schemas.enums import PathType, ReviewStatus


class MappingReviewDTO(StrictDTO):
    mapping_review_id: str
    mapping_proposal_ref: str
    reviewer_ref: str
    review_status: ReviewStatus
    review_comment: str | None = None
    approved_mapping: dict | None = None
    created_at_utc: datetime
    reviewed_at_utc: datetime | None = None


class LifecycleMetricDTO(StrictDTO):
    metric_id: str
    metric_name: str
    metric_value: float
    stage_name: str
    path_type: PathType
    timestamp_utc: datetime
    trace_id: str
    labels: dict[str, str] = Field(default_factory=dict)
