import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import random
from utils import predict_failure

st.set_page_config(page_title="Predictive Maintenance Platform", layout="wide")

# -----------------------------
# PROFESSIONAL UI + WIDTH FIX
# -----------------------------
st.markdown("""
<style>

/* Use full width */
section.main > div {
    max-width: 100% !important;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* Fix spacing */
.block-container {
    padding-top: 1rem !important;
}

/* KPI Cards */
.kpi-card {
    background: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #E6E9EF;
}

/* Section Panels */
.section-card {
    background: white;
    padding: 24px;
    border-radius: 12px;
    border: 1px solid #E6E9EF;
}

/* Title */
.title-text {
    font-size: 28px;
    font-weight: 600;
}

/* Subtitle */
.subtle-text {
    color: #6B7280;
}

/* Sidebar */
.sidebar .sidebar-content {
    background-color: #F7F9FC;
}

/* Buttons */
.stButton>button {
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOGIN
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Predictive Maintenance Platform")
    st.caption("Industrial Monitoring Suite")

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):
            if username == "admin" and password == "admin":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials")

    st.stop()

# -----------------------------
# HEADER (FIXED)
# -----------------------------
header_col1, header_col2 = st.columns([6,1])

with header_col1:
    st.markdown("""
    <div style='padding-top:5px'>
        <div class='title-text'>AI Predictive Maintenance</div>
        <div class='subtle-text'>
            Monitor equipment health and predict failures using AI
        </div>
    </div>
    """, unsafe_allow_html=True)

with header_col2:
    st.empty()

st.divider()

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

if "input_data" not in st.session_state:
    st.session_state.input_data = None

if "failure_prob" not in st.session_state:
    st.session_state.failure_prob = None

# -----------------------------
# DASHBOARD
# -----------------------------
if page == "Dashboard":

    st.subheader("System Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div class='kpi-card'><b>Machines Online</b><h2>3</h2></div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='kpi-card'><b>Sensors Active</b><h2>21</h2></div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='kpi-card'><b>AI Engine</b><h2>Operational</h2></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.subheader("Machine Health Comparison")

    comparison = {
        "Machine A": random.randint(70,95),
        "Machine B": random.randint(60,90),
        "Machine C": random.randint(50,85)
    }

    fig, ax = plt.subplots()
    ax.bar(comparison.keys(), comparison.values())
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# LIVE MONITORING
# -----------------------------
elif page == "Live Monitoring":

    st.subheader("Operational Parameters")

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        op1 = st.slider("Machine Load", 0.0, 1.0, 0.45)
    with col2:
        op2 = st.slider("Operating Speed", 0.0, 1.0, 0.34)
    with col3:
        op3 = st.slider("Environmental Stress", 0.0, 1.0, 0.89)

    st.markdown("</div>", unsafe_allow_html=True)

    sensor_values = [random.uniform(0,100) for _ in range(21)]
    st.session_state.input_data = [op1, op2, op3] + sensor_values

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.subheader("Sensor Trends")

    fig, ax = plt.subplots()
    ax.plot(sensor_values)
    st.pyplot(fig)

    st.markdown("</div>", unsafe_allow_html=True)

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

        if st.session_state.failure_prob:

            st.markdown("<div class='kpi-card'>", unsafe_allow_html=True)
            st.metric("Failure Probability", f"{round(st.session_state.failure_prob*100,2)}%")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            fig, ax = plt.subplots()
            ax.barh(["Risk"], [st.session_state.failure_prob])
            ax.set_xlim(0,1)
            st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# ALERTS
# -----------------------------
elif page == "Alerts":

    st.subheader("System Alerts")

    if st.session_state.failure_prob and st.session_state.failure_prob > 0.7:
        st.error("High failure risk detected. Maintenance recommended.")
    else:
        st.success("No critical alerts")

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
