import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

print("=" * 50)
print("DATABASE_URL repr:", repr(DATABASE_URL))
print("Length:", len(DATABASE_URL) if DATABASE_URL else None)

if DATABASE_URL:
    print("Characters:")
    for i, c in enumerate(DATABASE_URL):
        print(i, ord(c), repr(c))

DATABASE_URL = DATABASE_URL.strip()

print("=" * 50)
print(make_url(DATABASE_URL))
print("=" * 50)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)