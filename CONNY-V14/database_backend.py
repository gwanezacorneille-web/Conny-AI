from __future__ import annotations

import os
import sqlite3
from pathlib import Path


def get_database_url() -> str | None:
    value = os.getenv("DATABASE_URL", "").strip()
    return value or None


def using_postgres() -> bool:
    return bool(get_database_url())


def connect(database_path: str | Path):
    """
    V14 database connection selector.

    DATABASE_URL present:
        PostgreSQL

    DATABASE_URL absent:
        Existing SQLite database
    """
    database_url = get_database_url()

    if database_url:
        try:
            import psycopg
            from psycopg.rows import dict_row
        except ImportError as exc:
            raise RuntimeError(
                "DATABASE_URL is configured but psycopg is not installed"
            ) from exc

        connection = psycopg.connect(
            database_url,
            row_factory=dict_row,
        )
        return connection

    connection = sqlite3.connect(
        Path(database_path),
        check_same_thread=False,
    )
    connection.row_factory = sqlite3.Row
    return connection


def execute(connection, sql: str, params=()):
    """
    Execute SQL using either SQLite or PostgreSQL.

    V14 SQL uses '?' placeholders. PostgreSQL uses '%s',
    so PostgreSQL statements are translated here.
    """
    module_name = connection.__class__.__module__

    if module_name.startswith("psycopg"):
        sql = sql.replace("?", "%s")

    return connection.execute(sql, params)


def is_integrity_error(exc: Exception) -> bool:
    """Return True for SQLite or PostgreSQL integrity errors."""
    if isinstance(exc, sqlite3.IntegrityError):
        return True

    try:
        import psycopg
    except ImportError:
        return False

    return isinstance(exc, psycopg.IntegrityError)
