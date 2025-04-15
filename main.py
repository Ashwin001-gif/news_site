from fastapi import FastAPI, Request, Depends, Form, Security, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import APIKeyHeader
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session  # <-- This is the fix

from app.database import get_db
from app import crud, models, schemas
from app.routers import articles

import os

# Database setup
DATABASE_URL = "sqlite:///./test.db"  # Replace with actual DB for production

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI app instance
app = FastAPI()

# Create tables on startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Serve static files (CSS/JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates directory
templates = Jinja2Templates(directory="templates")

# API key config
API_KEY = "supersecretjournalistkey"
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

# Include routers
app.include_router(articles.router)

# Homepage
@app.get("/", response_class=HTMLResponse)
def read_home(request: Request, db: Session = Depends(get_db)):
    articles = crud.get_articles(db)
    return templates.TemplateResponse("index.html", {"request": request, "articles": articles})

# Search
@app.get("/articles/search", response_class=HTMLResponse)
def search_articles(request: Request, query: str, db: Session = Depends(get_db)):
    articles = crud.search_articles(db, query)
    return templates.TemplateResponse("index.html", {"request": request, "articles": articles})

# Create article
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

# Like
@app.post("/articles/{article_id}/like")
def like_article(article_id: int, db: Session = Depends(get_db)):
    article = crud.increment_like(db, article_id)
    return {"likes": article.likes, "dislikes": article.dislikes}

# Dislike
@app.post("/articles/{article_id}/dislike")
def dislike_article(article_id: int, db: Session = Depends(get_db)):
    article = crud.increment_dislike(db, article_id)
    return {"likes": article.likes, "dislikes": article.dislikes}
