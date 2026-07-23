from app.database.connection import SessionLocal

from app.sentiment.runner import SentimentRunner


db = SessionLocal()

runner = SentimentRunner(db)

runner.run()

db.close()