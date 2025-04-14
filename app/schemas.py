from pydantic import BaseModel
from typing import List, Optional


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    article_id: int

    class Config:
        orm_mode = True


class ArticleBase(BaseModel):
    title: str
    content: str
    category: str
    likes: int
    dislikes: int


class ArticleCreate(ArticleBase):
    pass


class Article(ArticleBase):
    id: int
    comments: List[Comment] = []

    class Config:
        orm_mode = True
