import pandas as pd
import streamlit as st

from app.database.connection import SessionLocal

from dashboard.services.overview_service import (
    DashboardOverviewService,
)

from dashboard.components.metric_cards import show_metrics
from dashboard.components.pie_charts import show_pie_chart
from dashboard.components.bar_chart import show_bar_chart

st.set_page_config(

    page_title="Overview",

    page_icon="🏠",

    layout="wide",

)

st.title("🏠 Executive Dashboard")

db = SessionLocal()

service = DashboardOverviewService(db)

total_news = service.total_news()

topics = service.total_topics()

trends = service.get_trends()

recommendations = service.get_recommendations()

high = len(

    [

        r

        for r in recommendations

        if r.score >= 0.8

    ]

)

show_metrics(

    [

        ("News", total_news),

        ("Topics", topics),

        ("Trending", len(trends)),

        ("High Recommendation", high),

    ]

)

st.markdown("<br>", unsafe_allow_html=True)

trend_rows = []

for trend in trends:

    trend_rows.append({

        "Topic": trend.topic.label,

        "Category": trend.topic.category,

        "Trend Score": trend.trend_score,

        "News": trend.news_count,

    })

trend_df = pd.DataFrame(trend_rows)

rec_rows = []

for rec in recommendations:

    rec_rows.append({

        "Topic": rec.topic.label,

        "Category": rec.topic.category,

        "Score": rec.score,

    })

rec_df = pd.DataFrame(rec_rows)

col1, col2 = st.columns(2)

with col1:

    show_bar_chart(

        trend_df,

        "Topic",

        "Top Trending Topics",

        value_column="Trend Score",

    )

with col2:

    show_bar_chart(

        rec_df,

        "Topic",

        "Top Recommendation",

        value_column="Score",

    )

    st.subheader("🔥 Top Trending Topics")

st.dataframe(

    trend_df.head(10),

    use_container_width=True,

    hide_index=True,

)

st.subheader("💡 Editorial Recommendation")

st.dataframe(

    rec_df.head(10),

    use_container_width=True,

    hide_index=True,

)