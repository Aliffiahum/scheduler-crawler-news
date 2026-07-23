from datetime import datetime
from urllib.parse import urlparse


class RSSValidator:

    # =====================================================
    # Validasi URL
    # =====================================================

    def is_valid_url(self, url: str | None) -> bool:

        if not url:
            return False

        try:

            result = urlparse(url)

            return bool(result.scheme and result.netloc)

        except Exception:

            return False

    # =====================================================
    # Validasi Judul
    # =====================================================

    def is_valid_title(self, title: str | None) -> bool:

        if title is None:
            return False

        if len(title.strip()) < 5:
            return False

        return True

    # =====================================================
    # Validasi Tanggal
    # =====================================================

    def is_valid_date(self, published_at) -> bool:

        return isinstance(published_at, datetime)

    # =====================================================
    # Validasi Berita
    # =====================================================

    def validate(self, news: dict) -> bool:

        if not self.is_valid_title(news.get("title")):
            return False

        if not self.is_valid_url(news.get("url")):
            return False

        if not self.is_valid_date(news.get("published_at")):
            return False

        return True