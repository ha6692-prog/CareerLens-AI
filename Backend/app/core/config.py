# pydantic-settings lets us load .env file values into a typed Python class
# This means if SECRET_KEY is missing from .env, the app crashes immediately
# with a clear error — instead of failing silently later
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # --- Database ---
    # This is the full MySQL connection string
    # Format: mysql+pymysql://USER:PASSWORD@HOST:PORT/DB_NAME
    DATABASE_URL: str

    # --- Security ---
    # Used to sign JWT tokens — if someone gets this key they can fake logins
    SECRET_KEY: str
    # How long a login token stays valid (1440 minutes = 24 hours)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # --- Groq AI ---
    # Your Groq API key for calling the AI model
    GROQ_API_KEY: str

    # --- App Meta ---
    APP_ENV: str = "development"   # switches to "production" on deploy
    APP_NAME: str = "CareerLens AI"
    API_VERSION: str = "v1"

    class Config:
        # Tells pydantic to read values from the .env file automatically
        env_file = ".env"
        # If .env has extra variables we didn't define above, just ignore them
        extra = "ignore"

# Create a single instance — every other file imports this object
# Usage in other files: from app.core.config import settings
settings = Settings()