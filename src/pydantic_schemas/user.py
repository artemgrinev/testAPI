from pydantic import BaseModel
from src.enum.users_enum import Title


class UserPreview(BaseModel):
    id: str
    title: Title    # ("mr", "ms", "mrs", "miss", "dr", "")
    firstName: str  # (length: 2 - 50)
    lastName: str   # (length: 2 - 50)
    picture: str


class UserFull(BaseModel):
    id: str
    title: Title
    firstName: str  #(length: 2 - 50)
    lastName: str   #(length: 2 - 50)
    gender: str #("male", "female", "other", "")
    email: str
    dateOfBirth: str    #(ISODate - value: 1 / 1 / 1900 - now)
    registerDate: str
    phone: str  #(phone number - anyformat)
    picture: str    #(url)
    location: object    #(Location)
