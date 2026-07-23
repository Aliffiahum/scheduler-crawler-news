from app.preprocessing.text_cleaner import TextCleaner
from app.preprocessing.normalizer import TextNormalizer
from app.preprocessing.stopword_remover import StopwordRemover
from app.preprocessing.stemmer import Stemmer


class PreprocessingService:

    def __init__(self):

        self.cleaner = TextCleaner()

        self.normalizer = TextNormalizer()

        self.stopword = StopwordRemover()

        self.stemmer = Stemmer()

    # =====================================================
    # Untuk Sentiment (IndoBERT)
    # =====================================================

    def preprocess_for_sentiment(
        self,
        text: str,
    ) -> str:

        text = self.cleaner.clean(text)

        text = self.normalizer.normalize(text)

        return text

    # =====================================================
    # Untuk Topic Modeling (BERTopic)
    # =====================================================

    def preprocess_for_topic(
        self,
        text: str,
    ) -> str:

        text = self.cleaner.clean(text)

        text = self.normalizer.normalize(text)

        text = self.stopword.remove(text)

        text = self.stemmer.stem(text)

        return text