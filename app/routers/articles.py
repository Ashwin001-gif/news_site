# articles.py
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from app import schemas, crud  # Change to absolute import
from app.database import get_db

router = APIRouter()

API_KEY = "supersecretjournalistkey"
api_key_header = APIKeyHeader(name="x-api-key")

@router.post("/articles", response_model=schemas.Article)
def create_article(
    article: schemas.ArticleCreate,
    x_api_key: str = Security(api_key_header),
    db: Session = Depends(get_db)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    return crud.create_article(db=db, article=article)
