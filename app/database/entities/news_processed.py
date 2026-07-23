import uuid

from datetime import datetime

from sqlalchemy import Text
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import func

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.entities.base import Base


class NewsProcessed(Base):
    __tablename__ = "news_processed"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    raw_news_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("news_raw.id"),
        unique=True,
        nullable=False,
    )

    # =====================================================
    # PREPROCESSING
    # =====================================================

    clean_title: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    clean_summary: Mapped[str | None] = mapped_column(
        Text,
    )

    clean_content: Mapped[str | None] = mapped_column(
        Text,
    )

    # =====================================================
    # SENTIMENT
    # =====================================================

    sentiment: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    sentiment_confidence: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    # =====================================================
    # TOPIC
    # =====================================================

    topic_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("topics.id"),
        nullable=True,
    )

    # =====================================================
    # TIMESTAMP
    # =====================================================

    processed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    raw_news = relationship(
        "NewsRaw",
        back_populates="processed",
    )

    topic = relationship(
        "Topic",
        back_populates="news",
    )

    def __repr__(self):
        return f"<NewsProcessed({self.id})>"