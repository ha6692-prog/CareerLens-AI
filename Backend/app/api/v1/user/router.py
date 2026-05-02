# ============================================================
# user/router.py — User Profile & Usage Endpoints
# ============================================================
# GET /user/profile   → get your full profile
# GET /user/usage     → how many analyses used vs limit
# ============================================================

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.auth import UserResponse
from app.services.user_service import get_usage_stats
from app.api.v1.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/profile", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    # current_user is already loaded by the dependency
    return current_user


@router.get("/usage")
def get_usage(current_user: User = Depends(get_current_user)):
    # Returns usage stats for the dashboard
    # e.g. { "analyses_used": 3, "free_limit": 5, "analyses_remaining": 2 }
    return get_usage_stats(user=current_user)