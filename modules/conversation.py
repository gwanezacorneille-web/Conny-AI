from conny_responses import RESPONSES


def handle_conversation(text):

    text = text.lower().strip()


    for key in RESPONSES:

        if key in text:

            return RESPONSES[key]


    return None
