"""Payload DTO contracts from 01_common_schema_dto Section 9.7."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from ledo_ontology_core.framework.schemas.base import StrictDTO
from ledo_ontology_core.framework.schemas.enums import ValidationStatus


class GenericPayloadDTO(StrictDTO):
    payload_type: str
    payload_schema_version: str
    payload: dict[str, Any] = Field(default_factory=dict)
    payload_hash: str | None = None
    validation_status: ValidationStatus
