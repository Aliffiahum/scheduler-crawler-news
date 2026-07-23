from datetime import datetime, timezone


class RecommendationScore:

    def calculate(

        self,

        trend_score: float,

        sentiments: list[str],

        published_dates,

        news_count: int,

        max_news: int,

    ):

        # ===========================
        # Sentiment Score
        # ===========================

        if sentiments:

            positive = sentiments.count("positive")
            neutral = sentiments.count("neutral")
            negative = sentiments.count("negative")

            sentiment_score = (

                positive * 1.0
                + neutral * 0.6
                + negative * 0.3

            ) / len(sentiments)

        else:

            sentiment_score = 0.5

        # ===========================
        # Freshness
        # ===========================

        if published_dates:

            latest = max(published_dates)

            if latest.tzinfo is None:

                latest = latest.replace(
                    tzinfo=timezone.utc
                )

            now = datetime.now(timezone.utc)

            hours = (
                now - latest
            ).total_seconds() / 3600

            freshness = max(
                0,
                1 - hours / 72,
            )

        else:

            freshness = 0

        # ===========================
        # Volume
        # ===========================

        volume = news_count / max_news

        # ===========================
        # Final Score
        # ===========================

        score = (

            trend_score * 0.50

            + sentiment_score * 0.20

            + freshness * 0.20

            + volume * 0.10

        )

        return round(score, 4)