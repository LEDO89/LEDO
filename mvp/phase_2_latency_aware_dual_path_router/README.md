# LEDO MVP Phase 2: Latency-Aware Dual-Path Router

This is an isolated MVP sandbox under `mvp/`. It is not the formal `src/` implementation.

This phase validates an enterprise pilot-grade LEDO War Room flow where critical real-time safety events bypass LLM latency and human pre-approval, while async planning may use a non-authoritative LLM candidate through a human approval loop.

## What This MVP Proves

- Critical real-time safety events bypass LLM.
- Critical real-time safety events bypass human pre-approval.
- Critical real-time safety events use deterministic `RuleEmergencyCore`.
- `RuleEmergencyCore` is explicit, inspectable, rule-based, and independently testable.
- Async planning events may use `LLMCandidateAdapter`.
- LLM candidates are non-authoritative.
- Async planning requires human approval before `ApprovedAction`.
- Safety Gate hot path never calls LLM, SPARQL, Graph DB, UI, or external APIs.
- Graph DB is mandatory in the stack.
- Ontology graph projection is generated from Graph DB query results.
- War Room UI is included with ReactFlow.
- External execution is mock only.
- No real robot, PLC, SCADA, access-control, or physical control occurs.
- `ExecutionRequest` is not `PhysicalCommand`.
- `PhysicalCommand` is never created.

## Architecture Coverage

All LEDO layers 0 through 12 are represented in code, state, audit trace, and UI payload:

0 Observability/Audit/Trace, 1 Presentation, 2 API Gateway, 3 Governance/Policy/Security, 4 Ontology Kernel, 5 Semantic Memory, 6 Real-Time World State, 7 Domain Agent/Rule Core, 8 Decision Router, 9 Safety Gate, 10 Cyber-Physical Core, 11 External Control Integration, 12 Physical World Boundary.

## Local Stack

- Backend: FastAPI, Uvicorn, Pydantic, REST, SSE
- Frontend: Next.js, React, TypeScript, ReactFlow
- World State: Redis
- Event Bus: Redpanda Kafka-compatible broker
- Persistence: PostgreSQL
- Semantic Graph: RDF triples, Apache Jena Fuseki, SPARQL query boundary
- Policy: OPA/Rego plus deterministic local evaluator mirroring the Rego policy
- Observability: structured audit trace with `trace_id`, `event_id`, `decision_case_id`, and idempotency keys

The demo and unit tests use in-process fallbacks when Docker services are not running. The fallback graph store is still queried to create the War Room graph projection; it is not hardcoded UI graph data.

## Run Infra

```bash
cd mvp/phase_2_latency_aware_dual_path_router
docker compose up -d
```

URLs:

- Backend: http://localhost:8765
- Frontend: http://localhost:3000
- Fuseki: http://localhost:3030
- OPA: http://localhost:8181
- PostgreSQL: localhost:5432
- Redis: localhost:6379
- Redpanda: localhost:9092

## Run Backend

```bash
cd mvp/phase_2_latency_aware_dual_path_router
python3 -m pip install -r requirements.txt
uvicorn backend.app:app --reload --port 8765
```

## Run Frontend

```bash
cd mvp/phase_2_latency_aware_dual_path_router/frontend
npm install
npm run dev
```

The local MVP backend allows browser requests from `localhost` and `127.0.0.1`
on frontend ports `3000` and `3001`. This CORS configuration is for local MVP
development only and is not a production-safe CORS policy.

## Run Demo

```bash
cd mvp/phase_2_latency_aware_dual_path_router
python3 run_demo.py
```

## Run Tests

```bash
cd mvp/phase_2_latency_aware_dual_path_router
python3 -m pytest tests
```

## API

- `GET /api/state`
- `POST /api/scenario/critical-collision`
- `POST /api/scenario/async-replan`
- `POST /api/approval/approve`
- `POST /api/approval/reject`
- `POST /api/reset`
- `GET /api/graph`
- `GET /api/audit`
- `GET /api/execution-status`
- `GET /api/rule-trace`
- `GET /api/events/stream`

## Known Limitations

- The local tests use service fallbacks if Redis/PostgreSQL/Fuseki/OPA/Redpanda are unavailable.
- The OPA HTTP call is represented by a deterministic evaluator that mirrors `backend/policy_rules.rego`; full OPA request wiring is left integration-ready.
- The MVP uses placeholder scenario facts only. Real domain thresholds, robot behavior semantics, approval authority rules, and field procedures require human domain expert governance.
- The mock adapter never sends real physical commands.
