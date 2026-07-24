def detect_intent(text):

    text = text.lower().strip()


    # -------------------------
    # Memory
    # -------------------------

    if text.startswith("remember "):
        return "memory"

    if text.startswith("forget "):
        return "memory"

    if (
        "what do you remember" in text
        or "show my memories" in text
        or "who am i" in text
        or "what is my profile" in text
        or "what is my name" in text
        or "what do you know about me" in text
    ):
        return "memory"


    # -------------------------
    # Calculator
    # -------------------------

    if text.startswith("calculate "):
        return "calculator"


    # -------------------------
    # Online Knowledge
    # -------------------------

    online_patterns = [

        "who",
        "what",
        "when",
        "where",
        "why",
        "how",

        "tell me about",
        "define",
        "search",
        "search for",
        "information about",
        "explain"

    ]


    for pattern in online_patterns:

        if text.startswith(pattern):
            return "online"


    # -------------------------
    # Conversation
    # -------------------------

    greetings = [

        "hello",
        "hi",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"

    ]

    if text in greetings:
        return "conversation"


    return "conversation"
