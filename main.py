from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.routes import router as ocr_router
import uvicorn
import os

app = FastAPI(title="SmartDoc AI Service", version="1.0.0")

# Setup folder structure
if not os.path.exists("uploads"):
    os.makedirs("uploads")
    
if not os.path.exists("static"):
    os.makedirs("static")

# Include OCR extraction routes
app.include_router(ocr_router, prefix="/api")

# Serve static frontend (HTML, CSS, JS)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    # Start the application
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
