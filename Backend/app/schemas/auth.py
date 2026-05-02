# ============================================================
# schemas/auth.py — Auth Request & Response Shapes
# ============================================================
# Schemas are like customs forms at an airport.
# Before any data enters your app, it must match the form exactly.
# Wrong field? Wrong type? Missing field? → Rejected automatically.
#
# Pydantic does this validation for you — no manual if/else checks.
# ============================================================

from pydantic import BaseModel, EmailStr
from datetime import datetime


# ── REQUESTS (data coming IN from the frontend) ──────────────

class RegisterRequest(BaseModel):
    # EmailStr → pydantic automatically validates it's a real email format
    # "hitesh" → rejected. "hitesh@gmail.com" → accepted.
    email: EmailStr
    password: str
    full_name: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ── RESPONSES (data going OUT to the frontend) ────────────────

class UserResponse(BaseModel):
    # This is what we send back about a user — notice NO hashed_password
    # Never expose the password hash to the frontend, even hashed
    id: int
    email: str
    full_name: str
    analyses_used: int
    free_limit: int
    created_at: datetime

    class Config:
        # Allows pydantic to read data directly from SQLAlchemy model objects
        # Without this: you'd have to manually convert user → dict every time
        from_attributes = True


class TokenResponse(BaseModel):
    # What the frontend receives after a successful login
    access_token: str
    token_type: str = "bearer"  # standard OAuth2 convention
    user: UserResponse