from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil, os
from PyPDF2 import PdfReader
import subprocess
import json

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
            if page.extract_text():
                extracted_text += page.extract_text() + "\n"

    return {
        "filename": file.filename,
        "extracted_text": extracted_text.strip()[:2000]  # limit for speed
    }

# NEW: Ask LLM about PDF
@app.post("/ask/")
async def ask_pdf(question: str = Form(...), context: str = Form(...)):
    prompt = f"""
    You are a helpful assistant. Answer the following question based on the context.

    Context: {context[:2000]}

    Question: {question}
    """

    # Call Ollama locally
    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt.encode("utf-8"),
        capture_output=True
    )

    answer = result.stdout.decode("utf-8").strip()
    return {"answer": answer}
    

# Allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
