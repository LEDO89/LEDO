# Runtime Framework

`runtime/` coordinates executable pipeline flow.

Runtime may coordinate event ingestion, world state update, decision routing, Safety Gate, evidence binding, audit logging, and execution request creation.

Runtime must not bypass validation, policy, Safety Gate, Evidence, or Audit.

No LLM call is allowed in the Safety Gate hot path.
