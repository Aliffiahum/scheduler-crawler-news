from app.database.connection import SessionLocal
from app.database.repositories.news_processed_repository import NewsProcessedRepository

from app.topic.service import TopicService


db = SessionLocal()

repository = NewsProcessedRepository(db)

news = repository.get_all_processed()

documents = []

for item in news[:100]:

    text = " ".join(filter(None, [

        item.clean_title,

        item.clean_summary,

        item.clean_content,

    ]))

    documents.append(text)

service = TopicService()

topics, mapping = service.process(documents)

print("=" * 60)

for topic, info in mapping.items():

    print("Topic :", topic)

    print("Category :", info["category"])

    print("Keywords :", info["keywords"])

    print("-" * 60)