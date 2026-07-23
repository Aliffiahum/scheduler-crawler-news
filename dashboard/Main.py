from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
    
import streamlit as st

st.set_page_config(
    page_title="Editorial Insight AI",
    page_icon="📰",
    layout="wide",
)

st.title("📰 Editorial Insight AI")

st.markdown("""
Selamat datang di Dashboard Editorial Insight AI.

Gunakan menu di sidebar untuk melihat:

- 📰 News
- 🏷 Topics
- 📈 Trends
- ⭐ Recommendation
""")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("News", "1251")

with c2:
    st.metric("Topics", "53")

with c3:
    st.metric("Trending", "53")

with c4:
    st.metric("Recommendation", "53")

st.divider()

st.info(
    "Dashboard akan otomatis mengambil data terbaru dari database."
)