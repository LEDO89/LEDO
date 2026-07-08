"""Action candidate DTO contracts from 01_common_schema_dto Section 16."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field

from ledo_ontology_core.framework.schemas.base import StrictDTO
from ledo_ontology_core.framework.schemas.context import ConfidenceDTO, TraceContextDTO
from ledo_ontology_core.framework.schemas.enums import RiskLevel
from ledo_ontology_core.framework.schemas.refs import EntityRefDTO, LocationRefDTO


class IntentDTO(StrictDTO):
    intent_id: str
    intent_type: str
    requested_by: str
    target_ref: EntityRefDTO
    reason: str
    source_event_ref: str | None = None
    confidence: ConfidenceDTO
    trace_context: TraceContextDTO


class ActionCandidateDTO(StrictDTO):
    candidate_id: str
    # action_type is a registry-managed vocabulary (06_registry_specs/action_registry),
    # not a fixed enum — new action types are added via registry entries, not code
    # changes. Kept as str intentionally.
    action_type: str
    target_ref: EntityRefDTO
    target_location: LocationRefDTO | None = None
    proposed_by: str
    reason: str
    risk_level: RiskLevel
    evidence_refs: list[str] = Field(default_factory=list)
    confidence: ConfidenceDTO
    constraints: dict[str, Any] = Field(default_factory=dict)
    required_capabilities: list[str] = Field(default_factory=list)
    requires_approval: bool
    created_at_utc: datetime
    trace_context: TraceContextDTO
