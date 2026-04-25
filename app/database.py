from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
import time

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@db:5432/sftmdb")

# Retry logic — waits for PostgreSQL to be ready
def create_engine_with_retry(url, retries=5, delay=3):
    for attempt in range(retries):
        try:
            engine = create_engine(url)
            engine.connect()
            print("✅ Database connected successfully!")
            return engine
        except Exception as e:
            print(f"⏳ DB not ready, retrying... ({attempt + 1}/{retries})")
            time.sleep(delay)
    raise Exception("❌ Could not connect to database after multiple retries.")

engine = create_engine_with_retry(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()