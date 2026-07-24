class Reasoning:


    def analyze(self, text):

        text = text.lower()


        if any(
            word in text
            for word in [
                "hello",
                "hi",
                "hey"
            ]
        ):
            return "greeting"


        if "your name" in text or "who are you" in text:

            return "name"


        return "unknown"
