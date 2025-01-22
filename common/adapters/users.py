"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3

Implementations of UserPort
"""

from typing import List

from common.models.errors import ObjectExistsError
from common.models.database import Database
from common.models.users import User
from common.ports.users import UserPort
from common.utils.file import DatabaseFileMixin, JSONFileMixin


class UserJSONFileAdapter(DatabaseFileMixin, JSONFileMixin, UserPort):
    """
    Handler for JSON file database for Users.

    WARNING: This is only intended for local development.
    Do not use in production environments.
    """

    def __init__(self, **kwargs):
        self.database = self._get_db_filename(
            kwargs['databasefile'],
            'json',
        )

    def _is_duplicate(
        self,
        existing_users: List[User],
        new_user: List[User],
    ) -> bool:
        return new_user in existing_users

    def create(self, user: User) -> User:
        """
        Create a new user in the database.

        WARNING: Please create a User object with `make_user`
        to set the password and id.

        :user: New User object to add to the database.
            User is counted as a duplicate when it has the same
            languageCode and baseUser.

        :return: Created User object.
        :raises: ObjectExistsError if the object already exists.
        """
        database = self._read_json()

        if self._is_duplicate(database.users, user):
            raise ObjectExistsError(
                f'User with {user.username} already exists')

        database.users.append(user)
        self._write_json(database)
        return user

    def create_in_batch(self, users: List[User]) -> List[User]:
        """
        Batch create multiple users.
        Ignores users that already exist.

        WARNING: Please create a User object with `make_user`
        to set the password and id.

        :user: New User object to add to the database.
            User is counted as a duplicate when it has the same username.

        :return: List of created users.
        """
        database = self._read_json()
        non_duplicates = list(set(users).difference(set(database.users)))
        if non_duplicates:
            database.users.extend(non_duplicates)
            self._write_json(database)
        return non_duplicates
