import uuid

from datetime import datetime

from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Enum

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.entities.base import Base
from app.database.entities.enums import NewsStatus


class NewsRaw(Base):
    __tablename__ = "news_raw"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    source_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("rss_sources.id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
    )

    content: Mapped[str | None] = mapped_column(
        Text,
    )

    url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    author: Mapped[str | None] = mapped_column(
        String(255),
    )

    published_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    collected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    status: Mapped[NewsStatus] = mapped_column(
        Enum(
            NewsStatus,
            name="news_status",
            create_type=False,
        ),
        default=NewsStatus.RAW,
        nullable=False,
    )

    # =====================================================
    # RELATIONSHIP
    # =====================================================

    source = relationship(
        "RSSSource",
        back_populates="news",
    )

    processed = relationship(
        "NewsProcessed",
        back_populates="raw_news",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<NewsRaw(title='{self.title[:40]}')>"