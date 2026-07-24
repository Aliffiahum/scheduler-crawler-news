from collections import defaultdict

from app.trend.score import TrendScore


class TrendService:

    def __init__(self):

        self.score = TrendScore()

    def process(self, recent_news, previous_news):

        recent_group = defaultdict(list)
        previous_group = defaultdict(list)

        for item in recent_news:

            if item.topic_id is not None:
                recent_group[item.topic_id].append(item)

        for item in previous_news:

            if item.topic_id is not None:
                previous_group[item.topic_id].append(item)

        if not recent_group:
            return []

        max_news = max(
            len(v)
            for v in recent_group.values()
        )

        results = []

        for topic_id, items in recent_group.items():

            news_count = len(items)

            previous_count = len(
                previous_group.get(topic_id, [])
            )

            if previous_count == 0:

                growth = 100.0 if news_count > 0 else 0.0

            else:

                growth = (
                    (news_count - previous_count)
                    / previous_count
                ) * 100

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
            growth_rate=growth,
            )

            results.append(
                {
                    "topic_id": topic_id,
                    "news_count": news_count,
                    "growth_rate": round(growth, 2),
                    "trend_score": trend_score,
                }
            )

        results.sort(
            key=lambda x: x["trend_score"],
            reverse=True,
        )

        return results