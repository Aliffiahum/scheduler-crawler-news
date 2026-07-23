import streamlit as st


def load_css():

    st.markdown(
        """
<style>

/* =====================================================
BACKGROUND
===================================================== */

.stApp{
    background-color:#F7F9FC;
}


/* =====================================================
SIDEBAR
===================================================== */

section[data-testid="stSidebar"]{
    background:#1E293B;
}

section[data-testid="stSidebar"] *{
    color:white;
}


/* =====================================================
TITLE
===================================================== */

h1{
    color:#0F172A;
    font-weight:700;
}

h2{
    color:#0F172A;
}

h3{
    color:#0F172A;
}


/* =====================================================
METRIC CARD
===================================================== */

div[data-testid="metric-container"]{

    background:white;

    border-radius:15px;

    padding:15px;

    border:1px solid #E2E8F0;

    box-shadow:0px 2px 10px rgba(0,0,0,.05);

}


/* =====================================================
DATAFRAME
===================================================== */

[data-testid="stDataFrame"]{

    border-radius:12px;

    overflow:hidden;

}


/* =====================================================
BUTTON
===================================================== */

.stButton>button{

    background:#2563EB;

    color:white;

    border-radius:10px;

    border:none;

}

.stButton>button:hover{

    background:#1D4ED8;

    color:white;

}


/* =====================================================
TEXT INPUT
===================================================== */

.stTextInput input{

    border-radius:10px;

}


/* =====================================================
SELECTBOX
===================================================== */

.stSelectbox{

    border-radius:10px;

}


/* =====================================================
SUCCESS
===================================================== */

.stSuccess{

    border-radius:10px;

}


/* =====================================================
INFO
===================================================== */

.stInfo{

    border-radius:10px;

}


/* =====================================================
WARNING
===================================================== */

.stWarning{

    border-radius:10px;

}


/* =====================================================
EXPANDER
===================================================== */

.streamlit-expanderHeader{

    font-weight:bold;

}


/* =====================================================
PLOTLY
===================================================== */

.js-plotly-plot{

    background:white;

    border-radius:15px;

    padding:10px;

}


/* =====================================================
FOOTER
===================================================== */

footer{

    visibility:hidden;

}

</style>
""",
        unsafe_allow_html=True,
    )