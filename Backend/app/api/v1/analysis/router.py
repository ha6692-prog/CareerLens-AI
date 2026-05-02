# ============================================================
# analysis/router.py — Run & Fetch Analysis Endpoints
# ============================================================
# POST /analysis/run        → run AI analysis on a resume
# GET  /analysis/           → get all your past analyses
# GET  /analysis/{id}       → get one full analysis result
#
# All routes are protected — must be logged in.
# ============================================================

import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.analysis import AnalysisRequest, AnalysisResponse, AnalysisHistoryItem
from app.services.analysis_service import run_analysis, get_user_analyses
from app.models.analysis import Analysis
from app.api.v1.auth.dependencies import get_current_user
from app.models.user import User
from app.core.exceptions import NotFoundException

router = APIRouter()


@router.post("/run", response_model=AnalysisResponse, status_code=201)
def analyze_resume(
    data: AnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Run the full AI analysis pipeline
    analysis = run_analysis(
        resume_id=data.resume_id,
        job_description=data.job_description,
        user=current_user,
        db=db,
    )

    # Parse JSON strings back to lists before sending to frontend
    return _format_analysis(analysis)


@router.get("/", response_model=List[AnalysisHistoryItem])
def list_analyses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    analyses = get_user_analyses(user_id=current_user.id, db=db)
    return analyses


@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id,
        Analysis.user_id == current_user.id   # security: only your own analyses
    ).first()

    if not analysis:
        raise NotFoundException(detail="Analysis not found")

    return _format_analysis(analysis)


def _format_analysis(analysis: Analysis) -> dict:
    # Helper to parse JSON strings from DB into Python lists
    # The DB stores '["Docker","AWS"]' — frontend expects ["Docker", "AWS"]
    return {
        "id": analysis.id,
        "resume_id": analysis.resume_id,
        "match_score": analysis.match_score,
        "missing_keywords": json.loads(analysis.missing_keywords or "[]"),
        "suggestions": json.loads(analysis.suggestions or "[]"),
        "ai_feedback": analysis.ai_feedback,
        "created_at": analysis.created_at,
    }