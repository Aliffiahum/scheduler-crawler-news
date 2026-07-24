from datetime import datetime, timezone


class TrendScore:

    def calculate(

        self,

        news_count,

        max_news,

        growth_rate,

        sentiments,

        published_dates,

    ):

        # ==================================
        # Volume
        # ==================================

        if max_news == 0:
            volume_score = 0
        else:
            volume_score = news_count / max_news

        # ==================================
        # Growth
        # ==================================

        growth_score = min(
            max(growth_rate, 0),
            1,
        )

        # ==================================
        # Sentiment
        # ==================================

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

        # ==================================
        # Freshness
        # ==================================

        if published_dates:

            latest = max(published_dates)

            now = datetime.now(timezone.utc)

            hours = (

                now - latest

            ).total_seconds() / 3600

            freshness_score = max(

                0,

                1 - (hours / 72),

            )

        else:

            freshness_score = 0

        # ==================================
        # Final Score
        # ==================================

        final_score = (

            volume_score * 0.35
            + growth_score * 0.35
            + sentiment_score * 0.10
            + freshness_score * 0.20

        )

        return round(final_score, 4)