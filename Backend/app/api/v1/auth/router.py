# ============================================================
# auth/router.py — Register & Login Endpoints
# ============================================================
# These are the only two routes that DON'T need a logged-in user.
# Everything else requires Depends(get_current_user).
#
# POST /auth/register → create account
# POST /auth/login    → get JWT token
# GET  /auth/me       → get current user profile (protected)
# ============================================================

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from app.services.auth_service import register_user, login_user
from app.api.v1.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    # Pydantic already validated the request body matches RegisterRequest shape
    # Now hand it to the service to do the actual work
    user = register_user(data=data, db=db)
    return user


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    result = login_user(data=data, db=db)

    # Build the response in the shape TokenResponse expects
    return {
        "access_token": result["token"],
        "token_type": "bearer",
        "user": result["user"],
    }


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    # get_current_user already fetched the user from DB
    # Just return it — no extra DB call needed
    return current_user