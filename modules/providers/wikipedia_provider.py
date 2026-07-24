import requests


HEADERS = {
    "User-Agent": "CONNY-AI/4.0 (Created by Gwaneza Corneille Karenzi)"
}


def search(query):

    url = (
        "https://en.wikipedia.org/api/rest_v1/page/summary/"
        + query.replace(" ", "_")
    )

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=5
        )

        if response.status_code != 200:
            return None

        data = response.json()

        return data.get("extract")

    except Exception:

        return None
