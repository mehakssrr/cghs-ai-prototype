from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

# No-show model
NOSHOW_MODEL_PATH = MODELS_DIR / "noshow_model.pkl"

# CGHS document validation rules
REQUIRED_DOCS_IPD = [
    "cghs_card",
    "referral_letter",
    "discharge_summary",
    "hospital_bill",
]

REQUIRED_DOCS_OPD = [
    "cghs_card",
    "referral_letter",
    "prescription",
    "hospital_bill",
]

OCR_CONFIDENCE_THRESHOLD = 60  # Tesseract confidence score
