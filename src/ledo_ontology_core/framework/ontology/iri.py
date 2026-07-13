"""IRI helpers for ontology module boundaries.

Source: 03_core_specifications/06_ontology_module_boundary/
6_ontology_module_boundary.md Section 21.
"""

from __future__ import annotations

import re

from ledo_ontology_core.framework.ontology.namespaces import MODULE_NAMESPACES

_LOCAL_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_VERSION_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.!~*'()/:-]*$")


def build_versioned_iri(
    module_id: str,
    version: str,
    local_name: str | None = None,
) -> str:
    """Build a governed versioned IRI for a module and optional local name.

    Version strings may include nested path segments such as `ifc/4.3`, matching
    Section 21.2's `mapping/ifc/4.3#` example. Parent-directory traversal is not
    allowed.
    """

    if module_id not in MODULE_NAMESPACES:
        raise ValueError(f"Unknown ontology module id: {module_id}")
    if ".." in version or "//" in version or version.endswith("/"):
        raise ValueError(f"Invalid ontology module version: {version}")
    if not _VERSION_RE.fullmatch(version):
        raise ValueError(f"Invalid ontology module version: {version}")
    if local_name is not None and not _LOCAL_NAME_RE.fullmatch(local_name):
        raise ValueError(f"Invalid ontology IRI local name: {local_name}")

    base = MODULE_NAMESPACES[module_id].removesuffix("#")
    versioned_base = f"{base}/{version}#"
    if local_name is None:
        return versioned_base
    return f"{versioned_base}{local_name}"
