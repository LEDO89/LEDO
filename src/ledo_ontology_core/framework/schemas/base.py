"""Base DTO contracts from 01_common_schema_dto Section 9.1."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class StrictDTO(BaseModel):
    """Shared Pydantic settings for DTO contracts."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class BaseDTO(StrictDTO):
    id: str
    created_at_utc: datetime = Field(default_factory=utc_now)
    updated_at_utc: datetime | None = None
    schema_version: str
    lifecycle_version: str
    metadata: dict[str, Any] = Field(default_factory=dict)
