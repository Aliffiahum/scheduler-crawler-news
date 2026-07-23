import re


class TextCleaner:

    # =====================================================
    # Bersihkan Text Dasar
    # =====================================================

    def clean(
        self,
        text: str | None,
    ) -> str:

        if text is None:

            return ""

        text = text.lower()

        text = re.sub(
            r"http\S+",
            "",
            text,
        )

        text = re.sub(
            r"www\S+",
            "",
            text,
        )

        text = re.sub(
            r"<.*?>",
            " ",
            text,
        )

        text = re.sub(
            r"&\w+;",
            " ",
            text,
        )

        text = re.sub(
            r"[^a-zA-Z0-9\s]",
            " ",
            text,
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()