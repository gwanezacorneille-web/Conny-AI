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
from account.models import Account, AccountType
from database_backend import is_integrity_error

from api.session_store import PersistentSessionStore
from production.database import ProductionDatabase
from cloud.api import ClientSyncStore
from api.chat import authenticated_chat

from security.audit import audit, create_audit_logger
from security.roles import has_permission
from settings.exceptions import (
    SettingsAuthorizationError,
    SettingsValidationError,
)
from settings.service import SettingsService
from settings.store import SettingsStore


DATA_DIR = V14_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

ACCOUNT_DB = DATA_DIR / "accounts.db"
SESSION_DB = DATA_DIR / "sessions.db"
SETTINGS_DB = DATA_DIR / "settings.db"
SECURITY_LOG = DATA_DIR / "security.log"

accounts = AccountStore(ACCOUNT_DB)
production_db = ProductionDatabase(ACCOUNT_DB)
sessions = PersistentSessionStore(SESSION_DB)
sync_store = ClientSyncStore(DATA_DIR / "cloud.db")

settings_store = SettingsStore(SETTINGS_DB)
security_audit_logger = create_audit_logger(SECURITY_LOG)


class PersistentSessionAccountAdapter:
    def __init__(self, session_store):
        self.session_store = session_store

    def validate_session(self, token):
        return self.session_store.validate(token)


security_service = type(
    "V14SecurityService",
    (),
    {
        "authorize": staticmethod(
            lambda account, permission: has_permission(account, permission)
        )
    },
)()

settings_service = SettingsService(
    settings_store,
    security_service,
    lambda event, user_id=None: audit(
        security_audit_logger,
        event,
        user_id,
    ),
)

app = FastAPI(
    title="CONNY AI V14 API",
    version="14.16.0",
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
        "version": "14.16.0",
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
    except Exception as exc:
        if is_integrity_error(exc):
            print(
                f"V14 REGISTRATION DATABASE INTEGRITY ERROR: "
                f"{type(exc).__name__}: {exc}",
                file=sys.stderr,
            )

            error_text = str(exc).lower()

            if (
                "unique constraint" in error_text
                or "duplicate key" in error_text
                or "unique violation" in error_text
            ):
                raise HTTPException(
                    409,
                    "Username is already registered",
                )

            raise HTTPException(
                500,
                "Account registration failed",
            )
        print(
            f"V14 REGISTRATION ERROR: {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        raise HTTPException(
            500,
            "Account registration failed",
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


class SettingUpdateRequest(BaseModel):
    value: object


def authenticated_settings_account(
    authorization: str | None,
    x_conny_token: str | None,
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

    try:
        account_type = AccountType(session.account_type)
    except ValueError:
        raise HTTPException(
            403,
            "Invalid account type",
        )

    return Account(
        user_id=session.user_id,
        account_type=account_type,
        username=session.username,
        is_active=session.active,
    )


def settings_http_error(exc):
    if isinstance(exc, SettingsAuthorizationError):
        return HTTPException(
            403,
            str(exc),
        )

    if isinstance(exc, SettingsValidationError):
        return HTTPException(
            400,
            str(exc),
        )

    return HTTPException(
        500,
        "Settings operation failed",
    )


@app.get("/settings")
def get_settings(
    authorization: str | None = Header(default=None),
    x_conny_token: str | None = Header(default=None),
):
    account = authenticated_settings_account(
        authorization,
        x_conny_token,
    )

    try:
        values = settings_service.get_all(account)
    except Exception as exc:
        raise settings_http_error(exc)

    return {
        "success": True,
        "user_id": account.user_id,
        "settings": values,
    }


@app.get("/settings/{key}")
def get_setting(
    key: str,
    authorization: str | None = Header(default=None),
    x_conny_token: str | None = Header(default=None),
):
    account = authenticated_settings_account(
        authorization,
        x_conny_token,
    )

    try:
        setting = settings_service.get(
            account,
            key,
        )
    except Exception as exc:
        raise settings_http_error(exc)

    return {
        "success": True,
        "user_id": setting.user_id,
        "key": setting.key,
        "value": setting.value,
    }


@app.put("/settings/{key}")
def update_setting(
    key: str,
    request: SettingUpdateRequest,
    authorization: str | None = Header(default=None),
    x_conny_token: str | None = Header(default=None),
):
    account = authenticated_settings_account(
        authorization,
        x_conny_token,
    )

    try:
        setting = settings_service.set(
            account,
            key,
            request.value,
        )
    except Exception as exc:
        raise settings_http_error(exc)

    return {
        "success": True,
        "user_id": setting.user_id,
        "key": setting.key,
        "value": setting.value,
        "message": "Setting updated successfully",
    }


@app.post("/settings/{key}/reset")
def reset_setting(
    key: str,
    authorization: str | None = Header(default=None),
    x_conny_token: str | None = Header(default=None),
):
    account = authenticated_settings_account(
        authorization,
        x_conny_token,
    )

    try:
        setting = settings_service.reset(
            account,
            key,
        )
    except Exception as exc:
        raise settings_http_error(exc)

    return {
        "success": True,
        "user_id": setting.user_id,
        "key": setting.key,
        "value": setting.value,
        "message": "Setting reset successfully",
    }


@app.get("/api/production/health")
def production_health():
    return {
        "status": "ok" if production_db.health() else "error",
        "database": production_db.backend,
        "sessions": "persistent",
        "version": "14.16.0",
    }


class SyncPushRequest(BaseModel):
    memory_id: str
    content: str
    version: int = 1
    deleted: bool = False


@app.post("/sync/push")
def sync_push(
    request: SyncPushRequest,
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

    return sync_store.push(
        session.user_id,
        request.memory_id,
        request.content,
        request.version,
        request.deleted,
    )


@app.get("/sync/pull")
def sync_pull(
    cursor: float = 0,
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

    records = sync_store.pull(
        session.user_id,
        cursor,
    )

    next_cursor = cursor

    if records:
        next_cursor = max(
            float(record["updated_at"])
            for record in records
        )

    return {
        "success": True,
        "records": records,
        "cursor": next_cursor,
    }
