from app.database.repositories.news_processed_repository import (
    NewsProcessedRepository,
)
from app.database.repositories.topic_trend_repository import (
    TopicTrendRepository,
)
from app.database.repositories.recommendation_repository import (
    RecommendationRepository,
)

from app.recommendation.service import RecommendationService


class RecommendationRunner:

    def __init__(self, db):

        self.db = db

        self.news_repository = NewsProcessedRepository(db)

        self.trend_repository = TopicTrendRepository(db)

        self.recommendation_repository = RecommendationRepository(db)

        self.service = RecommendationService()

    def run(self):

        print("=" * 60)
        print("RECOMMENDATION ENGINE")
        print("=" * 60)

        news = self.news_repository.get_all_processed()

        trends = self.trend_repository.get_all()

        trend_mapping = {

            trend.topic_id: trend

            for trend in trends

        }

        recommendations = self.service.process(

            news,

            trend_mapping,

        )

        for rec in recommendations:

            existing = self.recommendation_repository.get_by_topic_id(

                rec["topic_id"]

            )

            if existing is None:

                self.recommendation_repository.create_recommendation(

                    topic_id=rec["topic_id"],

                    score=rec["score"],

                    reason=rec["reason"],

                )

            else:

                self.recommendation_repository.update_recommendation(

                    topic_id=rec["topic_id"],

                    score=rec["score"],

                    reason=rec["reason"],

                )

        print(f"Recommendation dibuat : {len(recommendations)}")