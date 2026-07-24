class Conversation:
    """
    Handles current conversation history.
    """

    def __init__(self):

        self.history = []


    def add(self, speaker, message):

        self.history.append(
            {
                "speaker": speaker,
                "message": message
            }
        )


    def get_history(self):

        return self.history


    def last_message(self):

        if self.history:
            return self.history[-1]

        return None


    def clear(self):

        self.history = []
