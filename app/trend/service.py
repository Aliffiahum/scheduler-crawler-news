from collections import defaultdict

from app.trend.score import TrendScore


class TrendService:

    def __init__(self):

        self.score = TrendScore()

    def process(self, news_list):

        grouped = defaultdict(list)

        for item in news_list:

            if item.topic_id is None:
                continue

            grouped[item.topic_id].append(item)

        if not grouped:
            return []

        max_news = max(
            len(items)
            for items in grouped.values()
        )

        results = []

        for topic_id, items in grouped.items():

            news_count = len(items)

            sentiments = [
                n.sentiment
                for n in items
                if n.sentiment is not None
            ]

            published_dates = [
                n.raw_news.published_at
                for n in items
                if n.raw_news is not None
            ]

            trend_score = self.score.calculate(

                news_count=news_count,

                max_news=max_news,

                sentiments=sentiments,

                published_dates=published_dates,

            )

            results.append(

                {

                    "topic_id": topic_id,

                    "news_count": news_count,

                    "growth_rate": 0,

                    "trend_score": trend_score,

                }

            )

        results.sort(

            key=lambda x: x["trend_score"],

            reverse=True,

        )

        return results