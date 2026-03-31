import streamlit as st
import requests
import plotly.express as px
import pandas as pd

# Page config
st.set_page_config(page_title="AI Dashboard", layout="wide")

# ------------------ HEADER ------------------ #
st.markdown("## 📊 AI Customer Sentiment Dashboard")
st.caption("Real-time sentiment analysis powered by AI 🚀")

st.markdown("---")

# ------------------ SUMMARY ------------------ #
try:
    summary = requests.get("http://127.0.0.1:8000/analytics-summary").json()

    st.markdown("### 📈 Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Reviews", summary.get("total_reviews", 0))
    col2.metric("Positive", summary.get("positive", 0))
    col3.metric("Negative", summary.get("negative", 0))
    col4.metric("Confidence", f"{round(summary.get('avg_confidence', 0)*100,2)}%")

except Exception:
    st.error("⚠️ Unable to fetch summary data")

st.markdown("---")

# ------------------ CHARTS ------------------ #
try:
    data = requests.get("http://127.0.0.1:8000/analytics").json()

    if isinstance(data, list) and len(data) > 0:
        df = pd.DataFrame(data)

        # Sentiment counts
        sentiment_counts = df["sentiment"].value_counts().reset_index()
        sentiment_counts.columns = ["Sentiment", "Count"]

        st.markdown("### 📊 Sentiment Insights")

        col1, col2 = st.columns(2)

        # Pie chart
        fig1 = px.pie(
            sentiment_counts,
            names="Sentiment",
            values="Count",
            title="Sentiment Distribution",
            color="Sentiment",
            color_discrete_map={
                "POSITIVE": "green",
                "NEGATIVE": "red"
            }
        )
        col1.plotly_chart(fig1, use_container_width=True)

        # Bar chart
        fig2 = px.bar(
            sentiment_counts,
            x="Sentiment",
            y="Count",
            text="Count",
            title="Sentiment Count",
            color="Sentiment",
            color_discrete_map={
                "POSITIVE": "green",
                "NEGATIVE": "red"
            }
        )
        col2.plotly_chart(fig2, use_container_width=True)

    else:
        st.warning("⚠️ No analytics data available yet. Add reviews to see insights.")

except Exception:
    st.error("⚠️ Unable to fetch analytics data")

# ------------------ FOOTER ------------------ #
st.markdown("---")
st.caption("Built by Parth using FastAPI, Streamlit & AI")