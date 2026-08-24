import re
class ContextEngine:
    """
    CONNY AI V9 Context Engine

    Maintains short-term conversational context.

    Stores:
        - Last user message
        - Last assistant response
        - Last intent
        - Last decision
        - Current topic
    """

    def __init__(self, max_history=10):

        self.max_history = max_history

        self.history = []

        self.last_user_message = None
        self.last_response = None
        self.last_intent = None
        self.last_decision = None
        self.current_topic = None

    # ==================================================
    # ADD TURN
    # ==================================================

    def add_turn(
        self,
        user_message,
        response,
        intent=None,
        decision=None,
        topic=None,
        resolved_message=None
    ):

        self.last_user_message = user_message
        self.last_response = response
        self.last_intent = intent
        self.last_decision = decision

        if topic:
            self.current_topic = topic

        self.history.append({
            "user": user_message,
            "resolved": resolved_message or user_message,
            "assistant": response,
            "intent": intent,
            "decision": decision,
            "topic": self.current_topic
        })

        if len(self.history) > self.max_history:

            self.history = self.history[
                -self.max_history:
            ]

    # ==================================================
    # SET TOPIC
    # ==================================================

    def set_topic(self, topic):

        if topic:

            self.current_topic = str(
                topic
            ).strip()

    # ==================================================
    # RESOLVE FOLLOW-UP
    # ==================================================

    def _v12_personal_followup(self, message):
        """
        Resolve simple personal follow-up questions.

        Example:
            My favorite project is CONNY AI.
            What is my favorite project?
        """

        text = str(message).strip().lower()

        match = re.match(
            r"^(?:what|who|where|when)\s+(?:is|are|was|were)\s+my\s+(.+?)\??$",
            text
        )

        if not match:
            return None

        key = match.group(1).strip()

        for turn in reversed(self.history):
            user_message = str(turn.get("user", "")).strip()

            value_match = re.search(
                r"\bmy\s+"
                + re.escape(key)
                + r"\s+is\s+(.+?)(?:[.!?]|$)",
                user_message,
                re.IGNORECASE
            )

            if value_match:
                value = value_match.group(1).strip()
                return f"Your {key} is {value}."

        return None


    def resolve_followup(self, message, *args, **kwargs):
        personal = self._v12_personal_followup(message)

        if personal:
            return personal

        return self._v12_original_resolve_followup(
            message,
            *args,
            **kwargs
        )


    def _v12_original_resolve_followup(self, message):

        if not message:
            return message

        text = str(message).strip()
        lower = text.lower()

        followups = (
            "tell me more",
            "more about it",
            "more about that",
            "explain more",
            "go on",
            "continue",
            "what about it",
            "what about that",
            "can you explain more",
            "give me more information"
        )

        if lower in followups and self.current_topic:
            return f"tell me more about {self.current_topic}"

        return text

    # ==================================================
    # GET TOPIC
    # ==================================================

    def get_topic(self):

        return self.current_topic

    # ==================================================
    # GET LAST MESSAGE
    # ==================================================

    def get_last_message(self):

        return self.last_user_message

    # ==================================================
    # GET LAST RESPONSE
    # ==================================================

    def get_last_response(self):

        return self.last_response

    # ==================================================
    # GET LAST INTENT
    # ==================================================

    def get_last_intent(self):

        return self.last_intent

    # ==================================================
    # GET LAST DECISION
    # ==================================================

    def get_last_decision(self):

        return self.last_decision

    # ==================================================
    # GET HISTORY
    # ==================================================

    def get_history(self):

        return list(self.history)

    # ==================================================
    # GET RECENT TURNS
    # ==================================================

    def recent(self, count=3):

        return self.history[-count:]

    # ==================================================
    # CLEAR
    # ==================================================

    def clear(self):

        self.history.clear()

        self.last_user_message = None
        self.last_response = None
        self.last_intent = None
        self.last_decision = None
        self.current_topic = None

    # ==================================================
    # STATUS
    # ==================================================

    def status(self):

        return {
            "history_length":
                len(self.history),

            "last_user_message":
                self.last_user_message,

            "last_response":
                self.last_response,

            "last_intent":
                self.last_intent,

            "last_decision":
                self.last_decision,

            "current_topic":
                self.current_topic
        }
