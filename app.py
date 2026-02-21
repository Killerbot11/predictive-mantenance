import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import time
from utils import predict_failure

st.set_page_config(page_title="AI Predictive Maintenance", layout="wide")

# ==========================
# LOGIN SYSTEM
# ==========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login to Predictive Maintenance Platform")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin":
            st.session_state.logged_in = True
            st.success("Login Successful")
            st.rerun()
        else:
            st.error("Invalid Credentials")

    st.stop()

# ==========================
# DARK MODE TOGGLE
# ==========================
dark_mode = st.sidebar.toggle("🌙 Dark Mode")
if dark_mode:
    st.markdown("""
        <style>
        body { background-color: #0E1117; color: white; }
        </style>
    """, unsafe_allow_html=True)

# ==========================
# SIDEBAR NAVIGATION
# ==========================
st.sidebar.title("🔧 Predictive Maintenance")
page = st.sidebar.radio("Navigation", [
    "🏠 Dashboard",
    "📊 Live Monitoring",
    "📂 Upload Data",
    "🧠 AI Analysis",
    "📄 Reports",
    "ℹ️ About System"
])

# ==========================
# MACHINE SELECTOR
# ==========================
machine = st.sidebar.selectbox("Select Machine", ["Machine A", "Machine B", "Machine C"])

# ==========================
# GLOBAL STATE
# ==========================
if "input_data" not in st.session_state:
    st.session_state.input_data = None

if "last_result" not in st.session_state:
    st.session_state.last_result = None

# ==========================
# DASHBOARD
# ==========================
if page == "🏠 Dashboard":
    st.title("AI Predictive Maintenance System")
    st.markdown(f"### Monitoring: {machine}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Machines Monitored", "24")
    col2.metric("Active Sensors", "21")
    col3.metric("Prediction Engine", "Online")

# ==========================
# LIVE MONITORING
# ==========================
elif page == "📊 Live Monitoring":
    st.title("Live Monitoring")

    auto_refresh = st.toggle("Auto Refresh Live Data")

    op1 = st.slider("Machine Load", 0.0, 1.0, 0.45)
    op2 = st.slider("Operating Speed", 0.0, 1.0, 0.34)
    op3 = st.slider("Environmental Stress", 0.0, 1.0, 0.89)

    sensor_values = [random.uniform(0,100) for _ in range(21)]
    input_data = [op1, op2, op3] + sensor_values
    st.session_state.input_data = input_data

    fig, ax = plt.subplots()
    ax.bar(range(1,22), sensor_values)
    ax.set_title("Live Sensor Feed")
    st.pyplot(fig)

    if auto_refresh:
        time.sleep(3)
        st.rerun()

# ==========================
# UPLOAD
# ==========================
elif page == "📂 Upload Data":
    st.title("Upload Machine Data")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)

        if df.shape[1] == 24:
            st.session_state.input_data = df.iloc[0].values.tolist()
            st.success("Data Loaded")
        else:
            st.error("CSV must have 24 columns")

# ==========================
# AI ANALYSIS
# ==========================
elif page == "🧠 AI Analysis":
    st.title("AI Health Analysis")

    if st.session_state.input_data is None:
        st.warning("Provide monitoring or upload data first")
    else:
        if st.button("Run AI Prediction"):
            result = predict_failure(st.session_state.input_data)
            st.session_state.last_result = result

        if st.session_state.last_result is not None:
            result = st.session_state.last_result
            health_score = 100 - (result * 60)

            st.metric("Health Score", f"{health_score}%")

            # Gauge Chart
            fig, ax = plt.subplots()
            ax.pie([health_score, 100-health_score])
            ax.set_title("Health Gauge")
            st.pyplot(fig)

# ==========================
# REPORTS
# ==========================
elif page == "📄 Reports":
    st.title("Download Health Report")

    if st.session_state.last_result is None:
        st.warning("Run AI Analysis first")
    else:
        report = pd.DataFrame({
            "Machine": [machine],
            "Failure Risk": ["High" if st.session_state.last_result==1 else "Low"]
        })

        st.download_button("Download Report", report.to_csv(index=False), "report.csv")

# ==========================
# ABOUT
# ==========================
elif page == "ℹ️ About System":
    st.title("About Platform")
    st.write("Industry-grade AI monitoring system.")
