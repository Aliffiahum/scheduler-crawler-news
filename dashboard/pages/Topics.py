import math
import pandas as pd
import streamlit as st

from app.database.connection import SessionLocal

from dashboard.services.topic_service import DashboardTopicService

from dashboard.components.metric_cards import show_metrics
from dashboard.components.pie_charts import show_pie_chart
from dashboard.components.bar_chart import show_bar_chart


# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Topics",
    page_icon="🏷️",
    layout="wide",
)

st.title("🏷️ Topics")


# =====================================================
# DATABASE
# =====================================================

db = SessionLocal()
service = DashboardTopicService(db)


# =====================================================
# SESSION
# =====================================================

if "topic_page" not in st.session_state:
    st.session_state.topic_page = 1

PER_PAGE = 20


# =====================================================
# FILTER
# =====================================================

col1, col2 = st.columns(2)

with col1:

    keyword = st.text_input(
        "🔍 Cari Topic"
    )

with col2:

    categories = ["Semua"] + service.get_categories()

    selected_category = st.selectbox(
        "Kategori",
        categories,
    )


# =====================================================
# TOTAL
# =====================================================

total_topics = service.total_topics(

    keyword=keyword,

    category=selected_category,

)

total_pages = max(
    1,
    math.ceil(total_topics / PER_PAGE),
)

if st.session_state.topic_page > total_pages:
    st.session_state.topic_page = total_pages


# =====================================================
# LOAD DATA
# =====================================================

topics = service.get_topics(

    keyword=keyword,

    category=selected_category,

    page=st.session_state.topic_page,

    per_page=PER_PAGE,

)

chart_topics = service.get_chart_data(

    keyword=keyword,

    category=selected_category,

)


# =====================================================
# METRICS
# =====================================================

total_news = sum(len(t.news) for t in chart_topics)

show_metrics(
    [
        ("Total Topics", total_topics),
        ("Total News", total_news),
        ("Kategori", len(service.get_categories())),
        ("Per Page", PER_PAGE),
    ]
)

st.markdown("<br>", unsafe_allow_html=True)


# =====================================================
# CHART DATA
# =====================================================

chart_rows = []

for topic in chart_topics:

    chart_rows.append({

        "Topic": topic.label,

        "Category": topic.category or "-",

        "News Count": len(topic.news),

    })

chart_df = pd.DataFrame(chart_rows)


# =====================================================
# CHART
# =====================================================

col1, col2 = st.columns(2)

with col1:

    show_pie_chart(

        chart_df,

        "Category",

        "Distribusi Kategori",

    )

with col2:

    show_bar_chart(

        chart_df,

        "Topic",

        "Jumlah Berita per Topic",

        value_column="News Count",

    )


st.markdown("<br>", unsafe_allow_html=True)


# =====================================================
# TABLE
# =====================================================

rows = []

for topic in topics:

    rows.append({

        "Topic": topic.label,

        "Category": topic.category or "-",

        "Keywords": topic.keywords,

        "Description": topic.description,

        "Representative Docs": topic.representative_docs,

        "News Count": len(topic.news),

        "Created": topic.created_at.strftime("%d %b %Y"),

    })

df = pd.DataFrame(rows)

st.dataframe(

    df,

    use_container_width=True,

    hide_index=True,

)


# =====================================================
# PAGINATION
# =====================================================

left, center, right = st.columns([1,2,1])

with left:

    if st.button(

        "⬅ Previous",

        use_container_width=True,

        disabled=st.session_state.topic_page == 1,

    ):

        st.session_state.topic_page -= 1

        st.rerun()


with center:

    st.markdown(

        f"<h4 style='text-align:center;'>Halaman {st.session_state.topic_page} / {total_pages}</h4>",

        unsafe_allow_html=True,

    )


with right:

    if st.button(

        "Next ➡",

        use_container_width=True,

        disabled=st.session_state.topic_page >= total_pages,

    ):

        st.session_state.topic_page += 1

        st.rerun()