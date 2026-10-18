
import json
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path(__file__).resolve().parent
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def save_research(session_id, result):
    from uuid import UUID

    # Validate session identifier
    safe_id = str(UUID(session_id))

    report = {
        "session_id": safe_id,
        "created_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "research": result
    }

    destination = REPORTS_DIR / f"{safe_id}.json"
    temporary = REPORTS_DIR / f"{safe_id}.tmp"

    try:
        with temporary.open("w", encoding="utf-8") as file:
            json.dump(report, file, indent=4, ensure_ascii=False)

        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)

    return destination


def load_research(session_id):
    from uuid import UUID

    safe_id = str(UUID(session_id))
    destination = REPORTS_DIR / f"{safe_id}.json"

    if not destination.exists():
        return None

    with destination.open("r", encoding="utf-8") as file:
        return json.load(file)


def list_research():
    history = []

    for path in REPORTS_DIR.glob("*.json"):
        try:
            report = json.loads(
                path.read_text(encoding="utf-8")
            )

            research = report.get("research", {})

            history.append({
                "session_id": report["session_id"],
                "question": research.get("question", ""),
                "created_at": report.get("created_at", ""),
                "verdict": research.get("verdict", "uncertain")
            })

        except (OSError, ValueError, KeyError, TypeError):
            continue

    return sorted(
        history,
        key=lambda item: item["created_at"],
        reverse=True
    )

