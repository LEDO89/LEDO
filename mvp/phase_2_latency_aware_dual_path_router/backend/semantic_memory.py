from .graph_store import GraphStore


class SemanticMemory:
    def __init__(self, graph_store: GraphStore) -> None:
        self.graph_store = graph_store

    def lookup_context(self, trace_id: str) -> dict:
        return {
            "trace_id": trace_id,
            "source": "GraphDBQueryResult",
            "node_count": len(self.graph_store.query_nodes()),
            "edge_count": len(self.graph_store.query_edges()),
            "reason": "Semantic memory lookup reads Graph DB projection and never becomes Safety Gate hot path input.",
        }

