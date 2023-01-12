from pydantic import BaseModel

from src.pydantic_schemas.user import SchemaUserPreview


class SchemaPostCreate(BaseModel):
    """Post data for create request"""
    text: str
    image: str
    likes: int
    tags: list
    owner: str


class SchemaPostPreview(BaseModel):
    """Post data as a part of list"""
    id: str
    image: str
    likes: int
    tags: list
    text: str
    publishDate: str
    owner: SchemaUserPreview


class SchemaPost(BaseModel):
    """Post data returned by id"""
    id: str
    image: str
    likes: int
    link: str
    tags: list
    text: str
    publishDate: str
    updatedDate: str
    owner: SchemaUserPreview
