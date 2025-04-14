from sqlalchemy import Column, Integer, String
from .db_connection import Base  # Import Base here after db_connection.py is set up

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)

