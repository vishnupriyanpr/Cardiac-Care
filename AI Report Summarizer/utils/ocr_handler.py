# utils/ocr_handler.py

import pytesseract
from PIL import Image
import os
from pdf2image import convert_from_path

POPPLER_PATH = r"C:\Program Files\poppler-23.11.0\poppler-24.08.0\Library\bin"

def extract_text_tesseract(file_path):
    try:
        if file_path.lower().endswith('.pdf'):
            return extract_text_from_pdf(file_path)
        else:
            return extract_text_from_image(file_path)
    except Exception as e:
        return f"Error: {e}"

def extract_text_from_image(file_path):
    img = Image.open(file_path)
    text = pytesseract.image_to_string(img)
    return text.strip()

def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path, dpi=300, poppler_path=POPPLER_PATH)
    all_text = []
    for i, img in enumerate(images):
        text = pytesseract.image_to_string(img)
        all_text.append(f"\n--- Page {i + 1} ---\n{text.strip()}")
    return "\n".join(all_text).strip()
