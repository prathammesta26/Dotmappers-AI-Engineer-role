import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Support Ticket AI Analyst", layout="wide")
st.title("🎫 Enterprise Ticket AI Intelligence Engine")

tab1, tab2 = st.tabs(["💬 Natural Language Query", "⚠️ Anomaly Detection"])

with tab1:
    st.subheader("Ask questions about support tickets")
    sample_queries = [
        "How many tickets are currently open?",
        "Which agent resolved the most tickets?",
        "Show me all Critical tickets not resolved within 12 hours.",
        "What is the average customer rating for Technical category tickets?",
        "Which agent has the lowest average customer rating?"
    ]
    selected_query = st.selectbox("Or choose a sample question:", [""] + sample_queries)
    user_query = st.text_input("Enter your natural language query:", value=selected_query)

    if st.button("Run Query", type="primary"):
        if user_query:
            with st.spinner("Translating query via LLM and retrieving data..."):
                try:
                    res = requests.post(f"{API_URL}/query", json={"question": user_query})
                    if res.status_code == 200:
                        payload = res.json()
                        st.code(payload["generated_sql"], language="sql")
                        st.dataframe(pd.DataFrame(payload["data"]))
                    else:
                        st.error(res.json().get("detail", "Error processing query"))
                except Exception as e:
                    st.error(f"Failed to connect to FastAPI: {e}")

with tab2:
    st.subheader("Operational & Statistical Anomalies")
    if st.button("Scan for Anomalies"):
        try:
            res = requests.get(f"{API_URL}/anomalies")
            if res.status_code == 200:
                payload = res.json()
                st.metric("Total Anomalies Detected", payload["total_anomalies"])
                st.caption(f"Statistical outlier threshold: > {payload['statistical_threshold_hrs']} hours")
                st.dataframe(pd.DataFrame(payload["anomalies"]))
        except Exception as e:
            st.error(f"API Error: {e}")