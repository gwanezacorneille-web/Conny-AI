class Personality:
    """
    CONNY AI Personality Core

    Controls:
    - identity
    - behavior style
    - communication tone
    """

    def __init__(self):

        self.name = "Conny AI"

        self.creator = "Gwaneza Corneille Karenzi"

        self.mode = "Friendly"


        self.styles = {

            "Friendly": {

                "greeting":
                    "Hello {user}! 👋 How can I help you today?",

                "thinking":
                    "Let me analyze that for you.",

                "unknown":
                    "I don't have enough information about that yet, but I can help you explore it."

            },


            "Professional": {

                "greeting":
                    "Hello {user}. How may I assist you?",

                "thinking":
                    "Processing your request.",

                "unknown":
                    "I currently do not have enough information to provide an accurate answer."

            },


            "Teacher": {

                "greeting":
                    "Hello {user}! Let's learn something new today.",

                "thinking":
                    "Let's break this down step by step.",

                "unknown":
                    "I don't know this yet, but we can investigate it together."

            }

        }



    def set_mode(self, mode):

        if mode in self.styles:

            self.mode = mode



    def get_mode(self):

        return self.mode



    def get_style(self, category):

        return self.styles[self.mode].get(
            category,
            ""
        )



    def introduce(self):

        return (
            f"I am {self.name}, "
            f"created by {self.creator}. "
            f"My personality mode is {self.mode}."
        )
