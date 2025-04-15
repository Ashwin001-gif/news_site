from fastapi import FastAPI, Request, Depends, Form, Security, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import APIKeyHeader
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.database import get_db
from app import crud, models, schemas
from app.routers import articles

import os

# Create database engine and session
DATABASE_URL = "sqlite:///./test.db"  # Update with your actual database URL on Render or local file path
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Ensure tables are created on app startup
app = FastAPI()

@app.on_event("startup")
def on_startup():
    # Create all tables
    Base.metadata.create_all(bind=engine)

# Mount static directory for CSS/JS if needed
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up template directory
templates = Jinja2Templates(directory="templates")

# API Key for secure article creation
API_KEY = "supersecretjournalistkey"
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

# Include any API routers
app.include_router(articles.router)

# Homepage: Display all articles
@app.get("/", response_class=HTMLResponse)
def read_home(request: Request, db: Session = Depends(get_db)):
    articles = crud.get_articles(db)
    return templates.TemplateResponse("index.html", {"request": request, "articles": articles})

# Search route
@app.get("/articles/search", response_class=HTMLResponse)
def search_articles(request: Request, query: str, db: Session = Depends(get_db)):
    articles = crud.search_articles(db, query)
    return templates.TemplateResponse("index.html", {"request": request, "articles": articles})

# Create article (form POST)
@app.post("/articles", response_class=HTMLResponse)
def create_article(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    category: str = Form(...),
    db: Session = Depends(get_db),
    x_api_key: str = Security(api_key_header)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    article_data = schemas.ArticleCreate(title=title, content=content, category=category)
    crud.create_article(db=db, article=article_data)
    return RedirectResponse("/", status_code=303)

# Like article
@app.post("/articles/{article_id}/like")
def like_article(article_id: int, db: Session = Depends(get_db)):
    article = crud.increment_like(db, article_id)
    return {"likes": article.likes, "dislikes": article.dislikes}

# Dislike article
@app.post("/articles/{article_id}/dislike")
def dislike_article(article_id: int, db: Session = Depends(get_db)):
    article = crud.increment_dislike(db, article_id)
    return {"likes": article.likes, "dislikes": article.dislikes}
