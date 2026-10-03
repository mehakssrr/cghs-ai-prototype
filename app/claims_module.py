import streamlit as st
import tempfile
import os
from src.ocr_utils import extract_text_from_image
from src.validation_rules import validate_document

def show_claims_module():
    st.header("CGHS Reimbursement Document Validator (Demo)")
    
    claim_type = st.selectbox("Claim Type", ["OPD", "IPD"])
    uploaded_files = st.file_uploader(
        "Upload documents (images/PDFs)",
        type=["png", "jpg", "jpeg", "pdf"],
        accept_multiple_files=True
    )
    
    if not uploaded_files:
        st.info("Upload sample documents to see validation.")
        return
    
    results = []
    
    for f in uploaded_files:
        doc_type = st.selectbox(
            f"Document type for {f.name}",
            ["cghs_card", "referral_letter", "discharge_summary", "hospital_bill", "prescription", "other"],
            key=f"doctype_{f.name}"
        )
        
        # Save temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(f.read())
            tmp_path = tmp.name
        
        ocr_result = extract_text_from_image(tmp_path)
        val_result = validate_document(
            doc_type,
            ocr_result["text"],
            ocr_result["readable"]
        )
        val_result["filename"] = f.name
        results.append(val_result)
        
        os.remove(tmp_path)
    
    st.subheader("Validation Results")
    for r in results:
        with st.expander(f"{r['filename']} ({r['doc_type']})"):
            st.write(f"Readable: **{r['readable']}**")
            st.write(f"Overall OK: **{r['overall_ok']}**")
            if r["issues"]:
                st.warning("Issues:")
                for iss in r["issues"]:
                    st.write(f"- {iss}")
            else:
                st.success("No obvious issues detected.")
    
    all_ok = all(r["overall_ok"] for r in results)
    st.divider()
    if all_ok:
        st.success("All uploaded documents look OK for submission (demo check).")
    else:
        st.error("Some documents have issues. Fix them before submitting your claim.")
