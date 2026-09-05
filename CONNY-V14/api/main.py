from __future__ import annotations

import os
import sys
import uuid
from pathlib import Path

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

V14_ROOT = Path(__file__).resolve().parents[1]
ROOT = V14_ROOT.parent

if str(V14_ROOT) not in sys.path:
    sys.path.insert(0, str(V14_ROOT))

from account.database.store import AccountStore
from account.models import AccountType

from api.session_store import PersistentSessionStore
from api.chat import authenticated_chat


DATA_DIR = V14_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

ACCOUNT_DB = DATA_DIR / "accounts.db"
SESSION_DB = DATA_DIR / "sessions.db"

accounts = AccountStore(ACCOUNT_DB)
sessions = PersistentSessionStore(SESSION_DB)

app = FastAPI(
    title="CONNY AI V14 API",
    version="14.15.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RegisterRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str
    account_type: str = "private"


class AuthResponse(BaseModel):
    success: bool
    token: str | None = None
    user_id: str | None = None
    username: str | None = None
    account_type: str | None = None
    message: str


def response_for(session, message: str = "Success"):
    return {
        "success": True,
        "token": session.token,
        "user_id": session.user_id,
        "username": session.username,
        "account_type": session.account_type,
        "expires_at": session.expires_at,
        "message": message,
    }


def get_token(authorization: str | None, x_conny_token: str | None):
    if x_conny_token:
        return x_conny_token

    if authorization and authorization.lower().startswith("bearer "):
        return authorization[7:].strip()

    return None


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "brain": "v14",
        "auth": "online",
        "version": "14.15.0",
    }


@app.post("/auth/register")
def register(request: RegisterRequest):
    username = request.username.strip()

    if not username:
        raise HTTPException(400, "Username required")

    if not request.password:
        raise HTTPException(400, "Password required")

    try:
        user_id = accounts.create_private(
            username,
            request.password,
        )
    except Exception:
        raise HTTPException(
            409,
            "Username is already registered",
        )

    row = accounts.authenticate_private(
        username,
        request.password,
    )

    if row is None:
        raise HTTPException(
            500,
            "Account created but authentication failed",
        )

    session = sessions.create(
        row["user_id"],
        row["username"],
        row["account_type"],
    )

    return response_for(
        session,
        "Account created successfully",
    )


@app.post("/auth/login")
def login(request: LoginRequest):
    account_type = request.account_type.strip().lower()

    if account_type == "private":
        row = accounts.authenticate_private(
            request.username,
            request.password,
        )

        if row is None:
            raise HTTPException(
                401,
                "Invalid username or password",
            )

        session = sessions.create(
            row["user_id"],
            row["username"],
            row["account_type"],
        )

        return response_for(
            session,
            "Login successful",
        )

    if account_type == "vip":
        vip_username = os.getenv("CONNY_VIP_USERNAME")
        vip_secret = os.getenv("CONNY_VIP_SECRET")

        if (
            not vip_username
            or not vip_secret
            or request.username != vip_username
            or request.password != vip_secret
        ):
            raise HTTPException(
                401,
                "Invalid VIP credentials",
            )

        user_id = "vip-" + uuid.uuid5(
            uuid.NAMESPACE_DNS,
            vip_username,
        ).hex

        session = sessions.create(
            user_id,
            vip_username,
            AccountType.VIP.value,
        )

        return response_for(
            session,
            "VIP login successful",
        )

    raise HTTPException(
        400,
        "Unsupported account type",
    )


@app.post("/auth/guest")
def guest():
    user_id = "guest-" + uuid.uuid4().hex
    username = "Guest"

    session = sessions.create(
        user_id,
        username,
        AccountType.GUEST.value,
    )

    return response_for(
        session,
        "Guest session created",
    )


@app.get("/auth/session")
def validate_session(
    authorization: str | None = Header(default=None),
    x_conny_token: str | None = Header(default=None),
):
    token = get_token(
        authorization,
        x_conny_token,
    )

    session = sessions.validate(token)

    if session is None:
        raise HTTPException(
            401,
            "Invalid or expired session",
        )

    return response_for(
        session,
        "Session valid",
    )


@app.post("/auth/logout")
def logout(
    authorization: str | None = Header(default=None),
    x_conny_token: str | None = Header(default=None),
):
    token = get_token(
        authorization,
        x_conny_token,
    )

    if not token:
        raise HTTPException(
            401,
            "Authentication token required",
        )

    if not sessions.revoke(token):
        raise HTTPException(
            401,
            "Invalid session",
        )

    return {
        "success": True,
        "message": "Logged out successfully",
    }


class ChatRequest(BaseModel):
    message: str


@app.post("/api/chat")
def chat(
    request: ChatRequest,
    authorization: str | None = Header(default=None),
    x_conny_token: str | None = Header(default=None),
):
    token = get_token(
        authorization,
        x_conny_token,
    )

    session = sessions.validate(token)

    if session is None:
        raise HTTPException(
            401,
            "Valid V14 authentication required",
        )

    return authenticated_chat(
        session,
        request.message,
    )
