from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
from ocr.processor import extract_text
from parser.extractor import parse_structured_data
import pydantic

router = APIRouter()

class OCRResponse(pydantic.BaseModel):
    date: str = None
    total: float = 0.0
    items: list = []
    raw_text: str = ""

@router.post("/extract", response_model=OCRResponse)
async def extract_receipt_data(file: UploadFile = File(...)):
    """
    POST /extract -> returns structured JSON from receipt images or PDFs.
    """
    # Create uploads dir if it doesn't exist
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
        
    file_path = f"uploads/{file.filename}"
    
    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        # 1. OCR text extraction
        raw_text = extract_text(file_path)
        
        # 2. Extract structured data from text
        structured_data = parse_structured_data(raw_text)
        
        # 3. Form response
        response_data = OCRResponse(
            **structured_data,
            raw_text=raw_text
        )
        
        return response_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)
