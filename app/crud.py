from sqlalchemy.orm import Session
from app import models, schemas

def get_articles(db: Session):
    return db.query(models.Article).all()

def search_articles(db: Session, query: str):
    return db.query(models.Article).filter(models.Article.title.contains(query)).all()

def create_article(db: Session, article: schemas.ArticleCreate):
    db_article = models.Article(**article.dict())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

def increment_like(db: Session, article_id: int):
    article = db.query(models.Article).get(article_id)
    article.likes += 1
    db.commit()
    db.refresh(article)
    return article

def increment_dislike(db: Session, article_id: int):
    article = db.query(models.Article).get(article_id)
    article.dislikes += 1
    db.commit()
    db.refresh(article)
    return article
