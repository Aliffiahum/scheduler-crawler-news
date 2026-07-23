from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.database.entities.recommendation import Recommendation
from app.database.entities.topic import Topic
from app.database.repositories.base_repository import BaseRepository


class RecommendationRepository(
    BaseRepository[Recommendation]
):

    def __init__(self, db: Session):
        super().__init__(db, Recommendation)

    # =====================================================
    # BASE QUERY
    # =====================================================

    def base_query(self):

        return (

            self.db.query(Recommendation)

            .options(

                joinedload(Recommendation.topic)

            )

        )

    # =====================================================
    # CREATE
    # =====================================================

    def create_recommendation(

        self,

        topic_id,

        score: float,

        reason: str | None = None,

    ):

        recommendation = Recommendation(

            topic_id=topic_id,

            score=score,

            reason=reason,

            created_at=datetime.utcnow(),

        )

        return self.add(recommendation)

    # =====================================================
    # READ
    # =====================================================

    def get_all(self):

        return (

            self.base_query()

            .order_by(

                Recommendation.score.desc()

            )

            .all()

        )

    def get_latest(

        self,

        limit: int = 10,

    ):

        return (

            self.base_query()

            .order_by(

                Recommendation.score.desc()

            )

            .limit(limit)

            .all()

        )

    def get_by_topic_id(

        self,

        topic_id,

    ):

        return (

            self.base_query()

            .filter(

                Recommendation.topic_id == topic_id

            )

            .first()

        )

    def get_by_category(

        self,

        category,

    ):

        return (

            self.base_query()

            .join(Recommendation.topic)

            .filter(

                Topic.category == category

            )

            .order_by(

                Recommendation.score.desc()

            )

            .all()

        )

    # =====================================================
    # UPDATE
    # =====================================================

    def update_recommendation(

        self,

        topic_id,

        score,

        reason=None,

    ):

        recommendation = self.get_by_topic_id(
            topic_id
        )

        if recommendation is None:
            return None

        recommendation.score = score
        recommendation.reason = reason
        recommendation.created_at = datetime.utcnow()

        self.save()

        return recommendation

    # =====================================================
    # DELETE
    # =====================================================

    def delete_by_topic_id(

        self,

        topic_id,

    ):

        recommendation = self.get_by_topic_id(
            topic_id
        )

        if recommendation is None:
            return False

        self.delete(recommendation)

        return True

    # =====================================================
    # STATISTICS
    # =====================================================

    def total_recommendations(self):

        return self.count()

    def top_recommendation(self):

        return (

            self.base_query()

            .order_by(

                Recommendation.score.desc()

            )

            .first()

        )

    def average_score(self):

        recommendations = self.get_all()

        if not recommendations:
            return 0

        return round(

            sum(r.score for r in recommendations)
            / len(recommendations),

            4,

        )