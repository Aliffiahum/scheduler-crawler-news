from app.sentiment.loader import SentimentLoader

loader = SentimentLoader()

print("=" * 50)
print("Model      :", type(loader.get_model()).__name__)
print("Tokenizer  :", type(loader.get_tokenizer()).__name__)
print("Device     :", loader.get_device())
print("=" * 50)
print("Loader berhasil.")