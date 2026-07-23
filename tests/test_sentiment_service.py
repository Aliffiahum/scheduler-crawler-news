from app.services.sentiment_service import analyze_news

news = {
    "title": "Harga cabai naik drastis",
    "summary": "Harga cabai meningkat di berbagai daerah."
}

print(analyze_news(news))