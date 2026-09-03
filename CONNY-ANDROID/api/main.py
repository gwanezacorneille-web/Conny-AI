from pathlib import Path
import os
import sys
import threading
import uuid

from fastapi import FastAPI, Header
from pydantic import BaseModel


CORE_PATH = Path(r"/home/conny_the_miz/Conny-AI/Conny-AI-V5-V13-BACKUP-20260827-231231").resolve()

if not CORE_PATH.is_dir():
    raise FileNotFoundError(
        f"CONNY V13 core not found: {CORE_PATH}"
    )

if str(CORE_PATH) not in sys.path:
    sys.path.insert(0, str(CORE_PATH))


app = FastAPI(
    title="CONNY AI",
    version="V13",
)


_brains = {}
_brains_lock = threading.Lock()


def get_brain(session_id: str):
    session_id = (session_id or "anonymous").strip()

    with _brains_lock:
        if session_id not in _brains:
            from brain.brain import Brain

            old_cwd = Path.cwd()

            try:
                os.chdir(CORE_PATH)
                brain = Brain()
                _brains[session_id] = brain
            finally:
                os.chdir(old_cwd)

        return _brains[session_id]


def process_brain(brain, message: str):
    old_cwd = Path.cwd()

    try:
        os.chdir(CORE_PATH)

        if hasattr(brain, "process"):
            return brain.process(message)

        if hasattr(brain, "respond"):
            return brain.respond(message)

        if hasattr(brain, "run"):
            return brain.run(message)

        raise AttributeError(
            "CONNY Brain has no process/respond/run interface"
        )

    finally:
        os.chdir(old_cwd)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {
        "app": "CONNY AI",
        "version": "V13",
        "status": "online",
    }


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "brain": "online",
        "version": "V13",
    }


@app.post("/api/chat")
def chat(
    request: ChatRequest,
    x_session_id: str | None = Header(
        default=None,
        alias="X-Session-ID",
    ),
):
    message = request.message.strip()

    if not message:
        return {
            "response": "Please enter a message.",
            "success": False,
            "version": "V13",
        }

    session_id = x_session_id or str(uuid.uuid4())

    try:
        brain = get_brain(session_id)

        response = process_brain(
            brain,
            message,
        )

        if response is None:
            response = ""

        response = str(response).strip()

        if not response:
            return {
                "response": "CONNY returned an empty response.",
                "success": False,
                "intent": getattr(
                    brain,
                    "last_intent",
                    None,
                ),
                "decision": getattr(
                    brain,
                    "last_decision",
                    None,
                ),
                "session_id": session_id,
                "version": "V13",
            }

        return {
            "response": response,
            "success": True,
            "intent": getattr(
                brain,
                "last_intent",
                None,
            ),
            "decision": getattr(
                brain,
                "last_decision",
                None,
            ),
            "session_id": session_id,
            "version": "V13",
        }

    except Exception as exc:
        import traceback

        traceback.print_exc()

        return {
            "response": "CONNY encountered an internal error.",
            "success": False,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "session_id": session_id,
            "version": "V13",
        }
