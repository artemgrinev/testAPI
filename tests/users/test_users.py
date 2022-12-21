from src.baseclasses.response import Response
from src.pydantic_schemas.user import UserPreview, User, UserFull
from configuration import USER_URL, CREATE_USER_URL


class TestValidUser:
    """
    API EXAMPLE TEST
    1. Get list of registered users -GET
    2. Verify paginating - GET request(with url params)
    3. Add new user - POST request(without url params)
    4. Update newly added user details -PUT request
    5. Full update added user details -PUT request(with url params)
    5. Get user details -GET request(with url params)
    6. Delete newly added user -DELETE request
    7. Verify deleted user
    """

    def test_getting_users_list(self, get):
        Response(get(USER_URL)).assert_status_code(200).validate(UserPreview)

    def test_users_list_pagination(self, get):
        page = 1
        limit = 50
        url = f'{USER_URL}?page={page}&limit={limit}'
        res = Response(get(url))
        assert res.assert_status_code(200).validate(UserPreview).response_json['limit'] == limit

    def test_creating_new_user(self, post, generate_user_data, writing_data):
        res = Response(post(CREATE_USER_URL, generate_user_data))
        res.assert_status_code(200).validate(User)
        writing_data(res.response_json)

    def test_getting_user(self, get, riding_data):
        url = f"{USER_URL}{riding_data['id']}"
        Response(get(url)).assert_status_code(200).validate(User)

    def test_update_user(self, put, riding_data, writing_data, generate_user_data):
        new_user_date = generate_user_data
        url = f"{USER_URL}{riding_data['id']}"
        res = Response(put(url, new_user_date))
        res.assert_status_code(200).validate(User)
        assert res.response_json['id'] == riding_data['id']
        assert res.response_json != riding_data
        writing_data(res.response_json)

    def test_full_update_user(self, put, riding_data, generate_full_user_data, writing_data):
        full_user_date = generate_full_user_data
        url = f"{USER_URL}{riding_data['id']}"
        res = Response(put(url, full_user_date))
        print(res.response_json['location'])
        res.assert_status_code(200).validate(UserFull)
        writing_data(full_user_date)

    def test_getting_full_user_data(self, get, riding_data):
        url = f"{USER_URL}{riding_data['id']}"
        Response(get(url)).assert_status_code(200).validate(UserFull)

    def test_delete_added_user(self, delete, riding_data):
        url = f"{USER_URL}{riding_data['id']}"
        Response(delete(url)).assert_status_code(200)

    def test_verify_delete_user(self, get, riding_data):
        url = f"{USER_URL}{riding_data['id']}"
        res = Response(get(url))
        res.assert_status_code(404)
        assert res.response_json == {'error': 'RESOURCE_NOT_FOUND'}
