from brain.responses import ResponseGenerator
from brain.conversation import Conversation
from brain.personality import Personality
from brain.reasoning import Reasoning
from memory.memory import Memory


class Brain:

    def __init__(self):

        self.response = ResponseGenerator()

        self.conversation = Conversation()

        self.personality = Personality()

        self.reasoning = Reasoning()

        self.memory = Memory()


    def process(self, message):

        self.conversation.add(
            "User",
            message
        )

        intent = self.reasoning.analyze(message)


        # Remember command
        if message.lower().startswith("remember"):

            information = message[8:].strip()

            self.memory.remember(information)

            answer = "I will remember that."


        # Recall memory
        elif "what do you remember" in message.lower():

            memories = self.memory.recall()

            if memories:

                answer = "I remember: "

                for item in memories:

                    answer += item[1] + ", "

            else:

                answer = "I don't remember anything yet."


        # Greeting
        elif intent == "greeting":

            answer = self.response.greeting()


        # Identity
        elif intent == "name":

            answer = (
                "I am Conny AI V5.0, "
                "created by Gwaneza Corneille Karenzi."
            )


        # Unknown
        else:

            answer = self.response.unknown_response()


        self.conversation.add(
            "Conny",
            answer
        )


        return answer
