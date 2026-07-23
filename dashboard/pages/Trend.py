import pandas as pd
import streamlit as st

from app.database.connection import SessionLocal

from dashboard.services.trend_service import DashboardTrendService

from dashboard.components.metric_cards import show_metrics
from dashboard.components.bar_chart import show_bar_chart


# =====================================================
# CONFIG
# =====================================================

st.set_page_config(

    page_title="Trend",

    page_icon="📈",

    layout="wide",

)

st.title("📈 Trend Dashboard")


# =====================================================
# DATABASE
# =====================================================

db = SessionLocal()

service = DashboardTrendService(db)

trends = service.get_trends()


# =====================================================
# METRIC
# =====================================================

total_topics = len(trends)

highest_score = max(

    [t.trend_score for t in trends],

    default=0,

)

total_news = sum(

    t.news_count

    for t in trends

)

show_metrics(

    [

        ("Trending Topics", total_topics),

        ("Highest Score", round(highest_score, 2)),

        ("Total News", total_news),

    ]

)

st.markdown("<br>", unsafe_allow_html=True)


# =====================================================
# DATAFRAME
# =====================================================

rows = []

for trend in trends:

    rows.append({

        "Topic": trend.topic.label,

        "Category": trend.topic.category,

        "News Count": trend.news_count,

        "Growth Rate": round(trend.growth_rate, 2),

        "Trend Score": round(trend.trend_score, 2),

        "Updated": trend.updated_at.strftime("%d %b %Y %H:%M"),

    })

df = pd.DataFrame(rows)


# =====================================================
# BAR CHART
# =====================================================

show_bar_chart(

    df,

    "Topic",

    "Top Trending Topics",

    value_column="Trend Score",

)

st.markdown("<br>", unsafe_allow_html=True)


# =====================================================
# TABLE
# =====================================================

st.dataframe(

    df,

    use_container_width=True,

    hide_index=True,

)