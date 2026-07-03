DECISION_CHAIN_NODES = """
SELECT ?id ?label ?type WHERE {
  ?s <https://ledo.example/ontology/mvp-phase-2#graphId> ?id ;
     <https://ledo.example/ontology/mvp-phase-2#graphLabel> ?label ;
     <https://ledo.example/ontology/mvp-phase-2#graphType> ?type .
}
"""

DECISION_CHAIN_EDGES = """
SELECT ?id ?source ?target ?label WHERE {
  ?e <https://ledo.example/ontology/mvp-phase-2#edgeId> ?id ;
     <https://ledo.example/ontology/mvp-phase-2#edgeSource> ?source ;
     <https://ledo.example/ontology/mvp-phase-2#edgeTarget> ?target ;
     <https://ledo.example/ontology/mvp-phase-2#edgeLabel> ?label .
}
"""

EVENTS_BY_TRACE_ID = """
SELECT ?id ?label ?type WHERE {
  ?s <https://ledo.example/ontology/mvp-phase-2#traceId> ?trace ;
     <https://ledo.example/ontology/mvp-phase-2#graphId> ?id ;
     <https://ledo.example/ontology/mvp-phase-2#graphLabel> ?label ;
     <https://ledo.example/ontology/mvp-phase-2#graphType> ?type .
}
"""

EXECUTION_BOUNDARY = """
SELECT ?id ?label ?type WHERE {
  ?s <https://ledo.example/ontology/mvp-phase-2#graphType> "PhysicalWorldBoundary" ;
     <https://ledo.example/ontology/mvp-phase-2#graphId> ?id ;
     <https://ledo.example/ontology/mvp-phase-2#graphLabel> ?label ;
     <https://ledo.example/ontology/mvp-phase-2#graphType> ?type .
}
"""

RULE_EVALUATIONS_BY_TRACE_ID = """
SELECT ?id ?label ?type WHERE {
  ?s <https://ledo.example/ontology/mvp-phase-2#graphType> ?type ;
     <https://ledo.example/ontology/mvp-phase-2#graphId> ?id ;
     <https://ledo.example/ontology/mvp-phase-2#graphLabel> ?label .
  FILTER(?type = "RuleEvaluation" || ?type = "MatchedRule" || ?type = "EmergencyRule")
}
"""

