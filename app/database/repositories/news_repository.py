from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.database.entities.news_raw import NewsRaw
from app.database.entities.enums import NewsStatus
from app.database.repositories.base_repository import BaseRepository


class NewsRepository(BaseRepository[NewsRaw]):

    def __init__(self, db: Session):
        super().__init__(db, NewsRaw)

    # =====================================================
    # CREATE
    # =====================================================

    def create_raw_news(
        self,
        source_id: UUID,
        title: str,
        summary: str | None,
        content: str | None,
        url: str,
        author: str | None,
        published_at: datetime,
    ) -> NewsRaw:

        news = NewsRaw(
            source_id=source_id,
            title=title,
            summary=summary,
            content=content,
            url=url,
            author=author,
            published_at=published_at,
            collected_at=datetime.utcnow(),
            status=NewsStatus.RAW,
        )

        return self.add(news)

    # =====================================================
    # READ
    # =====================================================

    def get_raw_news(self):

        return (
            self.db.query(NewsRaw)
            .order_by(
                NewsRaw.published_at.desc()
            )
            .all()
        )

    def get_raw_news_by_id(
        self,
        news_id: UUID,
    ):

        return (
            self.db.query(NewsRaw)
            .filter(
                NewsRaw.id == news_id
            )
            .first()
        )

    def get_latest_raw_news(
        self,
        limit: int = 10,
    ):

        return (
            self.db.query(NewsRaw)
            .order_by(
                NewsRaw.published_at.desc()
            )
            .limit(limit)
            .all()
        )

    # =====================================================
    # SCHEDULER
    # =====================================================

    def get_unprocessed_news(self):

        """
        Berita yang masih RAW
        (belum masuk preprocessing)
        """

        return (

            self.db.query(NewsRaw)

            .filter(
                NewsRaw.status == NewsStatus.RAW
            )

            .order_by(
                NewsRaw.published_at.asc()
            )

            .all()

        )

    def mark_as_processed(
        self,
        news_id: UUID,
    ):

        news = self.get_raw_news_by_id(news_id)

        if news is None:
            return

        news.status = NewsStatus.PROCESSED

        self.save()

    # =====================================================
    # DUPLICATE CHECK
    # =====================================================

    def exists_by_url(
        self,
        url: str,
    ) -> bool:

        return (

            self.db.query(NewsRaw)

            .filter(
                NewsRaw.url == url
            )

            .first()

            is not None

        )

    # =====================================================
    # DELETE
    # =====================================================

    def delete_raw_news(
        self,
        news_id: UUID,
    ) -> bool:

        news = self.get_raw_news_by_id(news_id)

        if news is None:
            return False

        self.delete(news)

        return True

    # =====================================================
    # STATISTICS
    # =====================================================

    def count_raw_news(self):

        return (

            self.db.query(NewsRaw)

            .count()

        )

    def total_news_today(self):

        today = datetime.utcnow().date()

        return (

            self.db.query(NewsRaw)

            .filter(
                NewsRaw.published_at >= today
            )

            .count()

        )

    def total_news(self):

        return self.count()