# ============================================================
# session.py — The Database Phone Line
# ============================================================
# Before your app can talk to MySQL, it needs a connection.
# This file:
# 1. Creates the engine (the actual MySQL connection pool)
# 2. Provides get_db() — a function every route uses to get
#    a fresh DB session, and auto-closes it after the request
# ============================================================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# create_engine connects to MySQL using the URL from .env
# pool_pre_ping=True → tests each connection before using it
#   (handles cases where MySQL dropped the connection silently)
# pool_recycle=3600 → refreshes connections every 1 hour
#   (prevents "MySQL server has gone away" errors on long-running apps)
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# SessionLocal is a class — calling SessionLocal() gives you a session
# autocommit=False → changes only save when you call db.commit()
# autoflush=False → SQLAlchemy won't auto-send pending changes before queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    # This is a FastAPI dependency — routes use: db: Session = Depends(get_db)
    # FastAPI calls this automatically, injects the session, and cleans up
    db = SessionLocal()
    try:
        yield db        # hands the session to the route function
    finally:
        db.close()      # ALWAYS runs — even if the route threw an error
                        # prevents connection leaks