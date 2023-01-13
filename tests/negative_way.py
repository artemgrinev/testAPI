import allure
from pytest_check import check

from configuration import CREATE_USER_URL
from src.baseclasses.response import Response
from src.data.errors_body import body_not_valid, app_id_missing, app_id_not_exist, params_not_valid
from src.data.invalid_data import uppercase_body, existing_email, invalid_appi_key
from src.generators.users import User
from src.pydantic_schemas.errors import SchemaErrorData, SchemaError


@allure.suite("Negative Way Users")
class TestNegativeWayUsers:
    """
    NW-01: Check case-dependency dody
    NW-02: Creating a user with an existing email
    NW-03: Creating a user with a missing authorization token
    NW-04: Creating a user with an invalid auth token
    NW-05: Change email for created user
    NW-06: Change the id of the created user
    """

    @allure.title("NW-01: Check case-dependency dody")
    def test_case_dependency_body(self, post):
        body = uppercase_body
        r = Response(post(CREATE_USER_URL, body))
        r.assert_status_code(400).validate(SchemaErrorData)
        assert r.response_json['error'] == body_not_valid
        assert r.response_json['data']['lastName'] == 'Path `lastName` is required.'
        assert r.response_json['data']['firstName'] == 'Path `firstName` is required.'
        assert r.response_json['data']['email'] == 'Path `email` is required.'

    @allure.title("NW-02: Creating a user with an existing email")
    def test_create_user_with_exist_email(self, post):
        body = existing_email
        r = Response(post(CREATE_USER_URL, body))
        r.assert_status_code(400).validate(SchemaErrorData)
        assert r.response_json['error'] == body_not_valid
        assert r.response_json['data']['email'] == 'Email already used'

    @allure.title("NW-03: Creating a user with a missing authorization token")
    def test_create_user_missing_auth_token(self, post):
        body = User().result
        r = Response(post(CREATE_USER_URL, body, api_key=None))
        r.assert_status_code(403).validate(SchemaError)
        assert r.response_json['error'] == app_id_missing

    @allure.title("NW-04: Creating a user with an invalid auth token")
    def test_create_user_invalid_auth_token(self, post):
        body = User().result
        r = Response(post(CREATE_USER_URL, body, api_key=invalid_appi_key))
        r.assert_status_code(403).validate(SchemaError)
        assert r.response_json['error'] == app_id_not_exist

    @allure.title("NW-05: Change email for created user")
    def test_update_email(self, put):
        body = {'email': 'freddy.tester123@mail.ru'}
        r = Response(put(CREATE_USER_URL, body))
        r.assert_status_code(400).validate(SchemaError)
        assert r.response_json['error'] == params_not_valid

    @allure.title("NW-06: Change the id of the created user")
    def test_update_id(self, put):
        body = {'id': '8989cvx5x89320vsf'}
        r = Response(put(CREATE_USER_URL, body))
        r.assert_status_code(400).validate(SchemaError)
        assert r.response_json['error'] == params_not_valid
