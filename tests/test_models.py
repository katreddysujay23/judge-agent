# tests/test_models.py

import pytest
from pydantic import ValidationError
from app.models import JudgeResponse


def test_valid_judge_response():
    valid_payload = {
        "generation_prediction": {
            "label": "AI",
            "confidence": 0.8,
            "reasoning": "Highly structured phrasing."
        },
        "virality": {
            "score": 55,
            "confidence": 0.6,
            "reasoning": "Moderately engaging."
        },
        "distribution_analysis": {
            "likely_audiences": [
                {"community": "Tech Twitter", "why": "Topic relevance."}
            ],
            "reasoning": "Tech-oriented content."
        },
        "meta_explanation": "Structured evaluation completed."
    }

    result = JudgeResponse.model_validate(valid_payload)
    assert result.generation_prediction.label in ["AI", "Human"]


def test_extra_fields_forbidden():
    invalid_payload = {
        "generation_prediction": {
            "label": "AI",
            "confidence": 0.8,
            "reasoning": "Structured phrasing.",
            "extra_field": "not allowed"
        },
        "virality": {
            "score": 50,
            "confidence": 0.5,
            "reasoning": "Test"
        },
        "distribution_analysis": {
            "likely_audiences": [
                {"community": "Tech", "why": "Relevant"}
            ],
            "reasoning": "Test"
        },
        "meta_explanation": "Test"
    }

    with pytest.raises(ValidationError):
        JudgeResponse.model_validate(invalid_payload)
