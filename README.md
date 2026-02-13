Here is the final README.md content — ready to copy-paste directly into your repository.

Judge Agent — Structured Content Evaluation Engine
Overview

This project implements a modular Judge Agent that evaluates text and video content across four dimensions:

AI-generation likelihood

Virality potential (0–100)

Audience distribution analysis

Structured reasoning with confidence scoring

The system uses rubric-driven LLM evaluation with strict schema validation, controlled retry logic, and transcript-first video normalization. It is built with FastAPI and designed to demonstrate structured reasoning, defensive engineering, and clarity under ambiguity.

What Was Built
FastAPI Service

POST /evaluate

Version: 1.0.0

Swagger documentation enabled

Strict request and response schema validation

No raw exception leakage

Modular JudgeAgent

Encapsulates:

Prompt construction (rubric-driven)

LLM invocation

Deterministic JSON parsing

Pydantic validation (extra="forbid")

Retry-once repair strategy

Structured error responses

Business logic is isolated from the API layer.

Transcript-First Video Handling

Video input is normalized via transcript before evaluation.

This decision keeps the evaluation pipeline unified and avoids multimodal overengineering within the 6-hour implementation constraint. The architecture allows clean extension to multimodal analysis later.

Strict Schema Enforcement

Output constraints include:

virality.score → integer between 0 and 100

confidence → float between 0.0 and 1.0

label → "AI" or "Human"

Audience list size bounded

extra="forbid" on all response models

Malformed outputs trigger a controlled retry. Persistent failures return a structured error response — never a crash.

Offline Deterministic Mode

OPENAI_OFFLINE_MODE enables development and testing without external API calls.
This prevents flaky behavior and improves reproducibility.

Minimal High-Signal Tests

Tests cover:

Schema validation

Retry logic

API endpoint behavior

Error handling

All tests passing.

Architecture
Input (Text or Video)
    ↓
Video Normalization (Transcript-first)
    ↓
JudgeAgent
    ↓
LLM Structured Evaluation
    ↓
JSON Validation (Pydantic)
    ↓
Retry if malformed
    ↓
Structured API Response

Design Intent

Clear separation of concerns

Deterministic output contracts

Controlled failure handling

Extensible evaluation core

The API layer contains no evaluation logic.
The JudgeAgent owns orchestration.
Validation is enforced before any response leaves the system.

Evaluation Logic
1. AI vs Human Detection

Heuristic, explainable reasoning — not statistical classification.

AI-indicative signals

Structural symmetry

Over-coherence

Generic phrasing

Polished neutrality

Lack of lived detail

Human-indicative signals

Personal anecdotes

Emotional inconsistency

Idiosyncratic phrasing

Imperfect structure

Cultural specificity

Output includes label, confidence, and reasoning transparency.

2. Virality Scoring (0–100)

Derived from a defined rubric including:

Emotional intensity

Novelty

Relatability

Shareability

Clarity

Controversy potential

The model produces:

Numeric score

Confidence

Explicit reasoning

No historical engagement data is used. Scoring is inference-based.

3. Distribution Analysis

Infers likely audience segments based on:

Topic

Tone

Cultural signals

Optional platform metadata

Each audience segment includes:

community

why (explicit justification)

A summary reasoning field explains the overall distribution logic.

4. Confidence Modeling

Each dimension includes:

confidence: float (0.0–1.0)


Confidence reflects:

Strength of detected signals

Presence of ambiguity

Mixed indicators

It does not represent empirical calibration.

Design Decisions & Tradeoffs
Transcript-First Video Evaluation

Video is evaluated primarily via transcript.

Rationale:

AI detection is largely linguistic.

Virality drivers are primarily semantic.

Full multimodal CV exceeds the 6-hour scope.

The architecture allows multimodal extension without refactoring.

Heuristic AI Detection

No stylometric classifier or dataset-based model was implemented.

Tradeoff:

Higher explainability

No statistical accuracy guarantee

Aligned with the assignment’s focus on reasoning under ambiguity.

LLM-Based Structured Scoring

An LLM generates evaluations under a strict output contract.

Risk: Free-form output drift
Mitigation: JSON-only enforcement + retry repair strategy

Strict JSON Enforcement + Retry Strategy

Pipeline:

Prompt requires JSON-only output

json.loads() parsing

Pydantic schema validation

Retry once with repair prompt if malformed

If still invalid:

Return structured JudgeErrorResponse

No stack traces

No raw HTTP exceptions

This reflects defensive engineering practices.

Offline Deterministic Mode

Prevents:

Flaky tests

API instability during development

Non-deterministic CI behavior

Supports controlled iteration.

Assumptions

AI detection is heuristic and probabilistic.

Virality is inferred from linguistic and emotional features.

Video evaluation relies primarily on transcript semantics.

Audience segmentation is semantic inference, not demographic ground truth.

Confidence scores reflect model certainty, not statistical validation.

Cultural bias may influence interpretation.

Constraints

6-hour scoped implementation

Designed to demonstrate reasoning under ambiguity

Focused on clarity over complexity

Extensible but intentionally minimal

How to Run
git clone <repo-url>
cd judge-agent

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload


Open:

http://127.0.0.1:8000/docs

Example Request
{
  "type": "text",
  "content": "AI is about to replace every job in the next 5 years. No one is ready.",
  "metadata": {
    "platform": "twitter"
  }
}

Example Response (Shape)
{
  "generation_prediction": {
    "label": "AI",
    "confidence": 0.74,
    "reasoning": "..."
  },
  "virality": {
    "score": 81,
    "confidence": 0.69,
    "reasoning": "..."
  },
  "distribution_analysis": {
    "likely_audiences": [
      {
        "community": "Tech Twitter",
        "why": "..."
      }
    ],
    "reasoning": "..."
  },
  "meta_explanation": "..."
}

Future Improvements

Multimodal frame sampling for richer video evaluation

Stylometric AI-detection ensemble

Calibration against labeled dataset

Cost-aware model routing

Response caching for repeated content

Batch evaluation endpoint

Observability dashboard (latency, retries, model drift)

Confidence calibration layer

All improvements integrate cleanly into the current architecture.

Closing

This implementation prioritizes:

Explicit reasoning

Clear contracts

Defensive validation

Controlled scope

Extensibility

It is intentionally structured to demonstrate engineering judgment under ambiguity rather than maximize model complexity.