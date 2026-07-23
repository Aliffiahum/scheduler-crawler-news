from app.database.connection import SessionLocal

from app.recommendation.runner import RecommendationRunner


db = SessionLocal()

try:

    runner = RecommendationRunner(db)

    runner.run()

finally:

    db.close()