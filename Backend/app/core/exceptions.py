# ============================================================
# exceptions.py — The Error Rulebook
# ============================================================
# Instead of writing HTTPException(status_code=400, detail="...")
# everywhere, we define named classes once.
# Routes just do: raise NotFoundException()
# Clean, readable, professional.
# ============================================================

from fastapi import HTTPException, status

# 400 — User sent bad/wrong data
# Example: registering with an email that already exists
class BadRequestException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

# 401 — User is not logged in / token is missing or expired
# Example: trying to access dashboard without logging in
class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "Not authenticated"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

# 403 — User is logged in but not allowed to do this
# Example: a normal user trying to hit an admin-only route
class ForbiddenException(HTTPException):
    def __init__(self, detail: str = "Access forbidden"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

# 404 — The thing they asked for doesn't exist
# Example: fetching an analysis ID that was deleted
class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

# 429 — User hit their free plan limit
# Example: free users get 5 analyses, they tried a 6th
class UsageLimitException(HTTPException):
    def __init__(self, detail: str = "Free usage limit reached. Please upgrade."):
        super().__init__(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=detail)