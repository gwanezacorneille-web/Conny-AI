import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, unquote, quote


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
                    "DEBUG SearchEngine: "
                    "DUCKDUCKGO NO RESULTS — USING MEDIAWIKI FALLBACK"
                )

                fallback = self._search_mediawiki(
                    query
                )

                if fallback:
                    return fallback

                print(
                    "DEBUG SearchEngine: "
                    "NO RESULTS FROM ALL PROVIDERS"
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
    # MEDIAWIKI FALLBACK SEARCH
    # ==================================================

    def _search_mediawiki(self, query):

        query = str(query).strip()

        if not query:
            return None

        # ------------------------------------------
        # Build multiple search strategies
        # ------------------------------------------

        lower = query.lower()

        queries = []

        # ------------------------------------------
        # Semantic query strategies
        # ------------------------------------------

        # "what is the capital of France"
        # -> search the actual subject: France
        if "capital of " in lower:

            subject = lower.split(
                "capital of ",
                1
            )[1].strip()

            if subject:
                queries.append(subject)

        # "who is Albert Einstein"
        # -> search Albert Einstein
        for prefix in (
            "who is ",
            "who was ",
            "what is ",
            "what are ",
            "what's ",
            "where is ",
            "where are ",
            "tell me about ",
            "information about ",
            "explain ",
        ):

            if lower.startswith(prefix):

                subject = query[
                    len(prefix):
                ].strip()

                if subject:
                    queries.append(subject)

                break

        # Original query remains a fallback strategy.
        queries.append(query)

        # Natural-language question cleanup
        prefixes = (
            "what is ",
            "what are ",
            "what's ",
            "who is ",
            "who was ",
            "where is ",
            "where are ",
            "when was ",
            "when did ",
            "tell me about ",
            "information about ",
            "explain ",
        )

        cleaned = lower

        for prefix in prefixes:

            if cleaned.startswith(prefix):
                cleaned = cleaned[
                    len(prefix):
                ].strip()
                break

        if cleaned and cleaned != lower:
            queries.append(cleaned)

        # ------------------------------------------
        # Special high-value question patterns
        # ------------------------------------------

        if "capital of " in lower:

            subject = lower.split(
                "capital of ",
                1
            )[1].strip()

            if subject:
                queries.append(subject)

        # Remove duplicates while preserving order
        unique_queries = []

        for item in queries:

            item = item.strip()

            if (
                item
                and item.lower()
                not in {
                    q.lower()
                    for q in unique_queries
                }
            ):
                unique_queries.append(item)

        # ------------------------------------------
        # Try each strategy
        # ------------------------------------------

        for search_query in unique_queries:

            try:

                url = (
                    "https://en.wikipedia.org/"
                    "w/rest.php/v1/search/page"
                )

                response = requests.get(
                    url,
                    params={
                        "q": search_query,
                        "limit": max(
                            self.max_results,
                            10
                        )
                    },
                    headers={
                        "User-Agent": "CONNY-AI/11.0"
                    },
                    timeout=self.timeout
                )

                response.raise_for_status()

                data = response.json()

                pages = data.get(
                    "pages",
                    []
                )

                if not pages:
                    continue

                scored = []

                original_words = {
                    word.lower()
                    for word in query.split()
                    if len(word) > 2
                }

                search_words = {
                    word.lower()
                    for word in search_query.split()
                    if len(word) > 2
                }

                for page in pages:

                    title = page.get(
                        "title",
                        ""
                    ).strip()

                    description = page.get(
                        "description",
                        ""
                    ).strip()

                    key = page.get(
                        "key",
                        ""
                    ).strip()

                    if not title:
                        continue

                    title_words = {
                        word.lower()
                        for word in title.split()
                        if len(word) > 2
                    }

                    description_words = {
                        word.lower()
                        for word in description.split()
                        if len(word) > 2
                    }

                    # ----------------------------------
                    # Relevance score
                    # ----------------------------------

                    score = 0

                    score += len(
                        title_words & search_words
                    ) * 5

                    score += len(
                        title_words & original_words
                    ) * 3

                    score += len(
                        description_words & original_words
                    )

                    # Exact title/query relationship
                    if title.lower() == search_query.lower():
                        score += 12

                    if search_query.lower() in title.lower():
                        score += 6

                    # Strong preference for exact subject
                    if (
                        "capital of " in lower
                        and cleaned
                        and cleaned.lower() in title.lower()
                    ):
                        score += 15

                    page_url = ""

                    if key:
                        page_url = (
                            "https://en.wikipedia.org/wiki/"
                            + quote(
                                key,
                                safe=""
                            )
                        )

                    scored.append(
                        (
                            score,
                            {
                                "title": title,
                                "url": page_url,
                                "snippet": description
                            }
                        )
                    )

                if not scored:
                    continue

                scored.sort(
                    key=lambda item: item[0],
                    reverse=True
                )

                # ----------------------------------
                # Quality gate
                # ----------------------------------

                best_score = scored[0][0]

                if best_score <= 0:
                    print(
                        "DEBUG SearchEngine: "
                        f"MEDIAWIKI LOW QUALITY "
                        f"FOR QUERY: {search_query}"
                    )
                    continue

                results = [
                    item[1]
                    for item in scored[
                        :self.max_results
                    ]
                ]

                print(
                    "DEBUG SearchEngine: "
                    f"MEDIAWIKI RELEVANT RESULTS "
                    f"USING QUERY: {search_query}"
                )

                return {
                    "type": "search",
                    "query": query,
                    "results": results
                }

            except Exception as error:

                print(
                    "DEBUG SearchEngine MediaWiki Error:",
                    error
                )

        print(
            "DEBUG SearchEngine: "
            "MEDIAWIKI NO QUALITY RESULTS"
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
