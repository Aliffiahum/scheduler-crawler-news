from app.sentiment import predict_sentiment

texts = [
    "Pelayanan bank ini sangat memuaskan",
    "Harga cabai naik drastis",
    "Cuaca hari ini mendung"
]

for text in texts:
    print("=" * 50)
    print(text)
    print(predict_sentiment(text))