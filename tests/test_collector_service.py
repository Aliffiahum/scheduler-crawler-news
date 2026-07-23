from app.collector.collector_service import CollectorService

from app.database.connection import SessionLocal


db = SessionLocal()

collector = CollectorService(db)

collector.collect()

db.close()