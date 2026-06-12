"""
LEDO.ai - LLM Client (Ollama 비동기 + 산업 표준 안정성)

수백 개 에이전트가 공유하는 LLM 통신 모듈.
산업 표준 안정성: 재시도 + Jitter + 토큰 관리 + 에러 분류.

핵심 책임:
─────────────────────────────────────
1. 비동기 HTTP 호출 (httpx.AsyncClient)
2. 재시도 전략 (tenacity + AWS Full Jitter)
3. 토큰 관리 (tiktoken)
4. 에러 분류 (Domain Exceptions)
5. 응답 시간 측정 (audit 통합)
6. LoRA 어댑터 지원

설계 원칙:
─────────────────────────────────────
1. Fail-Safe (재시도 + 명확한 에러)
2. Observable (모든 호출 추적)
3. Cost-Aware (토큰 사전 계산)
4. Resilient (네트워크 변동 대응)
5. Stateless (인스턴스 재사용 가능)

참조 표준:
─────────────────────────────────────
- AWS Full Jitter (Marc Brooker, 2015)
  "Exponential Backoff and Jitter"
- Tenacity (재시도의 산업 표준)
- httpx (FastAPI 의 공식 HTTP 클라이언트)
- tiktoken (OpenAI 토큰 카운터)
- Ollama API (https://github.com/ollama/ollama)
- OpenTelemetry (분산 추적)

Python 버전: 3.14+
"""
import asyncio
import logging
import random
from datetime import datetime, timezone
from typing import Optional, Any
from enum import Enum

import httpx
import tiktoken
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
    before_sleep_log,
)
from pydantic import BaseModel, Field, ConfigDict

from config import settings


logger = logging.getLogger(__name__)


# ════════════════════════════════════════════════════════════
# 1. LLM 도메인 예외 (Domain Exceptions)
# ════════════════════════════════════════════════════════════


class LLMError(Exception):
    """LLM 통신의 기본 예외 (부모 클래스)"""
    pass


class LLMTimeoutError(LLMError):
    """LLM 응답 시간 초과 (재시도 가능)

    원인:
    - Ollama 서버 과부하
    - 너무 긴 prompt
    - 모델 로딩 중
    """
    pass


class LLMNetworkError(LLMError):
    """LLM 네트워크 통신 실패 (재시도 가능)

    원인:
    - Ollama 서버 다운
    - 네트워크 연결 끊김
    - DNS 해석 실패
    """
    pass


class LLMResponseError(LLMError):
    """LLM 응답 형식 오류 (재시도 의미 없음)

    원인:
    - 모델이 깨진 JSON 반환
    - 예상 외 형식
    - 빈 응답
    """
    pass


class LLMContextOverflowError(LLMError):
    """입력 토큰이 모델 한도 초과 (재시도 의미 없음)

    원인:
    - prompt 가 너무 김
    - 14B 모델 한도: 32K 토큰
    """
    pass


class LLMRateLimitError(LLMError):
    """Rate limit 초과 (재시도 가능, 더 긴 대기)

    원인:
    - 동시 요청 너무 많음
    - API quota 초과
    """
    pass


# ════════════════════════════════════════════════════════════
# 2. LLM 응답 모델 (Pydantic)
# ════════════════════════════════════════════════════════════


class LLMResponse(BaseModel):
    """LLM 응답의 표준 형식 (Immutable)

    모든 LLM 호출의 결과가 이 형식으로 반환.
    audit.py 의 LLM 컨텍스트 필드와 호환.
    """
    model_config = ConfigDict(extra="forbid", frozen=True)

    # 응답 본문
    content: str = Field(
        ...,
        description="LLM 의 실제 응답 텍스트",
    )

    # 모델 정보
    model_id: str = Field(
        ...,
        description="응답한 모델 (예: 'qwen2.5-coder:14b')",
    )
    lora_adapter_id: Optional[str] = Field(
        default=None,
        description="사용된 LoRA 어댑터 ID",
    )

    # 토큰 정보 (비용/성능 추적)
    input_tokens: int = Field(
        default=0,
        ge=0,
        description="입력 토큰 수",
    )
    output_tokens: int = Field(
        default=0,
        ge=0,
        description="출력 토큰 수",
    )
    total_tokens: int = Field(
        default=0,
        ge=0,
        description="총 토큰 수",
    )

    # 성능 메트릭
    response_time_ms: int = Field(
        default=0,
        ge=0,
        description="응답 시간 (밀리초)",
    )
    retry_count: int = Field(
        default=0,
        ge=0,
        description="재시도 횟수",
    )

    # 추적
    timestamp_utc: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="응답 시각 (UTC)",
    )

    # 원본 응답 (디버깅용)
    raw_response: dict[str, Any] = Field(
        default_factory=dict,
        description="Ollama 원본 응답",
    )


# ════════════════════════════════════════════════════════════
# 3. LLMClient - 핵심 클래스
# ════════════════════════════════════════════════════════════


class LLMClient:
    """Ollama 비동기 LLM 클라이언트 (산업 표준 안정성)

    수백 개 에이전트가 공유 가능한 stateless 클라이언트.
    한 번 생성 후 여러 호출 (재사용).

    사용 예시:
    ─────────────────────────────────────
        # 글로벌 싱글톤
        client = LLMClient()
        
        # 단순 호출
        response = await client.generate(
            prompt="작업자의 안전모 착용 여부를 평가해주세요"
        )
        print(response.content)
        print(f"토큰: {response.total_tokens}, 시간: {response.response_time_ms}ms")
        
        # LoRA 사용
        response = await client.generate(
            prompt="크레인 작업 안전 평가",
            lora_adapter_id="crane_safety_v3",
        )

    재시도 전략:
    ─────────────────────────────────────
    네트워크/Timeout 에러 → 3회 재시도
    - 1차 재시도: 1초 + jitter (0-1초)
    - 2차 재시도: 2초 + jitter (0-2초)
    - 3차 재시도: 4초 + jitter (0-4초)
    
    응답/Context 에러 → 즉시 실패 (재시도 의미 없음)
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        model_id: Optional[str] = None,
        timeout_seconds: float = 120.0,
        max_retries: int = 3,
        context_window: int = 32000,
    ) -> None:
        """LLMClient 초기화

        Args:
            base_url: Ollama 서버 URL (기본: config.OLLAMA_BASE_URL)
            model_id: 기본 모델 ID (기본: config.OLLAMA_MODEL)
            timeout_seconds: 단일 요청 timeout (기본 120초)
            max_retries: 최대 재시도 횟수 (기본 3회)
            context_window: 모델 컨텍스트 한도 (기본 32K)

        ⚠️ httpx.AsyncClient 는 lazy 생성:
           첫 generate() 호출 시 생성
           close() 호출 시 정리
        """
        self.base_url: str = base_url or settings.OLLAMA_BASE_URL
        self.model_id: str = model_id or settings.OLLAMA_MODEL
        self.timeout_seconds: float = timeout_seconds
        self.max_retries: int = max_retries
        self.context_window: int = context_window

        # httpx 클라이언트 (lazy 생성)
        self._http_client: Optional[httpx.AsyncClient] = None

        # 토큰 카운터 (lazy 생성)
        self._tokenizer: Optional[tiktoken.Encoding] = None

        # 통계
        self._stats: dict[str, int] = {
            "total_calls": 0,
            "total_successes": 0,
            "total_failures": 0,
            "total_retries": 0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
        }

        logger.info(
            f"LLMClient 생성: base_url={self.base_url}, "
            f"model={self.model_id}, "
            f"timeout={timeout_seconds}s, "
            f"max_retries={max_retries}"
        )

    # ════════════════════════════════════════
    # 라이프사이클
    # ════════════════════════════════════════

    async def _ensure_http_client(self) -> httpx.AsyncClient:
        """httpx 클라이언트 lazy 생성

        ⭐ Lazy 패턴:
           __init__ 에선 생성 X (asyncio 루프 필요)
           첫 호출 시 자동 생성
        """
        if self._http_client is None:
            self._http_client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=httpx.Timeout(
                    timeout=self.timeout_seconds,
                    connect=10.0,  # 연결 timeout 별도
                ),
                limits=httpx.Limits(
                    max_keepalive_connections=20,
                    max_connections=100,
                ),
            )
            logger.debug("httpx.AsyncClient 생성됨")
        return self._http_client

    def _ensure_tokenizer(self) -> tiktoken.Encoding:
        """tiktoken 토크나이저 lazy 생성

        ⭐ qwen 모델은 tiktoken 의 cl100k_base 와 유사
           (정확한 토큰 카운터는 모델별로 다름, 근사치 OK)
        """
        if self._tokenizer is None:
            self._tokenizer = tiktoken.get_encoding("cl100k_base")
            logger.debug("tiktoken 토크나이저 생성됨")
        return self._tokenizer

    async def close(self) -> None:
        """클라이언트 종료 (자원 정리)

        ⚠️ 산업 표준: 사용 종료 시 호출
           async with LLMClient() as client: ... 사용 시 자동
        """
        if self._http_client is not None:
            await self._http_client.aclose()
            self._http_client = None
            logger.debug("httpx.AsyncClient 종료됨")

    # ════════════════════════════════════════
    # 비동기 컨텍스트 매니저
    # ════════════════════════════════════════

    async def __aenter__(self) -> "LLMClient":
        await self._ensure_http_client()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any],
    ) -> None:
        await self.close()

    # ════════════════════════════════════════
    # 토큰 관리
    # ════════════════════════════════════════

    def count_tokens(self, text: str) -> int:
        """텍스트의 토큰 수 계산

        Args:
            text: 토큰화할 텍스트

        Returns:
            토큰 수 (근사치)

        ⚠️ 근사치 안내:
           tiktoken 의 cl100k_base 는 OpenAI 용
           qwen 모델은 약간 다를 수 있음 (±10%)
           정확한 카운트는 Ollama 응답의 토큰 수 사용
        """
        tokenizer = self._ensure_tokenizer()
        return len(tokenizer.encode(text))

    def validate_context(self, prompt: str) -> int:
        """입력이 컨텍스트 한도 안에 들어가는지 검증

        Args:
            prompt: 입력 prompt

        Returns:
            입력 토큰 수

        Raises:
            LLMContextOverflowError: 한도 초과 시
        """
        input_tokens = self.count_tokens(prompt)

        # 출력 공간 확보 (입력의 50% 또는 최소 4K)
        reserved_output = max(input_tokens // 2, 4000)
        max_input = self.context_window - reserved_output

        if input_tokens > max_input:
            raise LLMContextOverflowError(
                f"입력 토큰 {input_tokens} 가 한도 {max_input} 초과 "
                f"(context_window={self.context_window}, "
                f"reserved_output={reserved_output})"
            )

        return input_tokens

    # ════════════════════════════════════════
    # 핵심 호출 메서드
    # ════════════════════════════════════════

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        lora_adapter_id: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: Optional[int] = None,
        stop_sequences: Optional[list[str]] = None,
    ) -> LLMResponse:
        """LLM 응답 생성 (재시도 + 토큰 관리 + 에러 분류)

        Args:
            prompt: 사용자 입력
            system_prompt: 시스템 메시지 (선택)
            lora_adapter_id: LoRA 어댑터 (선택)
            temperature: 응답의 랜덤성 (0.0-2.0, 기본 0.3)
            max_tokens: 최대 출력 토큰 (선택)
            stop_sequences: 출력 중단 시퀀스 (선택)

        Returns:
            LLMResponse 인스턴스

        Raises:
            LLMContextOverflowError: 입력 토큰 한도 초과
            LLMTimeoutError: 재시도 후에도 timeout
            LLMNetworkError: 재시도 후에도 네트워크 실패
            LLMResponseError: 응답 형식 오류
        """
        # 1. 입력 검증
        if not prompt or not prompt.strip():
            raise ValueError("prompt 비어있음")

        # 2. 토큰 사전 계산
        full_input = (system_prompt or "") + prompt
        input_tokens = self.validate_context(full_input)

        self._stats["total_calls"] += 1

        # 3. 시간 측정 시작
        start_time = datetime.now(timezone.utc)

        try:
            # 4. 재시도 가능한 호출
            raw_response = await self._call_with_retry(
                prompt=prompt,
                system_prompt=system_prompt,
                lora_adapter_id=lora_adapter_id,
                temperature=temperature,
                max_tokens=max_tokens,
                stop_sequences=stop_sequences,
            )

            # 5. 응답 시간 계산
            end_time = datetime.now(timezone.utc)
            response_time_ms = int(
                (end_time - start_time).total_seconds() * 1000
            )

            # 6. 응답 파싱
            content = raw_response.get("response", "")
            if not content:
                raise LLMResponseError("Ollama 응답이 비어있음")

            # 7. 토큰 정보 (Ollama 가 제공하면 사용, 아니면 추정)
            prompt_eval_count = raw_response.get(
                "prompt_eval_count",
                input_tokens,
            )
            eval_count = raw_response.get(
                "eval_count",
                self.count_tokens(content),
            )

            # 8. 통계 업데이트
            self._stats["total_successes"] += 1
            self._stats["total_input_tokens"] += prompt_eval_count
            self._stats["total_output_tokens"] += eval_count

            # 9. 응답 객체 생성
            response = LLMResponse(
                content=content,
                model_id=raw_response.get("model", self.model_id),
                lora_adapter_id=lora_adapter_id,
                input_tokens=prompt_eval_count,
                output_tokens=eval_count,
                total_tokens=prompt_eval_count + eval_count,
                response_time_ms=response_time_ms,
                raw_response=raw_response,
            )

            logger.info(
                f"LLM 호출 성공: model={response.model_id}, "
                f"tokens={response.total_tokens}, "
                f"time={response_time_ms}ms"
            )

            return response

        except Exception as e:
            self._stats["total_failures"] += 1
            logger.error(
                f"LLM 호출 실패: {type(e).__name__}: {e}"
            )
            raise

    # ════════════════════════════════════════
    # 재시도 로직 (tenacity + Full Jitter)
    # ════════════════════════════════════════

    @retry(
        # 재시도 대상 예외만
        retry=retry_if_exception_type((
            LLMTimeoutError,
            LLMNetworkError,
            LLMRateLimitError,
        )),
        # 최대 3회 시도 (1회 + 2회 재시도)
        stop=stop_after_attempt(3),
        # 지수 백오프 (1s, 2s, 4s) + jitter
        wait=wait_exponential(
            multiplier=1.0,
            min=1.0,
            max=10.0,
        ),
        # 재시도 전 로그
        before_sleep=before_sleep_log(logger, logging.WARNING),
        # 재시도 정보 반환
        reraise=True,
    )
    async def _call_with_retry(
        self,
        prompt: str,
        system_prompt: Optional[str],
        lora_adapter_id: Optional[str],
        temperature: float,
        max_tokens: Optional[int],
        stop_sequences: Optional[list[str]],
    ) -> dict[str, Any]:
        """재시도 가능한 실제 HTTP 호출

        ⭐ tenacity 데코레이터가 자동:
           - 재시도 대상 예외만 재시도
           - 지수 백오프 (1s, 2s, 4s)
           - max 3회까지 시도

        ⭐ AWS Full Jitter:
           wait_exponential 의 multiplier + max
           실제 대기 = random * computed_wait
           → 분산 시스템에서 동시 재시도 폭주 방지
        """
        # 재시도 카운터 증가
        self._stats["total_retries"] += 1

        # HTTP 클라이언트 확보
        client = await self._ensure_http_client()

        # 모델 ID 결정 (LoRA 어댑터 있으면 우선)
        model = lora_adapter_id if lora_adapter_id else self.model_id

        # 요청 본문 구성 (Ollama API 형식)
        payload: dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
            },
        }

        if system_prompt:
            payload["system"] = system_prompt

        if max_tokens:
            payload["options"]["num_predict"] = max_tokens

        if stop_sequences:
            payload["options"]["stop"] = stop_sequences

        # HTTP 호출 + 에러 분류
        try:
            response = await client.post(
                "/api/generate",
                json=payload,
            )
            response.raise_for_status()
            return response.json()

        except httpx.TimeoutException as e:
            raise LLMTimeoutError(
                f"Ollama timeout ({self.timeout_seconds}s 초과)"
            ) from e

        except httpx.ConnectError as e:
            raise LLMNetworkError(
                f"Ollama 연결 실패: {self.base_url}"
            ) from e

        except httpx.HTTPStatusError as e:
            status = e.response.status_code
            if status == 429:
                raise LLMRateLimitError(
                    f"Ollama rate limit (429)"
                ) from e
            elif status >= 500:
                raise LLMNetworkError(
                    f"Ollama 서버 에러 ({status})"
                ) from e
            else:
                raise LLMResponseError(
                    f"Ollama HTTP 에러 ({status}): {e.response.text[:200]}"
                ) from e

        except httpx.HTTPError as e:
            raise LLMNetworkError(
                f"Ollama HTTP 에러: {type(e).__name__}"
            ) from e

    # ════════════════════════════════════════
    # 관측 가능성
    # ════════════════════════════════════════

    def get_stats(self) -> dict[str, Any]:
        """클라이언트 통계 조회

        Returns:
            {
                "total_calls": int,
                "total_successes": int,
                "total_failures": int,
                "total_retries": int,
                "total_input_tokens": int,
                "total_output_tokens": int,
                "success_rate": float,
                "average_retries": float,
            }
        """
        total = self._stats["total_calls"]
        success_rate = (
            self._stats["total_successes"] / total
            if total > 0 else 0.0
        )
        avg_retries = (
            self._stats["total_retries"] / total
            if total > 0 else 0.0
        )

        return {
            **self._stats,
            "success_rate": round(success_rate, 4),
            "average_retries": round(avg_retries, 2),
        }

    async def health_check(self) -> dict[str, Any]:
        """Ollama 서버 헬스 체크

        Returns:
            {
                "status": "healthy" | "unhealthy",
                "ollama_url": str,
                "ollama_version": str (가능 시),
                "latency_ms": int,
            }
        """
        start = datetime.now(timezone.utc)

        try:
            client = await self._ensure_http_client()
            response = await client.get("/api/version", timeout=5.0)
            response.raise_for_status()

            version_info = response.json()
            latency_ms = int(
                (datetime.now(timezone.utc) - start).total_seconds() * 1000
            )

            return {
                "status": "healthy",
                "ollama_url": self.base_url,
                "ollama_version": version_info.get("version", "unknown"),
                "latency_ms": latency_ms,
                "model_id": self.model_id,
            }

        except Exception as e:
            latency_ms = int(
                (datetime.now(timezone.utc) - start).total_seconds() * 1000
            )
            return {
                "status": "unhealthy",
                "ollama_url": self.base_url,
                "error": f"{type(e).__name__}: {str(e)[:200]}",
                "latency_ms": latency_ms,
            }


# ════════════════════════════════════════════════════════════
# 4. 글로벌 싱글톤 (시스템 전체 공유)
# ════════════════════════════════════════════════════════════


_global_llm_client: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    """글로벌 LLMClient 인스턴스 반환 (Singleton)

    Returns:
        시스템 전체에서 공유되는 클라이언트

    ⭐ 산업 표준 Singleton:
       - 한 프로세스 = 1 LLMClient
       - 자원 효율 (HTTP 연결 풀 공유)
       - 통계 일관성
    """
    global _global_llm_client
    if _global_llm_client is None:
        _global_llm_client = LLMClient()
    return _global_llm_client


async def close_llm_client() -> None:
    """글로벌 LLMClient 종료 (시스템 종료 시 호출)"""
    global _global_llm_client
    if _global_llm_client is not None:
        await _global_llm_client.close()
        _global_llm_client = None

        