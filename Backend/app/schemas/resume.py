# ============================================================
# schemas/resume.py — Resume Request & Response Shapes
# ============================================================
# File uploads don't use JSON — they use multipart/form-data.
# So the "request" schema here is minimal (just the file itself).
# The response schemas define what we send back after upload/fetch.
# ============================================================

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ── RESPONSES ─────────────────────────────────────────────────

class ResumeResponse(BaseModel):
    # Sent back after a resume is uploaded or when listing resumes
    id: int
    filename: str
    created_at: datetime

    # We don't send file_path or extracted_text to the frontend
    # file_path is an internal server path — frontend doesn't need it
    # extracted_text can be huge — we only send it when specifically needed

    class Config:
        from_attributes = True


class ResumeDetailResponse(BaseModel):
    # Full detail — used when frontend needs the extracted text
    # e.g. to display "here is what we read from your PDF"
    id: int
    filename: str
    extracted_text: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True