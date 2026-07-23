from collections import defaultdict

from app.recommendation.score import RecommendationScore


class RecommendationService:

    def __init__(self):

        self.score = RecommendationScore()

    def process(

        self,

        news_list,

        trend_mapping,

    ):

        grouped = defaultdict(list)

        for news in news_list:

            if news.topic_id is None:
                continue

            grouped[news.topic_id].append(news)

        if not grouped:
            return []

        max_news = max(

            len(items)

            for items in grouped.values()

        )

        recommendations = []

        for topic_id, items in grouped.items():

            trend = trend_mapping.get(topic_id)

            if trend is None:
                continue

            sentiments = [

                item.sentiment

                for item in items

                if item.sentiment is not None

            ]

            published_dates = [

                item.raw_news.published_at

                for item in items

                if item.raw_news is not None

            ]

            recommendation_score = self.score.calculate(

                trend_score=trend.trend_score,

                sentiments=sentiments,

                published_dates=published_dates,

                news_count=len(items),

                max_news=max_news,

            )

            recommendations.append(

                {

                    "topic_id": topic_id,

                    "score": recommendation_score,

                    "reason": self.generate_reason(

                        recommendation_score,

                        len(items),

                        trend.trend_score,

                    ),

                }

            )

        recommendations.sort(

            key=lambda x: x["score"],

            reverse=True,

        )

        return recommendations

    def generate_reason(

        self,

        score,

        news_count,

        trend_score,

    ):

        reasons = []

        if news_count >= 20:
            reasons.append("Volume berita tinggi")

        elif news_count >= 10:
            reasons.append("Volume berita cukup tinggi")

        if trend_score >= 0.8:
            reasons.append("Topik sedang tren")

        elif trend_score >= 0.5:
            reasons.append("Topik cukup aktif")

        if score >= 0.8:
            reasons.append("Layak diprioritaskan")

        elif score >= 0.6:
            reasons.append("Layak dipantau")

        return ", ".join(reasons)