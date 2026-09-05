from __future__ import annotations

import secrets
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AuthSession:
    token: str
    user_id: str
    username: str
    account_type: str
    created_at: float
    expires_at: float
    active: bool


class PersistentSessionStore:
    def __init__(self, database_path: str | Path, lifetime_hours: int = 24 * 30):
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.lifetime_seconds = lifetime_hours * 3600

        self.connection = sqlite3.connect(self.database_path)
        self.connection.row_factory = sqlite3.Row
        self.initialize()

    def initialize(self):
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS auth_sessions (
                token TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                username TEXT NOT NULL,
                account_type TEXT NOT NULL,
                created_at REAL NOT NULL,
                expires_at REAL NOT NULL,
                active INTEGER NOT NULL DEFAULT 1
            )
            """
        )
        self.connection.commit()

    def create(self, user_id: str, username: str, account_type: str) -> AuthSession:
        now = time.time()
        expires = now + self.lifetime_seconds
        token = secrets.token_urlsafe(48)

        self.connection.execute(
            """
            INSERT INTO auth_sessions
            (token, user_id, username, account_type, created_at, expires_at, active)
            VALUES (?, ?, ?, ?, ?, ?, 1)
            """,
            (token, user_id, username, account_type, now, expires),
        )
        self.connection.commit()

        return AuthSession(
            token=token,
            user_id=user_id,
            username=username,
            account_type=account_type,
            created_at=now,
            expires_at=expires,
            active=True,
        )

    def validate(self, token: str | None):
        if not token:
            return None

        row = self.connection.execute(
            """
            SELECT *
            FROM auth_sessions
            WHERE token = ?
            AND active = 1
            """,
            (token,),
        ).fetchone()

        if row is None:
            return None

        if float(row["expires_at"]) <= time.time():
            self.revoke(token)
            return None

        return AuthSession(
            token=row["token"],
            user_id=row["user_id"],
            username=row["username"],
            account_type=row["account_type"],
            created_at=float(row["created_at"]),
            expires_at=float(row["expires_at"]),
            active=True,
        )

    def revoke(self, token: str):
        cursor = self.connection.execute(
            """
            UPDATE auth_sessions
            SET active = 0
            WHERE token = ?
            """,
            (token,),
        )
        self.connection.commit()
        return cursor.rowcount > 0

    def cleanup(self):
        self.connection.execute(
            """
            DELETE FROM auth_sessions
            WHERE expires_at <= ?
            """,
            (time.time(),),
        )
        self.connection.commit()
