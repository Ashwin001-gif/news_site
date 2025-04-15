from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db

# Set up the template engine (Jinja2)
templates = Jinja2Templates(directory="templates")

# Initialize the router
router = APIRouter()

# Home route to display all articles in HTML (rendered by Jinja2)
@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    articles = crud.get_articles(db)  # Fetch all articles from database
    return templates.TemplateResponse("index.html", {"request": request, "articles": articles})


# Get a list of articles with pagination (skip, limit)
@router.get("/articles", response_model=List[schemas.Article])
def get_articles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    articles = crud.get_articles(db=db, skip=skip, limit=limit)
    return articles


# Get a specific article by its ID
@router.get("/articles/{article_id}", response_model=schemas.Article)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = crud.get_article_by_id(db=db, article_id=article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


# Search for articles based on a query
@router.get("/articles/search", response_model=List[schemas.Article])
def search_articles(query: str, db: Session = Depends(get_db)):
    results = crud.search_articles(db=db, search_query=query)
    return results


# Get articles by their category
@router.get("/articles/category/{category}", response_model=List[schemas.Article])
def get_articles_by_category(category: str, db: Session = Depends(get_db)):
    articles = crud.get_articles_by_category(db=db, category=category)
    return articles


# Create a new article
@router.post("/articles", response_model=schemas.Article)
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    db_article = crud.create_article(db=db, article=article)
    return db_article


# Like an article by its ID
@router.post("/articles/{article_id}/like", response_model=schemas.Article)
def like_article(article_id: int, db: Session = Depends(get_db)):
    article = crud.like_article(db=db, article_id=article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


# Add a comment to an article
@router.post("/articles/{article_id}/comments", response_model=schemas.Comment)
def add_comment(article_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    return crud.add_comment(db=db, article_id=article_id, content=comment.content)


# Update an existing article by its ID
@router.put("/articles/{article_id}", response_model=schemas.Article)
def update_article(article_id: int, article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    return crud.update_article(db=db, article_id=article_id, article=article)


# Delete an article by its ID
@router.delete("/articles/{article_id}", response_model=schemas.Article)
def delete_article(article_id: int, db: Session = Depends(get_db)):
    return crud.delete_article(db=db, article_id=article_id)
