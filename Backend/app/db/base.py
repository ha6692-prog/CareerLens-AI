# ============================================================
# base.py — The Blueprint Registry
# ============================================================
# Base is the parent class all your database models inherit from.
# SQLAlchemy uses it to track every table in your app.
#
# The imports at the bottom exist ONLY so Alembic can find
# all models in one place when generating migrations.
# Without them, Alembic won't create those tables.
# ============================================================

from sqlalchemy.orm import declarative_base

# Every model does: class User(Base) — which registers it here
# SQLAlchemy then knows to create a "users" table in MySQL
Base = declarative_base()

# These are imported here purely for Alembic's benefit
# Alembic scans Base to find all registered models
# If a model isn't imported here → Alembic ignores it → table never created
from app.models.user import User       # noqa: F401, E402
from app.models.resume import Resume   # noqa: F401, E402
from app.models.analysis import Analysis  # noqa: F401, E402