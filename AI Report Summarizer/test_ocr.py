# test_ocr.py
from utils.ocr_handler import extract_text_tesseract

text = extract_text_tesseract("uploads/sample_report.pdf")
print("Extracted Text:\n", text)
