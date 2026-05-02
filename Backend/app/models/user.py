# ============================================================
# models/user.py — The Users Table Definition
# ============================================================
# This file IS your "users" table in MySQL.
# Every Column here becomes a real column in the database.
# Open MySQL Workbench after running the app — you'll see
# this exact table with these exact columns.
# ============================================================

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class User(Base):
    __tablename__ = "users"     # actual table name in MySQL

    # Auto-incrementing primary key — every user gets a unique ID
    id              = Column(Integer, primary_key=True, index=True)
    full_name       = Column(String(255), nullable=False)

    # unique=True → no two users can share an email
    # index=True  → searching by email is fast (database index)
    email           = Column(String(255), unique=True, index=True, nullable=False)

    # NEVER store plain passwords — only the bcrypt hash
    hashed_password = Column(String(255), nullable=False)

    is_active       = Column(Boolean, default=True)

    # Tracks how many AI analyses this user has run
    analyses_used   = Column(Integer, default=0)

    # Free plan cap — 5 analyses before we ask them to upgrade
    free_limit      = Column(Integer, default=5)

    # server_default=func.now() → MySQL sets this automatically on INSERT
    created_at      = Column(DateTime(timezone=True), server_default=func.now())

    # onupdate=func.now() → MySQL updates this automatically on every UPDATE
    updated_at      = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships — ORM shortcuts, no SQL JOIN needed
    # user.resumes → returns all Resume rows for this user
    # cascade="all, delete" → deleting a user also deletes their resumes/analyses
    resumes   = relationship("Resume",   back_populates="owner", cascade="all, delete")
    analyses  = relationship("Analysis", back_populates="owner", cascade="all, delete")