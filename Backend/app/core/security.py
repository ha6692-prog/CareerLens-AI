# ============================================================
# security.py — The Security Guard
# ============================================================
# Two jobs:
# 1. Password hashing — never store plain passwords in the DB
# 2. JWT tokens — a signed "stamp" given to users on login
#    so they don't have to send their password on every request
# ============================================================

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.core.config import settings
from app.core.exceptions import UnauthorizedException

# bcrypt is the industry standard hashing algorithm
# "deprecated=auto" means passlib will warn if we use an old scheme
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    # Turns "mypassword123" → "$2b$12$eImiTXuWVxfM37..."
    # One-way — you can NEVER reverse this back to the original
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    # Hashes the plain text and compares it to the stored hash
    # Returns True if they match, False if not
    # Used during login to check the submitted password
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    # Token expires after X minutes (set in .env → config.py)
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # jwt.encode signs the data using your SECRET_KEY
    # Result is a long string like "eyJhbGci..." sent to the frontend
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


def decode_access_token(token: str) -> dict:
    try:
        # Verifies the token signature and checks it hasn't expired
        # Returns the original dict that was encoded (e.g. {"sub": "1", "email": "..."})
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        # Token is fake, tampered with, or expired → reject the request
        raise UnauthorizedException(detail="Token is invalid or expired")