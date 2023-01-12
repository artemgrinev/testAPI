from pydantic import BaseModel

from src.pydantic_schemas.user import SchemaUserPreview


class SchemaCommentCreate(BaseModel):
    """Comment data to create new item."""
    message: str
    owner: str
    post: str


class SchemaComment(BaseModel):
    id: str
    message: str
    owner: SchemaUserPreview
    post: str
    publishDate: str
