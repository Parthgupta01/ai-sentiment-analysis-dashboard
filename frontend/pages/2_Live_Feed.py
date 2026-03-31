import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="Live Feed", layout="wide")

st.title("📡 Live Review Feed")

st.markdown("Real-time customer reviews and processing status")

# Auto refresh
refresh = st.button("🔄 Refresh")

try:
    response = requests.get("http://127.0.0.1:8000/reviews")
    data = response.json()

    if len(data) == 0:
        st.warning("No reviews found.")
    else:
        df = pd.DataFrame(data)

        # Status color
        def highlight_status(val):
            if val == "Pending":
                return "color: orange"
            elif val == "Completed":
                return "color: green"
            elif val == "Processing":
                 return "color: blue"
            else:
                return ""

        st.dataframe(df.style.applymap(highlight_status, subset=["status"]))

except:
    st.error("🚫 Backend not running")

# Auto reload every 5 sec
time.sleep(5)
st.rerun()