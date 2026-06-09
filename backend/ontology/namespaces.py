"""
LEDO.ai - IRI 네임스페이스 + 외부 표준 매핑

이 모듈은 모든 IRI (Internationalized Resource Identifier) 의
단일 진실 원천 (Single Source of Truth).

설계 원칙:
─────────────────────────────────────
1. config.py 에서 LEDO_NAMESPACE 가져오기 (환경별 분리)
2. 외부 표준 네임스페이스는 영구 고정 (W3C/ISO/ETSI 발표값)
3. owlready2 + rdflib 모두 호환

참조 표준:
- W3C RDF 1.1 Concepts (2014)
- RFC 3987 (IRI - Internationalized Resource Identifier)
- ISO/IEC 21838-2:2021 (BFO 2.0)
- W3C SOSA/SSN (Sensor, Observation, Sample, Actuator)
- ETSI TS 103 264 (SAREF - Smart Applications REFerence)
- W3C PROV-O (Provenance Ontology)
- BuildingSMART ifcOWL (IFC Web Ontology Language)
- W3C BOT (Building Topology Ontology)

Python 버전: 3.14+
"""
from typing import Final

from rdflib import Namespace
from rdflib.namespace import (
    RDF,
    RDFS,
    OWL,
    SKOS,
    XSD,
    DCTERMS,
    PROV,
    GEO,
    TIME,
)

from config import settings


# ════════════════════════════════════════════════════════════
# 1. LEDO 시스템 네임스페이스 (.env 에서 환경별 결정)
# ════════════════════════════════════════════════════════════
LEDO: Final[Namespace] = Namespace(settings.LEDO_NAMESPACE)


# ════════════════════════════════════════════════════════════
# 2. 외부 표준 네임스페이스 (영구 고정)
# 한번 발표된 URL 은 절대 변경되지 않음 (Cool URIs)
# ════════════════════════════════════════════════════════════

# ─── 상위 온톨로지 (Top-Level Ontologies) ───
BFO: Final[Namespace] = Namespace(
    "http://purl.obolibrary.org/obo/"
)
"""ISO/IEC 21838-2:2021 - Basic Formal Ontology (BFO 2.0)"""

# ─── 센서 + IoT (Sensor + IoT) ───
SOSA: Final[Namespace] = Namespace(
    "http://www.w3.org/ns/sosa/"
)
"""W3C SOSA - Sensor, Observation, Sample, Actuator"""

SSN: Final[Namespace] = Namespace(
    "http://www.w3.org/ns/ssn/"
)
"""W3C SSN - Semantic Sensor Network"""

SAREF: Final[Namespace] = Namespace(
    "https://saref.etsi.org/core/"
)
"""ETSI TS 103 264 - SAREF (Smart Applications REFerence)"""

SAREF4BLDG: Final[Namespace] = Namespace(
    "https://saref.etsi.org/saref4bldg/"
)
"""ETSI - SAREF4BLDG (Building extension for SAREF)"""

# ─── BIM / 건축 (Building Information Modeling) ───
IFCOWL: Final[Namespace] = Namespace(
    "https://standards.buildingsmart.org/IFC/DEV/IFC4_3/OWL#"
)
"""BuildingSMART - ifcOWL (IFC Web Ontology Language)"""

BOT: Final[Namespace] = Namespace(
    "https://w3id.org/bot#"
)
"""W3C - BOT (Building Topology Ontology)"""

# ─── 단위 + 측정 (Units + Measurements) ───
QUDT: Final[Namespace] = Namespace(
    "http://qudt.org/schema/qudt/"
)
"""NASA QUDT - Quantities, Units, Dimensions, Types"""

UNIT: Final[Namespace] = Namespace(
    "http://qudt.org/vocab/unit/"
)
"""QUDT 단위 어휘 (m, kg, s, °C 등)"""

# ─── 권리 + 접근 제어 (Rights + Access Control) ───
ODRL: Final[Namespace] = Namespace(
    "http://www.w3.org/ns/odrl/2/"
)
"""W3C ODRL - Open Digital Rights Language"""


# ════════════════════════════════════════════════════════════
# 3. 네임스페이스 사전 (rdflib Graph 등록용)
# ════════════════════════════════════════════════════════════
ALL_NAMESPACES: Final[dict[str, Namespace]] = {
    # LEDO 시스템
    "ledo": LEDO,

    # 기본 시맨틱 웹 (rdflib 내장)
    "rdf": RDF,
    "rdfs": RDFS,
    "owl": OWL,
    "skos": SKOS,
    "xsd": XSD,
    "dcterms": DCTERMS,
    "prov": PROV,
    "geo": GEO,
    "time": TIME,

    # 상위 온톨로지
    "bfo": BFO,

    # 센서 + IoT
    "sosa": SOSA,
    "ssn": SSN,
    "saref": SAREF,
    "saref4bldg": SAREF4BLDG,

    # BIM
    "ifcowl": IFCOWL,
    "bot": BOT,

    # 단위
    "qudt": QUDT,
    "unit": UNIT,

    # 권리
    "odrl": ODRL,
}


# ════════════════════════════════════════════════════════════
# 4. 헬퍼 함수
# ════════════════════════════════════════════════════════════
def get_iri(class_name: str) -> str:
    """LEDO 클래스 이름 → 전체 IRI 반환

    예시:
        get_iri("Worker") 
        → "http://ledo.ai/ontology/2026/06/Worker"
    """
    return f"{LEDO}{class_name}"


def get_external_iri(prefix: str, term: str) -> str:
    """외부 표준의 IRI 반환

    예시:
        get_external_iri("bfo", "MaterialEntity")
        → "http://purl.obolibrary.org/obo/MaterialEntity"
        
        get_external_iri("sosa", "Sensor")
        → "http://www.w3.org/ns/sosa/Sensor"
    """
    ns = ALL_NAMESPACES.get(prefix.lower())
    if ns is None:
        raise ValueError(
            f"알 수 없는 네임스페이스 prefix: '{prefix}'. "
            f"사용 가능: {list(ALL_NAMESPACES.keys())}"
        )
    return f"{ns}{term}"


def list_namespaces() -> list[str]:
    """등록된 모든 네임스페이스 prefix 목록"""
    return list(ALL_NAMESPACES.keys())


def bind_to_graph(graph) -> None:
    """rdflib Graph 에 모든 네임스페이스 등록

    사용법:
        from rdflib import Graph
        g = Graph()
        bind_to_graph(g)
        # 이제 g 에 ledo:Worker 같은 짧은 표기 사용 가능
    """
    for prefix, ns in ALL_NAMESPACES.items():
        graph.bind(prefix, ns)