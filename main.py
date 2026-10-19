
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
