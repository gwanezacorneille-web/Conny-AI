class DecisionEngine:
    """
    CONNY AI Decision Engine V5

    Decides which intelligence module should handle
    the user's request.

    Priority:
        1. Explicit commands
        2. Memory
        3. Comparison
        4. Calculator
        5. Internet
        6. System
        7. Coding
        8. Creative
        9. Emotional support
        10. Knowledge
        11. Conversation
    """

    def __init__(self):

        self.intents = {

            # ==========================================
            # CONVERSATION
            # ==========================================

            "conversation": [
                "hi",
                "hello",
                "hey",
                "how are you",
                "who are you",
                "your name",
                "thank you",
                "thanks",
                "bye",
                "good morning",
                "good afternoon",
                "good evening",
                "good night"
            ],

            # ==========================================
            # EMOTIONAL SUPPORT
            # ==========================================

            "emotional_support": [
                "happy",
                "sad",
                "angry",
                "worried",
                "scared",
                "afraid",
                "stress",
                "stressed",
                "exam",
                "tired",
                "lonely",
                "excited",
                "love",
                "frustrated",
                "nervous"
            ],

            # ==========================================
            # MEMORY STORE
            # ==========================================

            "memory_store": [
                "remember",
                "save this",
                "store this",
                "my favorite",
                "my name is",
                "i like",
                "i love",
                "don't forget"
            ],

            # ==========================================
            # MEMORY RECALL
            # ==========================================

            "memory_recall": [
                "what do you remember",
                "show memories",
                "what do you know about me",
                "tell me about myself",
                "what did i tell you",
                "do you remember"
            ],

            # ==========================================
            # CALCULATOR
            # ==========================================

            "calculator": [
                "calculate",
                "solve",
                "plus",
                "minus",
                "multiply",
                "divide",
                "equation",
                "percentage",
                "percent",
                "square root"
            ],

            # ==========================================
            # COMPARISON
            # ==========================================

            "comparison": [
                "compare",
                "difference between",
                " vs ",
                "versus",
                "better than",
                "which is better",
                "difference"
            ],

            # ==========================================
            # CODING
            # ==========================================

            "coding": [
                "python",
                "java",
                "javascript",
                "html",
                "css",
                "code",
                "program",
                "programming",
                "bug",
                "error",
                "function",
                "class",
                "script",
                "debug",
                "syntax"
            ],

            # ==========================================
            # CREATIVE
            # ==========================================

            "creative": [
                "write",
                "create",
                "story",
                "poem",
                "design",
                "idea",
                "generate",
                "caption",
                "message",
                "letter"
            ],

            # ==========================================
            # SYSTEM
            # ==========================================

            "system": [
                "open",
                "launch",
                "install",
                "remove",
                "run",
                "terminal",
                "command",
                "shutdown",
                "restart",
                "file",
                "folder"
            ],

            # ==========================================
            # INTERNET
            # ==========================================

            "internet": [
                "search",
                "search online",
                "look up",
                "look online",
                "find online",
                "online",
                "internet",
                "latest",
                "today",
                "current",
                "news",
                "weather",
                "price",
                "score",
                "live"
            ],

            # ==========================================
            # KNOWLEDGE
            # ==========================================

            "knowledge": [
                "what is",
                "what are",
                "who is",
                "why",
                "how",
                "explain",
                "define",
                "meaning",
                "tell me about",
                "what does",
                "how does"
            ]
        }

        # Higher number = stronger priority
        self.priority = {

            "memory_store": 100,
            "memory_recall": 95,
            "comparison": 90,
            "calculator": 85,
            "internet": 80,
            "system": 75,
            "coding": 70,
            "creative": 65,
            "emotional_support": 60,
            "knowledge": 50,
            "conversation": 40
        }

        # IntentEngine intents handled by KnowledgeEngine
        self.knowledge_intents = {
            "definition",
            "explanation",
            "reason",
            "process",
            "examples",
            "functions"
        }

        self.last_scores = {}
        self.last_decision = None
        self.last_confidence = 0

    # ==================================================
    # CHOOSE DECISION
    # ==================================================

    def choose(self, message, intent=None):

        text = str(message).lower().strip()

        # ----------------------------------------------
        # Empty message
        # ----------------------------------------------

        if not text:

            return self._set_result(
                "conversation",
                1.0
            )

        # ----------------------------------------------
        # Explicit conversation commands
        # ----------------------------------------------

        if text in (
            "hi",
            "hello",
            "hey",
            "thanks",
            "thank you",
            "bye",
            "good morning",
            "good afternoon",
            "good evening",
            "good night"
        ):

            return self._set_result(
                "conversation",
                1.0
            )

        # ----------------------------------------------
        # MEMORY STORE
        # ----------------------------------------------

        if text.startswith((
            "remember ",
            "save ",
            "store ",
            "don't forget "
        )):

            return self._set_result(
                "memory_store",
                1.0
            )

        # ----------------------------------------------
        # MEMORY RECALL
        # ----------------------------------------------

        if (
            "what do you remember" in text
            or "show memories" in text
            or "what did i tell you" in text
            or "do you remember" in text
            or "what do you know about me" in text
        ):

            return self._set_result(
                "memory_recall",
                1.0
            )

        # ----------------------------------------------
        # COMPARISON
        # ----------------------------------------------

        if (
            " vs " in text
            or " versus " in text
            or text.startswith("compare")
            or "difference between" in text
        ):

            return self._set_result(
                "comparison",
                1.0
            )

        # ----------------------------------------------
        # EXPLICIT INTERNET COMMANDS
        #
        # These MUST override topic words.
        #
        # Example:
        # "search Python programming"
        #
        # Python/programming = coding
        # search = internet
        #
        # The explicit command wins.
        # ----------------------------------------------

        explicit_online = (

            text.startswith("search ")
            or text.startswith("search online ")
            or text.startswith("look up ")
            or text.startswith("look online ")
            or text.startswith("find online ")
        )

        if explicit_online:

            return self._set_result(
                "internet",
                1.0
            )

        # ----------------------------------------------
        # EXPLICIT NEWS
        # ----------------------------------------------

        if (
            "latest news" in text
            or "latest news about" in text
            or "news about" in text
            or text.startswith("news ")
        ):

            return self._set_result(
                "internet",
                1.0
            )

        # ----------------------------------------------
        # EXPLICIT WEATHER
        # ----------------------------------------------

        if (
            text.startswith("weather")
            or "weather today" in text
            or "weather in " in text
        ):

            return self._set_result(
                "internet",
                1.0
            )

        # ----------------------------------------------
        # EXPLICIT CURRENT / LIVE REQUEST
        # ----------------------------------------------

        if (
            text.startswith("latest ")
            or text.startswith("current ")
            or text.startswith("today ")
            or "right now" in text
            or "live " in text
        ):

            return self._set_result(
                "internet",
                1.0
            )

        # ----------------------------------------------
        # EXPLICIT WIKIPEDIA
        #
        # These MUST override coding/knowledge keywords.
        #
        # Example:
        # "wikipedia Python programming language"
        #
        # Python/programming = coding
        # wikipedia = internet
        #
        # The explicit command wins.
        # ----------------------------------------------

        if (
            text.startswith("wikipedia ")
            or text.startswith("wiki ")
            or text == "wikipedia"
            or text == "wiki"
        ):

            return self._set_result(
                "internet",
                1.0
            )

        # ----------------------------------------------
        # KNOWLEDGE INTENTS
        #
        # IntentEngine has already understood the
        # question, so knowledge questions should not
        # be hijacked by topic words.
        # ----------------------------------------------

        if intent in self.knowledge_intents:

            return self._set_result(
                "knowledge",
                0.9
            )

        # ----------------------------------------------
        # CALCULATOR
        # ----------------------------------------------

        if (
            text.startswith("calculate ")
            or text.startswith("solve ")
        ):

            return self._set_result(
                "calculator",
                1.0
            )

        # ----------------------------------------------
        # CALCULATE SCORES
        # ----------------------------------------------

        scores = {}

        for name, keywords in self.intents.items():

            score = 0

            for keyword in keywords:

                if keyword in text:
                    score += 1

            scores[name] = score

        self.last_scores = scores

        # ----------------------------------------------
        # NO MATCH
        # ----------------------------------------------

        best_score = max(
            scores.values()
        )

        if best_score == 0:

            return self._set_result(
                "knowledge",
                0.0
            )

        # ----------------------------------------------
        # STRONGEST MATCHES
        # ----------------------------------------------

        candidates = [
            name
            for name, score in scores.items()
            if score == best_score
        ]

        # ----------------------------------------------
        # PRIORITY TIE BREAKER
        # ----------------------------------------------

        best = max(
            candidates,
            key=lambda name:
                self.priority.get(
                    name,
                    0
                )
        )

        # ----------------------------------------------
        # CONFIDENCE
        # ----------------------------------------------

        confidence = min(
            best_score / 3,
            1.0
        )

        return self._set_result(
            best,
            confidence
        )

    # ==================================================
    # SET RESULT
    # ==================================================

    def _set_result(
        self,
        decision,
        confidence
    ):

        self.last_decision = decision
        self.last_confidence = confidence

        print(
            "DEBUG Decision:",
            decision
        )

        print(
            "DEBUG Confidence:",
            confidence
        )

        if self.last_scores:

            print(
                "DEBUG Intent Scores:",
                self.last_scores
            )

        return decision

    # ==================================================
    # GET LAST DECISION
    # ==================================================

    def get_last_decision(self):

        return {
            "decision":
                self.last_decision,

            "confidence":
                self.last_confidence,

            "scores":
                self.last_scores
        }

    # ==================================================
    # GET SCORES
    # ==================================================

    def get_scores(self):

        return self.last_scores
