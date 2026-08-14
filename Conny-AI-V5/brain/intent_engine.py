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
                "which is better"
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

            # Online intents
            "internet_search": 120,
            "news": 115,
            "wikipedia": 110,
            "weather": 105,
            "current_info": 100,

            # Knowledge intents
            "comparison": 90,
            "reason": 80,
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
