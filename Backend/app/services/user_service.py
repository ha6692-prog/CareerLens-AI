# ============================================================
# user_service.py — User Profile & Usage Logic
# ============================================================
# Handles anything related to reading/updating user data
# that isn't auth — like fetching profile, checking usage,
# or resetting the limit (admin feature later).
# ============================================================

from sqlalchemy.orm import Session
from app.models.user import User
from app.core.exceptions import NotFoundException


def get_user_by_id(user_id: int, db: Session) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundException(detail="User not found")
    return user


def get_usage_stats(user: User) -> dict:
    # Returns how many analyses the user has used vs their limit
    # Used on the dashboard to show "3 / 5 free analyses used"
    return {
        "analyses_used": user.analyses_used,
        "free_limit": user.free_limit,
        "analyses_remaining": max(0, user.free_limit - user.analyses_used),
        "is_limit_reached": user.analyses_used >= user.free_limit,
    }