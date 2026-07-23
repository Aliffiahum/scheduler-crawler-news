from app.database.connection import SessionLocal
from app.database.entities.news_processed import NewsProcessed

db = SessionLocal()

news = db.query(NewsProcessed).first()

print(news)

print(news.__dict__)

db.close()