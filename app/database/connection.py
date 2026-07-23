import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

print("DATABASE_URL repr =", repr(DATABASE_URL))
print("Length =", len(DATABASE_URL))

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True
)
