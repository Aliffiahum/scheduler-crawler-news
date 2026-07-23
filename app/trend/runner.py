from app.database.repositories.news_processed_repository import NewsProcessedRepository
from app.database.repositories.topic_trend_repository import TopicTrendRepository

from app.trend.service import TrendService


class TrendRunner:

    def __init__(self, db):

        self.db = db

        self.news_repository = NewsProcessedRepository(db)

        self.trend_repository = TopicTrendRepository(db)

        self.service = TrendService()

    def run(self):

        print("=" * 60)
        print("TREND ANALYSIS")
        print("=" * 60)

        news = self.news_repository.get_all_processed()

        print(f"Total News : {len(news)}")

        trends = self.service.process(news)

        print(f"Topic ditemukan : {len(trends)}")

        for trend in trends:

            existing = self.trend_repository.get_by_topic_id(
                trend["topic_id"]
            )

            if existing is None:

                self.trend_repository.create_trend(

                    topic_id=trend["topic_id"],

                    news_count=trend["news_count"],

                    growth_rate=trend["growth_rate"],

                    trend_score=trend["trend_score"],

                )

            else:

                self.trend_repository.update_trend(

                    topic_id=trend["topic_id"],

                    news_count=trend["news_count"],

                    growth_rate=trend["growth_rate"],

                    trend_score=trend["trend_score"],

                )

        print("=" * 60)
        print("TREND SELESAI")
        print("=" * 60)
        print(f"Trend dihitung : {len(trends)} topic")