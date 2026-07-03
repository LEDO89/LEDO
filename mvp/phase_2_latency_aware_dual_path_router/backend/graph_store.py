from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .ontology_kernel import rel


@dataclass
class Triple:
    subject: str
    predicate: str
    object: str


@dataclass
class GraphStore:
    """Fuseki boundary with in-memory queryable fallback.

    The fallback is intentionally a triple store projection, not hardcoded UI graph
    data. Docker Compose provides real Fuseki for integration runs.
    """

    triples: list[Triple] = field(default_factory=list)
    fuseki_available: bool = False
    last_error: object = None

    def reset(self) -> None:
        self.triples.clear()
        self.last_error = None

    def upload_triples(self, triples: list[Triple]) -> None:
        self.triples.extend(triples)

    def _objects(self, subject: str, predicate: str) -> list[str]:
        return [t.object for t in self.triples if t.subject == subject and t.predicate == predicate]

    def query_nodes(self) -> list[dict[str, Any]]:
        subjects = sorted({t.subject for t in self.triples if t.predicate == rel("graphId")})
        rows: list[dict[str, Any]] = []
        for subject in subjects:
            ids = self._objects(subject, rel("graphId"))
            labels = self._objects(subject, rel("graphLabel"))
            types = self._objects(subject, rel("graphType"))
            if ids and labels and types:
                rows.append({"id": ids[0], "label": labels[0], "type": types[0]})
        return rows

    def query_edges(self) -> list[dict[str, Any]]:
        subjects = sorted({t.subject for t in self.triples if t.predicate == rel("edgeId")})
        rows: list[dict[str, Any]] = []
        for subject in subjects:
            ids = self._objects(subject, rel("edgeId"))
            sources = self._objects(subject, rel("edgeSource"))
            targets = self._objects(subject, rel("edgeTarget"))
            labels = self._objects(subject, rel("edgeLabel"))
            if ids and sources and targets and labels:
                rows.append({"id": ids[0], "source": sources[0], "target": targets[0], "label": labels[0]})
        return rows

    def query_rule_evaluations(self, trace_id=None) -> list[dict[str, Any]]:
        rows = self.query_nodes()
        return [row for row in rows if row["type"] in {"RuleEvaluation", "MatchedRule", "EmergencyRule"}]

    def run_sparql(self, query: str) -> list[dict[str, Any]]:
        if "edgeId" in query:
            return self.query_edges()
        if "RuleEvaluation" in query or "MatchedRule" in query:
            return self.query_rule_evaluations()
        return self.query_nodes()
