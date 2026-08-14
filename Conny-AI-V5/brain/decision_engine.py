class DecisionEngine:
    """
    CONNY AI Decision Engine V7

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

            "conversation": [
                "hi", "hello", "hey",
                "how are you", "who are you",
                "your name", "thank you", "thanks",
                "bye", "good morning",
                "good afternoon", "good evening",
                "good night"
            ],

            "emotional_support": [
                "happy", "sad", "angry",
                "worried", "scared", "afraid",
                "stress", "stressed", "exam",
                "tired", "lonely", "excited",
                "love", "frustrated", "nervous"
            ],

            "memory_store": [
                "remember", "save this",
                "store this", "my favorite",
                "my name is", "i like",
                "i love", "don't forget"
            ],

            "memory_recall": [
                "what do you remember",
                "show memories",
                "what do you know about me",
                "tell me about myself",
                "what did i tell you",
                "do you remember"
            ],

            "calculator": [
                "calculate", "solve",
                "plus", "minus",
                "multiply", "divide",
                "equation", "percentage",
                "percent", "square root"
            ],

            "comparison": [
                "compare",
                "difference between",
                " vs ",
                "versus",
                "better than",
                "which is better",
                "difference"
            ],

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

            "creative": [
                "write", "create",
                "story", "poem",
                "design", "idea",
                "generate", "caption",
                "message", "letter"
            ],

            "system": [
                "open", "launch",
                "install", "remove",
                "run", "terminal",
                "command", "shutdown",
                "restart", "file",
                "folder"
            ],

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

        self.knowledge_intents = {
            "definition",
            "explanation",
            "examples",
            "functions"
        }

        self.reasoning_intents = {
            "reason",
            "process"
        }

        self.online_intents = {
            "internet_search",
            "news",
            "wikipedia",
            "weather",
            "current_info"
        }

        self.last_scores = {}
        self.last_decision = None
        self.last_confidence = 0

    # ==================================================
    # CHOOSE DECISION
    # ==================================================

    def choose(self, message, intent=None):

        text = str(message).lower().strip()

        if not text:
            return self._set_result(
                "conversation",
                1.0
            )

        # ==============================================
        # EXPLICIT CONVERSATION
        # ==============================================

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

        # ==============================================
        # MEMORY STORE
        # ==============================================

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

        # ==============================================
        # MEMORY RECALL
        # ==============================================

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

        # ==============================================
        # COMPARISON
        # ==============================================

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

        # ==============================================
        # EXPLICIT INTERNET
        # ==============================================

        if (
            text.startswith("search ")
            or text.startswith("search online ")
            or text.startswith("look up ")
            or text.startswith("look online ")
            or text.startswith("find online ")
        ):

            return self._set_result(
                "internet",
                1.0
            )

        # ==============================================
        # NEWS
        # ==============================================

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

        # ==============================================
        # WEATHER
        # ==============================================

        if (
            text.startswith("weather")
            or "weather today" in text
            or "weather in " in text
        ):

            return self._set_result(
                "internet",
                1.0
            )

        # ==============================================
        # CURRENT / LIVE
        # ==============================================

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

        # ==============================================
        # WIKIPEDIA
        # ==============================================

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

        # ==============================================
        # ONLINE INTENTS
        # ==============================================

        if intent in self.online_intents:

            return self._set_result(
                "internet",
                1.0
            )

        # ==============================================
        # CODING OVERRIDE
        #
        # Coding requests must override generic
        # knowledge intents such as "functions".
        # ==============================================

        if self._is_coding_request(text):

            return self._set_result(
                "coding",
                1.0
            )

        # ==============================================
        # REASONING INTENTS
        # ==============================================

        if intent in self.reasoning_intents:

            return self._set_result(
                "reasoning",
                0.9
            )

        # ==============================================
        # KNOWLEDGE INTENTS
        # ==============================================

        if intent in self.knowledge_intents:

            return self._set_result(
                "knowledge",
                0.9
            )

        # ==============================================
        # CALCULATOR
        # ==============================================

        if (
            text.startswith("calculate ")
            or text.startswith("solve ")
        ):

            return self._set_result(
                "calculator",
                1.0
            )

        # ==============================================
        # CALCULATE SCORES
        # ==============================================

        scores = {}

        for name, keywords in self.intents.items():

            score = 0

            for keyword in keywords:

                if keyword in text:

                    score += 1

            scores[name] = score

        self.last_scores = scores

        # ==============================================
        # NO MATCH
        # ==============================================

        best_score = max(
            scores.values()
        )

        if best_score == 0:

            return self._set_result(
                "knowledge",
                0.0
            )

        # ==============================================
        # STRONGEST MATCHES
        # ==============================================

        candidates = [
            name
            for name, score in scores.items()
            if score == best_score
        ]

        best = max(
            candidates,
            key=lambda name:
            self.priority.get(
                name,
                0
            )
        )

        confidence = min(
            best_score / 3,
            1.0
        )

        return self._set_result(
            best,
            confidence
        )

    # ==================================================
    # CODING REQUEST DETECTION
    # ==================================================

    def _is_coding_request(self, text):

        coding_phrases = (
            "write code",
            "generate code",
            "create code",
            "make code",
            "write a program",
            "create a program",
            "make a program",
            "build a program",
            "write program",
            "create program",
            "make program",
            "build program",
            "code for",
            "program for",
            "write a function",
            "create a function",
            "make a function",
            "write a script",
            "create a script",
            "make a script",
            "debug",
            "fix this code",
            "fix my code",
            "find the bug",
            "syntax error"
        )

        if any(
            phrase in text
            for phrase in coding_phrases
        ):

            return True

        languages = (
            "python",
            "javascript",
            "java",
            "c++",
            "cpp",
            "c language",
            "html",
            "css",
            "bash",
            "shell"
        )

        actions = (
            "write",
            "create",
            "make",
            "build",
            "generate",
            "code",
            "program",
            "function",
            "script",
            "debug",
            "fix"
        )

        has_language = any(
            language in text
            for language in languages
        )

        has_action = any(
            action in text
            for action in actions
        )

        return has_language and has_action

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
