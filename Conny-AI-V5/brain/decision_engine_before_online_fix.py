class DecisionEngine:
    """
    CONNY AI Decision Engine V4

    Combines:
    - IntentEngine result
    - keyword scoring
    - priority rules
    - confidence calculation

    The IntentEngine handles language understanding.
    The DecisionEngine decides which module should handle
    the request.
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
                "latest",
                "today",
                "current",
                "news",
                "weather",
                "price",
                "score",
                "online",
                "search",
                "internet"
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
            "system": 80,
            "coding": 75,
            "internet": 70,
            "creative": 65,
            "emotional_support": 60,
            "knowledge": 50,
            "conversation": 40
        }

        # Intents understood by IntentEngine that should
        # normally be handled by KnowledgeEngine.
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
        # Memory store
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
        # Memory recall
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
        # Comparison
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
        # IMPORTANT:
        # IntentEngine has already understood the
        # question. Knowledge questions must not be
        # hijacked by words such as "function", "work",
        # "do", etc.
        # ----------------------------------------------

        if intent in self.knowledge_intents:

            return self._set_result(
                "knowledge",
                0.9
            )

        # ----------------------------------------------
        # Calculate scores
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
        # Find strongest score
        # ----------------------------------------------

        best_score = max(scores.values())

        if best_score == 0:

            return self._set_result(
                "knowledge",
                0.0
            )

        candidates = [
            name
            for name, score in scores.items()
            if score == best_score
        ]

        # ----------------------------------------------
        # Priority tie-breaker
        # ----------------------------------------------

        best = max(
            candidates,
            key=lambda name: self.priority.get(
                name,
                0
            )
        )

        # ----------------------------------------------
        # Confidence
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

    def _set_result(self, decision, confidence):

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
            "decision": self.last_decision,
            "confidence": self.last_confidence,
            "scores": self.last_scores
        }

    # ==================================================
    # GET SCORES
    # ==================================================

    def get_scores(self):

        return self.last_scores
