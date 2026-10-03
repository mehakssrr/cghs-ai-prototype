import streamlit as st
import pandas as pd
import joblib
import numpy as np
from src.config import NOSHOW_MODEL_PATH

@st.cache_resource
def load_model():
    return joblib.load(NOSHOW_MODEL_PATH)

def show_appointment_module():
    st.header("Smart Appointments (Demo)")
    
    st.subheader("Beneficiary: Book Appointment")
    age = st.number_input("Age", 1, 100, 45)
    gender = st.selectbox("Gender", ["M", "F"])
    is_senior = 1 if age >= 60 else 0
    
    if st.button("Predict No‑Show Risk"):
        model = load_model()
        X = pd.DataFrame({
            "Age": [age],
            "is_senior": [is_senior],
            "gender_male": [1 if gender == "M" else 0]
        })
        prob = model.predict_proba(X)[0, 1]
        st.write(f"Predicted no‑show risk: **{prob:.2%}**")
        if prob > 0.4:
            st.warning("High risk of missing appointment. Consider sending extra reminders.")
        else:
            st.success("Risk is moderate/low.")
    
    st.divider()
    
    st.subheader("Admin: Today’s Appointments (Sample)")
    # Fake data for demo
    df = pd.DataFrame({
        "Time": ["09:00", "09:30", "10:00", "10:30", "11:00"],
        "Age": [65, 42, 58, 70, 33],
        "Gender": ["M", "F", "F", "M", "F"],
    })
    model = load_model()
    df["is_senior"] = (df["Age"] >= 60).astype(int)
    df["gender_male"] = (df["Gender"] == "M").astype(int)
    X = df[["Age", "is_senior", "gender_male"]]
    df["No‑Show Risk"] = model.predict_proba(X)[:, 1]
    
    st.dataframe(df)
    high_risk = df[df["No‑Show Risk"] > 0.4].shape[0]
    st.write(f"High‑risk appointments today: **{high_risk}**")
    if high_risk > 0:
        st.info(f"Suggestion: You can safely overbook **{min(high_risk, 2)}** extra slots.")
