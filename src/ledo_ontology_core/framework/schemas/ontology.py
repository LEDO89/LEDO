"""Ontology binding DTO contracts from 01_common_schema_dto Section 14."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field

from ledo_ontology_core.framework.schemas.base import StrictDTO
from ledo_ontology_core.framework.schemas.context import SourceMetadataDTO, TraceContextDTO
from ledo_ontology_core.framework.schemas.enums import BindingStatus
from ledo_ontology_core.framework.schemas.event import CanonicalEventEnvelopeDTO
from ledo_ontology_core.framework.schemas.refs import EntityRefDTO


class CanonicalIdentityDTO(StrictDTO):
    raw_identifier: str
    canonical_id: str
    canonical_iri: str | None = None
    runtime_key: str | None = None
    alias_matched: bool = False
    mapping_confidence: float | None = None
    mapping_table_version: str | None = None


class OntologyBindingDTO(StrictDTO):
    binding_id: str
    entity_ref: EntityRefDTO
    ontology_class: str | None = None
    ontology_property: str | None = None
    ontology_individual: str | None = None
    domain_module: str
    runtime_key: str | None = None
    binding_confidence: float | None = None
    binding_status: BindingStatus
    binding_errors: list[str] = Field(default_factory=list)


class OntologyBoundEventDTO(StrictDTO):
    event_id: str
    canonical_event: CanonicalEventEnvelopeDTO
    ontology_bindings: list[OntologyBindingDTO] = Field(default_factory=list)
    subject_ref: EntityRefDTO
    state_type: str | None = None
    event_semantics: dict[str, Any] = Field(default_factory=dict)
    evidence_candidate: dict[str, Any] | None = None
    trace_context: TraceContextDTO


class UnclassifiedEntityDTO(StrictDTO):
    unclassified_id: str
    raw_identifier: str
    source_metadata: SourceMetadataDTO
    observed_payload: dict[str, Any]
    possible_entity_types: list[str] = Field(default_factory=list)
    reason: str
    risk_blocked: bool
    mapping_review_required: bool
    created_at_utc: datetime


class MappingProposalDTO(StrictDTO):
    proposal_id: str
    unclassified_entity_id: str
    proposed_canonical_id: str | None = None
    proposed_ontology_class: str | None = None
    proposed_domain_module: str | None = None
    reasoning_summary: str
    supporting_evidence_refs: list[str] = Field(default_factory=list)
    confidence_score: float
    requires_human_approval: bool
