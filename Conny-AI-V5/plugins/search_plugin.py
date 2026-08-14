import urllib.request
import urllib.parse
import json


class SearchPlugin:

    def can_handle(self, message):

        text = message.lower().strip()

        keywords = [
            "search",
            "who is",
            "what is",
            "tell me about",
            "where is",
            "what are",
            "how does",
            "how do",
            "why is",
            "why does",
        ]

        return any(keyword in text for keyword in keywords)

    def run(self, message):

        try:

            query = message.strip()

            # Remove common request phrases
            prefixes = [
                "search",
                "tell me about",
                "what is",
                "what are",
                "who is",
                "where is",
                "how does",
                "how do",
                "why is",
                "why does",
            ]

            lower_query = query.lower()

            for prefix in prefixes:

                if lower_query.startswith(prefix):

                    query = query[len(prefix):].strip()

                    break

            if not query:

                return None

            encoded = urllib.parse.quote(query)

            url = (
                "https://api.duckduckgo.com/"
                "?q=" + encoded +
                "&format=json"
                "&no_html=1"
                "&skip_disambig=1"
            )

            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "CONNY-AI/5.0"
                }
            )

            with urllib.request.urlopen(
                request,
                timeout=8
            ) as response:

                data = json.loads(
                    response.read().decode("utf-8")
                )

            # ==========================================
            # Direct answer
            # ==========================================

            abstract = data.get("AbstractText")

            if abstract:

                return abstract

            # ==========================================
            # Related topics
            # ==========================================

            topics = data.get("RelatedTopics", [])

            answers = []

            for topic in topics:

                if not isinstance(topic, dict):
                    continue

                text = topic.get("Text")

                if text:

                    answers.append(text)

                if len(answers) >= 3:
                    break

            if answers:

                return (
                    "I found this online:\n\n"
                    + "\n\n".join(
                        f"- {answer}"
                        for answer in answers
                    )
                )

            # ==========================================
            # No useful result
            # ==========================================

            return None

        except Exception as error:

            print(
                "DEBUG Search Error:",
                error
            )

            return None
