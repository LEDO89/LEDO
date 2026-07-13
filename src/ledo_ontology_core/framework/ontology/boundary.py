"""Ontology module dependency boundary validation.

Primary source: 03_core_specifications/06_ontology_module_boundary/
6_ontology_module_boundary.md Sections 17-19 and 22-25.
"""

from __future__ import annotations

from ledo_ontology_core.framework.ontology.modules import (
    OntologyModuleCategory,
    OntologyModuleRef,
    infer_module_category,
)
from ledo_ontology_core.framework.ontology.namespaces import MODULE_NAMESPACES


class OntologyBoundaryError(ValueError):
    """Raised when an ontology module dependency crosses a forbidden boundary."""


def validate_module_dependency_direction(
    source_module: str | OntologyModuleRef,
    target_module: str | OntologyModuleRef,
    *,
    via_mapping_layer: bool = False,
    via_mediation_concept: bool = False,
) -> bool:
    """Validate dependency direction for one ontology module edge.

    `source_module` is the module declaring an import/reference to `target_module`.
    Direct domain-to-domain dependencies are rejected unless the caller explicitly
    marks the relationship as mediated through the mapping layer or a core
    mediation concept.

    This function validates one edge only. It does not perform the full DAG cycle
    detection required by Section 17.2; that requires a graph-level validator in a
    later ontology validation step.
    """

    source_id = _module_id(source_module)
    target_id = _module_id(target_module)
    _require_known_module(source_id)
    _require_known_module(target_id)

    if source_id == target_id:
        return True

    source_category = infer_module_category(source_id)
    target_category = infer_module_category(target_id)

    if source_category == OntologyModuleCategory.CORE_UPPER:
        raise OntologyBoundaryError("Core Upper must not import other LEDO modules")

    if source_category == OntologyModuleCategory.CORE_CROSSCUTTING:
        if target_category == OntologyModuleCategory.CORE_UPPER:
            return True
        raise OntologyBoundaryError(
            "Core Crosscutting may import Core Upper only"
        )

    if source_category == OntologyModuleCategory.DOMAIN:
        if target_category in {
            OntologyModuleCategory.CORE_UPPER,
            OntologyModuleCategory.CORE_CROSSCUTTING,
        }:
            return True
        if target_category == OntologyModuleCategory.DOMAIN:
            if via_mapping_layer or via_mediation_concept:
                return True
            raise OntologyBoundaryError(
                "Domain-to-domain dependency requires a Mapping layer or "
                "Mediation Concept"
            )
        raise OntologyBoundaryError("Domain modules must not import Mapping modules")

    if source_category == OntologyModuleCategory.MAPPING:
        return True

    raise OntologyBoundaryError(
        f"Unsupported ontology dependency: {source_id} -> {target_id}"
    )


def _module_id(module: str | OntologyModuleRef) -> str:
    if isinstance(module, OntologyModuleRef):
        return module.module_id
    return module


def _require_known_module(module_id: str) -> None:
    if module_id not in MODULE_NAMESPACES:
        raise OntologyBoundaryError(f"Unknown ontology module id: {module_id}")
