# ============================================================
# dependencies.py — The Auth Guard
# ============================================================
# This file answers one question on every protected request:
# "Who is this person and are they logged in?"
#
# Any route that needs a logged-in user adds this one line:
#   current_user: User = Depends(get_current_user)
# FastAPI automatically runs this check before the route runs.
# If the token is missing or invalid → request is rejected here.
# The route function never even runs.
# ============================================================

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import decode_access_token
from app.core.exceptions import UnauthorizedException
from app.models.user import User

# OAuth2PasswordBearer tells FastAPI:
# "Look for a Bearer token in the Authorization header"
# tokenUrl is just for the Swagger /docs UI to know where to login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),   # extracts token from header automatically
    db: Session = Depends(get_db)          # opens a DB session automatically
) -> User:

    # Step 1 — Decode and verify the JWT token
    # If token is expired or fake → decode_access_token raises UnauthorizedException
    payload = decode_access_token(token)

    # Step 2 — Extract user ID from the token payload
    user_id: str = payload.get("sub")
    if not user_id:
        raise UnauthorizedException(detail="Invalid token payload")

    # Step 3 — Fetch the actual user from the database
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise UnauthorizedException(detail="User no longer exists")

    # Step 4 — Check account is still active
    if not user.is_active:
        raise UnauthorizedException(detail="Account is disabled")

    # If all checks pass — return the user object to the route
    return user