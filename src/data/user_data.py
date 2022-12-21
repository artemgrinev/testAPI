from dataclasses import dataclass


@dataclass
class UserPreview:
    title: str = None       # ("mr", "ms", "mrs", "miss", "dr", "")
    firstName: str = None   # (length: 2 - 50)
    lastName: str = None    # (length: 2 - 50)
    picture: str = None     # url


@dataclass
class UserFull:
    title: str = None           # ("mr", "ms", "mrs", "miss", "dr", "")
    firstName: str = None       # (length: 2 - 50)
    lastName: str = None        # (length: 2 - 50)
    gender: str = None          # ("male", "female", "other", "")
    email: str = None           # (email)
    dateOfBirth: str = None     # (ISO Date - value: 1 / 1 / 1900 - now)
    phone: str = None           # (phone number - any format)
    picture: str = None         # (url)
    street: str = None          # (length: 5 - 100)
    city: str = None            # (length: 2 - 30)
    state: str = None           # (length: 2 - 30)
    country: str = None         # (length: 2 - 30)
    timezone: str = None        # (Valid timezone value ex. + 7: 00, -1: 00)


@dataclass
class Location:
    street: str = None      # (length: 5 - 100)
    city: str = None        # (length: 2 - 30)
    state: str = None       # (length: 2 - 30)
    country: str = None     # length: 2 - 30)
    timezone: str = None    # Valid timezone (value ex. + 7: 00, -1: 00)
