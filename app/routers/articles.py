from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.get("/articles", response_model=List[schemas.Article])
def get_articles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    articles = crud.get_articles(db=db, skip=skip, limit=limit)
    return articles


@router.get("/articles/{article_id}", response_model=schemas.Article)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = crud.get_article_by_id(db=db, article_id=article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.get("/articles/search", response_model=List[schemas.Article])
def search_articles(query: str, db: Session = Depends(get_db)):
    results = crud.search_articles(db=db, search_query=query)
    return results


@router.get("/articles/category/{category}", response_model=List[schemas.Article])
def get_articles_by_category(category: str, db: Session = Depends(get_db)):
    articles = crud.get_articles_by_category(db=db, category=category)
    return articles


@router.post("/articles", response_model=schemas.Article)
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    db_article = crud.create_article(db=db, article=article)
    return db_article


@router.post("/articles/{article_id}/like", response_model=schemas.Article)
def like_article(article_id: int, db: Session = Depends(get_db)):
    article = crud.like_article(db=db, article_id=article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.post("/articles/{article_id}/comments", response_model=schemas.Comment)
def add_comment(article_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    return crud.add_comment(db=db, article_id=article_id, content=comment.content)


@router.put("/articles/{article_id}", response_model=schemas.Article)
def update_article(article_id: int, article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    return crud.update_article(db=db, article_id=article_id, article=article)


@router.delete("/articles/{article_id}", response_model=schemas.Article)
def delete_article(article_id: int, db: Session = Depends(get_db)):
    return crud.delete_article(db=db, article_id=article_id)
6
