from database.database import Database


class KnowledgeFusion:
    """
    Combines built-in knowledge with learned knowledge.

    Search priority:

    1. Built-in knowledge
    2. Learned knowledge
    3. Merge both if available
    """

    def __init__(self, knowledge_engine):

        self.engine = knowledge_engine
        self.database = Database()


    def search(self, question):

        result = {

            "built_in": None,
            "learned": None,
            "best": None

        }

        # -----------------------
        # Built-in knowledge
        # -----------------------

        builtin = self.engine.find_concept(question)

        if builtin:

            result["built_in"] = builtin


        # -----------------------
        # Learned knowledge
        # -----------------------

        words = question.lower().split()

        for word in words:

            learned = self.database.search_keyword(word)

            if learned:

                result["learned"] = learned

                break


        # -----------------------
        # Choose best answer
        # -----------------------

        if builtin:

            result["best"] = "built_in"

        elif result["learned"]:

            result["best"] = "learned"

        return result
