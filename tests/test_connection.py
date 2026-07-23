from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(
    os.getenv("DATABASE_URL"),
    pool_pre_ping=True
)

with engine.connect() as conn:
    result = conn.execute(text("SELECT NOW();"))
    print(result.fetchone())