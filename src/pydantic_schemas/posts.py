from pydantic import BaseModel


class PostCreate(BaseModel):
    """Post data for create request"""
    text: str
    images: str
    likes: int
    tags: list
    owner: str


class PostPreview(BaseModel):
    """Post data as a part of list"""
    id: str
    text: str
    images: str
    likes: int
    tags: list
    publishDate: str
    owner: str


class Post(BaseModel):
    """Post data returned by id"""
    id: str
    text: str
    images: str
    likes: int
    link: str
    tags: list
    publishDate: str
    owner: str
