import pytest
import requests
import json
import configuration as conf
import src.generators as generate
import src.pydantic_schemas as schema
from src.baseclasses.response import Response as res


@pytest.fixture(scope='class')
def create_user_cls_scope():
    """Creates a user, returns its id, and deletes it when it's done"""
    data = generate.User().result
    response = res(requests.post(conf.CREATE_USER_URL, data=data, headers=conf.API_KEY))
    response.assert_status_code(200).validate(schema.User)
    user_json = response.json_data
    yield user_json
    url = f"{conf.USER_URL}{user_json['id']}"
    requests.delete(url, headers=conf.API_KEY)
    print(f"delete: {user_json['id']}")


@pytest.fixture(scope='function')
def create_user_func_scope():
    """Creates a user, returns its id, and deletes it when it's done"""
    data = generate.User().result
    response = res(requests.post(conf.CREATE_USER_URL, data=data, headers=conf.API_KEY))
    response.assert_status_code(200).validate(schema.User)
    user_json = response.json_data
    yield user_json
    url = f"{conf.USER_URL}{user_json['id']}"
    requests.delete(url, headers=conf.API_KEY)
    print(f"delete: {user_json['id']}")


def _writing_data(file_name="data", data=dict):
    with open(f'tests_data/{file_name}.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)


@pytest.fixture
def writing_data():
    return _writing_data


def _reading_data(file_name="data"):
    with open(f'tests_data/{file_name}.json') as json_file:
        data = json.load(json_file)
    return data


@pytest.fixture
def reading_data():
    return _reading_data


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


