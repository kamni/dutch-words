"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

import random
import string

from common.models.users import UserDB, UserUI

from .random_data import (
    random_email,
    random_password,
    random_string,
    random_uuid,
)


def make_user_db(**kwargs) -> UserDB:
    """
    Create a UserDB object.
    Not written to database.

    :kwargs: arguments that will be passed to UserDB during creation.
    """

    username = random_string()
    random_data = {
        'id': random_uuid(),
        'username': username,
        'password': random_password(),
        'email': random_email(username=username),
        'display_name': username.title(),
    }
    random_data.update(kwargs)

    user = UserDB(**random_data)
    return user


def make_user_ui(**kwargs) -> UserUI:
    """
    Create a UserUI object.
    Does not have a corresponding UserDB object.

    :kwargs: arguments that will be passed to UserUI during creation.
    """

    username = random_string()
    random_data = {
        'id': random_uuid(),
        'username': username,
        'displayName': username.title(),
    }
    random_data.update(kwargs)

    user = UserUI(**random_data)
    return user
