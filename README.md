# Project Atlas — Market Research Report Copilot

An AI-assisted market research copilot designed to retrieve authorized report excerpts, compare market metrics, calculate CAGR-based projections, and flag questions that require human review.

## Features

- **FastAPI backend** with `/chat` and `/health` endpoints.
- **Report retrieval** from Markdown files using keyword matching.
- **Client-based report access rules** for the provided sample clients.
- **Market metric comparison** to identify differing reported values.
- **CAGR calculator** for compound-growth projections.
- **Prompt-injection safeguards** for selected unsafe requests.
- **Confidence scores and escalation flags** when evidence is insufficient.
- **Automated tests** for core API, retrieval, access-control, and calculator behavior.

## Tech Stack

- Python
- FastAPI
- Pydantic
- Pytest
- Markdown-based report data

## Project Structure

```text
Project Atlas/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── knowledge.py
│   └── calculator.py
├── data/
│   └── reports/
├── test_project_atlas.py
├── test_calculator.py
├── requirements.txt
├── EVALUATION.md
└── README.md
```

## Prerequisites

- Python 3.10 or later
- pip
- Git

## Setup

Clone the repository:

```bash
git clone https://github.com/Wahsahil/Project-Atlas.git
cd Project-Atlas
```

Create and activate a virtual environment on Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Run the API

From the project root, run:

```powershell
python -m uvicorn app.main:app --reload
```

The API should be available at:

- Health check: http://127.0.0.1:8000/health
- Interactive API documentation: http://127.0.0.1:8000/docs

## API Usage

### Health Check

```http
GET /health
```

Expected response:

```json
{
  "status": "healthy",
  "service": "Project Atlas API"
}
```

### Chat

```http
POST /chat
Content-Type: application/json
```

Example request:

```json
{
  "client_id": "C-01",
  "question": "What is the CAGR reported for the smart water meter market?"
}
```

The response includes an answer, report citations, a confidence score, conflicts, derived values, and an escalation flag.

Example using PowerShell:

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/chat" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"client_id":"C-01","question":"What is the CAGR reported for the smart water meter market?"}'
```

## Run Tests

From the project root:

```powershell
python -m pytest -q
```

The current test suite has passed **9 tests** in the development environment.

## Current Limitations

This is a prototype, and the following assignment requirements are not yet fully implemented:

- Retrieval uses keyword matching rather than embeddings and a vector database.
- There is no external LLM integration or complete LangGraph agent workflow.
- Escalations are returned by the API but are not persisted in MySQL.
- Client IDs are supplied in the request; production-grade identity verification and authentication are not implemented.
- PDF and HTML ingestion, the full report