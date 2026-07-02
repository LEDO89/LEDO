# Applications

`apps/` contains application and service entrypoints.

`apps/` does not contain ontology source-of-truth logic.

Application entrypoints must call the shared framework/runtime and must not bypass validation, policy, Safety Gate, Evidence, or Audit.

Frontend is intentionally root-level under `frontend/`, not under `apps/`.
