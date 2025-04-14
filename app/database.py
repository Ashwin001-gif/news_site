from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from .models import Base

# Database URL (replace with your actual database URL)
SQLALCHEMY_DATABASE_URL = "sqlite:///./news.db"  # Example, use PostgreSQL or another database in production

# Create engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})  # Use check_same_thread=False for SQLite
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for models
Base = declarative_base()

# Dependency to get the DB session
def get_db(db: Session = Depends(SessionLocal)):
    try:
        yield db
    finally:
        db.close()

# app/database.py
print("Database module loaded!")  # Add this to verify if the module is loaded
