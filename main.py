from fastapi import FastAPI

from app.routers import articles
from app.database import engine
from app.models import Base

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the News Site!"}
