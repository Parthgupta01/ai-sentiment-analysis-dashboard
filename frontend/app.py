import streamlit as st
import requests
import plotly.express as px

st.title("📊 Customer Sentiment Dashboard")

# API call
data = requests.get("http://127.0.0.1:8000/analytics-summary").json()

# Show metrics
st.write("### Summary")
st.write(data)

# Pie chart
labels = ["Positive", "Negative"]
values = [data["positive"], data["negative"]]

fig = px.pie(names=labels, values=values, title="Sentiment Distribution")

st.plotly_chart(fig)