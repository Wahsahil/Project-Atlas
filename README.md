::: {align="center"}
# 🌊 Project Atlas

### Market Research Report Copilot --- Prototype

**Find evidence. Compare market figures. Escalate uncertainty.**

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)
![Tests](https://img.shields.io/badge/Automated%20tests-12%20passing-2ea44f)
![Status](https://img.shields.io/badge/Project-Prototype-orange)

*A small, evidence-oriented API prototype exploring how market-research
reports can be searched and compared with access controls and escalation
for uncertain answers.*
:::

------------------------------------------------------------------------

## 🖼️ At a glance

  ----------------------------------- -----------------------------------
  **Project type**                    AI / Generative AI application
                                      prototype

  **Primary interface**               FastAPI REST API with interactive
                                      Swagger docs

  **Report format**                   Markdown sample reports

  **Key behaviors**                   Entitlement-aware retrieval, CAGR
                                      calculations, conflict detection,
                                      escalation

  **Automated tests**                 12 passing in the latest reported
                                      run

  **Current storage**                 Local report files and JSON-backed
                                      escalation tickets

  **Status**                          Prototype; not production-ready
  ----------------------------------- -----------------------------------

> **Scope note:** This README describes the implementation currently
> tested in this repository. It does not claim that vector-database
> retrieval, a complete agent framework, MySQL persistence, or
> CodeIgniter 3 integration is finished.

## ✨ What is Project Atlas?

Project Atlas is a Python API prototype for a market-research report
copilot. It accepts a client's question, searches available report
excerpts, and returns a structured response containing an answer,
citations, confidence, conflict information, calculated values, and
escalation status.

The prototype is designed around three principles:

-   **Evidence before assertions:** cite report excerpts when relevant
    evidence is found.
-   **Access control matters:** only return evidence from reports the
    client is permitted to access.
-   **Fail safely:** refuse requests for private client information and
    escalate questions the prototype cannot answer reliably.

## 🗺️ Request flow

``` mermaid
flowchart TD
    A[Client question] --> B[FastAPI /chat]
    B --> C{Safety and client checks}
    C -->|Unsafe request| D[Refuse request]
    C -->|Allowed| E[Entitlement-aware report retrieval]
    E --> F[Compare evidence and detect conflicts]
    F --> G[Calculate CAGR projection when supported]
    G --> H{Reliable evidence available?}
    H -->|Yes| I[Structured answer with citations]
    H -->|No| J[Create escalation ticket]
    I --> K[JSON response]
    D --> K
    J --> K
```

*This diagram represents the current prototype behavior at a high level;
it is not a claim that every step uses a dedicated agent or an LLM.*

## 🧩 Features and implementation status

  -----------------------------------------------------------------------
  Capability              Current status          Notes
  ----------------------- ----------------------- -----------------------
  FastAPI application     ✅ Implemented          API includes chat and
                                                  health functionality,
                                                  plus escalation listing

  Interactive API         ✅ Available            Open Swagger UI at
  documentation                                   `/docs` while the local
                                                  server is running

  Markdown sample reports ✅ Included             Six sample report files
                                                  are present in
                                                  `data/reports/`

  Client entitlement      ✅ Implemented          Explicitly requested
  checks                                          unauthorized report IDs
                                                  return no report
                                                  evidence

  Prompt-injection        ✅ Tested               Requests to disclose
  refusal                                         private client
                                                  information are refused

  CAGR calculation logic  ✅ Implemented          Calculation helper
                                                  validates inputs and
                                                  returns formula/derived
                                                  value

  Conflict detection      ✅ Implemented          Prototype can identify
                                                  differing CAGR values
                                                  and forecast periods

  Escalation workflow     ✅ Implemented          Tickets are stored in a
                                                  local JSON file

  Automated test suite    ✅ Passing              Latest reported run:
                                                  `12 passed`

  Vector database /       ⏳ Not completed        Current retrieval is
  semantic search                                 keyword-based

  Full agent              ⏳ Not completed        No complete LangGraph
  orchestration and                               workflow is claimed
  critic                                          

  MySQL persistence       ⏳ Not completed        Escalations currently
                                                  use JSON storage

  CodeIgniter 3 portal    ⏳ Not completed        Current work is the
  integration                                     Python API prototype

  Full Docker Compose     ⏳ Not completed        Reproducible full-stack
  stack                                           deployment is not yet
                                                  claimed
  -----------------------------------------------------------------------

## 🔐 Access control model

The prototype uses client-to-report entitlement rules. The policy is
enforced by the retrieval layer, rather than relying on the answer
writer to ignore unauthorized material.

  Client   Authorized report IDs in the current prototype
  -------- ------------------------------------------------
  `C-01`   `R-101`, `R-102`, `R-103`
  `C-02`   `R-102`, `R-103`

Reports `R-104`, `R-105`, and `R-106` are sample files but are **not
automatically authorized** by their presence in the folder.

### Security behaviors tested

-   A `C-02` request explicitly asking for `R-101` receives no citations
    or protected report content.
-   A request to reveal private client information is refused.
-   An unsupported question can create an escalation ticket for human
    review.

> This is a prototype security boundary, not a substitute for a full
> security review, authentication/authorization hardening, or production
> monitoring.

## 📚 Sample report set

  -----------------------------------------------------------------------
  Report ID               Sample report title     Purpose in the
                                                  prototype
  ----------------------- ----------------------- -----------------------
  `R-101`                 Global Smart Water      Market size, CAGR, and
                          Meter Market            regional-share example

  `R-102`                 Smart Water Metering:   A deliberately
                          Industry Outlook 2024   different market scope
                                                  and forecast period for
                                                  conflict testing

  `R-103`                 Residential Water       Demonstrates a
                          Purifier Market 2025    different market topic
                                                  and limited available
                                                  figures

  `R-104`                 Additional sample       Additional sample
                          report                  content; not
                                                  automatically entitled

  `R-105`                 Additional sample       Additional sample
                          report                  content; not
                                                  automatically entitled

  `R-106`                 Additional sample       Additional sample
                          report                  content; not
                                                  automatically entitled
  -----------------------------------------------------------------------

**Data disclaimer:** These are assignment/demo sample reports. Do not
present the sample figures as independently verified market research.

## ⚖️ Example: conflict-aware response

The sample reports intentionally contain different smart-water-meter
CAGR figures:

  Report      Reported CAGR Period       Scope consideration
  --------- --------------- ------------ ----------------------------------
  `R-101`             11.2% 2025--2030   Broader smart water meter market
  `R-102`              9.8% 2024--2029   Hardware-only market

The prototype can surface both values and flag that the forecast periods
and market definitions differ. It should not silently combine the
figures or present them as directly comparable without qualification.

## 🧮 CAGR calculator

The calculation helper uses the standard compound-growth formula:

\[ `\text{Projected Value}`{=tex} = `\text{Base Value}`{=tex}
`\times `{=tex}(1 + `\text{CAGR}`{=tex}/100)\^{`\text{Years}`{=tex}} \]

It validates inputs such as negative base values, invalid CAGR values,
and inconsistent base/target years. A derived projection should always
be labeled as a calculation, with its source value, rate, time period,
and assumptions visible.

## 🛠️ Technology

  -----------------------------------------------------------------------
  Technology                          Role
  ----------------------------------- -----------------------------------
  Python                              Application logic

  FastAPI                             HTTP API and request validation

  Pydantic / typed models             Structured request and response
                                      data, where defined

  Markdown                            Sample report content

  JSON                                Local escalation-ticket persistence

  Pytest                              Automated tests

  Swagger UI / OpenAPI                Interactive endpoint testing
  -----------------------------------------------------------------------

Optional vector-search dependencies were explored during development,
but the local embedding stack encountered a Windows PyTorch DLL
dependency issue. **The current working prototype does not rely on those
optional dependencies to pass its existing tests.**

## 🚀 Run locally

### 1. Clone the repository

``` powershell
git clone https://github.com/Wahsahil/Project-Atlas.git
cd Project-Atlas
```

### 2. Create and activate a virtual environment

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use the execution-policy guidance
appropriate for your machine, or run the environment's Python executable
directly.

### 3. Install dependencies

``` powershell
python -m pip install -r requirements.txt
```

### 4. Start the API

If the application entry point is `app/main.py` and defines
`app = FastAPI(...)`, run:

``` powershell
uvicorn app.main:app --reload
```

### 5. Open the interactive API docs

Visit:

-   Swagger UI: `http://127.0.0.1:8000/docs`
-   Health endpoint: `http://127.0.0.1:8000/health`

Keep the terminal running while you use Swagger UI.

## 🔌 API endpoints

  -----------------------------------------------------------------------
  Method                  Endpoint                Purpose
  ----------------------- ----------------------- -----------------------
  `GET`                   `/health`               Check whether the API
                                                  is responding

  `POST`                  `/chat`                 Submit a client
                                                  question and receive a
                                                  structured answer

  `GET`                   `/escalations`          List locally stored
                                                  escalation tickets

  `POST`                  `/ingest`               Verify the actual
                                                  implementation before
                                                  relying on this
                                                  endpoint; a complete
                                                  ingestion pipeline is
                                                  not claimed here
  -----------------------------------------------------------------------

### Example request for `POST /chat`

``` json
{
  "client_id": "C-01",
  "question": "Compare the reported CAGR figures for the smart water meter market."
}
```

### Response shape

``` json
{
  "answer": "Answer text with relevant qualifications.",
  "citations": [
    {
      "report_id": "R-101",
      "text": "Relevant report excerpt."
    }
  ],
  "confidence": 0.85,
  "conflicts": [],
  "derived_values": [],
  "escalated": false
}
```

The values above illustrate the response structure only; actual output
depends on the question and the available report evidence.

## 🧪 Tests

Run the automated suite from the repository root:

``` powershell
python -m pytest -q
```

Latest result reported during development:

``` text
12 passed
```

### Manual Swagger test matrix

  -----------------------------------------------------------------------
  Scenario                            Expected behavior
  ----------------------------------- -----------------------------------
  Compare smart-water-meter CAGR      Surface relevant figures and flag
                                      differences

  `C-02` requests `R-101`             No unauthorized citations or report
                                      content

  Ask for private client contact      Refuse disclosure
  details                             

  Ask a question the prototype cannot Escalate for review
  answer reliably                     

  Open `/health`                      Successful health response

  Open `/escalations` after an        Show locally stored tickets
  escalation                          
  -----------------------------------------------------------------------

A passing test suite validates only the tested behaviors; it does not
mean every assignment requirement is complete.

## ⚠️ Current limitations

This prototype intentionally has a limited scope:

1.  **Keyword retrieval:** it is not yet a production-grade vector or
    semantic retrieval system.
2.  **No full LLM agent workflow:** routing, critic/fact-checker, and
    tool orchestration are not fully implemented as a dedicated agent
    graph.
3.  **JSON-backed escalations:** tickets are not persisted in MySQL.
4.  **No completed legacy portal integration:** a CodeIgniter 3 chat
    interface and integration are still outstanding.
5.  **No verified full-stack deployment:** the complete API, MySQL,
    vector database, and PHP portal Docker Compose stack is not
    finished.
6.  **Sample data only:** report figures are for demonstration and
    assignment testing, not investment or business advice.
7.  **Confidence is heuristic:** it should not be interpreted as a
    calibrated probability of correctness.
8.  **No production readiness claim:** authentication, observability,
    load testing, and comprehensive security validation require further
    work.

## 🗓️ Suggested next steps

-   [ ] Add a persistent vector store and embedding-based retrieval.
-   [ ] Ensure entitlement filtering occurs before report passages reach
    any generation component.
-   [ ] Implement a dedicated routing / critic workflow and read-only
    SQL tool.
-   [ ] Move report, entitlement, conversation, and escalation storage
    to MySQL.
-   [ ] Integrate the Python API with the CodeIgniter 3 portal.
-   [ ] Add a reproducible Docker Compose deployment.
-   [ ] Expand the evaluation set to 25+ questions and report failures
    honestly.
-   [ ] Record a short demo covering normal questions, conflicts, prompt
    injection, entitlements, and escalation.

## 📁 Repository structure

``` text
Project-Atlas/
├── app/
│   ├── main.py          # FastAPI application and endpoints
│   ├── knowledge.py     # Report retrieval and entitlement checks
│   ├── calculator.py    # CAGR calculation helper
│   └── escalations.py   # Local JSON-backed escalation workflow
├── data/
│   ├── reports/         # Markdown sample reports
│   └── escalations.json # Local tickets created during testing
├── test_project_atlas.py
├── test_calculator.py
├── requirements.txt
├── README.md
└── EVALUATION.md
```

The exact contents may evolve as the prototype is extended.

## 👤 Author

**Sahil Chaurasia**\
AI & ML / Software Development

Repository:
[Wahsahil/Project-Atlas](https://github.com/Wahsahil/Project-Atlas)

------------------------------------------------------------------------

::: {align="center"}
**Project Atlas --- a prototype for evidence-grounded market research.**

*Built as an AI Software Developer assignment project.*
:::
