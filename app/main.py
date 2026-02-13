# app/main.py
from fastapi import FastAPI
import logging
import uuid

from app.models import InputRequest, JudgeResponse, JudgeErrorResponse
from app.judge import JudgeAgent
from app.config import settings

# ---------------------------------------------------------
# Logging setup
# ---------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------
app = FastAPI(
    title="Judge Agent API",
    description="Evaluates text and video content for AI-generation likelihood, virality, and distribution analysis.",
    version=settings.app_version,
)

# ---------------------------------------------------------
# Instantiate JudgeAgent once at startup
# ---------------------------------------------------------
try:
    judge_agent = JudgeAgent()
except Exception as e:
    logger.exception("Failed to initialize JudgeAgent: %s", str(e))
    judge_agent = None

# ---------------------------------------------------------
# Health Endpoint
# ---------------------------------------------------------
@app.get("/health", summary="Health check endpoint")
def health() -> dict:
    return {"status": "ok"}


# ---------------------------------------------------------
# Evaluate Endpoint
# ---------------------------------------------------------
@app.post(
    "/evaluate",
    response_model=JudgeResponse,
    responses={
        400: {"model": JudgeErrorResponse},
        500: {"model": JudgeErrorResponse},
    },
    summary="Evaluate content for AI-generation, virality, and distribution analysis",
)
def evaluate(request: InputRequest):
    """
    Evaluates text or video content using the JudgeAgent.

    - Strict schema validation
    - Defensive LLM handling
    - Retry-once policy
    - Controlled failure surface
    """

    request_id = str(uuid.uuid4())

    if judge_agent is None:
        return JudgeErrorResponse(
            error="initialization_failed",
            detail="JudgeAgent failed to initialize.",
            request_id=request_id,
        )

    try:
        metadata_dict = request.metadata.model_dump() if request.metadata else None

        if request.type == "text":
            return judge_agent.evaluate_text(
                content=request.content,
                metadata=metadata_dict,
            )

        if request.type == "video":
            return judge_agent.evaluate_video(
                content=request.content,
                metadata=metadata_dict,
            )

        return JudgeErrorResponse(
            error="invalid_type",
            detail="Invalid type. Must be 'text' or 'video'.",
            request_id=request_id,
        )

    except RuntimeError:
        return JudgeErrorResponse(
            error="evaluation_failed",
            detail="LLM output invalid after retry or upstream call failed.",
            request_id=request_id,
        )

    except Exception as e:
        logger.exception("Unexpected server error: %s", str(e))
        return JudgeErrorResponse(
            error="unexpected_error",
            detail="Unexpected server error.",
            request_id=request_id,
        )
