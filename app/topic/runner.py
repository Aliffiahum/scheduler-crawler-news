from collections import Counter

from app.database.repositories.news_processed_repository import (
    NewsProcessedRepository,
)
from app.database.repositories.topic_repository import (
    TopicRepository,
)

from app.topic.service import TopicService


class TopicRunner:

    def __init__(self, db):

        self.db = db

        self.news_repository = NewsProcessedRepository(db)

        self.topic_repository = TopicRepository(db)

        self.service = TopicService()

    # Topic Modeling

    def run(self):

        print("=" * 60)
        print("TOPIC MODELING")
        print("=" * 60)

        news_list = self.news_repository.get_recent_processed(days=7)

        if len(news_list) == 0:

            print("Tidak ada data.")
            return

        documents = []
        news_mapping = []

        for news in news_list:

            text = " ".join(

                filter(

                    None,

                    [

                        news.clean_title,

                        news.clean_summary,

                    ],

                )

            )

            documents.append(text)
            news_mapping.append(news)

        # Topic Modeling
        
        topics, topic_mapping = self.service.process(
            documents
        )

        print("=" * 60)
        print("Distribusi Topic")
        print("=" * 60)
        print(Counter(topics))

        # Simpan Topic

        for topic_number, info in topic_mapping.items():

            topic = self.topic_repository.get_by_bertopic_id(
                topic_number
            )

            keywords = ", ".join(info["keywords"])

            representative_docs = "\n".join(
                info["representative_docs"]
            )

            if topic is None:

                self.topic_repository.create_topic(

                    bertopic_topic_id=topic_number,

                    label=info["label"],

                    category=info["category"],

                    keywords=keywords,

                    representative_docs=representative_docs,

                )

            else:

                self.topic_repository.update_topic(

                    bertopic_topic_id=topic_number,

                    label=info["label"],

                    category=info["category"],

                    keywords=keywords,

                    representative_docs=representative_docs,

                )

        # Pastikan Topic -1 (Lainnya) ada

        other_topic = self.topic_repository.get_by_bertopic_id(-1)

        if other_topic is None:

            other_topic = self.topic_repository.create_topic(

                bertopic_topic_id=-1,

                label="Lainnya",

                category="Lainnya",

                keywords="",

                representative_docs="",

            )
            
        # Update news_processed

        for news, topic_number in zip(news_mapping, topics):

            # ----------------------------
            # Outlier
            # ----------------------------

            if topic_number == -1:

                self.news_repository.update_topic(

                    news.raw_news_id,

                    other_topic.id,

                )

                continue

            topic = self.topic_repository.get_by_bertopic_id(

                topic_number

            )

            if topic is None:
                continue

            self.news_repository.update_topic(

                news.raw_news_id,

                topic.id,

            )

        # ==========================================
        # COMMIT SEKALI
        # ==========================================

        self.db.commit()

        print()

        print("=" * 60)
        print("TOPIC SELESAI")
        print("=" * 60)

        print(f"Jumlah Topic : {len(topic_mapping)}")
        print(f"Jumlah News  : {len(news_list)}")
