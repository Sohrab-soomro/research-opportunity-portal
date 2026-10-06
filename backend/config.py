"""
Configuration values are read from environment variables (the .env file).
No passwords are written in the source code.
"""
import os
from dotenv import load_dotenv

# Load variables from backend/.env (if the file exists)
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "research_portal"),
}

FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
