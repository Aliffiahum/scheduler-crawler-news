from pathlib import Path

from bertopic import BERTopic
from sentence_transformers import SentenceTransformer

from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer


class TopicLoader:

    _model = None

    def __init__(self):

        if TopicLoader._model is None:

            print("=" * 60)
            print("Loading BERTopic...")
            print("=" * 60)

            embedding_model = SentenceTransformer(
                "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
            )

            vectorizer_model = CountVectorizer(
                ngram_range=(1, 2),
                min_df=5,
            )

            umap_model = UMAP(
                n_neighbors=10,
                n_components=5,
                min_dist=0.0,
                metric="cosine",
                random_state=42,
            )

            hdbscan_model = HDBSCAN(
                min_cluster_size=10,
                min_samples=2,
                metric="euclidean",
                prediction_data=True,
            )

            TopicLoader._model = BERTopic(
                embedding_model=embedding_model,
                vectorizer_model=vectorizer_model,
                umap_model=umap_model,
                hdbscan_model=hdbscan_model,
                calculate_probabilities=True,
                verbose=True,
            )

            print("BERTopic loaded.")

        self.model = TopicLoader._model

    def get_model(self):
        return self.model