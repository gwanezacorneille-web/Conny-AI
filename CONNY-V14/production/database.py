from __future__ import annotations

from pathlib import Path

from database_backend import connect, execute, using_postgres


class ProductionDatabase:
    """
    V14 production database health wrapper.

    PostgreSQL is used when DATABASE_URL is configured.
    SQLite WAL remains the local fallback.
    """

    def __init__(self, database_path: str | Path):
        self.database_path = Path(database_path)

        if not self.database_path.parent.exists():
            self.database_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

        self.connection = connect(self.database_path)

        if not using_postgres():
            self.configure_sqlite()

    @property
    def backend(self) -> str:
        if using_postgres():
            return "postgresql"

        return "sqlite-wal"

    def configure_sqlite(self):
        self.connection.execute(
            "PRAGMA journal_mode=WAL"
        )
        self.connection.execute(
            "PRAGMA foreign_keys=ON"
        )
        self.connection.execute(
            "PRAGMA busy_timeout=5000"
        )
        self.connection.commit()

    def health(self):
        row = execute(
            self.connection,
            "SELECT 1 AS ok",
        ).fetchone()

        if not row:
            return False

        return row["ok"] == 1

    def close(self):
        self.connection.close()
