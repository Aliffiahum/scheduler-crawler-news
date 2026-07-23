import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# =====================================================
# Load Environment Variables
# =====================================================

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL tidak ditemukan")

DATABASE_URL = DATABASE_URL.strip()

# =====================================================
# Database Engine
# =====================================================

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)

# =====================================================
# Session Factory
# =====================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

# =====================================================
# Get DB
# =====================================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()