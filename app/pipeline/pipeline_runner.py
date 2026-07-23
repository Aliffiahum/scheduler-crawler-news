from app.database.connection import SessionLocal

from app.collector.collector_runner import CollectorRunner
from app.preprocessing.preprocessing_runner import PreprocessingRunner
from app.sentiment.runner import SentimentRunner
from app.topic.runner import TopicRunner
from app.trend.runner import TrendRunner
from app.recommendation.runner import RecommendationRunner


class PipelineRunner:

    def run_stage(self, runner_cls):

        db = SessionLocal()

        try:
            runner_cls(db).run()
        finally:
            db.close()

    def run(self):

        print("=" * 70)
        print("EDITORIAL INSIGHT AI PIPELINE")
        print("=" * 70)

        self.run_stage(CollectorRunner)
        self.run_stage(PreprocessingRunner)
        self.run_stage(SentimentRunner)
        self.run_stage(TopicRunner)
        self.run_stage(TrendRunner)
        self.run_stage(RecommendationRunner)

        print("=" * 70)
        print("PIPELINE SELESAI")
        print("=" * 70)