from app.database.connection import SessionLocal

from app.topic.runner import TopicRunner


db = SessionLocal()

runner = TopicRunner(db)

runner.run()