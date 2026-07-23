import pandas as pd
import plotly.express as px
import streamlit as st


def show_news_trend(df: pd.DataFrame):

    if df.empty:
        st.info("Belum ada data.")
        return

    trend = df.copy()

    trend["Published"] = pd.to_datetime(trend["Published"])

    trend = (
        trend.groupby(
            trend["Published"].dt.date
        )
        .size()
        .reset_index(name="Total")
    )

    fig = px.line(
        trend,
        x="Published",
        y="Total",
        markers=True,
        title="Jumlah Berita per Hari",
    )

    fig.update_layout(
        height=350,
        margin=dict(
            l=10,
            r=10,
            t=40,
            b=10,
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )