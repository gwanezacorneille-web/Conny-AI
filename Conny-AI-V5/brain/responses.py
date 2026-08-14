import random


class ResponseGenerator:
    """
    CONNY AI Response Engine V3

    Generates natural responses using
    personality and context.
    """


    def __init__(self, personality=None):

        self.personality = personality

        self.last_response = None


        self.user_name = "Corneille"


        self.responses = {


            "greeting": [

                "Hello {user}! 👋 How can I help you today?",

                "Hi {user}! CONNY AI is ready.",

                "Welcome back {user}. What are we working on?"

            ],


            "thanks": [

                "You're welcome {user}.",

                "Glad I could help!",

                "Anytime. I'm here when you need me."

            ],


            "goodbye": [

                "Goodbye {user}. See you soon!",

                "See you next time. CONNY AI will be ready.",

                "Take care {user}."

            ],


            "unknown": [

                "I don't have enough information about that yet.",

                "I am still learning about this topic.",

                "I couldn't find a confident answer, but I can help you investigate.",

                "I don't know that yet. Would you like to teach me?"

            ],


            "error": [

                "Something went wrong while processing that.",

                "I had trouble understanding that request.",

                "Could you try explaining it another way?"

            ]

        }



    def _select(self, category):

        choices = self.responses.get(
            category,
            self.responses["unknown"]
        )


        answer = random.choice(
            choices
        )


        while answer == self.last_response:

            answer = random.choice(
                choices
            )


        self.last_response = answer


        return answer.format(
            user=self.user_name
        )



    def greeting(self):

        return self._select(
            "greeting"
        )



    def thanks_response(self):

        return self._select(
            "thanks"
        )



    def goodbye(self):

        return self._select(
            "goodbye"
        )



    def unknown_response(self):

        return self._select(
            "unknown"
        )



    def error_response(self):

        return self._select(
            "error"
        )



    def set_user(self, name):

        self.user_name = name
