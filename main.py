from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the News Site!"}

from app.routers import articles
from app.database import engine
from app.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="News Website API")

app.include_router(articles.router)
