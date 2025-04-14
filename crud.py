from sqlalchemy.orm import Session
from app import models, schemas

def create_article(db: Session, article: schemas.ArticleCreate):
    db_article = models.Article(title=article.title, content=article.content, author=article.author)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

def get_articles(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Article).offset(skip).limit(limit).all()

def get_article_by_id(db: Session, article_id: int):
    return db.query(models.Article).filter(models.Article.id == article_id).first()
