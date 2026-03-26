# SmartDoc AI - Intelligent OCR Document Processing

SmartDoc AI is an automated document processing system for small businesses. It extracts structured data (Date, Total, Items) from receipts and invoices using OCR and modern preprocessing.

## ✨ Features
- **Upload Image/PDF**: Receipt or invoice formats.
- **Vibrant Frontend**: Modern glassmorph UI with smooth animations.
- **Smart Parsing**: Extract Date, Total Amount, and Line Items.
- **Noise Cleanup**: Built-in grayscale and thresholding for noisy images.
- **Export Anywhere**: One-click Export to CSV or Microsoft Excel.

## 🚀 Quick Setup

### 1. Install Tesseract OCR (Windows)
Download and install [Tesseract-OCR for Windows](https://github.com/UB-Mannheim/tesseract/wiki).
After installation, the app will try to find `tesseract.exe` automatically. If it fails, you can update the path in `ocr/processor.py`.

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the Server
```bash
python main.py
```
Open your browser at `http://localhost:8000`.

## 📂 Project Structure
- `/api`: FastAPI route handlers.
- `/ocr`: Text extraction and image processing logic.
- `/parser`: Logic for transforming raw text into structured JSON.
- `/static`: Frontend assets (Vibrant UI).
- `main.py`: Entry point.

## ⚙️ Tech Stack
- **Backend**: Python, FastAPI, Uvicorn, Pydantic, Pandas.
- **OCR Engine**: Pytesseract / Tesseract.
- **Preprocessing**: OpenCV (cv2).
- **Frontend**: HTML5, Vanilla CSS (Premium Design), Lucide icons.
