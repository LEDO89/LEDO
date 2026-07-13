import pytest

from ledo_ontology_core.framework.ontology import (
    CORE_UPPER_NAMESPACE,
    MODULE_NAMESPACES,
    OntologyBoundaryError,
    OntologyModuleBoundary,
    OntologyModuleCategory,
    OntologyModuleRef,
    build_versioned_iri,
    validate_module_dependency_direction,
)


def test_valid_namespace_and_iri_construction() -> None:
    assert MODULE_NAMESPACES["core_upper"] == CORE_UPPER_NAMESPACE
    assert MODULE_NAMESPACES["robot"] == "https://example.org/ontology/robot#"

    assert (
        build_versioned_iri("robot", "2026-06", "Robot")
        == "https://example.org/ontology/robot/2026-06#Robot"
    )
    assert (
        build_versioned_iri("mapping", "ifc-4.3")
        == "https://example.org/ontology/mapping/ifc-4.3#"
    )
    assert (
        build_versioned_iri("mapping", "ifc/4.3")
        == "https://example.org/ontology/mapping/ifc/4.3#"
    )


def test_invalid_iri_inputs_fail() -> None:
    with pytest.raises(ValueError, match="Unknown ontology module"):
        build_versioned_iri("unknown", "2026-06")

    with pytest.raises(ValueError, match="Invalid ontology module version"):
        build_versioned_iri("robot", "../bad")

    with pytest.raises(ValueError, match="Invalid ontology IRI local name"):
        build_versioned_iri("robot", "2026-06", "Robot Mission")


def test_module_ref_and_boundary_are_structural_only() -> None:
    module = OntologyModuleRef.from_module_id("construction", version="0.1.0")
    boundary = OntologyModuleBoundary.for_module_id("construction")

    assert module.category == OntologyModuleCategory.DOMAIN
    assert boundary.allowed_import_modules == frozenset({"core_upper", "core_cross"})
    assert "robot" in boundary.forbidden_import_modules


def test_invalid_dependency_direction_fails() -> None:
    with pytest.raises(OntologyBoundaryError, match="Core Upper"):
        validate_module_dependency_direction("core_upper", "construction")

    with pytest.raises(OntologyBoundaryError, match="Core Crosscutting"):
        validate_module_dependency_direction("core_cross", "robot")

    with pytest.raises(OntologyBoundaryError, match="Mapping"):
        validate_module_dependency_direction("robot", "mapping")


def test_domain_module_cannot_import_peer_without_governed_mediation() -> None:
    with pytest.raises(OntologyBoundaryError, match="Domain-to-domain"):
        validate_module_dependency_direction("robot", "construction")

    assert validate_module_dependency_direction(
        "robot",
        "construction",
        via_mediation_concept=True,
    )
    assert validate_module_dependency_direction(
        "mapping",
        "construction",
        via_mapping_layer=True,
    )


def test_no_domain_class_or_property_meaning_is_created_by_framework_code() -> None:
    module = OntologyModuleBoundary.for_module_id("robot")

    assert not hasattr(module, "classes")
    assert not hasattr(module, "properties")
    assert "Robot" not in MODULE_NAMESPACES


def test_single_edge_validator_does_not_claim_full_cycle_detection() -> None:
    assert validate_module_dependency_direction(
        "robot",
        "construction",
        via_mediation_concept=True,
    )
    assert validate_module_dependency_direction(
        "construction",
        "robot",
        via_mediation_concept=True,
    )
