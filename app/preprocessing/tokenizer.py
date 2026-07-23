class Tokenizer:

    # =====================================================
    # Tokenize
    # =====================================================

    def tokenize(
        self,
        text: str,
    ) -> list[str]:

        if not text:

            return []

        return text.split()