# ============================================================
# models/analysis.py — The Analysis Results Table
# ============================================================
# Every time a user runs an AI analysis, the result is saved here.
# This powers:
#   - The result page (show score + suggestions)
#   - The history page (all past analyses)
# ============================================================

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id      = Column(Integer, primary_key=True, index=True)

    # Links to the user who ran this analysis
    user_id   = Column(Integer, ForeignKey("users.id"),   nullable=False)

    # Links to which resume was used
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)

    # The job description the user pasted in — saved for history reference
    job_description = Column(Text, nullable=False)

    # AI match score between 0.0 and 100.0
    # e.g. 72.5 means "your resume matches 72.5% of this job's requirements"
    match_score = Column(Float, nullable=True)

    # Stored as a JSON string — e.g. '["Docker", "AWS", "Kubernetes"]'
    # We serialize/deserialize this in the service layer
    missing_keywords = Column(Text, nullable=True)

    # AI improvement suggestions — also a JSON string
    suggestions = Column(Text, nullable=True)

    # The full raw text response from the Groq AI model
    ai_feedback = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner  = relationship("User",   back_populates="analyses")
    resume = relationship("Resume", back_populates="analyses")