class Reasoning:


    def analyze(self, text):

        text = text.lower()


        if any(word in text for word in [
            "hello",
            "hi",
            "hey"
        ]):

            return "greeting"



        if "who are you" in text or "your name" in text:

            return "name"



        if "my favourite language is" in text:

            return "favorite_language"



        if "i study" in text:

            return "study"



        return "unknown"
