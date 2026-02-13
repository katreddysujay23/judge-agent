# tests/test_judge_retry.py

import json
from app.judge import JudgeAgent
from app.models import JudgeResponse


def test_retry_on_invalid_json(monkeypatch):
    agent = JudgeAgent()

    calls = {"count": 0}

    def mock_call_llm(*args, **kwargs):
        calls["count"] += 1
        if calls["count"] == 1:
            return "INVALID JSON"
        else:
            return json.dumps({
                "generation_prediction": {
                    "label": "Human",
                    "confidence": 0.7,
                    "reasoning": "Personal tone."
                },
                "virality": {
                    "score": 60,
                    "confidence": 0.6,
                    "reasoning": "Relatable."
                },
                "distribution_analysis": {
                    "likely_audiences": [
                        {"community": "Startup founders", "why": "Career topic."}
                    ],
                    "reasoning": "Founder-focused content."
                },
                "meta_explanation": "Retry succeeded."
            })

    monkeypatch.setattr(agent, "_call_llm", mock_call_llm)

    result = agent.evaluate_text("Test content")
    assert isinstance(result, JudgeResponse)
    assert calls["count"] == 2
