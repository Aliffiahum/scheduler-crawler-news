import plotly.express as px
import streamlit as st


def show_pie_chart(
    df,
    column,
    title,
):

    if df.empty:
        st.info("Tidak ada data.")
        return

    data = (
        df[column]
        .value_counts()
        .reset_index()
    )

    data.columns = [
        column,
        "Total",
    ]

    fig = px.pie(
        data,
        names=column,
        values="Total",
        hole=0.45,
    )

    fig.update_layout(
        title=title,
        height=380,
        margin=dict(
            l=10,
            r=10,
            t=40,
            b=10,
        ),
        legend_title=None,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )