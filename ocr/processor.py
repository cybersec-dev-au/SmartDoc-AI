import cv2
import numpy as np
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os
import tempfile

# --- TESSERACT CONFIGURATION ---
# Common installation paths on Windows
COMMON_TESSERACT_PATHS = [
    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
    r'C:\Users\USER\AppData\Local\Programs\Tesseract-OCR\tesseract.exe',
    r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe',
]

for path in COMMON_TESSERACT_PATHS:
    if os.path.exists(path):
        pytesseract.pytesseract.tesseract_cmd = path
        break

def preprocess_image(image_input):
    """
    Applies preprocessing to handle noisy images: grayscale, denoising, and thresholding.
    """
    if isinstance(image_input, str):
        img = cv2.imread(image_input)
    else:
        img = cv2.cvtColor(np.array(image_input), cv2.COLOR_RGB2BGR)

    if img is None:
        raise ValueError("Image not found or invalid format")
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, h=10)
    _, thresholded = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        processed_path = tmp.name
        cv2.imwrite(processed_path, thresholded)
    
    return processed_path

def extract_text(file_path):
    """
    Extracts raw text from an image or a single-page PDF using Pytesseract.
    """
    try:
        if file_path.lower().endswith('.pdf'):
            images = convert_from_path(file_path, first_page=1, last_page=1)
            if not images:
                return "Error: Could not convert PDF to image."
            processed_path = preprocess_image(images[0])
        else:
            processed_path = preprocess_image(file_path)
        
        # Check if tesseract is accessible
        try:
            text = pytesseract.image_to_string(Image.open(processed_path))
        except pytesseract.TesseractNotFoundError:
            return "ERROR_MISSING_TESSERACT"
        
        if os.path.exists(processed_path):
            os.remove(processed_path)
            
        return text
    except Exception as e:
        return f"Error during OCR: {str(e)}"
