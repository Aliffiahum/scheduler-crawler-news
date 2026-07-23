import uuid

from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import func

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.entities.base import Base


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    bertopic_topic_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    label: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    category: Mapped[str | None] = mapped_column(
        String(100),
    )

    description: Mapped[str | None] = mapped_column(
        Text,
    )

    keywords: Mapped[str | None] = mapped_column(
        Text,
    )

    representative_docs: Mapped[str | None] = mapped_column(
        Text,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    news = relationship(
        "NewsProcessed",
        back_populates="topic",
    )

    trend = relationship(
        "TopicTrend",
        back_populates="topic",
        uselist=False,
        cascade="all, delete-orphan",
    )

    recommendations = relationship(
        "Recommendation",
        back_populates="topic",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Topic({self.label})>"