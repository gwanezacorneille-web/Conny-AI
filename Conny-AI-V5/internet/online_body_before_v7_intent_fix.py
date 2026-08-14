from internet.search import SearchEngine
from internet.news import NewsEngine
from internet.wiki import WikiEngine
from internet.weather import WeatherEngine


class OnlineBody:
    """
    CONNY AI Online Body V3

    Central coordinator for online intelligence.

    Capabilities:
        - Web search
        - News
        - Wikipedia
    """

    def __init__(self):

        self.search = SearchEngine()
        self.news = NewsEngine()
        self.wiki = WikiEngine()
        self.weather = WeatherEngine()

        self.last_query = ""
        self.last_result = None
        self.online = True

    # ==================================================
    # MAIN ONLINE PROCESSOR
    # ==================================================

    def process(self, message):

        text = str(message).strip()

        if not text:
            return None

        self.last_query = text
        self.last_result = None

        lower = text.lower()

        # ==================================================
        # NEWS
        # ==================================================

        if self._is_news_request(lower):

            query = self._clean_news_query(text)

            print("DEBUG Online Body: NEWS")
            print("DEBUG News Query:", query)

            if not query:
                query = "latest news"

            try:

                result = self.news.get_news(query, 5)

                if result:

                    self.last_result = result

                    print("DEBUG Online Body: NEWS SUCCESS")
                    print("DEBUG Online Body: SUCCESS")

                    return result

            except Exception as error:

                print(
                    "DEBUG Online Body News Error:",
                    error
                )

            print("DEBUG Online Body: NEWS NO RESULT")

            return None

        # ==================================================
        # WEATHER
        # ==================================================

        if self._is_weather_request(lower):

            query = self._clean_weather_query(text)

            print("DEBUG Online Body: WEATHER")
            print("DEBUG Weather Query:", query)

            if not query:
                query = "Kigali"

            try:

                result = self.weather.get_weather(query)

                if result:

                    self.last_result = result

                    print("DEBUG Online Body: WEATHER SUCCESS")
                    print("DEBUG Online Body: SUCCESS")

                    return self.weather.format_weather(result)

            except Exception as error:

                print(
                    "DEBUG Online Body Weather Error:",
                    error
                )

            print("DEBUG Online Body: WEATHER NO RESULT")

            return None

        # ==================================================
        # WIKIPEDIA
        # ==================================================

        if self._is_wiki_request(lower):

            query = self._clean_wiki_query(text)

            print("DEBUG Online Body: WIKIPEDIA")
            print("DEBUG Wiki Query:", query)

            if not query:
                return None

            try:

                result = self.wiki.search(query)

                if result:

                    self.last_result = result

                    print("DEBUG Online Body: WIKIPEDIA SUCCESS")
                    print("DEBUG Online Body: SUCCESS")

                    return self._format_wiki(result)

            except Exception as error:

                print(
                    "DEBUG Online Body Wikipedia Error:",
                    error
                )

            print("DEBUG Online Body: WIKIPEDIA NO RESULT")

            return None

        # ==================================================
        # SEARCH
        # ==================================================

        if self._is_search_request(lower):

            query = self._clean_search_query(text)

            print("DEBUG Online Body: SEARCH")
            print("DEBUG Search Query:", query)

            if not query:
                return None

            try:

                result = self.search.search(query)

                if result:

                    self.last_result = result

                    print("DEBUG Online Body: SEARCH SUCCESS")
                    print("DEBUG Online Body: SUCCESS")

                    return self.search.format_results(result)

            except Exception as error:

                print(
                    "DEBUG Online Body Search Error:",
                    error
                )

            print("DEBUG Online Body: SEARCH NO RESULT")

            return None

        # ==================================================
        # NO ONLINE SERVICE MATCH
        # ==================================================

        print("DEBUG Online Body: NO SERVICE")

        return None

    # ==================================================
    # SEARCH DETECTION
    # ==================================================

    def _is_search_request(self, text):

        return (
            text.startswith("search ")
            or text.startswith("search online ")
            or text.startswith("look up ")
            or text.startswith("look online ")
            or text.startswith("find online ")
        )

    # ==================================================
    # NEWS DETECTION
    # ==================================================

    def _is_news_request(self, text):

        return (
            "latest news" in text
            or "news about" in text
            or text.startswith("news ")
        )

    # ==================================================
    # WEATHER DETECTION
    # ==================================================

    def _is_weather_request(self, text):

        return (
            text.startswith("weather")
            or text.startswith("weather in ")
            or text.startswith("what is the weather")
            or text.startswith("what's the weather")
            or "current weather" in text
        )

    # ==================================================
    # CLEAN WEATHER QUERY
    # ==================================================

    def _clean_weather_query(self, text):

        query = text.strip()

        prefixes = [
            "what is the weather in",
            "what's the weather in",
            "current weather in",
            "weather in",
            "weather"
        ]

        lower = query.lower()

        for prefix in prefixes:

            if lower.startswith(prefix):

                query = query[len(prefix):].strip()

                break

        return query

    # ==================================================
    # WIKIPEDIA DETECTION
    # ==================================================

    def _is_wiki_request(self, text):

        return (
            text.startswith("wikipedia ")
            or text.startswith("wiki ")
            or text.startswith("search wikipedia ")
            or text.startswith("look up on wikipedia ")
        )

    # ==================================================
    # CLEAN SEARCH QUERY
    # ==================================================

    def _clean_search_query(self, text):

        query = text.strip()

        prefixes = [
            "search online",
            "search",
            "look online",
            "look up",
            "find online"
        ]

        lower = query.lower()

        for prefix in prefixes:

            if lower.startswith(prefix):

                query = query[len(prefix):].strip()

                break

        return query

    # ==================================================
    # CLEAN NEWS QUERY
    # ==================================================

    def _clean_news_query(self, text):

        query = text.strip()

        prefixes = [
            "latest news about",
            "latest news on",
            "latest news",
            "news about",
            "news on",
            "news"
        ]

        lower = query.lower()

        for prefix in prefixes:

            if lower.startswith(prefix):

                query = query[len(prefix):].strip()

                break

        return query

    # ==================================================
    # CLEAN WIKIPEDIA QUERY
    # ==================================================

    def _clean_wiki_query(self, text):

        query = text.strip()

        prefixes = [
            "search wikipedia",
            "look up on wikipedia",
            "wikipedia",
            "wiki"
        ]

        lower = query.lower()

        for prefix in prefixes:

            if lower.startswith(prefix):

                query = query[len(prefix):].strip()

                break

        return query

    # ==================================================
    # FORMAT WIKIPEDIA
    # ==================================================

    def _format_wiki(self, result):

        title = result.get(
            "title",
            "Wikipedia"
        )

        answer = result.get(
            "answer"
        )

        url = result.get(
            "url"
        )

        response = (
            f"{title}\n\n"
            f"{answer}"
        )

        if url:

            response += (
                f"\n\nSource: {url}"
            )

        return response

    # ==================================================
    # STATUS
    # ==================================================

    def get_status(self):

        return {
            "online": self.online,
            "last_query": self.last_query,
            "last_result": self.last_result
        }
