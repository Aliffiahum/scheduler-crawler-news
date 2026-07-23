from app.topic.loader import TopicLoader


class TopicPredictor:

    def __init__(self, loader: TopicLoader):

        self.model = loader.get_model()

    # =====================================================
    # Fit Topic Model
    # =====================================================

    def fit(self, documents: list[str]):

        topics, probabilities = self.model.fit_transform(documents)

        return topics, probabilities

    # =====================================================
    # Topic Information
    # =====================================================

    def get_topic_info(self):

        return self.model.get_topic_info()

    # =====================================================
    # Topic Keywords
    # =====================================================

    def get_keywords(self, topic_number):

        return self.model.get_topic(topic_number)

    # =====================================================
    # Save Model
    # =====================================================

    def save(self, path):

        self.model.save(path)

    # =====================================================
    # Load Existing Model
    # =====================================================

    def load(self, path):

        self.model = self.model.load(path)