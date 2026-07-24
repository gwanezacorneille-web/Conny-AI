import sqlite3


DATABASE = "database/conny.db"


class Database:

    def __init__(self):

        self.connection = sqlite3.connect(DATABASE)

        self.create_tables()


    def create_tables(self):

        cursor = self.connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            category TEXT,

            information TEXT

        )
        """)

        self.connection.commit()


    def save_memory(self, category, information):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO memories
            (category, information)

            VALUES (?, ?)
            """,
            (category, information)
        )

        self.connection.commit()


    def get_memories(self):

        cursor = self.connection.cursor()

        cursor.execute(
            "SELECT category, information FROM memories"
        )

        return cursor.fetchall()
