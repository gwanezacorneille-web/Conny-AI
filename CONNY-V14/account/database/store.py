from __future__ import annotations

import uuid
from pathlib import Path


from account.security.passwords import (
    hash_password,
    verify_password,
)

from database_backend import connect, execute


class AccountStore:

    def __init__(self, database_path):
        self.database_path = Path(database_path)

        if not self.database_path.parent.exists():
            self.database_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

        self.connection = connect(self.database_path)
        self.initialize()

    def initialize(self):
        execute(
            self.connection,
            """
            CREATE TABLE IF NOT EXISTS accounts (
                user_id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT,
                account_type TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """,
        )
        self.connection.commit()

    def create_private(self, username, password):
        username = username.strip()

        if not username:
            raise ValueError("Username required")

        user_id = str(uuid.uuid4())

        execute(
            self.connection,
            """
            INSERT INTO accounts
            (user_id, username, password_hash, account_type)
            VALUES (?, ?, ?, 'private')
            """,
            (
                user_id,
                username,
                hash_password(password),
            ),
        )

        self.connection.commit()

        return user_id

    def authenticate_private(
        self,
        username,
        password,
    ):
        row = execute(
            self.connection,
            """
            SELECT *
            FROM accounts
            WHERE username = ?
            AND account_type = 'private'
            AND is_active = 1
            """,
            (username.strip(),),
        ).fetchone()

        if row is None:
            return None

        if not verify_password(
            password,
            row["password_hash"],
        ):
            return None

        return dict(row)
