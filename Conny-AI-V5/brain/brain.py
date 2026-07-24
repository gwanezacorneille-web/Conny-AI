from brain.responses import ResponseGenerator
from brain.conversation import Conversation
from brain.personality import Personality
from brain.reasoning import Reasoning
from brain.intent_router import IntentRouter
from memory.memory import Memory


class Brain:

    def __init__(self):

        self.response = ResponseGenerator()

        self.conversation = Conversation()

        self.personality = Personality()

        self.reasoning = Reasoning()

        self.memory = Memory()

        self.router = IntentRouter()


    def process(self, message):

        self.conversation.add(
            "User",
            message
        )


        intent = self.router.detect(message)


        # Remember information
        if intent == "remember":

            information = message.lower().replace(
                "remember",
                "",
                1
            ).strip()


            # Remember name
            if "my name is" in information:

                name = information.replace(
                    "my name is",
                    ""
                ).strip()


                self.memory.remember(
                    "personal",
                    "name",
                    name
                )


                answer = (
                    f"I will remember that your name is {name}."
                )


            else:

                self.memory.remember(
                    "fact",
                    "general",
                    information
                )


                answer = "I will remember that."


        # Favourite language
        elif intent == "favorite_language":

            language = message.lower().split(
                "is",
                1
            )[1].strip()


            self.memory.remember(
                "preference",
                "favorite_language",
                language
            )


            answer = (
                f"I will remember that your favorite language is {language}."
            )


        # Study
        elif intent == "study":

            subject = message.lower().replace(
                "i study",
                "",
                1
            ).strip()


            self.memory.remember(
                "education",
                "study",
                subject
            )


            answer = (
                f"I will remember that you study {subject}."
            )


        # Recall memory
        elif intent == "recall":

            memories = self.memory.recall()


            if memories:

                answer = "I remember:\n"

                for item in memories:

                    answer += (
                        f"- {item[1]}: {item[2]}\n"
                    )

            else:

                answer = "I don't remember anything yet."


        # Identity
        elif intent == "identity":

            answer = (
                "I am Conny AI V5.0, "
                "created by Gwaneza Corneille Karenzi."
            )


        # Greeting
        elif intent == "greeting":

            answer = self.response.greeting()


        # Unknown
        else:

            answer = self.response.unknown_response()


        self.conversation.add(
            "Conny",
            answer
        )


        return answer
