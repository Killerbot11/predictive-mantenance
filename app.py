import streamlit as st
import matplotlib.pyplot as plt
import random
from utils import predict_failure
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

st.set_page_config(page_title="AI Predictive Maintenance", layout="wide")

REVENUE_PER_HOUR = 15000
FAILURE_DOWNTIME = 24
SCHEDULED_COST = 20000
ROUTINE_COST = 5000

machine_colors = {
    "Machine A": "blue",
    "Machine B": "green",
    "Machine C": "red"
}

if "health_history" not in st.session_state:
    st.session_state.health_history = {
        "Machine A": [],
        "Machine B": [],
        "Machine C": []
    }

if "future_prediction" not in st.session_state:
    st.session_state.future_prediction = {
        "Machine A": [],
        "Machine B": [],
        "Machine C": []
    }

if "failure_prob" not in st.session_state:
    st.session_state.failure_prob = None

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

def roi_analysis(prob, rul):
    maintenance_cost = SCHEDULED_COST if rul <= 6 else ROUTINE_COST
    failure_loss = prob * FAILURE_DOWNTIME * REVENUE_PER_HOUR
    avoided_loss = failure_loss - maintenance_cost
    roi = (avoided_loss - maintenance_cost) / maintenance_cost if maintenance_cost else 0
    return maintenance_cost, failure_loss, avoided_loss, roi

def decision_engine(rul, roi):
    if rul <= 3:
        return "Immediate Action Required"
    if roi > 0 and rul <= 6:
        return "Maintain Now"
    if roi > 0:
        return "Plan Maintenance"
    return "Monitor"

# -----------------------------
# PDF GENERATOR
# -----------------------------
def generate_pdf(machine, prob, rul, roi, decision):

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>AI Predictive Maintenance Report</b>", styles['Title']))
    story.append(Spacer(1,20))

    story.append(Paragraph(f"<b>Machine:</b> {machine}", styles['Normal']))
    story.append(Paragraph(f"<b>Failure Probability:</b> {round(prob*100,2)}%", styles['Normal']))
    story.append(Paragraph(f"<b>Remaining Useful Life:</b> {rul} cycles", styles['Normal']))
    story.append(Paragraph(f"<b>ROI:</b> {round(roi*100,2)}%", styles['Normal']))
    story.append(Paragraph(f"<b>Decision:</b> {decision}", styles['Normal']))

    doc.build(story)
    buffer.seek(0)
    return buffer

# -----------------------------
# LOGIN
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("AI Predictive Maintenance Platform")
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
    "Failure Forecast",
    "ROI Analysis",
    "Decision Summary",
    "Export Report"
])

machine = st.sidebar.selectbox("Select Machine", ["Machine A", "Machine B", "Machine C"])

st.title("AI Predictive Maintenance")
st.divider()

# -----------------------------
# DASHBOARD
# -----------------------------
if page == "Dashboard":

    fig, ax = plt.subplots()

    for m, history in st.session_state.health_history.items():
        if history:
            ax.plot(history, marker='o', label=m, color=machine_colors[m])

    ax.set_ylim(0,1)
    ax.legend()
    st.pyplot(fig)

# -----------------------------
# LIVE MONITORING
# -----------------------------
elif page == "Live Monitoring":

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
            st.session_state.health_history[machine].append(prob)
            future = simulate_future(prob)
            st.session_state.future_prediction[machine] = future

        if st.session_state.failure_prob:
            st.metric("Failure Probability", f"{round(st.session_state.failure_prob*100,2)}%")

# -----------------------------
# FAILURE FORECAST
# -----------------------------
elif page == "Failure Forecast":

    future = st.session_state.future_prediction[machine]

    if future:
        rul = len(future)
        fig, ax = plt.subplots()
        ax.plot(range(len(future)), future, marker='o', color=machine_colors[machine])
        ax.axhline(0.9, linestyle='--')
        ax.set_ylim(0,1)
        st.pyplot(fig)
        st.metric("Remaining Useful Life", rul)

# -----------------------------
# ROI ANALYSIS
# -----------------------------
elif page == "ROI Analysis":

    future = st.session_state.future_prediction[machine]

    if future:
        rul = len(future)
        maintenance_cost, failure_loss, avoided_loss, roi = roi_analysis(
            st.session_state.failure_prob,
            rul
        )

        st.metric("ROI", f"{round(roi*100,2)}%")

# -----------------------------
# DECISION SUMMARY
# -----------------------------
elif page == "Decision Summary":

    future = st.session_state.future_prediction[machine]

    if future:
        rul = len(future)
        _, _, _, roi = roi_analysis(st.session_state.failure_prob, rul)
        decision = decision_engine(rul, roi)

        st.metric("Executive Recommendation", decision)
        st.metric("Remaining Life", rul)

# -----------------------------
# PDF EXPORT
# -----------------------------
elif page == "Export Report":

    future = st.session_state.future_prediction[machine]

    if future:
        rul = len(future)
        _, _, _, roi = roi_analysis(st.session_state.failure_prob, rul)
        decision = decision_engine(rul, roi)

        pdf = generate_pdf(machine,
                           st.session_state.failure_prob,
                           rul,
                           roi,
                           decision)

        st.download_button(
            label="Download Executive Report",
            data=pdf,
            file_name="Predictive_Maintenance_Report.pdf",
            mime="application/pdf"
        )
    else:
        st.info("Run AI Analysis first")
