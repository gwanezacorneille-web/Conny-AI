from __future__ import annotations

import sqlite3
from pathlib import Path


class ProductionDatabase:
    """
    Production-safe SQLite initialization.

    SQLite remains the default local/single-service database.
    WAL mode improves concurrent read behavior and reduces
    reader/writer blocking.
    """

    def __init__(self, database_path: str | Path):
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
        self.configure()

    def configure(self):
        self.connection.execute("PRAGMA journal_mode=WAL")
        self.connection.execute("PRAGMA foreign_keys=ON")
        self.connection.execute("PRAGMA busy_timeout=5000")
        self.connection.commit()

    def health(self):
        row = self.connection.execute(
            "SELECT 1 AS ok"
        ).fetchone()

        return bool(row and row["ok"] == 1)

    def close(self):
        self.connection.close()
