import pytest
import requests

from configuration import API_KEY
from src.generators.users import create_user_info


@pytest.fixture
def generate_user():
    user = next(create_user_info())
    data = {
        'firstName': user.firstName,
        'lastName': user.lastName,
        'email': user.email
    }
    return data


def _get_user_id(user_id=""):
    return user_id


@pytest.fixture(scope="session")
def get_user_id():
    user_id = _get_user_id
    return user_id
