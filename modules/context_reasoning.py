from modules.context_manager import get_context


def handle_context(text):

    context = get_context()

    topic = context.get(
        "last_topic",
        ""
    )

    response = context.get(
        "last_response",
        ""
    )


    if not topic or not response:
        return None



    follow_words = [
        "when",
        "where",
        "who",
        "why",
        "how old",
        "tell me more",
        "more"
    ]


    for word in follow_words:

        if text == word or word in text:

            if "Based on our previous topic" in response:
                return None


            return (
                "Based on our previous topic:\n\n"
                + response
            )


    return None
