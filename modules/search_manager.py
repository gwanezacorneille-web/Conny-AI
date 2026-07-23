from conny_online import search_online


def search_knowledge(question):
    """
    Main knowledge search manager.
    Future versions can search multiple sources.
    """

    answer = search_online(question)

    if answer.startswith("I couldn't"):
        return None

    return answer
