from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from sqlalchemy.orm import Session

import articles  # ✅ import your articles module directly
from app import models, crud
from app.database import engine, get_db

app = FastAPI()

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="app/template")

# Include article routes
app.include_router(articles.router)

# Homepage route
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db)):
    articles_list = crud.get_articles(db)
    return templates.TemplateResponse("index.html", {"request": request, "articles": articles_list})
