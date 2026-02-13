import pytest
from pydantic import ValidationError

from app.models import JudgeResponse


def test_judge_response_schema_accepts_valid_payload():
    payload = {
        "generation_prediction": {
            "label": "AI",
            "confidence": 0.72,
            "reasoning": "Highly structured phrasing and generic tone."
        },
        "virality": {
            "score": 68,
            "confidence": 0.61,
            "reasoning": "Relatable topic with clear hook; moderate novelty."
        },
        "distribution_analysis": {
            "likely_audiences": [
                {"community": "Tech Twitter / AI builders", "why": "Topic + jargon aligns."},
                {"community": "Productivity enthusiasts", "why": "Actionable framing invites sharing."},
            ],
            "reasoning": "Audience inferred from topic and tone."
        },
        "meta_explanation": "Heuristic assessment based on linguistic cues and semantic audience inference."
    }

    res = JudgeResponse.model_validate(payload)
    assert res.virality.score == 68


def test_judge_response_rejects_out_of_range_values():
    payload = {
        "generation_prediction": {"label": "AI", "confidence": 1.2, "reasoning": "x"},
        "virality": {"score": 101, "confidence": 0.5, "reasoning": "x"},
        "distribution_analysis": {
            "likely_audiences": [{"community": "c", "why": "w"}],
            "reasoning": "x",
        },
        "meta_explanation": "x",
    }

    with pytest.raises(ValidationError):
        JudgeResponse.model_validate(payload)
