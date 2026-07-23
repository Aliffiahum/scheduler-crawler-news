from app.database.connection import SessionLocal
from app.database.repositories.news_processed_repository import NewsProcessedRepository

from bertopic import BERTopic
from sentence_transformers import SentenceTransformer

db = SessionLocal()

repo = NewsProcessedRepository(db)

news = repo.get_all_processed()

documents = [
    " ".join(
        filter(
            None,
            [
                n.clean_title,
                n.clean_summary,
            ]
        )
    )
    for n in news
]

model = BERTopic(
    embedding_model=SentenceTransformer(
        "paraphrase-multilingual-MiniLM-L12-v2"
    ),
    verbose=True,
)

topics, _ = model.fit_transform(documents)

print(model.get_topic_info())