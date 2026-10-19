
from pathlib import Path
import re

REPORTS_DIR = Path(__file__).resolve().parent.parent / "data" / "reports"

# R-102 is a public excerpt.
# R-101 and R-103 are paid reports.
CLIENT_ENTITLEMENTS = {
    "C-01": {"R-101", "R-102", "R-103"},
    "C-02": {"R-102", "R-103"},
}

STOP_WORDS = {
    "the", "a", "an", "is", "are", "in", "of", "for",
    "and", "to", "what", "compare", "between", "report",
    "reports", "give", "me", "show", "please", "how",
    "tell", "about", "can", "you", "could", "would",
    "with", "from", "which", "does", "do", "their",
    "this", "that", "it", "on", "at", "by", "according",
    "market", "size", "accordingto"
}

ALIASES = {
    "cagr": {"cagr", "growth"},
    "growth": {"growth", "cagr"},
    "apac": {"apac", "asia", "pacific", "asia-pacific"},
    "asia": {"asia", "apac"},
    "pacific": {"pacific", "apac"},
    "global": {"global", "worldwide"},
    "worldwide": {"global", "worldwide"},
    "meter": {"meter", "meters", "metering"},
    "meters": {"meter", "meters", "metering"},
    "metering": {"meter", "meters", "metering"},
    "forecast": {"forecast", "projection", "growth"},
    "projection": {"projection", "forecast"},
    "2024": {"2024"},
    "2025": {"2025"},
    "2029": {"2029"},
    "2030": {"2030"},
}


def tokenize(text: str) -> set[str]:
    """Normalize text into searchable terms."""
    text = text.lower().replace("-", " ")
    return set(re.findall(r"\b[a-z0-9.]+\b", text))


def expand_terms(words: set[str]) -> set[str]:
    """Expand common synonyms and normalize report ID tokens."""
    expanded = set(words)

    for word in words:
        expanded.update(ALIASES.get(word, set()))

    return expanded


def retrieve_reports(
    client_id: str,
    question: str,
    top_k: int = 10,
) -> list[dict]:
    """
    Retrieve matching report snippets for an authorized client.

    Entitlements are checked before report contents are opened.
    """
    if client_id not in CLIENT_ENTITLEMENTS:
        return []

    if not question or not question.strip():
        return []

    allowed_reports = CLIENT_ENTITLEMENTS[client_id]
    query_words = tokenize(question) - STOP_WORDS
    query_words = expand_terms(query_words)

    # Extract explicit report IDs such as R-101 or R-102.
    requested_ids = {
        f"R-{number}"
        for number in re.findall(
            r"\br[\s-]*(101|102|103)\b",
            question.lower()
        )
    }

    results = []

    if not REPORTS_DIR.is_dir():
        return []

    # Authorization check occurs before opening each file.
    for report_path in sorted(REPORTS_DIR.glob("R-*.md")):
        report_id = report_path.stem

        if report_id not in allowed_reports:
            continue

        # If the user explicitly asks for a report ID, prioritize it.
        content = report_path.read_text(encoding="utf-8")

        for line in content.splitlines():
            chunk = line.strip()

            if not chunk:
                continue

            chunk_words = expand_terms(tokenize(chunk))
            score = len(query_words & chunk_words)

            if report_id in requested_ids:
                score += 5

            # Avoid returning unrelated lines with zero overlap.
            if score > 0:
                results.append({
                    "report_id": report_id,
                    "source": report_path.name,
                    "text": chunk,
                    "score": score,
                })

    # Higher-scoring evidence appears first.
    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    limit = max(1, min(top_k, 20))
    return results[:limit]
