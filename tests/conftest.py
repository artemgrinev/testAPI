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


def _delete(url):
    response = requests.delete(url, headers=API_KEY)
    return response


@pytest.fixture
def delete():
    return _delete


def _writing_data(file_name="data", data=dict):
    with open(f'tests_data/{file_name}.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)


@pytest.fixture
def writing_data():
    return _writing_data


def _riding_data(file_name="data"):
    with open(f'tests_data/{file_name}.json') as json_file:
        data = json.load(json_file)
    return data


@pytest.fixture
def riding_data():
    return _riding_data


def _add_data(file_name="data", add_data=dict):
    with open(f'tests_data/{file_name}.json', "r") as json_file:
        file_data = json.load(json_file)
    if isinstance(file_data, list):
        file_data.append(add_data)
    else:
        file_data = [file_data, add_data]
    with open(f"tests_data/{file_name}.json", "w") as file:
        json.dump(file_data, file, indent=2, ensure_ascii=False)


@pytest.fixture
def add_data():
    return _add_data


