from io import BytesIO
from fastapi.responses import StreamingResponse
from pdf_export import generate_pdf
from session_storage import load_research, list_research
from uuid import UUID
from session_storage import save_research
from uuid import uuid4
import threading
import urllib.request
import urllib.error
import json
import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, Field

from multi_agent_system import agent_graph

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("browsermind")

BASE_DIR = Path(__file__).resolve().parent
research_lock = threading.Lock()

app = FastAPI(
    title="BrowserMind API",
    description="Multi-Agent AI Research Platform",
    version="1.0.0"
)


class ResearchRequest(BaseModel):
    question: str = Field(
        min_length=3,
        max_length=500
    )


def initial_state(question):
    return {
        "question": question,
        "tasks": [],
        "sources": [],
        "analysis": "",
        "verdict": "pending"
    }


@app.get("/")
def home():
    return {
        "application": "BrowserMind",
        "status": "running"
    }


@app.get("/dashboard")
def dashboard():
    file_path = BASE_DIR / "frontend" / "index.html"

    if not file_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Dashboard file not found"
        )

    return FileResponse(file_path)


@app.post("/research")
def research(request: ResearchRequest):
    try:
        result = agent_graph.invoke(
            initial_state(request.question.strip())
        )

        return {
            "question": result["question"],
            "tasks": result["tasks"],
            "analysis": result["analysis"],
            "verdict": result["verdict"],
            "sources": [
                {
                    "url": source["url"],
                    "title": source.get("title", "")
                }
                for source in result["sources"]
                if source.get("status") == "success"
            ]
        }

    except Exception:
        logger.exception("Research workflow failed")
        raise HTTPException(
            status_code=500,
            detail="Research workflow failed"
        )


@app.get("/research/stream")
def stream_research(question: str):
    question = question.strip()

    if not 3 <= len(question) <= 500:
        raise HTTPException(
            status_code=422,
            detail="Question must contain 3-500 characters"
        )

    def send_event(event_name, data):
        return (
            f"event: {event_name}\n"
            f"data: {json.dumps(data)}\n\n"
        )

    
    def generate():

        session_id = str(uuid4())
        logger.info("Research session started: %s", session_id)

        if not research_lock.acquire(blocking=False):
            yield send_event(
                "research_error",
                {
                    "message": (
                        "BrowserMind is already researching. "
                        "Please try again after it finishes."
                    )
                }
            )
            return

        state = initial_state(question)
        
        yield send_event(
            "session",
            {"session_id": session_id}
        )

        try:
            for update in agent_graph.stream(
                state,
                stream_mode="updates"
            ):
                for agent, data in update.items():
                    state.update(data)

                    yield send_event(
                        "progress",
                        {
                            "agent": agent,
                            "status": "completed"
                        }
                    )

            result = {
                "question": state["question"],
                "tasks": state["tasks"],
                "analysis": state["analysis"],
                "verdict": state["verdict"],
                "sources": [
                    {
                        "url": source["url"],
                        "title": source.get("title", "")
                    }
                    for source in state["sources"]
                    if source.get("status") == "success"
                ]
            }

            result["session_id"] = session_id

            saved_path = save_research(
                session_id,
                result
            )

            logger.info(
                "Research report saved: %s",
                saved_path
            )

            
            

            yield send_event("result", result)

        except Exception:
            logger.exception("Streaming research failed")
            yield send_event(
                "research_error",
                {"message": "Research workflow failed"}
            )

        finally:
            research_lock.release()

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )


@app.get("/health")
def health_check():
    ollama_status = "offline"

    try:
        with urllib.request.urlopen(
            "http://127.0.0.1:11434/api/tags",
            timeout=3
        ) as response:
            if response.status == 200:
                ollama_status = "online"

    except (urllib.error.URLError, TimeoutError, OSError):
        pass

    return {
        "application": "BrowserMind",
        "api": "online",
        "ollama": ollama_status,
        "ready": ollama_status == "online"
    }


@app.get("/reports/{session_id}/download")
def download_report(session_id: str):
    try:
        UUID(session_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid session ID"
        )

    report = load_research(session_id)

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    return FileResponse(
        BASE_DIR / "reports" / f"{session_id}.json",
        media_type="application/json",
        filename=f"browsermind-{session_id}.json"
    )


@app.get("/reports/{session_id}/pdf")
def download_pdf(session_id: str):
    from uuid import UUID
    from session_storage import load_research

    try:
        safe_id = str(UUID(session_id))
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid session ID"
        )

    report = load_research(safe_id)

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Research report not found"
        )

    pdf_bytes = generate_pdf(report)

    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition":
                f'attachment; filename="browsermind-{safe_id}.pdf"'
        }
    )


@app.get("/history")
def research_history():
    return {
        "total": len(list_research()),
        "sessions": list_research()
    }


@app.get("/history/{session_id}")
def research_history_detail(session_id: str):
    from uuid import UUID

    try:
        safe_id = str(UUID(session_id))
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid session ID"
        )

    report = load_research(safe_id)

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Research session not found"
        )

    return report


