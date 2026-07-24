from conny_online import search_online


def search(query):

    answer = search_online(query)

    if (
        not answer
        or answer.startswith("I couldn't")
    ):
        return None

    return answer
