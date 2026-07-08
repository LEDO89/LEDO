"""Governance DTO contracts from 01_common_schema_dto Section 19.

`EmergencyActionSpecDTO` lives in `schemas/emergency.py` (matches the lifecycle doc's
own Section 12 "Recommended Code Mapping"), not here.
"""

from __future__ import annotations

from pydantic import Field

from ledo_ontology_core.framework.schemas.base import StrictDTO


class CapabilitySpecDTO(StrictDTO):
    capability_id: str
    capability_type: str
    owner_entity_type: str
    constraints: dict
    required_conditions: list[str] = Field(default_factory=list)
    risk_level: str
    ontology_iri: str | None = None


class AdapterSpecDTO(StrictDTO):
    adapter_id: str
    adapter_type: str
    external_system_type: str
    supported_action_types: list[str] = Field(default_factory=list)
    protocol: str
    endpoint_ref: str | None = None
    timeout_policy: dict
    retry_policy: dict
    health_status: str
