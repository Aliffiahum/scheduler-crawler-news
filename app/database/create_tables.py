from app.database.connection import engine
from app.database.entities.base import Base

# import semua entity
from app.database.entities.rss_source import RSSSource
from app.database.entities.news_raw import NewsRaw
from app.database.entities.news_processed import NewsProcessed
from app.database.entities.topic import Topic
from app.database.entities.topic_trend import TopicTrend
from app.database.entities.recommendation import Recommendation

Base.metadata.create_all(bind=engine)

print("Semua tabel berhasil dibuat.")