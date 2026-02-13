# app/video.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class NormalizedVideo:
    transcript: str
    notes: str  # brief explanation of what we did (for debugging/observability)


def normalize_video(content: str, metadata: Optional[Dict[str, Any]] = None) -> NormalizedVideo:
    """
    Transcript-first normalization.

    Current scope assumption:
    - For Stage 1, "video" content is provided as a transcript string in `content`.
    - Future: accept URLs, file paths, or structured {transcript, captions, ocr} payloads.

    We keep this logic deliberately small to match the 6-hour constraint.
    """
    transcript = (content or "").strip()

    # Defensive normalization
    if not transcript:
        return NormalizedVideo(
            transcript="",
            notes="Empty video content provided; expected transcript string in request.content."
        )
    
    # You can add lightweight cleanup here if needed (e.g., trim repeated whitespace).
    return NormalizedVideo(
        transcript=transcript,
        notes="Transcript-first normalization: treated request.content as transcript."
    )
