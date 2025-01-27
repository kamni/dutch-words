"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

import random
import string
import uuid

from common.models.user import UserDB
from tests.utils_for_test.random_data import (
    random_email,
    random_password,
    random_string,
)


def create_user_db(**kwargs) -> UserDB:
    """
    Create a UserDB object.
    Not written to database.

    :kwargs: arguments that will be passed to UserDB during creation.
    """

    username = random_string()
    random_data = {
        id: uuid.uuid4(),
        username: username
        password: random_password(),
        email: random_email(username=username),
        display_name: username.title(),
    }
    random_data.update(kwargs)

    user = UserDB(**random_data)
    return user
