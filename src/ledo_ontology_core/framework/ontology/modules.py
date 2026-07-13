"""Ontology module reference and boundary structures.

Primary source: 03_core_specifications/06_ontology_module_boundary/
6_ontology_module_boundary.md Sections 3, 17, 21, 25, and 37.

These structures describe module boundaries. They intentionally do not contain
domain class/property catalogs. `OntologyModuleBoundary` is a Step 3 scaffold for
the import/reference subset of Section 25's full `OntologyModuleSpecDTO`; it does
not implement the governance, owner, status, validity-window, or review fields.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from ledo_ontology_core.framework.ontology.namespaces import MODULE_NAMESPACES


class OntologyModuleCategory(str, Enum):
    """Structural module categories from the module boundary DAG."""

    CORE_UPPER = "CORE_UPPER"
    CORE_CROSSCUTTING = "CORE_CROSSCUTTING"
    DOMAIN = "DOMAIN"
    MAPPING = "MAPPING"


_CORE_UPPER_MODULES = frozenset({"core_upper"})
_CORE_CROSSCUTTING_MODULES = frozenset({"core_cross"})
_MAPPING_MODULES = frozenset({"mapping"})


def infer_module_category(module_id: str) -> OntologyModuleCategory:
    if module_id in _CORE_UPPER_MODULES:
        return OntologyModuleCategory.CORE_UPPER
    if module_id in _CORE_CROSSCUTTING_MODULES:
        return OntologyModuleCategory.CORE_CROSSCUTTING
    if module_id in _MAPPING_MODULES:
        return OntologyModuleCategory.MAPPING
    return OntologyModuleCategory.DOMAIN


@dataclass(frozen=True, slots=True)
class OntologyModuleRef:
    """Reference to a governed ontology module."""

    module_id: str
    namespace: str
    category: OntologyModuleCategory
    version: str | None = None

    @classmethod
    def from_module_id(
        cls,
        module_id: str,
        *,
        version: str | None = None,
    ) -> "OntologyModuleRef":
        if module_id not in MODULE_NAMESPACES:
            raise ValueError(f"Unknown ontology module id: {module_id}")
        return cls(
            module_id=module_id,
            namespace=MODULE_NAMESPACES[module_id],
            category=infer_module_category(module_id),
            version=version,
        )


@dataclass(frozen=True, slots=True)
class OntologyModuleBoundary:
    """Reduced boundary policy for imports and references between modules.

    This is not the full Section 25 `OntologyModuleSpecDTO`; Step 3 only needs
    enough structure to validate namespace and dependency direction.
    """

    module: OntologyModuleRef
    allowed_import_modules: frozenset[str] = field(default_factory=frozenset)
    forbidden_import_modules: frozenset[str] = field(default_factory=frozenset)
    allowed_reference_modules: frozenset[str] = field(default_factory=frozenset)
    requires_mediation_for_domain_references: bool = True

    @classmethod
    def for_module_id(cls, module_id: str) -> "OntologyModuleBoundary":
        module = OntologyModuleRef.from_module_id(module_id)
        if module.category == OntologyModuleCategory.CORE_UPPER:
            return cls(
                module=module,
                forbidden_import_modules=frozenset(MODULE_NAMESPACES) - {module_id},
            )
        if module.category == OntologyModuleCategory.CORE_CROSSCUTTING:
            return cls(
                module=module,
                allowed_import_modules=frozenset({"core_upper"}),
                forbidden_import_modules=_domain_modules() | _MAPPING_MODULES,
            )
        if module.category == OntologyModuleCategory.MAPPING:
            return cls(
                module=module,
                allowed_import_modules=frozenset(MODULE_NAMESPACES) - {module_id},
            )
        return cls(
            module=module,
            allowed_import_modules=frozenset({"core_upper", "core_cross"}),
            allowed_reference_modules=frozenset({"core_upper", "core_cross"}),
            forbidden_import_modules=(
                _domain_modules() - {module_id}
            )
            | _MAPPING_MODULES,
        )


def _domain_modules() -> frozenset[str]:
    return frozenset(
        module_id
        for module_id in MODULE_NAMESPACES
        if infer_module_category(module_id) == OntologyModuleCategory.DOMAIN
    )
