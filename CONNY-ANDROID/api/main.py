from __future__ import annotations

import os
import sys
import uuid
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel


API_DIR = Path(__file__).resolve().parent
REPO_ROOT = API_DIR.parents[1]

V13_PATH = REPO_ROOT / "Conny-AI-V5" / "v13"
CORE_PATH = REPO_ROOT / "Conny-AI-V5"

for path in (V13_PATH, CORE_PATH):
    value = str(path)
    if value not in sys.path:
        sys.path.insert(0, value)

os.environ["CONNY_CORE_PATH"] = str(CORE_PATH)

from bridge.conny_bridge import ConnyBridge


app = FastAPI(
    title="CONNY AI API",
    version="13.0",
)

bridge = ConnyBridge()


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


class ChatResponse(BaseModel):
    text: str
    success: bool
    session_id: str
    version: str


@app.get("/")
def root():
    return {
        "name": "CONNY AI",
        "status": "online",
        "version": "13.0",
    }


@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "service": "CONNY AI API",
        "version": "13.0",
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    message = request.message.strip()
    session_id = request.session_id or str(uuid.uuid4())

    if not message:
        return ChatResponse(
            text="Please enter a question.",
            success=False,
            session_id=session_id,
            version="13.0",
        )

    try:
        answer = bridge.process(message)

        if not isinstance(answer, str):
            answer = str(answer)

        return ChatResponse(
            text=answer,
            success=True,
            session_id=session_id,
            version="13.0",
        )

    except Exception:
        return ChatResponse(
            text="CONNY AI could not process that request right now.",
            success=False,
            session_id=session_id,
            version="13.0",
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8000")),
    )
