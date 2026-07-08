"""Source-specific input DTO contracts from 01_common_schema_dto Section 20."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import Field

from ledo_ontology_core.framework.schemas.base import StrictDTO
from ledo_ontology_core.framework.schemas.context import ConfidenceDTO
from ledo_ontology_core.framework.schemas.high_frequency import TimeSeriesSampleDTO


class IndustrialRawInputDTO(StrictDTO):
    device_id: str
    tag: str
    register_address: str | None = None
    value: Any
    unit: str | None = None
    protocol: str
    timestamp_utc: datetime
    raw_payload: dict[str, Any]


class IndustrialTimeSeriesInputDTO(StrictDTO):
    device_id: str
    tag: str
    unit: str | None = None
    protocol: str
    samples: list[TimeSeriesSampleDTO] = Field(default_factory=list)
    sampling_rate_hz: float | None = None
    window_start_utc: datetime
    window_end_utc: datetime
    quality_summary: str | None = None
    raw_ref: str | None = None


class RobotTelemetryInputDTO(StrictDTO):
    robot_id: str
    mission_id: str | None = None
    mission_status: str | None = None
    battery_level: float | None = None
    pose: dict[str, Any] | None = None
    velocity: dict[str, Any] | None = None
    fault_code: str | None = None
    timestamp_utc: datetime


class RobotTelemetryBundleInputDTO(StrictDTO):
    robot_id: str
    mission_id: str | None = None
    telemetry_type: str
    samples: list[TimeSeriesSampleDTO] = Field(default_factory=list)
    window_start_utc: datetime
    window_end_utc: datetime
    sampling_rate_hz: float | None = None
    quality_summary: str | None = None


class ConstructionProcessInputDTO(StrictDTO):
    task_id: str
    work_package_id: str | None = None
    zone_id: str | None = None
    status: str
    permit_id: str | None = None
    worker_group_id: str | None = None
    updated_by: str
    timestamp_utc: datetime


class MobileContextInputDTO(StrictDTO):
    user_id: str
    device_id: str
    location: dict[str, Any] | None = None
    qr_scan_result: str | None = None
    ble_proximity: dict[str, Any] | None = None
    biometric_status: str | None = None
    photo_ref: str | None = None
    manual_confirmation: bool | None = None
    timestamp_utc: datetime


class DocumentParseInputDTO(StrictDTO):
    document_id: str
    document_type: str
    parsed_sections: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
    version: str | None = None
    source_uri: str | None = None
    parsed_at_utc: datetime


class LLMOutputInputDTO(StrictDTO):
    model_id: str
    prompt_id: str
    output_type: Literal[
        "Intent",
        "ActionCandidate",
        "EvidenceSummary",
        "MappingProposal",
        "Explanation",
    ]
    structured_output: dict[str, Any]
    retrieved_doc_refs: list[str] = Field(default_factory=list)
    confidence: ConfidenceDTO
    created_at_utc: datetime
