from app.database.connection import SessionLocal
from app.database.repositories.news_processed_repository import NewsProcessedRepository

from app.topic.loader import TopicLoader
from app.topic.predictor import TopicPredictor


db = SessionLocal()

repository = NewsProcessedRepository(db)

news_list = repository.get_all_processed()

documents = []

for news in news_list[:100]:

    text = " ".join(filter(None, [
        news.clean_title,
        news.clean_summary,
        news.clean_content
    ]))

    documents.append(text)


loader = TopicLoader()

predictor = TopicPredictor(loader)

topics, probs = predictor.fit(documents)

print("=" * 60)

for doc, topic in zip(documents[:10], topics[:10]):

    print("Topic :", topic)
    print(doc)
    print("-" * 60)

print("=" * 60)

print(predictor.get_topic_info())