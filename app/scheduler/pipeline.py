from app.database.connection import SessionLocal

from app.collector.collector_runner import CollectorRunner
from app.preprocessing.preprocessing_runner import PreprocessingRunner
from app.sentiment.runner import SentimentRunner
from app.topic.runner import TopicRunner
from app.trend.runner import TrendRunner
from app.recommendation.runner import RecommendationRunner


class EditorialPipeline:

    def run(self):

        db = SessionLocal()

        try:

            print("=" * 70)
            print("EDITORIAL INSIGHT AI PIPELINE")
            print("=" * 70)

            # 1
            CollectorRunner(db).run()

            # 2
            PreprocessingRunner(db).run()

            # 3
            SentimentRunner(db).run()

            # 4
            TopicRunner(db).run()

            # 5
            TrendRunner(db).run()

            # 6
            RecommendationRunner(db).run()

            print("=" * 70)
            print("PIPELINE FINISHED")
            print("=" * 70)

        finally:

            db.close()