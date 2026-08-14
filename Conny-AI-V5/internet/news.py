import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET


class NewsEngine:
    """
    CONNY AI News Engine V1

    Retrieves recent news through Google News RSS.
    """

    def __init__(self, timeout=8):

        self.timeout = timeout

        self.last_query = ""
        self.last_results = []

    # ==================================================
    # NEWS SEARCH
    # ==================================================

    def search(self, query, limit=5):

        query = str(query).strip()

        if not query:
            return None

        self.last_query = query
        self.last_results = []

        try:

            encoded = urllib.parse.quote(query)

            url = (
                "https://news.google.com/rss/search"
                "?q=" + encoded +
                "&hl=en-US"
                "&gl=US"
                "&ceid=US:en"
            )

            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "CONNY-AI/5.0"
                }
            )

            with urllib.request.urlopen(
                request,
                timeout=self.timeout
            ) as response:

                raw = response.read()

            root = ET.fromstring(raw)

            results = []

            channel = root.find("channel")

            if channel is None:
                return None

            for item in channel.findall("item"):

                title_node = item.find("title")
                link_node = item.find("link")
                pub_node = item.find("pubDate")
                source_node = item.find("source")

                title = (
                    title_node.text.strip()
                    if title_node is not None
                    and title_node.text
                    else ""
                )

                link = (
                    link_node.text.strip()
                    if link_node is not None
                    and link_node.text
                    else ""
                )

                published = (
                    pub_node.text.strip()
                    if pub_node is not None
                    and pub_node.text
                    else ""
                )

                source = (
                    source_node.text.strip()
                    if source_node is not None
                    and source_node.text
                    else ""
                )

                if not title:
                    continue

                results.append({
                    "title": title,
                    "link": link,
                    "published": published,
                    "source": source
                })

                if len(results) >= limit:
                    break

            self.last_results = results

            if not results:
                return None

            return results

        except Exception as error:

            print(
                "DEBUG NewsEngine Error:",
                error
            )

            return None

    # ==================================================
    # FORMATTED NEWS RESPONSE
    # ==================================================

    def get_news(self, query, limit=5):

        results = self.search(
            query,
            limit=limit
        )

        if not results:
            return None

        response = (
            "Here are the latest results I found "
            "online:\n\n"
        )

        for index, item in enumerate(
            results,
            start=1
        ):

            title = item.get(
                "title",
                "Untitled"
            )

            source = item.get(
                "source",
                ""
            )

            published = item.get(
                "published",
                ""
            )

            response += (
                f"{index}. {title}\n"
            )

            if source:

                response += (
                    f"   Source: {source}\n"
                )

            if published:

                response += (
                    f"   Published: {published}\n"
                )

            response += "\n"

        return response

    # ==================================================
    # STATUS
    # ==================================================

    def get_status(self):

        return {
            "last_query": self.last_query,
            "results": len(self.last_results)
        }
