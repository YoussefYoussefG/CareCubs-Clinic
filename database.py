import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise RuntimeError("DB_URL environment variable is not set. Please configure it in your .env file.")

# Establish database connection with connection pooling
try:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,  # Verify connections before use (important for Supabase)
    )
    print("✅ Database engine created successfully.")
except SQLAlchemyError as e:
    raise RuntimeError(f"Failed to create database engine: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency that provides a database session and ensures cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
