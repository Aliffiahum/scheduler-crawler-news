from app.database.connection import SessionLocal

from app.trend.runner import TrendRunner


db = SessionLocal()

runner = TrendRunner(db)

runner.run()