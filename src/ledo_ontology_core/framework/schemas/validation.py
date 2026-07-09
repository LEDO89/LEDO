"""Validation DTO contracts from 01_common_schema_dto Section 10."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field

from ledo_ontology_core.framework.schemas.base import StrictDTO
from ledo_ontology_core.framework.schemas.context import TraceContextDTO
from ledo_ontology_core.framework.schemas.enums import ValidationStatus


class ValidationResultDTO(StrictDTO):
    validation_id: str
    input_ref: str
    validation_status: ValidationStatus
    validation_errors: list[str] = Field(default_factory=list)
    sanitized: bool
    sanitization_notes: list[str] = Field(default_factory=list)
    rate_limited: bool
    replay_detected: bool
    source_authenticated: bool
    source_authorized: bool
    validated_at_utc: datetime


class SanitizedInputDTO(StrictDTO):
    sanitized_input_id: str
    raw_input_ref: str
    sanitized_payload: dict[str, Any]
    removed_fields: list[str] = Field(default_factory=list)
    normalization_notes: list[str] = Field(default_factory=list)
    validation_result_ref: str
    trace_context: TraceContextDTO
    created_at_utc: datetime


class RateLimitContextDTO(StrictDTO):
    source_id: str
    limit_key: str
    allowed_rate: float = Field(ge=0)
    observed_rate: float = Field(ge=0)
    window_start_utc: datetime
    window_end_utc: datetime
    rate_limited: bool
    action_taken: str | None = None
