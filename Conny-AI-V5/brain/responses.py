import random


class ResponseGenerator:
    """Handles Conny's basic responses."""

    def __init__(self):

        self.greetings = [
            "Hello!",
            "Hi there!",
            "Hey! Nice to meet you.",
            "Welcome back!",
            "Good to see you!"
        ]

        self.unknown = [
            "I am still learning that.",
            "I don't have an answer yet.",
            "Can you explain that another way?",
            "That is interesting. I will learn more about it."
        ]


    def greeting(self):

        return random.choice(self.greetings)


    def unknown_response(self):

        return random.choice(self.unknown)
