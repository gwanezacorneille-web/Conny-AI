def detect_intent(text):

    text = text.lower().strip()


    # Memory
    if text.startswith("remember "):
        return "memory"


    if "what do you remember" in text:
        return "memory"


    if text.startswith("forget "):
        return "memory"


    # Calculator
    if text.startswith("calculate "):
        return "calculator"


    # Conversation
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

    # Personal profile questions

    profile_questions = [
        "who am i",
        "what is my profile",
        "what is my name",
        "what do you know about me"
    ]


    for question in profile_questions:

        if question in text:

            return "memory"


    # Online knowledge
    question_words = [
        "who",
        "what",
        "when",
        "where",
        "why",
        "how"
    ]

    if any(text.startswith(word + " ") for word in question_words):
        return "online"


    return "conversation"
