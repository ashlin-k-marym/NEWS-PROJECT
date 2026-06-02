import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(
    page_title="News Analytics Dashboard",
    layout="wide"
)

DATABASE_URL = "postgresql://..."

engine = create_engine(DATABASE_URL)

df = pd.read_sql(
    "SELECT * FROM news_data ORDER BY created_at DESC",
    engine
)

st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.main-title {
    font-size: 42px;
    font-weight: bold;
    color: black;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.radio(
    "",
    ["View News", "Analytics"]
)

st.sidebar.markdown("### Explanation")
st.sidebar.markdown("""
Sentiment score indicates whether the news sentiment is positive or negative.
""")

st.sidebar.markdown("### Latest update data")
if not df.empty:
    st.sidebar.write(df["created_at"].max())

    st.markdown(
    '<div class="main-title">News Analytics sentiment score dashboard</div>',
    unsafe_allow_html=True
)
    
    if df.empty:
    st.warning("No news data found in database.")

display_df = df[
    [
        "news_date",
        "source_name",
        "title",
        "sentiment_score",
        "sentiment_label",
        "created_at"
    ]
]

st.dataframe(display_df)

def color_sentiment(value):
    if value > 0:
        return "background-color: green; color: white"
    elif value < 0:
        return "background-color: red; color: white"
    else:
        return "background-color: gray; color: white"

styled_df = display_df.style.applymap(
    color_sentiment,
    subset=["sentiment_score"]
)