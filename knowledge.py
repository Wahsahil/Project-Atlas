from pathlib import Path
import re
REPORTS_DIR = Path(__file__).parent / "data" / "reports"

# Report access rules from the assignment.
# R-102 is a public excerpt; R-101 and R-103 are paid reports.
CLIENT_ENTITLEMENTS = {
    "C-01": {"R-101", "R-102", "R-103"},
    "C-02": {"R-102", "R-103"},
}


def retrieve_reports(client_id: str, question: str, top_k: int = 3):
    """Return relevant report snippets only after checking client access."""
    if client_id not in CLIENT_ENTITLEMENTS:
        return []

    allowed_reports = CLIENT_ENTITLEMENTS[client_id]
    query_words = set(re.findall(r"\b[a-z0-9.]+\b", question.lower()))
    results = []

    for report_path in REPORTS_DIR.glob("R-*.md"):
        report_id = report_path.stem

        # Enforce authorization before reading report content.
        if report_id not in allowed_reports:
            continue

        content = report_path.read_text(encoding="utf-8")
        chunks = [
            line.strip()
            for line in content.splitlines()
            if line.strip()
        ]

        for chunk in chunks:
            chunk_words = set(re.findall(r"\b[a-z0-9.]+\b", chunk.lower()))
            score = len(query_words & chunk_words)

            if score > 0:
                results.append({
                    "report_id": report_id,
                    "source": report_path.name,
                    "text": chunk,
                    "score": score,
                })

    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:top_k]
