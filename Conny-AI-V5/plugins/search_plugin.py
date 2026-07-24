import urllib.request
import urllib.parse
import json


class SearchPlugin:


    def can_handle(self, message):

        text = message.lower()

        keywords = [
            "search",
            "who is",
            "what is",
            "tell me about",
            "where is"
        ]


        for word in keywords:

            if word in text:

                return True


        return False



    def run(self, message):

        try:

            query = message


            query = query.replace(
                "search",
                ""
            )


            url = (
                "https://api.duckduckgo.com/?q="
                + urllib.parse.quote(query)
                + "&format=json"
            )


            response = urllib.request.urlopen(
                url,
                timeout=5
            )


            data = json.loads(
                response.read()
            )


            if data.get("AbstractText"):

                return data["AbstractText"]


            return (
                "I could not find a direct answer."
            )


        except Exception:

            return (
                "I cannot access the internet right now."
            )
