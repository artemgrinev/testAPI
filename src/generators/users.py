from randomuser import RandomUser
from random import randint

from src.data.user_data import UserFull

random_user = RandomUser({'nat': 'ua'})

__title = ["mr", "ms", "mrs", "miss", "dr", ""]


def create_user_info():
    yield UserFull(
        title=__title[randint(0, len(__title) - 1)],        # ("mr", "ms", "mrs", "miss", "dr", "")
        firstName=random_user.get_first_name(),             # (length: 2 - 50)
        lastName=random_user.get_last_name(),               # (length: 2 - 50)
        gender=random_user.get_gender(),                    # ("male", "female", "other", "")
        email=random_user.get_email(),                      # (email)
        dateOfBirth=random_user.get_dob(),                  # (ISO Date - value: 1 / 1 / 1900 - now)
        phone=random_user.get_phone(strip_hyphens=True),    # (phone number - any format)
        picture=random_user.get_picture(),                  # (url)
        street=random_user.get_street(),                    # (length: 5 - 100)
        city=random_user.get_city(),                        # (length: 2 - 30)
        state=random_user.get_state(),                      # (length: 2 - 30)
        country=random_user.get_country(),                  # length: 2 - 30)
        timezone="+7:00",                                   # (Valid timezone value ex. + 7: 00, -1: 00)
    )



