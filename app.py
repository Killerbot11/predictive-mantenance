import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import random
from utils import predict_failure

st.set_page_config(page_title="Predictive Maintenance Platform", layout="wide")

# -----------------------------
# THEME COLORS
# -----------------------------
theme = st.get_option("theme.base")

if theme == "dark":
    card_bg = "#1E1E1E"
    border = "#2D2D2D"
    badge_bg = "#1F3D2B"
    badge_text = "#A6E3B8"
else:
    card_bg = "#FFFFFF"
    border = "#E6E9EF"
    badge_bg = "#E6F4EA"
    badge_text = "#137333"

# -----------------------------
# HEALTH HISTORY INIT
# -----------------------------
if "health_history" not in st.session_state:
    st.session_state.health_history = []

# -----------------------------
# SYSTEM HEALTH LOGIC
# -----------------------------
def get_system_health(prob):

    if prob is None:
        return "Unknown", "#9AA0A6", "#E8EAED"

    if prob < 0.4:
        return "Healthy", "#137333", "#E6F4EA"
    elif prob < 0.7:
        return "Warning", "#B06000", "#FFF4E5"
    else:
        return "Critical", "#C5221F", "#FCE8E6"

# -----------------------------
# GLOBAL STYLING
# -----------------------------
st.markdown(f"""
<style>
.block-container {{
    padding-top: 3rem !important;
}}

section.main > div {{
    max-width: 100% !important;
    padding-left: 2rem;
    padding-right: 2rem;
}}

.kpi-card {{
    background: {card_bg};
    padding: 18px;
    border-radius: 12px;
    border: 1px solid {border};
}}

.section-card {{
    background: {card_bg};
    padding: 24px;
    border-radius: 12px;
    border: 1px solid {border};
}}
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
# STATE
# -----------------------------
if "failure_prob" not in st.session_state:
    st.session_state.failure_prob = None

if "input_data" not in st.session_state:
    st.session_state.input_data = None

# -----------------------------
# HEADER WITH HEALTH
# -----------------------------
health_status, health_color, health_bg = get_system_health(st.session_state.failure_prob)

title_col, status_col = st.columns([6,3])

with title_col:
    st.markdown("### AI Predictive Maintenance")
    st.caption("Monitor equipment health and predict failures using AI")

with status_col:
    st.markdown(f"""
    <div style='text-align:right; margin-top: 8px;'>

        <span style='font-size:13px; padding:6px 12px;
        border-radius:8px;
        background-color:{badge_bg};
        color:{badge_text};
        margin-right:6px;
        font-weight:500;'>
        {machine}
        </span>

        <span style='font-size:13px; padding:6px 12px;
        border-radius:8px;
        background-color:{health_bg};
        color:{health_color};
        font-weight:600;'>
        {health_status}
        </span>

    </div>
    """, unsafe_allow_html=True)

st.divider()

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

    # Health Trend
    if st.session_state.health_history:
        st.subheader("Health Trend")

        fig, ax = plt.subplots()
        ax.plot(st.session_state.health_history, marker='o')
        ax.set_ylim(0,1)
        ax.set_ylabel("Failure Probability")
        ax.set_xlabel("Prediction Run")
        st.pyplot(fig)

# -----------------------------
# LIVE MONITORING
# -----------------------------
elif page == "Live Monitoring":

    st.subheader("Operational Parameters")

    col1, col2, col3 = st.columns(3)

    with col1:
        op1 = st.slider("Machine Load", 0.0, 1.0, 0.45)
    with col2:
        op2 = st.slider("Operating Speed", 0.0, 1.0, 0.34)
    with col3:
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

    status, _, _ = get_system_health(st.session_state.failure_prob)

    if status == "Critical":
        st.error("Critical risk detected. Immediate maintenance required.")
    elif status == "Warning":
        st.warning("System showing early signs of failure.")
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
