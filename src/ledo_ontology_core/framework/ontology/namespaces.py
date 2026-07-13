"""Namespace constants from the Ontology Module Boundary specification.

Source: 03_core_specifications/06_ontology_module_boundary/
6_ontology_module_boundary.md Section 21.

The constants identify governed module namespaces only. They do not create OWL
classes, properties, domain rules, or physical-control semantics.
"""

from __future__ import annotations

CORE_UPPER_NAMESPACE = "https://example.org/ontology/core-upper#"
CORE_CROSSCUTTING_NAMESPACE = "https://example.org/ontology/core-crosscutting#"

MODULE_NAMESPACES: dict[str, str] = {
    "core_upper": CORE_UPPER_NAMESPACE,
    "core_cross": CORE_CROSSCUTTING_NAMESPACE,
    "construction": "https://example.org/ontology/construction#",
    "industrial": "https://example.org/ontology/industrial#",
    "robot": "https://example.org/ontology/robot#",
    "policy": "https://example.org/ontology/policy#",
    "ai": "https://example.org/ontology/ai#",
    "evidence": "https://example.org/ontology/evidence#",
    "event": "https://example.org/ontology/event#",
    "state": "https://example.org/ontology/state#",
    "action": "https://example.org/ontology/action#",
    "mapping": "https://example.org/ontology/mapping#",
}

INITIAL_ONTOLOGY_MODULES: frozenset[str] = frozenset(MODULE_NAMESPACES)
