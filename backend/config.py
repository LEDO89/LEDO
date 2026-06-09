"""
LEDO.ai - 중앙 설정 모듈

12-Factor App 원칙에 따라 모든 환경 변수와 임계값을 한 곳에 집중.
변경 시 한 줄만 수정하면 시스템 전체에 반영.

참조 표준:
- 12-Factor App (Adam Wiggins, Heroku, 2011)
- Hexagonal Architecture (Alistair Cockburn, 2005)
- Pydantic Settings (산업 표준 환경 변수 관리)

Python 버전: 3.14+ (PEP 649 lazy annotations 활용)
"""
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """LEDO 시스템 전역 설정

    모든 환경 변수는 .env 파일에서 자동 로드됨.
    Pydantic 이 타입 검증 + 기본값 + 문서화를 한꺼번에 제공.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # ════════════════════════════════════════
    # 1. 시스템 식별 (System Identity)
    # ════════════════════════════════════════
    LEDO_ENV: str = Field(
        default="development",
        description="실행 환경 (development | staging | production)",
    )
    LEDO_LOG_LEVEL: str = Field(
        default="DEBUG",
        description="로그 레벨 (DEBUG | INFO | WARNING | ERROR | CRITICAL)",
    )
    LEDO_API_PORT: int = Field(
        default=8000,
        ge=1024,
        le=65535,
        description="FastAPI 서버 포트",
    )

    # ════════════════════════════════════════
    # 2. IRI 네임스페이스 (W3C 표준)
    # ════════════════════════════════════════
    LEDO_NAMESPACE: str = Field(
        default="http://ledo.ai/ontology/2026/06/",
        description="LEDO 온톨로지 IRI 네임스페이스 (영구 불변)",
    )

    # ════════════════════════════════════════
    # 3. 데이터베이스 (PostgreSQL + Redis)
    # ════════════════════════════════════════
    POSTGRES_URL: str = Field(
        default="postgresql://ledo:ledo_dev_2026@localhost:5432/ledo_db",
        description="PostgreSQL 접속 URL",
    )
    REDIS_URL: str = Field(
        default="redis://localhost:6379",
        description="Redis 접속 URL",
    )

    # ════════════════════════════════════════
    # 4. LLM 설정 (Ollama + Qwen)
    # ════════════════════════════════════════
    OLLAMA_BASE_URL: str = Field(
        default="http://localhost:11434",
        description="Ollama 서버 URL",
    )
    OLLAMA_MODEL: str = Field(
        default="qwen2.5-coder:14b",
        description="기본 LLM 모델",
    )

    # ════════════════════════════════════════
    # 5. 토큰 관리 (14B 모델 한계 대응)
    # ════════════════════════════════════════
    LLM_MAX_CONTEXT_TOKENS: int = Field(
        default=32768,
        ge=1024,
        le=131072,
        description="LLM 컨텍스트 최대 토큰 (Qwen 2.5 = 32K)",
    )
    LLM_RESPONSE_RESERVED_TOKENS: int = Field(
        default=2048,
        ge=256,
        le=8192,
        description="응답용 예약 토큰 (입력에서 제외)",
    )
    LLM_CONTEXT_SAFETY_MARGIN: float = Field(
        default=0.85,
        ge=0.5,
        le=0.95,
        description="컨텍스트 안전 마진 (이 비율 넘으면 컷오프 시작)",
    )

    # ════════════════════════════════════════
    # 6. 재시도 정책 (tenacity)
    # ════════════════════════════════════════
    RETRY_MAX_ATTEMPTS: int = Field(
        default=5,
        ge=1,
        le=10,
        description="최대 재시도 횟수",
    )
    RETRY_INITIAL_WAIT_SEC: float = Field(
        default=1.0,
        ge=0.1,
        le=10.0,
        description="첫 재시도 대기 시간 (초)",
    )
    RETRY_MAX_WAIT_SEC: float = Field(
        default=60.0,
        ge=1.0,
        le=300.0,
        description="최대 대기 시간 (지수 백오프 상한)",
    )
    RETRY_JITTER_SEC: float = Field(
        default=5.0,
        ge=0.0,
        le=30.0,
        description="지터 (분산 시스템 동시 재시도 폭주 방지)",
    )

    # ════════════════════════════════════════
    # 7. 캐싱 정책 (Redis + vLLM APC)
    # ════════════════════════════════════════
    CACHE_TTL_SECONDS: int = Field(
        default=3600,
        ge=60,
        le=86400,
        description="Redis 캐시 기본 TTL (1시간)",
    )
    VLLM_ENABLE_PREFIX_CACHE: bool = Field(
        default=True,
        description="vLLM Automatic Prefix Caching 활성화 (Phase 7)",
    )

    # ════════════════════════════════════════
    # 8. 외부 API (Tavily)
    # ════════════════════════════════════════
    TAVILY_API_KEY: Optional[str] = Field(
        default=None,
        description="Tavily 검색 API 키 (.env에서 로드)",
    )

    # ════════════════════════════════════════
    # 9. 보안 정책 (NIST SP 800-53)
    # ════════════════════════════════════════
    AUDIT_RETENTION_DAYS: int = Field(
        default=2555,
        ge=1,
        le=36500,
        description="감사 로그 보관일 (기본 7년, 산업안전보건법 준수)",
    )
    PII_DEFAULT_RETENTION_DAYS: int = Field(
        default=1095,
        ge=1,
        le=36500,
        description="개인정보 기본 보관일 (3년, 한국 개인정보보호법)",
    )

    # ════════════════════════════════════════
    # 10. 파일 경로 (Project Layout)
    # ════════════════════════════════════════
    PROJECT_ROOT: Path = Field(
        default_factory=lambda: Path(__file__).parent.resolve(),
        description="backend 폴더 절대 경로",
    )

    @property
    def is_production(self) -> bool:
        """프로덕션 환경 여부"""
        return self.LEDO_ENV.lower() == "production"

    @property
    def llm_input_max_tokens(self) -> int:
        """입력에 사용 가능한 최대 토큰 (응답 예약분 제외)"""
        return self.LLM_MAX_CONTEXT_TOKENS - self.LLM_RESPONSE_RESERVED_TOKENS

    @property
    def llm_context_cutoff_threshold(self) -> int:
        """컨텍스트 컷오프 시작 임계값 (안전 마진 적용)"""
        return int(self.llm_input_max_tokens * self.LLM_CONTEXT_SAFETY_MARGIN)


# ════════════════════════════════════════════════════════════
# 싱글톤 인스턴스 (전역 import 용)
# ════════════════════════════════════════════════════════════
settings = Settings()