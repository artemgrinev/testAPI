from pydantic import BaseModel
from src.enum.users_enum import Title
from src.pydantic_schemas.location import Locations


class SchemaUser(BaseModel):
    id: str
    firstName: str
    lastName: str
    email: str
    registerDate: str
    updatedDate: str


class SchemaUserPreview(BaseModel):
    """User as a part of list or other data like post/comment"""
    id: str
    title: Title    # ("mr", "ms", "mrs", "miss", "dr", "")
    firstName: str  # (length: 2 - 50)
    lastName: str   # (length: 2 - 50)
    picture: str


class SchemaUserFull(BaseModel):
    """Full user data returned by id"""
    id: str
    title: Title
    firstName: str          # (length: 2 - 50)
    lastName: str           # (length: 2 - 50)
    picture: str            # (url)
    gender: str             # ("male", "female", "other", "")
    email: str
    dateOfBirth: str        # (ISODate - value: 1 / 1 / 1900 - now)
    phone: str              # (phone number - any format)
    location: Locations     # (Location)
    registerDate: str
    updatedDate: str


