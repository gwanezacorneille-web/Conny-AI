from __future__ import annotations

import sqlite3
import time
import uuid
from pathlib import Path


class ClientSyncStore:

    def __init__(self, database_path):
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.connection = sqlite3.connect(
            self.database_path,
            check_same_thread=False,
        )

        self.connection.row_factory = sqlite3.Row
        self.initialize()

    def initialize(self):
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS cloud_memory (
                sync_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                memory_id TEXT NOT NULL,
                content TEXT NOT NULL,
                updated_at REAL NOT NULL,
                version INTEGER NOT NULL DEFAULT 1,
                deleted INTEGER NOT NULL DEFAULT 0
            )
            """
        )

        self.connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_cloud_memory_user
            ON cloud_memory(user_id)
            """
        )

        self.connection.commit()

    def push(
        self,
        user_id,
        memory_id,
        content,
        version=1,
        deleted=False,
    ):
        now = time.time()

        existing = self.connection.execute(
            """
            SELECT version
            FROM cloud_memory
            WHERE user_id = ?
            AND memory_id = ?
            """,
            (user_id, memory_id),
        ).fetchone()

        if existing:
            next_version = max(
                int(existing["version"]) + 1,
                int(version),
            )

            self.connection.execute(
                """
                UPDATE cloud_memory
                SET content = ?,
                    updated_at = ?,
                    version = ?,
                    deleted = ?
                WHERE user_id = ?
                AND memory_id = ?
                """,
                (
                    content,
                    now,
                    next_version,
                    int(deleted),
                    user_id,
                    memory_id,
                ),
            )

        else:
            sync_id = str(uuid.uuid4())

            self.connection.execute(
                """
                INSERT INTO cloud_memory
                (
                    sync_id,
                    user_id,
                    memory_id,
                    content,
                    updated_at,
                    version,
                    deleted
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    sync_id,
                    user_id,
                    memory_id,
                    content,
                    now,
                    version,
                    int(deleted),
                ),
            )

        self.connection.commit()

        return {
            "success": True,
            "updated_at": now,
        }

    def pull(self, user_id, cursor=0):
        rows = self.connection.execute(
            """
            SELECT
                sync_id,
                user_id,
                memory_id,
                content,
                updated_at,
                version,
                deleted
            FROM cloud_memory
            WHERE user_id = ?
            AND updated_at > ?
            ORDER BY updated_at ASC
            """,
            (user_id, float(cursor)),
        ).fetchall()

        return [
            dict(row)
            for row in rows
        ]
