# app/judge.py
from __future__ import annotations

import json
import time
import uuid
import logging
from typing import Any, Dict, Optional

from pydantic import ValidationError

from app.config import settings, require_api_key
from app.models import JudgeResponse
from app.prompts import build_system_prompt, build_user_prompt, build_repair_prompt
from app.video import normalize_video

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class JudgeAgent:
    def __init__(self, client=None) -> None:
        """
        Dependency injection:
        - In prod: client=None -> require API key unless offline_mode.
        - In tests: pass dummy client and monkeypatch _call_llm.
        """
        if client is not None:
            self._client = client
            return

        require_api_key()

        # In offline mode, we don't need a client at all.
        if settings.offline_mode:
            self._client = None
        else:
            self._client = self._init_openai_client()

    def _init_openai_client(self):
        from openai import OpenAI
        return OpenAI(api_key=settings.openai_api_key)

    def evaluate_text(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> JudgeResponse:
        request_id = str(uuid.uuid4())
        system_prompt = build_system_prompt()
        user_prompt = build_user_prompt(content, metadata)

        logger.info("judge.evaluate_text start request_id=%s model=%s offline=%s",
                    request_id, settings.model_name, settings.offline_mode)

        raw = self._call_llm(system_prompt, user_prompt, request_id=request_id)
        parsed = self._parse_and_validate(raw, request_id=request_id)
        if parsed is not None:
            return parsed

        # Retry-once policy (schema/JSON failures)
        if settings.max_retries >= 1:
            logger.warning("judge.retry request_id=%s reason=validation_failed", request_id)
            repair_user_prompt = build_repair_prompt(raw)
            raw2 = self._call_llm(system_prompt, repair_user_prompt, request_id=request_id, is_retry=True)
            parsed2 = self._parse_and_validate(raw2, request_id=request_id)
            if parsed2 is not None:
                return parsed2

        raise RuntimeError(f"LLM output invalid after retry (request_id={request_id}).")

    def evaluate_video(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> JudgeResponse:
        norm = normalize_video(content, metadata)
        # Include normalization notes into metadata for traceability (optional, small signal)
        md = dict(metadata or {})
        md["video_normalization_notes"] = norm.notes
        return self.evaluate_text(norm.transcript, md)

    def _call_llm(self, system_prompt: str, user_prompt: str, request_id: str, is_retry: bool = False) -> str:
        # Offline mode: deterministic mock response for local dev / quota blockers
        if settings.offline_mode:
            logger.info("judge.offline_mode request_id=%s retry=%s", request_id, is_retry)
            return json.dumps({
                "generation_prediction": {
                    "label": "Human",
                    "confidence": 0.62,
                    "reasoning": "Contains personal narrative cues and emotionally specific phrasing; less uniformly polished."
                },
                "virality": {
                    "score": 68,
                    "confidence": 0.6,
                    "reasoning": "Relatable theme with moderate emotional intensity; clear and shareable framing."
                },
                "distribution_analysis": {
                    "likely_audiences": [
                        {"community": "LinkedIn professionals", "why": "Career and learning narratives perform well."},
                        {"community": "Startup builders", "why": "Build/ship stories resonate with builders."}
                    ],
                    "reasoning": "Topic aligns with career growth and builder communities; metadata can refine this further."
                },
                "meta_explanation": "Offline development mode: deterministic mock output to validate pipeline and schema."
            })

        start = time.time()
        try:
            resp = self._client.chat.completions.create(
                model=settings.model_name,
                temperature=settings.temperature,
                timeout=settings.timeout_seconds,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            text = resp.choices[0].message.content or ""
            latency_ms = int((time.time() - start) * 1000)
            logger.info(
                "judge.llm_ok request_id=%s retry=%s latency_ms=%s chars=%s",
                request_id, is_retry, latency_ms, len(text)
            )
            return text

        except Exception as e:
            latency_ms = int((time.time() - start) * 1000)
            logger.exception(
                "judge.llm_error request_id=%s retry=%s latency_ms=%s error=%s",
                request_id, is_retry, latency_ms, repr(e)
            )
            # Wrap OpenAI exceptions so API doesn’t leak vendor details
            raise RuntimeError("Upstream LLM call failed.") from e

    def _parse_and_validate(self, raw_text: str, request_id: str) -> Optional[JudgeResponse]:
        candidate = (raw_text or "").strip()
        obj: Any = None

        def try_load(s: str):
            return json.loads(s)

        # 1) direct parse
        try:
            obj = try_load(candidate)
        except Exception:
            # 2) best-effort brace extraction
            start = candidate.find("{")
            end = candidate.rfind("}")
            if start != -1 and end != -1 and end > start:
                sliced = candidate[start:end + 1]
                try:
                    obj = try_load(sliced)
                except Exception as e2:
                    logger.warning("judge.json_parse_failed request_id=%s error=%s", request_id, repr(e2))
                    return None
            else:
                logger.warning("judge.json_missing_braces request_id=%s", request_id)
                return None

        try:
            return JudgeResponse.model_validate(obj)
        except ValidationError as ve:
            logger.warning("judge.schema_validation_failed request_id=%s errors=%s", request_id, ve.errors())
            return None
