
from fastapi import FastAPI
from knowledge import retrieve_reports

app = FastAPI(
    title="Project Atlas",
    description="AI-powered market research report copilot",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "Project Atlas API is running"}


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "Project Atlas API",
    }

from pydantic import BaseModel

class ChatRequest(BaseModel):
    client_id: str
    question: str


@app.post("/chat")
def chat(request: ChatRequest):
    reports = retrieve_reports(
        client_id=request.client_id,
        question=request.question
    )

    if not reports:
        return {
            "answer": "No authorized report information was found. Please check the client ID or escalate this question.",
            "citations": [],
            "confidence": 0.0,
            "conflicts": [],
            "derived_values": [],
            "escalated": True
        }

    return {
        "answer": "Relevant authorized report excerpts were retrieved. Full AI answer generation is not configured yet.",
        "citations": [
            {
                "report_id": item["report_id"],
                "text": item["text"]
            }
            for item in reports
        ],
        "confidence": 0.5,
        "conflicts": [],
        "derived_values": [],
        "escalated": False
    }
