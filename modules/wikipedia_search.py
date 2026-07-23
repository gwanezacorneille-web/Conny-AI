import wikipedia


def search_wikipedia(question):

    try:

        result = wikipedia.summary(
            question,
            sentences=3
        )

        return result


    except Exception:

        return None
