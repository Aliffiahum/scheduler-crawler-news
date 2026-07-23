from app.sentiment.predictor import SentimentPredictor
from app.database.repositories.news_processed_repository import (
    NewsProcessedRepository,
)


class SentimentService:

    def __init__(
        self,
        predictor: SentimentPredictor,
        repository: NewsProcessedRepository,
    ):

        self.predictor = predictor
        self.repository = repository

    # =====================================================
    # Predict satu berita
    # =====================================================

    def process(self, news):

        text = (
            news.clean_content
            or news.clean_summary
            or news.clean_title
        )

        result = self.predictor.predict(text)

        self.repository.update_sentiment(

            raw_news_id=news.raw_news_id,

            sentiment=result["label"],

            confidence=result["confidence"],

        )

        return result