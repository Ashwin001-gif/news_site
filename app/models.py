from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    category = Column(String)
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)

    comments = relationship("Comment", back_populates="article")


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    article_id = Column(Integer, ForeignKey("articles.id"))
    article = relationship("Article", back_populates="comments")
