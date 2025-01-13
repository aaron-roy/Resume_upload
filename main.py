import fitz  # PyMuPDF
from fastapi import FastAPI, File, UploadFile
import os
from tempfile import NamedTemporaryFile
from database import add_resume
from helper import extract_pdf_text, parse_resume
from models.resume import ResumeSchema



# Initialize FastAPI app
app = FastAPI()

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}


# Endpoint to handle resume file upload and parsing
# 4 Steps:
# Step 1. Handle PDF file upload (convert PDF to string)
# Step 2. Parse resume content
# Step 3. Upload resume content to MongoDB (POST)
# Step 4. Response

@app.post("/resume/parse")
async def parse_resume_file(file: UploadFile = File(...)):

    ##############################
    # STEP 1: Handle PDF file upload (convert PDF to string)
    ##############################
    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(await file.read())
        tmp_file_path = tmp_file.name

    pdf_text = extract_pdf_text(tmp_file_path)

    ##############################
    # STEP 2: Parse resume content
    ##############################
    parsed_data = parse_resume(pdf_text)

    ##############################
    # STEP 3: Upload resume content to MongoDB (POST)
    ##############################
    resume_data = await add_resume(parsed_data)

    ##############################
    # STEP 4: Response
    ##############################
    return {
        "result": "success",
        "message": "Resume parsed and saved successfully",
        "data": resume_data
    }


    # return {"message": "Resume parsed and saved successfully", "pdf_text": pdf_text}
