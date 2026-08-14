class Router:
    """
    CONNY AI Request Router V7

    Routes requests between:

        - Identity
        - Conversation
        - Memory
        - Calculator
        - Comparison
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

            lower = text.lower().strip()

            # ==================================================
            # IDENTITY
            # ==================================================
            #
            # Identity questions must ALWAYS be handled here.
            # They must never fall through to knowledge.
            #

            identity_phrases = (
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

            if any(
                phrase in lower
                for phrase in identity_phrases
            ):

                return (
                    "I'm CONNY AI, your personal AI assistant."
                )

            # Explicit identity intent

            if intent == "identity":

                return (
                    "I'm CONNY AI, your personal AI assistant."
                )

            # ==================================================
            # EXPLICIT INTENTS
            # ==================================================

            if intent == "greeting":

                return self.brain.response.greeting()

            if intent == "recall":

                return self.brain.memory.show()

            # ==================================================
            # MEMORY
            # ==================================================

            if decision == "memory_recall":

                return self.brain.memory.show()

            if decision == "memory_store":

                return self._store_memory(text)

            # ==================================================
            # CONVERSATION
            # ==================================================

            if decision == "conversation":

                if lower in (
                    "hi",
                    "hello",
                    "hey",
                    "yo",
                    "hiya",
                    "good morning",
                    "good afternoon",
                    "good evening",
                    "good night"
                ):

                    return self.brain.response.greeting()

                if (
                    "thank you" in lower
                    or "thanks" in lower
                    or "thank u" in lower
                ):

                    return (
                        self.brain.response.thanks_response()
                    )

                if lower in (
                    "bye",
                    "goodbye",
                    "see you",
                    "see you soon",
                    "good bye"
                ):

                    return (
                        self.brain.response.goodbye()
                    )

            # ==================================================
            # INTERNET
            #
            # Internet requests stay online.
            #
            # If online search fails, do NOT fall through
            # into unrelated local knowledge.
            # ==================================================

            if decision == "internet":

                result = self._online(
                    text,
                    intent
                )

                if result is not None:

                    return result

                return (
                    "I couldn't find a useful online result "
                    "for that right now."
                )

            # ==================================================
            # CALCULATOR
            # ==================================================

            if decision == "calculator":

                result = self._run_plugin(text)

                if result is not None:

                    return result

                return (
                    "I could not calculate that."
                )

            # ==================================================
            # COMPARISON
            # ==================================================

            if decision == "comparison":

                result = self._comparison(
                    text
                )

                if result is not None:

                    return result

                # If no built-in comparison exists,
                # try local knowledge.

                result = self._knowledge(
                    text,
                    intent
                )

                if result is not None:

                    return result

                # Finally try online.

                result = self._online(
                    text,
                    intent
                )

                if result is not None:

                    return result

                return (
                    "I couldn't find enough information "
                    "to compare those yet."
                )

            # ==================================================
            # LOCAL KNOWLEDGE
            #
            # Offline knowledge first.
            # If unavailable, try online.
            # ==================================================

            if decision == "knowledge":

                result = self._knowledge(
                    text,
                    intent
                )

                if result is not None:

                    return result

                result = self._online(
                    text,
                    intent
                )

                if result is not None:

                    return result

                return (
                    "I don't have a good answer for that "
                    "yet, either locally or online."
                )

            # ==================================================
            # OTHER PLUGINS
            # ==================================================

            result = self._run_plugin(text)

            if result is not None:

                return result

            # ==================================================
            # FINAL LOCAL KNOWLEDGE
            # ==================================================

            result = self._knowledge(
                text,
                intent
            )

            if result is not None:

                return result

            # ==================================================
            # FINAL FALLBACK
            # ==================================================

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

    def _online(
        self,
        text,
        intent=None
    ):

        try:

            if not self.brain.online:

                print(
                    "DEBUG Online Body: DISABLED"
                )

                return None

            result = self.brain.online.process(
                text,
                intent=intent
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

    def _store_memory(
        self,
        text
    ):

        original = text.strip()

        prefixes = (
            "remember ",
            "save ",
            "store ",
            "don't forget ",
            "dont forget "
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
    # COMPARISON
    # ==================================================

    def _comparison(
        self,
        text
    ):

        lower = text.lower().strip()

        # ------------------------------------------
        # RAM vs ROM
        # ------------------------------------------

        if (
            "ram" in lower
            and "rom" in lower
        ):

            return (
                "RAM vs ROM\n\n"

                "RAM (Random Access Memory):\n\n"

                "- Temporary working memory\n"
                "- Stores data and programs currently in use\n"
                "- Fast read/write access\n"
                "- Volatile: data is lost when power is removed\n\n"

                "ROM (Read-Only Memory):\n\n"

                "- Non-volatile memory\n"
                "- Stores persistent instructions such as firmware\n"
                "- Keeps its contents when power is removed\n"
                "- Used for persistent instructions and firmware\n\n"

                "Main difference:\n"
                "RAM is mainly used as temporary working memory, "
                "while ROM is used to retain persistent "
                "instructions or firmware."
            )

        # ------------------------------------------
        # CPU vs GPU
        # ------------------------------------------

        if (
            "cpu" in lower
            and "gpu" in lower
        ):

            return (
                "CPU vs GPU\n\n"

                "CPU (Central Processing Unit):\n\n"

                "- General-purpose processor\n"
                "- Handles a wide variety of tasks\n"
                "- Strong at sequential and complex operations\n"
                "- Usually has fewer, more powerful cores\n\n"

                "GPU (Graphics Processing Unit):\n\n"

                "- Specialized for highly parallel workloads\n"
                "- Designed to process many operations at once\n"
                "- Excellent for graphics, video processing, AI "
                "and other parallel workloads\n"
                "- Usually has many smaller processing cores\n\n"

                "Main difference:\n"
                "A CPU is designed for general-purpose computing, "
                "while a GPU is optimized for massively parallel "
                "operations."
            )

        # ------------------------------------------
        # HDD vs SSD
        # ------------------------------------------

        if (
            "hdd" in lower
            and "ssd" in lower
        ):

            return (
                "HDD vs SSD\n\n"

                "HDD (Hard Disk Drive):\n\n"

                "- Uses spinning magnetic disks\n"
                "- Contains moving mechanical parts\n"
                "- Usually cheaper per unit of storage\n"
                "- Generally slower than an SSD\n\n"

                "SSD (Solid-State Drive):\n\n"

                "- Uses flash memory\n"
                "- Has no moving mechanical parts\n"
                "- Much faster access and boot times\n"
                "- Usually more resistant to physical shock\n\n"

                "Main difference:\n"
                "An HDD stores data magnetically on spinning disks, "
                "while an SSD stores data electronically in flash memory."
            )

        # ------------------------------------------
        # WINDOWS vs LINUX
        # ------------------------------------------

        if (
            "windows" in lower
            and "linux" in lower
        ):

            return (
                "Windows vs Linux\n\n"

                "Windows:\n\n"

                "- Proprietary operating system from Microsoft\n"
                "- Widely used on desktop PCs\n"
                "- Broad commercial software and game support\n"
                "- Generally designed for ease of use\n\n"

                "Linux:\n\n"

                "- Open-source operating-system family\n"
                "- Highly customizable\n"
                "- Common in servers, development and embedded systems\n"
                "- Available in many distributions\n\n"

                "Main difference:\n"
                "Windows is a proprietary operating system, "
                "while Linux is based on open-source software "
                "and offers extensive customization."
            )

        # ------------------------------------------
        # PYTHON vs JAVA
        # ------------------------------------------

        if (
            "python" in lower
            and "java" in lower
        ):

            return (
                "Python vs Java\n\n"

                "Python:\n\n"

                "- High-level programming language\n"
                "- Known for concise and readable syntax\n"
                "- Commonly used for automation, AI, data science "
                "and web development\n"
                "- Dynamically typed\n\n"

                "Java:\n\n"

                "- General-purpose programming language\n"
                "- Statically typed\n"
                "- Common in enterprise software, Android history "
                "and large-scale applications\n"
                "- Runs through the Java Virtual Machine (JVM)\n\n"

                "Main difference:\n"
                "Python generally emphasizes concise, readable code "
                "and rapid development, while Java emphasizes strong "
                "static typing, structure and portability through the JVM."
            )

        return None

    # ==================================================
    # KNOWLEDGE
    # ==================================================

    def _knowledge(
        self,
        text,
        intent=None
    ):

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

    def _run_plugin(
        self,
        text
    ):

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
