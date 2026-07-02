# Domain Packs

`domain_packs/` mirrors `05_domain_ontology_modules/` at the top-level module name level.

`05_domain_ontology_modules/` is the human-readable ontology module specification area.

`src/ledo_ontology_core/domain_packs/` is the executable implementation area.

Domain packs are intended for executable schemas, mappings, loaders, validators, ontology bindings, fixtures, and sample events over time.

Empty modules are intentional placeholders for traceability.

Frontend, backend, and API code must not be duplicated inside `domain_packs/`. Shared technical layers belong in `src/ledo_ontology_core/framework/`, `apps/`, `frontend/`, `contracts/`, and `infra/`.
