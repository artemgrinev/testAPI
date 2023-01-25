from pydantic import BaseModel

from src.pydantic_schemas.user import UserPreview


class CommentCreate(BaseModel):
    """Comment data to create new item."""
    message: str
    owner: str
    post: str


class Comment(BaseModel):
    id: str
    message: str
    owner: UserPreview
    post: str
    publishDate: str
