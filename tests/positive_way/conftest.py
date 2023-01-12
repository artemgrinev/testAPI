import pytest
import requests

from configuration import API_KEY
from src.generators.users import create_user_info


@pytest.fixture
def generate_user_data():
    user = next(create_user_info())
    data = {
        'firstName': user.firstName,
        'lastName': user.lastName,
        'email': user.email
    }
    return data


@pytest.fixture
def generate_full_user_data():
    user = next(create_user_info())
    data = {
        'title': user.title,
        'firstName': user.firstName,
        'lastName': user.lastName,
        'gender': user.gender,
        'email': user.email,
        'dateOfBirth': user.dateOfBirth,
        'phone': user.phone,
        'picture': user.picture,
        'location': {
                    'street': user.street,
                    'city': user.city,
                    'state': user.state,
                    'country': user.country,
                    'timezone': "+7:00"
                    }
        }
    return data


def _get_user_id(user_id=""):
    return user_id


@pytest.fixture(scope="session")
def get_user_id():
    user_id = _get_user_id
    return user_id
