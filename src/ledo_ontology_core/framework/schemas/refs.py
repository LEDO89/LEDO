"""Reference DTO contracts from 01_common_schema_dto Section 11."""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from ledo_ontology_core.framework.schemas.base import StrictDTO
from ledo_ontology_core.framework.schemas.enums import PolicyDecisionResult


class EntityRefDTO(StrictDTO):
    entity_id: str
    entity_type: str
    canonical_id: str | None = None
    display_name: str | None = None
    ontology_iri: str | None = None
    runtime_key: str | None = None


class LocationRefDTO(StrictDTO):
    location_id: str
    location_type: str
    site_id: str | None = None
    zone_id: str | None = None
    floor_id: str | None = None
    coordinates: dict[str, float] | None = None
    ontology_iri: str | None = None


class OntologyRefDTO(StrictDTO):
    ontology_iri: str
    ontology_class: str | None = None
    ontology_property: str | None = None
    domain_module: str | None = None
    runtime_key: str | None = None
    label: str | None = None


class EvidenceRefDTO(StrictDTO):
    evidence_id: str
    evidence_type: str
    source_id: str
    timestamp_utc: datetime
    confidence_score: float = Field(ge=0.0, le=1.0)
    summary: str | None = None


class PolicyRefDTO(StrictDTO):
    policy_id: str
    policy_type: str
    policy_version: str
    policy_bundle_version: str | None = None
    decision_result: PolicyDecisionResult | None = None


class ActorRefDTO(StrictDTO):
    actor_id: str
    actor_type: str
    role: str | None = None
    organization: str | None = None
    clearance_level: str | None = None
    ontology_iri: str | None = None
