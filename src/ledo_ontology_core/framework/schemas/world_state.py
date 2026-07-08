"""World state DTO contracts from 01_common_schema_dto Section 15."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field

from ledo_ontology_core.framework.schemas.base import StrictDTO
from ledo_ontology_core.framework.schemas.context import (
    ConfidenceDTO,
    FreshnessDTO,
    TraceContextDTO,
)
from ledo_ontology_core.framework.schemas.refs import EntityRefDTO


class WorldStateDTO(StrictDTO):
    state_id: str
    entity_ref: EntityRefDTO
    state_type: str
    state_value: Any
    source_ref: str
    evidence_ref: str | None = None
    timestamp_utc: datetime
    freshness: FreshnessDTO
    confidence: ConfidenceDTO
    valid_until: datetime | None = None
    trace_context: TraceContextDTO
    version: str


class WorldStateUpdateDTO(StrictDTO):
    update_id: str
    entity_ref: EntityRefDTO
    previous_state: WorldStateDTO | None = None
    new_state: WorldStateDTO
    change_reason: str
    evidence_refs: list[str] = Field(default_factory=list)
    updated_by: str
    updated_at_utc: datetime
    trace_context: TraceContextDTO
    idempotency_key: str
    state_version: str
    expected_previous_version: str | None = None
    deduplication_window_ms: int = Field(ge=0)


class StateSnapshotDTO(StrictDTO):
    snapshot_id: str
    site_id: str
    snapshot_time_utc: datetime
    states: list[WorldStateDTO] = Field(default_factory=list)
    ontology_version: str
    policy_context_version: str | None = None
    created_at_utc: datetime
