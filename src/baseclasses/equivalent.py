
def user_equivalent(d1, d2):
    return ((d1['firstName'] == d2['firstName']) and
            (d1['lastName'] == d2['lastName']) and
            (d1['email'] == d2['email']))


def user_full_equivalent(d1, d2):
    return ((d1['firstName'] == d2['firstName']) and
            (d1['lastName'] == d2['lastName']) and
            (d1['picture'] == d2['picture']) and
            (d1['gender'] == d2['gender']) and
            (d1['email'] == d2['email']) and
            (d1['dateOfBirth'] == d2['dateOfBirth']))


def post_equivalent(d1, d2):
    return ((d1['text'] == d2['text']) and
            (d1['image'] == d2['image']) and
            (d1['likes'] == d2['likes']) and
            (d1['picture'] == d2['picture']) and
            (d1['link'] == d2['link']) and
            (d1['tags'] == d2['tags']) and
            (d1['owner'] == d2['owner']))


def comment_equivalent(d1, d2):
    return ((d1['message'] == d2['message']) and
            (d1['owner'] == d2['owner']) and
            (d1['post'] == d2['post']))


def equivalent(obj: str, values: list):
    """
    :param obj: user, post, comment
    :param values: list with dictionaries containing data to check
    :return: bool
    """
    match obj:
        case "user" if isinstance(values[0], dict) and isinstance(values[1], dict):
            return user_equivalent(values[0], values[1])
        case "user_full" if isinstance(values[0], dict) and isinstance(values[1], dict):
            return user_full_equivalent(values[0], values[1])
        case "post" if isinstance(values[0], dict) and isinstance(values[1], dict):
            return post_equivalent(values[0], values[1])
        case "comment" if isinstance(values[0], dict) and isinstance(values[1], dict):
            return comment_equivalent(values[0], values[1])
