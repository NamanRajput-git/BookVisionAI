import cv2
import pytesseract
import os
import shutil

# Check for TESSERACT_PATH env var, else default
tesseract_cmd = os.getenv("TESSERACT_PATH", r"C:\Program Files\Tesseract-OCR\tesseract.exe")
if not os.path.exists(tesseract_cmd):
    # Try to find in PATH
    tesseract_cmd_shutil = shutil.which("tesseract")
    if tesseract_cmd_shutil:
        tesseract_cmd = tesseract_cmd_shutil
    else:
        print(f"Warning: Tesseract not found at {tesseract_cmd}. OCR may fail.")

pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

def run_ocr(image_path: str):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    data = pytesseract.image_to_data(
        gray, output_type=pytesseract.Output.DICT
    )

    text = " ".join([t for t in data["text"] if t.strip()])
    
    # Filter valid confidence values (tesseract returns -1 for invalid)
    confs = []
    for c in data["conf"]:
        try:
            val = int(c)
            if val >= 0:
                confs.append(val)
        except (ValueError, TypeError):
            pass

    confidence = sum(confs) / len(confs) / 100 if confs else 0.0

    return text.strip(), confidence
