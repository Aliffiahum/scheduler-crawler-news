import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.database.entities.news_processed import NewsProcessed
from app.database.entities.news_raw import NewsRaw
from app.database.entities.topic import Topic


class NewsProcessedRepository:

    def __init__(self, db: Session):
        self.db = db

    # BASE QUERY

    def base_query(self):

        return (

            self.db.query(NewsProcessed)

            .join(NewsProcessed.raw_news)

            .outerjoin(NewsProcessed.topic)

            .options(

                joinedload(NewsProcessed.raw_news)
                .joinedload(NewsRaw.source),

                joinedload(NewsProcessed.topic),

            )

        )

    # CREATE

    def create_processed_news(

        self,

        raw_news_id,

        clean_title,

        clean_summary,

        clean_content,

    ):

        news = NewsProcessed(

            raw_news_id=raw_news_id,

            clean_title=clean_title,

            clean_summary=clean_summary,

            clean_content=clean_content,

        )

        self.db.add(news)

        self.db.commit()

        self.db.refresh(news)

        return news

    # EXISTS

    def exists(

        self,

        raw_news_id,

    ):

        return (

            self.db.query(NewsProcessed)

            .filter(

                NewsProcessed.raw_news_id == raw_news_id

            )

            .first()

            is not None

        )

    # SEARCH

    def search(

        self,

        keyword=None,

        category=None,

        sentiment=None,

        sort="latest",

        page=1,

        per_page=20,

    ):

        query = self.base_query()

        if keyword:

            query = query.filter(

                NewsRaw.title.ilike(f"%{keyword}%")

            )

        if category and category != "Semua":

            query = query.filter(

                Topic.category == category

            )

        if sentiment and sentiment != "Semua":

            query = query.filter(

                NewsProcessed.sentiment == sentiment

            )

        if sort == "latest":

            query = query.order_by(

                NewsProcessed.processed_at.desc()

            )

        else:

            query = query.order_by(

                NewsProcessed.processed_at.asc()

            )

        return (

            query

            .offset((page - 1) * per_page)

            .limit(per_page)

            .all()

        )

    # GET ALL

    def get_all_processed(self):

        return (

            self.base_query()

            .order_by(

                NewsProcessed.processed_at.desc()

            )

            .all()

        )

    # COUNT

    def count(

        self,

        keyword=None,

        category=None,

        sentiment=None,

    ):

        query = (

            self.db.query(

                func.count(NewsProcessed.id)

            )

            .join(NewsProcessed.raw_news)

            .outerjoin(NewsProcessed.topic)

        )

        if keyword:

            query = query.filter(

                NewsRaw.title.ilike(f"%{keyword}%")

            )

        if category and category != "Semua":

            query = query.filter(

                Topic.category == category

            )

        if sentiment and sentiment != "Semua":

            query = query.filter(

                NewsProcessed.sentiment == sentiment

            )

        return query.scalar()

    # CATEGORY

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

            r[0]

            for r in rows

            if r[0]

        ]

    # SENTIMENT

    def sentiments(self):

        rows = (

            self.db.query(

                NewsProcessed.sentiment

            )

            .distinct()

            .order_by(

                NewsProcessed.sentiment

            )

            .all()

        )

        return [

            r[0]

            for r in rows

            if r[0]

        ]

    # UNPROCESSED SENTIMENT

    def get_unprocessed_sentiment(self):

        return (

            self.db.query(NewsProcessed)

            .filter(

                NewsProcessed.sentiment.is_(None)

            )

            .all()

        )

    # UPDATE SENTIMENT

    def update_sentiment(

        self,

        raw_news_id,

        sentiment,

        confidence,

    ):

        news = (

            self.db.query(NewsProcessed)

            .filter(

                NewsProcessed.raw_news_id == raw_news_id

            )

            .first()

        )

        if news:

            news.sentiment = sentiment

            news.sentiment_confidence = confidence

            self.db.commit()

    # UNPROCESSED TOPIC

    def get_unprocessed_topic(self):

        return (

            self.base_query()

            .filter(

                NewsProcessed.topic_id.is_(None)

            )

            .all()

        )

    # UPDATE TOPIC

    def update_topic(

    self,

    raw_news_id,

    topic_id,

    ):

        news = (

            self.db.query(NewsProcessed)

            .filter(

                NewsProcessed.raw_news_id == raw_news_id

            )

            .first()

        )

        if news:

            news.topic_id = topic_id

        return news

    # STATISTICS

    def sentiment_statistics(self):

        rows = (

            self.db.query(

                NewsProcessed.sentiment,

                func.count(NewsProcessed.id)

            )

            .group_by(

                NewsProcessed.sentiment

            )

            .all()

        )

        return {

            sentiment: total

            for sentiment, total in rows

            if sentiment

        }

    def topic_statistics(self):

        return (

            self.db.query(

                Topic.label,

                func.count(NewsProcessed.id)

            )

            .join(

                NewsProcessed,

                Topic.id == NewsProcessed.topic_id

            )

            .group_by(

                Topic.label

            )

            .all()

        )
    
    # RECENT NEWS

    def get_recent_processed(self, days=7):

        start_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)

        return (

            self.base_query()

            .filter(
                NewsProcessed.topic_id.isnot(None),
                NewsRaw.published_at >= start_date,
            )

            .all()

        )

    # PREVIOUS NEWS

    def get_previous_processed(self, start_days=14, end_days=7):

        end_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=end_days)

        start_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=start_days)

        return (

            self.base_query()

            .filter(
                NewsProcessed.topic_id.isnot(None),
                NewsRaw.published_at >= start_date,
                NewsRaw.published_at < end_date,
            )

            .all()

        )