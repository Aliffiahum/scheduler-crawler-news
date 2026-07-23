import streamlit as st
import pandas as pd


# ======================================================
# DEFAULT TABLE
# ======================================================

def data_table(
    dataframe: pd.DataFrame,
    height: int = 550,
):

    st.dataframe(
        dataframe,
        use_container_width=True,
        hide_index=True,
        height=height,
    )


# ======================================================
# SEARCHABLE TABLE
# ======================================================

def searchable_table(
    dataframe: pd.DataFrame,
    placeholder="Cari data...",
):

    keyword = st.text_input(
        "",
        placeholder=placeholder,
    )

    if keyword:

        keyword = keyword.lower()

        dataframe = dataframe[
            dataframe.astype(str)
            .apply(
                lambda row:
                row.str.lower().str.contains(keyword).any(),
                axis=1,
            )
        ]

    st.dataframe(
        dataframe,
        use_container_width=True,
        hide_index=True,
        height=600,
    )


# ======================================================
# PAGINATION TABLE
# ======================================================

def paginated_table(
    dataframe: pd.DataFrame,
    page_size: int = 20,
):

    total_rows = len(dataframe)

    total_pages = max(
        1,
        (total_rows - 1) // page_size + 1,
    )

    page = st.number_input(
        "Halaman",
        min_value=1,
        max_value=total_pages,
        value=1,
    )

    start = (page - 1) * page_size
    end = start + page_size

    st.dataframe(
        dataframe.iloc[start:end],
        use_container_width=True,
        hide_index=True,
        height=600,
    )

    st.caption(
        f"Menampilkan {start+1}-{min(end,total_rows)} dari {total_rows} data"
    )