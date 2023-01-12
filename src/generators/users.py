from datetime import datetime

from randomuser import RandomUser
from random import randint

from src.baseclasses.builder import BuilderBaseClass
from src.data.user_data import UserFullData

random_user = RandomUser({'nat': 'us'})

__title = ["mr", "ms", "mrs", "miss", "dr", ""]


class UserFull(BuilderBaseClass):

    def __init__(self):
        super().__init__()
        self.reset()

    def set_tittle(self, tittle='mr'):
        self.result['title'] = tittle
        return self

    def set_first_name(self, first_name='Freddy'):
        self.result['firstName'] = first_name
        return self

    def set_last_name(self, last_name='Tester'):
        self.result['lastName'] = last_name
        return self

    def set_gender(self, gender='male'):
        self.result['gender'] = gender
        return self

    def set_email(self, email='freddy.tester@yandex.com'):
        self.result['email'] = email
        return self

    def set_date_of_birth(self, year=1968, month=9, day=1):
        self.result['dateOfBirth'] = datetime(year, month, day).isoformat()
        return self

    def set_phone(self, phone='+99-354-85-98'):
        self.result['phone'] = phone
        return self

    def set_avatar(self, avatar="https://oir.mobi/uploads/posts/2020-01/thumbs/1578314596_2-5.jpg"):
        self.result['picture'] = avatar
        return self

    def set_location(self, reset=None):
        if reset is None:
            location = {
                'street': 'Genesee Ave.',
                'city': 'Los Angeles',
                'state': 'CA',
                'country': 'USA',
                'timezone': '-7'
            }
        else:
            location = reset
        self.result['location'] = location
        return self

    def reset(self):
        self.set_tittle()
        self.set_first_name()
        self.set_last_name()
        self.set_gender()
        self.set_date_of_birth()
        self.set_phone()
        self.set_avatar()
        self.set_location()
        return self


class User(UserFull):
    """Create User firstName, lastName, email are required"""
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.set_first_name()
        self.set_last_name()
        self.set_email()


def create_user_info():
    yield UserFullData(
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

#
# user = UserFull().set_email()
# print(user.result)
