from src.baseclasses.response import Response
from src.pydantic_schemas.user import SchemaUserPreview, SchemaUser, SchemaUserFull
from configuration import USER_URL, CREATE_USER_URL
from src.generators.users import User, UserFull
import allure
import datetime


@allure.title("Positive Way Users")
class TestPositiveWayUsers:
    """
    API EXAMPLE TEST
    PW-01: Getting users list
    PW-02: Pagination check
    PW-03: Creating new user
    PW-04: Find created user
    PW-05: Update created user
    PW-06: Change user information
    """

    @allure.step("PW-01: Getting users list")
    def test_getting_users_list(self, get):
        Response(get(USER_URL)).assert_status_code(200).validate(SchemaUserPreview)

    @allure.step("PW-02: Pagination check")
    def test_users_list_pagination(self, get):
        page = 1
        limit = 20
        url = f'{USER_URL}?page={page}&limit={limit}'
        res = Response(get(url))
        assert res.assert_status_code(200).validate(SchemaUserPreview).response_json['limit'] == limit

    @allure.step("PW-03: Create new user")
    def test_creating_new_user(self, post, writing_data):
        res = Response(post(CREATE_USER_URL, User().result))
        res.assert_status_code(200).validate(SchemaUser)
        writing_data(res.response_json)

    @allure.step("PW-04: Find created user")
    def test_getting_user(self, get, riding_data):
        url = f"{USER_URL}{riding_data['id']}"
        Response(get(url)).assert_status_code(200).validate(SchemaUser)
        print(Response(get(url)).response_json)

    @allure.step("PW-05: Update created user")
    def test_update_user(self, put, riding_data, writing_data):
        new_user_date = User().set_first_name("Freddy1").set_last_name("Tester1").result
        url = f"{USER_URL}{riding_data['id']}"
        res = Response(put(url, new_user_date))
        res.assert_status_code(200).validate(SchemaUser)
        assert res.response_json['id'] == riding_data['id']
        assert res.response_json != riding_data
        writing_data(res.response_json)

    @allure.step("PW-06: Change user information")
    def test_full_update_user(self, put, riding_data, writing_data):
        full_user_date = UserFull().result
        url = f"{USER_URL}{riding_data['id']}"
        res = Response(put(url, full_user_date))
        writing_data(res.response_json)
        res.assert_status_code(200).validate(SchemaUserFull)

    def test_getting_full_user_data(self, get, riding_data):
        url = f"{USER_URL}{riding_data['id']}"
        Response(get(url)).assert_status_code(200)
        assert riding_data["title"] == UserFull().result.get("title")
        assert riding_data["firstName"] == UserFull().result.get("firstName")
        assert riding_data["lastName"] == UserFull().result.get("lastName")
        assert riding_data["picture"] == UserFull().result.get("picture")
        assert riding_data["email"] == UserFull().set_email().result.get("email")
        assert riding_data["gender"] == UserFull().result.get("gender")
        assert riding_data["dateOfBirth"][:-5] == UserFull().result.get("dateOfBirth")
        assert riding_data["phone"] == UserFull().result.get("phone")
        assert riding_data["location"] == UserFull().result.get("location")

    def test_delete_added_user(self, delete, riding_data):
        url = f"{USER_URL}{riding_data['id']}"
        Response(delete(url)).assert_status_code(200)

    def test_verify_delete_user(self, get, riding_data):
        url = f"{USER_URL}{riding_data['id']}"
        res = Response(get(url))
        res.assert_status_code(404)
        assert res.response_json == {'error': 'RESOURCE_NOT_FOUND'}


