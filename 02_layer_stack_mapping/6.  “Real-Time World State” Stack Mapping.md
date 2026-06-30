# **Ontology Centric “Real-Time World State” Stack Mapping**

## **Layer 6\. Real-Time World State Layer**

─ Core Position  
└── Real-Time World State is the live operational state layer of the ontology-centric system  
└── It transforms real-time signals from sensors, cameras, LiDAR, robots, workers, equipment, PLCs, SCADA systems, fleet managers, and schedule systems into a live semantic world state  
└── It maintains current operational facts such as worker location, robot state, equipment status, zone risk, approval state, execution state, and sensor freshness  
└── It provides fresh state to agents, decision router, safety gate, digital twin, dashboards, alerts, and execution feedback loops  
└── It does not define ontology meaning  
└── It does not replace Knowledge & Semantic Memory  
└── It does not perform full offline reasoning  
└── It does not approve actions  
└── It does not directly control physical systems  
└── It provides the current state required for safe and timely operational decisions

---

## **Core Role**

└── Ingest real-time signals from physical and digital systems  
└── Normalize telemetry, events, sensor data, robot data, equipment data, worker tracking data, PLC signals, SCADA events, and fleet manager status  
└── Convert raw signals into ontology-grounded operational state updates  
└── Maintain live world state cache  
└── Maintain belief cache for domain agents  
└── Track freshness, confidence, source timestamp, ingestion timestamp, and state version  
└── Detect state changes, event patterns, anomalies, thresholds, and risk signals  
└── Synchronize operational nodes such as workers, robots, equipment, zones, tasks, sensors, and external systems  
└── Provide current state to dashboards, digital twin, agents, decision router, safety gate, and execution lifecycle  
└── Materialize meaningful events to knowledge layer, audit layer, and historical event store when required

---

## **Core Technologies**

└── Kafka  
└── MQTT  
└── ROS2 Telemetry  
└── OPC-UA Ingestion  
└── RDF Stream  
└── RSP Engine  
└── CEP Engine  
└── Apache Flink  
└── Kafka Streams  
└── Redis  
└── TimescaleDB  
└── InfluxDB  
└── In-Memory Semantic Graph  
└── World State Cache  
└── Belief Cache  
└── Dynamic State Store  
└── Event Stream Processor  
└── Stream Normalizer  
└── State Reconciliation Engine  
└── Freshness Validator

---

## **Optional Technologies**

└── Apache Pulsar  
└── NATS  
└── Redpanda  
└── RabbitMQ for simpler event routing  
└── Redis Streams  
└── Materialize  
└── RisingWave  
└── Apache Beam  
└── Spark Structured Streaming  
└── Edge MQTT Broker  
└── ROS2 Bridge  
└── WebRTC media ingestion for camera streams  
└── RTSP / ONVIF camera integration  
└── OpenCV-based vision preprocessing  
└── Edge inference gateway  
└── Time-series compression engine  
└── Stream schema registry  
└── Dead Letter Queue

---

## **Input Stream Stack**

└── IoT Streams  
└── Camera Streams  
└── LiDAR Streams  
└── Robot Telemetry  
└── Worker Tracking  
└── Equipment Status  
└── PLC Signals  
└── SCADA Events  
└── Fleet Manager Status  
└── Environmental Sensors  
└── BIM / Schedule Updates  
└── Weather Data  
└── Permit Status Updates  
└── Inspection Status Updates  
└── Safety Alert Streams  
└── Manual Field Report Streams  
└── External Control Feedback Streams

Input Rule:  
└── Every input stream must be normalized into typed events before operational use  
└── Raw input is not automatically trusted state  
└── Each stream requires source, timestamp, confidence, schema version, and ingestion metadata

---

## **State Model Stack**

└── Static Knowledge  
└── Ontology  
└── RDF Triple Store  
└── Knowledge Graph  
└── Document Store  
└── Construction Knowledge Base

└── Dynamic Knowledge  
└── World State Cache  
└── Belief Cache  
└── Memory Graph  
└── Redis  
└── Time-Series Store  
└── In-Memory Semantic Graph  
└── Dynamic State Store

State Boundary:  
└── Static knowledge defines meaning, long-term facts, documents, relationships, and domain knowledge  
└── Dynamic knowledge represents current operational conditions  
└── Current operational facts must prefer Layer 6  
└── Semantic meaning must prefer Layer 4  
└── Persistent memory and evidence must prefer Layer 5

---

## **Live State Ingestion Stack**

└── Stream Connector  
└── MQTT Subscriber  
└── Kafka Consumer  
└── ROS2 Telemetry Bridge  
└── OPC-UA Connector  
└── SCADA Event Connector  
└── Fleet Manager Status Connector  
└── PLC Signal Connector  
└── Camera Event Connector  
└── LiDAR Event Connector  
└── Worker Tracking Connector  
└── Equipment Telemetry Connector  
└── BIM / Schedule Update Connector

Ingestion Steps:  
└── Receive raw signal  
└── Validate message schema  
└── Attach source metadata  
└── Normalize units and timestamps  
└── Map source entity to canonical ontology IRI  
└── Calculate confidence and freshness  
└── Update world state cache  
└── Emit state change event  
└── Store event history when required  
└── Notify downstream services

---

## **Telemetry Normalization Stack**

└── Schema Normalization  
└── Unit Normalization  
└── Timestamp Normalization  
└── Coordinate Normalization  
└── Entity ID Normalization  
└── IRI Mapping  
└── Status Code Mapping  
└── Error Code Mapping  
└── Sensor Value Normalization  
└── Equipment Mode Normalization  
└── Robot State Normalization  
└── Worker Location Normalization  
└── Zone Risk Normalization  
└── Confidence Score Calculation  
└── Freshness Calculation

Normalization Rule:  
└── Different external systems may use different IDs, units, status codes, coordinates, and timestamps  
└── Layer 6 must normalize them into ontology-grounded operational DTOs  
└── Normalization must not invent semantic truth; ambiguous mappings must be flagged or quarantined

---

## **Event Stream Processing Stack**

└── Kafka Topics  
└── MQTT Topics  
└── Kafka Streams  
└── Apache Flink  
└── CEP Engine  
└── Stream Windowing  
└── Event Time Processing  
└── Processing Time Tracking  
└── Watermarking  
└── Deduplication  
└── Ordering  
└── Event Correlation  
└── Event Aggregation  
└── Threshold Detection  
└── Pattern Detection  
└── Anomaly Detection  
└── Dead Letter Queue

Stream Processing Use Cases:  
└── Worker enters restricted zone  
└── Robot enters high-risk area  
└── Equipment status changes to failure  
└── Sensor value exceeds threshold  
└── Multiple workers gather near danger zone  
└── PLC signal indicates abnormal machine state  
└── Fleet manager reports blocked robot route  
└── SCADA event indicates emergency condition  
└── Environmental sensor detects hazardous condition  
└── BIM schedule update changes active work zone

---

## **Kafka Stack**

└── Kafka Broker  
└── Kafka Topic  
└── Kafka Producer  
└── Kafka Consumer  
└── Consumer Group  
└── Partition  
└── Offset  
└── Schema Registry optional  
└── Dead Letter Topic  
└── Retry Topic  
└── Compacted Topic for latest state optional  
└── Event Replay  
└── Event Ordering by Key  
└── Backpressure Handling

Kafka Topic Examples:  
└── sensor.events  
└── worker.location.events  
└── robot.telemetry.events  
└── equipment.status.events  
└── zone.risk.events  
└── fleet.status.events  
└── scada.events  
└── plc.signals  
└── world.state.updates  
└── risk.signals  
└── execution.feedback.events

Kafka Rule:  
└── Kafka is for durable event streaming and event replay  
└── Kafka should not be used as the direct current-state lookup store  
└── Redis or world state cache should serve current state queries

---

## **MQTT Stack**

└── MQTT Broker  
└── MQTT Topic  
└── MQTT Publisher  
└── MQTT Subscriber  
└── QoS Level  
└── Retained Message  
└── Edge Device Topic  
└── Sensor Topic  
└── Equipment Topic  
└── Robot Edge Topic  
└── Environmental Sensor Topic  
└── Gateway Bridge to Kafka

MQTT Usage:  
└── Lightweight IoT sensor communication  
└── Edge devices  
└── Field gateways  
└── Environmental sensors  
└── Simple equipment status updates  
└── Site-local telemetry

MQTT Rule:  
└── MQTT is useful near the edge  
└── Kafka is useful for central durable event streaming  
└── MQTT events should be normalized and bridged into the central event pipeline when needed

---

## **ROS2 Telemetry Stack**

└── ROS2 Topic Bridge  
└── Robot Pose  
└── Robot Status  
└── Robot Battery State  
└── Robot Health  
└── Robot Task Status  
└── Robot Error State  
└── Sensor Message Conversion  
└── Fleet Manager Bridge  
└── ROS2 to Kafka / MQTT Bridge

Boundary:  
└── Layer 6 consumes robot telemetry and status  
└── It does not perform robot motion planning  
└── It does not run low-level robot control loops  
└── It does not replace robot middleware or fleet manager

---

## **OPC-UA / PLC / SCADA Ingestion Stack**

└── OPC-UA Client  
└── PLC Signal Reader  
└── SCADA Event Connector  
└── Tag Mapping  
└── Alarm Mapping  
└── Machine State Mapping  
└── Equipment Status Mapping  
└── Signal Quality Tracking  
└── Timestamp Alignment  
└── Industrial Gateway  
└── Protocol Bridge to Event Stream

Boundary:  
└── Layer 6 ingests PLC / SCADA signals and machine state  
└── It does not replace PLC logic  
└── It does not directly control SCADA commands  
└── Execution requests to PLC / SCADA systems belong to Layer 11

---

## **RDF Stream / RSP Stack**

└── RDF Stream  
└── RSP Engine  
└── RSP-QL optional  
└── Stream-to-Triple Mapping  
└── Sliding Window  
└── Tumbling Window  
└── Time Window Reasoning  
└── Event-to-RDF Conversion  
└── Semantic Stream Query  
└── Windowed SPARQL-like Query  
└── RDF Stream Materialization

Usage:  
└── Apply semantic queries over streaming events  
└── Detect ontology-grounded patterns in live streams  
└── Support semantic event detection  
└── Generate meaningful state transitions or risk signals

Boundary:  
└── RDF Stream is not the same as writing every telemetry tick into the triple store  
└── High-frequency streams should be windowed, filtered, aggregated, or event-bound before RDF materialization

---

## **CEP Engine Stack**

└── Complex Event Processing  
└── Event Pattern Matching  
└── Temporal Pattern Detection  
└── Multi-source Event Correlation  
└── Threshold Rule  
└── Sequence Rule  
└── Absence Rule  
└── Sliding Window Rule  
└── Risk Pattern Rule  
└── Emergency Pattern Rule

CEP Examples:  
└── Worker inside restricted zone \+ equipment active nearby  
└── Robot path blocked \+ high-risk zone nearby  
└── Gas sensor threshold exceeded \+ worker presence detected  
└── Crane movement detected \+ unauthorized worker nearby  
└── PLC abnormal signal \+ equipment overheating trend  
└── Multiple stale sensor sources in same zone

---

## **Redis / World State Cache Stack**

└── Redis  
└── World State Cache  
└── Belief Cache  
└── Current Node State  
└── Current Zone State  
└── Current Worker State  
└── Current Robot State  
└── Current Equipment State  
└── Current Sensor State  
└── Current Approval State  
└── Current Execution State  
└── State Version  
└── Freshness Timestamp  
└── TTL  
└── Stale State Flag  
└── Distributed Lock optional  
└── Pub/Sub optional  
└── Redis Streams optional

World State Keys:  
└── world:worker:{worker\_id}:state  
└── world:robot:{robot\_id}:state  
└── world:equipment:{equipment\_id}:state  
└── world:zone:{zone\_id}:state  
└── world:sensor:{sensor\_id}:state  
└── world:task:{task\_id}:state  
└── world:execution:{execution\_id}:state

Redis Rule:  
└── Redis is the priority source for current operational facts  
└── Redis stores current state, not long-term semantic truth  
└── Every state entry must include timestamp, source, version, and freshness status  
└── Stale state must be flagged or rejected for high-risk decisions

---

## **Belief Cache Stack**

└── Agent Belief Cache  
└── Safety Agent Belief  
└── Robot Agent Belief  
└── Equipment Agent Belief  
└── Worker Agent Belief  
└── Zone Risk Belief  
└── Task Status Belief  
└── Execution Status Belief  
└── Evidence Snapshot  
└── Confidence Score  
└── Freshness Level  
└── Belief Version  
└── Belief Expiration

Belief Rule:  
└── Belief Cache provides fast current context for domain agents  
└── Belief is not permanent semantic truth  
└── Belief must be refreshed, versioned, and traceable to source events  
└── Agents should not act on stale beliefs

---

## **In-Memory Semantic Graph Stack**

└── Current Entity Graph  
└── Current Zone Graph  
└── Current Worker-Equipment-Zone Graph  
└── Current Robot-Task-Zone Graph  
└── Current Risk Graph  
└── Current Execution Graph  
└── Dynamic Relationship View  
└── State-linked Graph Cache  
└── Graph Snapshot  
└── Graph Diff  
└── Graph TTL

Usage:  
└── Fast runtime relationship lookup  
└── Current operational context expansion  
└── Current nearby-risk lookup  
└── Current entity relationship snapshot  
└── Support agents and decision router without heavy graph database query

Boundary:  
└── In-memory semantic graph is a runtime view  
└── It must be derived from ontology definitions and current world state  
└── It should not become independent semantic authority

---

## **Time-Series Store Stack**

└── TimescaleDB  
└── InfluxDB  
└── Time-Series Telemetry  
└── Sensor History  
└── Robot Telemetry History  
└── Equipment Telemetry History  
└── Environmental Trend  
└── Zone Risk Trend  
└── Worker Location History  
└── Aggregated Metrics  
└── Downsampling  
└── Retention Policy  
└── Trend Query  
└── Anomaly Trend Analysis

Usage:  
└── Store historical telemetry trends  
└── Analyze sensor drift  
└── Analyze equipment behavior  
└── Analyze environmental risk trend  
└── Support incident investigation  
└── Support dashboards and reports

Boundary:  
└── Time-series store supports history and trend analysis  
└── Current operational state should still be served from world state cache  
└── Long-term confirmed events may be stored in Layer 5 historical event store

---

## **Node State Synchronization Stack**

└── OperationalNode State  
└── Worker State  
└── Robot State  
└── Equipment State  
└── Sensor State  
└── Zone State  
└── Task State  
└── Approval State  
└── Execution State  
└── External System State  
└── State Version  
└── State Diff  
└── State Patch  
└── State Snapshot  
└── Conflict Resolution  
└── Stale State Detection  
└── Source Authority Ranking

State Synchronization Rule:  
└── Multiple sources may report conflicting state  
└── The system must resolve by source authority, timestamp, confidence, and policy  
└── Conflicting high-risk state must be quarantined or escalated  
└── State updates must preserve causation and correlation IDs

---

## **Sensor Confidence Tracking Stack**

└── Source Reliability Score  
└── Sensor Confidence Score  
└── Signal Quality  
└── Calibration Status  
└── Last Seen Timestamp  
└── Heartbeat Status  
└── Staleness Score  
└── Outlier Detection  
└── Drift Detection  
└── Missing Data Detection  
└── Conflicting Sensor Detection  
└── Sensor Health State

Confidence Rule:  
└── Current state must include confidence when derived from uncertain sensors  
└── Low-confidence state must not automatically trigger high-risk actions  
└── Safety-critical decisions require sufficient confidence or human review

---

## **Real-time Risk Signal Stack**

└── RiskSignal  
└── ZoneRiskSignal  
└── WorkerRiskSignal  
└── RobotRiskSignal  
└── EquipmentRiskSignal  
└── EnvironmentalRiskSignal  
└── TaskRiskSignal  
└── IncidentRiskSignal  
└── Risk Level  
└── Risk Score  
└── Risk Source  
└── Risk Evidence  
└── Risk Timestamp  
└── Risk Freshness  
└── Risk Confidence  
└── Risk Escalation Hint

Risk Signal Examples:  
└── WorkerNearHazard  
└── WorkerInsideRestrictedZone  
└── RobotEnteringUnsafeZone  
└── EquipmentAbnormalState  
└── SensorThresholdExceeded  
└── GasLeakPossible  
└── CraneOperationNearWorker  
└── StaleSafetySensor  
└── EmergencyRouteBlocked  
└── UnauthorizedZoneEntry

Risk Signal Rule:  
└── Layer 6 generates real-time risk signals  
└── Decision Router classifies and routes risk cases  
└── Safety Gate validates executable actions  
└── Layer 6 does not independently approve or execute actions

---

## **World State DTO Stack**

└── WorldStateDTO  
└── OperationalNodeStateDTO  
└── WorkerStateDTO  
└── RobotStateDTO  
└── EquipmentStateDTO  
└── SensorStateDTO  
└── ZoneStateDTO  
└── TaskStateDTO  
└── RiskStateDTO  
└── ApprovalStateDTO  
└── ExecutionStateDTO  
└── SourceMetadataDTO  
└── FreshnessDTO  
└── ConfidenceDTO  
└── StateVersionDTO  
└── StateChangeEventDTO  
└── RiskSignalDTO

Required Fields:  
└── node\_id  
└── node\_type  
└── state\_type  
└── value  
└── source\_system  
└── source\_timestamp  
└── ingestion\_timestamp  
└── state\_version  
└── confidence\_score  
└── freshness\_status  
└── trace\_id  
└── correlation\_id

---

## **Freshness & Staleness Stack**

└── Source Timestamp  
└── Ingestion Timestamp  
└── Processing Timestamp  
└── Last Updated Timestamp  
└── TTL  
└── Freshness Requirement  
└── Stale State Flag  
└── State Expiration  
└── Heartbeat Timeout  
└── Source Lag Measurement  
└── Materialization Lag Measurement  
└── Dashboard Freshness Display  
└── Agent Freshness Requirement  
└── Safety Gate Freshness Requirement

Freshness Rule:  
└── High-risk decisions require fresh state  
└── Stale state must block, degrade, or escalate depending on risk level  
└── Dashboards must display stale state warnings  
└── Agents must declare required freshness level for the state they consume

---

## **State Materialization Stack**

└── Redis Current State Update  
└── Kafka State Change Event  
└── PostgreSQL Event Append  
└── TimescaleDB Telemetry Append  
└── RDF Materialization optional  
└── Neo4j Read Model Update optional  
└── Digital Twin State Push  
└── Audit Event Push  
└── Knowledge Layer Update for finalized events  
└── Cache Invalidation

Materialization Rule:  
└── Real-time updates first go to world state cache  
└── Meaningful state changes may be appended to event store  
└── Aggregated or confirmed facts may be materialized to RDF or graph read models  
└── High-frequency telemetry must not directly flood RDF triple store

---

## **Digital Twin Sync Stack**

└── World State Update  
└── Digital Twin State DTO  
└── WebSocket Push  
└── SSE Stream  
└── UI State Version  
└── Node Position Update  
└── Zone Status Update  
└── Risk Overlay Update  
└── Execution Status Overlay  
└── Event Timeline Update  
└── State Freshness Indicator  
└── Sync Lag Monitor  
└── Missed Update Detection

Digital Twin Rule:  
└── Digital twin is a visualization of world state  
└── It is not the source of truth  
└── It must show freshness and sync status for operational use

---

## **World State API Stack**

└── Current State API  
└── Node State API  
└── Zone State API  
└── Worker State API  
└── Robot State API  
└── Equipment State API  
└── Sensor State API  
└── Risk State API  
└── Execution State API  
└── State Snapshot API  
└── State Diff API  
└── State Subscription API  
└── Real-time Event API  
└── Freshness Check API

API Rule:  
└── Frontend, agents, decision router, and safety gate must consume world state through controlled backend APIs or service interfaces  
└── Direct frontend access to Redis, Kafka, MQTT, or time-series databases is not allowed

---

## **Observability Stack**

└── Stream Ingestion Rate  
└── Stream Processing Latency  
└── Kafka Consumer Lag  
└── MQTT Connection Status  
└── Redis Update Latency  
└── World State Freshness  
└── Stale State Count  
└── Dropped Event Count  
└── Dead Letter Count  
└── Sensor Confidence Trend  
└── Source System Health  
└── RDF Materialization Lag  
└── Digital Twin Sync Lag  
└── Risk Signal Count  
└── State Conflict Count  
└── State Reconciliation Failure Count

Observability Rule:  
└── World state must be observable because stale or incorrect current state can cause unsafe operational decisions

---

## **Security & Access Control Stack**

└── Stream Source Authentication  
└── MQTT Credential Control  
└── Kafka ACL  
└── Service Account Identity  
└── Source System Registration  
└── Topic-level Permission  
└── State Access Control  
└── Sensitive State Masking  
└── Worker Location Privacy  
└── Field-level Redaction  
└── Tamper Detection  
└── Message Signature optional  
└── mTLS optional  
└── Audit Log for State Access

Security Rule:  
└── Real-time data sources must be authenticated and scoped  
└── Worker location, incident state, and sensitive operational data must be protected  
└── Unauthorized systems must not publish state updates

---

## **Runtime Boundary**

└── This layer is active in real-time operational paths  
└── It prioritizes freshness, bounded latency, confidence, and state correctness  
└── It provides current facts to agents, decision router, safety gate, dashboards, and execution feedback loops  
└── It should avoid expensive full ontology reasoning in the critical path  
└── It should use ontology-grounded mappings, cached contracts, target-specific validation, stream rules, and fast state lookup  
└── It should materialize RDF or historical memory only at meaningful boundaries  
└── It must degrade safely when data is missing, stale, conflicting, or low-confidence

---

## **Not Responsible For**

└── Defining ontology meaning  
└── Replacing Core Ontology Kernel  
└── Storing all long-term documents and semantic memory  
└── Replacing Knowledge & Semantic Memory Layer  
└── Running full OWL reasoning in real time  
└── Acting as the final policy authority  
└── Approving actions  
└── Creating ApprovedAction independently  
└── Executing physical commands  
└── Controlling robots, PLCs, SCADA, equipment, or fleet managers  
└── Performing robot motion planning  
└── Performing fleet scheduling  
└── Replacing external control systems  
└── Replacing Decision Router  
└── Replacing Safety Gate  
└── Treating stale or low-confidence state as safe operational truth

---

## **Recommended MVP Stack Mapping**

└── Event Bus: Kafka or Redpanda  
└── Edge / Sensor Messaging: MQTT  
└── Current State Store: Redis  
└── Time-Series Store: TimescaleDB first, InfluxDB optional  
└── Stream Processing: Kafka Streams first, Apache Flink later  
└── CEP: lightweight rule engine first, dedicated CEP later  
└── RDF Stream: optional after ontology stream mapping stabilizes  
└── Robot Telemetry: ROS2 bridge when robot integration begins  
└── Industrial Ingestion: OPC-UA connector when PLC / SCADA integration begins  
└── World State DTOs: Pydantic models  
└── State API: FastAPI current state API  
└── Realtime UI Delivery: WebSocket / SSE through API Gateway  
└── Observability: Prometheus \+ Grafana metrics for freshness, lag, dropped events, and stale state  
└── Audit: state change events sent to Layer 0 / Layer 5 when meaningful

MVP Rule:  
└── Start with MQTT → FastAPI ingestion → Redis World State → WebSocket/SSE UI updates  
└── Add Kafka when event volume, replay, durability, or multi-consumer processing becomes necessary  
└── Add TimescaleDB for telemetry history  
└── Add Flink / RSP / advanced CEP only after simple stream processing becomes insufficient  
└── Do not push every telemetry tick into RDF or Neo4j  
└── Keep Redis as the current operational state source for runtime decisions

---

## **Real-Time World State Core Principles**

1. Current State Is Not Static Knowledge  
   └── Layer 6 represents what is happening now; Layer 5 stores memory and knowledge; Layer 4 defines meaning.  
2. Redis Is the Runtime Current-state Priority  
   └── Worker location, robot state, equipment status, zone risk, approval state, and execution state should be read from world state cache when freshness matters.  
3. Ontology Defines Meaning, World State Holds Values  
   └── Ontology defines what WorkerLocation means; Layer 6 stores where the worker is now.  
4. Raw Signals Are Not Trusted State  
   └── Raw sensor, robot, PLC, SCADA, and fleet data must be normalized, validated, timestamped, and source-tracked before becoming world state.  
5. Every State Needs Freshness  
   └── Current state must include source timestamp, ingestion timestamp, state version, freshness status, and confidence when relevant.  
6. Stale State Must Degrade Safely  
   └── High-risk decisions must block, degrade, or escalate when required state is stale or missing.  
7. Confidence Matters  
   └── Sensor uncertainty, source reliability, calibration status, signal quality, and conflicting sources must affect operational trust.  
8. High-frequency Telemetry Must Not Become Triple Flood  
   └── Sensor ticks, worker location updates, robot telemetry, and equipment telemetry should not write full RDF triples on every update.  
9. Materialize Only Meaningful State Changes  
   └── RDF, Neo4j, event store, or audit materialization should happen at event, threshold, aggregation, confirmation, or audit boundaries.  
10. Kafka Is for Events, Redis Is for Current State  
    └── Kafka provides durable streaming and replay; Redis provides fast current-state lookup.  
11. MQTT Is for Edge and IoT Communication  
    └── MQTT is useful for lightweight field and sensor messaging, often bridged into central event streams.  
12. Time-series Store Is for History and Trends  
    └── TimescaleDB or InfluxDB should store telemetry trends, not replace the current world state cache.  
13. World State Must Be Ontology-grounded  
    └── State updates must map source entities to canonical ontology IRIs or approved operational node IDs.  
14. Conflicting State Must Be Resolved or Escalated  
    └── When sources disagree, source authority, timestamp, confidence, and risk level must control resolution.  
15. Agents Must Consume Fresh Beliefs  
    └── Agent belief cache must be versioned, fresh, source-tracked, and invalidated when stale.  
16. Decision Router Needs Risk Signals, Not Raw Noise  
    └── Layer 6 should generate structured risk signals and state changes, not flood the decision router with every low-level event.  
17. Safety Gate Needs Fresh Evidence  
    └── Safety validation must use fresh world state for high-risk action approval.  
18. Digital Twin Is a Subscriber  
    └── Digital twin visualizes world state updates but does not define operational truth.  
19. External Control Feedback Updates World State  
    └── Fleet manager, robot middleware, PLC / SCADA, and equipment controller feedback must update execution and operational state.  
20. Missing Data Is a State  
    └── Sensor offline, heartbeat lost, stale telemetry, or missing fleet feedback must be represented as operational state.  
21. Real-time Layer Must Be Bounded  
    └── Critical runtime paths must avoid full graph scans, full ontology reasoning, unbounded retrieval, or heavy LLM calls.  
22. World State Must Be Observable  
    └── Lag, freshness, dropped events, stale state, sensor confidence, and conflict rate must be monitored.  
23. Unauthorized Sources Must Not Update State  
    └── State update publishers must be authenticated, authorized, scoped, and audited.  
24. Current State and Historical Memory Must Synchronize  
    └── Meaningful state changes should be appended to event history and semantic memory when finalized or operationally important.  
25. Layer 6 Is the Live Nervous System  
    └── Its purpose is to keep the ontology-centric system aware of the live site state without becoming the policy engine, ontology kernel, or physical control system.

