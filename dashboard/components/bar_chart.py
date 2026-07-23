import pandas as pd
import plotly.express as px
import streamlit as st


def show_bar_chart(

    df: pd.DataFrame,

    column: str,

    title: str,

    value_column: str | None = None,

    top_n: int = 10,

):

    if df.empty:

        st.info("Tidak ada data.")

        return

    # =====================================================
    # MODE 1
    # Hitung otomatis (News Page)
    # =====================================================

    if value_column is None:

        chart = (

            df[column]

            .value_counts()

            .head(top_n)

            .reset_index()

        )

        chart.columns = [column, "Count"]

        x = "Count"

    # =====================================================
    # MODE 2
    # Gunakan kolom numerik (Topic Page)
    # =====================================================

    else:

        chart = (

            df[[column, value_column]]

            .sort_values(

                value_column,

                ascending=False,

            )

            .head(top_n)

        )

        x = value_column

    fig = px.bar(

        chart,

        x=x,

        y=column,

        orientation="h",

        text=x,

        title=title,

    )

    fig.update_layout(

        yaxis=dict(

            categoryorder="total ascending"

        ),

        height=500,

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