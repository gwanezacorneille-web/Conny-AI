from conny_network import is_online
from conny_online import search_online


def handle_online(text):

    if not is_online():
        return None


    answer = search_online(text)


    if answer.startswith("I couldn't"):
        return None


    return (
        "🌐 Online Result:\n\n"
        + answer
    )
