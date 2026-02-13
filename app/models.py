from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict



# Request Contract


class InputMetadata(BaseModel):
    """
    Metadata is intentionally flexible, but we keep a few common keys documented.
    We avoid over-validating here to preserve extensibility (platforms, duration, etc.).
    """
    model_config = ConfigDict(extra="allow")

    platform: Optional[str] = None
    duration_seconds: Optional[int] = Field(default=None, ge=0)
    transcript_provided: Optional[bool] = None


class InputRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["text", "video"]
    content: str = Field(min_length=1)
    metadata: InputMetadata = Field(default_factory=InputMetadata)


# Response Contract

class GenerationPrediction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    label: Literal["AI", "Human"]
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str = Field(min_length=1)


class Virality(BaseModel):
    model_config = ConfigDict(extra="forbid")

    score: int = Field(ge=0, le=100)
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str = Field(min_length=1)


class AudienceSegment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    community: str = Field(min_length=1)
    why: str = Field(min_length=1)


class DistributionAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    likely_audiences: List[AudienceSegment] = Field(
        default_factory=list,
        min_length=1,
        max_length=6,
        description="Short list of likely audience communities (keep it tight).",
    )
    reasoning: str = Field(min_length=1)


class JudgeResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    generation_prediction: GenerationPrediction
    virality: Virality
    distribution_analysis: DistributionAnalysis
    meta_explanation: str = Field(min_length=1)


# Optional but very “production”: a structured error response.
class JudgeErrorResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    error: str
    detail: Optional[str] = None
    request_id: Optional[str] = None
