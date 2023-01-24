import pytest
import requests
import configuration as conf
import src.generators as generate
from src.baseclasses.response import Response


@pytest.fixture()
def create_user():
    data = generate.User().result
    response = requests.post(conf.CREATE_USER_URL, data=data, headers=conf.API_KEY)
    user_id = response.json()['id']
    yield user_id
    url = f"{conf.USER_URL}{user_id}"
    requests.delete(url, headers=conf.API_KEY)
    print(f"delete: {user_id}")


def test_fixture_create():
    print(conf.CREATE_USER_URL)


@pytest.mark.usefixtures('create_user')
class TestFixture:

    def test_2(self, create_user):
        print(create_user)

    def test_3(self, create_user):
        print(create_user)


user_date = (generate.UserFull().set_last_name('Nastia').set_gender('female').result,
             generate.UserFull().set_last_name('Misha').set_gender('male').result,
             generate.UserFull().set_last_name('Lesha').set_gender('male').result)


def equivalent(d1, d2):
    return ((d1['title'] == d2['title']) and
            (d1['firstName'] == d2['firstName']) and
            (d1['lastName'] == d2['lastName']) and
            (d1['picture'] == d2['picture']) and
            (d1['gender'] == d2['gender']) and
            (d1['email'] == d2['email']) and
            (d1['dateOfBirth'] == d2['dateOfBirth']))


@pytest.mark.parametrize('user', user_date)
def test_parameter(user, create_user):
    url = f"{conf.USER_URL}{create_user}"
    res = Response(requests.put(url, data=user, headers=conf.API_KEY))
    res.assert_status_code(200)
    assert equivalent(res.response_json, user)
