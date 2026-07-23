import uuid

from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import func

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.entities.base import Base


class TopicTrend(Base):
    __tablename__ = "topic_trends"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    topic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("topics.id"),
        unique=True,
    )

    news_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    growth_rate: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    trend_score: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    topic = relationship(
        "Topic",
        back_populates="trend",
    )

    def __repr__(self):
        return f"<TopicTrend(score={self.trend_score})>"