from app.database.connection import SessionLocal
from app.database.repositories.rss_repository import RSSRepository


db = SessionLocal()

repo = RSSRepository(db)

print("=" * 50)

print("Total RSS :", repo.total_sources())

print("Active :", repo.total_active_sources())

print("Inactive :", repo.total_inactive_sources())

print("=" * 50)

for rss in repo.get_all():

    print(rss.source_name)