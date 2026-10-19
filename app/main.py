
import re

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.calculator import calculate_cagr_projection
from app.knowledge import retrieve_reports


app = FastAPI(
    title="Project Atlas",
    description="AI-powered market research report copilot",
    version="1.1.0",
)


class ChatRequest(BaseModel):
    client_id: str = Field(min_length=1, max_length=50)
    question: str = Field(min_length=3, max_length=1000)


@app.get("/")
def root():
    return {"message": "Project Atlas API is running"}


@app.get("/health")
def health():
    return {"status": "healthy", "service": "Project Atlas API"}


def is_unsafe(question: str) -> bool:
    q = question.lower()

    unsafe_patterns = [
        "client email",
        "contact emails",
        "clients table",
        "drop table",
        "delete from",
        "ignore all previous instructions",
        "reveal private",
        "show me all client",
        "print the full contents",
    ]

    return any(term in q for term in unsafe_patterns)


def extract_cagr(reports):
    values = []

    for item in reports:
        match = re.search(
            r"CAGR:\s*([\d.]+)%\s+for\s+(\d{4})\s*[-–]\s*(\d{4})",
            item["text"],
            re.IGNORECASE,
        )

        if match:
            values.append({
                "report_id": item["report_id"],
                "cagr_percent": float(match.group(1)),
                "start_year": int(match.group(2)),
                "end_year": int(match.group(3)),
                "text": item["text"],
            })

    # Remove duplicate matches.
    unique = {
        (
            item["report_id"],
            item["cagr_percent"],
            item["start_year"],
            item["end_year"],
        ): item
        for item in values
    }

    return list(unique.values())


def extract_market_sizes(reports):
    values = []

    for item in reports:
        match = re.search(
            r"(?:2024\s+)?global market size:\s*USD\s*([\d.]+)"
            r"\s*billion",
            item["text"],
            re.IGNORECASE,
        )

        if match:
            values.append({
                "report_id": item["report_id"],
                "value_usd_billion": float(match.group(1)),
                "text": item["text"],
            })

    return values


def requested_target_year(question: str):
    """Return an explicit four-digit target year, if present."""

    matches = re.findall(r"\b(20\d{2})\b", question)

    if not matches:
        return None

    return int(matches[-1])


def wants_projection(question: str) -> bool:
    q = question.lower()

    projection_terms = (
        "project",
        "projection",
        "forecast",
        "by 2030",
        "by 2029",
        "by 2028",
        "by 2027",
        "by 2035",
        "what will",
        "estimate the market",
    )

    return any(term in q for term in projection_terms)


@app.post("/chat")
def chat(request: ChatRequest):
    question = request.question.strip()
    q = question.lower()

    if is_unsafe(question):
        return {
            "answer": (
                "I cannot disclose private client information or perform "
                "destructive database actions."
            ),
            "citations": [],
            "confidence": 1.0,
            "conflicts": [],
            "derived_values": [],
            "escalated": False,
        }

    reports = retrieve_reports(
        request.client_id,
        question,
        top_k=10,
    )

    if not reports:
        return {
            "answer": (
                "No authorized report evidence was found. Please clarify "
                "the question or escalate it for review."
            ),
            "citations": [],
            "confidence": 0.0,
            "conflicts": [],
            "derived_values": [],
            "escalated": True,
        }

    citations = [
        {
            "report_id": item["report_id"],
            "text": item["text"],
        }
        for item in reports
    ]

    cagr_values = extract_cagr(reports)
    market_values = extract_market_sizes(reports)

    conflicts = []
    derived_values = []
    confidence = 0.5
    escalated = False

    # Handle explicit projection requests.
    if wants_projection(question):
        target_year = requested_target_year(question)

        usable_pairs = []

        for market in market_values:
            for cagr in cagr_values:
                if market["report_id"] != cagr["report_id"]:
                    continue

                # The report's stated CAGR period must support the
                # requested projection horizon.
                if target_year is None:
                    continue

                if not (
                    cagr["start_year"] <= target_year
                    <= cagr["end_year"]
                ):
                    continue

                base_year = 2024

                # Do not project from a 2024 base using a CAGR that
                # starts in 2025 unless the calculation convention is
                # explicitly declared. This implementation requires
                # the CAGR period to start in the base year.
                if cagr["start_year"] != base_year:
                    continue

                years = target_year - base_year

                if years < 0:
                    continue

                usable_pairs.append((market, cagr, years))

        if usable_pairs:
            market, cagr, years = usable_pairs[0]

            projection = calculate_cagr_projection(
                base_value=market["value_usd_billion"],
                cagr_percent=cagr["cagr_percent"],
                years=years,
                base_year=2024,
                target_year=target_year,
            )

            derived_values.append({
                "report_id": market["report_id"],
                "metric": "projected_market_size",
                "unit": "USD billion",
                **projection,
                "assumption": (
                    "Compound annual growth is applied to the stated "
                    "base value for the specified number of years."
                ),
            })

            answer = (
                f"The calculated projection for {target_year} is "
                f"USD {projection['projected_value']:.2f} billion, "
                f"using the 2024 base value of "
                f"USD {market['value_usd_billion']:.2f} billion and "
                f"a CAGR of {cagr['cagr_percent']}% for "
                f"{years} compounding years."
            )
            confidence = 0.85

        else:
            answer = (
                "I could not calculate this projection reliably from the "
                "authorized excerpts. The available base value and CAGR "
                "must refer to a compatible market scope and period. "
                "Human review is required."
            )
            confidence = 0.25
            escalated = True

    # Handle CAGR questions and comparisons.
    elif "cagr" in q or "growth rate" in q:
        unique_values = {
            (
                item["report_id"],
                item["cagr_percent"],
                item["start_year"],
                item["end_year"],
            )
            for item in cagr_values
        }

        values = sorted(unique_values)

        if len(values) > 1:
            details = [
                f"{report_id} reports {rate}% for {start}–{end}."
                for report_id, rate, start, end in values
            ]

            answer = (
                "The retrieved reports contain different CAGR figures: "
                + " ".join(details)
                + " Check the market definitions and forecast periods "
                "before comparing them."
            )

            conflicts.append({
                "type": "different_cagr_figures",
                "report_values": [
                    {
                        "report_id": report_id,
                        "cagr_percent": rate,
                        "period": f"{start}-{end}",
                    }
                    for report_id, rate, start, end in values
                ],
                "explanation": (
                    "The reports use different forecast periods and may "
                    "use different market scopes."
                ),
            })
            confidence = 0.85

        elif values:
            report_id, rate, start, end = values[0]

            answer = (
                f"{report_id} reports a CAGR of {rate}% for "
                f"{start}–{end}."
            )
            confidence = 0.9

        else:
            answer = "No authorized CAGR figure was found in the retrieved excerpts."
            confidence = 0.25
            escalated = True

    # Handle market-size questions.
    elif "market size" in q or "market value" in q:
        if market_values:
            answer = "Reported market sizes: " + "; ".join(
                f"{item['report_id']}: USD "
                f"{item['value_usd_billion']:.2f} billion"
                for item in market_values
            ) + "."

            if len({
                item["value_usd_billion"]
                for item in market_values
            }) > 1:
                conflicts.append({
                    "type": "different_market_size_figures",
                    "values": market_values,
                    "explanation": (
                        "Market definitions and included segments must be "
                        "checked before comparing these figures."
                    ),
                })

            confidence = 0.9

        else:
            answer = (
                "The retrieved excerpts do not contain a market-size "
                "figure that answers this question."
            )
            confidence = 0.3
            escalated = True

    else:
        answer = (
            "Relevant authorized report excerpts were retrieved, but this "
            "prototype cannot reliably answer this question yet."
        )
        confidence = 0.3
        escalated = True

    return {
        "answer": answer,
        "citations": citations,
        "confidence": confidence,
        "conflicts": conflicts,
        "derived_values": derived_values,
        "escalated": escalated,
    }


@app.get("/escalations")
def escalations():
    # Persistent MySQL escalation tickets are not implemented yet.
    return {
        "items": [],
        "note": "Persistent escalation storage is not configured yet.",
    }
