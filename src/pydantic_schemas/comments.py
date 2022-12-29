from pydantic import BaseModel


class CommentCreate(BaseModel):
    """Comment data to create new item."""
    message: str
    owner: str
    post: str


class Comment(BaseModel):
    id: str
    message: str
    owner: str
    post: str
    publishDate: str
