class IntentRouter:
    """
    Decides what Conny should do
    based on the user's message.
    """


    def detect(self, message):

        text = message.lower()


        # Greetings
        if any(word in text for word in [
            "hello",
            "hi",
            "hey"
        ]):

            return "greeting"



        # Identity
        if (
            "who are you" in text
            or "your name" in text
        ):

            return "identity"



        # Memory
        if text.startswith("remember"):

            return "remember"



        if (
            "what do you remember" in text
            or "what do you know about me" in text
        ):

            return "recall"



        # Personal information

        if "my favourite language is" in text:

            return "favorite_language"



        if text.startswith("i study"):

            return "study"



        return "unknown"
