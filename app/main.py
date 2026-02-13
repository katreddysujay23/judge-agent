from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.models import InputRequest, JudgeResponse


app = FastAPI(
    title="Judge Agent API",
    description="Evaluates text and video content for AI-generation likelihood, virality, and distribution analysis.",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/evaluate", response_model=JudgeResponse)
def evaluate(request: InputRequest) -> JudgeResponse:
    """
    Phase 1 stub endpoint.
    Full JudgeAgent logic will be implemented in Phase 2.
    """
    # Temporary placeholder response to validate contract wiring.
    # This ensures FastAPI + Pydantic integration is correct early.
    return JudgeResponse(
        generation_prediction={
            "label": "AI",
            "confidence": 0.5,
            "reasoning": "Stub response – evaluation logic not yet implemented."
        },
        virality={
            "score": 50,
            "confidence": 0.5,
            "reasoning": "Stub response – evaluation logic not yet implemented."
        },
        distribution_analysis={
            "likely_audiences": [
                {
                    "community": "General social media users",
                    "why": "Placeholder audience for contract validation."
                }
            ],
            "reasoning": "Stub response – evaluation logic not yet implemented."
        },
        meta_explanation="Phase 1 contract validation response."
    )
