# **Ontology Centric “Knowledge & Semantic Memory” Stack Mapping**

## **Layer 5\. Knowledge & Semantic Memory Layer**

─ Core Position  
└── Knowledge & Semantic Memory is the persistent knowledge and memory layer of the ontology-centric system  
└── It stores static knowledge, site instances, graph relationships, documents, historical events, embeddings, incident records, offline reasoning results, and construction-domain knowledge  
└── It connects ontology-defined meaning with real project data, documents, events, evidence, and operational memory  
└── It supports retrieval, context expansion, RAG, semantic search, historical analysis, and evidence binding  
└── It does not define ontology meaning independently  
└── It does not replace the Core Ontology Kernel  
└── It does not replace Real-Time World State  
└── It does not make final safety decisions  
└── It does not execute actions  
└── It provides grounded memory and evidence for agents, decision router, safety gate, UI, audit, and reporting

---

## **Core Role**

└── Store ontology-grounded knowledge instances  
└── Store RDF triples and semantic facts  
└── Store graph relationships between workers, robots, equipment, zones, tasks, risks, actions, documents, and events  
└── Store documents, manuals, inspection reports, incident reports, BIM metadata, equipment manuals, and compliance documents  
└── Store embeddings for semantic search, similar incident retrieval, document retrieval, and entity search  
└── Store historical events, approval records, execution records, and incident history  
└── Provide semantic memory for agents and RAG pipelines  
└── Provide evidence-bound retrieval for decision cases and approval review  
└── Preserve provenance, versioning, source authority, freshness, and trust metadata  
└── Support construction-domain reusable knowledge across projects and sites

---

## **Core Technologies**

└── RDF Triple Store  
└── GraphDB  
└── Apache Jena Fuseki  
└── Blazegraph  
└── Neo4j  
└── Cypher  
└── SPARQL  
└── PostgreSQL  
└── pgvector  
└── Vector Store  
└── Document Store  
└── MinIO / S3  
└── RAG  
└── Semantic Memory  
└── Historical Event Store  
└── Construction Knowledge Base  
└── PROV-O  
└── RDFLib  
└── SPARQLWrapper  
└── Object Storage  
└── Metadata Store

---

## **Optional Technologies**

└── Stardog  
└── Qdrant  
└── Milvus  
└── Weaviate  
└── FAISS  
└── Elasticsearch / OpenSearch  
└── Apache Tika  
└── Unstructured  
└── OCR Pipeline  
└── BM25 Search  
└── Hybrid Search Engine  
└── Reranker Model  
└── Knowledge Graph Embeddings  
└── Data Catalog  
└── Data Lineage Tool  
└── GraphQL Read API optional  
└── Event Sourcing Store  
└── TimescaleDB for historical time-series events

---

## **Key Data Stack**

└── OWL Ontology Reference  
└── Knowledge Graph  
└── RDF Triple Store  
└── Vector Store  
└── Document Store  
└── Semantic Memory  
└── Historical Events  
└── Construction Knowledge Base  
└── Safety Manuals  
└── Inspection Reports  
└── Incident Reports  
└── BIM Metadata  
└── Equipment Manuals  
└── Legal / Compliance Documents  
└── Offline Reasoning Results  
└── Materialized Inferred Facts  
└── Evidence Records  
└── Approval Records  
└── Execution Feedback Records  
└── Lessons Learned  
└── Domain Glossary  
└── Entity Aliases  
└── Mapping Rules

---

## **Storage Responsibility Stack**

└── RDF Triple Store  
└── formal semantic facts  
└── ontology-grounded triples  
└── named graphs  
└── materialized inferred facts  
└── provenance graph

└── Neo4j  
└── graph read model  
└── operational relationship exploration  
└── dashboard graph view  
└── graph traversal for contextual neighborhood

└── PostgreSQL  
└── metadata  
└── event history  
└── approval records  
└── execution records  
└── document metadata  
└── audit-linked records

└── pgvector / Vector Store  
└── document chunk embeddings  
└── entity description embeddings  
└── incident summary embeddings  
└── policy rule embeddings  
└── semantic similarity retrieval

└── MinIO / S3  
└── raw documents  
└── drawings  
└── reports  
└── manuals  
└── images  
└── BIM files  
└── long-term evidence artifacts

└── Historical Event Store  
└── time-ordered operational memory  
└── event sequence  
└── command history  
└── approval history  
└── execution history  
└── incident history

---

## **RDF Triple Store Stack**

└── RDF Store  
└── SPARQL Endpoint  
└── Named Graphs  
└── GraphDB  
└── Apache Jena Fuseki  
└── Blazegraph  
└── Stardog optional  
└── Turtle  
└── RDF/XML  
└── JSON-LD  
└── SPARQL Query  
└── SPARQL Update  
└── SPARQL CONSTRUCT  
└── SPARQL ASK  
└── Named Graph Partitioning  
└── Materialized Inference Graph  
└── Provenance Graph

Usage:  
└── Store ontology-grounded structured knowledge  
└── Store semantic facts that need RDF / OWL compatibility  
└── Store inferred facts from offline reasoning or batch materialization  
└── Store provenance and evidence relationships  
└── Provide SPARQL-based retrieval for exact semantic queries

Boundary:  
└── RDF Triple Store preserves semantic facts  
└── It should not receive every high-frequency sensor tick  
└── Current runtime state should be handled by Layer 6 Real-Time World State

---

## **Knowledge Graph Stack**

└── Entity Graph  
└── Event Graph  
└── Evidence Graph  
└── Document-Entity Graph  
└── Policy Graph  
└── Risk Graph  
└── Task Graph  
└── Construction Process Graph  
└── Worker Context Graph  
└── Robot Context Graph  
└── Equipment Context Graph  
└── Zone Context Graph  
└── Incident Context Graph  
└── Approval Context Graph  
└── Execution Context Graph

Graph Relationships:  
└── Worker locatedIn Zone  
└── Robot assignedTo Task  
└── Equipment hasRisk Risk  
└── Incident hasEvidence Document  
└── Task requiresCapability Capability  
└── ActionCandidate hasEvidence Evidence  
└── DecisionCase refersTo ActionCandidate  
└── ExecutionRequest targets OperationalNode  
└── Policy appliesTo ActionType

Usage:  
└── Explore operational relationships  
└── Expand context around a worker, zone, task, incident, action, or decision case  
└── Support graph explorer UI  
└── Support agent context retrieval  
└── Support evidence-bound decision review

Boundary:  
└── Neo4j can be used as a graph read model  
└── Formal ontology semantics should remain grounded in RDF / OWL / SHACL where required  
└── Neo4j is useful for operational graph exploration but should not replace the ontology kernel

---

## **Neo4j / Cypher Stack**

└── Neo4j  
└── Cypher  
└── Graph Read Model  
└── Entity Relationship Query  
└── Context Neighborhood Query  
└── Path Query  
└── Risk Relationship Query  
└── Incident Relationship Query  
└── Task Dependency Query  
└── Graph Explorer API  
└── Graph Projection  
└── Graph Visualization Dataset

Usage:  
└── Fast graph traversal  
└── Graph explorer backend  
└── Operational relationship view  
└── Context expansion for agents and UI  
└── Dashboard graph queries

Boundary:  
└── Frontend must not connect directly to Neo4j  
└── Neo4j access must go through FastAPI or backend graph service  
└── Neo4j may be a read model derived from ontology and event data  
└── Neo4j should not independently redefine canonical ontology meaning

---

## **Vector Store Stack**

└── pgvector  
└── Qdrant optional  
└── Milvus optional  
└── Weaviate optional  
└── FAISS local development optional  
└── Embedding Store  
└── Semantic Similarity Search  
└── Hybrid Search  
└── Metadata-filtered Retrieval  
└── Vector Index Versioning  
└── Embedding Model Versioning  
└── HNSW Index  
└── Re-embedding Pipeline  
└── Vector Namespace / Collection Separation

Embedding Types:  
└── Document Chunk Embeddings  
└── Entity Description Embeddings  
└── Incident Summary Embeddings  
└── Event Summary Embeddings  
└── Policy Rule Embeddings  
└── Safety Procedure Embeddings  
└── Equipment Manual Embeddings  
└── Construction Method Embeddings

Vector Rule:  
└── Vector similarity supports recall  
└── Vector similarity does not define truth  
└── Vector-only results must not trigger action, approval, emergency response, or safety decision

---

## **pgvector Physical Table Stack**

└── document\_chunk\_embeddings  
└── entity\_description\_embeddings  
└── incident\_summary\_embeddings  
└── event\_summary\_embeddings  
└── policy\_rule\_embeddings  
└── safety\_procedure\_embeddings  
└── equipment\_manual\_embeddings  
└── construction\_method\_embeddings

Table Separation Rule:  
└── Do not mix all embeddings into one generic table  
└── Different retrieval purposes should use separate tables, namespaces, or collections  
└── Policy and safety embeddings must be isolated from general document embeddings  
└── Each embedding table should have its own metadata schema, access policy, and re-embedding schedule

---

## **Document Store Stack**

└── Raw Document Storage  
└── Structured Document Metadata  
└── MinIO / S3-compatible Object Storage  
└── PostgreSQL Document Metadata  
└── Document Parser  
└── OCR Pipeline optional  
└── Chunking Strategy  
└── Document Versioning  
└── Document Provenance  
└── Document Access Control  
└── Document-to-Entity Linking  
└── Document-to-Evidence Binding

Document Types:  
└── Safety Manuals  
└── Inspection Reports  
└── Incident Reports  
└── BIM Metadata  
└── Equipment Manuals  
└── Legal / Compliance Documents  
└── Construction Drawings  
└── Permits  
└── Work Procedures  
└── Checklists  
└── Maintenance Records  
└── Robot Operation Manuals  
└── Emergency Procedures

Document Rule:  
└── Raw documents remain source evidence  
└── Parsed chunks and embeddings support retrieval  
└── Operational decisions require source attribution, version, authority, and evidence binding

---

## **Historical Event Store Stack**

└── PostgreSQL Event Store  
└── Event Sourcing Pattern  
└── TimescaleDB optional for time-series history  
└── Command Event History  
└── Approval Event History  
└── Execution Event History  
└── Incident Event History  
└── Alert Event History  
└── Sensor Event History  
└── Worker Location History  
└── Robot Telemetry History  
└── Equipment Telemetry History  
└── Policy Decision History  
└── Ontology Change History  
└── Audit Event History  
└── Event ID  
└── Correlation ID  
└── Causation ID  
└── Sequence Number

Usage:  
└── Preserve operational memory  
└── Reconstruct timelines  
└── Support audit review  
└── Support incident analysis  
└── Support lessons learned  
└── Support replay, debugging, and historical comparison

Boundary:  
└── Historical events are confirmed memory  
└── Current operational facts belong to Layer 6 Real-Time World State  
└── Layer 5 can store finalized or materialized event history

---

## **Semantic Memory Stack**

└── Entity Memory  
└── Event Memory  
└── Task Memory  
└── Incident Memory  
└── Risk Memory  
└── Worker Context Memory  
└── Robot Context Memory  
└── Equipment Context Memory  
└── Site Context Memory  
└── Policy Decision Memory  
└── Action Candidate Memory  
└── Approval Memory  
└── Execution Feedback Memory  
└── Evidence-linked Memory  
└── Time-aware Memory  
└── Ontology-grounded Memory

Semantic Memory Rule:  
└── Semantic Memory connects context  
└── Semantic Memory does not define semantic truth  
└── Memory used for high-risk decisions must be ontology-grounded, evidence-bound, versioned, and policy-checked

---

## **Construction Knowledge Base Stack**

└── Construction Methods  
└── Safety Rules  
└── Work Procedures  
└── Inspection Criteria  
└── Equipment Operation Rules  
└── Robot Operation Rules  
└── Emergency Procedures  
└── Permit Requirements  
└── Quality Checklists  
└── Risk Control Measures  
└── Standard Operating Procedures  
└── Lessons Learned  
└── Incident Case Library  
└── Domain Glossary  
└── Regulation-linked Knowledge  
└── Ontology-linked Knowledge Articles

Usage:  
└── Provide reusable construction-domain knowledge  
└── Support retrieval for agents and supervisors  
└── Support safety and compliance decision context  
└── Support training, inspection, and incident analysis  
└── Support multi-site knowledge reuse

---

## **RAG / Retrieval Stack**

└── Query Understanding  
└── Intent Classification  
└── Entity Grounding  
└── SPARQL Retrieval  
└── Graph Neighborhood Retrieval  
└── Vector Similarity Retrieval  
└── Keyword / BM25 Retrieval  
└── Metadata-filtered Retrieval  
└── Document Evidence Retrieval  
└── Historical Event Retrieval  
└── Context Fusion  
└── Reranking  
└── Citation / Evidence Binding  
└── LLM Response Generation  
└── Output Grounding Check  
└── Policy-sensitive Response Filtering

Retrieval Sources:  
└── RDF Triple Store  
└── Neo4j Graph Read Model  
└── PostgreSQL Metadata  
└── pgvector  
└── Document Store  
└── Historical Event Store  
└── Construction Knowledge Base

Retrieval Rule:  
└── SPARQL has priority for exact ontology-grounded facts  
└── Graph retrieval has priority for connected operational context  
└── Vector retrieval has priority for similarity and recall  
└── Keyword search has priority for exact document terms, permit numbers, regulation clauses, and drawing IDs  
└── Metadata filtering must be applied before final response generation

---

## **Query-specific Retrieval Path Stack**

└── Safety-critical Query  
└── Current World State from Layer 6  
└── Ontology Policy / Rule Lookup  
└── SHACL / Policy Context  
└── Evidence Retrieval  
└── Human Approval if required  
└── Vector retrieval only as supporting context

└── Real-time Worker / Zone / Task Query  
└── Layer 6 World State  
└── Freshness Validation  
└── SPARQL Static Meaning Lookup  
└── Graph Neighborhood Context  
└── Event Timeline if required

└── Policy / Rule Query  
└── SPARQL Policy Lookup  
└── Document Evidence Retrieval  
└── Policy / Rule Embedding Search  
└── Source Authority Check  
└── Version Check

└── Incident Similarity Query  
└── Incident Summary Vector Search  
└── Graph Neighborhood Retrieval  
└── Historical Event Timeline  
└── Ontology Grounding  
└── Evidence Binding

└── Document Evidence Query  
└── Metadata Filter  
└── Keyword / BM25 Retrieval  
└── Document Chunk Vector Search  
└── Entity Linking  
└── Source Citation Binding

└── General Knowledge Query  
└── Hybrid Retrieval  
└── Reranking  
└── Grounding Check  
└── Evidence-bound Response

---

## **Entity Linking & Grounding Stack**

└── Named Entity Recognition  
└── Ontology Entity Resolution  
└── IRI Mapping  
└── Alias Dictionary  
└── Synonym Dictionary  
└── Construction Term Dictionary  
└── Multilingual Label Mapping  
└── Worker / Equipment / Zone / Task / Risk Linking  
└── Document-to-Entity Linking  
└── Event-to-Entity Linking  
└── Confidence Score  
└── Ambiguity Handling  
└── Human Verification for Low-confidence Grounding

Confidence Policy:  
└── High-confidence link: automatic linking allowed for low-risk use  
└── Medium-confidence link: review required for safety-critical or execution-related knowledge  
└── Low-confidence link: automatic operational use blocked  
└── Conflict case: reviewer must select canonical entity  
└── Unknown entity: create candidate entity only, then ontology governance review

---

## **Provenance & Evidence Stack**

└── PROV-O  
└── Source Document Reference  
└── Sensor Source Reference  
└── Human Reporter Reference  
└── System Event Reference  
└── Agent Output Reference  
└── LLM Recommendation Reference  
└── Evidence Chain  
└── Confidence Score  
└── Trust Level  
└── Timestamp  
└── Review Status  
└── Approval Status  
└── Audit Trace  
└── Explainable Knowledge Lineage

Evidence Rule:  
└── Knowledge used for decisions must preserve source, timestamp, trust level, version, and evidence reference  
└── High-risk knowledge must not be used without sufficient evidence or validation

---

## **Knowledge Ingestion Stack**

└── Document Upload  
└── Document Parsing  
└── Metadata Extraction  
└── Entity Extraction  
└── Relation Extraction  
└── Event Extraction  
└── Ontology Entity Linking  
└── IRI Mapping  
└── RDF Triple Generation  
└── Vector Embedding Generation  
└── Document Chunk Indexing  
└── Provenance Capture  
└── SHACL Validation  
└── Human Review for Critical Knowledge  
└── Knowledge Approval Workflow  
└── Knowledge Publication  
└── Cache Invalidation  
└── Re-embedding Trigger

Ingestion Rule:  
└── New knowledge must be grounded to ontology entities before operational use  
└── High-risk knowledge requires validation and review  
└── Document evidence must remain linked to extracted triples and embeddings

---

## **Offline Reasoning Results Stack**

└── HermiT Result  
└── Pellet Result  
└── Consistency Check Result  
└── Inferred Class Hierarchy  
└── Equivalent Class Result  
└── Disjointness Violation Result  
└── Unsatisfiable Class Result  
└── Materialized Inferred Facts  
└── Batch Materialization Output  
└── Ontology Release Validation Result  
└── Reasoning Report  
└── Inference Version  
└── Reasoning Timestamp

Boundary:  
└── Offline reasoning results can be stored in Layer 5  
└── The reasoning process itself belongs to ontology validation and release pipeline  
└── Materialized inferred facts used operationally must be freshness-checked and version-aligned

---

## **Knowledge Versioning Stack**

└── Ontology Version Reference  
└── RDF Named Graph Version  
└── Document Version  
└── Embedding Model Version  
└── Vector Index Version  
└── Event Sequence Number  
└── Knowledge Article Version  
└── Mapping Rule Version  
└── Source Document Version  
└── Valid From / Valid Until  
└── Superseded Knowledge Tracking  
└── Rollback Strategy

Versioning Rule:  
└── Knowledge must be versioned across RDF, graph, document, vector, event, and ontology references  
└── A retrieved answer must know which version of knowledge it used

---

## **Stale Knowledge Detection Stack**

└── validFrom  
└── validUntil  
└── supersededBy  
└── document expiry date  
└── regulation revision date  
└── manual version mismatch  
└── embedding model version mismatch  
└── vector index stale flag  
└── outdated policy detection  
└── stale incident lesson detection  
└── scheduled freshness scan  
└── stale knowledge alert  
└── auto-quarantine for expired high-risk knowledge

Stale Knowledge Rule:  
└── Expired, superseded, version-mismatched, contradictory, or low-confidence knowledge must be flagged, quarantined, or sent for review

---

## **Access Control Stack**

└── Knowledge Access Policy  
└── Document-level Permission  
└── Entity-level Permission  
└── Field-level Redaction  
└── Role-based Knowledge Access  
└── Attribute-based Knowledge Access  
└── Project-level Access Scope  
└── Site-level Access Scope  
└── Contractor / Subcontractor Boundary  
└── Sensitive Incident Data Protection  
└── Worker Privacy Protection  
└── Retrieval-time Permission Filtering  
└── Post-retrieval Redaction  
└── Knowledge Access Audit Log  
└── Prompt Injection Detection for Retrieved Documents  
└── Data Exfiltration Guardrail

Access Rule:  
└── Access control must apply during retrieval, not only after retrieval  
└── Unauthorized knowledge must not reach agents, users, or generated responses

---

## **Memory API Stack**

└── Knowledge Query API  
└── Entity Memory API  
└── Document Retrieval API  
└── Event Timeline API  
└── Hybrid Retrieval API  
└── Vector Search API  
└── SPARQL Query API  
└── Evidence Retrieval API  
└── Construction Knowledge Base API  
└── Memory Update API  
└── Knowledge Approval API  
└── Graph Context API  
└── Similar Incident API  
└── Document Evidence API

DTO Stack:  
└── EntityMemoryDTO  
└── EventMemoryDTO  
└── DocumentRefDTO  
└── EvidenceDTO  
└── KnowledgeArticleDTO  
└── RetrievalResultDTO  
└── HybridContextDTO  
└── ProvenanceDTO  
└── TrustScoreDTO  
└── MemoryUpdateDTO  
└── KnowledgeVersionDTO  
└── ConstructionKnowledgeDTO

Rule:  
└── APIs should return structured DTOs with evidence, source, version, confidence, and access metadata  
└── Raw database records should not be exposed directly

---

## **Agent Memory Integration Stack**

└── Agent Working Memory  
└── Agent Episodic Memory  
└── Agent Semantic Memory  
└── Tool-use History  
└── Action Candidate History  
└── Policy Decision Context  
└── Retrieved Evidence Context  
└── Prior Incident Context  
└── Previous Task Context  
└── Human Feedback Memory  
└── Memory Summarization  
└── Memory Compression  
└── Memory Expiration Policy  
└── Ontology-grounded Recall

Agent Memory Rule:  
└── Agent recall must be ontology-grounded  
└── Agent memory must preserve evidence references  
└── Agent memory must not bypass governance, policy, or safety gate validation

---

## **Memory Observability Stack**

└── SPARQL Query Latency  
└── Vector Search Latency  
└── Document Retrieval Latency  
└── Hybrid Retrieval Latency  
└── Entity Linking Accuracy  
└── Grounding Failure Rate  
└── Retrieval Hit Rate  
└── Retrieval Precision  
└── Stale Knowledge Rate  
└── Conflicting Knowledge Count  
└── Embedding Index Drift  
└── RDF / Vector / Document Sync Lag  
└── Memory Update Failure Rate  
└── RAG Grounding Failure Rate  
└── Evidence Missing Rate

Observability Rule:  
└── Memory retrieval must be measurable  
└── Slow, stale, ungrounded, or low-confidence retrieval must be detected

---

## **Runtime Boundary**

└── This layer supports runtime retrieval but should not become the real-time state authority  
└── Current operational facts should come from Layer 6 Real-Time World State  
└── RDF / OWL / SPARQL is the priority source for semantic facts and structured meaning  
└── Redis / world state cache is the priority source for fresh operational state  
└── Vector store supports recall and similarity, not truth or safety decisions  
└── Document store preserves evidence, not automatically validated knowledge  
└── Historical event store preserves confirmed operational memory  
└── High-risk retrieval must be bounded, evidence-bound, version-checked, and policy-aware

---

## **Not Responsible For**

└── Defining ontology meaning independently  
└── Replacing Core Ontology Kernel  
└── Holding high-frequency current state as the real-time source of truth  
└── Replacing Real-Time World State Layer  
└── Making final safety decisions  
└── Approving actions  
└── Creating ApprovedAction independently  
└── Executing physical commands  
└── Controlling robots, PLCs, SCADA, equipment, or fleet managers  
└── Replacing Governance / Policy / Security Layer  
└── Replacing Safety Gate validation  
└── Treating vector search as authority  
└── Treating documents as automatically verified truth  
└── Letting LLM-generated memory become canonical knowledge without grounding and review

---

## **Recommended MVP Stack Mapping**

└── Triple Store: Apache Jena Fuseki for shared SPARQL endpoint  
└── Production Triple Store Option: GraphDB or Stardog later  
└── Graph Read Model: Neo4j  
└── Relational Metadata: PostgreSQL  
└── Vector Store: pgvector  
└── Vector Tables: document\_chunk\_embeddings, entity\_description\_embeddings, incident\_summary\_embeddings, policy\_rule\_embeddings  
└── Document Store: PostgreSQL metadata \+ MinIO or local object storage  
└── Historical Events: PostgreSQL event store  
└── Time-Series History: TimescaleDB later if telemetry history grows  
└── Construction Knowledge Base: safety rules, procedures, checklists, manuals, incident cases  
└── Retrieval: SPARQL \+ graph neighborhood \+ pgvector \+ metadata filter \+ keyword search  
└── RAG: evidence-bound RAG with ontology grounding  
└── Entity Linking: canonical IRI mapping \+ alias dictionary \+ confidence policy  
└── Provenance: PROV-O model \+ evidence references  
└── Validation: pySHACL for target validation during ingestion  
└── Backend API: FastAPI \+ Pydantic DTOs  
└── Observability: retrieval latency, grounding failure, stale knowledge, sync lag

MVP Rule:  
└── Start with PostgreSQL \+ pgvector \+ MinIO/local storage \+ Jena Fuseki \+ Neo4j read model only if graph exploration is needed early  
└── Separate embeddings by purpose from the beginning  
└── Do not allow vector-only results to trigger operational actions  
└── Do not store high-frequency telemetry as RDF triples on every update  
└── Keep Layer 5 as memory and evidence, not as the real-time control brain

---

## **Knowledge & Semantic Memory Core Principles**

1. Ontology Defines Meaning  
   └── Layer 4 defines entities, relationships, actions, policies, constraints, and semantic truth.  
2. Semantic Memory Connects Context  
   └── Layer 5 connects ontology-grounded entities with documents, events, evidence, embeddings, and historical memory.  
3. Semantic Memory Must Not Replace Ontology Core  
   └── It retrieves, recalls, stores, and contextualizes knowledge, but does not redefine semantic meaning.  
4. RDF Triple Store Preserves Structured Semantic Facts  
   └── RDF / OWL / SPARQL is the authority for ontology-grounded structured knowledge.  
5. Knowledge Graph Connects Operational Relationships  
   └── Workers, robots, equipment, zones, tasks, risks, incidents, documents, actions, and evidence must be connected through graph relationships.  
6. Neo4j Is a Read Model, Not the Ontology Kernel  
   └── Neo4j supports graph exploration and traversal, but formal semantic meaning remains grounded in RDF / OWL / SHACL.  
7. Vector Store Supports Recall, Not Authority  
   └── Vector similarity improves retrieval but must not define truth, policy, action eligibility, or safety decisions.  
8. Vector-only Results Must Not Trigger Action  
   └── No action, emergency response, approval, or safety decision may be triggered by vector similarity alone.  
9. Documents Are Evidence, Not Automatically Verified Truth  
   └── Documents must be parsed, grounded, versioned, sourced, and reviewed when used for high-risk decisions.  
10. Historical Events Preserve Operational Memory  
    └── Commands, approvals, execution results, incidents, alerts, telemetry summaries, and policy decisions must be preserved as time-ordered memory.  
11. Every Knowledge Item Needs Provenance  
    └── Source, timestamp, confidence, trust level, version, review status, and evidence lineage must be preserved.  
12. High-risk Knowledge Requires Validation  
    └── Safety rules, emergency procedures, robot operation rules, equipment blocking rules, and action-related knowledge require grounding, validation, authority check, and review when required.  
13. Retrieval Must Be Evidence-bound  
    └── Retrieved knowledge used for decisions must include source references, confidence, version, and evidence chain.  
14. Retrieval Path Must Depend on Query Type  
    └── Safety-critical, real-time operational, policy, incident similarity, document evidence, and general knowledge queries must use different retrieval paths.  
15. Exact Structured Retrieval Comes First  
    └── Exact IRI, SPARQL, policy, document ID, or fresh world-state match should prevent unnecessary broad vector search.  
16. Embeddings Must Be Separated by Purpose  
    └── Document chunks, entity descriptions, incident summaries, policy rules, safety procedures, and equipment manuals should use separate tables or collections.  
17. Policy and Safety Embeddings Must Be Isolated  
    └── Policy, emergency, permit, safety, and robot operation embeddings require versioning, authority checks, and access control.  
18. Current Facts Must Prefer Layer 6  
    └── Worker location, robot state, equipment status, zone risk, approval state, and execution state should come from Real-Time World State when freshness matters.  
19. Semantic Facts Must Prefer RDF / OWL  
    └── Class definitions, relationships, policies, constraints, and meaning should come from ontology-grounded semantic stores.  
20. Materialized Knowledge Must Be Freshness-checked  
    └── Operational use of materialized inferred facts must check ontology version, graph version, event sequence, and freshness.  
21. High-frequency Telemetry Must Not Become Triple Flood  
    └── Telemetry updates should go to world state and time-series storage first, with RDF materialization only at meaningful boundaries.  
22. Knowledge Must Be Versioned  
    └── Documents, named graphs, embeddings, vector indexes, ontology references, mapping rules, and event sequences must be versioned.  
23. Stale Knowledge Must Trigger Review  
    └── Expired, superseded, conflicting, low-confidence, or version-mismatched knowledge must be flagged, quarantined, or reviewed.  
24. Entity Linking Controls Operational Use  
    └── High-confidence links may be used in low-risk contexts; low-confidence or conflicting links require review before operational use.  
25. Access Control Applies During Retrieval  
    └── Unauthorized documents, entities, incidents, fields, or knowledge must be filtered before reaching agents or users.  
26. Agent Recall Must Be Ontology-grounded  
    └── Agent memory must resolve entities to canonical IRIs and preserve evidence references.  
27. RAG Must Be Grounded and Bounded  
    └── RAG output must be linked to ontology entities and evidence; high-risk generated answers require validation or review.  
28. Knowledge Must Degrade Safely  
    └── If retrieval, vector search, graph expansion, or document access fails, high-risk use must block, degrade, or escalate.  
29. Memory Must Be Observable  
    └── SPARQL latency, vector search latency, retrieval hit rate, grounding failure, stale knowledge rate, and sync lag must be monitored.  
30. Layer 5 Serves the Ontology-centric Core  
    └── Its purpose is to strengthen ontology-grounded decisions through memory, evidence, history, and context, not bypass the ontology.

