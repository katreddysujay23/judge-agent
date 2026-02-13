Judge Agent — Structured Content Evaluation
Overview

This project implements a modular Judge Agent that evaluates text and video content across four dimensions:

AI-generated vs Human-generated prediction

Virality score (0–100)

Distribution analysis (audiences + justification)

Structured reasoning with confidence

The objective was to demonstrate structured reasoning, disciplined system design, and defensive engineering within a 6-hour constraint — not to maximize detection accuracy.

Architecture
Input (Text / Video)
        ↓
Transcript Normalization (video)
        ↓
JudgeAgent
        ↓
LLM Structured Evaluation
        ↓
JSON Validation (Pydantic)
        ↓
Retry-once (if malformed)
        ↓
Structured API Response


Design Principles

Clear separation of concerns

Strict output contracts (extra="forbid")

Bounded numeric validation

Controlled failure handling

Extensible but minimal

Evaluation Approach
AI vs Human (Heuristic)

Signals considered:

Structural symmetry vs narrative messiness

Over-coherence vs lived detail

Generic phrasing vs idiosyncratic voice

Emotional neutrality vs inconsistency

Output includes label, reasoning, and bounded confidence (0.0–1.0).

Virality (0–100)

Derived from rubric dimensions:

Emotional intensity

Novelty

Relatability

Shareability

Clarity

Controversy potential

Produces: score + confidence + explanation.

No engagement data is used — inference is semantic.

Distribution Analysis

Infers likely communities based on topic, tone, and metadata.
Each audience segment includes explicit justification.

Reliability & Defensive Engineering

JSON-only prompt enforcement

Deterministic parsing

Pydantic schema validation

Retry-once repair strategy

Structured error responses (no stack trace leakage)

Offline deterministic mode for dev/test stability

Health endpoint for production readiness

Key Tradeoffs

Transcript-first video evaluation
Chosen to respect the 6-hour scope while preserving semantic signal.
Architecture allows multimodal extension later.

Heuristic AI detection
Explainable but not statistically calibrated.
Aligned with ambiguity-focused evaluation.

Assumptions

AI detection is probabilistic.

Virality is inferred linguistically, not empirically.

Transcript-level analysis is sufficient for initial video evaluation.

Confidence reflects model certainty, not calibration.

How to Run
git clone <repo-url>
cd judge-agent

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --reload


Open: http://127.0.0.1:8000/docs

Future Extensions (With More Time)

Multimodal frame sampling

Stylometric ensemble detection

Calibration against labeled data

Cost-aware inference routing

Observability dashboards (latency, retries, drift)

Batch evaluation endpoints

Closing

This implementation prioritizes clarity, contract discipline, controlled scope, and reasoning transparency under ambiguity.