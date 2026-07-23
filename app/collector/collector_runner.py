from app.collector.collector_service import CollectorService


class CollectorRunner:

    def __init__(self, db):

        self.db = db
        self.service = CollectorService(db)

    def run(self):

        print("=" * 60)
        print("NEWS COLLECTOR")
        print("=" * 60)

        result = self.service.collect()

        print("=" * 60)
        print("COLLECTOR SELESAI")
        print("=" * 60)
        print(f"Total RSS       : {result['total_sources']}")
        print(f"Diambil         : {result['total_fetched']}")
        print(f"Berita Baru     : {result['saved']}")
        print(f"Duplikat        : {result['duplicates']}")

        return result