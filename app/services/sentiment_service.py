from app.sentiment import predict_sentiment


def analyze_news(news: dict) -> dict:
    """
    Analisis sentimen satu berita.
    """

    result = predict_sentiment(news["title"])

    return {
        **news,
        "sentiment": result["label"],
        "sentiment_score": result["score"]
    }