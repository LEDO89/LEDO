from __future__ import annotations

from .schemas import SiteEvent


class EventBus:
    """Kafka-compatible adapter boundary.

    Redpanda is provided in docker-compose. Local demo/tests use the same event
    envelope shape through this in-memory adapter when kafka-python is absent.
    """

    def __init__(self) -> None:
        self.published: list[dict] = []

    def publish_site_event(self, event: SiteEvent) -> dict:
        envelope = {
            "topic": "ledo.mvp.site-events",
            "key": event.id,
            "trace_id": event.trace_id,
            "payload": event.model_dump(mode="json"),
        }
        self.published.append(envelope)
        return envelope

    def reset(self) -> None:
        self.published.clear()

