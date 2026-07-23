from app.preprocessing.slang_dictionary import SLANG_DICT


class TextNormalizer:

    # =====================================================
    # Normalisasi Kata
    # =====================================================

    def normalize(
        self,
        text: str,
    ) -> str:

        words = text.split()

        normalized = []

        for word in words:

            normalized.append(

                SLANG_DICT.get(
                    word,
                    word,
                )

            )

        return " ".join(normalized)