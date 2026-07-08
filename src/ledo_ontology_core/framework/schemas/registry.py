"""Registry and governance DTO contracts from 01_common_schema_dto Section 19.

These DTOs *are* the registry entry shapes — their key vocabulary fields
(`action_type`, `event_type`, `state_type`) are the registry-managed values
themselves (06_registry_specs/), so they stay `str` by design, not by omission.
"""

from __future__ import annotations

from pydantic import Field

from ledo_ontology_core.framework.schemas.base import StrictDTO
from ledo_ontology_core.framework.schemas.enums import RiskLevel


class ActionTypeSpecDTO(StrictDTO):
    action_type: str
    description: str
    allowed_target_types: list[str] = Field(default_factory=list)
    required_evidence_types: list[str] = Field(default_factory=list)
    required_roles: list[str] = Field(default_factory=list)
    default_risk_level: RiskLevel
    requires_approval: bool
    allowed_external_systems: list[str] = Field(default_factory=list)
    expected_feedback_types: list[str] = Field(default_factory=list)


class EventTypeSpecDTO(StrictDTO):
    event_type: str
    domain_module: str
    allowed_sources: list[str] = Field(default_factory=list)
    allowed_subject_types: list[str] = Field(default_factory=list)
    default_lifecycle_path: str
    can_generate_evidence: bool
    can_generate_candidate: bool
    monitoring_only_allowed: bool
    emergency_trigger_allowed: bool
    supports_batching: bool
    supports_windowing: bool


class StateTypeSpecDTO(StrictDTO):
    state_type: str
    entity_type: str
    value_type: str
    allowed_values: list[str] = Field(default_factory=list)
    freshness_requirement_ms: int
    confidence_requirement: str | None = None
    is_safety_critical: bool
    requires_idempotent_update: bool
