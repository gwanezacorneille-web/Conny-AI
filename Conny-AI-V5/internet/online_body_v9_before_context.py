from internet.search import SearchEngine
from internet.news import NewsEngine
from internet.wiki import WikiEngine
from internet.weather import WeatherEngine


class OnlineBody:
    """
    CONNY AI Online Body V8

    Central coordinator for online intelligence.

    Services:
        - Web Search
        - News
        - Wikipedia
        - Weather

    V8 additions:
        - Automatic internet connection detection
        - IntentEngine-aware routing
        - General information search fallback
        - Safe online failure handling
        - Service state tracking
    """

    def __init__(self):

        # ==================================================
        # ONLINE SERVICES
        # ==================================================

        self.search = SearchEngine()
        self.news = NewsEngine()
        self.wiki = WikiEngine()
        self.weather = WeatherEngine()

        # ==================================================
        # STATE
        # ==================================================

        self.last_query = ""
        self.last_result = None
        self.last_service = None

        # ==================================================
        # AUTOMATIC INTERNET DETECTION
        # ==================================================

        self.online = self.check_connection()

    # ======================================================
    # INTERNET CONNECTION CHECK
    # ======================================================

    def check_connection(self):

        try:

            import urllib.request

            request = urllib.request.Request(
                "https://www.google.com",
                method="HEAD",
                headers={
                    "User-Agent": "CONNY-AI/8.0"
                }
            )

            with urllib.request.urlopen(
                request,
                timeout=3
            ):

                print(
                    "DEBUG Online Body: INTERNET AVAILABLE"
                )

                self.online = True

                return True

        except Exception as error:

            print(
                "DEBUG Online Body: INTERNET UNAVAILABLE"
            )

            print(
                "DEBUG Connection Error:",
                error
            )

            self.online = False

            return False
        # ==================================================
        # ONLINE SERVICES
        # ==================================================

        self.search = SearchEngine()
        self.news = NewsEngine()
        self.wiki = WikiEngine()
        self.weather = WeatherEngine()

        # ==================================================
        # STATE
        # ==================================================

        self.last_query = ""
        self.last_result = None
        self.last_service = None

        self.online = self.check_connection()

    # ======================================================
    # MAIN ONLINE PROCESSOR
    # ======================================================

    def process(self, message, intent=None):

        try:

            text = str(message).strip()

            if not text:
                return None

            self.last_query = text
            self.last_result = None
            self.last_service = None

            lower = text.lower()

            print(
                "DEBUG Online Body Intent:",
                intent
            )

            # ==================================================
            # INTENT-BASED ONLINE ROUTING
            # ==================================================

            # ------------------------------------------
            # NEWS
            # ------------------------------------------

            if intent == "news":

                return self._process_news(text)

            # ------------------------------------------
            # WEATHER
            # ------------------------------------------

            if intent == "weather":

                return self._process_weather(text)

            # ------------------------------------------
            # WIKIPEDIA
            # ------------------------------------------

            if intent == "wikipedia":

                return self._process_wikipedia(text)

            # ------------------------------------------
            # GENERAL WEB SEARCH
            # ------------------------------------------

            if intent in (
                "internet_search",
                "current_info"
            ):

                return self._process_search(text)

            # ==================================================
            # KEYWORD-BASED FALLBACK ROUTING
            # ==================================================

            # ------------------------------------------
            # NEWS
            # ------------------------------------------

            if self._is_news_request(lower):

                return self._process_news(text)

            # ------------------------------------------
            # WEATHER
            # ------------------------------------------

            if self._is_weather_request(lower):

                return self._process_weather(text)

            # ------------------------------------------
            # WIKIPEDIA
            # ------------------------------------------

            if self._is_wiki_request(lower):

                return self._process_wikipedia(text)

            # ------------------------------------------
            # GENERAL WEB SEARCH
            # ------------------------------------------

            if self._is_search_request(lower):

                return self._process_search(text)

            # ==================================================
            # NO SERVICE
            # ==================================================

            print(
                "DEBUG Online Body: NO SERVICE"
            )

            return None

        except Exception as error:

            print(
                "DEBUG Online Body Error:",
                error
            )

            return None

    # ======================================================
    # NEWS PROCESSOR
    # ======================================================

    def _process_news(self, text):

        query = self._clean_news_query(text)

        print(
            "DEBUG Online Body: NEWS"
        )

        print(
            "DEBUG News Query:",
            query
        )

        if not query:

            query = "latest news"

        try:

            result = self.news.get_news(
                query,
                5
            )

            if result:

                self.last_result = result
                self.last_service = "news"

                print(
                    "DEBUG Online Body: NEWS SUCCESS"
                )

                print(
                    "DEBUG Online Body: SUCCESS"
                )

                return result

        except Exception as error:

            print(
                "DEBUG Online Body News Error:",
                error
            )

        print(
            "DEBUG Online Body: NEWS NO RESULT"
        )

        return None

    # ======================================================
    # WEATHER PROCESSOR
    # ======================================================

    def _process_weather(self, text):

        query = self._clean_weather_query(text)

        print(
            "DEBUG Online Body: WEATHER"
        )

        print(
            "DEBUG Weather Query:",
            query
        )

        if not query:

            query = "Kigali"

        try:

            result = self.weather.get_weather(
                query
            )

            if result:

                self.last_result = result
                self.last_service = "weather"

                print(
                    "DEBUG Online Body: WEATHER SUCCESS"
                )

                print(
                    "DEBUG Online Body: SUCCESS"
                )

                return self.weather.format_weather(
                    result
                )

        except Exception as error:

            print(
                "DEBUG Online Body Weather Error:",
                error
            )

        print(
            "DEBUG Online Body: WEATHER NO RESULT"
        )

        return None

    # ======================================================
    # WIKIPEDIA PROCESSOR
    # ======================================================

    def _process_wikipedia(self, text):

        query = self._clean_wiki_query(text)

        print(
            "DEBUG Online Body: WIKIPEDIA"
        )

        print(
            "DEBUG Wiki Query:",
            query
        )

        if not query:

            return None

        try:

            result = self.wiki.search(
                query
            )

            if result:

                self.last_result = result
                self.last_service = "wikipedia"

                print(
                    "DEBUG Online Body: WIKIPEDIA SUCCESS"
                )

                print(
                    "DEBUG Online Body: SUCCESS"
                )

                return self._format_wiki(
                    result
                )

        except Exception as error:

            print(
                "DEBUG Online Body Wikipedia Error:",
                error
            )

        print(
            "DEBUG Online Body: WIKIPEDIA NO RESULT"
        )

        return None

    # ======================================================
    # SEARCH PROCESSOR
    # ======================================================

    def _process_search(self, text):

        query = self._clean_search_query(text)

        print(
            "DEBUG Online Body: SEARCH"
        )

        print(
            "DEBUG Search Query:",
            query
        )

        if not query:

            return None

        try:

            result = self.search.search(
                query
            )

            if result:

                self.last_result = result
                self.last_service = "search"

                print(
                    "DEBUG Online Body: SEARCH SUCCESS"
                )

                print(
                    "DEBUG Online Body: SUCCESS"
                )

                return self.search.format_results(
                    result
                )

        except Exception as error:

            print(
                "DEBUG Online Body Search Error:",
                error
            )

        print(
            "DEBUG Online Body: SEARCH NO RESULT"
        )

        return None

    # ======================================================
    # SEARCH DETECTION
    # ======================================================

    def _is_search_request(self, text):

        return (
            # ------------------------------------------
            # Explicit online searches
            # ------------------------------------------

            text.startswith("search ")
            or text.startswith("search online ")
            or text.startswith("look up ")
            or text.startswith("look online ")
            or text.startswith("find online ")

            # ------------------------------------------
            # General information questions
            #
            # These are used when local knowledge
            # cannot answer the request and the Router
            # falls back to the Online Body.
            # ------------------------------------------

            or text.startswith("who is ")
            or text.startswith("what is ")
            or text.startswith("what are ")
            or text.startswith("tell me about ")
            or text.startswith("where is ")
            or text.startswith("how does ")
            or text.startswith("how do ")
            or text.startswith("why is ")
            or text.startswith("why does ")
        )

    # ======================================================
    # NEWS DETECTION
    # ======================================================

    def _is_news_request(self, text):

        return (
            "latest news" in text
            or "news about" in text
            or "news on" in text
            or text.startswith("news ")
        )

    # ======================================================
    # WEATHER DETECTION
    # ======================================================

    def _is_weather_request(self, text):

        return (
            text.startswith("weather")
            or text.startswith("weather in ")
            or text.startswith("what is the weather")
            or text.startswith("what's the weather")
            or text.startswith("current weather")
            or "weather today" in text
        )

    # ======================================================
    # WIKIPEDIA DETECTION
    # ======================================================

    def _is_wiki_request(self, text):

        return (
            text.startswith("wikipedia ")
            or text.startswith("wiki ")
            or text.startswith("search wikipedia ")
            or text.startswith("look up on wikipedia ")
        )

    # ======================================================
    # CLEAN SEARCH QUERY
    # ======================================================

    def _clean_search_query(self, text):

        query = text.strip()

        prefixes = (
            "search online",
            "search",
            "look online",
            "look up",
            "find online",
            "current information about",
            "current information on",
            "current info about",
            "current info on",
            "latest information about",
            "latest information on",
            "latest info about",
            "latest info on"
        )

        lower = query.lower()

        for prefix in prefixes:

            if lower.startswith(prefix):

                query = query[
                    len(prefix):
                ].strip()

                break

        return query

    # ======================================================
    # CLEAN NEWS QUERY
    # ======================================================

    def _clean_news_query(self, text):

        query = text.strip()

        prefixes = (
            "latest news about",
            "latest news on",
            "latest news",
            "news about",
            "news on",
            "news"
        )

        lower = query.lower()

        for prefix in prefixes:

            if lower.startswith(prefix):

                query = query[
                    len(prefix):
                ].strip()

                break

        return query

    # ======================================================
    # CLEAN WEATHER QUERY
    # ======================================================

    def _clean_weather_query(self, text):

        query = text.strip()

        prefixes = (
            "what is the weather in",
            "what's the weather in",
            "current weather in",
            "weather today in",
            "weather in",
            "current weather",
            "weather"
        )

        lower = query.lower()

        for prefix in prefixes:

            if lower.startswith(prefix):

                query = query[
                    len(prefix):
                ].strip()

                break

        return query

    # ======================================================
    # CLEAN WIKIPEDIA QUERY
    # ======================================================

    def _clean_wiki_query(self, text):

        query = text.strip()

        prefixes = (
            "search wikipedia",
            "look up on wikipedia",
            "wikipedia",
            "wiki"
        )

        lower = query.lower()

        for prefix in prefixes:

            if lower.startswith(prefix):

                query = query[
                    len(prefix):
                ].strip()

                break

        return query

    # ======================================================
    # FORMAT WIKIPEDIA
    # ======================================================

    def _format_wiki(self, result):

        title = result.get(
            "title",
            "Wikipedia"
        )

        answer = result.get(
            "answer",
            ""
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

    # ======================================================
    # STATUS
    # ======================================================

    def get_status(self):

        return {
            "online": self.online,
            "last_query": self.last_query,
            "last_service": self.last_service,
            "last_result": self.last_result
        }
