# ============================================================
# main.py — The Front Door
# ============================================================
# This is where FastAPI starts.
# It does 4 things:
# 1. Creates the FastAPI app
# 2. Adds CORS middleware (allows frontend to talk to backend)
# 3. Adds request logging middleware
# 4. Registers all route groups under their URL prefixes
#
# When you run: uvicorn main:app --reload
# Python runs this file and starts the server.
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.db.session import engine
from app.db.base import Base
from app.middleware.logging import log_requests

# Import all routers
from app.api.v1.auth.router     import router as auth_router
from app.api.v1.resume.router   import router as resume_router
from app.api.v1.analysis.router import router as analysis_router
from app.api.v1.user.router     import router as user_router

# Create all database tables automatically on startup
# SQLAlchemy looks at all models registered with Base and creates
# any tables that don't exist yet — safe to run multiple times
Base.metadata.create_all(bind=engine)

# Create the FastAPI app instance
app = FastAPI(
    title="CareerLens AI",
    description="AI-powered resume analysis API",
    version="1.0.0",
)

# ── CORS Middleware ───────────────────────────────────────────
# CORS = Cross-Origin Resource Sharing
# Browsers block requests from one domain to another by default.
# This tells the browser: "requests from localhost:5173 are allowed"
# In production you'd replace localhost:5173 with your real frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],   # your Vite frontend URL
    allow_credentials=True,                    # allows cookies/auth headers
    allow_methods=["*"],                       # allow GET, POST, DELETE etc.
    allow_headers=["*"],                       # allow Authorization header etc.
)

# ── Logging Middleware ────────────────────────────────────────
# Logs every request: POST /auth/login → 200 (142ms)
app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests)

# ── Routes ───────────────────────────────────────────────────
# prefix="/api/v1/auth" means all routes in auth_router
# become: /api/v1/auth/register, /api/v1/auth/login etc.
app.include_router(auth_router,     prefix="/api/v1/auth",     tags=["Auth"])
app.include_router(resume_router,   prefix="/api/v1/resume",   tags=["Resume"])
app.include_router(analysis_router, prefix="/api/v1/analysis", tags=["Analysis"])
app.include_router(user_router,     prefix="/api/v1/user",     tags=["User"])


@app.get("/")
def root():
    # Health check — open http://localhost:8000 in browser to confirm server is running
    return {"status": "running", "app": "CareerLens AI", "version": "1.0.0"}