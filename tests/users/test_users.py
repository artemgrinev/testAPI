from src.baseclasses.response import Response
from src.pydantic_schemas.user import UserPreview, User
from configuration import USER_URL, CREATE_USER_URL


class TestUser:
    """
    API EXAMPLE TEST
    1. Get list of registered users -GET
    2. Verify paginating - GET request(with url_params)
    3. Add new user - POST request(without url_params)
    4. Update newly added user details -PUT request
    5. Get user details -GET request(with url_params)
    6. Register car - POST request(with url_params)
    8. Verify registered cars count
    9. Delete newly added user -DELETE request
    """

    def test_getting_users_list(self, get):
        Response(get(USER_URL)).assert_status_code(200).validate(UserPreview)

    def test_users_list_pagination(self, get):
        page = 1
        limit = 50
        pagination_endpoint = f'?page={page}&limit={limit}'
        res = Response(get(USER_URL+pagination_endpoint))
        assert res.assert_status_code(200).validate(UserPreview).response_json['limit'] == limit

    def test_creating_new_user(self, post, generate_user, writing_data):
        res = Response(post(CREATE_USER_URL, generate_user))
        res.assert_status_code(200).validate(User)
        writing_data(res.response_json)

    def test_getting_user(self, get, riding_data):
        url = f"{USER_URL}{riding_data['id']}"
        Response(get(url)).assert_status_code(200).validate(User)

    def test_update_user(self, put, riding_data, writing_data, generate_user):
        new_lastname = generate_user
        url = f"{USER_URL}{riding_data['id']}"
        res = Response(put(url, new_lastname))
        res.assert_status_code(200).validate(User)
        assert res.response_json['id'] == riding_data['id']
        assert res.response_json != riding_data
        writing_data(res.response_json)



