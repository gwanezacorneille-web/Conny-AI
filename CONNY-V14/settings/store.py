from pathlib import Path
from typing import Dict, Optional

from database_backend import connect, execute


class SettingsStore:

    def __init__(self, path: str = "data/settings.db"):
        self.path = Path(path)
        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        self._initialize()

    def _connect(self):
        return connect(self.path)

    def _initialize(self):
        with self._connect() as conn:
            execute(
                conn,
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
            row = execute(
                conn,
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
            "user_id": row["user_id"],
            "key": row["key"],
            "value": row["value"],
            "value_type": row["value_type"],
        }

    def list_for_user(
        self,
        user_id: str,
    ) -> Dict[str, Dict[str, str]]:
        with self._connect() as conn:
            rows = execute(
                conn,
                """
                SELECT key, value, value_type
                FROM settings
                WHERE user_id = ?
                ORDER BY key
                """,
                (user_id,),
            ).fetchall()

        return {
            row["key"]: {
                "value": row["value"],
                "value_type": row["value_type"],
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
            execute(
                conn,
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
            execute(
                conn,
                """
                DELETE FROM settings
                WHERE user_id = ? AND key = ?
                """,
                (user_id, key),
            )
            conn.commit()
