from typing import Optional

from sqlalchemy.orm import Session

from app.database.entities.rss_source import RSSSource
from app.database.repositories.base_repository import BaseRepository


class RSSRepository(BaseRepository[RSSSource]):

    def __init__(self, db: Session):
        super().__init__(db, RSSSource)

    # =====================================================
    # CREATE
    # =====================================================

    def create_source(
        self,
        source_name: str,
        rss_url: str,
        website_url: str | None = None,
        category: str | None = None,
        status: bool = True,
    ) -> RSSSource:

        source = RSSSource(
            source_name=source_name,
            rss_url=rss_url,
            website_url=website_url,
            category=category,
            status=status,
        )

        return self.add(source)

    # =====================================================
    # READ
    # =====================================================

    def get_active_sources(self):

        return (
            self.db.query(RSSSource)
            .filter(RSSSource.status.is_(True))
            .order_by(RSSSource.source_name)
            .all()
        )

    def get_inactive_sources(self):

        return (
            self.db.query(RSSSource)
            .filter(RSSSource.status.is_(False))
            .order_by(RSSSource.source_name)
            .all()
        )

    def find_by_name(
        self,
        source_name: str,
    ) -> Optional[RSSSource]:

        return (
            self.db.query(RSSSource)
            .filter(RSSSource.source_name == source_name)
            .first()
        )

    def find_by_url(
        self,
        rss_url: str,
    ) -> Optional[RSSSource]:

        return (
            self.db.query(RSSSource)
            .filter(RSSSource.rss_url == rss_url)
            .first()
        )

    def exists(
        self,
        rss_url: str,
    ) -> bool:

        return self.find_by_url(rss_url) is not None

    # =====================================================
    # UPDATE
    # =====================================================

    def enable_source(
        self,
        source_id,
    ) -> bool:

        source = self.get_by_id(source_id)

        if source is None:
            return False

        source.status = True

        self.save()

        return True

    def disable_source(
        self,
        source_id,
    ) -> bool:

        source = self.get_by_id(source_id)

        if source is None:
            return False

        source.status = False

        self.save()

        return True

    def update_category(
        self,
        source_id,
        category: str,
    ) -> bool:

        source = self.get_by_id(source_id)

        if source is None:
            return False

        source.category = category

        self.save()

        return True

    # =====================================================
    # STATISTICS
    # =====================================================

    def total_sources(self) -> int:

        return self.count()

    def total_active_sources(self) -> int:

        return len(self.get_active_sources())

    def total_inactive_sources(self) -> int:

        return len(self.get_inactive_sources())