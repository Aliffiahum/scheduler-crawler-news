import re

from bs4 import BeautifulSoup


class RSSCleaner:

    # =====================================================
    # Bersihkan HTML
    # =====================================================

    def clean_html(self, text: str | None) -> str | None:

        if text is None:
            return None

        soup = BeautifulSoup(text, "html.parser")

        return soup.get_text(
            separator=" ",
            strip=True
        )

    # =====================================================
    # Bersihkan karakter khusus
    # =====================================================

    def clean_special_characters(self, text: str | None) -> str | None:

        if text is None:
            return None

        text = text.replace("\xa0", " ")
        text = text.replace("\u200b", "")
        text = text.replace("\ufeff", "")

        return text

    # =====================================================
    # Rapikan spasi
    # =====================================================

    def clean_whitespace(self, text: str | None) -> str | None:

        if text is None:
            return None

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # =====================================================
    # Pipeline Cleaning
    # =====================================================

    def clean(self, text: str | None) -> str | None:

        text = self.clean_html(text)

        text = self.clean_special_characters(text)

        text = self.clean_whitespace(text)

        return text