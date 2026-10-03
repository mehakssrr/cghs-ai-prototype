
import pytesseract
from PIL import Image
import os

def extract_text_from_image(image_path: str) -> str:
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

def extract_text_from_pdf(pdf_path: str) -> str:
    from pdf2image import convert_from_path
    pages = convert_from_path(pdf_path, first_page=1, last_page=1)
    img = pages[0]
    text = pytesseract.image_to_string(img)
    return text

def quick_check_cgHS(text: str) -> dict:
    text_lower = text.lower()
    checks = {
        "has_cghs_keyword": any(k in text_lower for k in ["cghs", "central government health"]),
        "has_date": any(ch.isdigit() for ch in text[:200]),
        "has_hospital_keyword": any(k in text_lower for k in ["hospital", "clinic", "medical"]),
    }
    return checks
