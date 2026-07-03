from .graph_store import GraphStore
from .schemas import OntologyGraphEdge, OntologyGraphNode


def project_graph(store: GraphStore) -> tuple[list[OntologyGraphNode], list[OntologyGraphEdge]]:
    nodes = [
        OntologyGraphNode(id=row["id"], label=row["label"], type=row["type"], data={"source": "GraphDBQueryResult"})
        for row in store.query_nodes()
    ]
    edges = [
        OntologyGraphEdge(id=row["id"], source=row["source"], target=row["target"], label=row["label"])
        for row in store.query_edges()
    ]
    return nodes, edges

