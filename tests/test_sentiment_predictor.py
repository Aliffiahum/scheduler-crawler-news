from app.sentiment.loader import SentimentLoader
from app.sentiment.predictor import SentimentPredictor


loader = SentimentLoader()

predictor = SentimentPredictor(loader)


text = "Pemerintah berhasil meningkatkan pertumbuhan ekonomi Indonesia."

result = predictor.predict(text)


print("=" * 50)
print(result)
print("=" * 50)