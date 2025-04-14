# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# Create the base object for model classes
Base = declarative_base()
# Database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Change this as per your configuration
# Create engine and session maker
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# This function will be called later to import models and initialize the database
def get_db():
    from . import models  # Import models here, after the Base object is initialized
    return SessionLocal()

Base = declarative_base()
