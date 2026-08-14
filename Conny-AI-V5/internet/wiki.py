import requests

class WikiEngine:
    """
    CONNY AI Wikipedia Engine V1
    """

    def __init__(self, timeout=8):
        self.timeout = timeout

    def search(self, query):
        query = str(query).strip()

        if not query:
            return None

        try:
            url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + requests.utils.quote(query)

            response = requests.get(
                url,
                headers={
                    "User-Agent": "CONNY-AI/5.0"
                },
                timeout=self.timeout
            )

            if response.status_code != 200:
                print("DEBUG WikiEngine: NO RESULT")
                return None

            data = response.json()

            extract = data.get("extract")

            if not extract:
                return None

            print("DEBUG WikiEngine: SUCCESS")

            return {
                "type": "wikipedia",
                "title": data.get("title", query),
                "answer": extract,
                "url": data.get("content_urls", {})
                    .get("desktop", {})
                    .get("page")
            }

        except Exception as error:

            print(
                "DEBUG WikiEngine Error:",
                error
            )

            return None
