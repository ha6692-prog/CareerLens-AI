# ============================================================
# resume_service.py — PDF Upload & Text Extraction Logic
# ============================================================
# When a user uploads a resume:
# 1. Save the PDF file to disk (in a folder per user)
# 2. Extract all text from the PDF using PyMuPDF
# 3. Save the file path + extracted text to the database
# ============================================================

import os
import fitz   # fitz is the import name for PyMuPDF
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models.resume import Resume
from app.core.exceptions import BadRequestException

# Folder where uploaded PDFs are stored on the server
UPLOAD_DIR = "uploads"


def save_resume(file: UploadFile, user_id: int, db: Session) -> Resume:
    # Step 1 — Only allow PDF files
    if not file.filename.endswith(".pdf"):
        raise BadRequestException(detail="Only PDF files are accepted")

    # Step 2 — Create a folder for this user if it doesn't exist
    # e.g. uploads/3/ for user with id=3
    user_folder = os.path.join(UPLOAD_DIR, str(user_id))
    os.makedirs(user_folder, exist_ok=True)

    # Step 3 — Build the full file path and save the file to disk
    file_path = os.path.join(user_folder, file.filename)
    with open(file_path, "wb") as f:
        content = file.file.read()
        f.write(content)

    # Step 4 — Extract text from the PDF using PyMuPDF
    extracted_text = extract_text_from_pdf(file_path)

    # Step 5 — Save resume record to the database
    resume = Resume(
        user_id=user_id,
        filename=file.filename,
        file_path=file_path,
        extracted_text=extracted_text,
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)

    return resume


def extract_text_from_pdf(file_path: str) -> str:
    # PyMuPDF opens the PDF and reads text from every page
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            # get_text() returns the raw text on that page
            text += page.get_text()
    return text.strip()


def get_user_resumes(user_id: int, db: Session) -> list:
    # Returns all resumes belonging to this user, newest first
    return (
        db.query(Resume)
        .filter(Resume.user_id == user_id)
        .order_by(Resume.created_at.desc())
        .all()
    )


def get_resume_by_id(resume_id: int, user_id: int, db: Session) -> Resume:
    # Fetches a specific resume — also checks it belongs to this user
    # Prevents user A from accessing user B's resume
    resume = (
        db.query(Resume)
        .filter(Resume.id == resume_id, Resume.user_id == user_id)
        .first()
    )
    if not resume:
        from app.core.exceptions import NotFoundException
        raise NotFoundException(detail="Resume not found")
    return resume