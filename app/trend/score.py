from datetime import datetime, timezone


class TrendScore:

    def calculate(

        self,

        news_count,

        max_news,

        sentiments,

        published_dates,

    ):

        # ============================
        # Volume Score
        # ============================

        volume_score = news_count / max_news

        # ============================
        # Sentiment Score
        # ============================

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

        # ============================
        # Freshness Score
        # ============================

        if published_dates:

            latest = max(published_dates)

            now = datetime.now(timezone.utc)

            hours = (

                now - latest

            ).total_seconds() / 3600

            freshness_score = max(

                0,

                1 - hours / 72,

            )

        else:

            freshness_score = 0

        # ============================
        # Final Score
        # ============================

        final_score = (

            volume_score * 0.5
            + sentiment_score * 0.2
            + freshness_score * 0.3

        )

        return round(final_score, 4)