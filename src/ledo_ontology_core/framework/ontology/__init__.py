"""Ontology boundary scaffolding for LEDO framework code."""

from ledo_ontology_core.framework.ontology.boundary import (
    OntologyBoundaryError,
    validate_module_dependency_direction,
)
from ledo_ontology_core.framework.ontology.iri import build_versioned_iri
from ledo_ontology_core.framework.ontology.modules import (
    OntologyModuleBoundary,
    OntologyModuleCategory,
    OntologyModuleRef,
)
from ledo_ontology_core.framework.ontology.namespaces import (
    CORE_CROSSCUTTING_NAMESPACE,
    CORE_UPPER_NAMESPACE,
    MODULE_NAMESPACES,
)

__all__ = [
    "CORE_CROSSCUTTING_NAMESPACE",
    "CORE_UPPER_NAMESPACE",
    "MODULE_NAMESPACES",
    "OntologyBoundaryError",
    "OntologyModuleBoundary",
    "OntologyModuleCategory",
    "OntologyModuleRef",
    "build_versioned_iri",
    "validate_module_dependency_direction",
]
