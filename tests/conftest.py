import pytest
import requests
import json

from configuration import API_KEY


def _get(url: str, data=None):
    if data is not None:
        response = requests.get(url, data=data, headers=API_KEY)
    else:
        response = requests.get(url, headers=API_KEY)
    return response


@pytest.fixture
def get():
    return _get


def _post(url, data):
    response = requests.post(url, data=data, headers=API_KEY)
    return response


@pytest.fixture
def post():
    return _post


def _put(url, data):
    response = requests.put(url, data=data, headers=API_KEY)
    return response


@pytest.fixture
def put():
    return _put


def _writing_data(data: str):
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)


@pytest.fixture
def writing_data():
    return _writing_data


@pytest.fixture
def riding_data():
    with open('data.txt') as json_file:
        data = json.load(json_file)
    return data
