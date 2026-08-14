from database.database import Database


class Memory:
    """
    CONNY AI Memory System

    Handles:
    - storing memories
    - recalling memories
    - displaying memories
    """

    def __init__(self):

        self.database = Database()



    # =====================================
    # Store Memory
    # =====================================

    def remember(self, category, key, value):

        self.database.save_memory(
            category,
            key,
            value
        )


        return (
            f"I will remember that your {key} is {value}."
        )



    # =====================================
    # Recall Memory
    # =====================================

    def recall(self):

        memories = self.database.get_memories()


        return memories



    # =====================================
    # Display Memory
    # =====================================

    def show(self):

        memories = self.recall()


        if not memories:

            return (
                "I don't remember anything yet."
            )


        response = (
            "Here is what I remember:\n\n"
        )


        for memory in memories:

            category = memory[1]

            key = memory[2]

            value = memory[3]


            response += (
                f"- {key}: {value} "
                f"({category})\n"
            )


        return response
