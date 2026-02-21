import streamlit as st
import random
from utils import predict_failure

st.set_page_config(page_title="Predictive Maintenance Platform", layout="wide")

REVENUE_PER_HOUR = 15000
FAILURE_DOWNTIME = 24
SCHEDULED_COST = 20000
ROUTINE_COST = 5000

if "failure_prob" not in st.session_state:
    st.session_state.failure_prob = None

if "future_prediction" not in st.session_state:
    st.session_state.future_prediction = {
        "Machine A": [],
        "Machine B": [],
        "Machine C": []
    }

if "input_data" not in st.session_state:
    st.session_state.input_data = None

def simulate_future(prob):
    future = []
    current = prob
    for _ in range(15):
        current = min(current + random.uniform(0.02, 0.08), 1.0)
        future.append(current)
        if current >= 0.9:
            break
    return future

def get_system_health(prob):
    if prob is None:
        return "Unknown"
    elif prob < 0.4:
        return "Healthy"
    elif prob < 0.7:
        return "Warning"
    else:
        return "Critical"

def get_maintenance_cost(rul):
    if rul <= 6:
        return SCHEDULED_COST
    return ROUTINE_COST

def get_failure_loss(prob):
    return prob * FAILURE_DOWNTIME * REVENUE_PER_HOUR

def roi_analysis(prob, rul):
    maintenance_cost = get_maintenance_cost(rul)
    failure_loss = get_failure_loss(prob)
    avoided_loss = failure_loss - maintenance_cost
    roi = (avoided_loss - maintenance_cost) / maintenance_cost if maintenance_cost else 0
    return maintenance_cost, failure_loss, avoided_loss, roi

def decision_engine(prob, rul, roi):

    if rul <= 3:
        return "Immediate Action Required", "High Risk"

    if roi > 0 and rul <= 6:
        return "Maintain Now", "Financially Justified"

    if roi > 0:
        return "Plan Maintenance", "Upcoming Risk"

    return "Monitor", "Low Financial Impact"

# -----------------------------
# LOGIN
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Predictive Maintenance Platform")
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
    "Live Monitoring",
    "AI Analysis",
    "ROI Analysis",
    "Decision Summary",
    "Alerts"
])

machine = st.sidebar.selectbox("Select Machine", ["Machine A", "Machine B", "Machine C"])

health_status = get_system_health(st.session_state.failure_prob)

col1, col2 = st.columns([6,3])
with col1:
    st.title("AI Predictive Maintenance")
with col2:
    st.metric("Machine", machine)
    st.metric("Health", health_status)

st.divider()

# -----------------------------
# LIVE MONITORING
# -----------------------------
if page == "Live Monitoring":

    op1 = st.slider("Machine Load", 0.0, 1.0, 0.45)
    op2 = st.slider("Operating Speed", 0.0, 1.0, 0.34)
    op3 = st.slider("Environmental Stress", 0.0, 1.0, 0.89)

    sensor_values = [random.uniform(0,100) for _ in range(21)]
    st.session_state.input_data = [op1, op2, op3] + sensor_values

# -----------------------------
# AI ANALYSIS
# -----------------------------
elif page == "AI Analysis":

    if st.session_state.input_data is None:
        st.warning("Run Live Monitoring first")
    else:
        if st.button("Run Prediction"):

            result = predict_failure(st.session_state.input_data)
            prob = random.uniform(0.6,0.95) if result==1 else random.uniform(0.05,0.4)

            st.session_state.failure_prob = prob
            future = simulate_future(prob)
            st.session_state.future_prediction[machine] = future

        if st.session_state.failure_prob:
            st.metric("Failure Probability", f"{round(st.session_state.failure_prob*100,2)}%")

# -----------------------------
# ROI ANALYSIS
# -----------------------------
elif page == "ROI Analysis":

    future = st.session_state.future_prediction[machine]

    if not future:
        st.info("Run AI Analysis first")
    else:
        rul = len(future)
        maintenance_cost, failure_loss, avoided_loss, roi = roi_analysis(
            st.session_state.failure_prob,
            rul
        )

        st.metric("Maintenance Investment", f"₹{maintenance_cost}")
        st.metric("Potential Failure Loss", f"₹{int(failure_loss)}")
        st.metric("Loss Prevented", f"₹{int(avoided_loss)}")
        st.metric("ROI", f"{round(roi*100,2)} %")

# -----------------------------
# DECISION SUMMARY
# -----------------------------
elif page == "Decision Summary":

    future = st.session_state.future_prediction[machine]

    if not future:
        st.info("Run AI Analysis first")
    else:

        rul = len(future)
        maintenance_cost, failure_loss, avoided_loss, roi = roi_analysis(
            st.session_state.failure_prob,
            rul
        )

        decision, reason = decision_engine(
            st.session_state.failure_prob,
            rul,
            roi
        )

        st.subheader("Executive Decision Summary")

        st.metric("Recommended Action", decision)
        st.metric("Justification", reason)
        st.metric("Remaining Life (cycles)", rul)
        st.metric("ROI", f"{round(roi*100,2)}%")

# -----------------------------
# ALERTS
# -----------------------------
elif page == "Alerts":

    status = get_system_health(st.session_state.failure_prob)

    if status == "Critical":
        st.error("Critical risk detected.")
    elif status == "Warning":
        st.warning("Early warning signs detected.")
    elif status == "Healthy":
        st.success("System operating normally.")
    else:
        st.info("Run AI Analysis to generate system health.")
