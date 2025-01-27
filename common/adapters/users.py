"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3

Implementations of UserPort
"""

import hashlib
import time
import uuid
from typing import List

from common.models.errors import ObjectExistsError, ObjectNotFoundError
from common.models.database import Database
from common.models.users import User
from common.ports.users import UserPort
from common.utils.file import JSONFileMixin


class UserJSONFileAdapter(JSONFileMixin, UserPort):
    """
    Handler for JSON file database for Users.

    WARNING: This is only intended for local development.
    Do not use in production environments.
    """

    def __init__(self, **kwargs):
        self.initialize_database(
            data_dir=kwargs.get('datadir'),
            base_database_name=kwargs.get('databasefile'),
        )

    def _is_duplicate(
        self,
        existing_users: List[User],
        new_user: List[User],
    ) -> bool:
        return new_user in existing_users

    def _set_id(self, user: User):
        if not user.id:
            user.id = str(uuid.uuid4())

    def _set_password(self, user: User, password: str):
        # REMINDER: don't use this in production
        salt = str(time.monotonic())
        pswd_str = f'{salt}{password}'.encode('utf-8')
        phash = hashlib.sha256(pswd_str).hexdigest()
        user.password = f'{salt}${phash}'

    def create(self, user: User) -> User:
        """
        Create a new user in the database.

        :user: New User object to add to the database.
            User is counted as a duplicate when it has the same
            languageCode and baseUser.

        :return: Created User object.
        :raises: ObjectExistsError if the object already exists.
        """
        database = self.read_db()

        if self._is_duplicate(database.users, user):
            raise ObjectExistsError(
                f'User with {user.username} already exists')

        self._set_id(user)
        self._set_password(user, user.password or '')

        database.users.append(user)
        self.write_db()
        return user

    def create_in_batch(self, users: List[User]) -> List[User]:
        """
        Batch create multiple users.
        Ignores users that already exist.

        :user: New User object to add to the database.
            User is counted as a duplicate when it has the same username.

        :return: List of created users.
        """
        database = self.read_db()
        non_duplicates = list(set(users).difference(set(database.users)))
        if non_duplicates:
            for user in non_duplicates:
                self._set_id(user)
                self._set_password(user, user.password or '')
                database.users.append(user)
            self.write_db()
        return non_duplicates

    def read(self, username: str) -> User:
        """
        Read a single User from the database.

        :username: The username to search for.
            Username is expected to be unique.

        :return: The user that was found.
        :raises: ObjectNotFoundError if user doesn't exist
        """

        database = self.read_db()
        user_match = list(
            filter(
                lambda x: x.username == username,
                database.users,
            )
        )
        if not user_match:
            raise ObjectNotFoundError(f'No user with {username} found.')

        return user_match[0]
