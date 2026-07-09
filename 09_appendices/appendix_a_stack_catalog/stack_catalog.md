---
title: Stack Catalog
version: 1.2
status: populated
owner: platform-ontology
language: en
last_updated: 2026-07-06
---

# Stack Catalog

## Purpose

Catalog reference items and examples. Do not treat this appendix as executable runtime code.

This catalog consolidates the "Recommended Initial Stack Mapping" sections already defined per layer in `02_layer_stack_mapping/00`–`12`. It is a convenience index, not a new source of truth. If this catalog and a `02_layer_stack_mapping/*.md` file ever disagree, the per-layer stack mapping document wins (see `00_master_architecture/README.md` Source of Truth Principle).

## Notes

This document is intentionally written in English so that Codex and other coding agents can use it as a non-authoritative index.

## Initial Technology Stack by Layer

| Layer | Source Document | Initial Technology Choices |
| --- | --- | --- |
| 0. Observability / Audit / Trace | `02_layer_stack_mapping/00_observability_audit_trace_stack_mapping.md` | OpenTelemetry, Prometheus, Grafana, Loki or OpenSearch, Jaeger or Tempo, PostgreSQL (audit + event store), PROV-O (provenance model), structured JSON logs |
| 1. Experience / Presentation | `02_layer_stack_mapping/01_experience_presentation_stack_mapping.md` | Next.js, React, TypeScript, Tailwind CSS, shadcn/ui, TanStack Query, Zustand, WebSocket/SSE, ECharts, React Flow, Cytoscape.js, Three.js + React Three Fiber, Mapbox GL JS |
| 2. API Gateway | `02_layer_stack_mapping/02_api_gateway_stack_mapping.md` | FastAPI, Pydantic, REST first, WebSocket + SSE, OAuth2/OIDC-compatible JWT, OpenAPI, NGINX or Traefik, OpenTelemetry middleware |
| 3. Governance / Policy / Security | `02_layer_stack_mapping/03_governance_policy_security_stack_mapping.md` | Keycloak (or simple OIDC), OAuth2/OIDC, JWT, RBAC first (ABAC later), OPA/Rego, PostgreSQL-backed approval tables, Git-versioned policy files |
| 4. Core Ontology Kernel | `02_layer_stack_mapping/04_core_ontology_kernel_stack_mapping.md` | OWL 2, RDF/RDFS, SHACL, SPARQL, BFO-light alignment, SOSA/SSN, PROV-O, QUDT, Protégé, RDFLib + OWLReady2, HermiT or Pellet (offline only), pySHACL |
| 5. Knowledge & Semantic Memory | `02_layer_stack_mapping/05_knowledge_semantic_memory_stack_mapping.md` | Apache Jena Fuseki (SPARQL endpoint), Neo4j (graph read model), PostgreSQL, pgvector, MinIO or local object storage, PROV-O |
| 6. Real-Time World State | `02_layer_stack_mapping/06_real_time_world_state_stack_mapping.md` | MQTT, Kafka or Redpanda, Redis (current state), TimescaleDB (history), Kafka Streams first (Flink later), FastAPI current-state API |
| 7. Distributed Domain Agent | `02_layer_stack_mapping/07_distributed_domain_agent_stack_mapping.md` | Python async services, Ollama (local SLM serving), ONNX Runtime (later), Redis belief cache, Kafka or internal async broker, OPA/Rego precheck |
| 8. Decision Router / Escalation | `02_layer_stack_mapping/08_decision_router_escalation_stack_mapping.md` | Python rule-based decision table, OPA/Rego, explicit Python state machine, Redis Queue or Kafka topic routing |
| 9. Approved Action / Safety Gate | `02_layer_stack_mapping/09_approved_action_safety_gate_stack_mapping.md` | Python validation service, Pydantic DTOs, pySHACL (target-specific), OPA/Rego, PostgreSQL (approval records + audit), Redis (state freshness), OpenTelemetry |
| 10. Unified Cyber-Physical Core | `02_layer_stack_mapping/10_unified_cyber_physical_core_stack_mapping.md` | Pydantic schemas, UUID + UTC timestamps, explicit Python enum state machine, PostgreSQL append-only event table + transactional outbox, idempotency key table |
| 11. Execution Request & External Control Integration | `02_layer_stack_mapping/11_execution_request_external_control_integration_stack_mapping.md` | Python FastAPI/async adapter service, Pydantic DTOs, PostgreSQL outbox or Redis queue, REST adapter first, MQTT (notification), interface-stub adapters before real Fleet/ROS2/OPC-UA |
| 12. Physical World | `02_layer_stack_mapping/12_physical_world_stack_mapping.md` | Simulated physical entities first, MQTT-based IoT sensor events, manual/interface-stub worker location and equipment status, mobile/web notification |

## Non-Production Boundary Guidance (see `AGENTS.md` Mock First Rule)

`AGENTS.md`'s Mock First Rule distinguishes two categories, and this catalog follows the same distinction. Do not read either category as "not real code" — both require complete, tested implementations; the distinction is about which external systems they are allowed to talk to.

- **Physical/external control systems** (robot middleware, fleet manager, PLC, SCADA, access-control systems, external sensor gateway, external equipment controller — mainly Layers 11 and 12): using an interface-stub or dry-run implementation instead of real dispatch is a Constitution-level safety requirement (Safety Boundary Rule). These stay interface-stub or dry-run until explicit human approval, independent of how far implementation has progressed elsewhere. This is a permanent architectural boundary, not a temporary scope cut.
- **Infrastructure backing stores** (policy engine, message broker, database, graph database, triple store — appearing across Layers 3–10): starting with in-memory or lightweight implementations is a pragmatic sequencing choice, not a safety rule. These must be replaced with their real implementation as soon as the corresponding schema/contract stabilizes, and must not be left as interface stubs indefinitely — doing so risks schema drift and integration failures that only surface when the real backend is finally wired in.
