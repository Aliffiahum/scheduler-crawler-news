from Sastrawi.StopWordRemover.StopWordRemoverFactory import (
    StopWordRemoverFactory,
)


class StopwordRemover:

    def __init__(self):

        factory = StopWordRemoverFactory()

        self.stopwords = set(
            factory.get_stop_words()
        )

    # =====================================================
    # Remove Stopword
    # =====================================================

    def remove(
        self,
        text: str,
    ) -> str:

        words = text.split()

        filtered = [

            word

            for word in words

            if word not in self.stopwords

        ]

        return " ".join(filtered)