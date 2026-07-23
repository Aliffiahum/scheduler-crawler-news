import streamlit as st


def show_metrics(metrics: list[tuple[str, str]]) -> None:
    """
    metrics:
    [
        ("Total News", "1251"),
        ("Kategori", "12"),
        ("Source", "18"),
        ("Sentiment", "3")
    ]
    """

    cols = st.columns(len(metrics))

    for col, (title, value) in zip(cols, metrics):

        with col:

            st.markdown(
                f"""
                <div style="
                    background-color:#FFFFFF;
                    padding:18px;
                    border-radius:12px;
                    border:1px solid #E6E6E6;
                    text-align:center;
                    box-shadow:0 1px 4px rgba(0,0,0,.08);
                ">

                <div style="
                    color:#777;
                    font-size:14px;
                ">
                    {title}
                </div>

                <div style="
                    font-size:34px;
                    font-weight:bold;
                    color:#111;
                    margin-top:8px;
                ">
                    {value}
                </div>

                </div>
                """,
                unsafe_allow_html=True,
            )