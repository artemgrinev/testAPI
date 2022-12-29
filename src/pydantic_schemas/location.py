from pydantic import BaseModel


class Locations(BaseModel):
    """Using only as a part of full user data"""
    street: str     # (length: 5 - 100)
    city: str       # (length: 2 - 30)
    state: str      # (length: 2 - 30)
    country: str    # (length: 2 - 30)
    timezone: str   # (Valid timezone value ex. + 7: 00, -1: 00)
    