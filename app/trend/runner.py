from app.database.repositories.news_processed_repository import NewsProcessedRepository
from app.database.repositories.topic_trend_repository import TopicTrendRepository

from app.trend.service import TrendService


class TrendRunner:

    def __init__(self, db):

        self.news_repository = NewsProcessedRepository(db)

        self.trend_repository = TopicTrendRepository(db)

        self.service = TrendService()

    def run(self):

        print("=" * 60)
        print("TREND ANALYSIS")
        print("=" * 60)

        recent_news = self.news_repository.get_recent_processed(days=7)

        previous_news = self.news_repository.get_previous_processed(
            start_days=14,
            end_days=7,
        )

        print(f"Recent News   : {len(recent_news)}")
        print(f"Previous News : {len(previous_news)}")

        trends = self.service.process(
            recent_news,
            previous_news,
        )

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