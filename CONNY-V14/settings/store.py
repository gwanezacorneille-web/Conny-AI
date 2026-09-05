import sqlite3
from pathlib import Path
from typing import Any, Dict, Optional


class SettingsStore:

    def __init__(self, path: str = "data/settings.db"):
        self.path = Path(path)
        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        self._initialize()

    def _connect(self):
        return sqlite3.connect(self.path)

    def _initialize(self):
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS settings (
                    user_id TEXT NOT NULL,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL,
                    value_type TEXT NOT NULL,
                    PRIMARY KEY (user_id, key)
                )
                """
            )
            conn.commit()

    def get(
        self,
        user_id: str,
        key: str,
    ) -> Optional[Dict[str, str]]:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT user_id, key, value, value_type
                FROM settings
                WHERE user_id = ? AND key = ?
                """,
                (user_id, key),
            ).fetchone()

        if row is None:
            return None

        return {
            "user_id": row[0],
            "key": row[1],
            "value": row[2],
            "value_type": row[3],
        }

    def list_for_user(
        self,
        user_id: str,
    ) -> Dict[str, Dict[str, str]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT key, value, value_type
                FROM settings
                WHERE user_id = ?
                ORDER BY key
                """,
                (user_id,),
            ).fetchall()

        return {
            row[0]: {
                "value": row[1],
                "value_type": row[2],
            }
            for row in rows
        }

    def set(
        self,
        user_id: str,
        key: str,
        value: str,
        value_type: str,
    ):
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO settings
                    (user_id, key, value, value_type)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(user_id, key)
                DO UPDATE SET
                    value = excluded.value,
                    value_type = excluded.value_type
                """,
                (
                    user_id,
                    key,
                    value,
                    value_type,
                ),
            )
            conn.commit()

    def delete(
        self,
        user_id: str,
        key: str,
    ):
        with self._connect() as conn:
            conn.execute(
                """
                DELETE FROM settings
                WHERE user_id = ? AND key = ?
                """,
                (user_id, key),
            )
            conn.commit()
