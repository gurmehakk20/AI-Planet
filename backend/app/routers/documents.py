# app/routers/documents.py
from fastapi import APIRouter, UploadFile, File
import os
from app.utils.pdf_processing import extract_text_from_pdf

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    # Extract text for KnowledgeBase (mock embedding)
    text = extract_text_from_pdf(file_location)
    return {"status": "success", "filename": file.filename, "extracted_text": text[:200]}  # return first 200 chars
