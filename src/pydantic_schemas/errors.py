from pydantic import BaseModel

from src.pydantic_schemas.user import UserPreview


class ErrorData(BaseModel):
    """Error when entering incorrect data in body"""
    error: str
    data: dict


class Error(BaseModel):
    error: str
