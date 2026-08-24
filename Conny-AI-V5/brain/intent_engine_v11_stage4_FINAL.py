class IntentEngine:
    """
    CONNY AI Intent Engine V7

    Detects the type of request being made.

    The engine:
    - scores possible intents
    - gives stronger weight to phrases
    - handles explicit commands
    - recognizes online request types
    - resolves competing intents
    - exposes confidence and scores
    """

    def __init__(self):

        self.intents = {

            # ==========================================
            # IDENTITY
            # ==========================================

            "identity": [
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
            ],

            # ==========================================
            # CONVERSATION
            # ==========================================

            "conversation": [
                "hello",
                "hi",
                "hey",
                "hello conny",
                "hi conny",
                "hey conny",
                "how are you",
                "how are you doing",
                "how's it going",
                "hows it going",
                "what's up",
                "whats up",
                "good morning",
                "good afternoon",
                "good evening",
                "tell me something interesting"
            ],

            # ==========================================
            # ONLINE INTENTS
            # ==========================================

            "internet_search": [
                "search ",
                "search online ",
                "look up ",
                "look online ",
                "find online "
            ],

            "news": [
                "latest news",
                "news about",
                "latest news about",
                "news "
            ],

            "wikipedia": [
                "wikipedia ",
                "wiki "
            ],

            "weather": [
                "weather",
                "weather today",
                "weather in "
            ],

            "current_info": [
                "latest ",
                "current ",
                "today ",
                "right now",
                "live "
            ],

            # ==========================================
            # MEMORY INTENTS
            # ==========================================

            "memory_store": [
                "remember ",
                "remember that ",
                "save ",
                "save this",
                "store ",
                "store this",
                "don't forget ",
                "dont forget ",
                "my name is",
                "my favorite",
                "i like",
                "i love"
            ],

            "memory_recall": [
                "what do you remember",
                "show memories",
                "what did i tell you",
                "do you remember",
                "what do you know about me",
                "tell me about myself"
            ],

            # ==========================================
            # CALCULATOR
            # ==========================================

            "calculator": [
                "calculate ",
                "solve ",
                "plus",
                "minus",
                "multiply",
                "multiplied by",
                "divide",
                "divided by",
                "times",
                "sum of",
                "total of",
                "average of",
                "mean of",
                "product of",
                "quotient of",
                "difference of",
                "difference between",
                "maximum of",
                "minimum of",
                "square root",
                "square of",
                "cube of",
                "power of",
                "to the power"
            ],

            # ==========================================
            # CODING
            # ==========================================

            "coding": [
                "python",
                "javascript",
                "java",
                "c++",
                " c ",
                "html",
                "css",
                "code",
                "coding",
                "program",
                "programming",
                "debug",
                "debugging",
                "syntax",
                "function",
                "class",
                "script",
                "bug",
                "error"
            ],

            # ==========================================
            # CREATIVE
            # ==========================================

            "creative": [
                "write a",
                "write me",
                "create a",
                "create me",
                "story",
                "poem",
                "poetry",
                "caption",
                "letter",
                "message",
                "design",
                "idea",
                "generate"
            ],

            # ==========================================
            # SYSTEM
            # ==========================================

            "system": [
                "open ",
                "launch ",
                "install ",
                "remove ",
                "run ",
                "terminal",
                "command",
                "shutdown",
                "restart",
                "file",
                "folder"
            ],

            # ==========================================
            # EMOTIONAL SUPPORT
            # ==========================================

            "emotional_support": [
                "sad",
                "angry",
                "worried",
                "scared",
                "afraid",
                "stress",
                "stressed",
                "tired",
                "lonely",
                "excited",
                "frustrated",
                "nervous"
            ],

            # ==========================================
            # KNOWLEDGE / OFFLINE INTENTS
            # ==========================================

            "comparison": [
                "compare",
                "comparison",
                "difference between",
                "difference",
                " vs ",
                "versus",
                "better than",
                "which is better",
                "which is greater",
                "which is bigger",
                "which is larger",
                "greater than",
                "bigger than",
                "larger than",
                "are equal",
                "is equal",
                "equal to",
                "the same",
                "same as"
            ],
            "explanation": [
                "explain",
                "describe",
                "teach me",
                "teach",
                "simplify",
                "in simple terms",
                "what does it mean"
            ],

            "reason": [
                "why",
                "why is",
                "why are",
                "why does",
                "why do",
                "why did"
            ],

            "process": [
                "how",
                "how does",
                "how do",
                "how can",
                "how to",
                "how is",
                "how are"
            ],

            "examples": [
                "example",
                "examples",
                "give me an example",
                "give examples"
            ],

            "functions": [
                "function",
                "functions",
                "purpose",
                "purposes",
                "used for",
                "what is it used for",
                "what are its uses"
            ],

            "definition": [
                "what is",
                "what are",
                "define",
                "definition",
                "meaning",
                "what does it mean"
            ]
        }

        # ==============================================
        # PRIORITY
        # ==============================================

        self.priority = {

            # Identity
            "identity": 130,

            # Conversation
            "conversation": 125,

            # Online intents
            "internet_search": 120,
            "news": 115,
            "wikipedia": 110,
            "weather": 105,
            "current_info": 100,

            # Memory
            "memory_store": 120,
            "memory_recall": 118,

            # Calculator / comparison
            "calculator": 115,
            "comparison": 110,

            # Coding
            "coding": 105,

            # System / creative / emotional
            "system": 95,
            "creative": 90,
            "emotional_support": 85,

            # Knowledge intents
            "reason": 75,
            "process": 75,
            "examples": 70,
            "functions": 65,
            "explanation": 60,
            "definition": 50,

            # Fallback
            "general": 10
        }

        self.last_scores = {}
        self.last_intent = "general"
        self.last_confidence = 0.0

    # ==================================================
    # DETECT
    # ==================================================

    def detect(self, message):

        text = str(message).lower().strip()

        self.last_scores = {}

        # ==============================================
        # EMPTY MESSAGE
        # ==============================================

        if not text:

            return self._set_result(
                "general",
                0.0
            )

        # ==============================================
        # EXPLICIT ONLINE INTENTS
        #
        # These MUST override generic knowledge intents.
        #
        # Example:
        #
        # "search Python programming"
        #
        # Python/programming may be related to another
        # topic, but "search" explicitly requests online
        # information.
        # ==============================================

        # ----------------------------------------------
        # INTERNET SEARCH
        # ----------------------------------------------

        if (
            text.startswith("search ")
            or text.startswith("search online ")
            or text.startswith("look up ")
            or text.startswith("look online ")
            or text.startswith("find online ")
        ):

            return self._set_result(
                "internet_search",
                1.0
            )
        # ----------------------------------------------
        # NEWS
        # ----------------------------------------------

        if (
            "latest news" in text
            or "news about" in text
            or "latest news about" in text
            or text.startswith("news ")
            or text.endswith(" news")
            or " news " in text
        ):

            return self._set_result(
                "news",
                1.0
            )

        # ----------------------------------------------
        # WIKIPEDIA
        # ----------------------------------------------

        if (
            text.startswith("wikipedia ")
            or text.startswith("wiki ")
            or text == "wikipedia"
            or text == "wiki"
        ):

            return self._set_result(
                "wikipedia",
                1.0
            )

        # ----------------------------------------------
        # WEATHER
        # ----------------------------------------------

        if (
            text.startswith("weather")
            or "weather today" in text
            or "weather in " in text
        ):

            return self._set_result(
                "weather",
                1.0
            )

        # ----------------------------------------------
        # CURRENT / LIVE INFORMATION
        # ----------------------------------------------

        if (
            text.startswith("latest ")
            or text.startswith("current ")
            or text.startswith("today ")
            or "right now" in text
            or "live " in text
        ):

            return self._set_result(
                "current_info",
                1.0
            )

        # ==============================================
        # CONVERSATION OVERRIDES
        # ==============================================
        #
        # These must run BEFORE generic process matching.
        #
        # "how are you" must never become "process"
        # simply because the word "how" appears.
        # ==============================================

        conversation_phrases = {
            "hello",
            "hi",
            "hey",
            "hello conny",
            "hi conny",
            "hey conny",
            "how are you",
            "how are you doing",
            "how's it going",
            "hows it going",
            "what's up",
            "whats up",
            "good morning",
            "good afternoon",
            "good evening",
            "tell me something interesting"
        }

        if text in conversation_phrases:

            return self._set_result(
                "conversation",
                1.0
            )

        # ==============================================
        # COMPARISON OVERRIDES
        # ==============================================
        #
        # Natural comparison questions should be detected
        # even when they are not explicitly listed in the
        # scoring phrases.
        # ==============================================

        if (
            text.startswith("which is smaller ")
            or text.startswith("which is greater ")
            or text.startswith("which is bigger ")
            or text.startswith("which is larger ")
            or " is smaller than " in text
            or " is greater than " in text
            or " is bigger than " in text
            or " is larger than " in text
        ):

            return self._set_result(
                "comparison",
                1.0
            )

        # ==============================================
        # CALCULATION OVERRIDES
        # ==============================================
        #
        # Mathematical requests must beat definition
        # detection.
        # ==============================================

        if (
            text.startswith("calculate ")
            or "what is the sum of " in text
            or "what is the total of " in text
            or "add " in text
            or "subtract " in text
            or "multiply " in text
            or "divide " in text
        ):

            return self._set_result(
                "calculator",
                1.0
            )

        # ==============================================
        # IDENTITY
        # ==============================================
        #
        # Identity must always beat generic knowledge.
        # ==============================================

        if text in (
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
        ):

            return self._set_result(
                "identity",
                1.0
            )

        # ==============================================
        # MATH OVERRIDES
        #
        # Explicit mathematical requests must be detected
        # before generic knowledge/process scoring.
        # ==============================================

        import re

        # ------------------------------------------------
        # Numeric equality
        #
        # Examples:
        #   are 10 and 10 equal
        #   are 10 and 5 equal
        #   is 10 equal to 10
        # ------------------------------------------------

        equality_patterns = (
            r"^are\s+[-+]?\d+(?:\.\d+)?\s+and\s+[-+]?\d+(?:\.\d+)?\s+equal\??$",
            r"^is\s+[-+]?\d+(?:\.\d+)?\s+equal\s+to\s+[-+]?\d+(?:\.\d+)?\??$",
        )

        if any(
            re.search(pattern, text)
            for pattern in equality_patterns
        ):
            return self._set_result(
                "comparison",
                1.0
            )

        # ------------------------------------------------
        # Direct arithmetic expression
        #
        # Examples:
        #   10 + 5
        #   20 - 7
        #   4 * 8
        #   100 / 5
        #   2 ^ 3
        # ------------------------------------------------

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

        # ------------------------------------------------
        # Natural-language arithmetic
        # ------------------------------------------------

        math_phrases = (
            "calculate ",
            "solve ",
            "what is the sum of ",
            "what is the total of ",
            "add ",
            "subtract ",
            "multiply ",
            "divide ",
            "plus ",
            "minus ",
            "multiplied by",
            "divided by",
            " times ",
            "average of ",
            "mean of ",
            "sum of ",
            "total of ",
            "product of ",
            "quotient of ",
            "difference of ",
            "difference between ",
            "maximum of ",
            "minimum of ",
            "highest of ",
            "lowest of ",
            "square root",
            "square of ",
            "cube of ",
            "cubed",
            "squared",
            "power of ",
            "to the power "
        )

        if any(
            phrase in text
            for phrase in math_phrases
        ):
            return self._set_result(
                "calculator",
                1.0
            )

        # ==============================================
        # QUALITY OVERRIDES
        #
        # Explicit high-signal requests are resolved before
        # generic keyword scoring.
        # ==============================================

        lower_text = text.lower().strip()

        # ------------------------------------------------
        # CODING
        # ------------------------------------------------

        coding_phrases = (
            "write python code",
            "write javascript code",
            "write java code",
            "write c code",
            "write c++ code",
            "write html code",
            "write css code",
            "write code",
            "debug this python code",
            "debug this code",
            "debug my python code",
            "fix this python code",
            "fix this code",
            "program in python",
            "program in javascript",
            "program in java",
            "create python code",
            "create javascript code",
            "create java code",
        )

        if any(
            phrase in lower_text
            for phrase in coding_phrases
        ):
            return self._set_result(
                "coding",
                1.0
            )

        # ------------------------------------------------
        # SYSTEM
        # ------------------------------------------------

        system_phrases = (
            "open the terminal",
            "open terminal",
            "launch the terminal",
            "start the terminal",
            "open the file manager",
            "open file manager",
            "open settings",
            "open the settings",
            "shut down the computer",
            "shutdown the computer",
            "restart the computer",
            "reboot the computer",
        )

        if any(
            phrase in lower_text
            for phrase in system_phrases
        ):
            return self._set_result(
                "system",
                1.0
            )

        # ------------------------------------------------
        # CREATIVE
        # ------------------------------------------------

        creative_phrases = (
            "write me a story",
            "write a story",
            "tell me a story",
            "create a story",
            "make up a story",
            "write a poem",
            "write me a poem",
            "create a poem",
            "make up a poem",
        )

        if any(
            phrase in lower_text
            for phrase in creative_phrases
        ):
            return self._set_result(
                "creative",
                1.0
            )

        # ==============================================
        # MEMORY RECALL PRIORITY OVERRIDE
        #
        # Memory questions must be resolved before generic
        # knowledge/definition matching.
        # ==============================================

        memory_recall_phrases = (
            "what do you remember",
            "show memories",
            "what did i tell you",
            "do you remember",
            "what do you know about me",
            "tell me about myself",
        )

        if any(
            phrase in lower_text
            for phrase in memory_recall_phrases
        ):
            return self._set_result(
                "memory_recall",
                1.0
            )

        # ==============================================
        # KNOWLEDGE QUALITY OVERRIDES
        #
        # High-signal educational questions are resolved
        # before generic keyword scoring.
        # ==============================================

        lower_text = text.lower().strip()

        # ------------------------------------------------
        # DEFINITIONS
        # ------------------------------------------------

        definition_patterns = (
            "what is ",
            "what are ",
            "define ",
            "definition of ",
            "what does ",
            "what do ",
        )

        # Keep identity questions handled by identity.
        identity_patterns = (
            "what is your name",
            "what are you",
            "what is your purpose",
        )

        if (
            any(
                phrase in lower_text
                for phrase in definition_patterns
            )
            and not any(
                phrase in lower_text
                for phrase in identity_patterns
            )
        ):
            return self._set_result(
                "definition",
                1.0
            )

        # ------------------------------------------------
        # PROCESS / HOW QUESTIONS
        # ------------------------------------------------

        process_patterns = (
            "how does ",
            "how do ",
            "how is ",
            "how are ",
            "how can ",
            "how to ",
            "how is it made",
            "how does it work",
        )

        if any(
            phrase in lower_text
            for phrase in process_patterns
        ):
            return self._set_result(
                "process",
                1.0
            )

        # ------------------------------------------------
        # V11 FINAL CODING WHY OVERRIDE
        #
        # A question about why a user's programming code
        # does not work is a coding/debugging request.
        # This MUST run before generic WHY/reason matching.
        # ------------------------------------------------

        coding_debug_why = (
            "why does my",
            "why is my",
            "why isn't my",
            "why isnt my",
        )

        coding_debug_languages = (
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

        coding_debug_targets = (
            "code",
            "program",
            "script",
            "function",
        )

        coding_debug_failures = (
            "not work",
            "doesn't work",
            "does not work",
            "isn't working",
            "isnt working",
            "not working",
        )

        if (
            any(phrase in lower_text for phrase in coding_debug_why)
            and any(lang in lower_text for lang in coding_debug_languages)
            and any(target in lower_text for target in coding_debug_targets)
            and any(failure in lower_text for failure in coding_debug_failures)
        ):
            return self._set_result(
                "coding",
                1.0
            )

        # ------------------------------------------------
        # REASON / WHY QUESTIONS
        # ------------------------------------------------

        reason_patterns = (
            "why ",
            "why is ",
            "why are ",
            "why does ",
            "why do ",
            "why can ",
            "why would ",
        )

        if any(
            phrase in lower_text
            for phrase in reason_patterns
        ):
            return self._set_result(
                "reason",
                1.0
            )

        # ------------------------------------------------
        # EXPLANATION
        # ------------------------------------------------

        explanation_patterns = (
            "explain ",
            "explain how ",
            "explain why ",
            "can you explain ",
            "please explain ",
            "tell me how ",
            "tell me why ",
        )

        if any(
            phrase in lower_text
            for phrase in explanation_patterns
        ):
            return self._set_result(
                "explanation",
                1.0
            )

        # ------------------------------------------------
        # EXAMPLES
        # ------------------------------------------------

        example_patterns = (
            "give me an example",
            "give me examples",
            "show me an example",
            "show me examples",
            "example of ",
            "examples of ",
            "can you give an example",
        )

        if any(
            phrase in lower_text
            for phrase in example_patterns
        ):
            return self._set_result(
                "examples",
                1.0
            )

        # ==============================================
        # V11 CODING QUALITY OVERRIDES
        #
        # Coding requests must beat generic creative/reasoning
        # matches, while educational questions about programming
        # must remain knowledge/reasoning intents.
        # ==============================================

        lower_text = text.lower().strip()

        # ------------------------------------------------
        # Explicit coding construction / debugging
        # ------------------------------------------------

        coding_signals = (
            "write code",
            "write a program",
            "write a script",
            "write a function",
            "create code",
            "create a program",
            "create a script",
            "create a function",
            "make code",
            "make a program",
            "make a script",
            "make a function",
            "generate code",
            "build a program",
            "debug this",
            "debug my",
            "fix this code",
            "fix my code",
            "find the error in",
            "code not work",
            "code doesn't work",
            "code does not work",
            "program not work",
            "program doesn't work",
            "program does not work",
        )

        coding_languages = (
            "python",
            "javascript",
            "java",
            "c++",
            "c#",
            " c ",
            "html",
            "css",
        )

        has_language = any(
            lang in f" {lower_text} "
            for lang in coding_languages
        )

        # Strong explicit construction/debugging request.
        if (
            any(signal in lower_text for signal in coding_signals)
            and has_language
        ):
            self.last_intent = "coding"
            self.last_confidence = 1.0
            self.last_scores = {}
            print("DEBUG Intent:", self.last_intent)
            print("DEBUG Intent Confidence:", self.last_confidence)
            print("DEBUG Intent Scores:", self.last_scores)
            return "coding"

        # ------------------------------------------------
        # "why does my Python code not work"
        # ------------------------------------------------

        if (
            has_language
            and (
                "why does my" in lower_text
                or "why is my" in lower_text
                or "why isn't my" in lower_text
                or "why isnt my" in lower_text
            )
            and (
                "code" in lower_text
                or "program" in lower_text
                or "script" in lower_text
            )
            and (
                "not work" in lower_text
                or "doesn't work" in lower_text
                or "does not work" in lower_text
                or "isn't working" in lower_text
                or "isnt working" in lower_text
            )
        ):
            self.last_intent = "coding"
            self.last_confidence = 1.0
            self.last_scores = {}
            print("DEBUG Intent:", self.last_intent)
            print("DEBUG Intent Confidence:", self.last_confidence)
            print("DEBUG Intent Scores:", self.last_scores)
            return "coding"

        # ------------------------------------------------
        # Explicit educational questions about programming
        # ------------------------------------------------
        #
        # These must NOT become coding requests merely because
        # words such as Python, JavaScript or function appear.
        # ------------------------------------------------

        educational_start = (
            lower_text.startswith("what is ")
            or lower_text.startswith("what are ")
            or lower_text.startswith("define ")
            or lower_text.startswith("explain ")
            or lower_text.startswith("how does ")
            or lower_text.startswith("how do ")
            or lower_text.startswith("why does ")
            or lower_text.startswith("why do ")
            or lower_text.startswith("why is ")
            or lower_text.startswith("why are ")
            or lower_text.startswith("give me an example")
            or lower_text.startswith("show me an example")
        )

        if educational_start:
            if (
                lower_text.startswith("what is ")
                or lower_text.startswith("what are ")
                or lower_text.startswith("define ")
            ):
                self.last_intent = "definition"
                self.last_confidence = 1.0
                self.last_scores = {}
                print("DEBUG Intent:", self.last_intent)
                print("DEBUG Intent Confidence:", self.last_confidence)
                print("DEBUG Intent Scores:", self.last_scores)
                return "definition"

            if lower_text.startswith("explain "):
                self.last_intent = "explanation"
                self.last_confidence = 1.0
                self.last_scores = {}
                print("DEBUG Intent:", self.last_intent)
                print("DEBUG Intent Confidence:", self.last_confidence)
                print("DEBUG Intent Scores:", self.last_scores)
                return "explanation"

            if (
                lower_text.startswith("how does ")
                or lower_text.startswith("how do ")
            ):
                self.last_intent = "process"
                self.last_confidence = 1.0
                self.last_scores = {}
                print("DEBUG Intent:", self.last_intent)
                print("DEBUG Intent Confidence:", self.last_confidence)
                print("DEBUG Intent Scores:", self.last_scores)
                return "process"

            if (
                lower_text.startswith("why does ")
                or lower_text.startswith("why do ")
                or lower_text.startswith("why is ")
                or lower_text.startswith("why are ")
            ):
                self.last_intent = "reason"
                self.last_confidence = 1.0
                self.last_scores = {}
                print("DEBUG Intent:", self.last_intent)
                print("DEBUG Intent Confidence:", self.last_confidence)
                print("DEBUG Intent Scores:", self.last_scores)
                return "reason"

            if (
                lower_text.startswith("give me an example")
                or lower_text.startswith("show me an example")
            ):
                self.last_intent = "examples"
                self.last_confidence = 1.0
                self.last_scores = {}
                print("DEBUG Intent:", self.last_intent)
                print("DEBUG Intent Confidence:", self.last_confidence)
                print("DEBUG Intent Scores:", self.last_scores)
                return "examples"

        # ==============================================
        # MEMORY OVERRIDES
        #
        # Explicit memory commands must beat generic
        # intents such as coding or process.
        # ==============================================

        if text.startswith((
            "remember ",
            "remember that ",
            "save ",
            "store ",
            "don't forget ",
            "dont forget "
        )):

            return self._set_result(
                "memory_store",
                1.0
            )

        if text in (
            "what do you remember",
            "show memories",
            "what did i tell you",
            "do you remember",
            "what do you know about me",
            "tell me about myself"
        ):

            return self._set_result(
                "memory_recall",
                1.0
            )

        # ==============================================
        # SCORE GENERIC INTENTS
        # ==============================================

        scores = {}

        for intent, keywords in self.intents.items():

            score = 0

            for keyword in keywords:

                keyword = keyword.lower()

                if keyword in text:

                    words = len(
                        keyword.strip().split()
                    )

                    if words >= 4:
                        score += 4

                    elif words == 3:
                        score += 3

                    elif words == 2:
                        score += 2

                    else:
                        score += 1

            scores[intent] = score

        self.last_scores = scores

        # ==============================================
        # FIND STRONGEST INTENT
        # ==============================================

        best_score = max(
            scores.values()
        )

        # ==============================================
        # NO MATCH
        # ==============================================

        if best_score == 0:

            return self._set_result(
                "general",
                0.0
            )

        # ==============================================
        # STRONGEST CANDIDATES
        # ==============================================

        candidates = [
            intent
            for intent, score in scores.items()
            if score == best_score
        ]

        # ==============================================
        # PRIORITY TIE BREAKER
        # ==============================================

        best = max(
            candidates,
            key=lambda intent:
            self.priority.get(
                intent,
                0
            )
        )

        # ==============================================
        # CONFIDENCE
        # ==============================================

        sorted_scores = sorted(
            scores.values(),
            reverse=True
        )

        strongest = sorted_scores[0]

        second = (
            sorted_scores[1]
            if len(sorted_scores) > 1
            else 0
        )

        if second == 0:

            confidence = 0.90

        else:

            confidence = (
                strongest /
                (strongest + second)
            )

            if strongest - second >= 2:

                confidence += 0.10

            confidence = min(
                confidence,
                0.99
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
        intent,
        confidence
    ):

        self.last_intent = intent

        self.last_confidence = float(
            confidence
        )

        print(
            "DEBUG Intent:",
            intent
        )

        print(
            "DEBUG Intent Confidence:",
            self.last_confidence
        )

        print(
            "DEBUG Intent Scores:",
            self.last_scores
        )

        return intent

    # ==================================================
    # GET LAST RESULT
    # ==================================================

    def get_last_intent(self):

        return {
            "intent":
                self.last_intent,

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
