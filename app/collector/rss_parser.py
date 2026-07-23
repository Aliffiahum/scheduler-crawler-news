from datetime import datetime

import feedparser
from bs4 import BeautifulSoup


class RSSParser:
    """
    Mengubah XML RSS menjadi list berita.
    """

    def parse(self, xml: str):

        feed = feedparser.parse(xml)

        news = []

        for entry in feed.entries:

            news.append({

                "title": self.clean_html(
                    entry.get("title")
                ),

                "summary": self.clean_html(
                    entry.get("summary")
                ),

                "content": self.clean_html(
                    self.get_content(entry)
                ),

                "url": entry.get("link"),

                "author": entry.get("author"),

                "published_at": self.parse_date(entry)

            })

        return news

    # =====================================================
    # Ambil isi berita
    # =====================================================

    @staticmethod
    def get_content(entry):

        # RSS yang memiliki field content
        if entry.get("content"):

            content = entry.get("content")

            if isinstance(content, list):

                if len(content) > 0:

                    return content[0].get("value")

        # fallback description
        if entry.get("description"):

            return entry.get("description")

        # fallback summary
        if entry.get("summary"):

            return entry.get("summary")

        return None

    # =====================================================
    # Bersihkan HTML
    # =====================================================

    @staticmethod
    def clean_html(text):

        if text is None:

            return None

        soup = BeautifulSoup(
            text,
            "html.parser"
        )

        return soup.get_text(
            separator=" ",
            strip=True
        )

    # =====================================================
    # Parsing tanggal
    # =====================================================

    @staticmethod
    def parse_date(entry):

        if hasattr(entry, "published_parsed"):

            if entry.published_parsed:

                return datetime(
                    *entry.published_parsed[:6]
                )

        return None