from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import shutil
import os
from PyPDF2 import PdfReader

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Backend is running successfully!"}

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text if it's a PDF
    extracted_text = ""
    if file.filename.endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            extracted_text += page.extract_text() or ""  # avoid None errors

    return {
        "filename": file.filename,
        "extracted_text": extracted_text.strip()[:1000]  # limit for now
    }

# Allow requests from frontend (localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
