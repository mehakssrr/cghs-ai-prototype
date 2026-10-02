import streamlit as st
import os
import tempfile
from ocr_utils.ocr_extractor import extract_text_from_image, quick_check_cgHS

st.set_page_config(page_title="CGHS Claims Checker", layout="wide")
st.title("CGHS – Reimbursement Document Validator (Prototype)")

st.markdown("""
Upload your claim documents. This tool **checks completeness and readability**
using simple AI/OCR. It does **not** guarantee approval by CGHS.
""")

claim_type = st.selectbox("Claim Type", ["OPD", "IPD"])

st.subheader("Upload Documents")

uploaded_files = st.file_uploader(
    "Upload CGHS card, referral, bills, discharge summary, etc.",
    accept_multiple_files=True
)

if not uploaded_files:
    st.info("No files uploaded yet.")
    st.stop()

results = []

for f in uploaded_files:
    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(f.read())
        tmp_path = tmp.name

    # For demo, assume images only; extend for PDF later
    try:
        text = extract_text_from_image(tmp_path)
    except Exception as e:
        text = ""
        error = str(e)
    else:
        error = None

    checks = quick_check_cgHS(text) if text else {}

    results.append({
        "file": f.name,
        "text_length": len(text),
        "checks": checks,
        "error": error
    })

    os.remove(tmp_path)

st.subheader("Validation Results")

for r in results:
    st.write(f"**File:** {r['file']}")
    if r["error"]:
        st.error(f"OCR error: {r['error']}")
    else:
        if r["text_length"] == 0:
            st.warning("No text extracted (maybe blurry or unsupported format).")
        else:
            st.success(f"Text extracted ({r['text_length']} chars).")

        checks = r.get("checks", {})
        if checks.get("has_cghs_keyword"):
            st.write("- ✅ CGHS keyword found")
        else:
            st.write("- ⚠️ CGHS keyword NOT found (check if this is a CGHS document).")

        if checks.get("has_hospital_keyword"):
            st.write("- ✅ Hospital/clinic keyword found")
        else:
            st.write("- ⚠️ Hospital/clinic keyword NOT found.")

    st.markdown("---")

st.info("Next step (concept): show a checklist like ‘Missing: referral letter’ and generate a PDF summary.")
st.caption("This is a student prototype, not connected to the real CGHS system.")
