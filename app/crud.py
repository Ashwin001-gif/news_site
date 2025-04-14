from sqlalchemy.orm import Session
from app import models, schemas


def get_articles(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Article).offset(skip).limit(limit).all()


def get_article_by_id(db: Session, article_id: int):
    return db.query(models.Article).filter(models.Article.id == article_id).first()




def create_article(db: Session, article: schemas.ArticleCreate):
    db_article = models.Article(**article.dict())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article



def search_articles(db: Session, search_query: str):
    return db.query(models.Article).filter(
        models.Article.title.ilike(f"%{search_query}%") |
        models.Article.content.ilike(f"%{search_query}%")
    ).all()


def get_articles_by_category(db: Session, category: str):
    return db.query(models.Article).filter(models.Article.category == category).all()


def add_comment(db: Session, article_id: int, content: str):
    db_comment = models.Comment(article_id=article_id, content=content)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def like_article(db: Session, article_id: int):
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if article:
        article.likes += 1
        db.commit()
        db.refresh(article)
    return article


def update_article(db: Session, article_id: int, article: models.Article):
    db_article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if db_article:
        db_article.title = article.title
        db_article.content = article.content
        db_article.category = article.category
        db.commit()
        db.refresh(db_article)
    return db_article


def delete_article(db: Session, article_id: int):
    db_article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if db_article:
        db.delete(db_article)
        db.commit()
    return db_article
