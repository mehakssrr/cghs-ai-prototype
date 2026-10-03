import re
from src.ocr_utils import extract_text_from_image

KEYWORDS_CGHS = ["cghs", "central government health scheme"]
KEYWORDS_REFERRAL = ["referral", "refer", "wellness centre"]
KEYWORDS_DISCHARGE = ["discharge summary", "discharge note"]
KEYWORDS_BILL = ["bill", "invoice", "amount", "rs.", "rupees"]

def check_cghs_card(text: str) -> dict:
    t = text.lower()
    found = any(k in t for k in KEYWORDS_CGHS)
    return {
        "is_cghs_card": found,
        "issues": [] if found else ["No CGHS mention detected"]
    }

def check_referral(text: str) -> dict:
    t = text.lower()
    found = any(k in t for k in KEYWORDS_REFERRAL)
    return {
        "is_referral": found,
        "issues": [] if found else ["No referral keywords detected"]
    }

def check_discharge(text: str) -> dict:
    t = text.lower()
    found = any(k in t for k in KEYWORDS_DISCHARGE)
    return {
        "is_discharge": found,
        "issues": [] if found else ["No discharge summary keywords detected"]
    }

def check_bill(text: str) -> dict:
    t = text.lower()
    found = any(k in t for k in KEYWORDS_BILL)
    has_amount = bool(re.search(r"\d+", text))
    issues = []
    if not found:
        issues.append("No bill/invoice keywords detected")
    if not has_amount:
        issues.append("No numeric amount detected")
    return {
        "is_bill": found,
        "issues": issues
    }

def validate_document(doc_type: str, text: str, readable: bool) -> dict:
    result = {
        "doc_type": doc_type,
        "readable": readable,
        "checks": {},
        "overall_ok": False,
        "issues": []
    }
    
    if not readable:
        result["issues"].append("Document text not clearly readable")
    
    if doc_type == "cghs_card":
        check = check_cghs_card(text)
        result["checks"]["cghs_card"] = check
    elif doc_type == "referral_letter":
        check = check_referral(text)
        result["checks"]["referral"] = check
    elif doc_type == "discharge_summary":
        check = check_discharge(text)
        result["checks"]["discharge"] = check
    elif doc_type == "hospital_bill":
        check = check_bill(text)
        result["checks"]["bill"] = check
    
    # Simple overall OK logic
    all_checks_ok = all(
        v.get("is_cghs_card", False) or
        v.get("is_referral", False) or
        v.get("is_discharge", False) or
        v.get("is_bill", False)
        for v in result["checks"].values()
    )
    result["overall_ok"] = all_checks_ok and readable
    return result
