import pandas as pd
import streamlit as st

from app.database.connection import SessionLocal

from dashboard.services.news_service import DashboardNewsService
from dashboard.services.topic_service import DashboardTopicService
from dashboard.services.trend_service import DashboardTrendService
from dashboard.services.recommendation_service import (
    DashboardRecommendationService,
)

from dashboard.components.metric_cards import show_metrics


# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Editorial Insight AI",
    page_icon="🏠",
    layout="wide",
)

st.title("🏠 Executive Dashboard")
st.caption("Real-time Editorial Insight AI")


# =====================================================
# DATABASE
# =====================================================

db = SessionLocal()

news_service = DashboardNewsService(db)
topic_service = DashboardTopicService(db)
trend_service = DashboardTrendService(db)
recommendation_service = DashboardRecommendationService(db)


# =====================================================
# LOAD DATA
# =====================================================

news = news_service.get_chart_data()

topics = topic_service.get_topics()

trends = trend_service.get_trends()

recommendations = recommendation_service.get_recommendations()


# =====================================================
# METRICS
# =====================================================

high_priority = len(
    [
        r
        for r in recommendations
        if r.score >= 0.8
    ]
)

show_metrics(
    [
        ("📰 News", len(news)),
        ("🏷 Topics", len(topics)),
        ("📈 Trending", len(trends)),
        ("💡 High Priority", high_priority),
    ]
)

st.divider()


# =====================================================
# TOP TRENDING
# =====================================================

left, right = st.columns(2)

with left:

    st.subheader("🔥 Top 5 Trending Topic")

    trend_rows = []

    for trend in trends[:5]:

        trend_rows.append({

            "Topic": trend.topic.label,

            "Category": trend.topic.category,

            "News": trend.news_count,

            "Trend Score": round(
                trend.trend_score,
                3,
            )

        })

    st.dataframe(
        pd.DataFrame(trend_rows),
        use_container_width=True,
        hide_index=True,
    )


# =====================================================
# TOP RECOMMENDATION
# =====================================================

with right:

    st.subheader("💡 Top Recommendation")

    recommendation_rows = []

    for rec in recommendations[:5]:

        recommendation_rows.append({

            "Topic": rec.topic.label,

            "Category": rec.topic.category,

            "Score": round(
                rec.score,
                3,
            ),

            "Reason": rec.reason,

        })

    st.dataframe(
        pd.DataFrame(recommendation_rows),
        use_container_width=True,
        hide_index=True,
    )


st.divider()


# =====================================================
# LATEST NEWS
# =====================================================

st.subheader("📰 Latest News")

latest_rows = []

for item in news[:10]:

    raw = item.raw_news
    topic = item.topic

    latest_rows.append({

        "Title": raw.title,

        "Source": raw.source.source_name
        if raw.source else "-",

        "Category": topic.category
        if topic else "-",

        "Sentiment": item.sentiment,

        "Published": raw.published_at.strftime(
            "%d %b %Y %H:%M"
        )

    })

st.dataframe(
    pd.DataFrame(latest_rows),
    use_container_width=True,
    hide_index=True,
)


st.divider()


# =====================================================
# PIPELINE STATUS
# =====================================================

last_news = news[0].raw_news if len(news) else None

if last_news:

    st.success(
        f"Last update : {last_news.collected_at.strftime('%d %b %Y %H:%M')}"
    )

else:

    st.warning("Belum ada data.")