import pandas as pd
import streamlit as st

from app.database.connection import SessionLocal

from dashboard.services.recommendation_service import (
    DashboardRecommendationService,
)

from dashboard.components.metric_cards import show_metrics
from dashboard.components.pie_charts import show_pie_chart
from dashboard.components.bar_chart import show_bar_chart


# =====================================================
# CONFIG
# =====================================================

st.set_page_config(

    page_title="Recommendation",

    page_icon="💡",

    layout="wide",

)

st.title("💡 Recommendation Dashboard")


# =====================================================
# DATABASE
# =====================================================

db = SessionLocal()

service = DashboardRecommendationService(db)

recommendations = service.get_recommendations()


# =====================================================
# DATAFRAME
# =====================================================

rows = []

for rec in recommendations:

    topic = rec.topic

    if rec.score >= 0.8:
        priority = "High"

    elif rec.score >= 0.6:
        priority = "Medium"

    else:
        priority = "Low"

    rows.append({

        "Topic": topic.label,

        "Category": topic.category,

        "Score": round(rec.score, 3),

        "Priority": priority,

        "Reason": rec.reason,

        "Created": rec.created_at,

    })

df = pd.DataFrame(rows)

high = len(df[df["Priority"] == "High"])
medium = len(df[df["Priority"] == "Medium"])
low = len(df[df["Priority"] == "Low"])

show_metrics(

    [

        ("Recommendations", len(df)),

        ("High Priority", high),

        ("Medium Priority", medium),

        ("Low Priority", low),

    ]

)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:

    show_pie_chart(

        df,

        "Priority",

        "Priority Distribution",

    )

with col2:

    show_pie_chart(

        df,

        "Category",

        "Recommendation Category",

    )

st.markdown("<br>", unsafe_allow_html=True)

show_bar_chart(

    df,

    "Topic",

    "Recommendation Score",

    value_column="Score",

)

st.markdown("<br>", unsafe_allow_html=True)

st.dataframe(

    df,

    use_container_width=True,

    hide_index=True,

)