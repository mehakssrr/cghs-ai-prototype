
import streamlit as st
import pandas as pd
import joblib
import os
import numpy as np

PROJECT_DIR = "/content/drive/MyDrive/cghs-ai-prototype"

MODEL_PATH = os.path.join(PROJECT_DIR, "ml_models", "noshow_model.pkl")
PREPROCESS_PATH = os.path.join(PROJECT_DIR, "ml_models", "preprocess_noshow.pkl")

model = joblib.load(MODEL_PATH)
preprocess_info = joblib.load(PREPROCESS_PATH)
feature_cols = preprocess_info["feature_cols"]

st.set_page_config(page_title="CGHS Smart Appointments", layout="wide")
st.title("CGHS – Smart Appointment & No‑Show Predictor")

st.markdown("""
This is a **student prototype** to show how AI can improve CGHS appointments.
It predicts the chance that a patient might miss an appointment.
""")

st.header("1. Book an Appointment (Beneficiary View)")

with st.form("booking_form"):
    age = st.number_input("Age", min_value=0, max_value=120, value=45)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    city = st.selectbox("City", ["Chandigarh", "Delhi", "Other"])
    centre = st.selectbox("Wellness Centre", ["Sector‑22", "Sector‑34", "Main Market"])
    date = st.date_input("Preferred Date")
    time_slot = st.selectbox("Time Slot", ["9:00–9:30", "9:30–10:00", "10:00–10:30"])

    submitted = st.form_submit_button("Book Appointment")

if submitted:
    features = pd.DataFrame({
        "age": [age]
    })[feature_cols]

    no_show_prob = float(model.predict_proba(features)[0, 1])
    show_prob = 1 - no_show_prob

    st.success("Appointment booked (demo)!")
    st.write(f"**Predicted chance you will attend:** {show_prob:.1%}")
    st.write("We’ll send you an SMS reminder 1 day before.")

st.markdown("---")

st.header("2. Admin Dashboard (Wellness Centre)")
st.markdown("Today’s appointments with **no‑show risk** (demo data):")

demo_patients = [
    {"time": "9:00–9:30", "age": 68, "type": "Pensioner"},
    {"time": "9:30–10:00", "age": 42, "type": "Serving"},
    {"time": "10:00–10:30", "age": 55, "type": "Serving"},
    {"time": "10:30–11:00", "age": 72, "type": "Pensioner"},
]

rows = []
for p in demo_patients:
    feats = pd.DataFrame({"age": [p["age"]]})[feature_cols]
    risk = float(model.predict_proba(feats)[0, 1])
    rows.append({
        "Time": p["time"],
        "Age": p["age"],
        "Type": p["type"],
        "No‑show risk": f"{risk:.1%}"
    })

df_demo = pd.DataFrame(rows)
st.dataframe(df_demo, use_container_width=True)

avg_risk = np.mean([float(r["No‑show risk"].rstrip("%"))/100 for r in rows])
overbook_rec = max(1, int(round(avg_risk * len(rows))))

st.info(f"Average no‑show risk: {avg_risk:.1%}. "
        f"Suggested overbooking: **{overbook_rec}** extra slots today.")

st.caption("This is a student prototype, not connected to the real CGHS system.")
