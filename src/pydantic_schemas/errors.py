from pydantic import BaseModel

from src.pydantic_schemas.user import SchemaUserPreview


class SchemaErrorData(BaseModel):
    """Error when entering incorrect data in body"""
    error: str
    data: dict


class SchemaError(BaseModel):
    error: str
