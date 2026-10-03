import streamlit as st
from app.appointment_module import show_appointment_module
from app.claims_module import show_claims_module

st.set_page_config(page_title="CGHS AI Prototype", layout="wide")

st.title("CGHS AI Prototype")
st.markdown("""
Student prototype showing how AI can improve CGHS services:
- Smart appointments with no‑show prediction
- Reimbursement document validator
""")

menu = ["Home", "Smart Appointments", "Claims Document Validator"]
choice = st.sidebar.selectbox("Module", menu)

if choice == "Home":
    st.header("Welcome")
    st.write("""
    This is a **demo prototype** for an AI‑enhanced CGHS portal.
    It is not connected to the real CGHS system.
    
    Explore:
    - **Smart Appointments**: see how no‑show prediction can optimize slots.
    - **Claims Validator**: upload sample documents and get a checklist.
    """)
elif choice == "Smart Appointments":
    show_appointment_module()
elif choice == "Claims Document Validator":
    show_claims_module()
