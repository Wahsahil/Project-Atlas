
import json
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from uuid import uuid4

ESCALATIONS_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "escalations.json"
)

_lock = Lock()


def create_escalation(
    client_id: str,
    question: str,
    reason: str,
    confidence: float,
) -> dict:
    """Persist a human-review ticket in a local JSON file."""
    ticket = {
        "ticket_id": str(uuid4()),
        "client_id": client_id,
        "question": question,
        "reason": reason,
        "confidence": confidence,
        "status": "open",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    with _lock:
        ESCALATIONS_FILE.parent.mkdir(parents=True, exist_ok=True)

        if ESCALATIONS_FILE.exists():
            try:
                tickets = json.loads(
                    ESCALATIONS_FILE.read_text(encoding="utf-8")
                )
                if not isinstance(tickets, list):
                    tickets = []
            except (json.JSONDecodeError, OSError):
                tickets = []
        else:
            tickets = []

        tickets.append(ticket)

        ESCALATIONS_FILE.write_text(
            json.dumps(tickets, indent=2),
            encoding="utf-8",
        )

    return ticket


def list_escalations() -> list[dict]:
    """Return persisted escalation tickets."""
    with _lock:
        if not ESCALATIONS_FILE.exists():
            return []

        try:
            tickets = json.loads(
                ESCALATIONS_FILE.read_text(encoding="utf-8")
            )
            return tickets if isinstance(tickets, list) else []
        except (json.JSONDecodeError, OSError):
            return []
