from app.database.repositories.recommendation_repository import (
    RecommendationRepository,
)


class DashboardRecommendationService:

    def __init__(self, db):

        self.repo = RecommendationRepository(db)

    # =====================================================
    # GET RECOMMENDATIONS
    # =====================================================

    def get_recommendations(self):

        return self.repo.get_all()