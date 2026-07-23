from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


class Stemmer:

    def __init__(self):

        factory = StemmerFactory()

        self.stemmer = factory.create_stemmer()

    # =====================================================
    # Stem Text
    # =====================================================

    def stem(
        self,
        text: str,
    ) -> str:

        if not text:

            return ""

        return self.stemmer.stem(text)