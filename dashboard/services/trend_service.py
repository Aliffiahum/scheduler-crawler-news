from app.database.repositories.topic_trend_repository import (
    TopicTrendRepository,
)


class DashboardTrendService:

    def __init__(self, db):

        self.repo = TopicTrendRepository(db)

    # =====================================================
    # GET TREND
    # =====================================================

    def get_trends(self):

        return self.repo.get_all()