# app/config.py
from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    # Application
    app_version: str = os.getenv("APP_VERSION", "1.0.0")

    # OpenAI
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "").strip()
    model_name: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
    temperature: float = float(os.getenv("OPENAI_TEMPERATURE", "0.2"))
    timeout_seconds: float = float(os.getenv("OPENAI_TIMEOUT_SECONDS", "20"))

    # Reliability
    max_retries: int = int(os.getenv("MAX_RETRIES", "1"))  # retry-once policy

    # Dev ergonomics (avoid quota blockers)
    offline_mode: bool = os.getenv("OPENAI_OFFLINE_MODE", "false").strip().lower() == "true"


settings = Settings()


def require_api_key() -> None:
    # Only enforce when we actually intend to call OpenAI
    if not settings.offline_mode and not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not set. Add it to .env or your environment.")
