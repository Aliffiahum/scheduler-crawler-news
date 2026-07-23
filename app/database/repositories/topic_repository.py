from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.database.entities.topic import Topic
from app.database.entities.news_processed import NewsProcessed
from app.database.entities.news_raw import NewsRaw


class TopicRepository:

    def __init__(self, db: Session):
        self.db = db

    # =====================================================
    # BASE QUERY
    # =====================================================

    def base_query(self):

        return (

            self.db.query(Topic)

            .options(

                joinedload(Topic.news)
                .joinedload(NewsProcessed.raw_news)
                .joinedload(NewsRaw.source),

                joinedload(Topic.trend),

                joinedload(Topic.recommendations),

            )

        )

    # =====================================================
    # CREATE
    # =====================================================

    def create_topic(

        self,

        bertopic_topic_id,

        label,

        category,

        keywords,

        representative_docs,

    ):

        topic = Topic(

            bertopic_topic_id=bertopic_topic_id,

            label=label,

            category=category,

            description=None,

            keywords=keywords,

            representative_docs=representative_docs,

        )

        self.db.add(topic)
        self.db.commit()
        self.db.refresh(topic)

        return topic

    # =====================================================
    # GET BY ID
    # =====================================================

    def get_by_id(

        self,

        topic_id,

    ):

        return (

            self.base_query()

            .filter(

                Topic.id == topic_id

            )

            .first()

        )

    # =====================================================
    # GET BY BERTOPIC ID
    # =====================================================

    def get_by_bertopic_id(

        self,

        bertopic_topic_id,

    ):

        return (

            self.base_query()

            .filter(

                Topic.bertopic_topic_id == bertopic_topic_id

            )

            .first()

        )

    # =====================================================
    # UPDATE
    # =====================================================

    def update_topic(

        self,

        bertopic_topic_id,

        label,

        category,

        keywords,

        representative_docs,

    ):

        topic = self.get_by_bertopic_id(
            bertopic_topic_id
        )

        if topic is None:
            return None

        topic.label = label
        topic.category = category
        topic.keywords = keywords
        topic.representative_docs = representative_docs

        self.db.commit()
        self.db.refresh(topic)

        return topic

    # =====================================================
    # DELETE
    # =====================================================

    def delete_topic(

        self,

        topic_id,

    ):

        topic = self.get_by_id(topic_id)

        if topic is None:
            return False

        self.db.delete(topic)

        self.db.commit()

        return True

    # =====================================================
    # SEARCH
    # =====================================================

    def search(

        self,

        keyword=None,

        category=None,

        page=1,

        per_page=20,

    ):

        query = self.base_query()

        if keyword:

            query = query.filter(

                Topic.label.ilike(f"%{keyword}%")

            )

        if category and category != "Semua":

            query = query.filter(

                Topic.category == category

            )

        return (

            query

            .order_by(

                Topic.created_at.desc()

            )

            .offset((page - 1) * per_page)

            .limit(per_page)

            .all()

        )

    # =====================================================
    # GET ALL
    # =====================================================

    def get_all(

        self,

        keyword=None,

        category=None,

    ):

        query = self.base_query()

        if keyword:

            query = query.filter(

                Topic.label.ilike(f"%{keyword}%")

            )

        if category and category != "Semua":

            query = query.filter(

                Topic.category == category

            )

        return (

            query

            .order_by(

                Topic.created_at.desc()

            )

            .all()

        )

    # =====================================================
    # COUNT
    # =====================================================

    def count(

        self,

        keyword=None,

        category=None,

    ):

        query = self.db.query(

            func.count(Topic.id)

        )

        if keyword:

            query = query.filter(

                Topic.label.ilike(f"%{keyword}%")

            )

        if category and category != "Semua":

            query = query.filter(

                Topic.category == category

            )

        return query.scalar()

    # =====================================================
    # CATEGORY LIST
    # =====================================================

    def categories(self):

        rows = (

            self.db.query(

                Topic.category

            )

            .distinct()

            .order_by(

                Topic.category

            )

            .all()

        )

        return [

            row[0]

            for row in rows

            if row[0]

        ]

    # =====================================================
    # STATISTICS
    # =====================================================

    def statistics(self):

        rows = (

            self.db.query(

                Topic.category,

                func.count(Topic.id)

            )

            .group_by(

                Topic.category

            )

            .all()

        )

        return {

            category: total

            for category, total in rows

            if category

        }

    # =====================================================
    # TOTAL NEWS PER TOPIC
    # =====================================================

    def news_count_per_topic(self):

        rows = (

            self.db.query(

                Topic.label,

                func.count(NewsProcessed.id)

            )

            .join(

                NewsProcessed,

                NewsProcessed.topic_id == Topic.id

            )

            .group_by(

                Topic.label

            )

            .order_by(

                func.count(NewsProcessed.id).desc()

            )

            .all()

        )

        return rows