from app.sentiment.loader import SentimentLoader
from app.sentiment.predictor import SentimentPredictor
from app.sentiment.service import SentimentService

from app.database.repositories.news_processed_repository import (
    NewsProcessedRepository,
)


class SentimentRunner:

    def __init__(self, db):

        self.repository = NewsProcessedRepository(db)

        loader = SentimentLoader()
        predictor = SentimentPredictor(loader)

        self.service = SentimentService(
            predictor,
            self.repository,
        )

    def run(self):

        print("=" * 60)
        print("SENTIMENT ANALYSIS")
        print("=" * 60)

        news_list = self.repository.get_unprocessed_sentiment()

        total = 0

        if not news_list:
            print("Tidak ada berita yang perlu diproses.")
            return

        for news in news_list:

            try:

                # simpan dulu title sebelum commit
                title = news.clean_title

                result = self.service.process(news)

                total += 1

                print("-" * 60)
                print(title)
                print(result)

            except Exception as e:

                print("-" * 60)
                print("ERROR :", e)

        print()
        print("=" * 60)
        print("SENTIMENT SELESAI")
        print("=" * 60)
        print(f"Diproses : {total}")