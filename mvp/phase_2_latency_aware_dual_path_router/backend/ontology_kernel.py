from __future__ import annotations

import re

OT = "https://ledo.example/ontology/mvp-phase-2#"
ABOX = "https://ledo.example/abox/mvp-phase-2/"


def iri(local_id: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_\-]", "_", local_id)
    return f"{ABOX}{safe}"


def cls(name: str) -> str:
    return f"{OT}{name}"


def rel(name: str) -> str:
    return f"{OT}{name}"


def literal(value: object) -> str:
    return str(value)

