from sqlalchemy.orm import Session, joinedload

from app.database.entities.news_processed import NewsProcessed
from app.database.entities.news_raw import NewsRaw
from app.database.entities.topic import Topic

from app.database.repositories.news_processed_repository import (
    NewsProcessedRepository,
)


class DashboardNewsService:

    def __init__(self, db: Session):

        self.db = db
        self.repo = NewsProcessedRepository(db)

    # =====================================================
    # GET NEWS (PAGINATION)
    # =====================================================

    def get_news(
        self,
        keyword=None,
        category=None,
        sentiment=None,
        sort="latest",
        page=1,
        per_page=20,
    ):

        return self.repo.search(
            keyword=keyword,
            category=category,
            sentiment=sentiment,
            sort=sort,
            page=page,
            per_page=per_page,
        )

    # =====================================================
    # GET CHART DATA (SEMUA DATA TANPA PAGINATION)
    # =====================================================

    def get_chart_data(
        self,
        keyword="",
        category="Semua",
        sentiment="Semua",
        sort="latest",
    ):

        query = (

            self.db.query(NewsProcessed)

            .options(

                joinedload(NewsProcessed.raw_news)
                .joinedload(NewsRaw.source),

                joinedload(NewsProcessed.topic),

            )

        )

        if keyword:

            query = query.join(
                NewsProcessed.raw_news
            ).filter(
                NewsRaw.title.ilike(f"%{keyword}%")
            )

        if category != "Semua":

            query = query.join(
                NewsProcessed.topic
            ).filter(
                Topic.category == category
            )

        if sentiment != "Semua":

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

        return query.all()

    # =====================================================
    # TOTAL NEWS
    # =====================================================

    def total_news(
        self,
        keyword=None,
        category=None,
        sentiment=None,
    ):

        return self.repo.count(
            keyword=keyword,
            category=category,
            sentiment=sentiment,
        )

    # =====================================================
    # CATEGORY
    # =====================================================

    def get_categories(self):

        return self.repo.categories()

    # =====================================================
    # SENTIMENT
    # =====================================================

    def get_sentiments(self):

        return self.repo.sentiments()