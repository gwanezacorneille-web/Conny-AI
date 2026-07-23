import requests


def search_online(question):

    url = "https://api.duckduckgo.com/"

    params = {
        "q": question,
        "format": "json",
        "no_redirect": 1,
        "no_html": 1
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=5
        )

        data = response.json()

        if data.get("AbstractText"):
            return data["AbstractText"]

        elif data.get("Heading"):
            return data["Heading"]

        else:
            return (
                "I couldn't find a good answer online."
            )

    except Exception:

        return (
            "I couldn't connect to the online knowledge service."
        )
