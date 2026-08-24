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
                "percent", "square root",
                "average", "mean",
                "sum", "total",
                "product", "quotient",
                "difference",
                "maximum", "minimum",
                "highest", "lowest",
                "square root",
                "square of",
                "cube of",
                "power of",
                "to the power",
                "increase",
                "decrease"
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
            "examples",
            "functions"
        }

        self.reasoning_intents = {
            "reason",
            "process",
            "explanation"
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
        # IDENTITY
        # ==============================================
        #
        # Identity is a dedicated decision and must never
        # fall through to generic knowledge.
        # ==============================================

        if (
            intent == "identity"
            or text in (
                "what is your name",
                "what's your name",
                "whats your name",
                "who are you",
                "what are you",
                "tell me your name",
                "your name",
                "who is conny",
                "who is conny ai",
                "what is conny",
                "what's conny",
                "introduce yourself"
            )
        ):

            return self._set_result(
                "identity",
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
            "good night", 
            "how are you",
            "how are you?",
            "how are things",
            "how are things?",
            "how are you doing",
            "how are you doing?",
            "how have you been",
            "how have you been?"
        ):

            return self._set_result(
               "conversation",
               1.0
            )

        # ==============================================
        # CAPABILITIES
        # ==============================================

        if text in (
            "what can you do",
            "what can you do?",
            "what are your abilities",
            "what are your abilities?",
            "what can you help me with",
            "what can you help me with?"
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
        # NUMERIC DIFFERENCE → CALCULATOR
        # ==============================================

        if (
            "difference between" in text
            and len([
                value
                for value in text.split()
                if any(char.isdigit() for char in value)
            ]) >= 2
        ):

            return self._set_result(
                "calculator",
                1.0
            )


        # ==============================================
        # SYMBOLIC ARITHMETIC → CALCULATOR
        #
        # Detect direct mathematical expressions such as:
        #   10 + 5
        #   20 - 7
        #   4 * 8
        #   100 / 5
        #   2 ^ 3
        # ==============================================

        import re

        arithmetic_pattern = re.compile(
            r"^\s*[-+]?\d+(?:\.\d+)?\s*"
            r"[+\-*/%^]"
            r"\s*[-+]?\d+(?:\.\d+)?\s*$"
        )

        if arithmetic_pattern.match(text):
            return self._set_result(
                "calculator",
                1.0
            )

        # ==============================================
        # NUMERIC EQUALITY → COMPARISON
        #
        # Detect natural equality questions such as:
        #   are 10 and 10 equal
        #   are 5 and 7 equal
        #   is 10 equal to 10
        # ==============================================

        import re

        equality_patterns = (
            r"are\s+[-+]?\d+(?:\.\d+)?\s+and\s+[-+]?\d+(?:\.\d+)?\s+equal",
            r"is\s+[-+]?\d+(?:\.\d+)?\s+equal\s+to\s+[-+]?\d+(?:\.\d+)?",
        )

        if any(
            re.search(pattern, text)
            for pattern in equality_patterns
        ):
            return self._set_result(
                "comparison",
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
            or "what is greater" in text
            or "which is greater" in text
            or "what is bigger" in text
            or "which is bigger" in text
            or "what is larger" in text
            or "which is larger" in text
            or "what is smaller" in text
            or "which is smaller" in text
            or "what is less" in text
            or "which is less" in text
            or "greater than" in text
            or "bigger than" in text
            or "larger than" in text
            or "which is greatest" in text
            or "which is largest" in text
            or "which is smallest" in text
            or "which is least" in text
            or "greater," in text
            or "bigger," in text
            or "larger," in text
            or "greater or" in text
            or "bigger or" in text
            or "larger or" in text
            or "are equal" in text
            or "is equal" in text
            or "equal to" in text
            or "the same" in text
            or "same as" in text
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
        #
        # Detect current/latest information even when
        # the request is phrased as a natural question.
        # ==============================================

        current_phrases = (
            "latest ",
            "current ",
            "today ",
            "right now",
            "live ",
            "the latest ",
            "the current ",
            "latest version",
            "current version",
            "latest news",
            "current news",
            "current weather",
            "latest weather",
            "current price",
            "latest price",
            "what is the latest",
            "what's the latest",
            "whats the latest",
            "what is the current",
            "what's the current",
            "whats the current",
            "what is today's",
            "what's today's",
            "whats today's",
            "tell me the latest",
            "tell me the current"
        )

        if any(
            phrase in text
            for phrase in current_phrases
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
        # COMPARISON PROTECTION
        #
        # A comparison request must NEVER be mistaken
        # for a coding request just because it mentions
        # programming languages such as Python,
        # JavaScript, Java, C++, etc.
        # ==============================================

        comparison_phrases = (
            " vs ",
            " versus ",
            "compare ",
            "difference between ",
            "which is better ",
            "what is better ",
            "which programming language is better ",
            "what programming language is better ",
            "which language is better ",
            "what language is better ",
            "which is greater ",
            "which is smaller ",
            "which is bigger ",
            "which is larger ",
            "which is less ",
            "which is greater than ",
            "which is better than ",
            "are equal ",
            "are equal",
            "is equal ",
            "is equal",
            "equal to ",
            "equal to",
            "the same ",
            "the same",
            "same as "
        )

        if any(
            phrase in text
            for phrase in comparison_phrases
        ):
            return self._set_result(
                "comparison",
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
        # NATURAL-LANGUAGE CALCULATOR
        # ==============================================

        natural_math = (
            "average of",
            "mean of",
            "sum of",
            "total of",
            "maximum of",
            "minimum of",
            "highest of",
            "lowest of"
        )

        if any(
            phrase in text
            for phrase in natural_math
        ):

            import re

            numbers = re.findall(
                r"\d+(?:\.\d+)?",
                text
            )

            if len(numbers) >= 1:

                return self._set_result(
                    "calculator",
                    1.0
                )


        # ==============================================
        # NATURAL-LANGUAGE CALCULATOR
        # ==============================================

        calculator_phrases = (
            "average of",
            "mean of",
            "sum of",
            "total of",
            "product of",
            "quotient of",
            "difference between",
            "difference of",
            "maximum of",
            "minimum of",
            "highest of",
            "lowest of"
        )

        if any(
            phrase in text
            for phrase in calculator_phrases
        ):

            return self._set_result(
                "calculator",
                1.0
            )

        # ==============================================
        # CALCULATOR
        # ==============================================

        calculator_phrases = (
            # Explicit calculations
            "calculate ",
            "solve ",

            # Arithmetic operations
            " plus ",
            " minus ",
            " multiplied by ",
            " divided by ",
            " times ",

            # Aggregate calculations
            "average of",
            "mean of",
            "sum of",
            "total of",
            "product of",
            "quotient of",
            "maximum of",
            "minimum of",
            "highest of",
            "lowest of",
            "difference of",
            "difference between",

            # Powers / roots
            "square root",
            "square root of",
            "squared",
            "cubed",
            "cube of",
            "power of",
            "to the power",
        )

        if any(
            phrase in text
            for phrase in calculator_phrases
        ):

            return self._set_result(
                "calculator",
                1.0
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

        text = text.lower().strip()

        # ==================================================
        # V11 STAGE 4 — CODING PRECISION
        #
        # A programming language or programming term alone
        # must NEVER make a request a coding request.
        #
        # Coding requires an explicit construction or
        # debugging action.
        # ==================================================

        coding_phrases = (
            # Construction
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

            "write a function",
            "create a function",
            "make a function",

            "write a script",
            "create a script",
            "make a script",

            "code for",
            "program for",

            # Debugging
            "debug this",
            "debug my",
            "debug the",
            "fix this code",
            "fix my code",
            "fix the code",
            "find the bug",
            "find the error in",
            "syntax error",

            "code not work",
            "code does not work",
            "code doesn't work",
            "program not work",
            "program does not work",
            "program doesn't work",
            "script not work",
            "script does not work",
            "script doesn't work",
        )

        # Explicit coding construction/debugging request.
        if any(
            phrase in text
            for phrase in coding_phrases
        ):
            return True

        # ==================================================
        # Language + EXPLICIT coding verb
        #
        # Do NOT include generic programming nouns such as
        # "function", "program", "script", or "code" here.
        # Those nouns can appear in educational questions.
        # ==================================================

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
            "shell",
        )

        construction_actions = (
            "write",
            "create",
            "make",
            "build",
            "generate",
        )

        debugging_actions = (
            "debug",
            "fix",
        )

        has_language = any(
            language in text
            for language in languages
        )

        has_construction_action = any(
            action in text
            for action in construction_actions
        )

        has_debugging_action = any(
            action in text
            for action in debugging_actions
        )

        # A language + explicit construction verb is coding.
        if has_language and has_construction_action:
            return True

        # A language + debugging verb is coding only when the
        # request is actually about code/program/script behavior.
        if has_language and has_debugging_action:
            if any(
                term in text
                for term in (
                    "code",
                    "program",
                    "script",
                    "bug",
                    "error",
                    "syntax",
                    "work",
                    "working",
                )
            ):
                return True

        return False

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
