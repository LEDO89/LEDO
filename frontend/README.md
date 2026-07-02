# Frontend

`frontend/` is the root-level first-class Palantir-grade operator UI product surface.

It is intentionally not under `apps/`.

Frontend must consume backend/API contracts.

Frontend must not contain ontology source-of-truth logic.

Frontend must not bypass backend validation, policy, Safety Gate, Evidence, or Audit.

No frontend dependencies are added in this patch.
