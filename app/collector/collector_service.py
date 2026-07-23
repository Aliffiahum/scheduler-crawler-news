from app.collector.rss_fetcher import RSSFetcher
from app.collector.rss_parser import RSSParser
from app.collector.cleaner import RSSCleaner
from app.collector.validator import RSSValidator

from app.database.repositories.rss_repository import RSSRepository
from app.database.repositories.news_repository import NewsRepository


class CollectorService:

    def __init__(self, db):

        self.db = db

        self.rss_repository = RSSRepository(db)
        self.news_repository = NewsRepository(db)

        self.fetcher = RSSFetcher()
        self.parser = RSSParser()
        self.cleaner = RSSCleaner()
        self.validator = RSSValidator()

    # =====================================================
    # MAIN COLLECTOR
    # =====================================================

    def collect(self):

        rss_sources = self.rss_repository.get_active_sources()

        total_sources = len(rss_sources)
        total_fetched = 0
        total_saved = 0
        total_duplicates = 0
        total_errors = 0

        for source in rss_sources:

            print("=" * 60)
            print(f"Source : {source.source_name}")

            try:

                xml = self.fetcher.fetch(
                    source.rss_url
                )

                news_list = self.parser.parse(xml)

                total_fetched += len(news_list)

                print(f"Fetched : {len(news_list)} berita")

                for news in news_list:

                    result = self.process_news(
                        source,
                        news,
                    )

                    if result == "saved":
                        total_saved += 1

                    elif result == "duplicate":
                        total_duplicates += 1

                    elif result == "error":
                        total_errors += 1

            except Exception as e:

                self.db.rollback()

                total_errors += 1

                print(f"[ERROR] {source.source_name}")
                print(e)

        return {

            "total_sources": total_sources,

            "total_fetched": total_fetched,

            "saved": total_saved,

            "duplicates": total_duplicates,

            "errors": total_errors,

        }

    # =====================================================
    # PROCESS SATU BERITA
    # =====================================================

    def process_news(

        self,

        source,

        news,

    ):

        cleaned_news = {

            "title": self.cleaner.clean(
                news["title"]
            ),

            "summary": self.cleaner.clean(
                news["summary"]
            ),

            "content": self.cleaner.clean(
                news["content"]
            ),

            "url": news["url"],

            "author": news["author"],

            "published_at": news["published_at"],

        }

        # ==========================================
        # VALIDATION
        # ==========================================

        if not self.validator.validate(
            cleaned_news
        ):

            return "error"

        # ==========================================
        # DUPLICATE
        # ==========================================

        if self.news_repository.exists_by_url(
            cleaned_news["url"]
        ):

            return "duplicate"

        # ==========================================
        # SAVE
        # ==========================================

        self.news_repository.create_raw_news(

            source_id=source.id,

            title=cleaned_news["title"],

            summary=cleaned_news["summary"],

            content=cleaned_news["content"],

            url=cleaned_news["url"],

            author=cleaned_news["author"],

            published_at=cleaned_news["published_at"],

        )

        return "saved"