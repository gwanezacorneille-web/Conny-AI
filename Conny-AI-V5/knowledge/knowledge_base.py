import json
import os


class KnowledgeBase:


    def __init__(self):

        self.file = os.path.join(
            os.path.dirname(__file__),
            "concepts.json"
        )

        self.data = self.load()



    def load(self):

        try:

            with open(
                self.file,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)


        except Exception:

            return {}



    def search(self, question):

        question = question.lower()


        for key, value in self.data.items():

            if key in question:

                return value["description"]


        return None
