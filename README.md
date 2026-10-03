# CGHS AI Prototype

Student prototype showing how AI/ML can improve India's Central Government Health Scheme (CGHS) portal.

## Modules

1. **Smart Appointment + No‑Show Predictor**
   - Predicts which beneficiaries are likely to miss appointments.
   - Shows admin dashboard with no‑show risk and overbooking suggestions.

2. **Reimbursement Document Validator**
   - Upload claim documents (CGHS card, referral, discharge summary, bills).
   - AI checks completeness & readability and returns a checklist.

## Tech Stack

- Python 3.10+
- scikit‑learn, XGBoost
- pandas, numpy
- pytesseract (OCR)
- Streamlit (UI)

## Datasets

- Appointment no‑show: Kaggle “Healthcare Appointment No Shows” or similar.
- Claims documents: synthetic / sample PDFs for demo.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Run app

```bash
streamlit run app/app.py
```

## Note

This is a **student prototype** for demonstration only. Not connected to the real CGHS system.

## MADE BY 

MEHAK SHARMA
