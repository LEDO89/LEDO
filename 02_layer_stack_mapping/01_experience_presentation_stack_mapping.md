# **Ontology Centric “Experience / Presentation” Stack Mapping**

## **Layer 1\. Experience / Presentation Layer**

─ Core Position  
└── Experience / Presentation is the user-facing operational interface layer  
└── It provides dashboards, digital twin views, decision case review, approval workflows, graph exploration, workflow visualization, alerts, and manual override interfaces  
└── It serves operators, supervisors, safety managers, engineers, executives, and auditors  
└── It visualizes verified data from backend services  
└── It does not directly access databases  
└── It does not directly control robots, machines, PLCs, SCADA, or fleet managers  
└── It does not make final safety decisions independently  
└── It displays, explains, reviews, approves, and intervenes through controlled APIs

---

## **Core Role**

└── Provide real-time visibility into construction site operations  
└── Display current world state, risk status, robot state, equipment state, task state, and decision cases  
└── Allow operators and supervisors to review, approve, reject, escalate, or manually override when permitted  
└── Present ontology-grounded views such as graph explorer, node explorer, workflow explorer, and digital twin  
└── Support operational awareness, safety monitoring, approval workflows, and audit review  
└── Translate complex ontology-backed system state into human-understandable interfaces

---

## **Core Technologies**

└── Next.js  
└── React  
└── TypeScript  
└── Tailwind CSS  
└── shadcn/ui  
└── WebSocket  
└── SSE  
└── TanStack Query  
└── Zustand  
└── ECharts  
└── React Flow  
└── Cytoscape.js  
└── Three.js  
└── React Three Fiber  
└── Mapbox GL JS  
└── Deck.gl  
└── Leaflet  
└── REST API Client  
└── OpenAPI-generated TypeScript Types

---

## **Optional Technologies**

└── Flutter for mobile app  
└── CesiumJS for large-scale 3D geospatial digital twin  
└── D3.js for custom low-level visualization  
└── React Force Graph for interactive graph visualization  
└── WebRTC for video, camera stream, or media channel  
└── Grafana embedded panels for observability views  
└── Apache Superset embedded dashboards for management analytics  
└── Metabase embedded dashboards for lightweight reporting  
└── AR / VR Interface for advanced site visualization  
└── Voice Interface for operator interaction

---

## **Frontend Application Structure**

└── app / pages  
└── dashboard  
└── digital-twin  
└── graph-explorer  
└── ontology-explorer  
└── workflow  
└── map  
└── alerts  
└── approvals  
└── audit  
└── command-center

└── components  
└── dashboard  
└── digital-twin  
└── graph-explorer  
└── ontology-explorer  
└── workflow  
└── map  
└── charts  
└── realtime  
└── notification  
└── approval  
└── audit  
└── common

└── features  
└── safety  
└── robot  
└── equipment  
└── worker  
└── risk  
└── decision-case  
└── execution  
└── approval  
└── audit

└── api  
└── client.ts  
└── world-state.ts  
└── ontology.ts  
└── graph.ts  
└── decision.ts  
└── execution.ts  
└── approval.ts  
└── audit.ts

└── store  
└── world-state.store.ts  
└── ui.store.ts  
└── notification.store.ts  
└── selection.store.ts  
└── approval.store.ts

└── hooks  
└── useWorldState  
└── useRealtimeEvents  
└── useDecisionCases  
└── useGraphData  
└── useApprovalQueue  
└── useExecutionStatus

└── types  
└── node.ts  
└── event.ts  
└── action.ts  
└── decision-case.ts  
└── execution.ts  
└── approval.ts  
└── audit.ts

---

## **UI Module Stack**

└── Web UI  
└── Mobile UI  
└── Operator Console  
└── Supervisor Console  
└── Management Console  
└── War Room Display  
└── Command Center  
└── Human Approval Center  
└── Manual Override Center  
└── Alert Center  
└── Notification Center  
└── Audit Review Console

---

## **Dashboard Stack**

└── Safety Dashboard  
└── Robot Dashboard  
└── Equipment Dashboard  
└── Worker Dashboard  
└── Operations Dashboard  
└── Construction Progress Dashboard  
└── Risk Dashboard  
└── Compliance Dashboard  
└── KPI Dashboard  
└── Audit Dashboard  
└── Digital Twin Dashboard  
└── Execution Status Dashboard  
└── Decision Case Dashboard

Dashboard Technologies:  
└── ECharts  
└── Recharts for simple charts  
└── TanStack Query for server state  
└── WebSocket / SSE for real-time updates  
└── Grafana embedded panels for observability-only views  
└── Superset / Metabase embedded views for management analytics only

---

## **Digital Twin View Stack**

└── Digital Twin Dashboard  
└── Site State View  
└── Zone State View  
└── Worker Location View  
└── Robot State View  
└── Equipment State View  
└── Risk Overlay  
└── Execution Status Overlay  
└── Alert Overlay  
└── Decision Case Overlay

Technologies:  
└── Three.js  
└── React Three Fiber  
└── Drei  
└── Mapbox GL JS  
└── Deck.gl  
└── CesiumJS as optional large-scale 3D geospatial engine

Boundary:  
└── Digital Twin view visualizes world state  
└── It does not become the world state source of truth  
└── It must display freshness, timestamp, state version, and sync status when used operationally

---

## **Map / Geospatial Stack**

└── Site Map  
└── Zone Map  
└── Worker Location Map  
└── Equipment Location Map  
└── Robot Location Map  
└── Risk Heatmap  
└── Resource Heatmap  
└── Route Overlay  
└── Restricted Zone Overlay  
└── Emergency Zone Overlay

Technologies:  
└── Mapbox GL JS  
└── Deck.gl  
└── Leaflet  
└── CesiumJS optional

Usage:  
└── Mapbox GL JS for 2D operational maps  
└── Deck.gl for large-scale overlays, heatmaps, and trajectory visualization  
└── Leaflet for lightweight maps  
└── CesiumJS for large-scale geospatial or 3D terrain-based visualization

---

## **Graph Explorer Stack**

└── Knowledge Graph Explorer  
└── Ontology Explorer  
└── Entity Relationship Explorer  
└── Evidence Graph View  
└── Risk Graph View  
└── Task Graph View  
└── Worker / Equipment / Robot Context Graph  
└── Decision Case Evidence Graph

Technologies:  
└── Cytoscape.js  
└── React Force Graph  
└── D3.js optional

Recommended Use:  
└── Cytoscape.js as the main graph explorer for MVP  
└── React Force Graph for interactive force-directed views  
└── D3.js only when custom low-level visualization is required

Boundary:  
└── Frontend graph explorer queries backend graph APIs  
└── Frontend does not connect directly to Neo4j, RDF store, or SPARQL endpoint

---

## **Workflow Visualization Stack**

└── Construction Workflow  
└── Safety Workflow  
└── Inspection Workflow  
└── Emergency Workflow  
└── Approval Workflow  
└── Execution Workflow  
└── Recovery Workflow  
└── Robot Task Request Flow  
└── External Control Request Flow

Technology:  
└── React Flow

Workflow Concepts:  
└── Workflow Node  
└── Approval Step  
└── Decision Router Step  
└── Safety Gate Step  
└── Execution Request Step  
└── Feedback Step  
└── Recovery Step  
└── Manual Override Step

Boundary:  
└── Workflow UI visualizes and reviews workflow state  
└── Actual workflow execution remains in backend workflow/state machine services

---

## **Realtime Communication Stack**

└── WebSocket  
└── SSE  
└── Socket.IO optional  
└── WebRTC optional for video/media only

Usage Rules:  
└── WebSocket for bidirectional real-time operational events  
└── SSE for server-to-client event streaming  
└── REST for request/response queries  
└── WebRTC for video, camera streams, remote visual inspection, or media channels  
└── WebRTC should not be used for normal dashboard state updates

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

---

## **State Management Stack**

└── Zustand  
└── TanStack Query  
└── React Context

Usage:  
└── Zustand for local UI state, selected node, active panel, map layer, layout state, and interaction state  
└── TanStack Query for backend server state from FastAPI  
└── React Context for lightweight shared UI context  
└── Redux Toolkit is optional and should be added only if frontend state becomes complex enough to require it

Boundary:  
└── Server state must come from FastAPI APIs  
└── Frontend must not directly query Neo4j, RDF Store, PostgreSQL, Redis, Kafka, or MQTT

---

## **Chart / Visualization Stack**

└── ECharts  
└── Recharts  
└── D3.js optional  
└── Grafana embedded panels optional

Usage:  
└── ECharts for complex operational dashboards and risk visualization  
└── Recharts for simple React-friendly charts  
└── D3.js for custom visualization only  
└── Grafana embedded panels for monitoring and observability views only

Chart Types:  
└── Risk Trend Chart  
└── Equipment Status Chart  
└── Worker Safety Chart  
└── Robot Utilization Chart  
└── Execution Latency Chart  
└── Approval Waiting Time Chart  
└── Incident Timeline Chart  
└── Zone Risk Heatmap  
└── Resource Utilization Chart

---

## **Alert / Notification Stack**

└── Alert Center  
└── Notification Center  
└── Toast Notification  
└── Event Timeline  
└── Risk Alert Panel  
└── Approval Request Panel  
└── Execution Status Panel  
└── Emergency Alert Banner

Technologies:  
└── WebSocket  
└── SSE  
└── Zustand Notification Store  
└── Browser Notification API optional  
└── Mobile Push optional

Alert Types:  
└── Safety Alert  
└── Risk Warning  
└── Approval Request  
└── Execution Failure  
└── External Control Timeout  
└── Manual Override Required  
└── Stale World State Alert  
└── Ontology / Policy Change Alert  
└── System Health Alert

---

## **Human Approval UI Stack**

└── Human Approval Center  
└── Approval Queue  
└── Decision Case Review Panel  
└── Evidence Viewer  
└── Risk Summary  
└── Policy Validation Result  
└── SHACL Validation Result  
└── Action Candidate Comparison  
└── Approve / Reject / Escalate Buttons  
└── Manual Override Form  
└── Reviewer Comment Field  
└── Approval Audit Trail

Approval UI Requirements:  
└── Show action type  
└── Show target node  
└── Show risk tier  
└── Show evidence references  
└── Show policy result  
└── Show validation result  
└── Show required approval level  
└── Show execution impact  
└── Show reviewer identity  
└── Show timestamp  
└── Write approval decision through controlled backend API

Boundary:  
└── UI does not create ApprovedAction directly  
└── UI submits approval decision to backend approval workflow  
└── Safety Gate creates or rejects ApprovedAction

---

## **Manual Override UI Stack**

└── Manual Override Center  
└── Emergency Stop Request UI  
└── Override Reason Form  
└── Supervisor Authentication  
└── Policy Warning Panel  
└── Execution Impact Preview  
└── Override Audit Record  
└── Confirmation Dialog

Boundary:  
└── Manual override must pass Governance / Policy / Security Layer  
└── Manual override must be audited  
└── UI only submits override request  
└── Backend validates permission, policy, and safety constraints

---

## **Audit Review UI Stack**

└── Audit Dashboard  
└── Decision Timeline  
└── Execution Timeline  
└── Approval History  
└── Manual Override History  
└── Ontology Change History  
└── Policy Change History  
└── Failure Analysis View  
└── Evidence Chain Viewer  
└── Trace ID Search  
└── Decision Case Search

Usage:  
└── Review why an action was approved, rejected, escalated, or executed  
└── Review who approved or rejected an action  
└── Review which evidence supported the decision  
└── Review execution feedback and failure timeline  
└── Review ontology and policy changes

---

## **Embedded BI / Analytics Stack**

└── Grafana  
└── Apache Superset  
└── Metabase

Correct Placement:  
└── Grafana primarily belongs to Layer 0 Observability / Audit / Trace  
└── Superset and Metabase belong to optional management analytics and reporting  
└── They may be embedded into the Experience Layer as external dashboards  
└── They are not core React application components

Usage:  
└── Grafana for system metrics, latency, health, and observability panels  
└── Superset for management analytics, historical reporting, and executive views  
└── Metabase for lightweight BI and reporting

Boundary:  
└── Embedded BI dashboards visualize analytics  
└── They do not approve actions  
└── They do not execute commands  
└── They do not replace operational UI, approval UI, or safety gate UI

---

## **API Connection Stack**

Frontend communicates with backend through:  
└── FastAPI REST APIs  
└── FastAPI WebSocket  
└── SSE endpoints  
└── OpenAPI-generated TypeScript clients  
└── Authentication token flow  
└── Role-based UI permission model

Backend communicates with:  
└── Ontology Services  
└── Knowledge Graph APIs  
└── World State APIs  
└── Decision Router APIs  
└── Safety Gate APIs  
└── Execution Request APIs  
└── Audit APIs

Correct Connection Model:  
└── React / Next.js  
↔ FastAPI / WebSocket / SSE  
↔ World State / Decision Case / Knowledge Graph API  
↔ Redis / Neo4j / RDF Store / PostgreSQL / Event Store

Incorrect Connection Model:  
└── React directly connecting to Neo4j  
└── React directly querying RDF Store  
└── React directly reading Redis  
└── React directly consuming Kafka / MQTT  
└── React directly controlling robots or machines

---

## **DTO / Type Stack**

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
└── GraphNodeDTO  
└── GraphEdgeDTO  
└── DigitalTwinNodeDTO

Rule:  
└── Frontend types should be generated from backend OpenAPI schemas when possible  
└── UI components should consume DTOs, not raw database records

---

## **Security & Access Control Stack**

└── Authenticated UI Session  
└── Role-based UI Rendering  
└── Permission-based Action Buttons  
└── Field-level Redaction  
└── Sensitive Incident Data Masking  
└── Worker Privacy Masking  
└── Approval Permission Check  
└── Manual Override Permission Check  
└── Audit Access Control  
└── Secure Token Storage

UI Permission Examples:  
└── Operator can view operational status  
└── Supervisor can approve assigned decision cases  
└── Safety manager can review safety incidents  
└── Executive can view management dashboard  
└── Auditor can view audit trails  
└── Unauthorized users cannot see restricted worker data or sensitive incident details

---

## **Runtime Boundary**

└── This layer is active during operational monitoring, review, approval, and intervention  
└── It receives real-time updates from backend APIs  
└── It must display freshness, timestamp, and status for critical operational data  
└── It must not block critical emergency actions  
└── It must degrade safely if real-time UI updates fail  
└── It should show stale state warnings when data freshness is below required threshold  
└── It must not become a direct control plane for robots, PLCs, SCADA, or fleet managers

---

## **Not Responsible For**

└── Defining ontology truth  
└── Running OWL reasoning  
└── Running SHACL validation directly  
└── Running OPA / Rego policy evaluation directly  
└── Accessing Neo4j, RDF Store, PostgreSQL, Redis, Kafka, or MQTT directly  
└── Creating ApprovedAction directly  
└── Executing physical commands  
└── Controlling robots, machines, PLCs, SCADA, or fleet managers  
└── Performing fleet scheduling  
└── Performing motion planning  
└── Performing safety gate validation  
└── Replacing the Decision Router  
└── Replacing the Unified Cyber-Physical Core

---

## **Recommended MVP Stack Mapping**

└── Core Framework: Next.js \+ React \+ TypeScript  
└── Styling: Tailwind CSS \+ shadcn/ui  
└── Server State: TanStack Query  
└── UI State: Zustand  
└── Realtime: WebSocket \+ SSE  
└── Charts: ECharts  
└── Workflow: React Flow  
└── Graph Explorer: Cytoscape.js  
└── Map: Mapbox GL JS  
└── 3D: Three.js \+ React Three Fiber  
└── API Client: OpenAPI-generated TypeScript client  
└── Authentication: OAuth2 / OIDC token integration through backend  
└── Notifications: WebSocket / SSE \+ notification store  
└── Approval UI: DecisionCase \+ ApprovalRequest components  
└── Audit UI: Timeline \+ Trace ID search

MVP Rule:  
└── Start with Web UI, dashboard, graph explorer, decision case review, alert center, and approval center  
└── Add digital twin, 3D, advanced map overlays, embedded BI, AR / VR, and voice interface after core data contracts stabilize

---

## **Experience / Presentation Core Principles**

1. The UI Is an Operational Interface, Not the Source of Truth  
   └── It visualizes backend-verified state, decision cases, approvals, execution status, and audit history.  
2. Frontend Must Not Access Databases Directly  
   └── React / Next.js communicates with FastAPI; FastAPI communicates with Neo4j, RDF Store, PostgreSQL, Redis, Kafka, and other backend systems.  
3. Every Critical View Must Show Freshness  
   └── World state, robot state, equipment state, worker location, risk status, and execution status must display timestamp, version, or freshness state when used operationally.  
4. Dashboards Must Be Separated by Purpose  
   └── Operational dashboards, observability dashboards, management analytics, and audit dashboards serve different users and must not be mixed without clear boundaries.  
5. Approval UI Must Be Evidence-bound  
   └── Approval screens must show candidate action, evidence, risk tier, validation result, policy result, and approval requirement.  
6. Manual Override Must Be Controlled and Audited  
   └── Manual override must require permission, reason, confirmation, and audit trail.  
7. Digital Twin Is a View of World State  
   └── It visualizes current and historical state; it does not define operational truth.  
8. Graph Explorer Is for Understanding Relationships  
   └── It helps users explore ontology, knowledge graph, evidence graph, risk graph, and task graph relationships.  
9. Realtime UI Must Degrade Safely  
   └── If WebSocket or SSE fails, the UI must show degraded mode, stale data warnings, or polling fallback.  
10. UI Actions Must Go Through Backend Validation  
    └── Approve, reject, escalate, manual override, and command requests must go through controlled backend APIs and policy validation.  
11. Embedded BI Is Optional  
    └── Grafana, Superset, and Metabase may be embedded for monitoring or analytics but should not replace the operational UI.  
12. Role-based UI Must Protect Sensitive Data  
    └── Worker privacy, incident data, restricted documents, and security-sensitive operational details must be masked or hidden based on permission.  
13. UI Components Should Consume DTOs  
    └── Frontend components must consume structured DTOs from backend APIs, not raw database records.  
14. War Room Display Must Prioritize High-risk Decision Cases  
    └── War Room should not display every low-level event; it should prioritize high-risk, critical, exceptional, or approval-required cases.  
15. Human Attention Is a Limited Resource  
    └── UI must reduce noise through filtering, prioritization, risk tiering, and escalation rules.  
16. Visualization Must Support Actionability  
    └── Charts, maps, graphs, timelines, and digital twin views must help users understand risk, status, decision, approval, and execution.  
17. Audit Review Must Reconstruct the Timeline  
    └── The UI should allow users to reconstruct what happened, why it happened, who approved it, and what execution feedback was received.  
18. Frontend Must Respect the Control Boundary  
    └── The UI may request, approve, reject, or escalate through backend workflows, but it must not directly control physical systems.  
19. Operator Experience Must Match Operational Urgency  
    └── Routine, notice, warning, high-risk, critical emergency, and exceptional cases should have different UI treatment.  
20. Experience Layer Must Make the Ontology Understandable  
    └── The purpose of this layer is to translate ontology-backed operational intelligence into usable human interfaces.

