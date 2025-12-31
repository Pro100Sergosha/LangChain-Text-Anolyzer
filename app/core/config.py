import os

from dotenv import load_dotenv

load_dotenv()


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env")

DB_NAME = os.getenv("DB_NAME") or "database"

DB_URL = os.getenv("DB_URL") or f"sqlite:///{DB_NAME}.db"
