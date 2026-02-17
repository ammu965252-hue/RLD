import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Get the absolute path to the backend directory
BASE_DIR = Path(__file__).resolve().parent

# Ensure the directory exists
os.makedirs(BASE_DIR, exist_ok=True)

# Absolute path to the database file
DATABASE_FILE = BASE_DIR / "riceguard.db"
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# Create engine with proper SQLite settings for persistent storage
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False  # Set to True for SQL query logging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Create all tables on startup (idempotent - only creates missing tables)
def init_db():
    """Initialize database by creating all tables if they don't exist."""
    Base.metadata.create_all(bind=engine)
    print(f"✅ Database initialized at: {DATABASE_FILE}")