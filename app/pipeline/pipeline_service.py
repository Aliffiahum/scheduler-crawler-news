from app.collector.collector_service import CollectorService
from app.preprocessing.preprocessing_runner import PreprocessingRunner


class PipelineService:

    def __init__(self, db):

        self.db = db

        self.collector = CollectorService(db)

        self.preprocessing = PreprocessingRunner(db)

    # =====================================================
    # Jalankan Pipeline
    # =====================================================

    def run(self):

        print()

        print("=" * 60)
        print("PIPELINE DIMULAI")
        print("=" * 60)

        print()

        # ------------------------
        # 1. Collect RSS
        # ------------------------

        print("1. Collecting News...")

        self.collector.collect()

        print()

        # ------------------------
        # 2. Preprocessing
        # ------------------------

        print("2. Preprocessing...")

        self.preprocessing.run()

        print()

        print("=" * 60)
        print("PIPELINE SELESAI")
        print("=" * 60)