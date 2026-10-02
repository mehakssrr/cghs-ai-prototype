import pytesseract
from PIL import Image
from src.config import OCR_CONFIDENCE_THRESHOLD

def extract_text_from_image(image_path: str) -> dict:
    img = Image.open(image_path)
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    
    text_lines = []
    confidences = []
    
    for i, text in enumerate(data["text"]):
        conf = data["conf"][i]
        if text.strip() == "":
            continue
        text_lines.append(text.strip())
        confidences.append(conf)
    
    full_text = " ".join(text_lines)
    avg_conf = sum(confidences) / len(confidences) if confidences else 0
    
    return {
        "text": full_text,
        "avg_confidence": avg_conf,
        "readable": avg_conf >= OCR_CONFIDENCE_THRESHOLD
    }
