# ============================================================
# resume/router.py — Upload & Fetch Resume Endpoints
# ============================================================
# POST /resume/upload     → upload a PDF resume
# GET  /resume/           → list all your resumes
# GET  /resume/{id}       → get one resume with extracted text
# DELETE /resume/{id}     → delete a resume
#
# All routes are protected — must be logged in.
# ============================================================

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.resume import ResumeResponse, ResumeDetailResponse
from app.services.resume_service import (
    save_resume, get_user_resumes, get_resume_by_id
)
from app.api.v1.auth.dependencies import get_current_user
from app.models.user import User
from app.models.resume import Resume
from app.core.exceptions import NotFoundException
import os

router = APIRouter()


@router.post("/upload", response_model=ResumeResponse, status_code=201)
def upload_resume(
    file: UploadFile = File(...),                    # File(...) means required file upload
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)   # must be logged in
):
    # Pass the file and user ID to the service
    # Service handles: validation, saving to disk, extracting text, saving to DB
    resume = save_resume(file=file, user_id=current_user.id, db=db)
    return resume


@router.get("/", response_model=List[ResumeResponse])
def list_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Returns all resumes for the logged-in user
    resumes = get_user_resumes(user_id=current_user.id, db=db)
    return resumes


@router.get("/{resume_id}", response_model=ResumeDetailResponse)
def get_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # FastAPI automatically extracts resume_id from the URL
    # Service checks it belongs to this user before returning
    resume = get_resume_by_id(resume_id=resume_id, user_id=current_user.id, db=db)
    return resume


@router.delete("/{resume_id}", status_code=204)
def delete_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resume = get_resume_by_id(resume_id=resume_id, user_id=current_user.id, db=db)

    # Delete the actual PDF file from disk first
    if os.path.exists(resume.file_path):
        os.remove(resume.file_path)

    # Then delete the database record
    db.delete(resume)
    db.commit()

    # 204 = success with no response body