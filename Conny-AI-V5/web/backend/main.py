from pathlib import Path
import re

from fastapi import FastAPI, Header
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from brain.brain import Brain
import threading


BASE_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = BASE_DIR / "web" / "frontend"


app = FastAPI(
    title="CONNY AI V12",
    version="12.0.0",
)


# V12 SESSION-ISOLATED BRAINS
# Each browser session receives its own Brain instance.
_brains = {}
_brains_lock = threading.Lock()


def get_brain(session_id: str):
    session_id = session_id.strip() or "anonymous"

    with _brains_lock:
        if session_id not in _brains:
            _brains[session_id] = Brain()

        return _brains[session_id]


# CONNY V12 Web Frontend
app.mount(
    "/frontend",
    StaticFiles(directory=FRONTEND_DIR),
    name="frontend",
)


# ============================================================
# V12 RESPONSE QUALITY
# ============================================================

def format_v12_response(response, intent):
    """
    Keep public web responses concise and useful.
    """

    if not isinstance(response, str):
        return response

    response = response.strip()

    if not response:
        return response

    # Long definition / explanation responses should be summarized.
    if intent in {
        "definition",
        "explanation",
        "knowledge",
    } and len(response) > 650:

        paragraphs = [
            p.strip()
            for p in response.split("\n\n")
            if p.strip()
        ]

        if paragraphs:
            summary = paragraphs[0]

            if len(summary) > 500:
                sentences = re.split(
                    r"(?<=[.!?])\s+",
                    summary
                )

                selected = []
                length = 0

                for sentence in sentences:
                    selected.append(sentence)
                    length += len(sentence)

                    if length >= 300:
                        break

                summary = " ".join(selected)

            return summary.strip()

    return response


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "brain": "online",
    }


@app.post("/api/chat")
def chat(
    request: ChatRequest,
    x_session_id: str | None = Header(default=None, alias="X-Session-ID"),
):
    message = request.message.strip()

    if not message:
        return {
            "response": "Please enter a message."
        }

    session_id = x_session_id or "default"

    session_brain = get_brain(session_id)

    response = session_brain.process(message)

    return {
        "response": response,
        "intent": session_brain.last_intent,
        "decision": session_brain.last_decision,
    }

