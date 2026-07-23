import math
import pandas as pd
import streamlit as st

from app.database.connection import SessionLocal

from dashboard.services.news_service import DashboardNewsService

from dashboard.components.metric_cards import show_metrics
from dashboard.components.pie_charts import show_pie_chart
from dashboard.components.line_chart import show_news_trend
from dashboard.components.bar_chart import show_bar_chart


# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="News",
    page_icon="📰",
    layout="wide",
)

st.title("📰 News")


# =====================================================
# DATABASE
# =====================================================

db = SessionLocal()
service = DashboardNewsService(db)


# =====================================================
# SESSION
# =====================================================

if "page" not in st.session_state:
    st.session_state.page = 1

PER_PAGE = 50


# =====================================================
# MASTER FILTER DATA
# =====================================================

categories = service.get_categories()
sentiments = service.get_sentiments()


# =====================================================
# FILTER
# =====================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    keyword = st.text_input(
        "🔍 Cari Judul"
    )

with col2:

    selected_category = st.selectbox(
        "Kategori",
        ["Semua"] + categories,
    )

with col3:

    selected_sentiment = st.selectbox(
        "Sentiment",
        ["Semua"] + sentiments,
    )

with col4:

    sort = st.selectbox(
        "Urutan",
        ["latest", "oldest"],
        format_func=lambda x: "Terbaru" if x == "latest" else "Terlama",
    )


# =====================================================
# TOTAL DATA
# =====================================================

total_news = service.total_news(
    keyword=keyword,
    category=selected_category,
    sentiment=selected_sentiment,
)

total_pages = max(
    1,
    math.ceil(total_news / PER_PAGE),
)

if st.session_state.page > total_pages:
    st.session_state.page = total_pages


# =====================================================
# TABLE DATA
# =====================================================

news = service.get_news(
    keyword=keyword,
    category=selected_category,
    sentiment=selected_sentiment,
    sort=sort,
    page=st.session_state.page,
    per_page=PER_PAGE,
)


# =====================================================
# CHART DATA
# =====================================================

chart_news = service.get_chart_data(
    keyword=keyword,
    category=selected_category,
    sentiment=selected_sentiment,
    sort=sort,
)


# =====================================================
# METRICS
# =====================================================

show_metrics(
    [
        ("Total News", total_news),
        ("Kategori", len(categories)),
        ("Sentiment", len(sentiments)),
        ("Per Page", PER_PAGE),
    ]
)

st.markdown("<br>", unsafe_allow_html=True)


# =====================================================
# CHART DATAFRAME
# =====================================================

chart_rows = []

for item in chart_news:

    raw = item.raw_news
    topic = item.topic

    chart_rows.append({

        "Title": raw.title,

        "Source": raw.source.source_name if raw.source else "-",

        "Category": topic.category if topic else "-",

        "Topic": topic.label if topic else "-",

        "Sentiment": item.sentiment or "-",

        "Published": raw.published_at,

    })

chart_df = pd.DataFrame(chart_rows)


# =====================================================
# PIE CHART
# =====================================================

col1, col2 = st.columns(2)

with col1:

    show_pie_chart(
        chart_df,
        "Category",
        "Distribusi Kategori",
    )

with col2:

    show_pie_chart(
        chart_df,
        "Sentiment",
        "Distribusi Sentiment",
    )


st.markdown("<br>", unsafe_allow_html=True)


# =====================================================
# LINE CHART
# =====================================================

show_news_trend(chart_df)

st.markdown("<br>", unsafe_allow_html=True)


# =====================================================
# BAR CHART
# =====================================================

show_bar_chart(
    chart_df,
    "Source",
    "Top News Sources",
)

st.markdown("<br>", unsafe_allow_html=True)


# =====================================================
# TABLE DATAFRAME
# =====================================================

rows = []

for item in news:

    raw = item.raw_news
    topic = item.topic

    rows.append({

        "Title": raw.title,

        "Source": raw.source.source_name if raw.source else "-",

        "Category": topic.category if topic else "-",

        "Topic": topic.label if topic else "-",

        "Sentiment": item.sentiment or "-",

        "Published": raw.published_at.strftime("%d %b %Y %H:%M"),

        "URL": raw.url,

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

left, center, right = st.columns([1, 2, 1])

with left:

    if st.button(
        "⬅ Previous",
        use_container_width=True,
        disabled=st.session_state.page == 1,
    ):
        st.session_state.page -= 1
        st.rerun()

with center:

    st.markdown(
        f"""
        <h4 style='text-align:center'>
            Halaman {st.session_state.page} / {total_pages}
        </h4>
        """,
        unsafe_allow_html=True,
    )

with right:

    if st.button(
        "Next ➡",
        use_container_width=True,
        disabled=st.session_state.page >= total_pages,
    ):
        st.session_state.page += 1
        st.rerun()