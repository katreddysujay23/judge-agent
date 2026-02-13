# app/prompts.py
from __future__ import annotations
import json
from typing import Any, Dict

OUTPUT_SCHEMA_REMINDER = """
Return ONLY valid JSON.
Do not include markdown.
Do not include explanations outside the JSON object.
All fields must match the required schema exactly.

Rules:
- generation_prediction.label: "AI" or "Human"
- all confidence fields: 0.0 to 1.0
- virality.score: integer 0 to 100
- distribution_analysis.likely_audiences: 1 to 6 items
"""

def build_system_prompt() -> str:
    return f"""
You are a Judge Agent that evaluates content across:
1) AI vs Human generation prediction (heuristic, probabilistic)
2) Virality score (0-100)
3) Distribution analysis (likely audiences + why)
4) Clear, structured explanations

Heuristic signals:
- AI indicators: overly polished neutrality, symmetry, generic phrasing, over-coherence, lack of lived detail
- Human indicators: personal anecdotes, idiosyncratic phrasing, emotional inconsistency, cultural specificity, imperfect structure

Virality rubric dimensions:
- emotional intensity, novelty, relatability, shareability, clarity, controversy potential

You must be uncertainty-aware:
- confidence reflects your certainty given available evidence, not empirical calibration

{OUTPUT_SCHEMA_REMINDER}
""".strip()

def build_user_prompt(content: str, metadata: Dict[str, Any] | None) -> str:
    md = metadata or {}
    metadata_json = json.dumps(md, ensure_ascii=False)
    return f"""
CONTENT:
{content}

METADATA (json):
{metadata_json}

{OUTPUT_SCHEMA_REMINDER}
""".strip()

def build_repair_prompt(bad_output: str) -> str:
    return f"""
The previous output was invalid (not valid JSON and/or did not match the schema).
Fix it and return ONLY valid JSON that matches the schema exactly.

INVALID OUTPUT:
{bad_output}

Remember: output ONLY JSON.
""".strip()
