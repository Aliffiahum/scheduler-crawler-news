from app.preprocessing.preprocessing_service import PreprocessingService

service = PreprocessingService()

text = """

Pemerintah gk meningkatkan pembangunan infrastruktur yg sangat penting!!!

"""

print("=" * 50)

print("Sentiment")

print(service.preprocess_for_sentiment(text))

print("=" * 50)

print("Topic")

print(service.preprocess_for_topic(text))