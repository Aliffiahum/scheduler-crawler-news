from app.database.connection import SessionLocal
from app.database.repositories.news_repository import NewsRepository

db = SessionLocal()

repo = NewsRepository(db)

print("=" * 50)

print("Total News :", repo.count_raw_news())

print("=" * 50)

latest = repo.get_latest_raw_news(limit=5)

for news in latest:

    print(news.title)

print("=" * 50)

db.close()