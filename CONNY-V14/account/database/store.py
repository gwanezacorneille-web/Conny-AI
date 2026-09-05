import sqlite3
import uuid
from pathlib import Path

from account.security.passwords import (
    hash_password,
    verify_password,
)


class AccountStore:

    def __init__(self, database_path):
        self.database_path = Path(database_path)

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.connection = sqlite3.connect(
            self.database_path
        )

        self.connection.row_factory = sqlite3.Row

        self.initialize()

    def initialize(self):
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS accounts (
                user_id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT,
                account_type TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        self.connection.commit()

    def create_private(self, username, password):

        username = username.strip()

        if not username:
            raise ValueError("Username required")

        user_id = str(uuid.uuid4())

        self.connection.execute(
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

        row = self.connection.execute(
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
