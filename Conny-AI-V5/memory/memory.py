from database.database import Database


class Memory:


    def __init__(self):

        self.database = Database()



    def remember(self, category, key, value):

        self.database.save_memory(
            category,
            key,
            value
        )



    def recall(self):

        return self.database.get_memories()
