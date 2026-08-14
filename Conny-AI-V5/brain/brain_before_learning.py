from brain.responses import ResponseGenerator
from brain.conversation import Conversation
from brain.personality import Personality
from brain.reasoning import Reasoning
from brain.intent_router import IntentRouter
from brain.intent_engine import IntentEngine
from brain.decision_engine import DecisionEngine

from brain.language.language_engine import LanguageEngine
from brain.router import Router

from knowledge.knowledge_engine import KnowledgeEngine
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


        # Language intelligence

        self.language = LanguageEngine()


        # Knowledge intelligence

        self.knowledge = KnowledgeEngine()


        # Question understanding

        self.intent_engine = IntentEngine()


        # Decision engine

        self.decision = DecisionEngine()


        # Plugin system

        self.plugins = PluginManager()

        self.loader = PluginLoader()


        for plugin in self.loader.load_plugins():

            self.plugins.register(plugin)


        # Main router

        self.request_router = Router(self)


    def process(self, message):


        self.conversation.add(
            "User",
            message
        )


        # Correct spelling and understand text

        language = self.language.understand(
            message
        )


        corrected = language["corrected"]


        # Detect question purpose

        intent = self.intent_engine.detect(
            corrected
        )


        print(
            "DEBUG Intent:",
            intent
        )


        answer = self.request_router.route(
            corrected
        )


        self.conversation.add(
            "Conny",
            answer
        )


        return answer
