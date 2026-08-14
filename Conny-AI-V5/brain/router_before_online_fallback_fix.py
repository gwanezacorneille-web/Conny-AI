class Router:
    """
    CONNY AI Request Router V6

    Routes requests between:

        - Conversation
        - Memory
        - Calculator
        - Comparison
        - Coding
        - Internet
        - Local Knowledge
        - Plugins
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

                return (
                    self.brain.response.unknown_response()
                )

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

                if (
                    "thank you" in text
                    or "thanks" in text
                ):

                    return (
                        self.brain.response.thanks_response()
                    )

                if text in (
                    "bye",
                    "goodbye",
                    "see you",
                    "see you soon"
                ):

                    return (
                        self.brain.response.goodbye()
                    )

            # ------------------------------------------
            # INTERNET
            #
            # Only the INTERNET decision goes directly
            # to the Online Body.
            # ------------------------------------------

            if decision == "internet":

                result = self._online(text)

                if result is not None:

                    return result

            # ------------------------------------------
            # CALCULATOR
            # ------------------------------------------

            if decision == "calculator":

                result = self._run_plugin(text)

                if result is not None:

                    return result

            # ------------------------------------------
            # LOCAL KNOWLEDGE
            #
            # Knowledge is checked before going online.
            # ------------------------------------------

            if decision == "knowledge":

                result = self._knowledge(
                    text,
                    intent
                )

                if result is not None:

                    return result

                # Local knowledge failed.
                # Now use the Online Body.

                result = self._online(text)

                if result is not None:

                    return result

            # ------------------------------------------
            # OTHER PLUGINS
            # ------------------------------------------

            result = self._run_plugin(text)

            if result is not None:

                return result

            # ------------------------------------------
            # FINAL KNOWLEDGE ATTEMPT
            # ------------------------------------------

            result = self._knowledge(
                text,
                intent
            )

            if result is not None:

                return result

            # ------------------------------------------
            # FINAL FALLBACK
            # ------------------------------------------

            return (
                self.brain.response.unknown_response()
            )

        except Exception as error:

            print(
                "DEBUG Router Error:",
                error
            )

            return (
                self.brain.response.error_response()
            )

    # ==================================================
    # ONLINE BODY
    # ==================================================

    def _online(self, text):

        try:

            if not self.brain.online:

                return None

            result = self.brain.online.process(
                text
            )

            if result is not None:

                print(
                    "DEBUG Online Body: SUCCESS"
                )

                return result

            print(
                "DEBUG Online Body: NO RESULT"
            )

            return None

        except Exception as error:

            print(
                "DEBUG Online Body Error:",
                error
            )

            return None

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

                content = content[
                    len(prefix):
                ].strip()

                break

        if not content:

            return (
                "What would you like me to remember?"
            )

        lower = content.lower()

        # ------------------------------------------
        # "my X is Y"
        # ------------------------------------------

        if (
            lower.startswith("my ")
            and " is " in lower
        ):

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
        # "X is Y"
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

        return (
            "I can remember it, but please tell me "
            "what the information is, for example: "
            "'remember my favorite language is Python'."
        )

    # ==================================================
    # KNOWLEDGE
    # ==================================================

    def _knowledge(self, text, intent=None):

        try:

            result = self.brain.knowledge.search(
                text
            )

        except Exception as error:

            print(
                "DEBUG Knowledge Error:",
                error
            )

            return None

        if not result:

            return None

        data = result.get(
            "data",
            {}
        )

        # ------------------------------------------
        # Direct answer
        # ------------------------------------------

        answer = data.get(
            "answer"
        )

        if answer and intent not in (
            "functions",
            "examples"
        ):

            return answer

        # ------------------------------------------
        # Functions
        # ------------------------------------------

        if intent == "functions":

            functions = data.get(
                "functions"
            )

            if functions:

                return (
                    f"Functions of "
                    f"{result.get('name', 'this concept')}:\n\n"
                    + "\n".join(
                        f"- {item}"
                        for item in functions
                    )
                )

        # ------------------------------------------
        # Examples
        # ------------------------------------------

        if intent == "examples":

            examples = data.get(
                "examples"
            )

            if examples:

                return (
                    f"Examples of "
                    f"{result.get('name', 'this concept')}:\n\n"
                    + "\n".join(
                        f"- {item}"
                        for item in examples
                    )
                )

        # ------------------------------------------
        # Definition
        # ------------------------------------------

        definition = data.get(
            "definition"
        )

        if definition:

            response = definition

            functions = data.get(
                "functions"
            )

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

            examples = data.get(
                "examples"
            )

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

        return answer

    # ==================================================
    # PLUGINS
    # ==================================================

    def _run_plugin(self, text):

        plugin = self.brain.plugins.find_plugin(
            text
        )

        if plugin is None:

            return None

        try:

            return plugin.run(
                text
            )

        except Exception as error:

            print(
                "DEBUG Plugin Error:",
                error
            )

            return None
