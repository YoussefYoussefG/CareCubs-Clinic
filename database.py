import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL")

if not SQLALCHEMY_DATABASE_URL:
    print("⚠️ DB_URL not found in .env file. Falling back to local SQLite database for testing.")
    SQLALCHEMY_DATABASE_URL = "sqlite:///./carecubs_test.db"
    
    try:
        engine = create_engine(
            SQLALCHEMY_DATABASE_URL,
            connect_args={"check_same_thread": False} # Required for SQLite in FastAPI
        )
        print("✅ Local SQLite database engine created successfully.")
    except SQLAlchemyError as e:
        raise RuntimeError(f"Failed to create SQLite database engine: {e}")
else:
    try:
        # Establish Postgres database connection with connection pooling
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
