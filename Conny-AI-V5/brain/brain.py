from brain.responses import ResponseGenerator
from brain.emotion_engine import EmotionEngine
from brain.conversation import Conversation
from brain.personality import Personality
from brain.reasoning import Reasoning
from brain.intent_engine import IntentEngine
from brain.decision_engine import DecisionEngine
from brain.language.language_engine import LanguageEngine
from brain.router import Router
from brain.context_engine import ContextEngine
from brain.coding_engine import CodingEngine

from knowledge.knowledge_engine import KnowledgeEngine
from memory.memory import Memory

from plugins.plugin_manager import PluginManager
from plugins.plugin_loader import PluginLoader

from learning.learning_engine import LearningEngine

from internet.online_body import OnlineBody

class Brain:
    """
    CONNY AI Brain V6

    Main intelligence coordinator.

    Pipeline:

        User Input
            ↓
        Language Understanding
            ↓
        Intent Detection
            ↓
        Emotion Detection
            ↓
        Decision Engine
            ↓
        Request Router
            ↓
        Offline / Online Intelligence
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
        # V9 CONTEXT
        # ==================================================

        self.context = ContextEngine()

        # ==================================================
        # CODING
        # ==================================================

        self.coding = CodingEngine(self)

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
        # ONLINE BODY
        # ==================================================

        self.online = OnlineBody()

        # ==================================================
        # PLUGINS
        # ==================================================

        self.plugins = PluginManager()
        self.loader = PluginLoader()

        try:

            for plugin in self.loader.load_plugins():

                self.plugins.register(plugin)

        except Exception as error:

            print(
                "DEBUG Plugin Loading Error:",
                error
            )

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
        self.last_topic = None

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

                return (
                    "I didn't receive a message."
                )

            text = str(message).strip()

            if not text:

                return (
                    "Please tell me something."
                )

            lower = text.lower()

            self.last_message = text

            # ----------------------------------------------
            # V9 CONTEXT FOLLOW-UP
            # ----------------------------------------------

            original_text = text
            self.last_followup = False

            if not hasattr(
                self,
                "followup_depth"
            ):
                self.followup_depth = 0

            try:

                text = self.context.resolve_followup(
                    text
                )

                lower = text.lower()

            except Exception as error:

                print(
                    "DEBUG V9 Follow-up Error:",
                    error
                )

            self.last_followup = (
                text != original_text
            )

            if self.last_followup:

                self.followup_depth += 1

            else:

                self.followup_depth = 0

            # ----------------------------------------------
            # Learning mode
            # ----------------------------------------------

            if self._is_learning_command(lower):

                parts = text.split(
                    " ",
                    1
                )

                if len(parts) < 2:

                    return (
                        "What would you like me to learn?"
                    )

                subject = parts[1].strip()

                result = self.learning.start_learning(
                    subject
                )

                self.last_answer = result

                return result

            # ----------------------------------------------
            # Continue active learning session
            # ----------------------------------------------

            try:

                if self.learning.teacher.session.active:

                    result = self.learning.process_input(
                        text
                    )

                    if result is None:

                        return (
                            "Lesson received..."
                        )

                    if result.get("type") == "lesson_complete":

                        knowledge = result["knowledge"]

                        answer = (
                            "\n"
                            "==============================\n"
                            "Learning Complete\n"
                            "==============================\n\n"
                            f"Topic:\n{knowledge.topic}\n\n"
                            f"Facts found:\n"
                            f"{len(knowledge.facts)}\n\n"
                            f"Keywords found:\n"
                            f"{len(knowledge.keywords)}\n\n"
                            "Knowledge extracted successfully.\n"
                            "Ready for storage."
                        )

                        self.last_answer = answer

                        return answer

                    return (
                        "Lesson received..."
                    )

            except Exception as error:

                print(
                    "DEBUG Learning Error:",
                    error
                )

            # ----------------------------------------------
            # Conversation history
            # ----------------------------------------------

            self.conversation.add(
                "User",
                text
            )

            # ----------------------------------------------
            # Language understanding
            # ----------------------------------------------

            language = self.language.understand(
                text
            )

            corrected = language.get(
                "corrected",
                text
            )

            if not corrected:

                corrected = text

            # ----------------------------------------------
            # Intent detection
            # ----------------------------------------------

            try:

                intent = self.intent_engine.detect(
                    corrected
                )

            except Exception as error:

                print(
                    "DEBUG Intent Engine Error:",
                    error
                )

                intent = None

            # ----------------------------------------------
            # Emotion detection
            # ----------------------------------------------

            try:

                emotion = self.emotion.detect(
                    corrected
                )

            except Exception as error:

                print(
                    "DEBUG Emotion Engine Error:",
                    error
                )

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

                print(
                    "DEBUG Decision Engine Error:",
                    error
                )

                decision = "knowledge"

            # ----------------------------------------------
            # V9 FOLLOW-UP DECISION OVERRIDE
            # ----------------------------------------------

            if text != original_text:

                decision = "knowledge"

                print(
                    "DEBUG V9 Follow-up Decision Override:",
                    decision
                )

            # ----------------------------------------------
            # Debug
            # ----------------------------------------------

            print(
                "DEBUG Message:",
                corrected
            )

            print(
                "DEBUG Intent:",
                intent
            )

            print(
                "DEBUG Emotion:",
                emotion
            )

            print(
                "DEBUG Decision:",
                decision
            )

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

                answer = (
                    self.response.unknown_response()
                )

            if not isinstance(answer, str):

                answer = str(answer)

            # ----------------------------------------------
            # Store response
            # ----------------------------------------------

            self.conversation.add(
                "Conny",
                answer
            )

            self.last_answer = answer

            # ----------------------------------------------
            # V9 CONTEXT
            # ----------------------------------------------

            try:

                self.context.add_turn(
                    user_message=original_text,
                    response=answer,
                    intent=intent,
                    decision=decision,
                    topic=self.last_topic,
                    resolved_message=corrected
                )

                print(
                    "DEBUG V9 Context:",
                    self.context.status()
                )

            except Exception as error:

                print(
                    "DEBUG V9 Context Error:",
                    error
                )

            return answer

        except Exception as error:

            print(
                "DEBUG BRAIN ERROR:",
                error
            )

            answer = (
                "I encountered a problem while "
                "processing that. Please try again."
            )

            try:

                self.conversation.add(
                    "Conny",
                    answer
                )

            except Exception:
                pass

            return answer

    # ======================================================
    # LEARNING COMMAND DETECTION
    # ======================================================

    def _is_learning_command(self, text):

        commands = (
            "learn ",
            "teach ",
            "learn about ",
            "teach me about "
        )

        return text.startswith(commands)
