from app.preprocessing.preprocessing_service import PreprocessingService

from app.database.repositories.news_repository import NewsRepository
from app.database.repositories.news_processed_repository import NewsProcessedRepository


class PreprocessingRunner:

    def __init__(self, db):

        self.db = db

        self.news_repository = NewsRepository(db)

        self.processed_repository = NewsProcessedRepository(db)

        self.service = PreprocessingService()

    # =====================================================
    # Jalankan Preprocessing
    # =====================================================

    def run(self):

        news_list = self.news_repository.get_raw_news()

        total_processed = 0
        total_skip = 0

        print("=" * 60)
        print("PREPROCESSING")
        print("=" * 60)

        for news in news_list:

            # ----------------------------------------
            # Sudah pernah diproses
            # ----------------------------------------

            if self.processed_repository.exists(news.id):

                total_skip += 1
                continue

            # ----------------------------------------
            # Preprocessing
            # ----------------------------------------

            clean_title = self.service.preprocess_for_topic(
                news.title
            )

            clean_summary = self.service.preprocess_for_topic(
                news.summary or ""
            )

            clean_content = self.service.preprocess_for_topic(
                news.content or ""
            )

            # ----------------------------------------
            # Simpan ke database
            # ----------------------------------------

            self.processed_repository.create_processed_news(

                raw_news_id=news.id,

                clean_title=clean_title,

                clean_summary=clean_summary,

                clean_content=clean_content,

            )

            total_processed += 1

            print("-" * 60)
            print(news.title)
            print()
            print("Clean Title :")
            print(clean_title)
            print()
            print("Clean Summary :")
            print(clean_summary)
            print()
            print("Clean Content :")
            print(clean_content)

        print()
        print("=" * 60)
        print("PREPROCESSING SELESAI")
        print("=" * 60)

        print(f"Diproses   : {total_processed}")
        print(f"Skip       : {total_skip}")