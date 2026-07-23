from app.topic.loader import TopicLoader
from app.topic.predictor import TopicPredictor

from app.topic.interpreter.factory import TopicInterpreterFactory


class TopicService:

    def __init__(self):

        loader = TopicLoader()

        self.predictor = TopicPredictor(loader)

        self.interpreter = TopicInterpreterFactory.create()

    def process(self, documents: list[str]):

        topics, probabilities = self.predictor.fit(documents)

        topic_info = self.predictor.get_topic_info()

        topic_mapping = {}

        for _, row in topic_info.iterrows():

            topic_id = int(row["Topic"])

            if topic_id == -1:
                continue

            keywords = self.predictor.get_keywords(topic_id)

            keywords = [word for word, _ in keywords]

            category = self.interpreter.interpret(
                keywords
            )

            topic_mapping[topic_id] = {

                "label": row["Name"],

                "category": category,

                "keywords": keywords,

                "representative_docs": row[
                    "Representative_Docs"
                ],

            }

        return topics, topic_mapping