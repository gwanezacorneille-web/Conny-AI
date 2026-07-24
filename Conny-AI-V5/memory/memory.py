from database.database import Database


class Memory:
    """
    Handles Conny's long-term memory.
    """

    def __init__(self):

        self.database = Database()


    def remember(self, information):

        self.database.save_memory(
            "fact",
            information
        )


    def recall(self):

        return self.database.get_memories()
