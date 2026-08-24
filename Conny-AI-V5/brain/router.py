import re
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
            # V12 ABSOLUTE SELF-KNOWLEDGE
            # ==================================================

            absolute_self_knowledge = {
                "why were you created":
                    "I was created as an evolving AI project to understand people, reason about requests, assist users, act when appropriate, verify results, and continuously improve.",

                "what can you do":
                    "I can understand requests, answer questions, reason, use knowledge, search online, help with coding, calculations, technical projects, memory, tools, and other supported tasks.",

                "what is your mission":
                    "My mission is to become a useful, capable, trustworthy, and continuously improving AI assistant.",

                "what technologies do you use":
                    "I am primarily built with Python using a modular architecture containing the Brain, Router, Intent Engine, Decision Engine, Knowledge Engine, Memory, Reasoning, Coding, Internet, Tools, Plugins, Voice, Vision, and web interface.",

                "how are you built":
                    "I am built as a modular Python AI system. Requests pass through language understanding, intent detection, decision making, routing, intelligence modules, and response generation.",

                "tell me about your architecture":
                    "My architecture is modular and includes the Brain, Intent Engine, Decision Engine, Router, Knowledge Engine, Memory, Reasoning Engine, Coding Engine, Internet modules, Tools, Plugins, Voice, Vision, and web interface.",

                "tell me your history":
                    "CONNY AI began at V1 and evolved through successive development versions. Each version expanded its intelligence, architecture, capabilities, and interface. V10 reached major intelligence and routing milestones, V11 introduced the GUI, and V12 focuses on building the full website.",

                "what is v11":
                    "V11 is the CONNY AI GUI development stage.",

                "what is v12":
                    "V12 is the CONNY AI website development stage.",

                "what is v13":
                    "V13 is planned as the CONNY AI desktop application stage.",

                "what is v14":
                    "V14 is planned for security and user accounts.",

                "what is v15":
                    "V15 is planned for final cleaning, finishing, upgrading, and release."
            }

            for phrase, answer in absolute_self_knowledge.items():
                if phrase in lower:
                    return answer

            # ==================================================
            # IDENTITY
            # ==================================================
            #
            # Identity questions must ALWAYS be handled here.
            # They must never fall through to knowledge.
            #

            # ==================================================
            # V12 LEGENDARY CORE IDENTITY
            # ==================================================

            identity_answers = {
                "who are you":
                    "I'm CONNY AI, an evolving personal AI project created by Gwaneza Corneille Karenzi in Rwanda. My current development version is V12.",

                "what is your name":
                    "My name is CONNY AI.",

                "what's your name":
                    "My name is CONNY AI.",

                "whats your name":
                    "My name is CONNY AI.",

                "what are you":
                    "I'm CONNY AI, an evolving personal AI project created by Gwaneza Corneille Karenzi.",

                "who created you":
                    "I was created by Gwaneza Corneille Karenzi in Rwanda.",

                "who made you":
                    "I was created by Gwaneza Corneille Karenzi in Rwanda.",

                "who is your creator":
                    "My creator is Gwaneza Corneille Karenzi.",

                "who is conny":
                    "CONNY AI is an evolving personal AI project created by Gwaneza Corneille Karenzi in Rwanda.",

                "what is conny ai":
                    "CONNY AI is an evolving personal AI project designed to understand, reason, assist, act, verify, and improve.",

                "why were you created":
                    "I was created as an evolving AI project to understand people, reason about requests, assist users, act when appropriate, verify results, and improve over time.",

                "why were you made":
                    "I was created to become a capable, useful, reasoning AI that continuously improves.",

                "what is your purpose":
                    "My purpose is to understand people, reason about requests, assist, act when appropriate, verify results, and continuously improve.",

                "what do you do":
                    "I am designed to understand, reason, assist, act, verify, and improve.",

                "what can you do":
                    "I can understand requests, answer questions, reason, work with knowledge, search online when needed, help with coding, interact with tools, remember information when supported, and assist with technical projects.",

                "what is your core goal":
                    "My core goal is: Understand → Reason → Act → Verify → Improve.",

                "what is your main goal":
                    "My core goal is: Understand → Reason → Act → Verify → Improve.",

                "what is your mission":
                    "My mission is to become a useful, capable, trustworthy, and continuously improving AI assistant.",

                "what version are you":
                    "I am currently in V12, the CONNY AI website development stage.",

                "what is your version":
                    "I am currently in V12, the CONNY AI website development stage.",

                "what are you working on":
                    "I am currently being developed as the CONNY AI website in V12.",

                "what is v12":
                    "V12 is the CONNY AI website development stage.",

                "what is v11":
                    "V11 was the CONNY AI GUI development stage.",

                "what is v13":
                    "V13 is planned as the CONNY AI desktop application stage.",

                "what is v14":
                    "V14 is planned for security and accounts.",

                "what is v15":
                    "V15 is planned for final cleaning, finishing, upgrading, and release.",

                "what is your roadmap":
                    "My roadmap is V11 = GUI, V12 = Website, V13 = Desktop app, V14 = Security and accounts, and V15 = final cleaning, finishing, upgrading, and release.",

                "where are you from":
                    "I am a project created in Rwanda by Gwaneza Corneille Karenzi.",

                "where were you created":
                    "I was created as a project in Rwanda by Gwaneza Corneille Karenzi.",

                "what technologies do you use":
                    "My development uses Python and a modular architecture containing components for routing, reasoning, knowledge, memory, coding, internet access, tools, voice, vision, and web interaction.",

                "how are you built":
                    "I am built as a modular AI system with a brain, router, intent engine, reasoning, knowledge, memory, coding, internet, tools, and a web interface.",

                "tell me about your architecture":
                    "My architecture is modular. It includes language and intent understanding, decision routing, reasoning, knowledge, memory, coding, internet capabilities, tools, and a web interface.",

                "tell me your history":
                    "CONNY AI has evolved through multiple development stages. V10 focused on major routing and intelligence validation, V11 introduced the GUI, and V12 focuses on the website. Future stages are V13 desktop, V14 security and accounts, and V15 final release preparation.",

                "introduce yourself":
                    "I'm CONNY AI, an evolving personal AI project created by Gwaneza Corneille Karenzi in Rwanda. My mission is to Understand → Reason → Act → Verify → Improve."
            }

            # ==================================================
            # V12 SELF-KNOWLEDGE — PROJECT KNOWLEDGE
            # ==================================================

            self_knowledge = {
                "why were you created":
                    "I was created to become an evolving personal AI that can understand people, reason about requests, assist, act when appropriate, verify results, and continuously improve.",

                "what can you do":
                    "I can understand questions, detect intent, reason, use local knowledge, search online when needed, remember information, help with coding, calculations, explanations, and other tasks.",

                "what is your mission":
                    "My mission is to understand, reason, assist, act, verify, and improve while becoming a more capable personal AI.",

                "what technologies do you use":
                    "I am built primarily with Python and a modular AI architecture including a brain, router, intent engine, knowledge engine, memory, reasoning, coding, internet, voice, vision, tools, and a web interface.",

                "how are you built":
                    "I am built as a modular Python AI system. My pipeline includes language understanding, intent detection, decision making, routing, knowledge, reasoning, memory, tools, online intelligence, and response generation.",

                "tell me about your architecture":
                    "My architecture is modular. It includes the Brain, Intent Engine, Decision Engine, Request Router, Knowledge Engine, Memory, Reasoning Engine, Coding Engine, Internet modules, Tools, Plugins, Voice, Vision, and the web interface.",

                "tell me your history":
                    "CONNY AI evolved through multiple development versions. V10 completed the major intelligence and routing tests, V11 introduced the GUI, and V12 is focused on the full website.",

                "what is v11":
                    "V11 is the CONNY AI GUI development stage.",

                "what is v12":
                    "V12 is the CONNY AI website development stage.",

                "what is v13":
                    "V13 is planned as the CONNY AI desktop application stage.",

                "what is v14":
                    "V14 is planned for security and user accounts.",

                "what is v15":
                    "V15 is planned for final cleaning, finishing, upgrading, and releasing CONNY AI."
            }

            for phrase, answer in self_knowledge.items():
                if phrase in lower:
                    return answer

            for phrase, answer in identity_answers.items():
                if phrase in lower:
                    return answer

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
            # CODING
            # ==================================================

            if decision == "coding":

                # ==============================================
                # CODE FIXING
                # ==============================================

                if (
                    text.lower().startswith("fix ")
                    or text.lower().startswith("debug ")
                ):

                    result = self.brain.coding.fix(text)

                    language = result.get("language")
                    issues = result.get("issues", [])
                    code = result.get("code")

                    if code:

                        response = (
                            "I found these issues in "
                            + str(language)
                            + ":\n\n"
                        )

                        for issue in issues:
                            response += "- " + issue + "\n"

                        response += (
                            "\nHere is the corrected code:\n\n"
                            + "```"
                            + str(language)
                            + "\n"
                            + code
                            + "\n"
                            + "```"
                        )

                        return response

                if not self.brain.coding.is_coding_request(text):

                    return (
                        "I understand this is related to programming, "
                        "but I need a clearer coding request."
                    )

                lower = str(text).lower()

                # --------------------------------------------------
                # DEBUG / ANALYSIS REQUEST
                # --------------------------------------------------

                analysis_words = (
                    "debug",
                    "analyze",
                    "analyse",
                    "find the bug",
                    "find bugs",
                    "what is wrong",
                    "what's wrong",
                    "fix this code",
                    "fix my code",
                    "check this code",
                    "check my code",
                    "syntax error"
                )

                if any(
                    word in lower
                    for word in analysis_words
                ):

                    result = self.brain.coding.analyze(text)

                    language = result.get(
                        "language"
                    )

                    issues = result.get(
                        "issues",
                        []
                    )

                    suggestions = result.get(
                        "suggestions",
                        []
                    )

                    if issues:

                        response = (
                            "I found these issues"
                        )

                        if language:

                            response += (
                                " in "
                                + language
                            )

                        response += ":\n\n"

                        for issue in issues:

                            response += (
                                "- "
                                + issue
                                + "\n"
                            )

                        if suggestions:

                            response += (
                                "\nSuggestions:\n\n"
                            )

                            for suggestion in suggestions:

                                response += (
                                    "- "
                                    + suggestion
                                    + "\n"
                                )

                        return response

                    return (
                        "I couldn't find any obvious "
                        "basic problems in the code."
                    )

                # --------------------------------------------------
                # CODE GENERATION
                # --------------------------------------------------

                result = self.brain.coding.generate(text)

                language = result.get(
                    "language"
                )

                code = result.get(
                    "code"
                )

                if language and code:

                    return (
                        "Here is the "
                        + language
                        + " code:\n\n"
                        + "```"
                        + language
                        + "\n"
                        + code
                        + "\n"
                        + "```"
                    )

                if language:

                    return (
                        "I detected a coding request in "
                        + language
                        + ", but I couldn't generate the code yet."
                    )

                return (
                    "I detected a coding request, "
                    "but I couldn't determine the programming language."
                )


            # ==================================================
            # REASONING
            # ==================================================

            if decision == "reasoning":

                result = self.brain.reasoning.analyze(
                    text
                )

                if result is not None:

                    return result

                # V12: If reasoning cannot answer an
                # explanation request, fall back to knowledge.
                knowledge_result = self._knowledge(
                    text,
                    intent="explanation"
                )

                if knowledge_result is not None:

                    return knowledge_result

                return (
                    "I couldn't reason through that yet."
                )
            # ==================================================
            # CALCULATOR
            # ==================================================

            if decision == "calculator":

                # V10 Calculator Engine
                # Handles natural-language arithmetic directly.
                try:

                    result = self.brain.calculator.calculate(
                        text
                    )

                    if result is not None:

                        return self.brain.calculator.format_result(
                            result
                        )

                except Exception as error:

                    print(
                        "DEBUG Calculator Error:",
                        error
                    )

                # Keep plugin support as a fallback.
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
            # V10 AUTOMATIC ONLINE KNOWLEDGE FALLBACK
            # ==================================================

            result = self._auto_online(
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
    # V8 AUTOMATIC ONLINE ROUTING
    # ==================================================

    def _auto_online(
        self,
        text,
        intent=None
    ):
        """
        V8 automatic online fallback.

        Called only after local knowledge fails.

        The user does NOT need to explicitly say
        "search online".
        """

        print(
            "DEBUG V8: AUTO ONLINE ROUTING"
        )

        try:

            if not self.brain.online:

                print(
                    "DEBUG V8: ONLINE BODY DISABLED"
                )

                return None

            # Check actual internet state when available.

            online_state = getattr(
                self.brain.online,
                "online",
                True
            )

            if online_state is False:

                print(
                    "DEBUG V8: INTERNET UNAVAILABLE"
                )

                return None

            result = self.brain.online.process(
                text,
                intent=intent
            )

            if result is not None:

                print(
                    "DEBUG V8: AUTO ONLINE SUCCESS"
                )

                return result

            print(
                "DEBUG V8: AUTO ONLINE NO RESULT"
            )

            return None

        except Exception as error:

            print(
                "DEBUG V8 AUTO ONLINE ERROR:",
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

        # ------------------------------------------
        # Normalize "remember that ..."
        # ------------------------------------------

        if content.lower().startswith("remember that "):
            content = content[
                len("remember that "):
            ].strip()

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
        # NUMERIC COMPARISON
        # ------------------------------------------

        if (
            "what is greater" in lower
            or "which is greater" in lower
            or "what is bigger" in lower
            or "which is bigger" in lower
            or "what is larger" in lower
            or "which is larger" in lower
            or "what is smaller" in lower
            or "which is smaller" in lower
            or "what is less" in lower
            or "which is less" in lower
            or "greater than" in lower
            or "bigger than" in lower
            or "larger than" in lower
            or "less than" in lower
            or "which is greatest" in lower
            or "which is biggest" in lower
            or "which is largest" in lower
            or "which is smallest" in lower
            or "which is least" in lower
            or "which is lowest" in lower
            or "compare" in lower
            or "equal to" in lower
            or "are equal" in lower
            or " equal" in lower
            or "the same" in lower
            or "same as" in lower
        ):


            numbers = [
                float(value)
                for value in re.findall(
                    r"-?\d+(?:\.\d+)?",
                    lower
                )
            ]

            if len(numbers) >= 2:

                # ----------------------------------
                # GREATEST / LARGEST / BIGGEST
                # ----------------------------------

                if (
                    "greatest" in lower
                    or "largest" in lower
                    or "biggest" in lower
                ):

                    greatest = max(numbers)

                    if greatest.is_integer():
                        greatest = int(greatest)

                    return (
                        f"{greatest} is the greatest."
                    )

                # ----------------------------------
                # SMALLEST / LEAST / LOWEST
                # ----------------------------------

                if (
                    "smallest" in lower
                    or "least" in lower
                    or "lowest" in lower
                ):

                    smallest = min(numbers)

                    if smallest.is_integer():
                        smallest = int(smallest)

                    return (
                        f"{smallest} is the smallest."
                    )

                # ----------------------------------
                # TWO-NUMBER VALUES
                # ----------------------------------

                first = numbers[0]
                second = numbers[1]

                # ----------------------------------
                # EQUALITY TWO-NUMBER QUESTION
                # ----------------------------------

                if (
                    "equal to" in lower
                    or "are equal" in lower
                    or "the same" in lower
                    or "same as" in lower
                ):

                    if first == second:
                        return (
                            f"{first} and {second} are equal."
                        )

                    return (
                        f"{first} and {second} are not equal."
                    )

                # ----------------------------------
                # SMALLER / LESS TWO-NUMBER QUESTION
                # ----------------------------------

                if (
                    "smaller" in lower
                    or "less" in lower
                ):

                    if first < second:

                        return (
                            f"{first} is smaller than "
                            f"{second}."
                        )

                    if second < first:

                        return (
                            f"{second} is smaller than "
                            f"{first}."
                        )

                    return (
                        f"{first} and {second} are equal."
                    )

                # ----------------------------------
                # TWO-NUMBER GREATER COMPARISON
                # ----------------------------------

                if first > second:

                    if first.is_integer():
                        first = int(first)

                    if second.is_integer():
                        second = int(second)

                    return (
                        f"{first} is greater than "
                        f"{second}."
                    )

                if second > first:

                    if first.is_integer():
                        first = int(first)

                    if second.is_integer():
                        second = int(second)

                    return (
                        f"{second} is greater than "
                        f"{first}."
                    )

                if first.is_integer():
                    first = int(first)

                if second.is_integer():
                    second = int(second)

                return (
                    f"{first} and {second} are equal."
                )

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
        # PYTHON vs JAVASCRIPT
        # ------------------------------------------

        if (
            "python" in lower
            and "javascript" in lower
        ):

            return (
                "Python vs JavaScript\n\n"

                "Python:\n\n"

                "- High-level, general-purpose programming language\n"
                "- Known for concise and readable syntax\n"
                "- Commonly used for AI, automation, data science "
                "and backend development\n"
                "- Dynamically typed\n\n"

                "JavaScript:\n\n"

                "- High-level programming language primarily used "
                "for web development\n"
                "- Runs natively in web browsers\n"
                "- Also used for backend development with runtimes "
                "such as Node.js\n"
                "- Dynamically typed\n\n"

                "Main difference:\n"
                "Python is widely used for general-purpose programming, "
                "automation, AI and data science, while JavaScript is "
                "especially important for interactive web applications "
                "and can also be used on the server."
            )

        # ------------------------------------------
        # PYTHON vs JAVA
        # ------------------------------------------

        if (
            "python" in lower
            and "java" in lower
            and "javascript" not in lower
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


    # ============================================================
    # V12 RESPONSE QUALITY CLEANER
    # ============================================================

    def _v12_clean_knowledge_response(self, query, result):
        """
        V12 response-quality cleaner.

        Converts structured knowledge/search results into a concise,
        useful natural-language answer instead of exposing raw result
        dumps to the user.
        """

        if not result:
            return None

        # --------------------------------------------------
        # Extract structured data safely
        # --------------------------------------------------

        if isinstance(result, dict):
            name = str(result.get("name", "")).strip()

            data = result.get("data", {})

            if not isinstance(data, dict):
                data = {}

            definition = str(
                data.get("definition", "")
            ).strip()

            answer = str(
                data.get("answer", "")
            ).strip()

            description = str(
                data.get("description", "")
            ).strip()

            # Prefer the most useful concise field.
            if definition:
                response = definition
            elif answer:
                response = answer
            elif description:
                response = description
            else:
                response = ""

            if response:
                response = re.sub(
                    r"^\s*(?:here are the top results.*?:\s*)",
                    "",
                    response,
                    flags=re.IGNORECASE | re.DOTALL,
                ).strip()

                return response

            # --------------------------------------------------
            # Search-result fallback
            # --------------------------------------------------

            items = (
                result.get("results")
                or result.get("items")
                or result.get("data")
            )

            if isinstance(items, list):
                useful = []

                for item in items[:3]:

                    if not isinstance(item, dict):
                        continue

                    title = str(
                        item.get("title")
                        or item.get("name")
                        or ""
                    ).strip()

                    snippet = str(
                        item.get("snippet")
                        or item.get("description")
                        or item.get("text")
                        or ""
                    ).strip()

                    if title and snippet:
                        useful.append(
                            f"{title}: {snippet}"
                        )
                    elif snippet:
                        useful.append(snippet)

                if useful:
                    return "\n\n".join(useful)

            return name or None

        # --------------------------------------------------
        # Plain-text fallback
        # --------------------------------------------------

        if isinstance(result, str):

            cleaned = result.strip()

            cleaned = re.sub(
                r"^\s*here are the top results.*?:\s*",
                "",
                cleaned,
                flags=re.IGNORECASE | re.DOTALL,
            )

            # Remove numbered search-result formatting.
            cleaned = re.sub(
                r"(?m)^\s*\d+[.)]\s*",
                "",
                cleaned,
            )

            return cleaned.strip() or None

        return str(result).strip() or None

    # V12 PYTHON DISAMBIGUATION
    def _v12_normalize_knowledge_query(self, query):
        """
        Prefer Python programming-language knowledge for
        ambiguous questions such as:
            What is Python?
            Explain Python.
            Python programming language
        """

        text = str(query).strip()

        if re.search(
            r"\bpython\b",
            text,
            re.IGNORECASE
        ):
            return re.sub(
                r"\bpython\b",
                "Python programming language",
                text,
                count=1,
                flags=re.IGNORECASE
            )

        return text

    def _knowledge(
        self,
        text,
        intent=None
    ):

        try:

            normalized_query = self._v12_normalize_knowledge_query(
                text
            )

            result = self.brain.knowledge.search(
                normalized_query
            )

        except Exception as error:

            print(
                "DEBUG Knowledge Error:",
                error
            )

            return None

        if not result:

            return None

        self.brain.last_topic = result.get("name")

        data = result.get(
            "data",
            {}
        )

        # ------------------------------------------
        # V9 FOLLOW-UP RESPONSE
        #
        # Progressive follow-ups reveal different
        # parts of the knowledge instead of repeating.
        # ------------------------------------------

        if getattr(
            self.brain,
            "last_followup",
            False
        ):

            related = data.get(
                "related",
                []
            )

            functions = data.get(
                "functions",
                []
            )

            examples = data.get(
                "examples",
                []
            )

            name = result.get(
                "name",
                "this concept"
            )

            depth = getattr(
                self.brain,
                "followup_depth",
                1
            )

            # ------------------------------------------
            # FIRST FOLLOW-UP
            # ------------------------------------------

            if depth == 1 and functions:

                return (
                    "More about "
                    + name
                    + ":\n\n"
                    + "\n".join(
                        f"- {item}"
                        for item in functions
                    )
                )

            # ------------------------------------------
            # SECOND FOLLOW-UP
            # ------------------------------------------

            if depth == 2 and examples:

                return (
                    "Examples of "
                    + name
                    + ":\n\n"
                    + "\n".join(
                        f"- {item}"
                        for item in examples
                    )
                )

            # ------------------------------------------
            # THIRD+ FOLLOW-UP
            # ------------------------------------------

            if related:

                return (
                    "Related concepts to "
                    + name
                    + ":\n\n"
                    + "\n".join(
                        f"- {item}"
                        for item in related
                    )
                )

            # ------------------------------------------
            # FALLBACK
            # ------------------------------------------

            if functions:

                return (
                    "More about "
                    + name
                    + ":\n\n"
                    + "\n".join(
                        f"- {item}"
                        for item in functions
                    )
                )

        # ------------------------------------------
        # Direct answer
        # ------------------------------------------

        answer = data.get(
            "answer"
        )

        if not answer:
            answer = data.get(
                "definition"
            )
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

            return (
                self.brain.response.error_response()
            )

    # ==================================================
    # COMPARISON
    # ==================================================
