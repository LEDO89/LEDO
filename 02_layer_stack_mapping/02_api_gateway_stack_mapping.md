# **Ontology Centric “API Gateway” Stack Mapping**

## **Layer 2\. API Gateway Layer**

─ Core Position  
└── API Gateway is the controlled entry point of the ontology-centric system  
└── It connects user interfaces, mobile applications, dashboards, digital twins, agents, external systems, robot middleware, fleet managers, and backend services  
└── It provides controlled access, authentication, request validation, routing, versioning, real-time delivery, and API contracts  
└── It does not define ontology truth  
└── It does not make final safety decisions  
└── It does not execute physical commands  
└── It does not replace Governance / Policy / Security Layer  
└── It does not replace Execution Request & External Control Integration Layer

---

## **Core Role**

└── Provide a controlled entry point for all frontend, mobile, dashboard, agent, and external system requests  
└── Validate request schema, identity, permissions, API version, and routing target  
└── Expose backend capabilities through stable APIs  
└── Deliver real-time events to the frontend and operational consoles  
└── Protect backend services from direct uncontrolled access  
└── Standardize request / response contracts across the system  
└── Route requests to ontology services, world state services, knowledge services, decision services, safety gate services, execution services, and audit services

---

## **Core Technologies**

└── FastAPI  
└── REST API  
└── WebSocket  
└── SSE  
└── OpenAPI  
└── Pydantic  
└── OAuth2  
└── OIDC  
└── JWT  
└── API Rate Limiting  
└── API Versioning  
└── Schema Validation  
└── Request Validation  
└── Response Validation  
└── CORS Control  
└── Middleware  
└── Reverse Proxy  
└── API Gateway Routing  
└── OpenTelemetry Integration

---

## **Optional Technologies**

└── GraphQL  
└── gRPC  
└── Socket.IO  
└── Envoy  
└── NGINX  
└── Traefik  
└── Kong  
└── Istio  
└── Linkerd  
└── Service Mesh  
└── API Key Management  
└── Client Certificate Authentication  
└── mTLS  
└── OpenAPI TypeScript Client Generation  
└── GraphQL Federation  
└── AsyncAPI for event contracts

---

## **API Surface Stack**

└── Ontology API  
└── Knowledge Graph API  
└── World State API  
└── Realtime Event API  
└── Decision Case API  
└── Action Candidate API  
└── Approval API  
└── Safety Gate API  
└── Execution Request API  
└── External System Status API  
└── Audit API  
└── User / Role / Permission API  
└── Notification API  
└── Digital Twin API  
└── Graph Explorer API  
└── Workflow API

---

## **REST API Stack**

└── FastAPI Router  
└── Pydantic Request DTO  
└── Pydantic Response DTO  
└── OpenAPI Schema  
└── HTTP Status Code Policy  
└── Pagination  
└── Filtering  
└── Sorting  
└── Idempotency Key  
└── Correlation ID  
└── Trace ID  
└── Request Timeout  
└── Error Response Schema

REST API Usage:  
└── Standard request / response operations  
└── Querying decision cases  
└── Submitting approval decisions  
└── Loading graph data  
└── Loading digital twin state  
└── Retrieving audit records  
└── Creating execution requests through approved backend workflow

---

## **WebSocket / SSE Stack**

└── FastAPI WebSocket  
└── SSE Endpoint  
└── Realtime Event Stream  
└── Subscription Channel  
└── Client Session Tracking  
└── Heartbeat / Ping  
└── Reconnect Policy  
└── Backpressure Handling  
└── Event Sequence Number  
└── Event Replay Token  
└── Stale Connection Detection

Realtime Event Types:  
└── WorldStateUpdated  
└── RiskStateChanged  
└── DecisionCaseCreated  
└── ApprovalRequested  
└── ApprovalStatusChanged  
└── ExecutionRequestCreated  
└── ExecutionStatusUpdated  
└── ExternalControlFeedbackReceived  
└── AlertRaised  
└── ManualOverrideTriggered  
└── OntologyChanged  
└── PolicyChanged

Usage Rule:  
└── WebSocket is used for bidirectional real-time interaction  
└── SSE is used for server-to-client streaming  
└── REST is used for normal request / response queries

---

## **GraphQL Stack**

└── GraphQL API optional  
└── GraphQL Schema  
└── Typed Query  
└── GraphQL Resolver  
└── Query Depth Limit  
└── Query Complexity Limit  
└── Permission-aware Resolver  
└── GraphQL Federation optional

Recommended Usage:  
└── Optional for flexible frontend graph queries  
└── Useful for dashboard aggregation  
└── Useful for graph explorer and digital twin panels  
└── Not required for MVP

Boundary:  
└── GraphQL should not expose unrestricted graph traversal  
└── GraphQL must still pass authorization, rate limit, query complexity, and backend permission checks

---

## **gRPC Stack**

└── gRPC Service  
└── Protobuf Schema  
└── Internal Service Communication  
└── High-throughput Service Calls  
└── Streaming RPC optional  
└── mTLS optional  
└── Service-to-Service Authentication

Recommended Usage:  
└── Optional for internal backend service communication  
└── Useful for agent service, inference service, execution service, or high-throughput external integration  
└── Not required for first MVP

Boundary:  
└── gRPC is not the primary frontend protocol  
└── Browser UI should normally use REST, WebSocket, SSE, or GraphQL through FastAPI

---

## **Authentication Stack**

└── OAuth2  
└── OIDC  
└── JWT  
└── Access Token  
└── Refresh Token  
└── Token Introspection  
└── User Session  
└── Service Account Token  
└── API Key optional  
└── mTLS optional for service-to-service or external system integration

Identity Providers:  
└── Keycloak  
└── Auth0 optional  
└── Azure AD optional  
└── Google Workspace optional  
└── Enterprise SSO optional

Authentication Rule:  
└── Every user, agent, service, and external system must have a verifiable identity

---

## **Authorization Stack**

└── Role-based Access Control  
└── Attribute-based Access Control  
└── Permission Scope  
└── Resource Scope  
└── Project Scope  
└── Site Scope  
└── Entity-level Access Check  
└── API-level Permission Check  
└── Action-level Permission Check

Boundary:  
└── API Gateway can enforce coarse-grained authorization  
└── Fine-grained policy decisions belong to Layer 3 Governance / Policy / Security  
└── High-risk action approval belongs to Layer 9 Approved Action / Safety Gate

Example:  
└── API Gateway checks whether the user can access approval APIs  
└── Governance Layer checks whether the user has permission to approve this specific high-risk action  
└── ApprovalDecision produces ApprovedAction; Safety Gate later consumes ApprovedAction plus RuntimeValidationResult and issues SafetyGatePass or SafetyGateBlock

---

## **Request Validation Stack**

└── Pydantic DTO  
└── JSON Schema  
└── OpenAPI Contract  
└── Required Field Validation  
└── Type Validation  
└── Enum Validation  
└── UUID Validation  
└── Timestamp Validation  
└── Request Size Limit  
└── File Upload Validation  
└── Schema Version Validation  
└── Input Sanitization  
└── Prompt Injection Check for text-bearing requests

Validation Rule:  
└── Invalid request must be rejected before reaching ontology, agent, decision, safety, or execution services

---

## **Response Validation Stack**

└── Pydantic Response Model  
└── DTO Contract  
└── OpenAPI Schema  
└── Field-level Redaction  
└── Permission-aware Response Filtering  
└── Sensitive Data Masking  
└── Error Schema  
└── Trace ID in Response  
└── Correlation ID in Response

Response Rule:  
└── Frontend receives structured DTOs, not raw database records or internal service objects

---

## **API Versioning Stack**

└── URI Versioning  
└── Header Versioning optional  
└── OpenAPI Version  
└── DTO Version  
└── Backward Compatibility Policy  
└── Deprecation Policy  
└── Breaking Change Review  
└── Client Compatibility Check  
└── TypeScript Client Regeneration

Versioning Example:  
└── /api/v1/world-state  
└── /api/v1/decision-cases  
└── /api/v1/approvals  
└── /api/v1/execution-requests

Rule:  
└── API contracts must not change silently because frontend, agents, digital twin views, and external systems depend on stable DTOs

---

## **Rate Limiting & Traffic Control Stack**

└── Rate Limiting  
└── Burst Limit  
└── Request Quota  
└── User-based Limit  
└── Service-based Limit  
└── IP-based Limit  
└── Route-specific Limit  
└── Backpressure  
└── Circuit Breaker  
└── Timeout Policy  
└── Retry Policy  
└── Load Shedding  
└── Abuse Detection

Usage:  
└── Protect APIs from overload  
└── Protect graph queries from expensive traversal abuse  
└── Protect inference and retrieval APIs from high-cost repeated calls  
└── Protect real-time channels from uncontrolled subscriptions

---

## **Routing Stack**

└── API Router  
└── Service Router  
└── Request Context Builder  
└── Tenant / Project / Site Routing  
└── User Role Routing  
└── Route-level Middleware  
└── Backend Service Discovery  
└── Reverse Proxy  
└── Service Mesh optional

Routing Targets:  
└── Ontology Service  
└── Knowledge Service  
└── World State Service  
└── Real-time Event Service  
└── Agent Service  
└── Decision Router Service  
└── Safety Gate Service  
└── Execution Request Service  
└── External Integration Service  
└── Audit Service  
└── Notification Service

---

## **External System API Stack**

└── External System Registration  
└── API Key / OAuth Client  
└── Service Account  
└── Webhook Endpoint  
└── Callback URL  
└── Event Subscription  
└── Request Signature Verification  
└── mTLS optional  
└── External System Rate Limit  
└── External System Audit Log

External Systems:  
└── Digital Twin System  
└── Fleet Manager  
└── Robot Middleware  
└── SCADA Platform  
└── PLC Gateway  
└── Equipment Controller  
└── BIM Platform  
└── Document Management System  
└── Site Operation Platform

Boundary:  
└── API Gateway exposes controlled integration APIs  
└── Detailed protocol translation belongs to Layer 11 Execution Request & External Control Integration  
└── API Gateway should not directly implement PLC, ROS2, Modbus, OPC-UA, or fleet execution logic

---

## **API Security Stack**

└── TLS  
└── mTLS optional  
└── OAuth2 / OIDC  
└── JWT Validation  
└── Token Expiry Check  
└── Scope Check  
└── CORS Policy  
└── CSRF Protection where required  
└── Request Signature Validation  
└── API Key Rotation  
└── Secret Management  
└── WAF optional  
└── Input Sanitization  
└── Output Redaction  
└── Security Audit Log

Security Rule:  
└── No unauthenticated or unauthorized request should reach internal backend services

---

## **DTO / Contract Stack**

└── OperationalNodeDTO  
└── WorldStateDTO  
└── CoreEventDTO  
└── AlertDTO  
└── RiskStateDTO  
└── ActionCandidateDTO  
└── DecisionCaseDTO  
└── ApprovalRequestDTO  
└── ApprovalDecisionDTO  
└── ApprovedActionDTO  
└── ExecutionRequestDTO  
└── ExecutionStatusDTO  
└── FeedbackEventDTO  
└── AuditRecordDTO  
└── GraphQueryDTO  
└── GraphResultDTO  
└── DigitalTwinStateDTO  
└── ErrorResponseDTO

Rule:  
└── DTOs are the boundary language between frontend, external systems, agents, and backend services  
└── Internal database records must not leak through API contracts

---

## **Error Handling Stack**

└── Standard Error Schema  
└── Validation Error  
└── Authentication Error  
└── Authorization Error  
└── Not Found Error  
└── Conflict Error  
└── Rate Limit Error  
└── Timeout Error  
└── Backend Unavailable Error  
└── External System Error  
└── Trace ID Binding  
└── Correlation ID Binding  
└── User-safe Error Message  
└── Internal Error Log

Error Response Fields:  
└── error\_code  
└── message  
└── details  
└── trace\_id  
└── correlation\_id  
└── timestamp  
└── retryable  
└── severity

---

## **Observability Integration Stack**

└── OpenTelemetry Middleware  
└── Request Logging  
└── API Latency Metrics  
└── Error Rate Metrics  
└── Route Metrics  
└── WebSocket Connection Metrics  
└── SSE Stream Metrics  
└── Authentication Failure Metrics  
└── Authorization Failure Metrics  
└── Rate Limit Metrics  
└── Backend Routing Metrics  
└── Trace Context Propagation

Metrics:  
└── api\_request\_count  
└── api\_latency\_ms  
└── api\_error\_rate  
└── websocket\_connection\_count  
└── sse\_active\_stream\_count  
└── auth\_failure\_count  
└── rate\_limit\_block\_count  
└── backend\_timeout\_count  
└── schema\_validation\_failure\_count

---

## **Service Mesh Stack**

└── Istio optional  
└── Linkerd optional  
└── Envoy optional  
└── Service Discovery  
└── Traffic Policy  
└── mTLS  
└── Retry Policy  
└── Timeout Policy  
└── Circuit Breaker  
└── Canary Deployment  
└── Blue / Green Deployment  
└── Service-to-Service Observability

Boundary:  
└── Service Mesh is infrastructure support  
└── It is not required for MVP  
└── It becomes useful when the system is split into multiple services and deployed on Kubernetes

---

## **Runtime Boundary**

└── API Gateway is active in all runtime request paths  
└── It handles identity, validation, routing, versioning, throttling, and real-time delivery  
└── It must be lightweight and should not become a heavy reasoning engine  
└── It should not perform long-running inference, graph traversal, ontology reasoning, or physical execution logic directly  
└── It should forward valid requests to the correct backend service  
└── It must reject invalid, unauthorized, malformed, unsupported, or unsafe requests early

---

## **Not Responsible For**

└── Defining ontology classes, properties, rules, or semantic truth  
└── Running OWL reasoning  
└── Running HermiT / Pellet validation  
└── Running full SHACL validation as the semantic authority  
└── Running OPA / Rego final policy decisions as the policy authority  
└── Generating agent candidates  
└── Classifying decision risk tiers  
└── Approving high-risk actions  
└── Creating ApprovedAction independently  
└── Executing physical commands  
└── Controlling robots, PLCs, SCADA, equipment, or fleet managers  
└── Performing ROS2, Modbus, OPC-UA, or device-level protocol logic directly  
└── Storing core knowledge as source of truth  
└── Becoming the business logic layer

---

## **Recommended MVP Stack Mapping**

└── API Framework: FastAPI  
└── Request / Response Models: Pydantic  
└── API Style: REST first  
└── Realtime: WebSocket \+ SSE  
└── Auth: OAuth2 / OIDC-compatible JWT validation  
└── API Docs: OpenAPI  
└── Type Sharing: OpenAPI-generated TypeScript client  
└── Rate Limiting: FastAPI middleware or reverse proxy-level limit  
└── Reverse Proxy: NGINX or Traefik  
└── Observability: OpenTelemetry middleware \+ structured logs  
└── Error Handling: Standard ErrorResponseDTO  
└── Versioning: /api/v1  
└── Security: TLS, CORS, token validation, request validation  
└── Background Service Routing: internal Python service clients or HTTP clients

MVP Rule:  
└── Start with FastAPI \+ REST \+ WebSocket/SSE \+ Pydantic DTOs \+ OpenAPI \+ JWT validation  
└── Add GraphQL only if frontend data composition becomes painful  
└── Add gRPC only if internal service-to-service performance or streaming requires it  
└── Add service mesh only after multi-service Kubernetes deployment becomes real

---

## **API Gateway Core Principles**

1. API Gateway Is the Controlled Front Door  
   └── Every UI, mobile, dashboard, agent, external system, and integration request should enter through controlled APIs.  
2. Backend Stores Must Not Be Exposed Directly  
   └── Frontend and external systems must not directly access Neo4j, RDF Store, PostgreSQL, Redis, Kafka, MQTT, or internal services.  
3. Validate Early, Route Cleanly  
   └── Invalid schema, unsupported version, malformed payload, unauthorized identity, or unsafe request must be rejected before reaching core services.  
4. API Gateway Is Not the Brain  
   └── It routes and validates requests; it does not become the ontology, reasoning engine, policy engine, decision router, or safety gate.  
5. Authentication Is Required for Every Actor  
   └── Users, agents, services, and external systems must have verified identities.  
6. Authorization Has Layers  
   └── API Gateway enforces coarse access checks, while Governance / Policy / Security handles fine-grained policy and high-risk authority rules.  
7. API Contracts Must Be Stable  
   └── DTOs, OpenAPI schemas, versioning, and deprecation policy must protect frontend, agents, and external integrations from silent breaking changes.  
8. Realtime Delivery Must Be Controlled  
   └── WebSocket and SSE streams must use authentication, authorization, subscription control, event sequencing, and reconnection rules.  
9. External Integration Must Be Gated  
   └── External systems can connect only through registered, authenticated, audited, and rate-limited interfaces.  
10. Physical Control Must Stay Outside the Gateway  
    └── API Gateway may accept or route execution-related requests, but protocol translation and physical execution integration belong to Layer 11\.  
11. Errors Must Be Traceable  
    └── Every API error should include trace ID, correlation ID, timestamp, and safe error information.  
12. Rate Limits Protect the System  
    └── Expensive graph queries, retrieval calls, inference calls, and realtime subscriptions must be bounded.  
13. APIs Must Be Observable  
    └── Latency, errors, authentication failures, authorization failures, WebSocket connections, route traffic, and backend timeouts must be monitored.  
14. API Gateway Must Degrade Safely  
    └── If downstream services fail, the gateway should return safe errors, avoid uncontrolled retries, and preserve traceability.  
15. Request Context Must Travel Across Layers  
    └── User identity, role, site scope, trace ID, correlation ID, API version, and permission context must travel into downstream services.  
16. UI Actions Must Become Structured Requests  
    └── Approval, rejection, escalation, manual override, and execution-related actions must become typed DTO requests, not free-form commands.  
17. Service Mesh Is Optional Infrastructure  
    └── Service Mesh supports secure service-to-service communication, traffic policy, and observability, but it is not required for the initial MVP.  
18. GraphQL and gRPC Are Optional  
    └── REST \+ WebSocket/SSE should be the MVP baseline; GraphQL and gRPC should be introduced only when their specific advantages are needed.  
19. Gateway Must Not Hide Business Responsibility  
    └── Routing through the gateway does not mean the gateway owns the decision. Decision ownership remains in the proper backend layer.  
20. API Gateway Protects the Ontology-Centric Core  
    └── Its purpose is to expose the system safely while preserving control boundaries, contracts, identity, validation, and traceability.
