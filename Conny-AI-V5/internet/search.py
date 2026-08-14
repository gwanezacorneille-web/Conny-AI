import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, unquote


class SearchEngine:
    """
    CONNY AI Search Engine V3

    Performs real web searches using DuckDuckGo HTML.

    Features:
        - Web search
        - Result extraction
        - URL cleanup
        - Result formatting
        - Safe error handling
    """

    def __init__(self, timeout=10, max_results=5):

        self.timeout = timeout
        self.max_results = max_results

    # ==================================================
    # SEARCH
    # ==================================================

    def search(self, query):

        query = str(query).strip()

        if not query:
            return None

        try:

            url = "https://html.duckduckgo.com/html/"

            params = {
                "q": query
            }

            headers = {
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(X11; Linux x86_64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/151.0 Safari/537.36"
                )
            }

            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout
            )

            response.raise_for_status()

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            results = []

            # ------------------------------------------
            # DuckDuckGo result blocks
            # ------------------------------------------

            result_blocks = soup.select(
                ".result"
            )

            for block in result_blocks:

                if len(results) >= self.max_results:
                    break

                # --------------------------------------
                # Title
                # --------------------------------------

                title_element = block.select_one(
                    ".result__title"
                )

                if title_element is None:
                    continue

                link = title_element.find(
                    "a"
                )

                if link is None:
                    continue

                title = link.get_text(
                    " ",
                    strip=True
                )

                raw_url = link.get(
                    "href",
                    ""
                )

                if not title or not raw_url:
                    continue

                # --------------------------------------
                # URL
                # --------------------------------------

                clean_url = self._clean_url(
                    raw_url
                )

                # --------------------------------------
                # Snippet
                # --------------------------------------

                snippet_element = block.select_one(
                    ".result__snippet"
                )

                snippet = ""

                if snippet_element:

                    snippet = snippet_element.get_text(
                        " ",
                        strip=True
                    )

                results.append(
                    {
                        "title": title,
                        "url": clean_url,
                        "snippet": snippet
                    }
                )

            # ------------------------------------------
            # No results
            # ------------------------------------------

            if not results:

                print(
                    "DEBUG SearchEngine: NO RESULTS"
                )

                return None

            print(
                f"DEBUG SearchEngine: "
                f"{len(results)} RESULTS"
            )

            return {
                "type": "search",
                "query": query,
                "results": results
            }

        except Exception as error:

            print(
                "DEBUG SearchEngine Error:",
                error
            )

            return None

    # ==================================================
    # URL CLEANER
    # ==================================================

    def _clean_url(self, url):

        if not url:
            return ""

        # ------------------------------------------
        # Protocol-relative URL
        # ------------------------------------------

        if url.startswith("//"):

            url = "https:" + url

        # ------------------------------------------
        # DuckDuckGo redirect
        # ------------------------------------------

        if "duckduckgo.com/l/" in url:

            try:

                parsed = urlparse(url)

                params = parse_qs(
                    parsed.query
                )

                destination = params.get(
                    "uddg"
                )

                if destination:

                    return unquote(
                        destination[0]
                    )

            except Exception as error:

                print(
                    "DEBUG URL Cleanup Error:",
                    error
                )

        return url

    # ==================================================
    # FORMAT RESULTS
    # ==================================================

    def format_results(self, data):

        if not data:
            return None

        results = data.get(
            "results",
            []
        )

        if not results:
            return None

        lines = [
            "Here are the top results I found online:\n"
        ]

        for index, result in enumerate(
            results,
            start=1
        ):

            title = result.get(
                "title",
                "Untitled"
            )

            snippet = result.get(
                "snippet",
                ""
            )

            url = result.get(
                "url",
                ""
            )

            lines.append(
                f"{index}. {title}"
            )

            if snippet:

                lines.append(
                    f"   {snippet}"
                )

            if url:

                lines.append(
                    f"   {url}"
                )

            lines.append("")

        return "\n".join(lines).strip()
