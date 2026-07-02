# Contracts

`contracts/` contains implementation alignment contracts shared across backend, frontend, workers, adapters, LLM/tool interfaces, external systems, and tests.

`contracts/` is not the architecture source of truth.

Contract maturity path:

```text
Pydantic Models -> JSON Schema -> Examples -> OpenAPI -> AsyncAPI -> Protobuf
```

OpenAPI is not OpenAI and does not imply paid API usage.

AsyncAPI is for asynchronous event/message contracts.

Protobuf is for future strongly typed high-performance integration contracts.
