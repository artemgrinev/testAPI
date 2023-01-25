import pytest
import requests
import configuration as conf
import src.generators as generate
import src.pydantic_schemas as schema
from src.baseclasses.response import Response as res
import src.baseclasses.equivalent as eq


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


def test_fixture_create():
    print(conf.CREATE_USER_URL)


@pytest.mark.usefixtures('create_user_cls_scope')
class TestFixture:

    def test_1(self, create_user_cls_scope):
        print('test1', create_user_cls_scope)

    def test_2(self, create_user_cls_scope):
        print('test2', create_user_cls_scope)


user_data = (generate.UserFull().set_last_name('Nastia').set_gender('female').result,
             generate.UserFull().set_first_name('Potapova').set_tittle('ms').result,
             generate.UserFull().set_date_of_birth(year=2003, month=3, day=31).set_phone('+79312845578').result)


@pytest.mark.parametrize('user', user_data)
def test_parameter(user, create_user_func_scope):
    url = f"{conf.USER_URL}{create_user_func_scope['id']}"
    response = res(requests.put(url, data=user, headers=conf.API_KEY))
    response.assert_status_code(200).validate(schema.User)
    assert eq.equivalent('user', [user, response.json_data])

