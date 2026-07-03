from pydantic import BaseModel


class Settings(BaseModel):
    backend_port: int = 8765
    postgres_dsn: str = "postgresql://ledo:ledo@localhost:5432/ledo_mvp"
    redis_url: str = "redis://localhost:6379/0"
    fuseki_query_url: str = "http://localhost:3030/ledo/query"
    fuseki_update_url: str = "http://localhost:3030/ledo/update"
    opa_url: str = "http://localhost:8181/v1/data/ledo/mvp/allow"
    redpanda_bootstrap_servers: str = "localhost:9092"
    emergency_stop_distance_m: float = 2.0
    max_snapshot_age_ms: int = 1000
    policy_bundle_version: str = "mvp-phase-2-rego-v1"
    ontology_version: str = "ot-mvp-phase-2-v1"
    snapshot_version: str = "snapshot-mvp-phase-2-v1"


settings = Settings()

