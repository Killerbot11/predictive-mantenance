import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import random
import numpy as np
from utils import predict_failure

st.set_page_config(page_title="Predictive Maintenance Platform", layout="wide")

# -----------------------------
# STATE INIT
# -----------------------------
if "health_history" not in st.session_state:
    st.session_state.health_history = []

if "failure_prob" not in st.session_state:
    st.session_state.failure_prob = None

if "input_data" not in st.session_state:
    st.session_state.input_data = None

# -----------------------------
# SYSTEM HEALTH
# -----------------------------
def get_system_health(prob):
    if prob is None:
        return "Unknown"
    elif prob < 0.4:
        return "Healthy"
    elif prob < 0.7:
        return "Warning"
    else:
        return "Critical"

# -----------------------------
# LOGIN
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Predictive Maintenance Platform")
    st.caption("Industrial Monitoring Suite")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("Navigation")

page = st.sidebar.radio("", [
    "Dashboard",
    "Live Monitoring",
    "AI Analysis",
    "Reports",
    "Alerts",
    "About"
])

machine = st.sidebar.selectbox("Select Machine", ["Machine A", "Machine B", "Machine C"])

# -----------------------------
# HEADER
# -----------------------------
health_status = get_system_health(st.session_state.failure_prob)

title_col, status_col = st.columns([6,3])

with title_col:
    st.title("AI Predictive Maintenance")
    st.caption("Monitor equipment health and predict failures using AI")

with status_col:
    st.metric("Machine", machine)
    st.metric("System Health", health_status)

st.divider()

# -----------------------------
# DASHBOARD
# -----------------------------
if page == "Dashboard":

    st.subheader("System Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Machines Online", "3")
    col2.metric("Sensors Active", "21")
    col3.metric("AI Engine", "Operational")

    # -------- HEALTH TREND --------
    if st.session_state.health_history:
        st.subheader("Health Trend")
        fig, ax = plt.subplots()
        ax.plot(st.session_state.health_history, marker='o')
        ax.set_ylim(0,1)
        ax.set_ylabel("Failure Probability")
        ax.set_xlabel("Prediction Run")
        st.pyplot(fig)

    # -------- SENSOR DISTRIBUTION --------
    st.subheader("Sensor Distribution")

    sensor_data = np.random.normal(50, 15, 100)

    fig, ax = plt.subplots()
    ax.hist(sensor_data, bins=20)
    ax.set_title("Sensor Value Distribution")
    st.pyplot(fig)

    # -------- RISK TREND --------
    st.subheader("Risk Trend Over Time")

    risk_series = [random.uniform(0.2,0.9) for _ in range(10)]

    fig, ax = plt.subplots()
    ax.plot(risk_series)
    ax.set_ylim(0,1)
    ax.set_title("AI Risk Trend")
    st.pyplot(fig)

    # -------- OPERATING RADAR --------
    st.subheader("Operating Conditions")

    labels = ['Load', 'Speed', 'Stress']
    values = [random.random(), random.random(), random.random()]

    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.3)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    st.pyplot(fig)

    # -------- AI CONFIDENCE --------
    st.subheader("AI Confidence")

    confidence = random.uniform(0.6,0.95)

    fig, ax = plt.subplots()
    ax.bar(["Confidence"], [confidence])
    ax.set_ylim(0,1)
    st.pyplot(fig)

    # -------- STABILITY INDEX --------
    st.subheader("System Stability Index")

    stability = random.uniform(0.5,0.95)

    fig, ax = plt.subplots()
    ax.barh(["Stability"], [stability])
    ax.set_xlim(0,1)
    st.pyplot(fig)

# -----------------------------
# LIVE MONITORING
# -----------------------------
elif page == "Live Monitoring":

    st.subheader("Operational Parameters")

    op1 = st.slider("Machine Load", 0.0, 1.0, 0.45)
    op2 = st.slider("Operating Speed", 0.0, 1.0, 0.34)
    op3 = st.slider("Environmental Stress", 0.0, 1.0, 0.89)

    sensor_values = [random.uniform(0,100) for _ in range(21)]
    st.session_state.input_data = [op1, op2, op3] + sensor_values

# -----------------------------
# AI ANALYSIS
# -----------------------------
elif page == "AI Analysis":

    st.subheader("Failure Prediction")

    if st.session_state.input_data is None:
        st.warning("Run Live Monitoring first")
    else:
        if st.button("Run Prediction"):
            result = predict_failure(st.session_state.input_data)
            prob = random.uniform(0.6,0.95) if result==1 else random.uniform(0.05,0.4)

            st.session_state.failure_prob = prob
            st.session_state.health_history.append(prob)

        if st.session_state.failure_prob:
            st.metric("Failure Probability", f"{round(st.session_state.failure_prob*100,2)}%")

# -----------------------------
# ALERTS
# -----------------------------
elif page == "Alerts":

    st.subheader("System Alerts")

    status = get_system_health(st.session_state.failure_prob)

    if status == "Critical":
        st.error("Critical risk detected.")
    elif status == "Warning":
        st.warning("Early warning signs detected.")
    elif status == "Healthy":
        st.success("System operating normally.")
    else:
        st.info("Run AI Analysis to generate system health.")

# -----------------------------
# REPORTS
# -----------------------------
elif page == "Reports":

    st.subheader("Generate Report")

    if st.session_state.failure_prob:
        report = pd.DataFrame({
            "Machine":[machine],
            "Failure Probability":[st.session_state.failure_prob]
        })
        st.download_button("Download CSV Report", report.to_csv(index=False), "report.csv")

# -----------------------------
# ABOUT
# -----------------------------
elif page == "About":
    st.write("Enterprise AI Predictive Maintenance Platform")
