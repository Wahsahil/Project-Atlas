from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import os

app = FastAPI(
    title="Project Atlas",
    description="AI Market Research Report Copilot",
    version="0.1.0"
)

# Temporary development key. Replace with an environment variable later.
API_KEY = os.getenv("ATLAS_API_KEY", "atlas-dev-key-change-me")


class ChatRequest(BaseModel):
    client_id: str
    question: str


class ChatResponse(BaseModel):
    answer: str
    citations: list[str]
    confidence: float
    conflicts: list[str]
    derived_values: list[str]
    escalated: bool


@app.get("/health")
def health():
    return {"status": "ok", "project": "Project Atlas"}


@app.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    x_api_key: str = Header(default="")
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    # Temporary baseline: no LLM or report retrieval yet.
    # Never invent a market figure when the source has not been retrieved.
    return ChatResponse(
        answer=(
            "The report-retrieval and AI reasoning components are not "
            "configured yet. No market figure has been verified. "
            "Please ingest authorized reports before relying on an answer."
        ),
        citations=[],
        confidence=0.0,
        conflicts=[],
        derived_values=[],
        escalated=True
    )


@app.get("/")
def root():
    return {"message": "Project Atlas API is running"}
