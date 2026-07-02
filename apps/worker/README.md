# Worker Application

`apps/worker/` is the background worker entrypoint.

It is intended for later async jobs such as graph materialization, evidence indexing, registry sync, adapter polling, offline validation, snapshot generation, and event stream processing.

Workers must call framework/runtime and must not bypass validation, policy, Safety Gate, Evidence, or Audit.
