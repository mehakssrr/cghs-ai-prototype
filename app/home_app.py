import streamlit as st

st.set_page_config(page_title="CGHS AI Prototype", layout="wide")
st.title("CGHS AI – Student Prototype")

st.markdown("""
This repository demonstrates how AI/ML can improve the **Central Government Health Scheme (CGHS)** portal and services.

Modules in this prototype:
- **Smart Appointments** – predicts no‑show risk and suggests overbooking.
- **Claims Document Validator** – checks if uploaded documents are complete and readable.

These are **concept prototypes** for learning and demonstration, not official CGHS tools.
""")

st.subheader("Choose a module:")

if st.button("Open Smart Appointments"):
    # In Streamlit Cloud you’d use pages; locally, just tell user which file to run
    st.code("streamlit run app/appointment_app.py", language="bash")

if st.button("Open Claims Document Validator"):
    st.code("streamlit run app/claims_app.py", language="bash")

st.markdown("""
### How to run locally

From the repository root:

```bash
streamlit run app/appointment_app.py
streamlit run app/claims_app.py
```
""")
