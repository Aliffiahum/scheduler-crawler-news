from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.database.entities.topic_trend import TopicTrend


class TopicTrendRepository:

    def __init__(self, db: Session):

        self.db = db

    # =====================================================
    # CREATE
    # =====================================================

    def create_trend(

        self,

        topic_id,

        news_count,

        growth_rate,

        trend_score,

    ):

        trend = TopicTrend(

            topic_id=topic_id,

            news_count=news_count,

            growth_rate=growth_rate,

            trend_score=trend_score,

            updated_at=datetime.utcnow(),

        )

        self.db.add(trend)

        self.db.commit()

        self.db.refresh(trend)

        return trend

    # =====================================================
    # READ
    # =====================================================

    def get_all(self):

        return (

            self.db.query(TopicTrend)

            .options(

                joinedload(TopicTrend.topic)

            )

            .order_by(

                TopicTrend.trend_score.desc()

            )

            .all()

        )

    def get_by_topic_id(

        self,

        topic_id,

    ):

        return (

            self.db.query(TopicTrend)

            .filter(

                TopicTrend.topic_id == topic_id

            )

            .first()

        )

    def get_top_trends(

        self,

        limit=10,

    ):

        return (

            self.db.query(TopicTrend)

            .options(

                joinedload(TopicTrend.topic)

            )

            .order_by(

                TopicTrend.trend_score.desc()

            )

            .limit(limit)

            .all()

        )

    # =====================================================
    # UPDATE
    # =====================================================

    def update_trend(

        self,

        topic_id,

        news_count,

        growth_rate,

        trend_score,

    ):

        trend = self.get_by_topic_id(topic_id)

        if trend is None:
            return

        trend.news_count = news_count
        trend.growth_rate = growth_rate
        trend.trend_score = trend_score
        trend.updated_at = datetime.utcnow()

        self.db.commit()

    # =====================================================
    # DELETE
    # =====================================================

    def delete_trend(

        self,

        topic_id,

    ):

        trend = self.get_by_topic_id(topic_id)

        if trend is None:
            return False

        self.db.delete(trend)

        self.db.commit()

        return True

    # =====================================================
    # STATISTICS
    # =====================================================

    def total_trends(self):

        return (

            self.db.query(TopicTrend)

            .count()

        )

    def average_trend_score(self):

        trends = self.get_all()

        if not trends:
            return 0

        return round(

            sum(

                t.trend_score

                for t in trends

            ) / len(trends),

            4,

        )

    def highest_trend(self):

        return (

            self.db.query(TopicTrend)

            .options(

                joinedload(TopicTrend.topic)

            )

            .order_by(

                TopicTrend.trend_score.desc()

            )

            .first()

        )