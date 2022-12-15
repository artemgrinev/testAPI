from src.baseclasses.response import Response
from src.pydantic_schemas.user import UserPreview


def test_getting_users_list(user_list):
    Response(user_list).assert_status_code(200).validate(UserPreview)

def test_getting_user_info(user_info):

