import sqlite3


DATABASE = "database/conny.db"


class Database:

    def __init__(self):

        self.connection = sqlite3.connect(DATABASE)

        self.create_tables()


    # =====================================
    # Create Tables
    # =====================================

    def create_tables(self):

        cursor = self.connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            category TEXT,

            key TEXT UNIQUE,

            value TEXT
        )
        """)

        self.connection.commit()


    # =====================================
    # Save / Update Memory
    # =====================================

    def save_memory(self, category, key, value):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO memories(category, key, value)

            VALUES(?, ?, ?)

            ON CONFLICT(key)

            DO UPDATE SET

                value=excluded.value,
                category=excluded.category
            """,
            (
                category,
                key,
                value
            )
        )

        self.connection.commit()


    # =====================================
    # Get All Memories
    # =====================================

    def get_memories(self):

        cursor = self.connection.cursor()

        cursor.execute("""
        SELECT id, category, key, value

        FROM memories

        ORDER BY id
        """)

        return cursor.fetchall()


    # =====================================
    # Search Memory
    # =====================================

    def find_memory(self, key):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT id, category, key, value

            FROM memories

            WHERE key=?
            """,
            (key,)
        )

        return cursor.fetchone()


    # =====================================
    # Delete Memory
    # =====================================

    def delete_memory(self, key):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            DELETE FROM memories

            WHERE key=?
            """,
            (key,)
        )

        self.connection.commit()


    # =====================================
    # Count Memories
    # =====================================

    def count(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)

            FROM memories
            """
        )

        return cursor.fetchone()[0]
