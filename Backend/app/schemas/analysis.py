# ============================================================
# schemas/analysis.py — Analysis Request & Response Shapes
# ============================================================
# The user sends: resume_id + job_description
# We send back: match score + missing keywords + suggestions
# ============================================================

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# ── REQUEST ───────────────────────────────────────────────────

class AnalysisRequest(BaseModel):
    # The ID of the resume to analyze (must already be uploaded)
    resume_id: int

    # The job posting the user copied and pasted
    job_description: str


# ── RESPONSES ─────────────────────────────────────────────────

class AnalysisResponse(BaseModel):
    id: int
    resume_id: int
    match_score: Optional[float] = None

    # These come back as lists — we parse the JSON string from DB in the service
    missing_keywords: Optional[List[str]] = None
    suggestions: Optional[List[str]] = None
    ai_feedback: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AnalysisHistoryItem(BaseModel):
    # Lighter version used in the history list page
    # We don't send full ai_feedback in the list — too much data
    id: int
    resume_id: int
    match_score: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True