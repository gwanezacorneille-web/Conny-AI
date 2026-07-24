from brain.responses import ResponseGenerator
from brain.conversation import Conversation
from brain.personality import Personality
from brain.reasoning import Reasoning
from brain.intent_router import IntentRouter

from memory.memory import Memory

from plugins.plugin_manager import PluginManager
from plugins.plugin_loader import PluginLoader



class Brain:


    def __init__(self):

        self.response = ResponseGenerator()

        self.conversation = Conversation()

        self.personality = Personality()

        self.reasoning = Reasoning()

        self.memory = Memory()

        self.router = IntentRouter()


        # Plugin System

        self.plugins = PluginManager()

        self.loader = PluginLoader()


        loaded_plugins = self.loader.load_plugins()


        for plugin in loaded_plugins:

            self.plugins.register(
                plugin
            )



    def process(self, message):


        self.conversation.add(
            "User",
            message
        )


        # Check plugins first

        plugin = self.plugins.find_plugin(
            message
        )


        if plugin:


            answer = plugin.run(
                message
            )


            self.conversation.add(
                "Conny",
                answer
            )


            return answer



        intent = self.router.detect(
            message
        )



        if intent == "remember":


            information = message.lower().replace(
                "remember",
                "",
                1
            ).strip()


            self.memory.remember(
                "fact",
                "general",
                information
            )


            answer = "I will remember that."



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
                f"I will remember that your "
                f"favorite language is {language}."
            )



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



        elif intent == "recall":


            memories = self.memory.recall()


            answer = "I remember:\n"


            for item in memories:

                answer += (
                    f"- {item[1]}: {item[2]}\n"
                )



        elif intent == "identity":


            answer = (
                "I am Conny AI V5.0, "
                "created by Gwaneza Corneille Karenzi."
            )



        elif intent == "greeting":


            answer = self.response.greeting()



        else:


            answer = self.response.unknown_response()



        self.conversation.add(
            "Conny",
            answer
        )


        return answer
