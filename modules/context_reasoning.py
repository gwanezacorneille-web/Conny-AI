from modules.context_manager import get_context


def handle_context(text):

    context = get_context()

    topic = context.get(
        "topic",
        ""
    )

    answer = context.get(
        "answer",
        ""
    )


    if not topic or not answer:
        return None


    follow_phrases = [
        "tell me more",
        "more",
        "explain",
        "continue",
        "go deeper"
    ]


    for phrase in follow_phrases:

        if text == phrase:

            if answer.startswith(
                "🧠 Continuing from our previous topic:"
            ):
                return None


            return (
                "🧠 Continuing from our previous topic:\n\n"
                + answer
            )


    return None
