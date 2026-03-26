import cv2
import numpy as np
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os
import tempfile

def preprocess_image(image_input):
    """
    Applies preprocessing to handle noisy images: grayscale, denoising, and thresholding.
    Receives either a path or a PIL Image object.
    """
    if isinstance(image_input, str):
        # Path
        img = cv2.imread(image_input)
    else:
        # PIL Image directly
        img = cv2.cvtColor(np.array(image_input), cv2.COLOR_RGB2BGR)

    if img is None:
        raise ValueError("Image not found or invalid format")
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Denoise (handles noisy/blurry images)
    denoised = cv2.fastNlMeansDenoising(gray, h=10)
    
    # Thresholding for a clearer text separation
    _, thresholded = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Save a temporary processed image
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        processed_path = tmp.name
        cv2.imwrite(processed_path, thresholded)
    
    return processed_path

def extract_text(file_path):
    """
    Extracts raw text from an image or a single-page PDF using Pytesseract.
    """
    try:
        # 1. Handle PDF
        if file_path.lower().endswith('.pdf'):
            # Convert first page to image
            images = convert_from_path(file_path, first_page=1, last_page=1)
            if not images:
                return "Error: Could not convert PDF to image."
            processed_path = preprocess_image(images[0])
        else:
            # Handle standard image formats
            processed_path = preprocess_image(file_path)
        
        # 2. Extract text using OCR
        text = pytesseract.image_to_string(Image.open(processed_path))
        
        # Cleanup
        if os.path.exists(processed_path):
            os.remove(processed_path)
            
        return text
    except Exception as e:
        return f"Error during OCR: {str(e)}"
