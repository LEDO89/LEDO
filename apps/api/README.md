# API Application

`apps/api/` is the future backend service entrypoint.

It is intended for a REST/API service such as FastAPI later.

Over time it may expose event ingestion, action review, approval, audit query, world state query, registry query, and dashboard APIs.

The API must call framework/runtime and must not bypass validation, policy, Safety Gate, Evidence, or Audit.
