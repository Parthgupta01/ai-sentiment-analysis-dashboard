import streamlit as st
import requests

st.set_page_config(page_title="Submit Review", layout="wide")

st.title("📝 Submit Customer Review")

st.markdown("Enter product details and customer feedback below.")

# Form
with st.form("review_form"):
    product_id = st.number_input("Product ID", min_value=1)
    review_text = st.text_area("Customer Review")

    submit = st.form_submit_button("Submit Review")

if submit:
    if not review_text.strip():
        st.warning("⚠️ Please enter a review before submitting.")
    else:
        try:
            response = requests.post(
                "http://127.0.0.1:8000/submit-review",
                json={
                    "product_id": product_id,
                    "review_text": review_text
                }
            )

            if response.status_code == 200:
                st.success("✅ Review submitted successfully! Processing started.")
            else:
                st.error("❌ Failed to submit review. Try again.")

        except Exception as e:
            st.error("🚫 Backend not running or connection error.")