import allure
from pytest_check import check

from configuration import CREATE_USER_URL, CREATE_POST_URL, POST_URL, CREATE_COMMENT_URL
from src.baseclasses.response import Response
from src.data.errors_strings import body_not_valid, app_id_missing, app_id_not_exist, params_not_valid
from src.data.invalid_data import uppercase_body, existing_email, invalid_appi_key, invalid_user_id, invalid_post_id
from src.generators.comments import Comment
from src.generators.posts import Post
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
    user = User()

    @allure.title("NW-01: Check case-dependency dody")
    def test_case_dependency_body(self, post):
        body = uppercase_body
        response = Response(post(CREATE_USER_URL, body))
        response.assert_status_code(400).validate(SchemaErrorData)
        assert response.response_json['error'] == body_not_valid
        assert response.response_json['data']['lastName'] == 'Path `lastName` is required.'
        assert response.response_json['data']['firstName'] == 'Path `firstName` is required.'
        assert response.response_json['data']['email'] == 'Path `email` is required.'

    @allure.title("NW-02: Creating a user with an existing email")
    def test_create_user_with_exist_email(self, post):
        body = existing_email
        response = Response(post(CREATE_USER_URL, body))
        response.assert_status_code(400).validate(SchemaErrorData)
        assert response.response_json['error'] == body_not_valid
        assert response.response_json['data']['email'] == 'Email already used'

    @allure.title("NW-03: Creating a user with a missing authorization token")
    def test_create_user_missing_auth_token(self, post):
        body = self.user.result
        response = Response(post(CREATE_USER_URL, body, api_key=None))
        response.assert_status_code(403).validate(SchemaError)
        assert response.response_json['error'] == app_id_missing

    @allure.title("NW-04: Creating a user with an invalid auth token")
    def test_create_user_invalid_auth_token(self, post):
        body = self.user.result
        response = Response(post(CREATE_USER_URL, body, api_key=invalid_appi_key))
        response.assert_status_code(403).validate(SchemaError)
        assert response.response_json['error'] == app_id_not_exist

    @allure.title("NW-05: Change email for created user")
    def test_update_email(self, put):
        body = {'email': 'freddy.tester123@mail.ru'}
        response = Response(put(CREATE_USER_URL, body))
        response.assert_status_code(400).validate(SchemaError)
        assert response.response_json['error'] == params_not_valid

    @allure.title("NW-06: Change the id of the created user")
    def test_update_id(self, put):
        body = {'id': '8989cvx5x89320vsf'}
        response = Response(put(CREATE_USER_URL, body))
        response.assert_status_code(400).validate(SchemaError)
        assert response.response_json['error'] == params_not_valid


@allure.suite("Negative Way Posts")
class TestNegativeWayPosts:
    """
    NW-07: Create a post using a non-existent user id
    NW-08: Edit post using non-existent post id
    NW-09: Create a post without passing the required parameter - user id
    NW-10: Create post using existing user id with missing auth token
    NW-11: Create a post using an existing user id with an invalid auth token
    """
    post_data = Post()

    @allure.title("NW-07: Create a post using a non-existent user id")
    def test_create_post_no_exist_user(self, post):
        data = self.post_data.set_owner(invalid_user_id).result
        response = Response(post(CREATE_POST_URL, data=data))
        response.assert_status_code(400).validate(SchemaError)
        assert response.response_json['error'] == body_not_valid

    @allure.title("NW-08: Edit post using non-existent post id")
    def test_edit_post_no_exist_user(self, put, reading_data):
        post_id = reading_data(file_name='post')['id']
        url = f"{POST_URL}{post_id}"
        data = self.post_data.set_text("Being dead is not a problem").result
        response = Response(put(url, data=data))
        response.assert_status_code(400).validate(SchemaError)
        assert response.response_json['error'] == body_not_valid

    @allure.title("NW-09: Create a post without passing the required parameter - user id")
    def test_create_post_not_user_id(self, post):
        self.post_data.result.pop("owner")
        response = Response(post(CREATE_POST_URL, data=self.post_data.result))
        response.assert_status_code(400).validate(SchemaError)
        assert response.response_json['error'] == body_not_valid

    @allure.title("NW-10: Create post using existing user id with missing auth token")
    def test_create_post_with_missing_auth_token(self, post):
        data = self.post_data.result
        response = Response(post(CREATE_USER_URL, data=data, api_key=None))
        response.assert_status_code(403).validate(SchemaError)
        assert response.response_json['error'] == app_id_missing

    @allure.title("NW-11: Create a post using an existing user id with an invalid auth token")
    def test_create_post_with_invalid_auth_token(self, post):
        data = self.post_data.result
        response = Response(post(CREATE_USER_URL, data=data, api_key=invalid_appi_key))
        response.assert_status_code(403).validate(SchemaError)
        assert response.response_json['error'] == app_id_not_exist


@allure.suite("Negative Way Comment")
class TestNegativeWayComment:
    """
    NW-12: Create comment using existing user id and post id with missing auth token
    NW-13: Create a comment using an existing user id but not an existing post id
    NW-14: Create a comment using a non-existing user id but an existing post id
    """
    comment = Comment()

    @allure.title("NW-12: Create comment using existing user id and post id with missing auth token")
    def test_create_comment_with_missing_auth_token(self, post, reading_data):
        post_id = reading_data(file_name="post")["id"]
        user_id = reading_data(file_name="post")["owner"]["id"]
        data = self.comment.set_post(post_id).set_owner(user_id).result
        response = Response(post(CREATE_COMMENT_URL, data=data, api_key=None))
        response.assert_status_code(403).validate(SchemaError)
        assert response.response_json['error'] == app_id_missing

    @allure.title("NW-13: Create a comment using an existing user id but not an existing post id")
    def test_create_comment_with_not_existing_post(self, post, reading_data):
        user_id = reading_data(file_name="post")["owner"]["id"]
        data = self.comment.set_post(invalid_post_id).set_owner(user_id).result
        response = Response(post(CREATE_COMMENT_URL, data=data))
        response.assert_status_code(400).validate(SchemaError)
        assert response.response_json['error'] == body_not_valid

    @allure.title("NW-14: Create a comment using a non-existing user id but an existing post id")
    def test_create_comment_with_not_existing_user(self, post, reading_data):
        post_id = reading_data(file_name="post")["id"]
        data = self.comment.set_post(post_id).set_owner(invalid_user_id).result
        response = Response(post(CREATE_COMMENT_URL, data=data))
        response.assert_status_code(400).validate(SchemaError)
        assert response.response_json['error'] == body_not_valid


@allure.suite("Negative Way Delete")
class TestNegativeWayPosts:
    """
    NW-15: Delete non-existent comment
    NW-16: Delete non-existent post
    NW-17: Create a comment under the deleted post
    NW-18: Create post from remote user
    NW-19: Get a list of posts from a deleted user
    """
    comment = Comment()

    @allure.title("NW-15: Delete non-existent comment")
    def test_delete_not_existing_comment(self, delete):
        pass

    @allure.title("NW-16: Delete non-existent post")
    def test_delete_not_existing_post(self, delete):
        pass

    @allure.title("NW-17: Create a comment under the deleted post")
    def test_create_comment_under_delete_post(self, post):
        pass

    @allure.title("NW-18: Create post from remote user")
    def test_create_post_from_delete_user(self, post):
        pass

    @allure.title("NW-19: Get a list of posts from a deleted user")
    def test_get_list_post_from_deleted_user(self, get):
        pass
