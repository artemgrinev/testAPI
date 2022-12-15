import pytest
import requests

from configuration import USERS_LIST_URL, API_KEY, CREATE_USER_URL


@pytest.fixture
def user_list():
    response = requests.get(USERS_LIST_URL, headers=API_KEY)
    return response


@pytest.fixture
def create_user():
    response = requests.get(CREATE_USER_URL, headers=API_KEY)
    return response
