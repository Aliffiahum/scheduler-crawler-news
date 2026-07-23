from sqlalchemy.orm import Session

from dashboard.services.news_service import DashboardNewsService
from dashboard.services.topic_service import DashboardTopicService
from dashboard.services.trend_service import DashboardTrendService
from dashboard.services.recommendation_service import (
    DashboardRecommendationService,
)


class DashboardOverviewService:

    def __init__(self, db: Session):

        self.news_service = DashboardNewsService(db)
        self.topic_service = DashboardTopicService(db)
        self.trend_service = DashboardTrendService(db)
        self.recommendation_service = DashboardRecommendationService(db)

    # =====================================================
    # NEWS
    # =====================================================

    def total_news(self):

        return self.news_service.total_news()

    # =====================================================
    # TOPIC
    # =====================================================

    def total_topics(self):

        return len(self.topic_service.get_topics())

    # =====================================================
    # TREND
    # =====================================================

    def get_trends(self):

        return self.trend_service.get_trends()

    # =====================================================
    # RECOMMENDATION
    # =====================================================

    def get_recommendations(self):

        return self.recommendation_service.get_recommendations()