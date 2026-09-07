from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path

from database_backend import connect, execute


class MemoryStore:

    def __init__(self, database_path):
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)

        self.connection = connect(self.database_path)

        self.initialize()

    def initialize(self):
        execute(
            self.connection,
            """
            CREATE TABLE IF NOT EXISTS memories (
                memory_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                account_type TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """,
        )

        execute(
            self.connection,
            """
            CREATE INDEX IF NOT EXISTS idx_memories_user
            ON memories(user_id)
            """,
        )

        self.connection.commit()

    def add(self, user_id, account_type, content):

        if not user_id:
            raise ValueError("user_id required")

        if not account_type:
            raise ValueError("account_type required")

        if not isinstance(content, str):
            raise ValueError("Memory content must be text")

        content = content.strip()

        if not content:
            raise ValueError("Memory content cannot be empty")

        memory_id = str(uuid.uuid4())

        created_at = datetime.now(
            timezone.utc
        ).isoformat()

        execute(
            self.connection,
            """
            INSERT INTO memories
            (
                memory_id,
                user_id,
                account_type,
                content,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                memory_id,
                user_id,
                account_type,
                content,
                created_at,
            ),
        )

        self.connection.commit()

        return {
            "memory_id": memory_id,
            "user_id": user_id,
            "account_type": account_type,
            "content": content,
            "created_at": created_at,
        }

    def list_for_user(self, user_id):

        rows = execute(
            self.connection,
            """
            SELECT *
            FROM memories
            WHERE user_id = ?
            ORDER BY created_at ASC
            """,
            (user_id,),
        ).fetchall()

        return [dict(row) for row in rows]

    def delete_for_user(self, user_id, memory_id):

        result = execute(
            self.connection,
            """
            DELETE FROM memories
            WHERE memory_id = ?
            AND user_id = ?
            """,
            (
                memory_id,
                user_id,
            ),
        )

        self.connection.commit()

        return result.rowcount > 0
