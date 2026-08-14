class Router:
    """
    CONNY AI Request Router V6

    Responsible for sending a processed request
    to the correct intelligence module.
    """

    def __init__(self, brain):
        self.brain = brain

    # ==================================================
    # MAIN ROUTE
    # ==================================================

    def route(
        self,
        message,
        emotion=None,
        intent=None,
        decision=None
    ):

        try:

            text = str(message).strip()

            if not text:
                return self.brain.response.unknown_response()

            # ------------------------------------------
            # Explicit intent handling
            # ------------------------------------------

            if intent == "greeting":
                return self.brain.response.greeting()

            if intent == "identity":
                return (
                    "I'm CONNY AI, your personal AI assistant."
                )

            if intent == "recall":
                return self.brain.memory.show()

            # ------------------------------------------
            # Memory
            # ------------------------------------------

            if decision == "memory_recall":
                return self.brain.memory.show()

            if decision == "memory_store":
                return self._store_memory(text)

            # ------------------------------------------
            # Conversation
            # ------------------------------------------

            if decision == "conversation":

                # Greetings
                if text in (
                    "hi",
                    "hello",
                    "hey",
                    "good morning",
                    "good afternoon",
                    "good evening",
                    "good night"
                ):
                    return self.brain.response.greeting()

                # Thanks
                if (
                    "thank you" in text
                    or "thanks" in text
                ):
                    return self.brain.response.thanks_response()

                # Goodbye
                if text in (
                    "bye",
                    "goodbye",
                    "see you",
                    "see you soon"
                ):
                    return self.brain.response.goodbye()

            # ------------------------------------------
            # Calculator / explicit plugin decision
            # ------------------------------------------

            if decision == "calculator":

                result = self._run_plugin(text)

                if result is not None:
                    return result

            # ------------------------------------------
            # Local knowledge
            # ------------------------------------------

            if decision == "knowledge":

                result = self._knowledge(
                    text,
                    intent
                )

                if result is not None:
                    return result

            # ------------------------------------------
            # Other plugins
            # ------------------------------------------

            result = self._run_plugin(text)

            if result is not None:
                return result

            # ------------------------------------------
            # Fallback knowledge search
            # ------------------------------------------

            result = self._knowledge(
                text,
                intent
            )

            if result is not None:
                return result

            # ------------------------------------------
            # Final fallback
            # ------------------------------------------

            return self.brain.response.unknown_response()

        except Exception as error:

            print(
                "DEBUG Router Error:",
                error
            )

            return self.brain.response.error_response()

    # ==================================================
    # MEMORY
    # ==================================================

    def _store_memory(self, text):

        original = text.strip()

        prefixes = (
            "remember ",
            "save ",
            "store ",
            "don't forget "
        )

        content = original

        for prefix in prefixes:

            if content.lower().startswith(prefix):

                content = content[len(prefix):].strip()

                break

        if not content:

            return (
                "What would you like me to remember?"
            )

        # ------------------------------------------
        # Try "my X is Y"
        # ------------------------------------------

        lower = content.lower()

        if lower.startswith("my ") and " is " in lower:

            left, value = content.split(
                " is ",
                1
            )

            key = left[3:].strip()
            value = value.strip()

            if key and value:

                return self.brain.memory.remember(
                    "personal",
                    key,
                    value
                )

        # ------------------------------------------
        # Try "X is Y"
        # ------------------------------------------

        if " is " in content:

            key, value = content.split(
                " is ",
                1
            )

            key = key.strip()
            value = value.strip()

            if key and value:

                return self.brain.memory.remember(
                    "general",
                    key,
                    value
                )

        # ------------------------------------------
        # No recognizable structure
        # ------------------------------------------

        return (
            "I can remember it, but please tell me "
            "what the information is, for example: "
            "'remember my favorite language is Python'."
        )

    # ==================================================
    # KNOWLEDGE
    # ==================================================

    def _knowledge(self, text, intent=None):

        result = self.brain.knowledge.search(text)

        if not result:
            return None

        data = result.get("data", {})

        # ==============================================
        # Direct answer
        # ==============================================

        answer = data.get("answer")

        if answer and intent not in (
            "functions",
            "examples"
        ):
            return answer

        # ==============================================
        # Functions
        # ==============================================

        if intent == "functions":

            functions = data.get("functions")

            if functions:

                return (
                    f"Functions of "
                    f"{result.get('name', 'this concept')}:\n\n"
                    + "\n".join(
                        f"- {item}"
                        for item in functions
                    )
                )

        # ==============================================
        # Examples
        # ==============================================

        if intent == "examples":

            examples = data.get("examples")

            if examples:

                return (
                    f"Examples of "
                    f"{result.get('name', 'this concept')}:\n\n"
                    + "\n".join(
                        f"- {item}"
                        for item in examples
                    )
                )

        # ==============================================
        # Definition
        # ==============================================

        definition = data.get("definition")

        if definition:

            response = definition

            # ------------------------------------------
            # Functions
            # ------------------------------------------

            functions = data.get("functions")

            if functions and intent in (
                "definition",
                "explanation",
                "process",
                "reason",
                "general"
            ):

                response += (
                    "\n\nFunctions:\n"
                    + "\n".join(
                        f"- {item}"
                        for item in functions
                    )
                )

            # ------------------------------------------
            # Examples
            # ------------------------------------------

            examples = data.get("examples")

            if examples and intent in (
                "definition",
                "explanation",
                "general"
            ):

                response += (
                    "\n\nExamples:\n"
                    + "\n".join(
                        f"- {item}"
                        for item in examples
                    )
                )

            return response

        # ==============================================
        # Fallback
        # ==============================================

        return answer

    # ==================================================
    # PLUGINS
    # ==================================================

    def _run_plugin(self, text):

        plugin = self.brain.plugins.find_plugin(text)

        if plugin is None:
            return None

        try:

            return plugin.run(text)

        except Exception as error:

            print(
                "DEBUG Plugin Error:",
                error
            )

            return None
