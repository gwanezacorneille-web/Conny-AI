from brain.responses import ResponseGenerator
from brain.conversation import Conversation
from brain.personality import Personality
from brain.reasoning import Reasoning


class Brain:

    def __init__(self):

        self.response = ResponseGenerator()

        self.memory = Conversation()

        self.personality = Personality()

        self.reasoning = Reasoning()


    def process(self, message):

        self.memory.add(
            "User",
            message
        )

        intent = self.reasoning.analyze(message)


        if intent == "greeting":

            answer = self.response.greeting()


        elif intent == "name":

            answer = (
                "I am Conny AI V5.0, "
                "created by Gwaneza Corneille Karenzi."
            )


        else:

            answer = self.response.unknown_response()


        self.memory.add(
            "Conny",
            answer
        )


        return answer
