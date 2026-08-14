from brain.responses import ResponseGenerator
from brain.emotion_engine import EmotionEngine
from brain.conversation import Conversation
from brain.personality import Personality
from brain.reasoning import Reasoning
from brain.intent_engine import IntentEngine
from brain.decision_engine import DecisionEngine
from brain.language.language_engine import LanguageEngine
from brain.router import Router

from knowledge.knowledge_engine import KnowledgeEngine
from memory.memory import Memory

from plugins.plugin_manager import PluginManager
from plugins.plugin_loader import PluginLoader

from learning.learning_engine import LearningEngine


class Brain:
    """
    CONNY AI Brain V6

    Main intelligence coordinator.

    Pipeline:

        User Input
            ↓
        Language Understanding
            ↓
        Context
            ↓
        Intent Detection
            ↓
        Emotion Detection
            ↓
        Decision Engine
            ↓
        Router
            ↓
        Intelligence Module
            ↓
        Response
            ↓
        Conversation Memory
    """

    def __init__(self):

        # ==================================================
        # CORE SYSTEMS
        # ==================================================

        self.response = ResponseGenerator()
        self.conversation = Conversation()
        self.personality = Personality()
        self.reasoning = Reasoning()
        self.memory = Memory()

        # ==================================================
        # EMOTION
        # ==================================================

        self.emotion = EmotionEngine()

        # ==================================================
        # LEARNING
        # ==================================================

        self.learning = LearningEngine()

        # ==================================================
        # LANGUAGE
        # ==================================================

        self.language = LanguageEngine()

        # ==================================================
        # INTELLIGENCE / INTENT
        # ==================================================

        self.intent_engine = IntentEngine()
        self.decision = DecisionEngine()

        # ==================================================
        # KNOWLEDGE
        # ==================================================

        self.knowledge = KnowledgeEngine()

        # ==================================================
        # PLUGINS
        # ==================================================

        self.plugins = PluginManager()
        self.loader = PluginLoader()

        try:
            for plugin in self.loader.load_plugins():
                self.plugins.register(plugin)
        except Exception as error:
            print("DEBUG Plugin Loading Error:", error)

        # ==================================================
        # REQUEST ROUTER
        # ==================================================

        self.request_router = Router(self)

        # ==================================================
        # BRAIN STATE
        # ==================================================

        self.last_message = ""
        self.last_intent = None
        self.last_emotion = None
        self.last_decision = None
        self.last_answer = ""

        self.running = True

    # ======================================================
    # MAIN PROCESS
    # ======================================================

    def process(self, message):

        try:

            # ----------------------------------------------
            # Validate input
            # ----------------------------------------------

            if message is None:
                return "I didn't receive a message."

            text = str(message).strip()

            if not text:
                return "Please tell me something."

            lower = text.lower()

            self.last_message = text

            # ----------------------------------------------
            # Learning mode
            # ----------------------------------------------

            if self._is_learning_command(lower):

                parts = text.split(" ", 1)

                if len(parts) < 2:
                    return "What would you like me to learn?"

                subject = parts[1].strip()

                result = self.learning.start_learning(subject)

                self.last_answer = result

                return result

            # ----------------------------------------------
            # Continue active learning session
            # ----------------------------------------------

            try:

                if self.learning.teacher.session.active:

                    result = self.learning.process_input(text)

                    if result is None:
                        return "Lesson received..."

                    if result.get("type") == "lesson_complete":

                        knowledge = result["knowledge"]

                        answer = (
                            "\n"
                            "==============================\n"
                            "Learning Complete\n"
                            "==============================\n\n"
                            f"Topic:\n{knowledge.topic}\n\n"
                            f"Facts found:\n{len(knowledge.facts)}\n\n"
                            f"Keywords found:\n{len(knowledge.keywords)}\n\n"
                            "Knowledge extracted successfully.\n"
                            "Ready for storage."
                        )

                        self.last_answer = answer

                        return answer

                    return "Lesson received..."

            except Exception as error:

                print("DEBUG Learning Error:", error)

            # ----------------------------------------------
            # Conversation history
            # ----------------------------------------------

            self.conversation.add("User", text)

            # ----------------------------------------------
            # Language understanding
            # ----------------------------------------------

            language = self.language.understand(text)

            corrected = language.get("corrected", text)

            if not corrected:
                corrected = text

            # ----------------------------------------------
            # Intent detection
            # ----------------------------------------------

            try:
                intent = self.intent_engine.detect(corrected)
            except Exception as error:

                print("DEBUG Intent Engine Error:", error)

                intent = None

            # ----------------------------------------------
            # Emotion detection
            # ----------------------------------------------

            try:
                emotion = self.emotion.detect(corrected)
            except Exception as error:

                print("DEBUG Emotion Engine Error:", error)

                emotion = None

            # ----------------------------------------------
            # Decision
            # ----------------------------------------------

            try:
                decision = self.decision.choose(
                    corrected,
                    intent
                )
            except Exception as error:

                print("DEBUG Decision Engine Error:", error)

                decision = "knowledge"

            # ----------------------------------------------
            # Debug
            # ----------------------------------------------

            print("DEBUG Message:", corrected)
            print("DEBUG Intent:", intent)
            print("DEBUG Emotion:", emotion)
            print("DEBUG Decision:", decision)

            self.last_intent = intent
            self.last_emotion = emotion
            self.last_decision = decision

            # ----------------------------------------------
            # Route request
            # ----------------------------------------------

            answer = self.request_router.route(
                corrected,
                emotion=emotion,
                intent=intent,
                decision=decision
            )

            # ----------------------------------------------
            # Safety fallback
            # ----------------------------------------------

            if answer is None:
                answer = self.response.unknown_response()

            if not isinstance(answer, str):
                answer = str(answer)

            # ----------------------------------------------
            # Store response
            # ----------------------------------------------

            self.conversation.add("Conny", answer)

            self.last_answer = answer

            return answer

        except Exception as error:

            print("DEBUG BRAIN ERROR:", error)

            answer = (
                "I encountered a problem while processing that. "
                "Please try again."
            )

            try:
                self.conversation.add("Conny", answer)
            except Exception:
                pass

            return answer

    # ======================================================
    # LEARNING COMMAND DETECTION
    # ======================================================

    def _is_learning_command(self, text):

        commands = (
            "study ",
            "teach ",
            "learn "
        )

        return text.startswith(commands)

    # ======================================================
    # BRAIN STATUS
    # ======================================================

    def status(self):

        return {
            "running": self.running,
            "last_message": self.last_message,
            "last_intent": self.last_intent,
            "last_emotion": self.last_emotion,
            "last_decision": self.last_decision,
            "last_answer": self.last_answer
        }

    # ======================================================
    # RESET
    # ======================================================

    def reset_state(self):

        self.last_message = ""
        self.last_intent = None
        self.last_emotion = None
        self.last_decision = None
        self.last_answer = ""

        print("CONNY Brain state reset.")

    # ======================================================
    # SHUTDOWN
    # ======================================================

    def shutdown(self):

        self.running = False

        print("CONNY Brain shutting down.")
