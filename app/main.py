from fastapi import FastAPI

app = FastAPI(
    title="Judge Agent API",
    description="Evaluates text and video content for AI-generation likelihood, virality, and distribution analysis.",
    version="0.1.0",
)

@app.get("/health")
def health():
    return {"status": "ok"}
