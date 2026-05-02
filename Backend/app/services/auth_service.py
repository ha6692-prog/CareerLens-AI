# ============================================================
# auth_service.py — Register & Login Logic
# ============================================================
# Routes are just traffic directors — they receive the request
# and hand it off to a service.
# Services do the actual work: check the DB, hash passwords,
# create tokens, return results.
#
# Why separate from routes?
# If you ever want to add Google login or change how tokens work,
# you only touch this file — not 10 different route files.
# ============================================================

from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest
from app.core.security import hash_password, verify_password, create_access_token
from app.core.exceptions import BadRequestException, UnauthorizedException


def register_user(data: RegisterRequest, db: Session) -> User:
    # Step 1 — Check if email is already taken
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        # Raise our custom exception → FastAPI sends 400 to frontend
        raise BadRequestException(detail="An account with this email already exists")

    # Step 2 — Hash the password before storing
    # NEVER store data.password directly
    new_user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        full_name=data.full_name,
    )

    # Step 3 — Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)   # refresh loads the auto-generated id, created_at etc.

    return new_user


def login_user(data: LoginRequest, db: Session) -> dict:
    # Step 1 — Find user by email
    user = db.query(User).filter(User.email == data.email).first()

    # Step 2 — Check password (also covers "user not found" case)
    # We check both in one condition so we don't reveal whether
    # the email exists — security best practice
    if not user or not verify_password(data.password, user.hashed_password):
        raise UnauthorizedException(detail="Invalid email or password")

    # Step 3 — Check account is active
    if not user.is_active:
        raise UnauthorizedException(detail="Account is disabled")

    # Step 4 — Create JWT token with user identity inside it
    token = create_access_token(data={"sub": str(user.id), "email": user.email})

    return {"token": token, "user": user}