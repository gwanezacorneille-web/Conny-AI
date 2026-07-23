from conny_network import is_online
from modules.search_manager import search_knowledge


def handle_online(text):

    if not is_online():
        return None

    answer = search_knowledge(text)

    if not answer:
        return None

    return (
        "🌐 Online Result:\n\n"
        + answer
    )
