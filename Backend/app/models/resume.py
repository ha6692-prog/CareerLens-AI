# ============================================================
# models/resume.py — The Resumes Table Definition
# ============================================================
# When a user uploads a PDF:
#   - The actual file is saved to disk (e.g. uploads/1/cv.pdf)
#   - This table stores the METADATA about it:
#     who owns it, where it is, what text was extracted
# ============================================================

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Resume(Base):
    __tablename__ = "resumes"

    id      = Column(Integer, primary_key=True, index=True)

    # ForeignKey → every resume must belong to a user
    # If the user is deleted → their resumes are deleted too (cascade in User model)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Original filename the user uploaded (e.g. "My_Resume_2024.pdf")
    filename   = Column(String(255), nullable=False)

    # Where the file is physically saved on the server
    # e.g. "uploads/1/My_Resume_2024.pdf"
    file_path  = Column(String(500), nullable=False)

    # The raw text extracted from the PDF
    # Text type = unlimited length (unlike String which has a size limit)
    extracted_text = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # back_populates connects this to User.resumes — they point to each other
    owner    = relationship("User",     back_populates="resumes")
    analyses = relationship("Analysis", back_populates="resume", cascade="all, delete")