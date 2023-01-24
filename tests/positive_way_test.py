import allure
from pytest_check import check
from src.baseclasses.response import Response
from src.generators.comments import Comment
from src.pydantic_schemas.comments import SchemaComment
from src.pydantic_schemas.posts import SchemaPostPreview, SchemaPost
from src.pydantic_schemas.user import SchemaUserPreview, SchemaUser, SchemaUserFull
from configuration import USER_URL, CREATE_USER_URL, POST_URL, CREATE_POST_URL, COMMENT_URL, CREATE_COMMENT_URL
from src.generators.users import User, UserFull
from src.generators.posts import Post


@allure.suite("Positive Way Users")
class TestPositiveWayUsers:
    """
    PW-01: Getting positive_way list
    PW-02: Pagination check
    PW-03: Creating new user
    PW-04: Find created user
    PW-05: Update created user
    PW-06: Change user information
    PW-07: Change user information
    """
    user = User()

    @allure.title("PW-01: Getting positive_way list")
    def test_getting_users_list(self, get):
        Response(get(USER_URL)).assert_status_code(200).validate(SchemaUserPreview)

    @allure.title("PW-02: Pagination check")
    def test_users_list_pagination(self, get):
        page = 1
        limit = 20
        url = f'{USER_URL}?page={page}&limit={limit}'
        response = Response(get(url))
        response.assert_status_code(200).validate(SchemaUserPreview)
        assert response.response_json['limit'] == limit

    @allure.title("PW-03: Create new user")
    def test_creating_new_user(self, post, writing_data):
        response = Response(post(CREATE_USER_URL, self.user.result))
        writing_data(file_name="user", data=response.response_json)
        response.assert_status_code(200).validate(SchemaUser)

    @allure.title("PW-04: Find created user")
    def test_getting_user(self, get, reading_data):
        user_id = reading_data(file_name="user")['id']
        url = f"{USER_URL}{user_id}"
        Response(get(url)).assert_status_code(200).validate(SchemaUser)
        print(Response(get(url)).response_json)

    @allure.title("PW-05: Update created user")
    def test_update_user(self, put, reading_data, writing_data):
        user_id = reading_data(file_name="user")['id']
        data = self.user_data.set_first_name("Freddy1").set_last_name("Tester1").result
        url = f"{USER_URL}{user_id}"
        response = Response(put(url, data=data))
        response.assert_status_code(200).validate(SchemaUser)
        assert response.response_json['id'] == user_id
        assert response.response_json != reading_data(file_name="user")
        writing_data(file_name="user", data=response.response_json)

    @allure.title("PW-06: Full update created user")
    def test_full_update_user(self, put, reading_data, writing_data):
        data = self.user_data.result
        user_id = reading_data(file_name="user")['id']
        url = f"{USER_URL}{user_id}"
        response = Response(put(url, data=data))
        writing_data(file_name="user", data=response.response_json)
        response.assert_status_code(200).validate(SchemaUserFull)

    @allure.title("PW-07: Change user information")
    def test_getting_full_user_data(self, get, reading_data):
        json_data = reading_data(file_name="user")
        url = f"{USER_URL}{json_data['id']}"
        Response(get(url)).assert_status_code(200)
        assert json_data["title"] == UserFull().result.get("title")
        assert json_data["firstName"] == UserFull().result.get("firstName")
        assert json_data["lastName"] == UserFull().result.get("lastName")
        assert json_data["picture"] == UserFull().result.get("picture")
        assert json_data["email"] == UserFull().set_email().result.get("email")
        assert json_data["gender"] == UserFull().result.get("gender")
        assert json_data["dateOfBirth"][:-5] == UserFull().result.get("dateOfBirth")
        assert json_data["phone"] == UserFull().result.get("phone")
        assert json_data["location"] == UserFull().result.get("location")


@allure.suite("Positive Way Posts")
class TestPositiveWayPosts:
    """
    PW-08: Getting post list
    PW-09: Pagination check
    PW-10: Create new post
    PW-11: Find created post by Post id
    PW-12: Get a list of created posts by User id
    PW-13: Edit the information of a created post
    """
    post_data = Post()

    @allure.title("PW-08: Getting post list")
    def test_getting_post_list(self, get):
        Response(get(POST_URL)).assert_status_code(200).validate(SchemaPostPreview)

    @allure.title("PW-09: Pagination check")
    def test_post_list_pagination(self, get):
        page = 1
        limit = 20
        url = f'{POST_URL}?page={page}&limit={limit}'
        response = Response(get(url))
        response.assert_status_code(200).validate(SchemaPostPreview)
        assert response.response_json['limit'] == limit

    @allure.title("PW-10: Create new post")
    def test_create_post(self, post, writing_data, reading_data):
        owner = reading_data(file_name="user")['id']
        body = self.post_data.set_owner(owner).result
        response = Response(post(CREATE_POST_URL, body))
        response.assert_status_code(200).validate(SchemaPost)
        writing_data(file_name="post", data=response.response_json)

    @allure.title("PW-11: Find created post by Post id")
    def test_find_post_by_id(self, get, reading_data):
        post_json = reading_data(file_name="post")
        url = f"{POST_URL}{post_json['id']}"
        response = Response(get(url))
        response.assert_status_code(200).validate(SchemaPost)
        for key, value in post_json.items():
            with check:
                assert post_json[key] == response.response_json[key]

    @allure.title("PW-12: Get a list of created posts by User id")
    def test_find_post_list_by_userid(self, get, reading_data):
        user_id = reading_data(file_name="user")["id"]
        url = f"{USER_URL}{user_id}/post"
        response = Response(get(url))
        response.assert_status_code(200).validate(SchemaPostPreview)
        assert response.response_json["total"] == 1

    @allure.title("PW-13: Edit the information of a created post")
    def test_update_post(self, put, reading_data, writing_data):
        new_post_data = self.post_data.set_text("Being dead is not a problem.").\
                               set_tags(["philosophy"]).set_likes(150).result
        url = f"{POST_URL}{reading_data(file_name='post')['id']}"
        response = Response(put(url, data=new_post_data))
        response.assert_status_code(200).validate(SchemaPost)
        assert response.response_json['id'] == reading_data(file_name='post')['id']
        assert response.response_json != reading_data(file_name='post')
        writing_data(file_name="post", data=response.response_json)


@allure.suite("Positive Way Comments")
class TestPositiveWayComment:
    """
    PW-14: Getting comments list
    PW-15: Pagination check
    PW-16: Create a new comment under the created post
    PW-17: Find created comment by Post id
    PW-18: Leave a comment under the post of other positive_way
    PW-19: Get a list of created comments by User id
    """
    comment = Comment()

    @allure.title("PW-14: Getting comments list")
    def test_getting_comment_list(self, get):
        Response(get(COMMENT_URL)).assert_status_code(200).validate(SchemaComment)

    @allure.title("PW-15: Pagination check")
    def test_comment_list_pagination(self, get):
        page = 1
        limit = 20
        url = f'{COMMENT_URL}?page={page}&limit={limit}'
        response = Response(get(url))
        response.assert_status_code(200).validate(SchemaComment)
        assert response.response_json['limit'] == limit

    @allure.title("PW-16: Create a new comment under the created post")
    def test_create_comment(self, post, writing_data, reading_data):
        owner = reading_data(file_name="user")["id"]
        post_id = reading_data(file_name="post")["id"]
        body = self.comment.set_owner(owner).set_post(post_id).result
        response = Response(post(CREATE_COMMENT_URL, body))
        response.assert_status_code(200).validate(SchemaComment)
        writing_data(file_name="comment", data=response.response_json)

    @allure.title("PW-17: Find created comment by Post id")
    def test_find_comment_by_post_id(self, get, reading_data):
        post_id = reading_data(file_name="post")["id"]
        comment = reading_data(file_name="comment")
        url = f"{POST_URL}{post_id}/comment"
        response = Response(get(url))
        response.assert_status_code(200).validate(SchemaComment)
        for key in comment.keys():
            with check:
                assert comment[key] == response.response_json['data'][0][key]

    @allure.title("PW-18: Leave a comment under the post of other positive_way")
    def test_create_comment_other_user(self, get, post, add_data, reading_data):
        owner = reading_data(file_name="user")["id"]
        post_id = Response(get(POST_URL)).response_json["data"][0]["id"]
        body = self.comment.set_owner(owner).set_post(post_id).result
        response = Response(post(CREATE_COMMENT_URL, body))
        response.assert_status_code(200).validate(SchemaComment)
        add_data(file_name="comment", add_data=response.response_json)

    @allure.title("PW-19: Get a list of created comments by User id")
    def test_find_comment_by_user_id(self, get, reading_data):
        user_id = reading_data(file_name="user")["id"]
        url = f"{USER_URL}{user_id}/comment"
        response = Response(get(url))
        response.assert_status_code(200).validate(SchemaComment)
        assert len(response.response_json['data']) == 2


@allure.suite("Delete Test Data")
class TestDeleteData:
    """
    PW-20: Delete created comments
    PW-21: Check deleted comments
    PW-22: Delete created post
    PW-23: Check deleted post
    PW-24: Delete created user
    PW-25: Check deleted user
    """

    @allure.title("PW-20: Delete created comments")
    def test_delete_added_comment(self, get, delete, reading_data):
        user_id = reading_data(file_name="user")["id"]
        url = f"{USER_URL}{user_id}/comment"
        json_data = Response(get(url)).response_json["data"]
        for data in json_data:
            url = f"{COMMENT_URL}{data['id']}"
            Response(delete(url)).assert_status_code(200)
            print(f"comment {data['id']} deleted")

    @allure.title("PW-21: Check deleted comments")
    def test_verify_delete_comment(self, get, reading_data):
        user_id = reading_data(file_name="user")["id"]
        url = f"{USER_URL}{user_id}/comment"
        response = Response(get(url))
        response.assert_status_code(200)
        assert response.response_json["total"] == 0

    @allure.title("PW-22: Delete created post")
    def test_delete_added_post(self, delete, reading_data):
        post_id = reading_data(file_name="post")["id"]
        url = f"{POST_URL}{post_id}"
        Response(delete(url)).assert_status_code(200)

    @allure.title("PW-23: Check deleted post")
    def test_verify_delete_post(self, get, reading_data):
        post_id = reading_data(file_name="post")["id"]
        url = f"{USER_URL}{post_id}"
        response = Response(get(url))
        response.assert_status_code(404)
        assert response.response_json == {'error': 'RESOURCE_NOT_FOUND'}

    @allure.title("PW-24: Delete created user")
    def test_delete_added_user(self, delete, reading_data):
        user_id = reading_data(file_name="user")["id"]
        url = f"{USER_URL}{user_id}"
        Response(delete(url)).assert_status_code(200)

    @allure.title("PW-25: Check deleted user")
    def test_verify_delete_user(self, get, reading_data):
        user_id = reading_data(file_name="user")["id"]
        url = f"{USER_URL}{user_id}"
        response = Response(get(url))
        response.assert_status_code(404)
        assert response.response_json == {'error': 'RESOURCE_NOT_FOUND'}
