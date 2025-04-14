from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import articles
from app.database import engine, get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.responses import HTMLResponse
from fastapi.requests import Request

app = FastAPI()

# Create database tables
from app import models
models.Base.metadata.create_all(bind=engine)

# Mount static files for frontend
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up templates for frontend
templates = Jinja2Templates(directory="app/templates")

# Include article routes
app.include_router(articles.router)

# Homepage route
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db)):
    articles_list = crud.get_articles(db)
    return templates.TemplateResponse("index.html", {"request": request, "articles": articles_list})
