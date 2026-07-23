import requests


class RSSFetcher:
    """
    Bertugas mengambil XML dari RSS Feed.
    Tidak melakukan parsing.
    """

    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    def fetch(self, rss_url: str) -> str:

        headers = {
            "User-Agent": "EditorialInsightAI/1.0"
        }

        response = requests.get(
            rss_url,
            headers=headers,
            timeout=self.timeout
        )

        response.raise_for_status()

        return response.text